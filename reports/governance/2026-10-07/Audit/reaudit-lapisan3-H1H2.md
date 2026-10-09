# Re-audit Lapisan 3 Batch-1 -- S-H1 + S-H2 (Auditor)

**Peran:** Auditor (`.ai/AGENTS.md` v3.0 S26: verifikasi adversarial +
self-audit; DILARANG menulis kode produksi/implementasi). **Bukan vonis
H1/H2** -- dokumen ini menilai eksekusi terhadap spec, bukan menetapkan
vonis hipotesis. **Bukan audit ulang H3/H4/H5.**
**Tanggal:** 2026-10-09. **HEAD (terukur sesi ini):**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
**Dokumen yang diaudit (baca utuh, hash diukur sendiri):**
`arsitek/spesifikasi-lapisan3-H1H2.md` (369 baris),
`coder/hasil-lapisan3-H1H2.md` (1175 baris), `arsitek/hipotesis_lock_v1.md`,
`arsitek/putusan-arsitek-H1-H5.md`, `coder/protokol-H1-H2-H3.md:37-77`,
`arsitek/putusan-lapisan3-H3.md` (P-1/P-2/P-3).

**VERDICT AUDIT: LULUS.** Seluruh C1-C9 terpenuhi; C4 (gate kode) dan C5
(determinisme) diverifikasi ulang oleh auditor sendiri; gate S1 H1 cocok
9/9 presisi penuh; S-H2 (140 trade) dan VR OOS direkonstruksi dari nol
tanpa mengimpor skrip coder dan cocok **bit-exact** pada seluruh angka
penentu. Dua catatan bertanda **MEDIUM** (DEV-B1 dan DEV-B3) tidak
membatalkan eksekusi karena terbukti non-penentu di bawah ambang.

**Aturan besi yang dipakai:** klaim tanpa output mentah = GAGAL. Dokumen
audit menang atas ringkasan bila berselisih.

---

## A. Gerbang dokumen (blok [A1]-[A4])

Hash gate wajib [A1] + hash dokumen yang diaudit. Semuanya COCOK.

```
$ git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md
  aktual = fc29f6fa3595a89b918627dbdc71cfff82d8ebed   (prompt/spec: fc29f6fa...)  COCOK
$ git hash-object reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
  aktual = 1550209f40fde7998036c51c47a3f991b898f91c   (prompt: 1550209f...)        COCOK
$ git hash-object reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md
  aktual = 9720280320dcc813d422d6f540e37847b70571ff   COCOK
$ git hash-object reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
  aktual = e8eb03daf994051600258cf412ec9e9af65d800c   COCOK
$ git hash-object reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
  aktual = bc17e5de6cfefb355fe7418acd2a3a0d8b461212   COCOK
$ git hash-object reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md
  aktual = c643c1c934055d1b85d972f4e2e2f65d8d57a69f   COCOK
$ git rev-parse HEAD
  e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169                                    COCOK
TOTAL MISMATCH = 0
```

**C8 baris terakhir dokumen hasil** [A2] (`head -n -1 ... | git hash-object --stdin`):

```
$ bash -lc "cd /d/ANN && head -n -1 'reports/.../hasil-lapisan3-H1H2.md' | git hash-object --stdin"
522c221c9d9f4ee3ad480282f13d0bf97a8942be   (baris 1175 dokumen)                 COCOK
catatan proses: percobaan pertama salah karena `git hash-object --stdin` diberi
nama file (bukan isi) sehingga menghasilkan hash lain; diulang lewat bash dan
hasilnya cocok persis. Kesalahan di sisi auditor, bukan temuan dokumen.
```

Integritas berkas hasil [A3]: 1175 baris, 59016 byte, CRLF=0 (LF=1175), tanpa BOM,
decode UTF-8 strict OK.

Status repo dan cek karakter asing [A4]:

```
$ git diff --cached --name-only
(kosong = nol staged)   jumlah staged = 0
$ git log --oneline -1
e0b2b9f feat(features): fondasi B1 TERTUTUP + governance audit (konfirmasi 3xYA)
$ git status --porcelain -uall -- reports/.../coder/hasil-...md reports/.../arsitek/spesifikasi-...md Audit/
?? reports/governance/2026-10-07/Audit/
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md
?? reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
$ venv/Scripts/python.exe scripts/check_foreign_chars.py .../hasil-lapisan3-H1H2.md
OK: 1 file discan, tidak ada karakter asing.            rc=0
$ venv/Scripts/python.exe scripts/check_foreign_chars.py .../spesifikasi-lapisan3-H1H2.md
OK: 1 file discan, tidak ada karakter asing.            rc=0
```

---

## B. Kepatuhan terhadap spec -- Q2(a)-(f) dan larangan S-B [A9]

| Pin spec (`:96-125`) | Implementasi coder | Status |
|---|---|---|
| (a) bar sinyal tutup 15:00 UTC (`time`=14:45), 1x/hari-broker | `sh2.py:194` filter `utc.hour==14 & minute==45`, `assert len(sig)==1` | COCOK |
| (b) konfirmasi `day_label` **D4 beku** T-1 == trending | `sh2.py:168` `label_shift = d4["day_label"].shift(1)` | COCOK |
| (c) entry = close bar sinyal; ATR = `atr_14_d1` hari T-1; SL=entry-1xATR; TP=entry+2xATR | `sh2.py:209-212`, ATR via `daily["atr_14_d1"].shift(1)` | COCOK |
| (d) monitoring bar berikutnya; prioritas SL > TP > sinyal; time-stop close bar terakhir | `sh2.py:213-225` (urutan SL, TP, sinyal) | COCOK |
| (e) biaya = `cost_basis.by_session[label bar entry]` x `pip_size` 0.01; EV = exit-entry-biaya | `sh2.py:226-233` | COCOK |
| (f) tanpa pengecualian hari; karantina/gap hanya deskriptif | `sh2.py:236-239` hanya menghitung, tidak membuang | COCOK |

**Titik paling rawan -- Q2(b) vs S-B.10 (kopling H2 ke H1) DIVERIFIKASI
TERBALIK.** Spec `:101-104` menyebut konfirmasi **wajib** memakai label D4
beku dan eksplisit menyebut itu **BUKAN** prosedur identifikasi real-time
uji H1; S-B.10 melarang "hasil S-H1 mengubah strategi/kalkulasi S-H2".
Kode memenuhi keduanya: `sh2.py` tidak pernah menghitung `label_rt`
(kolom real-time hanya ada di `sh1.py:284`). Auditor mengukur ulang:

```
409 hari punya bar sinyal close>open  ->  140 konfirmasi trending, 269 tanpa
D4 day_label counts: {'normal': 320, 'trending': 330, 'range': 324}
kolom D4: [day_label, london_drift_4h, london_drift_norm, gap_f2_flag,
           rv_regime_flag, quarantine_mask]   <- tidak ada kolom real-time
```

Kesimpulan: kopling DILARANG tidak terjadi; justru memakai label real-time
yang akan melanggar spec. Ini membalik asumsi awal yang mungkin mengira
sebaliknya. **TIDAK ADA TEMUAN.**

**Larangan S-B, hasil grep terhadap `sh1.py`+`sh2.py` (blok [A9]):**

```
TAU        : 0 kemunculan
rv_regime  : 0 kemunculan
rv_score   : 0 kemunculan
auc        : 0 kemunculan
youden     : 0 kemunculan
H4         : 0 kemunculan
H5         : 0 kemunculan
H3         : 5 kemunculan -- SEMUA di komentar/docstring rujukan [O8] (sh1.py:10,
             47, 48, 91, 128); nol di jalur komputasi
label_rt   : 15 kemunculan -- seluruhnya di sh1.py (klasifikasi real-time S-H1);
             nol di sh2.py
```

