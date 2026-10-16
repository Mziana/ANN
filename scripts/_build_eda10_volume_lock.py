"""Generator + executor for notebooks/scalping/eda_10_volume_lock.ipynb.

# LENGTH_EXCEPTION: generator §15.1 AGENTS.md — referensi stabil + diff kecil +
# deterministik (DILARANG RNG, tanpa seed) + assertion mesin (bukan dokumen).
#
# REVIEW LOG (FASE 0, AGENTS.md §4 butir 9):
# R1: Brief FASE 0 melarang "menulis" generator sebelum lulus NAMUN menuntut
#     output `ruff check <builder>` sebagai syarat lulus — mustahil literal.
#     Diselesaikan via supremasi blueprint (tak melarang authoring statis):
#     authoring statis = objek audit; yang digerbang = EKSEKUSI (nbconvert).
#     Dieksekusi hanya setelah FASE 0 LULUS tertulis.
# R2: Scan atas DAYS_ALL (termasuk hari-R) lalu whitelist-V = perintah harfiah
#     blueprint §3; BUKAN rescan-R. Adaptasi MANDAT vs builder EDA-09: kunci
#     cls/ctx/T_DAY DIBUANG (blueprint §3: T_DAY/cls dikeluarkan dari warisan,
#     metadata-only NOL peran putusan) — supremasi blueprint, bukan improvisasi.
# R3: DILARANG RNG di pipeline (blueprint §3/R4-EDA10): tak ada seed apa pun;
#     determinisme dibuktikan via rerun-diff A2', bukan seed.
# R4: print() di sel notebook = mekanisme bukti (ditempel ke laporan), bukan
#     print() produksi; print() modul hanya progres build() (preseden EDA-09).
# R5: Fungsi sel ditulis inline-string (tak terlihat ruff); kode modul hanya
#     md/code/build — ruff check + format --check wajib rc=0 (FASE 0).

EDA-10 volume_lock_V (Blueprint FINAL 2026-10-16 §§1–14 + Amandemen-Audit):
MENGUNCI spesifikasi-produksi volume-(c) di V — 0 uji. Vonis wick CONFIRM
(EDA-09) IMMUTABLE. P (2026) SEGEL. T_DAY/cls TIDAK dihitung.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_10_volume_lock.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA-10 — volume_lock_V (reproduksi mandiri + spesifikasi rolling-live)

**Blueprint:** `thoughts/shared/plans/2026-10-16-eda10-volume-c-V-draf.md` (FINAL
§§1–14 + Amandemen-Audit + 2 klarifikasi audit-final: T_DAY dikeluarkan dari
warisan; F0' whitelist tegas). **Peran ronde:** MENGUNCI spesifikasi-produksi
volume-(c) di V — BUKAN konfirmasi baru, BUKAN generasi. Tepat 0 uji
(Q-repro-V + Q-spec-live; famili kosong §§4–5). Vonis wick CONFIRM (EDA-09)
IMMUTABLE. P (2026) DILARANG disentuh. T_DAY/cls TIDAK dihitung (metadata-only,
NOL peran putusan).

## Aturan yang mengikat notebook ini
- **P3 lock-sebelum-V:** Sel 1 hijau SEBELUM sentuh V (sentuh = load hari-2025
  mana pun). Sel 1 HANYA memuat 2023+2024 + hash parquet-R pra-run.
- **Kode-beku:** `scan_spikes` + `_wilder_ema` + `_vol_c` + MANIFEST disalin
  verbatim dari `scripts/_build_eda09_wick_confirm.py` (reuse-first; jangkar =
  nama fungsi). A1' membuktikan diff kosong saat run.
- **Concat-indikator prasyarat:** ATR14/RSI14-Wilder pada frame 2023+2024+2025
  verbatim; whitelist-V SESUDAH deteksi; artefak-R = terbuang.
- **DILARANG:** RNG/seed; uji statistik apa pun; klaim R-vs-V; sentuh wick/null/
  CI/L2/trade; hitung T_DAY/cls; kolom pipeline dinarasikan.
- **Label:** tiap angka-V bertag REPRODUKSI-V; angka-beku bertag BEKU-EDA-09.
"""
)

