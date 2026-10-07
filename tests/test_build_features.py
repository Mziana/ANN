"""Unit tests for src.features.build_features.

Two behaviours matter most and are protected hardest: the session definition
must stay identical to the locked notebook copy (``session_fingerprint``), and
no feature may look ahead. The dedicated look-ahead test mutates the tail of the
input and asserts the past rows do not move while the affected rows do.

Everything here is synthetic and in memory: no network, no MT5, deterministic.
"""

from __future__ import annotations

import inspect

import numpy as np
import pandas as pd
import pytest

from src.features.build_features import (
    ATR_WINDOW,
    DAILY_COLUMNS,
    EXPECTED_SESSION_FINGERPRINT,
    FEATURE_COLUMNS,
    RV_WINDOW,
    SESSION_COLUMNS,
    build_features,
    daily_metrics,
    exclusive_session_label,
    load_processed,
    prepare_bars,
    require_columns,
    session_fingerprint,
    session_flags,
    write_features,
)

# 2024-01-01T00:00:00 UTC, also used as the broker midnight of day 0.
BASE = 1_704_067_200
SECONDS_PER_DAY = 86_400
M15_PER_DAY = 96
M1_PER_DAY = 1440
PIP_SIZE = 0.01
DAYS = 45
DAY = pd.Timedelta(days=1)


def _times(days: int, per_day: int, step: int) -> list[int]:
    return [BASE + day * SECONDS_PER_DAY + k * step for day in range(days) for k in range(per_day)]


def _utc_strings(epochs: list[int]) -> list[str]:
    return [ts.strftime("%Y-%m-%dT%H:%M:%S%z") for ts in pd.to_datetime(epochs, unit="s", utc=True)]


def make_bars(
    days: int = DAYS,
    per_day: int = M15_PER_DAY,
    step: int = 900,
    tail_from: int | None = None,
    tail_scale: float = 1.0,
) -> pd.DataFrame:
    """Build a synthetic processed-shape frame.

    Args:
        days: Number of contiguous broker days.
        per_day: Bars per day.
        step: Seconds between bars.
        tail_from: First day whose prices are scaled; None leaves them alone.
        tail_scale: Multiplier applied to the tail days' prices.

    Returns:
        Frame with time, broker_time_raw and consistent OHLC.
    """
    epochs = _times(days, per_day, step)
    closes = np.array([150.0 + 0.0004 * i for i in range(len(epochs))])
    if tail_from is not None:
        boundary = tail_from * per_day
        closes[boundary:] = closes[boundary:] * tail_scale
    opens = np.concatenate([[closes[0]], closes[:-1]])
    return pd.DataFrame(
        {
            "time": _utc_strings(epochs),
            "broker_time_raw": epochs,
            "open": opens.round(3),
            "high": (np.maximum(opens, closes) + 0.0005).round(3),
            "low": (np.minimum(opens, closes) - 0.0005).round(3),
            "close": closes.round(3),
        }
    )


def make_m15(**kwargs) -> pd.DataFrame:
    return make_bars(per_day=M15_PER_DAY, step=900, **kwargs)


def make_m1(**kwargs) -> pd.DataFrame:
    return make_bars(per_day=M1_PER_DAY, step=60, **kwargs)


class TestSessionFingerprint:
    def test_matches_locked_expected(self):
        assert session_fingerprint() == EXPECTED_SESSION_FINGERPRINT

    def test_is_non_empty_and_mentions_all_sessions(self):
        fingerprint = session_fingerprint()
        for label in ("Tokyo", "London", "New York", "Sydney"):
            assert label in fingerprint

    def test_encodes_priority_order(self):
        assert session_fingerprint().endswith("priority=London>NewYork>Tokyo>Sydney")


