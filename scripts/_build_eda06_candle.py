"""Generator + executor for notebooks/scalping/eda_06_candle_anatomy_regime.ipynb.

EDA-06 Candle-Anatomy Regime-Matched (Blueprint v9.3 FINAL + Amandemen-1):
pengujian terkontrol hipotesis "candlestick meaning" (spike + exhaustion /
momentum + posisi terhadap daily-open) dengan sel bersarang Sel 1 > Sel 2 >
Sel 3, cabang momentum 4a1t/4a1s (+sensitivitas), null placebo DUA track yang
regime-matched per sel, dan FDR-BH q=0.10 atas sel inti yang diuji.

Konvensi repo: generator nbformat di scripts/ -> notebook di
notebooks/scalping/, dieksekusi top-to-bottom via nbconvert (pola
scripts/_build_eda05.py). Reuse-First: waktu via src/data/broker_time,
anomaly windows via configs/data.yaml (load_config); dilarang modul baru
di src/ dan dilarang menulis ke configs/.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_06_candle_anatomy_regime.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA-06 — Candle-Anatomy Regime-Matched (v9.3 + Amandemen-1)

**Blueprint:** `thoughts/shared/designs/2026-10-15-eda06-blueprint-v93.md`
**Amandemen-1:** `thoughts/shared/designs/2026-10-15-eda06-amandemen-1.md`
(A1+A2+A3 diratifikasi, A4 diputus FS-01→V — amandemen menang bila konflik.)

Hipotesis yang diuji: *candlestick memiliki makna* — spike mingguan-ekstrem
yang berakhir exhaustion (atau berlanjut momentum) di dekat harga pembuka
harian memiliki edge arah yang terukur, BUKAN artefak pilihan ambang, BUKAN
artefak satu rezim hari, dan BUKAN noise yang lolos koreksi multipel.

## Aturan yang mengikat notebook ini
- **Reuse-First:** `wall_clock_series` dari `src/data/broker_time.py`;
  anomaly windows dari `configs/data.yaml` via `load_config` (bukti reuse
  di-assert di Sel 1). Dilarang modul baru di `src/`, nol imputasi.
- **Partisi HANYA R** (2023-07-01 s.d. 2024-12-31, plus assert
  `max(utc) < 2025-01-01`). Tahun 2026 / partisi P SEGEL — tidak dibaca.
- **Nol angka terkunci diubah** (Cek 5): 0.95, 2.85, RR 1.0, K=16, gate 30,
  open [22,23], seed 20261006/20261007, power 5 pip, placebo 1000×2 track,
  FDR core {1,2,3,4a1t,4a1s}, PSEUDO_N=3.
- **STOP discipline:** assertion crash = STOP + lapor, bukan skip. Gate Cek 4
  revisi: STOP hanya jika Sel 1 < 30; Sel 2/3 < 30 → drop+label; split
  momentum MOOT bila cabangnya < 30 → pool 4a1+4a2 (aturan di Sel 4).
- **Event parquet ditulis SEBELUM vonis** (Sel 5), kolom persis kontrak Sel 7.
- **Satu vonis per sel** (§5): LOLOS / GUGUR / UNDERPOWERED / "TIDAK TAHU".
"""
)

code(
    '''"""Sel 1 — setup, kontrak terkunci, load, partisi R, assertion Cek 1-3."""
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

# ---- Kontrak angka terkunci (Cek 5: amandemen menang bila konflik) ----
PIP = 0.01
COST_PIP = 0.95
MIN_NET_TP_PIP = 2.85
MIN_RR = 1.0
KILL_K = 16
GATE_MIN_N = 30
DAILY_OPEN_HOURS = [22, 23]  # A1 (amandemen; v9.3 lama [21,22] GUGUR)
R_START = pd.Timestamp("2023-07-01", tz="UTC")
R_END_EXCL = pd.Timestamp("2025-01-01", tz="UTC")
SEED_BOOT = 20261006
SEED_NULL = 20261007
N_BOOT = 10_000
N_NULL = 1000
FDR_Q = 0.10
FDR_CORE = ("1", "2", "3", "4a1t", "4a1s")
POWER_MIN_N = 30
POWER_MAX_CIWIDTH_PIP = 5.0
PSEUDO_N = 3
PCTL_MACRO = 25
PCTL_MICRO = 50

assert DAILY_OPEN_HOURS == [22, 23], "Cek 5: DAILY_OPEN_HOURS amandemen [22,23]"
assert set(FDR_CORE) == {"1", "2", "3", "4a1t", "4a1s"}, "Cek 5: FDR_CORE amandemen"


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
assert anom_cfg, "anomaly_windows tidak ditemukan di configs/data.yaml (reuse gagal)"
ANOMALY = [(pd.Timestamp(w["start"]).date(), pd.Timestamp(w["end"]).date()) for w in anom_cfg]
print("reuse OK: broker_time.wall_clock_series +", len(ANOMALY), "anomaly windows dari configs/data.yaml")

# ---- Load parquet M15/D1 2023-2024 (P/2026 TIDAK dibaca) ----
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
print(f"M15: {len(m15)} bar | D1: {len(d1)} bar")

# ---- Partisi R + buang hari anomali ----
anom_days: set = set()
for start, end in ANOMALY:
    anom_days.update(pd.date_range(start, end).date)
r = m15[(m15["time"] >= R_START) & (m15["time"] < R_END_EXCL)].copy()
assert r["time"].max() < R_END_EXCL, "Cek 3: max(utc) R melanggar <2025-01-01"
r = r[~r["broker_day"].isin(anom_days)].copy()
assert not r["broker_day"].isin(anom_days).any(), "Cek 3: hari anomali bocor ke R"
print(f"R: {len(r)} bar, max(utc)={r['time'].max()}")

# ---- Tabel hari: open vs [22,23], OR 4-bar ----
DAYS: dict = {}
drops = []
for day, g in r.groupby("broker_day"):
    g = g.sort_values("time").reset_index(drop=True)
    if g["time"].iloc[0].hour not in DAILY_OPEN_HOURS:
        drops.append(day)
        continue
    f4 = g.iloc[:4]
    DAYS[day] = {
        "frame": g,
        "open": float(g["open"].iloc[0]),
        "or_top": float(f4["high"].max()),
        "or_bottom": float(f4["low"].min()),
    }
open_abnormal_rate = len(drops) / (len(DAYS) + len(drops))
print(f"hari bersih={len(DAYS)} drop-open={len(drops)} rate={open_abnormal_rate:.3%}")
assert open_abnormal_rate <= 0.05, "Cek 3: open-abnormal > 5% → STOP"
assert len(DAYS) >= 300, "Cek 3: hari bersih jauh dari ekspektasi ~384"
assert min(len(v["frame"]) for v in DAYS.values()) >= 60, "hari terlalu pendek utk jendela K=16"
print("SEL 1 SELESAI: setup + kontrak + partisi R + tabel hari OK")
'''
)

