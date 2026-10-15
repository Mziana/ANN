"""Generator + executor for notebooks/scalping/eda_07_spike_anatomy_outcome.ipynb.

EDA-07 spike_anatomy_outcome (Blueprint FINAL 2026-10-15-eda07-spike-anatomy):
deskriptif murni atas pool spike mentah R — base rate "terbalas",
karakteristik pra/pasca, hubungan magnitudo -> outcome, Q1-sub (bar-ke),
Q3-sub (net vs range), kill dua lapis (rate vs koin; trade implisit vs biaya).

Warisan verbatim EDA-06: scan_spikes, first_exhaustion, first-passage
(tie SL-dulu), null-machine pola placebo (diadaptasi tertulis §F6),
kelas hari A/B/C (resep T_DAY), biaya 0.95 flat, seed 20261006/20261007.

Pre-flight terkunci (F1/F0a-terkoreksi/F0b/F2/F4 HIJAU, F6 disahkan):
2116 = 856+1260; overlap 484; Nunik 1632; bands 515/415/240/462.
Resolusi 379 tersanksi: split sesi/jam atas 384 hari bersih yang sama.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_07_spike_anatomy_outcome.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA-07 — spike_anatomy_outcome (deskriptif murni)

**Blueprint:** `thoughts/shared/plans/2026-10-15-eda07-spike-anatomy.md` (§§1–13, FINAL).
**Status EDA-06:** CLOSED — spike+exhaustion → open terbukti eksis (51 event) tapi UNDERPOWERED.
Ronde ini menjawab base rate + anatomi; entry test = EDA-08/09.

## Aturan yang mengikat notebook ini
- **Warisan EDA-06 verbatim:** `scan_spikes` (range > thresh×ATR, ekstensi ≤2 bar,
  cooldown 16, mulai bar-4, `j >= n: break` = larangan cross-day),
  `first_exhaustion`, first-passage K=16 tie-SL-dulu, kelas hari, biaya 0.95.
- **Populasi unik:** 2116 deteksi → dedup overlap keep-max → **Nunik=1632**;
  band DISJOINT [1.5–2.0)/[2.0–2.5)/[2.5–3.0)/[3.0+); `mag_cont` kontinu di parquet.
- **Kill dua lapis:** L1 = bawah-CI95 reversal-rate agregat vs 50% (koin);
  L2 = mean net (biaya 0.95) ≤ 0 atau CI lewati 0 → GUGUR. Stres 2× tanpa daya bunuh.
- **STOP discipline:** assertion crash = sinyal bug. Sel/stratum <30 → drop+label.
- **Null F6 (disahkan):** permutasi jalur-16-bar pasca-spike; jendela donor =
  bar s+1..s+16 milik spike donor (ber-ruang-penuh); entry null = close bar
  PERTAMA jendela donor (analog exact close(s+1) sisi origin); TP/SL/prefilter
  dari spike asal. B=10000, seed null 20261007, bootstrap 20261006.
- **Parquet ditulis SEBELUM vonis.** P segel; arsip frozen; 384 hari bersih
  untuk agregat DAN split (resolusi 379 tersanksi — caveat di Sel penutup).
"""
)

code(
    '''"""Sel 1 — setup, kontrak terkunci, partisi R (384 hari bersih)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def find_project_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    raise RuntimeError("PROJECT_ROOT tidak ditemukan")


PROJECT_ROOT = find_project_root(Path.cwd().resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.broker_time import wall_clock_series  # noqa: E402
from src.utils.config import load_config  # noqa: E402

# ---- Kontrak terkunci ----
PIP = 0.01
COST = 0.95
COST_STRESS = 1.90
PREFILTER_NET = 2.85
KILL_K = 16
WIN = 16
DAILY_OPEN_HOURS = [22, 23]
R_START = pd.Timestamp("2023-07-01", tz="UTC")
R_END_EXCL = pd.Timestamp("2025-01-01", tz="UTC")
SEED_BOOT = 20261006
SEED_NULL = 20261007
N_BOOT = 10_000
N_NULL = 10_000
FDR_Q = 0.10
POWER_MIN_N = 30
BAND_EDGES = [1.5, 2.0, 2.5, 3.0]
EPS = 1e-6
HOUR_BINS = [(4, 10), (11, 20), (21, 32), (33, 10**9)]

assert DAILY_OPEN_HOURS == [22, 23]
assert (COST, COST_STRESS, KILL_K, N_BOOT, N_NULL) == (0.95, 1.90, 16, 10_000, 10_000)


def _find_key(node, target):
    if isinstance(node, dict):
        if target in node:
            return node[target]
        for value in node.values():
            hit = _find_key(value, target)
            if hit is not None:
                return hit
    return None


cfg = load_config("data")
anom_cfg = _find_key(cfg, "anomaly_windows")
assert anom_cfg, "anomaly_windows hilang (reuse gagal)"
ANOMALY = [(pd.Timestamp(w["start"]).date(), pd.Timestamp(w["end"]).date()) for w in anom_cfg]

DATA = PROJECT_ROOT / "data" / "processed"


def _load(tf: str) -> pd.DataFrame:
    frames = [pd.read_parquet(DATA / tf / f"usdjpy_{tf.lower()}_{y}.parquet") for y in (2023, 2024)]
    df = pd.concat(frames, ignore_index=True)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df = df.sort_values("time").reset_index(drop=True)
    df["broker_time"] = wall_clock_series(df["broker_time_raw"])
    df["broker_day"] = df["broker_time"].dt.date
    return df


m15 = _load("M15")
d1 = _load("D1")
anom_days: set = set()
for start, end in ANOMALY:
    anom_days.update(pd.date_range(start, end).date)
r = m15[(m15["time"] >= R_START) & (m15["time"] < R_END_EXCL)].copy()
assert r["time"].max() < R_END_EXCL
r = r[~r["broker_day"].isin(anom_days)].copy()
assert not r["broker_day"].isin(anom_days).any()

DAYS: dict = {}
for day, g in r.groupby("broker_day"):
    g = g.sort_values("time").reset_index(drop=True)
    if g["time"].iloc[0].hour not in DAILY_OPEN_HOURS:
        continue
    DAYS[day] = {"frame": g, "open": float(g["open"].iloc[0])}
print(f"R: {len(r)} bar | hari bersih = {len(DAYS)} (ekspektasi 384)")
assert len(DAYS) == 384, "partisi R != 384 → STOP"
print("SEL 1 SELESAI")
'''
)

md(
    """## Sel 2 — Indikator Wilder, konteks hari, kelas A/B/C, sesi

ATR14/RSI14 Wilder (shift-1 untuk ATR, tanpa look-ahead). Konteks = range
5-hari / ATR D1. $T_{day}$ = P25 konteks atas basis resep EDA-06 (exhaustion +
waktu + prefilter) — nilai harapan 1.7319 (di-assert). Kelas: B bila
ctx < $T_{day}$, else A/C dari tanda return 5-hari (operasionalisasi warisan
EDA-06). Sesi DST-aware via `_eda_common` (fingerprint di-assert).
"""
)