class TestSessionFlags:
    def test_london_flag_true_in_its_window(self):
        utc = pd.Series(pd.to_datetime(["2024-07-15T09:00:00Z"], utc=True))
        flags = session_flags(utc)
        assert bool(flags["is_london"].iloc[0])

    def test_flags_are_non_exclusive(self):
        # 13:00 UTC in summer is 14:00 London and 09:00 New York.
        utc = pd.Series(pd.to_datetime(["2024-07-15T13:00:00Z"], utc=True))
        flags = session_flags(utc)
        assert bool(flags["is_london"].iloc[0])
        assert bool(flags["is_ny"].iloc[0])

    def test_is_dst_aware(self):
        winter = session_flags(pd.Series(pd.to_datetime(["2024-01-15T07:00:00Z"], utc=True)))
        summer = session_flags(pd.Series(pd.to_datetime(["2024-07-15T07:00:00Z"], utc=True)))
        assert not bool(winter["is_london"].iloc[0])
        assert bool(summer["is_london"].iloc[0])

    def test_index_is_preserved(self):
        utc = pd.Series(pd.to_datetime(["2024-01-15T07:00:00Z", "2024-01-15T08:00:00Z"], utc=True))
        assert list(session_flags(utc).index) == [0, 1]


class TestExclusiveSessionLabel:
    def test_london_beats_newyork(self):
        flags = pd.DataFrame(
            {"is_london": [True], "is_ny": [True], "is_tokyo": [False], "is_sydney": [False]}
        )
        assert exclusive_session_label(flags).iloc[0] == "London"

    def test_off_when_no_flag(self):
        flags = pd.DataFrame(
            {"is_london": [False], "is_ny": [False], "is_tokyo": [False], "is_sydney": [False]}
        )
        assert exclusive_session_label(flags).iloc[0] == "Off"

    def test_sydney_when_alone(self):
        flags = pd.DataFrame(
            {"is_london": [False], "is_ny": [False], "is_tokyo": [False], "is_sydney": [True]}
        )
        assert exclusive_session_label(flags).iloc[0] == "Sydney"

    def test_name_is_session_label(self):
        flags = pd.DataFrame({column: [False] for column in SESSION_COLUMNS})
        assert exclusive_session_label(flags).name == "session_label"


class TestRequireColumns:
    def test_passes_when_all_present(self):
        require_columns(pd.DataFrame({"a": [1], "b": [2]}), ("a", "b"), "X")

    def test_raises_with_missing_listed(self):
        with pytest.raises(ValueError, match=r"\['b'\]"):
            require_columns(pd.DataFrame({"a": [1]}), ("a", "b"), "X")

    def test_error_names_the_source(self):
        with pytest.raises(ValueError, match="M15"):
            require_columns(pd.DataFrame({"a": [1]}), ("b",), "M15")


class TestPrepareBars:
    def test_adds_utc_wall_and_broker_day(self):
        out = prepare_bars(make_m15(), "M15", ("open", "high", "low", "close"))
        assert "utc" in out.columns and "wall" in out.columns and "broker_day" in out.columns
        assert str(out["utc"].dt.tz) == "UTC"
        assert out["broker_day"].iloc[0] == pd.Timestamp("2024-01-01")

    def test_sorts_by_broker_timestamp(self):
        frame = make_m15().iloc[::-1].reset_index(drop=True)
        out = prepare_bars(frame, "M15", ("close",))
        assert out["broker_time_raw"].is_monotonic_increasing

    def test_missing_column_raises(self):
        with pytest.raises(ValueError, match="close"):
            prepare_bars(make_m15().drop(columns=["close"]), "M15", ("close",))


