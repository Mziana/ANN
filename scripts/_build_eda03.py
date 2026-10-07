"""Generator + executor for notebooks/scalping/eda_03_autocorr.ipynb.

Q4 (autocorrelation of returns): ACF lag 1-60, the manual Ljung-Box screen required
by the design, variance-ratio at the contract horizons (k=5/15/60), sign
autocorrelation lag-1, and every headline metric repeated for strata A vs B
(plus per-session and per-year slices). Measurement only - no strategy, no P&L.
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
- **ACF lag 1-60** `[KD]` per time-frame (M1, M5, M15) untuk **strata A dan B**.
- **Uji Ljung-Box** manual — Q/n + besaran; p hanya pelengkap (D2).
- **Variance ratio** `Var(r_lag)/(l * Var(r_1))` pada horizon kontrak **k=5/15/60**,
  plus kurva penuh 1-60 (D3).
- **Sign-autocorrelation lag-1** (ACF dari tanda return) — D4.
- **Perbandingan strata A vs B** untuk seluruh metrik headline (D5).
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
- **B** = H1-2023 (regime SA-03, likuiditas rusak) — **dianalisis sebagai pembanding**
  untuk seluruh metrik headline (D5; `b_mask` sebelumnya didefinisikan tapi tak dipakai).
- **C** = dua jendela anomali digit jam — **eksklusi deskriptif**, tidak masuk kesimpulan
  (rancangan §6).
- **A** = sisanya (**stratum utama notebook ini**)"""
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

# Stratum B dipakai sebagai PEMBANDING (D5). Pola subset sengaja sama dengan A supaya
# perbandingannya apples-to-apples: hari-broker dari b_mask dipetakan ke tiap TF.
STRATA_B: dict[str, pd.DataFrame] = {}
for tf, frame in DATA.items():
    keep = frame["broker_day"].isin(wall_date[b_mask].unique())
    STRATA_B[tf] = add_labels(frame.loc[keep].copy())

for tf, subset in STRATA_B.items():
    assert subset["utc"].is_monotonic_increasing, f"B {tf}: urutan waktu harus naik"
    assert int(subset["gap_return"].sum()) < len(subset), f"B {tf}: gap_return harus jarang"

STRATA: dict[str, dict[str, pd.DataFrame]] = {"A": STRATA_A, "B": STRATA_B}
B_M1_DOC = 185_248  # bar M1 stratum B yang tercatat (STATE/Lapisan 1) - regression lock

print(f"symbol={SYMBOL} | pip_size={PIP_SIZE}")
print("strata A: " + ", ".join(f"{tf}={len(STRATA_A[tf]):,}" for tf in TIMEFRAMES))
print("strata B: " + ", ".join(f"{tf}={len(STRATA_B[tf]):,}" for tf in TIMEFRAMES))
assert len(STRATA_B["M1"]) == B_M1_DOC, f"stratum B M1 harus {B_M1_DOC:,} bar"
print("gap_return: " + ", ".join(f"{tf}={int(STRATA_A[tf]['gap_return'].sum()):,}" for tf in TIMEFRAMES))
assert not (b_mask & c_mask).any(), "B dan C tidak boleh tumpang tindih"
print("PASS: stratifikasi dan urutan waktu konsisten.")'''
)

md(
    """## 2. ACF lag 1-60 per time-frame (strata A dan B)

Autokorelasi sample (bukan teoritis) dihitung pada bar **berurutan waktu**. Dua versi
dilaporkan berdampingan:

- **all** — semua return (termasuk yang menyeberangi gap)
- **no-gap** — hanya return yang tidak menyeberangi gap

`LAGS = 1..60` sesuai rancangan §5 `[KD]`. Kolom `p_value_no_gap` memakai uji dua-sisi
per-lag dari scipy dan **bukan** kesimpulan per-lag; uji Ljung-Box ditegakkan di bagian 2b
bersama **aturan baca** yang mengikat. Analisis dijalankan untuk **strata A dan B**;
strata C tetap eksklusi deskriptif."""
)

code(
    '''"""Hitung ACF lag 1-60 per time-frame x strata, versi all dan no-gap."""