md(
    """## Sel 2 — Daily Open & Indikator (ATR/RSI Wilder, ATR D1, konteks 5-hari)

ATR14 = Wilder-EMA(14) true-range, di-shift(1) (tanpa look-ahead — nilai yang
dipakai bar-$t$ hanya memakai informasi ≤ bar-$t-1$). RSI14 = Wilder-EMA(14).
Konteks hari = range 5-hari / ATR D1 terakhir (`ctx`), dihitung dari bar D1
sebelum hari-$t$ (tanpa look-ahead). Semua dihitung di atas deret PENUH lalu
dipakai di R (tepi warmup identik pre-flight).
"""
)

code(
    '''"""Sel 2 — indikator Wilder + konteks 5-hari per hari (tanpa look-ahead)."""
NSMOOTH = 14


def _wilder_ema(series: pd.Series, n: int = NSMOOTH) -> pd.Series:
    return series.ewm(alpha=1.0 / n, adjust=False).mean()


_prev = m15["close"].shift(1)
_tr = pd.concat(
    [m15["high"] - m15["low"], (m15["high"] - _prev).abs(), (m15["low"] - _prev).abs()],
    axis=1,
).max(axis=1)
m15["atr"] = _wilder_ema(_tr).shift(1)  # A-fidelity: ATR dipakai shift(1)
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


def day_ctx(day) -> float | None:
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

n_ctx = sum(1 for v in DAYS.values() if v["ctx"] is not None)
print(f"ctx tersedia {n_ctx}/{len(DAYS)} hari")
assert n_ctx / len(DAYS) > 0.95, "konteks 5-hari hilang >5% hari → STOP"
print("SEL 2 SELESAI: ATR/RSI Wilder + ctx 5-hari OK")
'''
)

md(
    """## Sel 3 — Fitur kontinu & anatomi spike (kandidat, belum ambang)

Deteksi spike DUA ambang (2.0× dan 1.5× ATR) dengan cooldown 16 bar dan
ekstensi ≤2 bar searah (aturan v9.3). Kandidat exhaustion = sentuh RSI
ekstrem dalam $s+1..s+6$ (first-touch). Fitur anatomi: body-ratio, rasio
wick atas/bawah (di Bar 1), persentil rolling range vs 500 bar lampau,
ukuran/arah 10 bar pra-trigger, jarak ke daily-open, rasio makro (ctx hari),
mikro box/dist dari 12 bar pra-spike. Sel 3 TIDAK menerapkan ambang di sini —
ambang P25/P50 dihitung di Sel 4 (dry-run di dalam notebook) dan DILAPORKAN.
"""
)

code(
    '''"""Sel 3 — scan spike, kandidat exhaustion, fitur anatomi (tanpa ambang)."""
SPIKE_SCAN = []  # (day, thresh, i, s, sdir, hi, lo, atr_s)
EXH_CAND = []  # kandidat exhaustion (thresh 2.0): dict
ROLL_N = 500


def scan_spikes(g: pd.DataFrame, thresh: float) -> list:
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
            i = s + 16  # cooldown: satu spike per 16 bar
        else:
            i += 1
    return out


def first_exhaustion(g: pd.DataFrame, s: int, sdir: int):
    rsi = g["rsi"].to_numpy()
    for k in range(s + 1, min(s + 7, len(g))):
        v = rsi[k]
        if not np.isfinite(v):
            continue
        if (sdir == 1 and v >= 70) or (sdir == -1 and v <= 30):
            return k
    return None


for day in sorted(DAYS):
    info = DAYS[day]
    g = info["frame"]
    H, L, C, O = (g["high"].to_numpy(), g["low"].to_numpy(),
                  g["close"].to_numpy(), g["open"].to_numpy())
    for thresh in (2.0, 1.5):
        for (i, s, sdir, hi, lo) in scan_spikes(g, thresh):
            atr_s = float(g["atr"].iloc[s])
            atr_i = float(g["atr"].iloc[i])  # ATR Bar-1: utk normalisasi mikro
            SPIKE_SCAN.append((day, thresh, i, s, sdir, hi, lo, atr_s))
            if thresh != 2.0:
                continue
            r = first_exhaustion(g, s, sdir)
            atr_r = (float(g["atr"].iloc[r]) if r is not None
                     and np.isfinite(float(g["atr"].iloc[r])) else atr_s)
            rng = H[i] - L[i]
            body = abs(C[i] - O[i]) / rng if rng > 0 else np.nan
            wup = (H[i] - max(C[i], O[i])) / rng if rng > 0 else np.nan
            wdn = (min(C[i], O[i]) - L[i]) / rng if rng > 0 else np.nan
            base = g.iloc[max(0, i - ROLL_N) : i]
            pctl = float((base["high"] - base["low"] < rng).mean()) if len(base) >= 50 else np.nan
            pre_size, pre_dir = [], []
            rr = r if r is not None else s
            for k in range(rr - 1, rr - 11, -1):
                if k < 0:
                    pre_size.append(np.nan)
                    pre_dir.append(0)
                else:
                    pre_size.append(float((H[k] - L[k]) / PIP))
                    pre_dir.append(int(np.sign(C[k] - O[k])))
            micro_box, micro_dist = np.nan, np.nan
            if i >= 12:
                pre12 = g.iloc[i - 12 : i]
                micro_box = float((pre12["high"].max() - pre12["low"].min()) / atr_i)
                micro_dist = float(max(
                    min(abs(c - info["or_top"]), abs(c - info["or_bottom"]))
                    for c in pre12["close"].to_numpy()) / atr_i)
            EXH_CAND.append({
                "day": day, "i": i, "s": s, "sdir": sdir, "hi": hi, "lo": lo,
                "atr_s": atr_s, "atr_i": atr_i, "atr_r": atr_r, "r": r, "body": body, "wup": wup, "wdn": wdn,
                "pctl": pctl, "pre_size": pre_size, "pre_dir": pre_dir,
                "micro_box": micro_box, "micro_dist": micro_dist,
                "dist_open": float((C[rr] - info["open"]) / PIP),
            })

n_exh = sum(1 for c in EXH_CAND if c["r"] is not None)
print(f"spike terdeteksi: {len(SPIKE_SCAN)} | kandidat exhaustion (r ada): {n_exh}")
assert n_exh > 0, "Cek 6: nol kandidat exhaustion → probe/placebo hampa → STOP"
print("SEL 3 SELESAI: kandidat + anatomi OK (ambang di Sel 4)")
'''
)

