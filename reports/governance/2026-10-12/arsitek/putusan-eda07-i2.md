# Putusan Arsitek I-2: Eksekusi Diterima, Lapisan 3 Terkunci hingga Audit (2026-10-12)

Peran: Arsitek (rangkap asisten atas perintah user 2026-10-10).
Status: MENGIKAT. V-1 s/d V-6 tetap utuh.

## W-1 I-2 prosedural DITERIMA (bukan vonis isi)

Regresi 86/86 + 780/780 bit-identik, K24 24/24, 13/13 file beku sama,
T-07 x4 + FIG-13..16 + kesimpulan terkunci, 569 assert, HEAD tak gerak.
Semua diverifikasi asisten dari artefak (gerbang-hasil-i2.md).

## W-2 Disposisi C1-C3 coder

- C1 (37-vs-30): DITERIMA sebagai artefak tampilan. 7 pseudo-irisan dari
  target LA berkind-ses = perilaku verbatim run 9 (terverifikasi di
  builder beku + rekalkulasi independen = persis 37). Verdict per-target,
  gerbang, kandidat, FIG pick tak terpengaruh. Auditor wajib konfirmasi
  independen; bila auditor menemukan dampak ke verdict, putusan ini
  BATAL sebagian dan I-2 diulang.
- C2 (19-sel literal): kosmetik, abaikan. Angka acuan = parse ipynb.
- C3 (lift negatif): DITERIMA sebagai fakta dengan bacaan mengikat:
  5 LOLOS Tokyo = efek INVERS (dekat level bulat -> besaran LEBIH KECIL),
  konsisten dengan cerita magnet/stall, BERLAWANAN dengan intuisi sinyal.
  DILARANG memakai 5 LOLOS sebagai dasar sinyal long/label; DILARANG
  mengklaim edge positif. Sifat invers menempel pada setiap pemakaian
  5 kandidat ke depan.

## W-3 Nasib Lapisan 3: TERKUNCI (belum diputus)

Alasan: (a) auditor belum memverifikasi I-2 (wajib multi-AI);
(b) 98 LOLOS native belum dibaca arah-per-arahnya oleh arsitek
(153 baris G3-pass, 33 berlift negatif - tiap pemakaian harus tahu
arahnya seperti C3); (c) G4 hanya bermakna untuk LA (target-waktu
G4=NA), sehingga kriteria "layak ke Lapisan 3" untuk 98 pasangan
butuh definisi kelayakan model (null-model pembanding) yang BELUM ADA
di spec mana pun - itu isi spec Lapisan 3, bukan putusan ini.
Membuka Lapisan 3 sekarang = membuka tanpa gerbang masuk.

## W-4 Perintah auditor (ruang lingkup reaudit EDA-07)

Reaudit independen mencakup run 9 + I-1 + I-2: (i) A-3/A-7 tepat;
(ii) nol drift ambang lintas 3 ronde; (iii) V-1/V-2/V-4 dari CSV;
(iv) C1 independen (37 = 30 + 7, tanpa dampak verdict);
(v) C3 verbatim (aturan G3 tanpa syarat arah + invers tercatat);
(vi) kepatuhan I-1/I-2 ke falsifikasi dan batas scope.
Tanpa lolos audit ini, W-3 tidak dapat dibuka.

Berikutnya: brief reaudit auditor EDA-07 (paste-manual).
