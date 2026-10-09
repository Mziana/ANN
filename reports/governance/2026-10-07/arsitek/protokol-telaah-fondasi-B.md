# Protokol Arsitek -- Telaah Fondasi Opsi B (Diagnostik, BUKAN Vonis Ulang)

**Peran:** Arsitek (AGENTS.md S26-S27: merancang + memutus; DILARANG
menulis/mengubah kode produksi, data, config). **BUKAN coder**
(eksekusi = ronde coder terpisah), **BUKAN auditor, BUKAN asisten.**
**Tanggal:** 2026-10-09. **HEAD sesi ini:**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
**Konteks:** Batch-2 TERTUTUP 2026-10-09 (H4 TAHAN, H5 GUGUR telak;
H1/H2/H3 GUGUR). EKS-3 tercatat: median EV pool H4 +0,0144 tipis,
tanda tahun terbelah (2024 +0,048 / 2025 -0,005).
**Tugas ronde ini:** uji apakah kegagalan & ketipisan itu artefak
fondasi (data/biaya/regime) atau vonis informatif. Keluaran =
protokol diagnostik + rekomendasi cabang. **Vonis H1-H5 TETAP dan
tidak disentuh dalam bentuk apa pun oleh dokumen ini.**
**Lingkup TERTUTUP:** U-1, U-2, U-3 + rekomendasi cabang. DILARANG
merumuskan H6. DILARANG commit/push.
**Aturan besi: tiap klaim angka WAJIB ditempel output mentahnya --
klaim tanpa output mentah = GAGAL (AGENTS.md S5).**

---

## S0. Gerbang hash + Klaim & Bukti sesi ini

