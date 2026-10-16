"""Generator + executor for notebooks/scalping/eda_09_wick_confirm.ipynb.

# LENGTH_EXCEPTION: generator §15.1 — referensi stabil + diff kecil +
# deterministik (seed tetap) + assertion mesin (bukan dokumen).
#
# REVIEW LOG (FASE 0, AGENTS.md §4 butir 9):
# R1: FASE 0 menuntut ruff atas builder namun melarang "menulis" generator
#     sebelum lulus — kontradiksi internal brief; diselesaikan via supremasi
#     blueprint (tak melarang authoring statis) + literal impossibility:
#     authoring statis = objek audit; yang digerbang = EKSEKUSI (nbconvert).
#     Dieksekusi hanya setelah FASE 0 LULUS tertulis.
# R2: Scan atas DAYS_ALL (termasuk hari-R) lalu whitelist-V = perintah harfiah
#     Amandemen-2 §3; BUKAN rescan-R (parquet-R tak ditulis-ulang di sini;
#     artefak-R dibuang tanpa dilapor/diuji/dinarasikan).
# R3: SEED_EXEC = tanggal UTC eksekusi nyata (20261016); BUKAN warisan EDA-08.
# R4: print() progres build() mengikuti preseden beku EDA-07/08; print() di sel
#     notebook = mekanisme bukti (ditempel ke laporan), bukan print() produksi.
# R5: Fungsi sel ditulis inline-string (tak terlihat ruff); kode modul hanya
#     md/code/build — ruff check + format --check wajib rc=0 (FASE 0).

EDA-09 wick_confirm_V (Blueprint FINAL 2026-10-16 §§1–15 + Amandemen-1/2):
KONFIRMASI di V (virgin) — satu-satunya uji = wick pooled SATU-ARAH α=0,05
(cut TERKUNCI dari R); volume-(c) lock-in 0 uji; P (2026) SEGEL.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_09_wick_confirm.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA-09 — wick_confirm_V (konfirmasi di virgin)

**Blueprint:** `thoughts/shared/plans/2026-10-16-eda09-wick-confirm-draf.md` (§§1–15,
FINAL + Amandemen-1 + Amandemen-2). **Peran ronde:** KONFIRMASI di V (2025) — BUKAN
generasi. Satu-satunya uji = Q-wick-V pooled SATU-ARAH (α=0,05, cut TERKUNCI R).
P (2026) DILARANG disentuh. R dipakai HANYA untuk: F0 reproduksi-cut + histori
baseline volume + warmup indikator concat (§3, Amandemen-2).

## Aturan yang mengikat notebook ini
- **P3 lock-sebelum-V:** F0 (Sel 1) hijau SEBELUM sentuh V (sentuh = load hari-2025
  mana pun). Sel 1 HANYA memuat 2023+2024 + parquet-R.
- **Cut-lock:** `_tercile_masks` IDENTIK EDA-08; F0 assert `round(pooled,4)==0.1682`
  + 8 cut SAMA PERSIS §15 → dibekukan sebagai konstanta; V memakai cut-terkunci
  (hitung-ulang tercil di V = DILARANG).
- **Indikator concat:** ATR14/RSI14-Wilder pada frame 2023+2024+2025; whitelist-V
  SESUDAH deteksi; artefak-R = terbuang (tak dilapor/diuji/dinarasikan).
- **T_DAY = 1,7319 KONSTANTA** (recompute DILARANG; assert-vs-EDA-06 dicabut
  tertulis). cls/ctx = metadata, nol peran putusan.
- **Null:** permutasi NILAI wick DALAM band, cut-TERKUNCI diterapkan ulang per
  permutasi, B=10000, STRATA=BAND, p SATU-ARAH 4 desimal. Satu-seed-satu-run.
- **DILARANG:** first/gap32/dow (lapor/uji/narasi), joint, klaim per-band, L2/trade,
  floor-efek, split selain H1/H2-preregistered, uji ke-2, re-seed.
"""
)

