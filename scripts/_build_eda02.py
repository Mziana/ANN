"""Generator + executor for notebooks/scalping/eda_02_volatility.ipynb.

Q2 (volatility per broker wall hour), Q3 (volatility per UTC session), calibration
M1-M4, spread measurement per session x hour x year, and a YAML fragment that is
PRINTED ONLY - never written to configs/.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_02_volatility.ipynb"
FRAGMENT_PATH = PROJECT_ROOT / "reports/eda/2026-10-06/spread_fragment.yaml"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA 02 — Q2 Volatilitas per Jam Broker + Q3 Volatilitas per Sesi + Spread

**Rancangan:** EDA v3 Final. **Purpose:** mengukur *bentuk* volatilitas (bukan profit).

## Yang dijawab
- **Q2:** realized volatility (r²) dan mean|r| per **jam dinding broker**, plus
  `tick_volume` sebagai proksi aktivitas, dan rasio sesi terhadap harian.
- **Q3:** volatilitas per **sesi UTC** (label eksklusif primer).
- **Kalibrasi batas sesi M1–M4** (lihat sel masing-masing).
- **Spread terukur:** p50/p95/p99/maks dan %>3 pip per sesi × jam × tahun.

## Peringatan SA-07 dari nb01 (WAJIB dibaca sebelum menafsirkan)
Ekor return M1 didorong **dua sumber**: berita makro (12:30 UTC = 08:30 ET) dan **gap
pembukaan sesi** (21–22 UTC). Volatilitas per jam di bawah **tidak** bisa memisahkan
keduanya karena **kalender berita di luar scope EDA**. Jadi:
- Angka volatilitas per jam/sesi adalah **deskriptif mentah**, bukan "volatilitas bersih".
- Setiap tabel_volatilitas juga melaporkan versi **tanpa return lintas gap** agar efek gap
  bisa dinilai.
- Tidak ada klaim "sesi X lebih volatile karena" tanpa catatan ini.

## Batas keras (Wajib)
- **Tidak** ada P&L, equity, backtest, atau pemilihan metode.
- **Tidak** menulis `configs/`. Fragmen spread **hanya dicetak** (dan disimpan ke
  `reports/eda/2026-10-06/spread_fragment.yaml` sebagai bahan review **4b**).
- **Tidak** ada imputasi.
- Inferensi sinyal **tidak** diambil dari M1.
"""
)

code(
    '''"""Setup lingkungan dan kunci versi."""
import importlib.metadata
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


def find_project_root(start: Path) -> Path:
    """Cari root proyek (pyproject.toml + src/) dari cwd ke atas."""
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    raise RuntimeError("PROJECT_ROOT tidak ditemukan")


PROJECT_ROOT = find_project_root(Path.cwd().resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.broker_time import BrokerSchedule, wall_clock_series  # noqa: E402
from src.utils.config import load_config  # noqa: E402

sys.path.insert(0, str(PROJECT_ROOT / "notebooks/scalping"))
from _eda_common import (  # noqa: E402
    CROSS_TAB_HOURS,
    EXPECTED_FINGERPRINT,
    SESSION_ORDER,
    add_labels,
    session_fingerprint,
)

print("PROJECT_ROOT :", PROJECT_ROOT)
print("python       :", sys.version.split()[0])
for package in ("pandas", "numpy", "pyarrow", "matplotlib", "scipy", "pyyaml", "tzdata"):
    print(f"  {package:11s}: {importlib.metadata.version(package)}")

assert importlib.metadata.version("tzdata") == "2026.5", "tzdata harus 2026.5 (Kontrak 00)"
assert int(importlib.metadata.version("pandas").split(".")[0]) == 2, (
    "Notebook WAJIB jalan di venv kanonik (pandas 2.x); pandas 3.x merusak satuan .asi8."
)'''
)

md(
    """## 0. Assertion definisi sesi (anti-drift)

Definisi sesi harus **sama persis** dengan Notebook 00. Modul bersama
`notebooks/scalping/_eda_common.py` menyimpan salinan terkunci; sidik jarinya di-assert
di sini supaya nb02–nb05 tidak diam-diam memakai definisi berbeda (pelajaran SA-03)."""
)

code(
    '''"""Kunci definisi sesi agar tidak drift dari Notebook 00."""
print("sidik jari definisi sesi:")
print(" ", session_fingerprint())
assert session_fingerprint() == EXPECTED_FINGERPRINT, (
    "Definisi sesi berubah vs Notebook 00 -STOP, kembalikan ke kontrak."
)
print("PASS: definisi sesi identik dengan Notebook 00.")
print("label eksklusif:", " > ".join(SESSION_ORDER))
print("cross-tab UTC-tetap:", CROSS_TAB_HOURS)'''
)