code(
    '''"""Sel 2 — indikator + T_DAY (resep EDA-06) + kelas hari + sesi."""
NSMOOTH = 14


def _wilder_ema(series: pd.Series, n: int = NSMOOTH) -> pd.Series:
    return series.ewm(alpha=1.0 / n, adjust=False).mean()


_prev = m15["close"].shift(1)
_tr = pd.concat(
    [m15["high"] - m15["low"], (m15["high"] - _prev).abs(), (m15["low"] - _prev).abs()],
    axis=1,
).max(axis=1)
m15["atr"] = _wilder_ema(_tr).shift(1)
_delta = m15["close"].diff()
_rs = _wilder_ema(_delta.clip(lower=0)) / _wilder_ema((-_delta).clip(lower=0))
m15["rsi"] = 100.0 - 100.0 / (1.0 + _rs)

d1 = d1.sort_values("time").reset_index(drop=True)
_dprev = d1["close"].shift(1)
_dtr = pd.concat(
    [d1["high"] - d1["low"], (d1["high"] - _dprev).abs(), (d1["low"] - _dprev).abs()],
    axis=1,
).max(axis=1)
d1["atr"] = _wilder_ema(_dtr)
d1["bday"] = pd.to_datetime(d1["broker_time_raw"], unit="s").dt.date


def day_ctx(day):
    past = d1[d1["bday"] < day].tail(5)
    if len(past) < 5 or not np.isfinite(past["atr"].iloc[-1]) or past["atr"].iloc[-1] <= 0:
        return None
    return float((past["high"].max() - past["low"].min()) / past["atr"].iloc[-1])


for day, info in DAYS.items():
    g = info["frame"]
    idx = m15.index[m15["time"] == g["time"].iloc[0]][0]
    info["frame"] = g.assign(atr=m15["atr"].iloc[idx : idx + len(g)].to_numpy(),
                             rsi=m15["rsi"].iloc[idx : idx + len(g)].to_numpy()).reset_index(drop=True)
    info["ctx"] = day_ctx(day)
assert sum(1 for v in DAYS.values() if v["ctx"] is not None) / len(DAYS) > 0.95


def scan_spikes(g: pd.DataFrame, thresh: float) -> list:
    """Warisan verbatim EDA-06 (TERKUNCI blueprint §3)."""
    out, i, n = [], 4, len(g)
    H, L, C, O = (g["high"].to_numpy(), g["low"].to_numpy(),
                  g["close"].to_numpy(), g["open"].to_numpy())
    while i < n:
        atr = float(g["atr"].iloc[i])
        if not np.isfinite(atr) or atr <= 0:
            i += 1
            continue
        if H[i] - L[i] > thresh * atr:
            sdir = 1 if C[i] >= O[i] else -1
            hi, lo, s = H[i], L[i], i
            for j in (i + 1, i + 2):
                if j >= n:
                    break
                if sdir == 1 and C[j] > C[s]:
                    hi, lo, s = max(hi, H[j]), min(lo, L[j]), j
                elif sdir == -1 and C[j] < C[s]:
                    hi, lo, s = max(hi, H[j]), min(lo, L[j]), j
                else:
                    break
            out.append((i, s, sdir, float(hi), float(lo)))
            i = s + 16
        else:
            i += 1
    return out


def first_exhaustion(g: pd.DataFrame, s: int, sdir: int):
    """Warisan verbatim EDA-06."""
    rsi = g["rsi"].to_numpy()
    for k in range(s + 1, min(s + 7, len(g))):
        v = rsi[k]
        if not np.isfinite(v):
            continue
        if (sdir == 1 and v >= 70) or (sdir == -1 and v <= 30):
            return k
    return None


basis_ctx = []
for day in sorted(DAYS):
    info = DAYS[day]
    g = info["frame"]
    for (i, s, sdir, hi, lo) in scan_spikes(g, 2.0):
        rr = first_exhaustion(g, s, sdir)
        if rr is None or rr + 1 > 32:
            continue
        if abs(float(g["close"].iloc[rr]) - info["open"]) / PIP <= PREFILTER_NET:
            continue
        if info["ctx"] is not None:
            basis_ctx.append(info["ctx"])
T_DAY = float(np.percentile(np.array(basis_ctx), 25))
print(f"T_DAY = P25 = {T_DAY:.4f} (n={len(basis_ctx)}, ekspektasi 1.7319)")
assert round(T_DAY, 4) == 1.7319, "T_DAY drift vs EDA-06 → STOP"


def day_class(day) -> str:
    ctx = DAYS[day]["ctx"]
    if ctx is None or ctx < T_DAY:
        return "B"
    past = d1[d1["bday"] < day].tail(5)
    return "A" if float(past["close"].iloc[-1] - past["close"].iloc[0]) > 0 else "C"


for day in DAYS:
    DAYS[day]["cls"] = day_class(day)

sys.path.insert(0, str(PROJECT_ROOT / "notebooks/scalping"))
from _eda_common import exclusive_label, session_fingerprint, session_flags  # noqa: E402
from _eda_common import EXPECTED_FINGERPRINT  # noqa: E402

assert session_fingerprint() == EXPECTED_FINGERPRINT, "definisi sesi berubah → STOP"
for day, info in DAYS.items():
    g = info["frame"]
    flags = session_flags(g["time"])
    info["sess"] = exclusive_label(flags).to_numpy()
from collections import Counter
print("kelas hari:", dict(Counter(v["cls"] for v in DAYS.values())))
print("SEL 2 SELESAI")
'''
)

md(
    """## Sel 3 — Scan dua ambang, dedup overlap, band, anatomi

F0a/F0b sebagai assertion mesin: split 856+1260=2116, pasangan overlap 484,
Nunik=1632, band 515/415/240/462, overflow 5. Wakil grup = magnitudo terbesar
(`mag_cont=(hi−lo)/atr_s` disimpan kontinu — anti-cliff). Anatomi: pre_1..10
(relatif r bila exhaustion else s), micro 12-bar, jarak close(i−1)→open,
persentil rolling-500, RSI-i/s, jam UTC + sesi + bin bar (bin-1 = 4–10:
scan mulai bar-4 sehingga s=4 mungkin — deviasi terdokumentasi, hitungan
s<5 dicetak sebagai bukti).
"""
)

code(
    '''"""Sel 3 — dedup, band, anatomi (F0a/F0b = assertion mesin)."""
DET = []
for day in sorted(DAYS):
    g = DAYS[day]["frame"]
    for thresh in (2.0, 1.5):
        for (i, s, sdir, hi, lo) in scan_spikes(g, thresh):
            DET.append((day, thresh, i, s, sdir, hi, lo, float(g["atr"].iloc[s])))
n20 = sum(1 for d in DET if d[1] == 2.0)
n15 = sum(1 for d in DET if d[1] == 1.5)
assert (n20, n15, len(DET)) == (856, 1260, 2116), f"F0a: {(n20, n15, len(DET))} → STOP"

parent = list(range(len(DET)))


def _find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


by_day = {}
for k, d in enumerate(DET):
    by_day.setdefault(d[0], []).append(k)
pairs = 0
for day, idxs in by_day.items():
    a = [k for k in idxs if DET[k][1] == 2.0]
    b = [k for k in idxs if DET[k][1] == 1.5]
    for ka in a:
        for kb in b:
            if DET[ka][4] == DET[kb][4] and DET[ka][2] <= DET[kb][3] and DET[kb][2] <= DET[ka][3]:
                pairs += 1
                ra, rb = _find(ka), _find(kb)
                if ra != rb:
                    parent[rb] = ra
assert pairs == 484, f"F0a overlap: {pairs} != 484 → STOP"
groups = {}
for k in range(len(DET)):
    groups.setdefault(_find(k), []).append(k)
assert len(groups) == 1632, f"F0b Nunik: {len(groups)} → STOP"

UNIQ = []
overflow = 0
for members in groups.values():
    mag, k = max(((DET[k][5] - DET[k][6]) / DET[k][7], k) for k in members)
    day, thresh, i, s, sdir, hi, lo, atr_s = DET[k]
    band = next((bi for bi, (lo_, hi_) in enumerate(
        [(1.5, 2.0), (2.0, 2.5), (2.5, 3.0), (3.0, np.inf)]) if lo_ <= mag < hi_), None)
    if band is None:
        band, overflow = 0, overflow + 1
    info = DAYS[day]
    g = info["frame"]
    H, L, C, O = (g["high"].to_numpy(), g["low"].to_numpy(),
                  g["close"].to_numpy(), g["open"].to_numpy())
    rr = first_exhaustion(g, s, sdir)
    has_exh = rr is not None
    ref = rr if has_exh else s
    pre_size = [float((H[k2] - L[k2]) / PIP) if k2 >= 0 else np.nan
                for k2 in range(ref - 1, ref - 11, -1)]
    pre_dir = [int(np.sign(C[k2] - O[k2])) if k2 >= 0 else 0
               for k2 in range(ref - 1, ref - 11, -1)]
    f4 = g.iloc[:4]
    or_top, or_bottom = float(f4["high"].max()), float(f4["low"].min())
    micro_box, micro_dist = np.nan, np.nan
    if i >= 12:
        pre12 = g.iloc[i - 12 : i]
        atr_i = float(g["atr"].iloc[i])
        micro_box = float((pre12["high"].max() - pre12["low"].min()) / atr_i)
        micro_dist = float(max(min(abs(c - or_top), abs(c - or_bottom))
                               for c in pre12["close"].to_numpy()) / atr_i)
    rng_i = H[i] - L[i]
    base = g.iloc[max(0, i - 500) : i]
    pctl = float((base["high"] - base["low"] < rng_i).mean()) if len(base) >= 50 else np.nan
    sb = s
    hbin = next(name for name, (lo_, hi_) in
                zip(("b04_10", "b11_20", "b21_32", "b33p"), HOUR_BINS) if lo_ <= sb <= hi_)
    UNIQ.append({"day": day, "i": i, "s": s, "sdir": sdir, "hi": hi, "lo": lo,
                 "atr_s": atr_s, "mag": mag, "band": band,
                 "has_exh": has_exh, "r_bar": rr if has_exh else -1,
                 "or_top": or_top, "or_bottom": or_bottom,
                 "pre_size": pre_size, "pre_dir": pre_dir,
                 "micro_box": micro_box, "micro_dist": micro_dist,
                 "dist_open": float((C[i - 1] - info["open"]) / PIP),
                 "pctl500": pctl,
                 "body": abs(C[i] - O[i]) / rng_i if rng_i > 0 else np.nan,
                 "rsi_i": float(g["rsi"].iloc[i]), "rsi_s": float(g["rsi"].iloc[s]),
                 "utc_hour": int(g["time"].iloc[s].hour),
                 "sess": str(info["sess"][s]), "hbin": hbin,
                 "cls": info["cls"], "ctx": info["ctx"]})
assert overflow == 5, f"overflow: {overflow} != 5 → STOP"
bc = pd.Series([u["band"] for u in UNIQ]).value_counts().sort_index()
assert bc.to_dict() == {0: 515, 1: 415, 2: 240, 3: 462}, f"band: {bc.to_dict()} → STOP"
assert all(sum(1 for lo_, hi_ in [(1.5, 2.0), (2.0, 2.5), (2.5, 3.0), (3.0, np.inf)]
                 if lo_ <= u["mag"] < hi_) == 1 or u["mag"] < 1.5 for u in UNIQ)
first_idx = {}
for n, u in enumerate(UNIQ):
    if u["day"] not in first_idx or u["i"] < UNIQ[first_idx[u["day"]]]["i"]:
        first_idx[u["day"]] = n
for n, u in enumerate(UNIQ):
    u["first_of_day"] = (first_idx[u["day"]] == n)
print(f"UNIQ={len(UNIQ)} band={bc.to_dict()} overflow={overflow} "
      f"first_of_day={sum(1 for u in UNIQ if u['first_of_day'])} "
      f"s_lt5={sum(1 for u in UNIQ if u['s'] < 5)} (bin-1 mulai bar-4 "
      f"karena scan mulai bar-4 — deviasi terdokumentasi dari bin 5-10 blueprint)")
print("SEL 3 SELESAI")
'''
)

