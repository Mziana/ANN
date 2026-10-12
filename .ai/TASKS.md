# TASKS.md — Task Board

**Update terakhir:** 2026-10-07

## In Progress

- [x] Phase A-1: Update state files (selesai 2026-10-05)
- [x] Phase A-2: Fix `broker_timezone` -> `Etc/GMT-3` di `configs/data.yaml` (selesai 2026-10-05)
- [x] Patch `checkpoints/checkpoint_07` & `09d` -> `Etc/GMT-3` (2026-10-05)
- [x] Strip BOM UTF-8 dari 27 file (2026-10-05)- [x] Phase A-3: Hapus BOM UTF-8 dari 27 file (2026-10-05)
- [x] Phase A-4: Docstring Google Style untuk 4 fungsi `verify_claims.py` + `check_state.py` (2026-10-05)
- [x] Phase A-5: `docs/PROJECT_MAP.md` dibuat (2026-10-05)
- [x] **PHASE A SELESAI** — lanjut Phase B
- [x] Gate pre-commit dibetulkan: hapus hook `mixed-line-ending`, tambah `scripts/run_tests.py` (2026-10-05)
- [ ] **Commit Phase A** (menunggu review user)
- [x] Phase B: `fetch_data.py`, `config.py`, 2 `__init__.py`, 22 test — 7/7 verifikasi lolos (2026-10-05)
- [x] Fetch full 2023-2026: **1.347.847 bar M1** (2026-10-05)
- [x] Investigasi DST 2023-2026: **broker tidak ikut DST, offset tetap +3**
- [x] `validate_data.py`: 2 jendela anomali ditandai sebagai peringatan, bukan error
- [x] `src/data/validate_data.py` + 33 test — **LOLOS 4 tahun, 0 error** (2026-10-05)
- [x] Config spread `by_year` (2023=3,0) — dasar p99 2023 = 8,5 pip
- [ ] **`src/data/clean_data.py`** — raw -> `data/processed/M1/` (Parquet)
- [ ] Catatan: kalau `validate_data.py` tambah fungsi, pecah check vs render
- [x] Gate karakter asing `scripts/check_foreign_chars.py` (2026-10-05) — ditulis
      AI, bukan file asing; catatan lama "perlu keputusan user" sudah usang
- [x] `.gitattributes` dibuat (text=auto eol=lf, ps1/bat crlf, biner) (2026-10-05)
- [x] Line ending dinormalisasi: 38 file LF, 3 `.ps1` CRLF (2026-10-05)
- [x] Black dihapus dari `.pre-commit-config.yaml` + `pyproject.toml` (2026-10-05)

## Todo (Prioritas Tinggi)

- [ ] Phase B: `src/data/fetch_data.py` — fetch M1 per tahun -> `data/raw/M1/`
- [ ] Phase B: `fetch_data.py` WAJIB simpan `broker_time_raw` (timestamp broker mentah) bersama kolom UTC (keputusan user 2026-10-05)
- [ ] Phase B: `validate_data.py` WAJIB uji offset historis vs anchor UTC yang dikenal sebelum fitur session dipakai
- [ ] Phase B: `src/data/clean_data.py` — raw -> processed (Parquet)
- [ ] Tambah `src/__init__.py` per subpackage (`data`, `features`, `models`, `backtest`, `utils`)
- [ ] `tests/test_fetch_data.py` — minimal 3 test, tanpa API live
- [ ] EDA: distribusi return, volatilitas per sesi, karakter per regime

## Todo (Prioritas Sedang)

