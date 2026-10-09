# PROMPT_DISIPLIN.md — Doktrin Penyusunan Prompt (keputusan user 2026-10-08, WAJIB)

> **RUANG LINGKUP (klarifikasi 2026-10-08): file ini KHUSUS Asisten.**
> Coder/arsitek/auditor TIDAK perlu membacanya dan brief mereka DILARANG
> memuat pointer ke file ini. Setiap brief peran harus mandiri: klausul
> yang relevan (pasangan syarat+perintah mentah, larangan bentuk-spesifik,
> larangan vonis di luar lingkup, perintah .md + lokasi file) WAJIB disalin
> eksplisit ke dalam brief itu sendiri. File ini mengatur *bagaimana Asisten
> menyusun brief*, bukan *bagaimana peran lain bekerja*.
>
> Pengecualian: kontrak BERSAMA tetap boleh — dan wajib — dirujuk, yaitu
> `.ai/AGENTS.md` (berlaku untuk semua peran AI: §26 peran, §5 format
> laporan Klaim & Bukti, §20 anti-halusinasi, §21 protokol empiris).
> Yang dilarang hanya pointer ke file INTERNAL Asisten (PROMPT_DISIPLIN.md,
> REPORT_EXPLAINER.md, verifications/, dsb).

> File ini WAJIB dibaca Asisten setiap kali membaca `README.md` dan setiap kali
> menyusun prompt untuk coder/arsitek/auditor. Berlaku otomatis — bukan opsional,
> bukan "jika sempat". Alasan lahirnya: re-audit kedua (2026-10-08) membuktikan
> 60% kesalahan coder adalah disiplin verifikasi (klaim mendahului pengukuran),
> 25% adalah instruksi yang hanya menyebut *apa* tanpa *bagaimana-yang-bisa-dicek-mesin*,
> 15% adalah proses tanpa gerbang pra-audit.

## Aturan 1 — Pasangan syarat + perintah mentah

Setiap syarat fix dalam prompt WAJIB dipasangkan dengan perintah mentah yang
outputnya wajib ditempel di laporan. DILARANG bentuk imbauan umum ("pastikan X").

- Benar: "tempel output `git hash-object <file>` SESUDAH penulisan terakhir untuk tiap file klaim"
- Benar: "tempel output `git status --porcelain` untuk klaim tanpa-stage"
- Benar: "tempel output full-suite (bukan satu file) untuk klaim jumlah test"
- Salah: "pastikan hash benar", "pastikan tidak ada stage", "pastikan test hijau"

Klaim tanpa output mentah = gagal (tulis eksplisit di prompt).

## Aturan 2 — Larangan bentuk-spesifik (hasil pelajaran, terus ditambah)

Setiap ronde audit yang menemukan pola lolos-celah wajib diabadikan di sini
sebagai larangan bentuk-spesifik — bukan imbauan umum. Daftar awal (dari
re-audit pertama + kedua + adjudikasi):

1. DILARANG `utc.normalize()` / merekonstruksi hari dari UTC — grain tunggal
   hari-broker dari store (`date_broker`).
2. DILARANG membandingkan nilai dengan dirinya sendiri dalam guard apa pun
   (mis. `norm` vs `d/a` yang mendefinisikannya) — termasuk yang dibungkus
   komentar/docstring.
3. DILARANG fixture seragam (open/close sama di semua bar) untuk test yang
   mengklaim sensitif terhadap parameter/jendela.
4. DILARANG test tanpa assertion yang dihitung dalam total klaim.
5. DILARANG menempel output parsial (satu file) dengan label proses penuh
   ("pytest penuh", "ruff repo").
6. DILARANG klaim "diuji via X" di satu bagian sambil mengaku "belum ada test X"
   di bagian lain dokumen yang sama.
7. DILARANG menaikkan severity temuan yang sudah tertutup.
8. DILARANG kutipan baris/path tanpa verifikasi ulang (path bisa pindah folder,
   baris bisa bergeser).

Setiap temuan BARU di audit berikutnya yang berjenis "lolos-celah instruksi":
tambahkan sebagai butir 9, 10, … sebelum menyusun prompt fix berikutnya.

9. Guard provenans/identitas: deret referensi WAJIB dibaca dari sumber terpisah
   dari objek yang diperiksa (mis. store parquet dibaca ulang), DILARANG
   mengoper kolom dari frame yang sama lalu membandingkannya (`allclose(X, X)`
   benar untuk setiap X). Sabotase pembuktian WAJIB diarahkan ke jalur produksi
   persis seperti `main()` memanggilnya — DILARANG harness yang mensnapshot
   referensi SEBELUM sabotase (menguji kondisi yang tak pernah terjadi di
   produksi). (Pelajaran: re-audit ketiga §3 — 7/9 sabotase lolos di produksi
   meski suite hijau.)
10. Klaim gate format/lint wajib menyebut rc + cakupan (repo vs file): frasa
    "[N] files already formatted" hanya sah bila rc=0; file yang ditulis batch
    itu sendiri wajib rc=0; bila repo memuat kegagalan pra-ada di luar scope,
    D5 wajib membatasi klaimnya secara eksplisit, bukan mengklaim repo.
    (Pelajaran: re-audit ketiga §8.2 — klaim exit=0 padahal rc=1 di L149
    tulisan-batch-3 sendiri.)
11. Byte-reprodusibilitas parquet terikat toolchain (pyarrow/pandas): klaim
    byte-identik wajib menyebut versi; bila artefak di disk dibangun toolchain
    berbeda, catat eksplisit sebagai perbedaan metadata — DILARANG dibaca
    sebagai non-determinisme pipeline maupun sebagai reprodusibilitas.
    (Pelajaran: re-audit ketiga §8.4.)
12. Konstanta yang mengikat kalibrasi (mis. `RV_WINDOW_DAYS`) wajib dikunci test:
    mengubahnya tanpa TAU yang dihitung ulang HARUS merah. Membandingkan
    konstanta-dengan-konstanta bukan penguncian. (Pelajaran: re-audit ketiga
    §8.3 — mutasi 20→10 lolos.)

## Aturan 3 — Gerbang pra-audit Asisten

Laporan peran (coder/arsitek/auditor) DILARANG langsung menjadi bahan prompt
berikutnya. Sebelum menyusun prompt audit/fix lanjutan, Asisten WAJIB
verifikasi dulu fakta disknya sendiri:

1. `git hash-object` tiap file yang diklaim (cocok dengan yang ditempel?)
2. Jumlah baris / pagu (AST bila perlu)
3. `git status --porcelain` (klaim tanpa-stage benar?)
4. Byte-reprodusibilitas artefak (run ulang ke tmp, bandingkan sha256) bila relevan

Hasil gerbang ditulis di `verifications/` + dilapor ke user. Hanya yang lolos
gerbang yang diteruskan ke prompt berikutnya; yang gagal dikembalikan dengan
bukti, bukan diteruskan ke auditor.

## Pemicu otomatis

- Membaca `README.md` → WAJIB membaca file ini sampai habis, lalu terapkan
  ketiga aturan pada pekerjaan prompt berikutnya.
- Menyusun prompt apa pun → cek ulang: tiap syarat punya pasangan perintah
  mentah (Aturan 1)? larangan bentuk-spesifik sudah mencakup pelajaran lama
  (Aturan 2)? perintah .md + lokasi file eksplisit ada (README Pengingat
  Operasional)? gerbang pra-audit terjadwal (Aturan 3)?