LAGS = list(range(1, 61))  # rancangan §5: fungsi autokorelasi lag 1-60 [KD]


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


ACF: dict[str, dict[str, pd.DataFrame]] = {}
for strata_name, frames in STRATA.items():
    ACF[strata_name] = {}
    for tf, subset in frames.items():
        no_gap_mask = ~subset["gap_return"]
        # acf_table sudah menerima DAFTAR lag: satu panggilan per versi, bukan per lag
        # (60 lag x 3 TF x 2 strata tetap murah, tapi loop per-lag membuang waktu).
        full = acf_table(subset, LAGS)
        clean = acf_table(subset, LAGS, no_gap_mask)
        ACF[strata_name][tf] = pd.DataFrame(
            {
                "acf_all": full["acf"],
                "acf_no_gap": clean["acf"],
                "p_value_no_gap": clean["p_value"],
                "n_no_gap": clean["n"],
            }
        )

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
for strata_name, tables in ACF.items():
    for tf in TIMEFRAMES:
        print(f"=== ACF {tf} (stratum {strata_name}, lag 1-60) ===")
        print(tables[tf].to_string())
        print()'''
)

md(
    """## 2b. Ljung-Box (ditegakkan) + aturan baca

Rancangan §5 meminta uji **Ljung-Box** `[PS]`. Diimplementasikan **manual via scipy**
(tanpa dependensi baru): `Q(h) = n (n + 2) * sum_{k=1..h} rho_k^2 / (n - k)`, `df = h`,
`p = chi2.sf(Q, h)`.

**ATURAN BACA (mengikat - keputusan Architect atas keberatan coder):**
1. **Nilai p tidak dipakai sebagai kesimpulan.** Pada n > 1 juta bar, reject hampir pasti.
2. Yang dibaca: **`Q/n`** (besaran per bar) dan ukuran efek (`rho_k`) itu sendiri.
3. **Slice adalah bacaan utama** (per sesi, per tahun); agregat seluruh seri hanya konteks.
4. Ljung-Box dihitung pada seri **tanpa return lintas gap**, sama seperti ACF.
"""
)

code(
    '''"""Ljung-Box manual (Q dan p) untuk horizon kontrak, strata A dan B."""
LB_HORIZONS = (5, 15, 60)


def ljung_box(
    frame: pd.DataFrame, horizons: tuple[int, ...], mask: pd.Series | None = None
) -> pd.DataFrame:
    """Uji Ljung-Box manual: Q(h) dan p(h) per horizon.

    Q(h) = n (n + 2) * sum_{k=1..h} rho_k^2 / (n - k); p = chi2.sf(Q, df=h).

    Args:
        frame: Frame dengan kolom r.
        horizons: Horizon h yang dilaporkan (mis. (5, 15, 60)).
        mask: Masker bar opsional (mis. tanpa gap).

    Returns:
        DataFrame terindeks h dengan kolom n, Q, Q_per_n, df, p.

    Catatan: nilai p BUKAN kesimpulan (lihat aturan baca di markdown 2b); yang dibaca
    adalah Q/n dan besaran rho_k.
    """
    max_h = max(horizons)
    rho_table = acf_table(frame, list(range(1, max_h + 1)), mask)
    n = int(rho_table["n"].iloc[0])
    rho = rho_table["acf"].to_numpy(dtype="float64")
    weighted = np.cumsum(rho**2 / (n - np.arange(1, max_h + 1)))
    rows = []
    for h in horizons:
        q = float(n * (n + 2) * weighted[h - 1])
        rows.append(
            {"h": h, "n": n, "Q": q, "Q_per_n": q / n, "df": h, "p": float(stats.chi2.sf(q, h))}
        )
    return pd.DataFrame(rows).set_index("h")


LB: dict[str, dict[str, pd.DataFrame]] = {}
for strata_name, frames in STRATA.items():
    LB[strata_name] = {}
    for tf, subset in frames.items():
        LB[strata_name][tf] = ljung_box(subset, LB_HORIZONS, ~subset["gap_return"])

for strata_name, tables in LB.items():
    for tf in TIMEFRAMES:
        print(f"=== Ljung-Box {tf} (stratum {strata_name}, no-gap) ===")
        print(tables[tf].round(6).to_string())
        print()
