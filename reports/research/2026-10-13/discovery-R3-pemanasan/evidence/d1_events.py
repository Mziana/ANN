"""Pindai event E1/E2/E3 di M1 2026 + negasi side (perubahan R3 #1).

Definisi event = R1 D-1 verbatim (via spec R2 D2-1). Satu-satunya delta
R3: sesudah scan, ``side -> -side`` dalam satu operasi; logika scan
E1/E2/E3 tidak diubah apa pun.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

PIP = 0.01
PROJECT_ROOT = Path(__file__).resolve().parents[5]

ANOM_START = pd.Timestamp("2026-03-10", tz="UTC")
ANOM_END = pd.Timestamp("2026-03-28", tz="UTC")

E1_N = (4, 5, 6)
E1_D = (2.5, 3.5)
E2_LOOKBACK = 20
E2_RETRACE = 0.40
E2_PULLBACK_MAX = 5
E3_WINDOW = 30
E3_REF_WINDOWS = 20
E3_RATIO = 0.5
E3_BREAK_PIP = 1.0

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
EXPECTED_FP = (
    "Tokyo:Asia/Tokyo:9-18|London:Europe/London:8-16|New York:America/New_York:8-17"
    "|Sydney:Australia/Sydney:8-16|priority=London>NewYork>Tokyo>Sydney"
)


def session_labels(utc: pd.Series) -> pd.Series:
    """Label sesi eksklusif (definisi terkunci proyek, sidik jari dicek)."""
    fp = (
        "|".join(f"{s['name']}:{s['zone']}:{s['start']}-{s['end']}" for s in SESSION_SPECS.values())
        + "|priority="
        + ">".join(label for _, label in SESSION_PRIORITY)
    )
    assert fp == EXPECTED_FP, "definisi sesi menyimpang dari kontrak"
    flags = {}
    for col, spec in SESSION_SPECS.items():
        hr = utc.dt.tz_convert(spec["zone"]).dt.hour
        flags[col] = (hr >= spec["start"]) & (hr < spec["end"])
    frame = pd.DataFrame(flags, index=utc.index)
    conds = [frame[c] for c, _ in SESSION_PRIORITY]
    labels = [label for _, label in SESSION_PRIORITY]
    return pd.Series(np.select(conds, labels, default="Off"), index=utc.index)


def load_m1() -> pd.DataFrame:
    """Muat M1 2026 + kolom UTC; assert jumlah bar = spec D2-3."""
    path = PROJECT_ROOT / "data/processed/M1/usdjpy_m1_2026.parquet"
    frame = pd.read_parquet(path)
    assert len(frame) == 269846, "jumlah bar menyimpang dari spec"
    frame = frame.copy()
    frame["utc"] = pd.to_datetime(frame["time"], utc=True)
    assert bool(frame["utc"].is_monotonic_increasing), "M1 tidak terurut"
    return frame


def anomaly_mask(utc: pd.Series) -> np.ndarray:
    """Mask bar dalam jendela anomali 2026-03-10..03-27 (tanggal UTC)."""
    return ((utc >= ANOM_START) & (utc < ANOM_END)).to_numpy()


def compute_atr_m5(frame: pd.DataFrame, exclude: np.ndarray) -> np.ndarray:
    """ATR M5(14) kausal, resep _build_eda06.py:500-533 verbatim."""
    src = frame.loc[~exclude, ["utc", "high", "low", "close"]]
    m5 = (
        src.assign(bucket=src["utc"].dt.floor("5min"))
        .groupby("bucket", sort=True)
        .agg(h=("high", "max"), l=("low", "min"), c=("close", "last"), n=("close", "size"))
        .reset_index()
    )
    m5 = m5[m5["n"] >= 3].reset_index(drop=True)
    contig = m5["bucket"].diff() == pd.Timedelta(minutes=5)
    prev_c = m5["c"].shift(1)
    tr = pd.concat(
        [
            m5["h"] - m5["l"],
            (m5["h"] - prev_c).abs().where(contig),
            (m5["l"] - prev_c).abs().where(contig),
        ],
        axis=1,
    ).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean()
    span_ok = (m5["bucket"] - m5["bucket"].shift(13)) <= pd.Timedelta(minutes=100)
    m5["atr"] = atr.where(span_ok)
    m5["avail"] = m5["bucket"] + pd.Timedelta(minutes=5)
    left = pd.DataFrame({"T": frame["utc"] + pd.Timedelta(minutes=1)})
    right = m5.loc[m5["atr"].notna(), ["avail", "atr"]].sort_values("avail")
    merged = pd.merge_asof(
        left,
        right,
        left_on="T",
        right_on="avail",
        direction="backward",
        tolerance=pd.Timedelta(minutes=15),
    )
    return (merged["atr"] / PIP).to_numpy("float64")


def compute_atr_m1(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, step_ok: np.ndarray
) -> np.ndarray:
    """ATR(14) kausal di grid M1 untuk filter expansion E2.

    Judgment implementasi (dicatat di ledger run): TR tiga-komponen
    max dengan guard kontiguitas 60 detik, lalu rolling-mean 14
    (min_periods 14). Nilai pada bar e hanya memakai bar <= e.
    """
    prev_c = np.roll(close, 1)
    prev_c[0] = np.nan
    tr = np.maximum(high - low, np.abs(high - prev_c), np.abs(low - prev_c))
    tr[~step_ok] = np.nan
    return pd.Series(tr).rolling(14, min_periods=14).mean().to_numpy("float64")


def scan_e1(
    op: np.ndarray, hi: np.ndarray, lo: np.ndarray, cl: np.ndarray, t0_ok: np.ndarray
) -> list:
    """Pindai 6 sel E1; tiap sel independen (bersarang dibiarkan)."""
    n = len(cl)
    up = np.zeros(n, dtype=bool)
    up[1:] = cl[1:] > cl[:-1]
    down = np.zeros(n, dtype=bool)
    down[1:] = cl[1:] < cl[:-1]
    rng = hi - lo
    body = cl - op
    events = []
    for legs in E1_N:
        up_run = pd.Series(up.astype(int)).rolling(legs, min_periods=legs).sum().to_numpy() == legs
        down_run = (
            pd.Series(down.astype(int)).rolling(legs, min_periods=legs).sum().to_numpy() == legs
        )
        for dist in E1_D:
            for t0 in range(legs + 1, n):
                if not t0_ok[t0]:
                    continue
                if rng[t0] <= 0 or abs(body[t0]) / rng[t0] < 0.5:
                    continue
                if (
                    up_run[t0 - 1]
                    and body[t0] < 0
                    and (cl[t0 - 1] - cl[t0 - legs - 1]) >= dist * PIP
                ):
                    events.append((t0, f"E1_N{legs}_D{dist}", -1))
                elif (
                    down_run[t0 - 1]
                    and body[t0] > 0
                    and (cl[t0 - legs - 1] - cl[t0 - 1]) >= dist * PIP
                ):
                    events.append((t0, f"E1_N{legs}_D{dist}", 1))
    return events


def scan_e2(
    cl: np.ndarray, hi: np.ndarray, lo: np.ndarray, atr_m1: np.ndarray, t0_ok: np.ndarray
) -> list:
    """Pindai 1 sel E2 (expansion 20 bar + pullback <=40% <=5 bar)."""
    n = len(cl)
    disp = cl[E2_LOOKBACK:] - cl[:-E2_LOOKBACK]
    events = []
    for e in range(E2_LOOKBACK, n - 1):
        if not np.isfinite(atr_m1[e]):
            continue
        signed = disp[e - E2_LOOKBACK]
        if abs(signed) < atr_m1[e] or signed == 0:
            continue
        push = 1 if signed > 0 else -1
        window_hi = hi[e - E2_LOOKBACK + 1 : e + 1].max()
        window_lo = lo[e - E2_LOOKBACK + 1 : e + 1].min()
        span = window_hi - window_lo
        if span <= 0:
            continue
        for j in range(e + 1, min(e + 1 + E2_PULLBACK_MAX + 1, n)):
            if not t0_ok[j]:
                continue
            adverse = (cl[e] - cl[j]) * push
            if adverse > E2_RETRACE * span:
                break
            if (cl[j] - cl[j - 1]) * push > 0:
                events.append((j, "E2", push))
                break
    return events


def scan_e3(
    cl: np.ndarray, hi: np.ndarray, lo: np.ndarray, utc: pd.Series, t0_ok: np.ndarray
) -> list:
    """Pindai 1 sel E3 (kompresi 30 bar + break tutup >= 1 pip)."""
    series_hi = pd.Series(hi)
    series_lo = pd.Series(lo)
    high30 = series_hi.rolling(E3_WINDOW, min_periods=E3_WINDOW).max().to_numpy()
    low30 = series_lo.rolling(E3_WINDOW, min_periods=E3_WINDOW).min().to_numpy()
    range30 = high30 - low30
    span_ok = utc.diff(E3_WINDOW - 1).dt.total_seconds().to_numpy() == (E3_WINDOW - 1) * 60
    range30[~span_ok] = np.nan
    ref = pd.Series(range30).shift(1).rolling(E3_REF_WINDOWS, min_periods=E3_REF_WINDOWS)
    ref_med = ref.median().to_numpy()
    events = []
    for t0 in range(E3_WINDOW + E3_REF_WINDOWS, len(cl)):
        if not t0_ok[t0] or not np.isfinite(range30[t0 - 1]) or not np.isfinite(ref_med[t0 - 1]):
            continue
        if range30[t0 - 1] > E3_RATIO * ref_med[t0 - 1]:
            continue
        if cl[t0] >= high30[t0 - 1] + E3_BREAK_PIP * PIP:
            events.append((t0, "E3", 1))
        elif cl[t0] <= low30[t0 - 1] - E3_BREAK_PIP * PIP:
            events.append((t0, "E3", -1))
    return events


def negate_side(events: list) -> list:
    """Perubahan R3 #1: side -> -side, satu operasi sesudah scan."""
    return [(t0, cell, side, -side) for t0, cell, side in events]


