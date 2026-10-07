"""Generator + executor for notebooks/scalping/eda_05_regimes.ipynb.

Q7 (regime/day typology) and the final synthesis (H1-H5 with falsification
thresholds) for the scalping EDA chain, per Rancangan EDA v3.1 section 5 and
Lampiran A1 (R1-R3: all day-level work is locked to BROKER days; the UTC-day
label carries a structural -1 calendar offset and is never shifted to agree).

Every day-level metric is computed from native D1 broker-day buckets; strata
A/B/C reuse the exact nb01-nb04 day masks (B = H1-2023, C = anomaly windows
read from configs/data.yaml). Numbers that other notebooks locked (strata bar
counts, swing frequency, T-01 zero-mass) are re-derived here as regression
locks, not as new claims.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_05_regimes.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA 05 — Q7 Karakter per Regime + Sintesis Hipotesis H1-H5

**Rancangan:** EDA v3.1 (kanonik, §5 + Lampiran A1). **Purpose:** menutup rantai EDA —
tipologi hari (regime) per strata, lalu sintesis seluruh temuan nb01-nb04 menjadi
3-5 hipotesis kandidat metode yang **masing-masing falsifiable** (ambang yang
menggugurkannya di Lapisan 3). BUKAN output EDA: sinyal, model, backtest, P&L,
dan keputusan metode.

## Aturan yang mengikat notebook ini
- **Lampiran A1 R1-R3 (adjudikasi SA-03):** seluruh pekerjaan level-hari dikunci pada
  **tanggal-broker** (bucket D1 kalender-broker, batas tengah malam broker). Label
  "hari-UTC" membawa offset struktural −1 hari kalender; DILARANG menggeser data agar
  "sepakat". Hanya divergensi MELEBIHI geseran struktural yang menjadi temuan.
- **Metrik regime = §5 v3.1, bukan karangan:** tipologi hari dari rasio
  |return harian| terhadap Σ|r| intraday dan rasio range terhadap ATR; perbandingan
  A-vs-B di granularitas HARIAN (realized-vol harian, range/ATR harian, proporsi
  tipe-hari via chi-square) dengan KS/Mann-Whitney di level-hari **plus effect-size
  wajib** (beda median dengan CI, Cliff's delta). p-value tanpa effect-size dilarang
  disimpulkan.
- **Daya uji:** setiap tabel uji mencantumkan n-A/n-B/n-C; strata B (n=130 hari)
  hasil negatif dibaca "tidak terdeteksi pada n ini", bukan bukti kesamaan; catatan
  keterbatasan volatility clustering wajib; block bootstrap sirkular (block 20 hari,
  10.000 resample) hanya bila hasil hari-level marginal.
- **Reuse-First:** definisi sesi dari `_eda_common.py` (fingerprint di-assert); strata
  disalin pola nb03; dilarang modul baru di `src/`; nol imputasi; anti look-ahead.
- **Figures (skema D9):** notebook ini mengklaim **FIG-04..07** dan WAJIB memverifikasi
  registry direktori figures (tepat FIG-01..FIG-07).
- **Tidak** ada P&L, equity, backtest, pemilihan metode, penulisan `configs/`/`src/`,
  atau imputasi. **Tanpa bukti = tanpa klaim.**
"""
)

code(
    '''"""Setup lingkungan dan kunci definisi bersama."""
import importlib.metadata
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats


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
for package in ("pandas", "numpy", "scipy", "pyarrow", "tzdata"):
    print(f"  {package:11s}: {importlib.metadata.version(package)}")

assert importlib.metadata.version("tzdata") == "2026.5", "tzdata harus 2026.5 (Kontrak 00)"
assert int(importlib.metadata.version("pandas").split(".")[0]) == 2, (
    "Notebook WAJIB jalan di venv kanonik (pandas 2.x); pandas 3.x merusak satuan .asi8."
)
assert session_fingerprint() == EXPECTED_FINGERPRINT, "definisi sesi berubah - hentikan"
print("fingerprint sesi: OK (identik Kontrak 00)")''',
)

code(
    '''"""Muat D1 (bucket kalender-broker) dan kunci skema."""
config = load_config("data")
SYMBOL = config["mt5"]["symbol"]
YEARS = (2023, 2024, 2025, 2026)
ANOMALY_WINDOWS = tuple((w["start"], w["end"]) for w in config["validation"]["anomaly_windows"])
PIP_SIZE = float(config["spread"]["pip_size"][SYMBOL])
FIGURE_DIR = PROJECT_ROOT / "reports/eda/2026-10-06/figures"

D1_COLS = [
    "time",
    "broker_time_raw",
    "open",
    "high",
    "low",
    "close",
    "tick_volume",
    "m1_bars",
    "spread_pips_mean",
    "spread_pips_max",
]
d1 = pd.concat(
    [
        pd.read_parquet(PROJECT_ROOT / f"data/processed/D1/usdjpy_d1_{y}.parquet", columns=D1_COLS)
        for y in YEARS
    ],
    ignore_index=True,
)
d1["utc"] = pd.to_datetime(d1["time"], utc=True)
# Label hari D1 = tanggal bucket kalender-broker: broker_time_raw bucket adalah tengah
# malam broker, jadi wall_clock_series mengembalikan tepat 00:00 dinding hari tsb.
d1["wall"] = wall_clock_series(d1["broker_time_raw"])
d1["broker_day"] = d1["wall"].dt.normalize()
d1["year"] = d1["broker_day"].dt.year
d1 = d1.sort_values("utc", kind="mergesort").reset_index(drop=True)
assert d1["utc"].is_monotonic_increasing, "D1 harus urut waktu"
assert len(d1) == 974, f"D1 total bucket harus 974 (4 tahun), dapat {len(d1)}"
for col in ("open", "high", "low", "close", "m1_bars", "spread_pips_mean", "spread_pips_max"):
    assert col in d1.columns, f"kolom D1 hilang: {col}"
assert (d1["m1_bars"] > 0).all(), "ada bucket D1 tanpa bar M1"
print(f"D1: {len(d1):,} bucket kalender-broker 2023-2026 | pip={PIP_SIZE}")
print("tahun:", d1.groupby("year").size().to_dict())''',
)

code(
    '''"""Muat M1, strata hari A/B/C (pola nb03), dan kunci hitungan Lapisan 1."""
M1_COLS = ["time", "broker_time_raw", "close", "high", "low", "tick_volume", "spread_pips"]
m1 = pd.concat(
    [
        pd.read_parquet(PROJECT_ROOT / f"data/processed/M1/usdjpy_m1_{y}.parquet", columns=M1_COLS)
        for y in YEARS
    ],
    ignore_index=True,
)
m1["utc"] = pd.to_datetime(m1["time"], utc=True)
m1["wall"] = wall_clock_series(m1["broker_time_raw"])
m1["broker_day"] = m1["wall"].dt.normalize()
m1 = m1.sort_values("utc", kind="mergesort").reset_index(drop=True)
assert m1["utc"].is_monotonic_increasing, "M1 harus urut waktu"
m1["r"] = np.log(m1["close"] / m1["close"].shift(1))
TOTAL_DOC = 1_347_847
assert len(m1) == TOTAL_DOC, f"M1 total harus {TOTAL_DOC:,}, dapat {len(m1):,}"

wall_date = m1["broker_day"]
b_mask = (wall_date >= pd.Timestamp("2023-01-01")) & (wall_date <= pd.Timestamp("2023-06-30"))
c_mask = pd.Series(False, index=m1.index)
for start, end in ANOMALY_WINDOWS:
    c_mask |= (wall_date >= pd.Timestamp(start)) & (wall_date <= pd.Timestamp(end))
a_mask = ~(b_mask | c_mask)
assert not (b_mask & c_mask).any(), "B dan C tidak boleh tumpang tindih"

DAY_SETS = {
    "A": set(wall_date[a_mask].unique()),
    "B": set(wall_date[b_mask].unique()),
    "C": set(wall_date[c_mask].unique()),
}
BAR_COUNTS = {"A": int(a_mask.sum()), "B": int(b_mask.sum()), "C": int(c_mask.sum())}

# Kunci regresi dari Lapisan 1 / nb01-nb04 (dokumen): B=185.248, C=26.198,
# A=1.136.401; hari A=825, B=130, C=19 (5+14).
assert BAR_COUNTS["B"] == 185_248, f"stratum B M1 harus 185.248, dapat {BAR_COUNTS['B']:,}"
assert BAR_COUNTS["C"] == 26_198, f"stratum C M1 harus 26.198, dapat {BAR_COUNTS['C']:,}"
assert BAR_COUNTS["A"] == TOTAL_DOC - 185_248 - 26_198, "stratum A M1 tidak cocok"
assert (len(DAY_SETS["A"]), len(DAY_SETS["B"]), len(DAY_SETS["C"])) == (825, 130, 19), (
    f"hari A/B/C harus 825/130/19, dapat "
    f"{len(DAY_SETS['A'])}/{len(DAY_SETS['B'])}/{len(DAY_SETS['C'])}"
)
assert DAY_SETS["A"] | DAY_SETS["B"] | DAY_SETS["C"] == set(m1["broker_day"].unique()), (
    "strata hari harus menutup seluruh hari broker"
)
# R3: bucket D1 harus identik dengan hari broker M1 (satu kalender, bukan hari-UTC).
assert set(d1["broker_day"].unique()) == DAY_SETS["A"] | DAY_SETS["B"] | DAY_SETS["C"], (
    "bucket D1 != himpunan hari broker M1 - kalender tidak konsisten"
)
print("hari broker: A=825 B=130 C=19 | bar:", BAR_COUNTS)
print("PASS: stratifikasi hari-broker terkunci (R3: primer = tanggal-broker).")''',
)

