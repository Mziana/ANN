# Perintah Coder I-2: Penyelesaian EDA-07, G1-G4 Penuh (paste-manual, FINAL)

Peran: Coder. Tugas: run penyelesaian EDA-07 (mandat V-6): evaluasi
G1-G4 penuh (fitur asli + 7 kandidat round_d), T-07-1..4, FIG-13..16,
sel kesimpulan terisi. BUKAN arsitek (DILARANG ubah ambang/aturan),
BUKAN auditor. Workdir: D:\ANN. Bahasa: Indonesia. STOP setelah
serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (S5 format laporan),
   reports/governance/2026-10-12/arsitek/putusan-eda07-i1.md (V-4/V-5/V-6
   MENGIKAT), reports/governance/2026-10-10/arsitek/spesifikasi-eda07-
   label-fitur.md (S1-S9; S8-G2 = versi A-3, alarm = versi A-7),
   reports/eda/2026-10-12/laporan-coder-eda07-g2.md (run 9) +
   reports/eda/2026-10-12/laporan-coder-eda07-i1.md (I-1).
2. Patuh AGENTS.md penuh: reuse-first (pipeline run 9 + mesin I-1 dipakai
   ulang), tanpa dependensi baru, tanpa tulis ke configs/src/data, tanpa
   commit/push, tanpa klaim tanpa bukti.
3. Setiap syarat berpasangan perintah mentah + output di laporan.
   Klaim tanpa output mentah = GAGAL (tulis eksplisit).
4. Bila bertentangan dengan V-4/V-5/V-6 atau vonis terkunci, STOP dan
   laporkan; jangan improvisasi.

## S5 Tugas (batas I-2, DILARANG melampaui)

1. Bangun di atas pipeline run 9 (builder + notebook EDA-07, sel 01-15
   tetap) + definisi I-1 (X=10, DEKAT/JAUH): evaluasi G1-G4 S8-revisi
   untuk (a) SEMUA fitur asli S4 pada 23+7 irisan x 4 label, dan
   (b) round_d SEBAGAI FITUR hanya pada 7 pasangan kandidat V-5
   (LB_rng London t3/tALL N5; LB_bin Tokyo t2/tALL N15/N5;
   LB_rng Tokyo tALL N5/N15). Di luar 7 pasangan itu round_d tetap
   kontrol. pdhl_d tetap kontrol di mana-mana (ARTEFAK tertutup V-5).
2. Gerbang kontrol = pemeriksaan REGRESI (V-6, menggantikan STOP buta):
   himpunan alarm kontrol harus SAMA PERSIS dengan
   reports/eda/2026-10-12/_gate_G2_alarm.csv (86 baris, pasangan
   target-x-kontrol identik). Kontrol BARU lolos di luar 86 = STOP +
   adjudikasi baru, DILARANG bypass. Ketidakcocokan bit-identik
   skrining vs run 9 = drift pipeline = STOP.
3. Selesaikan sel verdict: G1/G3/G4 per irisan identik (preseden EDA-06),
   G4 menaut ke delta irisan itu; T-07-1..4 (teks + CSV satu lokasi
   reports/eda/2026-10-12/) + FIG-13..16 sekuensial + registry
   FIG-01..akhir terverifikasi + sel kesimpulan SATU paragraf WAJIB
   terisi manual SETELAH baca tabel (kunci label + horizon/barrier +
   daftar fitur untuk Lapisan 3).
4. Eksekusi detached bila >30 menit (Task Scheduler rantai tunggal,
   progres fraksi ke file log, checkpoint per irisan, hapus task
   selesai, pola run 9). Timeout nbconvert >= 5400 (pelajaran run 8).
5. Serahkan laporan S5: file + tabel Klaim & Bukti + yang belum
   diverifikasi + potensi masalah + rekomendasi irisan x label x fitur
   layak ke Lapisan 3 (tanpa vonis, tanpa klaim edge, tanpa buka
   Lapisan 3 - itu wewenang arsitek).

## Perintah mentah wajib

- Hash builder + notebook SESUDAH tulis terakhir + baris/byte.
- Bukti reuse + nol drift: 24/24 konstanta run 9 identik (diff kosong);
   X=10 + SEEDI1 + aturan V-2/V-5/V-6 tercatat dan di-assert.
- Bukti regresi kontrol: diff himpunan alarm vs _gate_G2_alarm.csv
   (harus KOSONG; bila tidak kosong = STOP + tempel diff).
- Bukti file lama tak tersentuh: hash _gate_/_ckpt_/T-I1/laporan run 9
   + I-1 SEBELUM vs SESUDAH = sama (tempel kedua output).
- Bukti eksekusi: urutan sel + exit code + T-07-1..4 + FIG-13..16 +
   isi paragraf kesimpulan + daftar CSV.
- Bukti G1-G4: jumlah irisan diuji + lolos tiap tahap per label +
   daftar 7 kandidat (lolos/gagal G1/G3/G4 masing-masing).
- git status --porcelain=v1 + git rev-parse HEAD (nol stage ronde ini).
- Cek ASCII/LF/tail-LF builder (perintah + output).
- DILARANG imbauan umum. Klaim tanpa output mentah = GAGAL.

## Larangan

1. DILARANG label/fitur/irisan baru di luar tugas 1; DILARANG pindai
   ambang/bin/window/theta; DILARANG promosikan pdhl_d.
2. DILARANG ubah ambang/kriteria A-3/A-7/V-2/V-5/V-6.
3. DILARANG model/backtest/P&L/vonis/edge sebagai klaim.
4. DILARANG tulis configs/src/data/governance selain laporan tugas.
5. DILARANG commit/push. DILARANG pointer ke file internal asisten.
6. File run 9 + I-1 hanya dibaca (bukti hash sebelum/sesudah di atas).
