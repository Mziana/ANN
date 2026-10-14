"""Outcome horizon + barrier race + biaya 3 lapis Discovery-R1.

Kontrak: entry OPEN t0+1; BUY entry ASK exit BID / SELL entry BID exit ASK;
mid dilarang; AMBIGUOUS_SEQUENCE dibuang-terhitung; biaya literal config.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

PIP = 0.01
HORIZONS = (1, 2, 3, 5, 10, 15, 20)
H_EVAL = 10
LADDER = ((1.5, 1.5), (1.5, 2.5), (2.5, 1.5), (2.5, 2.5), (4.0, 1.5), (4.0, 2.5))
TP_EVAL, SL_EVAL = 2.5, 2.5
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


def contiguous(raw: np.ndarray, start: int, length: int) -> bool:
    """Bar start..start+length-1 menit-berturut (batas GAP).

    Args:
        raw: Epoch broker mentah per bar.
        start: Posisi awal.
        length: Jumlah bar.

    Returns:
        True bila tiap langkah tepat +60 detik dan dalam data.
    """
    if start + length > len(raw):
        return False
    seg = raw[start : start + length]
    return bool((np.diff(seg) == 60).all())


def horizon_gross(
    o: np.ndarray,
    h: np.ndarray,
    low: np.ndarray,
    c: np.ndarray,
    spread: np.ndarray,
    t0: int,
    side: int,
    horizon: int,
) -> tuple[float, float, float, float, float, int, int] | None:
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


def _race_buy(
    h: np.ndarray,
    low: np.ndarray,
    c: np.ndarray,
    entry: float,
    t0: int,
    tp: float,
    sl: float,
    tstop: int,
) -> tuple[str, float, int]:
    """Race barrier sisi BUY (harga keluar = sisi BID)."""
    for k in range(1, tstop + 1):
        j = t0 + k
        hit_tp = h[j] - entry >= tp * PIP
        hit_sl = low[j] - entry <= -sl * PIP
        if hit_tp and hit_sl:
            return "AMBIGUOUS", float("nan"), k
        if hit_tp:
            return "TP", float(h[j]), k
        if hit_sl:
            return "SL", float(low[j]), k
    return "TIME", float(c[t0 + tstop]), tstop


def _race_sell(
    o: np.ndarray,
    h: np.ndarray,
    low: np.ndarray,
    c: np.ndarray,
    spread: np.ndarray,
    t0: int,
    tp: float,
    sl: float,
    tstop: int,
) -> tuple[str, float, int]:
    """Race barrier sisi SELL (harga keluar = sisi ASK)."""
    entry = o[t0 + 1]
    for k in range(1, tstop + 1):
        j = t0 + k
        ask_h, ask_l = h[j] + spread[j] * PIP, low[j] + spread[j] * PIP
        hit_tp = entry - ask_l >= tp * PIP
        hit_sl = ask_h - entry >= sl * PIP
        if hit_tp and hit_sl:
            return "AMBIGUOUS", float("nan"), k
        if hit_tp:
            return "TP", float(ask_l), k
        if hit_sl:
            return "SL", float(ask_h), k
    return "TIME", float(c[t0 + tstop] + spread[t0 + tstop] * PIP), tstop


def barrier_first(
    o: np.ndarray,
    h: np.ndarray,
    low: np.ndarray,
    c: np.ndarray,
    spread: np.ndarray,
    t0: int,
    side: int,
    tp: float,
    sl: float,
    tstop: int,
) -> tuple[str, float, int]:
    """Barrier race TP/SL + time-stop: hasil pertama atau AMBIGUOUS.

    Args: bid o/h/low/c; spread pip; side +1 BUY/-1 SELL; tp/sl pip.
    Returns: (hasil, exit_net_price, bar_offset).
    """
    if side == 1:
        return _race_buy(h, low, c, o[t0 + 1] + spread[t0 + 1] * PIP, t0, tp, sl, tstop)
    return _race_sell(o, h, low, c, spread, t0, tp, sl, tstop)


def _base_out(ev: pd.DataFrame) -> dict[str, np.ndarray]:
    """Kolom keluaran kosong (NaN/''/0) + identitas dari event."""
    m = len(ev)
    nan = np.full(m, np.nan)
    out: dict[str, np.ndarray] = {
        "family": ev["family"].to_numpy(),
        "cell": ev["cell"].to_numpy(),
        "t0_pos": ev["t0_pos"].to_numpy(dtype=np.int64),
        "t0_utc": ev["t0_utc"].to_numpy(),
        "day": ev["day"].to_numpy(),
        "session": ev["session"].to_numpy(),
        "spread_t0": ev["spread_t0"].to_numpy(dtype=float),
        "side": ev["side"].to_numpy(dtype=np.int64),
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
    for tp, sl in LADDER:
        tag = f"B{tp}g{sl}"
        out[tag + "_res"] = np.full(m, "", dtype=object)
        out[tag + "_kbar"] = np.zeros(m, dtype=np.int64)
        for suf in ("_exit", "_gross", "_net_obs", "_net_cons", "_net_stress"):
            out[tag + suf] = nan.copy()
    return out


def _cancel_mask(t0: np.ndarray, raw: np.ndarray, n: int) -> np.ndarray:
    """Cancel per event: NO_ENTRY_BAR / GAP / '' (setara contiguous)."""
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
    return cancel


def _fill_horizons(
    out: dict,
    ok: np.ndarray,
    cw: np.ndarray,
    acw: np.ndarray,
    buy: np.ndarray,
    entry: np.ndarray,
    obs: np.ndarray,
    cons: np.ndarray,
    stress: np.ndarray,
) -> None:
    """Outcome semua horizon ke kolom keluaran."""
    for horizon in HORIZONS:
        col, tag = horizon - 1, f"H{horizon}"
        gross = np.where(buy, (cw[:, col] - entry) / PIP, (entry - acw[:, col]) / PIP)
        out[tag + "_entry"][ok] = entry
        out[tag + "_exit"][ok] = np.where(buy, cw[:, col], acw[:, col])
        out[tag + "_gross"][ok] = gross
        out[tag + "_net_obs"][ok] = gross - obs
        out[tag + "_net_cons"][ok] = gross - cons
        out[tag + "_net_stress"][ok] = gross - stress


def _fill_one_barrier(
    out: dict,
    ok: np.ndarray,
    tp: float,
    sl: float,
    hw10: np.ndarray,
    lw10: np.ndarray,
    ahw10: np.ndarray,
    alw10: np.ndarray,
    tm_exit: np.ndarray,
    buy: np.ndarray,
    entry: np.ndarray,
    obs: np.ndarray,
    cons: np.ndarray,
    stress: np.ndarray,
) -> None:
    """Race satu tangga (tp, sl): first-hit / AMBIGUOUS / TIME."""
    tag = f"B{tp}g{sl}"
    side = buy[:, None]
    hit_tp = np.where(side, hw10 >= entry[:, None] + tp * PIP, alw10 <= entry[:, None] - tp * PIP)
    hit_sl = np.where(side, lw10 <= entry[:, None] - sl * PIP, ahw10 >= entry[:, None] + sl * PIP)
    any_hit = hit_tp | hit_sl
    has = any_hit.any(axis=1)
    first = any_hit.argmax(axis=1)
    rows = np.arange(len(entry))
    amb = has & hit_tp[rows, first] & hit_sl[rows, first]
    is_tp = has & ~amb & hit_tp[rows, first]
    is_sl = has & ~amb & hit_sl[rows, first]
    res = np.full(len(entry), "TIME", dtype=object)
    res[is_tp], res[is_sl], res[amb] = "TP", "SL", "AMBIGUOUS"
    exit_tp = np.where(buy, hw10[rows, first], alw10[rows, first])
    exit_sl = np.where(buy, lw10[rows, first], ahw10[rows, first])
    exit_net = np.where(is_tp, exit_tp, np.where(is_sl, exit_sl, tm_exit))
    gross = np.where(buy, (exit_net - entry) / PIP, (entry - exit_net) / PIP)
    out[tag + "_res"][ok] = res
    out[tag + "_exit"][ok] = np.where(amb, np.nan, exit_net)
    out[tag + "_kbar"][ok] = np.where(has, first + 1, H_EVAL)
    out[tag + "_gross"][ok] = np.where(amb, np.nan, gross)
    out[tag + "_net_obs"][ok] = np.where(amb, np.nan, gross - obs)
    out[tag + "_net_cons"][ok] = np.where(amb, np.nan, gross - cons)
    out[tag + "_net_stress"][ok] = np.where(amb, np.nan, gross - stress)


def _fill_mfe(
    out: dict,
    ok: np.ndarray,
    hw10: np.ndarray,
    lw10: np.ndarray,
    ahw10: np.ndarray,
    alw10: np.ndarray,
    buy: np.ndarray,
    entry: np.ndarray,
) -> None:
    """MFE/MAE + waktu atas window H_EVAL sisi-keluar."""
    side = buy[:, None]
    mfe = np.where(side, (hw10 - entry[:, None]) / PIP, (entry[:, None] - alw10) / PIP)
    mae = np.where(side, (lw10 - entry[:, None]) / PIP, (entry[:, None] - ahw10) / PIP)
    out["mfe"][ok] = mfe.max(axis=1)
    out["mae"][ok] = mae.min(axis=1)
    out["t_mfe"][ok] = mfe.argmax(axis=1) + 1
    out["t_mae"][ok] = mae.argmin(axis=1) + 1


def evaluate(df: pd.DataFrame, ev: pd.DataFrame) -> pd.DataFrame:
    """Nilai semua horizon + ladder per event; cancel beralasan eksplisit.

    Tervektorisasi; ekuivalensi vs skalar diverifikasi 50 event tiap run.
    """
    o = df["o"].to_numpy(dtype=float)
    h = df["h"].to_numpy(dtype=float)
    low = df["l"].to_numpy(dtype=float)
    c = df["c"].to_numpy(dtype=float)
    spread = df["spread"].to_numpy(dtype=float)
    n = len(df)
    ao, ah, al, ac = (a + spread * PIP for a in (o, h, low, c))

    out = _base_out(ev)
    out["cancel"] = _cancel_mask(out["t0_pos"], df["raw"].to_numpy(), n)
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
    j20 = t[:, None] + np.arange(1, 21)
    cw, hw, lw = c[j20], h[j20], low[j20]
    acw, ahw, alw = ac[j20], ah[j20], al[j20]
    buy = s == 1
    entry = np.where(buy, ao[e], o[e])
    _fill_horizons(out, ok, cw, acw, buy, entry, obs, cons, stress)

    hw10, lw10 = hw[:, :10], lw[:, :10]
    ahw10, alw10 = ahw[:, :10], alw[:, :10]
    _fill_mfe(out, ok, hw10, lw10, ahw10, alw10, buy, entry)

    tm_exit = np.where(buy, cw[:, H_EVAL - 1], acw[:, H_EVAL - 1])
    for tp, sl in LADDER:
        _fill_one_barrier(
            out, ok, tp, sl, hw10, lw10, ahw10, alw10, tm_exit, buy, entry, obs, cons, stress
        )
    out["ambiguous"][ok] = sum(
        (out[f"B{tp}g{sl}_res"][ok] == "AMBIGUOUS").astype(np.int64) for tp, sl in LADDER
    )

    _verify_sample(o, h, low, c, spread, ev, ok, out)
    return pd.DataFrame(out)


def _verify_sample(
    o: np.ndarray,
    h: np.ndarray,
    low: np.ndarray,
    c: np.ndarray,
    spread: np.ndarray,
    ev: pd.DataFrame,
    ok: np.ndarray,
    out: dict[str, np.ndarray],
) -> None:
    """Samakan 50 event pertama vektor vs skalar; gagal bila divergen."""
    for pos in ok[:50]:
        row = ev.iloc[int(pos)]
        t0, s = int(row["t0_pos"]), int(row["side"])
        got = horizon_gross(o, h, low, c, spread, t0, s, H_EVAL)
        assert got is not None
        _, _, gross, mfe, mae, tmfe, tmae = got
        assert abs(out["H10_gross"][pos] - gross) < 1e-9, f"divergen H10 @{t0}"
        assert abs(out["mfe"][pos] - mfe) < 1e-9, f"divergen MFE @{t0}"
        assert abs(out["mae"][pos] - mae) < 1e-9, f"divergen MAE @{t0}"
        assert out["t_mfe"][pos] == tmfe and out["t_mae"][pos] == tmae, f"divergen T @{t0}"
        res, exit_net, _ = barrier_first(o, h, low, c, spread, t0, s, TP_EVAL, SL_EVAL, H_EVAL)
        assert out["B2.5g2.5_res"][pos] == res, f"divergen barrier @{t0}"
        if res != "AMBIGUOUS":
            obs = COST_OBS.get(row["session"], COST_OBS_DEFAULT) + COMMISSION
            entry_px = o[t0 + 1] + spread[t0 + 1] * PIP if s == 1 else o[t0 + 1]
            scalar_gross = (exit_net - entry_px) / PIP if s == 1 else (entry_px - exit_net) / PIP
            assert abs(out["B2.5g2.5_gross"][pos] - scalar_gross) < 1e-9
            assert abs(out["B2.5g2.5_net_obs"][pos] - (scalar_gross - obs)) < 1e-9
    logger.info("verifikasi vektor-vs-skalar 50 event: IDENTIK")