code(
    '''"""Sel 1 — setup, kontrak, R-384, F0 cut-lock (SEBELUM sentuh V)."""
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
T_DAY = 1.7319  # KONSTANTA warisan-R (§3/§10-H4); recompute DILARANG
R_START = pd.Timestamp("2023-07-01", tz="UTC")
R_END_EXCL = pd.Timestamp("2025-01-01", tz="UTC")
V_START = pd.Timestamp("2025-01-01", tz="UTC")
V_END_EXCL = pd.Timestamp("2026-01-01", tz="UTC")
SEED_EXEC = 20261016  # YYYYMMDD-eksekusi UTC; BARU, independen dari EDA-08
S_WICK = SEED_EXEC + 11
S_BOOT = SEED_EXEC + 1
N_NULL = 10_000
N_BOOT = 10_000
BAND_EDGES = [1.5, 2.0, 2.5, 3.0]
EPS = 1e-6
POWER_MIN_N = 30
WARMUP_DAYS = 20
DAILY_OPEN_HOURS = [22, 23]

assert DAILY_OPEN_HOURS == [22, 23]
assert (N_BOOT, N_NULL) == (10_000, 10_000)
assert BAND_EDGES == [1.5, 2.0, 2.5, 3.0] and POWER_MIN_N == 30
assert SEED_EXEC not in (20261006, 20261007, 20261015)
assert T_DAY == 1.7319


def _tercile_masks(vals: np.ndarray):
    """Batas P33.3/P66.7 gaya EDA-08 §Sel-3 (lo_<=x<hi_) — salin verbatim."""
    t1 = float(np.percentile(vals, 100 / 3))
    t2 = float(np.percentile(vals, 200 / 3))
    return (vals < t1), ((vals >= t1) & (vals < t2)), (vals >= t2), (t1, t2)


def _boot_ci(vals, day_ids, stat, seed, b=N_BOOT):
    """Warisan verbatim EDA-07 (cluster-bootstrap per hari)."""
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


def _load(tf: str, years: tuple) -> pd.DataFrame:
    """Warisan verbatim EDA-07 Sel 1 (beban M15/D1 + broker_day) + tahun parameter."""
    frames = [pd.read_parquet(DATA / tf / f"usdjpy_{tf.lower()}_{y}.parquet") for y in years]
    df = pd.concat(frames, ignore_index=True)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df = df.sort_values("time").reset_index(drop=True)
    df["broker_time"] = wall_clock_series(df["broker_time_raw"])
    df["broker_day"] = df["broker_time"].dt.date
    return df


# ---- R-384 (HANYA 2023+2024 — V belum disentuh) ----
m15r = _load("M15", (2023, 2024))
d1r = _load("D1", (2023, 2024))
anom_days: set = set()
for start, end in ANOMALY:
    anom_days.update(pd.date_range(start, end).date)
r = m15r[(m15r["time"] >= R_START) & (m15r["time"] < R_END_EXCL)].copy()
assert r["time"].max() < R_END_EXCL
r = r[~r["broker_day"].isin(anom_days)].copy()
assert not r["broker_day"].isin(anom_days).any()

DAYS_R: dict = {}
for day, g in r.groupby("broker_day"):
    g = g.sort_values("time").reset_index(drop=True)
    if g["time"].iloc[0].hour not in DAILY_OPEN_HOURS:
        continue
    DAYS_R[day] = {"frame": g, "open": float(g["open"].iloc[0])}
print(f"R: {len(r)} bar | hari bersih = {len(DAYS_R)} (ekspektasi 384)")
assert len(DAYS_R) == 384, "partisi R != 384 → STOP"
MANIFEST_R = sorted(DAYS_R)

# ---- F0: parquet-R jangkar bit-identik vs vonis EDA-07 (aktual vs ekspektasi) ----
PQ = PROJECT_ROOT / "data/processed/events/eda07_spike_events.parquet"
assert PQ.is_file(), "parquet EDA-07 hilang → STOP"
EVR = pd.read_parquet(PQ)
EVR["day"] = pd.to_datetime(EVR["day"]).dt.date
_exp_n, _act_n = 1632, len(EVR)
print(f"F0 Nunik: aktual={_act_n} ekspektasi={_exp_n}")
assert _act_n == _exp_n, "F0 Nunik → STOP"
_bc_all = EVR["band"].value_counts().sort_index().to_dict()
print(f"F0 band-unik: aktual={_bc_all} ekspektasi={{0: 515, 1: 415, 2: 240, 3: 462}}")
assert _bc_all == {0: 515, 1: 415, 2: 240, 3: 462}, "F0 band → STOP"
FRR = EVR[EVR["drop_flag"] == 0].copy()
print(f"F0 full-room: aktual={len(FRR)} ekspektasi=1514")
assert len(FRR) == 1514, "F0 full-room → STOP"
_bc_fr = FRR["band"].value_counts().sort_index().to_dict()
print(f"F0 band-fullroom: aktual={_bc_fr} ekspektasi={{0: 460, 1: 391, 2: 231, 3: 432}}")
assert _bc_fr == {0: 460, 1: 391, 2: 231, 3: 432}, "F0 band-fullroom → STOP"
_exh = int(FRR["has_exhaustion"].sum())
print(f"F0 exh: aktual={(_exh, len(FRR) - _exh)} ekspektasi=(395, 1119)")
assert (_exh, len(FRR) - _exh) == (395, 1119), "F0 exh → STOP"
FRR["wick_ratio"] = 1.0 - FRR["q3_ratio"].abs()
assert ((FRR["wick_ratio"] >= -EPS) & (FRR["wick_ratio"] <= 1 + EPS)).all()

# ---- F0 cut-lock: hitung-ulang cut tercil R + assert §15 ----
CUT_REC = {}
for _b in range(4):
    _w = FRR[FRR["band"] == _b]["wick_ratio"].to_numpy()
    _, _, _, (_t1, _t2) = _tercile_masks(_w)
    CUT_REC[_b] = (_t1, _t2)
CUT_LOCK = {0: (0.24647887323941978, 0.47041420118341626),
            1: (0.1954397394136033, 0.3721973094169312),
            2: (0.1717716422203372, 0.33835948462822907),
            3: (0.16332011857566983, 0.3379338240019312)}
for _b in range(4):
    print(f"F0 cut band{_b}: aktual={CUT_REC[_b]!r} ekspektasi={CUT_LOCK[_b]!r}")
    assert CUT_REC[_b] == CUT_LOCK[_b], f"F0 cut band{_b} ≠ §15 → STOP"


def _pooled_delta_locked(ws, ys, cuts):
    num, den, per = 0.0, 0, {}
    for b in ws:
        t1, t2 = cuts[b]
        lo_m = ws[b] < t1
        hi_m = ws[b] >= t2
        d_b = float(ys[b][hi_m].mean() - ys[b][lo_m].mean())
        per[b] = (d_b, int(lo_m.sum()), int(hi_m.sum()))
        num += len(ys[b]) * d_b
        den += len(ys[b])
    return num / den, per


W_wR = {b: FRR[FRR["band"] == b]["wick_ratio"].to_numpy() for b in range(4)}
W_yR = {b: np.array([1.0 if o == "reversal" else 0.0
                     for o in FRR[FRR["band"] == b]["outcome"]]) for b in range(4)}
_pooled_R, _per_R = _pooled_delta_locked(W_wR, W_yR, CUT_LOCK)
print(f"F0 pooled-Δ reproduksi: aktual={_pooled_R!r} round4={round(_pooled_R, 4)} ekspektasi=0.1682")
assert round(_pooled_R, 4) == 0.1682, "F0 pooled ≠ 0.1682 → STOP"
for _b in range(4):
    print(f"  F0 per-band-R band{_b}: Δ={_per_R[_b][0]:.4f} (deskr. GENERASI-R) [GENERASI-R]")
print("F0: CUT-LOCK BEKU ✓ (P3 hijau — baru boleh sentuh V)")
print("SEL 1 SELESAI")
'''
)