- [ ] `src/features/build_features.py` + `build_labels.py`
- [ ] `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1)
- [ ] `src/models/baseline.py` (rule-based + logistic regression)
- [ ] `src/backtest/backtest.py` (spread + slippage + komisi WAJIB)
- [ ] `src/backtest/audit.py` (8 section AGENTS.md §18)
- [ ] Backtest library: putuskan vectorbt vs backtrader (belum diputuskan)

## Todo (Prioritas Rendah)

- [ ] Isi `README.md` (masih kosong)
- [x] Isi `CHANGELOG.md` (2026-10-05) — Fixed/Added/Changed/Removed/Known issues
- [ ] Isi `.env.example` (masih kosong)
- [x] `src/utils/config.py` loader YAML (2026-10-05) — RULES.md §10 terpenuhi,
      dipakai `fetch_data`, `validate_data`, `clean_data`
- [ ] Dashboard `dashboard/`

## Done

- [x] Checkpoint 01: Struktur folder (2026-10-05)
- [x] Checkpoint 05: State files (2026-10-05)
- [x] Checkpoint 06: scripts — verify_claims, check_state, pipeline.ps1 (2026-10-05)
- [x] Checkpoint 07: configs — requirements, pyproject, pre-commit, configs/*.yaml (2026-10-05)
- [x] Checkpoint 08: setup.ps1 + run.ps1 (2026-10-05)
- [x] Checkpoint 09a-09d: AGENTS v3.0, RULES v2.0, PROMPTS v2.0, CONTEXT v1.3, configs+jurnal+backtest (2026-10-05)
- [x] Setup environment: venv Python 3.12.8 + 134 paket (2026-10-05)
- [x] `git init` + 2 commit + pre-commit hook terpasang (2026-10-05)
- [x] Onboarding AI baru + inventarisasi (2026-10-05)
- [x] Verifikasi simbol MT5 = `USDJPY` (2026-10-05)
- [x] Verifikasi timezone broker = UTC+3 offset SAAT INI (2026-10-05)
- [~] Offset broker HISTORIS: belum terverifikasi — wajib dicek saat validate data
- [x] Patch `broker_timezone` di `checkpoints/checkpoint_07` & `09d` -> `Etc/GMT-3` (2026-10-05)
- [x] Verifikasi ketersediaan data = 1.348.135 bar M1 (2026-10-05)

## Blocked

- (kosong — tidak ada blocker aktif)

## Sudah Dibatalkan / Diganti

- [~] Fetch data MT5 — bukan "blocked", tapi **belum mulai** karena `src/` kosong.

## Catatan Verifikasi

- Checkpoint 06-09d, `git init`, dan setup environment **terbukti sudah dijalankan**
  (output-nya ada di working tree). Status lama "belum" sudah usang.
- `src/` hanya berisi `__init__.py` 0 byte. Semua modul inti belum ada.
- `trade_allowed=False` di terminal MT5: akun belum login untuk trading.

## Fase B — Pipeline Data (2026-10-05)

- [x] `src/utils/config.py` + `src/utils/__init__.py` (2026-10-05)
- [x] `src/data/fetch_data.py` + test (2026-10-05)
- [x] `configs/data.yaml` `broker_timezone: Etc/GMT-3` (2026-10-05)
- [x] `scripts/check_foreign_chars.py` + test + hook (2026-10-05)
- [x] `src/data/validate_data.py` + test + laporan validasi (2026-10-05)
- [x] `src/data/clean_data.py` + test (2026-10-05) — 103 test hijau
- [x] `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1) — 2026-10-05, 147 test hijau
- [ ] `src/features/build_features.py`
- [ ] `src/features/build_labels.py`

### Catatan clean_data

- Output `data/processed/M1/*.parquet`: 1.347.847 bar, folder di-gitignore.
- **D1 (2026-10-05): interpolasi dihapus.** Tidak ada lagi kolom `is_filled`
  karena tidak ada bar sintetis. Jumlah bar keluar == masuk di keempat tahun.
- diputuskan: 90 lubang 8-9 menit di broker 02:58-03:07 dulu diisi, kini tidak
  karena tidak ada interpolasi sama sekali. Jumlah bar asli per bucket terekspos
  lewat kolom `m1_bars` di hasil `resample.py`.

### Hasil audit Phase B (2026-10-05)

Auditor: 14 temuan. Verifikasi kode membatalkan 5 (C-02, H-02, H-03, H-04, L-02)
atas bukti dari data. 8 diperbaiki, LOW-04 ditunda.

- [x] Lazy import MT5 (`import_mt5`, `timeframe_constant`, `TIMEFRAME_NAMES`)
- [x] `check_spread` membandingkan p99 vs `spread.by_year` + multiplier di config
- [x] `validation.anomaly_windows` dipindah ke `configs/data.yaml`
- [x] `logging` + error ke stderr; `print` hanya di `main()`
- [x] `trading_days` dihitung dari jeda sesi, bukan tanggal broker
- [x] Komentar band bar-per-hari dikoreksi (200 hari rendah = 194 Senin)
- [x] Docstring: asumsi TF >= M1; `check_break_hour` = jam buka kembali
- [x] Marker `# EXCEPTION:` di `validate_data.py`
- [ ] (ditunda s/d akhir Milestone 1) Pecah `validate_data.py` jadi check vs
      render — 543 baris, batas keras: >600 baris / fungsi publik baru / akhir M1

### Hasil audit R1 — kolom `time` (2026-10-05)

Auditor (Klenz) mencatat kolom `time` 3 jam maju dari UTC; Coder semula
menyimpulkan "bukan bug" dengan metode sirkular. User mengabulkan fix.

- [x] Verifikasi ulang non-sirkular: tick + bar M5 MT5 vs jam internet
      independen (timeapi.io + HTTP `Date:`). Selisih +10.799 dtk, 5/5 sampel.
- [x] Klaim "drift 7 detik" gugur — `.ai/SESSION_LOG.md` sendiri mencatat
      10.807 dtk (= 3j 0m 7s), artinya jam pembanding lama sudah di frame broker.
