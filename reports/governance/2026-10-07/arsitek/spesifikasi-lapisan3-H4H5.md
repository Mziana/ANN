# Spesifikasi Lapisan 3 Batch-2 -- Uji H4 + Uji H5 -- 2026-10-09

**Peran:** Arsitek (S26 AGENTS.md: merancang + memutus konflik; DILARANG
menulis kode produksi/implementasi). **BUKAN eksekusi. BUKAN vonis H4/H5**
(vonis = putusan terpisah sesudah re-audit). BUKAN H1/H2/H3 (ketiganya
GUGUR final -- batch ini DILARANG membangkitkannya kembali dalam bentuk
apa pun).
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
| H4+H5 lock, blob `9720280320dcc813d422d6f540e37847b70571ff` | TERVERIFIKASI (rujukan) | `arsitek/hipotesis_lock_v1.md:104-149`, dibaca langsung S104-149 sesi ini |
| S5 (EV 6 jam tetap + cost_basis 4b; pola OOS hitung-ulang) + S6 (lapor jumlah sel; koreksi multiplicity bernama), blob `e8eb03daf994051600258cf412ec9e9af65d800c` | TERVERIFIKASI (rujukan) | `arsitek/putusan-arsitek-H1-H5.md:18-21`, dibaca utuh sesi ini |
| Basis EDA H4/H5 + M4 kanon + T-01, blob `15ecb37dcfc62df64196714eed3ceabdc6a31ced` | TERVERIFIKASI (rujukan) | `reports/eda/2026-10-06/report.md:36-48,68-76,99-125,127-132`, dibaca langsung sesi ini |
| H1/H2 GUGUR final; burn-in 60 POSISI; R-B1 manifest; R-B2 bucket genap 0+369+269+140=778; R-B3 exit DEV-B3; R-B4 venv kanonik, blob `ca4e0b70d9dc4272347b74b1ea78d7a5f94593ee` | TERVERIFIKASI (rujukan) | `arsitek/putusan-lapisan3-H1H2.md`, hash diukur sesi ini |
| Standing rule P-1/P-2/P-3 + S4b, blob `c643c1c934055d1b85d972f4e2e2f65d8d57a69f` | TERVERIFIKASI (rujukan) | `arsitek/putusan-lapisan3-H3.md`, hash diukur sesi ini |
| B1-1 (H5 baca `spread_pips` M1 langsung) + B1-2 (M5 bukan input), blob `91d4c99307e3750e78802b5b424af579e2113249` | TERVERIFIKASI (rujukan) | `arsitek/putusan-arsitek-B1.md:15-33`, hash diukur sesi ini |
| cost_basis satuan pip MEAN strata A; by_session London 0.61 / NewYork 0.69 / Tokyo 0.62 / Sydney 0.8; default 0.65; pip_size USDJPY 0.01 | TERVERIFIKASI | `configs/data.yaml` dibaca langsung sesi ini (blok `cost_basis` + `pip_size`) |
| Sesi beku: Tokyo 9-18 Asia/Tokyo; London 8-16 Europe/London; NewYork 8-17 America/New_York; Sydney 8-16 Australia/Sydney; prioritas London>NewYork>Tokyo>Sydney | TERVERIFIKASI | `src/features/build_features.py:72-89` dibaca langsung sesi ini, blob `399e64b372e430b6def79b4fa8324a4e8e629918` |
| Resep M2: `hourly.groupby("hour_utc")["abs_r_pips"].mean().sort_values(ascending=False).head(6)`; guard `n_Off_top6 < 2`; M3 DST-vs-xtab SETUJU | TERVERIFIKASI | `scripts/_build_eda05.py:814-859,876-878` dibaca langsung sesi ini, blob `e29e18c7eb98083ab0857eebf3c4529b8983f23e` |
| Protokol placebo nb04 PERSIS: seed 20261006; M5; ATR(14).shift(1); theta 0.5xATR; grid 0.5 xx.00 primer; touch `low<=L<=high`; direction `sign(close_{t-1}-L)`; through/away `L-/+d*theta`; scan t+1..t+24; window (6,12,24) primer 12; tie terpisah; denom away+through; placebo_acak U(5,25)pip + touch-genuine maju<=24; placebo_hl geser U(0.25,1.00)xATR; bootstrap 10.000 day-cluster | TERVERIFIKASI | `scripts/_build_eda04.py:158-180,263-265,562-668,690-810,820-959,974-1011` dibaca langsung sesi ini, blob `641210e72b63898aaa8d106e1a2a697901504575` |
| D4 sha256 `47d15c41...`; M15 features sha256 `cd6a85e4...` (kolom: session_label, hour_utc, date_broker, atr_14_d1, ...); M1 2024/2025 `69b2c026/ fce65a3a`; M5 2024/2025 `da5e8944/a999a4bb`; M1 punya `spread_pips`; M5 tanpa kolom sesi (derivasi runtime) | TERVERIFIKASI | `sha256sum` + baca kolom via venv sesi ini |
| Preseden struktur batch: spec Batch-1 `fc29f6fa...`, hasil Batch-1 `1550209f...`, re-audit `e4143132...`, spec-H3 `dacd0708...` | TERVERIFIKASI (rujukan) | hash diukur sesi ini |
| Kontrak S5/S21/S26/S27 | TERVERIFIKASI (rujukan) | `.ai/AGENTS.md:217` (Klaim & Bukti), `:465-466` (Proposal Uji), `:619` (S26), `:663` (S27), dibaca sesi lalu |

