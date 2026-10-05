"""Unit tests for src.data.clean_data.

The single most important behaviour here is what the module refuses to do:
the daily break and the weekend gap must survive cleaning untouched.
"""

from __future__ import annotations

import pandas as pd
import pytest

from src.data.clean_data import (
    FILLED_COLUMN,
    MAX_FILL_GAP_MINUTES,
    TIME_COLUMN,
    CleanResult,
    clean_frame,
    clean_year,
    deduplicate,
    discover_raw,
    fill_small_gaps,
    load_raw,
    normalize_ohlc,
    sort_by_time,
)

BASE = 1_700_000_000


def make_raw(epochs: list[int], spread: float = 0.6) -> pd.DataFrame:
    """Build a raw-shaped frame.

    Args:
        epochs: Broker epoch seconds, one per row.
        spread: Spread in pips for every row.

    Returns:
        Frame with the same columns fetch_data writes.
    """
    return pd.DataFrame(
        {
            TIME_COLUMN: epochs,
            "time": ["2026-01-01T00:00:00+0000"] * len(epochs),
            "open": [1.0] * len(epochs),
            "high": [1.1] * len(epochs),
            "low": [0.9] * len(epochs),
            "close": [1.0] * len(epochs),
            "tick_volume": [100] * len(epochs),
            "real_volume": [0] * len(epochs),
            "spread_points": [6] * len(epochs),
            "spread_pips": [spread] * len(epochs),
        }
    )


def consecutive(count: int, start: int = BASE) -> list[int]:
    """Return consecutive one-minute epochs."""
    return [start + i * 60 for i in range(count)]


class TestLoadRaw:
    def test_keeps_canonical_column_order(self, tmp_path):
        path = tmp_path / "usdjpy_m1_2026.csv"
        make_raw(consecutive(3)).to_csv(path, index=False)
        frame = load_raw(path)
        assert list(frame.columns)[0] == "time"
        assert "broker_time_raw" in frame.columns

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_raw(tmp_path / "nope.csv")


class TestDeduplicate:
    def test_clean_frame_unchanged(self):
        frame = make_raw(consecutive(5))
        cleaned, removed = deduplicate(frame)
        assert removed == 0
        assert len(cleaned) == 5

    def test_duplicates_removed(self):
        epochs = consecutive(3) + [BASE]
        cleaned, removed = deduplicate(make_raw(epochs))
        assert removed == 1
        assert len(cleaned) == 3

    def test_keeps_first_occurrence(self):
        epochs = consecutive(3) + [BASE]
        cleaned, _ = deduplicate(make_raw(epochs))
        assert cleaned[TIME_COLUMN].tolist() == consecutive(3)


class TestSortByTime:
    def test_sorts_ascending(self):
        frame = make_raw([BASE + 120, BASE, BASE + 60])
        assert sort_by_time(frame)[TIME_COLUMN].tolist() == consecutive(3)

    def test_resets_index(self):
        frame = make_raw([BASE + 120, BASE])
        assert sort_by_time(frame).index.tolist() == [0, 1]


class TestNormalizeOhlc:
    def test_valid_ohlc_unchanged(self):
        frame = make_raw(consecutive(3))
        cleaned, changed = normalize_ohlc(frame, 3)
        assert changed == 0
        assert cleaned["high"].tolist() == [1.1, 1.1, 1.1]

    def test_high_below_close_is_repaired(self):
        frame = make_raw(consecutive(1))
        frame.loc[0, "high"] = 0.5
        cleaned, changed = normalize_ohlc(frame, 3)
        assert changed == 1
        assert cleaned.loc[0, "high"] == 1.0

    def test_low_above_open_is_repaired(self):
        frame = make_raw(consecutive(1))
        frame.loc[0, "low"] = 5.0
        cleaned, changed = normalize_ohlc(frame, 3)
        assert changed == 1
        assert cleaned.loc[0, "low"] == 1.0

    def test_rounds_to_digits(self):
        frame = make_raw(consecutive(1))
        frame.loc[0, "close"] = 1.00049
        cleaned, _ = normalize_ohlc(frame, 3)
        assert cleaned.loc[0, "close"] == pytest.approx(1.0)

    def test_does_not_mutate_input(self):
        frame = make_raw(consecutive(1))
        frame.loc[0, "high"] = 0.5
        normalize_ohlc(frame, 3)
        assert frame.loc[0, "high"] == 0.5


