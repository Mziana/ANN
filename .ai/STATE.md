# STATE.md — Status Saat Ini

**Update terakhir:** 2026-10-05
**Fase:** Setup Fondasi (Fase 0) — transisi ke Fase 1 (Data)
**Progress keseluruhan:** ~55%

## Ringkasan Eksekutif

Semua checkpoint (01, 05-09d) **SUDAH SELESAI**. State file lama menandai
sebagian besar sebagai belum — itu sudah usang dan sudah dikoreksi di sini.
Environment siap, MT5 terhubung, data historis terbukti tersedia.
**Hambatan utama sekarang: `src/` masih kosong — nol baris logika.**

## Yang Sedang Dikerjakan

- **Data 2023-2026 ter-fetch**: 1.347.847 bar M1 total (4 file di `data/raw/M1/`).
- **KESIMPULAN DST: broker TIDAK ikut DST. Offset tetap `Etc/GMT-3` untuk 2023-2026.**
- Menunggu konfirmasi user sebelum commit.

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

## Yang Belum

- [x] Phase B: `src/data/fetch_data.py` + `src/utils/config.py` + `__init__.py` + 22 test
- [x] Test 1 bulan (2026-10-01 s/d 10-06) → 3.134 bar, **7/7 verifikasi LOLOS**
- [ ] **Fetch full 2023-01-01 s/d 2026-10-05** (menunggu approval user)
- [ ] `src/data/validate_data.py` (cek gap, baris, offset historis)
- [ ] Modul `src/data/`: clean_data.py, validate_data.py, resample.py
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
| Total data | **1.347.847 bar M1** (2023-2026) | jumlah file = jumlah `copy_rates_range` awal |

## Langkah Berikutnya

1. **Phase B: `src/data/fetch_data.py`** — M1 per tahun, simpan `broker_time_raw`.
2. Tambah `__init__.py` untuk subpackage `src/data/`.
3. `tests/test_fetch_data.py` — min 3 test, tanpa API live.
4. `validate_data.py` — cek gap, baris, offset historis vs anchor UTC.
5. EDA.

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