---

## Q1. PUTUSAN: walk-forward 2023-seed; evaluasi 2024-2025 pool; 2026 dikecualikan penuh (DIPUTUS)

**Putusan:**

- **Jendela evaluasi (penentu) = date_broker 2024-01-01..2025-12-31, pool
  tunggal** untuk H4 (pola + EV) dan H5 (sel). Satu angka penentu per
  kriteria (preseden VR-pool H2) -- tanpa uji per-tahun penentu, tanpa
  koreksi multiplicity antar-tahun.
- **2023 = seed/history SAJA, bukan evaluasi:** satu-satunya pemakaian
  2023 yang diizinkan adalah ambang kuartil ATR H5 (cutoff_2024 =
  kuantil-0,75 `atr_14_d1` harian 2023). H4 DILARANG memakai 2023 untuk
  apa pun (jam tetap dari lock, tanpa kalibrasi) -- 2023 bukan penentu,
  bukan deskriptif di batch ini.
- **2026 dikecualikan PENUH** (penentu maupun deskriptif) di H4 dan H5.
  Alasan: preseden H2 (2026 parsial = tahun berjalan) + anti-smuggling
  2026 (data yang sudah terlihat di EDA full-sample dilarang masuk
  evaluasi dengan dalih apa pun).
- **Deskriptif per-tahun 2024/2025 BOLEH** (top-6 per tahun, EV per
  tahun, n per sel) sebagai konteks stabilitas -- non-penentu, tanpa
  vonis parsial darinya.

**Alasan satu paragraf:** lock memerintahkan OOS ("data OOS baru",
"walk-forward, biaya penuh") tanpa menetapkan jendelanya, sementara EDA
full-sample 2023-2026 sudah terlihat sehingga memakai tahun mana pun di
dalamnya sebagai penentu tanpa pagar = shopping-jendela; 2024-2025 pool
adalah jendela utuh terbesar yang belum dipakai mengunci ambang
(2023 = tahun kalibrasi TAU H3 + seed; 2026 = parsial berjalan),
sehingga satu-satunya pemakaian 2023 yang sah adalah statistik
ambang-kuartil yang rumusnya terkunci di sini sebelum eksekusi, dan 2026
dibuang penuh mengikuti preseden H2.

## Q2. PUTUSAN: grid H5 = 4 sel + 1 agregat deskriptif; Holm alpha 0,01; aturan TAHAN/GUGUR (DIPUTUS)

**Putusan:**

- **Grid penentu H5 (TERTUTUP -- tepat 4 sel):** irisan
  {hari Q4-ATR} x {sesi bar event} untuk sesi =
  London / Tokyo / NewYork / Sydney, pada event **round_xx00 SAJA**
  (xx.00 = primer Kontrak 00), window primer **k=12 SAJA**,
  komparator **placebo_acak round_xx00 SAJA**. DILARANG menambah sel
  (xx.50, hl_broker, hl_utc, k=6/24, placebo_hl) sebagai penentu.
- **Agregat ke-5 = deskriptif non-penentu:** Q4-ATR semua-sesi pool
  (round_xx00, k=12, vs placebo_acak), dilaporkan tanpa vonis.
  k=6/24 dan CI terpisah gaya-nb04 BOLEH dilaporkan deskriptif,
  non-penentu.
- **Metrik sel:** `diff = HR_real - HR_plac` dengan CI95 bootstrap
  paired-day (resample hari-broker, hitung kedua HR pada resampel yang
  sama, B=10.000, seed 20261006, persentil). Sel POSITIF bila
  batas-bawah CI95 diff > 0.
- **Multiplicity: Holm step-down atas 4 p-value sel** (p dari bootstrap:
  proporsi resampel diff <= 0, satu-sisi ke arah real>plac),
  **alpha keluarga 0,01** (preseden alpha lock H1/H2). FDR/bonferroni
  biasa/nezavisni DILARANG (S6 menuntut koreksi *bernama*; yang
  terkunci di sini = Holm).
- **Aturan keputusan H5:** TAHAN bila >= 1 sel positif-Holm;
  GUGUR bila keempat sel gagal (lock verbatim `:147-148`).
