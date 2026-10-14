# Ledger Pra-Run — Pemanasan R3 (flip + resize) — NON-VONIS

Status: **PEMANASAN DIAGNOSTIK — BUKAN RONDE VONIS.**
Run ini tidak menghasilkan vonis apa pun (bukan TOLAK/KANDIDAT/BELUM JELAS).

Tafsir asimetris (ditetapkan arsitek + user, ditempel di laporan pulang):

- Hasil KALAH = ide paket gugur kuat (bahkan dengan setting dipilih
  sesudah melihat data pun gagal) → hemat bed 2025.
- Hasil MENANG = tanpa makna (artefak seleksi sirkuler) → tidak membuka
  segel apa pun, tidak mengubah status ronde mana pun, tetap wajib uji
  bed baru untuk arti apa pun.

## Otoritas

- Spec `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R2.md`
  (SPEC EKSEKUSI + Amandemen-R2-1), SHA-256:
  `c05d5e4fe94a364baa6bcb56863a7e5cc6507b8e0cdf9d9bdde12639a80654c5`
- Brief `.ai/assistant/prompts/2026-10-13_pemanasan-R3-coder.md`, SHA-256:
  `e3fee14ba1afb71471bd9da468d0961ae872fc0ac6cfc7fc2a8d5e45d59a62b3`
- Bila bertentangan dengan spec R2, spec R2 menang (tidak ditemukan
  konflik; dua perubahan di bawah diotorisasi brief R3).

## Bed + eksklusi (disalin dari spec, bukan dihitung-ulang)

- M1 2026: `data/processed/M1/usdjpy_m1_2026.parquet`, 269.846 bar,
  SHA-256 `7f267bb94005a34e07bf524e0275f04798e48c60fe2109f22ba5d0213ac02ba5`
  (terukur = spec D2-3).
- Anomali 2026-03-10..03-27 (tanggal UTC) KELUAR dari denominator:
  19.119 bar (terukur = spec D2-3). Usable 250.727 bar.
- Paruh stabilitas (salin spec D2-3): Paruh-1 = 2026-01-01..2026-05-18;
  Paruh-2 = 2026-05-19..2026-10-02 (tanggal UTC; anomali sudah keluar
  dari keduanya).
- Gap = selisih timestamp UTC antar bar berurutan != 60 detik: 255 gap
  pada file 2026 (terukur pra-run; akhir pekan/rollover termasuk).

## Dua perubahan (otorisasi brief R3, dinyatakan eksplisit)

1. **FLIP:** event E1 (6 sel) + E2 (1 sel) + E3 (1 sel, definisi R1 D-1
   verbatim) dipetakan di 2026, lalu `side → -side` — satu operasi
   sesudah scan, tanpa ubah logika scan E1/E2/E3 apa pun. Pagar SL/TP
   dan biaya mengikuti side HASIL NEGASI secara otomatis.
2. **RESIZE:** SATU paket barrier ATR — ATR = ATR M5(14) pip dari bar M5
   terakhir selesai ≤ t0 (resep `_build_eda06.py:500-533` verbatim,
   dibekukan saat entri); **SL = 1,0×ATR, TP = 1,5×ATR (RR 1,5:1)**.
   Tanpa ladder, tanpa pemilihan.

## Skala ATR-2026 terukur (pra-run, resep verbatim, anomali dikecualikan
dari pembangunan M5)

- ATR tersedia 238.300 dari 269.846 bar (88,3%).
- ATR pip: mean 5,1059; median 4,2429; q25 2,7571; q75 6,4000;
  min 0,3929; max 77,4000.
- R3: SL mean ≈ 5,1059 pip (≈ 51 point); TP mean ≈ 7,6588 pip
  (≈ 77 point). Konvensi point: 1 pip = 10 point (R1: 2,5 pip =
  25 point).
- Entry DIBUANG bila ATR tak tersedia / jendela menyeberangi gap /
  anomali / sesi Off — nol imputasi, jumlah buang dilaporkan, urutan
  hitung berurutan GAP → ANOMALY_CROSS → ATR_NA → OFF_SESSION.

