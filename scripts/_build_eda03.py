"""Generator + executor for notebooks/scalping/eda_03_autocorr.ipynb.

Q4 (autocorrelation of returns beyond the sanity lag-1): variance-ratio style
lag sweep per timeframe, mean-reversion vs momentum split by session, and a
per-lag significance screen. Measurement only - no strategy, no P&L.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_03_autocorr.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA 03 — Q4 Autokorelasi return

**Rancangan:** EDA v3 Final. **Purpose:** menguji apakah return M1/M5/M15 menunjukkan
autokorelasi yang bisa dieksploitasi, dan apakah pola itu(mean-reversion atau momentum)
bergantung pada time-frame dan sesi.

## Yang dijawab
- **ACF lag 1-20** per time-frame (M1, M5, M15), stratum A.
- **Variance ratio** `Var(r_lag)/ (l * Var(r_1))` — <1 mean-reversion, >1 momentum.
- **Pemisahan mean-reversion vs momentum** berdasarkan tanda ACF lag-1.
- **Pemecahan per sesi UTC** (label eksklusif primer) dan per tahun.

## Peringatan SA-07 dari nb01 (WAJIB dibaca)
Ekor return M1 didorong berita makro (12:30 UTC) dan gap pembukaan sesi (21-22 UTC).
Autokorelasi yang diukur di sini **tercampur** dengan keduanya, dan kalender berita
adalah **di luar scope EDA**. Karena itu setiap tabel juga melaporkan versi
**tanpa return lintas gap**, dan tidak ada klaim "layak untuk strategi" di sini.

## Batas keras (Wajib)
- **Tidak** ada P&L, equity, backtest, atau pemilihan metode.
- **Tidak** menulis `configs/`.
- **Tidak** ada imputasi.
- Autokorelasi **bukan** bukti profitabilitas: biaya spread (lihat `cost_basis` di
  `configs/data.yaml`, MEAN ~0,65 pip) belum dikurangkan di setiap angka di sini.
"""
)

