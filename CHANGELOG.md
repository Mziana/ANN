# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/).
Versi mengikuti [Semantic Versioning](https://semver.org/).

Semua tanggal memakai ISO-8601 (YYYY-MM-DD).

## [Unreleased]

### Fixed

- **Offset di luar jadwal DST tidak lagi diam-diam mengembalikan +2.**
  `BrokerSchedule.offset_seconds` untuk tanggal melewati jendela terakhir
  sekarang melempar `ValueError` alih-alih diam-diam memakai offset standar.
  Tanpa ini, fetch data setelah 1 Nov 2026 akan menghasilkan kolom `time` yang
  salah 1 jam tanpa jejak apa pun.
- **Deskripsi anomali jam broker dikoreksi setelah self-audit adversarial.**
  Gejalanya bukan "break di jam dinding 23" melainkan digit jam broker mundur
  1 jam (sesi buka 00:00, bukan 01:00), dan self-audit menemukan **tiga**
  jendela — termasuk 2023-03-17..24 yang sebelumnya tidak tercatat — tetapi
  Klenz membedakan 2023 sebagai regime SA-03. Arsitek menghapus entri 2023;
  dua jendela tersisa: 2024-10-28..11-01 dan 2026-03-10..03-27. Total
  **26.198 bar = 1,94%**. Keduanya kini terdaftar di `validation.anomaly_windows` dan tidak bisa terlewat diam-diam.
  Bukti internal menunjukkan offset +3 menghasilkan waktu buka sesi 21:00 UTC
  yang tidak pernah muncul di 4 tahun selain 19 hari tersebut, sedangkan +2
  menghasilkan 22:00 UTC yang identik dengan tetangganya. Status tetap BELUM
  TERVERIFIKASI sampai Finex menjawab.
- **Server Finex ternyata seasonal, bukan offset tetap.** Kolom `time` di
  `data/raw` dan bucket di `data/processed` memakai GMT+3 sepanjang tahun,
  padahal server berjalan GMT+2 (EET) di musim dingin dan GMT+3 (EEST) di
  musim panas, mengikuti DST Amerika. Konversi sekarang memakai jadwal
  transisi dari `configs/data.yaml` lewat modul baru `src/data/broker_time.py`,
  dan data di-fetch ulang. Effect: sekitar 35% bar (seluruh musim dingin) yang
  sebelumnya salah 1 jam. Sumber: `finex.co.id/trading/instruments` plus
  jawaban Finex Support 2026-10-05 yang menyebut tanggal persis 2023-2026;
  kedelapan tanggal diverifikasi ulang terhadap aturan DST AS dan 8 dari 8
  cocok.
- `resample` dan `validate_data` menghitung jam dinding broker dengan cara
  menambah offset tetap, padahal digit mentah `broker_time_raw` sudah berisi
  jam dinding broker. Keduanya sekarang membaca digit itu apa adanya. Akibatnya
  bucket D1 turun dari 311/314/313/236 menjadi 259/260/259/196, yang
  sesuai jumlah hari perdagangan (52 minggu x 5 hari), dan bucket M5/H1/D1
  kini identik dengan bar native MT5 di jendela musim dingin maupun musim
  panas.
- **Kolom `time` di `data/raw` tersimpan 3 jam Maju dari UTC (bug R1).** MT5
  tidak mengembalikan instants Unix; ia mengembalikan jam dinding broker
  yang dikodekan seolah-olah epoch UTC. Fungsi `broker_epoch_to_utc` lama
  (`fromtimestamp(epoch, tz=broker_tz).astimezone(UTC)`) adalah no-op
  matematis, sehingga argumen `broker_tz` tidak pernah berpengaruh dan tiap
  bar disimpan 3 jam lebih depan dari UTC sejati. Diperbaiki dengan membaca
  digit jam dinding lebih dulu, menandai offset broker, lalu mengonversi.
  Bukti: sebelum fix `symbol_info_tick().time` meleset +10.799 detik vs jam
  internet independen; sesudah fix selisihnya <=2 detik, 5/5 sampel.
  Seluruh `data/raw` M1 (2023-2026) di-fetch ulang: 1.347.847 bar, 0 bar
  salah konversi. `broker_time_raw` tetap mentah untuk audit.
- `fetch_data.split_by_year` memakai kolom `broker_time_raw` untuk menentukan
  tahun, sehingga beberapa jam pertama 1 Januari masuk ke file tahun baru
  sambil membawa stempel waktu Desember. Sekarang memakai kolom `time` (UTC).
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

- **`tzdata==2026.5` dipin eksplisit di `requirements.txt`.** `zoneinfo` di
  Windows bergantung padanya; sebelumnya hanya masuk sebagai dependensi
  transitif sehingga tidak terjaga saat reinstall. Pin atas persetujuan user
  (RULES §13).
- `validate_data.check_break_hour` kini mendokumentasikan bahwa angka yang
  dilaporkan adalah jam buka kembali (04:00), bukan jam break (03:00).
- `src/data/clean_data.py`: raw CSV ke Parquet. Tidak pernah mengarang bar; hanya
  membuang duplikat, mengurutkan, dan membulatkan harga ke presisi tick.
- `src/data/resample.py`: M1 ke M5/M15/M30/H1/H4/D1. Bucket mengikuti jam
  dinding broker dan diberi label awal interval. Agregasi spread menghasilkan
  `spread_pips_mean` dan `spread_pips_max`, dan setiap bucket membawa `m1_bars`
  berisi jumlah bar M1 asli di dalamnya. Bucket kosong tidak pernah ditulis.
- `scripts/verify_native_m5.py`: membandingkan hasil resample M5 dengan bar M5
  native MT5. Hasil 2026-09-01 s/d 09-14: 2.760 bucket, nol selisih OHLCV.

### Changed

- **`MetaTrader5` dipin ke `==5.0.6231`** (versi terinstal terverifikasi via
  `pip show`) — dependency terakhir yang sebelumnya tanpa pin versi.
- **Venv kanonik `venv/` diverifikasi sinkron dengan requirements**:
  `pip install -r requirements.txt` no-op; `jupyter==1.1.0` dan
  `ipykernel==6.29.5` sudah terpasang. Env bantu `.venv/` (dibuat uv
  2026-10-05 oleh sesi AI) tidak dipakai gate dan dicatat di `.ai/STATE.md`
  agar tidak tertukar.
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
- **Interpolasi gap dari `clean_data.py`.** `fill_small_gaps` dan kolom
  `is_filled` dihapus. Mengarang harga untuk bar yang hilang berarti membuat
  harga yang tidak pernah terjadi, dan tidak ada tahap berikutnya yang bisa
  membedakannya dari harga asli. Tidak ada bar lagi yang dikarang: jumlah bar M1
  keluar sama dengan jumlah bar M1 masuk di keempat tahun.

### Known issues

- `validate_data.py` panjangnya 543 baris, melewati soft limit 400 baris
  (RULES.md). Ditutup dengan `# EXCEPTION` yang punya tiga batas keras: file
  melewati 600 baris, ada fungsi publik baru, atau akhir Milestone 1. Karena itu
  pemecahan check vs render yang diminta STATE.md ditunda ke akhir Milestone 1.
- 90 dari 946 lubang gap kecil berada di broker 02:58-03:07, tepat sebelum
  pembukaan pasar. Dulu modul mengisinya karena di bawah ambang 20 menit, padahal
  itu bar pra-pembukaan yang tidak pernah ada. Sekarang tidak ada bar yang
  diinterpolasi sama sekali, sehingga masalah ini hilang. Jumlah bar M1 per bucket
  tetap terekspos lewat kolom `m1_bars` di hasil resample.
