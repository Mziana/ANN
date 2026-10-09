# Spesifikasi Lapisan 3 Batch-1 -- Vonis H1 + Backtest H2 -- 2026-10-08

**Peran:** Arsitek (S26 AGENTS.md: merancang + memutus konflik; DILARANG
menulis kode produksi/implementasi). **BUKAN eksekusi. BUKAN vonis H1/H2**
(vonis = putusan terpisah sesudah re-audit). BUKAN H3 (GUGUR via S4b --
filter dilarang di data mana pun), BUKAN H4/H5 (batch-2 terpisah).
**Kontrak yang mengikat dokumen ini:** `.ai/AGENTS.md` v3.0 --
S5 (tabel Klaim & Bukti; dilarang "sepertinya OK"),
S20 (setiap klaim wajib bukti; output asli ditempel),
S21 (uji dulu, simpulkan kemudian; format Proposal Uji),
S26 (peran terpisah), S27 (arbitrase).
**Aturan besi (tulis eksplisit): klaim tanpa output mentah = GAGAL.**
**Dokumen audit menang atas ringkasan bila berselisih.**

---

## S0. Klaim & Bukti konteks (S5)

Cara baca status: TERVERIFIKASI = saya ukur sendiri di sesi ini;
TERVERIFIKASI (rujukan) = saya verifikasi keberadaan + isinya di dokumen
ter-hash yang saya baca langsung (bukan saya yang menjalankan angkanya);
ASUMSI = keputusan arsitek dalam spec ini; BELUM DIVERIFIKASI = wajib
diisi pelaksana dengan output mentah; klaim tanpanya = GAGAL.

| Klaim | Status | Bukti |
|---|---|---|
| HEAD = `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` | TERVERIFIKASI | output `git rev-parse HEAD` sesi ini |
| H1+H2 lock, blob `9720280320dcc813d422d6f540e37847b70571ff` | TERVERIFIKASI (rujukan) | `arsitek/hipotesis_lock_v1.md:13-78`, dibaca langsung S13-78 sesi ini |
| S1 (H1 KUATKAN) + S2 (median dlm-tahun; strategi pra-registrasi), blob `e8eb03daf994051600258cf412ec9e9af65d800c` | TERVERIFIKASI (rujukan) | `arsitek/putusan-arsitek-H1-H5.md:10-14`, dibaca utuh sesi ini |
| Pra-registrasi H2 + ambang gugur, blob `bc17e5de6cfefb355fe7418acd2a3a0d8b461212` | TERVERIFIKASI (rujukan) | `coder/protokol-H1-H2-H3.md:37-77`, dibaca langsung S37-77 sesi ini |
| Standing rule P-1/P-2/P-3, blob `c643c1c934055d1b85d972f4e2e2f65d8d57a69f` | TERVERIFIKASI (rujukan) | `arsitek/putusan-lapisan3-H3.md:50-124`, dibaca sesi lalu, hash diukur sesi ini |
| Uji-1 IMMATERIAL (M1 GUGUR=GUGUR INK 974/EKS 740; M2 p=0,629431041054359; M3 tanda sama B1); INK tunggal boleh dipakai, flag TETAP di store | TERVERIFIKASI (rujukan) | `coder/hasil-lapisan3-H3.md` [O8][O9][O10] + `arsitek/spesifikasi-lapisan3-H3.md:86-94` |
| cost_basis satuan pip, MEAN spread strata A; by_session London 0.61 / NewYork 0.69 / Tokyo 0.62 / Sydney 0.8; pip_size USDJPY 0.01; blob config `e277d67ea618cd681915ae2474f4ae9a8d349516` | TERVERIFIKASI (rujukan) | `configs/data.yaml:119-132,158-159`, dibaca langsung sesi ini |
| Resep VR: r = ln(close_t/close_t-1); no-gap = `utc.diff() > 15min`; `variance_ratio` Lo-MacKinlay (cumsum overlapping, ddof=1); horizon (5,15,60) | TERVERIFIKASI (rujukan) | `scripts/_build_eda03.py:177-181,421-448`, dibaca langsung sesi ini |
| Sesi beku: Tokyo 9-18 JST; London 8-16 Europe/London; NewYork 8-17 ET; Sydney 8-16 AET; prioritas London>NewYork>Tokyo>Sydney; label London/NewYork/Tokyo/Sydney/Off | TERVERIFIKASI (rujukan) | `src/features/build_features.py:72-89`, dibaca langsung sesi ini |
| D1/D2 beku: `build_labels.py` blob `2561efd552544feeb9af0b6733711015b83f43dd`; `build_features.py` blob `399e64b372e430b6def79b4fa8324a4e8e629918` | TERVERIFIKASI (rujukan) | hash diukur sesi ini; pelaksana WAJIB ukur ulang (C3) |
| Kontrak S5/S21/S26/S27 | TERVERIFIKASI (rujukan) | `.ai/AGENTS.md:217` (Klaim & Bukti), `:465-466` (Proposal Uji), `:619` (S26), `:663` (S27) |

