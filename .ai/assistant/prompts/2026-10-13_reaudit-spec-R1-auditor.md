# Brief Re-Audit FOKUS Spec Discovery-R1 Amandemen-1 (Auditor Eksternal, 2026-10-13)

## Konteks
Spec: `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R1.md`
(status: SPEC EKSEKUSI + AMANDEMEN-1). Audit penuh Anda sebelumnya:
VERDICT GAGAL (3 HIGH + 6 MEDIUM + 5 LOW). Arsitek + user menerima
ketiga HIGH dan mengamandemen. Tugas ini BUKAN audit penuh.

## Yang harus diverifikasi — hanya 3 butir

1. **H1 (definisi M15 fisikal?)** — baca D-8.2 + A-H1. Pertanyaan:
   definisi baru ("bar M15 TERAKHIR YANG SELESAI pada atau sebelum t0",
   return close-to-close) dapat diimplementasi coder tanpa mengarang
   dan tanpa menyentuh data sesudah t0? Pastikan tidak ada sisa
   definisi lama yang hidup di luar catatan historis A-H1.
2. **H2 (family + kriteria terkunci?)** — baca A-H2, D-4.2, Q1/Q2
   (D-4.3), D-4.4. Pertanyaan: (a) setting evaluasi tunggal
   (horizon +10 M1 dari t0 close, TP 2,5/SL 2,5, observed net) beku
   sebelum data dibuka? (b) horizon/ladder lain eksplisit deskriptif
   dan DILARANG mengangkat kandidat? (c) kriteria KANDIDAT 4-syarat
   (pooled median > 0 + CI 95% cluster-hari + tanda sama 2024-H1/H2 +
   failure map, setelah gerbang kapasitas 300) operasional tanpa
   derajat bebas tersembunyi? (d) family untuk correction = 6 sel E1
   (+ E2/E3 satu-sel, diakui tanpa variasi)?
3. **H3 (kontradiksi M15 hilang?)** — baca A-H3, D-4.2, D-8/ D-8.2/
   D-8.3. Pertanyaan: apakah D-4.2 ("R1 TANPA pemisahan konteks
   primer") konsisten penuh dengan D-8 ("dilarang dipakai memilih/
   menyetel kandidat R1") — tidak ada kalimat yang memberi M15 peran
   evaluatif di R1?

## Format jawaban (sama seperti sebelumnya)
- Untuk tiap butir: LULUS / GAGAL + bukti (file:baris yang dicek).
- Verdict akhir: LULUS (ketiga butir lulus) / GAGAL (sebut butir +
   alasan). Temuan di luar 3 butir: catat sebagai CATATAN saja,
   tidak boleh mengubah verdict kecuali Anda menemukan cacat FATAL
   baru (definisikan eksplisit bila ada).
- Larangan: tidak merancang ulang, tidak mengusulkan angka alternatif,
  tidak menyentuh data.
