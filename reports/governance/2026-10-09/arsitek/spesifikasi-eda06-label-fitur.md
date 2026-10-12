# Spesifikasi EDA-06 LPFS-v1 (Label and Prediction Feasibility Study v1)

Peran: Arsitek (merancang + mengunci scope; DILARANG tulis kode produksi,
DILARANG ubah data/config/src, DILARANG commit/push).
Tanggal: 2026-10-09. Workdir: D:\ANN.
Status: SPEC BEKU untuk ronde discovery satu notebook.
Lingkup TERTUTUP: S1-S8 + larangan + gerbang. BUKAN H6, BUKAN vonis ulang
H1-H5/H4b/R-2, BUKAN pemilihan metode, BUKAN backtest P&L.

## S0. Sumber yang dikunci (dibaca sebelum tulis)

- reports/eda/2026-10-06/report.md (Q1-Q7 + sintesis H1-H5)
- reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md (redaksi H1-H5 beku)
- reports/governance/2026-10-07/arsitek/putusan-lapisan3-H1H2.md (H1/H2 GUGUR FINAL)
- reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md (H3 GUGUR, filter dilarang)
- reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md (H4 TAHAN tipis + H5 GUGUR telak)
- reports/governance/2026-10-07/arsitek/putusan-H4b-stabilitas.md (H4b GUGUR)
- reports/governance/2026-10-07/arsitek/putusan-R2-stratifikasi.md (R-2 GUGUR)
- reports/governance/2026-10-07/arsitek/disposisi-fondasi-B.md (D-1 s/d D-4)
- notebooks/scalping/_eda_common.py (fingerprint sesi, satu-satunya definisi sesi)
- configs/data.yaml (cost_basis + stress_bands + anomaly_windows + DST schedule)
- thoughts/shared/designs/2026-10-09-eda06-label-fitur-design.md (ide awal yang dibekukan user)

## S1. Tahap + tujuan (dikunci)

Nama tahap ronde ini: Label and Prediction Feasibility Study v1
(disingkat LPFS-v1; discovery, BUKAN konfirmasi, BUKAN vonis,
BUKAN kelanjutan EDA deskriptif v3.1).

Tujuan satu kalimat: menguji apakah 1 kombinasi utama
(L2 x N=15, ditetapkan pra-run) layak diprediksi pada data,
fitur, split, dan biaya yang sama, dengan 8 kombinasi sekunder
(L1/L2/L3 x N=5/15/30 minus utama) hanya sebagai pembanding
deskriptif.

Timeframe keputusan: M1 saja. N dihitung dalam BAR M1 yang sama
dengan menit pada bar tanpa gap (N = 5, 15, 30 bar = 5, 15,
30 menit ke depan dari close entry). DILARANG memakai N bar TF
lain atau menafsir N sebagai bar M5/M15/H1.

Kombinasi utama pra-run: L2 x N=15. Alasan pencatatan (bukan
hasil uji): titik tengah horizon; L2 satu-satunya label yang
memuat biaya di definisinya. Semua klaim layak/tidak-layak
ronde ini dinilai pada kombinasi utama; 8 sekunder DILARANG
dipromosikan menjadi klaim utama pasca-hoc.

## S2. Otoritas biaya 3-lapis + rumus P&L (diputus, mengikat ronde ini)

Satuan: pip. USDJPY pip_size = 0.01 (configs/data.yaml).
OHLC M1 = Bid. Kunci tahun STRING, akses str(year).

- Lapis-1 biaya primer (ambang utama): cost_basis MEAN strata A
  by_session (London 0.61 / NewYork 0.69 / Tokyo 0.62 /
  Sydney 0.80; default 0.65 hanya fallback bila sesi tak
  terpetakan). by_year cost_basis hanya info, BUKAN otoritas sesi.
- Lapis-2 biaya tambahan pra-registrasi: margin 0.20 pip di atas
  lapis-1 (buffer komisi+slippage deskriptif, tidak dioptimasi
  ronde ini). Total ambang tahap (a) = lapis-1 sesi + 0.20.