class TestFillSmallGaps:
    def test_short_gap_is_filled(self):
        frame = make_raw([BASE, BASE + 60 * 4])
        filled, count = fill_small_gaps(frame, max_minutes=20)
        assert count == 3
        assert len(filled) == 5

    def test_daily_break_is_not_filled(self):
        """The 61 minute break must never be filled with synthetic bars."""
        frame = make_raw([BASE, BASE + 61 * 60])
        filled, count = fill_small_gaps(frame, max_minutes=MAX_FILL_GAP_MINUTES)
        assert count == 0
        assert len(filled) == 2

    def test_weekend_gap_is_not_filled(self):
        frame = make_raw([BASE, BASE + 2880 * 60])
        filled, count = fill_small_gaps(frame, max_minutes=MAX_FILL_GAP_MINUTES)
        assert count == 0
        assert len(filled) == 2

    def test_contiguous_data_unchanged(self):
        frame = make_raw(consecutive(20))
        filled, count = fill_small_gaps(frame)
        assert count == 0
        assert len(filled) == 20

    def test_filled_rows_carry_forwarded_prices(self):
        frame = make_raw([BASE, BASE + 60 * 4])
        frame.loc[0, "close"] = 9.99
        filled, _ = fill_small_gaps(frame, max_minutes=20)
        assert filled.loc[filled[TIME_COLUMN] == BASE + 120, "close"].iloc[0] == 9.99

    def test_epoch_values_are_real_seconds(self):
        """Guard for datetime resolution: asi8 counts ns only after as_unit('ns').

        pandas 3.x builds a datetime64[s] index from unit='s', so a bare .asi8
        would collapse every epoch to 1 and still pass a flag-only assertion.
        """
        frame = make_raw([BASE, BASE + 60 * 4])
        filled, _ = fill_small_gaps(frame, max_minutes=20)
        assert filled[TIME_COLUMN].tolist() == consecutive(5)

    def test_filled_rows_are_flagged(self):
        frame = make_raw([BASE, BASE + 60 * 4])
        filled, _ = fill_small_gaps(frame, max_minutes=20)
        assert filled[FILLED_COLUMN].sum() == 3

    def test_real_rows_are_not_flagged(self):
        frame = make_raw(consecutive(20))
        filled, _ = fill_small_gaps(frame)
        assert not filled[FILLED_COLUMN].any()

    def test_dropped_break_rows_are_not_flagged_as_filled(self):
        """A break row is deleted, never emitted as a synthetic bar."""
        frame = make_raw([BASE, BASE + 61 * 60])
        filled, _ = fill_small_gaps(frame, max_minutes=MAX_FILL_GAP_MINUTES)
        assert not filled[FILLED_COLUMN].any()

    def test_time_column_matches_epoch(self):
        """The rebuilt time string must agree with the broker epoch."""
        frame = make_raw([BASE, BASE + 60 * 4])
        filled, _ = fill_small_gaps(frame, max_minutes=20)
        rebuilt = pd.to_datetime(filled["time"], format="%Y-%m-%dT%H:%M:%S%z", utc=True)
        expected = pd.to_datetime(filled[TIME_COLUMN], unit="s", utc=True)
        assert rebuilt.tolist() == expected.tolist()

    def test_does_not_mutate_input(self):
        frame = make_raw([BASE, BASE + 60 * 4])
        before = frame.copy()
        fill_small_gaps(frame, max_minutes=20)
        pd.testing.assert_frame_equal(frame, before)


class TestCleanFrame:
    def test_returns_result_with_counts(self):
        frame = make_raw(consecutive(10))
        cleaned, result = clean_frame(frame, 3)
        assert isinstance(result, CleanResult)
        assert result.rows_in == 10
        assert result.rows_out == len(cleaned)
        assert not result.changed

    def test_counts_duplicates(self):
        frame = make_raw(consecutive(3) + [BASE])
        _, result = clean_frame(frame, 3)
        assert result.duplicates_removed == 1
        assert result.changed

    def test_sorts_unsorted_input(self):
        frame = make_raw([BASE + 120, BASE, BASE + 60])
        cleaned, _ = clean_frame(frame, 3)
        assert cleaned[TIME_COLUMN].is_monotonic_increasing


class TestCleanYear:
    def test_writes_parquet(self, tmp_path):
        raw = tmp_path / "raw"
        raw.mkdir()
        make_raw(consecutive(30)).to_csv(raw / "usdjpy_m1_2026.csv", index=False)
        out = tmp_path / "processed"
        result = clean_year(
            raw / "usdjpy_m1_2026.csv", 3, out, "{symbol}_{tf}_{year}.{format}", "USDJPY", "M1"
        )
        assert result.year == "2026"
        assert (out / "usdjpy_m1_2026.parquet").is_file()

    def test_raw_file_is_not_modified(self, tmp_path):
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir()
        raw_path = raw_dir / "usdjpy_m1_2026.csv"
        make_raw(consecutive(30)).to_csv(raw_path, index=False)
        before = raw_path.read_bytes()
        clean_year(raw_path, 3, tmp_path / "out", "{symbol}_{tf}_{year}.{format}", "USDJPY", "M1")
        assert raw_path.read_bytes() == before


class TestDiscoverRaw:
    def test_returns_existing_only(self, tmp_path):
        for year in (2023, 2025):
            (tmp_path / f"usdjpy_m1_{year}.csv").write_text(
                "broker_time_raw\n1\n", encoding="utf-8"
            )
        found = discover_raw("USDJPY", "M1", "{symbol}_{tf}_{year}.{format}", tmp_path)
        assert [p.name for p in found] == ["usdjpy_m1_2023.csv", "usdjpy_m1_2025.csv"]

    def test_empty_dir_returns_empty(self, tmp_path):
        assert discover_raw("USDJPY", "M1", "{symbol}_{tf}_{year}.{format}", tmp_path) == []


class TestCleanResult:
    def test_changed_false_when_nothing_happened(self):
        assert not CleanResult("2026", 10, 10, 0, 0, 0).changed

    def test_changed_true_with_gap_filled(self):
        assert CleanResult("2026", 10, 11, 0, 0, 1).changed
