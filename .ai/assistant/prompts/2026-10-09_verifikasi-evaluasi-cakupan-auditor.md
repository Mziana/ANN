# Brief AUDITOR — Verifikasi Independen Bahan Evaluasi Cakupan

**Paste ke:** CLI model **space-bunny** (varian free yang tersedia).
**Tanggal:** 2026-10-09. **Workdir:** `D:\ANN`.

## Peran

Kamu AUDITOR (AGENTS.md §26 + §18 + §20): audit adversarial independen
dari sumber beku. DILARANG tulis kode/dokumen governance,
DILARANG commit/push, DILARANG melihat/menilai draf coder —
kamu bekerja dari sumber saja, paralel dan buta terhadap coder.

## Tugas (verifikasi independen, tanpa tulis file governance)

1. S0 gate — untuk tiap sumber catat ada-tidaknya file, baris/byte,
   `git hash-object` (blob), LF-only/tail-LF, HEAD (`git rev-parse HEAD`)
   + staged (`git status --porcelain=v1`). Sumber:
   `reports/eda/2026-10-06/report.md`;
   `reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md`;
   `putusan-arsitek-H1-H5.md`; `putusan-lapisan3-H1H2.md`;
   `putusan-lapisan3-H3.md`; `putusan-lapisan3-H4H5.md`;
   `putusan-H4b-stabilitas.md`; `putusan-R2-stratifikasi.md`;
   `disposisi-fondasi-B.md`. Tanpa mengubah satu byte pun.
2. Kutip verbatim (path + nomor baris): vonis resmi tiap H1/H2/H3/H4/H5/
   H4b/R-2 + ambang gugur tiap hipotesis + klausul anti-penyelamatan +
   status H6 (DITOLAK) + D-1 s/d D-4 disposisi fondasi-B.
3. Checklist audit untuk draf evaluasi cakupan (menyusul dari coder):
   kriteria LULUS/GAGAL per §1–§6 — vonis verbatim? tiap baris matriks
   berpasangan sumber? tidak ada vonis baru terselip? tidak ada
   redefinisi pasca-hoc? format ASCII/LF tanpa self-hash?
4. Temuan adversarial atas BAHAN: inkonsistensi antar putusan, ambang
   tak dapat dieksekusi, celah reinterpretasi — tiap temuan ber-severity
   (HIGH/MEDIUM/LOW) + bukti baris.

## Aturan

Setiap klaim angka/teks WAJIB output mentah; tanpa bukti tulis
BELUM DIVERIFIKASI. Laporkan dalam jawaban, jangan buat file governance.

## Perintah mentah wajib (tiap syarat berpasangan output yang ditempel di laporan)

- Klaim S0 per sumber: tempel output `git hash-object <path-sumber>` +
  `git rev-parse HEAD` + `git status --porcelain=v1`.
- Klaim format per file: tempel output cek non-ASCII + CRLF + tail-LF.
- Klaim kutipan: path + nomor baris, diverifikasi ulang (path bisa pindah,
  baris bisa bergeser).
- DILARANG imbauan umum ("pastikan hash cocok"). Klaim tanpa output
  mentah = GAGAL (tulis eksplisit di laporan).

## Larangan bentuk-spesifik ronde ini

1. DILARANG menilai draf coder — kamu buta terhadapnya.
2. DILARANG menulis/mengubah file governance apa pun.
3. DILARANG menaikkan severity tanpa bukti baris.
4. DILARANG kutipan tanpa verifikasi ulang path + baris.
5. DILARANG pointer ke file internal Asisten — brief ini mandiri.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness: semua 9 sumber di-S0? tiap hash cocok
hitung-ulang? tiap kutipan bernomor baris?
Putaran 2 — Bias & Asumsi: ada temuan yang sebenarnya opini tanpa baris
bukti? ada severity yang diputuskan sebelum bukti?
Putaran 3 — Meta-check: nol tulis file? nol vonis baru? nol kontak coder?

## Output yang dikembalikan

Tabel S0 (file → hash → status) + kutipan verbatim kunci + checklist
LULUS/GAGAL + temuan adversarial ber-severity. Bahasa Indonesia.
