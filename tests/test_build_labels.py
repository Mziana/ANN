"""Test build_labels.py — sintetis-in-memory, deterministik.

DILARANG menjalankan backtest di sini. Hanya test label builder.

Data sintetis dibangun sebagai frame M15 sumber dengan `broker_time_raw`
(epoch) EKSPLISIT, supaya grain broker-day (putusan C) benar-benar diuji —
bukan `utc.normalize()`. Offset broker dibuat dapat diubah agar hari-UTC dan
hari-broker bisa dibedakan.
"""

from __future__ import annotations

import ast
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import src.features.build_labels as bl
from src.features.build_labels import (
    CALIB_AUC_2023,
    CALIB_N_A,
    CALIB_N_B,
    LONDON_FIRST_N,
    M1_BARS_MIN,
    TAU_2023,
    _assert_atr_provenance,
    classify_day_label,
    compute_gap_f2_flag,
    compute_london_drift_4h,
    compute_rv_regime_flag,
    quarantine_mask,
    register_h2_strategy,
)

# Modul test ini sendiri: binding yang benar-benar dipanggil test di bawah.
# Mutasi WAJIB menambal nama di sini (bukan hanya atribut bl.<nama>), karena
# `from ... import` mengikat nama lokal sekali saat impor (temuan #25).
HERE = sys.modules[__name__]

# ==================== DATA SYNTHETIC ====================

LONDON_SUMMER_START_UTC_HOUR = 7  # local 8 di BST (UTC+1)
LONDON_WINTER_START_UTC_HOUR = 8  # local 8 di GMT (UTC+0)


def _raw_epoch(utc_iso: str, offset_hours: float = 0.0) -> int:
    """Epoch broker_time_raw: wall clock = utc + offset_hours."""
    wall = pd.Timestamp(utc_iso, tz="UTC") + pd.Timedelta(hours=offset_hours)
    return int(wall.timestamp())


def make_m15_bars(specs, offset_hours: float = 0.0) -> pd.DataFrame:
    """Bangun frame M15 sumber dari spesifikasi (utc_iso, open, close, m1_bars)."""
    rows = []
    for utc_iso, open_, close_, m1_bars in specs:
        rows.append(
            {
                "time": utc_iso,
                "broker_time_raw": _raw_epoch(utc_iso, offset_hours),
                "open": float(open_),
                "high": max(open_, close_) + 0.01,
                "low": min(open_, close_) - 0.01,
                "close": float(close_),
                "m1_bars": int(m1_bars),
            }
        )
    frame = pd.DataFrame(rows)
    frame["time"] = pd.to_datetime(frame["time"], utc=True)
    return frame


def make_london_rising(
    day: str = "2024-07-15", n_bars: int = 32, extra=None, step_minutes: int = 15
) -> pd.DataFrame:
    """Hari London dengan open/close BERBEDA tiap bar (sensitif ke jendela).

    Bar k: open = 150 + 0.01k, close = open + 0.05. Maka
    drift(N) = close[N-1] - open[0] = 0.05 + 0.01*(N-1) — berbeda untuk tiap N.
    Sesi London 8 jam = maks 32 bar M15; N>32 butuh grid lebih rapat
    (`step_minutes` < 15) agar menguji N bar PERTAMA, bukan "ambil semua"
    (re-audit ketiga §8.5, butir-5 batch-4).
    """
    start = pd.Timestamp(day, tz="UTC") + pd.Timedelta(hours=LONDON_SUMMER_START_UTC_HOUR)
    specs = []
    for k in range(n_bars):
        open_ = 150.0 + 0.01 * k
        specs.append((start.isoformat(), open_, open_ + 0.05, 15))
        start = start + pd.Timedelta(minutes=step_minutes)
    if extra:
        specs.extend(extra)
    return make_m15_bars(specs)


def make_daily(
    days,
    atr: float = 0.5,
    rv_roll_20d: float = 0.0,
    ratio: float = 0.02,
    range_atr: float = 80.0,
    close: float = 150.0,
) -> pd.DataFrame:
    """Frame grain broker-day sintetis (index date_broker, tz-naive)."""
    index = pd.DatetimeIndex(pd.to_datetime(list(days)))
    index.name = "date_broker"
    daily = pd.DataFrame(index=index)
    daily["atr_14_d1"] = float(atr)
    daily["rv_roll_20d"] = float(rv_roll_20d)
    daily["ratio_path"] = float(ratio)
    daily["range_atr"] = float(range_atr)
    daily["close"] = float(close)
    return daily