class TestLoadProcessed:
    def _write(self, base, timeframe, year, frame):
        directory = base / timeframe
        directory.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(directory / f"usdjpy_{timeframe.lower()}_{year}.parquet", index=False)

    def test_stacks_years(self, tmp_path):
        self._write(tmp_path, "M15", 2024, make_m15())
        self._write(tmp_path, "M15", 2025, make_m15())
        out = load_processed("M15", "USDJPY", base=tmp_path)
        assert len(out) == 2 * DAYS * M15_PER_DAY

    def test_year_filter(self, tmp_path):
        self._write(tmp_path, "M15", 2024, make_m15())
        self._write(tmp_path, "M15", 2025, make_m15())
        out = load_processed("M15", "USDJPY", base=tmp_path, years=(2024,))
        assert len(out) == DAYS * M15_PER_DAY

    def test_missing_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_processed("M15", "USDJPY", base=tmp_path)


class TestDailyMetrics:
    def test_index_is_broker_days_and_columns_present(self):
        daily = daily_metrics(make_m1(), make_m15(), PIP_SIZE)
        assert len(daily) == DAYS
        for column in DAILY_COLUMNS:
            assert column in daily.columns
        assert daily.index[0] == pd.Timestamp("2024-01-01")

    def test_atr_is_nan_during_warmup_then_filled(self):
        daily = daily_metrics(make_m1(), make_m15(), PIP_SIZE)
        assert int(daily["atr_14_d1"].isna().sum()) == ATR_WINDOW
        assert daily["atr_14_d1"].iloc[ATR_WINDOW : ATR_WINDOW + 3].notna().all()

    def test_rv_roll_is_nan_until_full_window(self):
        daily = daily_metrics(make_m1(), make_m15(), PIP_SIZE)
        assert int(daily["rv_roll_20d"].isna().sum()) == RV_WINDOW - 1
        first_full = daily["rv_roll_20d"].iloc[RV_WINDOW - 1]
        expected = daily["rv_day"].iloc[0:RV_WINDOW].sum()
        assert first_full == pytest.approx(expected)

    def test_range_atr_equals_range_over_atr(self):
        daily = daily_metrics(make_m1(), make_m15(), PIP_SIZE)
        row = daily.iloc[20]
        assert row["range_atr"] == pytest.approx(row["range_pips"] / row["atr_14_d1"])

    def test_bad_pip_size_raises(self):
        with pytest.raises(ValueError, match="pip_size"):
            daily_metrics(make_m1(), make_m15(), 0.0)

    def test_imbalance_m1_m15_raises(self):
        """F-4 (2026-10-07): daily_metrics harus gagal berisik bila cakupan

        M1 dan M15 timpang (join inner kehilangan hari diam).

        Bukti auditor: potong M1 dari 974 hari jadi 145 hari sambil M15 penuh
        menghasilkan join 148 hari (974→148, 826 hari hilang tanpa peringatan
        sebelum assertion ditambahkan).
        """
        m1_short = make_m1(days=3)
        m15_long = make_m15(days=5)
        with pytest.raises(ValueError, match="join hilang"):
            daily_metrics(m1_short, m15_long, PIP_SIZE)

    def test_balanced_m1_m15_silent(self):
        """F-4 (2026-10-07): daily_metrics harus hijau bila M1 dan M15 sama.

        Ini mengunci assertion: pada data sekarang (974=974) assertion hijau
        tanpa mengubah output parquet.
        """
        m1 = make_m1(days=5)
        m15 = make_m15(days=5)
        result = daily_metrics(m1, m15, PIP_SIZE)
        assert len(result) == 5


