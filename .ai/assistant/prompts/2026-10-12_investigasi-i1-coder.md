# Perintah Coder I-1: Investigasi Alarm Struktural (paste-manual, FINAL)

Peran: Coder. Tugas: investigasi terbatas I-1 atas 80 alarm struktural,
deskriptif, tanpa model, tanpa vonis edge. BUKAN arsitek (DILARANG ubah
aturan putus V-2), BUKAN auditor. Workdir: D:\ANN. Bahasa: Indonesia.
STOP setelah serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (S5 format laporan),
   reports/governance/2026-10-12/arsitek/putusan-eda07-g2.md (V-1/V-2/V-3
   MENGIKAT, blob 6c9644c57d0c28422815c55976780a7620a2c22e),
   reports/eda/2026-10-12/laporan-coder-eda07-g2.md (konteks run 9),
   reports/eda/2026-10-12/_gate_G2_alarm.csv (80 alarm = scope),
   reports/governance/2026-10-10/arsitek/amandemen-eda07-alarm.md (A-7/A-8).
2. Patuh AGENTS.md penuh: reuse-first (fungsi label/fitur run 9 dipakai
   ulang, bukan ditulis ulang), tanpa dependensi baru, tanpa tulis ke
   configs/src/data, tanpa commit/push, tanpa klaim tanpa bukti.
3. Setiap syarat berpasangan perintah mentah + output di laporan.
   Klaim tanpa output mentah = GAGAL (tulis eksplisit).
4. Bila bertentangan dengan V-2/V-3 atau vonis terkunci, STOP dan
   laporkan; jangan improvisasi.

## S5 Tugas (batas I-1, DILARANG melampaui)

1. Adendum kecil (bukan full-run): scripts/_build_eda07_i1.py +
   notebooks/scalping/eda_07_i1_adendum.ipynb, reuse path kode run 9
   untuk label + fitur (round_d, pdhl_d, rv15, LB/LC/LD/LA). Assert
   konsistensi: >= 1000 entri sampel, label/fitur hitung-ulang SAMA
   PERSIS dengan pipeline run 9. Satu beda = STOP.
2. Q1 konsentrasi (deskriptif, tanpa gerbang): tabulasi 80 alarm per
   target/irisan/sisi/sesi/horizon + 6 noise sebagai pembanding.
   Output T-I1-1 (teks + CSV satu lokasi reports/eda/2026-10-12/).
3. Q2 uji-kedekatan (pra-registrasi, mengikat): X = 10 pip (satu nilai,
   DILARANG pindai ambang). DEKAT = |jarak| <= 10 pip dari level
   (bulat untuk round_d, PDH/L untuk pdhl_d); JAUH = sisanya. Per
   pasangan alarm: P(label | DEKAT) vs P(label | JAUH) + CI klaster-hari.
   Kalibrasi negatif: prosedur SAMA pada 6 alarm noise (ekspektasi
   pra-registrasi: tidak berpola; bila berpola = mesin I-1 rusak, STOP).
   Output T-I1-2 + vonis-per-pasangan (DEKAT-mendominasi / JAUH-
   mendominasi / tak-beda).
4. Q3 uji-proxy (pra-registrasi, mengikat): dalam irisan, belah sampel
   per median rv15 (rendah/tinggi) + per desil rv15 (10 grup). Hitung
   lift DEKAT-vs-JAUH per grup. Bertahan = tanda sama >= 7/10 desil DAN
   lift pooled-dalam-grup CI tidak memuat 0. Output T-I1-3 + vonis Bertahan
   / Lenyap per pasangan.
5. Vonis-per-kontrol (aturan putus V-2, DILARANG ubah): ASLI bila dan
   hanya bila lift-kedekatan (Q2 DEKAT-mendominasi) BERTAHAN setelah
   stratifikasi (Q3); selain itu ARTEFAK. Hasil campuran
   (mis. pdhl_d vs round_d beda) diputus per kontrol apa adanya.
   DILARANG promosikan kontrol jadi fitur sinyal; hanya label
   ASLI/ARTEFAK + bukti. Sel kesimpulan SATU paragraf WAJIB terisi.
6. Serahkan laporan S5: file + tabel Klaim & Bukti + yang belum
   diverifikasi + potensi masalah + rekomendasi (tanpa vonis edge,
   tanpa buka Lapisan 3 - itu wewenang arsitek di V-3).

## Perintah mentah wajib

- Hash builder + notebook SESUDAH tulis terakhir + baris/byte.
- Bukti reuse: nama fungsi run 9 yang dipakai ulang + assert 1000
  sampel SAMA PERSIS (perintah + output).
- Bukti konstanta I-1: X=10 pip + seed + definisi DEKAT/JAUH tercatat
  dan di-assert (perintah + output); bukti 24/24 konstanta run 9
  tak tersentuh (diff kosong).
- Bukti bukti run 9 tak tersentuh: hash _gate_*.csv + _ckpt_*.csv
  SEBELUM vs SESUDAH I-1 = sama (8090.../...: tempel kedua output).
  Catatan: folder kini reports/eda/2026-10-12/ (pindahan 2026-10-12).
- Bukti eksekusi: urutan sel + 0 error + T-I1-1/2/3 + isi paragraf
  kesimpulan + daftar CSV.
- Bukti kalibrasi negatif: hasil Q2/Q3 pada 6 noise (harus tak-berpola).
- git status --porcelain=v1 + git rev-parse HEAD (nol stage ronde ini).
- Cek ASCII/LF/tail-LF builder (perintah + output).
- DILARANG imbauan umum. Klaim tanpa output mentah = GAGAL.

## Larangan

1. DILARANG label/fitur/irisan baru; DILARANG pindai X/ambang/desil.
2. DILARANG ubah aturan putus V-2; DILARANG promosikan kontrol.
3. DILARANG model/backtest/P&L/vonis/edge sebagai klaim.
4. DILARANG tulis configs/src/data/governance selain laporan tugas.
5. DILARANG commit/push. DILARANG pointer ke file internal asisten.
6. DILARANG sentuh file run 9 (_gate_, _ckpt_, notebook run 9) tulis;
   baca saja (ditambah bukti hash sebelum/sesudah di atas).