- [x] `broker_epoch_to_utc` diperbaiki jadi konversi sejati
- [x] `split_by_year` memakai kolom `time`, bukan `broker_time_raw`
- [x] 5 assertion lama di `tests/test_fetch_data.py` diperbaiki + 2 test baru
      (regresi ke bukti terukur 1791205620 -> 10:07:00, dan bar dekat tahun baru)
- [x] Fetch ulang 4 file M1: 1.347.847 bar, 0 salah konversi, tahun cocok nama file
- [x] Bersihkan + resample ulang; native M5 vs resample 2.760 bucket, beda 0
- [x] Validasi data exit 0 di 4 tahun; ruff bersih; 147 test hijau
- [x] **DST diverifikasi dari broker.** Finex mengonfirmasi GMT+2/GMT+3 mengikuti
      DST Amerika, dengan tanggal persis 2023-2026. Jadwal masuk
      `configs/data.yaml`, logika di `src/data/broker_time.py`, data di-fetch
      ulang, 151 test hijau.
- [x] **Self-audit adversarial DST (2026-10-05).** Temuan SA-01 (offset 2027+
      diam-diam +2) sudah diperbaiki + test. Temuan SA-02 membongkar bahwa
      gejalanya bukan "break di jam 23" tapi **digit jam mundur 1 jam** (buka
      00:00), dan self-audit menemukan **tiga** jendela, tetapi Klenz
      re-verifikasi menentukan 2023-03-17..24 adalah regime SA-03, bukan anom-
      ali. Arsitek menghapus entri 2023 — tinggal **dua** jendela.
- [x] Bukti lokal non-sirkular: dengan offset +3, buka sesi di jendela itu jadi
      21:00 UTC, nilai yang tidak pernah muncul di 4 tahun selain 19 hari
      tersebut. Dengan +2 jadi 22:00 UTC, identik dengan tetangganya.
- [x] Kedua jendela terdaftar di `anomaly_windows`; test mengunci jumlahnya
      (2) dan mewajibkan tiap note memuat "BELUM TERVERIFIKASI".
- [ ] **Offset kedua jendela masih BELUM TERVERIFIKASI.** Pertanyaan presisi ke
      Finex sudah disiapkan (gejalanya tepat -1 jam, bukan "break di jam 23").
- [ ] **Jangan bangun fitur sesi Tokyo/London/NY** sebelum anomali di atas ditutup.
- [ ] **SA-03: regime 2023-H1 berbeda.** Jan-Jun 2023 = 1.431 bar/hari (sesi
      ~23,9 jam, tanpa break 60 menit) dan digit buka ~00:07, berbeda dari
      seluruh periode lain. 185.248 bar = 13,74%. Belum dijelaskan.
- [x] Hapus `data/raw/M1/usdjpy_m1_2026-10_test.csv` (2026-10-05, atas izin
      user) — sisa uji sesi lalu, format lama salah label. `data/raw/M1/` kini
      hanya 4 file tahun 2023-2026.

### Verifikasi keputusan Architect (2026-10-05) — selesai

- [x] Q1 validate_data 543 baris -> SETUJU DENGAN CATATAN (premis "hampir semua
      docstring" salah: dari +99 baris hanya 22 kode; ada aturan STATE.md yang
      belum dibahas)
- [x] Q2 check_bar_count -> **SELESAI, pilihan (i) dikonfirmasi user 2026-10-05**:
      `trading_days` tetap session logic, `check_bar_count` tetap `dt.date`,
      keduanya tidak diubah. Alasan resmi ada di docstring `check_bar_count`.
- [x] Q3 pyarrow -> **CANCEL** (user 2026-10-05): pyarrow sudah ada di
      requirements.txt baris 8; pyproject.toml TIDAK disentuh; sebagai gantinya
      `black==24.10.0` yang basi dihapus
- [x] Perbaiki catatan usang TASKS.md soal `scripts/check_foreign_chars.py`
      (file itu dibuat AI, bukan file asing)
- [x] Hapus `black==24.10.0` dari requirements.txt (basi, Black sudah dihapus)

## Lapisan 2 — EDA (2026-10-06)

- [x] Langkah 0 — Reuse-Check: `load_config` + `broker_time` + parquet + tzdata
      terverifikasi; temuan **dua venv** (`venv/` kanonik vs `.venv/` env bantu)
- [x] Langkah 1 — pin `tzdata==2026.5` + `MetaTrader5==5.0.6231`; jupyter no-op
      (sudah terpasang di venv kanonik); commit `chore(deps)`
- [ ] Langkah 2 — `notebooks/scalping/eda_00_setup.ipynb` (audit strata, tabel
      sesi, preregistrasi placebo, Kontrak 00) + laporan mini → STOP
- [ ] Notebook 01 returns → 02 volatility + fragmen spread → 4b → 03 autocorr →
      04 swings/levels → 05 regimes + report
- [ ] **Aturan baru (untuk masuk AGENTS/RULES): Setiap upgrade venv wajib update
      requirements di commit yang sama.**