class TestBuildFeatures:
    def test_shape_columns_and_index(self):
        features = build_features(make_m1(), make_m15(), PIP_SIZE)
        assert list(features.columns) == FEATURE_COLUMNS
        assert len(features) == DAYS * M15_PER_DAY
        assert features.index.name == "time"
        assert str(features.index.tz) == "UTC"

    def test_daily_features_use_previous_completed_day(self):
        m1, m15 = make_m1(), make_m15()
        daily = daily_metrics(m1, m15, PIP_SIZE)
        features = build_features(m1, m15, PIP_SIZE)
        day = daily.index[25]
        rows = features.loc[features["date_broker"] == day]
        for column in DAILY_COLUMNS:
            assert np.allclose(rows[column].to_numpy(), daily[column].iloc[24])

    def test_first_day_has_no_daily_features(self):
        features = build_features(make_m1(), make_m15(), PIP_SIZE)
        first = features.loc[features["date_broker"] == pd.Timestamp("2024-01-01")]
        assert first["atr_14_d1"].isna().all()

    def test_session_label_matches_flags(self):
        features = build_features(make_m1(), make_m15(), PIP_SIZE)
        assert bool(features["session_label"].eq("London").any())
        labelled_london = features["session_label"].eq("London")
        assert features.loc[labelled_london, "is_london"].all()

    def test_m5_is_not_an_input(self):
        """B1-2: no column derives from M5; H2 reads the M5 parquet directly."""
        assert "m5" not in inspect.signature(build_features).parameters

    def test_no_lookahead_tail_mutation(self):
        """Mutating the tail must not move any earlier row, but must move later ones."""
        tail_from = DAYS - 6
        features = build_features(make_m1(), make_m15(), PIP_SIZE)
        mutated = build_features(
            make_m1(tail_from=tail_from, tail_scale=3.0),
            make_m15(tail_from=tail_from, tail_scale=3.0),
            PIP_SIZE,
        )
        cut = pd.Timestamp("2024-01-01") + (tail_from - 1) * DAY
        past_full = features.loc[features["date_broker"] <= cut]
        past_mut = mutated.loc[mutated["date_broker"] <= cut]
        pd.testing.assert_frame_equal(past_full, past_mut)

        affected = pd.Timestamp("2024-01-01") + (tail_from + 1) * DAY
        delta = (mutated.loc[mutated["date_broker"] == affected, "rv_roll_20d"]).to_numpy()
        baseline = features.loc[features["date_broker"] == affected, "rv_roll_20d"].to_numpy()
        assert not np.allclose(delta, baseline)

    def test_f2_m1_bars_not_in_feature_columns(self):
        """F-2 (2026-10-07): m1_bars ada di data M15 terproses tapi tidak

        masuk FEATURE_COLUMNS. Ini bukan defect — B1-1 memang tidak memasukkan
        kolom spread/cost ke store, dan m1_bars adalah atribut bucket bukan fitur.

        Efek terukur: menghapus bar M1 bermasalah lalu hitung ulang menghasilkan
        median ratio_path +0.019%, p95 +0.28%, maks +1.06% (audit fondasi B1,
        597 bucket mid-day). range_atr 0.000% karena OHLC D1 berasal dari M15,
        tidak terpengaruh.

        Konsumen B2-H1 (tipologi) dan B2-H5 (kuartil ATR) BELUM DIUJI di batch
        ini — klaim "tak terpengaruh material" di sini hanya catatan audit, bukan
        bukti uji. Efeknya kecil sehingga LOW, bukan MEDIUM.
        """
        assert "m1_bars" not in FEATURE_COLUMNS


class TestWriteFeatures:
    def test_writes_readable_parquet(self, tmp_path):
        features = build_features(make_m1(), make_m15(), PIP_SIZE)
        path = write_features(features, tmp_path / "out" / "features.parquet")
        assert path.is_file()
        loaded = pd.read_parquet(path)
        assert list(loaded.columns) == FEATURE_COLUMNS
        assert len(loaded) == len(features)

    def test_creates_missing_parent_directory(self, tmp_path):
        features = build_features(make_m1(), make_m15(), PIP_SIZE)
        path = write_features(features, tmp_path / "deep" / "nested" / "features.parquet")
        assert path.parent.is_dir()

    def test_index_round_trips_as_utc(self, tmp_path):
        features = build_features(make_m1(), make_m15(), PIP_SIZE)
        path = write_features(features, tmp_path / "features.parquet")
        loaded = pd.read_parquet(path)
        assert str(loaded.index.tz) == "UTC"
        assert loaded.index.equals(features.index)