- Lapis-3 stress (sensitivitas saja): stress_bands p95 by_session
  (London 0.80 / NewYork 1.20 / Tokyo 0.90 / Sydney 1.50).
  DILARANG memakai lapis-3 sebagai ambang utama.
- spread.default = 1.5 dan spread.by_year BUKAN otoritas ronde
  ini. Setiap angka biaya di notebook wajib menyebut lapis dan
  sumbernya (lapis-1 cost_basis vs lapis-3 p95). Mencampur
  otoritas tanpa label = temuan.

Rumus P&L per trade dalam pip (spread_pips dalam pip):

- Long: entry Ask = bid[t] + spread_pips[t]; exit Bid =
  bid[t+N]. PnL_long = (bid[t+N] - bid[t]) / pip_size
  - spread_pips[t].
- Short: entry Bid = bid[t]; exit Ask = bid[t+N] +
  spread_pips[t+N]. PnL_short = (bid[t] - bid[t+N]) / pip_size
  - spread_pips[t+N].
- EV-after-cost dilaporkan dua versi: (a) ambang primer
  (lapis-1 sesi + 0.20) dan (b) spread aktual per trade
  (rumus di atas); (c) lapis-3 p95 hanya kolom sensitivitas.

## S3. Tiga definisi label operasional (dikunci, DILARANG definisi ke-4)

Harga = close bid M1. pip_size = 0.01. Semua input threshold
dari info t <= entry saja (atr dan biaya sesi pre-registrasi).

- ret_pip[t,N] = (close[t+N] - close[t]) / pip_size.
- atr_pip[t] = ATR_M1_14[t] / pip_size. ATR_M1_14 = rolling 14
  bar close-to-close, shift(1) (tanpa look-ahead).
- L1 return-N (arah mentah): naik jika ret_pip > 0, turun jika
  ret_pip < 0, netral jika ret_pip == 0 persis (kelas nol
  deskriptif; preseden massa-nol T-01).
- L2 tiga-kelas threshold (kombinasi utama pada N=15):
  ambang_pip[t] = max(lapis-1 sesi + 0.20, 0.5 * atr_pip[t]);
  naik jika ret_pip > ambang_pip, turun jika
  ret_pip < -ambang_pip, netral selainnya (termasuk tepat
  sama dengan ambang = netral).
- L3 triple-barrier close-only (gaya Lopez de Prado, terkunci):
  upper_pip[t] = +max(1.0 * atr_pip[t], lapis-1 sesi + 0.20),
  lower_pip[t] = -max(1.0 * atr_pip[t], lapis-1 sesi + 0.20),
  timeout = N bar. Untuk k = 1..N hitung
  dev_pip[k] = (close[t+k] - close[t]) / pip_size; label =
  barrier pertama tersentuh (dev >= upper -> upper;
  dev <= lower -> lower). Aturan ambigu: close tunggal per bar
  sehingga maksimal satu barrier per k; sentuhan tepat sama
  dengan barrier dihitung tersentuh; bila tak tersentuh sampai
  k=N maka label = timeout. DILARANG sentuh high/low intra-bar
  selain close M1 ronde ini (dibuka di konfirmasi bila L3 lolos).

Ukur per label x N (9 kombinasi): class balance (share tiap
kelas, sum to 1), median |ret_pip| vs ambang primer + margin,
share |ret_pip| > ambang. Tanpa klaim tradability.

## S4. Rangkaian dua-tahap dengan prediksi-A di test (mengikat)

- Tahap (a) gerak (target biner): y_a = 1 jika
  |ret_pip| > lapis-1 sesi + 0.20, else 0. Laporkan hit-rate
  gerak + CI95 Wilson per kombinasi (9 sel).
- Tahap (b) arah kondisional: model arah dilatih HANYA pada
  subset train dengan y_a = 1; target y_b = sign(ret_pip)
  di antara movers (L1-sign atau sisi L2/L3, dicatat per label).
