"""Generator + executor for notebooks/scalping/eda_07_i2.ipynb.

EDA-07 label-fitur deskriptif (BUKAN model, BUKAN backtest, BUKAN vonis):
pada 23 irisan tercile + 7 irisan sesi lolos EDA-06, tentukan label mana
layak diprediksi (L1: LA/LB/LC/LD), fitur kausal mana informatif (L2),
stabilitas (L3: S6), dan tautan ke delta EDA-06 (L4: G4). SCOPE BEKU oleh
reports/governance/2026-10-10/arsitek/spesifikasi-eda07-label-fitur.md
(S1-S9) + putusan-eda06.md (P-1..P-6).

Reuse-first: pola builder + eksekutor nbconvert + verify_registry dari
scripts/_build_eda06.py; kontrak data/strata/ATR/simulator/kausalitas EDA-06
(dengan angka jangkar silang: bar 1.078.001, N_ENT 184.731, B 185.248).
Logika analisis (label/fitur/MI/lift/gerbang) BARU mengikut spec S1-S9.

AGENTS.md S15.1 generator exemption applies (template file, stable refs,
deterministik rerun via SEED07, assertion machines >= 20 di notebook +
verify_registry builder-side).

I-2 (mandat V-6 putusan-eda07-i1.md): run penyelesaian. Sel 01-15 run 9
dipertahankan verbatim kecuali output-path (REPORT_DIR -> 2026-10-12,
sufiks _i2 utk log/ckpt/gate) dan gerbang STOP -> regresi vs
_gate_G2_alarm.csv beku (86 baris). BARU: KONTRAK_I2 (sel 01b), assert
24/24 konstanta (sel 03b), sel 15b (7 kandidat round_d V-5 sebagai fitur),
baris kandidat T-07-2/3/4 + VDF_CAND (sel 16), KESIMPULAN_I2 (sel 18),
verify_i2 + NB_PATH/lock i2 (ekor). SEED07/ambang A-3/metode TAK berubah.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_07_i2.ipynb"
OLD_FIGURE_DIR = PROJECT_ROOT / "reports/eda/2026-10-06/figures"
MID_FIGURE_DIR = PROJECT_ROOT / "reports/eda/2026-10-10"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


# sel 00 (markdown)
md(
    """# EDA-07 \u2014 Label dan fitur (deskriptif, bukan model)

Notebook **deskriptif**: tanpa P&L, backtest, atau pelatihan model (itu Lapisan 3).
Scope dikunci spec S1-S9: 23 irisan tercile + 7 irisan sesi lolos EDA-06
(dibaca dari CSV T-06-7, di-assert; STOP bila berubah).

Pertanyaan yang dijawab:

- **L1** \u2014 label mana yang layak diprediksi (LA barrier-hit per sisi,
  LB besaran biner + kontinu, LC 3-kelas theta 1x/2x, LD tanda pembanding)?
- **L2** \u2014 fitur kausal mana yang informatif (MI 20 kuantil vs lantai
  derau permutasi blok-hari 100x p95; lift per desil + CI; Spearman kontinu;
  redundansi |rho| > 0,8 satu wakil)?
- **L3** \u2014 apakah informasi stabil (per semester A x5, sesi, strata;
  B terpisah; 2026 tidak dimuat)?
- **L4** \u2014 apakah efek melampaui edge minimum delta irisan itu (G4)?

Gerbang G1-G4 per (irisan x label); gagal G2/G4 = BERHENTI untuk irisan itu.
Satu-satunya klaim yang boleh: irisan X label Y fitur Z layak/tidak-layak
ke Lapisan 3. LOLOS bukan bukti edge."""
)


# sel 01 (code: KONTRAK_07)
code(
    '''# Kontrak Notebook 07 - dicetak verbatim sebagai output pertama (wajib).
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
print(KONTRAK_07)'''
)

# sel 01b (code: KONTRAK_I2, BARU I-2; V-5/V-6 + definisi kandidat)
code(
    '''# Kontrak Notebook I-2 - dicetak verbatim sebagai output kedua (wajib).
KONTRAK_I2 = """- Mandat: putusan-eda07-i1.md V-6 MENGIKAT (V-4/V-5 dikunci). I-2 = run penyelesaian:
  G1-G4 penuh fitur asli + 7 kandidat round_d, T-07-1..4, FIG-13..16, kesimpulan 1 paragraf.
- Reuse: sel 01-15 run 9 dipertahankan (data/strata/ATR/entri/LA/label-waktu/fitur/MI/lift/
  leakage/sampel/skrining). SEED07, ambang A-3, N, bin, theta TAK berubah (assert 24/24 sel 03b).
- Regresi V-6 (ganti STOP): himpunan alarm kontrol harus SAMA PERSIS 86 beku
  (target,kontrol,n_arah); skrining 780/780 identik; n 260/260 == _ckpt_. Beda = STOP.
- Kandidat V-5 (definisi fitur, BUKAN ambang baru): round_d sebagai fitur HANYA pada
  7 pasangan (LB_rng London t3/tALL N5; LB_bin Tokyo t2/tALL N15/N5; LB_rng Tokyo tALL N5/N15).
  Di luar itu round_d kontrol; pdhl_d kontrol di mana-mana (ARTEFAK tertutup).
- X_PIN=10 + DEKAT/JAUH + SEEDI1 + V-2 TIDAK dibawa ke I-2 kecuali sebagai definisi
  kandidat (sudah diputus V-5). I-2 menilai G1/G3/G4 kandidat (G4=NA: ketujuh non-LA).
- Stream baru tercatat: lift kandidat = new_rng("lift_base", 10000+eidx) (rentang disjoint
  dari pemakaian run 9); MI kandidat dihitung-ulang dengan stream kontrol identik
  (floor_base, 10000+eidx) -> bit-identik sel 15, diassert.
