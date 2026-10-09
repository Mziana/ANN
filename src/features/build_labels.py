"""Build H1-H3 daily labels on ONE grain: broker-day from the store.

DILARANG menjalankan backtest H2 (hanya pra-registrasi). H4/H5 tidak
divonis. H6+ tidak dibuat. Impor satu arah: modul ini imports
build_features, tidak ada import balik. Fungsi <=50 baris; modul <=400.

Grain tunggal (putusan C): `date_broker` dari `prepare_bars` store
(`broker_time_raw` -> wall clock); DILARANG rekonstruksi hari dari UTC (#21).

Alur kontrak (putusan Q2-b): drift + gap dari M15 sumber (jendela 16 bar
`is_london`; `m1_bars` < 15 non-tepi), rv via Q1(a) protokol §2; norm =
drift / atr_14_d1 + guard provenans (B): pembagi wajib identik deret
referensi store yang DIBACA ULANG dari file terpisah (DISIPLIN 9).
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.features.build_features import (
    FEATURES_DIR,
    daily_metrics,
    load_processed,
    prepare_bars,
    session_flags,
)
from src.utils.config import load_config

logger = logging.getLogger(__name__)

# Lokasi label output — terpisah dari store B1
LABELS_DIR = Path("data") / "labels"

# Ambang H1 (dari hipotesis_lock_v1.md, median stratum A)
RATIO_PATH_THRESHOLD = 0.0268
RANGE_ATR_THRESHOLD = 88.79

# TAU_2023 = hasil kalibrasi Q1(a), ditulis di protokol-H1-H2-H3.md §2. Span
# terkunci 2023-01-01..2023-12-31; label B (positif, hari-B) = 2023-01-01..
# 2023-06-30; label A = 2023-07-01..2023-12-31; Youden (maks sensitivitas +
# spesifisitas - 1) pada rv_score; AUC in-sample. DILARANG mengkalibrasi
# ulang pada span lain / memakai performa OOS.
TAU_2023 = 2.5951672079821496e-05
CALIB_AUC_2023 = 0.8173755150499336
CALIB_N_B = 111
CALIB_N_A = 129

# 19 hari anomali dari putusan F-1 butir 2
ANOMALY_WINDOWS = [
    ("2024-10-28", "2024-11-01"),
    ("2026-03-10", "2026-03-27"),
]

# Jendela London kontrak: 16 bar is_london pertama per broker-day.
# BLOKIR jendela hour_utc 8-12 (temuan re-audit #15).
LONDON_FIRST_N = 16

# Bucket M15 parsial: m1_bars < 15 (definisi Q3-a; audit F-2/B1).
M1_BARS_MIN = 15

# Transformasi label /20 (putusan Q4-ii; store tetap sum per B1-4).
RV_WINDOW_DAYS = 20

# Guard provenans ATR — toleransi eksplisit (putusan B butir 3).
ATR_PROVENANCE_RTOL = 1e-9
ATR_PROVENANCE_ATOL = 1e-9

# Smoke-bound kewajaran nilai; BUKAN bukti satuan (putusan B butir 2).
SMOKE_NORM_ABS_MAX = 1e3


def classify_day_label(daily: pd.DataFrame) -> pd.Series:
    """Klasifikasi hari ke label H1 (hipotesis_lock_v1.md, verbatim):
    trending = ratio_path > 0.0268 AND range_atr > 88.79; range = keduanya
    <= median A; normal = sisanya (ambang = median stratum A, lock).
    Metrik harian NaN -> "normal" (tidak ada None, acceptance putusan C).

    Args:
        daily: frame grain broker-day dengan kolom ratio_path, range_atr.
    Returns:
        Series index broker-day berisi label tanpa None.
    """

    out = {}
    for day, row in daily.iterrows():
        ratio = float(row["ratio_path"]) if pd.notna(row["ratio_path"]) else float("nan")
        atr_ratio = float(row["range_atr"]) if pd.notna(row["range_atr"]) else float("nan")
        if pd.isna(ratio) or pd.isna(atr_ratio):
            out[day] = "normal"
            continue
        if ratio > RATIO_PATH_THRESHOLD and atr_ratio > RANGE_ATR_THRESHOLD:
            out[day] = "trending"
        elif ratio <= RATIO_PATH_THRESHOLD and atr_ratio <= RANGE_ATR_THRESHOLD:
            out[day] = "range"
        else:
            out[day] = "normal"
    return pd.Series(out, name="day_label")


def _assert_atr_provenance(atr_used: pd.Series, atr_reference: pd.Series) -> None:
    """Guard provenans pembagi ATR (putusan B butir 3).

    Nilai tak bersaksi tentang satuan (1.0 / 88.79 / close-avg lolos nilai);
    yang diuji IDENTITAS pembagi terhadap deret referensi store yang
    dilewatkan eksplisit pemanggil dari SUMBER TERPISAH (DISIPLIN butir 9).
    Baseline LULUS; pembagi pengganti GAGAL.

    Args:
        atr_used: deret pembagi yang benar-benar dipakai membagi drift.
        atr_reference: deret `atr_14_d1` store, sumber terpisah dari used.
    Raises:
        AssertionError: bila pembagi menyimpang dari referensi.
    """

    used = pd.Series(atr_used).astype(float)
    ref = pd.Series(atr_reference).astype(float)
    common = used.dropna().index.intersection(ref.dropna().index)
    assert len(common) > 0, "atr_reference tidak punya satu pun titik banding"
    assert np.allclose(
        used.loc[common].to_numpy(),
        ref.loc[common].to_numpy(),
        rtol=ATR_PROVENANCE_RTOL,
        atol=ATR_PROVENANCE_ATOL,
    ), "pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) — putusan B"


def _assert_smoke_bounds(atr: pd.Series, norm: pd.Series) -> None:
    """Batas kewajaran nilai — BUKAN bukti satuan (putusan B butir 2).

    Klausa kewajaran: atr non-negatif dan |norm| < 1e3; keduanya TIDAK
    membuktikan satuan (88.79 lolos). Sabotase satuan dibuktikan lewat guard
    provenans, bukan lewat klausa ini.
    """
    negatif = "atr_14_d1 negatif (batas kewajaran, bukan bukti satuan)"
    ekstrem = "|london_drift_norm| >= 1e3 (batas kewajaran, bukan bukti satuan)"
    assert (atr.dropna() >= 0).all(), negatif
    assert (np.abs(norm.dropna()) < SMOKE_NORM_ABS_MAX).all(), ekstrem


def compute_london_drift_4h(
    m15: pd.DataFrame,
    daily: pd.DataFrame,
    atr_reference: pd.Series,
) -> pd.DataFrame:
    """Hitung dua kolom drift grain broker-day dari M15 sumber langsung.

    Grain = broker-day store (putusan C); jendela = 16 bar `is_london`
    pertama per broker-day (session_flags, DST-aware); drift = close
    terakhir - open pertama (satuan harga); norm = drift / atr_14_d1 dijaga
    `_assert_atr_provenance` terhadap `atr_reference` (putusan B).

    Args:
        m15: frame M15 dari load_processed (time, broker_time_raw, OHLC).
        daily: frame grain broker-day dari daily_metrics (kolom atr_14_d1).
        atr_reference: deret atr_14_d1 store, sumber terpisah dari daily.
    Returns:
        Frame index date_broker: london_drift_4h, london_drift_norm.
    Raises:
        AssertionError: hari broker tanpa bar London, atau provenans gagal.
    """
    bars = prepare_bars(m15, "M15", ("open", "close"))
    flags = session_flags(bars["utc"])
    london = bars[flags["is_london"].to_numpy()]
    window = london.groupby("broker_day", sort=True).head(LONDON_FIRST_N)
    first_open = window.groupby("broker_day", sort=True)["open"].first()
    last_close = window.groupby("broker_day", sort=True)["close"].last()
    drift = (last_close - first_open).reindex(daily.index)
    assert drift.notna().all(), "hari broker tanpa bar London — grain tidak lengkap"
    atr = daily["atr_14_d1"].reindex(drift.index)
    _assert_atr_provenance(atr, atr_reference)
    norm = drift / atr
    _assert_smoke_bounds(atr, norm)
    out = pd.DataFrame({"london_drift_4h": drift, "london_drift_norm": norm})
    out.index.name = "date_broker"
    return out


def compute_gap_f2_flag(m15: pd.DataFrame) -> pd.Series:
    """Flag hari yang punya bucket M15 parsial (gap M1).

    Residual F-2 #2; status BELUM DIUJI — materialitas H1/H5 belum teruji,
    eksklusi buta DILARANG. Bucket parsial = m1_bars < M1_BARS_MIN DAN
    bukan bucket pertama/terakhir hari-broker (mid-day); hari = 1 bila ada
    >=1 bucket mid-day parsial, else 0 (NaN/senyap DILARANG).

    Args:
        m15: frame M15 dari load_processed (memiliki m1_bars).
    Returns:
        Series index broker-day (date_broker), dtype int, nilai 0/1.
    """
    bars = prepare_bars(m15, "M15", ("m1_bars",))
    edges = (
        bars.groupby("broker_day").head(1).index.append(bars.groupby("broker_day").tail(1).index)
    )
    partial_midday = (bars["m1_bars"] < M1_BARS_MIN) & ~bars.index.isin(edges)
    flagged = partial_midday.groupby(bars["broker_day"]).any()
    days = pd.DatetimeIndex(bars["broker_day"].drop_duplicates().sort_values())
    out = flagged.reindex(days, fill_value=False).astype(int)
    out.index.name = "date_broker"
    return out.rename("gap_f2_flag")


def compute_rv_regime_flag(daily: pd.DataFrame) -> pd.Series:
    """Flag regime volatilitas tinggi (hasil kalibrasi Q1(a), protokol §2).

    rv_score = rv_roll_20d / RV_WINDOW_DAYS (mean, turunan label; store
    tetap sum per B1-4); flag = 1[rv_score > TAU_2023], TAU_2023 = ambang
    Youden span terkunci 2023 (B = Jan-Jun, A = Jul-Des). Hari warmup NaN
    dikecualikan dan berflag NaN — DILARANG default False.

    Args:
        daily: frame grain broker-day (memiliki rv_roll_20d).
    Returns:
        Series index broker-day, dtype float, nilai 0/1/NaN.
    """
    rv_score = daily["rv_roll_20d"] / RV_WINDOW_DAYS
    flag = pd.Series(np.nan, index=daily.index, dtype=float)
    known = rv_score.notna()
    flag[known] = (rv_score[known] > TAU_2023).astype(float)
    flag.index.name = "date_broker"
    return flag.rename("rv_regime_flag")


def quarantine_mask(daily: pd.DataFrame) -> pd.Series:
    """Mask 19 hari anomali (putusan F-1 butir 1-2: inklusi vs eksklusi).
    DILARANG memakai pola lain (mis. wall-open 00:00) sebagai predikat.

    Args:
        daily: frame grain broker-day (index = date_broker).
    Returns:
        Series index date_broker, dtype bool murni.
    """
    mask = pd.Series(False, index=daily.index, dtype=bool)
    for start, end in ANOMALY_WINDOWS:
        in_window = (daily.index >= pd.Timestamp(start)) & (daily.index <= pd.Timestamp(end))
        mask |= in_window
    mask.index.name = "date_broker"
    return mask.rename("quarantine_mask")


def register_h2_strategy() -> dict:
    """Pra-registrasi strategi H2 (ditulis, TIDAK dieksekusi — tanpa backtest).

    Jam 15 UTC, 1x/hari-broker, satuan harga JPY (protokol §1).
    """

    return {
        "name": "H2 M15 momentum",
        "entry": "Close > open di jam terakhir (jam 15 UTC), 1x per hari-broker",
        "exit": "Close < open di jam terakhir (jam 15 UTC)",
        "sl_atr": "1x ATR 14-hari (atr_14_d1, satuan harga JPY)",
        "tp": "2x ATR 14-hari (atr_14_d1, satuan harga JPY)",
        "biaya": "cost_basis mean sesi",
        "entry_time_utc": "15",
        "entry_frequency": "1x per broker-day",
        "price_unit": "JPY",
    }


def write_labels(
    labels: pd.DataFrame,
    name: str,
    out: Path | None = None,
    index: bool = True,
) -> Path:
    """Write labels ke parquet (membuat direktori bila perlu).

    Args:
        labels: frame label; index date_broker = row key baris (#20).
        name: nama file parquet.
        out: direktori tujuan (default LABELS_DIR).
        index: tulis index sebagai kolom identitas (default True).
    Returns:
        Path yang ditulis.
    """
    base = out if out is not None else LABELS_DIR
    path = Path(base) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    labels.to_parquet(path, index=index)
    logger.info("write_labels: %d bar -> %s", len(labels), path)
    return path


def _h2_trades_frame(symbol: str) -> pd.DataFrame:
    """Frame satu-baris spesifikasi H2 (tanpa kolom hasil — keputusan (c))."""
    strategy = register_h2_strategy()
    meta = {
        "symbol": symbol,
        "strategy": strategy["name"],
        "entry_rule": strategy["entry"],
        "exit_rule": strategy["exit"],
        "sl_atr": strategy["sl_atr"],
        "tp": strategy["tp"],
        "biaya": strategy["biaya"],
        "entry_time_utc": strategy["entry_time_utc"],
        "entry_frequency": strategy["entry_frequency"],
        "price_unit": strategy["price_unit"],
    }
    return pd.DataFrame([meta]).astype(str)


def _build_daily_labels(
    m15: pd.DataFrame,
    daily: pd.DataFrame,
    atr_reference: pd.Series,
) -> pd.DataFrame:
    """Kumpulkan label grain broker-day dari M15 sumber + frame daily.

    Args:
        m15: frame M15 sumber.
        daily: frame grain broker-day dari daily_metrics.
        atr_reference: deret atr_14_d1 dari store terpisah (putusan B-4).
    Returns:
        Frame index date_broker: day_label, london_drift_4h, london_drift_norm,
        gap_f2_flag, rv_regime_flag, quarantine_mask.
    """

    drift = compute_london_drift_4h(m15, daily, atr_reference)
    gap = compute_gap_f2_flag(m15).reindex(daily.index)
    assert gap.notna().all(), "gap_f2_flag kehilangan hari broker — grain campur"
    labels = pd.DataFrame(index=daily.index)
    labels.index.name = "date_broker"
    labels["day_label"] = classify_day_label(daily)
    labels["london_drift_4h"] = drift["london_drift_4h"]
    labels["london_drift_norm"] = drift["london_drift_norm"]
    labels["gap_f2_flag"] = gap.astype(int)
    labels["rv_regime_flag"] = compute_rv_regime_flag(daily)
    labels["quarantine_mask"] = quarantine_mask(daily).astype(bool)
    return labels


def _read_atr_reference_from_store(path: Path) -> pd.Series:
    """Baca ulang kolom atr_14_d1 dari store B1 — sumber TERPISAH pembagi.

    Putusan B-4 + DISIPLIN 9: DILARANG mengoper kolom dari frame yang sama
    (allclose(X, X) benar untuk setiap X). Store menyimpan nilai hari-D di
    baris hari-D+1 (attach anti-look-ahead daily.shift(1) build_features);
    shift(-1) = invers attach. Hari terakhir tak punya nilai lanjutan —
    pada produksi guard membandingkan 959/974 hari.

    Args:
        path: file parquet store fitur M15 (date_broker, atr_14_d1).
    Returns:
        Series atr_14_d1 index date_broker, dari file terpisah frame daily.
    """
    store = pd.read_parquet(path, columns=["date_broker", "atr_14_d1"])
    ref = store.groupby("date_broker")["atr_14_d1"].last().sort_index().shift(-1)
    ref.index.name = "date_broker"
    return ref.rename("atr_14_d1")


def main(argv: list[str] | None = None, out_dir: Path | None = None) -> None:
    """Build label store grain broker-day dari M15 sumber + daily.

    DILARANG backtest; D4 = tepat dua file nama kontrak; h2_trades tanpa
    kolom hasil (pnl/ev). Guard provenans (putusan B-4): atr_reference
    DIBACA ULANG dari file store B1 (`_read_atr_reference_from_store`) —
    sumber terpisah frame pembagi, bukan kolomnya (DISIPLIN 9). Baseline
    lolos; sabotase 1.0 / 88.79 / close-avg pada jalur produksi meledak —
    dibuktikan TestGuardProvenansJalurProduksi + harness batch-4 butir-1.
    """

    del argv
    config = load_config("data")
    symbol = config["mt5"]["symbol"]
    pip_size = float(config["spread"]["pip_size"][symbol])

    m15 = load_processed("M15", symbol)
    m1 = load_processed("M1", symbol)
    daily = daily_metrics(m1, m15, pip_size)

    # Referensi provenans: store B1 dibaca ulang — terpisah dari frame pembagi (B-4).
    store_path = FEATURES_DIR / "M15" / f"{symbol.lower()}_m15_features.parquet"
    atr_reference = _read_atr_reference_from_store(store_path)
    assert atr_reference.index.equals(daily.index), "hari store != hari label"
    atr_reference = atr_reference.reindex(daily.index)

    labels = _build_daily_labels(m15, daily, atr_reference)

    out = out_dir or LABELS_DIR
    day_path = write_labels(labels, f"{symbol.lower()}_day_labels.parquet", out=out)
    trades_path = write_labels(
        _h2_trades_frame(symbol), f"{symbol.lower()}_h2_trades.parquet", out=out, index=False
    )

    logger.info(
        "selesai: %d bar labels, day=%s, trades=%s",
        len(labels),
        day_path,
        trades_path,
    )


if __name__ == "__main__":
    main()