- Aturan test yang mengikat: tahap (b) di TEST dievaluasi HANYA
  pada subset PREDIKSI-A = 1 (keluaran model A di test), BUKAN
  pada oracle y_a = 1. Evaluasi (b) pada oracle di test
  DILARANG sebagai metrik utama (boleh sebagai diagnostik
  sekunder berlabel ORACLE-ONLY, tidak menentukan gerbang).
- Kesimpulan yang DILARANG: akurasi arah global 50%+ sebagai
  edge; akurasi (b)-pada-oracle sebagai bukti tradability.
  Kesimpulan yang WAJIB bila terjadi: gerak tidak melewati
  biaya pada kombinasi utama = label tidak layak, STOP.

## S5. Fitur kandidat (real-time only, DILARANG tambah di luar daftar)

Hanya dari t <= entry (candle closed saja). Multi-timeframe M5/M15/H1
hanya bucket yang close_time <= t entry.

- realized-vol rolling M1: sum r^2 window 20 dan 60 bar, shift(1).
- jam sesi: hour_utc + session_label primer DST-aware
  (fingerprint di-assert; cross-tab hanya sebagai kolom pembanding,
  bukan fitur ganda).
- jarak ke MA dalam ATR: (close - SMA20_M1)/ATR_M1_14, shift(1).
- momentum closed-only: return 5/15/60 bar M1 + return 1 bar M5/M15/H1
  terakhir yang sudah closed, shift(1).
- spread saat entry: spread_pips[t] + percentile vs median sesi
  TRAIN lipatan aktif (median di-fit pada train saja per S7,
  diterapkan ke test; median full-sample lintas tahun DILARANG
  sebagai input model dan hanya boleh tampil sebagai angka
  deskriptif berlabel FULL-SAMPLE-DESCRIPTIVE).

DILARANG sebagai fitur:

1. Tipologi trending/normal/range nb05 (median full-sample ex-post).
2. Label strata A/B/C sebagai fitur (hanya untuk split stabilitas).
3. Kolom time hasil konversi sendiri sebagai pengganti broker_time_raw
   untuk definisi hari (hari = tanggal-broker via wall_clock).
4. High/low masa depan, return N ke depan, ATR yang mencakup t+1.

## S6. MI / korelasi + pangkas redundansi

- Per label x N: mutual_info (diskrit 3 kelas) atau Spearman rank
  untuk fitur kontinu vs |return-N| dan vs kelas.
  Pearson saja DILARANG sebagai satu-satunya ukuran.
- Multikolinearitas: matriks Spearman antarfitur. Pasangan |rho|>0.85
  wajib dilaporkan sebagai redundan; pangkas satu (catat yang dibuang,
  tanpa optimasi akurasi).
- Fundamental (NFP/BoJ/CPI, selisih yield US10Y-JGB): hanya penanda
  event/regime deskriptif bila data tersedia. Tidak ada klaim kausal.

## S7. Split expanding + purge/gap + threshold train-only + stabilitas

- Skema lipatan (walk-forward expanding tahunan, kanonis):
  lipatan-1 train 2023 -> test 2024; lipatan-2 train 2023-2024
  -> test 2025. Strata A/B/C hanya untuk split stabilitas
  deskriptif, BUKAN untuk fitting.
- Purge/gap wajib pada tiap batas lipatan: jeda 30 bar M1
  (= horizon terpanjang) tanpa sampel pada batas train/test;
  setiap sampel yang jendela forward-N-nya melewati batas
  (entry + N melewati batas) DIBUANG dari kedua sisi. Jumlah
  sampel terbuang dilaporkan per lipatan (assert).
