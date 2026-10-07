"""Generator + executor for notebooks/scalping/eda_04_swings_levels.ipynb.

Q5 (swing/fractal structure) and Q6 (level touch & reaction) for the scalping EDA
chain, including the placebo protocol that was PREREGISTERED in notebook 00.
The preregistration constants are parsed straight out of notebook 00 and asserted
to match, so this notebook cannot silently drift from the locked protocol.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_04_swings_levels.ipynb"
NB00_PATH = PROJECT_ROOT / "notebooks/scalping/eda_00_setup.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA 04 — Q5 Struktur Swing + Q6 Level (dengan Placebo Preregistrasi)

**Rancangan:** EDA v3 Final. **Purpose:** mengukur *struktur bentuk* harga — bukan sinyal.

## Yang dijawab
- **Q5:** struktur swing/fraktal di M5 (k=3 dan k=5 per sisi), ukuran dinormalisasi ATR(14),
  sebaran per sesi dan per tahun.
- **Q6:** apakah level (round-number, prior-day high/low) benar-benar "dihormati" pasar,
  diukur lewat **touch & reaksi** dan dibandingkan terhadap **kontrol placebo**.

## Kontrak placebo (WAJIB — preregistrasi nb00, tanpa tuning)
Parameter protokol di notebook ini **bukan** pilihan baru: nilainya **dibaca langsung dari
`eda_00_setup.ipynb` dan di-assert sama persis**. Kalau nb00 berubah, notebook ini gagal
dengan sengaja, bukan diam-diam memakai protokol berbeda.

## Batas keras (Wajib)
- **Tidak** ada P&L, equity, backtest, atau pemilihan metode.
- **Tidak** menulis `configs/` atau `src/`.
- **Tidak** ada imputasi.
- Anti look-ahead: semua rolling memakai `.shift(1)`; theta dihitung sampai bar `t-1`.
- **Tanpa bukti = tanpa klaim.** Level/Fibonacci tidak diklaim bekerja bila hit-rate-nya
  tidak melampaui placebo.
"""
)

code(
    '''"""Setup lingkungan dan kunci versi."""
import ast
import importlib.metadata
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


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
    EXPECTED_FINGERPRINT,
    SESSION_ORDER,
    add_labels,
    session_fingerprint,
)

print("PROJECT_ROOT :", PROJECT_ROOT)
print("python       :", sys.version.split()[0])
for package in ("pandas", "numpy", "pyarrow", "tzdata"):
    print(f"  {package:11s}: {importlib.metadata.version(package)}")

assert importlib.metadata.version("tzdata") == "2026.5", "tzdata harus 2026.5 (Kontrak 00)"
assert int(importlib.metadata.version("pandas").split(".")[0]) == 2, (
    "Notebook WAJIB jalan di venv kanonik (pandas 2.x); pandas 3.x merusak satuan .asi8."
)'''
)

md(
    """## 0. Assertion definisi sesi + PREREGISTRASI PLACEBO (anti-drift)

Dua hal dikunci di sini:

1. **Definisi sesi** — sidik jari sama persis dengan nb00/nb01/nb02/nb03.
2. **Parameter protokol placebo Q6** — dibaca dari `eda_00_setup.ipynb` dan di-assert sama
   dengan nilai yang dipakai notebook ini. Inilah yang membuat klaim "persis preregistrasi
   nb00" menjadi **terverifikasi mesin**, bukan sekadar niat baik."""
)

code(
    '''"""Baca preregistrasi placebo dari nb00 dan assert sama persis dengan nb04."""


def preregistrasi_dari_nb00(path: Path) -> dict[str, object]:
    """Ekstrak konstanta protokol placebo dari notebook 00.

    Args:
        path: Path ke eda_00_setup.ipynb.

    Returns:
        Dict nama-konstanta -> nilai, untuk nama yang jadi bagian protokol.
    """
    notebook = json.loads(path.read_text(encoding="utf-8"))
    kunci = (
        "PLACEBO_SEED",
        "PLACEBO_TIMEFRAME",
        "TOUCH_ATR_WINDOW",
        "REACTION_THETA_ATR",
        "REACTION_WINDOWS_BARS",
        "REACTION_WINDOW_PRIMARY",
        "PLACEBO_RANDOM_OFFSET_PIPS",
        "PLACEBO_PRIOR_HL_SHIFT_ATR",
        "BOOTSTRAP_RESAMPLES",
        "BOOTSTRAP_UNIT",
        "CI_METHOD",
    )
    found: dict[str, object] = {}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        if "PLACEBO_SEED" not in source:
            continue
        for node in ast.parse(source).body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id in kunci:
                    found[target.id] = ast.literal_eval(node.value)
    return found


# ==== Protokol placebo: nilai di bawah WAJIB sama dengan nb00 ====
PLACEBO_SEED = 20261006
PLACEBO_TIMEFRAME = "M5"
TOUCH_ATR_WINDOW = 14
REACTION_THETA_ATR = 0.5
REACTION_WINDOWS_BARS = (6, 12, 24)
REACTION_WINDOW_PRIMARY = 12
PLACEBO_RANDOM_OFFSET_PIPS = (5.0, 25.0)
PLACEBO_PRIOR_HL_SHIFT_ATR = (0.25, 1.00)
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_UNIT = "hari perdagangan (day-cluster)"
CI_METHOD = "persentil 95%"

MILIK_NB04 = {
    "PLACEBO_SEED": PLACEBO_SEED,
    "PLACEBO_TIMEFRAME": PLACEBO_TIMEFRAME,
    "TOUCH_ATR_WINDOW": TOUCH_ATR_WINDOW,
    "REACTION_THETA_ATR": REACTION_THETA_ATR,
    "REACTION_WINDOWS_BARS": REACTION_WINDOWS_BARS,
    "REACTION_WINDOW_PRIMARY": REACTION_WINDOW_PRIMARY,
    "PLACEBO_RANDOM_OFFSET_PIPS": PLACEBO_RANDOM_OFFSET_PIPS,
    "PLACEBO_PRIOR_HL_SHIFT_ATR": PLACEBO_PRIOR_HL_SHIFT_ATR,
    "BOOTSTRAP_RESAMPLES": BOOTSTRAP_RESAMPLES,
    "BOOTSTRAP_UNIT": BOOTSTRAP_UNIT,
    "CI_METHOD": CI_METHOD,
}

NB00_PREREG = preregistrasi_dari_nb00(PROJECT_ROOT / "notebooks/scalping/eda_00_setup.ipynb")
print("PREREGISTRASI PLACEBO Q6 — dibaca dari eda_00_setup.ipynb:")
for name, value in sorted(NB00_PREREG.items()):
    print(f"  {name:26s}: {value}")

selisih = {
    k: (MILIK_NB04.get(k), v) for k, v in NB00_PREREG.items() if MILIK_NB04.get(k) != v
}
assert not selisih, f"Protokol nb04 berbeda dari preregistrasi nb00: {selisih}"
print()
print("PASS: seluruh konstanta protokol placebo nb04 identik dengan preregistrasi nb00.")
assert session_fingerprint() == EXPECTED_FINGERPRINT, (
    "Definisi sesi berubah vs Notebook 00 - STOP, kembalikan ke kontrak."
)
print("PASS: definisi sesi identik dengan Notebook 00.")'''
)