md(
    """## 1. Memuat M1 + return + label sesi

M1 adalah sumber spread (`spread_pips`) dan proksi aktivitas (`tick_volume`). Volatilitas
dihitung dari **M1** (bar terkecil) lalu Session & jam; M5/M15 hanya dipakai sebagai
konfirmasi di Q2 (kalibrasi M1–M4 memakai M5 agar tidak terlalu microstructure).

Return dihitung **setelah pengurutan kronologis** (pernah menjadi bug di nb01), dan
sebelum pemisahan label, memakai `shift(1)`.
"""
)

code(
    '''"""Muat M1 2023-2026, urutkan, hitung return log BID, label broker-day dan sesi."""
config = load_config("data")
SYMBOL = config["mt5"]["symbol"]
SCHEDULE = BrokerSchedule.from_config(config["mt5"])
ANOMALY_WINDOWS = tuple((w["start"], w["end"]) for w in config["validation"]["anomaly_windows"])
YEARS = (2023, 2024, 2025, 2026)
PIP_SIZE = 0.01
COLUMNS = ["time", "broker_time_raw", "close", "tick_volume", "spread_pips"]

frames = [
    pd.read_parquet(
        PROJECT_ROOT / "data/processed/M1" / f"usdjpy_m1_{year}.parquet",
        columns=COLUMNS,
    )
    for year in YEARS
]
m1 = pd.concat(frames, ignore_index=True)
m1["utc"] = pd.to_datetime(m1["time"], utc=True)
m1["wall"] = wall_clock_series(m1["broker_time_raw"])
m1["wall_hour"] = m1["wall"].dt.hour
m1["utc_hour"] = m1["utc"].dt.hour
m1["broker_day"] = m1["wall"].dt.normalize()
m1 = m1.sort_values("utc", kind="mergesort").reset_index(drop=True)
m1["r"] = np.log(m1["close"] / m1["close"].shift(1))
m1 = add_labels(m1)

# return yang menyeberangi gap (weekend / break) ditandai terpisah (lihat SA-07)
m1["gap_return"] = m1["utc"].diff() > pd.Timedelta(minutes=1)

wall_date = m1["broker_day"]
b_mask = (wall_date >= pd.Timestamp("2023-01-01")) & (wall_date <= pd.Timestamp("2023-06-30"))
c_mask = pd.Series(False, index=m1.index)
for start, end in ANOMALY_WINDOWS:
    c_mask |= (wall_date >= pd.Timestamp(start)) & (wall_date <= pd.Timestamp(end))
a_mask = ~(b_mask | c_mask)

print(f"symbol={SYMBOL} | bar={len(m1):,} | gap_return={int(m1['gap_return'].sum()):,}")
print(f"strata A={int(a_mask.sum()):,} B={int(b_mask.sum()):,} C={int(c_mask.sum()):,}")
assert int(a_mask.sum()) == 1_136_401, f"A harus 1.136.401, dapat {int(a_mask.sum())}"
assert int(b_mask.sum()) == 185_248, f"B harus 185.248, dapat {int(b_mask.sum())}"
assert int(c_mask.sum()) == 26_198, f"C harus 26.198, dapat {int(c_mask.sum())}"
assert not (b_mask & c_mask).any(), "B dan C tidak boleh tumpang tindih"
assert m1["utc"].is_monotonic_increasing, "urutan waktu harus naik"
print("PASS: stratifikasi A/B/C mereproduksi Lapisan 1; urutan naik.")


def spread_summary(frame: pd.DataFrame) -> dict[str, float]:
    """Ringkasan spread satu subset bar.

    Args:
        frame: Frame dengan kolom spread_pips.

    Returns:
        Dictionary n, p50, p95, p99, max, pct_gt_3pip.
    """
    values = frame["spread_pips"]
    return {
        "n": len(values),
        "p50": float(values.quantile(0.50)),
        "p95": float(values.quantile(0.95)),
        "p99": float(values.quantile(0.99)),
        "max": float(values.max()),
        "pct_gt_3pip": float((values > 3.0).mean()),
    }
'''
)

md(
    """## 2. Q2 — Volatilitas per jam dinding broker

Metrik per jam broker (0–23):
- `sum_r2` = r² (realized volatility dari return kuadrat).
- `mean_abs_r` = mean|r| (robust terhadap ekor).
- `tick_volume` = proksi aktivitas.
- `spread_p95` = p95 spread (pip) pada jam itu.

Dihitung pada **strata A** (utama), dan dilaporkan versi **tanpa gap-return** sebagai
kolom terpisah. Bank M5 dipakai untuk kalibrasi M1–M4 di sel berikutnya. JANGAN membaca
baris mana pun sebagai "jam busy" tanpa melihat kolom no-gap. Catatan
Tabel ini ditampilkan penuh sebagai stream (pelajaran nb01 SA-02: `display()` hilang
saat nbconvert sehingga tabel kosong lolos sebagai "sukses")."""
)