S-B.2 (eksklusi buta): tidak ada hari/bar dibuang; burn-in 60 S-H1
dilaporkan eksplisit (n + rentang) dan bucket tanpa-sinyal dilaporkan.
S-B.3/4 (shopping/kalibrasi): ambang H1 median expanding dan ambang EV/VR
mengikuti lock; `configs/data.yaml` hash beku tak berubah.
S-B.5 (P-1): harness memakai `np.array_equal(..., equal_nan=True)` +
`max_abs_diff` (sh1.py:218-221), bukan `isclose` default. S-B.6: R1/R2/R3
heterogen dan memang dihitung tiga estimator berbeda.
S-B.9 (grain): `broker_day` dari `prepare_bars`, tanpa `utc.normalize()`.
S-B.12: nol sentuh berkas lindung (lihat C2/C3).

---

## C. C4 -- gate kode, diulang auditor (venv kanonik) [A5]

```
$ venv/Scripts/python.exe -m pytest -q
254 passed in 20.71s                                                    rc=0
$ venv/Scripts/python.exe -m ruff check .
All checks passed!                                                      rc=0
$ venv/Scripts/python.exe -m ruff format --check .
37 files already formatted                                              rc=0
$ venv/Scripts/python.exe -m ruff --version ; python --version
ruff 0.6.9 ; Python 3.12.8
```

Nilai identik dengan klaim [O14] (254 passed, 37 files, ruff 0.6.9).
Gate memakai venv kanonik, bukan `.venv` --catalogue DEV-B5 yang dilaporkan
coder soal `.venv` tidak spoils verdict karena `.venv` memang di luar
kanonik spec.

## D. C3 -- hash beku, config, dan D4 [A6]

```
2561efd552544feeb9af0b6733711015b83f43dd  src/features/build_labels.py
399e64b372e430b6def79b4fa8324a4e8e629918  src/features/build_features.py
dc07a7e651d38f07a5cabbe4e693b10681312d25  tests/test_build_labels.py
ed7ac43520c4431519d4d7065504866ae9b3ad95  tests/test_build_features.py
bc17e5de6cfefb355fe7418acd2a3a0d8b461212  reports/.../coder/protokol-H1-H2-H3.md
345308540d27c38534b77cdcd278e32eb15735ec  reports/.../coder/laporan-final-fase1.md
07402f40478aaed9391203f5db3237d636f5a959  data/features/M15/usdjpy_m15_features.parquet
e277d67ea618cd681915ae2474f4ae9a8d349516  configs/data.yaml
47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c *data/labels/usdjpy_day_labels.parquet
32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f *data/labels/usdjpy_h2_trades.parquet
data/labels/usdjpy_day_labels.parquet | mtime=2026-10-08 15:04:01.2553716 | size=29121
data/labels/usdjpy_h2_trades.parquet  | mtime=2026-10-08 15:04:01.2553716 | size=7837
```

Tujuh prefix beku cocok; sha256 kedua D4 cocok nilai spec; mtime D4
identik dengan [O3]/[O17] (2026-10-08 15:04:01) -- D4 tidak pernah
ditimpa. `configs/data.yaml` `cost_basis` dibaca ulang nilai-per-nilai:

```
{'by_session': {'London': 0.61, 'NewYork': 0.69, 'Sydney': 0.8, 'Tokyo': 0.62},
 'default': 0.65, '_satuan': 'pip'}
pip_size: {'USDJPY': 0.01, 'default': 0.0001}
```

Cocok spec `:115-119` dan [O9].

## E. C2 -- nol tulis produksi (pola P-3: tracked-only + before/after) [A7]

```
$ diff c2_before.txt c2_after_final.txt
DIFF: IDENTIK (kosong)                     rc=0
$ cat c2_before.txt | wc -l -> 42 baris
```

`c2_before.txt`/`c2_after_final.txt` (snapshot coder sebelum/sesudah) kosong
selisihnya. Pola "output KOSONG" yang dipensiunkan P-3 **tidak** dipakai
sebagai pola lolos; yang dipakai before/after. Auditor memverifikasi
sendiri bahwa menjalankan harness 4x (bagian G) tidak menyentuh repo:

