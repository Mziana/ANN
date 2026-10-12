# Brief Eksekusi Coder EDA-07 (paste-manual, FINAL, siap paste ke coder)

Peran: Coder. Tugas: bangun + eksekusi EDA-07 label-fitur deskriptif.
BUKAN arsitek (tidak merancang ulang), BUKAN auditor (tidak menilai
vonis lama). Workdir: D:\ANN. Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (kontrak kerja, S5 format laporan),
   reports/governance/2026-10-10/arsitek/spesifikasi-eda07-label-fitur.md
   (SPEC BEKU S1-S9, blob 429892bd15ac4590fd755ec327a7f9ab3ef85096),
   reports/governance/2026-10-10/arsitek/putusan-eda06.md (P-1 s/d P-6,
   blob 03b0a8cdfa5541cf635dc949429061718a63c971),
   thoughts/shared/references/eda06/EDA_06_07_rancangan.md (bagian 0-3,
   pola label/fitur), scripts/_build_eda06.py (pola builder dipakai ulang).
2. Patuh AGENTS.md penuh: reuse-first (pola scripts/_build_eda06.py +
   notebooks/scalping/_eda_common.py), tanpa dependensi baru, tanpa tulis
   ke configs/src/data, tanpa commit/push, tanpa klaim tanpa bukti.
3. Setiap syarat di bawah berpasangan perintah mentah + output ditempel di
   laporan. Klaim tanpa output mentah = GAGAL (tulis eksplisit).
4. Bila instruksi bertentangan dengan vonis terkunci
   (H1/H2/H3/H5/H4b/R-2 GUGUR, H4 TAHAN) atau dengan spec S1-S9,
   STOP dan laporkan konflik; jangan improvisasi.

## S5 Tugas (substansi dari spec S1-S9, tidak diringkas ulang)

1. Tulis scripts/_build_eda07.py (generator + executor nbconvert, pola
   _build_eda06.py): setup venv kanonik (pandas 2.x tolak 3.x,
   tzdata 2026.5), PROJECT_ROOT via pyproject.toml + src/, fingerprint
   sesi assert keras, load_config("data"), wall_clock_series hari-broker.
   Parquet M1 2023-2025 saja (2026 tidak dimuat; bar tepi hari-broker
   dibuang, jumlah dicetak). Strata A/B/C pola EDA-06 (B = 185.248
   di-assert). Irisan dibaca dari CSV T-06-7 (assert 23 + 7, STOP bila
   berubah). Satu stream RNG per analisis (seed berbeda per blok,
   tercatat, iterasi grup terurut, rerun bit-identik).
2. Bangun + eksekusi notebooks/scalping/eda_07_label_fitur.ipynb dari
   atas ke bawah sampai 0 error, urutan terbukti. Empat label S3
   (LA barrier-hit per sisi combo irisan itu; LB besaran biner + kontinu,
   margin 0,20 pip; LC 3-kelas theta 1x + varian 2x; LD tanda pembanding),
   horizon N 5/15/30/60, sampel tanpa tumpang-tindih + bootstrap
   klaster-hari, buang jendela lewati gap/anomali (lapor per alasan).
   Fitur S4 daftar tertutup + 3 kontrol wajib (derau seed-terkunci,
   level bulat, prior-day H/L). Metode S5 (MI 20 kuantil + lantai derau
   permutasi blok-hari 100x p95, lift per desil + CI, Spearman kontinu,
   redundansi |rho| > 0,8 satu wakil). Stabilitas S6 per semester/sesi/
   strata (B terpisah, 2026 tidak dimuat). Anti-leakage S7 200/200 wajib
   (satu gagal = HIGH, STOP). Gerbang G1-G4 S8 per irisan identik
   (G2/G4 gagal = irisan itu BERHENTI). Assertion mesin >= 20. FIG-13..16
   sekuensial (DILARANG pakai ulang FIG-01..12), registry tepat
   FIG-01..akhir. T-07-1..4 teks + CSV satu lokasi reports/eda/<tanggal>/
   (catat). Sel kesimpulan SATU paragraf WAJIB terisi manual SETELAH
   baca tabel (kunci label + horizon/barrier + daftar fitur Lapisan 3).
3. Serahkan laporan pola AGENTS.md S5: file dibuat/diubah + apa dilakukan +
   tabel Klaim & Bukti (TERVERIFIKASI/BELUM DIVERIFIKASI/ASUMSI) +
   yang belum diverifikasi + potensi masalah + rekomendasi irisan x label
   x fitur layak ke Lapisan 3 (tanpa vonis, tanpa klaim edge).

