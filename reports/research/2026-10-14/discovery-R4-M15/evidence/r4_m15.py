# -*- coding: ascii -*-
"""Discovery R4-M15-native, bed 2024. Implementasi verbatim dari
reports/governance/2026-10-14/arsitek/spesifikasi-discovery-R4-M15.md (PRA-REGISTRASI).

M15 adalah basis tunggal. M1 2024 hanya dibaca sebagai sumber bar untuk resample.
Semua ambang jarak bersatuan ATR. Grid 8 sel beku; tidak ada parameter yang
diimprovisa. Tanpa operasi git. Output ASCII, line ending LF.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import OrderedDict

import numpy as np
import pandas as pd

# ---------------------------------------------------------------- konstanta beku
M1_PATH = r"D:\ANN\data\processed\M1\usdjpy_m1_2024.parquet"
FORBIDDEN_YEARS = ("2023", "2025", "2026")
PIP = 0.01
RACE = 10
SL_MULT = 1.5
TP_MULT = 3.0
E2_W = 12
E2_RETRACE = 0.40
E2_LENGTHS = (1, 2, 3, 4, 5)
E3_W = 16
E3_BLOCKS = 20
E3_COMPRESS = 0.5
E3_BREAK_ATR = 0.5
E3_START = 336
E1_KS = (1.0, 1.5)
E1_NS = (3, 4, 6)
E1_BODY = 0.5
E2_KS = (1.5, 2.5)
SESSIONS = ("London", "NewYork", "Tokyo", "Sydney")
COST_OBS = {"London": 0.61, "NewYork": 0.69, "Tokyo": 0.62, "Sydney": 0.80, "default": 0.65}
COST_P95 = {"London": 0.8, "NewYork": 1.2, "Tokyo": 0.9, "Sydney": 1.5, "default": 1.0}
BOOT_ITERS = 10000
BOOT_SEED = 1337
MIN_EVAL = 30
DET_CHECK = 50

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------- anti-drift: whitelist parquet
ACCESSED = []
_real_read_parquet = pd.read_parquet
_real_allowed = os.path.realpath(M1_PATH)


def _guarded_read_parquet(path, *args, **kwargs):
    resolved = os.path.realpath(str(path))
    ACCESSED.append(resolved)
    if resolved != _real_allowed:
        raise RuntimeError("PATH WHITELIST VIOLATION: %s" % resolved)
    for bad in FORBIDDEN_YEARS:
        if bad in os.path.basename(resolved):
            raise RuntimeError("FORBIDDEN YEAR FILE: %s" % resolved)
    return _real_read_parquet(path, *args, **kwargs)


pd.read_parquet = _guarded_read_parquet

LOG_LINES = []


def log(msg):
    line = str(msg)
    LOG_LINES.append(line)
    print(line, flush=True)


def write_json(name, obj):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="ascii", newline="\n") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=True, sort_keys=False)
        fh.write("\n")
    log("WROTE %s (%d bytes)" % (name, os.path.getsize(path)))


def jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================ 1. load M1 (whitelist)
log("STEP 1 load M1 2024 (whitelist)")
df = _guarded_read_parquet(M1_PATH)
df = df.sort_values("broker_time_raw", kind="mergesort").reset_index(drop=True)
m1_rows = int(len(df))
log("m1 rows = %d ; raw0 first=%s last=%s" % (m1_rows, int(df["broker_time_raw"].iloc[0]), int(df["broker_time_raw"].iloc[-1])))

# ============================================================ 2. resample M15
log("STEP 2 resample M15 (bucket penuh 15/15)")
time_utc = pd.to_datetime(df["time"], utc=True, format="ISO8601")
bucket = time_utc.dt.floor("15min")
grp = df.groupby(bucket, sort=True)
gsize = grp.size()
m15 = pd.DataFrame(
    {
        "bucket": gsize.index.to_numpy(),
        "o": grp["open"].first().to_numpy(),
        "h": grp["high"].max().to_numpy(),
        "l": grp["low"].min().to_numpy(),
        "c": grp["close"].last().to_numpy(),
        "n": grp.size().to_numpy(),
        "spread": grp["spread_pips"].max().to_numpy(),
        "raw0": grp["broker_time_raw"].first().to_numpy(),
    }
)
m15 = m15.sort_values("bucket", kind="mergesort").reset_index(drop=True)
buckets_total = int(len(m15))
mask_full = m15["n"].to_numpy() == 15
buckets_full = int(mask_full.sum())
buckets_partial = buckets_total - buckets_full
m15 = m15.loc[mask_full].reset_index(drop=True)
NB = int(len(m15))
log("buckets total=%d full=%d partial=%d ; M15 bars=%d" % (buckets_total, buckets_full, buckets_partial, NB))

o = m15["o"].to_numpy(np.float64)
h = m15["h"].to_numpy(np.float64)
l = m15["l"].to_numpy(np.float64)
c = m15["c"].to_numpy(np.float64)
spr = m15["spread"].to_numpy(np.float64)
spr_px = spr * PIP
raw0 = m15["raw0"].to_numpy(np.int64)

# ============================================================ 3. label sesi
log("STEP 3 label sesi via _eda_common")
sys.path.insert(0, "D:/ANN/notebooks/scalping")
from _eda_common import EXPECTED_FINGERPRINT, add_labels, session_fingerprint  # noqa: E402

FINGERPRINT = session_fingerprint()
assert FINGERPRINT == EXPECTED_FINGERPRINT, "SESSION FINGERPRINT MISMATCH: %s" % FINGERPRINT
lab = add_labels(pd.DataFrame({"utc": m15["bucket"]}))
sess = lab["session_label"].to_numpy().astype(object)
m15["session_label"] = sess
log("session fingerprint OK")
log("session counts: " + json.dumps({k: int(v) for k, v in pd.Series(sess).value_counts().items()}, sort_keys=True))

# ============================================================ 4. ATR(14) Wilder M15
log("STEP 4 ATR(14) Wilder, ewm alpha=1/14 adjust=False")
pc = np.empty(NB, dtype=np.float64)
pc[0] = np.nan
pc[1:] = c[:-1]
tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
tr[0] = h[0] - l[0]
atr = pd.Series(tr).ewm(alpha=1.0 / 14.0, adjust=False).mean().to_numpy(np.float64)
atr_pct = float(np.isfinite(atr).mean() * 100.0)
log("atr finite %.4f%% ; atr[0]=%.8f atr[-1]=%.8f" % (atr_pct, atr[0], atr[-1]))

# ============================================================ helper rolling
def roll_max(a, w):
    return pd.Series(a).rolling(w).max().to_numpy(np.float64)


def roll_min(a, w):
    return pd.Series(a).rolling(w).min().to_numpy(np.float64)


# ============================================================ 5. scan 8 sel
log("STEP 5 scan 8 sel (grid beku)")


def scan_e1(N, k):
    bull = (c > o).astype(np.int64)
    bear = (c < o).astype(np.int64)
    cb = np.concatenate(([0], np.cumsum(bear)))
    cu = np.concatenate(([0], np.cumsum(bull)))
    idx = np.arange(N, NB)
    run_up = (cb[idx] - cb[idx - N]) == 0
    run_dn = (cu[idx] - cu[idx - N]) == 0
    disp = c[idx] - o[idx - N]
    ok_disp = np.abs(disp) >= k * atr[idx]
    body = np.abs(c[idx] - o[idx])
    rng = h[idx] - l[idx]
    ok_body = body >= E1_BODY * rng
    ok_dir = (run_up & (bear[idx] == 1)) | (run_dn & (bull[idx] == 1))
    ok = ok_disp & ok_body & ok_dir
    t0 = idx[ok]
    side = np.where(bull[t0] == 1, 1, -1).astype(np.int8)
    return t0, side


HIW = roll_max(h, E2_W)
LOW = roll_min(l, E2_W)
DISP2 = np.full(NB, np.nan)
DISP2[E2_W:] = c[E2_W:] - c[:-E2_W]
MINL = {L: roll_min(l, L) for L in E2_LENGTHS}
MAXH = {L: roll_max(h, L) for L in E2_LENGTHS}


def scan_e2(k):
    n = NB
    t0 = np.empty(n, dtype=np.int64)
    sd = np.zeros(n, dtype=np.int8)
    found = np.zeros(n, dtype=bool)
    for L in E2_LENGTHS:
        i = np.arange(E2_W + L, n)
        e = i - L
        de = DISP2[e]
        ok_disp = np.abs(de) >= k * atr[e]
        push_up = de > 0
        push_dn = de < 0
        i_bull = c[i] > o[i]
        i_bear = c[i] < o[i]
        band = HIW[e] - LOW[e]
        up_ok = ok_disp & push_up & i_bull & ((HIW[e] - MINL[L][i]) <= E2_RETRACE * band)
        dn_ok = ok_disp & push_dn & i_bear & ((MAXH[L][i] - LOW[e]) <= E2_RETRACE * band)
        match = up_ok | dn_ok
        if not match.any():
            continue
        take = match & (~found[i])
        sel = i[take]
        t0[sel] = sel
        sd[sel] = np.where(up_ok[take], 1, -1).astype(np.int8)
        found[sel] = True
    sel = np.flatnonzero(found)
    return sel.astype(np.int64), sd[sel]


HI16 = roll_max(h, E3_W)
LO16 = roll_min(l, E3_W)
RNG16 = HI16 - LO16
MED16 = np.full(NB, np.nan)
_win = np.lib.stride_tricks.sliding_window_view(RNG16, E3_BLOCKS * E3_W + 1)
_sub = _win[:, ::-E3_W][:, 1:]
MED16[E3_BLOCKS * E3_W:] = np.nanmedian(_sub, axis=1)


def scan_e3():
    idx = np.arange(E3_START, NB)
    i1 = idx - 1
    comp = RNG16[i1] <= E3_COMPRESS * MED16[i1]
    brk_up = c[idx] >= HI16[i1] + E3_BREAK_ATR * atr[idx]
    brk_dn = c[idx] <= LO16[i1] - E3_BREAK_ATR * atr[idx]
    ok = comp & (brk_up | brk_dn)
    t0 = idx[ok]
    side = np.where(brk_up[ok], 1, -1).astype(np.int8)
    return t0, side


CELLS = []
for _N in E1_NS:
    for _k in E1_KS:
        _t, _s = scan_e1(_N, _k)
        CELLS.append(("E1_N%d_k%.1f" % (_N, _k), "E1", {"N": _N, "k": _k}, _t, _s))
for _k in E2_KS:
    _t, _s = scan_e2(_k)
    CELLS.append(("E2_W12_k%.1f" % _k, "E2", {"W": E2_W, "k": _k}, _t, _s))
_t, _s = scan_e3()
CELLS.append(("E3_W16", "E3", {"W": E3_W}, _t, _s))
for _name, _fam, _p, _t, _s in CELLS:
    log("  cell %-12s raw=%d" % (_name, len(_t)))

# ============================================================ 6. cancel beralasan
log("STEP 6 cancel beralasan (GAP, ATR_NA, OFF_SESSION)")
OFFS = np.arange(1, RACE + 1, dtype=np.int64)


def cancel_reason(t0):
    n = len(t0)
    if n == 0:
        return np.empty(0, dtype=object), 0
    boundary = (t0 + RACE) >= NB
    j = np.minimum(t0[:, None] + OFFS[None, :], NB - 1)
    noncontig = (np.diff(raw0[j], axis=1) != 900).any(axis=1)
    gap = boundary | noncontig
    atr_na = ~np.isfinite(atr[t0])
    off = np.array([s == "Off" for s in sess[t0]], dtype=bool)
    reason = np.full(n, "NONE", dtype=object)
    reason[gap] = "GAP"
    m = (~gap) & atr_na
    reason[m] = "ATR_NA"
    m = (~gap) & (~atr_na) & off
    reason[m] = "OFF_SESSION"
    return reason, n


# ============================================================ 7. race barrier
log("STEP 7 race barrier (SL=1.5*ATR, TP=3.0*ATR, j=t0+1..t0+10) + shadow kaki B")


def race_leg(side_s, entry, H, L, C, SPR, sl_px, tp_px):
    up = (side_s == 1)[:, None]
    fav = np.where(up, H, L + SPR)
    adv = np.where(up, L, H + SPR)
    s = side_s[:, None].astype(np.float64)
    tp_hit = s * (fav - entry[:, None]) >= tp_px[:, None]
    sl_hit = s * (entry[:, None] - adv) >= sl_px[:, None]
    ar = np.arange(RACE)
    tp_idx = np.where(tp_hit, ar, RACE).min(axis=1)
    sl_idx = np.where(sl_hit, ar, RACE).min(axis=1)
    amb = (tp_idx == sl_idx) & (tp_idx < RACE)
    out = np.full(len(side_s), "TIME", dtype=object)
    out[amb] = "AMBIGUOUS"
    out[(tp_idx < sl_idx) & (~amb)] = "TP"
    out[sl_idx < tp_idx] = "SL"
    rows = np.arange(len(side_s))
    tpc = np.minimum(tp_idx, RACE - 1)
    slc = np.minimum(sl_idx, RACE - 1)
    time_exit = C[:, RACE - 1] + np.where(up[:, 0], 0.0, SPR[:, RACE - 1])
    exit_px = np.full(len(side_s), np.nan)
    m_time = out == "TIME"
    m_tp = out == "TP"
    m_sl = out == "SL"
    exit_px[m_time] = time_exit[m_time]
    exit_px[m_tp] = fav[rows[m_tp], tpc[m_tp]]
    exit_px[m_sl] = adv[rows[m_sl], slc[m_sl]]
    gross = side_s.astype(np.float64) * (exit_px - entry) / PIP
    mfe = np.maximum(0.0, (s * (fav - entry[:, None])).max(axis=1)) / PIP
    mae = np.maximum(0.0, (s * (entry[:, None] - adv)).max(axis=1)) / PIP
    return out, exit_px, gross, mfe, mae


def costs_for(sess_arr):
    s = np.asarray(sess_arr, dtype=object)
    obs = np.array([COST_OBS.get(x, COST_OBS["default"]) for x in s]) + 0.3
    cons = obs + 0.2
    stress = np.array([COST_P95.get(x, COST_P95["default"]) for x in s]) + 0.3 + 0.3
    return obs, cons, stress


ALL_EV = []
for name, fam, params, t0, side in CELLS:
    n_raw = int(len(t0))
    reason, _ = cancel_reason(t0)
    keep = reason == "NONE"
    kt0 = t0[keep]
    kside = side[keep]
    kj = kt0[:, None] + OFFS[None, :]
    H = h[kj]
    L = l[kj]
    Cc = c[kj]
    SP = spr_px[kj]
    entry = o[kt0 + 1]
    atr0 = atr[kt0]
    sl_px = SL_MULT * atr0
    tp_px = TP_MULT * atr0
    sA = kside.astype(np.int64)
    sB = -sA
    outA, exA, gA, mfeA, maeA = race_leg(sA, entry, H, L, Cc, SP, sl_px, tp_px)
    outB, exB, gB, mfeB, maeB = race_leg(sB, entry, H, L, Cc, SP, sl_px, tp_px)
    c_obs, c_cons, c_stress = costs_for(sess[kt0])
    tp_pips = tp_px / PIP
    bt = pd.to_datetime(m15["bucket"].to_numpy()[kt0])
    for jpos in range(len(kt0)):
        ALL_EV.append(
            {
                "cell": name,
                "family": fam,
                "n_param": params.get("N", np.nan),
                "k_param": params.get("k", np.nan),
                "t0": int(kt0[jpos]),
                "t0_time": bt[jpos].isoformat().replace("+00:00", "Z"),
                "day": bt[jpos].strftime("%Y-%m-%d"),
                "half": "H1" if bt[jpos].month <= 6 else "H2",
                "session": sess[kt0[jpos]],
                "side": int(side[keep][jpos]),
                "atr": float(atr0[jpos]),
                "sl_price": float(sl_px[jpos]),
                "tp_price": float(tp_px[jpos]),
                "tp_pips": float(tp_pips[jpos]),
                "entry": float(entry[jpos]),
                "cost_obs": float(c_obs[jpos]),
                "cost_cons": float(c_cons[jpos]),
                "cost_stress": float(c_stress[jpos]),
                "outA": str(outA[jpos]),
                "exitA": float(exA[jpos]),
                "grossA": float(gA[jpos]),
                "netA_obs": float(gA[jpos] - c_obs[jpos]),
                "netA_cons": float(gA[jpos] - c_cons[jpos]),
                "netA_stress": float(gA[jpos] - c_stress[jpos]),
                "mfeA_pips": float(mfeA[jpos]),
                "maeA_pips": float(maeA[jpos]),
                "mfeA_R": float(mfeA[jpos] / tp_pips[jpos]),
                "outB": str(outB[jpos]),
                "exitB": float(exB[jpos]),
                "grossB": float(gB[jpos]),
                "netB_obs": float(gB[jpos] - c_obs[jpos]),
                "netB_cons": float(gB[jpos] - c_cons[jpos]),
                "netB_stress": float(gB[jpos] - c_stress[jpos]),
                "mfeB_pips": float(mfeB[jpos]),
                "maeB_pips": float(maeB[jpos]),
                "mfeB_R": float(mfeB[jpos] / tp_pips[jpos]),
                "cancel_reason": "NONE",
            }
        )
    # raw (cancelled) rows
    ct0 = t0[~keep]
    cside = side[~keep]
    for jpos in range(len(ct0)):
        bt = pd.to_datetime(m15["bucket"].to_numpy()[ct0[jpos]])
        ALL_EV.append(
            {
                "cell": name,
                "family": fam,
                "n_param": params.get("N", np.nan),
                "k_param": params.get("k", np.nan),
                "t0": int(ct0[jpos]),
                "t0_time": bt.isoformat().replace("+00:00", "Z"),
                "day": bt.strftime("%Y-%m-%d"),
                "half": "H1" if bt.month <= 6 else "H2",
                "session": sess[ct0[jpos]],
                "side": int(cside[jpos]),
                "atr": float(atr[ct0[jpos]]),
                "sl_price": np.nan,
                "tp_price": np.nan,
                "tp_pips": np.nan,
                "entry": np.nan,
                "cost_obs": np.nan,
                "cost_cons": np.nan,
                "cost_stress": np.nan,
                "outA": "CANCELLED",
                "exitA": np.nan,
                "grossA": np.nan,
                "netA_obs": np.nan,
                "netA_cons": np.nan,
                "netA_stress": np.nan,
                "mfeA_pips": np.nan,
                "maeA_pips": np.nan,
                "mfeA_R": np.nan,
                "outB": "CANCELLED",
                "exitB": np.nan,
                "grossB": np.nan,
                "netB_obs": np.nan,
                "netB_cons": np.nan,
                "netB_stress": np.nan,
                "mfeB_pips": np.nan,
                "maeB_pips": np.nan,
                "mfeB_R": np.nan,
                "cancel_reason": str(reason[~keep][jpos]),
            }
        )
    log("  cell %-12s kept_after_cancel=%d cancel=%d" % (name, int(keep.sum()), int((~keep).sum())))

ev = pd.DataFrame(ALL_EV)
ev["cancel_reason"] = ev["cancel_reason"].fillna("NONE").astype(str)
ev = ev.sort_values(["cell", "t0"], kind="mergesort").reset_index(drop=True)

# ============================================================ 8. determinisme vektor-vs-skalar
log("STEP 8 regresi determinisme: %d event pertama kaki-A" % DET_CHECK)


def scalar_legA(t0i, s):
    entry = o[t0i + 1]
    slp = SL_MULT * atr[t0i]
    tpp = TP_MULT * atr[t0i]
    out = "TIME"
    exitp = c[t0i + RACE] + (0.0 if s == 1 else spr_px[t0i + RACE])
    for kk in range(1, RACE + 1):
        jx = t0i + kk
        fav = h[jx] if s == 1 else l[jx] + spr_px[jx]
        adv = l[jx] if s == 1 else h[jx] + spr_px[jx]
        f = s * (fav - entry)
        a = s * (entry - adv)
        tph = f >= tpp
        slh = a >= slp
        if tph and slh:
            out = "AMBIGUOUS"
            exitp = np.nan
            break
        if tph:
            out = "TP"
            exitp = fav
            break
        if slh:
            out = "SL"
            exitp = adv
            break
    gross = np.nan if not np.isfinite(exitp) else s * (exitp - entry) / PIP
    best = 0.0
    worst = 0.0
    for kk in range(1, RACE + 1):
        jx = t0i + kk
        fav = h[jx] if s == 1 else l[jx] + spr_px[jx]
        adv = l[jx] if s == 1 else h[jx] + spr_px[jx]
        f = s * (fav - entry)
        a = s * (entry - adv)
        if f > best:
            best = f
        if a > worst:
            worst = a
    return out, gross, best / PIP, worst / PIP


det_rows = ev[(ev["outA"] != "CANCELLED")].head(DET_CHECK)
max_gross = 0.0
max_net = 0.0
max_mfe = 0.0
max_mae = 0.0
out_mismatch = 0
det_log = []
for _, r in det_rows.iterrows():
    sc_out, sc_gross, sc_mfe, sc_mae = scalar_legA(int(r["t0"]), int(r["side"]))
    if sc_out != r["outA"]:
        out_mismatch += 1
    if np.isfinite(sc_gross) and np.isfinite(r["grossA"]):
        max_gross = max(max_gross, abs(sc_gross - r["grossA"]))
        max_net = max(max_net, abs((sc_gross - r["cost_obs"]) - r["netA_obs"]))
    max_mfe = max(max_mfe, abs(sc_mfe - r["mfeA_pips"]))
    max_mae = max(max_mae, abs(sc_mae - r["maeA_pips"]))
assert out_mismatch == 0, "DETERMINISM OUTCOME MISMATCH n=%d" % out_mismatch
assert max_gross < 1e-9, "DETERMINISM gross diff %.3e" % max_gross
assert max_net < 1e-9, "DETERMINISM net diff %.3e" % max_net
assert max_mfe < 1e-9, "DETERMINISM mfe diff %.3e" % max_mfe
assert max_mae < 1e-9, "DETERMINISM mae diff %.3e" % max_mae
det_ok = True
det_log.append("determinism checked n=%d max|gross|diff=%.3e max|net_obs|diff=%.3e max|mfe|diff=%.3e max|mae|diff=%.3e outcome_mismatch=%d" % (len(det_rows), max_gross, max_net, max_mfe, max_mae, out_mismatch))
log("DETERMINISM PASS " + det_log[0])

# ============================================================ 9. bootstrap cluster-per-hari
log("STEP 9 bootstrap cluster-per-hari, %d iterasi, seed %d" % (BOOT_ITERS, BOOT_SEED))


def bootstrap_ci_cluster(values, days, n_iter=BOOT_ITERS, seed=BOOT_SEED):
    values = np.asarray(values, dtype=np.float64)
    days = np.asarray(days)
    n = len(values)
    if n == 0:
        return None, None, None, None
    uniq = np.unique(days)
    D = int(len(uniq))
    which = np.searchsorted(uniq, days)
    order = np.argsort(which, kind="stable")
    v_sorted = values[order]
    which_sorted = which[order]
    counts = np.bincount(which_sorted, minlength=D).astype(np.int64)
    offsets = np.concatenate(([0], np.cumsum(counts)))
    max_len = int(counts.max())
    gather = np.full((D, max_len), -1, dtype=np.int64)
    for kk in range(D):
        s0, s1 = int(offsets[kk]), int(offsets[kk + 1])
        gather[kk, : s1 - s0] = np.arange(s0, s1)
    flat = v_sorted
    rng = np.random.default_rng(seed)
    C = rng.multinomial(D, np.full(D, 1.0 / D), size=n_iter)
    med = np.empty(n_iter, dtype=np.float64)
    assert int(counts.min()) >= 1, "cluster bootstrap butuh setiap cluster punya >=1 event"
    CH = 500
    for start in range(0, n_iter, CH):
        Cc = C[start : start + CH]
        tc = Cc.sum(axis=1)
        mx = int(tc.max())
        assert mx == D, "baris resample harus berisi tepat D cluster-event"
        Cf = Cc.ravel()
        tot = int(Cf.sum())
        gpos = np.repeat(np.arange(Cf.size, dtype=np.int64), Cf)
        starts = np.repeat(np.cumsum(Cf) - Cf, Cf)
        occ = np.arange(tot, dtype=np.int64) - starts
        gday = gpos % D
        col = occ % counts[gday]
        vals = flat[gather[gday, col]].reshape(Cc.shape[0], mx)
        M = np.sort(vals, axis=1)
        nrm = tc.astype(np.int64)
        lo = (nrm - 1) // 2
        hi = nrm // 2
        ridx = np.arange(Cc.shape[0])
        med[start : start + Cc.shape[0]] = (M[ridx, lo] + M[ridx, hi]) / 2.0
    lo_ci = float(np.percentile(med, 2.5))
    hi_ci = float(np.percentile(med, 97.5))
    return lo_ci, hi_ci, float(np.median(values)), float(np.median(med))


# ============================================================ 10. vonis per sel
log("STEP 10 rekap per sel")
SUMMARY = OrderedDict()
for name, fam, params, t0, side in CELLS:
    raw = ev[ev["cell"] == name]
    cancelled = raw[raw["cancel_reason"] != "NONE"]
    cnt = {k: int((cancelled["cancel_reason"] == k).sum()) for k in ("GAP", "ATR_NA", "OFF_SESSION")}
    evald = raw[raw["cancel_reason"] == "NONE"]
    ambA = evald["outA"] == "AMBIGUOUS"
    ambB = evald["outB"] == "AMBIGUOUS"
    n_eval = int((~ambA).sum())
    E = evald[~ambA]
    Eb = evald[~ambA & (~ambB)]
    nA = len(E)
    countsA = {k: int((E["outA"] == k).sum()) for k in ("TP", "SL", "TIME", "AMBIGUOUS")}
    countsB = {k: int((E["outB"] == k).sum()) for k in ("TP", "SL", "TIME", "AMBIGUOUS")}
    decA = countsA["TP"] + countsA["SL"]
    decB = countsB["TP"] + countsB["SL"]
    wrA = float(countsA["TP"] / decA) if decA else None
    wrB = float(countsB["TP"] / decB) if decB else None
    medA = float(np.median(E["netA_obs"])) if nA else None
    medB = float(np.median(Eb["netB_obs"])) if len(Eb) else None
    medA_paired = float(np.median(Eb["netA_obs"])) if len(Eb) else None
    medA_cons = float(np.median(E["netA_cons"])) if nA else None
    medA_stress = float(np.median(E["netA_stress"])) if nA else None
    joint = OrderedDict()
    for oa in ("TP", "SL", "TIME", "AMBIGUOUS"):
        for ob in ("TP", "SL", "TIME", "AMBIGUOUS"):
            joint["A=%s|B=%s" % (oa, ob)] = int(((E["outA"] == oa) & (E["outB"] == ob)).sum())
    diff = (Eb["netA_obs"] - Eb["netB_obs"]).to_numpy(np.float64)
    diff_med = float(np.median(diff)) if len(diff) else None
    diff_share_pos = float((diff > 0).mean()) if len(diff) else None
    mfeA = float(np.median(E["mfeA_pips"])) if nA else None
    mfeB = float(np.median(E["mfeB_pips"])) if nA else None
    mfeAR = float(np.median(E["mfeA_R"])) if nA else None
    mfeBR = float(np.median(E["mfeB_R"])) if nA else None
    share_mfeA_1R = float((E["mfeA_R"] >= 1.0).mean()) if nA else None
    share_mfeB_1R = float((E["mfeB_R"] >= 1.0).mean()) if nA else None
    maeA = float(np.median(E["maeA_pips"])) if nA else None
    maeB = float(np.median(E["maeB_pips"])) if nA else None
    lo_ci, hi_ci, pt_med, boot_med = (None, None, None, None)
    if nA > 0:
        lo_ci, hi_ci, pt_med, boot_med = bootstrap_ci_cluster(E["netA_obs"].to_numpy(np.float64), E["day"].to_numpy())
    h1 = E[E["half"] == "H1"]["netA_obs"]
    h2 = E[E["half"] == "H2"]["netA_obs"]
    med_h1 = float(np.median(h1)) if len(h1) else None
    med_h2 = float(np.median(h2)) if len(h2) else None
    n_h1, n_h2 = int(len(h1)), int(len(h2))
    if n_h1 and n_h2:
        s1 = 1 if med_h1 > 0 else -1
        s2 = 1 if med_h2 > 0 else -1
        same_sign = bool(s1 == s2)
        sign_txt = "+" if s1 > 0 else "-"
    else:
        same_sign = False
        sign_txt = "NA"
    fmap = OrderedDict()
    for s in SESSIONS:
        sub = E[E["session"] == s]
        fmap[s] = OrderedDict(
            {
                "n": int(len(sub)),
                "median_netA_obs": float(np.median(sub["netA_obs"])) if len(sub) else None,
                "median_netB_obs": float(np.median(sub["netB_obs"])) if len(sub) else None,
            }
        )
    missing_sessions = [s for s in SESSIONS if fmap[s]["n"] == 0]
    n_missing_outcome = int(E["grossA"].isna().sum())
    unexplained_gap = bool(missing_sessions) or n_missing_outcome > 0
    crit = OrderedDict()
    if n_eval < MIN_EVAL:
        verdict = "TAK-TERUJI"
        reason = "n_eval=%d < %d (bukan gagal, bukan lolos)" % (n_eval, MIN_EVAL)
    else:
        crit["i_median_net_obs_A_gt0"] = bool(medA is not None and medA > 0)
        crit["ii_ci_lower_gt0"] = bool(lo_ci is not None and lo_ci > 0)
        crit["iii_same_sign_h1_h2"] = bool(same_sign)
        crit["iv_failure_map_complete"] = bool(not unexplained_gap)
        if not crit["i_median_net_obs_A_gt0"] or not crit["ii_ci_lower_gt0"] or not crit["iii_same_sign_h1_h2"]:
            verdict = "TOLAK"
            failed = [k for k in ("i_median_net_obs_A_gt0", "ii_ci_lower_gt0", "iii_same_sign_h1_h2") if not crit[k]]
            reason = "gagal: " + ",".join(failed)
        elif not crit["iv_failure_map_complete"]:
            verdict = "BELUM JELAS"
            reason = "(i)-(iii) benar, (iv) gagal: sesi hilang=%s ; event tanpa outcome=%d" % (missing_sessions, n_missing_outcome)
        else:
            verdict = "KANDIDAT"
            reason = "(i)-(iv) semuanya benar"
    SUMMARY[name] = OrderedDict(
        {
            "family": fam,
            "params": params,
            "n_raw": int(len(raw)),
            "cancel": cnt,
            "n_cancelled_total": int(len(cancelled)),
            "n_after_cancel": int(len(evald)),
            "n_ambiguous_A": int(ambA.sum()),
            "n_ambiguous_B": int(ambB.sum()),
            "n_eval": n_eval,
            "outcome_A": countsA,
            "outcome_B": countsB,
            "decisive_A": decA,
            "decisive_B": decB,
            "winrate_decisive_A": wrA,
            "winrate_decisive_B": wrB,
            "median_net_obs_A": medA,
            "median_net_obs_B": medB,
            "median_net_obs_A_paired_subset": medA_paired,
            "median_net_cons_A": medA_cons,
            "median_net_stress_A": medA_stress,
            "shadow_joint_matrix": joint,
            "shadow_paired": {
                "n_pairs": int(len(diff)),
                "median_netA_minus_netB_obs": diff_med,
                "share_gt0": diff_share_pos,
                "median_MFE_A_pips": mfeA,
                "median_MFE_B_pips": mfeB,
                "median_MFE_A_R": mfeAR,
                "median_MFE_B_R": mfeBR,
                "median_MAE_A_pips": maeA,
                "median_MAE_B_pips": maeB,
                "share_MFE_A_ge_1R": share_mfeA_1R,
                "share_MFE_B_ge_1R": share_mfeB_1R,
            },
            "bootstrap": {
                "point_median_netA_obs": pt_med,
                "bootstrap_median_of_medians": boot_med,
                "ci95_lower": lo_ci,
                "ci95_upper": hi_ci,
                "n_clusters_days": int(len(np.unique(E["day"]))) if nA else 0,
                "iters": BOOT_ITERS,
                "seed": BOOT_SEED,
                "method": "cluster-per-hari multinomial, bootstrap percentile 2.5/97.5",
            },
            "half_split": {
                "H1_n": n_h1,
                "H1_median_netA_obs": med_h1,
                "H2_n": n_h2,
                "H2_median_netA_obs": med_h2,
                "same_sign": same_sign,
                "sign": sign_txt,
            },
            "failure_map": fmap,
            "missing_sessions": missing_sessions,
            "n_event_without_outcome": n_missing_outcome,
            "criteria": crit,
            "verdict": verdict,
            "verdict_reason": reason,
        }
    )
    log("  %-12s raw=%4d n_eval=%4d medA=%s pt=%s ci=[%s,%s] verdict=%s" % (name, len(raw), n_eval, ("%.4f" % medA) if medA is not None else "NA", ("%.4f" % pt_med) if pt_med is not None else "NA", ("%.4f" % lo_ci) if lo_ci is not None else "NA", ("%.4f" % hi_ci) if hi_ci is not None else "NA", verdict))

# ============================================================ 11. artefak
log("STEP 11 tulis artefak")
contig = (np.diff(raw0) == 900)
qc = OrderedDict()
qc["spec"] = "spesifikasi-discovery-R4-M15.md (PRA-REGISTRASI, 2026-10-14)"
qc["run_date"] = "2026-10-14"
qc["bed"] = "2024"
qc["versions"] = {"numpy": np.__version__, "pandas": pd.__version__, "python": sys.version.split()[0]}
qc["session_fingerprint"] = FINGERPRINT
qc["session_fingerprint_expected"] = EXPECTED_FINGERPRINT
qc["session_fingerprint_match"] = True
qc["path_whitelist"] = {"allowed": [_real_allowed], "accessed": ACCESSED, "forbidden_years": list(FORBIDDEN_YEARS), "violations": 0}
qc["whitelist_note"] = "hanya usdjpy_m1_2024.parquet yang dibaca; tidak ada file 2023/2025/2026 yang diakses"
qc["m1_rows_source"] = m1_rows
qc["m15_buckets_total"] = buckets_total
qc["m15_buckets_full_15"] = buckets_full
qc["m15_buckets_partial_dropped"] = buckets_partial
qc["m15_bars"] = NB
qc["m15_contiguity_pct"] = float(contig.mean() * 100.0)
qc["m15_contiguity_pairs_ok"] = int(contig.sum())
qc["m15_noncontig_pairs"] = int((~contig).sum())
qc["spread_per_bucket_is_max_conservative"] = True
qc["pip_definition"] = {"PIP_price_units": PIP, "basis": "USDJPY 1 pip = 0.01 harga; spread_pips dikonversi ke satuan harga dengan spread_price = spread_pips * PIP"}
qc["spread_pips_stats"] = {
    "mean": float(np.mean(spr)),
    "median": float(np.median(spr)),
    "p95": float(np.percentile(spr, 95)),
    "max": float(np.max(spr)),
}
qc["atr_available_pct"] = atr_pct
qc["atr_first_valid_index"] = int(np.flatnonzero(np.isfinite(atr))[0])
qc["atr_note"] = "tr[0]=h[0]-l[0] (Wilder); ewm adjust=False; kausal"
qc["cost_table"] = {"COST_OBS": COST_OBS, "COST_P95": COST_P95, "obs": "COST_OBS+0.3", "cons": "obs+0.2", "stress": "COST_P95+0.6"}
qc["barrier"] = {"sl_atr_mult": SL_MULT, "tp_atr_mult": TP_MULT, "rr": 2.0, "race_bars": RACE, "entry": "OPEN bar t0+1", "twin_bar": "AMBIGUOUS (buang + hitung eksplisit)", "time_exit": "close bar ke-10 sisi keluar"}
qc["cancel_order"] = ["GAP", "ATR_NA", "OFF_SESSION"]
qc["events_per_cell"] = OrderedDict((k, v["n_raw"]) for k, v in SUMMARY.items())
qc["cancel_per_cell"] = OrderedDict((k, v["cancel"]) for k, v in SUMMARY.items())
qc["n_eval_per_cell"] = OrderedDict((k, v["n_eval"]) for k, v in SUMMARY.items())
qc["determinism_check"] = {"n_checked": int(len(det_rows)), "max_abs_gross_diff": max_gross, "max_abs_net_obs_diff": max_net, "max_abs_mfe_diff": max_mfe, "max_abs_mae_diff": max_mae, "outcome_mismatch": out_mismatch, "passed": det_ok}
qc["shadow_note"] = "kaki B cermin memakai entry/waktu/barrier/biaya identik; tidak mengubah vonis"
qc["verdicts"] = OrderedDict((k, v["verdict"]) for k, v in SUMMARY.items())
qc["total_events_rows"] = int(len(ev))

write_json("qc.json", jsonable(qc))
write_json("summary.json", jsonable(SUMMARY))

ev.to_parquet(os.path.join(HERE, "events.parquet"), index=False)
log("WROTE events.parquet (%d bytes, %d rows)" % (os.path.getsize(os.path.join(HERE, "events.parquet")), len(ev)))

log("DONE R4-M15-native")
