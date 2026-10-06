# Rancangan EDA v3.1 Final — Dokumen Acuan Kanonik Coder

**Status:** RATIFIKASI PENUH — acuan tunggal implementasi EDA. Coder WAJIB mengikuti dokumen ini.
**Tanggal:** 2026-10-06
**Penulis:** Spark (@ARCHITECT) — atas perintah user.
**Aturan versi (perintah user):** setiap perubahan rancangan WAJIB file baru dengan versi berbeda. DILARANG mengedit file ini in-place. DILARANG berimprovisasi keluar dokumen tanpa persetujuan Architect.

**Riwayat versi:**
- v3.0 (2026-10-06): rancangan full pasca re-audit Klenz (MEDIUM-14–17, LOW-17–21) + errata E1–E3. Disetujui user.
- v3.1 (2026-10-06, file ini): v3.0 + Lampiran A berisi 4 keputusan mengikat yang diratifikasi SETELAH v3.0 — (A1) adjudikasi SA-03, (A2) keputusan SPLIT langkah 4b + 6 patch self-audit, (A3) environment kanonik + pin tzdata, (A4) jejak audit. Isi v3.0 tidak diubah kecuali yang dinyatakan di Lampiran A.

**Notasi provenans** — setiap angka di dokumen ini membawa satu tanda, tanpa pengecualian:
`[S*=sumber]` `[PV=PERLU VERIFIKASI]` `[KD=KEPUTUSAN DESAIN + syarat robustness]` `[PS=PRAKTIK STANDAR]`

**Daftar sumber**: S1=BabyPips market-hours (Sydney 21–06, Tokyo 00–09, London 7–16, NY 13–22 UTC — tabel campuran musim, diakui terbuka); S2=AvaTrade (Tokyo 12AM–9AM, London 8AM–5PM, NY 1PM–10PM GMT); S3=FOREX.com SG (jam lokal: Sydney 08–16, Tokyo 09–18, London 08–16, NY 08–17 + peringatan eksplisit jam bergeser DST Mar/Apr/Okt/Nov); S4=Myfxbook (open lokal: Tokyo 09:00, London 08:00, NY 08:00; NYSE 9:30–16:00 EST; TSE 9:00–15:00 JST; NY "second-largest"); S5=FOREX.com Canada (overlap NY+London 13–16 GMT, Tokyo+Sydney 00–07 GMT, Tokyo+London 08–09 GMT; pergerakan USDJPY Tokyo 51 / London 66 / NY 59 pip — sumber sekunder); S6=FOREX.com US glossary (London 43% transaksi; jam bisnis 7:30–15:30 GMT — sumber sekunder); S7=RULES.md §18.9/§18.14/§18.16 (Tokyo fix 09:55 JST; zona BoJ 150/155/160; OHLC = BID); S8=STATE.md/SESSION_LOG Lapisan 1 terverifikasi (1.347.847 bar; H1-2023 185.248 bar = 13,74%, 1.431 vs 1.380 bar/hari; 2 window anomali 26.198 bar = 1,94%; SA-03 belum dijelaskan; residual M3 = open Senin 20 Mar 2023 00:00 tepat); S9=probe meta-audit (2025 = 0 hari anomali → tahun referensi bersih; H1-2023 = 130 hari kalender berbar); S10=cek langsung terverifikasi (parquet M1 2024 = 358.331 bar = raw tanpa interpolasi, kolom time, broker_time_raw, OHLC, tick_volume, real_volume, spread_points, spread_pips; M5 = spread_pips_mean/max, m1_bars; `tzdata==2026.5` terinstal di venv proyek; bucket D1-2024 = 260, terlabel 22:00 UTC winter / 21:00 UTC summer, nol bucket Sabtu/Minggu-wall).

---

## 1. Tujuan
Memahami karakter statistik data USDJPY M1–M15 periode 2023–2026 (1.347.847 bar [S8]) SEBELUM memilih metode strategi. Output akhir rantai EDA ini adalah: 7 pertanyaan terjawab dengan angka dan grafik, tabel spread terukur dari data, dan 3–5 hipotesis kandidat metode yang masing-masing falsifiable (setiap hipotesis membawa ambang yang menggugurkannya di Lapisan 3). Yang secara eksplisit BUKAN output EDA: sinyal trading, model, backtest, P&L simulasi, dan keputusan metode. Pemilihan metode adalah tugas terpisah setelah EDA direview user dan lulus audit Klenz, sesuai CONTEXT §5.

