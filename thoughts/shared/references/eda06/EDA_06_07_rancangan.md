# Rancangan EDA-06 dan EDA-07 (USDJPY scalping, bot ANN)

Dokumen untuk implementasi. EDA-06 sudah ditulis sebagai notebook (`eda_06_biaya_breakeven.ipynb`).
EDA-07 masih berupa rancangan di bagian 3.

Urutan kerja: **EDA-06 (gerbang biaya) → EDA-07 (label dan fitur, hanya bila gerbang lolos) → Lapisan 3 (baseline walk-forward) → ANN**.

---

## 0. Aturan bersama (berlaku untuk keduanya)

1. **Holdout 2026 dikunci.** Data dengan hari broker >= 2026-01-01 tidak dimuat. Asersi: `max(utc) < 2026-01-01`. Bar tepi (UTC 31 Des malam = hari broker 1 Jan 2026) ikut dikeluarkan dan jumlahnya dicetak.
2. **Universe**: strata A + B tahun 2023-2025, dikurangi strata C (jendela anomali). B (H1-2023, regime vol tinggi) dilaporkan terpisah dan tidak dihitung pada kriteria stabilitas.
3. **Semester** ditentukan dari hari broker: 2023H2, 2024H1, 2024H2, 2025H1, 2025H2 (lima semester strata A). 2023H1 = strata B.
4. **Kausal**: keputusan di akhir bar M1. Bar M5/M15/H1 hanya dipakai bila sudah selesai (merge backward pada `utc + 1 menit` terhadap waktu selesai bar).
5. **Nol imputasi**; entri/label yang dibuang dihitung dan dilaporkan per alasan.
6. **Tanpa dependensi baru** (tidak ada sklearn/numba). Pakai pandas, numpy, scipy, matplotlib yang sudah ada.
7. **Otoritas biaya**: `config["spread"]["cost_basis"]["by_session"]` (normal) dan `config["spread"]["stress_bands"]["p95"]["by_session"]` (stres). Bukan `spread.default` (1,5 pip, blok lama; masih terbuka di CHANGELOG, jadi backtest wajib menyebut kode mana yang jadi otoritas).
8. **Satuan**: 1 pip = 10 point (broker 3 digit). Lot 0,01: 1 point ~ ¥1 ~ $0,0064 (patokan: 251 point = $1,6), jadi SL 50 point ~ $0,32 dan TP 70 point ~ $0,45. Nilai per point ikut kurs USDJPY.
9. Notebook berjalan sekali dari atas ke bawah, tanpa gerbang review per sel. Gerbang keputusan ada di bagian akhir.
10. Tidak ada tulis ke `configs/`. Output ke `reports/eda/<tanggal>/`.

Koreksi terhadap diskusi sebelumnya: di chat saya sempat menulis stres = 1,5 kali. Repo memakai `stress_multiplier: 2.0` dan `stress_bands.p95`. Notebook memakai `stress_bands.p95.by_session` untuk skenario stres, dan hanya mencatat `stress_multiplier`.

---

## 1. EDA-06 `eda_06_biaya_breakeven` (SUDAH DITULIS)

**Tujuan**: apakah ada kombinasi sesi x horizon/barrier di mana ruang gerak cukup besar dibanding biaya.

| Bagian | Isi | Output |
|---|---|---|
| 1 (C1) | Sebaran spread: mean, p50, p90, p95, p99, p99,9, maks, pangsa > k x `cost_basis.default`; per sesi, jam UTC, semester | T-06-1a..1d |
| 2 (C2) | Spread vs desil realized-vol 15 menit (Spearman), dan di sekitar jam tetap (rollover broker, open Sydney/London/NY, fix Tokyo) | T-06-2a, 2b |
| 3 (C3) | Biaya per sesi x skenario (normal, stres) x slippage (+0/+0,1/+0,3 pip), dalam pip, point, dolar | T-06-3 |
| 4 (C4a) | Grid taruhan arah N-menit (N = 5/15/30/60): p* = 0,5 + c/(2m), sampel tanpa tumpang tindih, CI bootstrap per hari | T-06-4, FIG-10 |
| 5 (C4b) | Laju dasar barrier tanpa sinyal (kedua sisi): tetap 50/70, 30/45, 100/140 point; ATR M5(14) dengan k = 0,75/1,0/1,5 dan RR = 1,0/1,4/2,0 | T-06-5a..5f, FIG-12 |
| 6 | Stabilitas per semester | T-06-6, FIG-11 |
| 7 | Gerbang K1-K4 | T-06-7 |
| 8 | Gambar dan simpan CSV | FIG-08..12 |