md(
    """## Sel 4 — Outcome machine + Q1-sub + Q3-sub

Level = (hi+lo)/2; reversal-A primer = SENTUHAN PERTAMA level dalam s+1..s+16
(wick dihitung: spike naik via low ≤ level, turun via high ≥ level — §3 verbatim,
BUKAN close-crossing); continuation = close pertama ≥ ekstrem+1×atr_s searah.
Sentuh-dulu-menang antar-bar; tie se-bar = continuation menang (TERKUNCI).
Timeout bila tak ada keduanya. F2 = exemplars pre-flight tersanksi sebagai
assertion mesin (bukan first-found). F5 = drop per band/jam. Q1-sub = distribusi bar-ke reversal (event terbalas saja + n_rev/n_band).
Q3-sub (§2.6, SPIKE-LEVEL atas semua 1632 unik): net = sdir×(close(s)−open(i)),
|net| ≤ range selalu → A1 |rasio| ≤ 1+eps; wick = range−|net| (pip + ×atr_s);
negatif-dalam-eps → clamp 0 + counter, melebihi eps → crash.
"""
)

code(
    '''"""Sel 4 — outcome machine (§5 verbatim), A2, F2, F5, Q1-sub, Q3-sub."""
def _boot_ci(vals, day_ids, stat, seed=SEED_BOOT, b=N_BOOT):
    rng = np.random.default_rng(seed)
    vals = np.asarray(vals, dtype=float)
    day_ids = np.asarray(day_ids)
    days = np.unique(day_ids)
    per = [vals[day_ids == d] for d in days]
    boots = np.empty(b)
    for k in range(b):
        pick = rng.integers(0, len(days), len(days))
        boots[k] = stat(np.concatenate([per[j] for j in pick]))
    return float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


OUT = {}
for n, u in enumerate(UNIQ):
    g = DAYS[u["day"]]["frame"]
    nn = len(g)
    H, L, C = (g["high"].to_numpy(), g["low"].to_numpy(), g["close"].to_numpy())
    s, sdir, hi, lo, atr_s = u["s"], u["sdir"], u["hi"], u["lo"], u["atr_s"]
    if s + WIN >= nn:
        OUT[n] = {"drop": True, "reason": "no_room_16"}
        continue
    level = (hi + lo) / 2.0
    extreme = hi if sdir == 1 else lo
    res = None
    for bb in range(s + 1, s + 17):
        rev = (L[bb] <= level) if sdir == 1 else (H[bb] >= level)
        cont = (C[bb] - extreme) * sdir >= atr_s
        if rev and cont:
            res = ("continuation", bb)
            break
        if rev:
            res = ("reversal", bb)
            break
        if cont:
            res = ("continuation", bb)
            break
    if res is None:
        OUT[n] = {"drop": False, "outcome": "timeout", "bar_ke": -1,
                  "adv": np.nan, "fth": np.nan}
        continue
    oc, bbar = res
    rec = {"drop": False, "outcome": oc, "bar_ke": bbar - s,
           "adv": np.nan, "fth": np.nan}
    if oc == "reversal":
        seg = slice(s + 1, bbar + 1)
        rec["adv"] = (float(np.max(H[seg] - level)) / atr_s if sdir == 1
                      else float(np.max(level - L[seg])) / atr_s)
        full = slice(s + 1, s + 17)
        rec["fth"] = (float(np.max(level - L[full])) / atr_s if sdir == 1
                      else float(np.max(H[full] - level)) / atr_s)
    OUT[n] = rec

AN = [n for n in range(len(UNIQ)) if not OUT[n]["drop"]]
print(f"analyzed={len(AN)} dropped={len(UNIQ) - len(AN)}")
for b in range(4):
    idx = [n for n in AN if UNIQ[n]["band"] == b]
    cr = sum(1 for n in idx if OUT[n]["outcome"] == "reversal")
    cc = sum(1 for n in idx if OUT[n]["outcome"] == "continuation")
    ct = sum(1 for n in idx if OUT[n]["outcome"] == "timeout")
    assert cr + cc + ct == len(idx), f"A2 band {b}: {cr}+{cc}+{ct}!={len(idx)} → STOP"
    print(f"A2 band{b}: n={len(idx)} rev={cr} cont={cc} timeout={ct}")
from datetime import date as _date
F2_EXP = [
    {"day": _date(2023, 7, 3), "i": 31, "s": 31, "oc": "reversal", "bar_ke": 1},
    {"day": _date(2023, 7, 3), "i": 57, "s": 59, "oc": "continuation", "bar_ke": 4},
    {"day": _date(2023, 7, 4), "i": 66, "s": 68, "oc": "timeout", "bar_ke": -1},
]
_root_of = {}
for _ui, _members in enumerate(groups.values()):
    for _kk in _members:
        _root_of[_kk] = _ui
for _e in F2_EXP:
    _ks = [k for k, d in enumerate(DET)
           if d[0] == _e["day"] and d[2] == _e["i"] and d[3] == _e["s"]]
    assert _ks, f"F2 exemplar tak ada di DET: {_e} → STOP"
    _nn = _root_of[_find(_ks[0])]
    _oo = OUT[_nn]
    assert (not _oo["drop"] and _oo["outcome"] == _e["oc"]
            and _oo["bar_ke"] == _e["bar_ke"]), f"F2 meleset: {_e} vs {_oo} → STOP"
    _u0 = UNIQ[_nn]
    print(f"F2 {_e['oc']}: {_u0['day']} i={_u0['i']} s={_u0['s']} "
          f"sdir={_u0['sdir']} band={_u0['band']} bar_ke={_oo['bar_ke']} "
          f"mag={_u0['mag']:.3f} exh={_u0['has_exh']} ✓")
bd = pd.Series([UNIQ[n]["band"] for n in range(len(UNIQ)) if OUT[n]["drop"]])
print("F5 drop per band:", bd.value_counts().sort_index().to_dict() or {})
hd = pd.Series([UNIQ[n]["utc_hour"] for n in range(len(UNIQ)) if OUT[n]["drop"]])
print("F5 drop per jam-UTC:", hd.value_counts().sort_index().to_dict() or {})

DAYCODE = {d: k for k, d in enumerate(sorted(DAYS))}
Q1, Q3 = {}, {}
clamp_ctr = 0
for key in ("agg", 0, 1, 2, 3):
    ridx = [n for n in AN if OUT[n]["outcome"] == "reversal"
            and (key == "agg" or UNIQ[n]["band"] == key)]
    n_band = len([n for n in AN if key == "agg" or UNIQ[n]["band"] == key])
    if len(ridx) < POWER_MIN_N:
        Q1[key] = {"n": len(ridx), "status": "point-only (n<30) — tidak dipakai"}
        print(f"Q1 {key}: n_rev={len(ridx)}/n_band={n_band} → drop+label")
    else:
        bk = np.array([OUT[n]["bar_ke"] for n in ridx], dtype=float)
        dk = np.array([DAYCODE[UNIQ[n]["day"]] for n in ridx])
        lo, hi = _boot_ci(bk, dk, np.median)
        Q1[key] = {"n": len(ridx), "n_band": n_band,
                   "median": float(np.median(bk)),
                   "iqr": [float(np.percentile(bk, 25)), float(np.percentile(bk, 75))],
                   "ci95": [lo, hi], "status": "ok"}
UQ3 = {}
for n, u in enumerate(UNIQ):
    g = DAYS[u["day"]]["frame"]
    C_ = g["close"].to_numpy()
    O_ = g["open"].to_numpy()
    net_sp = u["sdir"] * (float(C_[u["s"]]) - float(O_[u["i"]]))
    rng_sp = u["hi"] - u["lo"]
    assert rng_sp > 0
    ratio = net_sp / rng_sp
    assert abs(ratio) <= 1 + EPS, f"A1 |rasio|>1+eps: {ratio} (event {n}) → STOP"
    wick = rng_sp - abs(net_sp)
    if wick < 0:
        assert wick > -1e-6, f"wick negatif melebihi eps: {wick} → STOP"
        wick = 0.0
        clamp_ctr += 1
    UQ3[n] = {"ratio": float(ratio), "net_pip": float(net_sp / PIP),
              "range_pip": float(rng_sp / PIP),
              "wick_pip": float(wick / PIP), "wick_atr": float(wick / u["atr_s"])}
for key in ("agg", 0, 1, 2, 3):
    idx = [n for n in range(len(UNIQ)) if key == "agg" or UNIQ[n]["band"] == key]
    if len(idx) < POWER_MIN_N:
        Q3[key] = {"n": len(idx), "status": "point-only (n<30) — tidak dipakai"}
        print(f"Q3 {key}: n={len(idx)} → drop+label")
        continue
    rk = np.array([UQ3[n]["ratio"] for n in idx])
    wk = np.array([UQ3[n]["wick_pip"] for n in idx])
    wa = np.array([UQ3[n]["wick_atr"] for n in idx])
    dk = np.array([DAYCODE[UNIQ[n]["day"]] for n in idx])
    rlo, rhi = _boot_ci(rk, dk, np.median)
    wlo, whi = _boot_ci(wk, dk, np.median)
    Q3[key] = {"n": len(idx),
               "ratio_med": float(np.median(rk)),
               "ratio_iqr": [float(np.percentile(rk, 25)), float(np.percentile(rk, 75))],
               "ratio_ci95": [rlo, rhi],
               "wick_pip_med": float(np.median(wk)),
               "wick_pip_iqr": [float(np.percentile(wk, 25)), float(np.percentile(wk, 75))],
               "wick_pip_ci95": [wlo, whi],
               "wick_atr_med": float(np.median(wa)), "status": "ok"}
print("Q1 (bar-ke reversal, event terbalas saja):",
      {k: (f"n_rev={v['n']}/n_band={v['n_band']}", v.get("median"), v.get("ci95"))
       if v.get("status") == "ok" else v["status"] for k, v in Q1.items()})
print("Q3 (spike-level, semua unik):",
      {k: (f"n={v['n']}", round(v.get("ratio_med"), 4),
           round(v.get("wick_pip_med"), 2), v.get("wick_pip_ci95"))
       if v.get("status") == "ok" else v["status"] for k, v in Q3.items()})
print(f"clamp wick negatif-noise: {clamp_ctr}")
print("SEL 4 SELESAI")
'''
)