md(
    """## 1. Metrik harian per strata (A/B/C) — tipologi hari

Semua dihitung dari **bucket D1 kalender-broker** (R3) dan agregat M1 per hari:

| Metrik | Definisi (§5 v3.1) |
|---|---|
| `ret_day` | ln(close/open) bucket D1 — arah & besar hari |
| `sum_abs_r` | Σ\\|r\\| intraday dari M1 (jalur harga, bukan net) |
| `rv_day` | Σr² intraday dari M1 (realized volatility) |
| `ratio_path` | \\|ret_day\\| / Σ\\|r\\| → 1 = satu arah, ≈0 = bolak-balik |
| `range_atr` | (high−low)/ATR(14) D1 — rentang vs volatilitas wajar |
| `tick_vol_sum` | Σ tick_volume M1 — proksi aktivitas [KD] |

Paritas `m1_bars` (parquet) vs hitungan ulang M1 di-assert per bucket — satu sumber
kalender. ATR(14) D1 memakai `shift(1)` (anti look-ahead): **14 hari pertama sampel**
(awal 2023, semuanya stratum B) belum punya ATR → dikeluarkan dari tipologi dengan
jumlah drop dilaporkan (aturan missing-data §6: drop dilaporkan, bukan diisi).

**Tipologi hari** (ambang = median strata A, deterministik setelah dihitung — bukan
tuning): `trending` bila ratio_path > median-A **dan** range_atr > median-A;
`range` bila keduanya ≤ median-A; selain itu `normal`.
**Ex-post (temuan audit L3-01, opsi b):** ambang dihitung dari SELURUH 825 hari A
(2023-01→2026, full-sample), sehingga label hari-t memakai informasi hari-hari
setelah t → label bersifat ex-post/deskriptif, TIDAK real-time-safe. Opsi ambang
walk-forward per tahun DITOLAK untuk EDA (mengubah angka tipologi/chi-square/H1 =
keputusan arsitektur, di luar scope fix; rancangan §2/§11: EDA deskriptif, metode
belum dipilih). Identifikasi tipe-hari secara real-time milik uji Lapisan 3
(H1: identifikasi H+1 pagi dengan data t-1 saja).
Perbandingan A-vs-B **wajib** level-hari: KS + Mann-Whitney + Cliff's delta +
beda median dengan CI bootstrap. n-A/n-B/n-C dicetak di tiap tabel."""
)

code(
    '''"""Hitung metrik harian, verifikasi paritas m1_bars, gabungkan strata."""
per_day_m1 = m1.groupby("broker_day").agg(
    sum_abs_r=("r", lambda s: float(np.nansum(np.abs(s)))),
    rv_day=("r", lambda s: float(np.nansum(np.square(s)))),
    tick_vol_sum=("tick_volume", "sum"),
    m1_bars_calc=("r", "size"),
)
daily = d1.set_index("broker_day").join(per_day_m1, how="inner")
assert len(daily) == 974, "join D1 x agregat M1 harus 974 hari"
parity = (daily["m1_bars"] == daily["m1_bars_calc"]).all()
assert parity, "m1_bars (parquet) != hitungan ulang dari M1 - sumber tidak konsisten"

daily["ret_day"] = np.log(daily["close"] / daily["open"])
daily["range_pips"] = (daily["high"] - daily["low"]) / PIP_SIZE
# ATR(14) D1 tanpa look-ahead: high-low hari t, dirata-rata 14 hari SEBELUM t.
tr = daily["high"] - daily["low"]
daily["atr14"] = tr.shift(1).rolling(14).mean()
daily["range_atr"] = daily["range_pips"] / daily["atr14"]
daily["ratio_path"] = daily["ret_day"].abs() / daily["sum_abs_r"]
daily["strata"] = np.select(
    [daily.index.isin(DAY_SETS["A"]), daily.index.isin(DAY_SETS["B"])],
    ["A", "B"],
    default="C",
)
assert daily["strata"].value_counts().to_dict() == {"A": 825, "B": 130, "C": 19}, (
    "label strata harian harus 825/130/19"
)
assert daily["ratio_path"].notna().all(), "ratio_path tidak boleh NaN"
warmup_nan = int(daily["range_atr"].isna().sum())
assert warmup_nan == 14, f"warmup ATR14 harus tepat 14 hari pertama, dapat {warmup_nan}"
assert daily.loc[daily["range_atr"].isna(), "strata"].eq("B").all(), (
    "hari warmup harus semuanya stratum B (awal 2023)"
)
print("paritas m1_bars: OK (974/974 bucket)")
print(f"warmup ATR14: {warmup_nan} hari stratum B tanpa range_atr (dikeluarkan dari tipologi)")
med_a = daily.loc[daily["strata"] == "A", ["ratio_path", "range_atr"]].median()
TH_RATIO, TH_RANGE = float(med_a["ratio_path"]), float(med_a["range_atr"])
print(f"ambang tipologi (median A full-sample 825 hari, ex-post — bukan ambang real-time): ratio_path={TH_RATIO:.4f} range_atr={TH_RANGE:.4f}")

COLS = ["ret_day", "sum_abs_r", "rv_day", "range_pips", "range_atr", "ratio_path", "tick_vol_sum"]
print()
print("=== median metrik harian per strata ===")
for strata_name in ("A", "B", "C"):
    frame = daily[daily["strata"] == strata_name]
    print(f"--- stratum {strata_name} (n={len(frame)} hari) ---")
    print(frame[COLS].median().round(4).to_string())
print()
print("PASS: metrik harian selesai.")''',
)

