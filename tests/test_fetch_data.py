"""Unit tests for src.data.fetch_data and src.utils.config.

No test in this file touches the MT5 API. Every test builds its own data so
the suite stays deterministic and fast (RULES.md section 11).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import pytest

from src.data.fetch_data import (
    broker_epoch_to_utc,
    build_filename,
    rates_to_frame,
    split_by_year,
    spread_points_to_pips,
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
        """Broker wall clock reads 3h ahead of UTC.

        Note: the epoch itself is preserved by design, so the offset only
        shows up when comparing the broker wall clock with the UTC one.
        """
        epoch = 1788224460
        broker_wall = datetime.fromtimestamp(epoch, tz=BROKER_TZ)
        utc_wall = broker_epoch_to_utc(epoch, BROKER_TZ)
        assert (broker_wall.replace(tzinfo=None) - utc_wall.replace(tzinfo=None)) == timedelta(
            hours=3
        )

    def test_epoch_is_preserved(self):
        """Converting must not shift the instant, only its representation."""
        epoch = 1788224460
        assert broker_epoch_to_utc(epoch, BROKER_TZ).timestamp() == epoch

    def test_epoch_zero_maps_to_known_instant(self):
        """Epoch 0 is a stable reference point for regression tests."""
        assert broker_epoch_to_utc(0, BROKER_TZ).isoformat() == "1970-01-01T00:00:00+00:00"


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
        """Both the raw broker epoch and the UTC timestamp must survive."""
        rates = make_rates([1788224460])
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        assert frame.loc[0, "broker_time_raw"] == 1788224460
        assert frame.loc[0, "time"] == "2026-09-01T01:01:00+0000"

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
        rates = make_rates([1704067200, 1735689600])
        frame = rates_to_frame(rates, BROKER_TZ, POINT, PIP_SIZE)
        pattern = "{symbol}_{tf}_{year}.{format}"
        written = split_by_year(frame, tmp_path, pattern, "USDJPY", "M1")
        assert [p.name for p in written] == ["usdjpy_m1_2024.csv", "usdjpy_m1_2025.csv"]

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