---

## Q1. PUTUSAN: verdict M1 BUKAN vonis H1; uji real-time tetap berjalan (DIPUTUS)

**Putusan: uji real-time H+1 TETAP BERJALAN sebagai satu-satunya sumber
vonis H1.** Verdict-lock M1 (GUGUR pada INK maupun EKS) dihitung di atas
label ex-post -- metrik hari-penuh + ambang median full-sample
(0,0268/88,79) -- dan bahkan memakai ambang yang mengandung data masa
depan. Ia tidak memenuhi "identifikasi H+1 pagi, data t-1 saja" (lock
H1 `:25-27`; catatan ex-post `:32-34`). Maka M1-GUGUR tidak dapat
dipakai sebagai vonis H1 ke arah mana pun.

**Relasi kedua vonis (mengikat):**
- Vonis H1 HANYA dari uji real-time spek ini (S-H1 di bawah). M1 tetap
  sebagai anotasi sensitivitas: karena Uji-1 IMMATERIAL, kesimpulan
  klasifikasi tidak digerakkan flag-gap -- sitiran konteks, bukan penentu.
- Bila hasil searah (real-time GUGUR seperti M1): vonis H1 = GUGUR,
  dengan M1 disitir sebagai anotasi bahwa gap-flag bukan penggeraknya.
- Bila hasil BERBEDA ARAH (mis. real-time TAHAN sementara M1 GUGUR, atau
  sebaliknya): vonis MENGIKUTI uji real-time (itulah uji yang ditetapkan
  lock), DAN divergensi menjadi temuan wajib-lapor (divergence annotation:
  kedua angka + selisih n per keranjang ditempel) yang memicu eskalasi
  arsitek SEBELUM hasil dipakai ke mana pun. Override senyap DILARANG.
- Klausul anti-penyelamatan lock (`:48-51`) mengikat dua arah: kegagalan
  tidak boleh ditafsir-ulang via reversal-day, dan keberhasilan pun tidak
  boleh diklaim sebagai bukti ketahanan terhadap reversal-day. Izin
  eksplorasi split-usia-tren (`:53-55`) tetap murni-eksplorasi, tanpa
  pengaruh pada vonis.

**Alasan satu paragraf:** M1 adalah formula verdict lock yang dijalankan
di atas label ex-post berambang full-sample, sedangkan lock memerintahkan
uji real-time tanpa kebocoran masa depan; memakai M1 sebagai vonis akan
menguji artefak ambang ex-post, bukan hipotesis. Satu-satunya perbedaan
prosedur yang diizinkan antara M1 dan uji real-time adalah identifikasi
ambang (expanding, t-1 saja) -- drift, kriteria gugur, dan populasi INK
tetap identik agar keduanya komparabel.

## Q2. PUTUSAN: pra-registrasi H2 DIRATIFIKASI dengan pin klarifikasi (DIPUTUS)