code(
    '''"""Tipologi hari (trending/range/normal) pada 960 hari valid + chi-square A-vs-B."""
valid = daily[daily["range_atr"].notna()].copy()
assert len(valid) == 974 - 14, "hari valid harus 960"
valid["tipe"] = np.select(
    [
        (valid["ratio_path"] > TH_RATIO) & (valid["range_atr"] > TH_RANGE),
        (valid["ratio_path"] <= TH_RATIO) & (valid["range_atr"] <= TH_RANGE),
    ],
    ["trending", "range"],
    default="normal",
)
assert set(valid["tipe"].unique()) <= {"trending", "range", "normal"}, "tipe bocor"
TIPO_ORDER = ["trending", "normal", "range"]
crosstab = pd.crosstab(valid["strata"], valid["tipe"]).reindex(
    index=["A", "B", "C"], columns=TIPO_ORDER, fill_value=0
)
assert int(crosstab.loc["A"].sum()) == 825, "n-A tipologi harus 825"
assert int(crosstab.loc["B"].sum()) == 116, "n-B tipologi harus 116 (130 - 14 warmup)"
assert int(crosstab.loc["C"].sum()) == 19, "n-C tipologi harus 19"
crosstab_pct = crosstab.div(crosstab.sum(axis=1), axis=0).round(4) * 100
print("=== distribusi tipe hari per strata (n-A=825, n-B=116, n-C=19; 14 warmup B drop) ===")
print("hitungan:")
print(crosstab.to_string())
print("persen:")
print(crosstab_pct.round(1).to_string())

chi2, p_chi, dof, expected = scipy.stats.chi2_contingency(crosstab.loc[["A", "B"]].values)
assert (expected > 0).all(), "sel ekspektasi chi-square nol"
print()
print(f"chi-square tipe-hari A vs B: chi2={chi2:.3f} dof={dof} p={p_chi:.4g} "
      f"(n-A=825, n-B=116)")
print("CATATAN DAYA: n-B kecil; hasil negatif = 'tidak terdeteksi pada n ini'.")
print("CATATAN CLUSTERING: hari saling bergantung (volatility clustering); uji level-hari")
print("mengurangi - tidak menghapus - dependensi; block bootstrap menyusul bila marginal.")''',
)

code(
    '''"""Uji A-vs-B level-hari: KS + Mann-Whitney + Cliff's delta + CI beda median."""
METRICS = ("rv_day", "range_atr", "sum_abs_r", "ratio_path")
rng = np.random.default_rng(20261006)  # seed Kontrak 00 (bukan parameter metrik baru)
B_BOOT = 2_000

rows = []
for metric in METRICS:
    a_vals = daily.loc[daily["strata"] == "A", metric].dropna().to_numpy()
    b_vals = daily.loc[daily["strata"] == "B", metric].dropna().to_numpy()
    n_b_expected = 116 if metric == "range_atr" else 130
    assert a_vals.size == 825 and b_vals.size == n_b_expected, (
        f"n {metric} tidak {825}/{n_b_expected}"
    )
    ks_stat, ks_p = scipy.stats.ks_2samp(a_vals, b_vals)
    mw = scipy.stats.mannwhitneyu(a_vals, b_vals, alternative="two-sided")
    cliffs = 2.0 * mw.statistic / (a_vals.size * b_vals.size) - 1.0
    med_a, med_b = float(np.median(a_vals)), float(np.median(b_vals))
    boot = np.empty(B_BOOT)
    for i in range(B_BOOT):
        sa = rng.choice(a_vals, size=a_vals.size, replace=True)
        sb = rng.choice(b_vals, size=b_vals.size, replace=True)
        boot[i] = np.median(sb) - np.median(sa)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    rows.append(
        {
            "metrik": metric,
            "n_A": a_vals.size,
            "n_B": b_vals.size,
            "median_A": round(med_a, 5),
            "median_B": round(med_b, 5),
            "beda_median_B-A": round(med_b - med_a, 5),
            "ci95_beda_iid": f"[{lo:.5f}, {hi:.5f}]",
            "cliffs_delta": round(cliffs, 4),
            "KS_D": round(float(ks_stat), 4),
            "KS_p": f"{ks_p:.3g}",
            "MW_p": f"{mw.pvalue:.3g}",
        }
    )
TESTS = pd.DataFrame(rows)
print("=== A vs B, uji level-hari (effect-size wajib; p tanpa effect-size tidak disimpulkan) ===")
print("(kolom ci95_beda_iid = bootstrap IID per hari; dependensi temporal diakui — lihat CATATAN CLUSTERING)")
print("(KONVENSI TANDA B4-08: cliffs_delta = P(A>B) − P(B>A); negatif berarti B cenderung LEBIH BESAR)")
print(TESTS.to_string(index=False))

marginal = [r["metrik"] for r in rows if float(r["MW_p"]) > 0.01]
print()
print(f"metrik marginal (MW p > 0,01): {marginal if marginal else 'TIDAK ADA'}")
if marginal:
    print("→ block bootstrap sirkular (block 20 hari ≈ 1 bulan dagang, menutup musiman mingguan — Kontrak 00; 10.000 resample, seed 20261006; KEDUA sisi A dan B di-resample blok — KOREKSI L3-02):")
    a_days = daily.loc[daily["strata"] == "A"].index.to_numpy()
    for metric in marginal:
        a_vals = daily.loc[a_days, metric].to_numpy()
        b_vals = daily.loc[daily["strata"] == "B", metric].dropna().to_numpy()
        n_block = 20
        n_blocks = int(np.ceil(a_vals.size / n_block))
        n_blocks_b = int(np.ceil(b_vals.size / n_block))
        b_rng = np.random.default_rng(20261006)
        boots = np.empty(10_000)
        for i in range(10_000):
            starts = b_rng.integers(0, a_vals.size, size=n_blocks)
            idx = ((starts[:, None] + np.arange(n_block)[None, :]) % a_vals.size).ravel()
            idx = idx[: a_vals.size]
            starts_b = b_rng.integers(0, b_vals.size, size=n_blocks_b)
            idx_b = ((starts_b[:, None] + np.arange(n_block)[None, :]) % b_vals.size).ravel()
            idx_b = idx_b[: b_vals.size]
            boots[i] = np.median(b_vals[idx_b]) - np.median(a_vals[idx])
        lo, hi = np.percentile(boots, [2.5, 97.5])
        print(f"  {metric}: beda median B-A CI95-block(kedua sisi)=[{lo:.5f}, {hi:.5f}]")
else:
    print("→ block bootstrap TIDAK dijalankan (kontrak: hanya bila hasil marginal).")''',
)

md(
    """## 2. Sintesis rantai EDA → draf hipotesis H1-H5

Format wajib §11 v3.1: {klaim, metrik EDA pendukung, rencana uji Lapisan 3, ambang
falsifikasi}. Angka pendukung **dihitung ulang ringkas** di notebook ini sebagai
regresi-lock (sumber penuh = nb01-nb04); ambang falsifikasi adalah angka Lapisan 3,
bukan angka EDA. Metode BELUM dipilih — hipotesis adalah kandidat. Teks klaim
menyematkan angka yang benar-benar terukur, bukan angka harapan."""
)