- [ ] Arsip: entri SESSION_LOG 2026-10-05 menyebut hash `1147eef`; hash final
      `a63d117`. Koreksi disimpan sebagai item terbuka.
- [x] Batch newline + M1 + commit (2026-10-07): F-NL (`newline="\n"` ×5 builder)
      + F-NL2 (pasca-proses CRLF→LF, putusan arsitek Q1–Q4) + regen nb05 saja
      (81.851 B, 0 CR, 68 assertion, FIG-04..07 identik) + fix frasa provenance
      M1 ×4 dokumen; re-audit F-NL/F-NL2/M1 TERVERIFIKASI TUTUP tanpa temuan
      baru; commit `43e2a07`; Batch C mutakhir 0 MEDIUM + 4 LOW terbuka
       (B8-01/B10-01 dikecualikan, L2-01/L2-02 catatan)
- [x] Penguncian hipotesis H1–H5 (2026-10-07): review user H1→H5 + putusan
      arsitek (H1 KUATKAN, H2–H5 TERIMA S1–S8, H6+ DITOLAK, H3 vonis TERBUKA
      s/d S4); dokumen `hipotesis_lock_v1.md` + `putusan-arsitek-H1-H5.md`;
      commit `0107a56`
- [x] Fondasi fitur B1 + rantai audit TERTUTUP (2026-10-07): `build_features.py`
      400/400 + 37 test, parquet `07402f40…` tak berubah; audit 0 HIGH/1 MEDIUM/
      3 LOW → putusan B1 (D0+4 butir) + putusan F-1 (karantina konsumen B2)
      tersimpan; F-2/F-3/F-4 → re-audit → micro-batch R1/R2/R3 → konfirmasi
      3×YA; residual #4/#5/#7 + materialitas H1/H5 (BELUM DIUJI) berdiri
- [x] B2: `build_labels.py` + protokol H1/H2/H3 — SELESAI 2026-10-08
      (D1 399 baris + 60 test, D4 974 hari-broker, re-audit keempat LULUS 5/5,
      regresi 13/13, Fase 1 tertutup; H4/H5 tetap dilarang vonis final sebelum
      eksklusi+sensitivitas tercatat)
- [x] Lapisan 3-H3: spec arsitek SELESAI 2026-10-08
      (`arsitek/spesifikasi-lapisan3-H3.md`, hash `dacd0708`, gerbang lolos)
- [x] Lapisan 3-H3: eksekusi coder SELESAI 2026-10-08
      (`coder/hasil-lapisan3-H3.md` 1051 baris, C8 `c5cb5177`, gerbang lolos;
      Uji-1 IMMATERIAL, Uji-2 TIDAK STABIL → konsekuensi spec S4b)
- [x] Lapisan 3-H3: re-audit auditor SELESAI 2026-10-08
      (`Audit/reaudit-lapisan3-H3.md`, LULUS DENGAN CATATAN; F-1/F-2 MEDIUM
      + F-3/F-4/F-5 LOW; C2 LULUS substansi/GAGAL pola; S4b tetap kutipan)
- [x] Lapisan 3-H3: TERTUTUP 2026-10-08
      (`arsitek/putusan-lapisan3-H3.md`, C8 `478fc831`; P-1 S0 diterima +
      rule exact-comparison; P-2 M2 dikunci + rule paired/CI; P-3 pola C2
      dipensiunkan; P-4 S4b AKTIF = H3 GUGUR, filter dilarang, S4 MOOT)
- [x] Jalur H1/H2/H4/H5: dipilih user 2026-10-08; desain dua-batch
      (Batch-1 H1+H2 verdict-ready, Batch-2 H4+H5); draf prompt spec Batch-1
      tersimpan (`prompts/2026-10-08_spec-batch1-H1H2-arsitek.md`)
- [x] Spec arsitek Batch-1 MASUK + gerbang LOLOS 2026-10-08
      (`arsitek/spesifikasi-lapisan3-H1H2.md`, hash `fc29f6fa`, 369 baris;
      blob S0 lock/putusan/protokol cocok 40-hex; Q1 real-time = vonis,
      Q2 ratifikasi + pin (a)–(f); S1 gate exact-match [O8])
- [x] Eksekusi coder Batch-1 SELESAI + gerbang LOLOS 2026-10-09
      (`coder/hasil-lapisan3-H1H2.md`, 1175 baris, hash `1550209f`,
      C8 `522c221c`; S1 9/9 bit-exact; S-H1 = GUGUR formula, S-H2 = GUGUR
      formula; fokus re-audit: DEV-B1 burn-in, DEV-B3 exit 140/140 sinyal)
