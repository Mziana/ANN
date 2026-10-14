# Brief Eksekusi Discovery 2026-Holdout — Coder Eksternal (2026-10-13)

## Otoritas + PRASYARAT
Satu-satunya otoritas = spec
`reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R2.md`
(status SPEC EKSEKUSI + Amandemen-R2-1). Brief ini turunan; bila
bertentangan dengan spec, spec menang — laporkan konflik, jangan
improvisasi.
**PRASYARAT: brief ini BARU boleh dijalankan setelah re-audit fokus
auditor atas Amandemen-R2-1 = LULUS.** Tanpa itu = run gagal.

## Tugas: SATU — discovery di 2026-holdout saja
1. Tulis LEDGER pra-run (D2-7): salin batas paruh-1/paruh-2 dari
   spec (2026-01-01..05-18 / 2026-05-19..10-02 — salin, bukan
   hitung-ulang) + seed bootstrap `1337` + kunci config spread
   literal yang dipakai + skala ATR-2026 terukur (mean ATR M5(14),
   SL/TP point Buck) + cakupan sesi-2026 + verifikasi
   `src/data/resample.py`. Ledger + manifest hash (SHA-256) masuk
   `reports/research/2026-10-13/discovery-R2/evidence/` SEBELUM run
   pertama. Tanpa ini = run gagal.
2. Petakan event E1 (6 sel) + E2 (1 sel) + E3 (1 sel, definisi R1
   D-1 verbatim) di 2026, KELUARKAN anomali 2026-03-10..03-27 dari
   denominator. Usable ≈ 250.727 bar.
3. Barrier ATR (D2-2 + Amandemen-R2-1 C1): ATR = ATR M5(14) pip dari
   bar M5 terakhir selesai ≤ t0, DIBEKUKAN saat entri; SL = 1,5xATR,
   TP = 2,0xSL; SATU paket, tanpa ladder. Entry DIBUANG bila ATR tak
   tersedia / jendela menyeberangi gap / anomali / sesi Off — nol
   imputasi, jumlah buang dilaporkan.
4. Kontrak eksekusi (D2-5): entry OPEN bar t0+1; horizon dari t0
   close; BUY ASK→BID / SELL BID→ASK; spread nol dan mid dilarang;
   first-passage pada bar SESUDAH bar entry (bar entry
   dikecualikan); bar-kembar SL+TP = AMBIGUOUS_SEQUENCE buang +
   hitung eksplisit.
5. Biaya 3 lapis per event (D2-4): observed =
   `spread.cost_basis.by_session` (+ komisi 0,3 pip round-turn asumsi
   per-side); conservative = observed + slippage 0,2 (ASUMSI);
   stress = `spread.stress_bands.p95.by_session` + slippage 0,3
   (ASUMSI) + komisi. `spread.default`, `by_year`,
   `stress_multiplier` DILARANG. Sesi-2026 tak terpetakan: fallback
   `cost_basis.default` + laporkan, bukan diam-diam.
6. Hitung Q0 dulu (gerbang kapasitas: sel < 300 event = dropped,
   tidak dinilai; E3 < 300 = GUGUR-dilaporkan), lalu Q1 (semua
   horizon dipetakan; evaluasi HANYA H+10 — horizon lain tidak boleh
   mengangkat kandidat), Q2 (SATU paket ATR, tanpa ladder), Q3 (tanpa
   RV/TAU; tanpa M15), Q4 failure map (wajib), Q5 paruh-2026.
7. Kriteria KANDIDAT (D2-6, 4-syarat, PADA SETTING BEKU H+10/paket
   ATR tunggal/observed net): (i) pooled median > 0; (ii) CI 95%
   bootstrap cluster-hari 10.000 resample seed 1337 mengecualikan 0
   positif; (iii) tanda sama paruh-1/paruh-2 2026; (iv) failure map
   lengkap. Coder MELAPORKAN angka per sel + vonis sementara per
   keluarga (TOLAK/KANDIDAT/BELUM JELAS); vonis final = arsitek.
8. Lampiran D-8 R2: hitung-ulang 8 pola + bias M15 di 2026
   (definisi R1 D-8.1/D-8.2, resample via `src/data/resample.py`),
   lalu SEGEL — jangan dibuka, jangan dibaca untuk keputusan.
   Segel R1 (`5bc324aa…67df963`) JANGAN dibuka, JANGAN dibaca.

## Keluaran (sebelum auditor mulai)
- Ledger + manifest hash + script/harness + JSON event-level
  (kolom minimum D-3.4 warisan) + stdout, semua di folder evidence
  di atas. Logging gagal = run gagal.

## Larangan (pelanggaran = run gagal)
Tanpa 2023/2024/2025 untuk evaluasi; tanpa tuning threshold/horizon/
barrier (k=1,5/RR=2,0/H+10 beku); tanpa keluarga ke-4; tanpa indikator
(RSI/MACD/EMA/nama-candle); tanpa M15 di evaluasi; tanpa buka segel
(R1 maupun R2); tanpa uji p-value untuk seleksi; tanpa ronde lain di
2026 sebelum R2 selesai (satu bed satu ronde); tanpa `except: pass`;
tanpa `print()` produksi bila kode Python (pakai logging); fungsi <
50 baris, file < 400 baris.

## Format pulang
Laporan §5 AGENTS.md (file dibuat/diubah, tabel Klaim & Bukti, yang
belum diverifikasi, potensi masalah, saran). Satu ronde satu vonis:
tidak ada "sekalian coba varian". Ekspektasi jujur (C2): porsi
TIME-out kemungkinan besar — laporkan proporsinya, jangan
"perbaiki" dengan mengubah horizon/barrier.