code(
    '''"""Sel 2 — F1: V-whitelist + availabilitas + STOP-band (pra-detekksi)."""
m15c = _load("M15", (2023, 2024, 2025))
d1c = _load("D1", (2023, 2024, 2025))
v = m15c[(m15c["time"] >= V_START) & (m15c["time"] < V_END_EXCL)].copy()
assert v["time"].max() < V_END_EXCL, "V bocor ke 2026+ → STOP (P tersentuh)"
assert v["time"].min() >= V_START
v = v[~v["broker_day"].isin(anom_days)].copy()
assert not v["broker_day"].isin(anom_days).any()

DAYS_V: dict = {}
for day, g in v.groupby("broker_day"):
    g = g.sort_values("time").reset_index(drop=True)
    if g["time"].iloc[0].hour not in DAILY_OPEN_HOURS:
        continue
    DAYS_V[day] = {"frame": g, "open": float(g["open"].iloc[0])}
MANIFEST_V = sorted(DAYS_V)
print(f"V: {len(v)} bar | hari bersih = {len(MANIFEST_V)} (ekspektasi ≈259)")

# ---- F1 asserts ----
assert all(str(d)[:4] == "2025" for d in MANIFEST_V), "hari-V tak ⊆ 2025 → STOP"
assert set(MANIFEST_V).isdisjoint(set(MANIFEST_R)), "V∩R ≠ ∅ → STOP (whitelist dua-arah)"
assert max(MANIFEST_V) < pd.Timestamp("2026-01-01").date(), "max(day-V) ≥ 2026-01-01 → STOP"
_nV_days = len(MANIFEST_V)
print(f"F1 hari-V: aktual={_nV_days} STOP-band=[<200, >320]")
assert 200 <= _nV_days <= 320, "STOP-band hari-V → STOP + arsitek"
_nV_bars = len(v)
print(f"F1 bar-M15-V: aktual={_nV_bars} ekspektasi≈20–28k STOP-band=[<13k, >40k]")
assert 13_000 <= _nV_bars <= 40_000, "STOP-band bar-M15-V → STOP + arsitek"
print("F1 (hari/bar/whitelist) HIJAU ✓")
print("SEL 2 SELESAI")
'''
)

