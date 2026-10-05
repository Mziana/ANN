# STATE.md — Status Saat Ini

**Update terakhir:** 2026-10-05
**Fase:** Fase B (Data) — pipeline data berjalan
**Progress keseluruhan:** ~60%

## Ringkasan Eksekutif

Semua checkpoint (01, 05-09d) **SUDAH SELESAI**. State file lama menandai
sebagian besar sebagai belum — itu sudah usang dan sudah dikoreksi di sini.
Environment siap, MT5 terhubung, data historis terbukti tersedia.
**`src/` sudah berisi logika: 1.276 baris** (`fetch_data.py` 349,
`validate_data.py` 543, `clean_data.py` 319, `utils/config.py` 65).

## Yang Sedang Dikerjakan

- **Data 2023-2026 ter-fetch**: 1.347.847 bar M1 total (4 file di `data/raw/M1/`).
- **KESIMPULAN DST: broker TIDAK ikut DST. Offset tetap `Etc/GMT-3` untuk 2023-2026.**
- **Validasi data LOLOS**: 0 error, 5 peringatan di 4 tahun.
- **Pembersihan data SELESAI**: `data/processed/M1/*.parquet`, 1.349.857 bar.
- Berikutnya: `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1).

## Yang Sudah Selesai

- [x] Checkpoint 01: Struktur folder
- [x] Checkpoint 05: State files
- [x] Checkpoint 06: scripts (verify_claims.py, check_state.py, pipeline.ps1)
- [x] Checkpoint 07: configs (requirements, pyproject, pre-commit, configs/*.yaml)
- [x] Checkpoint 08: setup.ps1 + run.ps1
- [x] Checkpoint 09a-09d: AGENTS v3.0, RULES v2.0, PROMPTS v2.0, CONTEXT, configs+jurnal+backtest
- [x] Setup environment: venv Python 3.12.8, 134 paket (MetaTrader5 5.0.6231, torch 2.4.0, pandas 2.2.3)
- [x] Git init + 2 commit + pre-commit hook terpasang
- [x] Struktur jurnal lengkap (header CSV 29 kolom)
- [x] Struktur backtest per tanggal + template audit 8 section
- [x] **Onboarding AI baru (Prompt 0 / AGENTS.md §24)** — inventarisasi + verifikasi
- [x] Verifikasi broker: simbol `USDJPY`, timezone UTC+3, data 3,75 tahun (1.348.135 bar M1)
- [x] **Phase A (task 1-5) SELESAI**: state files, `broker_timezone` UTC+3, hapus BOM 27 file,
      `.gitattributes`, ruff-only, docstring Google Style, `docs/PROJECT_MAP.md`
- [x] Gate pre-commit dibetulkan: hook `mixed-line-ending` dihapus (tabrak `.gitattributes`),
      `pytest-quick` -> `scripts/run_tests.py` (toleran exit 5). `pre-commit run --all-files` 11/11 hijau
- [x] **Phase B (task 6): `src/data/clean_data.py`** — raw CSV -> Parquet,
      1.347.847 -> 1.349.857 bar (2.010 gap kecil terisi = 0,1489%).
      Duplikat 0, OHLC diperbaiki 0, break & akhir week's TIDAK pernah diisi.
      Kolom baru `is_filled` menandai setiap bar sintetis. Audit independen
      14 check x 4 tahun = semua lolos. 103 test hijau.
- [x] **Bug `.asi8` pandas 3.x ditemukan & diperbaiki** — `datetime64[s].asi8`
      menghitung detik, bukan nanosekon, sehingga kolom epoch jadi `1` semua.
      Fix `as_unit("ns")` + tes regresi `test_epoch_values_are_real_seconds`.
- [x] Hook pre-commit lokal sekarang jalan dengan interpreter venv lewat
      `cmd /c "scripts\run_hook.bat" ...`. Sebelumnya pakai Python 3.14 sistem
      (tanpa pyarrow) sehingga 2 tes parquet selalu gagal.
- [x] **Perbaikan 8 temuan audit Phase B** (fetch_data + validate_data):
      import MT5 jadi lazy (`import_mt5()`, `timeframe_constant()`) — kedua modul
      kini import-able tanpa MetaTrader5 terpasang; `check_spread` benar-benar
      membandingkan p99 vs `spread.by_year` (2023 jadi WARN, sebelumnya selalu
      LOLOS); `KNOWN_ANOMALY_WINDOWS` pindah ke config; `print` + stderr +
      `logger`; `trading_days` pakai logika sesi. 120 test hijau.
- [x] **5 temuan audit DIBATALKAN** atas bukti data: C-02, H-02, H-03, H-04,
      L-02. Detail pembatalan ada di `SESSION_LOG.md`.
- [x] **Keputusan user atas Q1/Q2/Q3 diimplementasikan** (2026-10-05):
      `validate_data.py` tetap 543 baris dengan `# EXCEPTION` yang diperbaiki
      (jujur soal komposisi baris) + 3 batas keras (>600 baris / fungsi publik
      baru / akhir Milestone 1); `check_bar_count` tetap `dt.date` dengan
      docstring yang menjelaskan kenapa berbeda dari `trading_days`; `black==24.10.0`
      dihapus dari `requirements.txt`; pyproject TIDAK disentuh; `CHANGELOG.md`
      diisi; catatan usang `check_foreign_chars.py` di TASKS.md dibersihkan.

