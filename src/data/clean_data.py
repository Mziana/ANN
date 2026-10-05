"""Clean raw MT5 data into a processed Parquet dataset.

Raw data under data/raw/ is immutable and is never rewritten. This module
reads it, repairs the handful of things that are safe to repair, and writes
Parquet to data/processed/.

What counts as safe to repair:
    duplicates        - identical broker timestamps, keep the first
    ordering          - sort by broker timestamp
    OHLC invariants   - high/low must bracket open and close
    price precision   - round to the symbol's tick digits
    small gaps        - reindex only gaps shorter than a threshold

What is deliberately NOT repaired:
    the daily break (~61 min) and the weekend gap (~49 h). Filling those
    would fabricate bars that never traded, which would poison any
    volatility or session feature built on top.

Every bar this module invents is flagged in the ``is_filled`` column. Raw data
under data/raw/ stays byte-identical; nothing is ever written back to it.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.fetch_data import OUTPUT_COLUMNS, RAW_DIR, TIME_FORMAT, build_filename
from src.utils.config import load_config

# Gaps longer than this are left alone. The daily break is about 61 minutes,
# so anything under 20 minutes is a genuinely missing bar, not a session
# boundary.
MAX_FILL_GAP_MINUTES = 20

# Price columns rounded to the symbol tick size.
PRICE_COLUMNS = ["open", "high", "low", "close"]

TIME_COLUMN = "broker_time_raw"

# Marks rows this module invented rather than read. Downstream stages must be
# able to tell a real bar from a carried-forward one, otherwise an interpolated
# bar silently becomes a trade.
FILLED_COLUMN = "is_filled"


@dataclass
class CleanResult:
    """What cleaning one year changed."""

    year: str
    rows_in: int
    rows_out: int
    duplicates_removed: int
    ohlc_repaired: int
    gaps_filled: int

    @property
    def changed(self) -> bool:
        return bool(self.duplicates_removed or self.ohlc_repaired or self.gaps_filled)


def load_raw(path: Path) -> pd.DataFrame:
    """Load one raw CSV and restore its column order.

    Args:
        path: Raw CSV written by fetch_data.

    Returns:
        DataFrame with the canonical column order from fetch_data.
    """
    frame = pd.read_csv(path)
    return frame[OUTPUT_COLUMNS]


def deduplicate(frame: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Drop rows that repeat an already-seen broker timestamp.

    Args:
        frame: Raw frame.

    Returns:
        Tuple of the deduplicated frame and the number of rows removed.
    """
    mask = frame[TIME_COLUMN].duplicated(keep="first")
    return frame[~mask].reset_index(drop=True), int(mask.sum())


def sort_by_time(frame: pd.DataFrame) -> pd.DataFrame:
    """Sort rows by broker timestamp and return a clean index.

    Args:
        frame: Frame with a broker timestamp column.

    Returns:
        Sorted frame with a reset index.
    """
    return frame.sort_values(TIME_COLUMN).reset_index(drop=True)


def normalize_ohlc(frame: pd.DataFrame, digits: int) -> tuple[pd.DataFrame, int]:
    """Round prices to tick precision and restore the OHLC invariants.

    MT5 prices are already consistent (validate_data.py proves it), so this
    is a guard for future data rather than a routine transformation. Only the
    rows it actually changes are counted.

    Args:
        frame: Frame with open, high, low and close.
        digits: Price decimals from the symbol, 3 for USDJPY.

    Returns:
        Tuple of the normalised frame and the number of rows changed.
    """
    before = frame[PRICE_COLUMNS].round(digits)
    after = before.copy()
    after["high"] = after[PRICE_COLUMNS].max(axis=1)
    after["low"] = after[PRICE_COLUMNS].min(axis=1)

    changed = int((after[PRICE_COLUMNS] != frame[PRICE_COLUMNS]).any(axis=1).sum())
    frame = frame.copy()
    for column in PRICE_COLUMNS:
        frame[column] = after[column].astype("float64")
    del before
    return frame, changed