md(
    """## Sel 5 — Lapis-2: trade implisit fade

Entry = close(s+1) (selalu ada — room terjamin). Arah = −sdir, TP = level,
SL = hi+0.5ATR (fade short) / lo−0.5ATR (fade long). Prefilter
|entry−TP|−0.95 < 2.85 → degenerate (drop+label, dihitung). First-passage
K=16 tie-SL-dulu (counter) atas 16 bar PASCA-entry (s+2..s+17 — warisan
verbatim EDA-06 `confirm+1..confirm+K`; bar entry s+1 dikecualikan agar tak
ada sentuh-di-bar-entry = anti-lookahead intrabar). Syarat ruang lapis-2 =
s+17 se-hari — diuji SEBELUM prefilter (satu bar lebih jauh dari room-16 L1); tanpanya → drop+label
`no-room-l2` khusus lapis-2 (L1/primer tak berubah). Timeout → MTM
close(s+17). Mean + CI95 cluster @0.95
agregat + per band; stres @1.90 (prefilter dihitung-ulang pada biaya stres —
himpunan traded boleh menyusut) tanpa daya bunuh. Label win/loss/timeout =
MEKANIS (sentuh-dulu TP/SL, bukan klaim profit): net bertanda = P&L jujur
maka 'win' ber-net-negatif MUNGKIN — artinya entry close(s+1) sudah lewat
level (setup inversion: target sudah di belakang entry); dekomposisinya
dilaporkan deskriptif di bawah, BUKAN aturan drop baru (filter entry =
wilayah EDA-08/09, creep-scope di ronde ini).
"""
)