**Putusan: RATIFIKASI, bukan revisi strategi.** Ekonomika strategi tidak
berubah (sinyal, arah long-only, SL 1x ATR / TP 2x ATR, biaya session-mean
tetap sama seperti `:37-77` protokol dan `register_h2_strategy()`
`build_labels.py:245-261`). Yang ditambahkan spec ini hanyalah pin
klarifikasi atas ambiguitas yang akan membuat backtest tak-reproduksibel
bila dibiarkan. Karena backtest BELUM PERNAH berjalan, pin ini adalah
bagian desain spec, BUKAN optimasi-dari-data (tidak ada data evaluasi
yang terlihat sebelum pin ditetapkan).

**Satu-satunya perbaikan interpretif (terbukti inkoheren bila literal):**
"exit close < open di jam terakhir" tidak dapat dibaca pada bar yang sama
dengan entry (syarat entry justru close > open) -- maka sinyal exit
dievaluasi pada tiap bar M15 SESUDAH bar entry. Selain itu seluruh pin
adalah disambiguasi, bukan perubahan.

**Teks final strategi H2 (kata-per-kata, mengikat pelaksana):**

> Strategi "H2 M15 momentum" (trend-following M15 sederhana, LONG-ONLY).
> Universe: bar M15 USDJPY store B1, tahun date_broker 2023/2024/2025
> (2026 dikecualikan).
> (a) Bar sinyal: bar M15 yang tutup tepat pada 15:00 UTC. Sinyal entry
> bila close > open pada bar itu; 1x per hari-broker; bila bar tidak ada
> (gap) maka hari itu FLAT dan dihitung sebagai hari-tanpa-sinyal.
> (b) Konfirmasi: kolom `day_label` BEKU D4 pada hari T-1 == "trending"
> (klasifikasi terkunci atas data hari T-1 yang sudah lengkap; bebas
> lookahead terhadap entry hari T jam 15:00 UTC; BUKAN prosedur
> identifikasi real-time uji H1; BUKAN data hari T).
> (c) Harga entry = close bar sinyal. ATR = nilai `atr_14_d1` hari T-1
> (data t-1 saja). SL = entry - 1x ATR; TP = entry + 2x ATR (satuan harga JPY).
> (d) Monitoring mulai bar M15 berikutnya. Pada tiap bar berikutnya
> sampai batas hari: (i) bila low <= SL maka exit SL pada harga SL;
> (ii) selain itu bila high >= TP maka exit TP pada harga TP;
> (iii) selain itu bila bar tutup close < open maka exit pasar pada close
> bar itu; (iv) bila hari-broker habis maka exit pada close bar M15
> terakhir hari T (time-stop). Prioritas intra-bar: SL > TP > sinyal-exit
> (konservatif; ASUMSI spec, rasional: tanpa data intrabar, pilih yang
> merugikan strategi).
> (e) Biaya per trade = `cost_basis.by_session[session_label(bar entry)]`
> dalam pip (London 0.61 / NewYork 0.69 / Tokyo 0.62 / Sydney 0.8;
> bila label "Off" maka pakai `cost_basis.default` 0.65 -- ASUMSI spec,
> rasional: biocaya mean strata A sebagai fallback netral) dikali
> pip_size 0.01 menjadi JPY. EV per trade (JPY) = harga_exit - harga_entry
> - biaya_JPY. Fill pada harga teramati (level SL/TP exact; tanpa slippage
> di luar cost_basis -- ASUMSI spec, dinyatakan eksplisit).
> (f) Tanpa pengecualian hari: hari karantina dan hari ber-flag gap tetap
> diperdagangkan; overlay quarantine/gap hanya dilaporkan deskriptif
> (n trade di hari tsb). Rasional: strategi menguji EV pada realitas yang
> diperdagangkan; eksklusi butuh basis lock dan tidak ada.

**Alasan satu paragraf:** pra-registrasi yang ada sudah memuat seluruh
ekonomika strategi dan memenuhi syarat lock S2(b) (dokumen sebelum satu
pun backtest); yang kurang hanyalah ketepatan operasional yang tanpanya
dua pelaksana independen akan menghasilkan dua backtest berbeda. Pin di
atas tidak mengubah satu pun parameter ekonomi (jam, rasio SL:TP, basis
biaya), sehingga statusnya tetap pra-registrasi murni -- merevisinya
menjadi strategi berbeda justru akan melanggar S2 dan menyerupai
shopping-desain.

