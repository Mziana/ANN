# Perintah Auditor L3-0: Reaudit Peta Arah (paste-manual)

Peran: Auditor independen (bukan coder L3-0). Tugas: reaudit L3-0
read-only: hitung ulang dari CSV beku + baca source, tanpa
menjalankan builder/notebook. Harness di temp, DILARANG tulis ke
repo. Workdir: D:\ANN. Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak

1. Baca: .ai/AGENTS.md (S18 template audit, S20 anti-halusinasi),
   spesifikasi-lapisan3.md (S3-0..S3-5), putusan-eda07-audit.md,
   laporan-coder-eda07-l30.md (55 baris),
   .ai/assistant/verifications/2026-10-12_gerbang-hasil-l30.md.
2. Setiap syarat berpasangan perintah mentah + output. Klu tanpa
   bukti = BELUM DIVERIFIKASI (tulis eksplisit).
3. Jujur seperti reaudit EDA-07: koreksi-diri bila draf salah;
   bedakan temuan komputasi vs provenance vs kosmetik.

## S5 Tugas (batas L3-0)

1. S-0 gerbang masuk: HEAD, branch, staged, SHA256 6 file L3-0
   (klaim di laporan coder) + format ASCII/LF.
2. Hitung ulang independen: (a) 153 = filter G3 T-07-3 + split
   120/33 dari tanda lift; (b) 5 Tokyo 4-desimal + negatif;
   (c) 2 baris round_d London G3=False + CI memuat 0 + targetnya
   LOLOS via wakil asli; (d) rekonstruksi verdict verbatim dari
   CSV -> 98 (bandingkan daftar target vs I-2); (e) diff
   peta-vs-LOLOS kosong + arah = tanda wakil 98/98;
   (f) FIG-17 mencakup 153; (g) manifest 6/6 + EXITCODE=0;
   (h) kepatuhan S3: tanpa model/skor/null/2026, 5 Tokyo tak
   dipakai sebagai sinyal, K24 = transcription-guard (bukan
   bukti komputasi - pastikan tidak dilebihkan).
3. Serahkan reports/governance/2026-10-12/Audit/reaudit-l30.md:
   vonis LOLOS/GAGAL prosedural + temuan berperingkat + S6 yang
   belum diverifikasi + rekomendasi. Tanpa vonis edge/model.

## Catatan presisi (dari laporan coder, wajib konfirmasi)

"2 London absen" hanya benar di level BARIS kandidat round_d;
di level TARGET kedua London LOLOS via wakil asli. Pastikan
laporan audit memakai kualifikasi ini, bukan versi pendek.
