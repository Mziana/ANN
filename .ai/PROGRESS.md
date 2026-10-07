# PROGRESS.md — Milestone

**Update terakhir:** 2026-10-07

## Milestone 0: Setup Fondasi — SELESAI (100%)

- [x] Struktur folder
- [x] State files
- [x] Scripts (verify_claims.py, check_state.py, pipeline.ps1)
- [x] Configs (data.yaml, paths.yaml, logging.yaml, pyproject, requirements)
- [x] Setup.ps1 + run.ps1
- [x] Pre-commit hooks terpasang
- [x] AGENTS.md v3.0
- [x] RULES.md v2.0
- [x] PROMPTS.md v2.0
- [x] CONTEXT.md v1.3
- [x] Struktur jurnal + backtest
- [x] Environment (venv Python 3.12.8, 134 paket)
- [x] Git init + commit

## Milestone 0.5: Perbaikan Rumah (Phase A) — SELESAI

- [x] Fix `broker_timezone` -> UTC+3 di `configs/data.yaml`
- [x] Hapus BOM UTF-8 dari 27 file (0 tersisa)
- [x] Docstring Google Style untuk fungsi publik `verify_claims.py` + `check_state.py`
- [x] `.gitattributes` (text=auto eol=lf, ps1/bat crlf, biner)
- [x] Black dihapus, hanya ruff + ruff-format
- [x] Buat `docs/PROJECT_MAP.md`

## Milestone 1: Data Pipeline

- [x] Fetch data MT5 M1 per tahun -> `data/raw/M1/usdjpy_m1_<year>.csv`
- [x] Validasi data (gap, jumlah baris, duplikat, OHLC, spread) — **LOLOS 4 tahun**
- [ ] Clean data -> `data/processed/M1/` (Parquet)
- [ ] Simpan Parquet ke `data/processed/M1/` (menunggu clean_data.py)
- [ ] Resample M1 -> M5/M15/M30/H1/H4/D1 (setelah M1 tervalidasi)

## Milestone 2: Eksplorasi (EDA)

- [ ] Distribusi return
- [ ] Volatilitas per sesi (Tokyo/London/NY)
- [ ] Karakter per regime
- [ ] Pengukuran spread aktual per sesi (isi `configs/data.yaml`)

## Milestone 3: Metode

- [ ] Hipotesis dari EDA
- [ ] Uji kandidat
- [ ] Pilih metode (TIDAK sebelum EDA selesai)

## Milestone 4: Baseline Model

- [ ] Rule-based
- [ ] Logistic regression

## Milestone 5: ANN

- [ ] MLP
- [ ] Walk-forward validation

## Milestone 6: Backtest

- [ ] Spread + slippage + komisi (WAJIB, tanpa itu tidak valid)
- [ ] Bid/ask handling benar (RULES.md §18.16)
- [ ] Stress test

## Milestone 7: Paper Trading (Fase 1)

- [ ] 500+ trade data

## Milestone 8: Graduation (Fase 2)

- [ ] 100 trade simulasi limit

## Milestone 9: Live (Fase 3)

- [ ] Modal kecil

## Kemajuan Fase B — Data (per 2026-10-05)

- [x] Fetch MT5 M1 2023-2026 -> 1.347.847 bar CSV (raw, immutable)
- [x] `fetch_data.py` — timezone UTC+3, spread POINT vs PIP, epoch mentah
- [x] `validate_data.py` — 0 error, 5 peringatan, 4 tahun
- [x] `clean_data.py` — Parquet 1.349.857 bar, 2.010 gap kecil terisi
- [ ] `resample.py` — M1 -> M5/M15/M30/H1/H4/D1

Regresi: 103 test hijau. Gate `pre-commit run --all-files` 12/12.

### Update 2026-10-05 (audit Phase B)

- [x] 8 temuan diperbaiki, 5 dibatalkan atas bukti data
- [x] Validasi data nyata: exit 0, 2023 kini WARN karena spread p99 8,50 pip
- [x] 120 test hijau, pre-commit 12/12

### Update 2026-10-07 (batch newline + M1 + commit)

- [x] F-NL + F-NL2 ×5 builder, regen nb05 (81.851 B, 0 CR, 68/68 assertion),
      FIG-04..07 hash identik pin, diff ternormalisasi kosong + 9 baris chunking
      terdisposisi
- [x] Re-audit F-NL/F-NL2 TERVERIFIKASI TUTUP; temuan baru M1 (MEDIUM,
      provenance "era CRLF" salah kausal) diperbaiki ×4 dokumen + re-audit
      TERVERIFIKASI TUTUP
- [x] Commit `43e2a07` (37 file, semua hook hijau); Batch C: 0 MEDIUM + 4 LOW
      terbuka (B8-01/B10-01 dikecualikan, L2-01/L2-02 catatan)

### Update 2026-10-07 (penguncian hipotesis H1–H5)

- [x] Review redaksi H1→H5 oleh user (H1 ditahan untuk tanya arsitek
      reversal-day → putusan opsi iii: kunci + catat risiko + klausul
      anti-penyelamatan)
- [x] Putusan arsitek: H1 KUATKAN, H2–H5 TERIMA bersyarat S1–S8
      (H3 vonis TERBUKA sampai S4; H2 pra-registrasi strategi; H4 dua "6 jam"
      terpisah; H5 koreksi multiplicity), H6+ DITOLAK
- [x] Dokumen `hipotesis_lock_v1.md` + `putusan-arsitek-H1-H5.md`;
      commit `0107a56` (2 file, semua hook hijau)

### Update 2026-10-07 (fondasi fitur B1 + rantai audit TERTUTUP)

- [x] `build_features.py` 400/400 + 37 test, parquet `07402f40…` identik objek
      audit; audit fondasi 0 HIGH/1 MEDIUM/3 LOW → putusan arsitek B1 + F-1
      tersimpan → F-2/F-3/F-4 → re-audit → R1/R2/R3 → konfirmasi 3×YA
- [x] Residual berdiri: #4/#5/#7 + materialitas H1/H5 (BELUM DIUJI);
      headroom nol → B2 wajib buka dengan rencana split
