# Spesifikasi Lapisan 3: Baseline Terkalibrasi di atas EDA-07 (2026-10-12)

Status: DRAF ARSITEK, butuh persetujuan user sebelum brief coder.
Sifat: deskriptif-prediktif. Tanpa P&L, tanpa backtest klaim edge,
tanpa rekomendasi strategi. Fondasi = EDA-06 + EDA-07 TERTUTUP.

## S3-0 Fondasi yang dibawa (mengikat)

- 23+7 irisan EDA-06 (delta_normal per irisan = acuan biaya).
- 5 kandidat Tokyo = efek INVERS (C3/A-2 putusan-i2): dekat level
  bulat -> besaran LEBIH KECIL. DILARANG dipakai sebagai sinyal
  long/label arah positif dalam bentuk apa pun.
- 2 kandidat London GUGUR = tetap gugur, bukan cadangan.
- 98 LOLOS native = deskriptif, BELUM dibaca arahnya (W-3b).
- pdhl_d = ARTEFAK struktural, DILARANG masuk sebagai fitur/label.
- Holdout 2026 TERKUNCI. Strata A 2023H2-2025H2 = satu-satunya
  wilayah latih-uji. B = 185.248 baris tidak berubah.
- Ambang G1/G2-revisi/G3/G4 + A-7 + V-2/V-6 = warisan beku,
  DILARANG direvisi di Lapisan 3.

## S3-1 Scope bertahap (dua fase, fase-1 dulu)

- Fase L3-0 (wajib, tanpa model): baca arah 153 baris G3-pass
  (120 positif, 33 negatif) + peta 98 LOLOS ke arah + irisan.
  Output = 1 CSV arah + 1 FIG peta. Tanpa ini, fase model DILARANG.
- Fase L3-1 (baseline saja): model pembanding paling sederhana
  (mayoritas-kelas / laju-marginal per target-iris) di atas
  pasangan yang LOLOS gerbang masuk S3-2. ANN/bespoke = di luar
  spec ini, butuh spec tambahan.
- Maksimal pasangan fase L3-1 = 5 Tokyo + subset 98 yang lolos
  S3-2; pendaftarannya di brief coder, bukan di spec ini.

## S3-2 Gerbang masuk model (null-model, pra-registrasi)

Setiap pasangan calon WAJIB lolos ketiganya SEBELUM dilatih:

- M1 (arah diketahui): lift G3 + tandanya tercatat di CSV L3-0.
- M2 (aturan main terdaftar): metrik (akurasi/Brier, pilih SATU
  per target-kind), grid hiperparameter TERTUTUP, seed terkunci,
  dan ambang "kalah-null = STOP pasangan" ditulis SEBELUM run.
- M3 (kalahkan null): skor baseline vs prediktor null
  (mayoritas-kelas train) pada split pra-registrasi; hanya selisih
  di atas ambang M2 + stabil lintas semester (aturan >=4/5
  analog G2b) yang boleh lanjut. Gagal = GUGUR permanen ronde ini.
- DILARANG memindai ambang/bin/window/grid di luar yang
  didaftarkan. DILARANG generalisasi sesi di luar yang diuji.

## S3-3 Larangan (warisan + baru)

- Warisan EDA-07: tanpa model/backtest/P&L/edge di dokumen
  deskriptif; tanpa fitur/label/irisan baru; tanpa revisi ambang;
  tanpa sentuh file beku, configs/src/data; tanpa commit/push.
- Baru: tanpa klaim "layak-trade" dari skor baseline; tanpa
  memakai lift magnitudo-volatilitas (mis. true-top T-4) sebagai
  bukti prediktabilitas arah; tanpa 2026; tanpa threshold-scan.

## S3-4 Prosedur (pelajaran T-1/T-2/T-6 dikunci)

- Reuse-first pola _build_eda07*.py + _eda_common.py; hanya
  pandas/numpy/scipy/matplotlib; builder ASCII/LF/tail-LF.
- Run panjang = detached Task Scheduler rantai-tunggal + progres
  fraksi + checkpoint per unit + log-then-assert.
- Runner-log (stdout/stderr + exit code) WAJIB disimpan sebagai
  artefak di folder tanggal run (tutup T-2).
- CSV verdict terpisah WAJIB (tutup T-6): 1 baris per pasangan
  (M1/M2/M3, skor vs null, vonis).
- Nama kolom tunggal-makna (tutup T-3); label "TOP" hanya untuk
  hasil urutan benar (tutup T-4); hash 12+ karakter per file.
- Notebook tereksekusi 0 error, determinisme rerun bit-identik,
  seed per stream, sel kesimpulan terisi, FIG/CSV teregistrasi.
- HEAD tak bergerak, staged nol; repo beku selain deliverable.

## S3-5 Deliverable + audit L3

- T-L3-0 arah (153 baris + peta 98), T-L3-1 baseline vs null,
  FIG, notebook, laporan coder format Klaim & Bukti.
- Reaudit L3 independen (brief terpisah): M1/M2/M3 verbatim,
  hitung-ulang skor vs null dari CSV, nol drift, scope.
- Tanpa LOLOS audit L3, tidak ada fase model lanjutan.

Disetujui user -> brief coder L3-0 (fase deskriptif saja) terbit.