- **Aturan keputusan H4 (dua kriteria lock, OR-gugur, tanpa koreksi):**
  GUGUR bila (a) >= 2 dari 6 jam-teratas-hitung-ulang jatuh Off, ATAU
  (b) median EV-per-trade-after-cost pool <= 0. TAHAN = keduanya
  negatif. Tanpa koreksi multiplicity antar-(a)(b): keduanya syarat
  perlu yang arah-gugurnya sejalan falsifikasi (membuat TAHAN lebih
  sulit, bukan lebih mudah) -- didokumentasikan di sini, bukan dari data.
- **Lintas H4/H5 tanpa koreksi silang:** dua hipotesis pra-registrasi
  terpisah dengan ambang lock masing-masing (preseden H1/H2 Batch-1).

**Alasan satu paragraf:** S6 mengikat "klaim sel mana pun wajib koreksi
multiplicity bernama" dan lock mengunci "kuartil-atas ATR & sesi" tanpa
menetapkan kardinalitasnya, sehingga tanpa grid tertutup pelaksana bisa
mengukir sel sampai ada yang lolos (cell-carving); 4 sel =
satu-satunya bacaan harfiah "kuartil-atas x 4 sesi" pada satu famili
level primer, dengan komparator yang memang ada untuk famili itu
(placebo_acak hanya dibangun untuk round_xx00 + hl_broker), dan Holm
dipilih karena mengontrol FWER tanpa asumsi independensi antar-sel
sesi yang jelas berkorelasi; median untuk EV-H4 mengikuti S2(a) H2.

## Q3. PUTUSAN: otoritas biaya = by_session 4b; satuan JPY; fallback Off; by_year/stress-band DILARANG (DIPUTUS)

**Putusan:**

- **Otoritas biaya satu-satunya = `cost_basis.by_session`** (London
  0.61 / NewYork 0.69 / Tokyo 0.62 / Sydney 0.8 pip) + `default` 0.65
  untuk label "Off" (preseden Q2(e) H2) + `pip_size` 0.01
  (configs/data.yaml, S0). EV dalam JPY = harga_exit - harga_entry -
  cost_JPY.
- **`by_year` dan `stress_bands` DILARANG dipakai** untuk EV penentu
  (alasan: memilih basis biaya per tahun setelah melihat tahun
  evaluasi = shopping-biaya; S5 menyebut "`cost_basis` fragmen 4b"
  yang dipakai H2 = by_session).
- **Label sesi = kolom beku `session_label` store M15** untuk bar M15
  (H4); untuk bar M1/M5 (pola H4, event H5) = derivasi runtime resep
  beku SESSION_SPECS + SESSION_PRIORITY (fingerprint S0), read-only,
  dengan assert fingerprint cocok sebagai gate (GAGAL-eksekusi bila
  mismatch).
- **Satuan terkunci:** pip untuk biaya; JPY (harga) untuk EV/ATR/SL/TP;
  assert paritas satuan (preseden B1-3).

**Alasan satu paragraf:** lock + S5 menetapkan "cost_basis fragmen 4b"
tanpa memilih cabangnya, dan H2 telah mengunci bacaan by_session
(median strata-A per sesi, cocok <0,02 dengan p95-M4) yang lolos
re-audit nilai-per-nilai; mengganti cabang biaya per batch/jam/tahun
akan menggerakkan EV tanpa mengubah pasar -- shopping, maka cabang
dikunci di sini identik H2 sebelum satu pun angka Batch-2 dihitung.

## Q4. PUTUSAN: strategi diagnostik H4 pra-registrasi kata-per-kata; larangan tukar jam-tetap <-> top-6 (DIPUTUS)

**Putusan: strategi final (TERTUTUP -- satu strategi, tanpa varian):**

> Strategi "H4 sesi-pintu" (LONG-ONLY, tanpa tesis arah).
> Universe: bar M15 processed 2024/2025 + join posisional ke features
> store beku (gate: n sama + sekuens date_broker/hour_utc identik +
> sha S0; mismatch = GAGAL-eksekusi).
> (a) Bar sinyal: bar M15 yang buka tepat pada HH:00 UTC untuk
> HH dalam [14,13,0,15,12,7] (6 bar/hari; tanpa filter close>open --
> H4 tidak punya tesis momentum; memakai filter H2 = mencemari H4
> dengan H2).
> (b) Entry long pada close bar sinyal; 1x per jam-tetap per
> hari-broker; bar tak ada (gap) = jam itu FLAT, dilaporkan
> (bukan dibuang diam-diam).
> (c) ATR = `atr_14_d1` hari T-1. SL = entry - 1x ATR;
> TP = entry + 2x ATR (JPY). Monitoring mulai bar berikutnya.
> (d) Exit: (i) low <= SL -> exit SL; (ii) else high >= TP -> exit TP;
> (iii) else close bar M15 terakhir hari T -> time-stop. Prioritas
> intra-bar SL > TP (preseden H2; tanpa data intrabar pilih yang
> merugikan strategi). TIDAK ada signal-exit (tanpa tesis arah,
> tidak ada "kegagalan momentum" yang didefinisikan).
> (e) Biaya = `cost_basis.by_session[session_label(bar entry)]`
> (Off -> default 0.65) x 0.01. EV (JPY) = exit - entry - cost.
> Fill exact, tanpa slippage di luar cost_basis (preseden H2).
> (f) Posisi tumpang-tindih antar jam-tetap DIIZINKAN, dibukukan
> per-trade independen (tanpa agregasi portofolio/compounding).
> Tanpa pengecualian hari (karantina/gap-flag/anomali-C tetap
> diperdagangkan; overlay dilaporkan deskriptif).