md(
    """## 1. Memuat M5 + ATR(14) + theta + stratifikasi

M5 adalah timeframe protokol (preregistrasi). Return/ATR dihitung **setelah** pengurutan
kronologis, dan semua rolling memakai `.shift(1)` supaya theta di bar `t` hanya memakai
informasi sampai `t-1` (aturan anti look-ahead Kontrak 00).

Stratifikasi A/B/C sama seperti nb01-nb03:
- **B** = H1-2023 (regime SA-03) · **C** = dua jendela anomali digit jam · **A** = sisanya
  (**semua analisis utama di notebook ini**)"""
)

code(
    '''"""Muat M5 + D1, hitung ATR(14), theta, broker/UTC day, lalu ambil stratum A."""
config = load_config("data")
SYMBOL = config["mt5"]["symbol"]
SCHEDULE = BrokerSchedule.from_config(config["mt5"])
ANOMALY_WINDOWS = tuple((w["start"], w["end"]) for w in config["validation"]["anomaly_windows"])
YEARS = (2023, 2024, 2025, 2026)
PIP_SIZE = float(config["spread"]["pip_size"][SYMBOL])
COLUMNS = ["time", "broker_time_raw", "open", "high", "low", "close"]


def load_tf(tf: str) -> pd.DataFrame:
    """Muat satu timeframe 2023-2026, urutkan kronologis, tandai hari broker/UTC.

    Args:
        tf: Kode timeframe, mis. 'M5'.

    Returns:
        Frame terurut dengan kolom utc, broker_day, utc_day, broker_time_raw.
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
    out["utc_day"] = out["utc"].dt.normalize()
    out = out.sort_values("utc", kind="mergesort").reset_index(drop=True)
    return out


def true_range(frame: pd.DataFrame) -> pd.Series:
    """True range: max(H-L, |H-C_prev|, |L-C_prev|)."""
    prev_close = frame["close"].shift(1)
    return pd.concat(
        [
            frame["high"] - frame["low"],
            (frame["high"] - prev_close).abs(),
            (frame["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)


m5 = load_tf(PLACEBO_TIMEFRAME)
# ATR(14) lalu .shift(1): theta di bar t hanya memakai informasi sampai t-1.
m5["atr14"] = true_range(m5).rolling(TOUCH_ATR_WINDOW, min_periods=TOUCH_ATR_WINDOW).mean().shift(1)
m5["theta"] = REACTION_THETA_ATR * m5["atr14"]
m5["r"] = np.log(m5["close"] / m5["close"].shift(1))
m5 = add_labels(m5)
m5["year"] = m5["wall"].dt.year

wall_date = m5["broker_day"]
b_mask = (wall_date >= pd.Timestamp("2023-01-01")) & (wall_date <= pd.Timestamp("2023-06-30"))
c_mask = pd.Series(False, index=m5.index)
for start, end in ANOMALY_WINDOWS:
    c_mask |= (wall_date >= pd.Timestamp(start)) & (wall_date <= pd.Timestamp(end))
a_mask = ~(b_mask | c_mask)

A = m5.loc[a_mask].reset_index(drop=True)
A["row"] = np.arange(len(A))

print(f"symbol={SYMBOL} | timeframe protokol={PLACEBO_TIMEFRAME} | pip={PIP_SIZE}")
print(f"bar M5 total={len(m5):,} | strata A={len(A):,} | B={int(b_mask.sum()):,} | C={int(c_mask.sum()):,}")
print(f"theta tersedia (non-NaN) = {int(A['theta'].notna().sum()):,} bar")
assert A["utc"].is_monotonic_increasing, "urutan waktu harus naik"
assert len(A) > 0, "strata A kosong"
assert not (b_mask & c_mask).any(), "B dan C tidak boleh tumpang tindih"
print("PASS: M5 termuat, ATR/theta terhitung, urutan naik.")

# D1 dipakai untuk placebo 2 (shift prior-day H/L dalam satuan ATR(14) D1).
d1 = load_tf("D1")
d1["atr14_d1"] = true_range(d1).rolling(TOUCH_ATR_WINDOW, min_periods=TOUCH_ATR_WINDOW).mean()
print(f"bar D1 = {len(d1):,} | ATR(14) D1 non-NaN = {int(d1['atr14_d1'].notna().sum()):,}")'''
)

md(
    """## 2. Q5 — Struktur swing/fraktal (k=3 dan k=5)

Definisi terkunci Kontrak 00: **fraktal k=3 dan k=5 bar per sisi di M5, keduanya dilaporkan**,
ukuran dinormalisasi ATR(14).

Swing high di bar `i` untuk `k`: `high[i]` lebih tinggi dari `high[i-k..i-1]` dan `high[i+1..i+k]`.
**Catatan anti look-ahead:** fraktal baru terkonfirmasi `k` bar setelahnya. Karena itu Q5
dilaporkan sebagai **deskriptif struktur historis**, bukan fitur yang tersedia real-time.

Dua metrik kontrak yang ditambahkan di sel ini: **D6** frekuensi swing **per hari**
(rancangan §5: "frekuensi swing per hari dan per sesi") dan **D7** **waktu tahan median antar
swing** (jarak antar indeks fraktal - bukan durasi posisi)."""
)