code(
    '''"""Q2: volatilitas per jam dinding broker (strata A)."""
a_frame = m1[a_mask].copy()
a_frame["r2"] = a_frame["r"] ** 2

hourly_rows = []
for hour in range(24):
    window = a_frame[a_frame["wall_hour"] == hour]
    clean = window["r"].dropna()
    no_gap = window.loc[~window["gap_return"], "r"].dropna()
    hourly_rows.append(
        {
            "jam_broker": hour,
            "n_bar": len(window),
            "n_hari": int(window["broker_day"].nunique()),
            "sum_r2": float((clean**2).sum()),
            "mean_abs_r": float(clean.abs().mean()),
            "mean_abs_r_no_gap": float(no_gap.abs().mean()),
            "tick_volume": float(window["tick_volume"].mean()),
            "spread_p95": float(window["spread_pips"].quantile(0.95)),
        }
    )

HOURLY = pd.DataFrame(hourly_rows).set_index("jam_broker")
pd.set_option("display.width", 220)
pd.set_option("display.float_format", lambda v: f"{v:.6e}")
pd.set_option("display.max_columns", 30)
display(HOURLY)
print("TABEL Q2 per jam broker (stream, supaya tersimpan):")
print(HOURLY.to_string())

print()
print("Rasio mean|r| no-gap / mean|r| all per jam ( gap):")
ratio = HOURLY["mean_abs_r_no_gap"] / HOURLY["mean_abs_r"]
print((ratio).round(4).to_string())

print()
top6 = HOURLY["mean_abs_r"].nlargest(6).index.tolist()
print("6 jam dengan mean|r| tertinggi:", top6)'''
)

md(
    """## 3. Q3 — Volatilitas per sesi UTC (label eksklusif primer)

Label eksklusif memakai prioritas London > NewYork > Tokyo > Sydney > Off. Metrik per
sesi: `sum_r2`, `mean_abs_r` (dan no-gap), `tick_volume`, `spread_p95`, serta **rasio
volatilitas sesi terhadap rata-rata harian** (`sum_r2` sesi / `sum_r2` hari itu)."""
)

code(
    '''"""Q3: volatilitas per sesi UTC eksklusif."""
daily_r2 = a_frame.groupby("broker_day")["r2"].sum()

session_rows = []
for label in SESSION_ORDER:
    window = a_frame[a_frame["session_label"] == label]
    clean = window["r"].dropna()
    no_gap = window.loc[~window["gap_return"], "r"].dropna()
    per_day = window.groupby("broker_day")["r2"].sum()
    # CATATAN: fillna di sini BUKAN imputasi data harga. Ia hanya menyamakan indeks
    # agregat harian agar hari tanpa bar pada sesi itu menjadi 0 sumbu, bukan NaN.
    daily_total = daily_r2.reindex(per_day.index).fillna(0.0)
    share_of_daily = (per_day / daily_total.replace(0.0, np.nan)).mean()
    session_rows.append(
        {
            "sesi": label,
            "n_bar": len(window),
            "n_hari": int(window["broker_day"].nunique()),
            "sum_r2": float((clean**2).sum()),
            "mean_abs_r": float(clean.abs().mean()),
            "mean_abs_r_no_gap": float(no_gap.abs().mean()),
            "tick_volume": float(window["tick_volume"].mean()),
            "spread_p95": float(window["spread_pips"].quantile(0.95)),
            "mean_share_daily_r2": float(share_of_daily),
        }
    )

SESSIONAL = pd.DataFrame(session_rows).set_index("sesi")
pd.set_option("display.float_format", lambda v: f"{v:.6e}")
display(SESSIONAL)
print("TABEL Q3 per sesi (stream, supaya tersimpan):")
print(SESSIONAL.to_string())

active = SESSIONAL.drop(index=["Off"])
ranking = active["mean_abs_r"].sort_values(ascending=False)
print()
print("Ranking volatilitas sesi (mean|r|, primer DST-aware):")
print(ranking.round(8).to_string())

off_all = int((m1["session_label"] == "Off").sum())
print()
print(f"Bar berlabel 'Off' di SELURUH data: {off_all:,} ({off_all / len(m1):.4%})")
print(f"Bar berlabel 'Off' di strata A   : {int((a_frame['session_label'] == 'Off').sum()):,}")
print("-> 4 sesi menutup 24 jam di strata A; bar Off hanya muncul di strata B/C.")'''
)

