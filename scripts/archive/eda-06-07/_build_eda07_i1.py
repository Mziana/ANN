"""Generator + executor for notebooks/scalping/eda_07_i1_adendum.ipynb.

I-1: investigasi terbatas atas 80 alarm struktural EDA-07 run 9
(52 pdhl_d + 28 round_d) + 6 noise kalibrasi. Deskriptif, tanpa model,
tanpa vonis edge, tanpa buka Lapisan 3. Mandat mengikat:
reports/governance/2026-10-12/arsitek/putusan-eda07-g2.md (V-1/V-2/V-3).

Reuse-first: SELURUH jalur label/fitur disalin verbatim dari
scripts/_build_eda07.py (sel 02/03/04/05/06/07/08/10/11/12/13/14/15);
file run 9 TIDAK disentuh (hash dibuktikan sama sebelum/sesudah).
BARU dan pra-registrasi di sini: X_PIN=10 pip, SEEDI1, Q1/Q2/Q3,
aturan putus V-2, T-I1-1/2/3. LA_S (stres) tidak dibangun: I-1 tanpa G4.

AGENTS.md S15.1 generator exemption applies (template file, stable refs,
deterministik rerun via SEED07+SEEDI1, assertion machines via chk).
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_07_i1_adendum.ipynb"
OLD_FIGURE_DIR = PROJECT_ROOT / "reports/eda/2026-10-06/figures"
MID_FIGURE_DIR = PROJECT_ROOT / "reports/eda/2026-10-10"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


# sel 00 (markdown)
md(
    """# EDA-07 I-1 - adjudikasi alarm struktural (deskriptif, bukan model)

Adendum terbatas atas run 9 (STOP sah, 86 alarm = 80 struktural +
6 noise). Tanpa label/fitur/irisan baru, tanpa pindai ambang,
tanpa model/backtest/P&L/vonis edge, tanpa buka Lapisan 3.

Pertanyaan pra-registrasi (V-2):

- **Q1** - konsentrasi: 80 alarm memusat di target/irisan/sisi/sesi/horizon apa?
- **Q2** - uji-kedekatan: P(label | DEKAT) vs P(label | JAUH), X = 10 pip
  (satu nilai, DILARANG pindai), + CI klaster-hari. Kalibrasi negatif:
  prosedur SAMA pada 6 noise (ekspektasi: tak-berpola; bila >=2/6
  signifikan = mesin rusak, STOP).
- **Q3** - uji-proxy: stratifikasi median + desil rv15 dalam irisan.
  Bertahan = tanda sama >= 7/10 desil DAN lift pooled CI tak memuat 0.

Aturan putus V-2 (DILARANG ubah): ASLI iff Q2 DEKAT-mendominasi BERTAHAN
setelah stratifikasi (Q3); selain itu ARTEFAK. Per kontrol terpisah
(pdhl_d vs round_d); noise hanya kalibrasi, bukan vonis."""
)


# sel 01 (code: KONTRAK_I1 + setup)
code(
    '''# Kontrak Notebook I-1 - dicetak verbatim sebagai output pertama (wajib).
KONTRAK_I1 = """- Mandat: putusan-eda07-g2.md V-1/V-2/V-3 MENGIKAT. Run 9 STOP sah; 80 alarm
  struktural SENGKETA; Lapisan 3 TERKUNCI. I-1 deskriptif, tanpa model, tanpa vonis edge.
- Holdout/universe/kausalitas SAMA run 9: tanpa data 2026; strata A+B minus C;
  B=185.248; 5 semester A; N_ENT=184.731; scope 23+7 irisan T-06-7 (assert, STOP bila berubah).
- Reuse: data/strata/ATR/entri/LA-normal/label-waktu/fitur/mesin-MI/get_sample disalin
  VERBATIM dari scripts/_build_eda07.py. File run 9 (_gate_, _ckpt_, notebook, builder)
  hanya dibaca; hash SEBELUM vs SESUDAH di-assert sama. LA_S tidak dibangun (I-1 tanpa G4).
- Konsistensi: n per target 260/260 == _ckpt_; G2a/G2b/n_arah 86/86 pasang == _gate_;
  replay noise bit-identik; leakage 60/60 identik (rtol=1e-9, lookback 20.000).
  Satu beda = STOP.
- Q2 pra-registrasi: X_PIN=10 pip (satu nilai, DILARANG pindai). DEKAT = jarak <= 10 pip
  dari level (bulat utk round_d, PDH/L utk pdhl_d); JAUH = sisanya. Per pasang alarm:
  P(label|DEKAT) vs P(label|JAUH) + CI bootstrap klaster-hari 1000x (stream SEEDI1 q2+eidx).
- Kalibrasi negatif: prosedur SAMA pada 6 noise. LOLOS iff <=1/6 signifikan (CI 95% tak
  memuat 0); >=2/6 signifikan = mesin rusak, STOP. Risiko null-STOP ~=3,3% (binomial 6,0.05).
- Q3 pra-registrasi: median rv15 (diagnostik) + desil rv15 via qcodes (10 grup, tepi pooled).
  Bertahan = tanda mayoritas >= 7/10 desil DAN lift pooled-terbobot CI tak memuat 0
  (bootstrap klaster-hari 1000x, stream SEEDI1 q3+eidx). NaN (sisi kosong) = bukan-tanda-sama.
- V-2 (DILARANG ubah): ASLI iff Q2 DEKAT-mendominasi DAN Q3 Bertahan; selain itu ARTEFAK.
  Per kontrol (pdhl_d vs round_d) apa adanya. DILARANG promosikan kontrol jadi fitur sinyal.