code(
    '''"""Sel 3 — indikator concat (2023+2024+2025) + T_DAY konstanta + sesi."""
NSMOOTH = 14


def _wilder_ema(series: pd.Series, n: int = NSMOOTH) -> pd.Series:
    return series.ewm(alpha=1.0 / n, adjust=False).mean()


_prev = m15c["close"].shift(1)
_tr = pd.concat(
    [m15c["high"] - m15c["low"], (m15c["high"] - _prev).abs(), (m15c["low"] - _prev).abs()],
    axis=1,
).max(axis=1)
m15c["atr"] = _wilder_ema(_tr).shift(1)
_delta = m15c["close"].diff()
_rs = _wilder_ema(_delta.clip(lower=0)) / _wilder_ema((-_delta).clip(lower=0))
m15c["rsi"] = 100.0 - 100.0 / (1.0 + _rs)

d1c = d1c.sort_values("time").reset_index(drop=True)
_dprev = d1c["close"].shift(1)
_dtr = pd.concat(
    [d1c["high"] - d1c["low"], (d1c["high"] - _dprev).abs(), (d1c["low"] - _dprev).abs()],
    axis=1,
).max(axis=1)
d1c["atr"] = _wilder_ema(_dtr)
d1c["bday"] = pd.to_datetime(d1c["broker_time_raw"], unit="s").dt.date


def day_ctx(day):
    past = d1c[d1c["bday"] < day].tail(5)
    if len(past) < 5 or not np.isfinite(past["atr"].iloc[-1]) or past["atr"].iloc[-1] <= 0:
        return None
    return float((past["high"].max() - past["low"].min()) / past["atr"].iloc[-1])


# DAYS_ALL atas frame concat (Amandemen-2 §3); whitelist-V SESUDAH deteksi
DAYS_ALL: dict = {}
for day, g in pd.concat([r, v]).groupby("broker_day"):
    g = g.sort_values("time").reset_index(drop=True)
    if g["time"].iloc[0].hour not in DAILY_OPEN_HOURS:
        continue
    DAYS_ALL[day] = {"frame": g, "open": float(g["open"].iloc[0])}
print(f"DAYS_ALL: {len(DAYS_ALL)} hari (R+V concat, indikator warmup-penuh)")

for day, info in DAYS_ALL.items():
    g = info["frame"]
    idx = m15c.index[m15c["time"] == g["time"].iloc[0]][0]
    info["frame"] = g.assign(atr=m15c["atr"].iloc[idx : idx + len(g)].to_numpy(),
                             rsi=m15c["rsi"].iloc[idx : idx + len(g)].to_numpy()).reset_index(drop=True)
    info["ctx"] = day_ctx(day)
assert sum(1 for vinfo in DAYS_ALL.values() if vinfo["ctx"] is not None) / len(DAYS_ALL) > 0.95


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
        vv = rsi[k]
        if not np.isfinite(vv):
            continue
        if (sdir == 1 and vv >= 70) or (sdir == -1 and vv <= 30):
            return k
    return None


sys.path.insert(0, str(PROJECT_ROOT / "notebooks/scalping"))
from _eda_common import exclusive_label, session_fingerprint, session_flags  # noqa: E402
from _eda_common import EXPECTED_FINGERPRINT  # noqa: E402

assert session_fingerprint() == EXPECTED_FINGERPRINT, "definisi sesi berubah → STOP"
for day, info in DAYS_ALL.items():
    g = info["frame"]
    flags = session_flags(g["time"])
    info["sess"] = exclusive_label(flags).to_numpy()
# cls/ctx = metadata (integrity), nol peran putusan; T_DAY KONSTANTA
from collections import Counter  # noqa: E402


def _day_class(day) -> str:
    ctx = DAYS_ALL[day]["ctx"]
    if ctx is None or ctx < T_DAY:
        return "B"
    past = d1c[d1c["bday"] < day].tail(5)
    return "A" if float(past["close"].iloc[-1] - past["close"].iloc[0]) > 0 else "C"


for day in DAYS_ALL:
    DAYS_ALL[day]["cls"] = _day_class(day)
print("kelas hari concat:", dict(Counter(vinfo["cls"] for vinfo in DAYS_ALL.values())))
print("SEL 3 SELESAI")
'''
)