- [x] Re-audit Batch-1 SELESAI + gerbang LOLOS 2026-10-09
      (`Audit/reaudit-lapisan3-H1H2.md`, 511 baris, hash `e4143132`,
      verdict LULUS; S1/VR/S-H2 hitung-ulang bit-exact; DEV-B1 selesai
      tanpa re-run; DEV-B3 bukan bug; porcelain 98 = 97 + berkas saya)
- [x] Batch-1 TERTUTUP 2026-10-09 (`arsitek/putusan-lapisan3-H1H2.md`,
      hash `ca4e0b70`, gerbang LOLOS; vonis resmi H1 GUGUR + H2 GUGUR FINAL;
      burn-in kanonik 60 POSISI; R-B1…R-B4; H4/H5 untouched)
- [x] Desain Batch-2 SELESAI 2026-10-09 (walk-forward expanding tahunan
      kanonik; grid H5 4 sel + Holm; separasi S5; pin biaya/placebo/strategi
      sebagai Q1–Q5 arsitek)
- [x] Draf prompt spec Batch-2 tersimpan
      (`prompts/2026-10-09_spec-batch2-H4H5-arsitek.md`) — menunggu user
      paste ke arsitek
- [x] Spec arsitek Batch-2 MASUK + gerbang LOLOS 2026-10-09
      (`arsitek/spesifikasi-lapisan3-H4H5.md`, hash `4a46b815`, 461 baris;
      S0 + Q1–Q5 diputus + S-C C1–C9 + S-B 14 larangan; deviasi arsitek
      Q1 pool-tunggal/2026-dibuang-penuh, Q2 Holm, Q3 by_session,
      Q4 long-only, Q5 blok-tahunan — tercatat beralasan)
- [x] Draf prompt eksekusi coder Batch-2 tersimpan
      (`prompts/2026-10-09_eksekusi-batch2-H4H5-coder.md`) — menunggu user
      paste ke coder
- [x] Eksekusi coder Batch-2 SELESAI + gerbang LOLOS 2026-10-09
      (`coder/hasil-lapisan3-H4H5.md`, 1299 baris, hash `f06a8e27`,
      C8 `9cef2998`; S-H4 = TAHAN / S-H5 = GUGUR formula; DEV-B2-1..4 terbuka)
- [x] Re-audit Batch-2 SELESAI + gerbang LOLOS 2026-10-09
      (`Audit/reaudit-lapisan3-H4H5.md`, 707 baris, blob `8a4d2109`;
      LULUS DENGAN TEMUAN — 2 MEDIUM non-penentu + 4 LOW, 4 eskalasi)
- [x] Draf prompt putusan arsitek H4/H5 tersimpan
      (`prompts/2026-10-09_putusan-H4H5-arsitek.md`) — menunggu user
      paste ke arsitek
- [x] Batch-2 TERTUTUP 2026-10-09 (`arsitek/putusan-lapisan3-H4H5.md`,
      410 baris, blob `e02a203b`, C8 `5bfa76a2`, gerbang LOLOS;
      vonis resmi H4 TAHAN + H5 GUGUR FINAL; S-V per huruf;
      EKS-1–EKS-4 + T1–T6 diputus semua; P-5 kunci dua arah)
- [x] Brief telaah fondasi opsi B DISUSUN 2026-10-09
      (`assistant/prompts/2026-10-09_telaah-fondasi-B-arsitek.md`;
      U-1 karantina F-1 + U-2 dekomposisi biaya + U-3 regime deskriptif;
      diagnostik, BUKAN vonis ulang; H6+ tetap DITOLAK) — SUDAH dipaste,
      protokol MASUK (lihat entri berikut)
- [x] Rekomendasi T6 DIEKSEKUSI 2026-10-09 (atas perintah user): `git add`
      `src/features/build_labels.py` (399 baris) +
      `tests/test_build_labels.py` (713 baris) — staged file baru (A),
      BELUM commit; blind spot C2 tertutup; baseline staged kini 2 file
- [x] Protokol telaah fondasi B MASUK + gerbang LOLOS 2026-10-09
      (`arsitek/protokol-telaah-fondasi-B.md`, 218 baris, blob `ed436fdd`,
      C8-pengganti; S0+U-1–U-3+R-1–R-4+STOP lengkap; sitiran sh4:369-375
      TERVERIFIKASI dari `%TEMP%` harness; vonis tak tersentuh; H6 nihil) —
      SUDAH dieksekusi coder (lihat entri berikut)
- [x] Brief eksekusi coder fondasi-B DISUSUN 2026-10-09
      (`assistant/prompts/2026-10-09_eksekusi-fondasi-B-coder.md`;
      substansi arsitek verbatim U-1(b)/U-2/U-3/R-4 + 4 usulan asisten
      yang disetujui via paste) — SUDAH dipaste, laporan MASUK