code(
    '''"""Deteksi fraktal k=3/k=5 di M5 stratum A + sebaran ukuran (satuan ATR)."""


def fractal_mask(values: np.ndarray, k: int, high: bool) -> np.ndarray:
    """Tandai bar yang merupakan fraktal k-per-sisi.

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


high_arr = A["high"].to_numpy(dtype="float64")
low_arr = A["low"].to_numpy(dtype="float64")

SWING_ROWS = []
for k in (3, 5):
    for sisi, mask, col in (("high", fractal_mask(high_arr, k, True), "high"),
                            ("low", fractal_mask(low_arr, k, False), "low")):
        level = A[col].to_numpy(dtype="float64")[mask]
        atr = A["atr14"].to_numpy(dtype="float64")[mask]
        valid = np.isfinite(atr) & (atr > 0)
        # Ukuran swing dalam satuan ATR: |harga - close bar sebelumnya| / ATR.
        prev_close = A["close"].shift(1).to_numpy(dtype="float64")[mask]
        size_atr = np.abs(level - prev_close) / atr
        SWING_ROWS.append(
            {
                "k": k,
                "sisi": sisi,
                "n_swing": int(mask.sum()),
                "n_valid_atr": int(valid.sum()),
                "size_atr_median": float(np.nanmedian(size_atr[valid])) if valid.any() else np.nan,
                "size_atr_p90": float(np.nanpercentile(size_atr[valid], 90)) if valid.any() else np.nan,
            }
        )
        A[f"swing_{sisi}_k{k}"] = mask

SWINGS = pd.DataFrame(SWING_ROWS)
pd.set_option("display.width", 200)
print("=== Q5: jumlah swing dan ukuran ternormalisasi ATR (stratum A) ===")
print(SWINGS.to_string(index=False))
print()

# Mask per kombinasi (k x sisi) dipakai ulang oleh D6 (frekuensi/hari) dan D7 (holding),
# supaya kedua metrik itu memakai definisi fraktal yang SAMA dengan tabel di atas.
SWING_MASKS: dict[str, np.ndarray] = {
    "high_k3": A["swing_high_k3"].to_numpy(),
    "high_k5": A["swing_high_k5"].to_numpy(),
    "low_k3": A["swing_low_k3"].to_numpy(),
    "low_k5": A["swing_low_k5"].to_numpy(),
}
SWING_MASKS["gabungan"] = (
    SWING_MASKS["high_k3"]
    | SWING_MASKS["high_k5"]
    | SWING_MASKS["low_k3"]
    | SWING_MASKS["low_k5"]
)

# Sebaran swing per sesi dan per tahun (k=3 dan k=5 digabung per sisi).
swing_any = SWING_MASKS["gabungan"]
print("=== jumlah swing (semua k/sisi) per sesi ===")
per_sesi = A.assign(swing=swing_any).groupby("session_label")["swing"].agg(["sum", "size"])
per_sesi["rasio_per_1000_bar"] = (per_sesi["sum"] / per_sesi["size"] * 1000).round(3)
per_sesi = per_sesi.reindex([s for s in SESSION_ORDER if s in per_sesi.index])
print(per_sesi.to_string())
print()
print("=== jumlah swing (semua k/sisi) per tahun ===")
per_tahun = A.assign(swing=swing_any).groupby("year")["swing"].agg(["sum", "size"])
per_tahun["rasio_per_1000_bar"] = (per_tahun["sum"] / per_tahun["size"] * 1000).round(3)
print(per_tahun.to_string())

# --- D6 (frekuensi swing per hari) + D7 (waktu tahan median antar swing) ---------
BAR_MINUTES = 5  # protokol Q5 terkunci di M5 (Kontrak 00)
HARI_BERBAR = int(A["broker_day"].nunique())
print()
print(f"hari broker berbar di stratum A = {HARI_BERBAR:,}")

freq_rows = []
hold_rows = []
for nama, mask in SWING_MASKS.items():
    indeks = np.flatnonzero(mask)
    jarak = np.diff(indeks)
    freq_rows.append(
        {
            "kombinasi": nama,
            "n_swing": len(indeks),
            "swing_per_hari": len(indeks) / HARI_BERBAR,
            "swing_per_1000_bar": len(indeks) / len(A) * 1000,
        }
    )
    hold_rows.append(
        {
            "kombinasi": nama,
            "n_jarak": int(len(jarak)),
            "tahan_median_bar": float(np.median(jarak)),
            "tahan_p90_bar": float(np.percentile(jarak, 90)),
            "tahan_median_menit": float(np.median(jarak)) * BAR_MINUTES,
        }
    )

SWING_FREQ = pd.DataFrame(freq_rows).set_index("kombinasi")
SWING_HOLD = pd.DataFrame(hold_rows).set_index("kombinasi")
print()
print("=== D6: frekuensi swing per HARI (stratum A) ===")
print(SWING_FREQ.round(3).to_string())
print()
per_hari = A.assign(swing=swing_any).groupby("broker_day")["swing"].sum()
print("sebaran swing gabungan per hari broker:")
print(per_hari.describe(percentiles=[0.1, 0.5, 0.9]).round(2).to_string())
print()
print("=== D7: waktu tahan median antar swing (jarak antar indeks fraktal) ===")
print(SWING_HOLD.round(3).to_string())
print()

# Holding per sesi (gabungan): sesi diambil dari swing AWAL tiap pasangan.
indeks_gab = np.flatnonzero(swing_any)
sesi_awal = A["session_label"].to_numpy()[indeks_gab[:-1]]
HOLD_SESI = (
    pd.DataFrame({"sesi": sesi_awal, "jarak_bar": np.diff(indeks_gab)})
    .groupby("sesi")["jarak_bar"]
    .agg(["size", "median"])
    .reindex([s for s in SESSION_ORDER if s in set(sesi_awal)])
)
HOLD_SESI["median_menit"] = HOLD_SESI["median"] * BAR_MINUTES
print("waktu tahan median per sesi (gabungan, bar -> menit):")
print(HOLD_SESI.round(2).to_string())
print()
print("ATURAN: D7 = jarak antar indeks fraktal (bukan durasi posisi, bukan P&L).")'''
)

md(
    """## 2b. Zona BoJ 150/155/160 - eksposur deskriptif (BUKAN event-study)

RULES §18.14 dan rancangan §2 menandai **zona waspada intervensi BoJ** pada harga
150/155/160. Sel ini **hanya menghitung eksposur**: berapa bar yang menyentuh/mendekati level
itu, di tahun mana, dan di sesi mana. **Tidak ada** return setelah event, tidak ada reaksi,
tidak ada klaim - itu event-study dan **di luar scope EDA** (putusan Architect atas D12).

Dua ukuran dilaporkan, tanpa menyembunyikan pilihan:
1. **Touch eksak** - bar yang rentangnya memuat level persis (`low <= L <= high`): aturan touch
   yang **sama** dengan Q6.
2. **Eksposur band** - bar yang rentangnya bersinggungan dengan `[L - w, L + w]` untuk
   setengah-lebar `w` yang **dinyatakan**: 10, 25, dan 50 pip. Tidak ada satu `w` tunggal yang
   disembunyikan; kalau kelak dipakai sebagai filter, `w`-nya harus dipilih eksplisit.
"""
)