**Larangan tukar (mengikat):** uji EV memakai HANYA 6 jam tetap
di atas (S5: "EV memakai 6 jam tetap"); uji pola memakai HANYA 6 jam
teratas hitung-ulang OOS (S5: "uji pola OOS memakai 6 jam teratas
hitung-ulang"); menukar keduanya ke arah mana pun (trading top-6
rekomputasi, atau menilai pola pada jam tetap) = shopping-jam,
GAGAL total. Kedua uji "dicatat terpisah" (S5).

**Alasan satu paragraf:** lock memerintahkan "EV-after-cost per jam
masuk" tanpa mendaftarkan rule entry/exit, dan S5 memisahkan EV-jam-tetap
dari pola-hitung-ulang justru untuk mencegah desain-menyesuaikan-data;
strategi di atas adalah bacaan minimal yang setia pada keduanya
(mesin H2 yang sudah lolos re-audit, dikurangi filter arah yang milik
H2, bukan H4), dikunci kata-per-kata sebelum eksekusi sehingga statusnya
pra-registrasi murni seperti Q2 Batch-1.

## Q5. PUTUSAN: placebo PERSIS nb04; spread M1 langsung; kuartil expanding blok-tahunan; grain tunggal hari-broker (DIPUTUS)

**Putusan:**

- **Placebo PERSIS nb04 (verbatim S0, TERTUTUP):** M5; ATR(14) D1/M5
  `.shift(1)`; theta = 0.5 x ATR; event round_xx00 grid 0.5
  (`low <= L <= high`, direction `sign(close_{t-1}-L)`, lewati == 0);
  ambang through/away `L -/+ d*theta`; pindai bar t+1..t+24;
  klasifikasi tie-bila-bar-sama / away-dulu / through-dulu / none
  (S `_build_eda04.py:738-774`); denom = away+through; hit = away/denom.
  Placebo_acak: `L' = L + U(5,25) pip`, tanda acak per event, stream RNG
  sendiri seed 20261006, cari-maju bar penyentuh-genuine s/d 24,
  buang direction==0, retensi dilaporkan (preseden keterbatasan nb04).
  Dua stream RNG terpisah, keduanya seed 20261006 (verbatim nb04).
  Penyimpangan satu konstanta pun = GAGAL-eksekusi.
- **Spread dibaca langsung dari `spread_pips` M1** (doktrin D0, B1-1):
  dipakai untuk (i) penetapan sesi-eksklusif event? TIDAK -- sesi dari
  label; (ii) audit biaya deskriptif per sel (mean spread_pips M1 pada
  bar event vs cost_basis yang dipakai -- konteks M4, non-penentu).
- **Kuartil expanding blok-tahunan (ASUMSI spec):** cutoff_2024 =
  kuantil-0,75 `atr_14_d1` harian 2023 (dari features store beku, satu
  nilai per hari-broker = nilai bar pertama hari itu; assert
  konstan-dalam-hari); cutoff_2025 = kuantil-0,75 atas 2023-2024.
  Hari T Q4 bila `atr_14_d1(T-1) > cutoff_tahun(T)` (strict; tie jatuh
  ke Q3 -- didokumentasikan). Rasional: bacaan paling ketat dari
  "kondisioning kuartil-atas" tanpa kebocoran masa depan (preseden
  expanding-median H1); blok-tahunan (bukan per-hari expanding) agar
  dapat diaudit dalam satu tabel.
- **Grain tunggal hari-broker; `utc.normalize()` DILARANG**
  (preseden adjudikasi C). Hari event = date_broker kalender D1;
  bootstrap berunit hari-broker. R1/R2 lock H1 mengikat untuk label
  hari-UTC sekunder -- yang tidak dipakai di batch ini.

**Alasan satu paragraf:** lock menulis "PERSIS" dan "seed 20261006"
agar kontrol Batch-2 komparabel dengan temuan negatif Q6, sehingga
setiap "perbaikan" protokol (window lain, offset lain, seed lain)
adalah hipotesis baru, bukan ulangan; kuartil-nya pun harus expanding
karena cutoff full-sample mengandung masa depan (pelajaran ex-post
H1 L3-01), dan blok-tahunan dipilih atas per-hari expanding murni
demi auditabilitas dengan kehilangan ketajaman yang dinyatakan
eksplisit di sini, bukan disembunyikan.

