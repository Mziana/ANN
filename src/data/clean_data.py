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
    any gap at all. The daily break (~61 min), the weekend gap (~49 h) and
    small holes between bars are all left untouched. Interpolating a missing
    bar invents a price that never traded, and a strategy cannot tell an
    invented price from a real one. Downstream stages see only bars the broker
    actually produced; ``m1_bars`` in resample.py reports how many real bars a
    bucket holds instead of papering over the hole.

Raw data under data/raw/ stays byte-identical; nothing is ever written back to it.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.fetch_data import OUTPUT_COLUMNS, RAW_DIR, build_filename
from src.utils.config import load_config

# Price columns rounded to the symbol tick size.
PRICE_COLUMNS = ["open", "high", "low", "close"]

TIME_COLUMN = "broker_time_raw"


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
        """Whether cleaning altered the data at all.

        Returns:
            True when any row was removed or repaired. Gap filling no longer
            exists, so it is not part of this verdict.
        """
        return bool(self.duplicates_removed or self.ohlc_repaired)


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


def clean_frame(frame: pd.DataFrame, digits: int) -> tuple[pd.DataFrame, CleanResult]:
    """Run the full cleaning chain over one year of raw data.

    No bar is ever invented. Gaps of any size are left exactly as the broker
    produced them, so every row downstream is a bar that really traded.

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

    result = CleanResult(
        year="",
        rows_in=rows_in,
        rows_out=len(frame),
        duplicates_removed=duplicates,
        ohlc_repaired=repaired,
        gaps_filled=0,
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
