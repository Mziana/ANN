"""Generator + executor for notebooks/scalping/eda_07_l31_baseline.ipynb.

L3-1 baseline-vs-null (B-3 + Amandemen C mengikat bersama):
67 baris diskret = M3 B-3 utuh (Brier margin 0,001 + menang per-semester
+ akurasi, aturan prediksi C-3); 36 baris LB_rng kontinu = M3-kontinu C-2
(MSE margin relatif 1% + menang per-semester + MAE; null = mean global,
baseline = mean per-iris; Brier/akurasi DILARANG untuk baris ini).
Split waktu terkunci train 2023H2-2024H2 / test 2025H1+2025H2, tanpa
shuffle lintas batas, tanpa RNG selain stream noise run 9 (tanpa
bootstrap; SEEDL31 tak dipakai karena CI tak dihitung).

Reuse-first: harness builder + eksekutor nbconvert + verify_registry dari
scripts/_build_eda07_l30.py; konstruksi label per-bar VERBATIM run 9
(sel02-07 + sel10-11 kode label run 9; sel08-09 simulator LA DIHILANGKAN
sebagai wiring karena S3-3 melarang target LA dan jalur T-target tak
memakainya; sel12+ mesin MI/lift DIHILANGKAN kecuali literal YCODE/YPOS);
assoc_irisan + CAND_TOKYO + K24 verbatim builder L3-0 (sudah diaudit);
bukti verbatim = jangkar T-07-1 200/200 (n eksak + kelas eksak +
fraksi 1e-4) + hash source sel run 9.

AGENTS.md S15.1 generator exemption applies (template file, stable refs,
deterministik: RNG hanya stream noise verbatim run 9, assertion machines
di notebook + verify_registry builder-side).
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_07_l31_baseline.ipynb"
REPORT_OUT_L31 = PROJECT_ROOT / "reports/eda" / "2026-10-12"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


# sel 00 (markdown: kontrak L3-1)
md(
    """# L3-1 - Baseline vs null, 103 pasangan (B-3 + Amandemen C)

Notebook **prediktif-deskriptif** B-3 putusan-l30-audit + Amandemen C
(amandemen-l31-metrik.md C-1..C-4): baseline vs null-model, split waktu
terkunci, M3 assert mesin. BUKAN strategi, BUKAN backtest, BUKAN P&L,
tanpa klaim edge, tanpa vonis dagang (S8A: ronde berakhir dengan TABEL
M3; vonis dagang wewenang arsitek+user pasca-audit).

Aturan mengikat: 67 diskret (LB_bin/LC1/LC2/LD) = Brier + akurasi,
null = mayoritas-kelas train global (pooled kind+N), M3 (a) Brier_mod <
Brier_null - 0,001 pooled, (b) menang di 2025H1 DAN 2025H2, (c)
akr_mod >= akr_null; prediksi kelas = argmax marginal per-iris, tie ->
mayoritas global, masih tie -> indeks terendah (C-3). 36 kontinu
(LB_rng) = MSE primer + MAE sekunder, null = mean train global,
baseline = mean train per-iris, M3-kontinu (a) MSE_mod < MSE_null x
0,99 pooled, (b) menang per-semester, (c) MAE_mod < MAE_null;
Brier/akurasi DILARANG untuk baris ini (C-2). Binarisasi LB_rng,
bin-20-sebagai-kelas, MSE-sebagai-Brier, drop-36 DITOLAK permanen
(C-3). Label per-bar VERBATIM run 9 (jangkar T-07-1 200/200 di sel 4).
Split: train 2023H2+2024H1+2024H2, test 2025H1+2025H2 (S6 assert
max-train < min-test). 5 baris round_d Tokyo: M3 WAJIB identik kembaran
native (assert konsistensi C-3). Kolom pagar punya_round_d_invers (T-5)
+ metrik_jenis + vonis. FIG-18 dua panel terpisah (DILARANG banding
Brier vs MSE lintas jenis). Manifest BERKOLOM path (T-1). Redaksi baku:
"transcription-guard, dikonfirmasi independen 24/24 vs source run 9;
bukan bukti komputasi" (T-2). Runner-log via redirect (T-6)."""
)