---

## Uji S-H1 -- Vonis H1 real-time (identifikasi H+1 pagi, data t-1 saja)

### Proposal Uji (S21)

**Apa yang diuji:** apakah conditioning tipe-hari bertahan bila tipe hari
diidentifikasi tanpa kebocoran masa depan (bukan apakah gap "nyata" --
sudah terbukti B1; bukan vonis silang H2/H4/H5).
**Hipotesis:** H0 = gugur (salah satu kriteria lock terpenuhi);
H1 = tahan (keduanya negatif).
**Populasi terkunci:** INK 974 hari-broker, varian tunggal (per Uji-1
IMMATERIAL + boleh-pakai spec H3 `:86-94`); kolom flag TETAP di store.
Satu-satunya perbedaan vs M1 = prosedur ambang di bawah; drift, kriteria,
dan populasi identik (komparabilitas M1 <-> H1).
**Prosedur identifikasi real-time H+1 pagi (ASUMSI spec, rasional:
pembacaan paling ketat dari "data t-1 saja" -- ambang tak boleh memuat
hari yang diklasifikasi maupun hari sesudahnya):** untuk hari T terurut
date_broker, ambang = median(`ratio_path`) dan median(`range_atr`) atas
hari-broker selesai SEBELUM T (strictly past, expanding), dari
`daily_metrics` runtime via jalur D1 read-only (kode beku, tanpa ubah).
Syarat riwayat minimum 60 hari-broker (burn-in; ASUMSI spec, rasional:
stabilitas median awal ~3 bulan); hari tanpa 60 hari riwayat =
non-evaluable, dilaporkan n + rentang tanggal (bukan skip senyap).
Klasifikasi: trending = ratio_path_T > med_r DAN range_atr_T > med_a;
range = keduanya <= median; else normal. Drift = kolom `london_drift_norm`
BEKU D4 (provenans SAH per P-1 putusan H3), bertanda (konsisten M1).
NaN: dropna per kolom uji (sama M1). Karantina: inklusif identik M1
(mask dipertahankan) -- komparabilitas.
**Baseline (dihitung DULU, ditempel, baru dibandingkan -- S21 butir 7):**
S1 = reproduksi M1-INK dari D4 dalam run yang sama; WAJIB cocok presisi
penuh dengan [O8] hasil H3 (n_trending 330 / n_pembanding 324;
median 0.02948996641114935 / 0.015065793016650224;
CI95 [-0.02729045556350576, +0.052787080233690914];
chi2_2xk 0.7666041417663041, p_2xk 0.6816069745648556; verdict GUGUR).
Mismatch apa pun = GAGAL-eksekusi: STOP, eskalasi, DILARANG lanjut ke S2.
**Estimasi biaya:** komputasi read-only menit; nol perubahan repo (C2).
**Rencana:** S1 (gate reproduksi) -> S2 (verdict real-time + kriteria)
-> S3 (suplemen + divergence check Q1) -> keputusan GUGUR/TAHAN.
**Status:** BELUM DIUJI.

### Metrik + ambang (pra-registrasi; dilarang tambah pasca-hoc)

- **Kriteria (i) -- penentu (lock verbatim `:29-30`).** Selisih median
  drift (trending real-time vs range real-time), CI95 bootstrap percentile
  day-level, resampling TERPISAH dua himpunan disjoin (label wajib:
  "unpaired (disjoint)" -- standing rule P-2/F-3), B=10000, seed 20261006
  (ASUMSI spec: kontinuitas M1 + konvensi seed lock H5 `:145` + menutup
  celah F-4 permanen untuk batch ini). GUGUR bila CI95 memuat 0.
- **Kriteria (ii) -- penentu (lock verbatim `:29-30`).** Chi-square tabel
  tahun x trending/bukan, tahun utuh 2023-2025 (2026 parsial
  dikecualikan), tanpa koreksi Yates (ASUMSI spec: preseden A-3 Uji-1,
  dikunci permanen di sini). GUGUR bila p < 0,01.