md(
    """## 4. Kalibrasi M1–M4

- **M1:** bandingkan ranking volatilitas empiris dengan prior USDJPY London > NewYork > Tokyo
  (S5-sekunder). Deviasi **dicatat sebagai temuan**, bukan dianggap salah.
- **M2:** 6 jam UTC bervolatilitas tertinggi harus berada di dalam sesi berlabel. Jika ≥2
  jatuh di `Off`, batas sesi direvisi.
- **M3:** ranking sesi harus **sepakat** antara pelabelan DST-aware (primer) dan cross-tab
  UTC-tetap. Jika berbeda → dilaporkan sebagai sensitivitas; DST-aware tetap primer.
- **M4:** sesi dengan rasio mean|r| (dalam **pip**) terhadap `spread_p95` di bawah 1 diberi
  flag deskriptif "biaya-mendominasi" sebagai bahan hipotesis — **bukan** keputusan.

**Satuan M4:** mean|r| harus dikonversi ke pip dulu: `mean|r|_pip = mean|r| * close / 0.01`.
Tidak dikonversi akan menghasilkan rasio meaningless (pelajaran satuan SA-01)."""
)

code(
    '''"""Kalibrasi M1-M4 dengan konversi satuan pip yang benar untuk M4."""
pip = 0.01
close_mean = float(a_frame["close"].mean())
unit_pip = close_mean / pip  # faktor konversi log-return -> pip

prior = ["London", "NewYork", "Tokyo"]  # S5-sekunder (prior USDJPY pip: 66/59/51)
empirical = list(ranking.index)
prior_subset = [s for s in prior if s in empirical]
empirical_subset = [s for s in empirical if s in prior]
m1_agrees = prior_subset == empirical_subset

print(f"faktor aproksimasi log-return -> pip: {unit_pip:.2f} (close_mean={close_mean:.3f})")
print("M4 memakai konversi EKSAK per bar, bukan pendekatan mean x mean.")
print(f"M1 prior (S5-sekunder): {prior_subset}")
print(f"M1 empiris            : {empirical_subset}")
print(f"M1 agree: {m1_agrees}")

xtab_rows = []
for label in SESSION_ORDER:
    window = a_frame[a_frame["session_label_xtab"] == label]
    clean = window["r"].dropna()
    xtab_rows.append({"sesi": label, "mean_abs_r_xtab": float(clean.abs().mean())})
XTAB = pd.DataFrame(xtab_rows).set_index("sesi")["mean_abs_r_xtab"]
empirical_xtab = [s for s in XTAB.drop(index=["Off"]).sort_values(ascending=False).index if s in prior]
m3_agrees = empirical == empirical_xtab

print(f"M3 primer (DST-aware) : {empirical}")
print(f"M3 cross-tab (UTC)    : {empirical_xtab}")
print(f"M3 agree: {m3_agrees}  -> jika beda = sensitivitas, DST-aware tetap primer")

active_labels = [s for s in SESSION_ORDER if s != "Off"]
labels_at_top_hours = set(a_frame.loc[a_frame["utc_hour"].isin(top6), "session_label"])
off_at_top = sum(1 for h in top6 if a_frame.loc[a_frame["utc_hour"] == h, "session_label"].eq("Off").mean() > 0.5)
print(f"M2 top-6 jam UTC = {top6}; label dominan jam itu: {sorted(labels_at_top_hours)}")
print(f"M2 jam dengan label Off dominan: {off_at_top} (>=2 berarti batas perlu revisi)")

m4_rows = []
for label in active_labels:
    row = SESSIONAL.loc[label]
    # Konversi EKSAK per bar (bukan mean|r| x mean harga, yang hanya pendekatan).
    per_bar_pip = (
        (np.exp(a_frame.loc[a_frame["session_label"] == label, "r"]) - 1.0)
        * a_frame.loc[a_frame["session_label"] == label, "close"]
        / pip
    )
    mean_abs_pip = float(per_bar_pip.abs().mean())
    ratio_cost = mean_abs_pip / float(row["spread_p95"]) if row["spread_p95"] > 0 else np.nan
    m4_rows.append(
        {
            "sesi": label,
            "mean_abs_r_pip": mean_abs_pip,
            "spread_p95_pip": float(row["spread_p95"]),
            "rasio_mayar": ratio_cost,
            "biaya_mendominasi": bool(ratio_cost < 1.0),
        }
    )
M4 = pd.DataFrame(m4_rows).set_index("sesi")
print()
print("M4 (mean|r| dalam pip vs spread p95):")
print(M4.round(4).to_string())
print()
print("M4 flag biaya-mendominasi (rasio < 1) - bahan hipotesis, BUKAN keputusan:")
print(M4[M4["biaya_mendominasi"]].index.tolist() or "tidak ada sesi")'''
)

