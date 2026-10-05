"""Resample cleaned M1 data into higher timeframes.

Design decisions that matter (user approved 2026-10-05):

D2. Buckets follow the BROKER wall clock, not UTC, and every row is labelled
    with the START of its interval. The broker day runs 04:00 to 03:00 server
    time, so a UTC calendar day would cut sessions in the wrong place and the
    daily break would land mid-bucket. Etc/GMT-3 has no DST, which is verified
    over 2023-2026, so flooring on this zone is unambiguous.

D3. Spread is aggregated as both a mean and a max. The mean describes the usual
    cost of a trade; the max describes the tail, and the tail is what breaks an
    expectancy model when it is averaged away.

D4. Buckets with no M1 bar are simply absent rather than emitted as empty rows,
    and every kept bucket carries ``m1_bars``: how many real one-minute bars
    actually went into it. Nothing here invents a bar. A bucket built from 3
    bars instead of 5 says so in its own row instead of hiding it.

Prices are MT5 bid prices. Per RULES.md 18.16 a BUY enters on ask and exits on
bid, so a backtest must still add the spread; this module only reshapes data and
never converts prices.
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from datetime import UTC
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

from src.data.clean_data import TIME_COLUMN
from src.data.fetch_data import TIME_FORMAT, build_filename
from src.utils.config import load_config

logger = logging.getLogger(__name__)

# Minutes per supported output timeframe. The broker wall clock offset is a whole
# number of hours, so intraday buckets line up with UTC buckets too; only D1
# genuinely differs, because the broker trading day does not start at midnight.
TIMEFRAME_MINUTES = {"M5": 5, "M15": 15, "M30": 30, "H1": 60, "H4": 240, "D1": 1440}

OHLC_COLUMNS = ["open", "high", "low", "close"]
VOLUME_COLUMNS = ["tick_volume", "real_volume"]

# Broker wall-clock start of the bucket. Dropped from the written frame after it
# becomes the two timestamp columns.
BUCKET_COLUMN = "bucket_start"

OUTPUT_COLUMNS = [
    "time",
    TIME_COLUMN,
    "open",
    "high",
    "low",
    "close",
    "tick_volume",
    "real_volume",
    "spread_pips_mean",
    "spread_pips_max",
    "m1_bars",
]

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"


@dataclass
class ResampleResult:
    """What resampling one year into one timeframe produced."""

    year: str
    timeframe: str
    buckets: int
    m1_bars: int
    shortest_bucket: int
    longest_bucket: int

    @property
    def complete(self) -> bool:
        """Whether every bucket holds the full expected number of M1 bars.

        Returns:
            True when the shortest bucket still matches the timeframe length.
        """
        return self.shortest_bucket >= self.expected

    @property
    def expected(self) -> int:
        """M1 bars a full bucket should hold for this timeframe.

        Returns:
            The timeframe length in minutes.
        """
        return TIMEFRAME_MINUTES[self.timeframe]


def broker_bucket_start(frame: pd.DataFrame, minutes: int, broker_tz: ZoneInfo) -> pd.Series:
    """Floor each bar to the start of its broker wall-clock bucket.

    Args:
        frame: Frame carrying an integer broker timestamp column.
        minutes: Bucket length in minutes.
        broker_tz: Broker timezone. Must have no DST for flooring to be
            unambiguous, which Etc/GMT-3 satisfies.

    Returns:
        Series of broker-local bucket start timestamps aligned to ``frame``.
    """
    stamps = pd.to_datetime(frame[TIME_COLUMN], unit="s", utc=True).dt.tz_convert(broker_tz)
    frequency = "D" if minutes >= 1440 else f"{minutes}min"
    return stamps.dt.floor(frequency)


def aggregate_buckets(frame: pd.DataFrame, buckets: pd.Series) -> pd.DataFrame:
    """Aggregate M1 rows into one row per bucket.

    Args:
        frame: Cleaned M1 frame.
        buckets: Bucket start timestamp for every row of ``frame``.

    Returns:
        One row per non-empty bucket, with ``m1_bars`` recording how many M1 bars
        produced it.
    """
    # groupby carries the Series name into the key column, so name it explicitly
    # instead of guessing what reset_index will call it.
    keyed = buckets.rename(BUCKET_COLUMN)
    grouped = frame.groupby(keyed, sort=True)
    out = grouped.agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        tick_volume=("tick_volume", "sum"),
        real_volume=("real_volume", "sum"),
        spread_pips_mean=("spread_pips", "mean"),
        spread_pips_max=("spread_pips", "max"),
        m1_bars=("close", "size"),
    )
    return out.reset_index()


def finalise(frame: pd.DataFrame, digits: int) -> pd.DataFrame:
    """Rebuild the timestamp columns and round prices to the symbol tick.

    Args:
        frame: Aggregated buckets with a ``BUCKET_COLUMN`` column.
        digits: Price decimals for the symbol.

    Returns:
        Frame in :data:`OUTPUT_COLUMNS` order with UTC ``time`` and epoch
        ``broker_time_raw`` both marking the bucket start.
    """
    result = frame.copy()
    # as_unit("ns") matters on pandas 3.x, where a seconds-resolution index
    # would make .asi8 report seconds and collapse every epoch to 1.
    stamps = result[BUCKET_COLUMN].dt.tz_convert(UTC).dt.tz_localize(None)
    epoch_seconds = (pd.DatetimeIndex(stamps).as_unit("ns").asi8 // 10**9).astype("int64")

    result[TIME_COLUMN] = epoch_seconds
    result["time"] = pd.to_datetime(epoch_seconds, unit="s", utc=True).strftime(TIME_FORMAT)
    for column in OHLC_COLUMNS:
        result[column] = result[column].round(digits)
    return result[OUTPUT_COLUMNS]


def resample_frame(
    frame: pd.DataFrame, timeframe: str, broker_tz: ZoneInfo, digits: int
) -> tuple[pd.DataFrame, ResampleResult]:
    """Resample one cleaned M1 frame into a single higher timeframe.

    Args:
        frame: Cleaned M1 frame sorted by broker timestamp.
        timeframe: Output timeframe name from :data:`TIMEFRAME_MINUTES`.
        broker_tz: Broker timezone used for bucket boundaries.
        digits: Price decimals for the symbol.

    Returns:
        Tuple of the resampled frame and a ResampleResult.

    Raises:
        ValueError: If the timeframe name is unknown or the frame is empty.
    """
    if timeframe not in TIMEFRAME_MINUTES:
        raise ValueError(
            f"Unknown timeframe {timeframe!r}, expected one of {list(TIMEFRAME_MINUTES)}"
        )
    if frame.empty:
        raise ValueError("Cannot resample an empty frame")

    buckets = broker_bucket_start(frame, TIMEFRAME_MINUTES[timeframe], broker_tz)
    aggregated = aggregate_buckets(frame, buckets)
    out = finalise(aggregated, digits)

    counts = out["m1_bars"]
    result = ResampleResult(
        year="",
        timeframe=timeframe,
        buckets=len(out),
        m1_bars=int(counts.sum()),
        shortest_bucket=int(counts.min()),
        longest_bucket=int(counts.max()),
    )
    return out, result


def resample_year(
    source: Path,
    out_dir: Path,
    timeframe: str,
    symbol: str,
    pattern: str,
    broker_tz: ZoneInfo,
    digits: int,
) -> ResampleResult:
    """Resample one cleaned year file and write it as Parquet.

    Args:
        source: Cleaned M1 Parquet file.
        out_dir: Destination directory for this timeframe.
        timeframe: Output timeframe name.
        symbol: Trading symbol.
        pattern: Filename pattern from config.
        broker_tz: Broker timezone.
        digits: Price decimals for the symbol.

    Returns:
        ResampleResult for the year.

    Raises:
        FileNotFoundError: If the source file does not exist.
    """
    if not source.is_file():
        raise FileNotFoundError(f"Cleaned M1 file not found: {source}")

    frame = pd.read_parquet(source)
    out, result = resample_frame(frame, timeframe, broker_tz, digits)
    result.year = source.stem[-4:]

    name = build_filename(symbol, timeframe, result.year, pattern).replace(".csv", ".parquet")
    out_dir.mkdir(parents=True, exist_ok=True)
    out.to_parquet(out_dir / name, index=False)
    return result


def discover_cleaned(symbol: str, timeframe: str, pattern: str, base: Path) -> list[Path]:
    """Find every cleaned M1 year file available.

    Args:
        symbol: Trading symbol.
        timeframe: Source timeframe name, normally ``"M1"``.
        pattern: Filename pattern from config.
        base: Root of the processed data directory.

    Returns:
        Sorted list of existing Parquet paths.
    """
    directory = base / timeframe
    return sorted(path for path in directory.glob("*.parquet") if path.is_file())


def report_error(message: str) -> None:
    """Log an error and echo it to stderr.

    Args:
        message: Human readable failure description.
    """
    logger.error(message)
    print(message, file=sys.stderr)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Argument list, defaults to ``sys.argv[1:]``.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Resample cleaned M1 data.")
    parser.add_argument(
        "--timeframes",
        default=None,
        help="Comma separated output timeframes, default from config.",
    )
    parser.add_argument("--symbol", default=None, help="Symbol, default from config.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Resample every cleaned year into every requested timeframe.

    Returns:
        Process exit code: 0 when all combinations were written, 1 otherwise.
    """
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    config: dict[str, Any] = load_config("data")
    symbol = args.symbol or config["mt5"]["symbol"]
    source_tf = config["mt5"]["timeframes"][0]
    pattern = config["data"]["filename_pattern"]
    broker_tz = ZoneInfo(config["mt5"]["broker_timezone"])
    digits = int(config["mt5"]["price_digits"])

    if args.timeframes:
        wanted = [name.strip() for name in args.timeframes.split(",") if name.strip()]
    else:
        wanted = [tf for tf in config["mt5"]["timeframes"] if tf != source_tf]

    unknown = [tf for tf in wanted if tf not in TIMEFRAME_MINUTES]
    if unknown:
        report_error(f"GAGAL: timeframe tidak dikenal: {unknown}")
        return 1

    sources = discover_cleaned(symbol, source_tf, pattern, PROCESSED_DIR)
    if not sources:
        report_error(f"GAGAL: tidak ada M1 bersih di {PROCESSED_DIR / source_tf}")
        return 1

    for timeframe in wanted:
        out_dir = PROCESSED_DIR / timeframe
        for source in sources:
            result = resample_year(source, out_dir, timeframe, symbol, pattern, broker_tz, digits)
            mark = "penuh" if result.complete else f"ada bucket < {result.expected} bar"
            line = (
                f"{timeframe} {result.year}: {result.buckets:,} bucket dari "
                f"{result.m1_bars:,} bar M1 | bar/bucket "
                f"{result.shortest_bucket}-{result.longest_bucket} ({mark})"
            )
            logger.info(line)
            print(line)

    print(f"Output: {PROCESSED_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