# sel 01 (code: setup VERBATIM sel02 run 9 + wiring OUT + snapshot mtime)
code(
    '''# __VERBATIM_BEGIN sel01__
# Kontrak Notebook 07 - dicetak verbatim sebagai output pertama (wajib).
KONTRAK_07 = """- Holdout: data 2026 TIDAK dimuat sama sekali. Asersi max(utc) < 2026-01-01; bar tepi hari-broker dibuang, jumlah dicetak (jangkar EDA-06: 0 bar).
- Universe: strata A + B 2023-2025 minus C; B = 185.248 di-assert; 5 semester A; tanpa Off di A. Jangkar silang EDA-06: 1.078.001 bar, N_ENT 184.731.
- Scope: 23 irisan (combo x sesi x tercile) + 7 irisan (combo x sesi) dari T-06-7 (LOLOS=True); assert 23 dan 7, STOP bila berubah. 50/70, 30/45, NewYork/Sydney-nonlolos hanya pembanding deskriptif.
- Label (S3, dikunci): LA barrier-hit per sisi (combo irisan itu, SL = k x ATR min 0,5 pip, bar-kembar = SL pesimis); LB biner |gerak N| > biaya-stres + 0,20 pip + kontinu range-N; LC 3-kelas theta 1x/2x biaya-stres; LD tanda (pembanding). N = 5/15/30/60, sampel tanpa tumpang-tindih, jendela lewati gap/anomali dibuang per alasan.
- Fitur (S4, daftar tertutup, semua t <= entry): rv15, rv60, atr_m5, atr_m15, vol_ratio, min_lon_open, min_ny_open, hour_sin, hour_cos, weekday, tokyo_fix, ret_1/5/15/60, ema20_d_atr, ema60_d_atr, z60, m5_ret, m5_pos, m15_ret, m15_pos, h1_ret, h1_pos, h1_ema_slope, spread + KONTROL wajib noise/round_d/pdhl_d.
- Metode (S5): MI 20 kuantil + lantai derau (permutasi blok-hari 100x, p95); lift per desil + CI bootstrap klaster-hari; Spearman kontinu; redundansi |rho|>0,8 satu wakil (non-kontrol diutamakan, lalu MI maks).
- Stabilitas (S6): MI + arah lift per semester/sesi/strata; B terpisah tidak menentukan; pola satu-slice bukan klaim umum; Tokyo/London terkonsentrasi = tiap klaim menyebut irisan eksplisit.
- Anti-leakage (S7): 200 timestamp acak, hitung-ulang SEMUA fitur dari data s.d. T, assert_allclose rtol=1e-9; satu gagal = HIGH, STOP.
- Gerbang (S8 + Amandemen A-3, per irisan x label): G1 balance (biner 10-90%, 3-kelas minoritas >= 10%; kontinu: n>=1000 dan hari>=100); G2-revisi = G2a (MI pooled n_tot > lantai pooled p95 pada n_tot yang sama) DAN G2b (arah lift sama >=4/5 semester, tanpa banding MI); G3 lift desil-atas vs bawah CI tak memuat 0 (pooled); G4 (khusus LA) lift TP-duluan desil-atas vs laju-dasar >= delta_normal irisan DAN lift-stres >= 0 (memadai). Gagal G2/G4 = BERHENTI irisan itu.
- Determinisme (P-5/S8): SATU stream RNG per target-analisis, seed = basis + indeks-target (tercatat di sel parameter); iterasi grup terurut (target, semester); urutan draw = blok-lantai {target, perm 0..99, tiap draw = permutasi-hari lalu acak-dalam-blok, seluruh fitur sekaligus}, blok-lift {target, fitur, draw}, blok-kontrol {target+10000}; rerun bit-identik di-assert; CI tak-stabil = gerbang MOOT.
- Aturan kontrol (pra-registrasi + A-3/A-4): kontrol di atas lantai pooled individual = variasi null yang diharapkan (lantai = p95); ALARM STOP hanya bila kontrol lolos kriteria G2-revisi (G2a pooled + G2b arah, IDENTIK fitur). Kontrol struktural lolos = temuan adjudikasi arsitek (A-4), DILARANG abaikan/pisahkan diam-diam. Laju lolos kontrol pooled dilaporkan sebagai kalibrasi (harapan ~= 5%).
- Agregasi verdict (pra-registrasi): verdict per (irisan x label); irisan LOLOS bila >=1 label lolos G1-G4 penuh; rekomendasi = (irisan x label x fitur) wakil pasca-redundansi.
- Fig ilustratif (pra-registrasi): FIG pakai irisan berperingkat-t verdict-terbanyak, seri delta_normal terendah; target = label lolos-pertama, bila nihil = target MI-tertinggi.
- Catatan konflik-tercatat (bukan improvisasi diam-diam): putusan P-5.4 melarang gerbang bergantung CI, spec S8-G3 memakai CI; dipatuhi keduanya: scope-K dari CSV tanpa CI + G3-CI deterministik (seed terkunci, rerun di-assert) + klausul MOOT S8 bila CI tak stabil. Rincian di laporan S5."""
print(KONTRAK_07)
# __VERBATIM_END sel01__
# __VERBATIM_BEGIN sel02__
import importlib.metadata
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

# Satu stream RNG per target-analisis (P-5/S8); basis + indeks-target, tercatat.
SEED07 = {"noise": 70701, "leak": 70702, "floor_base": 70703, "lift_base": 70704, "atr_check": 70705,
          "stab_base": 70800}


def new_rng(name: str, idx: int = 0) -> np.random.Generator:
    """Stream RNG terkunci untuk blok analisis (nama, indeks tercatat di pemanggil)."""
    base = SEED07[name] if idx == 0 else SEED07[name] + idx
    return np.random.default_rng(base)


def show(df: pd.DataFrame, title: str) -> None:
    """Cetak tabel penuh sebagai teks agar tersimpan di output notebook."""
    print(title)
    print(df.to_string())
    print()
# __VERBATIM_END sel02__

# --- L3-1 wiring (bukan label): direktori + snapshot mtime file beku/L3-0 (S8B) ---
REPORT_10 = PROJECT_ROOT / "reports/eda" / "2026-10-12"
REPORT_10 = PROJECT_ROOT / "reports/eda" / "2026-10-10"
OUT = PROJECT_ROOT / "reports/eda" / "2026-10-12"
OUT.mkdir(parents=True, exist_ok=True)
FROZEN_WATCH = [OUT / "T-07-1_balance.csv", OUT / "T-07-2_mi_lantai.csv",
                OUT / "T-07-3_lift.csv", OUT / "T-07-4_stabilitas.csv",
                OUT / "_gate_G2_alarm.csv", REPORT_10 / "T-06-7_gerbang_tercile.csv",
                REPORT_10 / "T-06-7_gerbang_sesi.csv", OUT / "T-L3-0_arah.csv",
                OUT / "T-L3-0_peta98.csv", OUT / "_l30_manifest.csv",
                OUT / "FIG-17_peta_arah.png"]
MTIME_PRE = {str(p): (p.stat().st_size, p.stat().st_mtime_ns) for p in FROZEN_WATCH}
print(f"snapshot pra-eksekusi S8B: {len(MTIME_PRE)} file (size, mtime_ns)")
print("L3-1: RNG hanya stream noise verbatim run 9 (sel11); tanpa bootstrap/CI (SEEDL31 tak dipakai).")'''
)


