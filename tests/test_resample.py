"""Unit tests for src.data.resample.

The three behaviours worth protecting are the approved design decisions:
buckets follow the broker wall clock and are labelled with their start (D2),
spread is aggregated as mean plus max (D3), and empty buckets never appear while
every real bar stays counted in ``m1_bars`` (D4).
"""

from __future__ import annotations

from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import pytest

from src.data.resample import (
    BUCKET_COLUMN,
    OUTPUT_COLUMNS,
    TIMEFRAME_MINUTES,
    ResampleResult,
    aggregate_buckets,
    broker_bucket_start,
    discover_cleaned,
    finalise,
    resample_frame,
    resample_year,
)

BROKER_TZ = ZoneInfo("Etc/GMT-3")
# Exactly midnight broker time (UTC+3), so bars start on a bucket boundary for
# every timeframe including D1. 1700006400 is divisible by 86400.
BASE = 1_700_006_400


def make_minutes(count: int, start: int = BASE, spread: float = 1.0, tick: int = 1) -> pd.DataFrame:
    """Build a contiguous run of one-minute bars.

    Args:
        count: How many bars to emit.
        start: Epoch seconds of the first bar.
        spread: Spread in pips on every bar.
        tick: Tick volume on every bar.

    Returns:
        Cleaned-shape M1 frame with all columns the resampler reads.
    """
    epochs = [start + i * 60 for i in range(count)]
    return pd.DataFrame(
        {
            "broker_time_raw": epochs,
            "time": ["2026-01-01T00:00:00+0000"] * count,
            "open": [1.0 + i * 0.01 for i in range(count)],
            "high": [2.0 + i * 0.01 for i in range(count)],
            "low": [0.5 + i * 0.01 for i in range(count)],
            "close": [1.5 + i * 0.01 for i in range(count)],
            "tick_volume": [tick] * count,
            "real_volume": [0] * count,
            "spread_points": [10] * count,
            "spread_pips": [spread] * count,
        }
    )


class TestBrokerBucketStart:
    def test_floors_to_bucket_start(self):
        frame = make_minutes(12)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        first = buckets.iloc[0]
        assert first == first.floor("5min")

    def test_label_is_interval_start(self):
        """D2: every row is labelled with the start of its interval."""
        frame = make_minutes(10)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        assert buckets.iloc[4] == buckets.iloc[0]
        assert buckets.iloc[5] != buckets.iloc[0]

    def test_uses_broker_not_utc_for_daily(self):
        """D2: the broker day starts at 04:00 server time, not midnight."""
        frame = make_minutes(1, start=BASE)
        buckets = broker_bucket_start(frame, TIMEFRAME_MINUTES["D1"], BROKER_TZ)
        assert buckets.iloc[0].hour == buckets.iloc[0].floor("D").hour

    def test_count_is_preserved(self):
        frame = make_minutes(7)
        assert len(broker_bucket_start(frame, 5, BROKER_TZ)) == 7


class TestAggregateBuckets:
    def test_ohlc_uses_first_max_min_last(self):
        frame = make_minutes(5)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = aggregate_buckets(frame, buckets)
        assert out.loc[0, "open"] == pytest.approx(frame["open"].iloc[0])
        assert out.loc[0, "high"] == pytest.approx(frame["high"].max())
        assert out.loc[0, "low"] == pytest.approx(frame["low"].min())
        assert out.loc[0, "close"] == pytest.approx(frame["close"].iloc[-1])

    def test_volume_is_summed(self):
        frame = make_minutes(5, tick=7)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = aggregate_buckets(frame, buckets)
        assert out.loc[0, "tick_volume"] == 35

    def test_spread_mean_and_max(self):
        """D3: both the typical cost and the tail must survive."""
        frame = make_minutes(5)
        frame.loc[2, "spread_pips"] = 9.0
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = aggregate_buckets(frame, buckets)
        assert out.loc[0, "spread_pips_max"] == pytest.approx(9.0)
        assert out.loc[0, "spread_pips_mean"] < 9.0

    def test_m1_bars_counts_real_bars(self):
        """D4: the bar count is preserved so short buckets stay visible."""
        frame = make_minutes(7)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = aggregate_buckets(frame, buckets)
        assert out["m1_bars"].tolist() == [5, 2]

    def test_bucket_column_named(self):
        frame = make_minutes(5)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = aggregate_buckets(frame, buckets)
        assert BUCKET_COLUMN in out.columns