- [x] Laporan coder fondasi-B MASUK + gerbang LOLOS 2026-10-09
      (`coder/hasil-telaah-fondasi-B.md`, 416 baris, blob `0284f5f0`;
      R-4 terverifikasi independen via hash-ulang `%TEMP%`; headline
      cocok; atribusi staged=2 diluruskan = T6 asisten-atas-perintah-user;
      vonis tak tersentuh) — menunggu arsitek baca via R-1–R-4
- [x] Brief disposisi fondasi-B FINAL disetujui user 2026-10-09
      (`assistant/prompts/2026-10-09_disposisi-fondasi-B-arsitek.md`) —
      SUDAH dipaste, disposisi MASUK (lihat entri berikut)
- [x] Fondasi-B TERTUTUP 2026-10-09 (`arsitek/disposisi-fondasi-B.md`,
      75 baris / 2881 B, blob `7d125022`, gerbang LOLOS;
      D-1/D-2/D-3 DISAHKAN, D-4 SELESAI; R-2 DIBUKA, filter tetap DILARANG)
- [x] Spec pra-registrasi H4b-stabilitas MASUK + gerbang LOLOS 2026-10-09
      (`arsitek/spesifikasi-H4b-stabilitas.md`, 108 baris, blob `0437b563`;
      lock dua-arah + anti-intip + guard P-5; tindak lanjut R-2 yang sah,
      bukan H6) — menunggu perintah "jalankan ronde coder H4b"
- [x] Brief eksekusi coder H4b DISUSUN 2026-10-09
      (`assistant/prompts/2026-10-09_eksekusi-H4b-coder.md`;
      substansi spec verbatim + 3 usulan asisten menunggu konfirmasi
      via paste) — menunggu user paste ke coder
- [x] Laporan coder H4b MASUK + gerbang LOLOS 2026-10-09
      (`coder/hasil-H4b-stabilitas.md`, 259 baris, blob `6410b180`;
      vonis mekanis GUGUR(H4b), tepat satu; R-4 terverifikasi independen;
      branch codex/ANN tanpa divergensi; atribusi staged diluruskan) —
      SELESAI dieksekusi; berikut auditor independen
- [x] Brief reaudit H4b DISUSUN 2026-10-09
      (`assistant/prompts/2026-10-09_reaudit-H4b-auditor.md`;
      A1–A7: replikasi nol + anti-intip + Off/lock + scope + karantina/
      cross-validasi + determinisme + integritas; 3 usulan asisten
      disetujui via paste) — SUDAH dipaste, laporan MASUK (lihat entri berikut)
- [x] Reaudit H4b SELESAI + gerbang LOLOS DENGAN CATATAN 2026-10-09
      (`Audit/reaudit-H4b-stabilitas.md`, 18199 B / 476 baris aktual,
      sha `3560bc05…`, blob `e3530477…`, TANPA self-hash; verdict LULUS
      DENGAN CATATAN — A1 COCOK / A2 COCOK+LOW-1 / A3 COCOK+ESK-1 /
      A4 COCOK / A5 SAH / A6 COCOK / A7 COCOK+LOW-2, 0 MEDIUM/HIGH;
      S0 8/8 cocok; staged=2 tak berubah; HEAD `e0b2b9f9` utuh) —
      berikut putusan arsitek H4b (ESK-1: kriteria (a) tak operatif)
- [x] Prompt onboarding CTO DISUSUN 2026-10-09
      (`assistant/prompts/2026-10-09_onboarding-CTO.md`) — menunggu user pakai
- [x] Brief putusan H4b FINAL disetujui user 2026-10-09
      (`assistant/prompts/2026-10-09_putusan-H4b-arsitek.md`) —
      SUDAH dipaste, putusan MASUK (lihat entri berikut)
- [x] H4b TERTUTUP 2026-10-09 (`arsitek/putusan-H4b-stabilitas.md`,
      119 baris / 5326 B, blob `fe11383b`, gerbang LOLOS;
      vonis resmi H4b: GUGUR; ESK-1 BEKUKAN+CATAT; LOW-1/LOW-2 tetap LOW;
      H4 TAHAN Batch-2 + H1/H2/H3/H5 untouched; H6+ DITOLAK)
- [x] Brief desain R-2 FINAL disetujui user 2026-10-09
      (`assistant/prompts/2026-10-09_desain-R2-arsitek.md`;
      S1 verbatim D-2/P-5/V-4/EKS-3 + S2 4 bahan + S0 8-hash + S-V(a)–(d)
      + S3/S4 + U-1–U-5 digabung) — SUDAH dipaste, spec MASUK
- [x] Spec R-2 MASUK + gerbang LOLOS 2026-10-09
      (`arsitek/spesifikasi-R2-stratifikasi.md`, 141 baris / 6849 B,
      blob `c04199ce`, TANPA self-hash; gate
      `assistant/verifications/2026-10-09_gerbang-spec-R2.md`,
      blob `3e8cd57a`; S0 8/8 + HEAD `e0b2b9f9` + staged 2 T6 COCOK)