code(
    '''"""Eksposur deskriptif zona BoJ 150/155/160 (M5, stratum A) - TANPA event-study."""
BOJ_LEVELS = (150.0, 155.0, 160.0)
BOJ_BAND_HALF_PIP = (10, 25, 50)

boj_low = A["low"].to_numpy(dtype="float64")
boj_high = A["high"].to_numpy(dtype="float64")
boj_tahun = A["year"].to_numpy()
boj_sesi = A["session_label"].to_numpy()
boj_hari = A["broker_day"].to_numpy()

BOJ_ROWS = []
for level in BOJ_LEVELS:
    sentuh = (boj_low <= level) & (boj_high >= level)
    baris = {
        "level": level,
        "n_touch": int(sentuh.sum()),
        "pct_bar_touch": float(sentuh.mean()) * 100,
        "n_hari_touch": int(pd.Series(boj_hari[sentuh]).nunique()),
    }
    for half_pip in BOJ_BAND_HALF_PIP:
        half = half_pip * PIP_SIZE
        band = (boj_low <= level + half) & (boj_high >= level - half)
        baris[f"n_band_{half_pip}pip"] = int(band.sum())
    baris["tahun_touch"] = ",".join(str(y) for y in sorted(set(boj_tahun[sentuh].tolist()))) or "-"
    BOJ_ROWS.append(baris)

BOJ_EXPOSURE = pd.DataFrame(BOJ_ROWS).set_index("level")
pd.set_option("display.width", 220)
print("=== D12 (nb04): eksposur zona BoJ, M5 stratum A, deskriptif ===")
print(BOJ_EXPOSURE.to_string())
print()

BOJ_YEAR_ROWS = []
for level in BOJ_LEVELS:
    sentuh = (boj_low <= level) & (boj_high >= level)
    half = 25 * PIP_SIZE
    band = (boj_low <= level + half) & (boj_high >= level - half)
    for tahun in YEARS:
        mask_tahun = boj_tahun == tahun
        BOJ_YEAR_ROWS.append(
            {
                "level": level,
                "tahun": tahun,
                "n_touch": int((sentuh & mask_tahun).sum()),
                "n_band_25pip": int((band & mask_tahun).sum()),
            }
        )
BOJ_YEAR = pd.DataFrame(BOJ_YEAR_ROWS).set_index(["level", "tahun"])
print("=== eksposur per tahun (touch eksak vs band 25 pip) ===")
print(BOJ_YEAR.to_string())
print()

BOJ_SESI = pd.DataFrame(
    {
        str(level): [
            int(((boj_low <= level) & (boj_high >= level) & (boj_sesi == label)).sum())
            for label in SESSION_ORDER
        ]
        for level in BOJ_LEVELS
    },
    index=SESSION_ORDER,
)
print("=== touch eksak per sesi (label eksklusif primer) ===")
print(BOJ_SESI.to_string())
print()
print("DESKRIPTIF SAJA: tidak ada return pasca-event, tidak ada reaksi, tidak ada klaim.")
print("Sentuhan di sekitar rilis berita BoJ ikut terhitung (kalender berita di luar scope).")'''
)

md(
    """## 3. Q6 — Event level (round-number + prior-day H/L)

Level yang diuji sesuai Kontrak 00:
- **Round-number:** grid kelipatan 0,50; **xx.00 = primer**, xx.50 = granularitas alternatif.
- **Prior-day high/low:** primer = bucket **D1 kalender-broker**; sekunder = **hari-UTC**.
  Keduanya dilaporkan (putusan Architect R3: kerja level-hari dikunci pada tanggal-broker).
- **R1 (Lampiran A1):** agreement **literal** primer-vs-sekunder **tidak akan pernah tercapai** — offset struktural hari-UTC vs hari-broker = **−1**; DILARANG menggeser data agar "sepakat".
- **R2 (Lampiran A1):** hanya divergensi **MELEBIHI** geseran struktural itu yang dihitung sebagai temuan (sensitivitas), bukan selisih mentah.

Touch: bar M5 dengan `low <= L <= high`. Sisi datang: `sign(close_{t-1} - L)`; bar dengan
`close_{t-1} == L` dilewati."""
)

code(
    '''"""Bangun event touch untuk round-number dan prior-day H/L."""


def round_level_events(a: pd.DataFrame, grid: float, hanya_kelipatan: bool) -> pd.DataFrame:
    """Event touch untuk level round-number pada satu grid.

    Args:
        a: Frame stratum A.
        grid: Jarak antar kandidat level (0.5).
        hanya_kelipatan: True -> hanya kelipatan 1.00 (xx.00 primer);
            False -> hanya setengahnya (xx.50 alternatif).

    Returns:
        DataFrame event dengan kolom row, level, close_prev, theta, direction.
    """
    low = a["low"].to_numpy(dtype="float64")
    high = a["high"].to_numpy(dtype="float64")
    close_prev = a["close"].shift(1).to_numpy(dtype="float64")
    theta = a["theta"].to_numpy(dtype="float64")
    rows_idx, levels = [], []
    n_lo = np.ceil(low / grid)
    n_hi = np.floor(high / grid)
    for i in np.nonzero(n_hi >= n_lo)[0]:
        for n in range(int(n_lo[i]), int(n_hi[i]) + 1):
            if (n % 2 == 0) != hanya_kelipatan:
                continue
            rows_idx.append(i)
            levels.append(n * grid)
    ev = pd.DataFrame({"row": rows_idx, "level": levels})
    ev["close_prev"] = close_prev[ev["row"]] if len(ev) else []
    ev["theta"] = theta[ev["row"]] if len(ev) else []
    return ev


def prior_day_hl_events(a: pd.DataFrame, day_col: str, shift_fn=None) -> pd.DataFrame:
    """Event touch prior-day high dan low untuk satu definisi hari.

    Args:
        a: Frame stratum A.
        day_col: 'broker_day' (primer) atau 'utc_day' (sekunder).
        shift_fn: Opsional, fungsi (daily, day_col) -> daily yang menggeser
            prev_high/prev_low (dipakai kontrol placebo 2).

    Returns:
        DataFrame event dengan kolom row, level, jenis, day, close_prev, theta.
    """
    daily = a.groupby(day_col).agg(d_high=("high", "max"), d_low=("low", "min")).reset_index()
    daily["prev_high"] = daily["d_high"].shift(1)
    daily["prev_low"] = daily["d_low"].shift(1)
    if shift_fn is not None:
        daily = shift_fn(daily, day_col)
    m = a[[day_col]].merge(daily, on=day_col, how="left")
    close_prev = a["close"].shift(1).to_numpy(dtype="float64")
    theta = a["theta"].to_numpy(dtype="float64")
    low = a["low"].to_numpy(dtype="float64")
    high = a["high"].to_numpy(dtype="float64")
    out = []
    for jenis, kolom in (("high", "prev_high"), ("low", "prev_low")):
        lvl = m[kolom].to_numpy(dtype="float64")
        hit = np.isfinite(lvl) & (low <= lvl) & (lvl <= high)
        idx = np.nonzero(hit)[0]
        out.append(
            pd.DataFrame(
                {
                    "row": idx,
                    "level": lvl[idx],
                    "jenis": jenis,
                    "day": a[day_col].to_numpy()[idx],
                    "close_prev": close_prev[idx],
                    "theta": theta[idx],
                }
            )
        )
    return pd.concat(out, ignore_index=True)


EV_ROUND_PRIMARY = round_level_events(A, 0.5, hanya_kelipatan=True)
EV_ROUND_ALT = round_level_events(A, 0.5, hanya_kelipatan=False)
EV_HL_BROKER = prior_day_hl_events(A, "broker_day")
EV_HL_UTC = prior_day_hl_events(A, "utc_day")

# Buang event tanpa close_prev/theta valid dan tanpa sisi datang yang jelas.
def valid_events(ev: pd.DataFrame) -> pd.DataFrame:
    """Saring event yang siap diuji reaksinya.

    Args:
        ev: DataFrame event.

    Returns:
        Event dengan close_prev & theta finite, dan direction != 0.
    """
    if not len(ev):
        return ev.assign(direction=[])
    out = ev.copy()
    out["direction"] = np.sign(out["close_prev"] - out["level"])
    ok = (
        np.isfinite(out["close_prev"])
        & np.isfinite(out["theta"])
        & (out["theta"] > 0)
        & (out["direction"] != 0)
    )
    return out.loc[ok].reset_index(drop=True)


EV = {
    "round_xx00": valid_events(EV_ROUND_PRIMARY),
    "round_xx50": valid_events(EV_ROUND_ALT),
    "hl_broker": valid_events(EV_HL_BROKER),
    "hl_utc": valid_events(EV_HL_UTC),
    "jumlah_event_raw": {
        "round_xx00": len(EV_ROUND_PRIMARY),
        "round_xx50": len(EV_ROUND_ALT),
        "hl_broker": len(EV_HL_BROKER),
        "hl_utc": len(EV_HL_UTC),
    },
}

for nama, ev in EV.items():
    if nama == "jumlah_event_raw":
        continue
    print(f"  {nama:11s}: {len(ev):>7,} event siap diuji")
print()
print("event mentah:", EV["jumlah_event_raw"])
print()
print("agreement primer (broker) vs sekunder (UTC) untuk prior-day H/L:")
print(f"  event broker={len(EV['hl_broker']):,} | utc={len(EV['hl_utc']):,}")'''
)