---

## Uji S-H4 -- Sesi-pintu: pola OOS + EV-after-cost

### Proposal Uji (S21)

**Apa yang diuji:** apakah konsentrasi sesi (M2) bertahan OOS dan
apakah 6 jam masuk menghasilkan EV positif setelah biaya (bukan mencari
jam "lebih baik" -- shopping-jam DILARANG; H4 = klaim kapasitas-rendah
atas jam pra-terkunci).
**Hipotesis:** H0 = gugur (salah satu ambang lock terpenuhi);
H1 = tahan (keduanya negatif).
**Populasi terkunci:** (pola) seluruh bar M1 date_broker 2024-2025
(tanpa eksklusi strata/anomali; n hari anomali-C dilaporkan);
(EV) strategi Q4 pada M15 2024-2025, pool tunggal.
**Baseline (dihitung DULU, ditempel):** P0 = top-6 + n_Off + massa
London+NY + ranking mean|r| sesi versi EDA (lock `:113-119`:
[14,13,0,15,12,7], 0, 0,7827, 1,666/1,439/1,196/1,139) sebagai jangkar
komparabilitas; E0 = deskriptif pra-EV (n hari, n jam-FLAT, n trade,
n exit per jenis, n trade hari-karantina/gap/anomali, join-gate).
**Estimasi biaya:** komputasi read-only menit; nol perubahan repo (C2).
**Rencana:** P0 (jangkar) -> P1 (top-6 hitung-ulang + kriteria-a) ->
E0 (provenans) -> E1 (median EV + kriteria-b) -> GUGUR/TAHAN.
**Status:** BELUM DIUJI.

### Metrik + ambang (pra-registrasi; dilarang tambah pasca-hoc)

- **Kriteria (a) -- penentu (lock verbatim `:124-125` + resep M2 S0).**
  Resep kanon M2 dijalankan persis pada M1 2024-2025 pool:
  mean(`abs_r_pips`) per hour_utc, rank desc, head 6; label sesi resep
  beku (derivasi runtime + assert fingerprint); hitung n_Off.
  **GUGUR bila n_Off >= 2.**
- **Kriteria (b) -- penentu (lock verbatim `:124-125` + Q4).**
  Median EV-per-trade-after-cost (JPY, definisi Q4(e)) atas SELURUH
  trade pool 2024-2025. Deskriptif wajib: n, mean, % positif.
  **GUGUR bila median <= 0** (median per S2(a) H2 -- ASUMSI spec).
- **Hasil:** GUGUR (salah satu terpenuhi) / TAHAN (keduanya negatif).
- **Suplemen (dilaporkan, BUKAN penentu):** top-6 per tahun + agreement
  vs pool; massa London+NY share pool; ranking mean|r| sesi pool;
  median EV per tahun + per jam-tetap; kurva ekuitas kumulatif
  deskriptif (tanpa ambang drawdown -- itu milik H3 yang GUGUR).

---

## Uji S-H5 -- Reaksi level pada Q4-ATR x sesi vs placebo

### Proposal Uji (S21)

**Apa yang diuji:** apakah hit-rate level melampaui placebo pada
sub-populasi volatilitas-tinggi per sesi (bukan menguji ulang agregat
Q6 -- agregat sudah negatif dan final; bukan mencari famili level yang
"lebih baik" -- shopping-famili DILARANG).
**Hipotesis:** H0 = gugur (keempat sel gagal); H1 = tahan (>= 1 sel
positif-Holm).
**Populasi terkunci:** event round_xx00 M5 2024-2025 pada hari Q4
(Q5: atr T-1 > cutoff tahunan); placebo_acak atas event yang sama
(Q5 PERSIS); 2026 dikecualikan penuh; 2023 hanya untuk cutoff.
**Baseline (dihitung DULU, ditempel):** B0 = angka agregat Q6 EDA
(real 0,469-0,490; acak 0,4989 [0,4831-0,5144]; hl 0,4890-0,4922)
+ retensi placebo nb04 + n event per sel pra-bootstrap, sebagai jangkar
bahwa mesin ulangan menyala dengan benar (chek kewarasan: hit HR tanpa
kondisi pada 2024-2025 DILARANG dipakai sebagai penentu -- hanya
diagnostik mesin).
**Estimasi biaya:** komputasi read-only menit; nol perubahan repo (C2).
**Rencana:** B0 (jangkar) -> B1 (4 sel + agregat: diff + CI + p) ->
Holm -> GUGUR/TAHAN.
**Status:** BELUM DIUJI.

### Metrik + ambang (pra-registrasi; dilarang tambah pasca-hoc)