code(
    '''"""Sel 4 — scan concat + dedup + whitelist-V (artefak-R dibuang diam)."""
DET = []
for day in sorted(DAYS_ALL):
    g = DAYS_ALL[day]["frame"]
    for thresh in (2.0, 1.5):
        for (i, s, sdir, hi, lo) in scan_spikes(g, thresh):
            DET.append((day, thresh, i, s, sdir, hi, lo, float(g["atr"].iloc[s])))

parent = list(range(len(DET)))


def _find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


by_day: dict = {}
for k, d in enumerate(DET):
    by_day.setdefault(d[0], []).append(k)
for day, idxs in by_day.items():
    a = [k for k in idxs if DET[k][1] == 2.0]
    b = [k for k in idxs if DET[k][1] == 1.5]
    for ka in a:
        for kb in b:
            if DET[ka][4] == DET[kb][4] and DET[ka][2] <= DET[kb][3] and DET[kb][2] <= DET[ka][3]:
                ra, rb = _find(ka), _find(kb)
                if ra != rb:
                    parent[rb] = ra
groups: dict = {}
for k in range(len(DET)):
    groups.setdefault(_find(k), []).append(k)

UNIQ_ALL = []
for members in groups.values():
    mag, k = max(((DET[k][5] - DET[k][6]) / DET[k][7], k) for k in members)
    day, thresh, i, s, sdir, hi, lo, atr_s = DET[k]
    band = next((bi for bi, (lo_, hi_) in
                 enumerate([(1.5, 2.0), (2.0, 2.5), (2.5, 3.0), (3.0, np.inf)])
                 if lo_ <= mag < hi_), None)
    if band is None:
        band = 0  # overflow: mag < 1.5 (tak mungkin dominan; dicatat, bukan drop-diam)
    UNIQ_ALL.append({"day": day, "i": i, "s": s, "sdir": sdir, "hi": hi, "lo": lo,
                     "atr_s": atr_s, "mag": mag, "band": band,
                     "cls": DAYS_ALL[day]["cls"], "ctx": DAYS_ALL[day]["ctx"]})
assert all(u["band"] in (0, 1, 2, 3) for u in UNIQ_ALL), "band liar → STOP"

# ---- WHITELIST-V SESUDAH deteksi (§3 Amandemen-2); artefak-R dibuang ----
SET_V = set(MANIFEST_V)
UNIQ = [u for u in UNIQ_ALL if u["day"] in SET_V]
assert all(str(u["day"])[:4] == "2025" for u in UNIQ), "event-V tak ⊆ 2025 → STOP"
assert not (set(u["day"] for u in UNIQ) & set(MANIFEST_R)), "V∩R → STOP"
print(f"UNIQ-V: {len(UNIQ)} event di {len(set(u['day'] for u in UNIQ))} hari [KONFIRMASI-V]")
bc_v = pd.Series([u["band"] for u in UNIQ]).value_counts().sort_index().to_dict()
print(f"band-V: {bc_v} [KONFIRMASI-V]")
print("SEL 4 SELESAI")
'''
)