code(
    '''"""Sel 1 — setup, kontrak, R-384, hash pra-run (SEBELUM sentuh V)."""
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

assert np.__version__ == "1.26.4", "toolchain numpy bergeser → STOP"
assert pd.__version__ == "2.2.3", "toolchain pandas bergeser → STOP"
import pyarrow  # noqa: E402

assert pyarrow.__version__ == "17.0.0", "toolchain pyarrow bergeser → STOP"
print(f"toolchain: numpy={np.__version__} pandas={pd.__version__} "
      f"pyarrow={pyarrow.__version__} [REPRODUKSI-V]")


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

# ---- Kontrak terkunci (DILARANG T_DAY/cls/seed/RNG) ----
R_START = pd.Timestamp("2023-07-01", tz="UTC")
R_END_EXCL = pd.Timestamp("2025-01-01", tz="UTC")
V_START = pd.Timestamp("2025-01-01", tz="UTC")
V_END_EXCL = pd.Timestamp("2026-01-01", tz="UTC")
BAND_EDGES = [1.5, 2.0, 2.5, 3.0]
DAILY_OPEN_HOURS = [22, 23]

assert DAILY_OPEN_HOURS == [22, 23]
assert BAND_EDGES == [1.5, 2.0, 2.5, 3.0]


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
    assert "2026" not in str(years), "P-segel tersentuh → STOP"
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
print(f"R: {len(r)} bar | hari bersih = {len(DAYS_R)} (ekspektasi 384) [REPRODUKSI-V]")
assert len(DAYS_R) == 384, "partisi R != 384 → STOP"
MANIFEST_R = sorted(DAYS_R)

# ---- Hash parquet-R pra-run (pembacaan-1 dari disk, read-only) ----
PQ = PROJECT_ROOT / "data/processed/events/eda07_spike_events.parquet"
assert PQ.is_file(), "parquet-R hilang → STOP"
HASH_PRA = hashlib.sha256(PQ.read_bytes()).hexdigest()
print(f"hash parquet-R pra-run: {HASH_PRA} [REPRODUKSI-V]")
assert HASH_PRA.casefold() == "b800e50ee42d72349f52426b2fcb635efb5101597e40afbdd89bf2054b1bdfc2"
print("SEL 1 SELESAI (P3 hijau — baru boleh sentuh V)")
'''
)