md(
    """## Sel 4 — Operasionalisasi: ambang dry-run, kelas hari, rakitan sel + gate

Ambang DITURUNKAN dari data (dry-run di dalam notebook), BUKAN improvisasi:
$T_{day}$ = P25 rasio makro atas basis Sel-1; $T_{box},T_{dist}$ = P50 mikro
atas jendela pra-spike yang sama. Basis dry-run = kandidat exhaustion yang
lolos waktu + prefilter (pra-konfirm) — definisi identik pratinjau pre-flight.
Kelas hari: B (sideways, ctx < $T_{day}$), A (trending naik), C (trending
turun; A vs C dari tanda return 5-hari — operasionalisasi minimal yang
didaftarkan di sini). T0 = Sel 1 (semua hari), T1 = Sel 2 (hari B),
Sel 3 = Sel 2 + mikro. Momentum: 4 cabang (ambang × mode-RSI) × 2 kelas hari;
bila EITHER cabang < 30 → split MOOT → pool 4a1+4a2 (aturan amandemen).
Gate revisi: STOP (RuntimeError) HANYA jika Sel 1 < 30.
"""
)

code(
    '''"""Sel 4 — ambang P25/P50 (DILAPORKAN), kelas hari, rakitan sel, gate."""
# ---- Basis dry-run: exhaustion + waktu(r+1<=32) + prefilter(net TP>=2.85) ----
basis = []
for c in EXH_CAND:
    if c["r"] is None or c["r"] + 1 > 32:
        continue
    info = DAYS[c["day"]]
    if abs(info["frame"]["close"].iloc[c["r"]] - info["open"]) / PIP <= MIN_NET_TP_PIP:
        continue
    basis.append(c)
ratios = np.array([DAYS[c["day"]]["ctx"] for c in basis
                   if DAYS[c["day"]]["ctx"] is not None])
boxes = np.array([c["micro_box"] for c in basis if np.isfinite(c["micro_box"])])
dists = np.array([c["micro_dist"] for c in basis if np.isfinite(c["micro_dist"])])
T_DAY = float(np.percentile(ratios, PCTL_MACRO))
T_BOX = float(np.percentile(boxes, PCTL_MICRO))
T_DIST = float(np.percentile(dists, PCTL_MICRO))
print(f"AMBANG DRY-RUN (otoritatif): T_day=P{PCTL_MACRO} makro = {T_DAY:.4f} "
      f"(n={len(ratios)}) | T_box=P{PCTL_MICRO} = {T_BOX:.4f} (n={len(boxes)}) | "
      f"T_dist=P{PCTL_MICRO} = {T_DIST:.4f} (n={len(dists)})")


def day_class(day) -> str:
    ctx = DAYS[day]["ctx"]
    if ctx is None or ctx < T_DAY:
        return "B"
    past = d1[d1["bday"] < day].tail(5)
    return "A" if float(past["close"].iloc[-1] - past["close"].iloc[0]) > 0 else "C"


for day in DAYS:
    DAYS[day]["cls"] = day_class(day)
from collections import Counter
print("kelas hari:", dict(Counter(v["cls"] for v in DAYS.values())))


def exh_confirm_side(c):
    """Prefilter sudah lolos (basis); terapkan konfirm + postfilter + side."""
    info = DAYS[c["day"]]
    g = info["frame"]
    if c["r"] + 1 >= len(g):
        return None
    conf = g.iloc[c["r"] + 1]
    sdir = c["sdir"]
    is_conf = ((sdir == 1 and conf["close"] < conf["open"])
               or (sdir == -1 and conf["close"] > conf["open"]))
    if not is_conf:
        return ("gugur-confirm", None)
    entry = float(conf["close"])
    tp = info["open"]
    atr_trig = c["atr_r"]  # SL memakai ATR bar-trigger r (terkini & sah)
    sl = (max(entry + atr_trig, c["hi"] + 0.5 * PIP) if sdir == 1
          else min(entry - atr_trig, c["lo"] - 0.5 * PIP))
    if abs(entry - tp) / PIP - COST_PIP < MIN_NET_TP_PIP:
        return ("gugur-postfilter", None)
    rd = -sdir
    if not ((rd == -1 and entry > info["open"]) or (rd == 1 and entry < info["open"])):
        return ("gugur-side", None)
    return ("lolos", (entry, tp, sl, rd))


# ---- Cek 2 notebook: SATU contoh gugur dgn alasan benar ----
for c in basis:
    res = exh_confirm_side(c)
    if res[0] != "lolos":
        print(f"Cek2: kandidat {c['day']} spike@{c['i']} → {res[0]} (alasan benar, bukan bug)")
        break

SEL = {"1": [], "2": [], "3": []}  # event pra-first-passage (dict + entry/tp/sl/rd)
for c in basis:
    status, vals = exh_confirm_side(c)
    if status != "lolos":
        continue
    entry, tp, sl, rd = vals
    ev = dict(c)
    ev.update(entry=entry, tp=tp, sl=sl, rd=rd)
    SEL["1"].append(ev)
    if DAYS[c["day"]]["cls"] == "B":
        SEL["2"].append(ev)
        if c["micro_box"] <= T_BOX and c["micro_dist"] <= T_DIST:
            SEL["3"].append(ev)
print(f"Sel 1={len(SEL['1'])} Sel 2={len(SEL['2'])} Sel 3={len(SEL['3'])}")
assert len(SEL["1"]) == 51, f"drift funnel vs pre-flight: Sel1={len(SEL['1'])} != 51"
if len(SEL["1"]) < GATE_MIN_N:
    raise RuntimeError(f"GATE Cek4: Sel 1 = {len(SEL['1'])} < {GATE_MIN_N} → STOP UNDERPOWERED")
TESTED = ["1"]
for sel in ("2", "3"):
    if len(SEL[sel]) >= GATE_MIN_N:
        TESTED.append(sel)
    else:
        print(f"Sel {sel} = {len(SEL[sel])} < {GATE_MIN_N} → drop+label (bukan STOP)")

# ---- Momentum 4 cabang × 2 kelas hari ----
MOM = {}
for arm, thresh in (("a", 2.0), ("b", 1.5)):
    for mode in ("1", "2"):
        for dcls, dname in (("B", "t"), (("A", "C"), "s")):
            MOM[f"4{arm}{mode}{dname}"] = []
sp_by_day_thr = {}
for (day, thresh, i, s, sdir, hi, lo, atr_s) in SPIKE_SCAN:
    sp_by_day_thr.setdefault((day, thresh), []).append((i, s, sdir, hi, lo, atr_s))
for (day, thresh), lst in sp_by_day_thr.items():
    info = DAYS[day]
    g = info["frame"]
    arm = "a" if thresh == 2.0 else "b"
    for (i, s, sdir, hi, lo, atr_s) in lst:
        for mode in ("1", "2"):
            rp = float(g["rsi"].iloc[i if mode == "1" else s])
            if not np.isfinite(rp) or not (40 <= rp <= 55):
                continue
            if s + 1 > 32 or s + 1 >= len(g):
                continue
            ct = float(g["close"].iloc[s])
            if abs(ct - info["open"]) / PIP <= MIN_NET_TP_PIP:
                continue
            conf = g.iloc[s + 1]
            if not ((sdir == 1 and conf["close"] > ct) or (sdir == -1 and conf["close"] < ct)):
                continue
            entry = float(conf["close"])
            tp = entry + sdir * 1.5 * atr_s
            sl = entry - sdir * 1.0 * atr_s
            if abs(entry - tp) / PIP - COST_PIP < MIN_NET_TP_PIP:
                continue
            if (abs(entry - tp) / PIP - COST_PIP) / (abs(entry - sl) / PIP) < MIN_RR:
                continue
            cls = info["cls"]
            dname = "t" if cls == "B" else "s"
            MOM[f"4{arm}{mode}{dname}"].append({
                "day": day, "i": i, "s": s, "sdir": sdir, "hi": hi, "lo": lo,
                "atr_s": atr_s, "entry": entry, "tp": tp, "sl": sl, "rd": sdir,
                "rsi_bar1": float(g["rsi"].iloc[i]), "rsi_s": float(g["rsi"].iloc[s]),
            })
print("momentum mentah:", {k: len(v) for k, v in MOM.items()})
# Aturan pool: bila EITHER mode < 30 → MOOT → pool 4a1+4a2 per kelas hari
POOLED = {}
for arm in ("a", "b"):
    for dname in ("t", "s"):
        n1, n2 = len(MOM[f"4{arm}1{dname}"]), len(MOM[f"4{arm}2{dname}"])
        if n1 >= POWER_MIN_N and n2 >= POWER_MIN_N:
            POOLED[f"4{arm}1{dname}"] = MOM[f"4{arm}1{dname}"]
            POOLED[f"4{arm}2{dname}"] = MOM[f"4{arm}2{dname}"]
        else:
            print(f"4{arm}1{dname}={n1}, 4{arm}2{dname}={n2} → split MOOT → pool 4{arm}+4{arm}")
            POOLED[f"4{arm}_{dname}"] = MOM[f"4{arm}1{dname}"] + MOM[f"4{arm}2{dname}"]
for name, evs in POOLED.items():
    if len(evs) >= POWER_MIN_N:
        SEL[name] = evs
        print(f"{name} = {len(evs)} → UJI")
    else:
        print(f"{name} = {len(evs)} < {POWER_MIN_N} → drop+label (bukan STOP)")
for core in ("4a1t", "4a1s"):
    if core in SEL:
        TESTED.append(core)
for alt in ("4a_t", "4a_s"):
    if alt in SEL and alt not in TESTED:
        TESTED.append(alt)
        print(f"inti FDR memakai {alt} (hasil pool, dilaporkan)")
print("sel yang diuji:", TESTED)
print("SEL 4 SELESAI: ambang + rakitan + gate OK")
'''
)