code(
    '''"""Replica ringkas angka kunci nb03 (ACF lag-1 & VR M15, strata A) sebagai lock.

Metode replika = METODE EKSAK nb03 (bukan varian nb05): VR memakai salinan
verbatim fungsi `variance_ratio` nb03 (ddof=1, jumlah bertumpang tindih via
cumsum) di atas seri NO-GAP berbasis kolom `gap_return` (definisi stratifikasi
nb00: `utc.diff() > 15 menit` untuk M15) - sama seperti pemanggilan nb03.
ACF lag-1 = ACF BESARAN seri penuh (padanan `acf_all` tabel nb03, bukan
`acf_no_gap`); sign-ACF lag-1 memakai rumus `acf_table` nb03 pada seri no-gap
yang sama dengan VR."""
M15_COLS = ["time", "broker_time_raw", "close"]
m15 = pd.concat(
    [
        pd.read_parquet(
            PROJECT_ROOT / f"data/processed/M15/usdjpy_m15_{y}.parquet", columns=M15_COLS
        )
        for y in YEARS
    ],
    ignore_index=True,
)
m15["utc"] = pd.to_datetime(m15["time"], utc=True)
# Pemetaan hari M15 = METODE EKSAK nb03 (load_timeframe): wall_clock_series atas
# broker_time_raw bar M15 sendiri. Versi sebelumnya memakai aproksimasi searchsorted
# terhadap awal-hari M1; itu menggeser bucket pembuka hari yang M1-nya terlambat
# (mis. 22:07) ke hari sebelumnya, sehingga himpunan bar A dan hitungan gap_return
# tidak identik nb03. Disamakan agar replika benar-benar apples-to-apples.
m15["wall"] = wall_clock_series(m15["broker_time_raw"])
m15["broker_day"] = m15["wall"].dt.normalize()
m15 = m15.sort_values("utc", kind="mergesort").reset_index(drop=True)
m15["r"] = np.log(m15["close"] / m15["close"].shift(1))
# Definisi no-gap = kolom `gap_return` milik stratifikasi nb00 (return yang
# menyeberangi gap > 15 menit dibuang) - BUKAN adjacency timestamp yang dibangun
# ulang. Versi adjacency lama menghasilkan sign-ACF -0,022005 (meleset 2,74% dari
# nb03) karena himpunan pasangannya berbeda; kolom gap_return mereplikasi nb03
# secara eksak (terverifikasi offline sebelum rerun).
m15["gap_return"] = m15["utc"].diff() > pd.Timedelta(minutes=15)
m15_a = m15[m15["broker_day"].isin(DAY_SETS["A"])]
assert int(m15_a["broker_day"].nunique()) == 825, "stratum A M15 harus 825 hari"
assert len(m15_a) == 75_863, f"bar M15-A harus 75.863 (paritas nb03), dapat {len(m15_a):,}"
assert int(m15_a["gap_return"].sum()) == 825, "gap_return M15-A harus 825 (paritas nb03)"
r15 = m15_a["r"].dropna()
acf1_m15_a = float(r15.autocorr(lag=1))


def variance_ratio(series: pd.Series, lag: int) -> float:
    """Hitung VR(lag) dari satu seri return (formulasi Lo-MacKinlay).

    SALINAN VERBATIM dari `scripts/_build_eda03.py` (sumber kebenaran Q4) agar
    replika benar-benar se-metode dengan nb03: varian ddof=1, dan r_lag adalah
    JUMLAH lag return satu-periode yang bertumpang tindih
    (r_t + r_{t-1} + ... + r_{t-lag+1}), bukan selisihnya.

    Args:
        series: Seri return float.
        lag: Lag yang diuji.

    Returns:
        Var(r_lag) / (lag x Var(r_1)). Bernilai tepat 1 untuk lag=1, dan
        bernilai 1 untuk semua lag bila return iid.
    """
    values = series.to_numpy(dtype="float64")
    values = values[np.isfinite(values)]
    var1 = float(np.var(values, ddof=1))
    # Jumlah bertumpang tindih dihitung lewat cumulative sum supaya O(n).
    # JANGAN pakai (values[lag:] - values[:-lag]): itu SELISIH, bukan jumlah,
    # sehingga VR(1) = 2 dan VR(l) menuju 0 saat lag naik (bug ditemukan oleh
    # assertion "VR(lag=1) mendekati 1" pada eksekusi pertama nb03).
    cumulative = np.concatenate(([0.0], np.cumsum(values)))
    lag_sum = cumulative[lag:] - cumulative[:-lag]
    var_lag = float(np.var(lag_sum, ddof=1))
    return var_lag / (lag * var1)


no_gap = ~m15_a["gap_return"]
clean = m15_a.loc[no_gap, "r"]
n_no_gap = int(len(clean))
vr = {k: variance_ratio(clean, k) for k in (5, 15, 60)}
mean_vr = float(np.mean(list(vr.values())))
print(f"replica nb03 M15 (stratum A): ACF lag-1 (all) = {acf1_m15_a:.6f}")
print("VR per horizon: " + ", ".join(f"VR({k})={v:.4f}" for k, v in vr.items()))
print(f"rata-rata VR(5,15,60) = {mean_vr:.4f} (referensi nb03: 1,0312)")
print("catatan: 1,0337 pada nb03 = rata-rata VR LAG 2-60, bukan pembanding horizon 5/15/60")
# Kunci ketat fidelity (audit MEDIUM-02): toleransi eksplisit terhadap angka nb03.
assert abs(acf1_m15_a - 0.001793) < 0.0005, (
    "ACF1 M15 A menyimpang dari acf_all nb03 (0,001793) - investigasi"
)
assert abs(acf1_m15_a) < 0.05, "band lebar kedua: |ACF1| M15 A harus kecil"
assert abs(mean_vr - 1.0312) < 0.005, (
    "rata-rata VR M15 A keluar dari referensi nb03 1,0312 - investigasi"
)
assert 1.025 < mean_vr < 1.038, "band lebar kedua: rata-rata VR harus di sekitar 1"
# Sign-ACF lag-1 (no-gap) = headline D4 nb03 (-0,022624 M15 A) - kunci replikanya.
sign_frame = pd.DataFrame({"r": np.sign(m15_a["r"])})
values = sign_frame.loc[no_gap, "r"].to_numpy(dtype="float64")
values = values[np.isfinite(values)]
values = values - values.mean()
denom = float(np.dot(values, values))
sign_acf1 = float(np.dot(values[:-1], values[1:])) / denom
print(f"replica nb03: sign-ACF lag-1 M15 (A, no-gap kolom gap_return) = {sign_acf1:.6f}")
print("  (referensi nb03: -0,022624)")
print(f"n_no_gap M15-A = {n_no_gap:,} bar (nb03: 75.038); definisi no-gap = kolom gap_return")
assert n_no_gap == 75_038, "n no-gap M15-A tidak cocok dengan nb03 - definisi no-gap berbeda"
assert abs(sign_acf1 + 0.022624) < 0.001, (
    "sign-ACF lag-1 M15 A keluar dari referensi nb03 (-0,022624) - investigasi"
)
assert -0.030 < sign_acf1 < -0.015, "band lebar kedua: sign-ACF harus negatif lemah"''',
)

code(
    '''"""Replica ringkas: mean|r| & spread per sesi (M1 per-bar, strata A) → basis H4/H5 (M4 kanon: spread_p95).

KOREKSI B4-04 pasca-audit Batch B: proksi mean-D1 harian (rentang antar-sesi hanya
0,0086 pip, praktis datar → dimensi "spread" tak terukur) DIGANTI spread_pips
per-bar M1 + p95 per sesi sesuai kanon M4 (eda_design_v3.1.md:64 = rasio mean|r|
terhadap spread_p95). Kolom proksi lama dipertahankan TERCETAK sebagai pembanding
lama→baru, BUKAN dipakai klaim."""
m1_a = m1[m1["broker_day"].isin(DAY_SETS["A"])].copy()
m1_a = add_labels(m1_a)
assert int(m1_a["broker_day"].nunique()) == 825, "stratum A M1 harus 825 hari"
m1_a["abs_r_pips"] = m1_a["r"].abs() * m1_a["close"] / PIP_SIZE
assert m1_a["spread_pips"].notna().all(), "ada bar M1 A tanpa spread per-bar"
d1_spread = d1.set_index("broker_day")["spread_pips_mean"]
m1_a["spread_mean_day"] = m1_a["broker_day"].map(d1_spread)
assert m1_a["spread_mean_day"].notna().all(), "ada bar M1 A tanpa spread harian D1"
ses = m1_a.groupby("session_label").agg(
    n_bar=("r", "size"),
    mean_abs_r_pips=("abs_r_pips", "mean"),
    spread_mean_bar_pips=("spread_pips", "mean"),
    spread_p95_bar_pips=("spread_pips", lambda s: float(s.quantile(0.95))),
    spread_mean_D1_lama_pips=("spread_mean_day", "mean"),
)
ses["rasio_vol_over_spread"] = ses["mean_abs_r_pips"] / ses["spread_p95_bar_pips"]
ses = ses.reindex([s for s in SESSION_ORDER if s in ses.index])
print("=== M4 kanon: rasio mean|r| (pip/bar) terhadap spread p95 per-bar (pip) per sesi ===")
print(ses.round(4).to_string())
flagged = ses.index[ses["rasio_vol_over_spread"] < 1.0].tolist()
print(f"flag 'biaya-mendominasi' M4 (rasio p95 < 1): {flagged}")
cfg_basis = config["spread"]["cost_basis"]["by_session"]
for sesi in ("London", "NewYork", "Tokyo", "Sydney"):
    print(f"  cek silang {sesi}: mean per-bar={ses.loc[sesi, 'spread_mean_bar_pips']:.4f} "
          f"vs cost_basis={cfg_basis[sesi]:.2f}")
assert len(ses) >= 4, "label sesi utama harus lengkap"
assert (ses["mean_abs_r_pips"] > 0).all() and (ses["spread_p95_bar_pips"] > 0).all(), (
    "angka sesi harus positif"
)
assert all(
    abs(float(ses.loc[s, "spread_mean_bar_pips"]) - float(cfg_basis[s])) < 0.02
    for s in ("London", "NewYork", "Tokyo", "Sydney")
), "mean per-bar menyimpang dari cost_basis fragmen 4b - investigasi"
assert set(flagged) == {"NewYork", "Sydney"}, (
    f"flag M4 harus NewYork+Sydney (replika audit B4-04), dapat {flagged}"
)''',
)

