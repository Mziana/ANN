# PROGRESS.md — Milestone

**Update terakhir:** 2026-10-05

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