```
src/features/build_labels.py   mtime=2026-10-08 18:26:01 | 15370
src/features/build_features.py mtime=2026-10-07 22:27:02 | 15530
tests/test_build_labels.py     mtime=2026-10-08 18:30:12 | 29818
tests/test_build_features.py   mtime=2026-10-07 22:26:10 | 14177
data/features/M15/usdjpy_m15_features.parquet mtime=2026-10-07 22:07:52 | 962348
data/labels/usdjpy_day_labels.parquet        mtime=2026-10-08 15:04:01 | 29121
data/labels/usdjpy_h2_trades.parquet         mtime=2026-10-08 15:04:01 | 7837
configs/data.yaml                            mtime=2026-10-07 15:44:36 | 7320
reports/.../arsitek/hipotesis_lock_v1.md     mtime=2026-10-07 17:43:13 | 7357
reports/.../arsitek/spesifikasi-lapisan3-H3.md mtime=2026-10-08 21:45:05 | 13467
reports/.../arsitek/putusan-lapisan3-H3.md   mtime=2026-10-09 00:41:20 | 11167

$ find src tests data configs -type f -newermt "-10 menit"
(kosong = tidak ada berkas tersentuh)
```

Semua mtime mendahului mulai kerja auditor (terbaru 2026-10-09 00:41,
yaitu artefak Arsitek sebelumnya). Kode harness hanya menulis ke
`Path(__file__).with_name(...)` di dalam `%TEMP%\opencode\l3h1h2`.
`sh1.py` mengimpor `_build_daily_labels` (bukan `write_labels`) dan
`_build_daily_labels` (`build_labels.py:306-333`) tidak memuat
`to_parquet` -- larangan "main()/write_labels di jalur eksekusi" dipatuhi.

---

## F. C5 -- determinisme (4 run oleh auditor, bukan membaca log coder) [A8]

```
$ python sh1.py ; python sh1.py ; python sh2.py ; python sh2.py   (venv kanonik)
rc=0 ; rc=0 ; rc=0 ; rc=0

sha256 berkas hasil:
  41b3630c27ed1d3756c7bbe4509b2feeb18c622ca02c02300b2684ccc9f7fd77  sh1_auditor_run1.json
  41b3630c27ed1d3756c7bbe4509b2feeb18c622ca02c02300b2684ccc9f7fd77  sh1_auditor_run2.json
  c818aad30681f9629616da783671506ce16c2477c31c553ef115c3857df3b8f0  sh2_auditor_run1.json
  c818aad30681f9629616da783671506ce16c2477c31c553ef115c3857df3b8f0  sh2_auditor_run2.json

$ cmp sh1_auditor_run1.json sh1_auditor_run2.json  -> sh1 cmp: IDENTIK
$ cmp sh2_auditor_run1.json sh2_auditor_run2.json  -> sh2 cmp: IDENTIK
$ cmp sh1_hasil_run1.json  sh1_auditor_run1.json   -> sh1 coder-vs-auditor: IDENTIK
$ cmp sh2_hasil_run1.json  sh2_auditor_run1.json   -> sh2 coder-vs-auditor: IDENTIK
```

Hash auditor identik hash yang diklaim coder (`41b3630c...` / `c818aad3...`),
dan file keluaran auditor identik byte-per-byte dengan file keluaran coder.
Determinisme terverifikasi penuh, bukan dirujuk.

---

## G. Verifikasi ulang angka dari nol (tanpa mengimpor skrip coder)

### G.1 Gate S1 H1 -- reproduksi M1-INK dari D4 (blok [A10])

Auditor menghitung ulang sendiri (bootstrap day-level unpaired, B=10000,
seed=20261006, chi2 tanpa Yates) dari `data/labels/usdjpy_day_labels.parquet`:

```
n_trending        aktual=330                     O8=330                    equal=True
n_pembanding      aktual=324                     O8=324                    equal=True
median_trending   aktual=0.02948996641114935     O8=0.02948996641114935    equal=True
median_pembanding aktual=0.015065793016650224     O8=0.015065793016650224    equal=True
ci95_lo           aktual=-0.02729045556350576    O8=-0.02729045556350576   equal=True
ci95_hi           aktual=0.052787080233690914     O8=0.052787080233690914    equal=True
chi2_2xk          aktual=0.7666041417663041      O8=0.7666041417663041     equal=True
p_2xk             aktual=0.6816069745648556      O8=0.6816069745648556     equal=True
verdict           aktual='GUGUR'                 O8='GUGUR'                equal=True
checks true = 9 / 9   gate_pass = True   (dof chi2 = 2)
```