md(
    """## 4. Mesin reaksi (first passage)

Untuk tiap event, `theta` **dibekukan** dari ATR(14) di bar `t-1` (anti look-ahead), lalu
dua ambang statis dibentuk relatif ke arah datang `d = sign(close_{t-1} - L)`:

- `through = L - d*theta` → harga menembus level (breakout, searah datang)
- `away    = L + d*theta` → harga menjauh dari level (reversal/bounce)

First passage dipindai pada bar `t+1 .. t+max(k)`. Klasifikasi per window `k`:
`away` → reversal; `through` → bukan; **satu bar memuat dua ambang → `tie`** (tidak bisa
ditentukan dari OHLC, dilaporkan terpisah dan **tidak** dihitung sebagai reversal);
tidak ada keduanya → `none`."""
)

code(
    '''"""First passage: klasifikasi away/through/tie/none per window k."""
LOW = A["low"].to_numpy(dtype="float64")
HIGH = A["high"].to_numpy(dtype="float64")
N_BARS = len(A)
MAX_K = max(REACTION_WINDOWS_BARS)


def first_passage(row: int, level: float, theta: float, direction: float) -> dict[int, int]:
    """Cari indeks first passage untuk through dan away.

    Args:
        row: Indeks bar event.
        level: Level yang disentuh.
        theta: Jarak ambang (dibekukan dari ATR t-1).
        direction: sign(close_{t-1} - level).

    Returns:
        Dict dengan 'through' dan 'away' berisi indeks bar (1..MAX_K) atau None.
    """
    through_price = level - direction * theta
    away_price = level + direction * theta
    res = {"through": None, "away": None}
    stop = min(row + MAX_K, N_BARS - 1)
    for j in range(row + 1, stop + 1):
        lo = LOW[j]
        hi = HIGH[j]
        if res["through"] is None and lo <= through_price <= hi:
            res["through"] = j - row
        if res["away"] is None and lo <= away_price <= hi:
            res["away"] = j - row
        if res["through"] is not None and res["away"] is not None:
            break
    return res


def classify(events: pd.DataFrame) -> pd.DataFrame:
    """Klasifikasi reaksi per window k untuk seluruh event.

    Args:
        events: DataFrame event valid.

    Returns:
        DataFrame dengan kolom status_k<k> berisi away/through/tie/none.
    """
    if not len(events):
        return events.assign(**{f"status_k{k}": [] for k in REACTION_WINDOWS_BARS})
    status = {k: [] for k in REACTION_WINDOWS_BARS}
    for row, level, theta, direction in zip(
        events["row"].to_numpy(),
        events["level"].to_numpy(dtype="float64"),
        events["theta"].to_numpy(dtype="float64"),
        events["direction"].to_numpy(dtype="float64"),
        strict=True,
    ):
        fp = first_passage(int(row), float(level), float(theta), float(direction))
        for k in REACTION_WINDOWS_BARS:
            a = fp["away"]
            t = fp["through"]
            a_hit = a is not None and a <= k
            t_hit = t is not None and t <= k
            if a_hit and t_hit:
                status[k].append("tie" if a == t else ("away" if a < t else "through"))
            elif a_hit:
                status[k].append("away")
            elif t_hit:
                status[k].append("through")
            else:
                status[k].append("none")
    out = events.copy()
    for k in REACTION_WINDOWS_BARS:
        out[f"status_k{k}"] = status[k]
    return out


REAL = {nama: classify(ev) for nama, ev in EV.items() if nama != "jumlah_event_raw"}


def hit_rate_table(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Ringkas hit-rate reversal (away) per level x window.

    Args:
        data: Dict nama-level -> DataFrame terklasifikasi.

    Returns:
        DataFrame dengan kolom away/through/tie/none/hit_rate per window.
    """
    rows = []
    for nama, frame in data.items():
        for k in REACTION_WINDOWS_BARS:
            s = frame[f"status_k{k}"]
            away = int((s == "away").sum())
            through = int((s == "through").sum())
            tie = int((s == "tie").sum())
            none = int((s == "none").sum())
            denom = away + through
            rows.append(
                {
                    "level": nama,
                    "k": k,
                    "n": len(frame),
                    "away": away,
                    "through": through,
                    "tie": tie,
                    "none": none,
                    "hit_rate": (away / denom) if denom else np.nan,
                }
            )
    return pd.DataFrame(rows)


REAL_HR = hit_rate_table(REAL)
pd.set_option("display.width", 220)
print("=== Q6: hit-rate reversal LEVEL NYATA (stratum A) ===")
print(REAL_HR.to_string(index=False, float_format=lambda v: f"{v:.4f}"))'''
)