## Perintah mentah wajib (tiap syarat berpasangan output ditempel)

- Klaim file ada + ukuran: tempel output
  git hash-object scripts/_build_eda07.py +
  notebooks/scalping/eda_07_label_fitur.ipynb SESUDAH tulis terakhir
  + baris/byte tiap file.
- Klaim referensi tak berubah: tempel output
  git hash-object thoughts/shared/references/eda06/eda_06_biaya_breakeven.ipynb
  (harus 6a6c6516bc96e7e9a7845a13b1909927cc718e75) +
  git hash-object thoughts/shared/references/eda06/EDA_06_07_rancangan.md
  (harus 6724c37ec5493b821d0179d0d00768fbd343a485) +
  baris CSV T-06-7 tercile (144/23) + sesi (48/7).
- Klaim spec tak berubah: tempel output
  git hash-object reports/governance/2026-10-10/arsitek/spesifikasi-eda07-label-fitur.md
  (harus 429892bd15ac4590fd755ec327a7f9ab3ef85096) +
  git hash-object reports/governance/2026-10-10/arsitek/putusan-eda06.md
  (harus 03b0a8cdfa5541cf635dc949429061718a63c971).
- Klaim tanpa commit/stage oleh ronde ini: tempel output
  git status --porcelain=v1 + git rev-parse HEAD.
- Klaim ASCII/LF-only/tail-LF untuk builder: tempel output cek non-ASCII +
  CRLF + byte terakhir (perintah + output, bukan ringkasan).
- Klaim notebook tereksekusi + sel kesimpulan terisi: tempel output eksekusi
  (urutan sel + 0 error) + isi paragraf kesimpulan + daftar FIG/CSV tersimpan.
- Klaim angka: tiap angka penentu (irisan 23+7, lantai derau, MI fitur,
  lift desil, G1-G4 per irisan, 200/200 anti-leakage) menyebut sel notebook
  + artefak CSV + sha bila ada.
- DILARANG imbauan umum ("pastikan hash benar"). Klaim tanpa output
  mentah = GAGAL (tulis eksplisit).

## Larangan bentuk-spesifik ronde ini

1. DILARANG menambah irisan, label ke-5, atau fitur non-daftar sebagai
   penentu; DILARANG optimasi theta/bin/window pasca-hoc.
2. DILARANG melatih model/baseline/ANN/backtest/P&L sebagai klaim.
3. DILARANG memuat 2026, memakai tipologi full-sample, atau masa depan
   sebagai fitur; DILARANG klaim efek berita.
4. DILARANG generalisasi sesi (konsentrasi Tokyo/London menempel);
   tiap klaim menyebut irisan eksplisit.
5. DILARANG klaim edge tradable; satu-satunya klaim boleh: irisan X
   label Y fitur Z layak/tidak-layak ke Lapisan 3.
6. DILARANG menambah dependensi (sklearn/numba DILARANG); hanya pandas,
   numpy, scipy, matplotlib yang sudah ada.
7. DILARANG menulis ke configs/src/data; DILARANG commit/push; DILARANG tulis
   governance selain laporan tugas.
8. DILARANG mengubah/menafsir-ulang vonis H1-H5/H4b/R-2 atau definisi sesi/Off.
9. DILARANG pointer ke file internal asisten di luar repo; brief ini mandiri.

## SELF-AUDIT 3x ADVERSARIAL (wajib di laporan)

Putaran 1 Correctness: tiap label/fitur dari t<=entry saja? 200/200
anti-leakage? threshold pre-registrasi tanpa scan? fingerprint cocok?
irisan tepat 23+7 dari CSV? assertion >= 20 lolos? sel kesimpulan terisi?
rerun bit-identik? FIG-13..16 sekuensial? T-07-1..4 + CSV ada?
Putaran 2 Bias: ada H-gugur yang diselamatkan? ada theta/bin yang
dioptimasi diam-diam? ada slice tunggal digeneralisasi? ada kontrol yang
informatif tapi diabaikan? ada akurasi/MI yang diklaim sebagai edge?
ada G4 yang lolos tanpa tautan delta irisan?
Putaran 3 Meta-check: file hanya builder + notebook di lokasi kanonis?
referensi + spec tak tersentuh (4 hash cocok)? format ASCII/LF builder?
nol commit/push? nol model/backtest? nol vonis baru? nol tulis governance
selain laporan?