code(
    '''"""Replica ringkas: frekuensi swing M5 k=3 (A) sebagai lock nb04/D6."""
M5_COLS = ["time", "broker_time_raw", "high", "low"]
m5 = pd.concat(
    [
        pd.read_parquet(PROJECT_ROOT / f"data/processed/M5/usdjpy_m5_{y}.parquet", columns=M5_COLS)
        for y in YEARS
    ],
    ignore_index=True,
)
m5["utc"] = pd.to_datetime(m5["time"], utc=True)
# Pemetaan hari M5 = METODE EKSAK (wall_clock_series atas broker_time_raw bar M5
# sendiri, pola M15 di atas — KOREKSI L3-05). Pemetaan searchsorted lama terhadap
# awal-hari M1 DIHAPUS: ia menggeser 287 bar pembuka-hari (22:05 UTC) ke hari
# sebelumnya (terukur: 287 bar/287 hari; 114 melintasi batas A). Angka 40.483
# tidak berubah, tetapi assertion lama (n_leading5 == 1) memberi rasa aman semu
# sehingga diganti paritas absolut di bawah.
m5["wall"] = wall_clock_series(m5["broker_time_raw"])
m5["broker_day"] = m5["wall"].dt.normalize()
m5 = m5.sort_values("utc", kind="mergesort").reset_index(drop=True)
assert m5["broker_day"].notna().all(), "ada bar M5 tanpa hari broker"
m5_a = m5[m5["broker_day"].isin(DAY_SETS["A"])]
assert int(m5_a["broker_day"].nunique()) == 825, "stratum A M5 harus 825 hari"
assert len(m5_a) == 227_568, f"bar M5-A eksak harus 227.568, dapat {len(m5_a):,}"


def fractal_mask(values: np.ndarray, k: int, high: bool) -> np.ndarray:
    """Tandai bar yang merupakan fraktal k-per-sisi.

    SALINAN VERBATIM dari `scripts/_build_eda04.py` (sumber kebenaran Q5) -
    replika sebelumnya (OR per-pasangan tetangga) BUKAN algoritma nb04 dan
    menghasilkan ~10x terlalu banyak swing (lampu merah kedua, diperbaiki).

    Args:
        values: Array high atau low.
        k: Jumlah bar per sisi.
        high: True untuk swing high, False untuk swing low.

    Returns:
        Array boolean sepanjang values, True di bar fraktal.
    """
    n = len(values)
    out = np.zeros(n, dtype=bool)
    if n <= 2 * k:
        return out
    for i in range(k, n - k):
        left = values[i - k : i]
        right = values[i + 1 : i + k + 1]
        center = values[i]
        if high:
            out[i] = center > left.max() and center > right.max()
        else:
            out[i] = center < left.min() and center < right.min()
    return out


high = m5_a["high"].to_numpy(dtype="float64")
low = m5_a["low"].to_numpy(dtype="float64")
swings = int(fractal_mask(high, 3, True).sum() + fractal_mask(low, 3, False).sum())
SWING_PER_DAY_K3 = swings / 825
print(f"replica nb04: swing M5 k=3 high+low (A) = {swings:,} → {SWING_PER_DAY_K3:.2f} swing/hari")
print("referensi nb04: k=3 high 20.169 / low 20.314 (≈49/hari); gabungan k=3+k=5 = 48,74/hari")
assert abs(SWING_PER_DAY_K3 - 49.070) < 0.05, (
    "swing/hari k=3 keluar dari referensi nb04 49,070 (24.447 + 24.623) - investigasi"
)
assert 45.0 < SWING_PER_DAY_K3 < 52.0, "band lebar kedua: frekuensi swing k=3 wajar"''',
)

md(
    """### Draf hipotesis (format §11: klaim · metrik EDA · uji Lapisan 3 · ambang falsifikasi)

Ambang di bawah adalah **ambang Lapisan 3** (menggugurkan hipotesis), dinyatakan
eksplisit sebelum pengujian di sana. Angka EDA di sel berikutnya adalah *pendukung*,
bukan pembuktian."""
)

code(
    '''"""H1 - Regime day-trading trend/consolidation (dari Q7 tipologi).

KOREKSI B4-01 pasca-audit Batch B: bucket "range" = hari TENANG (ratio_path DAN
range/ATR ≤ median-A: volatilitas & range TERENDAH, bukan "choppy lebar") —
definisi kini eksplisit di klaim. Kontras trending-vs-range TERCEMAR level
volatilitas (Σ|r| trending 1,27x); uji Lapisan 3 karenanya memakai drift
RELATIF (dinormalisasi ATR harian), bukan drift absolut pip."""
h1 = {
    "klaim": (
        "Hari-hari terbagi dalam tipe yang terukur: hari trending "
        "(ratio_path dan range/ATR di atas median A) vs hari range = hari tenang "
        "(KEDUA metrik di bawah/≤ median A: volatilitas & range terendah) vs "
        "normal (campuran); kelanjutan arah pada hari trending layak diuji. "
        f"Share terukur (stratum A): "
        f"trending {crosstab_pct.loc['A', 'trending']:.1f}%, range "
        f"{crosstab_pct.loc['A', 'range']:.1f}%, normal "
        f"{crosstab_pct.loc['A', 'normal']:.1f}%."
    ),
    "metrik_pendukung": {
        "share_trending_A_pct": round(float(crosstab_pct.loc["A", "trending"]), 2),
        "share_range_A_pct": round(float(crosstab_pct.loc["A", "range"]), 2),
        "share_normal_A_pct": round(float(crosstab_pct.loc["A", "normal"]), 2),
        "chi2_p_A_vs_B": f"{p_chi:.3g}",
        "n_A": 825,
        "n_B": 116,
    },
    "uji_lapisan3": (
        "Conditioning on tipe hari (teridentifikasi H+1 pagi dengan data t-1 saja): "
        "hitung drift berarah RELATIF (M15 4 jam pertama sesi London dinormalisasi "
        "ATR harian t-1 — normalisasi memisahkan 'kelanjutan arah' dari "
        "'pergerakan lebih besar', koreksi confound level-volatilitas B4-01) pada "
        "hari trending vs range, sign test + bootstrap CI."
    ),
    "ambang_falsifikasi": (
        "GUGUR bila selisih drift median (trending - range) CI95 memuat 0, ATAU bila "
        "share trending tidak stabil antar tahun (chi-square antar-tahun p<0,01)."
    ),
}
assert 0 < h1["metrik_pendukung"]["share_trending_A_pct"] < 100, "share trending degenerat"
print("H1:", h1["klaim"])
print("   pendukung:", h1["metrik_pendukung"])
print("   ambang:", h1["ambang_falsifikasi"])''',
)