def make_range_day(day: str = "2024-07-15") -> pd.DataFrame:
    """Satu hari broker dengan metrik range (dipakai bukti mutasi)."""
    return make_daily([day], ratio=0.02, range_atr=80.0)


def _tau_youden_dari_store(window: int) -> tuple[float, int, int]:
    """Hitung-ulang TAU Youden Q1(a) dari kolom rv STORE dengan `window`.

    Prosedur identik protokol §2: rv_score = rv_roll_20d / window; span
    2023-01-01..2023-12-31; B = Jan-Jun (positif), A = Jul-Des; aturan
    strict `>`, Youden J = sens + spec - 1, ambang = kandidat skor observasi.
    Sumber = store terpisah (bukan frame runtime) — penguncian DATA untuk
    RV_WINDOW_DAYS (butir-3 batch-4, DISIPLIN 12).

    Returns:
        (tau, n_B, n_A) hasil hitung-ulang dari data.
    """
    config = bl.load_config("data")
    symbol = config["mt5"]["symbol"]
    path = bl.FEATURES_DIR / "M15" / f"{symbol.lower()}_m15_features.parquet"
    store = pd.read_parquet(path, columns=["date_broker", "rv_roll_20d"])
    rv = store.groupby("date_broker")["rv_roll_20d"].last().sort_index().shift(-1)
    score = rv / window
    span = score.loc["2023-01-01":"2023-12-31"].dropna()
    mask_b = span.index <= pd.Timestamp("2023-06-30")
    b, a = span[mask_b], span[~mask_b]
    best_j, best_t = -np.inf, float("nan")
    for t in np.unique(span.to_numpy()):
        j = (b > t).mean() + (a <= t).mean() - 1.0
        if j > best_j:
            best_j, best_t = j, float(t)
    return best_t, int(len(b)), int(len(a))


# ==================== TEST CLASSIFY_DAY_LABEL ====================


class TestClassifyDayLabel:
    def test_trending_label(self):
        """ratio_path > 0.0268 DAN range_atr > 88.79 → trending."""
        daily = make_daily(["2024-01-01"], ratio=0.03, range_atr=90.0)
        assert classify_day_label(daily).loc[pd.Timestamp("2024-01-01")] == "trending"

    def test_range_label(self):
        """ratio_path <= 0.0268 DAN range_atr <= 88.79 → range."""
        daily = make_range_day()
        assert classify_day_label(daily).loc[pd.Timestamp("2024-07-15")] == "range"

    def test_normal_label(self):
        """Di antara kedua aturan → normal."""
        daily = make_daily(["2024-01-01"], ratio=0.03, range_atr=80.0)
        assert classify_day_label(daily).loc[pd.Timestamp("2024-01-01")] == "normal"

    def test_nan_metrik_tetap_normal_bukan_none(self):
        """Metrik NaN → 'normal', tidak boleh None (acceptance putusan C)."""
        daily = make_daily(["2024-01-01"])
        daily.loc[pd.Timestamp("2024-01-01"), "ratio_path"] = float("nan")
        labels = classify_day_label(daily)
        assert labels.loc[pd.Timestamp("2024-01-01")] == "normal"
        assert labels.notna().all()

    def test_deterministic(self):
        """Input sama → output sama."""
        daily = make_range_day()
        assert classify_day_label(daily).equals(classify_day_label(daily))


# ==================== TEST LONDON DRIFT (Q2-b) + GRAIN (C) ====================