- [x] Brief eksekusi coder R-2 FINAL disetujui user 2026-10-09, DITULIS ULANG
      atas perintah user (patuh AGENTS.md penuh + PROMPT_DISIPLIN Aturan 1-2:
      S-0 kontrak/S5/S20/S21/S26 + tiap syarat berpasangan perintah mentah +
      path penuh + resep sh4.py terverifikasi ada)
      (`assistant/prompts/2026-10-09_eksekusi-R2-coder.md`,
      blob `928a86d1`, 8413 B, ASCII/LF) —
      SUDAH dipaste, laporan MASUK (lihat entri berikut)
- [x] Laporan coder R-2 MASUK + gerbang LOLOS 2026-10-09
      (`coder/hasil-R2-stratifikasi.md`, 9811 B / 226 baris, blob `c2f79913`,
      TANPA self-hash; artefak `r2_hasil.json` sha `4664B4D8...E64A4`
      run1=run2=induk; angka JSON-di-disk == JSON-di-laporan == S-V(b) spec;
      vonis mekanis tepat satu GUGUR(R-2) tahun_gugur [2025]; gate
      `assistant/verifications/2026-10-09_gerbang-hasil-R2.md`,
      blob `381a5967`; HEAD `e0b2b9f9` + staged 2 T6 utuh) —
      berikut brief re-audit independen (lihat entri berikut)
- [x] Brief re-audit R-2 DISUSUN 2026-10-09
      (`assistant/prompts/2026-10-09_reaudit-R2-auditor.md`,
      blob `a8cc3e19`, 9707 B, ASCII/LF; A1-A7 adaptasi R-2 + larangan 1-12
      + U-1–U-3 digabung sah) —
      SUDAH dipaste, laporan MASUK (lihat entri berikut)
- [x] Re-audit R-2 SELESAI + gerbang LOLOS 2026-10-09
      (`Audit/reaudit-R2-stratifikasi.md`, 27235 B / 600 baris logis
      (LF 599, tailLF False) / ASCII/LF, sha `25E3C0E9…`,
      blob `24a929c7…`, TANPA self-hash; PUTUSAN AUDIT: GAGAL atas
      T-1 HIGH tunggal — gate lock jam spec :92-93 tak menggigit
      (`r2.py:86` konstanta-vs-literal; S1b top-6 data-uji + S2 range(24)
      lolos rc=0); A1 COCOK 26/26 + A6 byte-identik 3 JSON (angka penentu
      + verdict mekanis GUGUR(R-2) BENAR, dampak T-1 NOL); T-2/T-3/T-4 LOW;
      S0 + HEAD `e0b2b9f9` + staged 2 T6 COCOK; gate
      `assistant/verifications/2026-10-09_gerbang-reaudit-R2.md`) —
      berikut putusan arsitek R-2 (nasib gate + klarifikasi spec)
- [x] Brief putusan R-2 DISUSUN 2026-10-09
      (`assistant/prompts/2026-10-09_putusan-R2-arsitek.md`,
      blob `65c32a6c`, 9928 B / 173 baris, ASCII/LF/tailLF;
      S-2d 10-hash + S-V(a)-(e) + V-1 vonis resmi + V-2 disposisi T-1 HIGH
      dua opsi + V-3 T-2/T-3/T-4 + V-4 anti-merambat) —
      SUDAH dipaste, putusan MASUK (lihat entri berikut)
- [x] R-2 TERTUTUP 2026-10-09 (`arsitek/putusan-R2-stratifikasi.md`,
      143 baris / 7697 B, blob `c92733fd`, sha `81F40E0B…`,
      TANPA self-hash, ASCII/LF/tailLF; gerbang LOLOS
      `assistant/verifications/2026-10-09_gerbang-putusan-R2.md`;
      vonis resmi GUGUR(R-2); V-2 opsi (ii) TERIMA DENGAN CATATAN
      (pola assert-konstanta PENSIUN, pengganti mengikat +
      S1b/S2 wajib rc non-0); V-3 T-2/T-3/T-4 TUTUP catatan +
      klarifikasi T-3 mengikat; V-4 anti-merambat penuh;
      H4 Batch-2/H1-H3/H5/H4b/fondasi-B untouched; H6 DITOLAK)
- [ ] Compaction agresif (15–20%): diagnosis + opsi solusi diajukan,
      menunggu keputusan user (opsi A sentuh config global)
- [x] EDA-07 I-2 SELESAI 2026-10-12 (coder): full-run G1-G4 + 7 kandidat via
      `scripts/_build_eda07_i2.py` -> `notebooks/scalping/eda_07_i2.ipynb`
      (22 sel, 21 tereksekusi, 0 error; exit=0). Regresi 86/86 + 780/780 PASS;
      native 98 LOLOS/162 GUGUR; kandidat 5 LOLOS-invers (Tokyo) + 2 GUGUR
      (London); T-07 x4 + FIG-13..16 + KESIMPULAN_I2; 13/13 beku untouched.
      Laporan `reports/eda/2026-10-12/laporan-coder-eda07-i2.md`.
      Berikutnya: AUDITOR independen, arsitek putusan Lapisan 3.