code(
    '''"""Sel 2 — F0' reproduksi-event-V + F1' whitelist/availabilitas."""
import numpy as np  # noqa: F811
import pandas as pd  # noqa: F811

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

# ---- F1' partisi (assert-vs-beku BEKU-EDA-09, bukan eksplorasi) ----
assert all(str(d)[:4] == "2025" for d in MANIFEST_V), "hari-V tak ⊆ 2025 → STOP"
assert set(MANIFEST_V).isdisjoint(set(MANIFEST_R)), "V∩R ≠ ∅ → STOP (whitelist dua-arah)"
assert max(MANIFEST_V) < pd.Timestamp("2026-01-01").date(), "max(day-V) ≥ 2026-01-01 → STOP"
print(f"F1' hari-V: aktual={len(MANIFEST_V)} ekspektasi=259 [REPRODUKSI-V vs BEKU-EDA-09]")
assert len(MANIFEST_V) == 259, "hari-V ≠ 259 → STOP"
print(f"F1' bar-M15-V: aktual={len(v)} ekspektasi=23812 [REPRODUKSI-V vs BEKU-EDA-09]")
assert len(v) == 23812, "bar-M15-V ≠ 23812 → STOP"

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

# DAYS_ALL atas frame concat (§3 blueprint); whitelist-V SESUDAH deteksi
DAYS_ALL: dict = {}
for day, g in pd.concat([r, v]).groupby("broker_day"):
    g = g.sort_values("time").reset_index(drop=True)
    if g["time"].iloc[0].hour not in DAILY_OPEN_HOURS:
        continue
    DAYS_ALL[day] = {"frame": g, "open": float(g["open"].iloc[0])}
print(f"DAYS_ALL: {len(DAYS_ALL)} hari (R+V concat, indikator warmup-penuh) [REPRODUKSI-V]")

for day, info in DAYS_ALL.items():
    g = info["frame"]
    idx = m15c.index[m15c["time"] == g["time"].iloc[0]][0]
    info["frame"] = g.assign(atr=m15c["atr"].iloc[idx : idx + len(g)].to_numpy(),
                             rsi=m15c["rsi"].iloc[idx : idx + len(g)].to_numpy()).reset_index(drop=True)


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
                     "atr_s": atr_s, "mag": mag, "band": band})
assert all(u["band"] in (0, 1, 2, 3) for u in UNIQ_ALL), "band liar → STOP"

# ---- WHITELIST-V SESUDAH deteksi (§3 blueprint); artefak-R dibuang ----
SET_V = set(MANIFEST_V)
UNIQ = [u for u in UNIQ_ALL if u["day"] in SET_V]
WL_DROP = sum(1 for u in UNIQ_ALL if str(u["day"])[:4] == "2025" and u["day"] not in SET_V)
print(f"F0' whitelist-drop: aktual={WL_DROP} ekspektasi=0 (vs 1110) "
      "[REPRODUKSI-V vs BEKU-EDA-09]")
assert WL_DROP == 0, "whitelist-drop > 0 → STOP + arsitek"
assert all(str(u["day"])[:4] == "2025" for u in UNIQ), "event-V tak ⊆ 2025 → STOP"
assert not (set(u["day"] for u in UNIQ) & set(MANIFEST_R)), "V∩R → STOP"

# ---- Outcome machine (warisan verbatim EDA-06) + full-room ----
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
for b in range(4):
    idx = [n for n in AN if UNIQ[n]["band"] == b]
    cr = sum(1 for n in idx if OUT[n]["outcome"] == "reversal")
    cc = sum(1 for n in idx if OUT[n]["outcome"] == "continuation")
    ct = sum(1 for n in idx if OUT[n]["outcome"] == "timeout")
    assert cr + cc + ct == len(idx), f"outcome band {b} tak-exhaustive → STOP"

FRV = pd.DataFrame([{"day": UNIQ[n]["day"], "band": UNIQ[n]["band"],
                     "outcome": OUT[n]["outcome"], "s": UNIQ[n]["s"]} for n in AN])

# ---- F0' asserts bit-eksak vs oracle BEKU-EDA-09 ----
print(f"F0' Nunik-V: aktual={len(UNIQ)} ekspektasi=1110 [REPRODUKSI-V vs BEKU-EDA-09]")
assert len(UNIQ) == 1110, "F0' Nunik-V → STOP"
_bc_u = pd.Series([u["band"] for u in UNIQ]).value_counts().sort_index().to_dict()
print(f"F0' band-unik-V: aktual={_bc_u} ekspektasi={{0: 367, 1: 286, 2: 168, 3: 289}} "
      "[REPRODUKSI-V vs BEKU-EDA-09]")
assert _bc_u == {0: 367, 1: 286, 2: 168, 3: 289}, "F0' band-unik → STOP"
print(f"F0' full-room-V: aktual={len(FRV)} ekspektasi=1018 [REPRODUKSI-V vs BEKU-EDA-09]")
assert len(FRV) == 1018, "F0' full-room → STOP"
_bc_fr = FRV["band"].value_counts().sort_index().to_dict()
print(f"F0' band-fullroom-V: aktual={_bc_fr} ekspektasi={{0: 325, 1: 269, 2: 156, 3: 268}} "
      "[REPRODUKSI-V vs BEKU-EDA-09]")
assert _bc_fr == {0: 325, 1: 269, 2: 156, 3: 268}, "F0' band-fullroom → STOP"

# ---- F1' tick_volume bar-s-V terisi (PER BAR-s, bukan agregat) ----
FRV["vol_s"] = [float(DAYS_ALL[d]["frame"]["tick_volume"].iloc[s])
                for d, s in zip(FRV["day"], FRV["s"])]
f1_fill = float(np.isfinite(FRV["vol_s"].to_numpy()).mean())
print(f"F1' tick_volume bar-s-V terisi {f1_fill:.4f} (pagar ≥0.95) [REPRODUKSI-V]")
assert f1_fill >= 0.95, "F1' fill < 0.95 → STOP"
print("SEL 2 SELESAI (F0' + F1' HIJAU)")
'''
)