code(
    '''"""H2 - Micro-momentum M15 (dari Q4: ACF & VR).

KOREKSI B4-07 pasca-audit Batch B: kata "terukur" DITURUNKAN — seluruh statistik
pendukung tak berbeda dari iid (z<1, CI95 memuat 0); angka dihitung ulang di sel
ini, BUKAN disalin audit. H2 dipertahankan sebagai hipotesis eksploratori yang
diuji di Lapisan 3, bukan sebagai temuan EDA.
KOREKSI B4-06: ambang "≥3 dari 4 tahun OOS" TIDAK DAPAT DIEKSEKUSI (span
2023-01-02→2026-10-02 = 3,75 tahun; 2026 hanya 196 hari) → diganti ambang
3-tahun-utuh yang dapat dievaluasi; ambang 4-tahun penuh MENUNGGU DATA."""
n_acf = int(r15.size)
se_acf = 1.0 / np.sqrt(n_acf)
z_acf = float(acf1_m15_a) / se_acf
ci_acf = (float(acf1_m15_a) - 1.96 * se_acf, float(acf1_m15_a) + 1.96 * se_acf)
h2 = {
    "klaim": (
        "Return M15 strata A menunjukkan pola horizon-pendek yang lemah dan "
        "SECARA STATISTIK TAK TERBEDAKAN dari iid "
        f"(ACF lag-1 = {acf1_m15_a:.4f}, z = {z_acf:.2f}, CI95 "
        f"[{ci_acf[0]:+.5f}, {ci_acf[1]:+.5f}] memuat 0; VR(5,15,60) z ≈ "
        "0,90/0,20/0,26 per audit independen): rata-rata VR(5,15,60) = "
        f"{mean_vr:.4f} (>1 = momentum lemah; referensi nb03 1,0312, metode eksak "
        "nb03: ddof=1 + no-gap kolom gap_return). Sinyal trend-following M15 "
        "layak diuji dengan biaya penuh SEBAGAI HIPOTESIS EKSPLORATORI — "
        "EDA tidak mengklaim sinyal terdeteksi."
    ),
    "metrik_pendukung": {
        "acf1_M15_A_all": round(acf1_m15_a, 6),
        "acf1_z_vs_iid": round(z_acf, 3),
        "acf1_ci95": [round(ci_acf[0], 6), round(ci_acf[1], 6)],
        "signifikan_vs_iid": bool(abs(z_acf) > 1.96),
        "sign_acf1_M15_A_nogap": round(sign_acf1, 6),
        "vr5_M15_A": round(vr[5], 4),
        "vr15_M15_A": round(vr[15], 4),
        "vr60_M15_A": round(vr[60], 4),
        "mean_vr": round(mean_vr, 4),
        "referensi_vr_nb03": 1.0312,
        "catatan": (
            "ACF M1 lag-1 negatif = mikrostruktur (bid-bounce), bukan sinyal. "
            "1,0337 pada nb03 = rata-rata VR lag 2-60, bukan pembanding horizon."
        ),
    },
    "uji_lapisan3": (
        "Strategy-like diagnostic: expected value per trade M15 momentum sederhana "
        "dikurangi cost_basis mean sesi (fragmen 4b), walk-forward per tahun."
    ),
    "ambang_falsifikasi": (
        "GUGUR bila EV-after-cost median ≤ 0 di ≥2 dari 3 tahun utuh 2023-2025 "
        "out-of-sample (2026 parsial 196 hari dikecualikan sebagai tahun berjalan; "
        "klarifikasi B4-06: ambang 4-tahun penuh MENUNGGU DATA), ATAU "
        "bila rata-rata VR out-of-sample ≤ 1."
    ),
}
assert ci_acf[0] < 0 < ci_acf[1], "CI95 ACF1 harus memuat 0 (replika B4-07)"
assert abs(z_acf) < 1.0, "z ACF1 harus < 1 (tak signifikan, replika B4-07)"
assert abs(mean_vr - 1.0312) < 0.005, (
    "pendukung H2 keluar dari referensi nb03 1,0312 - investigasi"
)
assert 0.9 < mean_vr < 1.2, "band lebar kedua: pendukung H2 harus dekat 1"
print("H2:", h2["klaim"])
print("   pendukung:", h2["metrik_pendukung"])''',
)

code(
    '''"""H3 - Regime-conditional filtering strata (dari Q4/Q7: A vs B)."""
rv_a = float(daily.loc[daily["strata"] == "A", "rv_day"].median())
rv_b = float(daily.loc[daily["strata"] == "B", "rv_day"].median())
rasio_rv = rv_b / rv_a
row_rv = TESTS[TESTS["metrik"] == "rv_day"].iloc[0]
h3 = {
    "klaim": (
        f"Regime H1-2023 (stratum B) berbeda level-hari dari A: median realized-vol "
        f"harian B = {rv_b:.6f} vs A = {rv_a:.6f} (rasio {rasio_rv:.2f}x), Cliff's "
        f"delta = {float(row_rv['cliffs_delta']):.3f} (KONVENSI TANDA B4-08: "
        "δ = P(A>B) − P(B>A); δ<0 berarti B cenderung LEBIH BESAR). Jika "
        "perbedaan ini dapat dideteksi real-time dari realized-vol rolling, "
        "filter regime menaikkan ketahanan strategi tanpa mengganti aturan."
    ),
    "metrik_pendukung": {
        "median_rv_A": round(rv_a, 8),
        "median_rv_B": round(rv_b, 8),
        "rasio_B_over_A": round(rasio_rv, 3),
        "cliffs_delta_rv": float(row_rv["cliffs_delta"]),
        "KS_p": row_rv["KS_p"],
        "n_A": 825,
        "n_B": 130,
    },
    "uji_lapisan3": (
        "Detektor regime real-time (RV rolling 20 hari > ambang) diuji apakah "
        "mengklasifikasikan hari B tanpa melihat label strata (AUC harian)."
    ),
    "ambang_falsifikasi": (
        "GUGUR bila detektor tidak memisahkan B dari A (AUC ≤ 0,7) ATAU bila "
        "filter memotong > 40% hari A tanpa mengurangi drawdown "
        "(klarifikasi B4-11: drawdown = max peak-to-trough pada kurva ekuitas "
        "strategi diagnostik Lapisan 3; strategi BELUM dipilih — ambang "
        "dievaluasi saat strategi ada)."
    ),
}
assert 0.5 < rasio_rv < 10.0, "rasio RV B/A di luar band masuk akal - investigasi"
print("H3:", h3["klaim"])
print("   pendukung:", h3["metrik_pendukung"])''',
)