class TestLondonDrift4h:
    def test_formula_close_terakhir_minus_open_pertama(self):
        """drift = close bar-16 - open bar-1 = 0.05 + 0.01*15 = 0.20."""
        m15 = make_london_rising()
        daily = make_daily(["2024-07-15"], atr=0.5)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        drift = float(out.loc[pd.Timestamp("2024-07-15"), "london_drift_4h"])
        assert drift == pytest.approx(0.20)

    def test_norm_adalah_drift_per_atr_index_sama(self):
        """london_drift_norm = drift / atr_14_d1 pada index yang sama."""
        m15 = make_london_rising()
        daily = make_daily(["2024-07-15"], atr=0.5)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        norm = float(out.loc[pd.Timestamp("2024-07-15"), "london_drift_norm"])
        assert norm == pytest.approx(0.20 / 0.5)

    def test_bar_luar_london_diabaikan(self):
        """Bar non-London (jam 20 UTC) tidak boleh ikut jendela."""
        extra = ("2024-07-15T20:00:00+0000", 999.0, 999.0, 15)
        m15 = make_london_rising(extra=[extra])
        daily = make_daily(["2024-07-15"], atr=0.5)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        assert float(out.loc[pd.Timestamp("2024-07-15"), "london_drift_4h"]) == pytest.approx(0.20)

    def test_dst_aware_musim_dingin_mulai_08_utc(self):
        """Januari: jendela London mulai 08 UTC; bar 07 UTC BUKAN London."""
        specs = [("2024-01-15T07:00:00+0000", 999.0, 999.0, 15)]
        start = pd.Timestamp("2024-01-15", tz="UTC") + pd.Timedelta(
            hours=LONDON_WINTER_START_UTC_HOUR
        )
        for k in range(32):
            open_ = 150.0 + 0.01 * k
            specs.append((start.isoformat(), open_, open_ + 0.05, 15))
            start = start + pd.Timedelta(minutes=15)
        m15 = make_m15_bars(specs)
        daily = make_daily(["2024-01-15"], atr=0.5)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        assert float(out.loc[pd.Timestamp("2024-01-15"), "london_drift_4h"]) == pytest.approx(0.20)

    def test_hari_tanpa_bar_london_meledak(self):
        """Hari broker tanpa bar London → AssertionError (grain tidak lengkap)."""
        m15 = make_m15_bars([("2024-07-15T20:00:00+0000", 150.0, 151.0, 15)])
        daily = make_daily(["2024-07-15"], atr=0.5)
        with pytest.raises(AssertionError, match="tanpa bar London"):
            compute_london_drift_4h(m15, daily, daily["atr_14_d1"])

    def test_index_output_grain_store_tanpa_hari_utc_hantu(self):
        """Index output = daily.index (date_broker store); hari-UTC hantu absen."""
        specs = [
            ("2024-07-15T22:00:00+0000", 150.0, 150.1, 15),
            ("2024-07-16T07:00:00+0000", 150.0, 150.2, 15),
            ("2024-07-16T07:15:00+0000", 150.2, 150.5, 15),
        ]
        m15 = make_m15_bars(specs, offset_hours=2.0)
        daily = make_daily(["2024-07-16"], atr=0.5)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        assert out.index.equals(daily.index)
        assert out.index.name == "date_broker"
        assert pd.Timestamp("2024-07-15") not in out.index


class TestJendelaLondonLock:
    """#26 — N terkunci: fixture SENSITIF, N=4/8/60 harus berbeda dari N=16."""

    def test_konstanta_terkunci_16(self):
        assert LONDON_FIRST_N == 16
        assert bl.LONDON_FIRST_N == 16

    @pytest.mark.parametrize("n_mut", [4, 8, 60])
    def test_n_lain_menghasilkan_drift_berbeda(self, monkeypatch, n_mut):
        m15 = make_london_rising()
        daily = make_daily(["2024-07-15"], atr=0.5)
        monkeypatch.setattr(bl, "LONDON_FIRST_N", n_mut)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        drift = float(out.loc[pd.Timestamp("2024-07-15"), "london_drift_4h"])
        assert drift != pytest.approx(0.20)

    def test_n_16_hasil_terkunci(self, monkeypatch):
        m15 = make_london_rising()
        daily = make_daily(["2024-07-15"], atr=0.5)
        monkeypatch.setattr(bl, "LONDON_FIRST_N", 16)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        drift = float(out.loc[pd.Timestamp("2024-07-15"), "london_drift_4h"])
        assert drift == pytest.approx(0.20)

    def test_n60_mengambil_60_bar_pertama_bukan_ambil_semua(self, monkeypatch):
        """Butir-5 batch-4: 70 bar London — N=60 = 60 bar PERTAMA, bukan ambil-semua."""
        m15 = make_london_rising(n_bars=70, step_minutes=5)
        daily = make_daily(["2024-07-15"], atr=0.5)
        out16 = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        drift16 = float(out16.loc[pd.Timestamp("2024-07-15"), "london_drift_4h"])
        assert drift16 == pytest.approx(0.20)
        monkeypatch.setattr(bl, "LONDON_FIRST_N", 60)
        out60 = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        drift60 = float(out60.loc[pd.Timestamp("2024-07-15"), "london_drift_4h"])
        assert drift60 == pytest.approx(0.05 + 0.01 * 59), "harus 60 bar pertama"
        assert drift60 != pytest.approx(0.05 + 0.01 * 69), "bukan ambil semua 70 bar"


