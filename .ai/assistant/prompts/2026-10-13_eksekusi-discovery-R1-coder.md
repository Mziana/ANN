# Brief Eksekusi Discovery 2024 — Coder Eksternal (2026-10-13)

## Otoritas
Satu-satunya otoritas = spec
`reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R1.md`
(status SPEC EKSEKUSI + AMANDEMEN-1 + AMANDEMEN-2). Brief ini turunan;
bila bertentangan dengan spec, spec menang — laporkan konflik,
jangan improvisasi.

## Tugas: SATU — discovery di 2024 saja
1. Tulis LEDGER pra-run (D-4.1 + A-C1 + A-C5): kolom wajib §9.1 +
   seed bootstrap `1337` + kunci config spread literal yang dipakai +
   verifikasi `src/data/resample.py`. Ledger + manifest hash (SHA-256)
   masuk `reports/research/2026-10-13/discovery-R1/evidence/`
   SEBELUM run pertama. Tanpa ini = run gagal.
2. Petakan event E1 (6 sel, D-1) + E2 (1 sel) + E3 (1 sel) di 2024,
   KELUARKAN jendela anomali 2024-10-28..11-01 dari denominator.
3. Kontrak eksekusi: entry = OPEN bar t0+1; horizon dari t0 close;
   BUY entry ASK exit BID / SELL entry BID exit ASK; spread nol
   dilarang; mid dilarang; AMBIGUOUS_SEQUENCE = buang + hitung
   eksplisit (D-3.1/D-3.2).
4. Biaya 3 lapis per event (D-3.3 + Amandemen-1): observed =
   `spread.cost_basis.by_session` (+ komisi 0,3 pip round-turn asumsi
   per-side); conservative = observed + slippage 0,2 (ASUMSI);
   stress = `spread.stress_bands.p95.by_session` + slippage 0,3
   (ASUMSI) + komisi. `spread.default`, `by_year`, `stress_multiplier`
   DILARANG.
5. Hitung Q0 dulu (gerbang kapasitas: sel < 300 event = dropped, tidak
   dinilai), lalu Q1 (semua horizon dipetakan; evaluasi hanya H+10),
   Q2 (ladder dipetakan; evaluasi hanya TP2,5/SL2,5), Q3 (tanpa
   rv_regime_flag/TAU; tanpa M15), Q4 failure map (wajib), Q5
   paruh-2024 (tanda H1 vs H2).
6. Kriteria KANDIDAT (D-4.4, 4-syarat, setting beku H+10/TP2,5/SL2,5/
   observed net): (i) pooled median > 0; (ii) CI 95% bootstrap
   cluster-hari 10.000 resample seed 1337 mengecualikan 0 positif;
   (iii) tanda sama 2024-H1/H2; (iv) failure map lengkap. Coder
   MELAPORKAN angka per sel + vonis sementara per keluarga
   (TOLAK/KANDIDAT/BELUM JELAS); vonis final = arsitek.
7. Lampiran D-8: hitung 8 pola + bias M15 (definisi D-8.1/D-8.2,
   resample via `src/data/resample.py`), lalu SEGEL — jangan dibuka,
   jangan dibaca untuk keputusan, jangan dilampirkan kesimpulannya
   sebelum vonis KANDIDAT beku (A-C4).

## Keluaran (sebelum auditor mulai)
- Ledger + manifest hash + script/harness + JSON event-level
  (kolom minimum D-3.4) + stdout, semua di folder evidence di atas.
  Logging gagal = run gagal.

## Larangan (pelanggaran = run gagal)
Tanpa 2025 / 2023-H2 / 2026; tanpa tuning threshold/horizon/barrier;
tanpa keluarga ke-4; tanpa indikator (RSI/MACD/EMA/nama-candle);
tanpa M15 di evaluasi; tanpa buka segel lampiran; tanpa uji p-value
untuk seleksi; tanpa `except: pass`; tanpa `print()` produksi bila
kode Python (pakai logging); fungsi < 50 baris, file < 400 baris.

## Format pulang
Laporan §5 AGENTS.md (file dibuat/diubah, tabel Klaim & Bukti,
yang belum diverifikasi, potensi masalah, saran). Satu ronde satu
vonis: tidak ada "sekalian coba varian".