# sel 02 (code: parameter/load/scope VERBATIM sel03-05 run 9 + K24)
code(
    '''# __VERBATIM_BEGIN sel03__
"""Parameter terkunci (diubah HANYA sebelum menjalankan, tidak sesudah melihat hasil)."""
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
SCENARIOS = {"normal": COST_NORMAL, "stres": COST_STRESS}

# Label waktu
N_HORIZONS = (5, 15, 30, 60)
LB_MARGIN_PIP = 0.20
LC_MULTS = (1.0, 2.0)

# Barrier LA (warisan EDA-06)
HORIZON = 120
STRIDE = 5

# Metode S5
MI_BINS = 20
N_PERM = 100
N_BOOT = 1000
N_LEAK = 200
RHO_DROP = 0.8

# Gerbang S8
# Gerbang S8 (pra-registrasi)
G1_BIN_LO, G1_BIN_HI = 0.10, 0.90
G1_MIN_CLASS = 0.10
G1_CONT_MIN_N, G1_CONT_MIN_DAYS = 1000, 100
G2_MIN_SEM = 4
G4_STRESS_MIN_PP = 0.0  # memadai = lift-stres tidak negatif (kolom sensitivitas)

REPORT_DIR = PROJECT_ROOT / "reports/eda" / "2026-10-10"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
MID_FIGURE_DIR = PROJECT_ROOT / "reports/eda" / "2026-10-10"  # baca T-06-7 (sama lokasi)
OLD_FIGURE_DIR = PROJECT_ROOT / "reports/eda" / "2026-10-06" / "figures"  # registry FIG-01..07

print(f"symbol={SYMBOL} | pip={PIP_SIZE} | tahun={YEARS} | holdout >= {HOLDOUT_START:%Y-%m-%d}")
print("cost normal :", COST_NORMAL)
print("cost stres  :", COST_STRESS)
print(f"label N={N_HORIZONS} | LB margin={LB_MARGIN_PIP} pip | LC mult={LC_MULTS}")
print(f"LA: HORIZON={HORIZON} mnt, STRIDE={STRIDE}")
print(f"metode: MI_bins={MI_BINS}, perm={N_PERM}, boot={N_BOOT}, leak={N_LEAK}")
print(f"gerbang: G1 biner [{G1_BIN_LO},{G1_BIN_HI}] 3-kelas min {G1_MIN_CLASS} | G2-revisi A-3: G2a pooled-vs-pooled + G2b arah >= {G2_MIN_SEM}/5 sem | G4 stres-min {G4_STRESS_MIN_PP} pp")
print("SEED07:", SEED07)
print("laporan ->", REPORT_DIR)
chk(set(SESSIONS) == set(COST_NORMAL) == set(COST_STRESS), "sesi config harus 4 sesi", loud=True)
# __VERBATIM_END sel03__

# --- L3-1 wiring: K24 literal (nilai verbatim, format checklist L3-0 yang sudah diaudit) ---
K24 = [("N_HORIZONS", N_HORIZONS, (5, 15, 30, 60)), ("LB_MARGIN_PIP", LB_MARGIN_PIP, 0.20),
       ("LC_MULTS", LC_MULTS, (1.0, 2.0)), ("HORIZON", HORIZON, 120), ("STRIDE", STRIDE, 5),
       ("MI_BINS", MI_BINS, 20), ("N_PERM", N_PERM, 100), ("N_BOOT", N_BOOT, 1000),
       ("N_LEAK", N_LEAK, 200), ("RHO_DROP", RHO_DROP, 0.8),
       ("G1_BIN_LO", G1_BIN_LO, 0.10), ("G1_BIN_HI", G1_BIN_HI, 0.90),
       ("G1_MIN_CLASS", G1_MIN_CLASS, 0.10), ("G1_CONT_MIN_N", G1_CONT_MIN_N, 1000),
       ("G1_CONT_MIN_DAYS", G1_CONT_MIN_DAYS, 100), ("G2_MIN_SEM", G2_MIN_SEM, 4),
       ("G4_STRESS_MIN_PP", G4_STRESS_MIN_PP, 0.0),
       ("SEED_noise", SEED07["noise"], 70701), ("SEED_leak", SEED07["leak"], 70702),
       ("SEED_floor", SEED07["floor_base"], 70703), ("SEED_lift", SEED07["lift_base"], 70704),
       ("SEED_atr", SEED07["atr_check"], 70705), ("SEED_stab", SEED07["stab_base"], 70800),
       ("YEARS", YEARS, (2023, 2024, 2025))]
chk(len(K24) == 24, "tepat 24 konstanta terkunci")
for nm, got, exp in K24:
    chk(got == exp, f"konstanta {nm} == {exp!r}")
print("PASS: 24/24 konstanta run 9 identik (nol drift).")

# __VERBATIM_BEGIN sel04__
"""Muat M1 2023-2025, bentuk strata A/B/C, siapkan array numpy (pola EDA-06)."""
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
chk(int(DAY_ARR.max()) + 1 == int(m1["broker_day"].nunique()), "paritas hari-broker")
# __VERBATIM_END sel04__

# __VERBATIM_BEGIN sel05__
"""Scope irisan dari CSV T-06-7 (assert 23 + 7, STOP bila berubah)."""
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
# __VERBATIM_END sel05__'''
)


# sel 03 (code: ATR + entri + label + fitur VERBATIM sel06/07/10/11 run 9)
code(
    '''# __VERBATIM_BEGIN sel06__
"""ATR M5(14) + M15(14) kausal (bar TF SELESAI) + uji anti look-ahead."""


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
print("PASS: ATR 12 timestamp hitung-ulang identik (tanpa look-ahead).")
# __VERBATIM_END sel06__

# __VERBATIM_BEGIN sel07__
"""Basis entri stride-5 (aturan identik EDA-06) + tercile ATR per sesi."""
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
chk(set(np.unique(ENT_TER)) == {1, 2, 3}, "tercile 1..3 lengkap")
# __VERBATIM_END sel07__

# __VERBATIM_BEGIN sel10__
"""Label waktu LB/LC/LD per N (sampel tanpa tumpang-tindih + buang jendela gap/anomali)."""
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
print(f"target waktu: {len(TLAB)} (sesskey x N x jenis)")
# __VERBATIM_END sel10__

# __VERBATIM_BEGIN sel11__
"""Fitur kausal 29 kolom (semua t <= entry) + drop NaN tercatat."""


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
# __VERBATIM_END sel11__'''
)