## Yang Belum

- [x] Phase B: `src/data/fetch_data.py` + `src/utils/config.py` + `__init__.py` + 22 test
- [x] Test 1 bulan (2026-10-01 s/d 10-06) → 3.134 bar, **7/7 verifikasi LOLOS**
- [x] Fetch full 2023-01-01 s/d 2026-10-05 -> 1.347.847 bar M1
- [x] `src/data/validate_data.py` (cek gap, baris, offset historis)
- [x] `src/data/clean_data.py` (raw -> Parquet + flag `is_filled`)
- [ ] `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1) — berikutnya
- [ ] **Akhir Milestone 1**: pecah `validate_data.py` (543 baris) jadi check vs
      render — batas keras dari user, bukan opsional lagi
- [ ] Modul `src/features/`: build_features.py, build_labels.py
- [ ] Modul `src/models/`, `src/backtest/`
- [ ] EDA (distribusi return, volatilitas per sesi, regime)
- [ ] Pemilihan metode strategi (menunggu EDA)
- [ ] Backtest + audit
- [ ] 500+ trade data (kriteria Fase 1)

## Blocker

- Tidak ada blocker eksternal.
- MT5 terminal terhubung (`connected=True`), simbol dan history data terbukti tersedia.
- `trade_allowed=False` — akun belum login untuk trading (tidak menghalangi fetch data).

## Keputusan Terverifikasi (2026-10-05)

| Keputusan | Nilai | Bukti |
|---|---|---|
| Simbol MT5 | `USDJPY` (bukan `USDJPYm`) | `symbols_get()` 82 simbol, `USDJPYm` absen |
| Timezone broker | **UTC+3** (`Etc/GMT-3`) | tick 05:58:13 vs UTC 02:58:06 -> +3.0019 jam; bar 05:58:00 -> +2.9983 jam |
| Offset historis broker | **TERVERIFIKASI: tetap +3, tanpa DST** | 40 dari 47 bulan break jam dinding 4; 2 anomali terisolasi (Okt-Nov 2024, Mar 2026), tidak berulang tahunan |
| 1 pip USDJPY | 0.01 | `digits=3`, `point=0.001` |
| Spread live | 0,8 pip | tick 157.851 / 157.859 |
| Pipeline order | M1 dulu, 1 TF, verifikasi, baru expand | diputuskan user 2026-10-05 |
| Format simpan | CSV per tahun: `usdjpy_m1_<year>.csv` | diputuskan user 2026-10-05 |
| Spread per tahun | `by_year`: 2023=3,0 · 2024-2026=1,5 | p99 2023 = 8,5 pip vs 1,2-1,7 tahun lain |
| Total data | **1.347.847 bar M1** (2023-2026) | jumlah file = jumlah `copy_rates_range` awal |

## Langkah Berikutnya

1. **`src/data/clean_data.py`** — raw -> `data/processed/M1/`, raw tidak diubah.
2. `src/data/resample.py` (M1 -> TF lain) — setelah clean.
3. EDA.

## Aturan Pipeline (2026-10-05)

- **Raw immutable.** `data/raw/` tidak pernah ditulis ulang.
- Processed = Parquet di `data/processed/M1/`.
- Kalau `validate_data.py` jadi panjang, pecah jadi logika check vs render.

## Format Kode (KEGIATAN 2026-10-05)

- **Ruff saja.** Black dihapus dari `.pre-commit-config.yaml` dan
  `[tool.black]` dari `pyproject.toml`. Dua formatter bisa saling menimpa.
- `.gitattributes`: `* text=auto eol=lf`, `*.ps1`/`*.bat` `eol=crlf`,
  biner (`png`/`jpg`/`parquet`) `binary`.
- Gate: `ruff check` + `ruff format --check` keduanya hijau.
- Line ending: 38 file teks LF, 3 file `.ps1` CRLF.

## Peringatan Waktu Broker (WAJIB)

Timestamp dari `mt5.copy_rates*` = **waktu broker UTC+3**, BUKAN UTC.
Wajib dikonversi saat fetch. Jika tidak, session Tokyo/London/NY salah
dan berpotensi look-ahead di boundary bar.