print("ATURAN BACA: p bukan kesimpulan; baca Q/n + besaran rho_k; slice = bacaan utama.")'''
)

md(
    """## 2c. Sign-autocorrelation lag-1

Autokorelasi dari **tanda** return (`sign(r)`) di lag 1 - mengukur persistensi arah, bukan
besaran. Melengkapi label momentum/mean-reversion yang sudah ada (D4). Dihitung untuk
strata A dan B pada seri tanpa gap.
"""
)

code(
    '''"""Sign-ACF lag-1 per time-frame x strata (no-gap)."""
SIGN_ACF: dict[str, dict[str, float]] = {}
for strata_name, frames in STRATA.items():
    SIGN_ACF[strata_name] = {}
    for tf, subset in frames.items():
        sign_frame = pd.DataFrame({"r": np.sign(subset["r"])})
        row = acf_table(sign_frame, [1], ~subset["gap_return"]).iloc[0]
        SIGN_ACF[strata_name][tf] = float(row["acf"])

SIGN_ACF_TABLE = pd.DataFrame(SIGN_ACF)
print("=== Sign-ACF lag 1 (no-gap) ===")
print(SIGN_ACF_TABLE.round(6).to_string())
print()
for strata_name in SIGN_ACF_TABLE:
    for tf in TIMEFRAMES:
        value = float(SIGN_ACF_TABLE.loc[tf, strata_name])
        print(f"{strata_name} {tf}: sign-ACF(1) = {value:+.6f} -> "
              f"{'momentum' if value > 0 else 'mean-reversion'}")'''
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
menyeberangi gap, supaya tidak tercampur lompatan harga saat pasar tutup.

Horizon kontrak `[KD]`: **k = 5/15/60** (dilaporkan eksplisit), dan kurva penuh 1-60 ikut
dihitung (ekstensi lag D1) supaya horizon alternatif terlihat. Rata-rata `lag >= 2`
dilaporkan **dua jendela** (2-20 lama vs 2-60 baru) agar efek ekstensi lag terpisah dari
efek struktur. `VR(2)` tetap ada di tabel per sesi. Dihitung untuk **strata A dan B**."""
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


VR_HORIZONS = (5, 15, 60)  # horizon kontrak rancangan §5

VR: dict[str, pd.DataFrame] = {}
for strata_name, frames in STRATA.items():
    rows = []
    for tf, subset in frames.items():
        clean = subset.loc[~subset["gap_return"], "r"]
        for lag in LAGS:
            rows.append({"timeframe": tf, "lag": lag, "vr_no_gap": variance_ratio(clean, lag)})
    table = pd.DataFrame(rows).pivot(index="lag", columns="timeframe", values="vr_no_gap")
    # .loc[:, ...] wajib: table[TIMEFRAMES] dibaca pandas sebagai SATU kunci tuple
    # (KeyError: ('M1','M5','M15')) - ditemukan saat eksekusi pertama nb03.
    VR[strata_name] = table.loc[:, list(TIMEFRAMES)]
    print(f"=== Variance ratio (no-gap, stratum {strata_name}) ===")
    print(VR[strata_name].round(4).to_string())
    print()
    print(f"--- VR pada horizon kontrak {VR_HORIZONS} (stratum {strata_name}) ---")
    print(VR[strata_name].loc[list(VR_HORIZONS)].round(4).to_string())
    print()
    for tf in TIMEFRAMES:
        mean_full = float(VR[strata_name][tf].loc[2:60].mean())
        mean_old = float(VR[strata_name][tf].loc[2:20].mean())
        print(f"{strata_name} {tf}: rata-rata VR(lag 2-60) = {mean_full:.4f} "
              f"| (lag 2-20 = {mean_old:.4f}) -> "
              f"{'mean-reversion' if mean_full < 1 else 'persistence/momentum'}")'''
)