code(
    '''"""Sel 5 — lapis-2 trade machine (§6 verbatim)."""
L2 = {}
sl_ties = 0
deg_n = 0
noroom_n = 0
for n in AN:
    u = UNIQ[n]
    g = DAYS[u["day"]]["frame"]
    H, L, C = (g["high"].to_numpy(), g["low"].to_numpy(), g["close"].to_numpy())
    s, sdir, hi, lo, atr_s = u["s"], u["sdir"], u["hi"], u["lo"], u["atr_s"]
    entry = float(C[s + 1])
    rd = -sdir
    tp = (hi + lo) / 2.0
    sl = hi + 0.5 * atr_s if rd == -1 else lo - 0.5 * atr_s
    nn = len(g)
    if s + 17 >= nn:
        noroom_n += 1
        L2[n] = {"label": "no-room-l2", "edge": float(abs(entry - tp) / PIP - COST)}
        continue
    if abs(entry - tp) / PIP - COST < PREFILTER_NET:
        deg_n += 1
        L2[n] = {"label": "degenerate", "edge": float(abs(entry - tp) / PIP - COST)}
        continue
    win = loss = None
    for bb in range(s + 2, s + 18):
        hit_tp = (L[bb] <= tp) if rd == -1 else (H[bb] >= tp)
        hit_sl = (H[bb] >= sl) if rd == -1 else (L[bb] <= sl)
        if hit_tp and hit_sl:
            sl_ties += 1
            loss = bb
            break
        if hit_tp:
            win = bb
            break
        if hit_sl:
            loss = bb
            break
    if win is not None:
        net = (tp - entry) * rd / PIP - COST
        L2[n] = {"label": "win", "net": float(net),
                 "edge": float(abs(entry - tp) / PIP - COST)}
    elif loss is not None:
        net = (sl - entry) * rd / PIP - COST
        L2[n] = {"label": "loss", "net": float(net),
                 "edge": float(abs(entry - tp) / PIP - COST)}
    else:
        net = (float(C[s + 17]) - entry) * rd / PIP - COST
        L2[n] = {"label": "timeout", "net": float(net),
                 "edge": float(abs(entry - tp) / PIP - COST)}
print(f"lapis-2: degenerate(prefilter)={deg_n} no-room-l2={noroom_n} tie-SL-dulu={sl_ties}")
TR = [n for n in AN if "net" in L2[n]]
TR_STRESS = [n for n in TR if L2[n]["edge"] + COST - COST_STRESS >= PREFILTER_NET]
print(f"traded@0.95={len(TR)} traded@1.90={len(TR_STRESS)} "
      f"(degenerate-stres={len(TR) - len(TR_STRESS)})")
print(f"traded={len(TR)} "
      f"(win={sum(1 for n in TR if L2[n]['label'] == 'win')} "
      f"loss={sum(1 for n in TR if L2[n]['label'] == 'loss')} "
      f"timeout={sum(1 for n in TR if L2[n]['label'] == 'timeout')})")
_inv_w = [n for n in TR if L2[n]["label"] == "win" and L2[n]["net"] < 0]
_inv_l = [n for n in TR if L2[n]["label"] == "loss" and L2[n]["net"] > 0]
print(f"dekomposisi inversion (deskriptif, bukan drop): TP-dulu-net-negatif={len(_inv_w)} "
      f"SL-dulu-net-positif={len(_inv_l)} dari {len(TR)} traded")
for b in range(4):
    _tb = [n for n in TR if UNIQ[n]["band"] == b]
    _ib = [n for n in _tb if (L2[n]["label"] == "win" and L2[n]["net"] < 0)
           or (L2[n]["label"] == "loss" and L2[n]["net"] > 0)]
    print(f"  inversion band{b}: {len(_ib)}/{len(_tb)} traded")


def _l2_stats(idxs, cost):
    if len(idxs) < POWER_MIN_N:
        return {"n": len(idxs), "status": "point-only (n<30) — tidak dipakai"}
    vals, dids = [], []
    for n in idxs:
        u = UNIQ[n]
        g = DAYS[u["day"]]["frame"]
        H, L, C = (g["high"].to_numpy(), g["low"].to_numpy(), g["close"].to_numpy())
        s, sdir, hi, lo, atr_s = u["s"], u["sdir"], u["hi"], u["lo"], u["atr_s"]
        entry = float(C[s + 1])
        rd = -sdir
        tp = (hi + lo) / 2.0
        sl = hi + 0.5 * atr_s if rd == -1 else lo - 0.5 * atr_s
        lab = L2[n]["label"]
        px = tp if lab == "win" else (sl if lab == "loss" else float(C[s + 17]))
        vals.append((px - entry) * rd / PIP - cost)
        dids.append(DAYCODE[u["day"]])
    vals = np.array(vals)
    lo, hi = _boot_ci(vals, np.array(dids), np.mean)
    return {"n": len(vals), "mean": float(np.mean(vals)), "ci95": [lo, hi], "status": "ok"}


def _has_room17(n):
    u = UNIQ[n]
    return u["s"] + 17 < len(DAYS[u["day"]]["frame"])


AN17 = [n for n in AN if _has_room17(n)]
assert noroom_n == len(AN) - len(AN17), "rekonsiliasi no-room-l2 gagal → STOP"
print(f"l2-room17: eligible={len(AN17)} (pool null lapis-2 = pool ini)")


L2R = {"agg": _l2_stats(TR, COST)}
L2S = {"agg": _l2_stats(TR_STRESS, COST_STRESS)}
for b in range(4):
    L2R[b] = _l2_stats([n for n in TR if UNIQ[n]["band"] == b], COST)
    L2S[b] = _l2_stats([n for n in TR_STRESS if UNIQ[n]["band"] == b], COST_STRESS)
print("L2 @0.95:",
      {k: (round(v["mean"], 3), [round(x, 3) for x in v["ci95"]])
       if v["status"] == "ok" else v["status"] for k, v in L2R.items()})
print("L2 @1.90 (stres, tanpa daya bunuh):",
      {k: (round(v["mean"], 3), [round(x, 3) for x in v["ci95"]])
       if v["status"] == "ok" else v["status"] for k, v in L2S.items()})
print("SEL 5 SELESAI")
'''
)

md(
    """## Sel 6 — Primer + F3 + null F6 + FDR

Rate reversal/continuation/timeout agregat + per band dengan CI95 cluster
(day-bootstrap) dan CI naive Wilson (F3: keduanya dilaporkan + arah
perbedaan). Null F6 = permutasi jalur-16-bar: tiap spike asal dipasangi
jendela donor acak (ber-ruang-penuh), entry null = close pertama jendela
donor, TP/SL/prefilter dari spike asal; B=10000. Jalur donor lapis-1 =
16 bar (s+1..s+16, cermin jendela outcome); donor lapis-2 = 17 bar
(s+1..s+17: close pertama = entry + 16 bar passage, cermin jendela trade
pasca-entry), pool donor lapis-2 = event beruang-17. FDR-BH q=0.10 atas keluarga
eksploratori (strata sesi×kelas×jambin + cross-tab exhaustion + split tahun).
"""
)

