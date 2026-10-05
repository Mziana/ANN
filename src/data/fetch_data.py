"""Fetch OHLC data from MetaTrader 5 and store it as CSV.

Two traps this module exists to handle correctly:

1. MT5 returns timestamps on the broker server clock, not UTC. The offset is
   verified at +3 hours (``Etc/GMT-3``). Both the UTC timestamp and the raw
   broker epoch are stored, so the conversion can be audited later without
   fetching again.

2. The ``spread`` column from MT5 is in POINTS, not pips. For USDJPY a
   point is 0.001 and a pip is 0.01, so treating the column as pips would
   overstate the spread by 10x and wreck any backtest expectancy.

Note on prices: MetaTrader5 returns BID prices in OHLC. Per RULES.md 18.16
a BUY must therefore enter on ask (bid + spread) and exit on bid. This module
never converts OHLC; it stores the bid prices exactly as received.

MetaTrader5 is imported lazily. It is a Windows-only package, and importing it
at module level made every test collection fail on any machine without it. Only
fetch_rates, timeframe_constant and main actually need the live connection.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from src.utils.config import PROJECT_ROOT, load_config

logger = logging.getLogger(__name__)

# Names of the MT5 timeframe constants, not their values. The values come from
# the MetaTrader5 module, which must not be imported at module level.
TIMEFRAME_NAMES = {
    "M1": "TIMEFRAME_M1",
    "M5": "TIMEFRAME_M5",
    "M15": "TIMEFRAME_M15",
    "M30": "TIMEFRAME_M30",
    "H1": "TIMEFRAME_H1",
    "H4": "TIMEFRAME_H4",
    "D1": "TIMEFRAME_D1",
}

OUTPUT_COLUMNS = [
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

RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Single source of truth for the ``time`` string layout. clean_data.py rebuilds
# this column for the bars it interpolates, and both stages must agree exactly.
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def broker_epoch_to_utc(epoch: int, broker_tz: ZoneInfo) -> datetime:
    """Convert an MT5 broker timestamp to a timezone-aware UTC datetime.

    Args:
        epoch: Raw epoch seconds as returned by MT5, on broker server time.
        broker_tz: Timezone of the broker server.

    Returns:
        The same instant expressed in UTC, with tzinfo attached.
    """
    return datetime.fromtimestamp(epoch, tz=broker_tz).astimezone(UTC)


def spread_points_to_pips(
    spread_points: float | pd.Series, point: float, pip_size: float
) -> float | pd.Series:
    """Convert an MT5 spread value from points to pips.

    Works on a scalar or on a whole Series so the same rule can be reused
    when converting a column.

    Args:
        spread_points: Spread as reported by MT5, in points.
        point: Symbol price increment, from ``symbol_info().point``.
        pip_size: Pip value from configs/data.yaml, e.g. 0.01 for USDJPY.

    Returns:
        Spread expressed in pips, same shape as the input.

    Raises:
        ValueError: If point or pip_size is zero or negative.
    """
    if point <= 0 or pip_size <= 0:
        raise ValueError(f"point and pip_size must be positive, got point={point}, pip={pip_size}")
    return spread_points * point / pip_size


def build_filename(symbol: str, timeframe: str, period: str, pattern: str) -> str:
    """Build an output filename from the configured pattern.

    Args:
        symbol: Trading symbol, lowercased in the result.
        timeframe: Timeframe name, lowercased in the result.
        period: Period string such as ``"2026"`` or ``"2026-10_test"``.
        pattern: Filename pattern from configs/data.yaml.

    Returns:
        Filename such as ``usdjpy_m1_2026.csv``.
    """
    return pattern.format(symbol=symbol.lower(), tf=timeframe.lower(), year=period, format="csv")


def import_mt5() -> Any:
    """Import and return the MetaTrader5 module on first use.

    The import is deferred rather than done at module level because
    MetaTrader5 only exists on Windows and needs the terminal to talk to.
    Keeping it here lets tests, and validate_data (which imports this module
    for its path helpers), run on any platform.

    Returns:
        The ``MetaTrader5`` module object.
    """
    import MetaTrader5 as mt5

    return mt5


def timeframe_constant(timeframe: str) -> int:
    """Resolve a timeframe name to its MT5 constant.

    Args:
        timeframe: Timeframe name from configs/data.yaml, such as ``"M1"``.

    Returns:
        The integer constant MetaTrader5 expects for that timeframe.

    Raises:
        ValueError: If the timeframe name is not recognised.
    """
    if timeframe not in TIMEFRAME_NAMES:
        raise ValueError(
            f"Unknown timeframe {timeframe!r}, expected one of {list(TIMEFRAME_NAMES)}"
        )
    return int(getattr(import_mt5(), TIMEFRAME_NAMES[timeframe]))


def fetch_rates(symbol: str, timeframe: str, start: datetime, end: datetime) -> np.ndarray:
    """Fetch raw rates from MetaTrader 5.

    Requires a running MT5 terminal. Start and end are converted with
    ``int(timestamp())``, which is exact for timeframes of one minute or
    coarser. Sub-minute timeframes would lose the sub-second part and must not
    be fetched with this function.

    Args:
        symbol: Trading symbol, for example ``"USDJPY"``.
        timeframe: Timeframe name from configs/data.yaml.
        start: Inclusive start of the range, timezone aware.
        end: Exclusive end of the range, timezone aware.

    Returns:
        Structured numpy array as returned by ``copy_rates_range``. The dtype is
        MT5's own rates dtype (time, open, high, low, close, tick_volume,
        spread, real_volume), so it is intentionally left as a plain
        ``np.ndarray`` rather than narrowed to a guess.

    Raises:
        ValueError: If the timeframe is unknown or MT5 returns nothing.
    """
    mt5 = import_mt5()
    rates = mt5.copy_rates_range(
        symbol,
        timeframe_constant(timeframe),
        int(start.timestamp()),
        int(end.timestamp()),
    )

    if rates is None or len(rates) == 0:
        raise ValueError(f"MT5 returned no data for {symbol} {timeframe}: {mt5.last_error()}")

    return rates


def rates_to_frame(
    rates: np.ndarray, broker_tz: ZoneInfo, point: float, pip_size: float
) -> pd.DataFrame:
    """Convert raw MT5 rates into the project's CSV schema.

    Args:
        rates: Structured array from ``fetch_rates``.
        broker_tz: Broker server timezone.
        point: Symbol price increment.
        pip_size: Pip value from config.

    Returns:
        DataFrame with :data:`OUTPUT_COLUMNS`, ordered, with UTC timestamps as
        ISO-8601 strings and the untouched broker epoch preserved.
    """
    frame = pd.DataFrame(rates)
    frame["broker_time_raw"] = frame["time"].astype("int64")
    frame["time"] = [
        broker_epoch_to_utc(int(epoch), broker_tz) for epoch in frame["broker_time_raw"]
    ]
    frame = frame.rename(columns={"spread": "spread_points"})
    frame["spread_pips"] = spread_points_to_pips(frame["spread_points"], point, pip_size)
    frame = frame[OUTPUT_COLUMNS].sort_values("broker_time_raw").reset_index(drop=True)
    frame["time"] = frame["time"].dt.strftime(TIME_FORMAT)
    return frame


def write_csv(frame: pd.DataFrame, path: Path) -> Path:
    """Write a DataFrame to CSV, creating parent directories as needed.

    Args:
        frame: Data to write.
        path: Destination path.

    Returns:
        The destination path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


