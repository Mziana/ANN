# Putusan Arsitek I-1 / V-3: 7 ASLI Diterima Terbatas, EDA-07 Dilanjutkan (2026-10-12)

Peran: Arsitek (rangkap asisten atas perintah user 2026-10-10).
Status: MENGIKAT. V-1 s/d V-3 putusan-eda07-g2.md tetap utuh.

## V-4 I-1 DINYATAKAN SAH (verifikasi asisten dari artefak)

- T-I1-1/2/3 masing-masing 86 baris; vonis_V2 = 7 ASLI / 79 ARTEFAK,
  sesuai klaim coder baris-per-baris (7 ASLI semuanya round_d x LB
  Tokyo/London N5/N15; 52/52 pdhl_d ARTEFAK, 39 JAUH-mendominasi).
- File run 9 tak tersentuh: _gate_ skrining/alarm sama dengan ukuran
  asisten sebelum I-1 (8cc207ac / 31f6959e). HEAD b18992b, staged nol.
- Kalibrasi negatif 0/6 noise + rebuild bit-identik + 591 assert:
  mesin I-1 sah, aturan V-2 diterapkan verbatim, tanpa promosi kontrol.
- Cacat kecil dicatat jujur coder (CRLF, lock basi, stream dipakai ulang,
  LB_rng pakai selisih mean) dinilai non-material: tak satu pun mengubah
  definisi DEKAT/JAUH, X=10 tunggal, atau aturan putus. Diterima dengan
  catatan untuk auditor.

## V-5 Reklasifikasi terbatas (wewenang V-3)

- 7 pasangan round_d DINAIKKAN dari "kontrol" menjadi "fitur kandidat",
  HANYA untuk 7 pasangan itu (LB London t3/tALL N5; LB Tokyo t2/tALL
  N15/N5). Di luar 7 pasangan itu round_d tetap kontrol.
- 52/52 pdhl_d DITUTUP sebagai ARTEFAK proxy-jarak (pola JAUH-dominan =
  ciri falsifikasi V-2). DILARANG dibawa ke tahap mana pun sebagai sinyal.
- Kenaikan ini BUKAN izin Lapisan 3: G1/G3/G4 untuk 7 kandidat BELUM
  dinilai (sel 16-18 tak pernah jalan). Tanpa G1/G3/G4, kandidat =
  bukan kelolosan.

## V-6 Mandat penyelesaian EDA-07 (I-2, mengikat)

Fakta yang belum terjawab: status G2 fitur ASLI (bukan kontrol) tak
diketahui - skrining 780 baris hanya berisi kontrol; sel verdict tak
pernah tereksekusi. Maka:

- I-2 = run penyelesaian: evaluasi G1-G4 PENUH (fitur asli + 7 kandidat
  round_d), T-07-1..4, FIG-13..16, sel kesimpulan terisi.
- Gerbang kontrol pada I-2 diganti pemeriksaan regresi (bukan STOP
  buta): alarm kontrol harus SAMA dengan himpunan 86 teradjudikasi;
  kontrol BARU lolos di luar 86 = STOP + adjudikasi baru. Alasan:
  gerbang sudah menjalankan tugasnya dua kali; mengulang STOP yang sama
  tanpa informasi baru adalah teater.
- Kriteria A-3 + alarm A-7 tetap; X dan aturan I-1 tidak dibawa ke I-2
  kecuali sebagai definisi fitur kandidat; Lapisan 3 tetap terkunci
  sampai I-2 + auditor selesai.

Berikutnya: brief coder I-2 (paste-manual), lalu eksekusi.
