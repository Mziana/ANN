"""Unit tests for src.data.fetch_data and src.utils.config.

No test in this file touches the MT5 API. Every test builds its own data so
the suite stays deterministic and fast (RULES.md section 11).
"""

from __future__ import annotations

import importlib
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import pytest

from src.data import fetch_data as fetch_data_module
from src.data.fetch_data import (
    TIMEFRAME_NAMES,
    broker_epoch_to_utc,
    build_filename,
    import_mt5,
    rates_to_frame,
    split_by_year,
    spread_points_to_pips,
    timeframe_constant,
    write_csv,
)
from src.utils.config import ConfigError, load_config

BROKER_TZ = ZoneInfo("Etc/GMT-3")
POINT = 0.001
PIP_SIZE = 0.01

RATES_DTYPE = [
    ("time", "<i8"),
    ("open", "<f8"),
    ("high", "<f8"),
    ("low", "<f8"),
    ("close", "<f8"),
    ("tick_volume", "<u8"),
    ("spread", "<i4"),
    ("real_volume", "<u8"),
]


def make_rates(epochs: list[int], spread: int = 6) -> np.ndarray:
    """Build a structured array shaped like MT5's copy_rates output.

    Args:
        epochs: Broker epoch seconds, one per row.
        spread: Spread in points, identical for every row.

    Returns:
        Structured numpy array with MT5's column layout.
    """
    rows = [(epoch, 159.700, 159.750, 159.690, 159.740, 120, spread, 0) for epoch in epochs]
    return np.array(rows, dtype=RATES_DTYPE)


class TestBrokerEpochToUtc:
    def test_converts_broker_time_to_utc(self):
        """A broker epoch on UTC+3 lands three hours earlier in UTC."""
        utc = broker_epoch_to_utc(1788224460, BROKER_TZ)
        assert utc.tzinfo is not None
        assert utc.utcoffset().total_seconds() == 0

    def test_offset_is_exactly_three_hours(self):
        """MT5 encodes the broker wall clock, so the UTC instant is 3h earlier.

        The broker digits are recovered by reading the epoch as if it were UTC,
        which is exactly what MT5 meant when it wrote them.
        """
        epoch = 1788224460
        broker_wall = datetime.fromtimestamp(epoch, tz=UTC).replace(tzinfo=None)
        utc_wall = broker_epoch_to_utc(epoch, BROKER_TZ).replace(tzinfo=None)
        assert broker_wall - utc_wall == timedelta(hours=3)

    def test_epoch_shifts_back_by_the_broker_offset(self):
        """Converting must move the instant back by the offset, not preserve it.

        The previous implementation was a no-op, which stored every bar three
        hours ahead of real UTC. This test pins the corrected direction.
        """
        epoch = 1788224460
        assert broker_epoch_to_utc(epoch, BROKER_TZ).timestamp() == epoch - 10800

    def test_matches_measured_evidence(self):
        """The exact bar audited on 2026-10-05 must land on real UTC.

        ``symbol_info_tick().time`` was measured at 1791205620 while an
        independent internet clock read 10:07 UTC, so the corrected conversion
        has to reproduce 10:07:00. If this ever flips back to 13:07 the stored
        data is three hours ahead again.
        """
        assert broker_epoch_to_utc(1791205620, BROKER_TZ).isoformat() == "2026-10-05T10:07:00+00:00"

    def test_epoch_zero_maps_to_known_instant(self):
        """Epoch 0 is a stable reference point for regression tests.

        Zero on the broker clock is 21:00 UTC on 1969-12-31, because the epoch
        carries a wall clock rather than an instant.
        """
        assert broker_epoch_to_utc(0, BROKER_TZ).isoformat() == "1969-12-31T21:00:00+00:00"