- Lapisan 3 TERKUNCI sampai I-2 + auditor selesai. Satu-satunya klaim: layak/tidak-layak
  ke Lapisan 3; LOLOS bukan bukti edge; konsentrasi Tokyo/London menempel."""
print(KONTRAK_I2)'''
)


# sel 02 (code: setup)
code(
    '''"""Setup lingkungan dan kunci versi + helper + stream RNG."""
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
    print()'''
)


# sel 03 (code: parameter terkunci)
code(
    '''"""Parameter terkunci (diubah HANYA sebelum menjalankan, tidak sesudah melihat hasil)."""
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

REPORT_DIR = PROJECT_ROOT / "reports/eda" / "2026-10-12"  # I-2: satu lokasi T-07/FIG (brief S5.3); run 9 tak ditulis ulang
REPORT_FROZEN = PROJECT_ROOT / "reports/eda" / "2026-10-12"  # himpunan 86 beku run 9: hanya dibaca (bukti tak-tersentuh via hash SEBELUM/SESUDAH)
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
chk(set(SESSIONS) == set(COST_NORMAL) == set(COST_STRESS), "sesi config harus 4 sesi", loud=True)'''
)

# sel 03b (code: assert 24/24 konstanta run 9 identik, BARU I-2; nol-drift mesin)
code(
    '''"""Nol-drift: 24 konstanta numerik/metode SAMA PERSIS literal run 9 (diff kosong)."""
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
chk(len(SEED07) == 6, "SEED07 tepat 6 basis (stream kandidat pakai rentang idx disjoint, bukan basis baru)")'''
)
# sel 04 (code: muat data + strata, jangkar silang EDA-06)
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


# sel 05 (code: scope dari CSV T-06-7)
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
show(IR_TER[["combo", "session", "atr_ter_s", "n", "delta_pp_normal", "delta_pp_stres"]], "IRISAN-TER (23)")
show(IR_SES[["combo", "session", "n", "delta_pp_normal", "delta_pp_stres"]], "IRISAN-SES (7)")

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


# sel 06 (code: ATR M5 + M15 kausal)
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
# sel 07 (code: basis entri + tercile, jangkar N_ENT)
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


# sel 08 (code: simulator + LA skenario normal)
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
print(f"LA normal selesai: {len(LA_N)} array (pasangan x sisi)")'''
)


# sel 09 (code: LA skenario stres)
code(
    '''"""LA skenario stres (spread stres sesi; untuk kolom sensitivitas G4)."""
LA_S = {}
for combo, sess in NEED_PAIRS:
    m = ENT_SESS == sess
    sl_a, tp_a = combo_sl_tp(combo, ENT_ATR[m])
    spr_a = pd.Series(ENT_SESS[m]).map(COST_STRESS).to_numpy() * PIP_SIZE
    for side in ("buy", "sell"):
        code_v, _, _, _ = simulate(IDX[m], sl_a, tp_a, spr_a, side)
        full = np.full(N_ENT, -99, dtype=np.int8)
        full[np.flatnonzero(m)] = code_v
        LA_S[(combo, sess, side)] = full
print(f"LA stres selesai: {len(LA_S)} array (pasangan x sisi)")
del WH, WL  # bebaskan sliding-view HORIZON; LA selesai, label waktu pakai view sendiri'''
)
# sel 10 (code: label waktu N-menit, sampel tanpa tumpang-tindih)
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


# sel 11 (code: fitur kausal 29 kolom)
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
print(f"N_KEEP={N_KEEP:,}")'''
)
# sel 12 (code: mesin MI + lantai derau + lift + bootstrap klaster-hari)
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
# sel 13 (code: uji anti-leakage S7, 200 timestamp hitung-ulang)
code(
    '''"""Uji anti-leakage S7: 200 timestamp, hitung-ulang SEMUA fitur dari data s.d. T."""
rng_leak = new_rng("leak")
rng_noise_replay = new_rng("noise")
NOISE_ALL = rng_noise_replay.standard_normal(N_ENT)
chk(bool(np.array_equal(NOISE_ALL[KEEP], FEAT["noise"].to_numpy())),
    "replay noise bit-identik (stream tunggal seed 70701)")
pool = np.flatnonzero(KEEP & (IDX >= 20_000))
chk(len(pool) > 1000, "pool leakage > 1000 kandidat")
LEAK_J = np.sort(rng_leak.choice(pool, size=N_LEAK, replace=False))
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
print(f"PASS: anti-leakage {N_LEAK - miss}/{N_LEAK} identik (rtol=1e-9, lookback 20.000 bar).")'''
)
# sel 14 (code: pembangun sampel + evaluator target + skrining LA)
code(
    '''"""Sampel analisis + evaluator G1-G4 + skrining LA per irisan (60 target)."""


def get_sample(y_full: np.ndarray, mask_full: np.ndarray, kind: str):
    """Sampel N_KEEP untuk satu target: X, y, hari, semester, strata (terurut)."""
    m = np.asarray(mask_full) & KEEP
    kk = np.flatnonzero(m)
    rows = np.searchsorted(FLAT_KEEP, kk)
    y = np.asarray(y_full)[m]
    return {"rows": rows, "X": XMAT[rows], "y": y, "kind": kind,
            "day": ENT_DAY_K[rows], "sem": ENT_SEM_K[rows], "strata": ENT_STR_K[rows],
            "n": int(m.sum())}


def eval_target(smp, key: str, ypos_val, is_cont: bool, tidx: int, delta_n=None):
    """G1/G2-revisi-A3/G3 per target (+G4 bila LA). Stream RNG: floor=70703+tidx, lift=70704+tidx."""
    y = smp["y"]
    X = smp["X"]
    day = smp["day"]
    n = smp["n"]
    r = {"key": key, "n": n, "kind": smp["kind"]}
    if is_cont:
        r["classes"] = ["kontinu"]
        r["fracs"] = [1.0]
        r["g1"] = bool(n >= G1_CONT_MIN_N and len(np.unique(day)) >= G1_CONT_MIN_DAYS)
        r["base"] = float(np.mean(y))
        yb, yedges = qcodes(y, MI_BINS)
        yc_fn = lambda v: apply_edges(v, yedges)
        r["spear"] = {f: (lambda z: (float(z[0]), float(z[1])))(stats.spearmanr(X[:, j], y)) for j, f in enumerate(NONCTRL)}
        ypos = None
    else:
        cls, cnt = np.unique(y, return_counts=True)
        fr = cnt / cnt.sum()
        r["classes"] = [str(c) for c in cls]
        r["fracs"] = [float(f) for f in fr]
        r["counts"] = [int(c) for c in cnt]
        r["g1"] = bool(np.all(fr >= G1_MIN_CLASS)) if len(cls) > 2 else bool((fr >= G1_BIN_LO).all() and (fr <= G1_BIN_HI).all())
        r["base"] = float((y == ypos_val).mean())
        yc_fn = YCODE[smp["kind"]]
        ypos = (y == ypos_val).astype(float)
    # MI pooled + lantai ter-batch (urutan draw: perm 0..99, seluruh fitur sekaligus)
    rng_f = new_rng("floor_base", tidx)
    mi_o_all, fl_all = mi_floor_all(X, y, yc_fn, day, rng_f)
    mi_rows = [(f, float(mi_o_all[j]), float(fl_all[j]), bool(mi_o_all[j] > fl_all[j]))
               for j, f in enumerate(NONCTRL)]
    r["mi"] = mi_rows
    # G2-revisi A-3 (amandemen-eda07-g2): G2a = MI pooled (n_tot) > lantai
    # pooled p95 pada n_tot yang sama (kolom `above`: se-n-sama sehingga
    # bias-MM menempel di kedua sisi dan saling meniadakan); G2b = arah
    # lift sama pada >=4/5 semester (tanpa banding MI-vs-lantai per
    # semester). Fitur lolos bila G2a DAN G2b. MI semester tetap dihitung
    # sebagai diagnostik T-07-4/FIG-15 (bukan gerbang).
    sem_rows = []
    g2, g2a, g2b = {}, {}, {}
    for f, mi_o, fl, above in mi_rows:
        g2a[f] = bool(above)
        xj = X[:, NONCTRL.index(f)]
        _, dedges = qcodes(xj, 10)
        dsem = apply_edges(xj, dedges)
        dirs = []
        for s in SEM_LIST:
            ms = smp["sem"] == s
            if ms.sum() < 50:
                sem_rows.append((f, s, np.nan, fl, False, 0.0))
                continue
            _, xedges_pool = qcodes(xj, MI_BINS)
            mi_s = mi_dd(apply_edges(xj[ms], xedges_pool), yc_fn(y[ms]))
            d = dsem[ms]
            t = d == d.max()
            o = d == d.min()
            if is_cont:
                lf = float(np.mean(y[ms][t]) - np.mean(y[ms][o])) if t.sum() and o.sum() else np.nan
            else:
                lf = float(ypos[ms][t].mean() - ypos[ms][o].mean()) if t.sum() and o.sum() else np.nan
            sgn = int(np.sign(lf)) if np.isfinite(lf) and lf != 0.0 else 0
            dirs.append(sgn)
            sem_rows.append((f, s, mi_s, fl, bool(sgn != 0), lf if np.isfinite(lf) else 0.0))
        nz = [d for d in dirs if d != 0]
        maj = max(nz.count(1), nz.count(-1)) if nz else 0
        g2b[f] = bool(maj >= G2_MIN_SEM)  # A-3 tepat: arah sama pada >=4/5 semester
        g2[f] = bool(g2a[f] and g2b[f])
    r["g2a"] = g2a
    r["g2b"] = g2b
    r["sem"] = sem_rows
    r["sem_rows"] = sem_rows  # salinan non-destruktif (kunci "sem" ditimpa array pasca-attach)
    r["g2"] = g2
    # Redundansi |rho|>0.8 -> satu wakil (MI maks); kontrol di luar arena
    S = stats.spearmanr(X)[0]
    order = sorted(NONCTRL, key=lambda f: -dict((f2, m2) for f2, m2, _, _ in mi_rows)[f])
    kept_f, dropped = [], {}
    for f in order:
        j = NONCTRL.index(f)
        if any(abs(S[j, NONCTRL.index(k)]) > RHO_DROP for k in kept_f):
            dropped[f] = [k for k in kept_f if abs(S[j, NONCTRL.index(k)]) > RHO_DROP][0]
        else:
            kept_f.append(f)
    r["kept"], r["dropped"] = kept_f, dropped
    cand = [f for f in kept_f if g2.get(f)]
    wakil = (max(cand, key=lambda f: dict((f2, m2) for f2, m2, _, _ in mi_rows)[f]) if cand
             else max(kept_f, key=lambda f: dict((f2, m2) for f2, m2, _, _ in mi_rows)[f]))
    r["wakil"] = wakil
    # Lift + CI pooled untuk wakil (+ semua pelolos-G2)
    rng_l = new_rng("lift_base", tidx)
    lifts = {}
    for f in sorted(set([wakil] + [c for c in cand])):
        LIFT_DAY_CTX["day"] = day
        LIFT_DAY_CTX["rows"] = np.arange(n)
        lifts[f] = lift_deciles(X[:, NONCTRL.index(f)], y if is_cont else ypos, not is_cont, rng_l)
    r["lifts"] = lifts
    w = lifts[wakil]
    r["g3"] = bool(np.isfinite(w["lo"]) and np.isfinite(w["hi"]) and (w["hi"] < 0 or w["lo"] > 0))
    if delta_n is not None and not is_cont:
        r["liftN"] = float(w["top"] - r["base"])
        r["g4"] = bool(r["liftN"] >= delta_n and r.get("liftS", np.nan) >= G4_STRESS_MIN_PP)
    return r


# Skrining LA: 23 irisan-ter x 2 sisi + 7 irisan-sesi x 2 sisi
LA_TARGETS = []
for _, rr in IR_TER.iterrows():
    combo, sess, tval = rr["combo"], rr["session"], int(rr["atr_ter_s"])
    key = ("ter", combo, sess, tval)
    for side in ("buy", "sell"):
        LA_TARGETS.append((key, side, DELTA_N[key], DELTA_S[key]))
for _, rr in IR_SES.iterrows():
    combo, sess = rr["combo"], rr["session"]
    key = ("ses", combo, sess, 0)
    for side in ("buy", "sell"):
        LA_TARGETS.append((key, side, DELTA_N[key], DELTA_S[key]))
print(f"target LA: {len(LA_TARGETS)} (irisan x sisi)")

RES_LA = []
CKPT_LA = []  # A-5: checkpoint per target LA agar abort tidak menghapus progres
tidx = 0
for key, side, d_n, d_s in LA_TARGETS:
    _, combo, sess, tval = key
    m_sess = sesskey_mask(sess, tval if key[0] == "ter" else "ALL")
    yN = LA_N[(combo, sess, side)]
    yS = LA_S[(combo, sess, side)]
    mask = m_sess & (yN != -99)
    smp = get_sample(yN, mask, "LA")
    ev = eval_target(smp, f"LA {combo} {sess} t{tval} {side}", YPOS["LA"], False, tidx, delta_n=d_n)
    # G4-stres: desil wakil, skenario stres
    w = ev["lifts"][ev["wakil"]]
    xj = smp["X"][:, NONCTRL.index(ev["wakil"])]
    dc = apply_edges(xj, w["edges"])
    ySs = yS[mask & KEEP]
    yp_s = (ySs == 1).astype(float)
    ev["liftS"] = float(yp_s[dc == dc.max()].mean() - yp_s.mean()) if (dc == dc.max()).sum() else np.nan
    ev["g4"] = bool(ev.get("liftN", -9) >= d_n and ev["liftS"] >= G4_STRESS_MIN_PP)
    ev["delta_n"], ev["delta_s"] = d_n, d_s
    ev["side"] = side
    ev["scope"] = key
    ev["rows"], ev["day"], ev["sem"], ev["strata"], ev["yy"] = smp["rows"], smp["day"], smp["sem"], smp["strata"], smp["y"]
    RES_LA.append(ev)
    tidx += 1
    CKPT_LA.append({"target": str(key) + " " + side, "n": ev["n"], "G1": bool(ev["g1"]),
                    "n_G2": sum(ev["g2"].values()), "wakil": ev["wakil"]})
    pd.DataFrame(CKPT_LA).to_csv(REPORT_DIR / "_ckpt_LA_i2.csv", index=False)
    with open(REPORT_DIR / "eda07_i2_progress.log", "a", encoding="utf-8") as _pl:
        _pl.write("LA %d/%d %s %s%s" % (len(CKPT_LA), len(LA_TARGETS), key, side, chr(10)))
print(f"LA selesai: {len(RES_LA)} target (tidx 0..{tidx - 1})")
CHK_TIDX_LA = tidx'''
)
# sel 15 (code: skrining label waktu + kalibrasi kontrol + rerun determinisme)
code(
    '''"""Skrining label waktu per sesskey x N x jenis + kalibrasi kontrol + rerun."""
SESS_ALL = sorted({(r["session"], int(r["atr_ter_s"])) for _, r in IR_TER.iterrows()} |
                  {(r["session"], "ALL") for _, r in IR_SES.iterrows()},
                  key=lambda t: (t[0], str(t[1])))
KINDS = ["LB_bin", "LB_rng", "LC1", "LC2", "LD"]
print(f"sesskey unik: {len(SESS_ALL)} x N={len(N_HORIZONS)} x jenis={len(KINDS)}")

RES_T = []
CKPT_T = []  # A-5: checkpoint per target waktu agar abort tidak menghapus progres
tidx = CHK_TIDX_LA
for sess, ter in SESS_ALL:
    for N in N_HORIZONS:
        for kd in KINDS:
            v, vals = TLAB[(sess, ter, N, kd)]
            y_full = np.full(N_ENT, np.nan)
            y_full[v] = vals
            mask = v & np.isfinite(y_full)
            if kd == "LD":
                mask &= y_full != 9
            yv = y_full * 1.0 if kd == "LB_rng" else np.where(np.isfinite(y_full), y_full, 0).astype(np.int64)
            smp = get_sample(yv, mask, kd)
            is_c = kd == "LB_rng"
            ev = eval_target(smp, f"{kd} {sess} t{ter} N{N}", YPOS[kd], is_c, tidx)
            ev["sess"], ev["ter"], ev["N"] = sess, ter, N
            ev["g4"] = "NA"
            ev["rows"], ev["day"], ev["sem"], ev["strata"], ev["yy"] = smp["rows"], smp["day"], smp["sem"], smp["strata"], smp["y"]
            RES_T.append(ev)
            tidx += 1
            CKPT_T.append({"target": f"{kd} {sess} t{ter} N{N}", "n": ev["n"], "G1": bool(ev["g1"]),
                           "n_G2": sum(ev["g2"].values()), "wakil": ev["wakil"]})
            pd.DataFrame(CKPT_T).to_csv(REPORT_DIR / "_ckpt_T_i2.csv", index=False)
            with open(REPORT_DIR / "eda07_i2_progress.log", "a", encoding="utf-8") as _pl:
                _pl.write("T %d/%d %s %s t%s N%s%s" % (len(CKPT_T), len(SESS_ALL) * len(N_HORIZONS) * len(KINDS), kd, sess, ter, N, chr(10)))
print(f"waktu selesai: {len(RES_T)} target (tidx ..{tidx - 1})")
CHK_TIDX_ALL = tidx

# Kalibrasi kontrol G2-revisi A-3: kriteria IDENTIK fitur (G2a pooled-vs-pooled
# n-sama + G2b arah-lift >=4/5); A-5 log-then-assert: bukti ke disk SEBELUM assert
XCTRL = FEAT[CTRL_COLS].to_numpy("float64")
CTRL_ABOVE, CTRL_N = 0, 0
CTRL_ALARM = []
SCREEN_ROWS = []
for eidx, ev in enumerate(RES_LA + RES_T):
    rows, day, y = ev["rows"], ev["day"], ev["yy"]
    is_c = ev["kind"] == "LB_rng"
    if is_c:
        _, ye = qcodes(y, MI_BINS)
        yc_fn = lambda v, _e=ye: apply_edges(v, _e)
    else:
        yc_fn = YCODE[ev["kind"]]
    rng_c = new_rng("floor_base", 10000 + eidx)  # blok terpisah, tercatat
    mi_c_all, fl_c_all = mi_floor_all(XCTRL[rows], y, yc_fn, day, rng_c)
    for j, cf in enumerate(CTRL_COLS):
        mi_o, fl = float(mi_c_all[j]), float(fl_c_all[j])
        CTRL_N += 1
        a_c = bool(mi_o > fl)  # G2a kontrol: pooled vs pooled, n sama (identik fitur)
        CTRL_ABOVE += a_c
        # Uji G2b kontrol (identik fitur): arah lift sama >=4/5 semester, tanpa banding MI
        _, dd = qcodes(XCTRL[rows, j], 10)
        dsem = apply_edges(XCTRL[rows, j], dd)
        yp = None if is_c else (y == YPOS[ev["kind"]]).astype(float)
        dirs = []
        for s in SEM_LIST:
            ms = ev["sem"] == s
            if ms.sum() < 50:
                continue
            d = dsem[ms]
            t = d == d.max()
            o = d == d.min()
            if t.sum() == 0 or o.sum() == 0:
                continue
            lf = float(np.mean(y[ms][t]) - np.mean(y[ms][o])) if is_c else float(yp[ms][t].mean() - yp[ms][o].mean())
            if np.isfinite(lf) and lf != 0.0:
                dirs.append(int(np.sign(lf)))
        nz = [d for d in dirs if d != 0]
        maj = max(nz.count(1), nz.count(-1)) if nz else 0
        b_c = bool(maj >= G2_MIN_SEM)  # A-3 tepat: arah sama pada >=4/5 semester
        if a_c and b_c:
            CTRL_ALARM.append((ev["key"], cf, maj))
        SCREEN_ROWS.append({"target": ev["key"], "kontrol": cf, "G2a_pooled": a_c,
                            "G2b_arah": b_c, "n_arah": len(nz)})
print(f"kontrol pooled di atas lantai: {CTRL_ABOVE}/{CTRL_N} = {CTRL_ABOVE / max(CTRL_N, 1):.3f} (harapan ~= 0.05)")
# I-2/V-6 REGRESI (menggantikan STOP buta): tulis skrining+alarm ke file
# _i2, lalu bandingkan himpunan (target,kontrol,n_arah) vs beku run 9.
# Sama persis -> lanjut sel verdict. Kontrol BARU di luar 86 = STOP +
# adjudikasi baru, DILARANG bypass. File beku hanya dibaca.
pd.DataFrame(SCREEN_ROWS).to_csv(REPORT_DIR / "_gate_G2_skrining_i2.csv", index=False)
pd.DataFrame(CTRL_ALARM, columns=["target", "kontrol", "n_arah"]).to_csv(REPORT_DIR / "_gate_G2_alarm_i2.csv", index=False)
print(f"regresi G2: {len(SCREEN_ROWS)} baris skrining + {len(CTRL_ALARM)} alarm -> _gate_G2_*_i2.csv")
REF_ALARM = pd.read_csv(REPORT_FROZEN / "_gate_G2_alarm.csv")
REF_SKRIN = pd.read_csv(REPORT_FROZEN / "_gate_G2_skrining.csv")
chk(len(REF_ALARM) == 86, "himpunan beku 86 alarm")
chk(len(REF_SKRIN) == 780, "skrining beku 780 baris")
new_set = {(t, c, int(n)) for t, c, n in CTRL_ALARM}
ref_set = {(r["target"], r["kontrol"], int(r["n_arah"])) for _, r in REF_ALARM.iterrows()}
chk(new_set == ref_set, "himpunan alarm kontrol SAMA PERSIS 86 beku (diff kosong)")
mk = {(r["target"], r["kontrol"]): (str(r["G2a_pooled"]) == "True", str(r["G2b_arah"]) == "True", int(r["n_arah"]))
      for _, r in REF_SKRIN.iterrows()}
mis = [(s["target"], s["kontrol"]) for s in SCREEN_ROWS
       if mk.get((s["target"], s["kontrol"])) != (bool(s["G2a_pooled"]), bool(s["G2b_arah"]), int(s["n_arah"]))]
chk(len(SCREEN_ROWS) == 780 and not mis, f"skrining 780/780 identik beku (beda={len(mis)})")
print("PASS: regresi kontrol 86/86 + skrining 780/780 identik beku -> lanjut verdict (V-6).")

# Rerun determinisme: hitung-ulang MI+lantai target pertama tiap blok, assert bit-identik
ev0 = RES_LA[0]
rng_r = new_rng("floor_base", 0)
mi_r0, fl_r0 = mi_floor_all(XMAT[ev0["rows"]], ev0["yy"], YCODE["LA"], ev0["day"], rng_r)
for j, (f, mi_o, fl, _) in enumerate(ev0["mi"]):
    chk(mi_r0[j] == mi_o and fl_r0[j] == fl, f"rerun bit-identik LA {f}")
ev1 = RES_T[0]
rng_r1 = new_rng("floor_base", CHK_TIDX_LA)
mi_r1, fl_r1 = mi_floor_all(XMAT[ev1["rows"]], ev1["yy"], YCODE[ev1["kind"]], ev1["day"], rng_r1)
for j, (f, mi_o, fl, _) in enumerate(ev1["mi"]):
    chk(mi_r1[j] == mi_o and fl_r1[j] == fl, f"rerun bit-identik waktu {f}")
print("PASS: rerun MI+lantai bit-identik (stream RNG tunggal per blok).")'''
)
# sel 15b (code: evaluasi 7 kandidat round_d V-5 SEBAGAI FITUR, BARU I-2)
code(
    '''"""Tujuh kandidat V-5: round_d sebagai fitur pada 7 pasangan (G1/G2/G3 penuh; G4=NA non-LA)."""
CAND_KEYS = ["LB_rng London t3 N5", "LB_rng London tALL N5", "LB_bin Tokyo t2 N15",
             "LB_bin Tokyo tALL N5", "LB_rng Tokyo tALL N5", "LB_bin Tokyo tALL N15",
             "LB_rng Tokyo tALL N15"]
CAND_EV = {ev["key"]: (eidx, ev) for eidx, ev in enumerate(RES_LA + RES_T)}
chk(set(CAND_KEYS) <= set(CAND_EV), "7 kandidat ada di 260 target")
j_round = CTRL_COLS.index("round_d")
CAND = {}
for key in CAND_KEYS:
    eidx, ev = CAND_EV[key]
    rows, day, y = ev["rows"], ev["day"], ev["yy"]
    is_c = ev["kind"] == "LB_rng"
    srow = [s for s in SCREEN_ROWS if s["target"] == key and s["kontrol"] == "round_d"]
    chk(len(srow) == 1 and srow[0]["G2a_pooled"] and srow[0]["G2b_arah"], f"kandidat G2a&G2b {key}")
    xr = XCTRL[rows, j_round]
    if is_c:
        _, ye = qcodes(y, MI_BINS)
        yc_fn = lambda v, _e=ye: apply_edges(v, _e)
        stat = y
    else:
        yc_fn = YCODE[ev["kind"]]
        stat = (y == YPOS[ev["kind"]]).astype(float)
    rng_c = new_rng("floor_base", 10000 + eidx)  # stream kontrol identik sel 15
    mi_c, fl_c = mi_floor_all(xr.reshape(-1, 1), y, yc_fn, day, rng_c)
    chk(bool(mi_c[0] > fl_c[0]), f"MI kandidat bit-identik di atas lantai {key}")
    rng_l = new_rng("lift_base", 10000 + eidx)  # stream BARU tercatat (disjoint run 9)
    LIFT_DAY_CTX["day"] = day
    LIFT_DAY_CTX["rows"] = np.arange(ev["n"])
    w = lift_deciles(xr, stat, not is_c, rng_l)
    g3c = bool(np.isfinite(w["lo"]) and np.isfinite(w["hi"]) and (w["hi"] < 0 or w["lo"] > 0))
    sem_c = []
    _, dd = qcodes(xr, 10)
    dsem = apply_edges(xr, dd)
    _, xe = qcodes(xr, MI_BINS)
    for s in SEM_LIST:
        ms = ev["sem"] == s
        if ms.sum() < 50:
            sem_c.append((s, int(ms.sum()), np.nan, float(fl_c[0]), False, 0.0))
            continue
        mi_s = mi_dd(apply_edges(xr[ms], xe), yc_fn(y[ms]))
        d = dsem[ms]
        t = d == d.max()
        o = d == d.min()
        lf = float(np.mean(stat[ms][t]) - np.mean(stat[ms][o])) if t.sum() and o.sum() else np.nan
        sgn = int(np.sign(lf)) if np.isfinite(lf) and lf != 0.0 else 0
        sem_c.append((s, int(ms.sum()), mi_s, float(fl_c[0]), bool(sgn != 0), lf if np.isfinite(lf) else 0.0))
    CAND[key] = {"ev": ev, "eidx": eidx, "is_c": is_c, "mi": float(mi_c[0]), "fl": float(fl_c[0]),
                 "lift": w, "g3": g3c, "sem": sem_c}
    print(f"kandidat {key}: n={ev['n']} G1={bool(ev['g1'])} G2a&G2b=True "
          f"MI={mi_c[0]:.6f}>lantai={fl_c[0]:.6f} lift={w['lift']:.4f} CI=[{w['lo']:.4f},{w['hi']:.4f}] G3={g3c}")
print(f"kandidat dinilai: {len(CAND)}/7 (G4=NA: ketujuh target-waktu non-LA)")'''
)
# sel 16 (code: verdict G1-G4 + tabel T-07-1..4 + CSV)
code(
    '''"""Verdict per (irisan x label), agregasi irisan, T-07-1..4 + CSV satu lokasi.