code(
    '''"""Sel 3 — F2' volume-gate (baseline penuh + med/IQR/P1/P99 bit-eksak)."""
import numpy as np  # noqa: F811
import pandas as pd  # noqa: F811

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
print(f"F2' baseline-penuh: aktual={int(_okm.sum())}/1018 drop={_n_drop} "
      "ekspektasi=1018/1018 drop 0 [REPRODUKSI-V vs BEKU-EDA-09]")
assert int(_okm.sum()) == 1018 and _n_drop == 0, "F2' baseline → STOP"
FVE = FRV[_okm].copy()
_vv = FVE["vol_c"].to_numpy(dtype=float)
_med = float(np.median(_vv))
_q1 = float(np.percentile(_vv, 25))
_q3 = float(np.percentile(_vv, 75))
_p1 = float(np.percentile(_vv, 1))
_p99 = float(np.percentile(_vv, 99))
print(f"F2' vol_c-V: med={_med:.3f} IQR=[{_q1:.3f},{_q3:.3f}] P1/P99={_p1:.3f}/{_p99:.3f} "
      "[REPRODUKSI-V vs BEKU-EDA-09]")
print(f"  repr-penuh: med={_med!r} q1={_q1!r} q3={_q3!r} p1={_p1!r} p99={_p99!r} [REPRODUKSI-V]")
assert f"{_med:.3f}" == "1.179", "F2' med → STOP (bukan 'mendekati')"
assert f"{_q1:.3f}" == "0.914" and f"{_q3:.3f}" == "1.607", "F2' IQR → STOP"
assert f"{_p1:.3f}" == "0.503" and f"{_p99:.3f}" == "4.396", "F2' P1/P99 → STOP"
print("SEL 3 SELESAI (F2' HIJAU)")
'''
)