md(
    """## 4. Mean-reversion vs momentum per sesi (strata A dan B)

Tabel ringkas per sesi: `acf1` (lag 1, no-gap), `sign_acf1` (lag 1 dari tanda return,
melengkapi label arah - D4), `vr2`, dan arahnya. Kolom `strata` memisahkan A dan B (D5).
Sesi **Off** bisa kosong di M1 (empat sesi menutup 24 jam), jadi label `Off` boleh hilang
di sini - dicatat, bukan dianggap bug."""
)

code(
    '''"""ACF lag-1, sign-ACF lag-1, dan VR(2) per sesi UTC eksklusif x strata."""
SESSION_ROWS = []
for strata_name, frames in STRATA.items():
    for tf, subset in frames.items():
        clean = subset.loc[~subset["gap_return"]]
        for label in SESSION_ORDER:
            window = clean[clean["session_label"] == label]
            if len(window) < 1000:
                SESSION_ROWS.append(
                    {
                        "strata": strata_name,
                        "timeframe": tf,
                        "sesi": label,
                        "n": len(window),
                        "acf1_no_gap": np.nan,
                        "sign_acf1": np.nan,
                        "vr2_no_gap": np.nan,
                    }
                )
                continue
            acf1 = acf_table(window, [1]).iloc[0]
            # D4: ACF dari TANDA return (bukan besaran) - melengkapi label arah.
            sign1 = acf_table(pd.DataFrame({"r": np.sign(window["r"])}), [1]).iloc[0]
            SESSION_ROWS.append(
                {
                    "strata": strata_name,
                    "timeframe": tf,
                    "sesi": label,
                    "n": int(len(window)),
                    "acf1_no_gap": float(acf1["acf"]),
                    "p_value_no_gap": float(acf1["p_value"]),
                    "sign_acf1": float(sign1["acf"]),
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
SESSION_ACF["arah_sign"] = np.where(
    SESSION_ACF["sign_acf1"].isna(),
    "n/a",
    np.where(SESSION_ACF["sign_acf1"] > 0, "momentum", "mean-reversion"),
)
pd.set_option("display.width", 220)
for strata_name in STRATA:
    for tf in TIMEFRAMES:
        view = SESSION_ACF[
            (SESSION_ACF["strata"] == strata_name) & (SESSION_ACF["timeframe"] == tf)
        ].set_index("sesi")
        print(f"=== ACF lag-1 & sign-ACF lag-1 per sesi - {tf} (stratum {strata_name}) ===")
        print(view.to_string())
        print()'''
)

md(
    """## 5. Stabilitas per tahun (stratum A)

Autokorelasi bisa berubah regime antar tahun. Tabel `acf1` per tahun per time-frame, plus
`Off` yang memang tidak muncul di M1. Slice per tahun ini **A saja**: stratum B = H1-2023
hanya memuat satu tahun kalender, sehingga slice per tahunnya degeneratif (satu baris) -
batas yang saya nyatakan terbuka, bukan disembunyikan."""
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
    """## 5b. Ljung-Box pada slice (bacaan utama)

Sesuai aturan baca 2b, **slice adalah bacaan utama**: `h = 15` per sesi (stratum A) dan per
tahun (stratum A). B tidak di-slice per tahun karena hanya satu tahun kalender; cakupan B di
level sesi sudah ada di tabel sesi berkolom `strata`. Per-sesi di sini **A saja** sesuai
keputusan user pada langkah 2."""
)

