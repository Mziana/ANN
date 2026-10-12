# Spesifikasi Arsitek EDA-07 Label-Fitur (deskriptif, BUKAN vonis)

Peran: Arsitek (merancang + mengunci scope; DILARANG tulis kode produksi,
DILARANG ubah data/config/src, DILARANG commit/push).
Tanggal: 2026-10-10. Workdir: D:\ANN.
Status: SPEC BEKU untuk ronde deskriptif satu notebook.
Syarat jalan: EDA-06 TERTUTUP dengan prosedural LOLOS
(putusan-eda06.md P-1). Tanpa itu spec ini MOOT.
Lingkup TERTUTUP: S1-S9 + larangan + gerbang. BUKAN baseline/model,
BUKAN backtest P&L, BUKAN vonis strategi, BUKAN vonis ulang
H1-H5/H4b/R-2.

## S0. Sumber yang dikunci (dibaca sebelum tulis)

- reports/governance/2026-10-10/arsitek/putusan-eda06.md (P-1 s/d P-6)
- reports/governance/2026-10-10/Audit/reaudit-eda06.md (A1-A7 + 3 temuan)
- reports/eda/2026-10-10/T-06-7_gerbang_tercile.csv (23 irisan lolos)
- reports/eda/2026-10-10/T-06-7_gerbang_sesi.csv (7 irisan lolos)
- thoughts/shared/references/eda06/EDA_06_07_rancangan.md (bagian 0-3)
- notebooks/scalping/_eda_common.py (fingerprint sesi, definisi sesi)
- configs/data.yaml (cost_basis + stress_bands + anomaly_windows + DST)
- scripts/_build_eda06.py (pola builder yang dipakai ulang)

## S1. Tujuan (satu kalimat)

Pada 23 irisan tercile + 7 irisan sesi yang lolos EDA-06, tentukan label
mana yang layak diprediksi, fitur kausal mana yang informatif terhadap
label itu, apakah informasi stabil, dan apakah efek terukur melampaui
edge minimum delta irisan tersebut - tanpa model, tanpa P&L, tanpa vonis.

## S2. Scope irisan (dikunci, DILARANG tambah di luar daftar)

- Primer evaluatif: 23 irisan (combo x sesi x tercile ATR dalam sesi)
  + 7 irisan (combo x sesi) dari T-06-7. Daftar dibaca dari CSV, jumlah
  di-assert (23 dan 7); bila CSV berubah, STOP.
- Gerbang G1-G4 dinilai per irisan secara identik (preseden EDA-06:
  semua diuji dengan gate sama = bukan cherry-picking). Maju ke
  Lapisan 3 hanya irisan yang lolos keempatnya.
- 50/70, 30/45, NewYork/Sydney-nonlolos, dan irisan gagal-K1-K4 hanya
  pembanding deskriptif; DILARANG menentukan gerbang atau dipromosikan.
- Peringatan menempel (skeptisisme auditor): 7 sesi lolos terkonsentrasi
  Tokyo/London. DILARANG klaim generalisasi sesi; tiap klaim menyebut
  irisan eksplisit.

## S3. Label L1 (empat definisi, dikunci, DILARANG definisi ke-5)

Horizon waktu N = 5/15/30/60 menit untuk label berbasis waktu; label
barrier memakai combo irisan yang lolos (SL/TP + horizon 120 dari EDA-06).
Sampel inferensi tanpa tumpang tindih (setiap N bar) + bootstrap
klaster-hari. Label yang jendelanya menyeberangi gap/jendela anomali
DIBUANG dan dilaporkan per alasan.

- LA (barrier-hit, per sisi): TP-duluan per sisi (buy dan sell terpisah)
  memakai combo lolos irisan itu. Timeout dan bar-kembar (dihitung SL,
  pesimis, preseden EDA-06) ditandai sebagai kelas sendiri.
- LB (besaran): biner 1 bila |gerak N menit| > biaya stres sesi + margin
  0,20 pip, plus versi kontinu (range N menit ke depan dalam pip).
  Target ini prioritas (besaran lebih terprediksi daripada arah).
- LC (tiga kelas): naik/netral/turun dengan ambang theta = 1x biaya stres
  sesi dan varian 2x (dua varian dicatat terpisah, bukan dipilih pasca-hoc).
- LD (tanda return): hanya pembanding (diharapkan ~50/50, preseden EDA-03).
- Output per label: class balance, median |gerak| vs biaya, ukuran sampel
  efektif. Semua threshold dari info t <= entry atau konstanta
  pre-registrasi; DILARANG threshold di-fit dari masa depan label.

## S4. Fitur L2 (kausal saja, daftar tertutup + kontrol wajib)

Hanya dari t <= entry (candle closed; MTF hanya bar yang sudah selesai,
merge backward utc+1mnt, preseden EDA-06). DILARANG tambah di luar daftar
kecuali kontrol tambahan yang dinyatakan non-informatif a priori.