- Threshold/konstanta dari train saja: median sesi untuk
  percentile spread, parameter scaler, dan tiap cut yang
  diestimasi dari data WAJIB di-fit pada train lipatan aktif
  saja lalu diterapkan ke test lipatan itu. Konstanta
  pre-registrasi (lapis-1/lapis-2/lapis-3, faktor 0.5/1.0 ATR)
  bukan hasil fit sehingga tidak berubah per lipatan.
  Median full-sample lintas tahun DILARANG sebagai input
  fitur prediktif (boleh hanya sebagai angka deskriptif biaya
  berlabel FULL-SAMPLE-DESCRIPTIVE, tidak masuk model).
- 2026 hanya periode terlihat deskriptif (dihitung dan
  ditampilkan, dikecualikan penuh sebagai penentu, preseden
  R-2/T-3). DILARANG memakai 2026 untuk memilih kombinasi,
  ambang, atau klaim lolos/gagal.
- Setiap temuan MI/balance/gerak dilaporkan per slice
  (lipatan x tahun x strata x sesi). Pola yang hanya bagus di
  satu slice = dilaporkan tidak umum, DILARANG disebut edge umum.
- Failure analysis wajib per kombinasi: kapan tahap (a) gagal
  (volatilitas rendah/tinggi, spread tinggi, setelah expansion
  candle, jam Off). Tujuannya menemukan kapan TIDAK masuk.

## S8. Mekanika notebook (pola rantai EDA, Reuse-First)

- Builder: scripts/_build_eda06.py (generator + executor nbconvert,
  pola _build_eda05.py). Notebook: notebooks/scalping/eda_06_label_fitur.ipynb.
- Setup sel: python venv kanonik (pandas 2.x, tolak pandas 3.x),
  tzdata 2026.5, PROJECT_ROOT via pyproject.toml + src/,
  session_fingerprint() == EXPECTED_FINGERPRINT (assert keras),
  load_config("data"), wall_clock_series untuk hari-broker.
- Parquet: data/processed/M1 2023-2026 (1.347.847 bar), M5/M15/H1
  closed-only untuk fitur momentum. D1 974 bucket hanya untuk
  kalender hari-broker (paritas m1_bars), bukan untuk fitur.
- Strata hari: A 825 / B 130 / C 19 hari-broker (pola nb03/nb05).
  Anomaly windows dari config (C deskriptif saja).
- Figures: FIG-08.. dst sekuensial (DILARANG pakai ulang FIG-01..07).
  Registry figures diverifikasi (tepat FIG-01.. akhir).
- Assertion mesin: tiap klaim angka dikunci assert (balance sum to 1,
  gerak vs biaya terhitung dari kolom yang sama, MI non-negatif,
  fingerprint cocok, paritas hari-broker). Target minimal 20 assertion.
- Gerbang baseline pra-registrasi (di dalam notebook,
  discovery-grade, hanya kombinasi utama L2 x N=15 yang
  menentukan; 8 sekunder tidak dapat mengubah hasil gerbang):
  SATU model dipilih sebelum run (logistic regression ATAU
  gradient boosting, dicatat; DILARANG coba keduanya lalu pilih
  yang bagus), fitur S5 saja, scaler + tiap konstanta fit
  hanya di train per S7, skema lipatan + purge/gap per S7.
  Metrik: EV-after-cost lapis-1+margin per trade (rumus S2)
  + hit-rate gerak + akurasi arah kondisional pada
  PREDIKSI-A=1. CI95 via day-cluster bootstrap (resample
  hari-broker dengan penggantian, 10000 ulangan, seed 20261009);
  weekly-block (blok 7-hari) sebagai sensitivitas berdampingan.
  Kriteria GO (ketiganya wajib, dinilai pada utama): (G1)
  EV lapis-1+margin pada trade prediksi-A=1 > 0 pada KEDUA
  lipatan; (G2) batas bawah CI95 day-cluster akurasi arah
  kondisional pada prediksi-A=1 > 0.50 pooled; (G3) hit-rate
  gerak (a) > base-rate naive (share y_a=1 di train lipatan
  yang sama) pada KEDUA lipatan. Selain itu = NO-GO/STOP.
  Keluaran berupa temuan (GO/NO-GO), BUKAN vonis strategi.