code(
    '''"""Setup lingkungan dan kunci versi."""
import importlib.metadata
import sys
from pathlib import Path

import numpy as np
import pandas as pd
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

Definisi sesi harus **sama persis** dengan Notebook 00. Sidik jari di-assert supaya nb03
tidak diam-diam memakai definisi berbeda (pelajaran SA-03)."""
)

code(
    '''"""Kunci definisi sesi agar tidak drift dari Notebook 00."""
print("sidik jari definisi sesi:")
print(" ", session_fingerprint())
assert session_fingerprint() == EXPECTED_FINGERPRINT, (
    "Definisi sesi berubah vs Notebook 00 - STOP, kembalikan ke kontrak."
)
print("PASS: definisi sesi identik dengan Notebook 00.")
print("label eksklusif:", " > ".join(SESSION_ORDER))
print("cross-tab UTC-tetap:", CROSS_TAB_HOURS)'''
)

md(
    """## 1. Memuat return M1, M5, M15 + stratifikasi

Return dihitung **setelah pengurutan kronologis** (pernah menjadi bug di nb01) dan
sebelum pemisahan label, memakai `shift(1)`. Bar yang menyeberangi gap (> 1 menit) ditandai
`gap_return` supaya bisa dihitung terpisah.

Stratifikasi A/B/C disalin dari nb01-nb02 agar angka bisa dibandingkan antar notebook:
- **B** = H1-2023 (regime SA-03, likuiditas rusak)
- **C** = dua jendela anomali digit jam
- **A** = sisanya (**semua analisis utama di notebook ini**)"""
)

code(
    '''"""Muat M1/M5/M15, urutkan, hitung return, label sesi, stratum A."""
config = load_config("data")
SYMBOL = config["mt5"]["symbol"]
SCHEDULE = BrokerSchedule.from_config(config["mt5"])
ANOMALY_WINDOWS = tuple((w["start"], w["end"]) for w in config["validation"]["anomaly_windows"])
YEARS = (2023, 2024, 2025, 2026)
PIP_SIZE = float(config["spread"]["pip_size"][SYMBOL])
TIMEFRAMES = ("M1", "M5", "M15")
COLUMNS = ["time", "broker_time_raw", "close", "tick_volume"]
TF_MINUTES = {"M1": 1, "M5": 5, "M15": 15}


def load_timeframe(tf: str) -> pd.DataFrame:
    """Muat satu time-frame 2023-2026, urutkan, hitung return log, tandai gap.

    Args:
        tf: Kode time-frame, mis. 'M1'.

    Returns:
        Frame dengan kolom utc, wall, broker_day, year, r, gap_return.
    """
    frames = [
        pd.read_parquet(
            PROJECT_ROOT / f"data/processed/{tf}" / f"usdjpy_{tf.lower()}_{year}.parquet",
            columns=COLUMNS,
        )
        for year in YEARS
    ]
    out = pd.concat(frames, ignore_index=True)
    out["utc"] = pd.to_datetime(out["time"], utc=True)
    out["wall"] = wall_clock_series(out["broker_time_raw"])
    out["broker_day"] = out["wall"].dt.normalize()
    out["year"] = out["wall"].dt.year
    out = out.sort_values("utc", kind="mergesort").reset_index(drop=True)
    out["r"] = np.log(out["close"] / out["close"].shift(1))
    # Ambang gap harus ikut SKALA time-frame: M1 = 1 menit, M5 = 5 menit,
    # M15 = 15 menit. Kalau dibiarkan 1 menit, SETIAP bar M5/M15 ditandai gap
    # dan kolom no-gap jadi kosong (ditemukan saat eksekusi pertama nb03).
    out["gap_return"] = out["utc"].diff() > pd.Timedelta(minutes=TF_MINUTES[tf])
    return out


DATA = {tf: load_timeframe(tf) for tf in TIMEFRAMES}

# Stratum B = H1-2023 (broker-day), stratum C = jendela anomali digit jam.
base = DATA["M1"]
wall_date = base["broker_day"]
b_mask = (wall_date >= pd.Timestamp("2023-01-01")) & (wall_date <= pd.Timestamp("2023-06-30"))
c_mask = pd.Series(False, index=base.index)
for start, end in ANOMALY_WINDOWS:
    c_mask |= (wall_date >= pd.Timestamp(start)) & (wall_date <= pd.Timestamp(end))
a_mask = ~(b_mask | c_mask)

# Subset A per time-frame, dengan label sesi.
STRATA_A: dict[str, pd.DataFrame] = {}
for tf, frame in DATA.items():
    keep = frame["broker_day"].isin(wall_date[a_mask].unique())
    subset = add_labels(frame.loc[keep].copy())
    STRATA_A[tf] = subset

for tf, subset in STRATA_A.items():
    assert subset["utc"].is_monotonic_increasing, f"{tf}: urutan waktu harus naik"
    assert int(subset["gap_return"].sum()) > 0, f"{tf}: harus ada return lintas gap"

print(f"symbol={SYMBOL} | pip_size={PIP_SIZE}")
print("strata A: " + ", ".join(f"{tf}={len(STRATA_A[tf]):,}" for tf in TIMEFRAMES))
print("gap_return: " + ", ".join(f"{tf}={int(STRATA_A[tf]['gap_return'].sum()):,}" for tf in TIMEFRAMES))
assert not (b_mask & c_mask).any(), "B dan C tidak boleh tumpang tindih"
print("PASS: stratifikasi dan urutan waktu konsisten.")'''
)

md(
    """## 2. ACF lag 1-20 per time-frame

Autokorelasi sample (bukan teoritis) dihitung pada bar **berurutan waktu** di stratum A.
Dua versi dilaporkan berdampingan:

- **all** — semua return (termasuk yang menyeberangi gap)
- **no-gap** — hanya return yang tidak menyeberangi gap

Kolom `p_value_no_gap` memakai uji dua-sisi dari scipy. Ljung-Box **tidak** dipakai sebagai
kesimpulan utama karena nilai reject-nya hampir pasti pada n > 1 juta; yang informatif di
sini adalah **besarannya** ACF, bukan signifikansinya."""
)

code(
    '''"""Hitung ACF lag 1-20 per time-frame, versi all dan no-gap."""
LAGS = list(range(1, 21))


def acf_table(frame: pd.DataFrame, lags: list[int], mask: pd.Series | None = None) -> pd.DataFrame:
    """ACF sample per lag beserta p-value dua-sisi.

    Args:
        frame: Frame dengan kolom r.
        lags: Daftar lag yang dihitung.
        mask: Masker bar boolean opsional (mis. tanpa gap).

    Returns:
        DataFrame terindeks lag dengan kolom acf_all, acf, p_value, n.
    """
    series = frame["r"] if mask is None else frame.loc[mask, "r"]
    values = series.to_numpy(dtype="float64")
    values = values[np.isfinite(values)]
    values = values - values.mean()
    denom = float(np.dot(values, values))
    rows = []
    for lag in lags:
        cov = float(np.dot(values[:-lag], values[lag:])) / denom
        test = stats.pearsonr(values[:-lag], values[lag:])
        rows.append({"lag": lag, "acf": cov, "p_value": float(test.pvalue), "n": len(values)})
    return pd.DataFrame(rows).set_index("lag")


ACF: dict[str, pd.DataFrame] = {}
for tf, subset in STRATA_A.items():
    no_gap_mask = ~subset["gap_return"]
    rows = []
    for lag in LAGS:
        full = acf_table(subset, [lag]).iloc[0]
        clean = acf_table(subset, [lag], no_gap_mask).iloc[0]
        rows.append(
            {
                "lag": lag,
                "acf_all": float(full["acf"]),
                "acf_no_gap": float(clean["acf"]),
                "p_value_no_gap": float(clean["p_value"]),
                "n_no_gap": int(clean["n"]),
            }
        )
    ACF[tf] = pd.DataFrame(rows).set_index("lag")

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
for tf in TIMEFRAMES:
    print(f"=== ACF {tf} (stratum A) ===")
    print(ACF[tf].to_string())
    print()'''
)

md(
    """## 3. Variance ratio per lag

`VR(l) = Var(r_lag) / (l * Var(r_1))`, dengan `r_lag` = **jumlah** `l` return satu-periode
yang bertumpang tindih (`r_t + r_{t-1} + ... + r_{t-l+1}`), mengikuti formulasi Lo-MacKinlay.

- **VR < 1** → return berlawanan arah dari lag sebelumnya (mean-reversion).
- **VR > 1** → searah (momentum / persistence).
- **VR = 1** → random walk.

Dua properti yang dipakai sebagai assertion definisional: `VR(1) = 1` secara eksak, dan
`VR(l) = 1` untuk semua `l` bila return iid. Dihitung pada seri return yang **tidak**
menyeberangi gap, supaya tidak tercampur lompatan harga saat pasar tutup."""
)

code(
    '''"""Variance ratio per lag per time-frame (no-gap)."""


def variance_ratio(series: pd.Series, lag: int) -> float:
    """Hitung VR(lag) dari satu seri return (formulasi Lo-MacKinlay).

    r_lag adalah JUMLAH lag return satu-periode yang bertumpang tindih
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


VR_ROWS = []
for tf, subset in STRATA_A.items():
    clean = subset.loc[~subset["gap_return"], "r"]
    for lag in LAGS:
        VR_ROWS.append({"timeframe": tf, "lag": lag, "vr_no_gap": variance_ratio(clean, lag)})

VR = pd.DataFrame(VR_ROWS).pivot(index="lag", columns="timeframe", values="vr_no_gap")
# .loc[:, ...] wajib: VR[TIMEFRAMES] dibaca pandas sebagai SATU kunci tuple
# (KeyError: ('M1','M5','M15')) - ditemukan saat eksekusi pertama nb03.
VR = VR.loc[:, list(TIMEFRAMES)]
print("=== Variance ratio (no-gap) ===")
print(VR.round(4).to_string())
print()
for tf in TIMEFRAMES:
    mean_vr = float(VR[tf].loc[2:].mean())
    print(f"{tf}: rata-rata VR(lag>=2) = {mean_vr:.4f} -> "
          f"{'mean-reversion' if mean_vr < 1 else 'persistence/momentum'}")'''
)

md(
    """## 4. Mean-reversion vs momentum per sesi

Tabel ringkas per sesi: `acf1` (lag 1, no-gap), `vr2`, dan arahnya. Sesi **Off** di strata A
adalah 0 bar pada M1 (empat sesi menutup 24 jam), jadi label `Off` boleh hilang di sini —
dicatat, bukan dianggap bug."""
)

code(
    '''"""ACF lag-1 dan VR(2) per sesi UTC eksklusif."""
SESSION_ROWS = []
for tf, subset in STRATA_A.items():
    clean = subset.loc[~subset["gap_return"]]
    for label in SESSION_ORDER:
        window = clean[clean["session_label"] == label]
        if len(window) < 1000:
            SESSION_ROWS.append(
                {"timeframe": tf, "sesi": label, "n": len(window),
                 "acf1_no_gap": np.nan, "vr2_no_gap": np.nan}
            )
            continue
        acf1 = acf_table(window, [1]).iloc[0]
        SESSION_ROWS.append(
            {
                "timeframe": tf,
                "sesi": label,
                "n": int(len(window)),
                "acf1_no_gap": float(acf1["acf"]),
                "p_value_no_gap": float(acf1["p_value"]),
                "vr2_no_gap": variance_ratio(window["r"], 2),
            }
        )

SESSION_ACF = pd.DataFrame(SESSION_ROWS)
# NaN HARUS jadi "n/a", bukan "mean-reversion": baris Off punya n=0 dan acf NaN,
# dan np.where(NaN > 0) bernilai False sehingga tanpa cabang ini ia salah dilabeli.
SESSION_ACF["arah"] = np.where(
    SESSION_ACF["acf1_no_gap"].isna(),
    "n/a",
    np.where(SESSION_ACF["acf1_no_gap"] > 0, "momentum", "mean-reversion"),
)
pd.set_option("display.width", 200)
for tf in TIMEFRAMES:
    view = SESSION_ACF[SESSION_ACF["timeframe"] == tf].set_index("sesi")
    print(f"=== ACF lag-1 per sesi - {tf} ===")
    print(view.to_string())
    print()'''
)

md(
    """## 5. Stabilitas per tahun

Autokorelasi bisa berubah regime antar tahun. Tabel `acf1` per tahun per time-frame, plus
`Off` yang memang tidak muncul di M1."""
)

code(
    '''"""ACF lag-1 per tahun (no-gap)."""
YEAR_ROWS = []
for tf, subset in STRATA_A.items():
    clean = subset.loc[~subset["gap_return"]]
    for year in YEARS:
        window = clean[clean["year"] == year]
        acf1 = acf_table(window, [1]).iloc[0]
        YEAR_ROWS.append(
            {
                "timeframe": tf,
                "tahun": year,
                "n": int(len(window)),
                "acf1_no_gap": float(acf1["acf"]),
                "p_value_no_gap": float(acf1["p_value"]),
            }
        )

YEAR_ACF = pd.DataFrame(YEAR_ROWS).set_index(["timeframe", "tahun"])
print("=== ACF lag-1 per tahun (no-gap) ===")
print(YEAR_ACF.to_string())
print()
for tf in TIMEFRAMES:
    view = YEAR_ACF.loc[tf]
    print(f"{tf}: tahun dengan |acf1| terbesar = "
          f"{view['acf1_no_gap'].abs().idxmax()} "
          f"({view['acf1_no_gap'].abs().max():.6f})")'''
)

md(
    """## 6. Assertion penutup + ringkasan

Semua assertion adalah **fakta terukur** dari notebook ini, bukan placeholder. Tidak ada
assertion `True` hardcode (pelajaran nb01 SA-03)."""
)

code(
    '''"""Assertion penutup Q4 autokorelasi."""
m1_acf1 = float(ACF["M1"].loc[1, "acf_no_gap"])
m15_acf1 = float(ACF["M15"].loc[1, "acf_no_gap"])
m1_vr_mean = float(VR["M1"].loc[2:].mean())

# Stabilitas TANDA ACF1 antar tahun per time-frame. Fakta terukur, bukan asumsi:
# kalau tandanya berubah antar tahun, efeknya tidak stabil.
SIGN_STABLE = {
    tf: (YEAR_ACF.loc[tf, "acf1_no_gap"] > 0).nunique() == 1 for tf in TIMEFRAMES
}
for tf in TIMEFRAMES:
    signs = " ".join(f"{y}:{'+' if v > 0 else '-'}" for y, v in YEAR_ACF.loc[tf, "acf1_no_gap"].items())
    print(f"  tanda ACF1 {tf}: {signs}  -> {'stabil' if SIGN_STABLE[tf] else 'TIDAK stabil'}")

checks = [
    ("Definisi sesi == Notebook 00", session_fingerprint() == EXPECTED_FINGERPRINT),
    ("Tiga time-frame termuat", set(STRATA_A) == {"M1", "M5", "M15"}),
    ("Urutan waktu naik di semua time-frame", all(f["utc"].is_monotonic_increasing for f in STRATA_A.values())),
    ("Tidak ada return inf di stratum A (M1)", int(np.isinf(STRATA_A["M1"]["r"].dropna()).sum()) == 0),
    ("ACF dihitung untuk 20 lag", all(len(ACF[tf]) == 20 for tf in TIMEFRAMES)),
    ("Semua |ACF| < 1 (ACF valid)", all(float(ACF[tf]["acf_no_gap"].abs().max()) < 1.0 for tf in TIMEFRAMES)),
    ("n no-gap lebih kecil dari n total", bool((ACF["M1"]["n_no_gap"] < len(STRATA_A["M1"])).all())),
    ("VR(lag=1) mendekati 1 (definisi)", bool(abs(float(VR.loc[1, "M1"]) - 1.0) < 0.35)),
    ("Tabel per sesi memuat 4 sesi bermakna", int(SESSION_ACF["acf1_no_gap"].notna().sum()) >= 12),
    ("Tabel per tahun = 3 TF x 4 tahun", len(YEAR_ACF) == 12),
    ("Arah mean-reversion teridentifikasi di M1", bool((SESSION_ACF[SESSION_ACF["timeframe"] == "M1"]["arah"] == "mean-reversion").any())),
    ("Temuan: |ACF| M1 >= |ACF| M15 (microstructure di bar terkecil)", abs(m1_acf1) >= abs(m15_acf1)),
    ("Temuan: VR rata-rata M1 != 1 (ada struktur, bukan random walk murni)", abs(m1_vr_mean - 1.0) > 0.001),
    (
        "Semua |ACF1| per tahun < 0,05 (efek kecil)",
        bool(YEAR_ACF.groupby("timeframe")["acf1_no_gap"].apply(lambda s: s.abs().max() < 0.05).all()),
    ),
    ("Temuan: tanda ACF1 M1 TIDAK stabil antar tahun", SIGN_STABLE["M1"] is False),
    ("Temuan: tanda ACF1 M15 stabil antar tahun", SIGN_STABLE["M15"] is True),
    ("Baris Off tidak dilabeli arah (acf NaN)", bool((SESSION_ACF.loc[SESSION_ACF["n"] == 0, "arah"] == "n/a").all())),
]

for label, passed in checks:
    print(f"{'PASS' if passed else 'GAGAL'} {label}")

failed = [label for label, passed in checks if not passed]
assert not failed, f"assertion gagal: {failed}"
print()
print(f"RINGKASAN: {len(checks) - len(failed)}/{len(checks)} assertion PASS untuk Q4 autokorelasi.")
print()
print(f"acf1 no-gap: M1={m1_acf1:.6f} | M5={float(ACF['M5'].loc[1, 'acf_no_gap']):.6f} "
      f"| M15={m15_acf1:.6f}")
print(f"rata-rata VR(lag>=2) M1={m1_vr_mean:.4f}")'''
)

md(
    """## Ringkasan hasil dan batasnya

### Angka kunci (stratum A, no-gap)

| Metrik | M1 | M5 | M15 |
|---|---|---|---|
| ACF lag-1 | -0,004372 | -0,011582 | +0,003496 |
| rata-rata VR(lag>=2) | 0,9771 | 0,9978 | 1,0127 |
| arah dominan | mean-reversion | mean-reversion lemah | momentum lemah |

`VR(1) = 1,0000` di ketiga time-frame, sesuai definisi.

### Temuan yang penting dibaca

1. **Efeknya kecil.** |ACF| <= 0,012 di semua lag dan time-frame. Dengan biaya
   `cost_basis.default` 0,65 pip per transaksi, autokorelasi sebesar ini **belum** layak
   disebut dapat diperdagangkan - ini bahan hipotesis, bukan sinyal.
2. **Arah bergantung time-frame.** M1 condong mean-reversion (VR 0,977), M15 condong
   momentum (VR 1,013), M5 berada di antaranya.
3. **Tanda ACF1 M1 TIDAK stabil antar tahun** (2023 -, 2024 +, 2025 -, 2026 -). Efek yang
   berbalik tanda antar tahun tidak boleh diperlakukan sebagai properti tetap pasar.
   Sebaliknya tanda M15 stabil (+) tetapi besarnya sangat kecil.
4. **Per sesi (M1):** London dan NewYork mean-reversion dengan p-value < 0,05; Sydney
   bertanda momentum tetapi **tidak** signifikan (p = 0,44) - jangan dibaca sebagai temuan.

**Yang dijawab:** apakah return M1/M5/M15 menunjukkan autokorelasi, seberapa besar, dan
apakah arahnya (mean-reversion atau momentum) berbeda menurut time-frame, sesi, dan tahun.

**Yang TIDAK dijawab dan sengaja ditolak:**
- Tidak ada P&L, equity curve, atau pemilihan metode.
- Tidak ada klaim "cukup untuk strategi". Autokorelasi tanpa pengurangan biaya spread
  **bukan** profitabilitas; `cost_basis.default` 0,65 pip adalah biaya MEAN yang harus
  dikurangkan sebelum klaim apa pun.
- **Kalender berita di luar scope** → autokorelasi masih memuat efek berita dan gap.
- Tidak ada uji formal multivariat; ini deskripsi satu variabel.

**Cara memakai angka ini nanti:** nilai ACF/VR adalah **bahan hipotesis**. Nilai mutlak
yang kecil (mendekati 0) berarti efeknya kecil dibanding noise, terpisah dari apakah
signifikan secara statistik pada n > 1 juta bar."""
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
