"""Statistik diagnostik R3: Q0, median + CI bootstrap cluster-hari, paruh.

Kriteria 4-syarat D2-6 dihitung sebagai ANGKA diagnostik per sel
(median pooled, CI, tanda paruh, failure map) — TANPA vonis per
keluarga. Tidak ada p-value untuk seleksi.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

SEED = 1337
N_BOOT = 10000
Q0_GATE = 300
HALF_SPLIT = "2026-05-18"


def q0_gate(counts: dict) -> dict:
    """Terapkan gerbang kapasitas 300 per sel; kembalikan status per sel."""
    return {cell: ("PASS" if n >= Q0_GATE else "DROP") for cell, n in counts.items()}


def bootstrap_median_ci(values: np.ndarray, days: np.ndarray) -> tuple:
    """CI 95% median via bootstrap cluster-hari (seed beku 1337)."""
    rng = np.random.default_rng(SEED)
    uniq = np.unique(days)
    day_idx = np.searchsorted(uniq, days)
    medians = np.empty(N_BOOT)
    for b in range(N_BOOT):
        pick = rng.integers(0, len(uniq), size=len(uniq))
        sample = np.concatenate([np.flatnonzero(day_idx == d) for d in pick])
        medians[b] = np.median(values[sample])
    return (
        float(np.median(values)),
        float(np.quantile(medians, 0.025)),
        float(np.quantile(medians, 0.975)),
    )


def halves_signs(frame: pd.DataFrame) -> dict:
    """Median net-obs per paruh + tanda (batas paruh disalin dari spec)."""
    first = frame[frame["t0"] <= HALF_SPLIT + "T23:59:59+0000"]
    second = frame[frame["t0"] > HALF_SPLIT + "T23:59:59+0000"]
    out = {}
    for name, part in (("H1", first), ("H2", second)):
        med = float(part["net_obs"].median()) if len(part) else float("nan")
        out[name] = {"n": int(len(part)), "median_net_obs": med}
    return out


def cell_diagnostic(frame: pd.DataFrame) -> dict:
    """Empat angka diagnostik D2-6 untuk satu sel (tanpa vonis)."""
    vals = frame["net_obs"].to_numpy("float64")
    days = frame["broker_day"].to_numpy()
    med, lo, hi = bootstrap_median_ci(vals, days)
    res_counts = frame["res"].value_counts().to_dict()
    total = len(frame)
    return {
        "n_eval": total,
        "median_net_obs": med,
        "ci95_lo": lo,
        "ci95_hi": hi,
        "median_net_cons": float(frame["net_cons"].median()),
        "median_net_stress": float(frame["net_stress"].median()),
        "median_gross": float(frame["gross"].median()),
        "mean_net_obs": float(frame["net_obs"].mean()),
        "share": {k: float(v) / total for k, v in res_counts.items()},
        "halves": halves_signs(frame),
        "median_sl_pips": float(frame["sl_pips"].median()),
        "median_tp_pips": float(frame["tp_pips"].median()),
    }


def summarize(records: list, cancels: list, counts: dict) -> dict:
    """Rakit ringkasan diagnostik per sel + failure map + total."""
    live = [r for r in records if r["cancel"] == ""]
    frame = pd.DataFrame([r for r in live if r["res"] != "AMBIGUOUS"])
    ambig = pd.DataFrame([r for r in live if r["res"] == "AMBIGUOUS"])
    eval_counts = frame["cell"].value_counts().to_dict()
    gate = q0_gate({c: int(eval_counts.get(c, 0)) for c in sorted(eval_counts)})
    cells = {}
    for cell in sorted(frame["cell"].unique()):
        part = frame[frame["cell"] == cell]
        cells[cell] = cell_diagnostic(part)
        cells[cell]["q0"] = gate.get(cell, "DROP")
        cells[cell]["n_ambig"] = int((ambig["cell"] == cell).sum())
    cancel_cells: dict = {}
    for _, cell, _, _, reason in cancels:
        cancel_cells.setdefault(cell, {}).setdefault(reason, 0)
        cancel_cells[cell][reason] += 1
    return {
        "q0_gate": Q0_GATE,
        "q0_status": gate,
        "cells": cells,
        "cancel_by_cell": cancel_cells,
        "cancel_sequential": counts,
        "n_ambig_total": int(len(ambig)),
        "n_eval_total": int(len(frame)),
        "n_cancel_total": int(len(cancels)),
    }
