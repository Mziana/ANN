"""Definisi bersama rantai notebook EDA (implementasi verbatim dari Notebook 00).

Notebook 00 adalah sumber tunggal definisi sesi (Rancangan EDA v3). Notebook tidak bisa
di-impor sebagai modul, jadi definisi yang sudah terkunci di sana diekstrak ke sini agar
nb01-nb05 tidak mengimplementasikan ulang (risiko drift definisi — pelajaran SA-03).

File ini berada di `notebooks/`, bukan `src/`, sehingga tidak melanggar larangan membuat
modul baru di `src/`. Isinya SALINAN dari sel Notebook 00; kalau Notebook 00 berubah,
sel ini harus berubah bersamaan.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

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

CROSS_TAB_HOURS = {
    "is_tokyo": (0, 9),
    "is_london": (8, 16),
    "is_ny": (13, 22),
    "is_sydney": (21, 6),
}

SESSION_ORDER = ["London", "NewYork", "Tokyo", "Sydney", "Off"]


def session_flags(utc: pd.Series) -> pd.DataFrame:
    """Flag sesi DST-aware (primer) dari series UTC tz-aware.

    Args:
        utc: Series bertipe datetime64[ns, UTC].

    Returns:
        DataFrame boolean berkolom is_tokyo, is_london, is_ny, is_sydney.
    """
    flags = {}
    for column, spec in SESSION_SPECS.items():
        local_hour = utc.dt.tz_convert(spec["zone"]).dt.hour
        flags[column] = (local_hour >= spec["start"]) & (local_hour < spec["end"])
    return pd.DataFrame(flags, index=utc.index)


def cross_tab_flags(utc: pd.Series) -> pd.DataFrame:
    """Flag sesi UTC-tetap (cross-tab pembanding campuran-musim) dari series UTC."""
    hour = utc.dt.hour
    flags = {}
    for column, (start, end) in CROSS_TAB_HOURS.items():
        if start < end:
            flags[column] = (hour >= start) & (hour < end)
        else:
            flags[column] = (hour >= start) | (hour < end)
    return pd.DataFrame(flags, index=utc.index)


def exclusive_label(flags: pd.DataFrame) -> pd.Series:
    """Label eksklusif: prioritas London > NewYork > Tokyo > Sydney > Off."""
    conditions = [flags[column] for column, _ in SESSION_PRIORITY]
    choices = [label for _, label in SESSION_PRIORITY]
    return pd.Series(
        np.select(conditions, choices, default="Off"), index=flags.index, name="session_label"
    )


def add_labels(frame: pd.DataFrame) -> pd.DataFrame:
    """Tambahkan flag sesi primer, cross-tab, dan label eksklusif ke frame.

    Args:
        frame: Frame dengan kolom 'utc'.

    Returns:
        Salinan frame dengan is_tokyo/is_london/is_ny/is_sydney,
        session_label, dan session_label_xtab.
    """
    out = frame.copy()
    primary = session_flags(out["utc"])
    cross = cross_tab_flags(out["utc"])
    for column in primary.columns:
        out[column] = primary[column]
    for column in cross.columns:
        out[f"{column}_xtab"] = cross[column]
    out["session_label"] = exclusive_label(primary)
    out["session_label_xtab"] = exclusive_label(cross)
    return out


def session_fingerprint() -> str:
    """Kembalikan sidik jari definisi sesi untuk assertion drift antar-notebook."""
    parts = [
        f"{spec['name']}:{spec['zone']}:{spec['start']}-{spec['end']}"
        for spec in SESSION_SPECS.values()
    ]
    parts.append("priority=" + ">".join(label for _, label in SESSION_PRIORITY))
    parts.append("xtab=" + ",".join(f"{k}:{v[0]}-{v[1]}" for k, v in CROSS_TAB_HOURS.items()))
    return "|".join(parts)


EXPECTED_FINGERPRINT = (
    "Tokyo:Asia/Tokyo:9-18|London:Europe/London:8-16|New York:America/New_York:8-17"
    "|Sydney:Australia/Sydney:8-16|priority=London>NewYork>Tokyo>Sydney"
    "|xtab=is_tokyo:0-9,is_london:8-16,is_ny:13-22,is_sydney:21-6"
)