Gate S1 LULUS presisi penuh (`==`, bukan `isclose` -- memenuhi P-1).
Angka [O8] di spec `:166-170` dan di `sh1.py:49-59` identik satu sama satu.

### G.2 S-H2 -- rekonstruksi strategi Q2 dari nol (blok [A11])

Auditor membangun ulang loop strategi dari nol (dengan hitung ulang
`atr_14_d1` sendiri dari OHLC M15 per broker-day, tanpa mengimpor
`sh2.py`):

```
total trade = 140 (kode coder 140)
per tahun   = {2023: 47, 2024: 42, 2025: 51} (kode 47/42/51)
exit_type   = {'sinyal': 140}
2023 median=-0.016099999999990906 mean=-0.015248936170214115
2024 median=-0.06060000000000443  mean=-0.03138571428571253
2025 median=-0.044099999999982493 mean=-0.025492156862744062
trade tidak cocok dengan JSON coder = 0
hari di JSON coder tapi tak direkonstruksi = 0
```

Per-trade dari JSON coder diperiksa ulang (140 trade):
`EV = exit - entry - cost` cocok untuk semuanya (0 selisih > 1e-9);
`cost_jpy = cost_pip * 0.01` benar; `SL = entry - 1*ATR` dan
`TP = entry + 2*ATR` benar untuk semua; 140 hari unik; seluruh 140 trade
berbiaya `('London', 0.61)`.

### G.3 Deskriptif S0 + spot-check trade[0] (blok [A12])

```
hari-broker per tahun: {2023: 259, 2024: 260, 2025: 259} total 778
n_hari_tanpa_bar_sinyal           : 0   (klaim 0)
n_hari_bar_ada_tanpa_sinyal_entry : 369 (klaim 369; 127/125/117)
cek 0 + 369 + 269 + 140 = 778
jumlah bar sinyal dipakai : 778
```

Bucket akunting tambahan DEV-B2 (369 hari `close<=open`) terverifikasi dan
total per tahun tetap utuh -- bukan hari hilang senyap.

Spot-check trade[0] (2023-01-24), dihitung ulang dari parquet M15:

```
entry=131.065  atr_t1=2.0603571428571406  sl=129.00464285714287  tp=135.18571428571428
bar monitoring #1 (15:00 UTC): open=131.069 high=131.109 low=130.642 close=130.673
low<=sl ? False   high>=tp ? False   close<open ? True
EV = 130.673 - 131.065 - 0.0061 = -0.3981   (JSON -0.3980999999999959; beda float repr)
session_label bar 14:45 di pool: {'London': 778}
broker_day bar pertama hari: 2023-01-23 22:00 UTC -> broker_day 2023-01-24
```

Cocok [O13]. Jejak "14:45 vs 15:00" yang dibantah coder terkonfirmasi: bar
ber-label 14:45 ditutup 15:00 UTC, bar monitoring berikutnya adalah 15:00,
dan seluruh 778 hari berlabel `London` pada bar sinyal -- tidak ada fallback
"Off" (0 kejadian), sesuai asumsi biaya spec `:115-118`.

### G.4 VR OOS (blok [A13])

Resep diverifikasi ulang baris-per-baris terhadap
`scripts/_build_eda03.py:177-181,421-448` (`r = log(C_t/C_{t-1})`;
`gap = utc.diff() > 15min`; `variance_ratio` = cumsum **jumlah**
overlapping, `ddof=1`; horizon `(5,15,60)`) dan dihitung ulang dari nol:

```
n_pool=72015  n_gap_dibuang=682  n_finite=71332
VR5=1.0172182521892266   VR15=1.0236432801419544   VR60=1.0387647008498926
rata-rata = 1.0265420777270247
match dengan klaim = True  (ketiganya identik bit-per-bit)
```