- **Hasil:** GUGUR (salah satu kriteria terpenuhi) / TAHAN (keduanya
  negatif). Selesainya uji (lulus-eksekusi) != hasilnya.
- **Suplemen (dilaporkan, BUKAN penentu):** sign test dua-sisi median
  drift keranjang trending = 0 (alpha lapor 0,01); tabel chi2 3-kolom;
  robustness R1 (drift `london_drift_4h` mentah) / R2 (pembanding
  normal+range) / R3 (kriteria-ii memuat 2026) sebagai verdict-formula
  non-penentu (kontinuitas M1, menjaga A-1/A-3); agreement label
  real-time vs ex-post (%, n pindah keranjang) sebagai diagnostik
  besar-pergeseran; median per keranjang + n evaluable per tahun.

---

## Uji S-H2 -- Backtest strategi diagnostik + VR OOS

### Proposal Uji (S21)

**Apa yang diuji:** apakah strategi pra-registrasi Q2 menghasilkan
EV-after-cost positif per tahun, dan apakah properti pasar (VR) bertahan
OOS (bukan mencari strategi "lebih baik" -- shopping DILARANG; H2 adalah
hipotesis eksploratori jujur per lock `:63-65`).
**Hipotesis:** H0 = gugur (salah satu ambang lock terpenuhi);
H1 = tahan.
**Populasi terkunci:** bar M15 2023-01-01..2025-12-31 (tahun date_broker;
2026 dikecualikan penuh); strategi final kata-per-kata di Q2 (TERTUTUP --
satu strategi, tanpa varian; dilarang tambah rule/split/pintu
pasca-lihat-hasil).
**Baseline (dihitung DULU, ditempel):** S0 deskriptif pra-EV per tahun:
n hari-broker, n hari-tanpa-bar-sinyal, n hari-tanpa-konfirmasi,
n trade tereksekusi, n exit per jenis (SL/TP/sinyal/time-stop),
n trade di hari karantina/gap-flag. S0 provenans: hash D4 + hash config
+ cocok-tabel cost_basis + jumlah baris M15.
**Estimasi biaya:** backtest read-only menit; nol perubahan repo (C2).
**Rencana:** S0 (provenans + deskriptif) -> S1 (EV per trade per tahun +
median + ambang) -> S2 (VR OOS + ambang) -> keputusan GUGUR/TAHAN.
**Status:** BELUM DIUJI (protokol `:39-40`: backtest menunggu persetujuan;
spec ini ADALAH persetujuan yang dimaksud -- eksekusi milik batch coder
berikutnya, bukan dokumen ini).

### Metrik + ambang (pra-registrasi; dilarang tambah pasca-hoc)

- **EV-after-cost (penentu; lock verbatim `:76-78` + S2(a)).** Per tahun
  2023/2024/2025: median EV-per-trade-after-cost (JPY, definisi Q2(e)).
  Deskriptif wajib: n, mean, % positif. **GUGUR bila median <= 0 pada
  >= 2 tahun.** Tanpa aturan minimum-trade (ASUMSI spec, rasional:
  lebih sedikit kenop = lebih sedikit sengketa; n dilaporkan apa adanya).
- **VR OOS (penentu; lock verbatim `:76-78`).** r = ln(C_t/C_{t-1}) M15
  pool 2023-2025; no-gap = `utc.diff() > 15 menit` (verbatim resep EDA);
  `variance_ratio` verbatim (cumsum overlapping, ddof=1); horizon 5/15/60;
  rata-rata VR = mean ketiganya; SATU angka penentu (ASUMSI spec,
  rasional: VR adalah properti pasar level-pool seperti basis EDA yang
  melaporkan satu angka, bukan performa strategi level-tahun).
  **GUGUR bila rata-rata VR OOS <= 1.**
- **Hasil:** GUGUR (salah satu ambang terpenuhi) / TAHAN (keduanya negatif).