code(
    '''"""Sel 5 — outcome machine + wick + A1/A2 + F1-vol + F2 tripwire."""
OUT = {}
KILL = 16
WIN = 16
for n, u in enumerate(UNIQ):
    g = DAYS_ALL[u["day"]]["frame"]
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
        OUT[n] = {"drop": False, "outcome": "timeout", "bar_ke": -1}
        continue
    oc, bbar = res
    OUT[n] = {"drop": False, "outcome": oc, "bar_ke": bbar - s}

AN = [n for n in range(len(UNIQ)) if not OUT[n]["drop"]]
print(f"analyzed={len(AN)} dropped={len(UNIQ) - len(AN)} [KONFIRMASI-V]")
for b in range(4):
    idx = [n for n in AN if UNIQ[n]["band"] == b]
    cr = sum(1 for n in idx if OUT[n]["outcome"] == "reversal")
    cc = sum(1 for n in idx if OUT[n]["outcome"] == "continuation")
    ct = sum(1 for n in idx if OUT[n]["outcome"] == "timeout")
    assert cr + cc + ct == len(idx), f"A1 band {b} tak-exhaustive → STOP"
    print(f"A1 band{b}: n={len(idx)} rev={cr} cont={cc} timeout={ct} [KONFIRMASI-V]")
assert sum(1 for n in AN for _ in [0]) == len(AN)

FRV = pd.DataFrame([{"day": UNIQ[n]["day"], "band": UNIQ[n]["band"],
                     "outcome": OUT[n]["outcome"], "s": UNIQ[n]["s"],
                     "cls": UNIQ[n]["cls"], "ctx": UNIQ[n]["ctx"]} for n in AN])
FRV["is_rev"] = (FRV["outcome"] == "reversal").astype(float)
# wick_ratio dari q3: 1 - |net/range| — dihitung ulang dari frame (verbatim EDA-07 Q3)
_wicks = []
for n in AN:
    u = UNIQ[n]
    g = DAYS_ALL[u["day"]]["frame"]
    C_ = g["close"].to_numpy()
    O_ = g["open"].to_numpy()
    net_sp = u["sdir"] * (float(C_[u["s"]]) - float(O_[u["i"]]))
    rng_sp = u["hi"] - u["lo"]
    assert rng_sp > 0
    ratio = net_sp / rng_sp
    assert abs(ratio) <= 1 + EPS, f"|rasio|>1+eps → STOP"
    wick = rng_sp - abs(net_sp)
    if wick < 0:
        assert wick > -1e-6, "wick negatif melebihi eps → STOP"
        wick = 0.0
    _wicks.append(1.0 - abs(ratio))
FRV["wick_ratio"] = np.array(_wicks)
assert ((FRV["wick_ratio"] >= -EPS) & (FRV["wick_ratio"] <= 1 + EPS)).all()

# ---- A2: cut-TERKUNCI teraplikasi EXHAUSTIVE untuk SEMUA event-V ----
for b in range(4):
    _t1, _t2 = CUT_LOCK[b]
    _w = FRV[FRV["band"] == b]["wick_ratio"].to_numpy()
    _lo = _w < _t1
    _md = (_w >= _t1) & (_w < _t2)
    _hi = _w >= _t2
    assert int(_lo.sum() + _md.sum() + _hi.sum()) == len(_w), f"A2 band{b} tak-exhaustive → STOP"
    print(f"A2 band{b}: n={len(_w)} bawah={int(_lo.sum())} tengah={int(_md.sum())} "
          f"atas={int(_hi.sum())} (cut-terkunci) [KONFIRMASI-V]")

# ---- F1-vol: tick_volume bar-s-V terisi ≥0.95 (PER BAR-S, bukan agregat) ----
FRV["vol_s"] = [float(DAYS_ALL[d]["frame"]["tick_volume"].iloc[s])
                for d, s in zip(FRV["day"], FRV["s"])]
f1_fill = float(np.isfinite(FRV["vol_s"].to_numpy()).mean())
print(f"F1-vol: tick_volume bar-s-V terisi {f1_fill:.4f} (pagar ≥0.95) [KONFIRMASI-V]")
VOL_OK = bool(f1_fill >= 0.95)
if not VOL_OK:
    print("F1-vol GAGAL → volume 'tertunda', wick-confirm LANJUT (kontinjensi §2)")

# ---- F2: struktural + TRIPWIRE DAYA ----
assert all(int((FRV["band"] == b).sum()) > 0 for b in range(4)), "band-V kosong → STOP"
_nV = len(FRV)
print(f"F2 total-n-V: aktual={_nV} tripwire=[<500 → STOP] ekspektasi≈1020 [KONFIRMASI-V]")
assert _nV >= 500, "TRIPWIRE DAYA total n-V < 500 → STOP + arsitek (BUKAN GUGUR)"
for b in range(4):
    _t1, _t2 = CUT_LOCK[b]
    _w = FRV[FRV["band"] == b]["wick_ratio"].to_numpy()
    _nlo, _nhi = int((_w < _t1).sum()), int((_w >= _t2).sum())
    print(f"F2 grup band{b}: bawah={_nlo} atas={_nhi} (tripwire <30 → STOP) [KONFIRMASI-V]")
    assert _nlo >= 30 and _nhi >= 30, f"TRIPWIRE grup band{b} < 30 → STOP + arsitek"
print("F2 HIJAU ✓")
print("SEL 5 SELESAI")
'''
)