- Nol tulis: DILARANG tulis configs/src/data, DILARANG commit/push,
  DILARANG P&L/equity sebagai klaim.

## Larangan bentuk-spesifik ronde ini

1. DILARANG mengubah/menafsir-ulang vonis H1-H5/H4b/R-2 dalam bentuk apa pun.
2. DILARANG menambah label ke-4, fitur di luar S5, atau horizon selain 5/15/30.
3. DILARANG optimasi threshold/barrier/window dengan memindai profit.
4. DILARANG memakai tipologi full-sample, label strata, atau masa depan sebagai fitur.
5. DILARANG memakai 2026 sebagai penentu atau mengubah definisi sesi/Off.
6. DILARANG klaim edge tradable. Satu-satunya klaim yang boleh:
   kombinasi utama L2 x N=15 layak/tidak-layak dibawa ke ronde
   konfirmasi (8 sekunder hanya deskriptif, tidak menentukan).
7. DILARANG pointer ke file internal asisten. Spec ini mandiri.

## Perintah mentah wajib (tiap syarat berpasangan output ditempel di laporan)

- Klaim file ada + ukuran: tempel output git hash-object <path-builder> +
  <path-notebook> SESUDAH tulis terakhir + baris/byte.
- Klaim tanpa commit/stage oleh ronde ini: tempel output
  git status --porcelain=v1 + git rev-parse HEAD.
- Klaim ASCII/LF-only/tail-LF: tempel output cek non-ASCII + CRLF +
  byte terakhir (perintah + output, bukan ringkasan).
- Klaim angka: tiap angka penentu menyebut sel notebook + artefak
  (parquet/JSON) + sha bila ada.
- DILARANG imbauan umum ("pastikan hash benar"). Klaim tanpa output
  mentah = GAGAL (tulis eksplisit).

## SELF-AUDIT 3x ADVERSARIAL (wajib di laporan coder)

Putaran 1 Correctness: tiap label x N terhitung dari t<=entry saja?
tiap ambang pre-registrasi tanpa scan? fingerprint cocok? paritas
hari-broker 974? assertion >=20 lolos?
Putaran 2 Bias: ada kalimat yang menyelamatkan H-gugur? ada threshold
yang diam-diam dioptimasi? ada slice tunggal yang digeneralisasi?
ada akurasi arah global yang diklaim sebagai edge?
Putaran 3 Meta-check: file hanya builder+notebook di lokasi kanonis?
format ASCII/LF tanpa self-hash? nol commit/push? nol vonis baru?
nol tulis governance selain laporan tugas?

## Output yang dikembalikan coder

- scripts/_build_eda06.py + notebooks/scalping/eda_06_label_fitur.ipynb
  tereksekusi (urutan terbukti, tanpa error), figures FIG-08+ di
  reports/eda/2026-10-06/figures/ atau reports/eda/2026-10-09/figures/
  (satu lokasi, dicatat).
- Laporan tugas pola AGENTS.md S5: file dibuat/diubah + apa dilakukan +
  tabel Klaim & Bukti (TERVERIFIKASI/BELUM DIVERIFIKASI/ASUMSI) +
  yang belum diverifikasi + potensi masalah + rekomendasi label mana
  yang layak ke konfirmasi (tanpa vonis).
- Bahasa Indonesia. STOP setelah serah-terima; ronde konfirmasi butuh
  spec baru.

## Pengikatan eksternal (pengganti C8, mengikat)

Dokumen spec ini TIDAK memuat self-hash. Hash (git-blob + sha256)
dihitung SETELAH tulis final dan dilaporkan di kanal luar dokumen.
Pola assert-konstanta-vs-literal sebagai satu-satunya gate DILARANG
(preseden V-2 R-2). Gate wajib: assert pasca-loop atas himpunan aktual
(mis himpunan N/label yang benar teruji) + sabotase wajib rc non-0
bila spec menuntutnya di ronde konfirmasi.