## 2. Pendekatan
Pendekatan EDA ini adalah analisis deskriptif-kuantitatif berstrata dalam kerangka empiris (§21 AGENTS.md: ukur dulu, hipotesiskan kemudian — berlaku penuh untuk EDA).
Timeframe primer adalah M1 dengan konfirmasi wajib di M5 dan M15 `[KD: ruang lingkup proyek adalah scalping M1–M15; M1 mengandung microstructure noise berupa bid-bounce sehingga inferensi berbentuk sinyal hanya boleh diambil dari M5/M15, sedangkan M1 dipakai untuk mikrostruktur seperti spread, jam, dan break]`. H1 dan D1 dipakai hanya sebagai konteks, yaitu klasifikasi regime harian dan level prior-day high/low dari resample D1.
Return didefinisikan sebagai log-return close BID dengan rumus `r = ln(close / close.shift(1))` `[PS]`; karena OHLC MT5 adalah harga BID `[S7]`, seluruh biaya sisi BUY dalam bentuk spread diperlakukan sebagai variabel terpisah dan EDA tidak menghitung P&L semu dalam bentuk apa pun.
Definisi sesi memakai sistem DST-aware per bar. Setiap bar diberi label sesi dari kolom UTC yang sudah terverifikasi, dikonversi ke waktu lokal masing-masing pusat finansial memakai zona IANA (`Asia/Tokyo`, `Europe/London`, `America/New_York`, `Australia/Sydney`). Alasan arsitektural: tiga rezim DST berinteraksi di data ini — offset server broker mengikuti aturan DST Amerika [S8], London mengikuti aturan Uni Eropa (Minggu terakhir Maret dan Oktober), New York mengikuti aturan Amerika — sehingga konstanta batas UTC tunggal pasti salah di satu musim. Database zona waktu menangani seluruh peralihan otomatis tanpa tabel DST manual.
Rentang operasional tiap sesi adalah definisi operasional proyek, bukan klaim universal:
- Tokyo: 09:00–18:00 JST, identik dengan 00:00–09:00 UTC setiap hari sepanjang tahun karena JST tidak mengenal DST `[S1,S2,S3]`.
- London: 08:00–16:00 waktu lokal London `[S3,S4; S6-sekunder menyebut jam bisnis 7:30–15:30 GMT — varians ini dicatat terbuka dan sensitivitas batas tutupnya diuji di cross-tab]`.
- NewYork: 08:00–17:00 waktu lokal New York `[S3,S4; setara 13:00–22:00 UTC saat EST/winter dan 12:00–21:00 UTC saat EDT/summer — konversi turunan ini ditampilkan di notebook 00]`.
- Sydney: 08:00–16:00 waktu lokal Sydney secara DST-aware `[S1 untuk padanan summer 21:00–06:00 UTC; padanan AEST murni adalah 22:00–07:00 UTC sebagai turunan aritmetika; tidak ada pengecualian DST untuk Sydney — kontribusi kecil sesi ini ditangani dengan sensitivitas, bukan dengan definisi yang salah]`.
Setiap bar membawa flag non-eksklusif (`is_tokyo`, `is_london`, `is_ny`, `is_sydney`) karena sesi-sesi tumpang tindih; tumpang tindih tersibuk adalah London+NewYork [S5-sekunder]. Untuk tabulasi dipakai label eksklusif dengan prioritas [London, NewYork, Tokyo, Sydney, Off] yang diturunkan dari dua prior: pangsa volume global (London ~43% [S6-sekunder], New York kedua terbesar [S4]) dan prior khusus USDJPY (pergerakan London 66 > NewYork 59 > Tokyo 51 pip [S5-sekunder]); kedua prior ini untuk dikalibrasi oleh data di EDA-02, bukan temuan. Tumpang tindih dianalisis tersendiri sebagai variabel overlap, bukan dilebur diam-diam.
Event marker yang bersifat deskriptif, bukan sinyal: Tokyo fix 09:55 JST = 00:55 UTC, tetap sepanjang tahun karena JST tanpa DST `[S7]`; buka bursa NYSE 09:30 EST = 14:30 UTC winter dan 13:30 UTC summer `[S4, turunan]`; flag zona harga 150/155/160 sebagai zona waspada intervensi BoJ `[S7]`.
Uji ketahanan batas (cross-tab robustness) mengulang seluruh analisis sesi dengan blok UTC-tetap berjangkar-winter dari literatur, yaitu Tokyo 00–09 [S1,S2,S3], London 08–16 [S2,S3], NewYork 13–22 [S1,S2], Sydney 21–06 [S1], yang dilabeli eksplisit sebagai pembanding campuran-musim dan bukan kebenaran. Kaidah keputusan: temuan sesi yang tidak bertahan di kedua sistem pelabelan diklasifikasikan sebagai artefak batas, bukan temuan `[KD]`.
Kalibrasi empiris di EDA-02: profil aktivitas dari data sendiri (lihat Metrik M1–M4) mengadili batas institusional di atas; batas final dikonfirmasi atau direvisi dengan bukti di laporan EDA, dan setiap revisi tercatat.
Aturan anti look-ahead berlaku penuh di EDA: semua indikator rolling memakai `.shift(1)`; tidak ada statistik prediktif; satu-satunya analisis yang melihat ke depan adalah event-study yang jendelanya murni pasca-event dan dilabeli deskriptif.