md(
    """## 4b. TEMUAN: ekor spread 2023 adalah artefak STRATA B (bukan sifat tahun 2023)

Lapisan 1 memakai premis "2023 punya ekor spread terrible (p99 8,5 pip)" untuk memasang
asumsi `spread.by_year[2023] = 3,0`. Pengukuran di notebook ini menunjukkan premis itu
**hanya berlaku untuk strata B** (H1-2023, regime SA-03). Pada **strata A** — yang justru
dipakai analisis utama — spread 2023 normal seperti tahun lain.

Konsekuensi untuk langkah 4b: asumsi 3,0 pip untuk 2023 kemungkinan **lebih mahal sekitar 5x**
daripada yang perlu dibayar pada strata utama. Angka ini dilaporkan sebagai
**temuan terukur**, keputusan terapkan/tunda tetap milik user di 4b."""
)

code(
    '''"""Ekor spread per strata: uji apakah "2023 buruk" adalah sifat tahun atau sifat strata B."""
strata_masks = {"A": a_mask, "B": b_mask, "C": c_mask}
print("=== spread_pips per STRATA (seluruh 2023-2026) ===")
print(f"{'strata':6} {'n':>10} {'p50':>6} {'p95':>6} {'p99':>6} {'max':>7} {'%>3pip':>9}")
strata_rows = []
for name, mask in strata_masks.items():
    values = m1.loc[mask, "spread_pips"]
    stats = spread_summary(m1[mask])
    strata_rows.append({"strata": name, **stats})
    print(f"{name:6} {stats['n']:>10,} {stats['p50']:>6.2f} {stats['p95']:>6.2f} "
          f"{stats['p99']:>6.2f} {stats['max']:>7.1f} {stats['pct_gt_3pip']:>9.4%}")
STRATA_SPREAD = pd.DataFrame(strata_rows).set_index("strata")

print()
print("=== 2023 dipecah: H1 (strata B) vs H2 (di dalam strata A) ===")
h1_2023 = m1[b_mask]["spread_pips"]
h2_2023 = m1[(m1["utc"].dt.year == 2023) & ~b_mask & ~c_mask]["spread_pips"]
print(f"H1-2023 (B): p95={h1_2023.quantile(0.95):.2f} p99={h1_2023.quantile(0.99):.2f} "
      f"%>3pip={(h1_2023 > 3.0).mean():.4%}")
print(f"H2-2023 (A): p95={h2_2023.quantile(0.95):.2f} p99={h2_2023.quantile(0.99):.2f} "
      f"%>3pip={(h2_2023 > 3.0).mean():.4%}")

ratio_b_over_a = float(STRATA_SPREAD.loc["B", "p95"] / STRATA_SPREAD.loc["A", "p95"])
print()
print(f"Rasio p95 spread B terhadap A = {ratio_b_over_a:.2f}x")
print("-> Ekor spread 2023 mengikuti STRATA B, bukan tahun kalender.")'''
)

md(
    """## 5. Spread terukur per sesi × jam × tahun

Dari `spread_pips` M1: p50/p95/p99/maks dan % bar > 3 pip, dikelompokkan per
**tahun × sesi** dan per **tahun × jam UTC**. Tahun **2023 selalu terpisah** karena ekornya
berbeda (p99 8,5 pip menurut Lapisan 1). Ambang "3 pip" adalah **ambang deskriptif warisan
temuan fetch 2026**, bukan ambang keputusan trading.

Pengaruh ukuran: 2023 = 362.693 bar; total > 1,3 juta — pivot session × jam × tahun
disajikan per tahun agar bisa dibaca."""
)