- Volatilitas: realized-vol 15 dan 60 menit, ATR M5 dan M15 kausal,
  rasio vol-pendek/vol-panjang. Regime HANYA ukuran real-time rolling;
  tipologi median full-sample nb05 DILARANG sebagai fitur.
- Waktu: sesi (label primer DST-aware, fingerprint di-assert), menit sejak
  open London/NY, jam sin/cos, hari-dalam-minggu, penanda fix Tokyo.
- Momentum/mean-reversion: return 1/5/15/60 menit, jarak ke EMA dalam
  satuan ATR, z-score harga.
- Multi-timeframe: return bar M5/M15/H1 terakhir yang selesai, posisi close
  dalam range bar, slope EMA H1 dalam satuan ATR.
- Biaya: spread_pips bar saat itu.
- Kontrol WAJIB (diharapkan tidak informatif; bila informatif = alarm
  kebocoran, STOP dan laporkan): satu fitur derau acak (seed terkunci),
  jarak ke level bulat, jarak ke prior-day H/L (H5 gugur di EDA-04).

## S5. Metode L2 (terkunci, dengan lantai derau)

- MI terbin (20 kuantil, numpy/pandas) + LANTAI DERAU: permutasi blok-hari
  100x, ambang = persentil 95. Fitur informatif HANYA bila di atas lantai.
- Lift per desil: peluang label per desil fitur + CI bootstrap klaster-hari
  (stream RNG terkunci per S8).
- Spearman untuk target kontinu (LB-range). Pearson saja DILARANG sebagai
  satu-satunya ukuran.
- Redundansi: pasangan |rho| > 0,8 diringkas ke satu wakil (catat yang
  dibuang, tanpa optimasi).

## S6. Stabilitas L3 (wajib, bukan opsional)

MI dan arah lift dilaporkan per semester (5 semester A), per sesi, per
strata A/B/C. B (H1-2023) terpisah dan tidak menentukan gerbang.
2026 tetap tidak dimuat. Pola satu-slice = tidak umum, DILARANG disebut
edge umum. NewYork p_none tertinggi dan Sydney n-kecil/spread-mahal
(temuan EDA-06) wajib masuk failure analysis, bukan alasan tambah irisan.

## S7. Uji anti-leakage (wajib)

Pada 200 timestamp acak (seed terkunci), hitung ulang SEMUA fitur hanya
dari data s.d. T dan asersikan sama dengan proses penuh. Satu
ketidakcocokan = temuan HIGH, STOP.

## S8. Gerbang G1-G4 (pra-registrasi, per irisan, ketiganya G1-G3 plus G4)

- G1: tidak ada kelas minoritas < 10% (tiga kelas); label biner 10-90%.
- G2: minimal satu fitur NON-KONTROL di atas lantai derau pada >= 4 dari
  5 semester dengan arah sama.
- G3: lift desil-teratas vs terbawah, CI tidak memuat 0 (pooled irisan itu).
- G4 (tautan EDA-06): kenaikan peluang TP-duluan di desil teratas vs laju
  dasar >= delta_normal irisan itu, dan masih memadai pada biaya stres
  (delta_stres sebagai kolom sensitivitas, bukan penentu tunggal).
- Gagal G2 atau G4 = BERHENTI untuk irisan itu, rumuskan ulang target;
  DILARANG lanjut ke baseline/Lapisan 3 untuk irisan itu.
- Determinisme bootstrap (mengikat, turunan P-5 butir 4): SATU stream RNG
  per analisis (seed berbeda per blok, tercatat), iterasi grup dalam urutan
  terurut, urutan draw didokumentasikan; rerun = bit-identik. CI yang tidak
  stabil antar-rerun = temuan, gerbang untuk irisan itu MOOT sampai stabil.

## S9. Mekanika notebook (pola rantai EDA, Reuse-First)

- Builder: scripts/_build_eda07.py (generator + executor nbconvert, pola
  _build_eda06.py). Notebook: notebooks/scalping/eda_07_label_fitur.ipynb.
- Setup sel: venv kanonik (pandas 2.x, tolak 3.x), tzdata 2026.5,
  PROJECT_ROOT via pyproject.toml + src/, fingerprint sesi assert keras,
  load_config("data"), wall_clock_series hari-broker.
- Parquet M1 2023-2025 (2026 tidak dimuat; bar tepi hari-broker dibuang,
  jumlah dicetak). Strata A/B/C pola EDA-06 (B = 185.248 di-assert).
- Figures FIG-13..16 sekuensial (DILARANG pakai ulang FIG-01..12).
  Registry figures diverifikasi tepat FIG-01..akhir.
- Assertion mesin minimal 20: balance sum to 1, jumlah irisan 23+7 dari CSV,
  MI >= lantai tercatat, kontrol di bawah lantai (atau alarm), 200/200
  anti-leakage, fingerprint, paritas hari-broker, determinisme rerun.
