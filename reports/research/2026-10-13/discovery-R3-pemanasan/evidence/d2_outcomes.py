"""Outcome H+10 + barrier race paket ATR tunggal R3 (SL=1,0xATR, TP=1,5xATR).

Kontrak eksekusi = spec R2 D2-5 persis; harga eksekusi memakai spread
observed sesi bar entry untuk semua lapis (lapis conservative/stress
menambah slippage di pembukuan, bukan eksekusi ulang).
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)

PIP = 0.01
COMMISSION = 0.3
SLIP_CONS = 0.2
SLIP_STRESS = 0.3


def layer_costs(spread_obs: float, spread_p95: float) -> tuple:
    """Tiga lapis biaya per event (pip): observed, conservative, stress."""
    obs = spread_obs + COMMISSION
    cons = spread_obs + SLIP_CONS + COMMISSION
    stress = spread_p95 + SLIP_STRESS + COMMISSION
    return obs, cons, stress


def find_touch(
    hi: np.ndarray, lo: np.ndarray, sl_px: float, tp_px: float, buy: bool
) -> tuple | None:
    """Sentuhan pertama (SL/TP/AMBIGUOUS) pada bar SESUDAH bar entry."""
    for pos in range(len(hi)):
        hit_sl = lo[pos] <= sl_px if buy else hi[pos] >= sl_px
        hit_tp = hi[pos] >= tp_px if buy else lo[pos] <= tp_px
        if hit_sl and hit_tp:
            return pos, "AMBIGUOUS"
        if hit_sl:
            return pos, "SL"
        if hit_tp:
            return pos, "TP"
    return None


def pack(
    res: str,
    kbar: int,
    gross: float,
    mfe: float,
    mae: float,
    t_mfe: int,
    t_mae: int,
    entry_px: float,
    exit_px: float,
) -> dict:
    """Kemas hasil race menjadi record outcome.

    Kontrak R2 D2-5: AMBIGUOUS_SEQUENCE dibuang dari evaluasi paket
    (exit/gross/net = null, dihitung eksplisit), MFE/MAE tetap dicatat.
    """
    return {
        "res": res,
        "kbar": kbar,
        "gross": None if gross is None else float(gross),
        "mfe": mfe,
        "mae": mae,
        "t_mfe": t_mfe,
        "t_mae": t_mae,
        "entry_px": entry_px,
        "exit_px": exit_px,
    }


def race_buy(
    op: float,
    hi: np.ndarray,
    lo: np.ndarray,
    close_end: float,
    sl_p: float,
    tp_p: float,
    spread_obs: float,
) -> dict:
    """Race barrier sisi BUY (entry ASK, exit BID); bar entry dikecualikan."""
    entry_ask = op + spread_obs * PIP
    sl_px = entry_ask - sl_p * PIP
    tp_px = entry_ask + tp_p * PIP
    touch = find_touch(hi, lo, sl_px, tp_px, True)
    up = (hi - entry_ask) / PIP
    down = (lo - entry_ask) / PIP
    mfe, mae = float(up.max()), float(down.min())
    t_mfe, t_mae = int(up.argmax()) + 1, int(down.argmin()) + 1
    if touch is None:
        return pack(
            "TIME", 10, (close_end - entry_ask) / PIP, mfe, mae, t_mfe, t_mae, entry_ask, close_end
        )
    pos, res = touch
    if res == "AMBIGUOUS":
        return pack(res, pos + 1, None, mfe, mae, t_mfe, t_mae, entry_ask, None)
    exit_px = sl_px if res == "SL" else tp_px
    return pack(
        res, pos + 1, (exit_px - entry_ask) / PIP, mfe, mae, t_mfe, t_mae, entry_ask, exit_px
    )


def race_sell(
    op: float,
    hi: np.ndarray,
    lo: np.ndarray,
    close_end: float,
    sl_p: float,
    tp_p: float,
    spread_obs: float,
) -> dict:
    """Race barrier sisi SELL (entry BID, exit ASK); bar entry dikecualikan."""
    entry_bid = op
    sl_px = entry_bid + sl_p * PIP
    tp_px = entry_bid - tp_p * PIP
    touch = find_touch(hi, lo, sl_px, tp_px, False)
    up = (entry_bid - lo) / PIP
    down = (entry_bid - hi) / PIP
    mfe, mae = float(up.max()), float(down.min())
    t_mfe, t_mae = int(up.argmax()) + 1, int(down.argmin()) + 1
    if touch is None:
        exit_ask = close_end + spread_obs * PIP
        return pack(
            "TIME", 10, (entry_bid - exit_ask) / PIP, mfe, mae, t_mfe, t_mae, entry_bid, exit_ask
        )
    pos, res = touch
    if res == "AMBIGUOUS":
        return pack(res, pos + 1, None, mfe, mae, t_mfe, t_mae, entry_bid, None)
    exit_px = sl_px if res == "SL" else tp_px
    return pack(
        res, pos + 1, (entry_bid - exit_px) / PIP, mfe, mae, t_mfe, t_mae, entry_bid, exit_px
    )


def outcome_fields(race: dict, obs: float, cons: float, stress: float, h10_gross: float) -> dict:
    """Kolom outcome + tiga lapis net (null bila AMBIGUOUS dibuang)."""
    gross = race["gross"]

    def net(cost: float) -> float | None:
        return None if gross is None else gross - cost

    return {
        "entry_px": race["entry_px"],
        "exit_px": race["exit_px"],
        "gross": gross,
        "net_obs": net(obs),
        "net_cons": net(cons),
        "net_stress": net(stress),
        "mfe": race["mfe"],
        "mae": race["mae"],
        "t_mfe": race["t_mfe"],
        "t_mae": race["t_mae"],
        "h10_gross": float(h10_gross),
        "h10_net_obs": float(h10_gross) - obs,
        "res": race["res"],
        "kbar": race["kbar"],
    }


def build_record(
    t0_str: str,
    cell: str,
    side_scan: int,
    side: int,
    sl_p: float,
    sess: str,
    spread_obs: float,
    spread_p95: float,
    race: dict,
    h10_gross: float,
    day: str,
) -> dict:
    """Rakit satu record D-3.4 dari hasil race + tiga lapis biaya."""
    obs, cons, stress = layer_costs(spread_obs, spread_p95)
    row = {
        "t0": t0_str,
        "cell": cell,
        "side_scan": side_scan,
        "side": side,
        "atr_pips": sl_p,
        "sl_pips": sl_p,
        "tp_pips": 1.5 * sl_p,
        "session": sess,
        "spread_obs": spread_obs,
        "spread_p95": spread_p95,
        "cost_obs": obs,
        "cost_cons": cons,
        "cost_stress": stress,
        "cancel": "",
        "broker_day": day,
        "year": 2026,
    }
    row.update(outcome_fields(race, obs, cons, stress, h10_gross))
    return row


def evaluate(
    evaluable: list,
    op: np.ndarray,
    hi: np.ndarray,
    lo: np.ndarray,
    cl: np.ndarray,
    sessions: np.ndarray,
    cost_obs_map: dict,
    cost_p95_map: dict,
    atr: np.ndarray,
    utc_str: np.ndarray,
    broker_day: np.ndarray,
) -> list:
    """Nilai tiap event evaluable; kembalikan record D-3.4 per event."""
    records = []
    for t0, cell, side_scan, side in evaluable:
        sess = str(sessions[t0 + 1])
        spread_obs = float(cost_obs_map[sess])
        spread_p95 = float(cost_p95_map[sess])
        sl_p = float(atr[t0])
        tp_p = 1.5 * sl_p
        window_hi = hi[t0 + 2 : t0 + 12]
        window_lo = lo[t0 + 2 : t0 + 12]
        if side == 1:
            race = race_buy(op[t0 + 1], window_hi, window_lo, cl[t0 + 11], sl_p, tp_p, spread_obs)
        else:
            race = race_sell(op[t0 + 1], window_hi, window_lo, cl[t0 + 11], sl_p, tp_p, spread_obs)
        h10_gross = side * (cl[t0 + 10] - cl[t0]) / PIP
        records.append(
            build_record(
                str(utc_str[t0]),
                cell,
                side_scan,
                side,
                sl_p,
                sess,
                spread_obs,
                spread_p95,
                race,
                h10_gross,
                str(broker_day[t0]),
            )
        )
    return records