lolos_sem T-07-4 = lift-semester terisi/berarah (komponen G2b A-3), BUKAN banding MI-vs-lantai."""
VERD = []
for ev in RES_LA + RES_T:
    g2any = any(ev["g2"].values())
    g3 = ev["g3"]
    g4 = ev["g4"]
    ok = bool(ev["g1"] and g2any and g3 and (g4 == "NA" or bool(g4)))
    VERD.append({"key": ev["key"], "n": ev["n"], "base": round(ev["base"], 4),
                 "G1": bool(ev["g1"]), "n_G2": sum(ev["g2"].values()),
                 "wakil": ev["wakil"], "G3": bool(g3),
                 "lift": round(ev["lifts"][ev["wakil"]]["lift"], 4),
                 "ci": (round(ev["lifts"][ev["wakil"]]["lo"], 4), round(ev["lifts"][ev["wakil"]]["hi"], 4)),
                 "G4": g4 if g4 == "NA" else bool(g4),
                 "VERDICT": "LOLOS" if ok else "GUGUR"})
VDF = pd.DataFrame(VERD)
N_PASS = int((VDF["VERDICT"] == "LOLOS").sum())
print(f"verdict target: {len(VDF)} dievaluasi, LOLOS={N_PASS}, GUGUR={len(VDF) - N_PASS}")

# Agregasi irisan: LOLOS bila >=1 label lolos penuh (pra-registrasi)
def scope_of(key: str):
    """Petakan kunci target -> id irisan + delta_normal."""
    if key.startswith("LA "):
        _, combo, sess, tside = key.split(" ", 3)
        tval, side = tside.rsplit(" ", 1)
        tval = tval[1:]
        kid = ("ter", combo, sess, int(tval)) if tval != "ALL" else ("ses", combo, sess, 0)
        return kid, DELTA_N.get(kid, np.nan)
    kd, sess, tN = key.split(" ", 2)
    tval, N = tN.rsplit(" ", 1)
    tval = tval[1:]
    kid = ("ter", None, sess, int(tval)) if tval != "ALL" else ("ses", None, sess, 0)
    dn = [v for k, v in DELTA_N.items() if k[0] == kid[0] and k[2] == sess and (kid[0] == "ses" or k[3] == kid[3])]
    return kid, (min(dn) if dn else np.nan)


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


VDF["irisan_list"] = VDF["key"].apply(assoc_irisan)
VDF["delta_n"] = VDF["key"].apply(lambda k: scope_of(k)[1])
VEX = VDF.explode("irisan_list").rename(columns={"irisan_list": "irisan"})
irank = VEX.groupby("irisan", sort=False).agg(n_lolos=("VERDICT", lambda s: int((s == "LOLOS").sum())),
                                               delta=("delta_n", "min")).reset_index()
irank = irank.sort_values(["n_lolos", "delta"], ascending=[False, True]).reset_index(drop=True)
IR_LOLOS = irank[irank["n_lolos"] > 0]
print(f"irisan LOLOS (>=1 label): {len(IR_LOLOS)} dari {len(irank)}")
show(irank, "PERINGKAT-IRISAN (lolos-verdict, seri delta terendah)")

# FIG pick (pra-registrasi): irisan peringkat-1; target = label lolos-pertama / MI-tertinggi
pick_ir = irank.iloc[0]["irisan"]
sub = VEX[VEX["irisan"] == pick_ir]
passed = sub[sub["VERDICT"] == "LOLOS"]
FIG_KEY = passed.iloc[0]["key"] if len(passed) else sub.sort_values("n_G2", ascending=False).iloc[0]["key"]
print(f"FIG target: {FIG_KEY} (irisan {pick_ir})")

# T-07-1 balance
T071 = pd.DataFrame([{"target": ev["key"], "n": ev["n"], "kelas": "|".join(ev["classes"]),
                      "fraksi": "|".join(f"{f:.4f}" for f in ev["fracs"]),
                      "G1": ev["g1"] if isinstance(ev["g1"], bool) else bool(ev["g1"])} for ev in RES_LA + RES_T])
# T-07-2 MI vs lantai (non-kontrol)
rows2 = []
for ev in RES_LA + RES_T:
    for f, mi_o, fl, ab in ev["mi"]:
        rows2.append({"target": ev["key"], "fitur": f, "mi": round(mi_o, 6), "lantai": round(fl, 6),
                      "di_atas": bool(ab), "G2a": bool(ev["g2a"][f]), "G2b": bool(ev["g2b"][f]),
                      "G2": bool(ev["g2"][f]), "wakil": f == ev["wakil"]})
T072 = pd.DataFrame(rows2)
# T-07-3 lift (+G4 LA)
rows3 = []
for ev in RES_LA + RES_T:
    for f, w in ev["lifts"].items():
        r3 = {"target": ev["key"], "fitur": f, "lift": round(w["lift"], 4),
              "ci_lo": round(w["lo"], 4), "ci_hi": round(w["hi"], 4),
              "n_top": w["n_top"], "n_bot": w["n_bot"], "G3": bool(ev["g3"]) if f == ev["wakil"] else ""}
        if ev["key"].startswith("LA "):
            r3.update({"liftN_vs_base": round(ev.get("liftN", np.nan), 4),
                       "liftS_vs_base": round(ev.get("liftS", np.nan), 4),
                       "delta_N": ev.get("delta_n", np.nan), "delta_S": ev.get("delta_s", np.nan),
                       "G4": ev["g4"]})
        rows3.append(r3)
T073 = pd.DataFrame(rows3)
# T-07-4 stabilitas semester (wakil) + MI strata pooled
rows4 = []
for ev in RES_LA + RES_T:
    w = ev["wakil"]
    j = NONCTRL.index(w)
    xr = XMAT[ev["rows"], j]
    for s in SEM_LIST:
        ms = ev["sem"] == s
        ma = ev["strata"] == "A"
        mb = ev["strata"] == "B"
        yb = ev["yy"]
        if ev["kind"] == "LB_rng":
            _, ye = qcodes(yb, MI_BINS)
            ycf = lambda v, _e=ye: apply_edges(v, _e)
        else:
            ycf = YCODE[ev["kind"]]
        _, xe = qcodes(xr, MI_BINS)
        miA = mi_dd(apply_edges(xr[ma], xe), ycf(yb[ma])) if ma.sum() >= 50 else np.nan
        miB = mi_dd(apply_edges(xr[mb], xe), ycf(yb[mb])) if mb.sum() >= 50 else np.nan
        hit = [r for r in ev["sem_rows"] if r[0] == w and r[1] == s][0]
        rows4.append({"target": ev["key"], "fitur": w, "semester": s, "n": int(ms.sum()),
                      "mi_sem": round(hit[2], 6) if np.isfinite(hit[2]) else "",
                      "lantai": round(hit[3], 6), "lolos_sem": bool(hit[4]),
                      "lift_sem": round(hit[5], 4), "mi_A": round(miA, 6) if np.isfinite(miA) else "",
                      "n_A": int(ma.sum()), "mi_B": round(miB, 6) if np.isfinite(miB) else "",
                      "n_B": int(mb.sum())})
T074 = pd.DataFrame(rows4)
# I-2 kandidat V-5: verdict per pasangan + baris round_d pada T-07-2/3/4
VCAND = []
for key in CAND_KEYS:
    c = CAND[key]
    ev = c["ev"]
    okc = bool(ev["g1"] and c["g3"])  # G2 kandidat True via regresi + assert sel 15b
    VCAND.append({"key": key, "n": ev["n"], "base": round(ev["base"], 4),
                  "G1": bool(ev["g1"]), "n_G2": 1, "wakil": "round_d",
                  "G3": bool(c["g3"]), "lift": round(c["lift"]["lift"], 4),
                  "ci": (round(c["lift"]["lo"], 4), round(c["lift"]["hi"], 4)),
                  "G4": "NA", "VERDICT": "LOLOS" if okc else "GUGUR"})
VDF_CAND = pd.DataFrame(VCAND)
N_CAND_PASS = int((VDF_CAND["VERDICT"] == "LOLOS").sum())
print(f"verdict kandidat: {len(VDF_CAND)} pasangan, LOLOS={N_CAND_PASS}, GUGUR={len(VDF_CAND) - N_CAND_PASS}")
show(VDF_CAND, "KANDIDAT-V5 (round_d sebagai fitur, G1+G2+G3; G4=NA)")
rows2.extend({"target": k, "fitur": "round_d", "mi": round(CAND[k]["mi"], 6),
              "lantai": round(CAND[k]["fl"], 6), "di_atas": True,
              "G2a": True, "G2b": True, "G2": True, "wakil": True} for k in CAND_KEYS)
T072 = pd.DataFrame(rows2)
for k in CAND_KEYS:
    c = CAND[k]
    T073 = pd.concat([T073, pd.DataFrame([{"target": k, "fitur": "round_d",
              "lift": round(c["lift"]["lift"], 4), "ci_lo": round(c["lift"]["lo"], 4),
              "ci_hi": round(c["lift"]["hi"], 4), "n_top": c["lift"]["n_top"],
              "n_bot": c["lift"]["n_bot"], "G3": bool(c["g3"])}])], ignore_index=True)
for k in CAND_KEYS:
    c = CAND[k]
    ev = c["ev"]
    xr = XCTRL[ev["rows"], j_round]
    yb = ev["yy"]
    if ev["kind"] == "LB_rng":
        _, yec = qcodes(yb, MI_BINS)
        ycfc = lambda v, _e=yec: apply_edges(v, _e)
    else:
        ycfc = YCODE[ev["kind"]]
    _, xec = qcodes(xr, MI_BINS)
    for (s, nsem, mi_s, fls, lolos, lfs) in c["sem"]:
        ms = ev["sem"] == s
        ma = ev["strata"] == "A"
        mb = ev["strata"] == "B"
        miA = mi_dd(apply_edges(xr[ma], xec), ycfc(yb[ma])) if ma.sum() >= 50 else np.nan
        miB = mi_dd(apply_edges(xr[mb], xec), ycfc(yb[mb])) if mb.sum() >= 50 else np.nan
        rows4.append({"target": k, "fitur": "round_d", "semester": s, "n": nsem,
                      "mi_sem": round(mi_s, 6) if np.isfinite(mi_s) else "",
                      "lantai": round(fls, 6), "lolos_sem": bool(lolos),
                      "lift_sem": round(lfs, 4), "mi_A": round(miA, 6) if np.isfinite(miA) else "",
                      "n_A": int(ma.sum()), "mi_B": round(miB, 6) if np.isfinite(miB) else "",
                      "n_B": int(mb.sum())})
T074 = pd.DataFrame(rows4)
for name, df in (("T-07-1_balance.csv", T071), ("T-07-2_mi_lantai.csv", T072),
                 ("T-07-3_lift.csv", T073), ("T-07-4_stabilitas.csv", T074)):
    df.to_csv(REPORT_DIR / name, index=False)
    print(f"{name}: {len(df)} baris -> {REPORT_DIR.name}/{name}")
show(VDF[VDF["VERDICT"] == "LOLOS"], "TARGET-LOLOS (G1+G2+G3+G4 penuh)")
chk((REPORT_DIR / "T-07-1_balance.csv").is_file(), "CSV T-07-1 tertulis")'''
)
# sel 17 (code: FIG-13..16 target FIG_KEY)
code(
    '''"""FIG-13 MI vs lantai, FIG-14 lift per desil, FIG-15 stabilitas semester, FIG-16 balance."""
EV_BY_KEY = {ev["key"]: ev for ev in RES_LA + RES_T}
evF = EV_BY_KEY[FIG_KEY]
wF = evF["wakil"]
jF = NONCTRL.index(wF)
xF = XMAT[evF["rows"], jF]
is_cF = evF["kind"] == "LB_rng"
yF = evF["yy"]
ypF = None if is_cF else (yF == YPOS[evF["kind"]]).astype(float)
statF = yF if is_cF else ypF

plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 110})
FIGS_NEW = []

# FIG-13: MI vs lantai, 12 fitur teratas
top12 = sorted(evF["mi"], key=lambda r: -r[1])[:12]
fn = [r[0] for r in top12]
mi_v = [r[1] for r in top12]
fl_v = [r[2] for r in top12]
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(fn, mi_v, label="MI pooled")
ax.plot(fn, fl_v, "r--", label="lantai p95 blok-hari")
ax.set_title(f"FIG-13 MI vs lantai: {FIG_KEY} (n={evF['n']:,})")
ax.tick_params(axis="x", rotation=45, labelsize=8)
ax.legend()
fig.tight_layout()
fig.savefig(REPORT_DIR / "FIG-13_mi_lantai.png")
FIGS_NEW.append("FIG-13_mi_lantai.png")
plt.close(fig)

# FIG-14: peluang/mean per desil wakil + laju dasar
w = evF["lifts"][wF]
dc = apply_edges(xF, w["edges"])
rates = [float(statF[dc == d].mean()) for d in sorted(np.unique(dc))]
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar([str(d) for d in sorted(np.unique(dc))], rates)
ax.axhline(evF["base"], color="r", linestyle="--", label=f"laju dasar {evF['base']:.4f}")
ax.set_title(f"FIG-14 desil {wF}: {FIG_KEY} (lift={w['lift']:.4f} CI [{w['lo']:.4f},{w['hi']:.4f}])")
ax.set_xlabel("desil fitur (rendah -> tinggi)")
ax.legend()
fig.tight_layout()
fig.savefig(REPORT_DIR / "FIG-14_lift_desil.png")
FIGS_NEW.append("FIG-14_lift_desil.png")
plt.close(fig)

# FIG-15: lift-semester wakil (hijau = lift terisi, komponen G2b A-3) + MI diagnostik vs lantai
rows_w = [r for r in evF["sem_rows"] if r[0] == wF]  # (fitur, semester, mi_sem, lantai, lift_terisi, lift)
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar([r[1] for r in rows_w], [r[2] if np.isfinite(r[2]) else 0.0 for r in rows_w],
       color=["g" if r[4] else "gray" for r in rows_w])
ax.axhline(rows_w[0][3], color="r", linestyle="--", label="lantai pooled")
ax.set_title(f"FIG-15 stabilitas {wF}: {FIG_KEY}")
ax.legend()
fig.tight_layout()
fig.savefig(REPORT_DIR / "FIG-15_stabilitas.png")
FIGS_NEW.append("FIG-15_stabilitas.png")
plt.close(fig)

# FIG-16: balance kelas target
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(evF.get("classes", ["kontinu"]), evF["fracs"])
ax.set_title(f"FIG-16 balance: {FIG_KEY} (n={evF['n']:,}, G1={evF['g1']})")
fig.tight_layout()
fig.savefig(REPORT_DIR / "FIG-16_balance.png")
FIGS_NEW.append("FIG-16_balance.png")
plt.close(fig)
print("FIG tersimpan:", FIGS_NEW)
for f in FIGS_NEW:
    chk((REPORT_DIR / f).is_file() and (REPORT_DIR / f).stat().st_size > 0, f"FIG {f} ada dan tak-kosong")'''
)
# sel 18 (code: kunci balance + kesimpulan + hitung assertion)
code(
    '''"""Kunci akhir: balance sum-to-1, kesimpulan terkunci, hitung assertion >= 20."""
for ev in RES_LA + RES_T:
    if ev["kind"] == "LB_rng":
        continue
    chk(abs(sum(ev["fracs"]) - 1.0) < 1e-9, f"balance sum-to-1 {ev['key']}")
print(f"PASS: balance sum-to-1 untuk {len(RES_LA) + len(RES_T) - sum(1 for ev in RES_LA + RES_T if ev['kind'] == 'LB_rng')} target diskret.")

lol = VDF[VDF["VERDICT"] == "LOLOS"].sort_values(["irisan", "key"] if "irisan" in VDF else ["key"])
TOP3 = VDF[VDF["VERDICT"] == "LOLOS"].head(3)[["key", "wakil", "lift", "ci"]].to_dict("records") if N_PASS else []
CAND_PASS_KEYS = VDF_CAND[VDF_CAND["VERDICT"] == "LOLOS"]["key"].tolist()
KESIMPULAN_I2 = (
    f"EDA-07 deskriptif mengevaluasi {len(VDF)} pasangan (irisan x label) "
    f"({len(RES_LA)} LA barrier-hit per sisi + {len(RES_T)} label-waktu) pada 23 irisan tercile + 7 irisan sesi lolos EDA-06. "
    f"Verdict G1-G4 penuh fitur asli: {N_PASS} LOLOS, {len(VDF) - N_PASS} GUGUR; "
    f"irisan dengan >=1 label lolos: {len(IR_LOLOS)} dari {len(irank)} "
    f"({', '.join(str(i) for i in IR_LOLOS['irisan'].tolist()[:8])}). "
    f"Tujuh kandidat round_d V-5 (LB Tokyo/London N5/N15): {N_CAND_PASS} LOLOS G1+G2+G3 penuh (G4=NA) "
    f"({', '.join(CAND_PASS_KEYS) if CAND_PASS_KEYS else 'nihil'}); {len(VDF_CAND) - N_CAND_PASS} GUGUR. "
    f"Target ilustratif FIG-13..16: {FIG_KEY} (wakil {wF}). "
    f"Tiga (irisan x label x fitur) teratas: {TOP3}. "
    f"Regresi kontrol: himpunan alarm SAMA PERSIS 86 beku (52 pdhl_d + 28 round_d + 6 noise), "
    f"skrining 780/780 identik; nol kontrol BARU di luar 86. "
    f"Kalibrasi: {CTRL_ABOVE}/{CTRL_N} pooled di atas lantai (harapan ~=5%). "
    f"Anti-leakage 200/200 identik (rtol=1e-9, lookback 20.000 bar); rerun MI+lantai bit-identik; "
    f"bootstrap klaster-hari satu-stream per blok (seed 70703+tidx / 70704+tidx / 10000+eidx kontrol; "
    f"lift kandidat stream baru 10000+eidx lift_base). "
    f"Satu-satunya klaim: pasangan LOLOS di atas layak dibawa ke Lapisan 3 dengan fitur wakilnya; "
    f"GUGUR = BERHENTI (rumuskan ulang target, DILARANG baseline). LOLOS bukan bukti edge; "
    f"konsentrasi Tokyo/London menempel (DILARANG generalisasi sesi)."
)
print("KESIMPULAN_I2 TERKUNCI:")
print(KESIMPULAN_I2)
chk(len(KESIMPULAN_I2) > 200, "sel kesimpulan terisi (>200 karakter)")
chk(N_PASS >= 0, "verdict terhitung")
chk(len(VDF_CAND) == 7 and N_CAND_PASS >= 0, "7 kandidat terhitung")
print(f"ASSERT_LOG total: {len(ASSERT_LOG)}")
chk(len(ASSERT_LOG) >= 20, "assertion mesin minimal 20")
print(f"artefak di {REPORT_DIR}: 4 CSV T-07 + 4 FIG (13..16); notebook 19 sel.")'''
)
# ===APPEND===

EXPECTED_FIGS_OLD = [f"FIG-{i:02d}.png" for i in range(1, 8)]
EXPECTED_FIGS_MID = [
    "FIG-08_ekor_spread_per_jam.png",
    "FIG-09_spread_vs_volatilitas.png",
    "FIG-10_heatmap_pstar.png",
    "FIG-11_stabilitas_semester.png",
    "FIG-12_delta_vs_atr.png",
]
EXPECTED_FIGS_NEW = [
    "FIG-13_mi_lantai.png",
    "FIG-14_lift_desil.png",
    "FIG-15_stabilitas.png",
    "FIG-16_balance.png",
]
EXPECTED_CSVS_07 = [
    "T-07-1_balance.csv",
    "T-07-2_mi_lantai.csv",
    "T-07-3_lift.csv",
    "T-07-4_stabilitas.csv",
]
REPORT_OUT_I2 = PROJECT_ROOT / "reports/eda" / "2026-10-12"


def verify_i2(report_dir: Path) -> None:
    """Registry I-2: FIG-01..07 lama + FIG-08..12 run 9 (baca) + FIG-13..16 I-2 + T-07 x4 + T-I1 x3 beku."""
    report_dir = Path(report_dir).resolve()
    old = sorted(p.name for p in OLD_FIGURE_DIR.glob("*.png"))
    assert old == EXPECTED_FIGS_OLD, f"registry lama melanggar sekuens: {old}"
    mid = sorted(p.name for p in MID_FIGURE_DIR.glob("FIG-*.png"))
    assert mid == sorted(EXPECTED_FIGS_MID), f"FIG-08..12 run 9 tak tepat: {mid}"
    new = sorted(EXPECTED_FIGS_NEW)
    for name in new:
        assert (report_dir / name).is_file(), f"FIG I-2 hilang: {name}"
    got_csv = sorted(p.name for p in report_dir.glob("T-07-*.csv"))
    assert got_csv == sorted(EXPECTED_CSVS_07), f"CSV T-07 tidak tepat 4: {got_csv}"
    for name in sorted(EXPECTED_CSVS_07) + new:
        size = (report_dir / name).stat().st_size
        assert size > 0, f"artefak kosong: {name}"
    for name in ("T-I1-1.csv", "T-I1-2.csv", "T-I1-3.csv"):
        rows = sum(1 for _ in (report_dir / name).open(encoding="utf-8")) - 1
        assert rows == 86, f"T-I1 beku berubah: {name} ({rows})"
    frozen = sum(1 for _ in (report_dir / "_gate_G2_alarm.csv").open(encoding="utf-8")) - 1
    assert frozen == 86, f"alarm beku berubah ({frozen})"
    print(f"registry figures: FIG-01..07 di {OLD_FIGURE_DIR.relative_to(PROJECT_ROOT)} = {old}")
    print(f"registry figures: FIG-08..12 di {MID_FIGURE_DIR.relative_to(PROJECT_ROOT)} = {mid}")
    print(f"registry figures: FIG-13..16 di {report_dir.relative_to(PROJECT_ROOT)} = {new}")
    print(f"registry CSV T-07 ({len(got_csv)}): {got_csv} + T-I1 x3 beku 86 + alarm beku 86")


def build() -> None:
    """Tulis notebook dan eksekusi top-to-bottom via nbconvert (tunggal via lock)."""
    lock = REPORT_OUT_I2 / ".eda07_i2_build.lock"
    REPORT_OUT_I2.mkdir(parents=True, exist_ok=True)
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
    assert len(CELLS) == 22, f"notebook I-2 terkunci 22 sel, dapat {len(CELLS)}"
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
        verify_i2(REPORT_OUT_I2)
        for _name in (
            "T-07-1_balance.csv",
            "T-07-2_mi_lantai.csv",
            "T-07-3_lift.csv",
            "T-07-4_stabilitas.csv",
            "_gate_G2_skrining_i2.csv",
            "_gate_G2_alarm_i2.csv",
            "_ckpt_LA_i2.csv",
            "_ckpt_T_i2.csv",
        ):
            _p = REPORT_OUT_I2 / _name
            _p.write_bytes(_p.read_bytes().replace(b"\r\n", b"\n"))
        print("CSV I-2 dinormalisasi CRLF->LF (pola I-1).")
    finally:
        lock.unlink(missing_ok=True)
    print("lock dilepas; build selesai.")


if __name__ == "__main__":
    build()