# sel 04 (code: YCODE/YPOS + jangkar 200/200 + register 103 + split + M3 + CSV)
code(
    '''"""YCODE/YPOS verbatim sel12 run 9 + jangkar T-07-1 + register 103 + M3 + CSV."""
# Kode-y per jenis label (pra-registrasi, tetap) -- VERBATIM sel12 run 9
# (hanya literal; mesin MI/lift sel12 tidak dipakai L3-1)
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
print("YCODE/YPOS verbatim sel12 run 9 dimuat (L3-1 memakai YCODE diskret; YPOS tak dipakai).")

# TER_IDS/SES_IDS + assoc_irisan -- VERBATIM builder L3-0 sel02 (sudah diaudit = run 9 sel16)
TER_IDS = [(r["combo"], r["session"], int(r["atr_ter_s"])) for _, r in IR_TER.iterrows()]
SES_IDS = [(r["combo"], r["session"]) for _, r in IR_SES.iterrows()]


def assoc_irisan(key: str):
    """Irisan EDA-06 yang menaungi target (LA -> irisannya; waktu -> semua irisan se-sesskey)."""
    if key.startswith("LA "):
        _, combo, sess, tside = key.split(" ", 3)
        tval = tside.rsplit(" ", 1)[0][1:]
        if tval == "ALL":
            return [("ses", combo, sess, 0)]
        return [("ter", combo, sess, int(tval))]
    _, sess, tN = key.split(" ", 2)
    tval = tN.rsplit(" ", 1)[0][1:]
    if tval == "ALL":
        return [("ses", c, s, 0) for c, s in SES_IDS if s == sess]
    return [("ter", c, s, int(tval)) for c, s, t in TER_IDS if s == sess and t == int(tval)]


# --- Jangkar T-07-1: seluruh 200 target waktu (n eksak + kelas eksak + fraksi 1e-4) ---
t1 = pd.read_csv(OUT / "T-07-1_balance.csv")
chk(len(t1) == 260, "T-07-1 beku 260 baris")
t1map = dict(zip(t1["target"], range(len(t1))))
chk(len(TLAB) == 200, "TLAB tepat 200 (sesskey x N x 5 jenis)")
n_anchor = 0
for (sess, ter, N, kd) in sorted(TLAB.keys(), key=lambda k: (k[3], k[0], str(k[1]), k[2])):
    name = f"{kd} {sess} t{ter} N{N}"
    chk(name in t1map, f"jangkar {name} ada di T-07-1")
    row = t1.iloc[t1map[name]]
    v, vals = TLAB[(sess, ter, N, kd)]
    yf = np.full(N_ENT, np.nan)
    yf[v] = vals
    m = v & KEEP
    if kd == "LD":
        m &= yf != 9  # VERBATIM sel15 run 9: LD mengeluarkan flat-9
    chk(int(m.sum()) == int(row["n"]), f"jangkar n {name}")
    if kd == "LB_rng":
        chk(str(row["kelas"]) == "kontinu", f"jangkar kelas kontinu {name}")
    else:
        yy = yf[m].astype(np.int64)
        cls, cnt = np.unique(yy, return_counts=True)
        chk("|".join(str(c) for c in cls) == str(row["kelas"]), f"jangkar kelas {name}")
        fr = cnt / cnt.sum()
        froz = [float(x) for x in str(row["fraksi"]).split("|")]
        chk(len(froz) == len(fr) and all(abs(a - b) < 1e-4 for a, b in zip(froz, fr)),
            f"jangkar fraksi {name}")
    n_anchor += 1
print(f"PASS: jangkar T-07-1 {n_anchor}/200 target waktu (n eksak, kelas eksak, fraksi 1e-4).")

# --- Register 103: 98 native peta98 + 5 Tokyo round_d (neg) ---
PE = pd.read_csv(OUT / "T-L3-0_peta98.csv")
AR = pd.read_csv(OUT / "T-L3-0_arah.csv")
chk(len(PE) == 98, "peta98 beku 98 baris (re-read)")
chk(len(AR) == 153, "arah beku 153 baris (re-read)")
CAND_TOKYO = {
    "LB_bin Tokyo t2 N15": -0.0473,
    "LB_bin Tokyo tALL N5": -0.0549,
    "LB_rng Tokyo tALL N5": -0.7446,
    "LB_bin Tokyo tALL N15": -0.0279,
    "LB_rng Tokyo tALL N15": -1.5868,
}
tok = AR[(AR["fitur"] == "round_d") & (AR["target"].isin(CAND_TOKYO))]
chk(len(tok) == 5, "5/5 Tokyo hadir di set G3-pass")
for k, liftv in CAND_TOKYO.items():
    got = tok[tok["target"] == k]
    chk(len(got) == 1, f"Tokyo {k} unik di set")
    chk(bool(abs(float(got["lift"].iloc[0]) - liftv) < 1e-9 and float(got["lift"].iloc[0]) < 0),
        f"Tokyo {k} lift tepat {liftv} dan negatif")
REG_NATIVE = PE["target"].tolist()
REG_TOKYO = list(CAND_TOKYO.keys())
NATSET = set(REG_NATIVE)
for k in REG_TOKYO:
    chk(k in NATSET, f"kembaran native ada di peta98 untuk {k}")
REG = REG_NATIVE + REG_TOKYO
chk(len(REG) == 103, "register tepat 103 baris (98 native + 5 Tokyo)")
wakil_of = dict(zip(PE["target"], PE["wakil"]))
arah_of = dict(zip(PE["target"], PE["arah"]))
n_dis = sum(1 for k in REG if k.split(" ", 1)[0] != "LB_rng")
n_con = sum(1 for k in REG if k.split(" ", 1)[0] == "LB_rng")
chk(n_dis == 67 and n_con == 36, "split jenis 67 diskret + 36 kontinu")
print(f"PASS: register 103 = 98 native + 5 Tokyo (diskret={n_dis}, kontinu={n_con}).")


def parse_target(key: str):
    """Pecah nama target waktu -> (kind, sess, ter, N)."""
    kd, sess, tN = key.split(" ", 2)
    tpart, npart = tN.split(" ")
    ter = "ALL" if tpart == "tALL" else int(tpart[1:])
    return kd, sess, ter, int(npart[1:])


# --- Split waktu terkunci (S6: max-train < min-test, tanpa shuffle lintas batas) ---
chk(SEM_A == ["2023H2", "2024H1", "2024H2", "2025H1", "2025H2"], "SEM_A eksak 5 semester")
TRAIN_SEMS = SEM_A[:3]
H1S, H2S = SEM_A[3], SEM_A[4]
is_tr = np.isin(ENT_SEM, TRAIN_SEMS)
is_te = np.isin(ENT_SEM, [H1S, H2S])
chk(bool(is_tr.sum() > 0 and is_te.sum() > 0), "train dan test tak-kosong di level entri")
chk(int(UTC_NS[IDX[is_tr]].max()) < int(UTC_NS[IDX[is_te]].min()),
    "S6: max-train < min-test (tanpa bocor waktu)")
print(f"split: train {TRAIN_SEMS} (UTC {UTC_NS[IDX[is_tr]].min()}..{UTC_NS[IDX[is_tr]].max()}) | "
      f"test {[H1S, H2S]} (UTC {UTC_NS[IDX[is_te]].min()}..{UTC_NS[IDX[is_te]].max()})")


def brier_score(P: np.ndarray, y_enc: np.ndarray, axis: np.ndarray) -> float:
    """Brier multikelas C-2: rerata kuadrat galat probabilitas atas semua kelas + entri."""
    idx = np.searchsorted(axis, y_enc)
    O = np.zeros((len(y_enc), len(axis)))
    O[np.arange(len(y_enc)), idx] = 1.0
    return float((((P[None, :] - O) ** 2).mean()))


# Aturan prediksi C-3 + unit determinisme tie (assert mesin, data sintetis).
# np.argmax pada sumbu terurut = argmax, tie -> indeks pertama = kelas terendah.
_axis_u = np.array([0, 1, 2])
chk(int(_axis_u[int(np.argmax(np.array([0.5, 0.5, 0.0])))]) == 0, "C-3 tie marginal+global -> indeks terendah")
chk(int(_axis_u[int(np.argmax(np.array([0.2, 0.5, 0.3])))]) == 1, "C-3 argmax marginal desisif")
chk(int(_axis_u[int(np.argmax(np.array([0.0, 0.0, 1.0])))]) == 2, "C-3 argmax tunggal")
print("PASS: unit C-3 (argmax/tie) 3/3.")

ROWS = []
for key in REG:
    kd, sess, ter, N = parse_target(key)
    v, vals = TLAB[(sess, ter, N, kd)]
    yf = np.full(N_ENT, np.nan)
    yf[v] = vals
    mt = v & KEEP
    if kd == "LD":
        mt &= yf != 9
    semt = ENT_SEM[mt]
    mtr = np.isin(semt, TRAIN_SEMS)
    mh1 = semt == H1S
    mh2 = semt == H2S
    chk(bool(mtr.sum() > 0 and mh1.sum() > 0 and mh2.sum() > 0), f"sampel train/H1/H2 tak-kosong ({key})")
    if kd == "LB_rng":
        # M3-kontinu C-2: null = mean train global (pooled kind+N), baseline = mean train per-iris.
        G = np.zeros(N_ENT, dtype=bool)
        for (s2, t2, N2, k2), (v2, _vv) in TLAB.items():
            if N2 == N and k2 == kd:
                G |= v2
        G &= KEEP
        yG = TL[(N,)]["rng"][G]
        semG = ENT_SEM[G]
        null_c = float(yG[np.isin(semG, TRAIN_SEMS)].mean())
        mod_c = float(yf[mt][mtr].mean())
        yte = yf[mt]
        mse_mod = float((((yte[mh1 | mh2] - mod_c) ** 2).mean()))
        mse_null = float((((yte[mh1 | mh2] - null_c) ** 2).mean()))
        mse_mod_h1 = float((((yte[mh1] - mod_c) ** 2).mean()))
        mse_null_h1 = float((((yte[mh1] - null_c) ** 2).mean()))
        mse_mod_h2 = float((((yte[mh2] - mod_c) ** 2).mean()))
        mse_null_h2 = float((((yte[mh2] - null_c) ** 2).mean()))
        mae_mod = float(np.abs(yte[mh1 | mh2] - mod_c).mean())
        mae_null = float(np.abs(yte[mh1 | mh2] - null_c).mean())
        chk(mse_null > 0, f"MSE_null > 0 ({key})")
        a = bool(mse_mod < mse_null * 0.99)
        b = bool(mse_mod_h1 < mse_null_h1 and mse_mod_h2 < mse_null_h2)
        c = bool(mae_mod < mae_null)
        ROWS.append({"target": key, "kind": kd, "sess": sess, "ter": ter, "N": N,
                     "M1": True, "jenis_target": "kontinu", "metrik_jenis": "mse",
                     "n_train": int(mtr.sum()), "n_test_h1": int(mh1.sum()), "n_test_h2": int(mh2.sum()),
                     "baseline": "mean-per-iris", "nullmodel": "mean-global",
                     "metrik_mod_pooled": mse_mod, "metrik_null_pooled": mse_null,
                     "lolos_a": a, "menang_h1": bool(mse_mod_h1 < mse_null_h1),
                     "menang_h2": bool(mse_mod_h2 < mse_null_h2),
                     "sekunder_mod": mae_mod, "sekunder_null": mae_null,
                     "sekunder_jenis": "mae", "lolos_c": c,
                     "vonis": ("LOLOS" if (a and b and c) else "GUGUR")})
    else:
        # M3 B-3 utuh: null = mayoritas-kelas train global (pooled kind+N, C-3 tie -> terendah).
        G = np.zeros(N_ENT, dtype=bool)
        for (s2, t2, N2, k2), (vv2, vals2) in TLAB.items():
            if N2 == N and k2 == kd:
                if kd == "LD":
                    yf2 = np.full(N_ENT, np.nan)
                    yf2[vv2] = vals2
                    G |= vv2 & (yf2 != 9)
                else:
                    G |= vv2
        G &= KEEP
        yG = TL[(N,)]["move"][G]
        ye_G = YCODE[kd](yG)
        semG = ENT_SEM[G]
        ye_tr = ye_G[np.isin(semG, TRAIN_SEMS)]
        axis = np.unique(ye_tr)
        chk(len(axis) > 0, f"sumbu kelas tak-kosong ({key})")
        cnt = np.array([(ye_tr == cc).sum() for cc in axis])
        maj = axis[int(np.argmax(cnt))]  # tie -> kelas terendah (sumbu terurut)
        ye_t = YCODE[kd](yf[mt])
        Ptr = np.array([(ye_t[mtr] == cc).sum() for cc in axis]) / float(mtr.sum())
        pred_mod = axis[int(np.argmax(Ptr))]
        P_mod = Ptr
        P_null = (axis == maj).astype(float)
        for _twice in range(2):  # assert mesin determinisme tie: hitung-ulang identik
            _cnt2 = np.array([(ye_tr == cc).sum() for cc in axis])
            _Ptr2 = np.array([(ye_t[mtr] == cc).sum() for cc in axis]) / float(mtr.sum())
            chk(bool((_cnt2 == cnt).all() and np.allclose(_Ptr2, Ptr)),
                f"determinisme tie ({key})")
        yte = ye_t[mh1 | mh2]
        b_mod = brier_score(P_mod, yte, axis)
        b_null = brier_score(P_null, yte, axis)
        b_mod_h1 = brier_score(P_mod, ye_t[mh1], axis)
        b_null_h1 = brier_score(P_null, ye_t[mh1], axis)
        b_mod_h2 = brier_score(P_mod, ye_t[mh2], axis)
        b_null_h2 = brier_score(P_null, ye_t[mh2], axis)
        acc_mod = float((((yte == pred_mod)).sum()) / len(yte))
        acc_null = float((((yte == maj)).sum()) / len(yte))
        a = bool(b_mod < b_null - 0.001)
        b = bool(b_mod_h1 < b_null_h1 and b_mod_h2 < b_null_h2)
        c = bool(acc_mod >= acc_null)
        ROWS.append({"target": key, "kind": kd, "sess": sess, "ter": ter, "N": N,
                     "M1": True, "jenis_target": "diskret", "metrik_jenis": "brier",
                     "n_train": int(mtr.sum()), "n_test_h1": int(mh1.sum()), "n_test_h2": int(mh2.sum()),
                     "baseline": "marginal-per-iris", "nullmodel": "mayoritas-global",
                     "metrik_mod_pooled": b_mod, "metrik_null_pooled": b_null,
                     "lolos_a": a, "menang_h1": bool(b_mod_h1 < b_null_h1),
                     "menang_h2": bool(b_mod_h2 < b_null_h2),
                     "sekunder_mod": acc_mod, "sekunder_null": acc_null,
                     "sekunder_jenis": "akurasi", "lolos_c": c,
                     "vonis": ("LOLOS" if (a and b and c) else "GUGUR")})
print(f"M3 selesai: {len(ROWS)} baris.")

# --- Pagar T-5/B-2: punya_round_d_invers (aturan coder, terdokumentasi di laporan) ---
T5_LIFTS = [0.4162, 11.9112, 0.2722, 19.3823, 13.8349, 14.1417]
big = AR[AR["lift"].apply(lambda x: any(abs(float(x) - bb) < 1e-9 for bb in T5_LIFTS))]
chk(len(big) == 6, "T-5 tepat 6 baris big-lift (4 Tokyo + 2 London)")
T5_TARGETS = set(big["target"].tolist()) | set(REG_TOKYO)
chk(len(T5_TARGETS) == 7, "pagar T-5 menaungi 7 target unik")
print(f"target pagar T-5: {sorted(T5_TARGETS)}")

RES = pd.DataFrame(ROWS)
chk(REG[98:] == REG_TOKYO, "posisi register 98..102 = 5 Tokyo (tertib REG_NATIVE + REG_TOKYO)")
RES["wakil"] = RES["target"].map(wakil_of)
RES["arah"] = RES["target"].map(arah_of)
RES.loc[RES.index[98:], "wakil"] = "round_d"  # 5 baris Tokyo: wakil fitur round_d
RES.loc[RES.index[98:], "arah"] = "neg"  # 5 baris Tokyo: arah negatif (terdaftar)
RES["irisan"] = RES["target"].apply(lambda k: "|".join(str(i) for i in assoc_irisan(k)))
RES["punya_round_d_invers"] = RES["target"].apply(lambda k: bool(k in T5_TARGETS))
RES = RES[["target", "kind", "sess", "ter", "N", "wakil", "arah", "irisan", "M1",
           "jenis_target", "metrik_jenis", "punya_round_d_invers", "n_train",
           "n_test_h1", "n_test_h2", "baseline", "nullmodel", "metrik_mod_pooled",
           "metrik_null_pooled", "lolos_a", "menang_h1", "menang_h2",
           "sekunder_mod", "sekunder_null", "sekunder_jenis", "lolos_c", "vonis"]]
RES.to_csv(OUT / "T-L3-1_baseline.csv", index=False)
RE = pd.read_csv(OUT / "T-L3-1_baseline.csv")  # bukti re-read dari disk
chk(len(RE) == 103, "T-L3-1_baseline.csv tepat 103 baris (re-read)")
chk(set(RE["vonis"].unique().tolist()) <= {"LOLOS", "GUGUR"}, "vonis biner {LOLOS,GUGUR}")
chk(set(RE["metrik_jenis"].unique().tolist()) == {"brier", "mse"}, "metrik_jenis {brier,mse}")
chk(int((RE["jenis_target"] == "diskret").sum()) == 67, "67 baris diskret (re-read)")
chk(int((RE["jenis_target"] == "kontinu").sum()) == 36, "36 baris kontinu (re-read)")
chk(bool(RE["M1"].all()), "M1 True 103/103 (terdaftar + arah diketahui)")
chk(int(RE["punya_round_d_invers"].sum()) >= 5, "pagar T-5 menandai >=5 baris")

# --- Assert konsistensi C-3: M3 5 baris round_d = M3 kembaran native (label sama) ---
NUMCOLS = ["metrik_mod_pooled", "metrik_null_pooled", "sekunder_mod", "sekunder_null"]
for k in REG_TOKYO:
    dup = RE[RE["target"] == k]
    chk(len(dup) == 2, f"C-3 duplikat tepat 2 baris {k} (native + Tokyo)")
    rt = dup.iloc[1]  # baris Tokyo (posisi register 98..102)
    rn = dup.iloc[0]  # kembaran native (posisi register 0..97)
    for cc in NUMCOLS:
        chk(float(rt[cc]) == float(rn[cc]), f"C-3 M3 identik {k} [{cc}]")
    for cc in ["lolos_a", "menang_h1", "menang_h2", "lolos_c", "vonis"]:
        chk(str(rt[cc]) == str(rn[cc]), f"C-3 vonis identik {k} [{cc}]")
print("PASS: C-3 konsistensi 5 round_d = kembaran native (angka + vonis identik).")
lol_d = int(((RE["jenis_target"] == "diskret") & (RE["vonis"] == "LOLOS")).sum())
lol_c = int(((RE["jenis_target"] == "kontinu") & (RE["vonis"] == "LOLOS")).sum())
print(f"TAL intermediate: LOLOS diskret={lol_d}/67 kontinu={lol_c}/36 GUGUR={103 - lol_d - lol_c}.")
show(RE[["target", "metrik_jenis", "metrik_mod_pooled", "metrik_null_pooled",
         "sekunder_mod", "sekunder_null", "vonis"]].head(12), "T-L3-1_baseline.csv (12 pertama)")'''
)


