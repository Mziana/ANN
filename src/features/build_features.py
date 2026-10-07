"""Build the per-bar M15 feature store foundation for Lapisan 3.

Lapisan 2 (EDA) is closed and H1-H5 are locked
(``reports/governance/2026-10-07/hipotesis_lock_v1.md``). Lapisan 3 tests those
hypotheses walk-forward and needs columns the processed data does not carry:

* Session columns - the DST-aware non-exclusive flags plus the exclusive label
  (London > NewYork > Tokyo > Sydney > Off), ported verbatim from the locked
  definition in ``notebooks/scalping/_eda_common.py``; a notebook is not
  importable, so the copy is deliberate (``session_fingerprint`` pins it).
* ``atr_14_d1`` / ``range_atr`` / ``ratio_path`` - H1 daily typology inputs,
  computed exactly as nb05 section 1 did (see :func:`daily_metrics`).
* ``rv_roll_20d`` - H3 detector input: 20-day rolling sum of the daily rv_day.
* ``hour_utc`` / ``date_broker`` - clock keys for H4 and broker-calendar joins.

Satuan terkunci: atr_14_d1 = JPY (harga, faithful nb05); range_pips = pip;
range_atr = pip/harga (konvensi campuran, median lock 88,79); ratio_path, rv_day,
rv_roll_20d = tak-berdimensi. DILARANG rasio kaki-campur selain range_atr.

M5 sengaja bukan input (putusan arsitek B1-2): tak ada kolom yang menurunkannya;
H2 membaca parquet M5 langsung per doktrin D0.

Anti look-ahead: a bar at time t uses only data at or before t, so a bar on
broker day D carries the last COMPLETED day's (D-1) values and never sees day
D. :func:`build_features` enforces that with a machine assertion, and a
dedicated test rebuilds after mutating the tail of the input.

Reuse-First: ``load_config``, ``wall_clock_series``, ``clean_data.TIME_COLUMN``
and ``resample.discover_cleaned`` are reused; only the session definition is
duplicated, and only because importing a notebook is forbidden.

Out of scope: labels (B2), the H2 diagnostic strategy, the H3 filter, backtest.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.data.broker_time import wall_clock_series
from src.data.clean_data import TIME_COLUMN
from src.data.resample import discover_cleaned
from src.utils.config import load_config

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FEATURES_DIR = PROJECT_ROOT / "data" / "features"

# Columns read from the processed data; checked before use so schema drift
# fails loudly instead of silently producing NaNs.
M1_REQUIRED = ("time", TIME_COLUMN, "close")
M15_REQUIRED = ("time", TIME_COLUMN, "open", "high", "low", "close")
# Kolom spread tidak ditambahkan (putusan arsitek B1-1): H5 membaca spread_pips M1 langsung per doktrin D0.

ATR_WINDOW = 14
RV_WINDOW = 20

SESSION_COLUMNS = ["is_tokyo", "is_london", "is_ny", "is_sydney"]
CLOCK_COLUMNS = ["hour_utc", "date_broker"]
DAILY_COLUMNS = ["atr_14_d1", "rv_roll_20d", "range_atr", "ratio_path"]
FEATURE_COLUMNS = SESSION_COLUMNS + ["session_label"] + CLOCK_COLUMNS + DAILY_COLUMNS

# Ported verbatim from notebooks/scalping/_eda_common.py (the locked nb00
# definition). Keep both copies in sync; session_fingerprint guards it.
SESSION_SPECS = {
    "is_tokyo": {"name": "Tokyo", "zone": "Asia/Tokyo", "start": 9, "end": 18},
    "is_london": {"name": "London", "zone": "Europe/London", "start": 8, "end": 16},
    "is_ny": {"name": "New York", "zone": "America/New_York", "start": 8, "end": 17},
    "is_sydney": {"name": "Sydney", "zone": "Australia/Sydney", "start": 8, "end": 16},
}

SESSION_PRIORITY = [
    ("is_london", "London"),
    ("is_ny", "NewYork"),
    ("is_tokyo", "Tokyo"),
    ("is_sydney", "Sydney"),
]

EXPECTED_SESSION_FINGERPRINT = (
    "Tokyo:Asia/Tokyo:9-18|London:Europe/London:8-16|New York:America/New_York:8-17"
    "|Sydney:Australia/Sydney:8-16|priority=London>NewYork>Tokyo>Sydney"
)


def session_fingerprint() -> str:
    """Return a fingerprint of the ported session definition.

    Returns:
        String that changes whenever a session window or the priority order
        changes, so drift between the notebook and this module is detected.
    """
    parts = [
        f"{spec['name']}:{spec['zone']}:{spec['start']}-{spec['end']}"
        for spec in SESSION_SPECS.values()
    ]
    parts.append("priority=" + ">".join(label for _, label in SESSION_PRIORITY))
    return "|".join(parts)


def session_flags(utc: pd.Series) -> pd.DataFrame:
    """Flag the four sessions on each bar, DST-aware.

    Args:
        utc: Series of timezone-aware UTC timestamps.

    Returns:
        Boolean frame with columns is_tokyo, is_london, is_ny, is_sydney.
        Flags are non-exclusive: a bar may sit in several sessions at once.
    """
    flags = {}
    for column, spec in SESSION_SPECS.items():
        local_hour = utc.dt.tz_convert(spec["zone"]).dt.hour
        flags[column] = (local_hour >= spec["start"]) & (local_hour < spec["end"])
    return pd.DataFrame(flags, index=utc.index)


def exclusive_session_label(flags: pd.DataFrame) -> pd.Series:
    """Collapse the session flags into one exclusive label.

    Args:
        flags: Boolean frame as returned by :func:`session_flags`.

    Returns:
        Series named ``session_label`` holding London, NewYork, Tokyo, Sydney
        or Off, resolved by the locked priority order.
    """
    conditions = [flags[column] for column, _ in SESSION_PRIORITY]
    choices = [label for _, label in SESSION_PRIORITY]
    return pd.Series(
        np.select(conditions, choices, default="Off"), index=flags.index, name="session_label"
    )


def require_columns(frame: pd.DataFrame, columns: tuple[str, ...], source: str) -> None:
    """Fail loudly if required columns are absent.

    Args:
        frame: Frame about to be consumed.
        columns: Column names the caller needs.
        source: Human label used in the error message.

    Raises:
        ValueError: If any required column is missing.
    """
    missing = [name for name in columns if name not in frame.columns]
    if missing:
        raise ValueError(f"{source}: kolom wajib hilang: {missing}")


def prepare_bars(frame: pd.DataFrame, source: str, required: tuple[str, ...]) -> pd.DataFrame:
    """Add the UTC instant and broker-calendar day to a processed frame.

    Args:
        frame: Processed frame with ``time`` and ``broker_time_raw``.
        source: Human label used in the schema error message.
        required: Columns that must exist before use.

    Returns:
        Copy sorted by broker timestamp with ``utc`` (tz-aware), ``wall`` and
        ``broker_day`` columns added.

    Raises:
        ValueError: If a required column is missing.
    """
    require_columns(frame, ("time", TIME_COLUMN) + required, source)
    out = frame.copy()
    out["utc"] = pd.to_datetime(out["time"], utc=True)
    out["wall"] = wall_clock_series(out[TIME_COLUMN])
    out["broker_day"] = out["wall"].dt.normalize()
    return out.sort_values(TIME_COLUMN, kind="mergesort").reset_index(drop=True)


def load_processed(
    timeframe: str,
    symbol: str,
    base: Path = PROCESSED_DIR,
    years: tuple[int, ...] | None = None,
) -> pd.DataFrame:
    """Load and stack every processed Parquet year for one timeframe.

    Args:
        timeframe: Timeframe directory, e.g. ``"M15"``.
        symbol: Trading symbol, e.g. ``"USDJPY"``.
        base: Root of the processed data directory.
        years: Optional year filter; all years when omitted.

    Returns:
        Concatenated frame sorted by broker timestamp.

    Raises:
        FileNotFoundError: If no processed file matches.
    """
    files = discover_cleaned(symbol, timeframe, "", base)
    if years is not None:
        wanted = {str(year) for year in years}
        files = [path for path in files if path.stem[-4:] in wanted]
    if not files:
        raise FileNotFoundError(
            f"Tidak ada parquet {timeframe} untuk {symbol} di {base / timeframe}"
        )
    out = pd.concat([pd.read_parquet(path) for path in files], ignore_index=True)
    logger.info("load_processed %s: %d file, %d bar", timeframe, len(files), len(out))
    return out.sort_values(TIME_COLUMN, kind="mergesort").reset_index(drop=True)


def daily_metrics(m1: pd.DataFrame, m15: pd.DataFrame, pip_size: float) -> pd.DataFrame:
    """Compute broker-day metrics as nb05 section 1 did.

    Daily OHLC from M15 (= D1 bucket); return path (sum_abs_r, rv_day)
    from M1. atr_14_d1 follows nb05 verbatim; range_atr keeps nb05 units
    so locked median (88.79) reproduces. rv_roll_20d = sum(rv_day) 20 hari,
    min_periods=20 → 19 bar awal NaN.

    Args:
        m1: Processed M1 with time, broker_time_raw, close.
        m15: Processed M15 with OHLC columns.
        pip_size: Pip value, e.g. 0.01 for USDJPY.

    Returns:
        Frame indexed by broker day with daily metric columns.

    Raises:
        ValueError: missing column atau pip_size tidak valid.
    """
    if pip_size <= 0:
        raise ValueError(f"pip_size harus positif, dapat {pip_size}")
    bars_m1 = prepare_bars(m1, "M1", ("close",))
    bars_m15 = prepare_bars(m15, "M15", ("open", "high", "low", "close"))
    bars_m1["r"] = np.log(bars_m1["close"] / bars_m1["close"].shift(1))

    daily_bars = bars_m15.groupby("broker_day").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
    )
    intraday = bars_m1.groupby("broker_day").agg(
        sum_abs_r=("r", lambda s: float(np.nansum(np.abs(s)))),
        rv_day=("r", lambda s: float(np.nansum(np.square(s)))),
    )
    daily = daily_bars.join(intraday, how="inner")
    if len(daily) != len(daily_bars) or len(daily) != len(intraday):
        raise ValueError(
            f"daily_metrics: join hilang - M1 {len(intraday)}, M15 {len(daily_bars)}, "
            f"join {len(daily)}. Cek cakupan tahun."
        )
    daily["ret_day"] = np.log(daily["close"] / daily["open"])
    daily["range_pips"] = (daily["high"] - daily["low"]) / pip_size
    true_range = daily["high"] - daily["low"]
    # REVIEW: atr_14_d1 satuan harga (JPY) persis nb05, agar ambang 88,79 tereproduksi.
    daily["atr_14_d1"] = true_range.shift(1).rolling(ATR_WINDOW).mean()
    daily["range_atr"] = daily["range_pips"] / daily["atr_14_d1"]
    daily["ratio_path"] = daily["ret_day"].abs() / daily["sum_abs_r"]
    daily["rv_roll_20d"] = daily["rv_day"].rolling(RV_WINDOW, min_periods=RV_WINDOW).sum()
    return daily


def build_features(m1: pd.DataFrame, m15: pd.DataFrame, pip_size: float) -> pd.DataFrame:
    """Assemble the per-bar M15 feature store.

    Every bar carries its own session/clock keys plus the previous completed
    broker day's typology features, so no row sees the day it belongs to.

    Args:
        m1: Processed M1 frame used for the intraday return path.
        m15: Processed M15 frame defining the output bars.
        pip_size: Pip value for the symbol.

    Returns:
        Feature frame indexed by UTC timestamp (index name ``time``) with
        :data:`FEATURE_COLUMNS`.
    """
    bars = prepare_bars(m15, "M15", ("open", "high", "low", "close"))
    daily = daily_metrics(m1, m15, pip_size)

    flags = session_flags(bars["utc"])
    # REVIEW: hari D menerima nilai hari kerja selesai terakhir (D-1 posisional), bukan D.
    previous = daily[DAILY_COLUMNS].shift(1)
    attached = previous.reindex(bars["broker_day"].to_numpy())
    attached.index = bars.index

    features = pd.concat(
        [
            flags,
            exclusive_session_label(flags),
            bars["utc"].dt.hour.rename("hour_utc"),
            bars["wall"].dt.normalize().rename("date_broker"),
            attached,
        ],
        axis=1,
    )
    features = features[FEATURE_COLUMNS]
    _assert_daily_is_previous_day(features, daily)
    features.index = pd.DatetimeIndex(bars["utc"], name="time")
    return features


def _assert_daily_is_previous_day(features: pd.DataFrame, daily: pd.DataFrame) -> None:
    """Machine guard: daily features must belong to the last completed day.

    Independent of the ``shift(1)`` used to attach values: each output day is
    compared against the PREVIOUS trading day of the raw (unshifted) frame, so
    an accidental same-day join fails here instead of in Lapisan 3.

    Args:
        features: Output frame from :func:`build_features`.
        daily: Raw per-day metrics from :func:`daily_metrics`.

    Raises:
        AssertionError: If any bar carries its own or a future day's features.
    """
    days = pd.DatetimeIndex(daily.index)
    for day, block in features.groupby("date_broker", sort=True):
        position = days.get_loc(day) if day in days else -1
        anchor = days[position - 1] if position > 0 else None
        for column in DAILY_COLUMNS:
            expected = np.nan if anchor is None else float(daily.at[anchor, column])
            values = block[column].to_numpy(dtype="float64")
            assert np.allclose(
                values, expected, rtol=1e-9, atol=0.0, equal_nan=True
            ), f"{column} hari {day} != hari selesai {anchor} - indikasi look-ahead"


def write_features(features: pd.DataFrame, path: Path) -> Path:
    """Write the feature frame to Parquet, creating the directory.

    Args:
        features: Frame returned by :func:`build_features`.
        path: Destination Parquet path.

    Returns:
        The path that was written.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(path)
    logger.info("write_features: %d bar -> %s", len(features), path)
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Argument list, defaults to ``sys.argv[1:]``.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Build the M15 feature store.")
    parser.add_argument("--symbol", default=None, help="Symbol, default from config.")
    parser.add_argument("--out", default=None, help="Output parquet, default data/features/M15/.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Build the feature store from the processed data and write it.

    Args:
        argv: Argument list, defaults to ``sys.argv[1:]``.

    Returns:
        Selalu 0. ``FileNotFoundError`` dari ``load_processed`` tidak tertangkap
        dan akan membuat interpreter keluar dengan kode 1 — perilaku yang
        diperoleh secara kebetulan, bukan yang dijanjikan.
    """
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    config = load_config("data")
    symbol = args.symbol or config["mt5"]["symbol"]
    pip_size = float(config["spread"]["pip_size"][symbol])

    m1 = load_processed("M1", symbol)
    m15 = load_processed("M15", symbol)
    features = build_features(m1, m15, pip_size)

    # REVIEW: satu file gabungan (bukan per-tahun) demi walk-forward satu time series.
    default_out = FEATURES_DIR / "M15" / f"{symbol.lower()}_m15_features.parquet"
    written = write_features(features, Path(args.out) if args.out else default_out)
    logger.info(
        "selesai: %d bar M15, %d kolom, %d bar tanpa fitur harian (warmup)",
        len(features),
        len(features.columns),
        int(features["atr_14_d1"].isna().sum()),
    )
    logger.info("output: %s", written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