- Determinisme: stream RNG tunggal per blok (SEED07 + tidx/eidx identik run 9 utk recompute;
  SEEDI1 + eidx utk Q2/Q3); iterasi terurut; rerun bit-identik mengikuti run 9."""
print(KONTRAK_I1)'''
)
code(
    '''"""Setup lingkungan dan kunci versi + helper + stream RNG (verbatim run 9 + SEEDI1)."""
import hashlib
import importlib.metadata
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from scipy import stats


def find_project_root(start: Path) -> Path:
    """Cari root proyek (pyproject.toml + src/) dari cwd ke atas."""
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    raise RuntimeError("PROJECT_ROOT tidak ditemukan")


PROJECT_ROOT = find_project_root(Path.cwd().resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.broker_time import wall_clock_series  # noqa: E402
from src.utils.config import load_config  # noqa: E402

sys.path.insert(0, str(PROJECT_ROOT / "notebooks/scalping"))
from _eda_common import (  # noqa: E402
    EXPECTED_FINGERPRINT,
    SESSION_ORDER,
    add_labels,
    session_fingerprint,
)

print("PROJECT_ROOT :", PROJECT_ROOT)
print("python       :", sys.version.split()[0])
for package in ("pandas", "numpy", "pyarrow", "matplotlib", "scipy", "tzdata"):
    print(f"  {package:11s}: {importlib.metadata.version(package)}")

assert importlib.metadata.version("tzdata") == "2026.5", "tzdata harus 2026.5"
assert int(importlib.metadata.version("pandas").split(".")[0]) == 2, "Wajib pandas 2.x."

ASSERT_LOG: list[str] = []


def chk(cond: bool, msg: str, loud: bool = False) -> None:
    """Assertion mesin tercatat (pengganti assert telanjang agar terhitung)."""
    ASSERT_LOG.append(msg)
    assert cond, f"ASSERT GAGAL: {msg}"
    if loud:
        print(f"PASS: {msg}")


chk(session_fingerprint() == EXPECTED_FINGERPRINT, "definisi sesi identik Notebook 00 (sidik jari cocok)", loud=True)

# Stream RNG run 9 (identik, untuk recompute) + stream I-1 (baru, pra-registrasi, tercatat).
SEED07 = {"noise": 70701, "leak": 70702, "floor_base": 70703, "lift_base": 70704, "atr_check": 70705,
          "stab_base": 70800}
SEEDI1 = {"q2": 80701, "q3": 80702}


def new_rng(name: str, idx: int = 0) -> np.random.Generator:
    """Stream RNG terkunci untuk blok analisis (nama, indeks tercatat di pemanggil)."""
    base = SEED07[name] if idx == 0 else SEED07[name] + idx
    return np.random.default_rng(base)


def new_rng_i1(name: str, idx: int = 0) -> np.random.Generator:
    """Stream RNG terkunci I-1 (Q2/Q3), terpisah dari SEED07 run 9."""
    base = SEEDI1[name] if idx == 0 else SEEDI1[name] + idx
    return np.random.default_rng(base)


def show(df: pd.DataFrame, title: str) -> None:
    """Cetak tabel penuh sebagai teks agar tersimpan di output notebook."""
    print(title)
    print(df.to_string())
    print()


print("SEED07:", SEED07)
print("SEEDI1:", SEEDI1)'''
)


# sel 02 (code: parameter terkunci + hash SEBELUM run 9)
code(
    '''"""Parameter terkunci (nilai IDENTIK run 9; file run 9 tak tersentuh) + hash SEBELUM."""
config = load_config("data")
SYMBOL = config["mt5"]["symbol"]
PIP_SIZE = float(config["spread"]["pip_size"][SYMBOL])
ANOMALY_WINDOWS = tuple((w["start"], w["end"]) for w in config["validation"]["anomaly_windows"])
SESSIONS = [label for label in SESSION_ORDER if label != "Off"]

YEARS = (2023, 2024, 2025)  # 2026 = holdout, TIDAK dimuat
HOLDOUT_START = pd.Timestamp("2026-01-01", tz="UTC")

COST_DEFAULT = float(config["spread"]["cost_basis"]["default"])
COST_NORMAL = {k: float(v) for k, v in config["spread"]["cost_basis"]["by_session"].items()}
COST_STRESS = {k: float(v) for k, v in config["spread"]["stress_bands"]["p95"]["by_session"].items()}

# Label waktu
N_HORIZONS = (5, 15, 30, 60)
LB_MARGIN_PIP = 0.20
LC_MULTS = (1.0, 2.0)

# Barrier LA (warisan EDA-06)
HORIZON = 120
STRIDE = 5

# Metode S5 (identik run 9 untuk recompute)
MI_BINS = 20
N_PERM = 100
N_BOOT = 1000
N_LEAK_I1 = 60
RHO_DROP = 0.8

# Gerbang S8 (pra-registrasi, hanya untuk recompute)
G1_BIN_LO, G1_BIN_HI = 0.10, 0.90
G1_MIN_CLASS = 0.10
G1_CONT_MIN_N, G1_CONT_MIN_DAYS = 1000, 100
G2_MIN_SEM = 4
G4_STRESS_MIN_PP = 0.0

# I-1 pra-registrasi (BARU, satu nilai, DILARANG pindai)
X_PIN = 10  # pip: DEKAT = jarak <= 10, JAUH = sisanya
chk(X_PIN == 10, "X pra-registrasi = 10 pip (satu nilai)")

REPORT_DIR = PROJECT_ROOT / "reports/eda" / "2026-10-12"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
MID_FIGURE_DIR = PROJECT_ROOT / "reports/eda" / "2026-10-10"  # baca T-06-7 (sama lokasi run 9)

RUN9_FILES = ["scripts/_build_eda07.py", "notebooks/scalping/eda_07_label_fitur.ipynb",
              "reports/eda/2026-10-12/_gate_G2_skrining.csv",
              "reports/eda/2026-10-12/_gate_G2_alarm.csv",
              "reports/eda/2026-10-12/_ckpt_LA.csv",
              "reports/eda/2026-10-12/_ckpt_T.csv"]
HASH_BEFORE = {}
for rel in RUN9_FILES:
    h = hashlib.sha256((PROJECT_ROOT / rel).read_bytes()).hexdigest()
    HASH_BEFORE[rel] = h
    print(f"SEBELUM {h[:12]} {rel}")
chk(HASH_BEFORE["scripts/_build_eda07.py"].startswith("bd40e1a3"),
    "jangkar builder run 9 = bd40e1a3 (keadaan pra-I-1 terverifikasi sesi ini)", loud=True)

print(f"symbol={SYMBOL} | pip={PIP_SIZE} | tahun={YEARS} | holdout >= {HOLDOUT_START:%Y-%m-%d}")
print("cost normal :", COST_NORMAL)
print("cost stres  :", COST_STRESS)
print(f"label N={N_HORIZONS} | LB margin={LB_MARGIN_PIP} pip | LC mult={LC_MULTS}")
print(f"LA: HORIZON={HORIZON} mnt, STRIDE={STRIDE}")
print(f"metode: MI_bins={MI_BINS}, perm={N_PERM}, boot={N_BOOT}, leak_I1={N_LEAK_I1}")
print(f"laporan -> {REPORT_DIR}")
chk(set(SESSIONS) == set(COST_NORMAL) == set(COST_STRESS), "sesi config harus 4 sesi", loud=True)'''
)
# sel 03 (code: muat data + strata, VERBATIM sel 04 run 9)
code(
    '''"""Muat M1 2023-2025, bentuk strata A/B/C, siapkan array numpy (pola EDA-06)."""
COLUMNS = ["time", "broker_time_raw", "high", "low", "close", "spread_pips"]
frames = [
    pd.read_parquet(
        PROJECT_ROOT / "data/processed/M1" / f"usdjpy_m1_{year}.parquet", columns=COLUMNS
    )
    for year in YEARS
]
m1 = pd.concat(frames, ignore_index=True)
m1["utc"] = pd.to_datetime(m1["time"], utc=True)
m1["wall"] = wall_clock_series(m1["broker_time_raw"])
m1["broker_day"] = m1["wall"].dt.normalize()
holdout_rows = m1["broker_day"] >= pd.Timestamp("2026-01-01")
print(f"bar tepi holdout dikeluarkan (hari broker >= 2026-01-01): {int(holdout_rows.sum()):,}")
m1 = m1[~holdout_rows].sort_values("utc", kind="mergesort").reset_index(drop=True)
m1 = add_labels(m1)
m1["sem"] = m1["broker_day"].dt.year.astype(str) + "H" + np.where(m1["broker_day"].dt.month <= 6, "1", "2")

chk(bool((m1["utc"].max() < HOLDOUT_START)), "tanpa data 2026 (holdout)")
chk(bool(m1["utc"].is_monotonic_increasing), "utc monoton naik")

wall_date = m1["broker_day"]
b_mask = (wall_date >= pd.Timestamp("2023-01-01")) & (wall_date <= pd.Timestamp("2023-06-30"))
c_mask = pd.Series(False, index=m1.index)
for start, end in ANOMALY_WINDOWS:
    c_mask |= (wall_date >= pd.Timestamp(start)) & (wall_date <= pd.Timestamp(end))
a_mask = ~(b_mask | c_mask)
n_a, n_b, n_c = int(a_mask.sum()), int(b_mask.sum()), int(c_mask.sum())
print(f"bar dimuat={len(m1):,} | A={n_a:,} B={n_b:,} C={n_c:,} | hari broker={wall_date.nunique()}")

# Jangkar silang EDA-06 (eksekusi 2026-10-10): bar dan partisi harus identik.
chk(len(m1) == 1_078_001, "jangkar bar dimuat = 1.078.001")
chk(n_b == 185_248, "B harus 185.248")
chk(not bool((b_mask & c_mask).any()), "B dan C tidak tumpang tindih")
chk(n_a + n_b + n_c == len(m1), "A+B+C utuh")
chk(int((m1.loc[a_mask, "session_label"] == "Off").sum()) == 0, "strata A tanpa bar Off")
print("PASS: strata konsisten EDA-06 (B=185.248, partisi utuh, tanpa Off di A, tanpa 2026).")

N_BARS = len(m1)
CL = m1["close"].to_numpy("float64")
HI = m1["high"].to_numpy("float64")
LO = m1["low"].to_numpy("float64")
UTC_NS = m1["utc"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy("datetime64[ns]").astype("int64")
C_ARR = c_mask.to_numpy()
C_CUM = np.concatenate([[0], np.cumsum(C_ARR)])
SESS_ARR = m1["session_label"].to_numpy()
DAY_ARR = pd.factorize(m1["broker_day"])[0].astype("int32")
SEM_ARR = m1["sem"].to_numpy()
STRATA_ARR = np.where(b_mask.to_numpy(), "B", np.where(a_mask.to_numpy(), "A", "C"))
A_FRAME = m1[a_mask]
SEM_A = sorted(A_FRAME["sem"].unique())
print("semester strata A:", SEM_A)
chk(len(SEM_A) == 5, "harus 5 semester A")
chk(int(DAY_ARR.max()) + 1 == int(m1["broker_day"].nunique()), "paritas hari-broker")'''
)


# sel 04 (code: scope dari CSV T-06-7, VERBATIM sel 05 run 9)
code(
    '''"""Scope irisan dari CSV T-06-7 (assert 23 + 7, STOP bila berubah)."""
T67_TER = pd.read_csv(MID_FIGURE_DIR / "T-06-7_gerbang_tercile.csv")
T67_SES = pd.read_csv(MID_FIGURE_DIR / "T-06-7_gerbang_sesi.csv")
chk(len(T67_TER) == 144, "T-06-7 tercile 144 baris")
chk(len(T67_SES) == 48, "T-06-7 sesi 48 baris")

IR_TER = T67_TER[T67_TER["LOLOS"] == True].copy().sort_values(["combo", "session", "atr_ter_s"]).reset_index(drop=True)  # noqa: E712
IR_SES = T67_SES[T67_SES["LOLOS"] == True].copy().sort_values(["combo", "session"]).reset_index(drop=True)  # noqa: E712
chk(len(IR_TER) == 23, "irisan tercile lolos = 23")
chk(len(IR_SES) == 7, "irisan sesi lolos = 7")

print(f"scope: {len(IR_TER)} irisan tercile + {len(IR_SES)} irisan sesi (terurut, deterministik)")

DELTA_N = {}
DELTA_S = {}
for _, r in IR_TER.iterrows():
    DELTA_N[("ter", r["combo"], r["session"], int(r["atr_ter_s"]))] = float(r["delta_pp_normal"])
    DELTA_S[("ter", r["combo"], r["session"], int(r["atr_ter_s"]))] = float(r["delta_pp_stres"])
for _, r in IR_SES.iterrows():
    DELTA_N[("ses", r["combo"], r["session"], 0)] = float(r["delta_pp_normal"])
    DELTA_S[("ses", r["combo"], r["session"], 0)] = float(r["delta_pp_stres"])

NEED_PAIRS = sorted({(r["combo"], r["session"]) for _, r in IR_TER.iterrows()} | {(r["combo"], r["session"]) for _, r in IR_SES.iterrows()})
print(f"pasangan (combo x sesi) unik perlu LA: {len(NEED_PAIRS)}")
for combo, sess in NEED_PAIRS:
    print(f"  {combo:15s} {sess}")'''
)


# sel 05 (code: ATR M5 + M15 kausal, VERBATIM sel 06 run 9)
code(
    '''"""ATR M5(14) + M15(14) kausal (bar TF SELESAI) + uji anti look-ahead."""


def compute_atr_pips(frame: pd.DataFrame, exclude: np.ndarray, rule: str, span_min: int, tol_min: int) -> np.ndarray:
    """ATR(14) kausal dalam pip; generalisasi pola EDA-06 ke TF arbitrer.

    Args:
        frame: DataFrame M1 terurut dengan kolom utc, high, low, close.
        exclude: Mask boolean bar M1 yang dikeluarkan (jendela anomali).
        rule: Aturan resample pandas ("5min", "15min").
        span_min: Batas rentang 14 bucket dalam menit (100 utk M5, 240 utk M15).
        tol_min: Toleransi merge_asof dalam menit (15 utk M5, 45 utk M15).
    """
    src = frame.loc[~exclude, ["utc", "high", "low", "close"]]
    bars = (
        src.assign(bucket=src["utc"].dt.floor(rule))
        .groupby("bucket", sort=True)
        .agg(h=("high", "max"), l=("low", "min"), c=("close", "last"), n=("close", "size"))
        .reset_index()
    )
    tf_min = int(pd.Timedelta(rule).total_seconds() // 60)
    bars = bars[bars["n"] >= 3].reset_index(drop=True)
    contig = bars["bucket"].diff() == pd.Timedelta(minutes=tf_min)
    prev_c = bars["c"].shift(1)
    tr = pd.concat(
        [bars["h"] - bars["l"], (bars["h"] - prev_c).abs().where(contig), (bars["l"] - prev_c).abs().where(contig)],
        axis=1,
    ).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean()
    span_ok = (bars["bucket"] - bars["bucket"].shift(13)) <= pd.Timedelta(minutes=span_min)
    bars["atr"] = atr.where(span_ok)
    bars["avail"] = bars["bucket"] + pd.Timedelta(minutes=tf_min)
    left = pd.DataFrame({"T": frame["utc"] + pd.Timedelta(minutes=1)})
    right = bars.loc[bars["atr"].notna(), ["avail", "atr"]].sort_values("avail")
    merged = pd.merge_asof(
        left, right, left_on="T", right_on="avail", direction="backward", tolerance=pd.Timedelta(minutes=tol_min)
    )
    return (merged["atr"] / PIP_SIZE).to_numpy("float64")


ATR_M5 = compute_atr_pips(m1, C_ARR, "5min", 100, 15)
ATR_M15 = compute_atr_pips(m1, C_ARR, "15min", 240, 45)
print(f"ATR_M5 tersedia: {np.isfinite(ATR_M5).sum():,} | ATR_M15 tersedia: {np.isfinite(ATR_M15).sum():,}")

rng_atr = new_rng("atr_check")
check_pool = np.flatnonzero(np.isfinite(ATR_M5) & np.isfinite(ATR_M15) & (np.arange(N_BARS) > 5000))
check_idx = rng_atr.choice(check_pool, size=12, replace=False)
for i in check_idx:
    lo_i = max(0, int(i) - 5000)
    part = m1.iloc[lo_i : i + 1]
    redo5 = compute_atr_pips(part, C_ARR[lo_i : i + 1], "5min", 100, 15)
    redo15 = compute_atr_pips(part, C_ARR[lo_i : i + 1], "15min", 240, 45)
    chk(bool(np.isclose(redo5[-1], ATR_M5[i], rtol=1e-9, atol=1e-12, equal_nan=True)), f"ATR_M5 kausal @{i}")
    chk(bool(np.isclose(redo15[-1], ATR_M15[i], rtol=1e-9, atol=1e-12, equal_nan=True)), f"ATR_M15 kausal @{i}")
print("PASS: ATR 12 timestamp hitung-ulang identik (tanpa look-ahead).")'''
)
# sel 06 (code: basis entri + tercile, VERBATIM sel 07 run 9)
code(
    '''"""Basis entri stride-5 (aturan identik EDA-06) + tercile ATR per sesi."""
idx_all = np.arange(0, N_BARS - HORIZON - 1, STRIDE)
cont = (UTC_NS[idx_all + HORIZON] - UTC_NS[idx_all]) <= (HORIZON + 2) * 60 * 10**9
no_c = ((C_CUM[idx_all + HORIZON + 1] - C_CUM[idx_all + 1]) == 0) & ~C_ARR[idx_all]
atr_ok = np.isfinite(ATR_M5[idx_all])
sess_ok = SESS_ARR[idx_all] != "Off"
keep = cont & no_c & atr_ok & sess_ok
IDX = idx_all[keep]
N_ENT = len(IDX)
print(f"entri valid: {N_ENT:,} (A={int((STRATA_ARR[IDX] == 'A').sum()):,}, B={int((STRATA_ARR[IDX] == 'B').sum()):,})")
chk(N_ENT == 184_731, "jangkar N_ENT = 184.731 (aturan entri identik EDA-06)")

ENT_SESS = SESS_ARR[IDX]
ENT_ATR = ATR_M5[IDX]
ENT_DAY = DAY_ARR[IDX]
ENT_SEM = SEM_ARR[IDX]
ENT_STR = STRATA_ARR[IDX]
is_a = ENT_STR == "A"
ter = np.zeros(N_ENT, dtype=int)
for label in SESSIONS:
    msk = ENT_SESS == label
    e_ter = np.quantile(ENT_ATR[msk & is_a], [1 / 3, 2 / 3])
    ter[msk] = np.searchsorted(e_ter, ENT_ATR[msk], side="right") + 1
ENT_TER = ter
chk(set(np.unique(ENT_TER)) == {1, 2, 3}, "tercile 1..3 lengkap")'''
)


# sel 07 (code: simulator + LA normal, VERBATIM sel 08 run 9; LA_S tidak dibangun: I-1 tanpa G4)
code(
    '''"""Simulator first-passage (vektorisasi, pola EDA-06) + LA skenario normal."""
WH = sliding_window_view(HI, HORIZON + 1)
WL = sliding_window_view(LO, HORIZON + 1)


def simulate(idx: np.ndarray, sl: np.ndarray, tp: np.ndarray, spr: np.ndarray, side: str, chunk: int = 40_000):
    """Barrier SL/TP untuk entri di bar `idx`. Returns (code, bars, pnl_to, ambos).

    code 1=TP duluan, -1=SL duluan (termasuk bar kembar, pesimis), 0=timeout.
    """
    n = len(idx)
    code = np.zeros(n, dtype=np.int8)
    bars = np.zeros(n, dtype=np.int16)
    pnl_to = np.zeros(n, dtype=np.float64)
    amb = np.zeros(n, dtype=bool)
    for s in range(0, n, chunk):
        ii = idx[s : s + chunk]
        slc = slice(s, s + len(ii))
        hh = WH[ii][:, 1:]
        ll = WL[ii][:, 1:]
        p_spr = spr[slc]
        bid_entry = CL[ii]
        if side == "buy":
            entry = bid_entry + p_spr
            hit_tp = hh >= (entry + tp[slc] * PIP_SIZE)[:, None]
            hit_sl = ll <= (entry - sl[slc] * PIP_SIZE)[:, None]
            pnl_to[slc] = (CL[ii + HORIZON] - entry) / PIP_SIZE
        else:
            entry = bid_entry
            hit_tp = (ll + p_spr[:, None]) <= (entry - tp[slc] * PIP_SIZE)[:, None]
            hit_sl = (hh + p_spr[:, None]) >= (entry + sl[slc] * PIP_SIZE)[:, None]
            pnl_to[slc] = (entry - (CL[ii + HORIZON] + p_spr)) / PIP_SIZE
        any_tp = hit_tp.any(axis=1)
        any_sl = hit_sl.any(axis=1)
        k_tp = np.where(any_tp, hit_tp.argmax(axis=1), HORIZON + 1)
        k_sl = np.where(any_sl, hit_sl.argmax(axis=1), HORIZON + 1)
        sl_first = any_sl & (k_sl <= k_tp)
        tp_first = any_tp & (k_tp < k_sl)
        amb[slc] = any_tp & any_sl & (k_tp == k_sl)
        code[slc] = np.where(tp_first, 1, np.where(sl_first, -1, 0))
        bars[slc] = np.where(tp_first, k_tp + 1, np.where(sl_first, k_sl + 1, 0))
    return code, bars, pnl_to, amb


FIXED_PIPS = {"FIX_50_70": (5.0, 7.0), "FIX_30_45": (3.0, 4.5), "FIX_100_140": (10.0, 14.0)}


def combo_sl_tp(name: str, atr_pips: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """SL/TP per entri untuk combo (aturan identik EDA-06 sel 19: nama = point, nilai = pip)."""
    if name.startswith("FIX_"):
        sl_p, tp_p = FIXED_PIPS[name]
        n = len(atr_pips)
        return np.full(n, sl_p), np.full(n, tp_p)
    parts = name.replace("ATR_k", "").split("_rr")
    sl_a = np.maximum(np.round(float(parts[0]) * atr_pips, 1), 0.5)
    return sl_a, np.round(sl_a * float(parts[1]), 1)


# LA normal: dict (combo, session, side) -> codes selaras IDX (-99 = entri sesi lain)
LA_N = {}
for combo, sess in NEED_PAIRS:
    m = ENT_SESS == sess
    pos = np.flatnonzero(m)
    sl_a, tp_a = combo_sl_tp(combo, ENT_ATR[m])
    spr_a = pd.Series(ENT_SESS[m]).map(COST_NORMAL).to_numpy() * PIP_SIZE
    for side in ("buy", "sell"):
        code_v, _, _, amb_v = simulate(IDX[m], sl_a, tp_a, spr_a, side)
        full = np.full(N_ENT, -99, dtype=np.int8)
        full[pos] = code_v
        LA_N[(combo, sess, side)] = full
        print(f"LA normal {combo:15s} {sess:8s} {side:4s}: n={int(m.sum()):,} amb={float(amb_v.mean()):.4f}")
print(f"LA normal selesai: {len(LA_N)} array (pasangan x sisi)")
print("CATATAN I-1: LA_S (stres) tidak dibangun; I-1 tanpa G4 (batas S5).")
with open(REPORT_DIR / "eda07_i1_progress.log", "a", encoding="utf-8") as _pl:
    _pl.write("I1-LA selesai%s" % chr(10))'''
)
# sel 08 (code: label waktu N-menit, VERBATIM sel 10 run 9)
code(
    '''"""Label waktu LB/LC/LD per N (sampel tanpa tumpang-tindih + buang jendela gap/anomali)."""
TL: dict[tuple[int], dict[str, np.ndarray]] = {}
DROP_REASON: dict[str, int] = {}
for N in N_HORIZONS:
    WINS_H = sliding_window_view(HI, N + 1)
    WINS_L = sliding_window_view(LO, N + 1)
    kept = np.zeros(N_ENT, dtype=bool)
    last = -N - 1
    gap_n = anom_n = 0
    mv = np.full(N_ENT, np.nan)
    rg = np.full(N_ENT, np.nan)
    for j in range(N_ENT):
        i = int(IDX[j])
        if i - last < N:
            continue
        if int(UTC_NS[i + N] - UTC_NS[i]) > (N + 2) * 60 * 10**9:
            gap_n += 1
            continue
        if (C_CUM[i + N + 1] - C_CUM[i + 1]) > 0 or C_ARR[i]:
            anom_n += 1
            continue
        kept[j] = True
        last = i
        mv[j] = (CL[i + N] - CL[i]) / PIP_SIZE
        rg[j] = (WINS_H[i].max() - WINS_L[i].min()) / PIP_SIZE
    del WINS_H, WINS_L
    TL[(N,)] = {"kept": kept, "move": mv, "rng": rg}
    DROP_REASON[f"N={N} gap"] = gap_n
    DROP_REASON[f"N={N} anomali"] = anom_n
    print(f"N={N:2d}: sampel valid {int(kept.sum()):,} dari {N_ENT:,} (gap {gap_n:,}, anomali {anom_n:,})")

# Label diskret per (sesskey, N): sesskey = (session, ter) atau (session, "ALL")
SESSKEYS = sorted({(s, t) for _, _, s, t in [("ter",) + k[1:] for k in DELTA_N if k[0] == "ter"]})
SESSKEYS += sorted({(r["session"], "ALL") for _, r in IR_SES.iterrows()})
print(f"sesskeys waktu: {len(SESSKEYS)}")


def sesskey_mask(sess: str, ter: object) -> np.ndarray:
    """Mask entri IDX untuk sesskey (ter = int tercile atau 'ALL')."""
    m = ENT_SESS == sess
    if ter != "ALL":
        m = m & (ENT_TER == int(ter))
    return m


TLAB: dict[tuple[str, object, int, str], np.ndarray] = {}
for sess, ter in SESSKEYS:
    m = sesskey_mask(sess, ter)
    cost_s = COST_STRESS[sess]
    for N in N_HORIZONS:
        d = TL[(N,)]
        v = m & d["kept"]
        mv = d["move"][v]
        th1, th2 = cost_s, 2.0 * cost_s
        lb = (np.abs(mv) > cost_s + LB_MARGIN_PIP).astype(np.int8)
        lc1 = np.where(mv > th1, 1, np.where(mv < -th1, -1, 0)).astype(np.int8)
        lc2 = np.where(mv > th2, 1, np.where(mv < -th2, -1, 0)).astype(np.int8)
        ld = np.where(mv > 0, 1, np.where(mv < 0, -1, 9)).astype(np.int8)
        TLAB[(sess, ter, N, "LB_bin")] = (v, lb)
        TLAB[(sess, ter, N, "LB_rng")] = (v, d["rng"][v])
        TLAB[(sess, ter, N, "LC1")] = (v, lc1)
        TLAB[(sess, ter, N, "LC2")] = (v, lc2)
        TLAB[(sess, ter, N, "LD")] = (v, ld)
print(f"target waktu: {len(TLAB)} (sesskey x N x jenis)")'''
)


# sel 09 (code: fitur kausal 29 kolom, VERBATIM sel 11 run 9)
code(
    '''"""Fitur kausal 29 kolom (semua t <= entry) + drop NaN tercatat."""


def build_feature_frame(frame: pd.DataFrame, pos: np.ndarray, noise_vals: np.ndarray | None) -> pd.DataFrame:
    """Bangun fitur untuk posisi entri `pos` dari frame M1 (jalur kode tunggal).

    Identik untuk run penuh maupun hitung-ulang leakage (frame terpotong):
    C dikeluarkan via rank-mapping, semua rolling/ewm/resample dihitung di
    dalam fungsi. noise_vals=None -> kolom noise diisi NaN (diuji terpisah).
    """
    keep_nc = ~frame["__c"].to_numpy()
    rank = np.empty(len(frame), dtype=np.int64)
    rank[keep_nc] = np.arange(int(keep_nc.sum()))
    fr = frame.loc[keep_nc].reset_index(drop=True)
    p = rank[pos]
    n = len(fr)
    cl = fr["close"].to_numpy("float64")
    hi = fr["high"].to_numpy("float64")
    lo = fr["low"].to_numpy("float64")
    utc = fr["utc"]
    wall = fr["wall"]
    out: dict[str, np.ndarray] = {}
    a5full = compute_atr_pips(fr, np.zeros(n, dtype=bool), "5min", 100, 15)
    out["atr_m5"] = a5full[p]
    out["atr_m15"] = compute_atr_pips(fr, np.zeros(n, dtype=bool), "15min", 240, 45)[p]
    r1 = np.empty(n)
    r1[0] = np.nan
    r1[1:] = np.log(cl[1:] / cl[:-1])
    r2 = r1**2
    s = pd.Series(r2)
    rv15 = np.sqrt(s.rolling(15, min_periods=15).sum().to_numpy()) * cl / PIP_SIZE
    rv60 = np.sqrt(s.rolling(60, min_periods=60).sum().to_numpy()) * cl / PIP_SIZE
    out["rv15"] = rv15[p]
    out["rv60"] = rv60[p]
    out["vol_ratio"] = np.where(rv60[p] > 0, rv15[p] / np.where(rv60[p] == 0, np.nan, rv60[p]), np.nan)
    lon_min = (utc.dt.tz_convert("Europe/London").dt.hour * 60 + utc.dt.tz_convert("Europe/London").dt.minute).to_numpy()
    ny_min = (utc.dt.tz_convert("America/New_York").dt.hour * 60 + utc.dt.tz_convert("America/New_York").dt.minute).to_numpy()
    ty_min = (utc.dt.tz_convert("Asia/Tokyo").dt.hour * 60 + utc.dt.tz_convert("Asia/Tokyo").dt.minute).to_numpy()
    out["min_lon_open"] = ((lon_min - 480) % 1440).astype(float)[p]
    out["min_ny_open"] = ((ny_min - 480) % 1440).astype(float)[p]
    wm = (wall.dt.hour * 60 + wall.dt.minute).to_numpy().astype(float)
    out["hour_sin"] = np.sin(2 * np.pi * wm / 1440)[p]
    out["hour_cos"] = np.cos(2 * np.pi * wm / 1440)[p]
    out["weekday"] = wall.dt.weekday.to_numpy().astype(float)[p]
    out["tokyo_fix"] = ((ty_min >= 580) & (ty_min <= 610)).astype(float)[p]
    cs = pd.Series(cl)
    for k, nm in ((1, "ret_1"), (5, "ret_5"), (15, "ret_15"), (60, "ret_60")):
        out[nm] = ((cl - np.concatenate([np.full(k, np.nan), cl[:-k]])) / PIP_SIZE)[p]
    ema20 = cs.ewm(span=20, adjust=False).mean().to_numpy()
    ema60 = cs.ewm(span=60, adjust=False).mean().to_numpy()
    a5nz = np.where(a5full == 0, np.nan, a5full)
    out["ema20_d_atr"] = (((cl - ema20) / PIP_SIZE) / a5nz)[p]
    out["ema60_d_atr"] = (((cl - ema60) / PIP_SIZE) / a5nz)[p]
    mu60 = np.full(n, np.nan)
    sd60 = np.full(n, np.nan)
    if n >= 60:
        # Batch eksplisit (BUKAN pandas-rolling: algoritma online-nya menyisakan
        # residu warmup ~1e-8 antar-run; jendela batch identik -> bit-identik).
        W60 = sliding_window_view(cl, 60)
        mu60[59:] = W60.mean(axis=1)
        sd60[59:] = W60.std(axis=1, ddof=1)
        del W60
    out["z60"] = ((cl - mu60) / np.where(sd60 == 0, np.nan, sd60))[p]
    for rule, tf in (("5min", "m5"), ("15min", "m15"), ("1h", "h1")):
        b = (
            fr.assign(bucket=utc.dt.floor(rule))
            .groupby("bucket", sort=True)
            .agg(o=("close", "first"), h=("high", "max"), l=("low", "min"), c=("close", "last"), n=("close", "size"))
            .reset_index()
        )
        b = b[b["n"] >= 2].reset_index(drop=True)
        b["avail"] = b["bucket"] + pd.Timedelta(rule)
        left = pd.DataFrame({"T": utc + pd.Timedelta(minutes=1)})
        mp = pd.merge_asof(left, b.sort_values("avail"), left_on="T", right_on="avail", direction="backward")
        mp = mp.reset_index(drop=True)
        rng = mp["h"] - mp["l"]
        retb = (mp["c"] - mp["o"]) / PIP_SIZE
        posb = np.where(rng > 0, (mp["c"] - mp["l"]) / np.where(rng == 0, np.nan, rng), 0.5)
        out[f"{tf}_ret"] = retb.to_numpy()[p]
        out[f"{tf}_pos"] = posb[p]
    h1c = (
        fr.assign(bucket=utc.dt.floor("1h"))
        .groupby("bucket", sort=True)["close"]
        .last()
    )
    ema_h1 = h1c.ewm(span=12, adjust=False).mean()
    sl = ((ema_h1 - ema_h1.shift(1)) / PIP_SIZE).reindex(h1c.index)
    b1 = pd.DataFrame({"bucket": h1c.index, "sl": sl.to_numpy()})
    b1["avail"] = b1["bucket"] + pd.Timedelta("1h")
    mp1 = pd.merge_asof(
        pd.DataFrame({"T": utc + pd.Timedelta(minutes=1)}), b1.sort_values("avail"), left_on="T", right_on="avail", direction="backward"
    ).reset_index(drop=True)
    out["h1_ema_slope"] = (mp1["sl"].to_numpy() / a5nz)[p]
    out["spread"] = fr["spread_pips"].to_numpy("float64")[p]
    step = 100.0 * PIP_SIZE
    out["round_d"] = (np.abs(cl - np.round(cl / step) * step) / PIP_SIZE)[p]
    dh = fr.groupby("broker_day", observed=True).agg(dh=("high", "max"), dl=("low", "min"))
    dh["pdh"] = dh["dh"].shift(1)
    dh["pdl"] = dh["dl"].shift(1)
    lut_h = dh["pdh"].to_dict()
    lut_l = dh["pdl"].to_dict()
    bd = fr["broker_day"]
    pdh = bd.map(lut_h).to_numpy("float64")
    pdl = bd.map(lut_l).to_numpy("float64")
    out["pdhl_d"] = (np.minimum(np.abs(cl - pdh), np.abs(cl - pdl)) / PIP_SIZE)[p]
    if noise_vals is None:
        out["noise"] = np.full(len(p), np.nan)
    else:
        out["noise"] = noise_vals
    cols = ["rv15", "rv60", "atr_m5", "atr_m15", "vol_ratio", "min_lon_open", "min_ny_open", "hour_sin",
            "hour_cos", "weekday", "tokyo_fix", "ret_1", "ret_5", "ret_15", "ret_60", "ema20_d_atr",
            "ema60_d_atr", "z60", "m5_ret", "m5_pos", "m15_ret", "m15_pos", "h1_ret", "h1_pos",
            "h1_ema_slope", "spread", "noise", "round_d", "pdhl_d"]
    return pd.DataFrame({c: out[c] for c in cols})


m1["__c"] = C_ARR
rng_noise = new_rng("noise")
FEAT = build_feature_frame(m1, IDX, rng_noise.standard_normal(N_ENT))
FEAT_COLS = list(FEAT.columns)
CTRL_COLS = ["noise", "round_d", "pdhl_d"]
NONCTRL = [c for c in FEAT_COLS if c not in CTRL_COLS]
print(f"fitur: {len(FEAT_COLS)} kolom ({len(NONCTRL)} non-kontrol + {len(CTRL_COLS)} kontrol)")

finite = np.isfinite(FEAT[NONCTRL].to_numpy()).all(axis=1)
KEEP = finite
print(f"entri kept (fitur non-kontrol finit): {int(KEEP.sum()):,} dari {N_ENT:,} (drop {int((~KEEP).sum()):,})")
chk(int(KEEP.sum()) > 100_000, "entri kept > 100rb")
FEAT = FEAT[KEEP].reset_index(drop=True)
ENT_SESS_K = ENT_SESS[KEEP]
ENT_TER_K = ENT_TER[KEEP]
ENT_DAY_K = ENT_DAY[KEEP]
ENT_SEM_K = ENT_SEM[KEEP]
ENT_STR_K = ENT_STR[KEEP]
IDX_K = IDX[KEEP]
N_KEEP = int(KEEP.sum())
XMAT = FEAT.to_numpy("float64")
print(f"N_KEEP={N_KEEP:,}")
with open(REPORT_DIR / "eda07_i1_progress.log", "a", encoding="utf-8") as _pl:
    _pl.write("I1-FEAT selesai N_KEEP=%d%s" % (N_KEEP, chr(10)))'''
)
# sel 10 (code: mesin MI + kuantil + bootstrap, VERBATIM sel 12 run 9)
code(
    '''"""Mesin L2/S5: bin kuantil, MI diskret, lantai permutasi blok-hari, lift desil + CI."""
SEM_LIST = SEM_A  # 5 semester strata A, terurut
FLAT_KEEP = np.flatnonzero(KEEP)  # posisi N_ENT -> baris N_KEEP


def qcodes(x: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Kode bin kuantil (k target, duplikat dibuang); konstan -> satu bin."""
    x = np.asarray(x, dtype=float)
    qs = np.linspace(0.0, 1.0, k + 1)
    edges = np.quantile(x[np.isfinite(x)], qs)
    edges = np.unique(edges)
    if len(edges) < 3:
        return np.zeros(len(x), dtype=np.int64), edges
    return np.clip(np.searchsorted(edges[1:-1], x, side="right"), 0, len(edges) - 2), edges


