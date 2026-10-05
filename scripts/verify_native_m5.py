"""Compare our resampled M5 against the broker's own native M5 bars.

Native MT5 M5 bars are the reference. If our broker wall-clock bucketing is
right, open/high/low/close and tick volume must match bar for bar over the same
window. Any difference is either a bucketing bug or a genuine data gap.

Run: venv\\Scripts\\python.exe verify_native.py
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

# Run directly as scripts\verify_native_m5.py, so the project root has to be on
# the import path; pytest would have added it, a plain run does not.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.fetch_data import import_mt5  # noqa: E402
from src.data.resample import resample_frame  # noqa: E402
from src.utils.config import load_config  # noqa: E402

SYMBOL = "USDJPY"
BROKER_TZ = ZoneInfo("Etc/GMT-3")
START = datetime(2026, 9, 1, tzinfo=UTC)
END = datetime(2026, 9, 15, tzinfo=UTC)


def fetch_native(tf_seconds: int) -> pd.DataFrame:
    """Fetch native MT5 bars for the comparison window.

    Args:
        tf_seconds: Native timeframe length in seconds.

    Returns:
        Frame with broker epoch and OHLCV columns.

    Raises:
        RuntimeError: If MT5 cannot be initialised or returns nothing.
    """
    mt5 = import_mt5()

    if not mt5.initialize():
        raise RuntimeError(f"mt5.initialize gagal: {mt5.last_error()}")
    try:
        rates = mt5.copy_rates_range(
            SYMBOL,
            mt5.TIMEFRAME_M5 if tf_seconds == 300 else mt5.TIMEFRAME_M15,
            int(START.timestamp()),
            int(END.timestamp()),
        )
        if rates is None or len(rates) == 0:
            raise RuntimeError(f"copy_rates_range kosong: {mt5.last_error()}")
        return pd.DataFrame(rates)
    finally:
        mt5.shutdown()


def main() -> None:
    config = load_config("data")
    digits = int(config["mt5"]["price_digits"])

    native = fetch_native(300)
    print("=== NATIVE MT5 M5 ===")
    print(f"  bar     : {len(native):,}")
    print(
        f"  periode : {pd.to_datetime(native['time'].iloc[0], unit='s', utc=True)} "
        f"s/d {pd.to_datetime(native['time'].iloc[-1], unit='s', utc=True)}"
    )
    print()

    m1 = pd.read_parquet("data/processed/M1/usdjpy_m1_2026.parquet")
    lo, hi = int(START.timestamp()), int(END.timestamp())
    window = m1[(m1["broker_time_raw"] >= lo) & (m1["broker_time_raw"] < hi)]
    print("=== KITA (resample dari M1 bersih) ===")
    print(f"  bar M1  : {len(window):,}")
    print()

    mine, result = resample_frame(window, "M5", BROKER_TZ, digits)
    print("=== HASIL RESAMPLE ===")
    print(f"  bucket  : {len(mine):,}")
    print(f"  bar/bucket: {result.shortest_bucket}-{result.longest_bucket}")
    print()

    left = native.rename(columns={"time": "broker_time_raw"})[
        ["broker_time_raw", "open", "high", "low", "close", "tick_volume"]
    ].copy()
    right = mine[["broker_time_raw", "open", "high", "low", "close", "tick_volume"]].copy()
    for column in ("open", "high", "low", "close"):
        left[column] = left[column].round(digits)

    merged = left.merge(right, on="broker_time_raw", how="outer", suffixes=("_native", "_kita"))
    only_native = int(merged["close_kita"].isna().sum())
    only_mine = int(merged["close_native"].isna().sum())
    both = merged.dropna(subset=["close_native", "close_kita"])

    print("=== PERBANDINGAN BAR PER BAR ===")
    print(f"  timestamp sama      : {len(both):,}")
    print(f"  hanya di native     : {only_native}")
    print(f"  hanya di kita       : {only_mine}")
    print()

    for column in ("open", "high", "low", "close", "tick_volume"):
        a = both[f"{column}_native"]
        b = both[f"{column}_kita"]
        diff = (a != b).sum()
        worst = (a - b).abs().max() if column != "tick_volume" else (a - b).abs().max()
        print(f"  {column:11s}: beda {diff:6,} bar  selisih maks {worst}")

    print()
    if only_mine:
        sample = merged[merged["close_native"].isna()].head(5)
        print("  contoh timestamp hanya di kita:")
        for ts in sample["broker_time_raw"]:
            print("   ", pd.to_datetime(int(ts), unit="s", utc=True))
    if only_native:
        sample = merged[merged["close_kita"].isna()].head(5)
        print("  contoh timestamp hanya di native:")
        for ts in sample["broker_time_raw"]:
            print("   ", pd.to_datetime(int(ts), unit="s", utc=True))


if __name__ == "__main__":
    main()