md(
    """## 5. Kontrol placebo (PERSIS preregistrasi — dua-duanya, protokol identik)

1. **Level acak ber-offset:** `L' = L + U(5, 25) pip` dengan **tanda acak per event**;
   jumlah event sama.
2. **Prior-day H/L digeser:** tiap H/L digeser `U(0.25, 1.00) x ATR(14) harian` dengan
   tanda acak independen per level per hari.

Seed tetap `PLACEBO_SEED`, tidak ada penggantian seed.

### Catatan interpretasi yang dinyatakan terbuka (butuh konfirmasi Klenz)

Protokol di nb00 menulis pergeseran **level**, tanpa menyatakan eksplisit bahwa level
placebo harus **benar-benar disentuh** harga. Implementasi literal (memakai bar event yang
sama, level digeser) menghasilkan hit-rate placebo **0,89-0,95 vs nyata 0,47** karena level
yang digeser sering jatuh **di luar rentang bar**, sehingga `away` terpicu seketika. Itu
artefak geometri, bukan kontrol.

Yang dipakai di sini: **semua parameter preregistrasi dipertahankan persis** (rentang
offset 5-25 pip, tanda acak per event, ATR harian 0,25-1,00, seed 20261006), tetapi tiap
level placebo diwajibkan **genuinely disentuh** - placebo 1 mencari bar terdekat (maju
sampai `MAX_K`) yang menyentuh `L'`, placebo 2 membangun H/L yang sudah digeser lalu
mendeteksi touch-nya dengan cara yang sama seperti level nyata. Ini **interpretasi**, bukan
tuning parameter, dan tetap perlu dikonfirmasi Klenz."""
)

code(
    '''"""Bangun kedua kontrol placebo sesuai preregistrasi."""


def placebo_random_offset(events: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Placebo 1: level digeser U(offset) pip dengan tanda acak per event.

    PENTING - interpretasi protokol (lihat catatan di markdown): level placebo
    HARUS benar-benar disentuh harga, kalau tidak event-nya bukan event touch
    dan "away" terpicu seketika hanya karena level berada di luar rentang bar.
    Implementasi pertama menghasilkan hit-rate placebo 0,89 vs nyata 0,47 - itu
    artefak, bukan kontrol. Karena itu tiap level placebo dicari bar terdekat
    (mulai bar event, maju sampai MAX_K) yang genuinely menyentuhnya.

    Args:
        events: Event level nyata.
        rng: Generator numpy ber-seed PLACEBO_SEED.

    Returns:
        Event placebo dengan level ter-offset dan bar yang benar-benar menyentuhnya.
    """
    lo, hi = PLACEBO_RANDOM_OFFSET_PIPS
    besar = rng.uniform(lo, hi, size=len(events))
    tanda = rng.choice([-1.0, 1.0], size=len(events))
    target = events["level"].to_numpy(dtype="float64") + tanda * besar * PIP_SIZE
    rows = events["row"].to_numpy(dtype=np.int64)
    close_prev_arr = A["close"].shift(1).to_numpy(dtype="float64")
    theta_arr = A["theta"].to_numpy(dtype="float64")
    keep_row, keep_level = [], []
    for i, lvl in zip(rows, target, strict=True):
        for j in range(int(i), min(int(i) + MAX_K, N_BARS - 1) + 1):
            if LOW[j] <= lvl <= HIGH[j]:
                keep_row.append(j)
                keep_level.append(lvl)
                break
    out = pd.DataFrame({"row": keep_row, "level": keep_level})
    out["close_prev"] = close_prev_arr[out["row"]] if len(out) else []
    out["theta"] = theta_arr[out["row"]] if len(out) else []
    out["direction"] = np.sign(out["close_prev"] - out["level"])
    return out.loc[out["direction"] != 0].reset_index(drop=True)


def atr_map(day_col: str) -> pd.Series:
    """ATR(14) D1 per hari, mengikuti definisi hari yang diminta.

    Placebo 2 untuk varian UTC WAJIB memakai peta UTC; memakai peta broker_day
    membuat seluruh ATR NaN dan placebo-nya kosong (bug saat eksekusi pertama).

    Args:
        day_col: 'broker_day' atau 'utc_day'.

    Returns:
        Series ATR(14) D1 terindeks hari.
    """
    key = d1["wall"].dt.normalize() if day_col == "broker_day" else d1["utc"].dt.normalize()
    return d1.assign(_day=key).drop_duplicates(subset="_day", keep="last").set_index("_day")["atr14_d1"]


def make_hl_shifter(day_col: str, rng: np.random.Generator):
    """Buat fungsi penggeser prev-day H/L sesuai preregistrasi placebo 2.

    Args:
        day_col: Definisi hari yang dipakai event.
        rng: Generator numpy ber-seed PLACEBO_SEED.

    Returns:
        Fungsi (daily, day_col) -> daily dengan prev_high/prev_low ter-geser.
    """
    atr = atr_map(day_col)

    def _shifter(daily: pd.DataFrame, _day_col: str) -> pd.DataFrame:
        """Geser prev_high/prev_low dengan tanda acak independen per level per hari."""
        lo, hi = PLACEBO_PRIOR_HL_SHIFT_ATR
        out = daily.copy()
        a = out[_day_col].map(atr).to_numpy(dtype="float64")
        for kolom in ("prev_high", "prev_low"):
            tanda = rng.choice([-1.0, 1.0], size=len(out))
            besar = rng.uniform(lo, hi, size=len(out)) * a
            out[kolom] = out[kolom] + tanda * besar
        return out

    return _shifter


RNG_PLACEBO_RANDOM = np.random.default_rng(PLACEBO_SEED)
RNG_PLACEBO_HL = np.random.default_rng(PLACEBO_SEED)

# Placebo 1 hanya untuk level yang punya "L" tunggal.
PLACEBO_RANDOM_SRC = ("round_xx00", "hl_broker")
PLACEBO_HL_SRC = ("hl_broker", "hl_utc")

PLACEBO_RANDOM = {
    nama: classify(placebo_random_offset(REAL[nama], RNG_PLACEBO_RANDOM))
    for nama in PLACEBO_RANDOM_SRC
}
# Placebo 2 dibangun sebagai event touch dari H/L yang SUDAH digeser - identik
# protokolnya dengan level nyata, hanya levelnya yang diacak.
PLACEBO_HL = {
    nama: classify(valid_events(prior_day_hl_events(A, day_col, make_hl_shifter(day_col, RNG_PLACEBO_HL))))
    for nama, day_col in (("hl_broker", "broker_day"), ("hl_utc", "utc_day"))
}

print("retensi event placebo 1 (placebo / nyata):")
for nama in PLACEBO_RANDOM_SRC:
    rasio = len(PLACEBO_RANDOM[nama]) / max(1, len(REAL[nama]))
    print(f"  {nama:11s}: {len(PLACEBO_RANDOM[nama]):,} / {len(REAL[nama]):,} = {rasio:.3f}")
print("jumlah event placebo 2:")
for nama in PLACEBO_HL:
    print(f"  {nama:11s}: {len(PLACEBO_HL[nama]):,}")

print("=== PLACEBO 1 (level digeser U(5,25) pip, tanda acak per event) ===")
print(hit_rate_table(PLACEBO_RANDOM).to_string(index=False, float_format=lambda v: f"{v:.4f}"))
print()
print("=== PLACEBO 2 (prior-day H/L digeser U(0.25,1.00) x ATR D1) ===")
print(hit_rate_table(PLACEBO_HL).to_string(index=False, float_format=lambda v: f"{v:.4f}"))'''
)