md(
    """## Sel 5 — Konfirmasi, first-passage K=16, timeout MTM, simpan parquet

First-passage K=16 primer atas bar `confirm+1..confirm+K` (kontrak v9.3):
sentuh TP dulu → label 1; sentuh SL dulu → label 0; tak tersentuh → label 2
(timeout, dievaluasi MTM di `close(confirm+K)`). Tie intra-bar (TP dan SL
tersentuh bar yang sama) → SL-dulu (konservatif; jumlah tie
dilaporkan). Net pip = win `+(|entry−TP|−cost)`, loss `−(|entry−SL|−cost)`,
timeout MTM bertanda minus cost. Robustness K=8/32 dihitung di memori
(dilaporkan di Sel 6; parquet menyimpan primer K=16). **Parquet ditulis
SEBELUM vonis apa pun** (aturan §5).
"""
)

code(
    '''"""Sel 5 — pelabelan first-passage + simpan event parquet (pra-vonis)."""
import time

EVENTS_PARQUET = PROJECT_ROOT / "data" / "processed" / "events" / "eda06_candle_events.parquet"
T0 = time.perf_counter()
tie_count = 0


def first_passage(day, entry, tp, sl, rd, confirm_idx, K):
    """Return (label, net_pip, tie). SL-dulu bila tie intra-bar."""
    global tie_count
    g = DAYS[day]["frame"]
    H, L, C = g["high"].to_numpy(), g["low"].to_numpy(), g["close"].to_numpy()
    end = confirm_idx + K
    assert end < len(g), f"jendela K={K} keluar hari {day} → STOP (bukan diam)"
    for b in range(confirm_idx + 1, end + 1):
        if rd == -1:  # SELL: TP bawah (L), SL atas (H)
            hit_tp, hit_sl = L[b] <= tp, H[b] >= sl
        else:  # BUY: TP atas (H), SL bawah (L)
            hit_tp, hit_sl = H[b] >= tp, L[b] <= sl
        if hit_tp and hit_sl:
            tie_count += 1
            return 0, -((abs(entry - sl) / PIP) - COST_PIP), True
        if hit_tp:
            return 1, (abs(entry - tp) / PIP) - COST_PIP, False
        if hit_sl:
            return 0, -((abs(entry - sl) / PIP) - COST_PIP), False
    mtm = (C[end] - entry) / PIP if rd == 1 else (entry - C[end]) / PIP
    return 2, mtm - COST_PIP, False


LABELED = {}  # sel -> list row-dict (K=16 primer)
K_ROBUST = {}  # sel -> {8: [label], 32: [label]} (memori, utk Sel 6)
for sel, evs in SEL.items():
    if sel not in TESTED and sel in ("1", "2", "3"):
        continue
    if sel not in TESTED:
        continue
    rows, r8, r32 = [], [], []
    for ev in evs:
        info = DAYS[ev["day"]]
        g = info["frame"]
        is_mom = sel.startswith("4")
        trig = ev["s"] if is_mom else ev["r"]
        confirm_idx = trig + 1
        label, net, _ = first_passage(ev["day"], ev["entry"], ev["tp"], ev["sl"],
                                      ev["rd"], confirm_idx, KILL_K)
        l8, _n8, _t8 = first_passage(ev["day"], ev["entry"], ev["tp"], ev["sl"],
                                     ev["rd"], confirm_idx, 8)
        l32, _n32, _t32 = first_passage(ev["day"], ev["entry"], ev["tp"], ev["sl"],
                                        ev["rd"], confirm_idx, 32)
        r8.append(l8)
        r32.append(l32)
        rr = ((abs(ev["entry"] - ev["tp"]) / PIP - COST_PIP)
              / (abs(ev["entry"] - ev["sl"]) / PIP))
        if not is_mom:
            row = dict(day=ev["day"], i=ev["i"], s=ev["s"], r=ev["r"], trig=trig,
                       rsi14=float(g["rsi"].iloc[trig]),
                       rsi_bar1=float(g["rsi"].iloc[ev["i"]]),
                       rsi_s=float(g["rsi"].iloc[ev["s"]]))
        else:
            row = dict(day=ev["day"], i=ev["i"], s=ev["s"], r=None, trig=trig,
                       rsi14=float(g["rsi"].iloc[trig]),
                       rsi_bar1=ev["rsi_bar1"], rsi_s=ev["rsi_s"])
        row.update(sel_name=sel, entry=ev["entry"], tp=ev["tp"], sl=ev["sl"],
                   rd=ev["rd"], rr_value=float(rr), net_pnl_pip=float(net),
                   label_final=label, skip_reason=None, confirm_idx=confirm_idx)
        rows.append(row)
    LABELED[sel] = rows
    K_ROBUST[sel] = {8: r8, 32: r32}
print(f"tie intra-bar (SL-dulu, konservatif): {tie_count}")

# overlap + first-spike (in-memory, butuh info hari) → kolom string/bool
for sel, rows in LABELED.items():
    for n, row in enumerate(rows):
        wins = [(o["confirm_idx"] + 1, o["confirm_idx"] + KILL_K) for o in rows]
        ov = [str(m) for m, (a, b) in enumerate(wins)
              if m != n and a <= wins[n][1] and wins[n][0] <= b]
        row["overlap_with"] = ",".join(ov)
        day_spikes = [c["i"] for c in EXH_CAND if c["day"] == row["day"]] if not sel.startswith("4") \\
            else [t[2] for t in SPIKE_SCAN if t[0] == row["day"]]
        trig_i = row["s"] if sel.startswith("4") else row["i"]
        row["is_first_spike_of_day"] = bool(day_spikes and trig_i == min(day_spikes))

# ---- Bangun DataFrame kontrak Sel 7 (KOLOM PERSIS) ----
REC = []
for sel, rows in LABELED.items():
    for row in rows:
        info = DAYS[row["day"]]
        g = info["frame"]
        utc = g["time"].iloc[row["trig"]]
        if sel.startswith("4"):
            cand = None
            pre_size = [float((g["high"].iloc[k] - g["low"].iloc[k]) / PIP)
                        if k >= 0 else np.nan for k in range(row["s"] - 1, row["s"] - 11, -1)]
            pre_dir = [int(np.sign(g["close"].iloc[k] - g["open"].iloc[k]))
                       if k >= 0 else 0 for k in range(row["s"] - 1, row["s"] - 11, -1)]
            hi, lo = float(g["high"].iloc[row["i"] : row["s"] + 1].max()), \\
                float(g["low"].iloc[row["i"] : row["s"] + 1].min())
            is_cc = bool((row["rd"] == 1 and g["close"].iloc[row["confirm_idx"]] > row["entry"])
                         or (row["rd"] == -1 and g["close"].iloc[row["confirm_idx"]] < row["entry"]))
        else:
            cand = next(c for c in EXH_CAND if c["day"] == row["day"] and c["i"] == row["i"])
            pre_size, pre_dir = cand["pre_size"], cand["pre_dir"]
            hi, lo = cand["hi"], cand["lo"]
            cc = g.iloc[row["confirm_idx"]]
            is_cc = bool((row["rd"] == -1 and cc["close"] < cc["open"])
                         or (row["rd"] == 1 and cc["close"] > cc["open"]))
        rec = {
            "utc": utc, "daily_open_price": info["open"],
            "or_top": info["or_top"], "or_bottom": info["or_bottom"],
            "atr14": float(g["atr"].iloc[row["trig"]]),
            "rsi14": row["rsi14"], "rsi_bar1": row["rsi_bar1"], "rsi_at_s": row["rsi_s"],
            "spike_dir": int(-row["rd"]) if not sel.startswith("4") else int(row["rd"]),
            "spike_high": hi, "spike_low": lo,
            "trigger_bar": int(row["trig"]), "confirm_bar": int(row["confirm_idx"]),
            "entry_price": row["entry"], "tp_price": row["tp"], "sl_price": row["sl"],
            "rr_value": row["rr_value"], "net_pnl_pip": row["net_pnl_pip"],
            "label_final": row["label_final"], "skip_reason": row["skip_reason"],
            "sel_name": sel, "overlap_with": row["overlap_with"],
            "is_first_spike_of_day": row["is_first_spike_of_day"],
        }
        for j in range(10):
            rec[f"pre_{j + 1}_size"] = float(pre_size[j])
            rec[f"pre_{j + 1}_dir"] = int(pre_dir[j])
        rec["is_confirmed_color"] = is_cc
        rec["is_confirmed_breakout"] = is_cc
        REC.append(rec)
events = pd.DataFrame(REC)
EVENTS_PARQUET.parent.mkdir(parents=True, exist_ok=True)
events.to_parquet(EVENTS_PARQUET, index=False)
assert EVENTS_PARQUET.is_file(), "parquet gagal ditulis → STOP"
print(f"parquet PRA-VONIS tersimpan: {EVENTS_PARQUET.relative_to(PROJECT_ROOT)} "
      f"({len(events)} baris, {time.perf_counter() - T0:.1f}s)")
print(events["sel_name"].value_counts().to_dict())
print("SEL 5 SELESAI: pelabelan + parquet pra-vonis OK")
'''
)

