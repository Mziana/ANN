# TASKS.md — Task Board

**Update terakhir:** 2026-10-05

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
- [ ] `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1) — berikutnya
- [ ] `src/features/build_features.py`
- [ ] `src/features/build_labels.py`

### Catatan clean_data

- Output `data/processed/M1/*.parquet` sudah dibuat: 1.349.857 bar.
  Folder ini di-gitignore, jadi reproducible dari raw.
- Kolom `is_filled` WAJIB dipakai `resample.py` dan `build_features.py`.
  Bar sintetis tidak boleh diperlakukan sebagai bar dagangan.
- **BUTUH KEPUTUSAN USER**: 90 dari 946 lubang (9,5%) adalah lubang 8-9 menit
  di broker 02:58-03:07, tepat sebelum pembukaan pasar. Modul mengisinya
  karena < 20 menit, tapi itu bar pra-pembukaan yang sebenarnya tidak pernah ada.
  Pertimbangkan sebelum resample.

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