- [x] EDA-07 L3-0 SELESAI 2026-10-12 (coder): peta arah deskriptif via
      scripts/_build_eda07_l30.py ->
otebooks/scalping/eda_07_l30_arah.ipynb
      (8 sel, 7 tereksekusi, 0 error; exit=0; tanpa RNG).
      T-L3-0_arah.csv 153 (pos 120/neg 33) + T-L3-0_peta98.csv 98
      (pos 78/neg 20, diff kosong) + FIG-17 + manifest 6/6 + runner-log;
      5 Tokyo negatif eksak (INVERS); 2 baris kandidat London G3=False
      (targetnya LOLOS via wakil asli rv15/rv60 pos); K24 24/24;
      ASSERT_LOG 343; file beku untouched (penjaga 260/6767/1315/1335/86).
       Laporan
eports/eda/2026-10-12/laporan-coder-eda07-l30.md.
       Berikutnya: AUDITOR independen L3-0, arsitek putusan buka L3-1.
- [x] EDA-07 L3-1 STOP pra-eksekusi 2026-10-12 (coder): S-0 read-only menemukan
      konflik B-3 mengikat — M3 (Brier+akurasi+mayoritas, sama-untuk-semua,
      tanpa-pengecualian, 103 DILARANG tambah/kurang) tak terdefinisi untuk
      36 pasangan kontinu LB_rng (34 native + 2 Tokyo; YCODE/YPOS=None verbatim
      run 9, T-07-1 kelas=kontinu). Alternatif binarisasi/drop/MSE Renaming
      semua melanggar klausul (label-baru/ubah-M3/pengecualian). STOP + lapor
      per S-0.4; nol artefak M3 ditulis. Laporan
       `reports/eda/2026-10-12/laporan-coder-eda07-l31-konflik-B3.md`.
       Berikutnya: AMANDEMEN ARSITEK B-3 (aturan per-jenis LB_rng atau
       persempit scope + kunci normalisasi Brier multikelas), baru brief
       coder L3-1-revisi. HEAD `b18992b`, staged nol ronde ini.
- [x] EDA-07 L3-1 SELESAI 2026-10-12 (coder, pasca-Amandemen C):
      `scripts/_build_eda07_l31.py` -> `eda_07_l31_baseline.ipynb`
      (8 sel, 0 error, EXIT=0, ASSERT_LOG 1268). TABEL M3 103:
      LOLOS 68/GUGUR 35 (diskret 56/11 Brier, kontinu 12/24 MSE);
      jangkar 200/200, register 98+5, C-3 twin identik, split tak-bocor,
      hash 5/5, S8B 11/11. 3 perbaikan builder terdokumentasi di laporan.
      Laporan `reports/eda/2026-10-12/laporan-coder-eda07-l31.md`.
      HEAD `b18992b`, staged nol ronde ini.
- [x] Re-audit L3-1 SELESAI + gerbang LOLOS 2026-10-13
      (`Audit/reaudit-l31.md`, 452 baris / 24728 B, SHA256 `B091A4FC...`,
      LOLOS PROSEDURAL; 11 mandat nol selisih; 0/0/4/2; R1 TERIMA catatan
      log; R3 asumsi EOL-manifest jadi FAKTA; S6 jujur 6 butir; gate
      `assistant/verifications/2026-10-13_gerbang-reaudit-l31.md`) —
      berikut VONIS BINER B-4 arsitek (lihat entri berikut)
- [x] Brief vonis B-4 DISUSUN 2026-10-13
      (`assistant/prompts/2026-10-13_putusan-l31-arsitek.md`;
      V-1 biner GO/NO-GO + V-2 register + V-3 R1-R4 + V-4 pagar T-5/S8A;
      GO = minta izin user utk spec pemodelan, BUKAN paper-trade) —
      menunggu user paste ke arsitek
- [x] VONIS B-4 SELESAI 2026-10-13 (arsitek dirangkap asisten, S1A;
      brief eksternal MOOT): `arsitek/putusan-l31-final.md`
      (81 baris, blob `dfc20e6d`, SHA256 `EA1BC4FD...`, ASCII/LF;
      S-2d 5 blob COCOK + HEAD/staged bersih) — V-1 GO cabang (a)
      = minta izin user utk spec pemodelan pra-registrasi (BUKAN
      paper-trade; 5 syarat mengikat incl. skrutini LB_bin 25/25);
      V-2 register 68 beku / 35 tutup; V-3 R1-R4 + I1-I4; V-4 T-5/S8A.
      Ronde L3 DITUTUP. Menunggu: persetujuan eksplisit user.