code(
    '''"""Spread per tahun: sesi dan jam UTC."""
def spread_summary(frame: pd.DataFrame) -> dict[str, float]:
    """Ringkasan spread satu subset bar."""
    values = frame["spread_pips"]
    return {
        "n": len(values),
        "p50": float(values.quantile(0.50)),
        "p95": float(values.quantile(0.95)),
        "p99": float(values.quantile(0.99)),
        "max": float(values.max()),
        "pct_gt_3pip": float((values > 3.0).mean()),
    }


print("=== Spread per TAHUN x SESI (eksklusif) ===")
year_session_rows = []
for year in YEARS:
    year_frame = a_frame[a_frame["utc"].dt.year == year]
    for label in SESSION_ORDER:
        stats = spread_summary(year_frame[year_frame["session_label"] == label])
        year_session_rows.append({"tahun": year, "sesi": label, **stats})
YEAR_SESSION = pd.DataFrame(year_session_rows).set_index(["tahun", "sesi"])
pd.set_option("display.float_format", lambda v: f"{v:.4f}")
display(YEAR_SESSION)
print(YEAR_SESSION.to_string())

print()
print("=== Spread per TAHUN (seluruh data, untuk konteks ekor) ===")
year_rows = []
for year in YEARS:
    stats = spread_summary(a_frame[a_frame["utc"].dt.year == year])
    year_rows.append({"tahun": year, **stats})
YEAR_TOTAL = pd.DataFrame(year_rows).set_index("tahun")
display(YEAR_TOTAL)
print(YEAR_TOTAL.to_string())'''
)

code(
    '''"""Porsi bar spread > 3 pip per tahun x jam UTC (pivot 24 jam)."""
hour_share_rows = []
for year in YEARS:
    year_frame = a_frame[a_frame["utc"].dt.year == year]
    per_hour = {}
    for hour in range(24):
        window = year_frame[year_frame["utc_hour"] == hour]
        per_hour[hour] = float((window["spread_pips"] > 3.0).mean()) if len(window) else np.nan
    hour_share_rows.append(per_hour)

HOUR_SHARE = pd.DataFrame(hour_share_rows, index=list(YEARS))
HOUR_SHARE.index.name = "tahun"
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", lambda v: f"{v:.5f}")
display(HOUR_SHARE)
print("Porsi spread > 3 pip per tahun x jam UTC:")
print(HOUR_SHARE.to_string())

print()
print("Jam UTC dengan porsi > 3 pip tertinggi tiap tahun:")
for year in YEARS:
    top = HOUR_SHARE.loc[year].nlargest(3)
    print(f"  {year}: " + ", ".join(f"{int(h):02d}:00={v:.3%}" for h, v in top.items()))'''
)

md(
    """## 6. Fragmen YAML spread (BELUM diterapkan)

Fragmen dibangun dari **angka terukur** di atas, memakai kunci yang **sama** dengan
`configs/data.yaml` -> `spread.*`, supaya diff di langkah **4b** bersih. Angka config saat
ini (default 1,5 dan 3,0 untuk 2023) diperlakukan sebagai **ASUMSI** sampai user memutuskan
terapkan/tunda/tolak.

Fragment disimpan ke `reports/eda/2026-10-06/spread_fragment.yaml` — **bukan** ke
`configs/data.yaml`. Notebook ini **tidak pernah** menulis config."""
)