md(
    """## 6. Inferensi — bootstrap day-cluster

CI persentil 95% via **10.000 resample**, unit resample = **hari perdagangan** (day-cluster,
menghormati dependensi intraday). Ini yang membuat pembandingan nyata-vs-placebo tidak
mengklaim signifikansi dari bar yang saling bergantung."""
)

code(
    '''"""Bootstrap day-cluster untuk hit-rate reversal tiap level dan window."""


def day_cluster_ci(frame: pd.DataFrame, k: int, rng: np.random.Generator) -> dict[str, float]:
    """CI persentil 95% hit-rate reversal dengan resample per hari perdagangan.

    Args:
        frame: DataFrame terklasifikasi (punya kolom day & status_k{k}).
        k: Window reaksi.
        rng: Generator numpy ber-seed PLACEBO_SEED.

    Returns:
        Dict berisi hit_rate, ci_low, ci_high, n_hari.
    """
    status = frame[f"status_k{k}"]
    resolved = status.isin(["away", "through"])
    if not resolved.any():
        return {"hit_rate": np.nan, "ci_low": np.nan, "ci_high": np.nan, "n_hari": 0}
    per_day = (
        frame.loc[resolved]
        .assign(away=(status[resolved] == "away").astype("int64"))
        .groupby("day")["away"]
        .agg(["sum", "size"])
    )
    succ = per_day["sum"].to_numpy(dtype="float64")
    tri = per_day["size"].to_numpy(dtype="float64")
    n_days = len(per_day)
    idx = rng.integers(0, n_days, size=(BOOTSTRAP_RESAMPLES, n_days))
    s = succ[idx].sum(axis=1)
    t = tri[idx].sum(axis=1)
    rates = np.divide(s, t, out=np.full_like(s, np.nan), where=t > 0)
    rates = rates[np.isfinite(rates)]
    return {
        "hit_rate": float(succ.sum() / tri.sum()),
        "ci_low": float(np.percentile(rates, 2.5)),
        "ci_high": float(np.percentile(rates, 97.5)),
        "n_hari": n_days,
    }


def ci_table(data: dict[str, pd.DataFrame], k: int, label: str) -> pd.DataFrame:
    """Tabel CI day-cluster untuk satu window dan sekumpulan level.

    Args:
        data: Dict nama-level -> frame (harus punya kolom day).
        k: Window reaksi.
        label: Label kontrol ('nyata'/'placebo').

    Returns:
        DataFrame dengan hit_rate + CI per level.
    """
    rng = np.random.default_rng(PLACEBO_SEED)
    rows = []
    for nama, frame in data.items():
        if "day" not in frame.columns:
            continue
        res = day_cluster_ci(frame, k, rng)
        rows.append({"kontrol": label, "level": nama, "k": k, **res})
    return pd.DataFrame(rows)


# Kolom 'day' diperlukan untuk day-cluster; round-number tidak punya hari sendiri,
# jadi memakai broker_day dari bar event (bukan hari level).
for _nama, frame in list(REAL.items()) + list(PLACEBO_RANDOM.items()) + list(PLACEBO_HL.items()):
    if "day" not in frame.columns and len(frame):
        frame["day"] = A["broker_day"].to_numpy()[frame["row"].to_numpy()]

CI_ROWS = []
K_PRIMER = REACTION_WINDOW_PRIMARY
for nama, frame in REAL.items():
    CI_ROWS.append(ci_table({nama: frame}, K_PRIMER, "nyata"))
for nama, frame in PLACEBO_RANDOM.items():
    CI_ROWS.append(ci_table({nama: frame}, K_PRIMER, "placebo_acak"))
for nama, frame in PLACEBO_HL.items():
    CI_ROWS.append(ci_table({nama: frame}, K_PRIMER, "placebo_hl"))

CI = pd.concat([r for r in CI_ROWS if len(r)], ignore_index=True)
print(f"=== CI persentil 95% (day-cluster, {BOOTSTRAP_RESAMPLES:,} resample, k={K_PRIMER}) ===")
print(CI.to_string(index=False, float_format=lambda v: f"{v:.4f}"))'''
)

md(
    """## 7. Assertion penutup + ringkasan

Assertion di bawah adalah fakta terukur. Yang paling penting: **protokol placebo identik
dengan preregistrasi nb00**, dan placebo benar-benar dibangun dengan jumlah event yang
sebanding."""
)