---

## S-C. Kriteria selesai Batch-1 (mesin + output mentah)

Dokumen hasil kontrak: `coder/hasil-lapisan3-H1H2.md`
(muat tabel Klaim & Bukti S5 + semua [On] bernomor; tiap angka tertaut
ke [On]; auditor memverifikasi dengan mencocokkan ulang, bukan membaca
narasi).

| # | Syarat | Perintah mentah (jalankan, tempel output) | Pola lolos |
|---|---|---|---|
| C1 | HEAD tak berubah | `git rev-parse HEAD` | `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` |
| C2 | Nol tulis produksi + nol sentuh lindung (pola P-3: tracked-only + before/after; pola "output KOSONG" PENSIUN dan DILARANG dipakai) | SEBELUM tugas: `git status --porcelain -uall -- src/ tests/ data/ configs/ reports/eda/ <daftar-C2>` ditempel sebagai BEFORE; SESUDAH tugas: perintah sama sebagai AFTER; plus `find src tests data configs -type f -newermt "<timestamp-mulai-tugas>"` | AFTER identik BEFORE (diff ditempel; bila beda = GAGAL) DAN find kosong. Daftar-C2 (= lindung): `src/features/build_labels.py`, `src/features/build_features.py`, `tests/test_build_labels.py`, `tests/test_build_features.py`, `data/features/M15/`, `data/labels/`, `data/processed/`, `data/raw/`, `arsitek/hipotesis_lock_v1.md`, `arsitek/putusan-arsitek-B1.md`, `arsitek/putusan-arsitek-H1-H5.md`, `arsitek/spesifikasi-lapisan3-H3.md`, `arsitek/putusan-lapisan3-H3.md`, `configs/data.yaml`, `reports/eda/` |
| C3 | Hash beku cocok + cost tercatat | `git hash-object` 7 berkas trio+D1/D2 (prefix `2561efd5` / `dc07a7e6` / `bc17e5de` / `34530854` / `399e64b3` / `ed7ac435` / `07402f40` -- S0) ; `sha256sum data/labels/*.parquet` (cocok `47d15c41` / `32eaf6b2`) + mtime D4 tak berubah vs sebelum tugas ; `git hash-object configs/data.yaml` ditempel + tabel cost_basis S0 dicocokkan nilai-per-nilai | semua prefix cocok; cost sama persis S0 |
| C4 | Gate hijau | `pytest` penuh ; `ruff check .` ; `ruff format --check .` ; `python scripts/check_foreign_chars.py coder/hasil-lapisan3-H1H2.md` | N passed, 0 fail/skip (N dicatat) ; All checks passed ; N files already formatted ; OK asing -- masing-masing dengan rc + cakupan ditempel |
| C5 | Determinisme | harness S-H1 + harness S-H2 masing-masing dijalankan 2x, `sha256` berkas angka-hasil ditempel keduanya | kedua hash IDENTIK per harness (`cmp` IDENTIK) |
| C6 | S-H1 selesai + hasil diputus | S1 (reproduksi [O8] presisi penuh) + S2 (2 median, CI95, chi2, p, verdict) + S3 (suplemen + divergence) ditempel [On] | S1 exact-match (else GAGAL-eksekusi) ; GUGUR/TAHAN per S-Uji-S-H1 |
| C7 | S-H2 selesai + hasil diputus | S0 (provenans + deskriptif per tahun) + S1 (median/mean/n/% per tahun) + S2 (VR5/VR15/VR60 + rata-rata) ditempel [On] | GUGUR/TAHAN per S-Uji-S-H2 |
| C8 | Dokumen hasil final | `git hash-object coder/hasil-lapisan3-H1H2.md` SESUDAH penulisan terakhir ditempel (contoh BENAR: output hash; contoh SALAH yang DILARANG: "pastikan hash benar" tanpa output) | hash tercatat |
| C9 | Staged = 0, tanpa commit | `git diff --cached --name-only` (harus kosong) ; `git log --oneline -1` (tetap C1) | nol staged, HEAD tetap |