def apply_exclusions(
    events: list, utc_ns: np.ndarray, anom: np.ndarray, atr: np.ndarray, sessions: np.ndarray
) -> tuple:
    """Buang berurutan GAP -> ANOMALY_CROSS -> ATR_NA -> OFF_SESSION."""
    n = len(utc_ns)
    evaluable = []
    cancels: list = []
    counts = {"GAP": 0, "ANOMALY_CROSS": 0, "ATR_NA": 0, "OFF_SESSION": 0}
    for t0, cell, side_scan, side in events:
        if t0 + 11 >= n or bool((np.diff(utc_ns[t0 : t0 + 12]) != 60_000_000_000).any()):
            counts["GAP"] += 1
            cancels.append((t0, cell, side_scan, side, "GAP"))
        elif bool(anom[t0 : t0 + 12].any()):
            counts["ANOMALY_CROSS"] += 1
            cancels.append((t0, cell, side_scan, side, "ANOMALY_CROSS"))
        elif not np.isfinite(atr[t0]):
            counts["ATR_NA"] += 1
            cancels.append((t0, cell, side_scan, side, "ATR_NA"))
        elif sessions[t0 + 1] == "Off":
            counts["OFF_SESSION"] += 1
            cancels.append((t0, cell, side_scan, side, "OFF_SESSION"))
        else:
            evaluable.append((t0, cell, side_scan, side))
    return evaluable, cancels, counts