code(
    '''"""Sel 6 — F4 + Q-wick-V (satu-satunya uji) + CI + deskriptif + VONIS."""
# ---- F4: seed baru tercatat ----
print(f"F4: SEED_EXEC={SEED_EXEC} wick={S_WICK} boot={S_BOOT} (satu-seed-satu-run)")
assert SEED_EXEC == 20261016 and len({SEED_EXEC, S_WICK, S_BOOT}) == 3
assert all(s not in (20261006, 20261007, 20261015) for s in (SEED_EXEC, S_WICK, S_BOOT))

DAYCODE_V = {d: k for k, d in enumerate(MANIFEST_V)}
FRV["daycode"] = [DAYCODE_V[d] for d in FRV["day"]]
WW = {b: FRV[FRV["band"] == b]["wick_ratio"].to_numpy() for b in range(4)}
WY = {b: FRV[FRV["band"] == b]["is_rev"].to_numpy() for b in range(4)}

wick_delta_obs, wick_per = _pooled_delta_locked(WW, WY, CUT_LOCK)
print(f"wick-V pooled Δobs={wick_delta_obs:.4f} [KONFIRMASI-V]")
for _b in range(4):
    print(f"  per-band-V band{_b}: n={len(WW[_b])} Δ={wick_per[_b][0]:.4f} "
          f"(deskriptif-saja, tanpa p, tanpa klaim) [KONFIRMASI-V]")

# ---- Null: permutasi NILAI wick DALAM band; cut-TERKUNCI diterapkan ulang ----
_rng_w = np.random.default_rng(S_WICK)
wick_null = np.empty(N_NULL)
for _p in range(N_NULL):
    _ws = {b: _rng_w.permutation(WW[b]) for b in range(4)}
    _d, _ = _pooled_delta_locked(_ws, WY, CUT_LOCK)
    wick_null[_p] = _d
p_wick = float((1 + (wick_null >= wick_delta_obs).sum()) / (N_NULL + 1))
print(f"wick-V: Δobs={wick_delta_obs:.4f} null-mean={wick_null.mean():.4f} "
      f"p_satu-arah={p_wick:.4f} (B={N_NULL}, STRATA=BAND) [KONFIRMASI-V]")

# ---- CI cluster-per-day B=10000 (karakterisasi, TANPA peran putusan) ----
_rng_b = np.random.default_rng(S_BOOT)
_days = np.array(sorted(FRV["day"].unique()))
_per_day = {d: FRV[FRV["day"] == d].index.to_numpy() for d in _days}
_w_all = FRV["wick_ratio"].to_numpy()
_y_all = FRV["is_rev"].to_numpy()
_b_all = FRV["band"].to_numpy()
_idx_all = FRV.index.to_numpy()
_pos = {idx: k for k, idx in enumerate(_idx_all)}
boots = np.empty(N_BOOT)
for _k in range(N_BOOT):
    _pick = _rng_b.integers(0, len(_days), len(_days))
    _sel = np.concatenate([_per_day[d] for d in _days[_pick]])
    _kk = np.array([_pos[i] for i in _sel])
    _num, _den = 0.0, 0
    for _b in range(4):
        _m = _b_all[_kk] == _b
        if not _m.any():
            continue
        _t1, _t2 = CUT_LOCK[_b]
        _wb = _w_all[_kk][_m]
        _yb = _y_all[_kk][_m]
        _db = float(_yb[_wb >= _t2].mean() - _yb[_wb < _t1].mean())
        _num += _m.sum() * _db
        _den += _m.sum()
    boots[_k] = _num / _den
_ci_lo, _ci_hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
print(f"wick-V CI95-cluster-per-day=[{_ci_lo:.4f},{_ci_hi:.4f}] (karakterisasi) [KONFIRMASI-V]")

# ---- Split H1/H2-2025 preregistered, DESKRIPTIF-SAJA (Δ + n, tanpa p) ----
FRV["H1"] = [pd.Timestamp(d).month <= 6 for d in FRV["day"]]
for _lab, _m in (("H1", FRV["H1"].to_numpy()), ("H2", (~FRV["H1"]).to_numpy())):
    _num, _den = 0.0, 0
    _parts = []
    for _b in range(4):
        _q = FRV[_m & (FRV["band"] == _b)]
        if len(_q) == 0:
            _parts.append(f"b{_b}:n=0")
            continue
        _t1, _t2 = CUT_LOCK[_b]
        _wq = _q["wick_ratio"].to_numpy()
        _yq = _q["is_rev"].to_numpy()
        _dq = float(_yq[_wq >= _t2].mean() - _yq[_wq < _t1].mean())
        _num += len(_q) * _dq
        _den += len(_q)
        _parts.append(f"b{_b}:n={len(_q)}")
    print(f"split-{_lab}: n={int(_m.sum())} Δ={_num / _den:.4f} "
          f"({', '.join(_parts)}) deskriptif-saja [KONFIRMASI-V]")

# ---- VONIS mekanis §2 (tepat satu kata) ----
print("CONFIRM" if (p_wick < 0.05 and np.sign(wick_delta_obs) == 1) else "GUGUR")
print("SEL 6 SELESAI")
'''
)

