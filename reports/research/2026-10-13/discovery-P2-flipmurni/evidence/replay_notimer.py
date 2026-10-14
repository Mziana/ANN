"""Analisis apa-jika: matikan timer 10-menit, posisi hidup sampai pagar kena.

Bukan ronde (tanpa ledger/segel): replay 1-posisi + race SL/TP tanpa batas
dari M1 2026 langsung, mekanik sentuh = d2_outcomes.barrier_first R2.
Gap/anomali dalam jendela = CANCEL (lapor, tidak diblokir).
"""

from __future__ import annotations

import datetime
import json
import logging
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
R2EV = ROOT / "reports" / "research" / "2026-10-13" / "discovery-R2" / "evidence"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(R2EV))

from d1_events import load_m1  # noqa: E402
from d2_outcomes import PIP, cost_layers  # noqa: E402
from run_discovery import anomaly_mask  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("notimer")

R3EV = ROOT / "reports" / "research" / "2026-10-13" / "discovery-R3-pemanasan" / "evidence"


def load_signals() -> tuple[list[dict], list[dict]]:
    """Sinyal evaluable jendela 26Apr23xx-27Apr00xx (R3-flip + R2-asli)."""
    r3, r2 = [], []
    for line in open(R3EV / "events.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r.get("cancel") or r.get("broker_day") != "2026-04-26":
            continue
        r3.append(r)
    for line in open(R2EV / "events.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r.get("cancel") or r.get("ambiguous"):
            continue
        u = r.get("t0_utc", "")
        if "2026-04-26T23" in u or "2026-04-27T00" in u:
            r2.append(r)
    return r3, r2


def race(o, h, low, c, sp, t0: int, side: int, sl: float, tp: float, n: int):
    """Race tanpa timer dari bar t0+2; bar entry dikecualikan (warisan R2).

    Returns: (hasil, exit_px, j_bar, mfe_pt, mae_pt) atau ('OPEN',...).
    """
    if side == 1:
        entry = o[t0 + 1] + sp[t0 + 1] * PIP
        fav = h[t0 + 2 :] - entry
        adv = entry - low[t0 + 2 :]
        tpx = h
        slx = low
    else:
        entry = o[t0 + 1]
        ask_h, ask_l = h + sp * PIP, low + sp * PIP
        fav = entry - ask_l[t0 + 2 :]
        adv = ask_h[t0 + 2 :] - entry
        tpx = ask_l
        slx = ask_h
    htp, hsl = fav >= tp * PIP, adv >= sl * PIP
    any_hit = htp | hsl
    if not any_hit.any():
        return "OPEN", float("nan"), -1, float(fav.max() / PIP), float(-adv.max() / PIP)
    f = int(any_hit.argmax())
    j = t0 + 2 + f
    mfe = float(fav[: f + 1].max() / PIP)
    mae = float(-adv[: f + 1].max() / PIP)
    if htp[f] and hsl[f]:
        return "AMBIGUOUS", float(c[j]), j, mfe, mae
    if htp[f]:
        return "TP", float(tpx[j]), j, mfe, mae
    return "SL", float(slx[j]), j, mfe, mae


def replay(signals: list[dict], tag: str, o, h, low, c, sp, raw, anom, pos_of) -> list[dict]:
    """Replay 1-posisi tanpa timer; busy = close bar exit aktual."""
    out, busy, skipped = [], -1, 0
    for r in sorted(signals, key=lambda r: r["_t"]):
        t0 = pos_of[r["_t"]]
        e = t0 + 1
        if e < busy:
            skipped += 1
            continue
        res, xpx, j, mfe, mae = race(o, h, low, c, sp, t0, r["side"], r["sl"], r["tp"], len(o))
        if res == "OPEN":
            out.append({**r, "_out": ("OPEN", xpx, -1, mfe, mae)})
            busy = len(o)
            continue
        seg = raw[t0 + 1 : j + 1]
        if (np.diff(seg) != 60).any() or anom[t0 + 1 : j + 1].any():
            skipped += 1  # CANCEL: gap/anomali — lapor sebagai dilewat
            continue
        out.append({**r, "_out": (res, xpx, j, mfe, mae)})
        busy = j + 1
    logger.info("%s: dibuka=%d dilewat=%d", tag, len(out), skipped)
    return out


def show(trades: list[dict], tag: str) -> None:
    """Tabel format sama + TINGGI/RENDAH selama pegang (bukan 10 mnt)."""
    print(f"=== {tag} TANPA TIMER ===")
    kum = 0.0
    for i, r in enumerate(trades, 1):
        res, xpx, j, mfe, mae = r["_out"]
        side = "BUY" if r["side"] == 1 else "SELL"
        t0 = r["_t0pos"]
        held = j - (t0 + 1)
        obs = cost_layers(r["session"])[0]
        if res == "OPEN":
            pt, net, w = "OPEN", 0.0, "-"
        elif res == "AMBIGUOUS":
            gross = (xpx - r["_entry"] if side == "BUY" else r["_entry"] - xpx) / PIP
            pt = round(gross * 10)
            net = gross - obs
            w = "W" if net > 0 else "L"
        else:
            gross = (xpx - r["_entry"] if side == "BUY" else r["_entry"] - xpx) / PIP
            pt = round(gross * 10)
            net = gross - obs
            w = "W" if res == "TP" else "L"
        kum += net
        print(f"{i} {r['_t'][11:16]} {side} | entry {r['_entry']:.3f} | "
              f"exit {xpx:.3f} ({res} bar-{held}) | TINGGI +{round(mfe * 10)} | "
              f"RENDAH {round(mae * 10)} | point {'+' + str(pt) if isinstance(pt, int) and pt > 0 else pt} "
              f"{w} | net {net:.2f} kum {kum:.2f}")


def main() -> int:
    """Muat M1 + sinyal, replay tanpa timer, cetak dua tabel."""
    df = load_m1(ROOT / "data/processed/M1/usdjpy_m1_2026.parquet")
    o = df["o"].to_numpy(float)
    h = df["h"].to_numpy(float)
    low = df["l"].to_numpy(float)
    c = df["c"].to_numpy(float)
    sp = df["spread"].to_numpy(float)
    raw = df["raw"].to_numpy()
    anom = anomaly_mask(df)
    # 'time' = jam dinding broker (label +0000), raw = epoch UTC sejati.
    pos_of = {str(v): i for i, v in enumerate(df["time"].to_list())}
    r3, r2 = load_signals()
    for r in r3:
        r["_t"], r["_t0pos"] = r["t0"], pos_of[r["t0"]]
        r["_entry"] = (o[r["_t0pos"] + 1] + sp[r["_t0pos"] + 1] * PIP if r["side"] == 1
                       else o[r["_t0pos"] + 1])
        r["sl"], r["tp"] = r["sl_pips"], r["tp_pips"]
    for r in r2:
        assert pos_of[r["t0_utc"]] == r["t0_pos"], "peta waktu vs t0_pos divergen"
        r["_t"], r["_t0pos"] = r["t0_utc"], r["t0_pos"]
        r["_entry"] = (o[r["_t0pos"] + 1] + sp[r["_t0pos"] + 1] * PIP if r["side"] == 1
                       else o[r["_t0pos"] + 1])
        r["sl"], r["tp"] = r["sl_pips"], r["tp_pips"]
    logger.info("sinyal: R3=%d R2=%d", len(r3), len(r2))
    show(replay(r3, "R3", o, h, low, c, sp, raw, anom, {r["_t"]: r["_t0pos"] for r in r3}), "R3-FLIP")
    show(replay(r2, "R2", o, h, low, c, sp, raw, anom, {r["_t"]: r["_t0pos"] for r in r2}), "R2-ASLI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
