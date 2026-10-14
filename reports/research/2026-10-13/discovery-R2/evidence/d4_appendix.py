"""Lampiran D-8 R2: 8 pola + bias M15 di 2026 — DIHITUNG lalu DISEGEL.

DILARANG membaca isi untuk keputusan, DILARANG melampirkan kesimpulan
sebelum vonis KANDIDAT R2 beku. Skrip ini hanya mencetak SHA-256 segel.
Segel R1 TIDAK dibuka, TIDAK dibaca. Resample M15 via src/data/resample.py.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.data.resample import resample_frame

logger = logging.getLogger(__name__)

PIP = 0.01


def patterns(o, h, low, c, o1, h1, low1, c1, o2, c2, med_range20: float) -> dict:
    """Delapan pola D-8.1 atas bar k vs k-1/k-2 (boolean mentah).

    Args: o/h/low/c = bar k; o1/h1/low1/c1 = bar k-1; o2/c2 = bar k-2;
        med_range20 = median range 20 bar selesai sebelum k.
    Returns: Flag P1..P8.
    """
    body, rng = c - o, h - low
    abody = abs(body)
    body1, rng1 = c1 - o1, h1 - low1
    lo_wick = min(o, c) - low
    hi_wick = h - max(o, c)
    return {
        "P1": body > 0 > body1
        and min(o, c) <= min(o1, c1)
        and max(o, c) >= max(o1, c1)
        and rng >= 1.5 * med_range20,
        "P2": abody > 0 and lo_wick >= 2 * abody and hi_wick <= 0.5 * abody and c >= (h + low) / 2,
        "P3": abody > 0 and hi_wick >= 2 * abody and lo_wick <= 0.5 * abody and c <= (h + low) / 2,
        "P4": c > c1 > c2 and (c - o) > 0 and (c1 - o1) > 0 and (c2 - o2) > 0,
        "P5": c < c1 < c2 and (c - o) < 0 and (c1 - o1) < 0 and (c2 - o2) < 0,
        "P6": rng > 0 and abody <= 0.10 * rng,
        "P7": rng1 > 0
        and min(o, c) >= min(o1, c1)
        and max(o, c) <= max(o1, c1)
        and rng <= 0.6 * rng1,
        "P8": rng > 0 and abody > 0 and (lo_wick + hi_wick) <= 0.10 * rng,
    }


def _bar_flags(o, h, low, c, med20) -> dict[str, np.ndarray]:
    """Delapan flag pola D-8.1 per bar, tervektorisasi (setara patterns()).

    Args: o/h/low/c = array bid; med20 = median range 20 bar.
    Returns: Delapan array boolean P1..P8.
    """
    body = c - o
    rng = h - low
    abody = np.abs(body)
    o1 = np.roll(o, 1)
    h1 = np.roll(h, 1)
    low1 = np.roll(low, 1)
    c1 = np.roll(c, 1)
    o2 = np.roll(o, 2)
    c2 = np.roll(c, 2)
    body1 = c1 - o1
    rng1 = h1 - low1
    lo_wick = np.minimum(o, c) - low
    hi_wick = h - np.maximum(o, c)
    return {
        "P1": (body > 0)
        & (body1 < 0)
        & (np.minimum(o, c) <= np.minimum(o1, c1))
        & (np.maximum(o, c) >= np.maximum(o1, c1))
        & (rng >= 1.5 * med20),
        "P2": (abody > 0)
        & (lo_wick >= 2 * abody)
        & (hi_wick <= 0.5 * abody)
        & (c >= (h + low) / 2),
        "P3": (abody > 0)
        & (hi_wick >= 2 * abody)
        & (lo_wick <= 0.5 * abody)
        & (c <= (h + low) / 2),
        "P4": (c > c1) & (c1 > c2) & ((c - o) > 0) & ((c1 - o1) > 0) & ((c2 - o2) > 0),
        "P5": (c < c1) & (c1 < c2) & ((c - o) < 0) & ((c1 - o1) < 0) & ((c2 - o2) < 0),
        "P6": (rng > 0) & (abody <= 0.10 * rng),
        "P7": (rng1 > 0)
        & (np.minimum(o, c) >= np.minimum(o1, c1))
        & (np.maximum(o, c) <= np.maximum(o1, c1))
        & (rng <= 0.6 * rng1),
        "P8": (rng > 0) & (abody > 0) & ((lo_wick + hi_wick) <= 0.10 * rng),
    }


def _cumsum_flags(o, h, low, c, med20) -> dict[str, np.ndarray]:
    """Flag per bar + verifikasi skalar 20 bar + cumsum jendela."""
    flags = _bar_flags(o, h, low, c, med20)
    for k in range(20, 40):
        p = patterns(
            o[k],
            h[k],
            low[k],
            c[k],
            o[k - 1],
            h[k - 1],
            low[k - 1],
            c[k - 1],
            o[k - 2],
            c[k - 2],
            med20[k - 1],
        )
        for key, val in p.items():
            assert bool(flags[key][k]) == bool(val), f"divergen pola {key} @{k}"
    logger.info("verifikasi pola-vektor-vs-skalar 20 bar: IDENTIK")
    return {
        key: np.concatenate([[0], np.cumsum(val.astype(np.int64))]) for key, val in flags.items()
    }


def _m15_bias_inputs(df, o, h, low, c, digits, sched):
    """Resample M15 + array akhir-bar, return M15, dan t0_end (int64 ns)."""
    m15_input = pd.DataFrame(
        {
            "broker_time_raw": df["raw"].to_numpy(),
            "open": o,
            "high": h,
            "low": low,
            "close": c,
            "tick_volume": df["tick_volume"].to_numpy(),
            "real_volume": df["real_volume"].to_numpy(),
            "spread_pips": df["spread"].to_numpy(),
        }
    )
    m15, _ = resample_frame(m15_input, "M15", digits, sched)
    m15_end = (
        (pd.to_datetime(m15["time"], utc=True) + pd.Timedelta(minutes=15))
        .to_numpy(dtype="datetime64[ns]")
        .astype(np.int64)
    )
    m15_ret = (m15["close"].to_numpy(dtype=float) - m15["open"].to_numpy(dtype=float)) / PIP
    t0_end = (
        (pd.to_datetime(df["time"], utc=True) + pd.Timedelta(minutes=1))
        .to_numpy(dtype="datetime64[ns]")
        .astype(np.int64)
    )
    return m15_end, m15_ret, t0_end


def _sealed_rows(ev_all, n, cs, m15_end, m15_ret, t0_end) -> dict:
    """Tabel jendela pola + bias M15 per event (tanpa baca isi)."""
    pos = ev_all["t0_pos"].to_numpy(dtype=np.int64)
    fam = ev_all["family"].to_numpy()
    cell = ev_all["cell"].to_numpy()
    side = ev_all["side"].to_numpy(dtype=np.int64)
    tstr = pd.to_datetime(ev_all["t0_utc"], utc=True).dt.strftime("%Y-%m-%dT%H:%M%z")
    keys = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")
    sealed = {"windows": [], "m15": []}
    for j in np.flatnonzero((pos >= 21) & (pos + 5 < n)):
        i = int(pos[j])
        win = {
            name: {key: int(cs[key][hi] - cs[key][lo]) for key in keys}
            for name, lo, hi in (
                ("SEBELUM", i - 5, i),
                ("SAAT", i, i + 1),
                ("SESUDAH", i + 1, i + 6),
            )
        }
        row = {"family": str(fam[j]), "cell": str(cell[j]), "t0": str(tstr.iloc[j]), "win": win}
        sealed["windows"].append(row)
        last = int(np.searchsorted(m15_end, t0_end[i], side="right")) - 1
        if last < 0:
            bias = "TAK-ADA"
        else:
            ret = float(m15_ret[last])
            if abs(ret) < 0.5:
                bias = "DATAR"
            else:
                bias = "SEARAH" if np.sign(ret) == side[j] else "BERLAWANAN"
        sealed["m15"].append({"family": str(fam[j]), "t0": str(tstr.iloc[j]), "bias": bias})
    return sealed


def seal(df: pd.DataFrame, ev_all: pd.DataFrame, sched, digits: int, out_path: str) -> str:
    """Hitung pola×jendela + M15-bias, tulis, segel (hanya SHA-256 dibaca).

    Args: df = M1; ev_all = event semua sel; sched/digits = resample M15.
    Returns: SHA-256 hex file segel.
    """
    o = df["o"].to_numpy(dtype=float)
    h = df["h"].to_numpy(dtype=float)
    low = df["l"].to_numpy(dtype=float)
    c = df["c"].to_numpy(dtype=float)
    med20 = pd.Series(h - low).rolling(20).median().to_numpy()
    cs = _cumsum_flags(o, h, low, c, med20)
    m15_end, m15_ret, t0_end = _m15_bias_inputs(df, o, h, low, c, digits, sched)
    sealed = _sealed_rows(ev_all, len(df), cs, m15_end, m15_ret, t0_end)
    blob = json.dumps(sealed).encode()
    Path(out_path).write_bytes(blob)
    return hashlib.sha256(blob).hexdigest()