class TestGrainBrokerDay:
    """#21/#29 — kunci anti-regresi grain tunggal."""

    def test_source_tanpa_panggilan_normalize_dan_daily_from_m15(self):
        """Kode (bukan docstring) tidak boleh memanggil normalize / _daily_from_m15."""
        source = Path(bl.__file__).read_text(encoding="utf-8")
        calls = [
            ast.unparse(node)
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Attribute)
        ]
        assert not any("normalize" in call for call in calls), calls
        assert "_daily_from_m15" not in source

    def test_hari_hantu_utc_tidak_masuk_gap(self):
        """UTC-day 2024-07-15 ada di bar, broker-day-nya 2024-07-16 (offset +2)."""
        specs = [
            ("2024-07-15T22:00:00+0000", 150.0, 150.1, 3),
            ("2024-07-16T07:00:00+0000", 150.0, 150.1, 15),
            ("2024-07-16T07:15:00+0000", 150.0, 150.1, 3),
            ("2024-07-16T07:30:00+0000", 150.0, 150.1, 15),
        ]
        flag = compute_gap_f2_flag(make_m15_bars(specs, offset_hours=2.0))
        assert pd.Timestamp("2024-07-15") not in flag.index
        assert pd.Timestamp("2024-07-16") in flag.index

    def test_drift_grain_mengikuti_broker_day_bukan_utc(self):
        """Dua UTC-day → satu broker-day: drift hanya untuk broker-day itu."""
        specs = [
            ("2024-07-15T22:00:00+0000", 150.0, 150.1, 15),
            ("2024-07-16T07:00:00+0000", 150.0, 150.2, 15),
            ("2024-07-16T07:15:00+0000", 150.2, 150.5, 15),
        ]
        m15 = make_m15_bars(specs, offset_hours=2.0)
        daily = make_daily(["2024-07-16"], atr=0.5)
        out = compute_london_drift_4h(m15, daily, daily["atr_14_d1"])
        assert list(out.index) == [pd.Timestamp("2024-07-16")]
        assert float(out["london_drift_4h"].iloc[0]) == pytest.approx(0.5)


# ==================== TEST GAP F2 FLAG (Q3-a) ====================


class TestGapF2Flag:
    def test_bucket_midday_parsial_memberi_flag_1(self):
        """m1_bars < 15 di bucket tengah → flag hari = 1."""
        specs = [
            ("2024-07-15T07:00:00+0000", 150.0, 150.1, 15),
            ("2024-07-15T07:15:00+0000", 150.0, 150.1, 14),
            ("2024-07-15T07:30:00+0000", 150.0, 150.1, 15),
            ("2024-07-15T07:45:00+0000", 150.0, 150.1, 15),
        ]
        flag = compute_gap_f2_flag(make_m15_bars(specs))
        assert flag.loc[pd.Timestamp("2024-07-15")] == 1

    def test_tanpa_bucket_parsial_flag_0(self):
        flag = compute_gap_f2_flag(make_london_rising(n_bars=8))
        assert flag.loc[pd.Timestamp("2024-07-15")] == 0

    def test_bucket_tepi_parsial_tidak_dihitung(self):
        """Bucket pertama/terakhir parsial → bukan mid-day (flag tetap 0)."""
        specs = [
            ("2024-07-15T07:00:00+0000", 150.0, 150.1, 1),
            ("2024-07-15T07:15:00+0000", 150.0, 150.1, 15),
            ("2024-07-15T07:30:00+0000", 150.0, 150.1, 15),
            ("2024-07-15T07:45:00+0000", 150.0, 150.1, 2),
        ]
        flag = compute_gap_f2_flag(make_m15_bars(specs))
        assert flag.loc[pd.Timestamp("2024-07-15")] == 0

    def test_dtype_int_tanpa_nan(self):
        flag = compute_gap_f2_flag(make_london_rising(n_bars=8))
        assert flag.dtype == int
        assert not flag.isna().any()
        assert set(flag.unique()) <= {0, 1}

    def test_konstanta_batas_parsial_terkunci(self):
        assert M1_BARS_MIN == 15