class TestSpreadPointsToPips:
    def test_converts_points_to_pips(self):
        """6 points on USDJPY is 0.6 pip, not 6 pips."""
        assert spread_points_to_pips(6, POINT, PIP_SIZE) == pytest.approx(0.6)

    def test_zero_spread_maps_to_zero_pips(self):
        assert spread_points_to_pips(0, POINT, PIP_SIZE) == 0.0

    def test_rejects_non_positive_point(self):
        with pytest.raises(ValueError, match="positive"):
            spread_points_to_pips(6, 0.0, PIP_SIZE)

    def test_rejects_non_positive_pip_size(self):
        with pytest.raises(ValueError, match="positive"):
            spread_points_to_pips(6, POINT, 0.0)


class TestRatesToFrame:
    def test_keeps_broker_epoch_and_adds_utc(self):
        """Both the raw broker epoch and the corrected UTC timestamp must survive."""
        rates = make_rates([1788224460])
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        assert frame.loc[0, "broker_time_raw"] == 1788224460
        assert frame.loc[0, "time"] == "2026-08-31T22:01:00+0000"

    def test_column_order_is_stable(self):
        rates = make_rates([1788224460, 1788224520])
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        expected = [
            "time",
            "broker_time_raw",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "real_volume",
            "spread_points",
            "spread_pips",
        ]
        assert list(frame.columns) == expected

    def test_spread_columns_agree(self):
        rates = make_rates([1788224460], spread=6)
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        assert frame.loc[0, "spread_points"] == 6
        assert frame.loc[0, "spread_pips"] == pytest.approx(0.6)

    def test_ohlc_pass_through_unchanged(self):
        """OHLC is bid data from MT5; this module must not alter it."""
        rates = make_rates([1788224460])
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        assert frame.loc[0, "open"] == 159.700
        assert frame.loc[0, "high"] == 159.750
        assert frame.loc[0, "low"] == 159.690
        assert frame.loc[0, "close"] == 159.740

    def test_sorts_by_broker_epoch(self):
        rates = make_rates([1788224520, 1788224400])
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        assert frame["broker_time_raw"].tolist() == [1788224400, 1788224520]


class TestBuildFilename:
    def test_uses_config_pattern(self):
        pattern = "{symbol}_{tf}_{year}.{format}"
        assert build_filename("USDJPY", "M1", "2026", pattern) == "usdjpy_m1_2026.csv"

    def test_lowercases_symbol_and_timeframe(self):
        pattern = "{symbol}_{tf}_{year}.{format}"
        assert build_filename("UsdJpy", "M15", "2023", pattern) == "usdjpy_m15_2023.csv"


class TestSplitByYear:
    def test_writes_one_file_per_year(self, tmp_path):
        """The file year follows the UTC timestamp, not the broker wall clock.

        Midnight on the broker clock is 21:00 UTC the previous day, so these two
        broker midnights belong to the previous calendar year in real UTC.
        """
        rates = make_rates([1704067200, 1735689600])
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        pattern = "{symbol}_{tf}_{year}.{format}"
        written = split_by_year(frame, tmp_path, pattern, "USDJPY", "M1")
        assert [p.name for p in written] == ["usdjpy_m1_2023.csv", "usdjpy_m1_2024.csv"]

    def test_bar_near_new_year_lands_in_its_utc_year(self, tmp_path):
        """A 02:00 broker bar on 1 January is still December in UTC."""
        rates = make_rates([1735696800])  # 2025-01-01 02:00:00 on the broker clock
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        assert frame.loc[0, "time"] == "2024-12-31T23:00:00+0000"
        written = split_by_year(frame, tmp_path, "{symbol}_{tf}_{year}.{format}", "USDJPY", "M1")
        assert [p.name for p in written] == ["usdjpy_m1_2024.csv"]

    def test_raises_on_empty_frame(self, tmp_path):
        empty = pd.DataFrame(columns=["time", "broker_time_raw"])
        with pytest.raises(ValueError, match="empty"):
            split_by_year(empty, tmp_path, "{symbol}_{tf}_{year}.{format}", "USDJPY", "M1")


