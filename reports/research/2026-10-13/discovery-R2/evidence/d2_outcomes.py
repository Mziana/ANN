"""Outcome horizon + SATU paket barrier ATR + biaya 3 lapis Discovery-R2.

Kontrak D2-5: entry OPEN t0+1; BUY entry ASK exit BID / SELL entry BID
exit ASK; mid dilarang; first-passage pada 10 bar SESUDAH bar entry
(t0+2..t0+11, bar entry dikecualikan, loop-dari-k=1 EDA-06); bar-kembar
SL+TP = AMBIGUOUS_SEQUENCE (buang + hitung eksplisit); TIME exit =
close t0+11. Barrier per event: SL=1,5xATR, TP=2,0xSL, DIBEKUKAN.
Buang EDA-06: GAP -> ANOMALY_CROSS -> ATR_NA -> OFF_SESSION.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

PIP = 0.01
HORIZONS = (1, 2, 3, 5, 10, 15, 20)
H_EVAL = 10
K_MIN, K_MAX = 2, 11
ATR_K_SL = 1.5
ATR_RR = 2.0
COMMISSION = 0.3
SLIP_CONS = 0.2
SLIP_STRESS = 0.3

COST_OBS = {"London": 0.61, "NewYork": 0.69, "Tokyo": 0.62, "Sydney": 0.80}
COST_OBS_DEFAULT = 0.65
COST_P95 = {"London": 0.8, "NewYork": 1.2, "Tokyo": 0.9, "Sydney": 1.5}
COST_P95_DEFAULT = 1.0


def cost_layers(session: str) -> tuple[float, float, float]:
    """Tiga lapis biaya pip per event dari literal config beku.

    Args:
        session: Label sesi eksklusif t0.

    Returns:
        (observed, conservative, stress) dalam pip.
    """
    obs = COST_OBS.get(session, COST_OBS_DEFAULT) + COMMISSION
    cons = obs + SLIP_CONS
    stress = COST_P95.get(session, COST_P95_DEFAULT) + SLIP_STRESS + COMMISSION
    return obs, cons, stress


def horizon_gross(o, h, low, c, spread, t0: int, side: int, horizon: int):
    """Outcome horizon tetap + MFE/MAE sisi-keluar. Acuan skalar audit.

    Args: o/h/low/c = bid; spread = pip; t0 = posisi t0; side = +1/-1.
    Returns: (entry, exit, gross, mfe, mae, t_mfe, t_mae) pip.
    """
    ask_o = o + spread * PIP
    lo, hi = t0 + 1, t0 + horizon + 1
    if side == 1:
        entry, exits = ask_o[lo], c[lo:hi]
        mfe, mae = (h[lo:hi] - entry) / PIP, (low[lo:hi] - entry) / PIP
        gross, exit_net = (exits[-1] - entry) / PIP, exits[-1]
    else:
        entry = o[lo]
        exits = c[lo:hi] + spread[lo:hi] * PIP
        mfe = (entry - (low[lo:hi] + spread[lo:hi] * PIP)) / PIP
        mae = (entry - (h[lo:hi] + spread[lo:hi] * PIP)) / PIP
        gross, exit_net = (entry - exits[-1]) / PIP, exits[-1]
    return (
        float(entry),
        float(exit_net),
        float(gross),
        float(mfe.max()),
        float(mae.min()),
        int(mfe.argmax()) + 1,
        int(mae.argmin()) + 1,
    )


def barrier_first(o, h, low, c, spread, t0: int, side: int, sl: float, tp: float):
    """Race paket ATR: 10 bar sesudah bar entry, twin = AMBIGUOUS.

    Args: bid o/h/low/c; spread pip; sl/tp pip (beku per event).
    Returns: (hasil, exit_net_price, bar_offset 1..10).
    """
    if side == 1:
        entry = o[t0 + 1] + spread[t0 + 1] * PIP
        for k in range(1, H_EVAL + 1):
            j = t0 + 1 + k
            hit_tp = h[j] - entry >= tp * PIP
            hit_sl = low[j] - entry <= -sl * PIP
            if hit_tp and hit_sl:
                return "AMBIGUOUS", float("nan"), k
            if hit_tp:
                return "TP", float(h[j]), k
            if hit_sl:
                return "SL", float(low[j]), k
        return "TIME", float(c[t0 + K_MAX]), H_EVAL
    entry = o[t0 + 1]
    for k in range(1, H_EVAL + 1):
        j = t0 + 1 + k
        ask_h, ask_l = h[j] + spread[j] * PIP, low[j] + spread[j] * PIP
        hit_tp = entry - ask_l >= tp * PIP
        hit_sl = ask_h - entry >= sl * PIP
        if hit_tp and hit_sl:
            return "AMBIGUOUS", float("nan"), k
        if hit_tp:
            return "TP", float(ask_l), k
        if hit_sl:
            return "SL", float(ask_h), k
    return "TIME", float(c[t0 + K_MAX] + spread[t0 + K_MAX] * PIP), H_EVAL


def _base_out(ev: pd.DataFrame) -> dict[str, np.ndarray]:
    """Kolom keluaran kosong + identitas + ATR beku per event."""
    m = len(ev)
    nan = np.full(m, np.nan)
    atr = ev["atr"].to_numpy(dtype=float)
    out: dict[str, np.ndarray] = {
        "family": ev["family"].to_numpy(),
        "cell": ev["cell"].to_numpy(),
        "t0_pos": ev["t0_pos"].to_numpy(dtype=np.int64),
        "t0_utc": ev["t0_utc"].to_numpy(),
        "day": ev["day"].to_numpy(),
        "broker_day": ev["broker_day"].to_numpy(),
        "year": np.full(m, 2026, dtype=np.int64),
        "session": ev["session"].to_numpy(),
        "spread_t0": ev["spread_t0"].to_numpy(dtype=float),
        "side": ev["side"].to_numpy(dtype=np.int64),
        "atr": atr,
        "sl_pips": ATR_K_SL * atr,
        "tp_pips": ATR_K_SL * ATR_RR * atr,
        "cancel": np.full(m, "", dtype=object),
        "ambiguous": np.zeros(m, dtype=np.int64),
        "cost_obs": nan.copy(),
        "cost_cons": nan.copy(),
        "cost_stress": nan.copy(),
        "mfe": nan.copy(),
        "mae": nan.copy(),
        "t_mfe": np.zeros(m, dtype=np.int64),
        "t_mae": np.zeros(m, dtype=np.int64),
    }
    for horizon in HORIZONS:
        tag = f"H{horizon}"
        for suf in ("_entry", "_exit", "_gross", "_net_obs", "_net_cons", "_net_stress"):
            out[tag + suf] = nan.copy()
    for suf in ("_res", "_kbar", "_exit", "_gross", "_net_obs", "_net_cons", "_net_stress"):
        out["BATR" + suf] = (
            np.full(m, "", dtype=object)
            if suf == "_res"
            else (np.zeros(m, dtype=np.int64) if suf == "_kbar" else nan.copy())
        )
    return out


def _cancel_mask(t0, raw, n: int, anom_cs, atr_ok, sess_ok) -> np.ndarray:
    """Cancel per event urutan EDA-06: GAP/ANOMALY_CROSS/ATR_NA/OFF.

    Args:
        t0: Posisi t0 per event.
        raw: Epoch broker mentah per bar.
        n: Jumlah bar.
        anom_cs: Cumsum flag bar anomali.
        atr_ok: ATR tersedia per event.
        sess_ok: Sesi t0 bukan Off per event.

    Returns:
        Array alasan cancel ('' = lolos).
    """
    m = len(t0)
    cancel = np.full(m, "", dtype=object)
    entry_bar, win_end = t0 + 1, t0 + 20
    cancel[entry_bar >= n] = "NO_ENTRY_BAR"
    gap = np.zeros(n, dtype=bool)
    gap[1:] = np.diff(raw) != 60
    gcs = np.concatenate([[0], np.cumsum(gap, dtype=np.int64)])
    in_bounds = (entry_bar < n) & (win_end < n)
    has_gap = np.zeros(m, dtype=bool)
    has_gap[in_bounds] = (gcs[win_end[in_bounds] + 1] - gcs[entry_bar[in_bounds]]) > 0
    pending = cancel == ""
    cancel[pending & ~in_bounds] = "GAP"
    cancel[pending & has_gap] = "GAP"
    pending = cancel == ""
    cross = np.zeros(m, dtype=bool)
    cross[in_bounds] = (anom_cs[win_end[in_bounds] + 1] - anom_cs[entry_bar[in_bounds]]) > 0
    cancel[pending & cross] = "ANOMALY_CROSS"
    pending = cancel == ""
    cancel[pending & ~atr_ok] = "ATR_NA"
    pending = cancel == ""
    cancel[pending & ~sess_ok] = "OFF_SESSION"
    return cancel


def _fill_horizons(out, ok, cw, acw, buy, entry, obs, cons, stress) -> None:
    """Outcome semua horizon ke kolom keluaran (Q1 pemetaan deskriptif)."""
    for horizon in HORIZONS:
        col, tag = horizon - 1, f"H{horizon}"
        gross = np.where(buy, (cw[:, col] - entry) / PIP, (entry - acw[:, col]) / PIP)
        out[tag + "_entry"][ok] = entry
        out[tag + "_exit"][ok] = np.where(buy, cw[:, col], acw[:, col])
        out[tag + "_gross"][ok] = gross
        out[tag + "_net_obs"][ok] = gross - obs
        out[tag + "_net_cons"][ok] = gross - cons
        out[tag + "_net_stress"][ok] = gross - stress


def _fill_barrier(out, ok, sl, tp, hw, lw, ahw, alw, tm_exit, buy, entry, costs) -> None:
    """Race paket ATR tunggal: first-hit / AMBIGUOUS / TIME."""
    obs, cons, stress = costs
    side = buy[:, None]
    hit_tp = np.where(
        side, hw >= entry[:, None] + tp[:, None] * PIP, alw <= entry[:, None] - tp[:, None] * PIP
    )
    hit_sl = np.where(
        side, lw <= entry[:, None] - sl[:, None] * PIP, ahw >= entry[:, None] + sl[:, None] * PIP
    )
    any_hit = hit_tp | hit_sl
    has = any_hit.any(axis=1)
    first = any_hit.argmax(axis=1)
    rows = np.arange(len(entry))
    amb = has & hit_tp[rows, first] & hit_sl[rows, first]
    is_tp = has & ~amb & hit_tp[rows, first]
    is_sl = has & ~amb & hit_sl[rows, first]
    res = np.full(len(entry), "TIME", dtype=object)
    res[is_tp], res[is_sl], res[amb] = "TP", "SL", "AMBIGUOUS"
    exit_tp = np.where(buy, hw[rows, first], alw[rows, first])
    exit_sl = np.where(buy, lw[rows, first], ahw[rows, first])
    exit_net = np.where(is_tp, exit_tp, np.where(is_sl, exit_sl, tm_exit))
    gross = np.where(buy, (exit_net - entry) / PIP, (entry - exit_net) / PIP)
    out["BATR_res"][ok] = res
    out["BATR_exit"][ok] = np.where(amb, np.nan, exit_net)
    out["BATR_kbar"][ok] = np.where(has, first + 1, H_EVAL)
    out["BATR_gross"][ok] = np.where(amb, np.nan, gross)
    out["BATR_net_obs"][ok] = np.where(amb, np.nan, gross - obs)
    out["BATR_net_cons"][ok] = np.where(amb, np.nan, gross - cons)
    out["BATR_net_stress"][ok] = np.where(amb, np.nan, gross - stress)
    out["ambiguous"][ok] = amb.astype(np.int64)


def _fill_mfe(out, ok, hw, lw, ahw, alw, buy, entry) -> None:
    """MFE/MAE sisi-keluar atas jendela race t0+2..t0+11."""
    side = buy[:, None]
    mfe = np.where(side, (hw - entry[:, None]) / PIP, (entry[:, None] - alw) / PIP)
    mae = np.where(side, (lw - entry[:, None]) / PIP, (entry[:, None] - ahw) / PIP)
    out["mfe"][ok] = mfe.max(axis=1)
    out["mae"][ok] = mae.min(axis=1)
    out["t_mfe"][ok] = mfe.argmax(axis=1) + 1
    out["t_mae"][ok] = mae.argmin(axis=1) + 1


def evaluate(df: pd.DataFrame, ev: pd.DataFrame, anom: np.ndarray) -> pd.DataFrame:
    """Nilai horizon + paket ATR per event; cancel beralasan eksplisit.

    Args:
        df: Frame M1 2026.
        ev: Event + kolom atr (NaN = tak tersedia).
        anom: Flag boolean bar anomali selaras df.

    Returns:
        Rekaman event-level (kolom minimum D-3.4 warisan).
    """
    o = df["o"].to_numpy(dtype=float)
    h = df["h"].to_numpy(dtype=float)
    low = df["l"].to_numpy(dtype=float)
    c = df["c"].to_numpy(dtype=float)
    spread = df["spread"].to_numpy(dtype=float)
    n = len(df)
    ao, ah, al, ac = (a + spread * PIP for a in (o, h, low, c))
    anom_cs = np.concatenate([[0], np.cumsum(anom.astype(np.int64))])

    out = _base_out(ev)
    atr_ev = ev["atr"].to_numpy(dtype=float)
    out["cancel"] = _cancel_mask(
        out["t0_pos"],
        df["raw"].to_numpy(),
        n,
        anom_cs,
        np.isfinite(atr_ev),
        out["session"] != "Off",
    )
    ok = np.flatnonzero(out["cancel"] == "")
    if len(ok) == 0:
        return pd.DataFrame(out)

    sess = out["session"][ok]
    obs = np.array([COST_OBS.get(s, COST_OBS_DEFAULT) for s in sess]) + COMMISSION
    cons = obs + SLIP_CONS
    stress = np.array([COST_P95.get(s, COST_P95_DEFAULT) for s in sess]) + SLIP_STRESS + COMMISSION
    for key, val in (("cost_obs", obs), ("cost_cons", cons), ("cost_stress", stress)):
        out[key][ok] = val

    t, s, e = out["t0_pos"][ok], out["side"][ok], out["t0_pos"][ok] + 1
    sl = ATR_K_SL * atr_ev[ok]
    tp = ATR_K_SL * ATR_RR * atr_ev[ok]
    j20 = t[:, None] + np.arange(1, 21)
    cw = c[j20]
    acw = ac[j20]
    buy = s == 1
    entry = np.where(buy, ao[e], o[e])
    _fill_horizons(out, ok, cw, acw, buy, entry, obs, cons, stress)

    j10 = t[:, None] + np.arange(K_MIN, K_MAX + 1)
    hw, lw, ahw, alw = h[j10], low[j10], ah[j10], al[j10]
    _fill_mfe(out, ok, hw, lw, ahw, alw, buy, entry)

    tm_exit = np.where(buy, c[t + K_MAX], ac[t + K_MAX])
    _fill_barrier(out, ok, sl, tp, hw, lw, ahw, alw, tm_exit, buy, entry, (obs, cons, stress))

    _verify_sample(o, h, low, c, spread, ev, ok, out, atr_ev)
    return pd.DataFrame(out)


def _verify_sample(o, h, low, c, spread, ev, ok, out, atr_ev) -> None:
    """Samakan 50 event pertama vektor vs skalar; gagal bila divergen."""
    for pos in ok[:50]:
        row = ev.iloc[int(pos)]
        t0, s = int(row["t0_pos"]), int(row["side"])
        got = horizon_gross(o, h, low, c, spread, t0, s, H_EVAL)
        assert got is not None
        _, _, gross, _, _, _, _ = got
        assert abs(out["H10_gross"][pos] - gross) < 1e-9, f"divergen H10 @{t0}"
        sl, tp = ATR_K_SL * atr_ev[pos], ATR_K_SL * ATR_RR * atr_ev[pos]
        res, exit_net, _ = barrier_first(o, h, low, c, spread, t0, s, sl, tp)
        assert out["BATR_res"][pos] == res, f"divergen barrier @{t0}"
        if res != "AMBIGUOUS":
            obs = COST_OBS.get(row["session"], COST_OBS_DEFAULT) + COMMISSION
            entry_px = o[t0 + 1] + spread[t0 + 1] * PIP if s == 1 else o[t0 + 1]
            scalar = (exit_net - entry_px) / PIP if s == 1 else (entry_px - exit_net) / PIP
            assert abs(out["BATR_gross"][pos] - scalar) < 1e-9
            assert abs(out["BATR_net_obs"][pos] - (scalar - obs)) < 1e-9
    logger.info("verifikasi vektor-vs-skalar 50 event: IDENTIK")