code(
    '''"""Sel 6 — primer, F3, null-machine F6, FDR-BH."""
from math import sqrt as _sqrt


def _wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * _sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - m) / d, (c + m) / d


PRIMER = {}
for key in ("agg", 0, 1, 2, 3):
    idx = [n for n in AN if key == "agg" or UNIQ[n]["band"] == key]
    n_all = len(idx)
    rows = {}
    for oc in ("reversal", "continuation", "timeout"):
        k = sum(1 for n in idx if OUT[n]["outcome"] == oc)
        vals = np.array([1.0 if OUT[n]["outcome"] == oc else 0.0 for n in idx])
        dids = np.array([DAYCODE[UNIQ[n]["day"]] for n in idx])
        lo, hi = _boot_ci(vals, dids, np.mean)
        rows[oc] = {"k": k, "rate": k / n_all, "ci_cluster": [lo, hi]}
    k = rows["reversal"]["k"]
    wlo, whi = _wilson(k, n_all)
    rows["reversal"]["ci_naive"] = [wlo, whi]
    PRIMER[key] = {"n": n_all, **rows}
for key, P in PRIMER.items():
    r = P["reversal"]
    wider = "cluster-lebih-lebar" if (r["ci_cluster"][1] - r["ci_cluster"][0]) >= (
        r["ci_naive"][1] - r["ci_naive"][0]) else "naive-lebih-lebar"
    print(f"F3 primer {key}: n={P['n']} rev={r['rate']:.4f} "
          f"CIcl={[round(x, 4) for x in r['ci_cluster']]} "
          f"CInaive={[round(x, 4) for x in r['ci_naive']]} ({wider}) "
          f"cont={P['continuation']['rate']:.4f} timeout={P['timeout']['rate']:.4f}")

S = len(AN)
apos = {n: j for j, n in enumerate(AN)}
sdir_a = np.array([UNIQ[n]["sdir"] for n in AN])
level_a = np.array([(UNIQ[n]["hi"] + UNIQ[n]["lo"]) / 2.0 for n in AN])
extr_a = np.array([UNIQ[n]["hi"] if UNIQ[n]["sdir"] == 1 else UNIQ[n]["lo"] for n in AN])
atr_a = np.array([UNIQ[n]["atr_s"] for n in AN])
band_a = np.array([UNIQ[n]["band"] for n in AN])
exh_a = np.array([1 if UNIQ[n]["has_exh"] else 0 for n in AN])
year_a = np.array([1 if str(UNIQ[n]["day"])[:4] == "2024" else 0 for n in AN])
strat_key = [(UNIQ[n]["sess"], UNIQ[n]["cls"], UNIQ[n]["hbin"]) for n in AN]
from collections import Counter as _C
_sc = _C(strat_key)
strat_a = np.array([k if _sc[k] >= POWER_MIN_N else None for k in strat_key], dtype=object)
STRATA = sorted({k for k in strat_a if k is not None})
print(f"donor pool S={S}; strata teruji={len(STRATA)} "
      f"(drop+label strata n<30: {_sc and sum(1 for k, c in _sc.items() if c < POWER_MIN_N)})")
H16 = np.zeros((S, WIN))
L16 = np.zeros((S, WIN))
C16 = np.zeros((S, WIN))
for j, n in enumerate(AN):
    u = UNIQ[n]
    g = DAYS[u["day"]]["frame"]
    s = u["s"]
    H16[j] = g["high"].to_numpy()[s + 1 : s + 17]
    L16[j] = g["low"].to_numpy()[s + 1 : s + 17]
    C16[j] = g["close"].to_numpy()[s + 1 : s + 17]
S17 = len(AN17)
sdir_a17 = np.array([UNIQ[n]["sdir"] for n in AN17])
level_a17 = np.array([(UNIQ[n]["hi"] + UNIQ[n]["lo"]) / 2.0 for n in AN17])
extr_a17 = np.array([UNIQ[n]["hi"] if UNIQ[n]["sdir"] == 1 else UNIQ[n]["lo"] for n in AN17])
atr_a17 = np.array([UNIQ[n]["atr_s"] for n in AN17])
band_a17 = np.array([UNIQ[n]["band"] for n in AN17])
H17 = np.zeros((S17, WIN + 1))
L17 = np.zeros((S17, WIN + 1))
C17 = np.zeros((S17, WIN + 1))
for j, n in enumerate(AN17):
    u = UNIQ[n]
    g = DAYS[u["day"]]["frame"]
    s = u["s"]
    H17[j] = g["high"].to_numpy()[s + 1 : s + 18]
    L17[j] = g["low"].to_numpy()[s + 1 : s + 18]
    C17[j] = g["close"].to_numpy()[s + 1 : s + 18]
print(f"donor lapis-2: S17={S17} (jalur 17-bar s+1..s+17)")


def _first_idx(mask):
    any_ = mask.any(axis=1)
    return np.where(any_, mask.argmax(axis=1), WIN)


def _null_iter(di):
    Hd, Ld, Cd = H16[di], L16[di], C16[di]
    rvt = _first_idx((Cd - level_a[:, None]) * sdir_a[:, None] < 0)
    ctt = _first_idx((Cd - extr_a[:, None]) * sdir_a[:, None] > atr_a[:, None])
    rev = (rvt < WIN) & (rvt < ctt)
    cont = (ctt < WIN) & (ctt <= rvt)
    return rev, cont


def _null_l2(di):
    Hd, Ld, Cd = H17[di], L17[di], C17[di]
    entry = Cd[:, 0]
    rd = -sdir_a17
    tp = level_a17
    sl = np.where(rd == -1, extr_a17 + 0.5 * atr_a17, extr_a17 - 0.5 * atr_a17)
    tp_hit = np.where(rd[:, None] == -1, Ld[:, 1:] <= tp[:, None], Hd[:, 1:] >= tp[:, None])
    sl_hit = np.where(rd[:, None] == -1, Hd[:, 1:] >= sl[:, None], Ld[:, 1:] <= sl[:, None])
    tpf, slf = _first_idx(tp_hit), _first_idx(sl_hit)
    win = (tpf < WIN) & (tpf < slf)
    loss = (slf < WIN) & (slf <= tpf)
    px = np.where(win, tp, np.where(loss, sl, Cd[:, -1]))
    net = (px - entry) * rd / PIP - COST
    edge = np.abs(entry - tp) / PIP - COST
    traded = edge >= PREFILTER_NET
    return net, traded


rng_null = np.random.default_rng(SEED_NULL)
null_rev_agg = np.empty(N_NULL)
null_rev_band = np.empty((4, N_NULL))
null_rev_strat = {k: np.empty(N_NULL) for k in STRATA}
null_rev_exh = np.empty((2, N_NULL))
null_rev_year = np.empty((2, N_NULL))
null_l2_agg = np.empty(N_NULL)
null_l2_band = np.empty((4, N_NULL))
obs_rev = np.array([OUT[n]["outcome"] == "reversal" for n in AN])
for p in range(N_NULL):
    di = rng_null.integers(0, S, S)
    rev, cont = _null_iter(di)
    null_rev_agg[p] = rev.mean()
    for b in range(4):
        m = band_a == b
        null_rev_band[b, p] = rev[m].mean()
    for k in STRATA:
        m = np.array([s == k for s in strat_a])
        null_rev_strat[k][p] = rev[m].mean()
    for e in (0, 1):
        null_rev_exh[e, p] = rev[exh_a == e].mean()
        null_rev_year[e, p] = rev[year_a == e].mean()
    di17 = rng_null.integers(0, S17, S17)
    net17, traded17 = _null_l2(di17)
    null_l2_agg[p] = net17[traded17].mean() if traded17.any() else np.nan
    for b in range(4):
        tm = traded17 & (band_a17 == b)
        null_l2_band[b, p] = net17[tm].mean() if tm.any() else np.nan
print(f"null selesai: B={N_NULL} seed={SEED_NULL} "
      f"rev_agg null-mean={null_rev_agg.mean():.4f}")


def _p_upper(null, obs):
    return float((1 + (null >= obs).sum()) / (len(null) + 1))


obs_agg = obs_rev.mean()
P_FAM = {}
for k in STRATA:
    m = np.array([s == k for s in strat_a])
    P_FAM[("strat",) + tuple(k)] = _p_upper(null_rev_strat[k], obs_rev[m].mean())
for e in (0, 1):
    P_FAM[("exh", e)] = _p_upper(null_rev_exh[e], obs_rev[exh_a == e].mean())
    P_FAM[("year", e)] = _p_upper(null_rev_year[e], obs_rev[year_a == e].mean())


def _bh(pvals, q=FDR_Q):
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    thr = 0.0
    for rank, (_, p) in enumerate(items, 1):
        if p <= rank / m * q:
            thr = p
    return {k for k, p in pvals.items() if p <= thr}, thr


FDR_PASS, fdr_thr = _bh(P_FAM)
print(f"FDR-BH q={FDR_Q}: keluarga={len(P_FAM)} lolos={len(FDR_PASS)} ambang={fdr_thr:.6f}")
for k in sorted(P_FAM, key=lambda k: P_FAM[k])[:10]:
    print(f"  p={P_FAM[k]:.4f} {'LOLOS' if k in FDR_PASS else 'gugur'} {k}")
NULLP = {"agg_rev": _p_upper(null_rev_agg, obs_agg)}
for b in range(4):
    m = band_a == b
    NULLP[f"band{b}_rev"] = _p_upper(null_rev_band[b], obs_rev[m].mean())
obs_l2 = np.array([L2[n]["net"] for n in TR])
NULLP["l2_agg"] = _p_upper(null_l2_agg[~np.isnan(null_l2_agg)], obs_l2.mean())
for b in range(4):
    idx = [n for n in TR if UNIQ[n]["band"] == b]
    col = null_l2_band[b][~np.isnan(null_l2_band[b])]
    NULLP[f"l2_band{b}"] = _p_upper(col, np.mean([L2[n]["net"] for n in idx])) if idx else np.nan
print("p nominal (di luar FDR):",
      {k: round(v, 4) for k, v in NULLP.items()})
print("SEL 6 SELESAI")
'''
)

md(
    """## Sel 7 — Eksploratori + robustness + kurva

Strata (rate + CI + p-null + flag FDR), cross-tab exhaustion, split tahun
(rate + distribusi jarak pip + ×ATR, agregat + per tahun), robustness
(tercil magnitudo, definisi reversal B/C §3 — deskriptif + CI, tanpa p),
sensitivitas first-of-day (3 rate, searah/divergen), Q4 stratifikasi +
SMD (tanpa uji), kurva magnitudo-vs-rate + PNG.
"""
)

