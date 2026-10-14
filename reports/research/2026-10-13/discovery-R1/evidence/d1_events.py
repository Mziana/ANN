"""Pemindai event E1/E2/E3 Discovery-R1, 2024 saja.

Definisi mengikat = ledger pra-run 00_ledger_prarun.md. Semua fitur hanya
memakai bar yang selesai pada/saat t0 close (tanpa intip masa depan).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "notebooks" / "scalping"))
from _eda_common import EXPECTED_FINGERPRINT, add_labels, session_fingerprint

logger = logging.getLogger(__name__)

PIP = 0.01
ANOM_START = "2024-10-28"
ANOM_END = "2024-11-01"
E1_GRID = [(4, 2.5), (4, 3.5), (5, 2.5), (5, 3.5), (6, 2.5), (6, 3.5)]


def load_m1(path: str) -> pd.DataFrame:
    """Muat parquet M1 2024 + kolom UTC + sesi eksklusif + sidik sesi.

    Args:
        path: Path parquet M1 2024.

    Returns:
        Frame terurut dengan kolom utc, broker_raw, o/h/l/c, spread, sesi.
    """
    df = pd.read_parquet(path).sort_values("broker_time_raw").reset_index(drop=True)
    df["utc"] = pd.to_datetime(df["time"], utc=True)
    assert str(session_fingerprint()) == EXPECTED_FINGERPRINT, "definisi sesi drift"
    df = add_labels(df.rename(columns={"utc": "utc"}).assign(utc=df["utc"]))
    df = df.rename(
        columns={
            "open": "o",
            "high": "h",
            "low": "l",
            "close": "c",
            "spread_pips": "spread",
            "broker_time_raw": "raw",
        }
    )
    df["day"] = df["utc"].dt.strftime("%Y-%m-%d")
    return df


def add_atr14(df: pd.DataFrame) -> pd.DataFrame:
    """ATR(14) Wilder atas true range; nilai bar-i hanya pakai bar ≤ i.

    Args:
        df: Frame keluaran load_m1.

    Returns:
        Frame + kolom atr14.
    """
    prev_c = df["c"].shift(1)
    tr = pd.concat(
        [df["h"] - df["l"], (df["h"] - prev_c).abs(), (df["l"] - prev_c).abs()],
        axis=1,
    ).max(axis=1)
    df["atr14"] = tr.ewm(alpha=1.0 / 14.0, adjust=False).mean()
    return df


def scan_e1(df: pd.DataFrame, n: int, d: float) -> pd.DataFrame:
    """Satu sel E1: N tutup searah + displacement ≥ D + t0 reversal berbody.

    Args:
        df: Frame + ATR (ATR tak dipakai E1, hanya keseragaman).
        n: Panjang run (4/5/6).
        d: Ambang displacement pip (2,5/3,5).

    Returns:
        Event (t0_pos, side); side = arah bar t0.
    """
    o = df["o"].to_numpy()
    h = df["h"].to_numpy()
    low = df["l"].to_numpy()
    c = df["c"].to_numpy()
    up = c > o
    dn = c < o
    run_up = pd.Series(up).rolling(n).sum().to_numpy() == n
    run_dn = pd.Series(dn).rolling(n).sum().to_numpy() == n
    body = c - o
    rng = h - low
    rows = []
    for i in range(n, len(df)):
        t0_up = body[i] > 0 and rng[i] > 0 and body[i] >= 0.5 * rng[i]
        t0_dn = body[i] < 0 and rng[i] > 0 and -body[i] >= 0.5 * rng[i]
        if run_up[i - 1] and (c[i - 1] - o[i - n]) / PIP >= d and t0_dn:
            rows.append((i, -1))
        if run_dn[i - 1] and (o[i - n] - c[i - 1]) / PIP >= d and t0_up:
            rows.append((i, 1))
    return pd.DataFrame(rows, columns=["t0_pos", "side"])


def _e2_retrace_ok(
    up_push: np.ndarray,
    hi20: np.ndarray,
    lo20: np.ndarray,
    low: np.ndarray,
    high: np.ndarray,
    i: int,
    e: int,
) -> bool:
    """Retrace maks adverse atas bar e+1..i ≤ 40% range expansion.

    Args:
        up_push: Arah push True = naik.
        hi20: High maks window expansion per e.
        lo20: Low min window expansion per e.
        low: Array low.
        high: Array high.
        i: Posisi t0.
        e: Posisi akhir expansion.

    Returns:
        True bila retrace dalam batas.
    """
    rng = hi20[e] - lo20[e]
    if rng <= 0:
        return False
    adverse = hi20[e] - low[e + 1 : i + 1].min() if up_push else high[e + 1 : i + 1].max() - lo20[e]
    return bool(adverse <= 0.40 * rng)


def scan_e2(df: pd.DataFrame) -> pd.DataFrame:
    """Satu sel E2: expansion 20 bar ≥ ATR14 + pullback ≤40%/≤5 bar.

    Args:
        df: Frame + atr14.

    Returns:
        Event (t0_pos, side, e_pos); e terdekat dipakai bila ganda.
    """
    o = df["o"].to_numpy()
    h = df["h"].to_numpy()
    low = df["l"].to_numpy()
    c = df["c"].to_numpy()
    atr = df["atr14"].to_numpy()
    disp = c - np.roll(c, 20)
    disp[:20] = np.nan
    hi20 = pd.Series(h).rolling(20).max().to_numpy()
    lo20 = pd.Series(low).rolling(20).min().to_numpy()
    valid = np.abs(disp) >= atr
    push_up = disp > 0
    rows = []
    for i in range(25, len(df)):
        t0_up = c[i] > o[i]
        t0_dn = c[i] < o[i]
        for length in (1, 2, 3, 4, 5):
            e = i - length
            if e < 20 or not valid[e]:
                continue
            if push_up[e] and not t0_up:
                continue
            if not push_up[e] and not t0_dn:
                continue
            if _e2_retrace_ok(push_up[e], hi20, lo20, low, h, i, e):
                rows.append((i, 1 if push_up[e] else -1, e))
                break
    return pd.DataFrame(rows, columns=["t0_pos", "side", "e_pos"])


def scan_e3(df: pd.DataFrame) -> pd.DataFrame:
    """Satu sel E3: kompresi 30 bar + break t0 ≥ 1,0 pip dari edge.

    Args:
        df: Frame M1 2024.

    Returns:
        Event (t0_pos, side).
    """
    h = df["h"].to_numpy()
    low = df["l"].to_numpy()
    c = df["c"].to_numpy()
    hi30 = pd.Series(h).rolling(30).max().to_numpy()
    lo30 = pd.Series(low).rolling(30).min().to_numpy()
    rng30 = hi30 - lo30
    past = np.column_stack([np.roll(rng30, 30 * j) for j in range(1, 21)])
    med = np.median(past, axis=1)
    rows = []
    for i in range(630, len(df)):
        if np.isnan(med[i - 1]) or rng30[i - 1] > 0.5 * med[i - 1]:
            continue
        if c[i] >= hi30[i - 1] + 1.0 * PIP:
            rows.append((i, 1))
        elif c[i] <= lo30[i - 1] - 1.0 * PIP:
            rows.append((i, -1))
    return pd.DataFrame(rows, columns=["t0_pos", "side"])


def apply_exclusions(df: pd.DataFrame, ev: pd.DataFrame) -> pd.DataFrame:
    """Buang event t0 di jendela anomali 2024-10-28..11-01 (UTC).

    Args:
        df: Frame M1 (sumber tanggal t0).
        ev: Event mentah.

    Returns:
        Event bersih + kolom day/session/spread t0.
    """
    ev = ev.copy()
    ev["day"] = df["day"].to_numpy()[ev["t0_pos"].to_numpy()]
    ev["session"] = df["session_label"].to_numpy()[ev["t0_pos"].to_numpy()]
    ev["spread_t0"] = df["spread"].to_numpy()[ev["t0_pos"].to_numpy()]
    ev["t0_utc"] = df["time"].to_numpy()[ev["t0_pos"].to_numpy()]
    keep = ~((ev["day"] >= ANOM_START) & (ev["day"] <= ANOM_END))
    return ev[keep].reset_index(drop=True)
