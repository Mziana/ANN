# Perintah Coder L3-1: Baseline vs Null, 103 Pasangan (paste-manual)

Peran: Coder. Tugas: eksekusi B-3 putusan-l30-audit persis:
prediktor laju-marginal-per-iris vs null mayoritas-kelas, Brier,
split waktu terkunci, pada MAKSIMAL 103 pasangan terdaftar.
BUKAN arsitek (DILARANG ubah M1/M2/M3/split/ambang), BUKAN
auditor. Workdir: D:\ANN. Bahasa: Indonesia. STOP setelah
serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (S5, S8A), spesifikasi-lapisan3.md,
   putusan-l30-audit.md (B-1..B-4 MENGIKAT - M2/M3/split/ambang
   SUDAH dikunci, tinggal eksekusi), putusan-eda07-audit.md (A),
   reaudit-l30.md (T-1..T-6 + S6).
2. Reuse-first: konstruksi label per-bar VERBATIM run 9
   (_eda_common + kode label run 9; DILARANG definisi label baru),
   pola builder I-2/L3-0. Tanpa dependensi baru, tanpa tulis ke
   configs/src/data, tanpa commit/push, tanpa klaim tanpa bukti.
3. Setiap syarat berpasangan perintah mentah + output. Klaim tanpa
   output mentah = GAGAL.
4. Bertentangan dengan B-3 -> STOP + lapor; jangan improvisasi.

## S5 Tugas (batas L3-1)

1. Pasangan: 98 native peta98 (wakil, arah) + 5 Tokyo round_d
   (neg). Total 103, DILARANG tambah/kurang.
2. Per pasangan: baseline = laju-marginal train per iris target;
   null = mayoritas-kelas train global. Metrik Brier (+ akurasi).
   Train 2023H2-2024H2, test 2025H1+2025H2, tanpa shuffle lintas
   batas. Seed 31001/31002 hanya untuk bootstrap CI.
3. M3 per pasangan (assert mesin): (a) Brier_mod < Brier_null -
   0,001 test pooled; (b) menang di 2025H1 DAN 2025H2
   masing-masing; (c) akr_mod >= akr_null pooled. Gagal satu =
   GUGUR. Lift besar (T-5) BUKAN presumi - M3 sama untuk semua.
4. Output di reports/eda/2026-10-12/: T-L3-1_baseline.csv (1 baris
   per pasangan: M1/M2/M3, Brier keduanya, akurasi, vonis +
   kolom punya_round_d_invers), FIG-18, notebook 0 error +
   kesimpulan 1 paragraf, builder ASCII/LF, runner-log via
   REDIRECT langsung (tutup T-6), manifest DENGAN kolom path
   (tutup T-1), redaksi K24 baku (tutup T-2).
5. Laporan S5: file + Klaim & Bukti + belum-diverifikasi +
   potensi masalah. Tanpa vonis dagang, tanpa klaim edge, tanpa
   P&L/backtest. Selesai = TABEL M3 terkunci.

## Perintah mentah wajib

- Hash builder + notebook + CSV + FIG + log + manifest.
- Bukti label verbatim run 9 (diff kode label vs source = KOSONG
  kecuali wiring).
- Bukti split waktu (rentang train/test per semester + tanpa
  bocor: max train < min test).
- Bukti M3 per pasangan (tabel Brier/akurasi; daftar GUGUR vs
  LOLOS dengan angka).
- Bukti 103 pasangan tepat (daftar vs peta98 + 5 Tokyo).
- Runner-log EXITCODE + manifest path + hash input beku.
- git status + HEAD (nol stage ronde ini). ASCII/LF builder.
- DILARANG imbauan umum. Klaim tanpa output mentah = GAGAL.

## S8A diingatkan

Ronde ini berakhir dengan TABEL M3 (siapa kalahkan null),
bukan investigasi baru. Vonis dagang = wewenang arsitek+user
pasca-audit L3-1.