code(
    '''"""H4 - Sesi-as-alpha (dari Q2/Q3 + M2 kalibrasi jam + M3 sensitivitas di sel berikut).

KOREKSI B4-02: share_Off_di_top6 hanya mengukur "di dalam sesi berlabel" (juga
dipenuhi Tokyo/Sydney) — DITAMBAH metrik massa London+NY yang benar-benar menguji
klaim konsentrasi London/NY (metrik lama dipertahankan, bukan dihapus). Jam 00 UTC
(peringkat 3, 100% Tokyo) dicatat sebagai caveat eksplisit di klaim.
KOREKSI B4-03: guard mesin diketatkan menegakkan kanon M2 (gugur pada ≥2 Off)."""
hourly = m1_a.copy()
hourly["hour_utc"] = hourly["utc"].dt.hour
assert (
    "hour_utc" in hourly.columns
    and len(hourly) > 0
    and hourly["hour_utc"].notna().all()
    and hourly["hour_utc"].between(0, 23).all()
), "hour_utc hilang/rusak - regresi B9-01 (KeyError hour_utc pada riwayat nb05)"
vol_hour = hourly.groupby("hour_utc")["abs_r_pips"].mean().sort_values(ascending=False)
top6 = list(vol_hour.head(6).index)
in_session = hourly.loc[hourly["hour_utc"].isin(top6), "session_label"]
share_off_top6 = float((in_session == "Off").mean())
n_off_top6 = int((in_session == "Off").sum())
massa_top6 = hourly.loc[hourly["hour_utc"].isin(top6)].groupby("session_label")["abs_r_pips"].sum()
share_londonny_top6 = float(
    (float(massa_top6.get("London", 0.0)) + float(massa_top6.get("NewYork", 0.0)))
    / float(massa_top6.sum())
)
rank = {
    s: float(ses.loc[s, "mean_abs_r_pips"])
    for s in ses.index
    if s in ("London", "NewYork", "Tokyo")
}
rank_ok = rank.get("London", 0) > rank.get("NewYork", 0) > rank.get("Tokyo", 0)
h4 = {
    "klaim": (
        "Volatilitas terkonsentrasi di jam-jam sesi berlabel (M2: 6 jam teratas "
        "harus di dalam sesi berlabel) dengan massa |r| London+NY "
        f"{share_londonny_top6 * 100:.1f}% dari massa 6 jam teratas (definisi: "
        "Σ|r| pip per sesi pada 6 jam teratas) - strategi "
        "sesi-pintu (trade hanya di jam tertentu) layak diuji sebagai alpha "
        "kapasitas-rendah. Caveat: konsentrasi London/NY parsial, bukan eksklusif "
        "(jam 00 UTC peringkat 3 = 100% Tokyo; ranking sesi Tokyo>NY menyalahi "
        "prior S5 — deviasi M1 dilaporkan jujur)."
    ),
    "metrik_pendukung": {
        "top6_jam_utc": top6,
        "share_Off_di_top6": round(share_off_top6, 4),
        "n_Off_di_top6": n_off_top6,
        "share_LondonNY_massa_top6": round(share_londonny_top6, 4),
        "ranking_mean_abs_r": {k: round(v, 4) for k, v in rank.items()},
        "ranking_sesuai_prior_USDJPY": bool(rank_ok),
    },
    "uji_lapisan3": (
        "Sesi-window strategy diagnostic: EV-after-cost per jam masuk, korelasi "
        "antar-tahun jam teratas (stabilitas jam)."
    ),
    "ambang_falsifikasi": (
        "GUGUR bila > 1 dari 6 jam teratas jatuh di sesi Off pada data out-of-sample "
        "baru, ATAU bila EV-after-cost semua jam masuk (6 jam teratas) ≤ 0 "
        "(klarifikasi B4-11: 'semua jam' = 6 jam masuk H4)."
    ),
}
assert n_off_top6 < 2, "M2 kanon: ≥2 jam Off di top6 memicu revisi batas - guard mesin"
assert len(rank) == 3, "label London/NewYork/Tokyo harus lengkap di stratum A"
print("H4:", h4["klaim"])
print("   pendukung:", h4["metrik_pendukung"])''',
)

code(
    '''"""M3 - Sensitivitas pelabelan sesi: DST-aware (primer) vs cross-tab UTC-tetap.

KOREKSI B4-12 pasca-audit Batch B: item preregistrasi M3 (eda_design_v3.1.md:64)
kini DIJALANKAN dan dilaporkan sebagai sensitivitas; pelabelan DST-aware tetap
primer. Kolom session_label_xtab sudah tersedia via add_labels (_eda_common)."""
rank_dst = m1_a.groupby("session_label")["abs_r_pips"].mean()
rank_xtab = m1_a.groupby("session_label_xtab")["abs_r_pips"].mean()
order_dst = list(rank_dst.sort_values(ascending=False).index)
order_xtab = list(rank_xtab.sort_values(ascending=False).index)
hours_m3 = m1_a["utc"].dt.hour
in_xtab = m1_a.loc[hours_m3.isin(top6), "session_label_xtab"]
share_off_xtab = float((in_xtab == "Off").mean())
m3_setuju = (order_dst == order_xtab) and (share_off_top6 == share_off_xtab == 0.0)
print("M3 ranking DST-aware :", {k: round(float(v), 4) for k, v in rank_dst.items()})
print("M3 ranking cross-tab :", {k: round(float(v), 4) for k, v in rank_xtab.items()})
print(f"M3 urutan DST={order_dst} vs xtab={order_xtab}; share_Off xtab={share_off_xtab:.4f}")
print(f"M3 SENSITIVITAS: {'SETUJU (DST-aware tetap primer)' if m3_setuju else 'BERBEDA - lihat selisih di atas'}")
assert order_dst == ["London", "Tokyo", "Sydney", "NewYork"], (
    f"urutan DST-aware berubah: {order_dst}"
)
assert order_xtab == ["London", "Tokyo", "Sydney", "NewYork"], (
    f"urutan cross-tab berubah: {order_xtab}"
)
assert share_off_xtab == 0.0, "share Off xtab harus 0 seperti primer"''',
)

code(
    '''"""H5 - Level-reaction syarat biaya rendah (dari Q6 + T-01 + M4 kanon p95).

KOREKSI B4-04/B4-05: rasio memakai spread_p95 per-bar (M4 kanon), bukan proksi
mean-D1; flag kosong lama ([]) adalah artefak proksi, kini NewYork+Sydney ter-flag.
KOREKSI B4-09: placebo ditampilkan dua varian terpisah (bukan rentang rakitan).
KOREKSI B4-10: contoh sesi ber-rasio tinggi = London (tertinggi), bukan Tokyo."""
zero_pct_h5 = float((m1["r"] == 0).mean() * 100)
london_ratio = float(ses.loc["London", "rasio_vol_over_spread"])
rasio_p95 = {s: round(float(ses.loc[s, "rasio_vol_over_spread"]), 4) for s in ses.index}
h5 = {
    "klaim": (
        "Reaksi level (round-number/prior-day H/L) hanya dapat dieksploitasi bila "
        "biaya rendah relatif pergerakan. Dengan rasio kanon M4 (mean|r|/spread-p95 "
        f"per-bar): London {rasio_p95['London']:.2f} & Tokyo {rasio_p95['Tokyo']:.2f} "
        f"di atas biaya, NewYork {rasio_p95['NewYork']:.2f} & Sydney "
        f"{rasio_p95['Sydney']:.2f} ter-flag biaya-mendominasi. "
        "Q6 menemukan hit-rate TIDAK melampaui placebo secara agregat; hipotesis "
        "ini mempersempit: pada sub-populasi volatilitas tinggi reaksi level "
        "mungkin melampaui placebo."
    ),
    "metrik_pendukung": {
        "q6_hit_rate_real": "0,469-0,490 (nb04)",
        "q6_hit_rate_placebo": (
            "placebo_acak 0,4989 [0,4831-0,5144]; placebo_hl 0,4890-0,4922 "
            "(KOREKSI Q-TR-03/B8-04: sebelumnya 0,4890-0,5050 - 0,5050 milik "
            "placebo_acak; 0,4890 = titik estimasi hl_utc, bukan batas bawah CI "
            "[0,4748/0,4798]; titik estimasi 0,4890 tumpang tindih batas atas real 0,490)"
        ),
        "rasio_vol_over_spread_p95": rasio_p95,
        "rasio_vol_over_spread_London": round(london_ratio, 4),
        "flag_biaya_mendominasi": flagged,
        "t01_massa_nol_pct": round(zero_pct_h5, 3),
    },
    "uji_lapisan3": (
        "Ulangi protokol placebo nb04 PERSIS, dikondisikan pada |ATR| hari tinggi "
        "(kuartil atas) dan sesi vol/spread tinggi; hit-rate real vs placebo dengan "
        "CI bootstrap day-cluster (seed 20261006)."
    ),
    "ambang_falsifikasi": (
        "GUGUR bila pada setiap sub-populasi hit-rate real tetap ≤ placebo (beda CI95 "
        "memuat 0) - maka level dinyatakan tak dieksploitasi dan hipotesis disimpan "
        "sebagai temuan negatif."
    ),
}
assert 0 < zero_pct_h5 < 10, "massa nol di luar band wajar"
assert london_ratio > 0, "rasio London harus positif"
print("H5:", h5["klaim"])
print("   pendukung:", h5["metrik_pendukung"])''',
)

md(
    """## 3. T-01 "massa nol" — ratifikasi via laporan final (backlog Klenz)

Temuan nb01: ≈5,83% bar M1 ber-return **persis 0**. Dihitung ulang di sini sebagai
bagian laporan final sesuai backlog (ratifikasi dilaporkan di `report.md`)."""
)