- **Metrik sel (penentu; Q2).** Per sel: `diff = HR_real - HR_plac`
  (k=12, denom away+through masing-masing); CI95 + p satu-sisi dari
  bootstrap paired-day B=10.000 seed 20261006 (resample hari-broker
  dengan pengembalian; pada tiap resampel hitung kedua HR di atas
  multiset hari yang sama; p = proporsi resampel diff <= 0).
  **Sel positif bila lolos Holm alpha 0,01 atas 4 p-value.**
- **Hasil:** TAHAN (>= 1 sel positif-Holm) / GUGUR (keempatnya gagal;
  lock `:147-148`).
- **Suplemen (dilaporkan, BUKAN penentu):** agregat Q4-ALL + diff/CI;
  CI terpisah gaya-nb04 per sel (kontinuitas mesin); k=6/24 per sel;
  n/tie/none/retensi per sel; mean spread_pips M1 bar event per sel
  vs cost_basis (konteks M4); n hari Q4 per tahun + nilai cutoff.

---

## S-C. Kriteria selesai Batch-2 (mesin + output mentah)

Dokumen hasil kontrak: `coder/hasil-lapisan3-H4H5.md`
(muat tabel Klaim & Bukti S5 + semua [On] bernomor; tiap angka tertaut
ke [On]; auditor memverifikasi dengan mencocokkan ulang, bukan membaca
narasi).

| # | Syarat | Perintah mentah (jalankan, tempel output) | Pola lolos |
|---|---|---|---|
| C1 | HEAD tak berubah | `git rev-parse HEAD` | `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` |
| C2 | Nol tulis produksi + nol sentuh lindung (pola P-3: tracked-only + before/after; pola "output KOSONG" PENSIUN dan DILARANG dipakai) | SEBELUM tugas: `git status --porcelain -uall -- src/ tests/ data/ configs/ reports/eda/ <daftar-C2>` ditempel sebagai BEFORE; SESUDAH tugas: perintah sama sebagai AFTER; plus `find src tests data configs -type f -newermt "<timestamp-mulai-tugas>"` | AFTER identik BEFORE (diff ditempel; bila beda = GAGAL) DAN find kosong. Daftar-C2 (= lindung): `src/features/build_labels.py`, `src/features/build_features.py`, `tests/test_build_labels.py`, `tests/test_build_features.py`, `data/features/M15/`, `data/labels/`, `data/processed/`, `data/raw/`, `arsitek/hipotesis_lock_v1.md`, `arsitek/putusan-arsitek-B1.md`, `arsitek/putusan-arsitek-H1-H5.md`, `arsitek/spesifikasi-lapisan3-H1H2.md`, `arsitek/putusan-lapisan3-H1H2.md`, `arsitek/spesifikasi-lapisan3-H3.md`, `arsitek/putusan-lapisan3-H3.md`, `coder/hasil-lapisan3-H1H2.md`, `coder/protokol-H1-H2-H3.md`, `scripts/_build_eda04.py`, `scripts/_build_eda05.py`, `configs/data.yaml`, `reports/eda/` |
| C3 | Hash beku cocok + cost tercatat | `git hash-object` trio+D1/D2+Batch-1+nb04/nb05-builder (prefix `2561efd5` / `dc07a7e6` / `bc17e5de` / `34530854` / `399e64b3` / `ed7ac435` / `07402f40` / `fc29f6fa` / `1550209f` / `e4143132` / `641210e7` / `e29e18c7` -- S0) ; `sha256sum` D4 (`47d15c41...`) + M15 features (`cd6a85e4...`) + M1/M5 2024-2025 (`69b2c026/fce65a3a/da5e8944/a999a4bb`) + mtime tak berubah vs sebelum tugas ; `git hash-object configs/data.yaml` + tabel cost_basis S0 dicocokkan nilai-per-nilai ; assert fingerprint sesi cocok | semua cocok; cost sama persis S0 |
| C4 | Gate hijau | `pytest` penuh ; `ruff check .` ; `ruff format --check .` ; `python scripts/check_foreign_chars.py coder/hasil-lapisan3-H4H5.md` | N passed, 0 fail/skip (N dicatat) ; All checks passed ; N files already formatted ; OK asing -- masing-masing dengan rc + cakupan ditempel |
| C5 | Determinisme | harness S-H4 + harness S-H5 masing-masing dijalankan 2x, `sha256` berkas angka-hasil ditempel keduanya | kedua hash IDENTIK per harness (`cmp` IDENTIK) |
| C6 | S-H4 selesai + hasil diputus | P0 (jangkar EDA) + P1 (top-6 OOS, n_Off) + E0 (provenans + join-gate) + E1 (median/mean/n/% + per-tahun/per-jam deskriptif) ditempel [On] | GUGUR/TAHAN per S-Uji-S-H4 |
| C7 | S-H5 selesai + hasil diputus | B0 (jangkar Q6) + B1 (4 sel + agregat: diff, CI95, p, Holm) + suplemen ditempel [On] | GUGUR/TAHAN per S-Uji-S-H5 |
| C8 | Dokumen hasil final | `git hash-object coder/hasil-lapisan3-H4H5.md` SESUDAH penulisan terakhir ditempel (contoh BENAR: output hash; contoh SALAH yang DILARANG: "pastikan hash benar" tanpa output) | hash tercatat |
| C9 | Staged = 0, tanpa commit | `git diff --cached --name-only` (harus kosong) ; `git log --oneline -1` (tetap C1) | nol staged, HEAD tetap |