code(
    '''"""Ljung-Box h=15 pada slice: per sesi (A) dan per tahun (A)."""
LB_SLICE_H = 15

LB_SESSION_ROWS = []
for tf, subset in STRATA_A.items():
    clean = subset.loc[~subset["gap_return"]]
    for label in SESSION_ORDER:
        window = clean[clean["session_label"] == label]
        if len(window) < 1000:
            continue
        row = ljung_box(window, (LB_SLICE_H,)).iloc[0]
        LB_SESSION_ROWS.append(
            {
                "timeframe": tf,
                "sesi": label,
                "n": int(row["n"]),
                "Q": float(row["Q"]),
                "Q_per_n": float(row["Q_per_n"]),
                "p": float(row["p"]),
            }
        )
LB_SESSION = pd.DataFrame(LB_SESSION_ROWS)

LB_YEAR_ROWS = []
for tf, subset in STRATA_A.items():
    clean = subset.loc[~subset["gap_return"]]
    for year in YEARS:
        window = clean[clean["year"] == year]
        row = ljung_box(window, (LB_SLICE_H,)).iloc[0]
        LB_YEAR_ROWS.append(
            {
                "timeframe": tf,
                "tahun": year,
                "n": int(row["n"]),
                "Q": float(row["Q"]),
                "Q_per_n": float(row["Q_per_n"]),
                "p": float(row["p"]),
            }
        )
LB_YEAR = pd.DataFrame(LB_YEAR_ROWS)

print(f"=== Ljung-Box h={LB_SLICE_H} per sesi (stratum A, no-gap) ===")
print(LB_SESSION.round(6).to_string(index=False))
print()
print(f"=== Ljung-Box h={LB_SLICE_H} per tahun (stratum A, no-gap) ===")
print(LB_YEAR.round(6).to_string(index=False))
print()'''
)

md(
    """## 5c. Perbandingan A vs B (inti SA-03)

Selisih `B - A` untuk tiga metrik headline Q4. Dibaca sebagai **besaran**, bukan
signifikansi: B = H1-2023 hanya 6 bulan, jadi daya ujinya kecil ("tidak terdeteksi" bukan
"sama"). Tidak ada uji formal di sini - ini deskripsi selisih, bukan klaim."""
)

code(
    '''"""Tabel delta A vs B untuk metrik headline (no-gap)."""
DELTA_ROWS = []
for tf in TIMEFRAMES:
    a_acf1 = float(ACF["A"][tf].loc[1, "acf_no_gap"])
    b_acf1 = float(ACF["B"][tf].loc[1, "acf_no_gap"])
    a_sign = float(SIGN_ACF_TABLE.loc[tf, "A"])
    b_sign = float(SIGN_ACF_TABLE.loc[tf, "B"])
    a_vr = float(VR["A"][tf].loc[2:60].mean())
    b_vr = float(VR["B"][tf].loc[2:60].mean())
    DELTA_ROWS.append(
        {
            "timeframe": tf,
            "acf1_A": a_acf1,
            "acf1_B": b_acf1,
            "d_acf1": b_acf1 - a_acf1,
            "sign_A": a_sign,
            "sign_B": b_sign,
            "d_sign": b_sign - a_sign,
            "vrmean_A": a_vr,
            "vrmean_B": b_vr,
            "d_vrmean": b_vr - a_vr,
        }
    )
DELTA_AB = pd.DataFrame(DELTA_ROWS).set_index("timeframe")
print("=== Delta A vs B (B - A), no-gap, lag 1-60 ===")
print(DELTA_AB.round(6).to_string())'''
)

md(
    """## 6. Assertion penutup + ringkasan

Semua assertion adalah **fakta terukur** dari notebook ini, bukan placeholder. Tidak ada
assertion `True` hardcode (pelajaran nb01 SA-03)."""
)

