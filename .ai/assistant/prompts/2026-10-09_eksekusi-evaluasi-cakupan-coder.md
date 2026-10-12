# Brief CODER — Draf Dokumen Evaluasi Cakupan Riset

**Paste ke:** CLI model **muse-spark-1.3** (atau varian free yang tersedia).
**Tanggal:** 2026-10-09. **Workdir:** `D:\ANN`.

## Peran

Kamu CODER (AGENTS.md §26): implementasi + self-audit + fix.
DILARANG menentukan arsitektur, DILARANG audit sendiri,
DILARANG tulis/ubah kode produksi, data, config, DILARANG commit/push.

## Tugas (satu file)

Susun DRAF di `reports/governance/2026-10-09/evaluasi-cakupan-riset.md`
mengikuti kerangka arsitek (sudah disetujui user):

- §1 Tujuan & Batas — menilai cukup-tidaknya EDA + Lapisan 3 untuk arah
  riset scalping. DILARANG mengubah vonis, merehabilitasi H-gugur,
  merumuskan H6.
- §2 Peta EDA Q1–Q7 sebagai karakteristik pasar + batas klaim tiap Q.
  Sumber: `reports/eda/2026-10-06/report.md`, `laporan_tahap_12_sintesis.md`.
- §3 Peta vonis Lapisan 3 per H1/H2/H3/H4/H5/H4b/R-2: pertanyaan persis
  yang diuji + populasi/definisi + ambang gugur + vonis resmi satu kalimat.
  WAJIB kolom "yang tidak diuji oleh vonis ini".
  Sumber: `arsitek/hipotesis_lock_v1.md`, `putusan-arsitek-H1-H5.md`,
  `putusan-lapisan3-H1H2.md`, `putusan-lapisan3-H3.md`,
  `putusan-lapisan3-H4H5.md`, `putusan-H4b-stabilitas.md`,
  `putusan-R2-stratifikasi.md`, `disposisi-fondasi-B.md`
  (semua di `reports/governance/2026-10-07/arsitek/`).
- §4 Matriks cakupan tiga kolom: sudah dijawab / belum diuji /
  di luar tujuan H1–H5.
- §5 Kandidat arah (H6+ baru / penelitian event baru / langsung dev metode /
  tahan) + kriteria pemicu konkret tiap opsi, tanpa memutuskan.
- §6 Rekomendasi berpasal (satu arah + alasan + prasyarat penguncian).

## Aturan besi

- Kutip vonis VERBATIM; dilarang parafrase yang menggeser arti.
- Tiap baris matriks §4 berpasangan ke sumber (path + baris + hash bila ada).
- Prinsip dua arah eksplisit di §1: gugur-sebagai-rancangan ≠
  karakteristik mati total; gugur ≠ boleh diselamatkan via redefinisi
  pasca-hoc (pertanyaan baru = penelitian baru, pra-registrasi segar).
- Format: ASCII-only, LF-only, TANPA self-hash.
- Satu-satunya file yang boleh ditulis = file draf di atas.

## Perintah mentah wajib (tiap syarat berpasangan output yang ditempel di laporan)

- Klaim file draf ada + ukurannya: tempel output `git hash-object <path-draf>`
  SESUDAH penulisan terakhir + jumlah baris/byte.
- Klaim tanpa commit/stage: tempel output `git status --porcelain=v1`.
- Klaim format ASCII/LF-only/tail-LF: tempel output cek non-ASCII + CRLF +
  byte terakhir (perintah + outputnya, bukan ringkasannya).
- Klaim kutipan verbatim: tiap kutipan menyebut path + nomor baris sumber.
- DILARANG imbauan umum ("pastikan hash benar", "pastikan format bersih").
  Klaim tanpa output mentah = GAGAL (tulis eksplisit di laporan).

## Larangan bentuk-spesifik ronde ini

1. DILARANG merekonstruksi vonis dengan kata sendiri — kutip verbatim.
2. DILARANG menambah baris matriks tanpa pasangan sumber.
3. DILARANG menulis vonis baru dalam bentuk apa pun (termasuk
   "kesimpulan sementara" atau "rekomendasi vonis").
4. DILARANG menaikkan/menurunkan status vonis lama.
5. DILARANG pointer ke file internal Asisten — brief ini mandiri.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness: tiap baris matriks punya pasangan sumber? tiap
kutipan verbatim + bernomor baris? hash ditempel sesudah tulis terakhir?
Putaran 2 — Bias & Asumsi: ada kalimat yang menyelamatkan H-gugur? ada
redefinisi pasca-hoc? ada opsi §5 yang diam-diam diputuskan?
Putaran 3 — Meta-check: file hanya satu + di lokasi kanonis? format
ASCII/LF tanpa self-hash? nol commit/push/test?

## Output yang dikembalikan

Tulis draf sebagai **file .md** di
`reports/governance/2026-10-09/evaluasi-cakupan-riset.md`, lalu kembalikan:
path file + tabel Klaim & Bukti (TERVERIFIKASI / BELUM DIVERIFIKASI /
ASUMSI + bukti) + daftar yang belum diverifikasi + potensi masalah.
Bahasa Indonesia.