Skrip analisis HANYA di `%TEMP%\opencode\l3h1h2` (tidak di-commit;
C2 menegakkan). D4 di disk tidak ditimpa (sha256 + mtime before/after
identik di C3; `main()`/`write_labels` DILARANG di jalur eksekusi).
Provenans WAJIB exact-comparison atau toleransi eksplisit (P-1);
sampel bersarang WAJIB estimator paired + CI selaras alpha (P-2).

---

## S-B. Batasan eksplisit (larangan bentuk-spesifik)

1. **Vonis H3/H4/H5 di batch ini DILARANG.** H3 sudah GUGUR (S4b);
   filter/TAU DILARANG dipakai dalam bentuk apa pun di batch ini.
2. **Eksklusi buta TETAP DILARANG** -- tidak ada hari/bar yang dibuang
   dari populasi terkunci kecuali burn-in 60-hari S-H1 (pra-registrasi di
   atas, dilaporkan eksplisit) dan bar-tanpa-data (dilaporkan sebagai
   hari-tanpa-sinyal, bukan dibuang diam-diam).
3. **Shopping DILARANG:** ambang/rule/alternatif/strategi/varian dari data;
   TAU_alt tidak ada di batch ini; threshold real-time expanding bukan
   objek optimasi (rumus median terkunci di atas).
4. **Kalibrasi ulang apa pun DILARANG** (ambang klasifikasi, median,
   ATR, biaya -- semua dari lock/config ter-hash).
5. **Guard nilai-vs-diri DILARANG** (pelajaran P-1): setiap klaim
   reproduksi/identik WAJIB instrumen exact atau toleransi eksplisit;
   `isclose`-default untuk klaim ketiadaan-sel = temuan.
6. **Fixture seragam untuk klaim sensitivitas DILARANG** (pelajaran H3):
   robustness WAJIB R1/R2/R3 heterogen di atas, bukan satu fixture
   diulang-ulang.
7. **Output parsial berlabel proses-penuh DILARANG; klaim "diuji via X"
   sambil mengaku belum ada test X DILARANG** (tahun tanpa trade tetap
   dilaporkan; median atas n kecil = apa adanya, bukan disembunyikan).
8. **Menaikkan severity temuan tertutup DILARANG** (F-3/F-4/F-5 H3 tetap
   LOW; Uji-1 IMMATERIAL tetap).
9. **Grain selain hari-broker tunggal DILARANG; `utc.normalize()`
   DILARANG** (adjudikasi C). Tahun bar = date_broker store B1.
10. **Kopling H2 ke hasil H1 DILARANG:** konfirmasi H2 memakai label D4
    beku (Q2(b)), bukan label real-time S-H1; hasil S-H1 tidak boleh
    mengubah strategi/kalkulasi S-H2 dan sebaliknya.
11. **Mengubah redaksi/ambang lock DILARANG** kecuali addendum berversi
    yang disahkan arsitek (bukan bagian batch ini).
12. **Menyentuh file beku/lindung DILARANG** (daftar C2); pelanggaran =
    gagal total (preseden putusan fix DILARANG-1).

---

## S-R. Relasi ke konsumen hilir (boleh vs dilarang pakai hasil)

| Hasil dipakai untuk | Status |
|---|---|
| Vonis H1 dari S-H1 (GUGUR/TAHAN) | BOLEH (satu-satunya sumber vonis H1) |
| Vonis H2 dari S-H2 (GUGUR/TAHAN) | BOLEH (satu-satunya sumber vonis H2) |
| Anotasi sensitivitas: M1-IMMATERIAL + agreement real-time-vs-expost pada vonis H1 | BOLEH (preseden Uji-1) |
| Keputusan arsitek tahap berikut atas dasar kedua vonis | BOLEH |
| Vonis silang untuk H4/H5 (placebo/kuartil butuh desain independen) | DILARANG |
| Mengubah ambang/threshold apa pun berdasarkan hasil | DILARANG (optimasi-dari-data) |
| Membuang hari/bar/flag/kolom dengan alasan hasil apa pun | DILARANG |
| Memakai S-H1 sebagai vonis klasifikasi lain / S-H2 sebagai kalibrasi | DILARANG |