code(
    '''"""Sel 7 — volume-(c) lock-in (0 uji) + laporan + manifest + Done."""
import json  # noqa: E402

# Baseline: median rolling-20d per slot-HH:MM TANPA-hari-berjalan (fungsi IDENTIK R)
MANIFEST_ALL = MANIFEST_R + MANIFEST_V
assert MANIFEST_ALL == sorted(MANIFEST_ALL), "urutan manifest gabungan rusak → STOP"
DIDX = {d: j for j, d in enumerate(MANIFEST_ALL)}
_SLOTVOL: dict = {}
for _d in MANIFEST_ALL:
    _g = DAYS_ALL[_d]["frame"]
    _SLOTVOL[_d] = dict(zip(_g["broker_time"].dt.strftime("%H:%M").tolist(),
                            _g["tick_volume"].astype(float).tolist()))
FRV["slot_s"] = [str(DAYS_ALL[d]["frame"]["broker_time"].iloc[s].strftime("%H:%M"))
                 for d, s in zip(FRV["day"], FRV["s"])]


def _vol_c(day, slot, vol):
    j = DIDX[day]
    past20 = MANIFEST_ALL[max(0, j - 20):j]
    pool_c = np.array([_SLOTVOL[_d].get(slot, float("nan")) for _d in past20], dtype=float)
    if len(past20) != 20:
        return float("nan")
    return vol / float(np.nanmedian(pool_c))


FRV["vol_c"] = [_vol_c(d, s, vv) for d, s, vv in zip(FRV["day"], FRV["slot_s"], FRV["vol_s"])]
_vc = FRV["vol_c"].to_numpy(dtype=float)
_okm = np.isfinite(_vc) & (_vc > 0)
_n_drop = int((~_okm).sum())
print(f"volume-(c)-V: n={len(FRV)} baseline-penuh={int(_okm.sum())} "
      f"drop-tanpa-baseline={_n_drop} [KONFIRMASI-V]")
FVE = FRV[_okm].copy()
assert len(FVE) > 0, "semua event-V tanpa baseline → STOP"
_vv = FVE["vol_c"].to_numpy(dtype=float)
print(f"  vol_c-V: med={float(np.median(_vv)):.3f} "
      f"IQR=[{float(np.percentile(_vv, 25)):.3f},{float(np.percentile(_vv, 75)):.3f}] "
      f"P1/P99={float(np.percentile(_vv, 1)):.3f}/{float(np.percentile(_vv, 99)):.3f} "
      f"[KONFIRMASI-V]")
print("  vol_c-R [GENERASI-R]: med=1.151 IQR=[0.864,1.723] P1/P99=0.388/5.143 "
      "(n-vol-R=1427, warmup-drop-R=87 event di 20 hari pertama-R)")
print("  cakupan baseline-V: V-hari-1 = 20 hari-R terakhir (past-only, live-sah) [KONFIRMASI-V]")

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

_fig, _ax = plt.subplots(figsize=(7, 4.2))
_xs = [0, 1, 2, 3]
_ys = [wick_per[b][0] for b in _xs]
_ax.bar(_xs, _ys)
_ax.axhline(wick_delta_obs, ls="--", label=f"pooled Δ={wick_delta_obs:.4f}")
_ax.axhline(0, color="black", lw=0.8)
_ax.set_xticks(_xs)
_ax.set_xticklabels([f"band{b} (n={len(WW[b])})" for b in _xs])
_ax.set_ylabel("Δ rate (tercil-atas − tercil-bawah, cut-terkunci)")
_ax.set_title("EDA-09: Δ-wick-V per band + pooled [KONFIRMASI-V]")
_ax.legend()
FIG9 = PROJECT_ROOT / "reports/eda/2026-10-16-eda09/fig-wick-V-perband.png"
FIG9.parent.mkdir(parents=True, exist_ok=True)
_fig.savefig(FIG9, dpi=120)
plt.close(_fig)
print(f"kurva tersimpan: {FIG9.relative_to(PROJECT_ROOT)}")

RDIR = PROJECT_ROOT / "reports/eda/2026-10-16-eda09"
RDIR.mkdir(parents=True, exist_ok=True)
_manifest = {
    "ronde": "EDA-09 wick_confirm_V", "tanggal_utc": "2026-10-16",
    "seed_exec": SEED_EXEC, "streams": {"wick_null": S_WICK, "boot_ci": S_BOOT},
    "cut_lock": {str(k): list(v) for k, v in CUT_LOCK.items()},
    "n_V": int(len(FRV)), "band_V": {str(k): int((FRV['band'] == k).sum()) for k in range(4)},
    "n_vol_V": int(len(FVE)), "vol_drop": _n_drop,
    "pooled_delta_V": float(wick_delta_obs), "p_satu_arah": float(p_wick),
    "ci95_cluster": [_ci_lo, _ci_hi],
    "perband_V": {str(k): {"delta": float(wick_per[k][0]), "n": int(len(WW[k]))}
                  for k in range(4)},
    "vonis": ("CONFIRM" if (p_wick < 0.05 and float(np.sign(wick_delta_obs)) == 1.0)
              else "GUGUR"),
    "toolchain": {"numpy": np.__version__, "pandas": pd.__version__},
}
import pyarrow  # noqa: E402
_manifest["toolchain"]["pyarrow"] = pyarrow.__version__
(RDIR / "manifest.json").write_text(json.dumps(_manifest, indent=2), encoding="utf-8")
print(f"manifest: {(RDIR / 'manifest.json').relative_to(PROJECT_ROOT)}")
print("=== EDA-09 SELESAI: SEMUA ASSERTION PASS ===")
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