Skrip analisis HANYA di `%TEMP%\opencode\l3h4h5` (tidak di-commit;
C2 menegakkan). D4/parquet di disk tidak ditimpa (sha256 + mtime
before/after identik di C3; `main()`/`write_*` DILARANG di jalur
eksekusi). Provenans WAJIB exact-comparison atau toleransi eksplisit
(P-1); sampel bersarang WAJIB estimator paired + CI selaras alpha (P-2).

---

## S-B. Batasan eksplisit (larangan bentuk-spesifik)

1. **Vonis H1/H2/H3 di batch ini DILARANG.** Ketiganya GUGUR final;
   batch ini tidak membangkitkan, menafsir-ulang, atau memakai
   hasilnya sebagai kalibrasi/konfirmasi H4/H5.
2. **Cell-carving DILARANG** -- grid H5 = tepat 4 sel Q2 + 1 agregat;
   sel tambahan (famili level lain, window lain, split kuartil lain,
   split sesi lain) DILARANG sebagai penentu maupun "konfirmasi".
3. **Hour-shopping DILARANG** -- larangan tukar Q4 mengikat dua arah;
   TAU_alt tidak ada di batch ini; threshold kuartil blok-tahunan
   bukan objek optimasi (rumus terkunci Q5).
4. **2026-smuggling DILARANG** -- 2026 tidak muncul di tabel penentu
   maupun deskriptif batch ini, dengan dalih apa pun.
5. **Threshold-peeking DILARANG** -- cutoff kuartil dari 2023(/2024)
   dihitung sekali sebelum evaluasi; cutoff full-sample/2024-2025/
   in-eval DILARANG.
6. **FDR/unadjusted-multiple-looks DILARANG** -- satu-satunya koreksi
   yang sah = Holm Q2; klaim sel tanpa Holm = eksplorasi (S6).
7. **Eksklusi buta TETAP DILARANG** -- tidak ada bar/hari/event yang
   dibuang kecuali yang ditetapkan di atas (bar-tanpa-data =
   jam-FLAT lapor-eksplisit; event direction==0 = lewati per nb04
   dan dilaporkan n-nya; burn-in ATR-warmup = min_periods verbatim
   nb04, dilaporkan).
8. **Cabang biaya selain by_session DILARANG** (Q3); satuan selain
   pip->JPY-0.01 DILARANG.
9. **Kalibrasi ulang apa pun DILARANG** (jam, offset placebo, seed,
   window, theta, grid -- semua dari lock/nb04/config ter-hash).
10. **Guard nilai-vs-diri DILARANG** (pelajaran P-1): klaim
    reproduksi/identik/join-gate WAJIB instrumen exact atau toleransi
    eksplisit.
11. **Output parsial berlabel proses-penuh DILARANG** (tahun/sel tanpa
    event tetap dilaporkan; diff atas n kecil = apa adanya).
12. **Grain selain hari-broker tunggal DILARANG; `utc.normalize()`
    DILARANG** (Q5, preseden adjudikasi C).
13. **Menyentuh file beku/lindung DILARANG** (daftar C2); pelanggaran =
    gagal total (preseden putusan fix DILARANG-1).
14. **Mengubah redaksi/ambang lock DILARANG** kecuali addendum berversi
    yang disahkan arsitek (bukan bagian batch ini).

---

## S-R. Relasi ke konsumen hilir (boleh vs dilarang pakai hasil)

| Hasil dipakai untuk | Status |
|---|---|
| Vonis H4 dari S-H4 (GUGUR/TAHAN) | BOLEH (satu-satunya sumber vonis H4) |
| Vonis H5 dari S-H5 (GUGUR/TAHAN) | BOLEH (satu-satunya sumber vonis H5) |
| Anotasi: P0/E0/B0 sebagai jangkar komparabilitas mesin | BOLEH (preseden M1-Uji-1) |
| Keputusan arsitek tahap berikut atas dasar kedua hasil | BOLEH |
| Vonis silang H4<->H5 (pola/EV vs placebo butuh desain independen -- sudah independen di sini) | DILARANG |
| Mengubah ambang/threshold/cabang-biaya apa pun berdasarkan hasil | DILARANG (optimasi-dari-data) |
| Membuang bar/hari/event/flag/kolom dengan alasan hasil apa pun | DILARANG |
| Memakai S-H4 sebagai kalibrasi jam / S-H5 sebagai daftar level tradable | DILARANG |
| Membangkitkan H1/H2/H3 dari hasil batch ini | DILARANG |