md(
    """## Sel 6 — Inferensi: bootstrap cluster-hari, placebo dua track, FDR, vonis

Mean net per event (termasuk timeout MTM, minus cost) dengan CI95 bootstrap
cluster-hari 10.000 resample (seed 20261006). Null placebo DUA track
(regime-matched per sel — A2e): (i) reversal-track — pseudo-trigger seragam
atas 32 bar pertama tiap hari ber-event, $n$ = trigger riil hari itu
(min 1), pseudo-dir = tanda(close_trigger − O), entry = close(trigger+1),
TP = O, SL analog, postfilter biaya, side-agreement analog (salah-sisi
dibuang); (ii) momentum-track — coin-flip terarah (seed sama), TP = entry ±
1.5 ATR, SL = entry ∓ 1.0 ATR, postfilter biaya + RR. Trigger set IDENTIK
untuk kedua track (shared, PSEUDO_N=3 bar ekstrem trailing, seed 20261007).
$p_{sel}$ = (1 + #{null ≥ riil})/(1+$N_{valid}$); set tanpa event
qualifying → NaN → dikeluarkan ($N_{valid}$ dilaporkan; flag bila < 100).
FDR-BH q=0.10 atas sel inti yang DIUJI (subset FDR_CORE). Daya: CI95 lebih
lebar dari 5 pip → UNDERPOWERED. Robustness K=8/32 atas event riil
(dilaporkan; nested-test dicatat).
"""
)