Hash diukur sesi ini dengan `git hash-object` + `git rev-parse HEAD`
SEBELUM satu butir pun dirancang:

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  arsitek/spesifikasi-lapisan3-H4H5.md
f06a8e27b916172f5824438acd545614360d3b57  coder/hasil-lapisan3-H4H5.md
8a4d21090f27dd53555b3a12583ec337819efb2f  Audit/reaudit-lapisan3-H4H5.md
e02a203b96879d73e90339f2d78a37d15834a23a  arsitek/putusan-lapisan3-H4H5.md
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD
```

Staged = 2 berkas T6 (`src/features/build_labels.py`,
`tests/test_build_labels.py`) -- sesuai brief; worktree selebihnya
tak tersentuh sesi ini. Hash pendukung (diukur sesi ini):
`putusan-arsitek-F1.md = 746052b0256b36e088acb213e45c1f455b690795`,
`rencana-B2-fase0.md = 009ae48df1253bfc7d035df801419bd148d50ace`,
`configs/data.yaml = e277d67ea618cd681915ae2474f4ae9a8d349516`,
`src/features/build_labels.py = 2561efd552544feeb9af0b6733711015b83f43dd`
(dua terakhir cocok read-proof Batch-2).

| Klaim | Status | Bukti |
|---|---|---|
| 4 blob + HEAD cocok brief S-2d | TERVERIFIKASI | `git hash-object` + `git rev-parse` sesi ini |
| H4 eksekusi = varian INKLUSI (masker hanya counter) | TERVERIFIKASI | `sh4.py:369-375` (baca sesi ini); tanpa filter/drop di seluruh skrip |
| 19 hari F-1 eksplisit; H1-2023 dikecualikan | TERVERIFIKASI | `build_labels.py:53-56,228-242`; `data.yaml:184-198`; `rencana-B2-fase0.md:75-90`; `putusan-arsitek-F1.md:31-33,80` |
| Definisi EV + biaya per sesi | TERVERIFIKASI | `hasil:93` (manifest biaya), `hasil:410` (definisi EV) |
| Rasio vol/spread M4 lock | TERVERIFIKASI (rujukan) | lock `:140-141` (ter-hash `97202803`) |
| Regime spread H1-2023 vs H2-2023 | TERVERIFIKASI (rujukan) | `report.md:43` (ter-hash `15ecb37d`) |
| Larangan filter regime mengikat | TERVERIFIKASI (rujukan) | `putusan-lapisan3-H3.md:141` (ter-hash `c643c1c9`) |
| Tanpa tulis repo oleh sesi ini | TERVERIFIKASI | kecuali berkas protokol ini; tanpa commit/push |

---

## U-1. Sensitivitas H4 vs karantina F-1 (DIRANCANG)

**(a) Varian yang dieksekusi -- ditetapkan dari kode sesi ini.**
`sh4.py:369` membaca `d4.at[day, "quarantine_mask"]` HANYA untuk
counter deskriptif (`:374-375` `if bool(dq):
counter["n_trade_hari_karantina"] += 1`); tidak ada filter, drop,
atau cabang eksklusi di seluruh 483 baris skrip. Populasi P1
(`:187` "tanpa eksklusi strata/anomali") dan pool E1 mencakup
penuh 3114 trade termasuk 30 trade hari-karantina, 636
gap-flag, 30 anomali-C ([O8]). **Varian tereksekusi = INKLUSI.**
Fakta aritmetika: dari 19 hari F-1 (`build_labels.py:53-56` =
`2024-10-28..11-01` + `2026-03-10..03-27`), yang overlap jendela
evaluasi 2024-2025 hanya 5 hari pertama (14 hari 2026 di luar
eval); 5 hari x 6 jam = 30 trade karantina di pool -- cocok
`n_trade_hari_karantina = 30` ([O8]).

**(b) Prosedur hitungan varian EKSKLUSI (ronde coder).** Input beku:
parquet M1 2024-2025 (`69b2c026`/`fce65a3a`), M15 store
(`cd6a85e4`), D4 (`47d15c41`), `ANOMALY_WINDOWS`
(`build_labels.py:53-56`), `quarantine_mask()`
(`build_labels.py:228-242`), konstanta Q3/Q4 spec Batch-2
(identik S-H4: jam tetap, ATR T-1, SL 1x/TP 2x, biaya by_session).
Langkah: (1) bangun ulang pool H4 PERSIS S-H4 (resep `sh4.py`);
(2) varian INKLUSI direplikasi (cek kesamaan median pool
`0.014399999999998407` digit-per-digit -- gate kewarasan);
(3) varian EKSKLUSI: buang 5 broker_day karantina dalam-jendela
(`2024-10-28..2024-11-01`) dari pool M1 P1 DAN pool M15 E1,
hitung-ulang top-6 M2 + `n_Off`/any_off/maj_off + median EV pool
+ median per-tahun + n trade; (4) tulis JSON artefak kedua varian
+ tabel selisih digit-per-digit (inklusi vs eksklusi).
DILARANG eksklusi buta di luar 19 hari F-1 (H1-2023 BUKAN objek:
`putusan-arsitek-F1.md:31-33,80`). DILARANG menukar daftar jam
(larangan Q4 dua arah tetap berlaku pada kedua varian).
Perintah mentah WAJIB ditempel coder: (i) `grep anomaly_windows`
pada `configs/data.yaml` (blok `:184-198`); (ii) `git hash-object`
tiap artefak JSON yang diklaim; (iii) sha256 tiap parquet yang
dipakai; (iv) cetak 5 tanggal karantina dalam-jendela yang
dibuang + cacah trade terbuang (harus 30).

**(c) Aturan baca TERTUTUP.** Dilaporkan: apakah median 2025
membalik tanda (negatif -> non-negatif) atau tidak; selisih median
pool inklusi-vs-eksklusi angka; `n_Off` kedua varian. Kedua hasil
dicatat apa adanya. **Vonis H4 TETAP TAHAN apa pun hasilnya** --
ini diagnostik fondasi, bukan vonis ulang (P-5 putusan H4/H5
mengikat).

---

## U-2. Dekomposisi biaya H4 + H5 (DIRANCANG)

**Definisi yang dipakai (tunggal, dari hasil beku):** EV JPY =
exit - entry - cost_jpy; cost_jpy = cost_basis.by_session
(Off -> default 0.65) x pip 0.01; fill exact tanpa slippage
(`hasil:410`); biaya per sesi London 0,61 / NewYork 0,69 /
Tokyo 0,62 / Sydney 0,8 (`hasil:93`; `data.yaml` cost_basis).
Kaki bruto per trade = exit - entry; kaki biaya = cost_jpy.

**Prosedur (ronde coder).** H4: dari 3114 trade pool (`sh4_hasil.json`
ter-hash `b1b69d33`), urai per sesi (London/NewYork/Tokyo/Sydney/Off):
n trade, mean/median kaki bruto, mean/median kaki biaya, mean/median
EV, porsi biaya = mean(kaki biaya) / mean(|kaki bruto|) + porsi
terhadap median pool +0,0144. H5: per sel (London/Tokyo/NewYork/Sydney)
laporkan cost_basis pip sel + `mean_spread_pips_m1_bar_event` sel
(sudah di JSON `7a7f5ee7`) + rasio vol/spread M4 lock (London 2,08 /
Tokyo 1,60 / NewYork 0,95 / Sydney 0,80; flag biaya-mendominasi =
[NewYork, Sydney], lock `:140-141`) disandingkan dengan diff/CI95/p
sel (`hasil [O13]`). Tanpa statistik keputusan baru -- tanpa
ambang, tanpa uji, tanpa peringkat sel.

**Aturan baca TERTUTUP.** Ini KUANTIFIKASI headwind biaya, BUKAN
jalur penyelamatan: gap Holm H5 (p terkecil 0,244 vs ambang pertama
0,0025) berorde magnitude -- tidak ada porsi biaya yang dapat
menutupnya, dan P-5 putusan H4/H5 mengikat (kegagalan H5 DILARANG
ditafsir-ulang pasca-hoc; ketipisan H4 DILARANG dibaca sebagai
ruang kalibrasi biaya). Keluaran = tabel per-nilai + kalimat
"biaya menjelaskan X dari Y", bukan rekomendasi ubah biaya
(by_session beku; S-B.8).

---

## U-3. Cek regime deskriptif 2024 vs 2025 (DIRANCANG)

**Prosedur (ronde coder).** Deskriptif saja dari data beku
(M1 2024-2025 `69b2c026`/`fce65a3a`, M15 store `cd6a85e4`):
per tahun 2024 vs 2025 -- spread p95 + mean M1 (kolom
`spread_pips` beku), level RV (kolom store beku), jumlah bar/trade
-- disandingkan dengan split tanda H4 (median EV 2024 +0,04835
vs 2025 -0,00505, [O8]). Grain = `date_broker` store; DILARANG
rekonstruksi grain dari UTC (`utc.normalize()` DILARANG, S-B.12).
Acuan konteks (bukan filter): H1-2023 (B) spread p95 5,30 vs
H2-2023 (A) 0,60 = 5,3x (`report.md:43`).

**Larangan eksplisit (mengikat, putusan H3):** DILARANG mengaktifkan
`rv_regime_flag`/`rv_score`/TAU sebagai filter pada data mana pun
(`putusan-lapisan3-H3.md:141`). DILARANG kalibrasi-ulang ambang apa
pun. DILARANG menambah kolom/menulis store.

**Aturan baca TERTUTUP.** Keluaran = SATU dari dua kalimat:
"bertepatan" (2025 rezim biaya/vol berbeda searah dengan
pembalikan tanda) atau "tidak bertepatan" -- keduanya deskriptif,
bukan vonis, tanpa konsekuensi pada H4 TAHAN. Bila "bertepatan",
rekomendasi BUKAN filter, melainkan cabang R-2 di bawah.

---

## Rekomendasi cabang ("jika X maka Y", tanpa vonis)

- **R-1 (dari U-1):** JIKA eksklusi 5 hari membalik tanda 2025
  (negatif -> positif) MAKA catat fondasi-H4 sensitif-karantina dan
  laporkan sebagai keterbatasan jendela (5 hari DST-belum-
  terverifikasi) pada konsumen hilir; vonis TETAP. JIKA tidak
  membalik MAKA EKS-3 ditutup sebagai noise tahunan murni.
- **R-2 (dari U-3):** JIKA "bertepatan" MAKA usul ronde desain
  berikutnya BOLEH mempertimbangkan stratifikasi tahun
  pra-registrasi (BUKAN filter regime -- filter tetap DILARANG
  tanpa spec baru + uji stabilitas yang LULUS, putusan H3:150).
  JIKA "tidak bertepatan" MAKA ketipisan H4 dicatat irreducibel
  pada fondasi terukur.
- **R-3 (dari U-2):** JIKA porsi biaya > 50% median pool H4 MAKA
  catat H4 sebagai temuan biaya-sensitif untuk desain posisi
  berikutnya (tanpa mengubah biaya beku). Untuk H5 tidak ada
  cabang aksi -- GUGUR telak final.
- **R-4 (umum):** Semua artefak JSON ronde coder WAJIB ter-hash
  (`git hash-object` ditempel) sebelum dibaca arsitek; klaim tanpa
  output mentah = GAGAL.

---

## Self-audit 3x adversarial (sebelum STOP)

**Putaran 1 -- Correctness.** (a) Hash S-2d (4 blob + HEAD) diukur
sesi ini, 5/5 cocok (S0). (b) Tiap U berpasangan sumber beku
file:baris terverifikasi-ulang sesi ini: U-1 ->
`sh4.py:369-375`, `build_labels.py:53-56,228-242`,
`data.yaml:184-198`, `rencana-B2-fase0.md:75-90`,
`putusan-arsitek-F1.md:31-33,80`; U-2 -> `hasil:93,410`,
lock `:140-141`; U-3 -> `report.md:43`,
`putusan-lapisan3-H3.md:141`, S-B.12. (c) Perintah mentah ada
untuk tiap klaim yang diminta dari coder (U-1(b)(iv), U-2 tabel
per-nilai, U-3 kolom beku). (d) Aturan baca tiap U tertutup dua
sisi hasil (U-1(c), U-2, U-3).

**Putaran 2 -- Bias & Asumsi.** (a) Tidak ada butir membuka vonis
ulang: U-1(c)/U-2/U-3 masing-masing menyatakan vonis TETAP
eksplisit. (b) Tidak ada filter/ambang baru via U-3: filter regime
dilarang kata-per-kata mengikat putusan H3; cabang R-2 hanya
stratifikasi pra-registrasi di ronde desain terpisah. (c) U-2 bukan
pintu penyelamatan H5: gap Holm orde-magnitude dinyatakan + P-5
dikutip; tanpa statistik keputusan baru. (d) U-1 tidak melegalkan
eksklusi buta: objek eksklusi dikunci 19 hari F-1 (5 dalam
jendela), H1-2023 dikecualikan eksplisit.

**Putaran 3 -- Meta-check.** (a) Lock tak tersentuh: nol redaksi/
ambang diubah; biaya by_session, seed, grid, window, Holm tetap
beku. (b) H6+ tetap DITOLAK -- tidak dirumuskan di dokumen ini.
(c) Ruang coder tidak diambil: hanya prosedur + perintah mentah +
aturan baca; eksekusi menunggu ronde terpisah. (d) STOP menutup
ronde rancang ini; protokol ini sendiri mengikuti pengganti C8
(P-4 putusan H4/H5): tanpa self-hash di dalam dokumen, hash
dilaporkan di kanal luar.

STOP. Menunggu ronde coder terpisah untuk eksekusi protokol ini.