class TestFinalise:
    def test_output_column_order(self):
        frame = make_minutes(5)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = finalise(aggregate_buckets(frame, buckets), 3)
        assert list(out.columns) == OUTPUT_COLUMNS

    def test_epoch_is_bucket_start_in_seconds(self):
        """The epoch column must be real seconds, not nanoseconds or 1."""
        frame = make_minutes(5)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = finalise(aggregate_buckets(frame, buckets), 3)
        epoch = int(out["broker_time_raw"].iloc[0])
        assert epoch > 1_000_000_000
        assert epoch % 60 == 0

    def test_time_matches_epoch(self):
        frame = make_minutes(5)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = finalise(aggregate_buckets(frame, buckets), 3)
        parsed = pd.to_datetime(out["time"].iloc[0], format="%Y-%m-%dT%H:%M:%S%z", utc=True)
        assert int(parsed.timestamp()) == int(out["broker_time_raw"].iloc[0])

    def test_prices_rounded_to_digits(self):
        frame = make_minutes(5)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = finalise(aggregate_buckets(frame, buckets), 2)
        assert (out["close"] - out["close"].round(2)).abs().max() < 1e-9

    def test_bucket_column_dropped(self):
        frame = make_minutes(5)
        buckets = broker_bucket_start(frame, 5, BROKER_TZ)
        out = finalise(aggregate_buckets(frame, buckets), 3)
        assert BUCKET_COLUMN not in out.columns


class TestResampleFrame:
    def test_empty_buckets_are_dropped(self):
        """D4: a gap leaves no empty row behind."""
        frame = pd.concat([make_minutes(5), make_minutes(5, start=BASE + 7200)])
        out, _ = resample_frame(frame, "M5", BROKER_TZ, 3)
        assert len(out) == 2

    def test_short_bucket_is_reported(self):
        """D4: a bucket with fewer bars still exists and says so."""
        frame = pd.concat([make_minutes(5), make_minutes(2, start=BASE + 300)])
        out, result = resample_frame(frame, "M5", BROKER_TZ, 3)
        assert out["m1_bars"].tolist() == [5, 2]
        assert result.shortest_bucket == 2
        assert not result.complete

    def test_total_m1_bars_conserved(self):
        """Every input bar lands in exactly one bucket."""
        frame = make_minutes(37)
        _, result = resample_frame(frame, "M5", BROKER_TZ, 3)
        assert result.m1_bars == 37

    def test_unknown_timeframe_raises(self):
        with pytest.raises(ValueError, match="Unknown timeframe"):
            resample_frame(make_minutes(5), "M99", BROKER_TZ, 3)

    def test_empty_frame_raises(self):
        with pytest.raises(ValueError, match="empty"):
            resample_frame(make_minutes(0), "M5", BROKER_TZ, 3)

    def test_broken_weekend_gap_survives(self):
        """A 49 hour hole must not be bridged by synthetic buckets."""
        frame = pd.concat([make_minutes(5), make_minutes(5, start=BASE + 49 * 3600)])
        out, _ = resample_frame(frame, "H1", BROKER_TZ, 3)
        assert len(out) == 2


class TestResampleYear:
    def test_writes_parquet(self, tmp_path):
        source = tmp_path / "usdjpy_m1_2026.parquet"
        make_minutes(30).to_parquet(source, index=False)
        out = tmp_path / "M5"
        result = resample_year(
            source, out, "M5", "USDJPY", "{symbol}_{tf}_{year}.{format}", BROKER_TZ, 3
        )
        assert result.year == "2026"
        assert (out / "usdjpy_m1_2026.parquet".replace("m1", "m5")).is_file()

    def test_missing_source_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            resample_year(
                tmp_path / "nope.parquet",
                tmp_path / "M5",
                "M5",
                "USDJPY",
                "{symbol}_{tf}_{year}.{format}",
                BROKER_TZ,
                3,
            )


class TestDiscoverCleaned:
    def test_returns_only_parquet(self, tmp_path):
        directory = tmp_path / "M1"
        directory.mkdir()
        (directory / "usdjpy_m1_2025.parquet").write_bytes(b"x")
        (directory / "usdjpy_m1_2026.parquet").write_bytes(b"x")
        (directory / "notes.txt").write_text("skip", encoding="utf-8")
        found = discover_cleaned("USDJPY", "M1", "{}", tmp_path)
        assert [p.name for p in found] == [
            "usdjpy_m1_2025.parquet",
            "usdjpy_m1_2026.parquet",
        ]

    def test_empty_dir_returns_empty(self, tmp_path):
        assert discover_cleaned("USDJPY", "M1", "{}", tmp_path) == []


class TestResampleResult:
    def test_complete_when_all_buckets_full(self):
        result = ResampleResult("2026", "M5", 10, 50, 5, 5)
        assert result.complete
        assert result.expected == 5

    def test_incomplete_when_a_bucket_is_short(self):
        result = ResampleResult("2026", "M15", 10, 140, 4, 15)
        assert not result.complete


class TestTimeframeTable:
    def test_covers_configured_timeframes(self):
        from src.utils.config import load_config

        config = load_config("data")
        assert set(config["mt5"]["timeframes"]) - {"M1"} == set(TIMEFRAME_MINUTES)

    def test_source_module_not_missing(self):
        assert Path("src/data/resample.py").is_file()