code(
    '''"""Assertion penutup Q4 autokorelasi (strata A + B)."""
m1_acf1 = float(ACF["A"]["M1"].loc[1, "acf_no_gap"])
m15_acf1 = float(ACF["A"]["M15"].loc[1, "acf_no_gap"])
m1_vr_mean = float(VR["A"]["M1"].loc[2:60].mean())
m1_vr_mean_old = float(VR["A"]["M1"].loc[2:20].mean())
acf_max_abs = max(float(ACF[s][tf]["acf_no_gap"].abs().max()) for s in ACF for tf in TIMEFRAMES)

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
    ("Strata A dan B keduanya dianalisis", set(STRATA) == {"A", "B"}),
    ("Jumlah bar M1 stratum B = catatan resmi", len(STRATA_B["M1"]) == B_M1_DOC),
    ("Urutan waktu naik di semua time-frame", all(f["utc"].is_monotonic_increasing for f in STRATA_A.values())),
    ("Tidak ada return inf di stratum A (M1)", int(np.isinf(STRATA_A["M1"]["r"].dropna()).sum()) == 0),
    ("ACF dihitung untuk 60 lag (1-60)", all(len(ACF[s][tf]) == 60 for s in ACF for tf in TIMEFRAMES)),
    ("LAGS memuat 1, 5, 15, 60", {1, 5, 15, 60} <= set(LAGS)),
    ("Semua |ACF| < 1 (ACF valid)", all(float(ACF[s][tf]["acf_no_gap"].abs().max()) < 1.0 for s in ACF for tf in TIMEFRAMES)),
    ("n no-gap lebih kecil dari n total (A, M1)", bool((ACF["A"]["M1"]["n_no_gap"] < len(STRATA_A["M1"])).all())),
    ("VR(lag=1) mendekati 1 di A dan B", bool(all(abs(float(VR[s].loc[1, tf]) - 1.0) < 0.35 for s in VR for tf in TIMEFRAMES))),
    ("VR memuat horizon kontrak 5/15/60", all(set(VR_HORIZONS) <= set(VR[s].index) for s in VR)),
    ("VR dihitung untuk 60 lag", all(len(VR[s]) == 60 for s in VR)),
    ("Ljung-Box: Q > 0 dan Q/n > 0 di A dan B", all(bool((t["Q"] > 0).all() and (t["Q_per_n"] > 0).all()) for s in LB for t in LB[s].values())),
    ("Ljung-Box: p dalam [0, 1]", all(bool(t["p"].between(0.0, 1.0).all()) for s in LB for t in LB[s].values())),
    ("Ljung-Box slice sesi h=15 terisi (A)", len(LB_SESSION) >= 12),
    ("Ljung-Box slice tahun h=15 = 3 TF x 4 tahun (A)", len(LB_YEAR) == 12),
    ("Sign-ACF lag-1 terhitung (finite) di A dan B", bool(np.isfinite(SIGN_ACF_TABLE.to_numpy(dtype="float64")).all())),
    ("Tabel per sesi mencakup A dan B", set(SESSION_ACF.loc[SESSION_ACF["acf1_no_gap"].notna(), "strata"]) == {"A", "B"}),
    ("Tabel per sesi memuat >= 12 baris bermakna", int(SESSION_ACF["acf1_no_gap"].notna().sum()) >= 12),
    ("Arah berbasis tanda terisi untuk baris bermakna", bool((SESSION_ACF.loc[SESSION_ACF["sign_acf1"].notna(), "arah_sign"] != "n/a").all())),
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
    ("Tabel delta A vs B lengkap (3 TF)", len(DELTA_AB) == 3),
    ("Delta A vs B konsisten dengan tabel sumber", bool(np.isclose(float(DELTA_AB.loc["M1", "d_acf1"]), float(ACF["B"]["M1"].loc[1, "acf_no_gap"]) - m1_acf1))),
]

for label, passed in checks:
    print(f"{'PASS' if passed else 'GAGAL'} {label}")

failed = [label for label, passed in checks if not passed]
assert not failed, f"assertion gagal: {failed}"
print()
print(f"RINGKASAN: {len(checks) - len(failed)}/{len(checks)} assertion PASS untuk Q4 autokorelasi.")
print()
for strata_name, tables in ACF.items():
    print(f"acf1 no-gap {strata_name}: " + " | ".join(
        f"{tf}={float(tables[tf].loc[1, 'acf_no_gap']):.6f}" for tf in TIMEFRAMES))
print(f"rata-rata VR(lag 2-60) A M1={m1_vr_mean:.4f} (lag 2-20 = {m1_vr_mean_old:.4f})")
print(f"|ACF| maksimum lintas strata/TF = {acf_max_abs:.4f} (semua lag 1-60)")
for strata_name, tables in LB.items():
    for tf in TIMEFRAMES:
        row = tables[tf]
        print(f"LB {strata_name} {tf}: Q/n(h=5)={float(row.loc[5, 'Q_per_n']):.6f} "
              f"| Q/n(h=15)={float(row.loc[15, 'Q_per_n']):.6f} "
              f"| Q/n(h=60)={float(row.loc[60, 'Q_per_n']):.6f}")
print("sign-ACF lag-1 (no-gap):")
print(SIGN_ACF_TABLE.round(6).to_string())'''
)

