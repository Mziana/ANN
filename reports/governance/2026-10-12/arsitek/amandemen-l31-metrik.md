# Amandemen B-3: Metrik per-Jenis untuk LB_rng Kontinu (2026-10-12)

Status: MENGIKAT. Menyatu dengan B-3 (putusan-l30-audit.md);
bagian yang diubah hanya M2/M3 untuk jenis kontinu + kunci
sekunder. Selebihnya B-3 utuh (103 pasangan, split, seed,
larangan, B-4).

## C-1 Kesalahan yang diakui

B-3 mengunci `Brier untuk semua 103` sementara S3-2 M2 menulis
`pilih SATU per target-kind` (mengakui jenis label berbeda).
B-3 over-spesifikasi melampaui spec. Amandemen ini MEMULIHKAN
maksud spec, bukan melonggarkan gerbang: bentuk gerbang sama
(kalahkan null + stabil per-semester), metrik mengikuti jenis.

## C-2 Aturan terdaftar per-jenis (M2 revisi)

- Diskret (LB_bin, LC1, LC2, LD; 67 baris): Brier + akurasi,
  null = mayoritas-kelas train global. M3 (a)(b)(c) B-3 UTUH.
  Brier multikelas = rerata kuadrat galat probabilitas atas
  semua kelas (definisi standar). Margin 0,001 absolut berlaku
  untuk semua diskret; untuk multikelas bar absolut ini relatif
  longgar dan DIKOMPENSASI konjungsi (b)+(c) - dicatat jujur.
- Kontinu (LB_rng; 36 baris): MSE primer + MAE sekunder,
  null = mean train global, baseline = mean train per-iris.
  M3-kontinu menang IFF: (a) MSE_mod < MSE_null x 0,99 pada
  test pooled; DAN (b) MSE_mod < MSE_null pada MASING-MASING
  2025H1 dan 2025H2; DAN (c) MAE_mod < MAE_null pooled.
  Gagal satu = GUGUR permanen ronde ini.

## C-3 Kunci sekunder (ditutup di sini, DILARANG diisi coder)

- Prediksi kelas baseline: argmax distribusi marginal per-iris.
  Tie -> mayoritas-kelas train global; masih tie -> indeks
  kelas terendah. Deterministik.
- Tie-break mayoritas null: aturan yang sama.
- 5 baris round_d vs kembaran nativenya: label per-bar SAMA
  (satu seri label, M1 + flag berbeda) -> M3 keduanya WAJIB
  identik; assert mesin kesamaan ini sebagai cek konsistensi.
- DITOLAK permanen: binarisasi LB_rng (label baru), bin-20
  sebagai kelas (tepi kuantil tak teregistrasi), MSE
  dilaporkan sebagai Brier, drop-36, normalisasi per-jenis
  yang oportunistik.

## C-4 S8A: satu amandemen, lalu eksekusi

Konflik ini arbitrase satu-putaran atas celah authorship
(komposisi jenis-vs-metrik tak diaudit sebelum kunci M3 -
pelajaran proses dari coder, DITERIMA). Bukan preseden ronde
baru. Setelah addendum, L3-1 dieksekusi; vonis tetap biner
B-4 pasca-audit L3-1.
