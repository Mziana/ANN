# Laporan Tahap 14 — C4: Figures FIG-04..07 + Verifikasi Registry (Skema D9)

**Tanggal:** 2026-10-06 · **Skema terkunci (putusan D9):** FIG-01..03 = nb01
(M1/M5/M15 QQ); FIG-04+ sekuensial dari nb05. Notebook WAJIB memverifikasi registry —
di-assert di dalam nb05 dan diverifikasi ulang dari disk di luar notebook.

**Patokan notebook aktif (F-B802):** `notebooks/scalping/eda_05_regimes.ipynb` blob
`661c0aeb235760dab66f202d7f2b84f52499e21a` (`git hash-object`, EOL **LF** deterministik dari builder — KOREKSI NL2, 2026-10-07) — regenerasi penuh
2026-10-07, 26 sel (19 kode), 68 assertion PASS. Semua rujukan sel di bawah patok ke
blob ini. (KOREKSI M1 2026-10-07: Pin lama `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` dipensiunkan karena merge chunking output pada regen NL2 — bukan karena era CRLF (provenance Q4.2); klaim EOL era KOREKSI B9-02 ikut dipensiunkan.)

(KOREKSI B9-02: klaim `LF` pada patokan di atas sebelumnya salah — pembacaan byte disk:
83.611 byte = 1.663 CRLF + 0 LF-only → EOL notebook SAAT ITU = CRLF. Akar masalah: kelima
builder memakai `NB_PATH.open("w", encoding="utf-8")` tanpa `newline=` (lihat
`scripts/_build_eda05.py:1109`), sehingga `\n` menjadi `\r\n` di Windows. Fakta (a):
binding hash tetap benar — konvensi `git hash-object` LF-normalized, terverifikasi
identik dengan hash konten LF (tidak terpengaruh EOL). Fakta (b) — STATUS KOREKSI NL2
(2026-10-07): akar masalah DITUTUP — `newline="\n"` mendarat di kelima builder (F-NL) +
langkah pasca-proses CRLF→LF sesudah nbconvert `--inplace` (F-NL2, putusan Q2); regen
nb05 = 81.851 byte, 0 CR, LF deterministik dari builder.)

## Tabel Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Empat figure baru tersimpan oleh nb05 | TERVERIFIKASI | output nb05 sel json idx 22 (kode_sel #17, `execution_count` 17): `tersimpan: …FIG-04.png …FIG-07.png` (4 baris) |
| Registry = tepat FIG-01..07 | TERVERIFIKASI | output nb05 sel json idx 23 (kode_sel #18, `execution_count` 18): `PASS: registry figures tepat FIG-01..FIG-07`; cek disk: `glob("*.png")` = 7 file persis |
| FIG-01..03 tidak tersentuh rerun nb05 | TERVERIFIKASI | hash HEAD vs worktree: `709db8ae0d64` / `e55fc1f5294b` / `73d65368398b` = **IDENTIK** ×3; mtime tetap 15:49:27 |
| FIG-04..07 valid PNG, ukuran benar | TERVERIFIKASI | header IHDR dibaca: FIG-04/05/06 = 840×540 (7×4,5 in @120dpi), FIG-07 = 960×540 (8×4,5); semua >20 KB |
| Satu figure satu pesan | TERVERIFIKASI | FIG-04 range/ATR A-vs-B · FIG-05 RV harian log10 · FIG-06 tipologi per strata · FIG-07 mean\|r\| per jam UTC (masing-masing 1 pesan, dirujuk report.md) |

## Hash · mtime · ukuran (worktree, dibaca dari disk)

```
709db8ae0d64  28695B  15:49:27  FIG-01.png  (HEAD-identik)
e55fc1f5294b  31344B  15:49:27  FIG-02.png  (HEAD-identik)
73d65368398b  32883B  15:49:27  FIG-03.png  (HEAD-identik)
3420bca32643  31927B  11:42:24 2026-10-07  FIG-04.png  (baru; mtime diperbarui rerun Batch C, hash IDENTIK)
fedd896ff8a2  27778B  11:42:24 2026-10-07  FIG-05.png  (baru; mtime diperbarui rerun Batch C, hash IDENTIK)
124867c6620c  21101B  11:42:24 2026-10-07  FIG-06.png  (baru; mtime diperbarui rerun Batch C, hash IDENTIK)
a90a16b0e40d  23351B  11:42:24 2026-10-07  FIG-07.png  (baru; mtime diperbarui rerun Batch C, hash IDENTIK)
```

(Catatan Batch C: hanya baris FIG-04..07 di atas yang disentuh — mtime-nya basi karena
rerun penuh 2026-10-07. Baris FIG-01..03 dan klaim mtime "15:49:27" sengaja TIDAK
diubah — temuan B8-01 dikecualikan: bulk EOL sync 10:42:00 menetralkan mtime sebagai
bukti, jalur hash tetap pendukung utama.)

## Konvensi penomoran sel (jawaban Q1 auditor — F-B802)

- **Konvensi yang dipakai dokumen ini: json idx** — index 0-indexed dalam daftar
  `cells` JSON notebook. Konvensi ini konvensi yang juga dipakai auditor
  (`audit:2573` menyebut "json idx 18") dan `tahap_12:5` (sel #13–#18).
  Agar silang-verifikasi tanpa tebakan, tiap rujukan kini disandingkan **kode_sel**
  (nomor ke-k di antara sel kode, 1-indexed) dan **`execution_count`** — mis. figures
  = json idx 22 = kode_sel #17 = exec 17; registry = json idx 23 = kode_sel #18 = exec 18.
- Rujukan lama "sel #21"/"#22" ditulis tanpa patokan blob (temuan B8-02) dan basi
  setelah Batch A/B menambah sel — `tahap_12:5` mencatat pergeseran serupa
  (H1–H5 `#13–#17` → `#13–#18`). Blob notebook lama tidak tersimpan di Git
  (nb05 untracked; `git cat-file -e 8158d5b57b20e` / `2d8f600acade` → tidak ada),
  sehingga posisi lama tak dapat direkonstruksi ulang; rujukan kini dipatok ke blob
  aktif di header laporan ini.

## Self-audit 3×

1. **Correctness** — registry dicek dua jalur (assert di dalam nb05 + listing disk di
   luar notebook); dimensi dibaca dari byte IHDR, bukan dari niat kode.
2. **Bias & asumsi** — penomoran mengikuti skema D9 tanpa pengecualian; tidak ada
   figure yang menampilkan inferensi sinyal (semua deskriptif).
3. **Meta-check** — FIG-01..03 byte-identik membuktikan nb05 tidak mem-bypass skema;
   jumlah total 7 = 3 (nb01) + 4 (nb05), sesuai "satu grafik satu pesan" §3 v3.1.

## Yang belum diverifikasi

- Keterbacaan visual figure untuk manusia (reviewer yang menilai; angka dasarnya
  terverifikasi dari output sel).
