"""Statistik Q0-Q5 + bootstrap cluster-hari + kriteria KANDIDAT R2.

Setting evaluasi beku: H+10 race SESUDAH bar entry, paket ATR tunggal
(SL=1,5xATR/TP=2,0xSL), observed net. Kriteria D2-6 4-syarat per sel;
coder melapor angka + vonis sementara per keluarga (final = arsitek).
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

BOOT_RESAMPLES = 10_000
BOOT_SEED = 1337
Q0_MIN = 300
EVAL_NET = "BATR_net_obs"
HALF_CUT = "2026-05-19"


def q0_gate(rec: pd.DataFrame) -> pd.DataFrame:
    """Gerbang kapasitas: sel evaluable (tanpa cancel) >= 300 event.

    Args:
        rec: Rekaman event-level.

    Returns:
        Ringkasan per sel: n_raw, n_eval, lolos_q0.
    """
    rows = []
    for (fam, cell), grp in rec.groupby(["family", "cell"]):
        n_raw = len(grp)
        n_eval = int((grp["cancel"] == "").sum())
        rows.append(
            {
                "family": fam,
                "cell": cell,
                "n_raw": n_raw,
                "n_eval": n_eval,
                "lolos_q0": n_eval >= Q0_MIN,
            }
        )
    return pd.DataFrame(rows)


def bootstrap_median(values: np.ndarray, days: np.ndarray) -> tuple[float, float]:
    """CI 95% median pooled via bootstrap jaga-cluster hari, seed 1337.

    Args:
        values: Net-observed paket ATR per event.
        days: Id hari per event (sejajar values).

    Returns:
        (median_pooled, ci_bawah_2.5%) atas event non-ambigu (NaN dibuang).
    """
    mask = ~np.isnan(values)
    values = values[mask]
    days = days[mask]
    rng = np.random.default_rng(BOOT_SEED)
    uniq = np.unique(days)
    per_day = [values[days == d] for d in uniq]
    med = float(np.median(values))
    boots = np.empty(BOOT_RESAMPLES)
    for b in range(BOOT_RESAMPLES):
        pick = rng.integers(0, len(uniq), len(uniq))
        boots[b] = np.median(np.concatenate([per_day[k] for k in pick]))
    return med, float(np.percentile(boots, 2.5))


def cell_verdict(grp: pd.DataFrame) -> dict:
    """Empat syarat D2-6 atas satu sel (setting beku R2).

    Args:
        grp: Event evaluable satu sel.

    Returns:
        Kamus angka + lolos per syarat + vonis sementara sel.
    """
    vals = grp[EVAL_NET].to_numpy()
    days = grp["day"].to_numpy()
    med, ci_lo = bootstrap_median(vals, days)
    half = grp["day"] < HALF_CUT
    med_h1 = float(np.nanmedian(vals[half])) if half.any() else float("nan")
    med_h2 = float(np.nanmedian(vals[~half])) if (~half).any() else float("nan")
    s1 = bool(med > 0)
    s2 = bool(ci_lo > 0)
    s3 = bool(np.sign(med_h1) == np.sign(med_h2) != 0)
    s4 = True
    lolos = s1 and s2 and s3 and s4
    return {
        "n": len(grp),
        "median": med,
        "ci_lo": ci_lo,
        "med_h1": med_h1,
        "med_h2": med_h2,
        "s1": s1,
        "s2": s2,
        "s3": s3,
        "s4": s4,
        "lolos": lolos,
    }


def failure_map(grp: pd.DataFrame) -> dict:
    """Peta kegagalan wajib Q4: sesi, spread, ambigu, cancel, kontribusi.

    Args:
        grp: Semua event satu sel (termasuk cancel).

    Returns:
        Kamus peta kegagalan.
    """
    ev = grp[grp["cancel"] == ""]
    by_sess = ev.groupby("session")[EVAL_NET].median().round(4).to_dict()
    amb = int((ev["BATR_res"] == "AMBIGUOUS").sum())
    cancels = grp[grp["cancel"] != ""].groupby("cancel").size().to_dict()
    day_net = ev.groupby("day")[EVAL_NET].sum()
    top_share = (
        float(day_net.abs().max() / day_net.abs().sum())
        if len(day_net) and day_net.abs().sum() > 0
        else 0.0
    )
    res_eval = ev["BATR_res"].value_counts().to_dict()
    time_share = float((ev["BATR_res"] == "TIME").mean()) if len(ev) else 0.0
    return {
        "by_session": by_sess,
        "ambiguous": amb,
        "cancels": cancels,
        "top_day_share": round(top_share, 4),
        "res_eval": res_eval,
        "time_share": round(time_share, 4),
    }