# sel 05 (code: FIG-18 dua panel)
code(
    '''"""FIG-18: baseline vs null per jenis (panel terpisah; DILARANG banding lintas jenis)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

FE = pd.read_csv(OUT / "T-L3-1_baseline.csv")  # plot dari disk (re-read)
chk(len(FE) == 103, "FIG-18 mencakup penuh 103 baris")
D = FE[FE["metrik_jenis"] == "brier"].copy()
C = FE[FE["metrik_jenis"] == "mse"].copy()
chk(len(D) == 67 and len(C) == 36, "FIG-18 split 67/36")
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
for _ax, _df, _xl, _yl, _ti in (
    (ax[0], D, "Brier null (mayoritas-global)", "Brier baseline (marginal-per-iris)",
     "FIG-18a Brier 67 diskret (satuan Brier)"),
    (ax[1], C, "MSE null (mean-global)", "MSE baseline (mean-per-iris)",
     "FIG-18b MSE 36 kontinu (satuan pip^2; TAK sebanding panel-a)"),
):
    lol = _df[_df["vonis"] == "LOLOS"]
    gug = _df[_df["vonis"] == "GUGUR"]
    _ax.scatter(gug["metrik_null_pooled"], gug["metrik_mod_pooled"], s=18, label="GUGUR", alpha=0.7)
    _ax.scatter(lol["metrik_null_pooled"], lol["metrik_mod_pooled"], s=18, label="LOLOS", alpha=0.9)
    lo = float(min(_df["metrik_null_pooled"].min(), _df["metrik_mod_pooled"].min()))
    hi = float(max(_df["metrik_null_pooled"].max(), _df["metrik_mod_pooled"].max()))
    _ax.plot([lo, hi], [lo, hi], linestyle="--", linewidth=1)
    _ax.set_xlabel(_xl)
    _ax.set_ylabel(_yl)
    _ax.set_title(_ti)
    _ax.legend()
fig.suptitle("L3-1 baseline-vs-null (panel terpisah per jenis; DILARANG banding Brier vs MSE)")
fig.tight_layout()
fig.savefig(OUT / "FIG-18_baseline.png", dpi=100)
plt.close(fig)
print("FIG tersimpan: ['FIG-18_baseline.png']")'''
)