md(
    """## Ringkasan hasil dan batasnya

### Angka kunci (no-gap, lag 1-60)

| Metrik | A M1 | A M5 | A M15 | B M1 | B M5 | B M15 |
|---|---|---|---|---|---|---|
| ACF lag-1 | -0,004372 | -0,011582 | +0,003496 | -0,000864 | -0,005795 | +0,005980 |
| sign-ACF lag-1 | -0,017702 | -0,009805 | -0,022624 | -0,013226 | -0,012994 | -0,017336 |
| rata-rata VR(lag 2-60) | 0,9796 | 0,9942 | 1,0337 | 0,9848 | 1,0332 | 1,0236 |
| VR pada k=60 | 0,9809 | 0,9992 | 1,0657 | 0,9916 | 1,0564 | 0,9631 |

`VR(1) = 1,0000` di semua strata/time-frame (definisi). Untuk perbandingan, jendela lama
A saja (lag 2-20): 0,9771 / 0,9978 / 1,0127 - **pergeseran akibat ekstensi lag dilaporkan,
bukan disembunyikan**.

### Temuan yang penting dibaca

1. **Ekstensi lag 1-60 menemukan hal baru, dan klaim lama gugur.** Klaim "|ACF| <= 0,012 di
   semua lag" **TIDAK berlaku lagi**: maksimum |ACF| lintas strata/time-frame/lag =
   **0,0226** (B M15, lag 50); di A saja M15 lag 2 = 0,0148 dan lag 30 = 0,0125. Sebagian
   nilai terbesar jatuh di lag 21-60 yang sebelumnya tidak pernah diperiksa.
2. **sign-ACF lag-1 negatif di semua sel** (-0,0098 s/d -0,0226), dan **lebih besar** dari
   ACF lag-1 biasa. Artinya arah cenderung berbalik sementara besarnya tidak. Di M15 A ini
   **berlawanan arah** dengan label dari ACF besaran (+0,0035, VR > 1): dua label dilaporkan
   berdampingan, tidak ada yang dipilih diam-diam.
3. **A vs B:** pada M15 efek B sebanding/lebih besar (maks |ACF| 0,0226 vs A 0,0148),
   sedangkan ACF lag-1 M1 B lebih kecil dari A (-0,00086 vs -0,00437). B hanya 6 bulan
   (n M15 = 12.395) sehingga "tidak terdeteksi" TIDAK sama dengan "sama".
4. **Ljung-Box:** Q/n sangat kecil di semua sel (A M1 5,1e-5 pada h=5 s/d 4,1e-4 pada h=60;
   B M15 2,8e-4 s/d 5,3e-3). p nyaris selalu 0 di A karena n > 1 juta, dan baru informatif di
   B M15 (0,63 / 0,28 / 0,30). Sesuai aturan baca: **p tidak menyimpulkan**, yang dibaca Q/n.
   Slice: terbesar di Sydney (M15 Q/n = 0,0225) dan di M1 2023/2026 (0,00117 / 0,00124) vs
   2024/2025 (~0,0003).
5. **Tanda ACF1 tidak stabil antar tahun di M1 DAN M5** (M1: -, +, -, - ; M5: +, -, -, -);
   hanya M15 stabil (+) dengan besaran sangat kecil (maks |acf1| tahunan 0,0079).
6. **Per sesi (M1, stratum A):** acf1 London -0,0063 / NewYork -0,0041 / Tokyo -0,0032 /
   Sydney +0,0027, semuanya sign-ACF negatif (Sydney paling negatif, -0,0238). Label
   "Sydney momentum" berasal dari besaran dan **hilang** saat dibaca dari tanda.

**Yang dijawab:** apakah return M1/M5/M15 menunjukkan autokorelasi, seberapa besar, dan
apakah arahnya (mean-reversion atau momentum) berbeda menurut time-frame, sesi, tahun, dan
**strata (A vs B)**; apakah lag 21-60 memuat struktur yang tidak terlihat di lag 1-20;
apakah tanda return (sign-ACF) searah dengan besaran; dan apakah autokorelasi itu lebih dari
sekadar artefak n > 1 juta (dibaca lewat Q/n, bukan p).

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
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
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