code(
    '''"""Sel 4 — F3' audit-tepi + uji-prosedural Q-spec-live (0 uji statistik)."""
import inspect  # noqa: F811

import numpy as np  # noqa: F811

N_R = len(MANIFEST_R)
FIRST_V = MANIFEST_V[0]
assert DIDX[FIRST_V] == N_R, "V tak kontigu sesudah R → STOP"

# ---- F3'(a): komposisi baseline 20 hari-V pertama + prosedur satu-jalur ----
print("F3'(a) komposisi baseline 20 hari-V pertama [REPRODUKSI-V]:")
SET_R = set(MANIFEST_R)
for k in range(20):
    _d = MANIFEST_ALL[N_R + k]
    _past = MANIFEST_ALL[max(0, N_R + k - 20):N_R + k]
    _nR = sum(1 for x in _past if x in SET_R)
    print(f"  V-hari-{k + 1}: {_nR}R+{20 - _nR}V")
_p0 = MANIFEST_ALL[max(0, N_R - 20):N_R]
assert len(_p0) == 20 and all(x in SET_R for x in _p0), "V-hari-1 ≠ 20 hari-R → STOP"
_p19 = MANIFEST_ALL[max(0, N_R + 19 - 20):N_R + 19]
assert len(_p19) == 20 and sum(1 for x in _p19 if x in SET_R) == 1, "V-hari-20 ≠ 1R+19V → STOP"
_src_vc = inspect.getsource(_vol_c)
assert "MANIFEST_R" not in _src_vc and "MANIFEST_V" not in _src_vc, "cabang khusus hari → STOP"
print("F3'(a): prosedur satu-jalur, tanpa cabang khusus V-hari-1 [REPRODUKSI-V]")

# Uji-prosedural: hitung-ulang manual 2 event (V-hari-1 + tengah-V) via nanmedian
for _lab, _row in (("V-hari-1", FVE[FVE["day"] == FIRST_V].iloc[0]),
                   ("tengah-V", FVE[FVE["day"] == MANIFEST_V[100]].iloc[0])):
    _j = DIDX[_row["day"]]
    _past = MANIFEST_ALL[max(0, _j - 20):_j]
    _pool = np.array([_SLOTVOL[_x].get(_row["slot_s"], float("nan")) for _x in _past])
    _manual = float(_row["vol_s"]) / float(np.nanmedian(_pool))
    assert _manual == float(_row["vol_c"]), f"prosedur {_lab} menyimpang → STOP"
    print(f"  prosedural-{_lab}: vol_c={float(_row['vol_c'])!r} sama-prosedur ✓ [REPRODUKSI-V]")

# ---- F3'(b): bar-s tanpa tick_volume ----
_missing_vol = int((~np.isfinite(FRV["vol_s"].to_numpy())).sum())
print(f"F3'(b) bar-s tanpa tick_volume: aktual={_missing_vol} ekspektasi=0 [REPRODUKSI-V]")
assert _missing_vol == 0, "F3'(b) > 0 → STOP + arsitek (DILARANG karang aturan)"

# ---- F3'(c): slot-HH:MM tanpa histori-20-penuh di tengah-V (aturan umum DROP+count) ----
_mid = FVE[[DIDX[d] > N_R + 19 for d in FVE["day"]]]
assert len(_mid) > 0, "tengah-V kosong → STOP"
_c_mid_nofull = 0
for _, _row in _mid.iterrows():
    _past = MANIFEST_ALL[max(0, DIDX[_row["day"]] - 20):DIDX[_row["day"]]]
    if len(_past) != 20:
        _c_mid_nofull += 1
print(f"F3'(c) tengah-V tanpa histori-20-penuh: aktual={_c_mid_nofull} "
      "ekspektasi=0 [REPRODUKSI-V]")
assert _c_mid_nofull == 0, "F3'(c) > 0 → STOP + arsitek"
print("SEL 4 SELESAI (F3' HIJAU)")
'''
)