# sel 06 (code: manifest T-1 + S8B mtime + registry + K24 baku T-2)
code(
    '''"""Manifest _l31_manifest.csv (BERKOLOM path, T-1) + S8B mtime + registry beku + K24 baku."""
import hashlib

MANIFEST_SEBELUM = {
    "T-07-1_balance.csv": "7DFF3D15A78F1013E99B3ADF1152602EEDD28CFC0D76E33C8ACE1FA27BA50155",
    "T-06-7_gerbang_tercile.csv": "E03EA9AB070CC14A3658D30ADE1FD6C5FE47C51565C69D123D957AA097F34E51",
    "T-06-7_gerbang_sesi.csv": "2DD86BC709C2D06BEA104782E86ECDC3215B2BD7BF2814403EA0DFC8ABF7E385",
    "T-L3-0_arah.csv": "F48323D2C671C0FA963B2B2C940ADF3A1DB12B83C3080B5821793EE508344D1F",
    "T-L3-0_peta98.csv": "1F58D4DFE460CBCC7D436FCFD40401B0A6EE3F41AC13503C36BDD736D1BC95C5",
}
MANIFEST_PATHS = {
    "T-07-1_balance.csv": OUT / "T-07-1_balance.csv",
    "T-06-7_gerbang_tercile.csv": REPORT_10 / "T-06-7_gerbang_tercile.csv",
    "T-06-7_gerbang_sesi.csv": REPORT_10 / "T-06-7_gerbang_sesi.csv",
    "T-L3-0_arah.csv": OUT / "T-L3-0_arah.csv",
    "T-L3-0_peta98.csv": OUT / "T-L3-0_peta98.csv",
}
man_rows = []
for name, path in MANIFEST_PATHS.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    man_rows.append({"path": str(path.relative_to(PROJECT_ROOT)).replace(chr(92), "/"),
                     "file": name, "sha256_sebelum": MANIFEST_SEBELUM[name],
                     "sha256_aktual": actual, "cocok": bool(actual == MANIFEST_SEBELUM[name])})
for name in ("T-L3-1_baseline.csv", "FIG-18_baseline.png"):
    path = OUT / name
    man_rows.append({"path": str(path.relative_to(PROJECT_ROOT)).replace(chr(92), "/"),
                     "file": name, "sha256_sebelum": "NA (output)",
                     "sha256_aktual": hashlib.sha256(path.read_bytes()).hexdigest().upper(),
                     "cocok": True})
MANIFEST = pd.DataFrame(man_rows)
MANIFEST.to_csv(OUT / "_l31_manifest.csv", index=False)
show(MANIFEST, "MANIFEST L3-1 (path + SEBELUM vs aktual)")
chk(bool(MANIFEST[MANIFEST["sha256_sebelum"] != "NA (output)"]["cocok"].all()),
    "hash 5/5 input sama SEBELUM (bukti di _l31_manifest.csv)", loud=True)
chk("path" in MANIFEST.columns, "manifest BERKOLOM path (T-1)")

MTIME_POST = {str(p): (p.stat().st_size, p.stat().st_mtime_ns) for p in FROZEN_WATCH}
chk(MTIME_POST == MTIME_PRE, "S8B: 11 file beku/L3-0 TAK tersentuh (size+mtime identik pra/pasca)")
print("PASS: S8B mtime+size 11/11 identik.")

for _name, _exp in (("T-07-1_balance.csv", 260), ("T-07-2_mi_lantai.csv", 6767),
                    ("T-07-3_lift.csv", 1315), ("T-07-4_stabilitas.csv", 1335),
                    ("_gate_G2_alarm.csv", 86), ("T-L3-0_arah.csv", 153),
                    ("T-L3-0_peta98.csv", 98)):
    _df = pd.read_csv(OUT / _name)
    chk(len(_df) == _exp, f"registry {_name} {_exp} baris (tak berubah)")
print("PASS: registry 5 beku + 2 L3-0 utuh.")
print("transcription-guard, dikonfirmasi independen 24/24 vs source run 9; bukan bukti komputasi")'''
)