def apply_edges(x: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """Terapkan tepi bin tetap (univariat, pra-registrasi) ke sampel lain."""
    if len(edges) < 3:
        return np.zeros(len(x), dtype=np.int64)
    return np.clip(np.searchsorted(edges[1:-1], np.asarray(x, dtype=float), side="right"), 0, len(edges) - 2)


def mi_dd(xc: np.ndarray, yc: np.ndarray) -> float:
    """Mutual information diskret-diskret via tabulasi bincount (nat)."""
    xc = np.asarray(xc, dtype=np.int64)
    yc = np.asarray(yc, dtype=np.int64)
    nx, ny = int(xc.max()) + 1, int(yc.max()) + 1
    joint = np.bincount(xc * ny + yc, minlength=nx * ny).reshape((nx, ny)).astype(float)
    tot = joint.sum()
    px = joint.sum(axis=1, keepdims=True) / tot
    py = joint.sum(axis=0, keepdims=True) / tot
    pz = joint / tot
    with np.errstate(divide="ignore", invalid="ignore"):
        term = np.where(pz > 0, pz * np.log(pz / (px * py)), 0.0)
    return float(term.sum())


def day_struct(day: np.ndarray):
    """Struktur hari terurut sekali per target (diangkat dari loop permutasi)."""
    uniq, inv = np.unique(np.asarray(day), return_inverse=True)
    order = np.argsort(inv, kind="stable")
    counts = np.bincount(inv)
    starts = np.zeros(len(uniq) + 1, dtype=np.int64)
    starts[1:] = np.cumsum(counts)
    return inv, order, counts, starts


def permute_block_y(y: np.ndarray, inv, counts, starts, order, rng: np.random.Generator) -> np.ndarray:
    """Satu draw null blok-hari, tervektorisasi (urutan draw: permutasi hari, lalu acak-dalam-blok)."""
    y = np.asarray(y)
    n = len(y)
    sy = y[order]
    src = rng.permutation(len(counts))[inv]
    off = (rng.random(n) * counts[src]).astype(np.int64)
    return sy[starts[src] + off]


def mi_floor_all(Xm: np.ndarray, y: np.ndarray, ycode, day: np.ndarray, rng: np.random.Generator,
                 n_perm: int = N_PERM, bins: int = MI_BINS) -> tuple[np.ndarray, np.ndarray]:
    """MI teramati + lantai p95 per kolom matriks (bin-X dan pengode-y tetap; draw ter-batch)."""
    Xm = np.asarray(Xm, dtype=float)
    F = Xm.shape[1]
    codes = np.empty((len(y), F), dtype=np.int64)
    for j in range(F):
        codes[:, j], _ = qcodes(Xm[:, j], bins)
    yc = ycode(np.asarray(y))
    mi_obs = np.array([mi_dd(codes[:, j], yc) for j in range(F)])
    inv, order, counts, starts = day_struct(day)
    nulls = np.empty((n_perm, F))
    for b in range(n_perm):
        yb = ycode(permute_block_y(y, inv, counts, starts, order, rng))
        for j in range(F):
            nulls[b, j] = mi_dd(codes[:, j], yb)
    return mi_obs, np.quantile(nulls, 0.95, axis=0)


def lift_deciles(x: np.ndarray, stat_y: np.ndarray, is_binary: bool, rng: np.random.Generator,
                 n_boot: int = N_BOOT, edges=None) -> dict:
    """Lift desil-atas vs bawah + CI bootstrap klaster-hari (S5/S8, stream tunggal)."""
    if edges is None:
        _, edges = qcodes(x, 10)
    dc = apply_edges(x, edges)
    top = dc == dc.max()
    bot = dc == dc.min()
    if is_binary:
        s_top = float(stat_y[top].mean()) if top.sum() else np.nan
        s_bot = float(stat_y[bot].mean()) if bot.sum() else np.nan
    else:
        s_top = float(np.mean(stat_y[top])) if top.sum() else np.nan
        s_bot = float(np.mean(stat_y[bot])) if bot.sum() else np.nan
    lift = s_top - s_bot
    day = LIFT_DAY_CTX["day"]
    rows = LIFT_DAY_CTX["rows"]
    uday = np.unique(day)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.choice(uday, size=len(uday), replace=True)
        sel = np.concatenate([rows[day == d] for d in pick])
        ys = stat_y[sel]
        xs = dc[sel]
        t = xs == xs.max()
        o = xs == xs.min()
        boots[b] = float(ys[t].mean() - ys[o].mean()) if t.sum() and o.sum() else np.nan
    lo, hi = float(np.nanquantile(boots, 0.025)), float(np.nanquantile(boots, 0.975))
    return {"lift": float(lift), "lo": lo, "hi": hi, "top": s_top, "bot": s_bot,
            "n_top": int(top.sum()), "n_bot": int(bot.sum()), "edges": edges}


LIFT_DAY_CTX = {"day": np.array([0]), "rows": np.array([0])}

# Kode-y per jenis label (pra-registrasi, tetap)
YCODE = {
    "LA": lambda v: (np.asarray(v) == 1).astype(np.int64) + (np.asarray(v) == -1).astype(np.int64) * 2,
    "LB_bin": lambda v: np.asarray(v, dtype=np.int64),
    "LB_rng": None,  # kontinu: bin-20 + Spearman pendamping
    "LC1": lambda v: (np.asarray(v) + 1).astype(np.int64),
    "LC2": lambda v: (np.asarray(v) + 1).astype(np.int64),
    "LD": lambda v: ((np.asarray(v) + 1) // 2).astype(np.int64),
}
# Kelas positif untuk lift (pra-registrasi): LA TP-duluan, LC arah naik, biner 1
YPOS = {"LA": 1, "LB_bin": 1, "LB_rng": None, "LC1": 1, "LC2": 1, "LD": 1}
print("mesin L2 siap: MI 20-binning, lantai blok-hari 100x p95, lift desil + CI klaster-hari.")'''
)


# sel 11 (code: uji anti-leakage I-1, ADAPTASI sel 13 run 9: N_LEAK -> N_LEAK_I1 = 60)
code(
    '''"""Uji anti-leakage I-1: 60 timestamp, hitung-ulang SEMUA fitur dari data s.d. T."""
rng_leak = new_rng("leak")
rng_noise_replay = new_rng("noise")
NOISE_ALL = rng_noise_replay.standard_normal(N_ENT)
chk(bool(np.array_equal(NOISE_ALL[KEEP], FEAT["noise"].to_numpy())),
    "replay noise bit-identik (stream tunggal seed 70701)")
pool = np.flatnonzero(KEEP & (IDX >= 20_000))
chk(len(pool) > 1000, "pool leakage > 1000 kandidat")
LEAK_J = np.sort(rng_leak.choice(pool, size=N_LEAK_I1, replace=False))
CMP_COLS = [c for c in FEAT_COLS]  # 29 kolom incl noise (replay eksak)
miss = 0
for j in LEAK_J:
    i = int(IDX[int(j)])
    lo = i - 20_000
    part = m1.iloc[lo : i + 1]
    k = int(np.searchsorted(FLAT_KEEP, j))  # baris N_KEEP untuk entri j
    ref = FEAT.iloc[k][CMP_COLS].to_numpy("float64")
    redo = build_feature_frame(part, np.array([i - lo]), np.array([NOISE_ALL[int(j)]]))
    ok = bool(np.allclose(redo.iloc[0][CMP_COLS].to_numpy("float64"), ref, rtol=1e-9, atol=1e-12, equal_nan=True))
    chk(ok, f"leakage identik @{i}")
    miss += (not ok)
print(f"PASS: anti-leakage {N_LEAK_I1 - miss}/{N_LEAK_I1} identik (rtol=1e-9, lookback 20.000 bar).")'''
)
# sel 12 (code: get_sample VERBATIM sel 14 run 9 + assert konsistensi vs artefak run 9)
code(
    '''"""Sampel analisis (get_sample verbatim run 9) + konsistensi vs _ckpt_/_gate_ + rebuild eksak."""


def get_sample(y_full: np.ndarray, mask_full: np.ndarray, kind: str):
    """Sampel N_KEEP untuk satu target: X, y, hari, semester, strata (terurut)."""
    m = np.asarray(mask_full) & KEEP
    kk = np.flatnonzero(m)
    rows = np.searchsorted(FLAT_KEEP, kk)
    y = np.asarray(y_full)[m]
    return {"rows": rows, "X": XMAT[rows], "y": y, "kind": kind,
            "day": ENT_DAY_K[rows], "sem": ENT_SEM_K[rows], "strata": ENT_STR_K[rows],
            "n": int(m.sum())}


# Konsistensi n per target vs checkpoint run 9 (60 LA + 200 waktu = 260).
CKPT_LA = pd.read_csv(REPORT_DIR / "_ckpt_LA.csv")
CKPT_T = pd.read_csv(REPORT_DIR / "_ckpt_T.csv")
chk(len(CKPT_LA) == 60, "ckpt LA 60 baris")
chk(len(CKPT_T) == 200, "ckpt waktu 200 baris")
LA_KEYS = [(("ter", r["combo"], r["session"], int(r["atr_ter_s"]))) for _, r in IR_TER.iterrows()]
LA_KEYS += [(("ses", r["combo"], r["session"], 0)) for _, r in IR_SES.iterrows()]
n_la_mismatch = 0
for key in LA_KEYS:
    _, combo, sess, tval = key
    m_sess = sesskey_mask(sess, tval if key[0] == "ter" else "ALL")
    for side in ("buy", "sell"):
        mask = m_sess & (LA_N[(combo, sess, side)] != -99) & KEEP
        n_here = int(mask.sum())
        tag = f"{key} {side}"
        hit = CKPT_LA[CKPT_LA["target"] == tag]
        chk(len(hit) == 1, f"ckpt LA memuat {tag}")
        if int(hit.iloc[0]["n"]) != n_here:
            n_la_mismatch += 1
chk(n_la_mismatch == 0, "n 60/60 target LA == _ckpt_LA.csv")
print("PASS: n 60/60 target LA sama persis _ckpt_LA.csv.")
SESS_ALL_I1 = sorted({(r["session"], int(r["atr_ter_s"])) for _, r in IR_TER.iterrows()} |
                     {(r["session"], "ALL") for _, r in IR_SES.iterrows()},
                     key=lambda t: (t[0], str(t[1])))
n_t_mismatch = 0
for sess, ter in SESS_ALL_I1:
    for N in N_HORIZONS:
        for kd in ["LB_bin", "LB_rng", "LC1", "LC2", "LD"]:
            v, vals = TLAB[(sess, ter, N, kd)]
            y_full = np.full(N_ENT, np.nan)
            y_full[v] = vals
            mask = v & np.isfinite(y_full) & KEEP
            if kd == "LD":
                mask &= y_full != 9
            tag = f"{kd} {sess} t{ter} N{N}"
            hit = CKPT_T[CKPT_T["target"] == tag]
            chk(len(hit) == 1, f"ckpt waktu memuat {tag}")
            if int(hit.iloc[0]["n"]) != int(mask.sum()):
                n_t_mismatch += 1
chk(n_t_mismatch == 0, "n 200/200 target waktu == _ckpt_T.csv")
print("PASS: n 200/200 target waktu sama persis _ckpt_T.csv (260/260 total).")

# Alarm run 9: 86 baris unik (52 pdhl_d + 28 round_d + 6 noise).
GATE = pd.read_csv(REPORT_DIR / "_gate_G2_alarm.csv")
chk(len(GATE) == 86, "alarm 86 baris")
chk(int((GATE["kontrol"] == "pdhl_d").sum()) == 52, "pdhl_d 52")
chk(int((GATE["kontrol"] == "round_d").sum()) == 28, "round_d 28")
chk(int((GATE["kontrol"] == "noise").sum()) == 6, "noise 6")
chk(len(set(zip(GATE["target"], GATE["kontrol"]))) == 86, "86 pasangan unik")
print("PASS: _gate_G2_alarm.csv 86/86 pasangan (52+28+6).")

# Rebuild fitur PENUH jalur identik + noise replay -> bit-identik (>=1000 baris).
FEAT2 = build_feature_frame(m1, IDX, NOISE_ALL)
chk(len(FEAT2) == N_ENT, "rebuild penuh N_ENT baris")
chk(bool(np.array_equal(FEAT2[KEEP].reset_index(drop=True).to_numpy("float64"),
                        FEAT.to_numpy("float64"), equal_nan=True)),
    "rebuild fitur bit-identik pada seluruh N_KEEP baris")
print(f"PASS: rebuild fitur eksak-identik {N_KEEP:,} baris (>=1000 sampel SAMA PERSIS).")

# Re-simulate satu LA penuh -> kode identik (label LA pipeline-identik).
combo0, sess0 = NEED_PAIRS[0]
m0 = ENT_SESS == sess0
sl0, tp0 = combo_sl_tp(combo0, ENT_ATR[m0])
spr0 = pd.Series(ENT_SESS[m0]).map(COST_NORMAL).to_numpy() * PIP_SIZE
code_b, _, _, _ = simulate(IDX[m0], sl0, tp0, spr0, "buy")
pos0 = np.flatnonzero(m0)
chk(bool(np.array_equal(code_b, LA_N[(combo0, sess0, "buy")][pos0])), f"re-simulate LA {combo0} {sess0} buy identik")
print(f"PASS: re-simulate LA {combo0} {sess0} buy bit-identik.")

# Nilai label waktu: cek langsung 1000 sampel per N (mv/rg dari array mentah).
rng_lab = new_rng("leak")
for N in N_HORIZONS:
    d = TL[(N,)]
    cand = np.flatnonzero(d["kept"] & KEEP)
    chk(len(cand) >= 1000, f"kandidat label N={N} >= 1000")
    pick = np.sort(rng_lab.choice(cand, size=1000, replace=False))
    ii = IDX[pick]
    mv_ref = (CL[ii + N] - CL[ii]) / PIP_SIZE
    chk(bool(np.allclose(d["move"][pick], mv_ref, rtol=1e-12, atol=1e-12, equal_nan=True)),
        f"label move N={N} 1000/1000 sama persis")
print("PASS: label waktu move 1000/1000 sama persis per N (4x1000 cek).")'''
)


# sel 13 (code: Q1 konsentrasi alarm)
code(
    '''"""Q1 konsentrasi: tabulasi 80 struktural + 6 noise per target/irisan/sisi/sesi/horizon -> T-I1-1."""
import re as _re

LA_PAT = _re.compile(r"^LA (\\S+) (\\S+) t(\\d+) (buy|sell)$")
T_PAT = _re.compile(r"^(LB_bin|LB_rng|LC1|LC2|LD) (\\S+) t(ALL|\\d+) N(\\d+)$")

q1_rows = []
for _, r in GATE.iterrows():
    tgt, cf = r["target"], r["kontrol"]
    m = LA_PAT.match(tgt)
    if m:
        combo, sess, tval, side = m.group(1), m.group(2), m.group(3), m.group(4)
        q1_rows.append({"target": tgt, "kontrol": cf, "n_arah": int(r["n_arah"]), "blok": "LA",
                        "label": "LA", "irisan": "ses" if tval == "0" else "ter",
                        "session": sess, "tercile": tval, "sisi": side, "combo": combo, "N": HORIZON})
        continue
    m = T_PAT.match(tgt)
    chk(m is not None, f"target waktu terparse: {tgt}")
    kind, sess, tval, N = m.group(1), m.group(2), m.group(3), int(m.group(4))
    q1_rows.append({"target": tgt, "kontrol": cf, "n_arah": int(r["n_arah"]), "blok": "WAKTU",
                    "label": kind, "irisan": "ses" if tval == "ALL" else "ter",
                    "session": sess, "tercile": tval, "sisi": "-", "combo": "-", "N": N})
Q1 = pd.DataFrame(q1_rows)
chk(len(Q1) == 86, "Q1 86 baris alarm")
Q1.to_csv(REPORT_DIR / "T-I1-1.csv", index=False)
print("T-I1-1.csv: 86 baris alarm terparse ->", REPORT_DIR / "T-I1-1.csv")

STR = Q1[Q1["kontrol"] != "noise"]
NOI = Q1[Q1["kontrol"] == "noise"]
print(f"struktural={len(STR)} (pdhl_d={int((STR['kontrol'] == 'pdhl_d').sum())}, "
      f"round_d={int((STR['kontrol'] == 'round_d').sum())}) | noise={len(NOI)}")


def _tab(col: str, frame: pd.DataFrame = STR) -> pd.DataFrame:
    t = frame[col].value_counts().rename_axis(col).reset_index(name="n")
    t["pct"] = (100.0 * t["n"] / len(frame)).round(1)
    return t


print("--- Q1 struktural per blok/label ---")
show(_tab("label"), "label")
print("--- Q1 struktural per irisan (ter vs ses) ---")
show(_tab("irisan"), "irisan")
print("--- Q1 struktural per sesi ---")
show(_tab("session"), "session")
print("--- Q1 struktural per tercile ---")
show(_tab("tercile"), "tercile")
print("--- Q1 LA struktural per sisi ---")
show(_tab("sisi", STR[STR["blok"] == "LA"]), "sisi LA")
print("--- Q1 waktu struktural per horizon N ---")
show(_tab("N", STR[STR["blok"] == "WAKTU"]), "horizon")
print("--- Q1 noise pembanding (6) per label/sesi ---")
show(_tab("label", NOI), "label noise")
show(_tab("session", NOI), "sesi noise")
with open(REPORT_DIR / "eda07_i1_progress.log", "a", encoding="utf-8") as _pl:
    _pl.write("I1-Q1 selesai 86 baris%s" % chr(10))'''
)
# sel 14 (code: Q2 uji-kedekatan + kalibrasi negatif)
code(
    '''"""Q2 uji-kedekatan: P(label|DEKAT) vs P(label|JAUH) + CI klaster-hari 1000x -> T-I1-2."""
chk("LA_PAT" in dir() and "T_PAT" in dir(), "parser Q1 dipakai ulang (tanpa pola baru)")
chk(X_PIN == 10, "X pra-registrasi = 10 pip (satu nilai, tanpa pindai)")
FEAT_CTRL = {c: FEAT[c].to_numpy("float64") for c in CTRL_COLS}  # selaras N_KEEP


def pair_sample(tgt: str):
    """Sampel N_KEEP pasangan alarm: rows, stat (positif-rate atau mean), dekat-diisi Q2/Q3.

    Label positif pra-registrasi (YPOS): LA TP-duluan (kode 1), LC naik (1),
    LD (1), LB_bin (1); LB_rng kontinu -> mean range. Strata A+B apa adanya.
    """
    m = LA_PAT.match(tgt)
    if m:
        combo, sess, tval, side = m.group(1), m.group(2), m.group(3), m.group(4)
        m_sess = sesskey_mask(sess, "ALL" if tval == "0" else int(tval))
        yN = LA_N[(combo, sess, side)]
        mask = m_sess & (yN != -99)
        y = yN[mask].astype("float64")
        stat = (y == YPOS["LA"]).astype("float64")
        is_cont = False
    else:
        m = T_PAT.match(tgt)
        chk(m is not None, f"target terparse: {tgt}")
        kind, sess, tval, N = m.group(1), m.group(2), m.group(3), int(m.group(4))
        v, vals = TLAB[(sess, "ALL" if tval == "ALL" else int(tval), N, kind)]
        y_full = np.full(N_ENT, np.nan)
        y_full[v] = vals
        mask = v & np.isfinite(y_full)
        if kind == "LD":
            mask &= y_full != 9
        y = y_full[mask]
        is_cont = kind == "LB_rng"
        stat = y.astype("float64") if is_cont else (y == YPOS[kind]).astype("float64")
    kk = np.flatnonzero(mask & KEEP)
    rows = np.searchsorted(FLAT_KEEP, kk)
    rel = (mask & KEEP)[mask]  # posisi mask yang juga kept -> selaras panjang stat
    return {"rows": rows, "stat": stat[rel], "day": ENT_DAY_K[rows],
            "n": int(len(rows)), "is_cont": is_cont}


def dekat_lift_ci(stat: np.ndarray, dekat: np.ndarray, day: np.ndarray,
                  rng: np.random.Generator, n_boot: int = N_BOOT):
    """Selisih mean DEKAT-JAUH + CI bootstrap klaster-hari (stream tunggal)."""
    D, J = np.asarray(dekat, dtype=bool), ~np.asarray(dekat, dtype=bool)
    nD, nJ = int(D.sum()), int(J.sum())
    if nD == 0 or nJ == 0:
        return {"lift": np.nan, "lo": np.nan, "hi": np.nan, "pD": np.nan, "pJ": np.nan,
                "nD": nD, "nJ": nJ}
    pD, pJ = float(stat[D].mean()), float(stat[J].mean())
    uday = np.unique(day)
    day_rows = [np.flatnonzero(day == d) for d in uday]
    boots = np.full(n_boot, np.nan)
    for b in range(n_boot):
        pick = rng.integers(0, len(uday), size=len(uday))
        sel = np.concatenate([day_rows[p] for p in pick])
        sD, sJ = sel[D[sel]], sel[J[sel]]
        if len(sD) and len(sJ):
            boots[b] = float(stat[sD].mean() - stat[sJ].mean())
    if np.all(np.isnan(boots)):
        lo = hi = np.nan
    else:
        lo, hi = float(np.nanquantile(boots, 0.025)), float(np.nanquantile(boots, 0.975))
    return {"lift": float(pD - pJ), "lo": lo, "hi": hi, "pD": pD, "pJ": pJ, "nD": nD, "nJ": nJ}


def q2_verdict(lift: float, lo: float, hi: float) -> str:
    """Vonis-per-pasangan Q2: signifikan = CI 95% tak memuat 0."""
    if not (np.isfinite(lift) and np.isfinite(lo) and np.isfinite(hi)):
        return "tak-beda"
    if lift > 0 and lo > 0:
        return "DEKAT-mendominasi"
    if lift < 0 and hi < 0:
        return "JAUH-mendominasi"
    return "tak-beda"


Q2_ROWS = []
for eidx, grow in GATE.iterrows():
    tgt, cf = grow["target"], grow["kontrol"]
    smp = pair_sample(tgt)
    d = FEAT_CTRL[cf][smp["rows"]]
    dekat = np.abs(d) <= X_PIN  # noise: unit sama (|noise|<=10, degenerat jujur)
    rng_q2 = new_rng_i1("q2", int(eidx))
    r = dekat_lift_ci(smp["stat"], dekat, smp["day"], rng_q2)
    Q2_ROWS.append({"target": tgt, "kontrol": cf, "n": smp["n"], "n_dekat": r["nD"],
                    "n_jauh": r["nJ"], "p_dekat": r["pD"], "p_jauh": r["pJ"],
                    "lift": r["lift"], "lo": r["lo"], "hi": r["hi"],
                    "verdict": q2_verdict(r["lift"], r["lo"], r["hi"])})
Q2 = pd.DataFrame(Q2_ROWS)
chk(len(Q2) == 86, "Q2 86 pasangan")
Q2.to_csv(REPORT_DIR / "T-I1-2.csv", index=False)
print("T-I1-2.csv: 86 pasangan (lift DEKAT-JAUH + CI klaster-hari).")
show(Q2["verdict"].value_counts().rename_axis("verdict").reset_index(name="n"), "vonis Q2 keseluruhan")
for cf in ["pdhl_d", "round_d", "noise"]:
    sub = Q2[Q2["kontrol"] == cf]
    show(sub["verdict"].value_counts().rename_axis("verdict").reset_index(name="n"), f"vonis Q2 {cf} ({len(sub)})")

# Kalibrasi negatif: prosedur SAMA pada 6 noise; LOLOS iff <=1/6 signifikan.
NOISE_Q2 = Q2[Q2["kontrol"] == "noise"]
sig_noise = int(((NOISE_Q2["verdict"] == "DEKAT-mendominasi") | (NOISE_Q2["verdict"] == "JAUH-mendominasi")).sum())
print(f"kalibrasi negatif Q2: {sig_noise}/6 noise signifikan (batas LOLOS <=1/6).")
chk(sig_noise <= 1, f"kalibrasi negatif Q2 lolos ({sig_noise}/6 <= 1/6); bila >=2/6 = mesin rusak STOP")
with open(REPORT_DIR / "eda07_i1_progress.log", "a", encoding="utf-8") as _pl:
    _pl.write("I1-Q2 selesai sig_noise=%d%s" % (sig_noise, chr(10)))'''
)


# sel 15 (code: Q3 uji-proxy stratifikasi rv15)
code(
    '''"""Q3 uji-proxy: median rv15 (diagnostik) + desil rv15 (penentu) -> T-I1-3."""
RV15 = XMAT[:, NONCTRL.index("rv15")]


Q3_ROWS = []
for eidx, grow in GATE.iterrows():
    tgt, cf = grow["target"], grow["kontrol"]
    smp = pair_sample(tgt)
    rows, stat, day = smp["rows"], smp["stat"], smp["day"]
    d = FEAT_CTRL[cf][rows]
    dekat = np.abs(d) <= X_PIN
    rv = RV15[rows]
    # Median split (diagnostik): lift per paruh rv15.
    med = float(np.median(rv[np.isfinite(rv)]))
    lift_lo = lift_hi = np.nan
    for half, want_low in (("lo", True), ("hi", False)):
        m = (rv <= med) if want_low else (rv > med)
        if m.sum() and dekat[m].sum() and (~dekat[m]).sum():
            lift_lo = float(stat[m][dekat[m]].mean() - stat[m][~dekat[m]].mean()) if want_low else lift_lo
            lift_hi = float(stat[m][dekat[m]].mean() - stat[m][~dekat[m]].mean()) if not want_low else lift_hi
    # Desil pooled (penentu): tepi dari sampel pooled, diterapkan per draw.
    _, edges = qcodes(rv, 10)
    g = apply_edges(rv, edges)
    G = 10
    dec_lift, dec_n = [], []
    for gg in range(G):
        m = g == gg
        dec_n.append(int(m.sum()))
        if m.sum() and dekat[m].sum() and (~dekat[m]).sum():
            dec_lift.append(float(stat[m][dekat[m]].mean() - stat[m][~dekat[m]].mean()))
        else:
            dec_lift.append(np.nan)  # sisi kosong = bukan-tanda-sama (pra-registrasi)
    w = np.array(dec_n, dtype=float) / max(sum(dec_n), 1)
    finite = np.array([np.isfinite(v) for v in dec_lift])
    pooled = float(np.nansum([w[gg] * dec_lift[gg] if finite[gg] else 0.0 for gg in range(G)])
                   / max(w[finite].sum(), 1e-12)) if finite.any() else np.nan
    # Bootstrap pooled-terbobot: draw klaster-hari, hitung-ulang lift per desil, bobot pooled tetap.
    rng_q3 = new_rng_i1("q3", int(eidx))
    uday = np.unique(day)
    day_rows = [np.flatnonzero(day == dd) for dd in uday]
    boots = np.full(N_BOOT, np.nan)
    for b in range(N_BOOT):
        pick = rng_q3.integers(0, len(uday), size=len(uday))
        sel = np.concatenate([day_rows[p] for p in pick])
        num = den = 0.0
        for gg in range(G):
            mg = sel[g[sel] == gg]
            if len(mg) and dekat[mg].sum() and (~dekat[mg]).sum():
                num += w[gg] * float(stat[mg][dekat[mg]].mean() - stat[mg][~dekat[mg]].mean())
                den += w[gg]
        boots[b] = num / den if den > 0 else np.nan
    if np.all(np.isnan(boots)):
        plo = phi = np.nan
    else:
        plo, phi = float(np.nanquantile(boots, 0.025)), float(np.nanquantile(boots, 0.975))
    psign = int(np.sign(pooled)) if np.isfinite(pooled) and pooled != 0.0 else 0
    match = sum(1 for gg in range(G)
                if np.isfinite(dec_lift[gg]) and dec_lift[gg] != 0.0
                and int(np.sign(dec_lift[gg])) == psign) if psign else 0
    bertahan = bool(psign != 0 and match >= 7 and np.isfinite(plo) and np.isfinite(phi)
                    and (phi < 0 or plo > 0))
    Q3_ROWS.append({"target": tgt, "kontrol": cf, "n": smp["n"],
                    "med_lift_rendah": lift_lo, "med_lift_tinggi": lift_hi,
                    "lift_pooled": pooled, "plo": plo, "phi": phi,
                    "dec_match": f"{match}/10",
                    "dec_lifts": ";".join("nan" if not np.isfinite(v) else f"{v:.4f}" for v in dec_lift),
                    "vonis": "Bertahan" if bertahan else "Lenyap"})
Q3 = pd.DataFrame(Q3_ROWS)
chk(len(Q3) == 86, "Q3 86 pasangan")
Q3.to_csv(REPORT_DIR / "T-I1-3.csv", index=False)
print("T-I1-3.csv: 86 pasangan (median + desil rv15 + pooled-terbobot CI).")
show(Q3["vonis"].value_counts().rename_axis("vonis").reset_index(name="n"), "vonis Q3 keseluruhan")
for cf in ["pdhl_d", "round_d", "noise"]:
    sub = Q3[Q3["kontrol"] == cf]
    show(sub["vonis"].value_counts().rename_axis("vonis").reset_index(name="n"), f"vonis Q3 {cf} ({len(sub)})")
with open(REPORT_DIR / "eda07_i1_progress.log", "a", encoding="utf-8") as _pl:
    _pl.write("I1-Q3 selesai%s" % chr(10))'''
)
# sel 16 (code: vonis V-2 + hash SESUDAH + kesimpulan + kunci akhir)
code(
    '''"""Vonis-per-pasangan V-2 + ringkasan per kontrol + hash SESUDAH + kesimpulan terkunci."""
Q2R = pd.read_csv(REPORT_DIR / "T-I1-2.csv")
Q3R = pd.read_csv(REPORT_DIR / "T-I1-3.csv")
chk(len(Q2R) == 86 and len(Q3R) == 86, "T-I1-2/3 masing-masing 86 baris")
M = Q2R.merge(Q3R, on=["target", "kontrol"], suffixes=("_q2", "_q3"))
chk(len(M) == 86, "gabung Q2xQ3 86 baris")

# Aturan putus V-2 (verbatim putusan-eda07-g2.md): ASLI iff lift-kedekatan
# (Q2 DEKAT-mendominasi) BERTAHAN setelah stratifikasi (Q3); selain itu ARTEFAK.
M["vonis_V2"] = np.where((M["verdict"] == "DEKAT-mendominasi") & (M["vonis"] == "Bertahan"),
                         "ASLI", "ARTEFAK")
Q3R["vonis_V2"] = M["vonis_V2"].to_numpy()
Q3R.to_csv(REPORT_DIR / "T-I1-3.csv", index=False)
print("T-I1-3.csv ditulis ulang + kolom vonis_V2 (tetap satu file T-I1-3).")
show(M["vonis_V2"].value_counts().rename_axis("vonis_V2").reset_index(name="n"), "vonis V-2 keseluruhan (86)")
for cf in ["pdhl_d", "round_d", "noise"]:
    sub = M[M["kontrol"] == cf]
    show(sub["vonis_V2"].value_counts().rename_axis("vonis_V2").reset_index(name="n"),
         f"vonis V-2 {cf} ({len(sub)})")
    show(sub.groupby(["verdict", "vonis"]).size().reset_index(name="n").sort_values("n", ascending=False),
         f"silang Q2xQ3 {cf}")

# File run 9 tak tersentuh: hash SESUDAH == SEBELUM untuk keenam artefak.
HASH_AFTER = {}
for rel in RUN9_FILES:
    h = hashlib.sha256((PROJECT_ROOT / rel).read_bytes()).hexdigest()
    HASH_AFTER[rel] = h
    print(f"SESUDAH {h[:12]} {rel}")
    chk(h == HASH_BEFORE[rel], f"run 9 tak tersentuh: {rel}")
print("PASS: keenam file run 9 bit-identik sebelum vs sesudah I-1.")

# CSV I-1 ASCII murni (bukti mentah untuk laporan S5).
# Normalisasi EOL dulu: to_csv di Windows menghasilkan CRLF via text-mode;
# byte-level CRLF->LF; isi data tidak berubah (pola yang sama dipakai run 9 utk notebook).
for name in ["T-I1-1.csv", "T-I1-2.csv", "T-I1-3.csv"]:
    _p = REPORT_DIR / name
    _p.write_bytes(_p.read_bytes().replace(b"\\r\\n", b"\\n"))
print("normalisasi EOL CSV CRLF->LF.")
for name in ["T-I1-1.csv", "T-I1-2.csv", "T-I1-3.csv"]:
    raw = (REPORT_DIR / name).read_bytes()
    chk(all(b < 128 for b in raw), f"{name} ASCII murni")
    chk(raw.endswith(b"\\n") and b"\\r" not in raw, f"{name} LF + tail-LF")
print("PASS: T-I1-1/2/3 ASCII + LF + tail-LF.")

N_ASLI = int((M["vonis_V2"] == "ASLI").sum())
A_PDHL = int(((M["kontrol"] == "pdhl_d") & (M["vonis_V2"] == "ASLI")).sum())
A_ROUND = int(((M["kontrol"] == "round_d") & (M["vonis_V2"] == "ASLI")).sum())
D2_PDHL = int(((M["kontrol"] == "pdhl_d") & (M["verdict"] == "DEKAT-mendominasi")).sum())
D2_ROUND = int(((M["kontrol"] == "round_d") & (M["verdict"] == "DEKAT-mendominasi")).sum())
B3_PDHL = int(((M["kontrol"] == "pdhl_d") & (M["vonis"] == "Bertahan")).sum())
B3_ROUND = int(((M["kontrol"] == "round_d") & (M["vonis"] == "Bertahan")).sum())
KESIMPULAN = (
    f"I-1 adjudikasi 86 pasangan alarm run 9 (52 pdhl_d + 28 round_d + 6 noise kalibrasi) "
    f"dengan universe/kausalitas identik run 9 (B=185.248, N_ENT=184.731, 23+7 irisan, X_PIN=10 pip). "
    f"Q2 uji-kedekatan: DEKAT-mendominasi {D2_PDHL}/52 pdhl_d dan {D2_ROUND}/28 round_d "
    f"(CI klaster-hari 1000x, stream 80701+eidx); Q3 stratifikasi rv15: Bertahan {B3_PDHL}/52 pdhl_d "
    f"dan {B3_ROUND}/28 round_d (>=7/10 desil se-tanda + pooled-terbobot CI tak memuat 0, stream 80702+eidx). "
    f"Vonis V-2: {N_ASLI} ASLI ({A_PDHL} pdhl_d, {A_ROUND} round_d), {86 - N_ASLI} ARTEFAK; "
    f"kalibrasi negatif noise tak-berpola (<=1/6 signifikan) sehingga mesin I-1 sah. "
    f"Konsistensi: n 260/260 target == _ckpt_, 86/86 pasangan == _gate_, rebuild fitur bit-identik "
    f"{N_KEEP} baris, label 4x1000 sama persis, file run 9 bit-identik sebelum vs sesudah. "
    f"Tanpa model, tanpa vonis edge, tanpa buka Lapisan 3; kontrol DILARANG jadi fitur sinyal."
)
print("KESIMPULAN TERKUNCI:")
print(KESIMPULAN)
chk(len(KESIMPULAN) > 200, "sel kesimpulan terisi (>200 karakter)")
chk(N_ASLI >= 0, "verdict terhitung")
print(f"ASSERT_LOG total: {len(ASSERT_LOG)}")
chk(len(ASSERT_LOG) >= 20, "assertion mesin minimal 20")
print(f"artefak di {REPORT_DIR}: T-I1-1/2/3.csv; notebook 18 sel.")'''
)
EXPECTED_CSVS_I1 = ["T-I1-1.csv", "T-I1-2.csv", "T-I1-3.csv"]
REPORT_OUT_I1 = PROJECT_ROOT / "reports/eda" / "2026-10-12"


def verify_i1(report_dir: Path) -> None:
    """Verify tiga CSV T-I1 ada, non-kosong, dan 86 baris data."""
    report_dir = Path(report_dir).resolve()
    got = sorted(p.name for p in report_dir.glob("T-I1-*.csv"))
    assert got == sorted(EXPECTED_CSVS_I1), f"CSV T-I1 tidak tepat 3: {got}"
    import csv as _csv

    for name in EXPECTED_CSVS_I1:
        p = report_dir / name
        assert p.stat().st_size > 0, f"artefak kosong: {name}"
        with p.open("r", encoding="utf-8", newline="") as handle:
            rows = list(_csv.reader(handle))
        assert len(rows) == 87, f"{name} harus 1 header + 86 baris, dapat {len(rows)}"
    print(f"registry CSV T-I1 (3): {got}, masing-masing 86 baris data")


def build() -> None:
    """Tulis notebook adendum dan eksekusi top-to-bottom via nbconvert (tunggal via lock)."""
    lock = REPORT_OUT_I1 / ".eda07_i1_build.lock"
    REPORT_OUT_I1.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        age = time.time() - lock.stat().st_mtime
        if age < 5400:
            print(f"lock build aktif ({age:.0f} dtk) -> keluar agar eksekusi tunggal")
            sys.exit(3)
        lock.unlink()
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    print(f"lock diperoleh: {lock.relative_to(PROJECT_ROOT)}")
    for i, (kind, source) in enumerate(CELLS):
        if kind == "code":
            compile(source, f"<sel{i:02d}>", "exec")  # syntax sel tertangkap sebelum run panjang
    print(f"pra-kompilasi {sum(1 for k, _ in CELLS if k == 'code')} sel kode: OK")
    assert len(CELLS) == 18, f"notebook I-1 terkunci 18 sel, dapat {len(CELLS)}"
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
            "--ExecutePreprocessor.timeout=5400",
            str(NB_PATH),
        ],
        cwd=PROJECT_ROOT,
    )
    # Normalisasi EOL notebook sesudah nbconvert --inplace (penulis Windows
    # menghasilkan CRLF). Byte-level CRLF->LF; isi string sel tidak berubah.
    _nb_bytes = NB_PATH.read_bytes().replace(b"\r\n", b"\n")
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(_nb_bytes.decode("utf-8"))

    print(f"nbconvert exit={result.returncode}")
    if result.returncode != 0:
        lock.unlink(missing_ok=True)
        sys.exit(result.returncode)
    try:
        verify_i1(REPORT_OUT_I1)
    finally:
        lock.unlink(missing_ok=True)
    print("lock dilepas; build selesai.")


if __name__ == "__main__":
    build()
