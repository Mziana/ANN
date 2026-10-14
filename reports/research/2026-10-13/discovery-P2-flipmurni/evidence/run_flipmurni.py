"""Pemanasan-2 flip-murni: reuse scan+race R2, negasi side, replay 1-posisi.

Satu-satunya perubahan vs R2: side -> -side pasca-scan. Pagar, biaya,
horizon, cancel = warisan R2 via import (anti-drift R3).
"""

from __future__ import annotations

import hashlib
import json
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[5]
R2EV = ROOT / "reports" / "research" / "2026-10-13" / "discovery-R2" / "evidence"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(R2EV))

from d1_events import add_atr14, compute_atr_m5, load_m1  # noqa: E402
from d2_outcomes import evaluate  # noqa: E402
from run_discovery import anomaly_mask, check_atr_causal, collect_events  # noqa: E402

EVIDENCE = Path(__file__).resolve().parent
M1_2026 = "data/processed/M1/usdjpy_m1_2026.parquet"
R2_EVENTS = R2EV / "events.jsonl"
logger = logging.getLogger("discovery-P2")


def setup_logging() -> None:
    """Logging ganda konsol + berkas UTF-8."""
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    fh = logging.FileHandler(EVIDENCE / "run_stdout.log", encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logging.basicConfig(level=logging.INFO, handlers=[fh, sh])


def sha256(path: Path) -> str:
    """Hash SHA-256 berkas."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def write_manifest(outputs: dict[str, str]) -> None:
    """Manifest hash input pra-run + output pasca-run."""
    man = {
        "inputs": {
            "m1_2026": sha256(ROOT / M1_2026),
            "d1_events.py": sha256(R2EV / "d1_events.py"),
            "d2_outcomes.py": sha256(R2EV / "d2_outcomes.py"),
            "run_script": sha256(Path(__file__).resolve()),
            "ledger": sha256(EVIDENCE / "00_ledger_prarun.md"),
        },
        "outputs": outputs,
    }
    with open(EVIDENCE / "00_manifest.json", "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1)


def replay_single(rec: pd.DataFrame) -> pd.DataFrame:
    """Replay 1-posisi kronologis (definisi beku brief P2).

    Args:
        rec: Rekaman event-level hasil evaluate (+side_scan).

    Returns:
        rec + kolom pos1_seq (-1 = dilewat) + pos1_busy_until.
    """
    n = len(rec)
    seq = np.full(n, -1, dtype=np.int64)
    busy_col = np.full(n, -1, dtype=np.int64)
    ok = (rec["cancel"] == "") & (rec["ambiguous"] == 0)
    idx = np.flatnonzero(ok.to_numpy())
    t0 = rec["t0_pos"].to_numpy(dtype=np.int64)
    kbar = rec["BATR_kbar"].to_numpy(dtype=np.int64)
    res = rec["BATR_res"].to_numpy()
    order = sorted(idx.tolist(), key=lambda i: (int(t0[i]) + 1, i))
    busy, s = -1, 0
    for i in order:
        e = int(t0[i]) + 1
        if e < busy:
            busy_col[i] = busy
            continue
        k = int(kbar[i])
        busy = int(t0[i]) + (12 if res[i] == "TIME" else k + 1)
        seq[i], busy_col[i] = s, busy
        s += 1
    rec["pos1_seq"] = seq
    rec["pos1_busy_until"] = busy_col
    logger.info("1-posisi: dibuka=%d dilewat=%d", s, len(order) - s)
    return rec


def verify_vs_r2(rec: pd.DataFrame) -> None:
    """Verifikasi byte-level vs R2 (gagal = raise).

    Args:
        rec: Rekaman P2 (+side_scan).
    """
    r2 = pd.read_json(R2_EVENTS, lines=True)
    key = ["t0_utc", "family", "cell"]
    assert len(rec) == len(r2), f"n {len(rec)} != R2 {len(r2)}"
    c1 = rec.groupby(["family", "cell"]).size()
    c2 = r2.groupby(["family", "cell"]).size()
    assert c1.equals(c2), f"drift scan:\n{c1}\n{c2}"
    m = rec.merge(r2[key + ["side"]].rename(columns={"side": "r2_side"}), on=key)
    assert len(m) == len(rec), "pasangan tak-1:1"
    assert bool((rec["side_scan"] == m["r2_side"]).all()), "side_scan != side R2"
    assert bool((rec["side"] == -rec["side_scan"]).all()), "flip tak-sempurna"
    ev = rec["cancel"] == ""
    assert bool(
        (abs(rec.loc[ev, "sl_pips"] - 1.5 * rec.loc[ev, "atr"]) < 1e-9).all()
    ), "SL != 1,5xATR"
    assert bool(
        (abs(rec.loc[ev, "tp_pips"] - 3.0 * rec.loc[ev, "atr"]) < 1e-9).all()
    ), "TP != 3,0xATR"
    logger.info("verifikasi: scan IDENTIK R2, flip %d/%d, pagar beku OK", len(rec), len(rec))


def cell_rows(rec: pd.DataFrame) -> list[dict]:
    """Ringkasan stacked + 1-posisi per sel."""
    rows = []
    for (fam, cell), g in rec.groupby(["family", "cell"]):
        ev = g[g["cancel"] == ""]
        net = ev["BATR_net_obs"].to_numpy(dtype=float)
        net = net[np.isfinite(net)]
        op = g[g["pos1_seq"] >= 0]
        onet = op["BATR_net_obs"].to_numpy(dtype=float)
        rows.append(
            {
                "cell": f"{fam}/{cell}",
                "n_scan": int(len(g)),
                "n_eval": int(len(ev)),
                "TP": int((ev["BATR_res"] == "TP").sum()),
                "SL": int((ev["BATR_res"] == "SL").sum()),
                "TIME": int((ev["BATR_res"] == "TIME").sum()),
                "AMBIG": int((ev["BATR_res"] == "AMBIGUOUS").sum()),
                "med_net": float(np.median(net)) if len(net) else None,
                "sum_net": float(net.sum()) if len(net) else 0.0,
                "pos1_open": int(len(op)),
                "pos1_skip": int(((g["cancel"] == "") & (g["ambiguous"] == 0) & (g["pos1_seq"] < 0)).sum()),
                "pos1_W": int(((op["BATR_res"] == "TP") | ((op["BATR_res"] == "TIME") & (op["BATR_net_obs"] > 0))).sum()),
                "pos1_sum": float(onet[np.isfinite(onet)].sum()),
            }
        )
    return rows


def main() -> int:
    """Scan R2 + flip + race R2 + replay 1-posisi + verifikasi + tulis."""
    setup_logging()
    logger.info("P2-flipmurni mulai (bed 2026, NON-VONIS)")
    write_manifest({})  # pra-run: kunci hash input sebelum run pertama
    df = add_atr14(load_m1(ROOT / M1_2026))
    anom = anomaly_mask(df)
    atr = compute_atr_m5(df, anom)
    check_atr_causal(df, anom, atr)
    ev = collect_events(df, atr)
    logger.info("event pasca-eksklusi-t0: %d", len(ev))
    ev["side_scan"] = ev["side"]
    ev["side"] = -ev["side"]  # SATU perubahan: flip-murni
    rec = evaluate(df, ev, anom)
    assert len(rec) == len(ev)
    rec["side_scan"] = ev["side_scan"].to_numpy(dtype=np.int64)
    rec = replay_single(rec)
    verify_vs_r2(rec)
    rec.to_json(EVIDENCE / "events.jsonl", orient="records", lines=True)
    r2 = pd.read_json(R2_EVENTS, lines=True)
    m = rec.merge(
        r2[["t0_utc", "family", "cell", "BATR_res"]].rename(columns={"BATR_res": "r2_res"}),
        on=["t0_utc", "family", "cell"],
    )
    mirror = m.groupby(["r2_res", "BATR_res"]).size().to_dict()
    summary = {
        "status": "PEMANASAN NON-VONIS",
        "n": int(len(rec)),
        "cells": cell_rows(rec),
        "mirror_vs_R2": {f"{a}->{b}": int(v) for (a, b), v in sorted(mirror.items())},
    }
    with open(EVIDENCE / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, default=str)
    for c in summary["cells"]:
        logger.info("%s eval=%d TP/SL/TIME=%d/%d/%d med=%.3f sum=%.2f |1pos open=%d skip=%d W=%d sum=%.2f",
                    c["cell"], c["n_eval"], c["TP"], c["SL"], c["TIME"],
                    c["med_net"] or 0.0, c["sum_net"], c["pos1_open"],
                    c["pos1_skip"], c["pos1_W"], c["pos1_sum"])
    logger.info("cermin vs R2: %s", summary["mirror_vs_R2"])
    write_manifest({"events.jsonl": sha256(EVIDENCE / "events.jsonl"),
                    "summary.json": sha256(EVIDENCE / "summary.json")})
    logger.info("P2-flipmurni selesai")
    return 0


if __name__ == "__main__":
    sys.exit(main())