code(
    '''"""Sel 7 — eksploratori, robustness, kurva magnitudo-vs-rate."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

print("== strata ==")
for k in STRATA:
    m = np.array([s == k for s in strat_a])
    idx = [AN[j] for j in np.where(m)[0]]
    vals = np.array([1.0 if OUT[n]["outcome"] == "reversal" else 0.0 for n in idx])
    dids = np.array([DAYCODE[UNIQ[n]["day"]] for n in idx])
    lo, hi = _boot_ci(vals, dids, np.mean)
    pk = ("strat",) + tuple(k)
    print(f"  {k} n={len(idx)} rev={vals.mean():.4f} CI=[{lo:.4f},{hi:.4f}] "
          f"p={P_FAM[pk]:.4f} {'FDR-LOLOS' if pk in FDR_PASS else ''}")
print("== exhaustion cross-tab ==")
for e, lab in ((1, "exh"), (0, "tanpa-exh")):
    idx = [n for n in AN if (UNIQ[n]["has_exh"]) == bool(e)]
    vals = np.array([1.0 if OUT[n]["outcome"] == "reversal" else 0.0 for n in idx])
    dids = np.array([DAYCODE[UNIQ[n]["day"]] for n in idx])
    lo, hi = _boot_ci(vals, dids, np.mean)
    pk = ("exh", e)
    print(f"  {lab} n={len(idx)} rev={vals.mean():.4f} CI=[{lo:.4f},{hi:.4f}] "
          f"p={P_FAM[pk]:.4f} {'FDR-LOLOS' if pk in FDR_PASS else ''}")
print("== split tahun (rate + distribusi jarak) ==")
for lab, idx in (("AGREGAT", AN),
                 ("2023H2", [n for n in AN if str(UNIQ[n]["day"])[:4] != "2024"]),
                 ("2024", [n for n in AN if str(UNIQ[n]["day"])[:4] == "2024"])):
    vals = np.array([1.0 if OUT[n]["outcome"] == "reversal" else 0.0 for n in idx])
    dids = np.array([DAYCODE[UNIQ[n]["day"]] for n in idx])
    lo, hi = _boot_ci(vals, dids, np.mean)
    dd = np.array([abs(UNIQ[n]["dist_open"]) for n in idx])
    da = np.array([abs(UNIQ[n]["dist_open"]) * PIP / UNIQ[n]["atr_s"] for n in idx])
    tag = ""
    if lab != "AGREGAT":
        e = 1 if lab == "2024" else 0
        pk = ("year", e)
        tag = f"p={P_FAM[pk]:.4f} {'FDR-LOLOS' if pk in FDR_PASS else ''} | "
    print(f"  {lab} n={len(idx)} rev={vals.mean():.4f} CI=[{lo:.4f},{hi:.4f}] {tag}"
          f"|jarak| pip med={np.median(dd):.1f} p25/p75={np.percentile(dd, 25):.1f}/"
          f"{np.percentile(dd, 75):.1f} p95={np.percentile(dd, 95):.1f} | "
          f"xATR med={np.median(da):.2f} p25/p75={np.percentile(da, 25):.2f}/"
          f"{np.percentile(da, 75):.2f} p95={np.percentile(da, 95):.2f}")
mags = np.array([u["mag"] for u in [UNIQ[n] for n in AN]])
t1, t2 = np.percentile(mags, 100 / 3), np.percentile(mags, 200 / 3)
print(f"== tercil magnitudo (batas {t1:.3f}/{t2:.3f}) ==")
for ti, (lo_, hi_) in enumerate([(0, t1), (t1, t2), (t2, np.inf)]):
    idx = [n for n in AN if lo_ <= UNIQ[n]["mag"] < hi_]
    vals = np.array([1.0 if OUT[n]["outcome"] == "reversal" else 0.0 for n in idx])
    dids = np.array([DAYCODE[UNIQ[n]["day"]] for n in idx])
    lo, hi = _boot_ci(vals, dids, np.mean)
    print(f"  T{ti + 1} n={len(idx)} rev={vals.mean():.4f} CI=[{lo:.4f},{hi:.4f}]")
print("== robustness definisi reversal (§3: B/C, deskriptif, tanpa p) ==")


def _revB(u):
    g = DAYS[u["day"]]["frame"]
    H, L, C = (g["high"].to_numpy(), g["low"].to_numpy(), g["close"].to_numpy())
    pre = float(C[u["i"] - 1])
    for bb in range(u["s"] + 1, u["s"] + 17):
        if (L[bb] <= pre) if u["sdir"] == 1 else (H[bb] >= pre):
            return True
    return False


def _revC(u):
    g = DAYS[u["day"]]["frame"]
    H, L = (g["high"].to_numpy(), g["low"].to_numpy())
    for bb in range(u["s"] + 1, u["s"] + 17):
        if (L[bb] <= u["hi"] - u["atr_s"]) if u["sdir"] == 1 else (
            H[bb] >= u["lo"] + u["atr_s"]):
            return True
    return False


for name, fn in (("def-B", _revB), ("def-C", _revC)):
    for key in ("agg", 0, 1, 2, 3):
        idx = [n for n in AN if key == "agg" or UNIQ[n]["band"] == key]
        if len(idx) < POWER_MIN_N:
            print(f"  {name}/{key}: n={len(idx)} → drop+label")
            continue
        vals = np.array([1.0 if fn(UNIQ[n]) else 0.0 for n in idx])
        dids = np.array([DAYCODE[UNIQ[n]["day"]] for n in idx])
        lo, hi = _boot_ci(vals, dids, np.mean)
        print(f"  {name}/{key} n={len(idx)} rev={vals.mean():.4f} CI=[{lo:.4f},{hi:.4f}]")
fod = [n for n in AN if UNIQ[n]["first_of_day"]]
print(f"== sensitivitas first-of-day (n={len(fod)}) vs primer agregat ==")
for oc in ("reversal", "continuation", "timeout"):
    _fv = np.array([1.0 if OUT[n]["outcome"] == oc else 0.0 for n in fod])
    _fd = np.array([DAYCODE[UNIQ[n]["day"]] for n in fod])
    _flo, _fhi = _boot_ci(_fv, _fd, np.mean)
    _plo, _phi = PRIMER["agg"][oc]["ci_cluster"]
    _overlap = not (_fhi < _plo or _phi < _flo)
    print(f"  {oc}: fod={_fv.mean():.4f} CI=[{_flo:.4f},{_fhi:.4f}] vs "
          f"agg={PRIMER['agg'][oc]['rate']:.4f} CI=[{_plo:.4f},{_phi:.4f}] → "
          f"{'SEARAH (CI tumpang-tindih)' if _overlap else 'DIVERGEN (waspada bias)'}")
print("== Q4 stratifikasi pra-karakteristik per outcome + SMD rev-vs-cont ==")
FEATS = [("mag_cont", lambda u: u["mag"]), ("dist_open", lambda u: u["dist_open"]),
         ("pre1", lambda u: u["pre_size"][0]),
         ("micro_box", lambda u: u["micro_box"]),
         ("micro_dist", lambda u: u["micro_dist"]),
         ("pctl500", lambda u: u["pctl500"]),
         ("rsi_i", lambda u: u["rsi_i"]), ("rsi_s", lambda u: u["rsi_s"]),
         ("body", lambda u: u["body"]),
         ("ctx", lambda u: (u["ctx"] if u["ctx"] is not None else np.nan))]
for fname, fn in FEATS:
    grp = {}
    for oc in ("reversal", "continuation", "timeout"):
        vv = np.array([fn(UNIQ[n]) for n in AN if OUT[n]["outcome"] == oc], dtype=float)
        vv = vv[~np.isnan(vv)]
        grp[oc] = vv
    r, c = grp["reversal"], grp["continuation"]
    smd = ((np.mean(r) - np.mean(c)) / np.sqrt((np.var(r) + np.var(c)) / 2))
    if len(r) < POWER_MIN_N or len(c) < POWER_MIN_N:
        print(f"  {fname}: rev-n={len(r)} cont-n={len(c)} → SMD drop+label")
        continue
    print(f"  {fname}: rev med={np.median(r):.3f} [{np.percentile(r, 25):.3f},"
          f"{np.percentile(r, 75):.3f}] cont med={np.median(c):.3f} "
          f"[{np.percentile(c, 25):.3f},{np.percentile(c, 75):.3f}] "
          f"timeout med={np.median(grp['timeout']):.3f} SMD={smd:.3f}")

xs = [1.75, 2.25, 2.75, 3.5]
ys = [PRIMER[b]["reversal"]["rate"] for b in range(4)]
yl = [PRIMER[b]["reversal"]["rate"] - PRIMER[b]["reversal"]["ci_cluster"][0] for b in range(4)]
yu = [PRIMER[b]["reversal"]["ci_cluster"][1] - PRIMER[b]["reversal"]["rate"] for b in range(4)]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.errorbar(xs, ys, yerr=[yl, yu], fmt="o-", capsize=4, label="per band (CI95 cluster)")
ax.axhline(PRIMER["agg"]["reversal"]["rate"], ls="--", label="agregat")
ax.axhline(0.5, color="red", ls=":", label="koin 50%")
ax.set_xlabel("magnitudo (×ATR; 3.5 = band 3.0+)")
ax.set_ylabel("reversal rate")
ax.set_title("EDA-07: magnitudo vs reversal-rate (Nunik=1632)")
ax.legend()
FIG = PROJECT_ROOT / "reports/eda/2026-10-15-eda07/fig-mag-rate.png"
FIG.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(FIG, dpi=120)
plt.close(fig)
print(f"kurva tersimpan: {FIG.relative_to(PROJECT_ROOT)}")
print("SEL 7 SELESAI")
'''
)