def split_by_year(
    frame: pd.DataFrame, out_dir: Path, pattern: str, symbol: str, tf: str
) -> list[Path]:
    """Write one CSV per calendar year.

    Args:
        frame: DataFrame whose ``broker_time_raw`` column drives the split.
        out_dir: Destination directory.
        pattern: Filename pattern from config.
        symbol: Trading symbol.
        tf: Timeframe name.

    Returns:
        Paths written, sorted by year.

    Raises:
        ValueError: If the frame is empty.
    """
    if frame.empty:
        raise ValueError("Cannot split an empty frame")

    years = pd.to_datetime(frame["broker_time_raw"], unit="s", utc=True).dt.year
    written = []
    for year in sorted(years.unique()):
        chunk = frame[years == year]
        filename = build_filename(symbol, tf, str(year), pattern)
        written.append(write_csv(chunk, out_dir / filename))
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Argument list, defaults to ``sys.argv[1:]``.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Fetch USDJPY data from MetaTrader 5.")
    parser.add_argument("--start", help="Start date YYYY-MM-DD, default from config.")
    parser.add_argument("--end", help="End date YYYY-MM-DD, default from config.")
    parser.add_argument("--timeframe", default=None, help="Timeframe, default from config.")
    parser.add_argument("--out", default=None, help="Single output file; skips the per-year split.")
    return parser.parse_args(argv)


def report_error(message: str) -> None:
    """Log an error and echo it to stderr.

    Errors go to stderr so a caller can pipe the normal summary on stdout and
    still see the failure.

    Args:
        message: Human readable failure description.
    """
    logger.error(message)
    print(message, file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    """Fetch data and write it to CSV.

    Returns:
        Process exit code: 0 on success, 1 on failure.
    """
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    config = load_config("data")
    mt5_config: dict[str, Any] = config["mt5"]

    symbol = mt5_config["symbol"]
    timeframe = args.timeframe or mt5_config["timeframes"][0]
    start = datetime.fromisoformat(args.start or mt5_config["start_date"]).replace(tzinfo=UTC)
    end = datetime.fromisoformat(args.end or mt5_config["end_date"]).replace(tzinfo=UTC)
    broker_tz = ZoneInfo(mt5_config["broker_timezone"])
    pip_size = float(config["spread"]["pip_size"][symbol])
    pattern = config["data"]["filename_pattern"]

    mt5 = import_mt5()
    if not mt5.initialize():
        report_error(f"GAGAL: mt5.initialize() -> {mt5.last_error()}")
        return 1

    try:
        info = mt5.symbol_info(symbol)
        if info is None:
            report_error(f"GAGAL: simbol {symbol} tidak dikenal")
            return 1
        rates = fetch_rates(symbol, timeframe, start, end)
        frame = rates_to_frame(rates, broker_tz, info.point, pip_size)
    finally:
        mt5.shutdown()

    if args.out:
        paths = [write_csv(frame, Path(args.out))]
    else:
        paths = split_by_year(frame, RAW_DIR / timeframe, pattern, symbol, timeframe)

    summary = f"OK: {len(frame)} bar {symbol} {timeframe} -> {len(paths)} file"
    logger.info(summary)
    print(summary)
    for path in paths:
        logger.info("wrote %s", path)
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