class TestWriteCsv:
    def test_creates_parent_directories(self, tmp_path):
        target = tmp_path / "nested" / "deeper" / "out.csv"
        write_csv(pd.DataFrame({"a": [1]}), target)
        assert target.is_file()

    def test_writes_without_index(self, tmp_path):
        target = tmp_path / "out.csv"
        write_csv(pd.DataFrame({"a": [1, 2]}), target)
        assert target.read_text(encoding="utf-8").splitlines()[0] == "a"


class TestLoadConfig:
    def test_loads_data_config(self):
        config = load_config("data")
        assert config["mt5"]["symbol"] == "USDJPY"
        assert config["mt5"]["broker_timezone"] == "Etc/GMT-3"

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(ConfigError, match="Config not found"):
            load_config("tidak_ada", config_dir=tmp_path)

    def test_non_mapping_raises(self, tmp_path):
        (tmp_path / "scalar.yaml").write_text("- just\n- a\n- list\n", encoding="utf-8")
        with pytest.raises(ConfigError, match="mapping"):
            load_config("scalar", config_dir=tmp_path)


class MetaTrader5Blocker:
    """Context manager that makes importing MetaTrader5 fail.

    MetaTrader5 only exists on Windows, so the module must stay importable on a
    machine that cannot load it. Blocking the import is how these tests prove
    that without needing a second environment.
    """

    class _Finder:
        """Meta path finder that refuses to load MetaTrader5."""

        def find_module(self, name: str, path: object = None) -> object:
            """Return self for MetaTrader5 only.

            Args:
                name: Module name being imported.
                path: Search path, unused.

            Returns:
                This finder when the name is blocked, otherwise None.
            """
            return self if name == "MetaTrader5" else None

        def load_module(self, name: str) -> object:
            """Reject the import.

            Args:
                name: Module name being imported.

            Raises:
                ImportError: Always, because the package is unavailable.
            """
            raise ImportError("MetaTrader5 blocked for test")

    def __enter__(self) -> MetaTrader5Blocker:
        """Install the blocking finder.

        Returns:
            This blocker.
        """
        self._finder = self._Finder()
        sys.meta_path.insert(0, self._finder)
        return self

    def __exit__(self, *exc_info: object) -> bool:
        """Remove the blocking finder.

        Args:
            *exc_info: Unused exception triple from the with block.

        Returns:
            False so exceptions are never suppressed.
        """
        if self._finder in sys.meta_path:
            sys.meta_path.remove(self._finder)
        return False


class TestLazyMt5Import:
    """MetaTrader5 is Windows-only, so it must not be imported at module level."""

    def test_no_top_level_mt5_import_in_source(self):
        source = Path(fetch_data_module.__file__).read_text(encoding="utf-8")
        top_level = [line for line in source.splitlines() if line.startswith("import MetaTrader5")]
        assert top_level == []

    def test_mt5_absent_still_allows_pure_helpers(self):
        """Every non-network helper must work with MetaTrader5 unimportable."""
        with MetaTrader5Blocker():
            for name in list(sys.modules):
                if name.startswith("src.data.fetch_data"):
                    del sys.modules[name]
            module = importlib.import_module("src.data.fetch_data")
            name = module.build_filename("USDJPY", "M1", "2026", "{symbol}_{tf}_{year}.{format}")
            assert name == "usdjpy_m1_2026.csv"
            assert module.spread_points_to_pips(6, 0.001, 0.01) == pytest.approx(0.6)

    def test_mt5_absent_still_allows_validate_data(self):
        """validate_data imports fetch_data only for its path helpers."""
        with MetaTrader5Blocker():
            for name in list(sys.modules):
                if name.startswith(("src.data.fetch_data", "src.data.validate_data")):
                    del sys.modules[name]
            module = importlib.import_module("src.data.validate_data")
            assert callable(module.check_bar_count)

    def test_timeframe_constant_rejects_unknown_name(self):
        with pytest.raises(ValueError, match="Unknown timeframe"):
            timeframe_constant("M99")

    def test_timeframe_names_cover_config(self):
        config = load_config("data")
        assert set(config["mt5"]["timeframes"]) == set(TIMEFRAME_NAMES)

    def test_import_mt5_is_callable(self):
        assert callable(import_mt5)