# sel 07 (code: kesimpulan + assert log)
code(
    '''"""Kesimpulan L3-1 satu paragraf (tanpa vonis dagang/edge; STOP setelah ini)."""
RE2 = pd.read_csv(OUT / "T-L3-1_baseline.csv")
ld = int(((RE2["jenis_target"] == "diskret") & (RE2["vonis"] == "LOLOS")).sum())
lc = int(((RE2["jenis_target"] == "kontinu") & (RE2["vonis"] == "LOLOS")).sum())
gd = int(((RE2["jenis_target"] == "diskret") & (RE2["vonis"] == "GUGUR")).sum())
gc = int(((RE2["jenis_target"] == "kontinu") & (RE2["vonis"] == "GUGUR")).sum())
KESIMPULAN_L31 = (
    f"L3-1 baseline-vs-null mengunci TABEL M3 103 pasangan (B-3 + Amandemen C): "
    f"67 diskret via Brier (null mayoritas-global pooled kind+N; M3 margin 0,001 + menang "
    f"2025H1&H2 + akurasi; prediksi argmax C-3) -> LOLOS {ld} / GUGUR {gd}; "
    f"36 kontinu LB_rng via MSE (null mean-global; M3 1% relatif + menang per-semester + MAE; "
    f"Brier/akurasi tidak dihitung) -> LOLOS {lc} / GUGUR {gc}. "
    f"Label per-bar VERBATIM run 9 (jangkar T-07-1 200/200 n+kelas+fraksi; C-3 twin 5 round_d "
    f"identik native); split train 2023H2-2024H2/test 2025H1+H2 tanpa bocor (max-train<min-test); "
    f"pagar T-5 menandai 7 target; FIG-18 dua panel tak-sebanding; hash 5/5 input sama; "
    f"S8B 11 file beku/L3-0 utuh; K24 24/24. "
    f"Satu-satunya keluaran: TABEL M3 (siapa kalahkan null). Tanpa vonis dagang, tanpa klaim "
    f"edge, tanpa P&L/backtest; vonis dagang wewenang arsitek+user pasca-audit L3-1.")
print("KESIMPULAN_L31 TERKUNCI:")
print(KESIMPULAN_L31)
chk(len(KESIMPULAN_L31) > 200, "sel kesimpulan terisi (>200 karakter)")
print(f"ASSERT_LOG total: {len(ASSERT_LOG)}")
chk(len(ASSERT_LOG) >= 100, "assertion mesin minimal 100")
print("artefak L3-1: T-L3-1_baseline.csv (103) + FIG-18_baseline.png + _l31_manifest.csv")'''
)