code(
    '''"""Sel 6 — bootstrap + placebo regime-matched + FDR-BH + vonis per sel."""
import time

T1 = time.perf_counter()
rng_boot = np.random.default_rng(SEED_BOOT)
rng_null = np.random.default_rng(SEED_NULL)
RES = {}  # sel -> dict hasil


def boot_ci(values: np.ndarray, groups: np.ndarray):
    vals, groups = np.asarray(values), np.asarray(groups)
    uniq = np.unique(groups)
    idx = {u: np.where(groups == u)[0] for u in uniq}
    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        pick = rng_boot.integers(0, len(uniq), size=len(uniq))
        sel_idx = np.concatenate([idx[uniq[p]] for p in pick])
        boots[b] = vals[sel_idx].mean()
    return float(vals.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


for sel, rows in LABELED.items():
    nets = np.array([o["net_pnl_pip"] for o in rows])
    grps = np.array([o["day"] for o in rows])
    mean, lo, hi = boot_ci(nets, grps)
    l1 = sum(1 for o in rows if o["label_final"] == 1)
    l0 = sum(1 for o in rows if o["label_final"] == 0)
    l2 = sum(1 for o in rows if o["label_final"] == 2)
    RES[sel] = {"n": len(rows), "mean": mean, "ci_lo": lo, "ci_hi": hi,
                "winrate": (l1 / (l1 + l0)) if (l1 + l0) else np.nan,
                "n_l1": l1, "n_l0": l0, "n_l2": l2,
                "k8_mean_win": float(np.mean([1 if v == 1 else 0 for v in K_ROBUST[sel][8]])),
                "k32_mean_win": float(np.mean([1 if v == 1 else 0 for v in K_ROBUST[sel][32]]))}

# ---- Prakomputasi array hari utk placebo ----
PD = {}
for day in {o["day"] for rows in LABELED.values() for o in rows}:
    g = DAYS[day]["frame"]
    n = len(g)
    box = np.full(n, np.nan)
    dist = np.full(n, np.nan)
    O = DAYS[day]["open"]
    H, L, C = g["high"].to_numpy(), g["low"].to_numpy(), g["close"].to_numpy()
    for k in range(12, n):
        seg = slice(k - 12, k)
        box[k] = (H[seg].max() - L[seg].min()) / g["atr"].iloc[k]
        dist[k] = max(min(abs(c - DAYS[day]["or_top"]), abs(c - DAYS[day]["or_bottom"]))
                        for c in C[seg]) / g["atr"].iloc[k]
    PD[day] = {"H": H, "L": L, "C": C, "O": O, "n": n,
               "atr": g["atr"].to_numpy(), "ctx": DAYS[day]["ctx"],
               "cls": DAYS[day]["cls"], "box": box, "dist": dist}


def qualifies(sel, day, pk, pseudo_dir=None):
    """Predikat rezim sel atas trigger placebo pk (A2e)."""
    if sel == "1":
        return True
    if PD[day]["cls"] != "B":
        return False
    if sel == "2":
        return True
    if sel == "3":
        b, d = PD[day]["box"][pk], PD[day]["dist"][pk]
        return bool(np.isfinite(b) and np.isfinite(d) and b <= T_BOX and d <= T_DIST)
    if sel.endswith("t") and PD[day]["cls"] != "B":
        return False
    if sel.endswith("s") and PD[day]["cls"] == "B":
        return False
    return True


def label_track(day, entry, tp, sl, rd, confirm_idx):
    """First-passage K=16 primer utk SATU event placebo. None bila tak valid."""
    d = PD[day]
    end = confirm_idx + KILL_K
    if end >= d["n"]:
        return None
    H, L, C = d["H"], d["L"], d["C"]
    for b in range(confirm_idx + 1, end + 1):
        if rd == -1:
            htp, hsl = L[b] <= tp, H[b] >= sl
        else:
            htp, hsl = H[b] >= tp, L[b] <= sl
        if htp and hsl:
            return -((abs(entry - sl) / PIP) - COST_PIP)
        if htp:
            return (abs(entry - tp) / PIP) - COST_PIP
        if hsl:
            return -((abs(entry - sl) / PIP) - COST_PIP)
    mtm = (C[end] - entry) / PIP if rd == 1 else (entry - C[end]) / PIP
    return mtm - COST_PIP


evdays = sorted(PD)
trig_count = {d: max(1, sum(1 for rows in LABELED.values() for o in rows if o["day"] == d))
              for d in evdays}
print(f"Cek6: {len(evdays)} hari ber-event; mulai placebo {N_NULL}x2 track ...")
for sel, rows in LABELED.items():
    null_rev, null_mom = [], []
    for _ in range(N_NULL):
        pk_by_day = {d: rng_null.integers(4, min(32, PD[d]["n"]), size=trig_count[d])
                     for d in evdays}
        # Track reversal (pseudo-dir dari tanda close-O)
        vals = []
        for d in evdays:
            dd = PD[d]
            for pk in pk_by_day[d]:
                if pk + 1 >= dd["n"]:
                    continue
                a = dd["atr"][pk]
                if not np.isfinite(a) or a <= 0:
                    continue
                pdirec = -1 if dd["C"][pk] >= dd["O"] else 1
                en = float(dd["C"][pk + 1])
                if not ((pdirec == -1 and en > dd["O"]) or (pdirec == 1 and en < dd["O"])):
                    continue  # side-agreement analog
                if abs(en - dd["O"]) / PIP - COST_PIP < MIN_NET_TP_PIP:
                    continue
                lo3 = max(0, pk - PSEUDO_N)
                ph, pl = (float(dd["H"][lo3:pk].max()), float(dd["L"][lo3:pk].min())) \\
                    if pk > lo3 else (en, en)
                sl = max(en + a, ph + 0.5 * PIP) if pdirec == -1 else min(en - a, pl - 0.5 * PIP)
                if not qualifies(sel, d, pk, pdirec):
                    continue
                v = label_track(d, en, dd["O"], sl, pdirec, pk + 1)
                if v is not None:
                    vals.append(v)
        null_rev.append(float(np.mean(vals)) if vals else np.nan)
        # Track momentum (coin-flip, TP 1.5R / SL 1.0R)
        vals = []
        for d in evdays:
            dd = PD[d]
            for pk in pk_by_day[d]:
                if pk + 1 >= dd["n"]:
                    continue
                a = dd["atr"][pk]
                if not np.isfinite(a) or a <= 0:
                    continue
                mdirec = 1 if rng_null.random() < 0.5 else -1
                en = float(dd["C"][pk + 1])
                tp = en + mdirec * 1.5 * a
                sl = en - mdirec * 1.0 * a
                if abs(en - tp) / PIP - COST_PIP < MIN_NET_TP_PIP:
                    continue
                if (abs(en - tp) / PIP - COST_PIP) / (abs(en - sl) / PIP) < MIN_RR:
                    continue
                if not qualifies(sel, d, pk, mdirec):
                    continue
                v = label_track(d, en, tp, sl, mdirec, pk + 1)
                if v is not None:
                    vals.append(v)
        null_mom.append(float(np.mean(vals)) if vals else np.nan)
    for track, null in (("rev", null_rev), (("mom", null_mom))):
        arr = np.array([v for v in null if np.isfinite(v)])
        RES[sel][f"{track}_n_valid"] = len(arr)
        RES[sel][f"{track}_null_mean"] = float(arr.mean()) if len(arr) else np.nan
        RES[sel][f"{track}_null_p95"] = float(np.percentile(arr, 95)) if len(arr) else np.nan
        RES[sel][f"{track}_p"] = float((1 + np.sum(arr >= RES[sel]["mean"])) / (1 + len(arr))) \\
            if len(arr) else np.nan
        if len(arr) < 100:
            print(f"PERINGATAN: {sel}/{track} hanya {len(arr)} set valid (<100)")
print(f"placebo selesai ({time.perf_counter() - T1:.1f}s)")

# ---- FDR-BH q=0.10 atas sel inti yang DIUJI ----
core_tested = [s for s in FDR_CORE if s in RES] + [s for s in ("4a_t", "4a_s") if s in RES]
pvals = sorted(((RES[s]["rev_p"], s) for s in core_tested))
m = len(pvals)
fdr_pass = set()
for rank, (p, s) in enumerate(pvals, start=1):
    if p <= rank / m * FDR_Q:
        fdr_pass.add(s)
print("FDR-BH: inti diuji =", core_tested, "| lolos =", sorted(fdr_pass))


def vonis(sel):
    r = RES[sel]
    if (r["ci_hi"] - r["ci_lo"]) > POWER_MAX_CIWIDTH_PIP:
        return "UNDERPOWERED", "CI95 lebih lebar dari 5 pip"
    Ribeiro = min(r["rev_p"], r["mom_p"])
    if sel in core_tested:
        if sel in fdr_pass:
            return "LOLOS", f"FDR-pass (p_rev={r['rev_p']:.4f} p_mom={r['mom_p']:.4f})"
        return "GUGUR", f"null tak-terkalahkan/FDR-gugur (p_rev={r['rev_p']:.4f} p_mom={r['mom_p']:.4f})"
    if Ribeiro < 0.10:
        return "SINYAL-NOMINAL", f"p={Ribeiro:.4f} (sensitivitas, tanpa klaim)"
    return "GUGUR", f"p nominal >= 0.10 (p_rev={r['rev_p']:.4f} p_mom={r['mom_p']:.4f})"


print("\\n=== VONIS PER SEL (§5) ===")
for sel in RES:
    r = RES[sel]
    v, why = vonis(sel)
    r["vonis"], r["vonis_why"] = v, why
    print(f"Sel {sel}: n={r['n']} mean={r['mean']:+.2f} CI95=[{r['ci_lo']:+.2f},{r['ci_hi']:+.2f}] "
          f"win={r['winrate']:.2f} (L1={r['n_l1']}/L0={r['n_l0']}/L2={r['n_l2']}) "
          f"K8win={r['k8_mean_win']:.2f} K32win={r['k32_mean_win']:.2f} → {r['vonis']} ({r['vonis_why']})")
DROPPED = {}  # sel drop+label (<30): vonis §5 = TIDAK TAHU
for sel in ("2", "3"):
    if sel not in RES:
        DROPPED[sel] = (f"n={len(SEL[sel])} < {POWER_MIN_N} (drop+label, bukan STOP)")
for name, evs in POOLED.items():
    if name not in SEL:
        DROPPED[name] = (f"n={len(evs)} < {POWER_MIN_N} (drop+label, bukan STOP)")
for sel, why in DROPPED.items():
    print(f"Sel {sel}: → TIDAK TAHU ({why})")
print("SEL 6 SELESAI: inferensi + vonis OK (parquet sudah tersimpan di Sel 5)")
'''
)