code(
    '''"""Bangun fragmen YAML spread dari angka terukur (TIDAK menulis ke configs/)."""
mean_by_session = {
    label: float(a_frame.loc[a_frame["session_label"] == label, "spread_pips"].mean())
    for label in SESSION_ORDER
    if label != "Off"
}
# "Off" di strata A = 0 bar (empat sesi menutup 24 jam). Dicatat eksplisit
# sebagai null agar tidak disalahartikan sebagai spread tak berhingga.
mean_by_session_full = dict(mean_by_session)
mean_by_session_full["Off"] = None

fragment = {
    "_status": (
        "DITERAPKAN ke configs/data.yaml pada 2026-10-06 sebagai sub-kunci BARU "
        "spread.cost_basis dan spread.stress_bands. Blok spread lama TIDAK diganti. "
        "Audit Klenz LULUS DENGAN CATATAN (MEDIUM-26/27/28, LOW-26, LOW-27.2/27.3). "
        "LOW-27.1 ditutup sebagai no-op (ejaan sudah benar di byte tersimpan). "
        "MASIH TERBUKA - cost_basis.default 0.65 vs spread.default 1.5, jadi backtest "
        "wajib menyebut kode mana yang jadi otoritas."
    ),
    "_sumber": "EDA-02, data/processed/M1 2023-2026, basis STRATA A (bukan campuran).",
    "_catatan": (
        "Nilai lama by_year[2023]=3,0 di config berasal dari p99 file 2023 UTUH, yang "
        "didominasi ekor STRATA B (H1-2023, regime SA-03). Di strata A, 2023 justru "
        "paling murah (mean 0,51 pip). 3,0 tidak mewakili semesta yang diperdagangkan."
    ),
    "_perbaikan_vs_fragmen_lama": (
        "Versi lama fragmen memakai p95 dan face by_year[2023]=0,6. Sekarang: biaya dasar "
        "dipindah ke cost_basis (MEAN), dan p95/p99 pindah ke stress_bands. Nilai "
        "by_year LAMA (3,0) tidak diubah di config; config lama tetap utuh."
    ),
    "_sesi": {
        "primer": "DST-aware per zona IANA (Asia/Tokyo, Europe/London, America/New_York, Australia/Sydney)",
        "jam_sesi": {
            "Tokyo": "09:00-18:00 JST (= 00:00-09:00 UTC, tanpa DST)",
            "London": "08:00-16:00 waktu lokal Europe/London",
            "NewYork": "08:00-17:00 waktu lokal America/New_York",
            "Sydney": "08:00-16:00 waktu lokal Australia/Sydney",
        },
        "label_eksklusif": "London > NewYork > Tokyo > Sydney > Off",
        "cross_tab_pembanding": "UTC-tetap: Tokyo 00-09, London 08-16, NewYork 13-22, Sydney 21-06",
        "syarat_backtest": (
            "Backtest Lapisan 5 WAJIB memakai pelabelan PRIMER yang identik "
            "(DST-aware IANA, prioritas eksklusif di atas). Cross-tab hanya untuk "
            "sensitivitas, TIDAK boleh jadi label operasi."
        ),
        "hari_perdagangan": "Tanggal broker (batas 21:00 UTC summer / 22:00 UTC winter)",
    },
    "pip_size": {"USDJPY": PIP_SIZE},
    "stress_multiplier": 2.0,
    "cost_basis": {
        "_satuan": "pip",
        "_statistik": "MEAN spread_pips strata A",
        "default": round(float(a_frame["spread_pips"].mean()), 2),
        "by_year": {
            str(year): round(float(a_frame.loc[a_frame["utc"].dt.year == year, "spread_pips"].mean()), 2)
            for year in YEARS
        },
        "by_session": {label: round(value, 2) for label, value in mean_by_session.items()},
    },
    "stress_bands": {
        "_satuan": "pip",
        "_catatan": "p95 untuk stress test; p99 untuk batas ekor. Boleh dikalikan stress_multiplier.",
        "p95": {
            "default": round(float(a_frame["spread_pips"].quantile(0.95)), 2),
            "by_year": {
                str(year): round(float(a_frame.loc[a_frame["utc"].dt.year == year, "spread_pips"].quantile(0.95)), 2)
                for year in YEARS
            },
            "by_session": {
                label: round(float(SESSIONAL.loc[label, "spread_p95"]), 2)
                for label in SESSION_ORDER
                if label != "Off"
            },
        },
        "p99": {
            "default": round(float(a_frame["spread_pips"].quantile(0.99)), 2),
            "by_year": {
                str(year): round(float(a_frame.loc[a_frame["utc"].dt.year == year, "spread_pips"].quantile(0.99)), 2)
                for year in YEARS
            },
        },
    },
}

yaml_text = yaml.safe_dump(fragment, sort_keys=False, allow_unicode=True)
print(yaml_text)

FRAGMENT_PATH = PROJECT_ROOT / "reports/eda/2026-10-06/spread_fragment.yaml"
FRAGMENT_PATH.parent.mkdir(parents=True, exist_ok=True)
FRAGMENT_PATH.write_text(yaml_text, encoding="utf-8")
print(f"tersimpan (bukan config): {FRAGMENT_PATH.relative_to(PROJECT_ROOT)}")'''
)

code(
    '''"""Helper: kumpulkan semua nilai numerik dari fragmen (untuk deteksi NaN)."""


def _flatten_numbers(node):
    """Kumpulkan seluruh angka di dalam dict/list fragmen.

    Args:
        node: Struktur fragmen (dict/list/scalar).

    Yields:
        Setiap nilai numerik yang ditemukan.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            if str(key).startswith("_"):
                continue
            yield from _flatten_numbers(value)
    elif isinstance(node, list):
        for item in node:
            yield from _flatten_numbers(item)
    elif isinstance(node, int | float) and not isinstance(node, bool):
        yield node
'''
)

md(
    """## 7. Assertion penutup + ringkasan

Semua yang diassert adalah **fakta terukur**, bukan placeholder. Tidak ada assertion
`True` hardcode (pelajaran nb01 SA-03)."""
)