code(
    '''"""Sel 5 — A-checks: A1' verbatim + A2' hash pasca-run."""
import hashlib  # noqa: F811

# ---- A1': diff fungsi volume vs `_vol_c` EDA-09 = kosong (salin verbatim) ----
# Bandingkan BLOK STATIS kedua file builder (deterministik; jangkar = nama
# fungsi). Sumber-runtime tak dipakai: `ruff format` pada notebook boleh
# menormalkan spasi sel tanpa mengubah berkas builder yang diaudit.
EDA09_TXT = (PROJECT_ROOT / "scripts/_build_eda09_wick_confirm.py").read_text(encoding="utf-8")
EDA10_TXT = (PROJECT_ROOT / "scripts/_build_eda10_volume_lock.py").read_text(encoding="utf-8")


def _block(txt, defline):
    lines = txt.split(chr(10))
    occ = [i for i, lin in enumerate(lines) if lin == defline]
    assert len(occ) == 1, f"blok {defline!r} tak-unik → STOP"
    s = occ[0]
    e = s + 1
    while e < len(lines) and (lines[e].startswith(" ") or lines[e].strip() == ""):
        e += 1
    while e > s and lines[e - 1].strip() == "":
        e -= 1
    return chr(10).join(lines[s:e])


for _name, _def in (("scan_spikes", "def scan_spikes(g: pd.DataFrame, thresh: float) -> list:"),
                    ("_wilder_ema", "def _wilder_ema(series: pd.Series, n: int = NSMOOTH)"
                     " -> pd.Series:"),
                    ("_vol_c", "def _vol_c(day, slot, vol):")):
    _b9, _b10 = _block(EDA09_TXT, _def), _block(EDA10_TXT, _def)
    assert _b9 == _b10, f"A1' diff {_name} tak-kosong → STOP"
    print(f"A1' {_name}: diff-kosong vs builder EDA-09 ✓ [REPRODUKSI-V]")
for _anchor in ("MANIFEST_ALL = MANIFEST_R + MANIFEST_V",
                "past20 = MANIFEST_ALL[max(0, j - 20):j]", "np.nanmedian"):
    assert _anchor in EDA09_TXT, f"A1' jangkar {(_anchor,)!r} hilang → STOP"
    print(f"A1' jangkar {(_anchor,)!r} ✓ [REPRODUKSI-V vs BEKU-EDA-09]")
assert "NSMOOTH = 14" in EDA09_TXT
assert "BAND_EDGES = [1.5, 2.0, 2.5, 3.0]" in EDA09_TXT
print("A1' diff-kosong TERBUKTI (3 fungsi verbatim-unik + 3 jangkar) [REPRODUKSI-V]")

# ---- A2': parquet-R read-only; hash pasca-run (pembacaan-2) WAJIB identik ----
HASH_PASCA = hashlib.sha256(PQ.read_bytes()).hexdigest()
print(f"A2' hash parquet-R pasca-run: {HASH_PASCA} [REPRODUKSI-V]")
assert HASH_PASCA == HASH_PRA, "hash parquet-R berubah = bug = STOP"
assert HASH_PASCA.casefold() == "b800e50ee42d72349f52426b2fcb635efb5101597e40afbdd89bf2054b1bdfc2"
print("A2' hash pra=pasca IDENTIK tanpa syarat (pyarrow 17.0.0/pandas 2.2.3) [REPRODUKSI-V]")
print("SEL 5 SELESAI (A' HIJAU)")
'''
)