## 3. Struktur File
- `notebooks/scalping/eda_00_setup.ipynb` — fondasi seluruh rantai: load config dan parquet; tabel pemetaan sesi primer vs cross-tab pada contoh tanggal winter dan summer; audit hitungan stratifikasi (strata A + B + C harus tepat 1.347.847 bar [S8]); matriks ketersediaan kolom per timeframe; preregistrasi protokol placebo untuk Q6 (seed `PLACEBO_SEED = 20261006`, di-assert di kode); penguncian seluruh definisi (return, volatilitas, swing-k, level); pencetakan Kontrak 00 sebagai output (lihat bagian 14. Kontrak Notebook 00 — wajib tercetak verbatim termasuk errata E1–E3).
- `notebooks/scalping/eda_01_returns.ipynb` — menjawab Q1 distribusi return M1/M5/M15 per strata, dengan catatan eksplisit keterbatasan biaya BID-only.
- `notebooks/scalping/eda_02_volatility.ipynb` — menjawab Q2 volatilitas per jam dinding broker dan Q3 volatilitas per sesi UTC, sekaligus pengukuran spread per sesi per jam per tahun yang menghasilkan fragmen YAML (fragmen BELUM diterapkan ke config di tahap ini).
- `notebooks/scalping/eda_03_autocorr.ipynb` — menjawab Q4 autokorelasi return dengan pemisahan tegas mikrostruktur M1 vs kandidat sinyal M5/M15, per sesi dan per strata A vs B.
- `notebooks/scalping/eda_04_swings_levels.ipynb` — menjawab Q5 swing high/low dan Q6 level yang dihormati, dengan kontrol placebo persis preregistrasi notebook 00 dan aturan hari-broker vs hari-UTC pada Lampiran A1.
- `notebooks/scalping/eda_05_regimes.ipynb` — menjawab Q7 karakter per regime plus sintesis seluruh rantai menjadi draf 3–5 hipotesis.
- `reports/eda/YYYY-MM-DD/report.md` — laporan EDA: 7 jawaban masing-masing dengan tabel Klaim & Bukti (mengikuti §5/§20 AGENTS.md), tabel spread terukur, daftar hipotesis H1–H5 dengan ambang falsifikasi, daftar hal BELUM DIVERIFIKASI (termasuk angka sumber-sekunder S5/S6 dan kalender libur), dan catatan daya uji strata B.
- `reports/eda/YYYY-MM-DD/figures/FIG-01.png` s/d `FIG-NN.png` — satu grafik satu pesan, bernomor, dirujuk dari report.md.
- `configs/data.yaml` — pembaruan bagian `spread.*` HANYA melalui proposal fragmen YAML terpisah yang direview dan disetujui user pada langkah 4b, dengan struktur SPLIT pada Lampiran A2; notebook dilarang menulis config.
- Disiplin notebook: setiap notebook dieksekusi ulang top-to-bottom sebelum direview; output cell disimpan untuk reviewability (fakta: pre-commit tidak punya hook notebook sehingga kebersihan output adalah tanggung jawab coder); tidak ada dump data mentah di cell; seed acak `PLACEBO_SEED = 20261006` ditetapkan tetap untuk bagian placebo agar reproducible.

## 4. Urutan Analisis
1. Notebook 00 (setup, audit strata, tabel sesi winter vs summer, preregistrasi placebo, kunci definisi, cetak Kontrak termasuk errata E1–E3) → laporan mini → STOP dan tunggu review user.
2. Notebook 01 (distribusi return) → laporan mini → STOP dan tunggu review.
3. Notebook 02 (volatilitas jam dan sesi + pengukuran spread + fragmen YAML yang tidak diterapkan) → laporan mini → STOP dan tunggu review.
4. Langkah 4b — review fragmen spread sebagai langkah eksplisit terpisah dengan deliverable fragmen + diff terhadap config saat ini + catatan dampak ke asumsi lapisan hilir, menghasilkan putusan user (terapkan, tunda, atau tolak; putusan yang berlaku: Lampiran A2) → STOP dan tunggu putusan.
5. Notebook 03 (autokorelasi) → laporan mini → STOP dan tunggu review.
6. Notebook 04 (swing + level dengan placebo sesuai preregistrasi dan aturan hari Lampiran A1) → laporan mini → STOP dan tunggu review.
7. Notebook 05 (regime + sintesis hipotesis) plus `reports/eda/YYYY-MM-DD/report.md` dan figures → laporan penuh → review user → audit adversarial Klenz → penguncian hipotesis. Pemilihan metode tetap tugas terpisah setelah itu.
8. Setiap langkah memakai format laporan §5/§20 AGENTS.md (tabel Klaim & Bukti dengan status TERVERIFIKASI / BELUM DIVERIFIKASI / ASUMSI / GAGAL); satu langkah bermasalah berarti rantai berhenti dan tidak lanjut ke notebook berikutnya.

