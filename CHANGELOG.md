# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/).
Versi mengikuti [Semantic Versioning](https://semver.org/).

Semua tanggal memakai ISO-8601 (YYYY-MM-DD).

## [Unreleased]

### Fixed

- `validate_data.check_spread` selalu mengembalikan `passed=True` walau tidak
  pernah membandingkan apa pun. Sekarang membandingkan p99 terhadap
  `spread.by_year[year]` dengan `warn_multiplier` (2x) dan `error_multiplier`
  (5x). Dampak pada data nyata: tahun 2023 menjadi WARN (p99 8,50 pip > 6,00).
- `spread.by_year` tidak pernah terpakai di mana pun. Pencarian kunci gagal
  karena YAML membaca `2023:` sebagai key int, bukan string, sehingga jatuh ke
  `default` secara senyap. Kunci kini dinormalisasi ke `str`.
- `validate_data.check_known_anomalies` memakai daftar anomali yang hardcode.
  Dipindahkan ke `configs/data.yaml` (`validation.anomaly_windows`).
- `import MetaTrader5` di module level membuat seluruh test collection gagal di
  mesin tanpa MT5 (paket Windows-only). Diganti import lazy lewat
  `import_mt5()` dan `timeframe_constant()`.
- Error runtime (`mt5.initialize()` gagal, simbol tidak dikenal, tidak ada file
  data) sebelumnya ditulis ke stdout. Sekarang ke stderr, dengan `logger`.
- Komentar band bar-per-hari di `validate_data` mengklaim hari trading terpecah
  dua tanggal broker. Salah: break ada di 03:00-04:00 broker, wholly di dalam
  satu tanggal. 200 hari "rendah" adalah 194 hari Senin, bukan hari terpecah.

### Added

- Kolom `is_filled` pada output `clean_data`, menandai setiap bar sintetis agar
  `resample.py` dan `build_features.py` tidak memperlakukannya sebagai bar
  dagangan.
- `validate_data.check_break_hour` kini mendokumentasikan bahwa angka yang
  dilaporkan adalah jam buka kembali (04:00), bukan jam break (03:00).
- `src/data/clean_data.py`: raw CSV ke Parquet, dengan gap < 20 menit diisi dan
  break harian serta jeda akhir pekan tidak pernah diisi.

### Changed

- `validate_data.trading_days` dihitung dari jeda sesi (>= 55 menit), bukan
  `dt.date`. Dampak: 2023 turun dari 311 tanggal broker menjadi 163 sesi.
- `configs/data.yaml` mendapat `mt5.price_digits`, `spread.warn_multiplier`,
  `spread.error_multiplier`, dan `validation.anomaly_windows`.
- Hook pre-commit lokal memakai interpreter venv lewat
  `scripts/run_hook.bat`. Sebelumnya memakai Python 3.14 sistem yang tidak punya
  pyarrow, sehingga dua tes parquet selalu gagal.

### Removed

- `black==24.10.0` dari `requirements.txt`. Black sudah dihapus 2026-10-05 demi
  satu formatter saja (`ruff-format`); pin tersebut sudah basi.

### Known issues

- `validate_data.py` panjangnya 543 baris, melewati soft limit 400 baris
  (RULES.md). Ditutup dengan `# EXCEPTION` yang punya tiga batas keras: file
  melewati 600 baris, ada fungsi publik baru, atau akhir Milestone 1. Karena itu
  pemecahan check vs render yang diminta STATE.md ditunda ke akhir Milestone 1.
- 90 dari 946 lubang gap kecil berada di broker 02:58-03:07, tepat sebelum
  pembukaan pasar. Modul mengisinya karena di bawah ambang 20 menit, padahal itu
  bar pra-pembukaan. Semua ditandai `is_filled`, tapi belum diputuskan.