## Sesi + biaya (literal config, pra-run)

- `configs/data.yaml` SHA-256
  `1127514518aaf23cd48acac3e4f482159d14a25f37d05168b4444f2c38709dad`.
- Definisi sesi = salinan terkunci proyek (fingerprint cocok):
  Tokyo Asia/Tokyo 9-18 | London Europe/London 8-16 | NewYork
  America/New_York 8-17 | Sydney Australia/Sydney 8-16;
  prioritas London>NewYork>Tokyo>Sydney; selain itu Off.
- Cakupan sesi bar usable 2026: London 87.348, Tokyo 79.248, NewYork
  65.113, Sydney 19.018, Off 0.
- Biaya 3 lapis per event (sesi = sesi bar entry t0+1):
  observed = `cost_basis.by_session` (London 0,61 / NewYork 0,69 /
  Tokyo 0,62 / Sydney 0,80) + komisi 0,3 pip round-turn (asumsi
  per-side, sekali per event); conservative = observed + slippage 0,2
  (ASUMSI); stress = `stress_bands.p95.by_session` (London 0,8 /
  NewYork 1,2 / Tokyo 0,9 / Sydney 1,5) + slippage 0,3 (ASUMSI) +
  komisi 0,3. Fallback `cost_basis.default` 0,65 bila sesi tak
  terpetakan + laporkan. `spread.default`, `by_year`,
  `stress_multiplier` DILARANG dan tidak dipakai.

## Kontrak eksekusi (spec R2 D2-5, diringkas)

- Entry OPEN bar t0+1; horizon dari t0 close; BUY ASK→BID / SELL
  BID→ASK (side hasil negasi); spread nol dan mid dilarang.
- Race 10 bar SESUDAH bar entry (t0+2..t0+11); TIME exit = close
  t0+11. Bar-kembar SL+TP = AMBIGUOUS_SEQUENCE (buang + hitung
  eksplisit).
- t0 di dalam jendela anomali tidak dipindai sama sekali.

## Evaluasi (brief R3; 4-syarat D2-6 sebagai angka diagnostik, TANPA vonis)

- Q0 gerbang 300 (dilaporkan; sel < 300 = dropped, bukan tuning).
- Q1 evaluasi HANYA H+10 (barrier race + gross H+10). Tanpa RV/TAU;
  tanpa M15 di evaluasi. Tanpa lampiran D-8, tanpa segel.
- Q2 satu paket (tanpa ladder). Q4 failure map wajib. Q5 paruh-2026.
- Bootstrap median: 10.000 resample cluster hari-broker t0, seed 1337.
- Determinisme: 2 run byte-identik.

## Verifikasi pra-run

- `src/data/resample.py` (SHA-256
  `54fc73693b0faba7724ef3463df91acc46f944ef654ebf6fe14b8f5ca846efac`):
  resample M1-2026 → M15 menghasilkan 18.026 bucket, m1_sum = 269.846
  (= input, struktural cocok), bar/bucket 2-15. `TIME_COLUMN =
  broker_time_raw`.
- Resep ATR: `scripts/_build_eda06.py` SHA-256
  `5bf6cb6a3dda9a92a86ec8a3621cbd10649866daec412993ba760facc97b1cf4`;
  definisi sesi: `src/features/build_features.py` SHA-256
  `6549a657adc9eae45d50aae4d6d44ed1353804e37b10f2b59254ada471d5b5a6`.
- Recon dibangkitkan oleh skrip TEMP
  (di luar repo; membaca saja, tidak menulis artefak).

## Larangan ronde ini

- Folder `discovery-R2/evidence/` + segel R2 + segel R1 TIDAK DISENTUH
  (baca pun tidak). Tanpa 2023/2024/2025 untuk evaluasi. Tanpa varian
  selain dua perubahan di atas. Tanpa indikator. Tanpa uji p-value
  untuk seleksi. Tanpa `except: pass`. Tanpa `print()` produksi.
  Fungsi < 50 baris, file < 400 baris.