## 5. Metrik yang Diukur
- Distribusi return `[PS]`: skewness, kurtosis ekses, kuantil 0,1%/1%/99%/99,9%, pangsa bar dengan |r| di atas 3σ dan 5σ, QQ-plot terhadap normal, per TF (M1/M5/M15) × per strata (A/B/C).
- Volatilitas `[PS + KD]`: realized volatility Σr² dan mean|r| per jam dinding broker, per sesi UTC, per hari; `tick_volume` per jam sebagai proksi aktivitas `[KD]`; rasio volatilitas tiap sesi terhadap harian.
- Spread (sumber kolom terverifikasi ada di parquet [S10]): dari `spread_pips` M1 dihitung p50/p95/p99/maksimum dan persentase bar di atas 3 pip, dikelompokkan per sesi × per jam × per tahun dengan tahun 2023 selalu terpisah karena ekornya berbeda (p99 8,5 pip [S8]); dari M5 dipakai `spread_pips_max` untuk ekor per bucket. Ambang ">3 pip" adalah ambang deskriptif warisan temuan fetch 2026 (151 bar di atasnya, SESSION_LOG) dan BUKAN ambang keputusan trading `[S8]`.
- Kalibrasi batas sesi di EDA-02: **M1** — ranking volatilitas sesi empiris dibandingkan prior USDJPY London > NewYork > Tokyo [S5-sekunder], deviasi dicatat sebagai temuan; **M2** — enam jam UTC bervolatilitas tertinggi harus berada di dalam sesi berlabel, jika dua jam atau lebih jatuh di Off maka batas direvisi `[KD]`; **M3** — ranking sesi harus sepakat antara pelabelan DST-aware dan cross-tab UTC-tetap, jika berbeda maka dilaporkan sebagai sensitivitas dengan pelabelan DST-aware tetap primer `[KD]`; **M4** — sesi dengan rasio mean|r| terhadap spread_p95 di bawah 1 diberi flag deskriptif "biaya-mendominasi" sebagai bahan hipotesis, bukan sebagai keputusan `[KD]`.
- Autokorelasi `[PS + KD]`: fungsi autokorelasi lag 1–60 `[KD]` dengan uji Ljung-Box `[PS]`; variance-ratio dengan horizon k=5/15/60 (nilai di bawah 1 = mean-reverting, di atas 1 = trending) `[PS + KD: pilihan horizon dilaporkan beserta alternatifnya]`; autokorelasi tanda lag-1; seluruhnya diulang per sesi dan per strata A vs B.
- Swing `[KD]`: fraktal dengan k=3 dan k=5 bar tiap sisi di M5, kedua nilai k dilaporkan sebagai uji robustness dan tidak satu pun dipilih diam-diam; frekuensi swing per hari dan per sesi; ukuran swing dinormalisasi ATR(14); waktu tahan median antar swing.
- Level `[KD + placebo wajib]`: level round-number xx.00 dan granularitas alternatif xx.50 (pemilihan granularitas adalah keputusan desain yang diuji, bukan klaim) serta prior-day high/low dari resample D1; hit-rate reversal dalam window +k bar setelah sentuh versus kontrol placebo berupa level ber-offset acak dan prior-HL yang digeser, lengkap dengan interval kepercayaan. Aturan Fibonacci hanya boleh diuji dengan protokol placebo yang identik; tanpa bukti maka tidak ada klaim.
- Prior-day H/L didefinisikan sebagai bucket D1 kalender-broker (batas tengah malam broker: 21:00 UTC summer, 22:00 UTC winter [S10]) yang mencakup ekor 00:00–03:00 wall sesi sebelumnya; bucket Sabtu/Minggu-wall tidak ada sehingga rantai Jumat→Senin aman [S10]. Definisi sekunder adalah hari-UTC yang dihitung ulang; berlaku aturan perbandingan Lampiran A1 (sepakat-dengan-kesadaran-geser; DILARANG menggeser data agar "sepakat").
- Regime `[PS + KD]`: tipologi hari memakai rasio |return harian| terhadap Σ|r| intraday plus rasio range terhadap ATR; distribusi tipe hari per strata A vs B vs C; perbandingan A-vs-B dilakukan di granularitas HARIAN (realized-vol harian, range/ATR harian, proporsi tipe-hari via chi-square) dengan KS/Mann-Whitney di level-hari plus effect-size wajib (beda median dengan CI, Cliff's delta) — p-value tanpa effect-size dilarang disimpulkan; catatan keterbatasan residual (volatility clustering harian) wajib di laporan; block bootstrap sirkular (block 20 hari dagang ≈ 1 bulan menutup musiman mingguan, 10.000 resample) `[KD]` dipakai sebagai sensitivitas opsional hanya bila hasil hari-level marginal. Setiap tabel uji mencantumkan n-A/n-B/n-C; untuk strata B (n≈130 hari dagang [S9]) berlaku catatan daya: hasil negatif dibaca "tidak terdeteksi pada n ini", bukan bukti kesamaan.

## 6. Constraint
- Strata H1-2023 (185.248 bar = 13,74% [S8]) dianalisis penuh terpisah sebagai strata B; angka strata utama A tidak boleh memuat satu bar pun dari B.
- Dua window anomali (2024-10-28 s/d 11-01 dan 2026-03-10 s/d 03-27, total 26.198 bar = 1,94% [S8]) dieksklusi dari strata A dan dikarakterisasi terpisah sebagai strata C berukuran kecil yang hasilnya deskriptif saja.
- Tahun 2025 adalah tahun referensi bersih (0 hari anomali [S9]).
- Spread diukur dari data; angka spread di config saat ini diperlakukan sebagai asumsi sampai proposal pengganti disetujui pada langkah 4b dengan struktur Lampiran A2.
- Anti look-ahead dan anti leakage penuh: `.shift(1)` di semua rolling; tidak ada pemakaian data t+1 di fitur waktu t; event-study hanya memakai window pasca-event.
- OHLC adalah harga BID sehingga seluruh biaya diperlakukan terpisah sebagai spread dan tidak ada P&L semu [S7].
- EDA menyiapkan (tidak melatih) untuk validasi walk-forward di Lapisan 3.
- Aturan missing-data: statistik deskriptif memakai drop dengan jumlah drop dilaporkan; series sejajar memakai NaN+flag (terutama warmup indikator); window kosong yang tak seharusnya ada → flag + investigasi, tidak pernah diisi diam-diam; nol imputasi di seluruh EDA (konsisten dengan penghapusan interpolasi D1 di Lapisan 1).
- Kalender libur NYSE/TSE di luar scope EDA (dependensi data baru); keterbatasannya dicatat sebagai "missing event" di laporan — hari bervolume rendah terlihat di data tetapi tak teratribusi.

## 7. Dependency (reuse)
Modul yang dipakai ulang tanpa perubahan: `src/utils/config.load_config` untuk simbol, path, dan pembacaan asumsi spread saat ini; `src/data/broker_time` (`wall_clock_series`, `utc_series`, `BrokerSchedule`) untuk indeks ganda jam dinding vs UTC dan batas stratifikasi tanggal; file parquet `data/processed/M1,M5,M15,H1,D1/usdjpy_*.parquet` tahun 2023–2026 sebagai satu-satunya sumber data; definisi sesi dari notebook 00 sebagai sumber tunggal yang dirujuk notebook 01–05. Dilarang membuat modul baru di `src/`; dilarang mengimpor `strategies/` dan `models/` karena di luar scope EDA.
Dependensi environment: `tzdata==2026.5` (terverifikasi terinstal di venv proyek [S10]; penambahan disetujui user mengikuti RULES §13). Env kanonik adalah `venv/` (Python 3.12.8, pandas 2.2.3); `.venv/` adalah artefak uv yang DILARANG dipakai; sesi AI dilarang membuat atau mengubah environment alternatif tanpa izin user (Lampiran A3).

## 8. Sumber Data
Satu-satunya sumber adalah parquet Lapisan 1: M1 1.347.847 bar [S8] dengan skema dan hitungan terverifikasi (2024 = 358.331 bar, sama dengan raw [S10]); M5/M15/M30/H1/D1 hasil resample terverifikasi cocok dengan bar native MT5 [S8]; bucket D1 berjumlah 260 pada 2024, terlabel 22:00 UTC winter dan 21:00 UTC summer, tanpa bucket Sabtu/Minggu-wall [S10]. Data raw CSV tidak dibaca langsung oleh EDA. Sumber eksternal hanya referensi jam sesi S1–S6 (diperlakukan sekunder) dan jawaban Finex yang masih ditunggu dengan status offset window BELUM TERVERIFIKASI [S8].

## 9. Risiko
Kontaminasi strata (bar B atau C bocor ke A) dimitigasi audit hitungan notebook 00 plus assertion jumlah bar per strata di setiap notebook. Ekor spread 2023 (p99 8,5 pip [S8]) dapat merusak rata-rata biaya sehingga tahun 2023 selalu dilaporkan terpisah dengan median DAN tail. Bid-bounce M1 dapat terbaca sebagai mean-reversion palsu sehingga inferensi sinyal hanya diambil dari M5/M15. Temuan level palsu dimitigasi placebo yang diregistrasi sebelum eksekusi notebook 04. Scope creep ke backtest atau model dimitigasi aturan notebook 05 berhenti di hipotesis. Sengketa definisi sesi dimitigasi status kontrak pada tabel notebook 00 (mengubah definisi berarti mengulang notebook 02–05). Signifikansi palsu dari dependensi observasi dimitigasi desain level-hari + effect-size + catatan clustering. Perubahan config tak-terreview dimitigasi langkah 4b dan struktur SPLIT Lampiran A2. Sisa hal bertanda PV (tutup London 16:00 vs 17:00 lokal, granularitas level .50, angka S5/S6) dicover cross-tab, uji robustness, dan label sumber-sekunder sehingga tidak menjadi asumsi diam-diam.

## 10. Alternatif yang Ditolak (dengan alasan tercatat)
Opsi EDA hanya di M5 (lebih cepat, lebih sedikit noise) ditolak sebagai primer karena target mencakup M1, dengan M5/M15 sebagai konfirmasi. Opsi satu notebook monolit ditolak karena tidak teraudit dan kegagalan sebagian memaksa pengulangan total. Opsi library Polars ditolak demi konsistensi stack pandas karena 1,3 juta bar trivial di memori. Opsi blok UTC-tetap sebagai definisi primer ditolak berdasarkan hasil verifikasi sesi (salah di satu musim) dan dipakai hanya sebagai cross-tab. Opsi uji KS/MW di level M1 ditolak karena dependensi membuat semua hal signifikan semu. Opsi fragmen spread menumpang di laporan mini 02 ditolak karena perubahan global butuh review eksplisit. Opsi AEST-only untuk Sydney ditolak demi konsistensi DST-aware seluruh sesi. Opsi penerapan fragmen bulat-bulat ditolak karena merusak skema `pip_size`, menjebol gate validasi 2023, dan memakai basis-p95 yang overcharge (Lampiran A2).

## 11. Kriteria Sukses
Tujuh pertanyaan terjawab dan setiap jawaban terdiri dari angka, grafik, dan tabel Klaim & Bukti, atau pernyataan BELUM DIVERIFIKASI yang beralasan. Tabel spread terukur per sesi per jam per tahun tersedia beserta fragmen YAML yang siap direview. Tiga sampai lima hipotesis tertulis dengan format lengkap {klaim, metrik EDA pendukung, rencana uji di Lapisan 3, ambang falsifikasi}, dan nol hipotesis tanpa metrik pendukung. Metode BELUM dipilih pada titik ini. Audit adversarial Klenz atas EDA lulus dengan fokus stratifikasi, placebo, look-ahead, ketepatan sesi, dan ketepatan statistik.

## 12. Rencana Implementasi (Coder — dibaca berurutan, tidak boleh dilompat)
1. Reuse-check §16 AGENTS.md: daftarkan ulang seluruh dependensi di atas termasuk konfirmasi `tzdata==2026.5` via pip show, penambahan ke requirements + CHANGELOG sesuai persetujuan user, dan konfirmasi tidak ada file baru di `src/`. Tunggu konfirmasi user sebelum menulis notebook apa pun. (STATUS: SELESAI — commit `9a60995`.)
2. Tulis `eda_00_setup.ipynb` (audit strata, tabel sesi winter vs summer, preregistrasi placebo, kunci definisi, cetak Kontrak 00 di bawah secara verbatim) → laporan mini → STOP dan tunggu review. (STATUS: SELESAI di disk, belum di-commit — aturan: jangan commit sebelum audit Klenz EDA.)
3. Tulis `eda_01_returns.ipynb` → laporan mini → STOP dan tunggu review.
4. Tulis `eda_02_volatility.ipynb` termasuk fragmen YAML spread yang BELUM diterapkan ke config → laporan mini → STOP dan tunggu review.
5. Langkah 4b — review fragmen spread sebagai langkah eksplisit terpisah dengan deliverable fragmen + diff terhadap config saat ini + catatan dampak ke asumsi lapisan hilir, menghasilkan putusan user (terapkan, tunda, atau tolak; putusan yang berlaku: Lampiran A2) → STOP dan tunggu putusan.
6. Tulis `eda_03_autocorr.ipynb` → laporan mini → STOP dan tunggu review.
7. Tulis `eda_04_swings_levels.ipynb` dengan placebo persis preregistrasi dan aturan hari Lampiran A1 → laporan mini → STOP dan tunggu review.
8. Tulis `eda_05_regimes.ipynb` plus `reports/eda/YYYY-MM-DD/report.md` dan figures → laporan penuh → review user → audit Klenz → penguncian hipotesis.
9. Setiap langkah memakai format laporan §5/§20 AGENTS.md (tabel Klaim & Bukti dengan status TERVERIFIKASI / BELUM DIVERIFIKASI / ASUMSI / GAGAL); satu langkah bermasalah berarti rantai berhenti dan tidak lanjut ke notebook berikutnya.

## 13. Yang WAJIB Dihindari
Look-ahead bias dan data leakage dalam bentuk apa pun; mencampur H1-2023 ke strata utama tanpa stratifikasi; memasukkan window anomali ke strata A; klaim level tanpa kontrol placebo; menghitung P&L atau kurva ekuitas semu; memilih metode strategi; membuat file baru di `src/`; memakai angka spread asumsi config sebagai fakta; menulis sitasi baris, angka, atau grafik tanpa verifikasi; menjalankan KS/MW di level M1 atau menyimpulkan p-value tanpa effect-size; menerapkan fragmen spread tanpa langkah 4b; imputasi data dalam bentuk apa pun; memakai `.venv/` atau environment selain `venv/` kanonik; serta commit apa pun sebelum audit Klenz atas EDA selesai.

## 14. Kontrak Notebook 00 (wajib tercetak verbatim sebagai output)
- Sydney: 08:00–16:00 waktu lokal `Australia/Sydney` secara DST-aware, konsisten dengan seluruh sesi (keputusan MEDIUM-14 opsi A; kontradiksi v2 antara angka 21–06 UTC dan "DST diabaikan" dicabut).
- Prior-day H/L: primer = bucket D1 kalender-broker (batas tengah malam broker: 21:00 UTC summer, 22:00 UTC winter), mencakup ekor 00:00–03:00 wall sesi sebelumnya; bucket Sabtu/Minggu-wall tidak ada; sekunder = hari-UTC yang dihitung ulang; berlaku aturan perbandingan Lampiran A1 (sepakat-dengan-kesadaran-geser; DILARANG menggeser data agar "sepakat").
- Statistik regime: granularitas harian; effect-size wajib (beda median dengan CI, Cliff's delta); p-value tanpa effect-size dilarang disimpulkan; catatan keterbatasan clustering wajib; block bootstrap sirkular (block 20 hari dagang, 10.000 resample) hanya bila hasil marginal; setiap tabel uji mencantumkan n-A/n-B/n-C; untuk strata B (n≈130 hari dagang) hasil negatif dibaca "tidak terdeteksi pada n ini".
- Fragmen spread: langkah 4b terpisah dengan deliverable fragmen + diff-vs-config + catatan dampak; tanpa putusan user tidak diterapkan; struktur yang berlaku adalah SPLIT Lampiran A2.
- tzdata: `tzdata==2026.5` terverifikasi di venv proyek, ditambahkan ke requirements + CHANGELOG atas persetujuan user.
- Missing-data: drop dilaporkan jumlahnya; NaN+flag untuk warmup; window-kosong diinvestigasi; nol imputasi.
- Kalender libur: di luar scope; missing-event tercatat di laporan.
- Prior sesi ganda untuk dikalibrasi M1–M4: pangsa volume global dan prior khusus-USDJPY London 66 > NewYork 59 > Tokyo 51 pip; angka S5/S6 berlabel sumber sekunder.
- Strata dan hitungan kunci: A + B + C = 1.347.847 bar; B = 185.248 bar = 13,74%; C = 26.198 bar = 1,94% (5 + 14 hari); 2025 tahun referensi bersih.
- Env kanonik: `venv/` (Python 3.12.8, pandas 2.2.3). `.venv/` DILARANG dipakai.

---

## Lampiran A — Keputusan Mengikat Pasca-v3.0 (diratifikasi user; setara bobotnya dengan isi di atas)

### A1. Adjudikasi SA-03: jebakan kalender hari-UTC vs hari-broker (2026-10-06)
Temuan coder (terverifikasi independen oleh Architect): label UTC bucket D1 bergeser struktural −1 hari kalender terhadap tanggal broker (batas bucket = tengah malam broker), sehingga definisi sekunder "hari-UTC" tidak akan pernah "sepakat" literal dengan primer hari-broker. Putusan:
- **R1**: "Hari-UTC" = label kalender murni dengan offset struktural −1 yang didokumentasikan; DILARANG menggeser data agar sepakat.
- **R2**: Syarat "wajib sepakat" ditafsir ulang menjadi sepakat-dengan-kesadaran-geser: bandingkan H/L hari-broker vs H/L hari-UTC dengan memperhitungkan offset struktural; hanya divergensi MELEBIHI geseran struktural yang menjadi temuan (dilaporkan sebagai sensitivitas).
- **R3**: Seluruh pekerjaan level-hari (uji regime Q7, primer prior-day Q6) dikunci pada tanggal-broker — konsisten dengan bucket D1, strata, dan window anomali yang semuanya broker-defined. Hari-UTC sekunder saja.
- **R4**: Tanpa redesain, tanpa penundaan langkah 1–3; aturan R1–R3 dicatat di nb04/nb05 dan laporan final.

### A2. Keputusan SPLIT langkah 4b: review fragmen spread (2026-10-06)
Temuan SA-17 terverifikasi (ekor spread 2023 = artefak strata B: B p95 5,3 / H2-2023 p95 0,6 = rasio 8,83×; A p95 1,0 / mean 0,65): `by_year[2023]=3,0` menghargai biaya rezim tereksklusi ke semesta yang diperdagangkan. Putusan:
- `by_year` (2023: 3,0), `default: 1,5`, multiplier, `pip_size` dict DIPERTAHANKAN persis — semantiknya validasi whole-file; gate Lapisan 1 dipertahankan; fetch utuh. (Penerapan bulat-bulat terbukti merusak: TypeError `pip_size[symbol]`, dan validasi 2023 berbalik ERROR.)
- TAMBAH namespace baru untuk biaya backtest dari strata A: `spread.cost_basis` (default/by_year/by_session berisi MEAN — coder wajib menambah kolom mean; basis harapan = mean, bukan p95) dan `spread.stress_bands` (p95/p99 dari fragmen).
- TULIS ULANG komentar `by_year`: 3,0 adalah sifat file 2023 utuh (didominasi ekor B), BUKAN semesta yang diperdagangkan (H2-2023 ≈ 0,5 mean). Opsi "3,0 konservatif untuk backtest" DITOLAK sebagai basis (overcharge ~5×; konservatisme milik stress-test eksplisit: multiplier 2,0 + skenario rezim-B mean 1,39).
- Fragmen wajib baris `_sesi:` (pelabelan yang dipakai) dan `_metode:` (sumber file, predikat strata, agregasi); backtest kelak WAJIB pelabelan identik.
- DILARANG menyentuh `by_session`/`by_news`/`default`/`pip_size` di 4b (taksonomi beda + belum terukur).
- 6 patch self-audit mengikat: guard jangan-sentuh (di atas); `_metode:`+`_sesi:` wajib; means untuk cost_basis; checklist Klenz eksplisit atas nb02 (reproduksi prioritas pelabelan; klaim Off=0 di A; 10 bar cek tangan termasuk 2024-10-28 dan 2026-03-10); Layer 5 fail-closed (backtest menolak jalan bila kunci cost_basis hilang/basi); re-run `validate_data` pasca-aplikasi dengan ekspektasi identik 2/2/1/1; skenario max-fill + caveat sampling last-tick (kolom spread kemungkinan last-tick-per-menit sehingga mean bisa bias-rendah — mitigasi utama adalah costing per-bar di Layer 5).

### A3. Environment dan dependensi (2026-10-06)
- Env kanonik tunggal: `venv/` (Python 3.12.8, pandas 2.2.3, stack penuh: torch, MetaTrader5, jupyter, tzdata). Seluruh gate yang diverifikasi independen berjalan di env ini.
- `.venv/` (Python 3.12.13, pandas 3.0.6, tanpa pip/torch/sklearn/MT5/jupyter) adalah artefak sesi uv yang DILARANG dipakai untuk pekerjaan proyek apa pun. Dibiarkan di disk + dicatat (bukan dihapus) kecuali ada izin eksplisit penghapusan.
- Aturan proses: sesi AI DILARANG membuat, mengubah, atau memasang paket ke environment alternatif tanpa izin user. Setiap upgrade `venv/` WAJIB memutakhirkan requirements di commit yang sama.
- `tzdata==2026.5` + `MetaTrader5==5.0.6231` di-pin di requirements + CHANGELOG (commit `9a60995`, RULES §13 terpenuhi).

### A4. Jejak audit dan commit
- Lapisan 1: commit `a63d117` (HEAD saat itu). Langkah 1 EDA: commit `9a60995` (`chore(deps)`). Notebook 00 + laporan tahap 0–2: di disk, belum di-commit (aturan: jangan commit sebelum audit Klenz EDA).
- Rantai audit: temuan Klenz v2 (MEDIUM-14–17, LOW-17–21) → v3 → re-audit Klenz v3 (LOW-22–25, verdict LULUS) → meta-audit Spark (semua terkonfirmasi) → adjudikasi SA-03 → putusan 4b. Nol CRITICAL/HIGH di seluruh rantai EDA.

---

*Akhir dokumen v3.1. Perubahan berikutnya = file v3.2 (atau versi yang ditetapkan user). Coder yang menyimpang dari dokumen ini tanpa persetujuan Architect akan dikembalikan ke dokumen ini.*