# ==================== TEST RV REGIME FLAG (Q1-a) ====================


class TestRvRegimeFlag:
    def test_flag_1_di_atas_tau(self):
        daily = make_daily(["2024-01-01"], rv_roll_20d=TAU_2023 * 20.0 * 1.5)
        flag = compute_rv_regime_flag(daily)
        assert flag.loc[pd.Timestamp("2024-01-01")] == 1.0

    def test_flag_0_di_bawah_tau(self):
        daily = make_daily(["2024-01-01"], rv_roll_20d=TAU_2023 * 20.0 * 0.5)
        flag = compute_rv_regime_flag(daily)
        assert flag.loc[pd.Timestamp("2024-01-01")] == 0.0

    def test_warmup_nan_bukan_default_false(self):
        daily = make_daily(["2024-01-01"], rv_roll_20d=float("nan"))
        flag = compute_rv_regime_flag(daily)
        assert pd.isna(flag.loc[pd.Timestamp("2024-01-01")])

    def test_tau_dan_angka_kalibrasi_terkunci(self):
        """Angka kalibrasi Q1(a) di kode = angka yang ditulis di protokol §2."""
        assert pytest.approx(2.5951672079821496e-05) == TAU_2023
        assert pytest.approx(0.8173755150499336) == CALIB_AUC_2023
        assert CALIB_N_B == 111
        assert CALIB_N_A == 129

    def test_rv_window_terikat_kalibrasi_ulang(self):
        """Butir-3 batch-4: RV_WINDOW_DAYS terikat DATA kalibrasi — jendela
        berubah tanpa TAU hitung-ulang harus MERAH (bukan konstanta-vs-konstanta).
        """
        tau, n_b, n_a = _tau_youden_dari_store(bl.RV_WINDOW_DAYS)
        assert tau == TAU_2023, "TAU_2023 tidak cocok hasil kalibrasi ulang data"
        assert n_b == CALIB_N_B and n_a == CALIB_N_A

    def test_bukan_all_nan_pada_data_berisi(self):
        daily = make_daily(["2024-01-01", "2024-01-02"], rv_roll_20d=1.0)
        flag = compute_rv_regime_flag(daily)
        assert flag.notna().all()


# ==================== TEST QUARANTINE MASK ====================


class TestQuarantineMask:
    def test_hari_dalam_jendela_true(self):
        mask = quarantine_mask(make_daily(["2024-10-29"]))
        assert bool(mask.loc[pd.Timestamp("2024-10-29")])

    def test_hari_luar_jendela_false(self):
        mask = quarantine_mask(make_daily(["2024-01-01"]))
        assert not bool(mask.loc[pd.Timestamp("2024-01-01")])

    def test_dtype_bool_murni_tanpa_none(self):
        mask = quarantine_mask(make_daily(["2024-10-29", "2024-01-01"]))
        assert mask.dtype == bool
        assert mask.notna().all()

    def test_19_hari_dua_jendela_terhitung(self):
        """Kedua jendela F-1 terbawa: 5 + 14 = 19 hari broker (weekday)."""
        days = [d for d in pd.date_range("2024-10-28", "2024-11-01", freq="D") if d.weekday() < 5]
        days += [d for d in pd.date_range("2026-03-10", "2026-03-27", freq="D") if d.weekday() < 5]
        days += [pd.Timestamp("2024-01-01"), pd.Timestamp("2025-01-01")]
        assert len(days) == 21
        mask = quarantine_mask(make_daily(days))
        assert int(mask.sum()) == 19