md(
    """## Sel 8 — Parquet pra-vonis + handoff + vonis

**Urutan terkunci:** blok parquet (tulis + assertion) dieksekusi DULU,
vonis kill dua lapis SESUDAHNYA dalam sel yang sama. Kolom wajib
(mag_cont kontinu — anti-cliff). A2 diverifikasi ulang dari parquet.
Vonis: L1 = bawah-CI95 agregat vs 50%; L2 = mean ≤ 0 atau CI lewati 0 →
GUGUR. Klausul scoping + live-applicability + caveat-379 dicetak.
"""
)

code(
    '''"""Sel 8 — tulis parquet DULU, lalu vonis (urutan terkunci)."""
rows = []
for n, u in enumerate(UNIQ):
    o = OUT[n]
    drop = bool(o["drop"])
    r = {"day": u["day"], "i": u["i"], "s": u["s"], "sdir": u["sdir"],
         "hi": u["hi"], "lo": u["lo"], "atr_s": u["atr_s"],
         "mag_cont": u["mag"], "band": u["band"],
         "has_exhaustion": bool(u["has_exh"]), "r_bar": u["r_bar"],
         "or_top": u["or_top"], "or_bottom": u["or_bottom"],
         "micro_box": u["micro_box"], "micro_dist": u["micro_dist"],
         "dist_open": u["dist_open"], "pctl500": u["pctl500"], "body": u["body"],
         "rsi_i": u["rsi_i"], "rsi_s": u["rsi_s"],
         "utc_hour": u["utc_hour"], "sess": u["sess"], "hbin": u["hbin"],
         "cls": u["cls"], "ctx": u["ctx"], "first_of_day": bool(u["first_of_day"]),
         "drop_flag": int(drop), "drop_reason": o.get("reason", "none") if drop else "none",
         "outcome": "drop" if drop else o["outcome"],
         "bar_ke": -1 if drop else o["bar_ke"],
         "adv_exc_atr": np.nan if drop else o["adv"],
         "follow_thru_atr": np.nan if drop else o["fth"],
         "q3_net_pip": UQ3[n]["net_pip"], "q3_range_pip": UQ3[n]["range_pip"],
         "q3_wick_pip": UQ3[n]["wick_pip"], "q3_wick_atr": UQ3[n]["wick_atr"],
         "q3_ratio": UQ3[n]["ratio"]}
    for k in range(10):
        r[f"pre_size_{k + 1}"] = u["pre_size"][k]
        r[f"pre_dir_{k + 1}"] = u["pre_dir"][k]
    lab = "drop" if drop else L2.get(n, {}).get("label", "drop")
    r["l2_label"] = lab
    r["l2_net_pip"] = float(L2[n]["net"]) if lab in ("win", "loss", "timeout") else np.nan
    rows.append(r)
EV = pd.DataFrame(rows)
PQ = PROJECT_ROOT / "data/processed/events/eda07_spike_events.parquet"
PQ.parent.mkdir(parents=True, exist_ok=True)
EV.to_parquet(PQ, index=False)
assert PQ.is_file()
for col in ("mag_cont", "band", "has_exhaustion", "r_bar", "first_of_day",
            "drop_flag", "drop_reason"):
    assert col in EV.columns, f"kolom wajib {col} hilang → STOP"
assert len(EV) == 1632, f"baris parquet {len(EV)} != 1632 → STOP"
assert str(EV["day"].max()) < "2025-01-01"
chk = EV[EV["drop_flag"] == 0]
for b in range(4):
    g = chk[chk["band"] == b]["outcome"]
    assert ((g == "reversal") | (g == "continuation") | (g == "timeout")).all()
    assert (g.value_counts().sum()) == len(g)
print(f"parquet: {PQ.relative_to(PROJECT_ROOT)} ({len(EV)} baris, {len(EV.columns)} kolom)")

assert DAILY_OPEN_HOURS == [22, 23] and COST == 0.95 and COST_STRESS == 1.90
assert (N_BOOT, N_NULL, SEED_BOOT, SEED_NULL) == (10_000, 10_000, 20261006, 20261007)
assert BAND_EDGES == [1.5, 2.0, 2.5, 3.0] and FDR_Q == 0.10
rev = PRIMER["agg"]["reversal"]
L1 = "GUGUR" if rev["ci_cluster"][0] < 0.50 else "LOLOS"
print(f"VONIS LAPIS-1 (rate vs koin): bawah-CI95={rev['ci_cluster'][0]:.4f} vs 0.50 → {L1}")
m = L2R["agg"]
if m.get("status") != "ok":
    L2V = "GUGUR (tak-teruji: traded<30 — fade tak tereksekusi pada kontrak ini)"
elif m["mean"] <= 0 or m["ci95"][0] <= 0:
    L2V = "GUGUR"
else:
    L2V = "LOLOS"
print(f"VONIS LAPIS-2 (trade implisit @0.95): "
      f"mean={m.get('mean')} CI95={m.get('ci95')} → {L2V}")
print("SCOPING: vonis hanya untuk pool spike mentah R + band/kontrak di atas; "
      "generalisasi di luar itu DILARANG tanpa ronde baru. GUGUR di sini HANYA "
      "mematikan hipotesis fade-standalone — status fitur spike di registry "
      "amunisi ANN diputus TERPISAH (pola univariat-mati bisa hidup kondisional "
      "dalam model multivariat); dilarang mengklaim 'spike tidak berguna untuk ANN'.")
_b4 = len([n for n in AN if UNIQ[n]["band"] == 3])
print(f"fallback band (§3 A-4): band-4 analyzed n={_b4} → "
      f"{'tak terpicu' if _b4 >= 30 else 'TERPICU — pool [2.5+) sekunder dipakai'}")
print(f"drop lapis-2 khusus (no-room-l2, butuh s+17 se-hari): n={noroom_n} — "
      f"subset validasi ANN berikutnya HANYA atas event beruang-17 (B-5).")
print("LIVE: entry close(s+1) + level/TP/SL replikabel live HANYA dengan end-detector "
      "(s diketahui ex-post) — sinyal bersifat lagged-causal; biaya live ≠ 0.95 flat.")
for rule in ("biaya-hanya-0.95", "larangan-cross-day", "prefilter-degenerate",
             "stratum<30-drop", "stres-tanpa-daya-bunuh",
             "passage-s+2-tanpa-entry-bar", "room17-lapis2"):
    print(f"live-applicability [{rule}]: berlaku verbatim bila kontrak sama; "
          f"ubah kontrak → uji ulang.")
print("CAVEAT-379: split sesi/jam memakai 384 hari bersih yang sama dengan agregat "
      "(resolusi tersanksi); 5 hari anomali 2024-10-28..11-01 sudah di luar R.")
print("F3: banding CI cluster-vs-naive tercetak di Sel 6; "
      "F5: tabulasi drop tercetak di Sel 4.")
print("HANDOFF: EDA-08/09 (entry test) HANYA bila L1+L2 LOLOS; bila salah satu GUGUR "
      "→ jalur fade-spike DITUTUP untuk R/kontrak ini.")
print("=== EDA-07 SELESAI: SEMUA ASSERTION PASS ===")
'''
)


def build() -> None:
    """Tulis notebook dan eksekusi top-to-bottom via nbconvert."""
    notebook = nbf.v4.new_notebook()
    notebook.cells = [
        nbf.v4.new_markdown_cell(source) if kind == "md" else nbf.v4.new_code_cell(source)
        for kind, source in CELLS
    ]
    notebook.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    }
    NB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        nbf.write(notebook, handle)
    print(f"notebook ditulis: {NB_PATH.relative_to(PROJECT_ROOT)} ({len(notebook.cells)} sel)")

    subprocess.run(
        [sys.executable, "-m", "ruff", "format", str(NB_PATH)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=1800",
            str(NB_PATH),
        ],
        cwd=PROJECT_ROOT,
    )
    _nb_bytes = NB_PATH.read_bytes().replace(b"\r\n", b"\n")
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(_nb_bytes.decode("utf-8"))

    print(f"nbconvert exit={result.returncode}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    build()
