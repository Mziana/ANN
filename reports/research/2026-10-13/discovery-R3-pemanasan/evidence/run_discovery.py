"""Orkestrasi run pemanasan R3: pindai -> nilai -> statistik -> tulis bukti."""

from __future__ import annotations

import hashlib
import json
import logging
import sys
from pathlib import Path

import d1_events
import d2_outcomes
import d3_stats
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.utils.config import load_config

logger = logging.getLogger(__name__)

EVIDENCE = Path(__file__).resolve().parent
NULL_RECORD = {
    "entry_px": None,
    "exit_px": None,
    "gross": None,
    "net_obs": None,
    "net_cons": None,
    "net_stress": None,
    "mfe": None,
    "mae": None,
    "t_mfe": None,
    "t_mae": None,
    "h10_gross": None,
    "h10_net_obs": None,
    "res": "CANCEL",
    "kbar": None,
}


def broker_days(raw: np.ndarray) -> np.ndarray:
    """Hari-broker per bar: jam dinding server minus 4 jam (hari 04:00-03:00)."""
    wall = pd.to_datetime(raw, unit="s")
    return ((wall - pd.Timedelta(hours=4)).date).astype(str)


def cost_maps(config: dict) -> tuple:
    """Peta biaya sesi literal + fallback default bila tak terpetakan."""
    basis = config["spread"]["cost_basis"]
    stress = config["spread"]["stress_bands"]["p95"]
    obs = {k: float(v) for k, v in basis["by_session"].items()}
    p95 = {k: float(v) for k, v in stress["by_session"].items()}
    return obs, p95, float(basis["default"]), float(stress["default"])


def cancel_records(
    cancels: list, utc_str: np.ndarray, sessions: np.ndarray, broker_day: np.ndarray
) -> list:
    """Bangun record cancel (kolom outcome = null, alasan eksplisit)."""
    rows = []
    n_sess = len(sessions)
    for t0, cell, side_scan, side, reason in cancels:
        sess = str(sessions[t0 + 1]) if t0 + 1 < n_sess else "END"
        row = {
            "t0": str(utc_str[t0]),
            "cell": cell,
            "side_scan": side_scan,
            "side": side,
            "atr_pips": None,
            "sl_pips": None,
            "tp_pips": None,
            "session": sess,
            "spread_obs": None,
            "spread_p95": None,
            "cost_obs": None,
            "cost_cons": None,
            "cost_stress": None,
            "cancel": reason,
            "broker_day": str(broker_day[t0]),
            "year": 2026,
        }
        row.update(NULL_RECORD)
        rows.append(row)
    return rows


def write_outputs(records: list, summary: dict) -> None:
    """Tulis events.jsonl + summary.json (format deterministik)."""
    with open(EVIDENCE / "events.jsonl", "w") as handle:
        for row in records:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    with open(EVIDENCE / "summary.json", "w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)


def file_hashes() -> dict:
    """SHA-256 harness (bukti disiplin determinisme)."""
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(EVIDENCE.glob("*.py"))
    }


def scan_phase(frame: pd.DataFrame) -> tuple:
    """Fase pindai: mask, sesi, ATR, scan E1/E2/E3, negasi, eksklusi."""
    utc = frame["utc"]
    op = frame["open"].to_numpy("float64")
    hi = frame["high"].to_numpy("float64")
    lo = frame["low"].to_numpy("float64")
    cl = frame["close"].to_numpy("float64")
    anom = d1_events.anomaly_mask(utc)
    logger.info("anomali=%d usable=%d", int(anom.sum()), int((~anom).sum()))
    sessions = d1_events.session_labels(utc).to_numpy()
    atr = d1_events.compute_atr_m5(frame, anom)
    logger.info("atr_ok=%d", int(np.isfinite(atr).sum()))
    t0_ok = ~anom
    step_ok = np.concatenate([[True], np.diff(utc.values.astype("int64")) == 60_000_000_000])
    scanned = d1_events.scan_e1(op, hi, lo, cl, t0_ok)
    scanned += d1_events.scan_e2(cl, hi, lo, d1_events.compute_atr_m1(hi, lo, cl, step_ok), t0_ok)
    scanned += d1_events.scan_e3(cl, hi, lo, utc, t0_ok)
    logger.info("terpindai=%d", len(scanned))
    flipped = d1_events.negate_side(scanned)
    utc_ns = utc.values.astype("int64")
    evaluable, cancels, counts = d1_events.apply_exclusions(flipped, utc_ns, anom, atr, sessions)
    logger.info("evaluable=%d cancel=%s", len(evaluable), counts)
    return op, hi, lo, cl, sessions, atr, evaluable, cancels, counts, flipped


def main() -> int:
    """Jalankan ronde pemanasan sekali penuh."""
    log_path = EVIDENCE / "run_stdout.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path, mode="w"), logging.StreamHandler(sys.stderr)],
    )
    logger.info("R3-pemanasan mulai (flip + resize, NON-VONIS)")
    config = load_config("data")
    frame = d1_events.load_m1()
    utc_str = frame["time"].to_numpy()
    days = broker_days(frame["broker_time_raw"].to_numpy())
    op, hi, lo, cl, sessions, atr, evaluable, cancels, counts, flipped = scan_phase(frame)
    obs_map, p95_map, obs_dflt, p95_dflt = cost_maps(config)
    sessions4 = ("London", "NewYork", "Tokyo", "Sydney", "Off")
    evaluate_maps = (
        {s: obs_map.get(s, obs_dflt) for s in sessions4},
        {s: p95_map.get(s, p95_dflt) for s in sessions4},
    )
    records = d2_outcomes.evaluate(
        evaluable, op, hi, lo, cl, sessions, evaluate_maps[0], evaluate_maps[1], atr, utc_str, days
    )
    records += cancel_records(cancels, utc_str, sessions, days)
    scan_counts: dict = {}
    for _, cell, _, _ in flipped:
        scan_counts[cell] = scan_counts.get(cell, 0) + 1
    summary = d3_stats.summarize(records, cancels, counts)
    summary["n_scanned_total"] = len(flipped)
    summary["scan_counts"] = scan_counts
    summary["harness_sha256"] = file_hashes()
    write_outputs(records, summary)
    logger.info(
        "selesai: eval=%d cancel=%d ambig=%d",
        summary["n_eval_total"],
        summary["n_cancel_total"],
        summary["n_ambig_total"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