---

## Self-audit 1x

1. Tidak ada instruksi eksekusi selain perintah verifikasi C1-C9;
   tidak ada vonis H4/H5 di spec ini (hasil = GUGUR/TAHAN milik coder +
   putusan terpisah); tidak ada perubahan kode/data/ambang (ambang
   kuartil adalah prosedur kondisioning dari lock "kuartil-atas",
   bukan ambang baru -- nilainya dihitung saat eksekusi dari rumus
   terkunci).
2. Setiap ambang penentu tertaut ke lock (kriteria H4 `:124-125`;
   kriteria H5 `:147-148`; S5/S6 putusan `:18-21`) atau dilabel ASUMSI
   dengan rasional (median-EV, Holm-0,01, diff-bootstrap-paired,
   kuartil-blok-tahunan, cutoff-strict, fallback-Off, tanpa-min-n,
   tanpa-koreksi-antar-(a)(b)) -- tidak ada angka dari data evaluasi
   (OOS 2024-2025 BELUM disentuh batch ini).
3. Q1-Q5 semuanya diputus eksplisit dengan alasan satu paragraf
   masing-masing di atas.

**Putaran adversarial (cek sendiri sebelum serah):**
- *Correctness.* Sitiran S0: lock H4 `:104-126` (redaksi, basis,
  uji, ambang) + H5 `:129-148`; putusan H1-H5 `:18-21` (S5/S6);
  report `:36-48` (Q2/Q3/spread), `:68-76` (Q6), `:99-125` (spread,
  sintesis H4/H5, catatan jujur M4), `:127-132` (T-01); nb04
  `_build_eda04.py:158-180,263-265,562-668,690-810,820-959`
  (konstanta + event + klasifikasi + placebo); M2
  `_build_eda05.py:814-859`; sesi `build_features.py:72-89`;
  cost `configs/data.yaml` (by_session + default + pip_size);
  sha D4/M15/M1/M5 + hash 12 berkas -- semua diukur sesi ini.
  Path + baris diverifikasi ulang sesi ini -- path pindah atau baris
  geser akan tertangkap C3/hash.
- *Bias & Asumsi.* Tidak ada ambang baru yang diselipkan -- kriteria
  penentu verbatim lock; ASUMSI hanya menutup titik yang lock tidak
  menetapkan bentuk operasionalnya (bentuk EV-H4, koreksi bernama,
  estimator diff, rumus kuartil, cabang biaya, fallback Off, aturan
  OR-gugur), masing-masing dengan rasional + preseden Batch-1.
  Q4 tidak mengandung konflik kepentingan: OOS 2024-2025 belum
  disentuh sehingga strategi diagnostik tak dapat menyesuaikan hasil;
  ekonomika mesin identik H2 (SL 1x/TP 2x, by_session, prioritas
  SL>TP). Bacaan yang DITOLAK dan alasannya: mean-EV (ditolak --
  S2(a) mengunci median); FDR (ditolak -- S6 + korelasi antar-sel);
  sel-hl/xx50 (ditolak -- komparator tak sebanding + shopping);
  k=6/24 penentu (ditolak -- primer nb04 = 12); cutoff full-sample
  (ditolak -- kebocoran masa depan, pelajaran L3-01); 2026 deskriptif
  (ditolak -- smuggling, preseden H2); signal-exit H4 (ditolak --
  tanpa tesis arah, tak terdefinisi).
- *Meta.* Spec mandiri (seluruh konstanta verbatim di dalam; merujuk
  file:baris terverifikasi, bukan parafrasa). Ruang putusan nyata
  arsitek terpakai: Q1 (pool-tunggal + 2026-dibuang-penuh, menolak
  uji-per-tahun), Q2 (grid-4 + Holm + OR-gugur-tanpa-koreksi, menolak
  FDR dan cell-carving), Q3 (by_session-saja, menolak cabang biaya
  lain), Q4 (strategi tanpa-filter-arah + larangan-tukar, menolak
  daur-ulang filter H2), Q5 (kuartil-blok-tahunan + diff-paired,
  menolak cutoff-full-sample dan CI-terpisah-sebagai-penentu).
  Pelajaran Batch-1 tercakup bentuk-spesifik: P-1 (larangan 10 +
  C5/C3 exact), P-2 (paired-day + Holm selaras alpha 0,01),
  P-3 (C2 tracked-only + before/after; pola KOSONG dipensiunkan
  eksplisit), burn-in/warmup lapor-eksplisit (ATR min_periods,
  jam-FLAT, direction==0), ANOMALI-style eskalasi (join-gate/fingerprint
  mismatch = GAGAL-eksekusi STOP).