# ==================== TEST DUA-VARIAN EKSKLUSI ====================


class TestDuaVarianEksklusi:
    def test_inklusi_vs_eksklusi_berbeda_di_hari_anomali(self):
        days = list(pd.date_range("2024-10-28", "2024-11-01", freq="D"))
        daily = make_daily(days, ratio=0.02, range_atr=80.0)
        labels_inklusi = classify_day_label(daily)
        mask = quarantine_mask(daily)
        labels_eksklusi = labels_inklusi.copy()
        labels_eksklusi[mask] = "excluded"
        diff = int((labels_inklusi != labels_eksklusi).sum())
        assert diff == 5

    def test_selisih_dapat_dilaporkan(self):
        days = list(pd.date_range("2024-10-28", "2024-11-01", freq="D"))
        daily = make_daily(days, ratio=0.03, range_atr=90.0)
        labels = classify_day_label(daily)
        mask = quarantine_mask(daily)
        assert int(mask.sum()) == 5
        assert (labels[mask] == "trending").all()


# ==================== TEST REGISTER H2 STRATEGY ====================


class TestRegisterH2Strategy:
    def test_returns_dict_dengan_kunci_kontrak(self):
        strategy = register_h2_strategy()
        assert isinstance(strategy, dict)
        for key in (
            "name",
            "entry",
            "exit",
            "sl_atr",
            "tp",
            "biaya",
            "entry_time_utc",
            "entry_frequency",
            "price_unit",
        ):
            assert key in strategy

    def test_biaya_cost_basis_mean_sesi(self):
        assert register_h2_strategy()["biaya"] == "cost_basis mean sesi"

    def test_entry_time_utc_15(self):
        assert register_h2_strategy()["entry_time_utc"] == "15"

    def test_entry_frequency_1x_per_broker_day(self):
        assert register_h2_strategy()["entry_frequency"] == "1x per broker-day"

    def test_price_unit_jpy(self):
        assert register_h2_strategy()["price_unit"] == "JPY"

    def test_sl_atr_1x_atr_jpy(self):
        assert register_h2_strategy()["sl_atr"] == "1x ATR 14-hari (atr_14_d1, satuan harga JPY)"


# ==================== TEST GUARD PROVENANS ATR (putusan B) ====================


GUARD_DAYS = ["2024-07-15", "2024-07-16", "2024-07-17"]


def _write_store_parquet(path: Path, days, atr: float) -> Path:
    """Tulis store semu persis mekanisme attach build_features.

    Nilai hari-D disimpan pada baris hari-D+1 (`shift(1)` anti-look-ahead);
    baris hari pertama NaN — sama seperti store produksi B1.
    """
    values = [float("nan")] + [float(atr)] * (len(days) - 1)
    frame = pd.DataFrame({"date_broker": pd.to_datetime(list(days)), "atr_14_d1": values})
    frame.to_parquet(path, index=False)
    return path


def _guard_fixture(tmp_path):
    """Kondisi produksi: pembagi dari frame daily, referensi dari STORE PARQUET
    terpisah — persis wiring main() (baca store -> cocok hari -> reindex).
    BUKAN snapshot daily sebelum sabotase (re-audit ketiga §3.4)."""
    m15 = pd.concat([make_london_rising(day=d) for d in GUARD_DAYS], ignore_index=True)
    daily = make_daily(GUARD_DAYS, atr=0.5)
    path = _write_store_parquet(Path(tmp_path) / "features_guard.parquet", GUARD_DAYS, atr=0.5)
    reference = bl._read_atr_reference_from_store(path)
    assert reference.index.equals(daily.index), "hari store != hari label"
    return m15, daily, reference.reindex(daily.index)