def fill_small_gaps(
    frame: pd.DataFrame, max_minutes: int = MAX_FILL_GAP_MINUTES
) -> tuple[pd.DataFrame, int]:
    """Reindex the timeline only where the hole is genuinely a missing bar.

    A hole is filled only when it is strictly longer than one minute and no
    longer than ``max_minutes``. Longer holes collapse back to their two
    endpoints, so the daily break and the weekend gap survive exactly as the
    broker produced them.

    Filled rows carry the previous bar's values forward, which means their high,
    low, open and close are all equal. They are flagged in
    :data:`FILLED_COLUMN` so nothing downstream mistakes them for real ticks.

    Args:
        frame: Frame carrying an integer broker timestamp column.
        max_minutes: Longest hole that may be filled.

    Returns:
        Tuple of the resulting frame in canonical column order plus the filled
        flag, and the number of rows inserted.
    """
    step = pd.Timedelta(minutes=1)
    limit = pd.Timedelta(minutes=max_minutes)

    # Both timestamp columns are rebuilt from the index below, so drop them
    # first. Keeping either would collide on insert, and forward-filling a stale
    # time string would be worse than forward-filling a stale price.
    working = frame.drop(columns=[TIME_COLUMN, "time"])
    working.index = pd.to_datetime(frame[TIME_COLUMN], unit="s", utc=True)
    working = working.sort_index()

    original = working.index
    holes = original.to_series().diff()
    fillable_ends = original[(holes > step) & (holes <= limit)]

    timeline = pd.date_range(original.min(), original.max(), freq=step)
    absent = ~timeline.isin(original)

    fillable = pd.Series(False, index=timeline)
    for end in fillable_ends:
        hole = pd.date_range(end - holes[end] + step, end - step, freq=step)
        fillable.loc[hole] = True

    dropped = absent & ~fillable
    keep = ~dropped
    kept = working.reindex(timeline)[keep].ffill()

    # as_unit("ns") is not optional: pandas 3.x lets to_datetime(..., unit="s")
    # build a datetime64[s] index, whose .asi8 counts seconds rather than
    # nanoseconds. Without this the epoch column collapses to 1 on every row.
    epoch = kept.index.as_unit("ns").asi8 // 10**9
    result = kept.reset_index(drop=True)
    result.insert(0, TIME_COLUMN, epoch)
    result.insert(0, "time", pd.to_datetime(epoch, unit="s", utc=True).strftime(TIME_FORMAT))
    # A kept row was flagged filled exactly when raw data had no bar for it.
    result[FILLED_COLUMN] = absent[keep]

    return result[OUTPUT_COLUMNS + [FILLED_COLUMN]], int((absent & fillable).sum())


def clean_frame(frame: pd.DataFrame, digits: int) -> tuple[pd.DataFrame, CleanResult]:
    """Run the full cleaning chain over one year of raw data.

    Args:
        frame: Raw frame from load_raw.
        digits: Price decimals for the symbol.

    Returns:
        Tuple of the cleaned frame and a CleanResult describing the changes.
    """
    rows_in = len(frame)
    frame, duplicates = deduplicate(frame)
    frame = sort_by_time(frame)
    frame, repaired = normalize_ohlc(frame, digits)
    frame, filled = fill_small_gaps(frame)

    result = CleanResult(
        year="",
        rows_in=rows_in,
        rows_out=len(frame),
        duplicates_removed=duplicates,
        ohlc_repaired=repaired,
        gaps_filled=filled,
    )
    return frame, result


def clean_year(
    raw_path: Path, digits: int, out_dir: Path, pattern: str, symbol: str, timeframe: str
) -> CleanResult:
    """Clean one raw year file and write it as Parquet.

    Args:
        raw_path: Source CSV under data/raw/.
        digits: Price decimals for the symbol.
        out_dir: Destination directory for Parquet output.
        pattern: Filename pattern from config.
        symbol: Trading symbol.
        timeframe: Timeframe name.

    Returns:
        CleanResult for the year, with the year label filled in.
    """
    frame, result = clean_frame(load_raw(raw_path), digits)
    result.year = raw_path.stem[-4:]

    name = build_filename(symbol, timeframe, result.year, pattern).replace(".csv", ".parquet")
    out_dir.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(out_dir / name, index=False)
    return result


def discover_raw(symbol: str, timeframe: str, pattern: str, data_dir: Path) -> list[Path]:
    """Find every raw year file for a symbol and timeframe.

    Args:
        symbol: Trading symbol.
        timeframe: Timeframe name.
        pattern: Filename pattern from config.
        data_dir: Raw data directory.

    Returns:
        Sorted list of existing CSV paths.
    """
    years = range(2023, date.today().year + 1)
    return [
        path
        for path in (
            data_dir / build_filename(symbol, timeframe, str(year), pattern) for year in years
        )
        if path.is_file()
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Argument list, defaults to ``sys.argv[1:]``.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Clean raw MT5 data into Parquet.")
    parser.add_argument("--timeframe", default=None, help="Timeframe, default from config.")
    parser.add_argument(
        "--digits", type=int, default=None, help="Price decimals, default from config."
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Clean every raw year file and report what changed.

    Returns:
        Process exit code: 0 when all years were processed, 1 otherwise.
    """
    args = parse_args(argv)
    config: dict[str, Any] = load_config("data")
    symbol = config["mt5"]["symbol"]
    timeframe = args.timeframe or config["mt5"]["timeframes"][0]
    pattern = config["data"]["filename_pattern"]
    digits = args.digits if args.digits is not None else int(config["mt5"]["price_digits"])

    raw_dir = RAW_DIR / timeframe
    out_dir = RAW_DIR.parents[0] / "processed" / timeframe
    files = discover_raw(symbol, timeframe, pattern, raw_dir)

    if not files:
        print(f"GAGAL: tidak ada file raw di {raw_dir}")
        return 1

    for path in files:
        result = clean_year(path, digits, out_dir, pattern, symbol, timeframe)
        print(
            f"{result.year}: {result.rows_in:,} -> {result.rows_out:,} bar | "
            f"duplikat {result.duplicates_removed}, OHLC diperbaiki "
            f"{result.ohlc_repaired}, gap diisi {result.gaps_filled}"
        )
    print(f"Output: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