code(
    '''"""T-01: hitung ulang massa nol M1 (seluruh data dan per strata)."""
zero_all = int((m1["r"] == 0).sum())
zero_pct = zero_all / len(m1) * 100
zero_a = int((m1.loc[a_mask, "r"] == 0).sum())
zero_b = int((m1.loc[b_mask, "r"] == 0).sum())
print(f"T-01 massa nol M1: {zero_all:,}/{len(m1):,} bar = {zero_pct:.2f}%")
print(
    f"  stratum A: {zero_a:,} ({zero_a / BAR_COUNTS['A'] * 100:.2f}%) | "
    f"stratum B: {zero_b:,} ({zero_b / BAR_COUNTS['B'] * 100:.2f}%)"
)
assert 5.0 < zero_pct < 6.5, "massa nol menyimpang dari temuan nb01 (5,83%)"
print("RATIFIKASI T-01: temuan nb01 terkonfirmasi ulang dari parquet; dicatat di report.md.")''',
)

md(
    """## 4. Figures FIG-04..07 + verifikasi registry (skema D9)

Skema terkunci: FIG-01..03 = nb01 (M1/M5/M15 QQ); FIG-04+ sekuensial dari nb05.
Notebook ini WAJIB memverifikasi registry direktori figures."""
)

code(
    '''"""Empat figure satu-pesan: FIG-04..FIG-07 (savefig dpi=120, pola nb01)."""
import matplotlib  # noqa: E402  (backend harus diset sebelum pyplot; pola nb01)

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
figures = []
a_daily = daily[daily["strata"] == "A"]
b_daily = daily[daily["strata"] == "B"]

# FIG-04: distribusi range/ATR A vs B (level-hari).
fig, axis = plt.subplots(figsize=(7, 4.5))
axis.hist(
    a_daily["range_atr"], bins=40, alpha=0.55,
    label=f"stratum A (n={len(a_daily)})", density=True,
)
axis.hist(
    b_daily["range_atr"].dropna(), bins=40, alpha=0.55,
    label=f"stratum B valid (n={int(b_daily['range_atr'].notna().sum())})", density=True,
)
axis.set_title("Q7: range/ATR harian - strata A vs B (KS/MW + Cliff di tabel)")
axis.set_xlabel("(high-low)/ATR14")
axis.set_ylabel("densitas")
axis.legend()
fig.tight_layout()
path = FIGURE_DIR / "FIG-04.png"
fig.savefig(path, dpi=120)
plt.close(fig)
figures.append(path)

# FIG-05: realized vol harian A vs B (log10).
fig, axis = plt.subplots(figsize=(7, 4.5))
axis.hist(np.log10(a_daily["rv_day"]), bins=40, alpha=0.55, label="stratum A", density=True)
axis.hist(np.log10(b_daily["rv_day"]), bins=40, alpha=0.55, label="stratum B", density=True)
axis.set_title("Q7: realized vol harian Σr² (log10) - strata A vs B")
axis.set_xlabel("log10(Σr² M1 intraday)")
axis.set_ylabel("densitas")
axis.legend()
fig.tight_layout()
path = FIGURE_DIR / "FIG-05.png"
fig.savefig(path, dpi=120)
plt.close(fig)
figures.append(path)

# FIG-06: tipologi per strata (proporsi tipe hari, hari valid).
share = crosstab_pct.loc[["A", "B", "C"]]
fig, axis = plt.subplots(figsize=(7, 4.5))
bottom = np.zeros(len(share))
for tipe in TIPO_ORDER:
    axis.bar(share.index, share[tipe], bottom=bottom, label=tipe)
    bottom += share[tipe].to_numpy()
axis.set_title("Q7: proporsi tipe hari per strata (n-A=825, n-B=116, n-C=19)")
axis.set_ylabel("% hari")
axis.legend()
fig.tight_layout()
path = FIGURE_DIR / "FIG-06.png"
fig.savefig(path, dpi=120)
plt.close(fig)
figures.append(path)

# FIG-07: profil mean|r| per jam UTC (basis H4/M2).
fig, axis = plt.subplots(figsize=(8, 4.5))
axis.bar(vol_hour.index, vol_hour.to_numpy(), color="steelblue")
axis.set_title("Q7/M2: mean |r| (pip) per jam UTC - stratum A M1")
axis.set_xlabel("jam UTC")
axis.set_ylabel("mean |r| (pip/bar)")
fig.tight_layout()
path = FIGURE_DIR / "FIG-07.png"
fig.savefig(path, dpi=120)
plt.close(fig)
figures.append(path)

for path in figures:
    assert path.is_file() and path.stat().st_size > 5_000, f"figure rusak/hilang: {path}"
    print("tersimpan:", path.relative_to(PROJECT_ROOT))''',
)

code(
    '''"""Verifikasi registry figures (skema D9): tepat FIG-01..FIG-07."""
registry = sorted(p.name for p in FIGURE_DIR.glob("*.png"))
expected = [f"FIG-{i:02d}.png" for i in range(1, 8)]
print("registry figures:", registry)
assert registry == expected, f"registry figures melanggar skema D9: {registry} != {expected}"
print("PASS: registry figures tepat FIG-01..FIG-07 (D9 terpenuhi, nb05 = FIG-04..07).")''',
)

md(
    """## 5. Keterbatasan & catatan Lampiran A1

- **R1:** label hari-UTC membawa offset struktural −1; tidak dipakai sebagai primer di
  notebook ini dan tidak digeser agar "sepakat".
- **R2:** perbandingan hari-broker vs hari-UTC tidak diulang di Q7 (tidak relevan untuk
  tipologi); yang dikunci adalah kalender tunggal bucket D1 == hari broker (di-assert).
- **R3:** seluruh uji A-vs-B level-hari terkunci tanggal-broker.
- **Keterbatasan statistik:** hari-hari saling bergantung (volatility clustering) — uji
  level-hari mengurangi (tidak menghapus) dependensi; effect-size + CI bootstrap
  dilaporkan. CI utama tabel = bootstrap IID per hari (kolom `ci95_beda_iid`);
  block bootstrap sirkular 20-hari (≈1 bulan dagang, menutup musiman mingguan)
  hanya bila hasil marginal, dan me-resample KEDUA sisi A dan B (KOREKSI L3-02).
- **Tipologi ex-post (L3-01, opsi b):** ambang = median SELURUH 825 hari A
  (full-sample) → label hari-t memakai info hari setelah t: deskriptif ex-post,
  TIDAK real-time-safe. Walk-forward per tahun ditolak untuk EDA (mengubah angka =
  keputusan arsitektur); identifikasi real-time milik uji Lapisan 3 (H1).
- **Daya uji B:** n-B = 130 hari (116 valid untuk metrik berbasis ATR); "tidak
  terdeteksi" ≠ "tidak ada perbedaan".
- **Warmup ATR14:** 14 hari pertama sampel (stratum B) tanpa range_atr → dikeluarkan
  dari tipologi, jumlah drop dilaporkan (nol imputasi).
- **Proksi spread sesi:** kolom spread per bar M1 tidak ada di skema nb03; M4 memakai
  mean D1 harian → dilabel ASUMSI-PROKSI, bukan pengukuran final.
- **Kalender libur** di luar scope → hari bervolume rendah terlihat di data, tidak
  teratribusi. **Sumber sekunder** S5/S6 tetap berlabel sekunder.
- **Tidak ada P&L / pemilihan metode.** Hipotesis H1-H5 = kandidat untuk Lapisan 3.

**STOP.** Laporan akhir rantai: `reports/eda/2026-10-06/report.md` + laporan mini
tahap 11-14 + review user + audit Klenz sebelum penguncian hipotesis."""
)

code(
    '''"""Penutup: penanda semua assertion lulus."""
print("=== nb05 SELESAI: SEMUA ASSERTION PASS (Q7 + sintesis H1-H5 + T-01 + figures) ===")''',
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
    # Baca byte -> CRLF->LF -> tulis dengan newline="\n"; idempoten pada file LF.
    _nb_bytes = NB_PATH.read_bytes().replace(b"\r\n", b"\n")
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(_nb_bytes.decode("utf-8"))

    print(f"nbconvert exit={result.returncode}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    build()