---

## Self-audit 1x

1. Tidak ada instruksi eksekusi selain perintah verifikasi C1-C9;
   tidak ada vonis H1/H2 di spec ini (hasil = GUGUR/TAHAN milik coder +
   putusan terpisah); tidak ada perubahan kode/data/ambang (ambang
   expanding-median adalah prosedur identifikasi dari lock "data t-1
   saja", bukan ambang baru -- nilainya dihitung saat eksekusi).
2. Setiap ambang penentu tertaut ke lock (kriteria H1 `:29-30`; ambang H2
   `:76-78`; S2(a)(b) putusan H1-H5 `:12-14`) atau dilabel ASUMSI dengan
   rasional (burn-in 60, B=10000+seed, tanpa-Yates, prioritas SL>TP,
   fallback Off, VR-pool, tanpa-min-trade) -- tidak ada angka dari data
   evaluasi (backtest dan uji real-time keduanya BELUM jalan).
3. Q1 dan Q2 keduanya diputus eksplisit dengan alasan satu paragraf
   masing-masing (S-Q1, S-Q2 di atas).

**Putaran adversarial (cek sendiri sebelum serah):**
- *Correctness.* Sitiran S3: H1 `:13-55` (redaksi, ambang gugur, ex-post,
  reversal 3-lapis, anti-penyelamatan, izin eksplorasi); H2 `:59-78`;
  S1/S2 putusan `:10-14`; prereg `:37-77`; standing rule P-1/P-2/P-3
  putusan H3 `:50-124`; angka persis -- 0,0268/88,79; TAU
  2.5951672079821496e-05; AUC 0.8173755150499336; p M1
  0,629431041054359; INK 974/EKS 740; median M1
  0.02948996641114935/0.015065793016650224; CI95 M1
  [-0.02729045556350576, +0.052787080233690914]; chi2 M1
  0.7666041417663041/p 0.6816069745648556; cost 0.61/0.69/0.62/0.8/0.65;
  pip_size 0.01; SL 1x/TP 2x; entry 15:00 UTC; burn-in 60; B=10000 seed
  20261006. Path + baris diverifikasi ulang sesi ini (S0) -- path pindah
  atau baris geser akan tertangkap C3/hash.
- *Bias & Asumsi.* Tidak ada ambang baru yang diselipkan -- kriteria penentu
  verbatim lock; ASUMSI hanya menutup titik yang lock/spec tidak
  menetapkan bentuk operasionalnya (prosedur ambang real-time, B/seed,
  Yates, prioritas intra-bar, fallback Off, pool VR, tanpa-min-trade),
  masing-masing dengan rasional terdokumentasi dan -- bila berisiko
  menopang kesimpulan -- dijaga robustness non-penentu (R1-R3) atau
  suplemen. Q2 tidak mengandung konflik kepentingan: backtest belum jalan
  sehingga pin klarifikasi tak dapat menyesuaikan hasil; ekonomika
  strategi identik dengan prereg yang sudah disahkan S2(b).
- *Meta.* Brief mandiri (seluruh S3 verbatim di dalam brief; spec tetap
  merujuk file:baris terverifikasi, bukan parafrasa). Ruang putusan nyata
  arsitek terpakai: Q1 (memilih real-time-sebagai-vonvis + aturan
  divergensi, menolak jalan pintas M1) dan Q2 (ratifikasi-berpin,
  menolak revisi strategi maupun eksekusi prematur). Pelajaran H3
  tercakup bentuk-spesifik: P-1 (larangan 5 + C5/C3 exact), P-2 (label
  unpaired + CI selaras alpha di kriteria-i), P-3 (C2 tracked-only +
  before/after; pola KOSONG dipensiunkan eksplisit), C2-gagal-eksekusi
  (S1 exact-match gate; burn-in/hari-tanpa-sinyal lapor-eksplisit),
  ANOMALI (divergence annotation Q1 sebagai eskalasi wajib).