**Metode barrier (ringkas)**
- Entri tanpa sinyal setiap 5 bar M1, buy dan sell digabung (arah acak). Ini laju dasar, **bukan strategi**.
- Harga close/high/low = BID. Buy masuk di ask (= bid + spread); sell masuk di bid dan keluar di ask. Spread konstan per sesi bar entri.
- First-passage pada high/low M1 bar **sesudah** entri. TP dan SL tersentuh di bar yang sama dihitung SL (pesimis), pangsanya dilaporkan. Timeout 120 menit keluar di close.
- ATR M5(14) dari bar M5 yang sudah selesai, dibekukan saat entri. SL = k x ATR (min 0,5 pip), TP = SL x RR.
- E = ekspektasi dasar per entri (pip), sudah memuat spread dan hasil timeout.
- **delta = -E / (TP + SL)** = berapa poin persentase peluang TP-duluan harus naik di atas laju dasar agar impas. Untuk 50/70 point dengan spread 6,5 point, perkiraan kasar delta ~ 5,4 pp. Slippage menambah delta.

**Gerbang (dikunci sebelum menjalankan)**

| Kode | Syarat |
|---|---|
| K1 | delta_normal <= 3,0 pp **dan** delta_stres <= 5,0 pp |
| K2 | delta_normal <= 3,0 pp pada >= 4 dari 5 semester A |
| K3 | n >= 1000 entri-sisi dan >= 100 hari |
| K4 | p_none <= 50% (barrier benar-benar tercapai dalam horizon; mencegah barrier raksasa yang hampir selalu timeout lolos secara semu) |

Ambang 3 pp dan 5 pp setara dengan p* 0,53 dan 0,55 pada taruhan simetris. Itu tebakan terdidik, bukan hasil hitung dari data; ubah **sebelum** menjalankan bila perlu.

**Keputusan**
- Tidak ada irisan lolos: jangan jalankan EDA-07 dengan rumusan ini. Opsi: horizon lebih panjang (M15/H1), hanya sesi atau kondisi tertentu, atau tinjau ulang kelayakan scalping pada biaya ini.
- Ada irisan lolos: EDA-07 hanya berfokus pada irisan itu (combo, sesi, tercile ATR dalam sesi). Lolos bukan bukti edge, hanya izin lanjut.
- Irisan yang diuji: 144 (combo x sesi x tercile) + 48 (combo x sesi); jumlahnya dicetak.

**Uji bawaan notebook**
- ATR di 12 timestamp acak dihitung ulang hanya dari data s.d. T dan harus identik (anti look-ahead).
- Simulator barrier vektorisasi dicocokkan dengan implementasi naif per bar (400 entri x 2 sisi).
- Asersi strata: B = 185.248 bar, A+B+C = total, tanpa bar `Off` di A, tanpa data 2026, sidik jari definisi sesi = Notebook 00.

**Status uji**: notebook sudah dijalankan ujung ke ujung (sekitar 40 detik) pada **data sintetis** yang meniru skema parquet M1; semua uji bawaan lolos. Angka dari data sintetis **bukan temuan**. Belum dijalankan pada data asli.

---

## 2. Yang perlu dicek saat implementasi EDA-06 pada data asli

1. Asersi `assert abs(measured - COST_NORMAL[label]) < 0.15` (kecocokan `cost_basis` config dengan mean 2023-2025 strata A). Bila gagal, itu informasi, bukan bug; investigasi sebelum melonggarkan.
2. Notebook memakai `add_labels` dari `_eda_common` dan mengandalkan kolom `session_label` (sama seperti notebook 02-05), serta kolom M1: `time, broker_time_raw, high, low, close, spread_pips`.
3. Venv kanonik: pandas 2.x, `tzdata==2026.5` (asersi bawaan).
4. Waktu lari yang diharapkan: puluhan detik sampai beberapa menit. Parameter yang bisa diubah di sel parameter: `STRIDE`, `HORIZON`, `N_BOOT`.
5. Pekerjaan terpisah yang masih menggantung: perpanjang jadwal DST di `broker_time.py` sebelum 1 November 2026 (fetch data setelah tanggal itu melempar `ValueError`). EDA-06 sendiri tidak memanggil `utc_series`, jadi tidak terpengaruh.
6. Setelah dijalankan: isi bagian "Kesimpulan" di akhir notebook secara manual (lima pertanyaan sudah disiapkan).

---

## 3. EDA-07 `eda_07_label_fitur` (RANCANGAN, belum ditulis)

**Syarat jalan**: verdict EDA-06 = LOLOS. Fokus pada irisan lolos (combo barrier, sesi, tercile ATR). Notebook ini tetap deskriptif: tanpa P&L, backtest, atau pelatihan model.

**Pertanyaan**
- L1: label mana yang layak diprediksi?
- L2: fitur mana yang punya informasi terhadap label?
- L3: apakah informasi itu stabil?
- L4: apakah efek yang terukur melampaui edge minimum (delta) dari EDA-06?