- Tabel: T-07-1 balance label, T-07-2 MI vs lantai, T-07-3 lift per desil,
  T-07-4 stabilitas semester (+ CSV satu lokasi reports/eda/<tanggal>/).
- Output akhir notebook: SATU paragraf kesimpulan yang mengunci label,
  horizon/barrier, dan daftar fitur untuk Lapisan 3 (ditulis manual
  SETELAH membaca tabel, sebelum serah-terima; sel kesimpulan WAJIB terisi
  - pelajaran T-MEDIUM EDA-06).
- Nol tulis: DILARANG tulis configs/src/data, DILARANG commit/push,
  DILARANG P&L/equity/backtest/model sebagai klaim.

## Larangan bentuk-spesifik ronde ini

1. DILARANG menambah irisan, label ke-5, atau fitur non-daftar sebagai
   penentu (kontrol tambahan non-penentu boleh bila dinyatakan a priori).
2. DILARANG melatih model apa pun (baseline/ANN) - itu Lapisan 3.
3. DILARANG memakai 2026, tipologi full-sample, atau masa depan sebagai fitur.
4. DILARANG optimasi theta/bin/window dengan memindai hasil.
5. DILARANG klaim edge tradable. Satu-satunya klaim yang boleh: irisan X
   dengan label Y dan fitur Z layak/tidak-layak dibawa ke Lapisan 3.
6. DILARANG generalisasi sesi (peringatan konsentrasi Tokyo/London menempel).
7. DILARANG klaim efek berita (tanpa kalender historis di repo).
8. DILARANG pointer ke file internal asisten. Spec ini mandiri.

## Perintah mentah wajib (tiap syarat berpasangan output ditempel di laporan)

- Klaim file ada + ukuran: tempel output git hash-object <path-builder> +
  <path-notebook> SESUDAH tulis terakhir + baris/byte.
- Klaim referensi tak berubah: tempel output git hash-object 2 file
  referensi (harus 6a6c6516... dan 6724c37e...) + 2 CSV T-06-7
  (jumlah baris 144/23 dan 48/7).
- Klaim tanpa commit/stage oleh ronde ini: tempel output
  git status --porcelain=v1 + git rev-parse HEAD.
- Klaim ASCII/LF-only/tail-LF builder: tempel output cek non-ASCII + CRLF +
  byte terakhir (perintah + output, bukan ringkasan).
- Klaim notebook tereksekusi + sel kesimpulan terisi: tempel output eksekusi
  (urutan + 0 error) + isi paragraf kesimpulan + daftar FIG/CSV.
- Klaim angka: tiap angka penentu menyebut sel notebook + artefak
  (CSV) + sha bila ada.
- DILARANG imbauan umum ("pastikan hash benar"). Klaim tanpa output
  mentah = GAGAL (tulis eksplisit).

## SELF-AUDIT 3x ADVERSARIAL (wajib di laporan coder)

Putaran 1 Correctness: tiap label/fitur dari t<=entry saja? 200/200
anti-leakage? threshold pre-registrasi tanpa scan? fingerprint cocok?
irisan tepat 23+7 dari CSV? assertion >=20 lolos? sel kesimpulan terisi?
Putaran 2 Bias: ada H-gugur yang diselamatkan? ada theta/bin yang
dioptimasi diam-diam? ada slice tunggal digeneralisasi? ada kontrol yang
informatif tapi diabaikan? ada akurasi/MI yang diklaim sebagai edge?
Putaran 3 Meta-check: file hanya builder+notebook kanonis? format
ASCII/LF tanpa self-hash? nol commit/push? nol model/backtest? nol vonis
baru? nol tulis governance selain laporan tugas?

## Output yang dikembalikan coder

- scripts/_build_eda07.py + notebooks/scalping/eda_07_label_fitur.ipynb
  tereksekusi (urutan terbukti, tanpa error), FIG-13..16 + T-07-1..4 di
  satu lokasi reports/eda/<tanggal>/ (dicatat).
- Laporan tugas pola AGENTS.md S5: file dibuat/diubah + apa dilakukan +
  tabel Klaim & Bukti (TERVERIFIKASI/BELUM DIVERIFIKASI/ASUMSI) +
  yang belum diverifikasi + potensi masalah + rekomendasi irisan x label
  x fitur yang layak ke Lapisan 3 (tanpa vonis).
- Bahasa Indonesia. STOP setelah serah-terima; Lapisan 3 butuh spec baru.

## Pengikatan eksternal (pengganti C8, mengikat)

Dokumen spec ini TIDAK memuat self-hash. Hash (git-blob + sha256)
dihitung SETELAH tulis final dan dilaporkan di kanal luar dokumen.
Pola assert-konstanta-vs-literal sebagai satu-satunya gate DILARANG
(preseden V-2 R-2). Gate wajib: assert pasca-loop atas himpunan aktual
(irisan/label/fitur yang benar teruji) + sabotase wajib rc non-0
bila spec menuntutnya di ronde konfirmasi.
