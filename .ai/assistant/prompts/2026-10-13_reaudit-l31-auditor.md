# Perintah Auditor L3-1: Reaudit Baseline vs Null (paste-manual)

Peran: Auditor independen (bukan coder L3-1). Tugas: reaudit
read-only dari CSV beku + source, tanpa eksekusi builder/notebook.
Harness di temp, DILARANG tulis ke repo. Workdir: D:\ANN.
Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak

1. Baca: AGENTS.md (S18, S20), spesifikasi-lapisan3.md,
   putusan-l30-audit.md (B-3), amandemen-l31-metrik.md (C-1..C-4),
   laporan-coder-eda07-l31.md,
   verifications/2026-10-13_gerbang-hasil-l31.md.
2. Perintah mentah + output per syarat; tanpa bukti =
   BELUM DIVERIFIKASI. Bedakan komputasi/provenance/kosmetik.

## S5 Tugas (batas L3-1)

1. S-0: HEAD, staged, SHA256 6 file L3-1 + format.
2. Hitung ulang independen: (a) 103 = 98 peta98 + 5 Tokyo,
   67 brier + 36 mse; (b) aturan M3 = vonis 103/103; (c) margin
   0,001 diskret + 1% kontinu tanpa pelanggaran; distribusi
   margin (menempel ambang atau headroom); (d) menang-H1&H2
   per baris; (e) twin 5/5 identik; (f) flag invers = 12;
   (g) split train<test tanpa bocor (desain, bukan re-run);
   (h) label verbatim run 9 (spot-check konstruktor TLAB/YCODE/
   jalur kontinu vs source); (i) manifest path + hash;
   (j) FIG-18 cakupan data; (k) kepatuhan S3-3/S8A (tanpa
   P&L/backtest/edge/vonis dagang; tanpa fitur/label baru).
3. Catatan asisten (wajib konfirmasi/bantah): run_l31.log
   UTF-16LE + wrapper NativeCommandError = perbaikan T-6 tak
   dijalankan; nilai dampaknya.
4. Serahkan reports/governance/2026-10-12/Audit/reaudit-l31.md:
   vonis LOLOS/GAGAL prosedural + temuan berperingkat + S6 +
   rekomendasi + daftar LOLOS-per-jenis (angka, bukan vonis
   dagang). Tanpa klaim edge/profitabilitas.