class TestGuardProvenansAtr:
    def test_baseline_pembagi_kolom_store_lolos(self, tmp_path):
        m15, daily, reference = _guard_fixture(tmp_path)
        out = compute_london_drift_4h(m15, daily, reference)
        assert float(out["london_drift_norm"].iloc[0]) == pytest.approx(0.20 / 0.5)

    @pytest.mark.parametrize(
        "sabotage",
        [
            pytest.param(lambda d: 1.0, id="atr_1.0_non_harga"),
            pytest.param(lambda d: 88.79, id="atr_88.79_tak_berdimensi"),
            pytest.param(
                lambda d: float(d["close"].mean()), id="atr_close_avg_harga_kuantitas_salah"
            ),
        ],
    )
    def test_sabotase_pembagi_meledak(self, sabotage, tmp_path):
        """Sabotase frame daily; referensi tetap dari FILE store terpisah
        (bukan snapshot sebelum sabotase) — kondisi sama dengan produksi."""
        m15, daily, reference = _guard_fixture(tmp_path)
        daily["atr_14_d1"] = sabotage(daily)
        with pytest.raises(AssertionError, match="provenans"):
            compute_london_drift_4h(m15, daily, reference)

    def test_guard_unit_membedakan_deret(self):
        _assert_atr_provenance(pd.Series([0.5, 0.6]), pd.Series([0.5, 0.6]))
        with pytest.raises(AssertionError, match="provenans"):
            _assert_atr_provenance(pd.Series([1.0, 1.0]), pd.Series([0.5, 0.6]))


# ==================== GUARD PADA JALUR PRODUKSI (batch-4 butir 1) ====================


@pytest.fixture(scope="module")
def prod_guard_frames():
    """Frame produksi sekali-baca: m15, daily, referensi dari STORE TERPISAH.

    Meniru wiring main(): atr_reference = _read_atr_reference_from_store(path)
    — bukan kolom frame pembagi, bukan snapshot (DISIPLIN butir 9).
    """
    config = bl.load_config("data")
    symbol = config["mt5"]["symbol"]
    pip_size = float(config["spread"]["pip_size"][symbol])
    m15 = bl.load_processed("M15", symbol)
    m1 = bl.load_processed("M1", symbol)
    daily = bl.daily_metrics(m1, m15, pip_size)
    store = bl.FEATURES_DIR / "M15" / f"{symbol.lower()}_m15_features.parquet"
    reference = bl._read_atr_reference_from_store(store)
    assert reference.index.equals(daily.index), "hari store != hari label"
    return m15, daily, reference.reindex(daily.index)


class TestGuardProvenansJalurProduksi:
    """Butir-1 batch-4: sabotase frame jalur produksi; referensi ikut dari
    store terpisah — dipanggil persis seperti main() (via _build_daily_labels)."""

    def test_baseline_produksi_lolos(self, prod_guard_frames):
        m15, daily, reference = prod_guard_frames
        out = bl._build_daily_labels(m15, daily, reference)
        assert int(out["london_drift_4h"].isna().sum()) == 0
        assert int(out["london_drift_norm"].isna().sum()) == 14

    @pytest.mark.parametrize(
        "kasus",
        [
            pytest.param("1.0", id="atr_1.0_non_harga"),
            pytest.param("88.79", id="atr_88.79_tak_berdimensi"),
            pytest.param("close-avg", id="atr_close_avg_harga_kuantitas_salah"),
        ],
    )
    def test_sabotase_produksi_meledak(self, prod_guard_frames, kasus):
        m15, daily, reference = prod_guard_frames
        bad = daily.copy()
        bad["atr_14_d1"] = float(m15["close"].mean()) if kasus == "close-avg" else float(kasus)
        with pytest.raises(AssertionError, match="provenans"):
            bl._build_daily_labels(m15, bad, reference)


# ==================== BUKTI MUTASI (D2) ====================