md(
    """## Sel 7 — Handoff: consistency check + kolom + batas klaim

Consistency check meng-assert konstanta amandemen (`DAILY_OPEN_HOURS==[22,23]`,
`FDR_CORE=={1,2,3,4a1t,4a1s}`), daftar kolom parquet persis kontrak, dan
keberadaan file SEBELUM vonis dirujuk. Klaim maju (bila Sel 1 LOLOS): reversal
pasca-spike umum. Batas: TV-01 & FS-01 pindah ke Lapisan V (putusan A4);
partisi P/2026 SEGEL dan tak tersentuh notebook ini; AMD-full = UNTESTED.
"""
)

code(
    '''"""Sel 7 — consistency check amandemen + handoff ( dibaca auditor )."""
assert DAILY_OPEN_HOURS == [22, 23], "inkonsistensi DAILY_OPEN_HOURS"
assert set(FDR_CORE) == {"1", "2", "3", "4a1t", "4a1s"}, "inkonsistensi FDR_CORE"
assert EVENTS_PARQUET.is_file(), "parquet hilang sesudah vonis → STOP"

BASE_COLS = ["utc", "daily_open_price", "or_top", "or_bottom", "atr14", "rsi14",
             "rsi_bar1", "rsi_at_s", "spike_dir", "spike_high", "spike_low",
             "trigger_bar", "confirm_bar", "entry_price", "tp_price", "sl_price",
             "rr_value", "net_pnl_pip", "label_final", "skip_reason", "sel_name",
             "overlap_with", "is_first_spike_of_day"]
PRE_COLS = [f"pre_{j}_{k}" for j in range(1, 11) for k in ("size", "dir")]
CONF_COLS = ["is_confirmed_color", "is_confirmed_breakout"]
NULL_COLS = [f"{t}_{c}" for t in ("rev", "mom")
             for c in ("null_mean", "null_p95", "p_sel", "ci_lo", "ci_hi", "n_null")]
ev = pd.read_parquet(EVENTS_PARQUET)
for sel, r in RES.items():
    mask = ev["sel_name"] == sel
    ev.loc[mask, "rev_null_mean"] = r["rev_null_mean"]
    ev.loc[mask, "rev_null_p95"] = r["rev_null_p95"]
    ev.loc[mask, "rev_p_sel"] = r["rev_p"]
    ev.loc[mask, "rev_ci_lo"] = r["ci_lo"]
    ev.loc[mask, "rev_ci_hi"] = r["ci_hi"]
    ev.loc[mask, "rev_n_null"] = r["rev_n_valid"]
    ev.loc[mask, "mom_null_mean"] = r["mom_null_mean"]
    ev.loc[mask, "mom_null_p95"] = r["mom_null_p95"]
    ev.loc[mask, "mom_p_sel"] = r["mom_p"]
    ev.loc[mask, "mom_ci_lo"] = r["ci_lo"]
    ev.loc[mask, "mom_ci_hi"] = r["ci_hi"]
    ev.loc[mask, "mom_n_null"] = r["mom_n_valid"]
assert list(ev.columns) == BASE_COLS + PRE_COLS + CONF_COLS + NULL_COLS, \\
    f"kolom parquet melanggar kontrak Sel 7: {list(ev.columns)}"
ev.to_parquet(EVENTS_PARQUET, index=False)  # tulis balik dgn kolom placebo
print(f"kolom OK ({len(ev.columns)} kolom persis kontrak) + placebo terisi; "
      f"file: {EVENTS_PARQUET.relative_to(PROJECT_ROOT)}")
print("ambang:", round(T_DAY, 4), round(T_BOX, 4), round(T_DIST, 4),
      "| vonis:", {s: RES[s]['vonis'] for s in RES}, "| drop (TIDAK TAHU):", sorted(DROPPED))
print("HANDOFF: TV-01/FS-01 → Lapisan V (A4); P/2026 SEGEL tak tersentuh; AMD-full UNTESTED.")
print("=== nb06 SELESAI: SEMUA ASSERTION PASS ===")
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

    # Normalisasi format SEL NOTEBOOK sebelum eksekusi (kelas regresi SA-41).
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
    # Pasca-proses Q2 (putusan arsitek 2026-10-07): normalisasi EOL notebook
    # sesudah nbconvert --inplace (penulis Windows menghasilkan CRLF).
    _nb_bytes = NB_PATH.read_bytes().replace(b"\r\n", b"\n")
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(_nb_bytes.decode("utf-8"))

    print(f"nbconvert exit={result.returncode}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    build()