code(
    '''"""Assertion penutup Q5/Q6 + placebo."""
placebo_acak_ok = all(len(PLACEBO_RANDOM[n]) > 0 for n in PLACEBO_RANDOM)
placebo_hl_ok = all(len(PLACEBO_HL[n]) > 0 for n in PLACEBO_HL)
sama_protokol = not selisih

checks = [
    ("Definisi sesi == Notebook 00", session_fingerprint() == EXPECTED_FINGERPRINT),
    ("Protokol placebo identik preregistrasi nb00", sama_protokol),
    ("Seed placebo == 20261006", PLACEBO_SEED == 20261006),
    ("Timeframe protokol == M5", PLACEBO_TIMEFRAME == "M5"),
    ("Window primer ada di daftar window", REACTION_WINDOW_PRIMARY in REACTION_WINDOWS_BARS),
    ("Fraktal dihitung untuk k=3 dan k=5", set(SWINGS["k"]) == {3, 5}),
    ("Empat sisi/kombinasi swing dilaporkan", len(SWINGS) == 4),
    ("Setiap kombinasi swing punya swing > 0", bool((SWINGS["n_swing"] > 0).all())),
    ("Stratum A berjumlah sama dengan nb03 (M5)", len(A) == 227_568),
    (
        "Stratum A tidak punya theta NaN (warmup ATR habis di stratum B)",
        int(A["theta"].isna().sum()) == 0,
    ),
    ("Round-number xx.00 dan xx.50 terdeteksi", len(EV["round_xx00"]) > 0 and len(EV["round_xx50"]) > 0),
    ("Prior-day H/L broker dan UTC terdeteksi", len(EV["hl_broker"]) > 0 and len(EV["hl_utc"]) > 0),
    ("Placebo 1 tidak kosong (event touch genuine)", placebo_acak_ok),
    ("Placebo 2 tidak kosong untuk broker DAN UTC", placebo_hl_ok),
    ("Placebo 2 dibangun untuk H/L broker dan UTC", set(PLACEBO_HL) == set(PLACEBO_HL_SRC)),
    (
        "Placebo bukan artefak (hit-rate tidak >0,95 di semua level)",
        bool((hit_rate_table(PLACEBO_RANDOM)["hit_rate"] < 0.95).all()),
    ),
    ("Tie dilaporkan terpisah (tidak dihitung reversal)", {"tie"} <= set(REAL_HR.columns)),
    ("Hit-rate nyata dan placebo sama-sama terhitung", bool(REAL_HR["hit_rate"].notna().any() and CI["hit_rate"].notna().any())),
    ("CI tidak runtuh (ci_low < ci_high)", bool((CI["ci_low"] < CI["ci_high"]).all())),
    ("Semua baris CI punya >= 30 hari", bool((CI["n_hari"] >= 30).all())),
    ("D6: frekuensi per hari dihitung untuk 5 kombinasi", len(SWING_FREQ) == 5),
    (
        "D6: tiap kombinasi punya swing dan hari berbar > 0",
        bool((SWING_FREQ["n_swing"] > 0).all()) and HARI_BERBAR > 0,
    ),
    ("D6: swing gabungan per hari > 0", bool(float(per_hari.mean()) > 0)),
    (
        "D7: waktu tahan median > 0 dan finite di semua kombinasi",
        bool(np.isfinite(SWING_HOLD["tahan_median_bar"]).all())
        and bool((SWING_HOLD["tahan_median_bar"] > 0).all()),
    ),
    ("D7: holding per sesi terisi (>= 3 sesi)", len(HOLD_SESI) >= 3),
    ("D12-BoJ: 3 level dieksposur", len(BOJ_EXPOSURE) == 3),
    (
        "D12-BoJ: band memuat touch dan naik monoton dengan lebar",
        bool((BOJ_EXPOSURE["n_band_10pip"] >= BOJ_EXPOSURE["n_touch"]).all())
        and bool((BOJ_EXPOSURE["n_band_25pip"] >= BOJ_EXPOSURE["n_band_10pip"]).all())
        and bool((BOJ_EXPOSURE["n_band_50pip"] >= BOJ_EXPOSURE["n_band_25pip"]).all()),
    ),
    ("D12-BoJ: minimal satu level tersentuh (tidak vakum)", int(BOJ_EXPOSURE["n_touch"].sum()) > 0),
    ("D12-BoJ: tabel per tahun lengkap (3 level x 4 tahun)", len(BOJ_YEAR) == 12),
    (
        "D12-BoJ: tidak ada kolom pasca-event (bukan event-study)",
        not any("return" in kolom or "reaksi" in kolom for kolom in BOJ_EXPOSURE.columns),
    ),
]

for label, passed in checks:
    print(f"{'PASS' if passed else 'GAGAL'} {label}")

failed = [label for label, passed in checks if not passed]
assert not failed, f"assertion gagal: {failed}"
print()
print(f"RINGKASAN: {len(checks) - len(failed)}/{len(checks)} assertion PASS untuk Q5/Q6/placebo.")

print()
print("=== PERBANDINGAN NYATA vs PLACEBO (k primer) ===")
banding = CI.pivot_table(index="level", columns="kontrol", values="hit_rate")
print(banding.to_string(float_format=lambda v: f"{v:.4f}"))'''
)

md(
    """## Ringkasan hasil dan batasnya

**Yang dijawab:** struktur swing M5 (k=3/k=5, ukuran dalam ATR), **frekuensi swing per hari
(D6)**, **waktu tahan median antar swing (D7)**, **eksposur deskriptif zona BoJ 150/155/160
(D12)**, dan apakah level (round-number xx.00/xx.50, prior-day H/L broker/UTC) menunjukkan
reaksi reversal yang **melampaui** kontrol placebo.

### Angka kunci (hasil eksekusi, stratum A)

| Metrik | nilai |
|---|---|
| swing k=3 high / low | 20.169 / 20.314 |
| swing k=5 high / low | 12.787 / 13.070 |
| ukuran median (satuan ATR) | 0,648 / 0,722 / 0,667 / 0,779 |
| **D6** swing gabungan per hari | **48,74** (median 49; p10 43; p90 54; min 37; maks 61; 825 hari berbar) |
| **D7** tahan median per kombinasi | 10 bar = 50 menit (k=3); 15 bar = 75 menit (k=5) |
| **D7** tahan median gabungan | 5 bar = 25 menit (jarak antar tanda fraktal berurutan) |
| **D12** touch eksak BoJ 150 / 155 / 160 | 728 / 518 / 151 bar (53 / 51 / 20 hari) |
| **D12** eksposur band 25 pip | 8.474 / 5.770 / 3.587 bar |

### Temuan penting

1. **D7 punya dua wajah, keduanya dilaporkan.** Jarak antar fraktal **sejenis** mengikuti
   `k` (10 bar untuk k=3; 15 bar untuk k=5), sedangkan **gabungan** hanya 5 bar karena
   didominasi pergantian high-low. Tabel per sesi memakai definisi gabungan sehingga
   mediannya seragam 5 bar (25 menit) - **keterbatasan yang dinyatakan**, bukan temuan sesi.
2. **Q6 tetap negatif dan tidak bergeser** karena penambahan D6/D7/D12: hit-rate nyata
   0,4694 (xx.00) / 0,4892 (xx.50) / 0,4799 (H/L broker) / 0,4905 (H/L UTC) vs placebo
   0,4989-0,5050, dan jumlah event nyata identik dengan eksekusi sebelumnya.
3. **D12 (zona BoJ) deskriptif:** touch terbanyak di sesi London (282/228/78) dan 2024
   mendominasi (150: 508; 155: 179; 160: 7), sedangkan 2026 hanya menyentuh 155 (153) dan
   160 (144); level 150 nol di 2026. **Tidak ada** return pasca-event yang dihitung.

**Aturan pembacaan (wajib):** bila hit-rate level nyata **tidak** melampaui placebo di luar
CI, maka **tidak ada klaim** bahwa level itu "dihormati" pasar. Level yang tampak bekerja
hanya boleh diangkat sebagai hipotesis bila ia memisahkan diri dari placebo.

**Yang TIDAK dijawab dan sengaja ditolak:**
- Tidak ada P&L, equity, atau pemilihan metode.
- Tidak ada klaim Fibonacci: hanya boleh diuji dengan protokol placebo identik ini, dan
  tidak diuji di notebook ini.
- **Kalender berita di luar scope** → reaksi di sekitar rilis berita ikut terhitung.
- Fraktal baru terkonfirmasi `k` bar setelah terbentuk → Q5 deskriptif, bukan fitur real-time.
- Tidak ada p-value tanpa effect-size (AGENTS §20/§21).
- **D7 bukan durasi posisi**: yang diukur jarak antar indeks fraktal, bukan waktu tahan
  trade, dan tidak ada P&L.
- **D12 setengah-lebar band (10/25/50 pip) adalah pilihan deskriptif** yang dinyatakan,
  bukan angka kontrak; dan zona BoJ **tidak** dianalisis sebagai event (tanpa return
  pasca-event) sesuai putusan Architect.

**STOP.** Laporan mini + self-audit adversarial, lalu tunggu review user sebelum notebook 05.
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