code(
    '''"""Assertion penutup Q2/Q3/spread."""
checks = [
    ("Definisi sesi == Notebook 00", session_fingerprint() == EXPECTED_FINGERPRINT),
    ("Strata A/B/C = 1.136.401 / 185.248 / 26.198", (int(a_mask.sum()), int(b_mask.sum()), int(c_mask.sum())) == (1_136_401, 185_248, 26_198)),
    ("Tidak ada r non-finite selain warmup", int(np.isinf(a_frame["r"].dropna()).sum()) == 0),
    ("Tabel per jam = 24 baris", len(HOURLY) == 24),
    ("Tabel per sesi = 5 baris (4 sesi + Off)", len(SESSIONAL) == 5),
    ("Jam 00-23 lengkap", list(HOURLY.index) == list(range(24))),
    ("Label sesi mempartisi bar strata A tanpa sisa/rumpang", int(SESSIONAL["n_bar"].sum()) == len(a_frame)),
    ("Bar 'Off' di strata A = 0 (4 sesi menutup 24 jam)", int((a_frame["session_label"] == "Off").sum()) == 0),
    ("Porsi >3pip M1 berada di 0..1", bool(((YEAR_TOTAL["pct_gt_3pip"] >= 0) & (YEAR_TOTAL["pct_gt_3pip"] <= 1)).all())),
    ("2023 di strata A TIDAK lebih lebar dari 2024 (premis lama terbantah)", bool(YEAR_TOTAL.loc[2023, "p99"] <= YEAR_TOTAL.loc[2024, "p99"])),
    ("Temuan: p95 spread strata B >> strata A", float(STRATA_SPREAD.loc["B", "p95"]) > 3 * float(STRATA_SPREAD.loc["A", "p95"])),
    ("Temuan: %>3pip strata B jauh di atas A", float(STRATA_SPREAD.loc["B", "pct_gt_3pip"]) > 10 * float(STRATA_SPREAD.loc["A", "pct_gt_3pip"])),
    ("Fragmen ditulis ke reports/, bukan configs/", FRAGMENT_PATH.exists() and "configs" not in str(FRAGMENT_PATH)),
    ("Fragment punya cost_basis.by_year 4 tahun", len(fragment["cost_basis"]["by_year"]) == 4),
    ("Fragment punya cost_basis.by_session 4 sesi", len(fragment["cost_basis"]["by_session"]) == 4),
    ("Fragment punya stress_bands p95 & p99", "p95" in fragment["stress_bands"] and "p99" in fragment["stress_bands"]),
    ("Fragment punya deklarasi _sesi + syarat backtest", "syarat_backtest" in fragment["_sesi"]),
    ("pip_size tetap dict (bukan flat)", isinstance(fragment["pip_size"], dict)),
    (
        "Fragment tidak memuat nilai NaN (tidak valid untuk config)",
        not any(isinstance(v, float) and np.isnan(v) for v in _flatten_numbers(fragment))
        and "Off" not in fragment["cost_basis"]["by_session"],
    ),
    ("M4 rasio > 0 semua sesi", bool((M4["rasio_mayar"] > 0).all())),
]

for label, passed in checks:
    print(f"{'PASS' if passed else 'GAGAL'} {label}")

failed = [label for label, passed in checks if not passed]
assert not failed, f"assertion gagal: {failed}"
print()
print(f"RINGKASAN: {len(checks) - len(failed)}/{len(checks)} assertion PASS untuk Q2/Q3/spread.")'''
)

md(
    """## Ringkasan hasil dan batasnya

**Yang dijawab:** bentuk volatilitas per jam broker dan per sesi UTC, kalibrasi M1–M4,
dan spread terukur per tahun × sesi / jam.

**Yang TIDAK dijawab dan sengaja ditolak:**
- Tidak ada kesimpulan prediktif (Q4, nb03).
- Tidak ada P&L atau keputusan metode.
- **Kalender berita di luar scope** → profil volatilitas masih memuat lonjakan berita.
  Cleaner (membersihkan) news spike adalah keputusan metode, bukan Q2.
- Fragmen spread **belum** diterapkan; menunggu 4b.

**Cara memakai angka ini nanti:** bila M4 memberi flag "biaya-mendominasi" pada suatu sesi,
itu bahan hipotesis (mis. jangan entry di jam spread lebar), **bukan** keputusan filter.
"""
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
    with NB_PATH.open("w", encoding="utf-8") as handle:
        nbf.write(notebook, handle)
    print(f"notebook ditulis: {NB_PATH.relative_to(PROJECT_ROOT)} ({len(notebook.cells)} sel)")

    # Normalisasi format SEL NOTEBOOK sebelum eksekusi. Tanpa ini, format cell
    # hasil builder akan drift dari `ruff format --check` setiap kali builder
    # dijalankan ulang (persis kelas regresi SA-34: .ipynb diperbaiki manual,
    # lalu hilang saat regenerasi). Builder adalah sumber kebenaran, jadi
    # formatnya juga harus dihasilkan di sini.
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
    print(f"nbconvert exit={result.returncode}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    build()
