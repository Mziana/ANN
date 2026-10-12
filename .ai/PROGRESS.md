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

### Update 2026-10-12 (EDA-07 I-2 selesai, coder)

- [x] Full-run I-2 (mandat V-6): 260 pasangan (60 LA + 200 waktu), verdict
      G1-G4 penuh fitur asli = 98 LOLOS / 162 GUGUR; irisan 29/37;
      regresi kontrol 86/86 + 780/780 identik beku; 7 kandidat round_d V-5
      dinilai (5 LOLOS Tokyo efek INVERS + 2 GUGUR London, G4=NA);
      T-07-1..4 + FIG-13..16 + KESIMPULAN_I2 terkunci (ASSERT_LOG 569);
      13/13 file beku hash sama; HEAD `b18992b`, nol stage/commit.
      Laporan `reports/eda/2026-10-12/laporan-coder-eda07-i2.md`.
      Berikutnya: AUDITOR independen, arsitek putusan Lapisan 3.

### Update 2026-10-12 (EDA-07 L3-0 selesai, coder)

- [x] Peta arah L3-0 (S3-1 deskriptif, tanpa model): 153 baris G3-pass
      (120 pos/33 neg) -> T-L3-0_arah.csv + FIG-17 per sesi x horizon;
      98 LOLOS native (verdict verbatim) -> T-L3-0_peta98.csv
      (arah pos 78/neg 20, diff himpunan kosong); 5 Tokyo INVERS menempel;
      2 kandidat London gugur sbg round_d (target LOLOS via wakil asli);
      manifest hash 6/6 + runner-log EXITCODE=0; KESIMPULAN_L30 terkunci
      (ASSERT_LOG 343); beku untouched. Laporan
eports/eda/2026-10-12/laporan-coder-eda07-l30.md.
      Berikutnya: AUDITOR independen L3-0, arsitek putusan buka L3-1.

### Update 2026-10-12 (EDA-07 L3-1 STOP pra-eksekusi, coder)

- [x] S-0 read-only -> konflik B-3: M3 Brier+akurasi+mayoritas tak terdefinisi
      untuk 36/103 pasangan kontinu LB_rng (YPOS/YCODE=None verbatim run 9).
      STOP + lapor per S-0.4; nol artefak M3. Laporan
      `laporan-coder-eda07-l31-konflik-B3.md`. Berikutnya: AMANDEMEN ARSITEK B-3.

### Update 2026-10-12 (EDA-07 L3-1 SELESAI, coder)

- [x] Eksekusi L3-1 pasca-Amandemen C via `scripts/_build_eda07_l31.py` ->
      `notebooks/scalping/eda_07_l31_baseline.ipynb` (8 sel, 0 error, EXIT=0).
      TABEL M3 103 pasangan terkunci: LOLOS 68 / GUGUR 35 (diskret 56/11 via
      Brier; kontinu 12/24 via MSE). Jangkar T-07-1 200/200; register 98+5;
      C-3 twin 5 round_d identik native; split max-train<min-test; hash 5/5
      input sama; S8B 11/11 utuh; ASSERT_LOG 1268; KESIMPULAN_L31 terkunci.
      3 perbaikan builder terdokumentasi (FIG-18 kolom, `)` berlebih, C-3 twin
      posisi-register). T-5 menandai 12 baris / 7 target. FIG-18 dua panel.
      Laporan `reports/eda/2026-10-12/laporan-coder-eda07-l31.md`.
      HEAD `b18992b`, staged nol ronde ini.
      Berikutnya: AUDITOR independen L3-1, arsitek putusan + vonis dagang.

### Update 2026-10-13 (reaudit L3-1 LOLOS PROSEDURAL + brief vonis B-4)

- [x] Reaudit L3-1 LOLOS (B091A4FC, 452 baris dibaca penuh):
      11 mandat (a)-(k) nol selisih; 0 TINGGI/0 MENENGAH/4 RENDAH
      (format, nol dampak)/4 INFORMATIF; R1 TERIMA catatan log;
      R3 asumsi EOL-manifest jadi FAKTA reproducible; S6 jujur.
      Gerbang LOLOS (`2026-10-13_gerbang-reaudit-l31.md`).
- [x] Brief vonis B-4 arsitek terbit
      (`2026-10-13_putusan-l31-arsitek.md`, V-1 biner + V-2 + V-3 + V-4).
      Menunggu user paste -> `putusan-l31-final.md` -> GO/NO-GO (S8A).

### Update 2026-10-13 (VONIS B-4: GO cabang (a), ronde L3 DITUTUP)

- [x] Vonis arsitek (dirangkap asisten, S1A; brief eksternal MOOT):
      `arsitek/putusan-l31-final.md` (81 baris, SHA256 `EA1BC4FD...`).
- [x] V-1 GO = minta persetujuan user utk spec pemodelan
      pra-registrasi (BUKAN paper-trade; 5 syarat incl. skrutini
      LB_bin 25/25). V-2 register 68 beku / 35 tutup.
- [ ] Menunggu persetujuan eksplisit user (S8A butir 3) sebelum
      ronde spec pemodelan.