# ===APPEND (verify + build, pola L3-0)===

EXPECTED_FROZEN_ROWS = {
    "T-07-1_balance.csv": 260,
    "T-07-2_mi_lantai.csv": 6767,
    "T-07-3_lift.csv": 1315,
    "T-07-4_stabilitas.csv": 1335,
    "_gate_G2_alarm.csv": 86,
}


def verify_l31(report_dir: Path) -> None:
    """Registry L3-1: FIG-18 + CSV 103 + manifest + penjaga baris beku/L3-0."""
    report_dir = Path(report_dir).resolve()
    fig = report_dir / "FIG-18_baseline.png"
    assert fig.is_file(), "FIG-18 hilang"
    assert fig.stat().st_size > 0, "FIG-18 kosong"
    base = sum(1 for _ in (report_dir / "T-L3-1_baseline.csv").open(encoding="utf-8")) - 1
    assert base == 103, f"T-L3-1_baseline.csv bukan 103 ({base})"
    assert (report_dir / "_l31_manifest.csv").is_file(), "manifest hilang"
    arah = sum(1 for _ in (report_dir / "T-L3-0_arah.csv").open(encoding="utf-8")) - 1
    assert arah == 153, f"T-L3-0_arah.csv bukan 153 ({arah})"
    peta = sum(1 for _ in (report_dir / "T-L3-0_peta98.csv").open(encoding="utf-8")) - 1
    assert peta == 98, f"T-L3-0_peta98.csv bukan 98 ({peta})"
    for name, exp in EXPECTED_FROZEN_ROWS.items():
        rows = sum(1 for _ in (report_dir / name).open(encoding="utf-8")) - 1
        assert rows == exp, f"file beku berubah: {name} ({rows} vs {exp})"
    print("registry L3-1: T-L3-1_baseline.csv (103) + FIG-18_baseline.png + _l31_manifest.csv")
    print("penjaga beku/L3-0: 5 beku + arah(153) + peta98(98) tak berubah")


def build() -> None:
    """Tulis notebook dan eksekusi top-to-bottom via nbconvert (tunggal via lock)."""
    lock = REPORT_OUT_L31 / ".eda07_l31_build.lock"
    REPORT_OUT_L31.mkdir(parents=True, exist_ok=True)
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
            compile(source, f"<sel{i:02d}>", "exec")  # syntax sel tertangkap sebelum run
    print(f"pra-kompilasi {sum(1 for k, _ in CELLS if k == 'code')} sel kode: OK")
    assert len(CELLS) == 8, f"notebook L3-1 terkunci 8 sel, dapat {len(CELLS)}"
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
        verify_l31(REPORT_OUT_L31)
        for _name in ("T-L3-1_baseline.csv", "_l31_manifest.csv"):
            _p = REPORT_OUT_L31 / _name
            _p.write_bytes(_p.read_bytes().replace(b"\r\n", b"\n"))
        print("CSV L3-1 dinormalisasi CRLF->LF (pola I-1/I-2/L3-0).")
    finally:
        lock.unlink(missing_ok=True)
    print("lock dilepas; build selesai.")


if __name__ == "__main__":
    build()
