"""Orkestrasi run Discovery-R2 2026-holdout: event → ATR → outcome → Q0-Q5 → segel."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[5]
        / "reports"
        / "research"
        / "2026-10-13"
        / "discovery-R2"
        / "evidence"
    ),
)

import pandas as pd
from d1_events import (
    ANOM_END,
    ANOM_START,
    E1_GRID,
    add_atr14,
    apply_exclusions,
    compute_atr_m5,
    load_m1,
    scan_e1,
    scan_e2,
    scan_e3,
)
from d2_outcomes import evaluate
from d3_stats import cell_verdict, failure_map, q0_gate
from d4_appendix import seal

from src.data.broker_time import BrokerSchedule
from src.utils.config import load_config

EVIDENCE = Path(__file__).resolve().parent
M1_2026 = "data/processed/M1/usdjpy_m1_2026.parquet"
logger = logging.getLogger("discovery-R2")


def setup_logging() -> None:
    """Logging ganda: konsol + berkas UTF-8 (logging gagal = run gagal)."""
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    file_handler = logging.FileHandler(EVIDENCE / "run_stdout.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])


def anomaly_mask(df: pd.DataFrame) -> np.ndarray:
    """Mask bar anomali 2026-03-10..03-27 (hari UTC)."""
    day = df["day"].to_numpy()
    return (day >= ANOM_START) & (day <= ANOM_END)


def check_atr_causal(df: pd.DataFrame, exclude: np.ndarray, atr: np.ndarray) -> None:
    """ATR di 2 indeks tetap identik bila hanya memakai data sampai T."""
    n = len(df)
    for i in (n // 3, 2 * n // 3):
        part = df.iloc[: i + 1]
        redo = compute_atr_m5(part, exclude[: i + 1])
        np.testing.assert_allclose(redo[-1], atr[i], rtol=1e-9, equal_nan=True)
    logger.info("PASS: ATR kausal di 2 indeks tetap identik (tanpa look-ahead)")


def collect_events(df: pd.DataFrame, atr: np.ndarray) -> pd.DataFrame:
    """Pindai 8 sel + eksklusi anomali; tempel ATR beku + hari broker.

    Args:
        df: Frame M1 + ATR14.
        atr: ATR M5(14) pip selaras df (NaN = tak tersedia).

    Returns:
        Event semua sel + kolom atr/broker_day.
    """
    parts = []
    for n, d in E1_GRID:
        ev = scan_e1(df, n, d)
        ev["family"], ev["cell"] = "E1", f"N{n}-D{d}"
        parts.append(apply_exclusions(df, ev))
    ev = scan_e2(df)
    ev["family"], ev["cell"] = "E2", "single"
    parts.append(apply_exclusions(df, ev))
    ev = scan_e3(df)
    ev["family"], ev["cell"] = "E3", "single"
    parts.append(apply_exclusions(df, ev))
    all_ev = pd.concat(parts, ignore_index=True)
    pos = all_ev["t0_pos"].to_numpy(dtype=np.int64)
    all_ev["atr"] = atr[pos]
    wall = pd.to_datetime(df["raw"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
    all_ev["broker_day"] = wall.to_numpy()[pos]
    return all_ev


def _verdict_cells(rec: pd.DataFrame, q0: pd.DataFrame, summary: dict) -> None:
    """Vonis per sel (Q0→Q5 + failure map) ke summary + log."""
    for _, row in q0.iterrows():
        fam, cell = row["family"], row["cell"]
        key = f"{fam}/{cell}"
        grp = rec[(rec["family"] == fam) & (rec["cell"] == cell) & (rec["cancel"] == "")]
        if not row["lolos_q0"]:
            summary["cells"][key] = {"vonis": "DROPPED-Q0", "n_eval": int(row["n_eval"])}
            logger.info("%s DROPPED-Q0 (n_eval=%d)", key, row["n_eval"])
            continue
        verdict = cell_verdict(grp)
        verdict["vonis"] = "KANDIDAT" if verdict["lolos"] else "TOLAK"
        verdict["failure"] = failure_map(rec[(rec["family"] == fam) & (rec["cell"] == cell)])
        summary["cells"][key] = verdict
        logger.info(
            "%s n=%d med=%.4f ci_lo=%.4f h1=%.4f h2=%.4f %s",
            key,
            verdict["n"],
            verdict["median"],
            verdict["ci_lo"],
            verdict["med_h1"],
            verdict["med_h2"],
            verdict["vonis"],
        )


def _verdict_family(rec: pd.DataFrame, summary: dict) -> None:
    """Vonis sementara per keluarga (final = arsitek)."""
    for fam in rec["family"].unique():
        fam_cells = [k for k in summary["cells"] if k.startswith(fam + "/")]
        subs = [k for k in fam_cells if summary["cells"][k].get("vonis") == "KANDIDAT"]
        dropped = [k for k in fam_cells if summary["cells"][k].get("vonis") == "DROPPED-Q0"]
        if subs:
            prov = f"KANDIDAT-sementara {list(subs)}"
        elif dropped and len(dropped) == len(fam_cells):
            prov = "TOLAK-sementara (semua sel dropped-Q0)"
        else:
            prov = "TOLAK-sementara (nol sel lolos 4-syarat)"
        summary["family"][fam] = prov
        logger.info("keluarga %s: %s (final = arsitek)", fam, prov)


def main() -> int:
    """Jalankan discovery 2026-holdout penuh + segel lampiran D-8 R2."""
    setup_logging()
    logger.info("discovery-R2 mulai (2026-holdout, paket ATR tunggal beku)")
    df = add_atr14(load_m1(M1_2026))
    logger.info("M1 2026: %d bar (%s .. %s)", len(df), df["time"].iloc[0], df["time"].iloc[-1])
    anom = anomaly_mask(df)
    logger.info("bar anomali 2026-03-10..03-27: %d (keluar denominator)", int(anom.sum()))
    atr = compute_atr_m5(df, anom)
    logger.info("ATR tersedia: %d dari %d bar", int(np.isfinite(atr).sum()), len(df))
    ok_atr = atr[np.isfinite(atr)]
    logger.info(
        "ATR mean=%.3f median=%.3f pip; SL~=%.0f TP~=%.0f point",
        float(ok_atr.mean()),
        float(np.median(ok_atr)),
        float(ok_atr.mean()) * 150,
        float(ok_atr.mean()) * 300,
    )
    check_atr_causal(df, anom, atr)
    ev = collect_events(df, atr)
    logger.info("event pasca-eksklusi-t0: %d", len(ev))
    rec = evaluate(df, ev, anom)
    rec.to_json(EVIDENCE / "events.jsonl", orient="records", lines=True)
    logger.info("events.jsonl: %d rekaman", len(rec))
    logger.info("cancel: %s", rec["cancel"].value_counts().to_dict())
    logger.info("sesi-2026: %s", rec["session"].value_counts().to_dict())

    q0 = q0_gate(rec)
    logger.info("Q0:\n%s", q0.to_string(index=False))
    summary = {"q0": q0.to_dict(orient="records"), "cells": {}, "family": {}}
    _verdict_cells(rec, q0, summary)
    _verdict_family(rec, summary)

    with open(EVIDENCE / "summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, default=str)
    cfg = load_config("data")
    sched = BrokerSchedule.from_config(cfg["mt5"])
    digest = seal(
        df, ev, sched, int(cfg["mt5"]["price_digits"]), str(EVIDENCE / "appendix_D8.sealed.json")
    )
    logger.info("lampiran D-8 R2 DISEGEL sha256=%s (jangan dibuka)", digest)
    with open(EVIDENCE / "seal.txt", "w", encoding="utf-8") as fh:
        fh.write(f"appendix_D8.sealed.json sha256={digest}\n")
    logger.info("discovery-R2 selesai")
    return 0


if __name__ == "__main__":
    sys.exit(main())