### 3.1 Label (L1)
Horizon N = 5/15/30/60 menit untuk label berbasis waktu; barrier untuk label berbasis hit.
- **LA (barrier-hit)**: TP-duluan per sisi (buy dan sell terpisah) memakai combo yang lolos di EDA-06. Timeout dan ambigu ditandai.
- **LB (besaran)**: 1 bila |gerak N menit| > biaya stres + margin, plus versi kontinu (range N menit ke depan dalam pip). Target ini sesuai temuan EDA bahwa besaran gerak lebih terprediksi daripada arah.
- **LC (tiga kelas)**: naik/netral/turun dengan ambang theta = 1x atau 2x biaya stres.
- **LD (tanda return)**: hanya pembanding.
- Label yang jendelanya menyeberangi gap atau jendela anomali dibuang dan dilaporkan.
- Output: class balance, median |gerak| dibanding biaya, ukuran sampel efektif. Inferensi memakai sampel tanpa tumpang tindih (setiap N bar) dan bootstrap klaster-hari.

### 3.2 Fitur (L2), semua kausal
- **Volatilitas**: realized vol 15 dan 60 menit, ATR M5 dan M15, rasio vol pendek terhadap vol panjang. Regime hanya memakai ukuran **real-time** (rolling), bukan median full-sample seperti tipologi di Notebook 05.
- **Waktu**: sesi (DST-aware, label primer), menit sejak open London/NY, jam (sin/cos), hari dalam minggu, penanda fix Tokyo.
- **Momentum/mean-reversion**: return 1/5/15/60 menit, jarak ke EMA dalam satuan ATR, z-score harga.
- **Multi-timeframe**: return bar M5/M15/H1 terakhir yang selesai, posisi close dalam range bar, slope EMA H1 dalam satuan ATR.
- **Biaya**: spread bar saat itu (`spread_pips`).
- **Kontrol (diharapkan tidak informatif)**: satu fitur derau acak, jarak ke level bulat, jarak ke prior-day H/L (H5 gugur di EDA-04).

### 3.3 Metode
- MI terbin (20 kuantil) dengan numpy/pandas, dengan **lantai derau**: permutasi blok-hari 100 kali, ambil persentil 95. Fitur dianggap informatif hanya bila di atas lantai.
- **Lift per desil**: peluang label per desil fitur, dengan CI bootstrap klaster-hari.
- Spearman untuk target kontinu. Redundansi: pasangan |rho| > 0,8 diringkas ke satu wakil.

### 3.4 Stabilitas (L3)
MI dan arah lift per semester (lima), per sesi, per strata A/B/C. H1-2023 dilaporkan terpisah.

### 3.5 Uji anti-leakage
Pada 200 timestamp acak, hitung ulang fitur hanya dari data s.d. T dan asersikan sama dengan proses penuh.

### 3.6 Gerbang (usulan; kunci sebelum menjalankan)
- G1: tidak ada kelas minoritas < 10% (label tiga kelas); label biner antara 10% dan 90%.
- G2: minimal satu fitur non-kontrol di atas lantai derau pada >= 4 dari 5 semester dengan arah sama.
- G3: lift desil teratas vs terbawah punya CI yang tidak memuat 0.
- **G4 (tautan ke EDA-06)**: efek terukur (kenaikan peluang TP-duluan di desil teratas dibanding laju dasar) >= delta_normal irisan itu di EDA-06, dan masih memadai pada biaya stres.
- Gagal G2 atau G4: berhenti dan rumuskan ulang target; jangan lanjut ke baseline.

### 3.7 Output
T-07-1..T-07-4 (balance label, MI vs lantai derau, lift per desil, stabilitas semester) dan FIG-13..16. Satu paragraf kesimpulan yang mengunci label, horizon/barrier, dan daftar fitur untuk Lapisan 3.

---

## 4. Setelah EDA-07 (Lapisan 3, ringkas)

1. **Baseline walk-forward** dengan model sederhana (logistic regression atau gradient boosting) pada label dan fitur terkunci. Split per waktu, biaya penuh per sesi, stres, dan slippage. **2026 dibuka satu kali** sebagai holdout akhir.
2. **Pemilihan metode** dengan aturan sama untuk semua kandidat (H1-H5 plus breakout/ekspansi volatilitas, maksimal 5-6 kandidat; jumlah percobaan dicatat). Lolos bila ekspektasi per trade bersih biaya positif dengan CI bootstrap per hari yang tidak memuat 0, positif di >= 3 dari 4 tahun, jumlah trade cukup, dan masih positif di biaya stres. Pilih yang paling sederhana di antara yang lolos.
3. **ANN** hanya bila mengalahkan baseline pada periode uji yang sama. Bila tidak, pakai baseline.
4. **Paper trading** beberapa minggu (slippage, spread nyata, jam berita), lalu **live ukuran kecil** dengan batas kerugian harian.

---

## 5. Keputusan yang perlu dikonfirmasi

1. Ambang gerbang EDA-06 (3 pp / 5 pp / 100 hari / 1000 entri / 50% timeout) dan EDA-07 (bagian 3.6) sudah sesuai, atau ada yang diubah.
2. Horizon timeout 120 menit dan stride 5 menit pada EDA-06 dipertahankan.
3. Slippage tetap menjadi skenario (tidak terukur dari OHLC); nilai nyata diukur saat paper trading.
4. Baseline dan pemilihan metode tetap di Lapisan 3, bukan di EDA.
