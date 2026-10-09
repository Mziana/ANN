BATCH A — LANGKAH 2 + LANGKAH 3 AUDIT nb05 (HANYA dua langkah ini)

Konteks: Langkah 1 LULUS (re-audit `2db14c9e…`). Fondasi replika dianggap
beres. Tugasmu sekarang dua lapisan berikutnya. DILARANG menyentuh Langkah
4–10 dan DILARANG membuka materi lama (A/B/C, D1–D12, MEDIUM/LOW lama).

=== LANGKAH 2 — INSIDEN SALAH-BACA ACF (resolusi "dua metrik") ===

Klaim yang harus kamu uji (bukan dipercaya): "-0,022624 adalah sign-ACF
(metrik tanda, D4 nb03), bukan ACF besaran; builder mengunci keduanya
terpisah (`acf1_m15_a` vs `sign_acf1`)."

Periksa, masing-masing dengan bukti file:baris:
1. Setiap kemunculan angka ACF/sign-ACF di `_build_eda05.py`, output notebook
   (sel 9), `report.md`, `laporan_tahap_11/12`, dan dict H2 — apakah labelnya
   konsisten (besaran vs tanda tidak tertukar di SATU pun tempat)?
2. Lacak semua pemakaian variabel `acf1_m15_a` dan `sign_acf1` di builder:
   adakah titik di mana keduanya tercampur (mis. assert/assertion, print,
   dict H2, perhitungan turunan)?
3. Komentar yang merujuk "headline D4 nb03" (`:447` dan sejenisnya): apakah
   rujukannya akurat terhadap isi nb03?
4. Catatan `1,0337 = rata-rata VR LAG 2-60` (:487, output sel 9, dict H2):
   apakah ketiga tempat itu saling konsisten dan tidak ada sisa label lama
   "referensi nb03: 1,0337" yang belum terganti?
5. Jika ada inkonsistensi tersembunyi (angka benar tapi label salah di sudut
   yang luput), laporkan sebagai temuan dengan lokasi persis.

=== LANGKAH 3 — LOOK-AHEAD / LEAKAGE ===

Uji tiga permukaan, masing-masing dengan bukti file:baris:
1. Pelabelan regime + tipologi (`tipe`: trending/range/normal): apakah label
   hari-t hanya memakai informasi yang tersedia pada hari-t? Waspadai:
   normalisasi/standardisasi memakai statistik seluruh sampel, threshold yang
   dihitung dari masa depan, atau agregat yang menengok hari berikutnya.
2. Block bootstrap (coder menyatakan "marginal" — jangan percaya, uji):
   apakah panjang block dan skema resampling menghormati dependensi temporal?
   Apakah keterbatasan hasilnya di-disclose di output/laporan, atau disajikan
   seolah definitif? Resampling dilakukan dalam strata atau bocor antar strata?
3. Agregasi hari-broker: pemetaan M15/M5 → hari broker (`wall_clock_series`,
   `n_leading`/`n_leading5`, bucket pembuka 22:07). Rerun-1 coder GAGAL pada
   assertion paritas baru karena pemetaan lama menggeser bucket pembuka —
   pastikan perbaikan (`:430-437`, `:444-445`) benar-benar menutupnya dan tidak
   ada jalur agregat lain yang memakai pemetaan lama. Periksa penanganan DST
   (UTC+2/+3) bila relevan.

Di luar tiga permukaan di atas: JANGAN melebar (mis. jangan menilai kualitas
metode bootstrap sebagai pilihan arsitektur — itu bukan audit; yang diaudit
hanya kebocoran dan kejujuran disclosure).

=== ATURAN BATCH (mengikat) ===
1. Objek HANYA file nb05 yang sudah kamu kenal + blob barunya
   (`8ac848ce…`, `93ea7695…`, `72e83777…`, `6ab21459…`, `eae21308…`).
2. Setiap temuan WAJIB file:baris + angka/output. Tanpa bukti = bukan temuan.
3. "Tidak sesuai rancangan" ≠ "perhitungannya salah" ≠ "kesimpulannya salah".
4. Ragu → BELUM DIVERIFIKASI + Pertanyaan untuk Coder.
5. Append ke `D:\ANN\reports\governance\2026-10-06\audit\eda_nb05_audit_v1.md`.
   Hitung hash SETELAH tulis final, sebut di chat.
6. Verdict per langkah (LULUS / PERLU PERBAIKAN) + verdict batch.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap angka/temuan bersumber file:baris/output.
Putaran 2 — Bias: apakah kamu menilai pilihan metode (tugas arsitek) alih-alih
  kebocoran/kejujuran (tugas auditor)? Apakah ada temuan di luar scope 2–3?
Putaran 3 — Meta: objek benar (nb05)? Langkah 4–10 dan materi lama tak
  tersentuh? Hash setelah final?

STOP. Batch B (Langkah 4–6) HANYA atas perintah terpisah.