Coder menyalin fungsi ini verbatim (termasuk komentar peringatan "JANGAN
pakai selisih"), tidak mengimplementasi ulang sendiri. Kode upstream
`_build_eda03.py` memang memakai TF_MINUTES yang diskalakan per time-frame
(komentar `:178-180`), cocok `> 15 menit` untuk M15.

### G.5 Suplemen S-H1 (blok [A14])

```
sign test  : n_pos=168 n_neg=143 n_zero=0 p_two_sided=0.17344255582155393
chi2 3-kolom: chi2=5.542508433280522 p=0.23601814600793775 dof=4
tabel 3-kolom: normal {57,95,80} range {63,82,93} trending {79,83,86}
R1 drift_4h : n_t=311 n_n=314 CI95=[-0.03099999999997749, 0.0589999999999975] p=0.18882820311496487 GUGUR
R2 norm/rng : n_t=311 n_n=603 CI95=[-0.040334484530474134, 0.03759738849077979] p=0.18882820311496487 GUGUR
R3 +2026    : n_t=311 n_n=314 CI95=[-0.02668182694022586, 0.05242264543726398] p=0.28950804557521426 GUGUR
agreement   : persen_sama=0.9803063457330415 n_pindah=18 n=914
crosstab    : normal{normal 281, range 2, trending 6} range{normal 9, range 305, trending 0}
              trending{normal 1, range 0, trending 310}
```

Semua identik digit terakhir dengan [O7]. Distribusi label real-time
(range 314 / trending 311 / normal 289; n_evaluable 914; share trending
79/199, 83/260, 86/259) juga cocok. Verdict formula H1 = **GUGUR** via
kriteria (i) CI95 memuat 0; kriteria (ii) p=0.1888 >= 0.01 tidak terpenuhi.

**Koreksi diri yang harus tercatat (disiplin P-1):** hitung ulang
pertama untuk ATR T-1 trade[0] memberi 2.0568571428571403 (nilai ATR "hari
T"), berbeda dari JSON coder 2.0603571428571406. Setelah penelusuran,
penyebabnya pembacaan ATR auditor yang salah -- spec `:105-106` meminta
`atr_14_d1` **hari T-1**, dan `daily.at[2023-01-23]` tepat
2.0603571428571406. Kode coder BENAR; tidak ada temuan.

---

## H. Dua catatan bertanda MEDIUM (non-penentu)

### H.1 DEV-B1 -- pembacaan burn-in 60 hari (MEDIUM, bukan penentu)

Coder membaca "60 hari riwayat" sebagai **60 posisi** hari-broker dengan
median expanding `skipna`, dan melaporkannya apa adanya termasuk fakta
bahwa ambang pertama hanya punya 46 nilai `range_atr` non-NaN
(`hasil:363`, `[O6]`). Auditor menghitung ulang **kedua** pembacaan dari
nol:

```
NaN awal range_atr = 14 (ATR warmup) | posisi pertama dgn 60 nilai non-NaN = 74

A: 60 posisi          n_non_eval=60  akhir 2023-03-24  n_evaluable=914
   label_rt={normal 289, trending 311, range 314}
   median_t=0.0290361935746169  median_n=0.013991553584495942
   CI95=[-0.02668182694022586, 0.05242264543726398] memuat 0 = True
   chi2=3.333835311042838  p=0.18882820311496487  p<0.01 = False
   VERDICT_FORMULA = GUGUR

B: 60 nilai non-NaN   n_non_eval=74  akhir 2023-04-13  n_evaluable=900
   label_rt={normal 286, trending 305, range 309}
   median_t=0.0290361935746169  median_n=0.010872941907445723
   CI95=[-0.026548072765492807, 0.05635897548118707] memuat 0 = True
   chi2=2.970237484523199  p=0.22647544687302634  p<0.01 = False
   VERDICT_FORMULA = GUGUR
```

Kedua pembacaan menghasilkan **verdict formula identik (GUGUR)**: kriteria
(i) tetap terpenuhi (CI95 memuat 0) dan kriteria (ii) tetap tidak
terpenuhi di kedua pembacaan (p ~ 0.19-0.23, jauh di atas alpha 0.01).
Burn-in dengan demikian **tidak menyentuh penentu mana pun**.

**Sikap auditor:** **TERIMA** pembacaan 60-posisi yang dipakai coder --
cukup karena non-penentu. DEV-B1 tetap dicatat sebagai **MEDIUM** untuk
Arsitek: spec `:157-159` memang tidak menyebut `min_periods` nilai, jadi
pembacaan ini sah sebagai asumsi spec, tapi ambang burn-in eventual harus
menjadi keputusan eksplisit Arsitek, bukan pembacaan yang diwariskan. Re-run
**tidak diwajibkan** (tidak ada angka penentu yang bergerak).

### H.2 DEV-B3 -- 140/140 exit "sinyal" (MEDIUM, terbukti masuk akal)

Klaim "`n_exit_SL`=0, `n_exit_TP`=0, `n_exit_time_stop`=0; 140 exit sinyal"
(A-titel [O10]) diverifikasi ulang sebagai **fakta, bukan kekeliruan**:

```
total trade = 140 ; exit_type = {'sinyal': 140} ; monitoring menyentuh SL = 0 hari
monitoring menyentuh TP = 0 hari ; exit pada bar ke-1 = 66 (47.1%)
ATR T-1 (JPY): min=0.6185 median=1.2828 maks=2.5837
jarak terdekat ke SL/TP saat exit: min=0.2606 JPY median=1.2144 JPY
(jarak dalam satuan ATR: min 0.203 median 0.947)
```

**Mekanika yang menjelaskan:** SL/TP berada >= 1x ATR dari entry, sementara
syarat exit-sinyal (`close < open`) diperiksa pada **tiap** bar monitoring
dan bar dengan close<open sangat sering (47% trade keluar di bar
monitoring pertama, yang notabene bukan SL/TP). Akibatnya harga tidak pernah
cukup bergerak 1x ATR sebelum sinyal close<open lebih dulu menyala. Ini
konsekuensi deterministik Q2(d) seperti yang dilaporkan coder, bukan bug.
Yang diperiksa auditor: (a) urutan prioritas SL>TP>sinyal benar di kode;
(b) tidak ada trade yang *hampir* menyentuh SL/TP lalu salah exited -- jarak
terdekat saat exit 0.26 JPY, jadi tidak ada trade yang terlewati SL/TP
karena bug urutan. **Tidak ada temuan.** DEV-B3 dicatat MEDIUM hanya sebagai
catatan realitas strategi (exit hampir selalu via sinyal, bukan SL/TP) --
informatif untuk Lapisan 4, tidak mencederai S-H2.

---

## I. Status akhir C1-C9 (rekap)

| # | Syarat | Status | Bukti auditor |
|---|---|---|---|
| C1 | HEAD tak berubah | LULUS | `git rev-parse HEAD` = e0b2b9f9 (Bagian A) |
| C2 | Nol tulis produksi (P-3) | LULUS | diff BEFORE/AFTER kosong; mtime + find kosong setelah 4 run (Bagian E) |
| C3 | Hash beku + cost | LULUS | 7/7 prefix; sha256 D4; cost_basis per nilai (Bagian D) |
| C4 | Gate hijau | LULUS | 254 passed / ruff check / ruff format 37 (Bagian C) |
| C5 | Determinisme | LULUS | 4 run, sha256 identik, cmp IDENTIK coder-vs-auditor (Bagian F) |
| C6 | S-H1 selesai + diputus | LULUS | gate S1 9/9; S2 verdict GUGUR; S3 suplemen; divergence Q1 searah (Bagian G) |
| C7 | S-H2 selesai + diputus | LULUS | S0 deskriptif; S1 median 3/3 <=0; S2 VR>1; verdict GUGUR (Bagian G) |
| C8 | Dokumen final | LULUS | `head -n -1` = 522c221c (Bagian A) |
| C9 | Staged=0, tanpa commit | LULUS | `git diff --cached` kosong; HEAD tetap (Bagian A) |

## J. Temuan (tidak ada yang memblokir; 2 catatan non-penentu)

- **T-0 (MEDIUM, non-penentu) -- DEV-B1 burn-in 60 posisi vs 60 nilai
  non-NaN.** Kedua pembacaan menghasilkan verdict formula identik GUGUR;
  tidak ada angka penentu yang bergerak. Sikap: terima pembacaan coder,
  putuskan ambang eksplisit di Arsitek. Tidak butuh re-run.
- **T-1 (MEDIUM, non-penentu) -- DEV-B3 140/140 exit via sinyal.** Fakta
  terverifikasi; mekanikanya dijelaskan (SL/TP >= 1x ATR, sinyal exit
  sangat cepat). Bukan bug, bukan eksklusi tersembunyi. Catatan realitas
  strategi saja.

Tidak ditemukan: pengiplian ambang, kopling H2<->H1, penggunaan filter/TAU,
kalibrasi ulang, eksklusi buta, klaim tanpa bukti, kenaikan severity
tertutup, atau pelanggaran peran. Klaim `GUGUR` pada dokumen hasil adalah
keluaran formula lock yang dihitung skrip -- **bukan vonis auditor** dan
bukan vonis resmi H1/H2, yang tetap milik Arsitek pada putusan terpisah.

---

## K. Self-audit adversarial (3 putaran)

**Putaran 1 -- Correctness.** (a) Tujuh hash + HEAD diukur sendiri, bukan
dibaca dari dokumen; C8 diverifikasi lewat `head -n -1` setelah pertama
salah cara (dicatat). (b) Gate S1, S-H2, VR, dan seluruh suplemen S-H1
dihitung ulang dari nol tanpa mengimpor skrip coder, dan cocok bit-exact
pada semua angka penentu. (c) C4/C5 dijalankan ulang auditor sendiri, bukan
rujukan. (d) Instrumen P-1 dipakai: `np.array_equal` + `max_abs_diff`, bukan
`isclose`. (e) Satu kesalahan hitung-ulang sendiri (ATR T-1) ditemukan dan
dikoreksi secara terbuka, bukan dipoles.

**Putaran 2 -- Bias & asumsi.** (a) DEV-B1 diuji dua arah (bukan hanya
menerima asumsi coder) sehingga independensi pembacaan burn-in terbukti
non-penentu. (b) DEV-B3 diuji secara kuantitatif (jarak ke SL/TP saat exit)
untuk menyingkirkan kemungkinan bug urutan prioritas, bukan sekadar menerima
narasi "konsekuensi mekanis". (c) Q2(b) diuji terbalik (apakah kopling
terjadi) dan hasilnya justru membuktikan kepatuhan. (d) Tidak ada temuan
baru yang muncul dari spec -- spec menang dalam semua benturan yang diuji.

**Putaran 3 -- Meta-check.** (a) Peran dipisah: auditor tidak menulis kode
produksi, tidak memvonis H1/H2, tidak mengubah ambang. (b) Dua catatan
MEDIUM tidak menaikkan severity temuan tertutup H3 (F-3/F-4/F-5 tetap
LOW, Uji-1 IMMATERIAL tetap). (c) Verdict LULUS diberikan berdasarkan C1-C9
+ verifikasi ulang, bukan karena "tidak ada yang salah" -- dua catatan
dicatat eksplisit beserta buktinya. (d) Sikap terhadap DEV-B1 dan DEV-B3
disarankan sebagai keputusan Arsitek, bukan keputusan auditor.

## L. Batasan audit ini (jujur)

1. Auditor memverifikasi eksekusi terhadap spec dan lock, bukan underlying
   hipotesis H1/H2 secara substantif (mis. apakah H2 layak diuji lagi) --
   di luar mandat.
2. Data_store/D4 berakhir 2026-10-02; S-H1 evaluable mencakup 2026
   parsial (dilaporkan per tahun), S-H2 hanya 2023-2025. Tidak ada klaim
   di luar cakupan itu.
3. Re-run harness memakai venv kanonik (numpy 1.26.4 / pandas 2.2.3 /
   scipy 1.17.1) yang sama dengan meta JSON; determinisme lintas versi
   lain tidak dijamin (di luar scope C5 yang meminta 2x pada env sama).
4. Secara independen, spec tidak menyatakan `min_periods` untuk median
   expanding, sehingga DEV-B1 adalah ketiadaan spesifikasi, bukan
   pelanggaran -- itu sebabnya MEDIUM dan bukan HIGH.