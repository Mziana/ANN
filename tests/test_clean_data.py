"""Unit tests for src.data.clean_data.

The single most important behaviour here is what the module refuses to do:
invent nothing. Every gap the broker produces, small or large, must survive
cleaning untouched.
"""

from __future__ import annotations

import pandas as pd
import pytest

from src.data.clean_data import (
    TIME_COLUMN,
    CleanResult,
    clean_frame,
    clean_year,
    deduplicate,
    discover_raw,
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


class TestNoInterpolation:
    """D1: cleaning must never invent a bar.

    Interpolating a missing price is the one thing this pipeline must not do,
    because nothing downstream can tell an invented bar from a real one. These
    tests pin that behaviour at every gap size the broker actually produces.
    """

    def test_short_gap_is_left_alone(self):
        frame = make_raw([BASE, BASE + 60 * 4])
        cleaned, result = clean_frame(frame, 3)
        assert result.gaps_filled == 0
        assert len(cleaned) == 2

    def test_daily_break_is_left_alone(self):
        """The 61 minute break must not become synthetic bars."""
        frame = make_raw([BASE, BASE + 61 * 60])
        cleaned, result = clean_frame(frame, 3)
        assert result.gaps_filled == 0
        assert len(cleaned) == 2

    def test_weekend_gap_is_left_alone(self):
        frame = make_raw([BASE, BASE + 2880 * 60])
        cleaned, result = clean_frame(frame, 3)
        assert result.gaps_filled == 0
        assert len(cleaned) == 2

    def test_no_is_filled_column_survives(self):
        """The flag existed only to mark invented rows; it is gone now."""
        cleaned, _ = clean_frame(make_raw(consecutive(5)), 3)
        assert "is_filled" not in cleaned.columns

    def test_row_count_never_increases(self):
        for gap in (1, 4, 20, 61, 2880):
            cleaned, _ = clean_frame(make_raw([BASE, BASE + gap * 60]), 3)
            assert len(cleaned) == 2, f"gap {gap} menit menambah bar"

    def test_timestamps_are_untouched(self):
        """Cleaning must preserve the exact epochs the broker produced."""
        epochs = [BASE, BASE + 60 * 4, BASE + 61 * 60]
        cleaned, _ = clean_frame(make_raw(epochs), 3)
        assert cleaned[TIME_COLUMN].tolist() == epochs

    def test_changed_is_false_when_only_gaps_differ(self):
        cleaned, result = clean_frame(make_raw([BASE, BASE + 60 * 4]), 3)
        assert result.gaps_filled == 0
        assert not result.changed


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

    def test_changed_true_with_ohlc_repaired(self):
        assert CleanResult("2026", 10, 10, 0, 1, 0).changed

    def test_changed_false_when_only_gap_counted(self):
        """D1 removed filling, so a nonzero gaps_filled alone is not a change."""
        assert not CleanResult("2026", 10, 10, 0, 0, 5).changed
