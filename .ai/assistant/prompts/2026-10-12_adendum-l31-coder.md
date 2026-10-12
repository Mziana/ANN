# Adendum Brief Coder L3-1: Eksekusi dengan Amandemen C (paste-manual)

Brief induk 2026-10-12_eksekusi-l31-coder.md + amandemen-l31-metrik.md
(C-1..C-4) MENGIKAT BERSAMA. Yang berubah hanya metrik/M3/kunci
di C-2/C-3; S-0/S5/perintah-mentah/S8A induk UTUH.

Delta eksekusi:

1. 67 baris diskret: M3 B-3 utuh (Brier margin 0,001 + menang
   per-semester + akurasi). Aturan prediksi kelas + tie-break =
   C-3 (assert mesin determinisme tie).
2. 36 baris LB_rng: M3-kontinu C-2 (MSE margin relatif 1% +
   menang per-semester + MAE). Null = mean global, baseline =
   mean per-iris. Brier/akurasi DILARANG untuk baris ini.
3. Assert konsistensi: M3 5 baris round_d = M3 kembaran native
   (label sama). CSV L3-1 satu tabel 103 baris dengan kolom
   metrik_jenis (brier/mse) + vonis + punya_round_d_invers.
4. FIG-18 mencakup kedua jenis (panel terpisah, DILARANG
   membandingkan angka Brier vs MSE lintas jenis).
5. Laporan S5 + STOP. Tanpa vonis dagang, tanpa klaim edge.

S8A: adendum ini penutup konflik, bukan ronde baru.