class TestBuktiMutasi:
    """Mutasi ditambal pada binding yang DIPAKAI test (HERE), lalu test
    pengunci yang sama dijalankan dan harus MERAH. Kontras dengan batch-2
    yang menambal `bl.<nama>` sehingga mutasi tidak pernah terpanggil (#25).
    """

    def test_mutasi_classify_day_label_membuat_test_range_merah(self, monkeypatch):
        fake = lambda daily: pd.Series(  # noqa: E731
            "trending", index=daily.index, name="day_label"
        )
        with monkeypatch.context() as patch:
            patch.setattr(HERE, "classify_day_label", fake)
            with pytest.raises(AssertionError):
                TestClassifyDayLabel().test_range_label()
        # Binding pulih → test pengunci hijau kembali.
        TestClassifyDayLabel().test_range_label()

    def test_mutasi_quarantine_mask_membuat_test_jendela_merah(self, monkeypatch):
        fake = lambda daily: pd.Series(False, index=daily.index, dtype=bool)  # noqa: E731
        with monkeypatch.context() as patch:
            patch.setattr(HERE, "quarantine_mask", fake)
            with pytest.raises(AssertionError):
                TestQuarantineMask().test_hari_dalam_jendela_true()
        TestQuarantineMask().test_hari_dalam_jendela_true()

    def test_patch_bl_tidak_terjangkau_binding_lokal(self, monkeypatch):
        """Dokumentasi bug batch-2: menambal bl.<nama> TIDAK mengubah binding test."""
        with monkeypatch.context() as patch:
            patch.setattr(
                bl,
                "classify_day_label",
                lambda daily: pd.Series("trending", index=daily.index, name="day_label"),
            )
            # Binding lokal `classify_day_label` di modul ini masih fungsi asli.
            daily = make_range_day()
            assert classify_day_label(daily).loc[pd.Timestamp("2024-07-15")] == "range"


# ==================== PAGU BARIS (D1) ====================


class TestPaguBarisD1:
    def test_modul_le_400_baris_dan_main_le_50_ast(self):
        source = Path(bl.__file__).read_text(encoding="utf-8")
        assert len(source.splitlines()) <= 400, "D1 melampaui pagu 400 baris"
        tree = ast.parse(source)
        spans = {
            node.name: node.end_lineno - node.lineno + 1
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }
        assert spans["main"] <= 50, f"main {spans['main']} baris AST > 50"
        assert all(span <= 50 for span in spans.values()), spans


# ==================== TEST END-TO-END MAIN (D2 blocking 7) ====================


@pytest.fixture(scope="module")
def d4_dir(tmp_path_factory):
    """Jalankan main() sekali untuk seluruh test end-to-end."""
    out = tmp_path_factory.mktemp("labels")
    bl.main(out_dir=out)
    return out


class TestMainEndToEnd:
    def test_dua_file_nama_kontrak_saja(self, d4_dir):
        names = sorted(p.name for p in Path(d4_dir).glob("*.parquet"))
        assert names == ["usdjpy_day_labels.parquet", "usdjpy_h2_trades.parquet"]

    def test_day_labels_grain_dan_row_key(self, d4_dir):
        day = pd.read_parquet(Path(d4_dir) / "usdjpy_day_labels.parquet")
        assert len(day) == 974, "D4 harus 974 hari broker (putusan C)"
        assert day.index.name == "date_broker", "row key #20 hilang"
        assert day["day_label"].notna().all(), "day_label tidak boleh None"
        assert day["quarantine_mask"].dtype == bool
        assert int(day["quarantine_mask"].sum()) == 19
        assert int(day["london_drift_4h"].isna().sum()) == 0
        assert int(day["london_drift_norm"].isna().sum()) == 14, "NaN norm hanya warmup ATR"
        assert int(day["gap_f2_flag"].sum()) == 234, "recount Q3(a) pada grain broker-day"

    def test_h2_trades_tanpa_kolom_hasil(self, d4_dir):
        trades = pd.read_parquet(Path(d4_dir) / "usdjpy_h2_trades.parquet")
        assert list(trades.columns) == [
            "symbol",
            "strategy",
            "entry_rule",
            "exit_rule",
            "sl_atr",
            "tp",
            "biaya",
            "entry_time_utc",
            "entry_frequency",
            "price_unit",
        ]
        for column in ("pnl", "pnl_after_cost", "ev"):
            assert column not in trades.columns

    def test_d4_deterministik_byte_identik(self, d4_dir, tmp_path):
        """Gate §3: run ulang main() → sha256 identik dengan yang di disk."""
        second = Path(tmp_path) / "labels2"
        bl.main(out_dir=second)
        for name in ("usdjpy_day_labels.parquet", "usdjpy_h2_trades.parquet"):
            first_bytes = (Path(d4_dir) / name).read_bytes()
            second_bytes = (second / name).read_bytes()
            digest_a = hashlib.sha256(first_bytes).hexdigest()
            digest_b = hashlib.sha256(second_bytes).hexdigest()
            assert digest_a == digest_b, f"{name} tidak byte-reprodusibel"