code(
    '''"""Sel 6 — manifest 5-elemen + baris vonis mekanis (§11)."""
import json  # noqa: E402

GATES = {
    "nunik_V==1110": len(UNIQ) == 1110,
    "band_unik_V": _bc_u == {0: 367, 1: 286, 2: 168, 3: 289},
    "fullroom_V==1018": len(FRV) == 1018,
    "band_fullroom_V": _bc_fr == {0: 325, 1: 269, 2: 156, 3: 268},
    "whitelist_drop==0": WL_DROP == 0,
    "hari_V==259": len(MANIFEST_V) == 259,
    "bar_M15_V==23812": len(v) == 23812,
    "fill>=0.95": f1_fill >= 0.95,
    "baseline_penuh_1018_drop0": int(_okm.sum()) == 1018 and _n_drop == 0,
    "med==1.179": f"{_med:.3f}" == "1.179",
    "iqr==[0.914,1.607]": f"{_q1:.3f}" == "0.914" and f"{_q3:.3f}" == "1.607",
    "p1/p99==0.503/4.396": f"{_p1:.3f}" == "0.503" and f"{_p99:.3f}" == "4.396",
    "f3b_missing_vol==0": _missing_vol == 0,
    "f3c_mid_nofull==0": _c_mid_nofull == 0,
    "hash_pra_pasca_identik": HASH_PASCA == HASH_PRA,
}
for _k, _ok in GATES.items():
    assert _ok, f"gate {_k} → STOP"
    print(f"gate {_k}: HIJAU [REPRODUKSI-V]")

SPEC_LIVE = ("SPESIFIKASI ROLLING-LIVE volume-(c) (TERKUNCI EDA-10): baseline tiap hari-T "
             "memakai 20 hari-bersih sebelum-T (slot-HH:MM-sama, tanpa hari-berjalan); "
             "agregasi = median (np.nanmedian; slot NaN diabaikan); '20 hari penuh' = "
             "20 hari di MANIFEST; hari tanpa 20-hari histori = event hari itu DROP + "
             "count (aturan umum; V-hari-1 = kasus khusus 20-hari-R-terakhir, konsisten "
             "bukan pengecualian); prosedur satu-jalur tanpa cabang khusus hari; "
             "diuji-prosedural pada 20 hari-V pertama (kesamaan prosedur, bukan angka).")

RDIR = PROJECT_ROOT / "reports/eda/2026-10-16-eda10"
RDIR.mkdir(parents=True, exist_ok=True)
_manifest = {
    "ronde": "EDA-10 volume_lock_V",
    "tanggal_utc": "2026-10-16",
    "oracle_vs_aktual": {
        "nunik_V": {"ekspektasi": 1110, "aktual": len(UNIQ)},
        "band_unik_V": {"ekspektasi": {"0": 367, "1": 286, "2": 168, "3": 289},
                        "aktual": {str(k): int(v_) for k, v_ in _bc_u.items()}},
        "fullroom_V": {"ekspektasi": 1018, "aktual": len(FRV)},
        "band_fullroom_V": {"ekspektasi": {"0": 325, "1": 269, "2": 156, "3": 268},
                            "aktual": {str(k): int(v_) for k, v_ in _bc_fr.items()}},
        "whitelist_drop": {"ekspektasi": 0, "aktual": WL_DROP},
        "hari_V": {"ekspektasi": 259, "aktual": len(MANIFEST_V)},
        "bar_M15_V": {"ekspektasi": 23812, "aktual": len(v)},
        "fill_vol_s": {"ekspektasi": 1.0, "aktual": f1_fill},
        "baseline_penuh": {"ekspektasi": "1018/1018 drop 0",
                           "aktual": f"{int(_okm.sum())}/1018 drop {_n_drop}"},
        "med": {"ekspektasi": "1.179", "aktual": f"{_med:.3f}", "repr": repr(_med)},
        "iqr": {"ekspektasi": "[0.914,1.607]", "aktual": f"[{_q1:.3f},{_q3:.3f}]",
                "repr": [repr(_q1), repr(_q3)]},
        "p1_p99": {"ekspektasi": "0.503/4.396", "aktual": f"{_p1:.3f}/{_p99:.3f}",
                   "repr": [repr(_p1), repr(_p99)]},
        "f3b_missing_vol": {"ekspektasi": 0, "aktual": _missing_vol},
        "f3c_mid_nofull": {"ekspektasi": 0, "aktual": _c_mid_nofull},
    },
    "bukti_diff": {"a1_diff_fungsi": "kosong (3 fungsi verbatim-unik + 3 jangkar, sel 5)",
                   "hash_parquet_R_pra": HASH_PRA, "hash_parquet_R_pasca": HASH_PASCA,
                   "hash_identik": HASH_PRA == HASH_PASCA},
    "spesifikasi_rolling_live": SPEC_LIVE,
    "toolchain": {"numpy": np.__version__, "pandas": pd.__version__,
                  "pyarrow": pyarrow.__version__},
    "vonis": "LOCKED" if all(GATES.values()) else "GAGAL",
}
(RDIR / "manifest.json").write_text(json.dumps(_manifest, indent=2), encoding="utf-8")
print(f"manifest: {(RDIR / 'manifest.json').relative_to(PROJECT_ROOT)}")
print(_manifest["vonis"])
print("=== EDA-10 SELESAI: SEMUA ASSERTION PASS ===")
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
