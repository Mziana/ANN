# Re-audit Lapisan 3 Batch-2 -- S-H4 + S-H5 (Auditor)

**Peran:** Auditor (`.ai/AGENTS.md` v3.0 S26: verifikasi adversarial +
self-audit; DILARANG menulis kode produksi/implementasi). **Bukan vonis
H4/H5** -- dokumen ini menilai eksekusi terhadap spec, bukan menetapkan vonis
hipotesis. **Bukan audit ulang H1/H2/H3.**
**Tanggal:** 2026-10-09. **HEAD (terukur sesi ini):**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
**Dokumen yang diaudit (baca utuh, hash diukur sendiri):**
`arsitek/spesifikasi-lapisan3-H4H5.md` (461 baris),
`coder/hasil-lapisan3-H4H5.md` (1299 baris), `arsitek/hipotesis_lock_v1.md`,
`arsitek/putusan-arsitek-H1-H5.md`, `coder/protokol-H1-H2-H3.md`,
`arsitek/spesifikasi-lapisan3-H3.md`, `coder/hasil-lapisan3-H3.md`,
`coder/hasil-lapisan3-H1H2.md`. Skrip coder `sh4.py` (483 baris) dan
`sh5.py` (629 baris) dibaca utuh baris-per-baris.

**VERDICT AUDIT: LULUS DENGAN TEMUAN.** Seluruh angka penentu S-H4 dan
S-H5 **direproduksi ulang dari nol oleh auditor tanpa mengimpor skrip coder**
dan cocok **bit-exact** (termasuk median EV yang hanya cocok sampai 15
digit desimal, serta keempat nilai p bootstrap). Kedua harness direplikasi
ulang dan menghasilkan artefak **byte-identik**. C1-C9 terpenuhi; 15 blob
sumber + 7 sha256 data + hash dokumen auditor ukur sendiri 100% cocok.
Enam temuan: **2 MEDIUM** (pernyataan sesi London/NewYork yang terbukti
salah, dan kontrol C8 yang sirkular) + **4 LOW** (satuan persen salah tulis,
efek batas 2023 tidak diumumkan, file log run-3 tidak diumumkan, dan dua
file produksi tidak terlacak git).
Kedua MEDIUM **non-penentu**: tidak mengubah angka penentu, tidak mengubah
formula verdict, dan tidak melanggar S-B yang berbasis hasil.
**Aturan besi yang dipakai:** klaim tanpa output mentah = GAGAL. Dokumen
audit menang atas ringkasan bila berselisih. Kesalahan di sisi auditor
dinyatakan terbuka, bukan disembunyikan (lihat bagian K).

---

## A. Gerbang dokumen (blok [A1])

Hash gate WAJIB memakai `git hash-object` (bukan sha256 mentah). Auditor
awalnya sempat salah memakai sha256 dan menyimpulkan dokumen berubah; setelah
dikoreksi ke git-blob, hash cocok persis. Kesalahan itu di sisi auditor.

```
$ git hash-object reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md
  aktual = f06a8e27b916172f5824438acd545614360d3b57   (prompt/spec: f06a8e27...)  COCOK
$ git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md
  aktual = 4a46b815211e6b0b050cbb6f3e98ce5e27904069   (prompt/spec: 4a46b815...)  COCOK
$ git rev-parse HEAD
  e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169                                     COCOK
$ git diff --cached --name-only | wc -l
  0                                                                             COCOK
$ git status --porcelain  (dokumen hasil)
  ?? reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md   (untracked, belum commit)
bytes = 50219 ; baris = 1299 ; LF-only ; endswith-LF ; pure ASCII
```

### A.1 Read-proof ulang oleh auditor (15 blob + 7 sha256)

Semua diukur ulang oleh auditor dari repo, bukan diambil dari dokumen.

```
BLOB (git hash-object)                                          hasil
spesifikasi-lapisan3-H4H5.md          4a46b815211e6b0b050cbb6f3e98ce5e27904069  COCOK
hipotesis_lock_v1.md                  9720280320dcc813d422d6f540e37847b70571ff  COCOK
putusan-arsitek-H1-H5.md              e8eb03daf994051600258cf412ec9e9af65d800c  COCOK
protokol-H1-H2-H3.md                  bc17e5de6cfefb355fe7418acd2a3a0d8b461212  COCOK
spesifikasi-lapisan3-H3.md            dacd07087f4e1f66154dcc75a259ecfcdb769043  COCOK
hasil-lapisan3-H3.md                  fd52d72242109a74bbb9a9d5425033604b04145a  COCOK
hasil-lapisan3-H1H2.md                1550209f40fde7998036c51c47a3f991b898f91c  COCOK
.ai/AGENTS.md                          4549dc1268d9d5d2caf84a058ec0951524b171ec  COCOK
scripts/_build_eda04.py                641210e72b63898aaa8d106e1a2a697901504575  COCOK
scripts/_build_eda05.py                e29e18c7eb98083ab0857eebf3c4529b8983f23e  COCOK
src/features/build_features.py         399e64b372e430b6def79b4fa8324a4e8e629918  COCOK
src/features/build_labels.py           2561efd552544feeb9af0b6733711015b83f43dd  COCOK
tests/test_build_features.py           ed7ac43520c4431519d4d7065504866ae9b3ad95  COCOK
configs/data.yaml                      e277d67ea618cd681915ae2474f4ae9a8d349516  COCOK
notebooks/scalping/_eda_common.py      2740be07fd1c9518f6753c1fd0a7ee5b0068994f  COCOK
BLOB: COCOK = 15 / 15

SHA256 DATA
data/processed/M1/usdjpy_m1_2024.parquet     69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac  COCOK
data/processed/M1/usdjpy_m1_2025.parquet     fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af  COCOK
data/processed/M5/usdjpy_m5_2024.parquet     da5e8944763202a7f6fdfc429e287b235d8b3091bf5449af61d4204ba23de3d6  COCOK
data/processed/M5/usdjpy_m5_2025.parquet     a999a4bbedd52af976d0cc2d5a0649ab00df071ade7a6bfcc44c38d527350940  COCOK
data/features/M15/usdjpy_m15_features.parquet cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb  COCOK
data/labels/usdjpy_day_labels.parquet        47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c  COCOK
data/labels/usdjpy_h2_trades.parquet         32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f  COCOK
DATA: COCOK = 7 / 7
```

### A.2 C2 -- nol tulis file produksi

```
$ (equiv find src tests data configs -type f -newermt 2026-10-09T03:11:41)
  total file dipindai (seluruh repo, excl .git/venv/cache) = 5198
  file repo LEWAT cutoff = 9
   thoughts\ledgers\CONTINUITY_ses_ef0b.md                          08:57:36
   reports\governance\...\coder\hasil-lapisan3-H4H5.md             09:05:04
   .ai\assistant\verifications\2026-10-09_gerbang-hasil-H4H5.md     09:11:34
   journal\daily\2026-10-09.md                                      09:11:43
   .ai\SESSION_LOG.md / .ai\TASKS.md / .ai\STATE.md                09:11:43
   .ai\assistant\prompts\2026-10-09_reaudit-batch2-H4H5-auditor.md  09:14:01
   thoughts\ledgers\CONTINUITY_ses_eef7.md                          09:21:09
  -> 9/9 adalah bookkeeping sesi (ledgers, .ai/, journal, prompt) + dokumen hasil.
  -> NOL file di src/ scripts/ notebooks/ tests/ data/ configs/.            LULUS
```

---

## B. R1 -- Rekomputasi S-H4 dari nol (tanpa impor `sh4.py`)

Probe auditor: `r1_top6.py` (top-6 + n_Off), `r1_ev.py` (join-gate + EV).
Resep M2 diverifikasi ulang terhadap kanonik `_build_eda05.py:814-823`
(`vol_hour = hourly.groupby("hour_utc")["abs_r_pips"].mean().sort_values(
ascending=False); top6 = head(6)`) -- identik.

```
$ venv/Scripts/python.exe %TEMP%/opencode/l3h4h5_audit/r1_top6.py
pip=0.01 cost={'London':0.61,'NewYork':0.69,'Tokyo':0.62,'Sydney':0.8} default=0.65
fingerprint_src_ok=True
sha256 m1_2024 = 69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac
sha256 m1_2025 = fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af
n_bar_pool_m1 = 715308   (klaim 715308)   COCOK
n_hari_pool_m1 = 519     (klaim 519)      COCOK

top6 hitung-ulang = [14, 13, 0, 15, 12, 1]
  klaim coder     = [14, 13, 0, 15, 12, 1]                                COCOK
  lock P0         = [14, 13, 0, 15, 12, 7]
n_Off = 0 ; share_Off = 0.0   (klaim 0 / 0.0)                              COCOK
kriteria_(a) GUGUR bila n_Off>=2 -> False

mean abs_r_pips per jam (desc): 14:2.2418878150507267 13:2.2074284436303433
0:1.9958603495949216 15:1.9544640745309416 12:1.927724758070991
1:1.8656446453129658 7:1.8623607812964862 6:1.7390643676434798

distribusi session_label per jam dalam top-6 hitung-ulang:
  hour_utc  London  NewYork  Tokyo
   0            0         0   31133
   1            0         0   31138
  12        31133         0       0
  13        31130         0       0
  14        31134         0       0
  15        13139     17999       0
share_LondonNY_massa_top6 = 0.6832894546066546  (klaim 0.6832894546066546)   COCOK
```

### B.1 Join-gate (R1c)

```
$ venv/Scripts/python.exe %TEMP%/opencode/l3h4h5_audit/r1_ev.py
sha256 m15_features = cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb
n_bar_pool_m15   = 47721   (klaim 47721)   COCOK
n_bar_store_pool = 47721   (klaim 47721)   COCOK
n_sama                        = True   COCOK
sekuens date_broker identik  = True   COCOK
sekuens hour_utc identik      = True   COCOK
ATR daily_metrics.shift(1) == store (exact) = True   n_common = 974   COCOK
rentang_pool = [2024-01-02T00:00:00, 2025-12-31T00:00:00]   COCOK
n_hari_broker_pool = 519      COCOK
```

### B.2 EV-after-cost (R1d) -- rekonstruksi kata-per-kata Q4

```
n_hari_broker            = 519      (klaim 519)     COCOK
n_jam_slot_total         = 3114     (klaim 3114)    COCOK
n_jam_flat_bar_tidak_ada = 0        (klaim 0)       COCOK
n_hari_dengan_flat       = 0        (klaim 0)       COCOK
n_trade_tereksekusi      = 3114     (klaim 3114)    COCOK
n_exit_SL=158 (klaim 158)  n_exit_TP=15 (klaim 15)  n_exit_time_stop=2941 (klaim 2941)  COCOK
n_fallback_label_Off     = 0        (klaim 0)       COCOK
n_aksi_ATR_Tminus1_nan  = 0        (klaim 0)       COCOK
n_trade_hari_karantina   = 30       (klaim 30)      COCOK
n_trade_hari_gap_flag    = 636      (klaim 636)     COCOK
n_trade_hari_anomali_C   = 30       (|datum 30)     COCOK

MEDIAN EV pool   = 0.014399999999998407   equal_exact = True   COCOK
MEAN EV pool     = 0.010463395724378413   COCOK
n_trade_pool     = 3114    persen_positif = 0.5211946050096339   COCOK
kriteria_(b) GUGUR bila median<=0 -> False
per_tahun 2024: n=1560 median=0.04834999999999022  COCOK
per_tahun 2025: n=1554 median=-0.005049999999992838 COCOK

per jam tetap (semua 519 trade, n_flat=0):
  jam 14 median=0.02490000000000591  jam 13 median=0.017900000000000908
  jam  0 median=0.10679999999999955  jam 15 median=-9.999999999977301e-05
  jam 12 median=0.007899999999981581  jam  7 median=0.008800000000014779
S-H4 VERDICT FORMULA: kriteria_a=False, kriteria_b=False -> TAHAN
```

Median EV cocok sampai digit ke-15 desimal. Kesesuaian float ini tidak
mungkin terjadi bila ada selisih urutan bar, pembulatan, atau filter.

### B.3 Spot-check 3 trade (claims [O16]) -- exit dihitung ulang dari parquet

```
2024-01-05 jam14 (SL)         entry 142->145.448 COCOK | exit SL/143.95292857142857 COCOK | ev -1.5011714285714355 COCOK
2024-04-10 jam0  (TP) Tokyo    entry 151.76      COCOK | exit TP/153.0912857142857  COCOK | ev  1.3250857142857126 COCOK
2024-01-02 jam14 (time_stop)  entry 142.031      COCOK | exit time_stop/141.98    COCOK | ev -0.057100000000016145 COCOK
```

### B.4 Pemeriksaan silang `n_flat = 0` (independen)

`[O3]` melaporkan 11931 bar HH:00 dengan distribusi {23: 513, 22: 6}. Auditor
menguji apakah 6 hari bermasalah kehilangan jam yang ada di daftar tetap
(yang jika benar seharusnya membuat `n_flat > 0`).

```
hari dengan jumlah bar HH:00 != 23 : 6
  2024-01-22 n=22 jam hilang=[22,23]  -> hilang dari FIXED? TIDAK ADA
  2024-03-22 n=22 jam hilang=[20,21]  -> hilang dari FIXED? TIDAK ADA
  2025-03-14 n=22 jam hilang=[20,21]  -> hilang dari FIXED? TIDAK ADA
  2025-03-21 n=22 jam hilang=[20,21]  -> hilang dari FIXED? TIDAK ADA
  2025-03-28 n=22 jam hilang=[20,21]  -> hilang dari FIXED? TIDAK ADA
  2025-10-31 n=22 jam hilang=[20,21]  -> hilang dari FIXED? TIDAK ADA
total bar HH:00 pool = 11931   (klaim [O3] 11931)   COCOK
=> n_jam_flat_bar_tidak_ada = 0 terbukti sah, bukan bug masking.
```

---

## C. R2 -- Rekomputasi S-H5 dari nol (tanpa impor `sh5.py`)

Probe auditor: `r2_sel.py` + `r34_extra.py`. Protokol placebo ditulis ulang
dari spec Q5/nb04 (M5, ATR(14).shift(1) min_periods=14, theta=0.5xATR,
grid 0.5 kelipatan genap, U(5,25) pip + tanda acak, scan t+1..t+24,
denom away+through, bootstrap paired-day B=10000, Holm alpha 0.01).

```
$ venv/Scripts/python.exe %TEMP%/opencode/l3h4h5_audit/r2_sel.py
sha256 m5_2024 = da5e8944763202a7f6fdfc429e287b235d8b3091bf5449af61d4204ba23de3d6
sha256 m5_2025 = a999a4bbedd52af976d0cc2d5a0649ab00df071ade7a6bfcc44c38d527350940
n_bar_m5_frame = 269964   rentang [2023-01-01T22:05:00+00:00, 2026-10-02T20:55:00+00:00]
n_event_raw_round_xx00      = 14482   COCOK
n_event_valid_semua_tahun   = 14316   COCOK
n_event_valid_2024_2025     = 8450    COCOK
cutoff_2024 (q0.75 ATR 2023)      = 1.5216964285714296  equal_exact=True  COCOK
cutoff_2025 (q0.75 ATR 2023-2024) = 1.6039464285714264  equal_exact=True  COCOK
n_atr_store_2023 = 259 ; n_atr_store_2023_2024 = 519 ; atr_constancy = 1   COCOK
n_event_q4_2024_2025 = 2672        COCOK
n_hari_q4_per_tahun  = {2024: 100, 2025: 34}   COCOK
n_hari_eval_per_tahun_store = {2024: 260, 2025: 259}   COCOK
```

```
sel       n_real n_plac    HR_real    HR_plac           diff         p  n_hari
London      1089    767   0.439262   0.440843      -0.001580    0.5176      110
Tokyo        828    526   0.476608   0.460674       0.015934    0.2910       92
NewYork      536    268   0.470833   0.504310      -0.033477    0.7658       77
Sydney       219    137   0.445122   0.401869       0.043253    0.2440       46

Banding per-butir terhadap [O9] dan JSON artefak:
  London  diff -0.0015803147973013076  p 0.5176  n_hari 110  -> COCOK / COCOK / COCOK
  Tokyo   diff  0.015934029831132124  p 0.2910  n_hari  92  -> COCOK / COCOK / COCOK
  NewYork diff -0.03347701149425286   p 0.7658  n_hari  77  -> COCOK / COCOK / COCOK
  Sydney  diff  0.04325279234100754   p 0.2440  n_hari  46  -> COCOK / COCOK / COCOK
  (n_hari = bootstrap n_hari_universe, BEDA dari ci_nb04_style.n_hari -- lihat DEV-B2-3)

Q4-ALL agregat: diff 0.003102545800618639  p 0.4373  n_hari 126   COCOK
Holm: urutan p [Sydney, Tokyo, London, NewYork]
  Sydney p=0.2440 ambang 0.002500 reject=False
  Tokyo  p=0.2910 ambang 0.003333 reject=False
  London p=0.5176 ambang 0.005000 reject=False
  NewYork p=0.7658 ambang 0.010000 reject=False
  sel_positif_holm = []   -> S-H5 VERDICT FORMULA = GUGUR      COCOK
```

Empat nilai p bootstrap (0.244 / 0.291 / 0.5176 / 0.7658) dan keempat CI95
paired-day tereproduksi **digit-per-digit**. Ini bukti terkuat bahwa urutan
konsumsi stream RNG `rng_boot` (London -> Tokyo -> NewYork -> Sydney ->
Q4-ALL) diimplementasikan persis sesuai `meta.rng_streams`.

### C.1 B0 diagnostik (non-penentu) -- juga direproduksi penuh

```
real     claims = hitung = {"n":8450,"away":3309,"through":3753,"tie":867,
                           "none":521,"denom":7062,"hit_rate":0.4685641461342396}   COCOK
placebo  claims = hitung = {"n":4847,"away":1981,"through":2057,"tie":466,
                           "none":343,"denom":4038,"hit_rate":0.49058940069341256}  COCOK
retensi_b0 claims 0.5736094674556212 = hitung 0.5736094674556212   COCOK
```

### C.2 CI nb04-style per sel (suplemen, non-penentu)

```
London  real HR=0.43926247288503256 CI=[0.40963825833787015, 0.4686108781326992] n_hari=108
London  plac HR=0.44084278768233387 CI=[0.38769217970049913, 0.4923607539797157] n_hari=105
Tokyo   real HR=0.4766081871345029  CI=[0.4407252440725244, 0.5110811018775008] n_hari=91
Tokyo   plac HR=0.4606741573033708  CI=[0.410958904109589, 0.5089489083597959] n_hari=84
NewYork real HR=0.4708333333333333  CI=[0.4245047232748038, 0.5167003353856524] n_hari=69
NewYork plac HR=0.5043103448275862  CI=[0.42338636096067817, 0.5870473201352003] n_hari=67
Sydney  real HR=0.4451219512195122  CI=[0.3676439165409754, 0.5117647058823529] n_hari=40
Sydney  plac HR=0.40186915887850466 CI=[0.2906882970742686, 0.5111111111111111] n_hari=40
```

---

## D. R3 -- Larangan tukar Q4 (hour-shopping / S-B.3)

spec Q4(ii) mengikat dua arah: **EV HANYA 6 jam tetap**; **pola HANYA
6 jam teratas hitung-ulang**. Auditor memeriksa kode, bukan hanya dokumen.

* `sh4.py:318-320` `per_hour` dibangun HANYA dari `FIXED_HOURS = [14,13,0,15,
  12,7]` (`sh4.py:59`, lock `:113-119`). Jam 1 tidak pernah masuk hitungan EV.
* `sh4.py:329` loop entry HANYA `for hh in FIXED_HOURS`.
* `sh4.py:451` `gugur_a = bool(n_off_bars >= 2)` memakai `n_off_bars` yang
  berasal dari `top6` hitung-ulang (`sh4.py:158-160`). Jam 7 tidak dipakai
  di kriteria-(a).
* Tidak ada `TAU_alt` di kedua skrip.
* **Bukti tak-tukar yang tidak ambigu:** jam 7 tercatat 519 trade di pool EV;
  jam 1 tidak tercatat sama sekali. Pembeda nyata kedua daftar adalah
  (7 -> 1), bukan jam 0 yang memang ada di kedua daftar.

**HASIL: TIDAK ADA TUKAR. S-B.3 COMPLIANT.**

Kriteria-(a) diuji auditor pada KEDUA bacaan:

```
[R3] top6 bacaan LOCK    [14,13,0,15,12,7]: n_Off = 0 -> kriteria_(a) GUGUR = False
[R3] top6 hitung-ulang   [14,13,0,15,12,1]: n_Off = 0 -> kriteria_(a) GUGUR = False
```

Hasil ini **mendukung** kesimpulan coder (kriteria-(a) negatif pada keduanya),
tetapi **alasan yang ditulis coder salah** -- lihat TEMUAN-1.

---

## E. R4 -- Temuan angka & timestamp

1. **pool 3114 = 6 x 519, tanpa FLAT** -- diverifikasi (bagian B.2 + B.4).
2. **`n_hari` 108 (CI) vs 110 (bootstrap) London** -- diverifikasi sebagai
   **dua definisi berbeda, keduanya benar**: `ci_nb04_style` resample hari
   yang punya event *resolved* di frame itu saja; `paired_day_bootstrap`
   memakai *universe* union hari (real ATAU placebo). Auditor
   mereproduksi kedua angka tepat (108 dan 110). DEV-B2-3 coder **benar**.
3. **C2 memakai timestamp mulai-tugas `2026-10-09T03:11:41`** -- benar,
   disclosed di DEV-B2-4. Auditor memakai cutoff yang sama dan menemukan 9
   file (>0) tetapi semuanya bookkeeping sesi, nol file produksi (bagian A.2).

---

## F. R5 -- Gate penuh (output mentah + rc + cakupan)

```
$ venv/Scripts/python.exe -m pytest -q
platform win32 -- Python 3.12.8, pytest-8.3.3, pluggy-1.6.0
rootdir: D:\ANN   configfile: pyproject.toml   testpaths: tests
collected 254 items
tests\test_build_features.py .....................          [ 14%]
tests\test_build_labels.py ..............................      [ 32%]
tests\test_check_foreign_chars.py ................              [ 44%]
tests\test_clean_data.py .............................         [ 55%]
tests\test_fetch_data.py ................................     [ 69%]
tests\test_resample.py ...............................         [ 81%]
tests\test_validate_data.py ............................      [ 99%]
============================ 254 passed in 20.55s =========================
rc = 0                                                          COCOK (klaim 254 passed)

$ venv/Scripts/python.exe -m ruff check .
All checks passed!            rc = 0                             COCOK
$ venv/Scripts/python.exe -m ruff format --check .
37 files already formatted     rc = 0                             COCOK
Cakupan: seluruh repo (D:\ANN), bukan scope parsial.
```

---

## G. R6 -- Replikasi harness (byte-identik)

Harness **tidak dijalankan in-place**: `OUT = Path(__file__).with_name(...)`
(`sh4.py:76`, `sh5.py:94`) sehingga eksekusi di direktori coder akan
**menimpa artefak bukti**. Auditor menyalin skrip ke direktori audit lalu
menjalankannya; hash artefak coder diukur SEBELUM dan SESUDAH.

```
salinan : repro_sh4.py sha256 = 544e3d3f3d85ec047693e1d3c5354623d21b4e3c56228f88185d0bc64d463eee
          repro_sh5.py sha256 = adbf6efb2723b04458cc6e9df4bee7b3f5bf648b05c436599667a0ca32a8cddc

SEBELUM replikasi:
  sh4_hasil.json b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588
  sh5_hasil.json 7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245

HASIL REPLIKASI ULANG (full run, bukan parsial):
  sh4_hasil.json (replikasi) = b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588
  sh5_hasil.json (replikasi) = 7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245
  IDENTIK sh4 = True ; IDENTIK sh5 = True

SESUDAH replikasi (artefak coder utuh):
  sh4_hasil.json b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588
  sh5_hasil.json 7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245
stderr sh4 = 0 byte ; stderr sh5 = 0 byte
```

Toolchain yang dipakai auditor identik dengan yang deklarasikan coder, jadi
klaim "byte-identik" sah tanpa ruang grey:

```
auditor : python 3.12.8  numpy 1.26.4  pandas 2.2.3  scipy 1.17.1  pytest 8.3.3  ruff 0.6.9
meta sh4: python 3.12.8  numpy 1.26.4  pandas 2.2.3  scipy 1.17.1
meta sh5: python 3.12.8  numpy 1.26.4  pandas 2.2.3  scipy 1.17.1
IDENTIK pada keenam versi. Determinisme terverifikasi 3x (run1, run2 coder + 1 replikasi auditor).
```

---

## H. R7/R8 -- Struktur dokumen dan kepatuhan S-B

```
[O1]..[O18] : 18/18 penanda ada, tidak ada di luar rentang           LULUS
Tabel klaim : K1..K14 lengkap, 14 butir                              LULUS
C1..C9      : C1,C2,C3,C4,C5,C6,C7,C8,C9 seluruhnya hadir + diuji      LULUS
Karakter asing (C1 policy): 0 karakter non-ASCII, ASCII murni        LULUS
Serah-terima: 6 item tertera di bagian akhir dokumen                 LULUS
C8 (baris terakhir): 9cef2998867fc10c295a4ac53825aa9ad39e4cab
   auditor hitung ulang (head -n -1 | git hash-object --stdin) = 9cef2998...  REPRODUSIBEL
   -> tetapi kontrol ini sirkular, lihat TEMUAN-2.
```

### H.1 Status tiap butir S-B

| # | Butir | Status | Bukti |
|---|---|---|---|
| S-B.1 | Vonis H1/H2/H3 dilarang | COMPLIANT |Kedua skrip tidak membaca hasil H1/H2/H3; H4 dan H5 dipakai terpisah |
| S-B.2 | Cell-carving dilarang | COMPLIANT |`CELLS` 4 sel tetap + 1 agregat; k6/k24 dilaporkan non-penuntuh |
| S-B.3 | Hour-shopping dilarang | COMPLIANT |Bagian D: tidak ada tukar 6 jam tetap vs top-6 |
| S-B.4 | 2026-smuggling dilarang | COMPLIANT |2026 tidak masuk populasi penentu; hanya muncul di `rentang_frame`/`n_toucher_placebo_jatuh_2026` yang justru diwajibkan spec untuk dilaporkan |
| S-B.5 | Threshold-peeking dilarang | COMPLIANT |`cutoff_2024`/`cutoff_2025` dihitung sekali di `sh5.py:419-422` sebelum event Q4 dibentuk (`sh5.py:433`); tidak ada cutoff full-sample/in-eval |
| S-B.6 | Hanya Holm yang sah | COMPLIANT |Holm step-down `sh5.py:573-599`; p tak-Holm tidak dipakai untuk vonis |
| S-B.7 | Eksklusi buta dilarang | COMPLIANT |`n_flat=0`, `n_fallback_Off=0`, `n_aksi_ATR_nan=0`, `direction==0` dilewati lalu dilaporkan (14482 -> 14316) |
| S-B.8 | Cabang biaya lain dilarang | COMPLIANT |`cost_by_session` + default 0.65 saja; satuan pip x 0.01 |
| S-B.9 | Kalibrasi ulang dilarang | COMPLIANT |seed/theta/grid/window/offset/B/Holm semuanya literal dari lock+nb04 |
| S-B.10 | Guard nilai-vs-diri dilarang | **VIOLATED** |C8 = self-hash dokumen -> TEMUAN-2 |
| S-B.11 | Output parsial berlabel penuh dilarang | COMPLIANT |`n_resampel_dibuang=0` di keempat sel; semua tahun/sel dilaporkan |
| S-B.12 | Grain selain hari-broker + `utc.normalize()` dilarang | COMPLIANT |`build_features.py:176` `broker_day = wall.dt.normalize()` dari `broker_time_raw`, **bukan** dari `utc` |
| S-B.13 | File beku/lindung tidak boleh disentuh | COMPLIANT |15 blob + 7 sha256 identik; nol file produksi berubah mtime. Catatan 2 file untracked, lihat TEMUAN-6 |
| S-B.14 | Redaksi/ambang lock tidak diubah | COMPLIANT |Tidak ada addendum; `FIXED_HOURS` = lock `:113-119` verbatim |

---

## I. TEMUAN

### TEMUAN-1 -- MEDIUM -- pernyataan "semua 6 bar dalam sesi London/NewYork" terbukti salah

**Lokasi:** `hasil-lapisan3-H4H5.md:1197` dan `:1229` (dan turunannya `:1230`).
**Status:** FAKTA SALAH. **Dampak verdict: nol.**

Dokumen menyatakan dua kali:

* `:1197` -- "Top-6 hitung-ulang M2 OOS = [14, 13, 0, 15, 12, 1] **(semua 6
  bar dalam sesi London/NewYork**; share_Off = 0.0)."
* `:1229` -- "**Karena keduanya tetap dalam sesi London/NewYork**, n_Off = 0 dan
  kriteria-(a) negatif baik pada bacaan lock maupun hitung-ulang."

Bukti auditor (lihat B.1): pada top-6 hitung-ulang, **jam 0 = 31133/31133
Tokyo (100%)** dan **jam 1 = 31138/31138 Tokyo (100%)**. Pada bacaan lock
`[14,13,0,15,12,7]`, jam 0 juga 100% Tokyo dan jam 7 bercampur
(London 17990 / Tokyo 13140). Jadi pernyataan itu salah untuk **kedua**
bacaan, bukan hanya satu.

Dokumen juga **bertentangan dengan angkanya sendiri**: `[O6]` melaporkan
`share_LondonNY_massa_top6 = 0.6832894546066546` (68,3%). Jika semua 6 bar
London/NewYork, angka itu mestinya 1,0.

Sumber EDA asli konsisten dengan auditor: `_build_eda05.py:837-838`
menyatakan "konsentrasi London/NY **parsial, bukan eksklusif** (jam 00 UTC
peringkat 3 = 100% Tokyo)". Dokumen coder malah menyatakan sebaliknya.

**Mengapa non-penentu:** `n_Off = 0` adalah hasil **hitungan**, bukan hasil
penalaran; Tokyo bukan `Off`, sehingga 2 dari 6 jam berupa Tokyo tidak
menggeser `n_Off` sama sekali. Auditor memverifikasi `n_Off = 0` pada kedua
bacaan secara independen. Kriteria-(a) tetap negatif, `kriteria_(b)` tetap
negatif, verdict formula tetap `TAHAN`.

**Yang harus dibetulkan:** kalimatnya. Klaim konsentrasi London/NY adalah
argumen yang dibaca arsitek untuk menilai kelayakan sesi-pintu, jadi
overstatement ini dapat membuat arsitek menyimpulkan kelayakan yang keliru.

### TEMUAN-2 -- MEDIUM -- kontrol C8 sirkular (melanggar S-B.10)

**Lokasi:** `hasil-lapisan3-H4H5.md:1299`.
**Status:** REPRODUSIBEL tetapi VACUOUS. **Dampak verdict: nol.**

```
C8: 9cef2998867fc10c295a4ac53825aa9ad39e4cab   <- git hash-object atas isi
dokumen ini TANPA baris C8 (reproducible: head -n -1 | git hash-object --stdin)
```

Auditor mereproduksi: `head -n -1 | git hash-object --stdin` menghasilkan
`9cef2998867fc10c295a4ac53825aa9ad39e4cab`. Jadi klaim **secara teknis benar**
dan coder bahkan disclose metode beserta perintah reprokusinya.

Masalahnya S-B.10 secara eksplisit melarang "guard nilai-vs-diri (pelajaran
P-1)". C8 membandingkan dokumen **dengan dirinya sendiri** (dikurangi baris
terakhirnya). Konsekuensinya: kontrol ini **tidak dapat mendeteksi
permanipulasi isi** -- siapa pun bisa menghitung ulang C8 dari dokumen yang
sudah diubah dan mendapat hash baru yang "cocok". Tidak ada binding eksternal
apa pun (tidak ada blob tanda tangan, tidak ada referensi ke hash dokumen
sebelumnya).

Perlu dicatat secara adil: audit H1/H2 sebelumnya juga menerima C8
sebagai COCOK. Jadi ini cacat **sistemik pada pola C8**, bukan kelalaian
khusus Batch-2. Ini bukan fabrikasi atau kelalaian khusus.

### TEMUAN-3 -- LOW -- salah satuan persen

**Lokasi:** `hasil-lapisan3-H4H5.md:1199` -- "% positif = 0.5211946050096339%".
Nilai itu adalah **pecahan** 0,52119 (= 52,12%). Menulis `%` setelahnya
menyalahartikan 100 kali. JSON artefak benar
(`persen_positif_pool = 0.5211946050096339`, satuan pecahan). Kesalahan hanya
di prosa. Tidak dipakai di mana pun sebagai angka penentu.

### TEMUAN-4 -- LOW -- efek batas 2023 pada `r` P1 tidak diumumkan di dokumen

**Lokasi:** `sh4.py:152` (`p1["r"] = np.log(p1["close"] / p1["close"].shift(1))`
dihitung pada frame penuh 2023-2026, baru difilter ke 2024-2025).
**Status:** TERCOCOK DENGAN RESEP KANONIK; hanya pengungkapan yang kurang.

Efeknya terukur auditor:

```
hari-broker pertama pool = 2024-01-02 ; utc bar pertama = 2024-01-01T23:00:00+00:00
utc bar sebelumnya       = 2023-12-29T21:59:00+00:00  (tahun 2023)
bar pool yang r-nya mewarisi close 2023 = 1 dari 715308 (0.000140%)
top6 JIKA r dihitung dalam-pool (tanpa waris 2023) = [14, 13, 0, 15, 12, 1]
top6 yang dipakai coder                              = [14, 13, 0, 15, 12, 1]  -> IDENTIK
n_Off pada top6 alternatif = 0
```

Jadi **immaterial** secara numerik. Praktik ini justru **cocok dengan**
kanonik `_build_eda05.py` (r dihitung urut pada concat penuh lalu
difilter) dan sudah **diumumkan** di komentar kode `sh4.py:151`. Yang
hilang adalah pengungkapan itu di dalam dokumen hasil. Spec Q1/S-B.4 melarang
2026 masuk tanpa pengecualian; untuk 2023 pada H4 spec tidak mengatur sedetail
itu, jadi auditor tidak menghakimi ini sebagai pelanggaran. Yang hilang murni
pengungkapan. Auditor menilai ini LOW karena 1 bar dari 715308 dan nol
perubahan hasil.

### TEMUAN-5 -- LOW -- artefak `run3` di direktori kerja coder tidak diumumkan

Dokumen melaporkan determinisme "2x" ([O15], `sh4_hasil_run1.json` =
`sh4_hasil_run2.json` = `b1b69d33...`). Di direktori kerja coder ada tambahan
`sh4_run3.log` dan `sh5_run3.log` yang tidak disebut di dokumen. Apakah run-3
menghasilkan hash berbeda **tidak dapat disimpulkan dari log**; yang pasti,
replikasi penuh auditor (`b1b69d33...`, `7a7f5ee7...`) cocok byte-identik,
jadi determinisme tetap terbukti tiga kali. Temuan ini murni gap pengungkapan
artifact.

### TEMUAN-6 -- LOW -- dua file produksi tidak terlacak git

**Lokasi:** `src/features/build_labels.py`, `tests/test_build_labels.py`.
**Status:** PRASYARAT REPO (bukan pelanggaran coder). **Dampak verdict: nol.**

```
$ git ls-files --error-unmatch src/features/build_labels.py
  error: pathspec 'src/features/build_labels.py' did not match any file(s) known to git
$ git ls-files --error-unmatch tests/test_build_labels.py
  error: pathspec 'tests/test_build_labels.py' did not match any file(s) known to git
$ git status --porcelain -- src scripts notebooks tests
  ?? src/features/build_labels.py
  ?? tests/test_build_labels.py
mtime src/features/build_labels.py = 2026-10-08T18:26:01   (SEBELUM mulai batch 2026-10-09T03:11:41)
mtime tests/test_build_labels.py = 2026-10-08T18:30:12   (SEBELUM mulai batch)
```

**Penilaian.** Dua file produksi ini berada di luar kendali versi git, jadi
`git status` tidak pernah menampilkan *diff* untuk keduanya. Gerbang C2 yang
bergantung pada `git status --porcelain` secara khusus **buta** terhadap file
ini. Sebaliknya, mtime keduanya jatuh **sebelum** batch dimulai, sehingga
ini bukan pekerjaan Batch-2, dan hash keduanya cocok dengan read-proof
(`2561efd5...`, `ed7ac435...`), sehingga integritas isinya terbukti.

**Kredit untuk coder.** Status untracked ini **tidak disembunyikan**: coder
mencantumkan kedua baris `??` itu secara eksplisit di [O4] BEFORE (baris
262-263) dan mengulanginya di [O18] AFTER (baris 1175-1176), sehingga
AFTER == BEFORE benar-benar berlaku. Lebih jauh, coder tidak bergantung pada
`git status` saja: `find -newermt` (yang menutupi file untracked) juga
menghasilkan kosong. Jadi klaim "nol tulis lindung" **tetap sah**; hanya
mekanisme git-nya yang sebagian vakual.

**Rekomendasi (untuk pemilik repo, di luar wewenang auditor):** masukkan kedua
file itu ke `git add` agar berada di bawah kendali versi, lalu gerbang berbasis
`git status` menjadi benar-benar buta-proof.
---

## J. ESKALASI ARSITEK (bukan vonis auditor)

Yang berikut **bukan temuan eksekusi**; murnikoridor keputusan arsitek.
Auditor tidak menetapkan vonis H4/H5.

* **EKS-1 -- selisih lock vs hitung-ulang layak dieskalasikan.** Coder menulis
  "Tidak ada eskalasi wajib" untuk DEV-B2-1. Auditor **tidak setuju** tanpa
  bukti lanjutan. Lock `:113-119` = `[14,13,0,15,12,7]`, hitung-ulang OOS =
  `[14,13,0,15,12,1]`: jam 7 digantikan jam 1, dan keduanya berbeda komposisi
  sesi (jam 7 London+Tokyo, jam 1 Tokyo 100%). Ini mengubah **benda uji**
  kriteria-(a), meski tidak mengubah hasil (n_Off = 0 pada keduanya).
  Keputusan "lock tetap dipakai" memang dalam wewenang arsitek, tapi harus
  dicatat sebagai keputusan sadar, bukan "tidak ada eskalasi wajib".
* **EKS-2 -- `cutoff_2025` memakai ATR 2024 (tahun in-eval).** Sesuai
  S-B.5 yang mengizinkan "2023(/2024)" dan memang dihitung sekali sebelum
  evaluasi (`sh5.py:419-422` sebelum `:433`), sehingga **bukan** peeking.
  Dicatat agar tidak disalahpahami di kemudian hari.
* **EKS-3 -- tanda tahun 2024/2025 pada S-H4.** Median EV pool = +0,0144 JPY
  (positif tipis), tetapi median per tahun 2024 = +0,04835 sementara 2025 =
  **-0,00505** (negatif). Stabilitas tanda antar tahun adalah pertanyaan
  arsitek; ini bukan cacat eksekusi (keduanya dilaporkan jujur sebagai
  deskriptif, `sh4.py:419-429`).
* **EKS-4 -- definisi "Off" vs Tokyo.** `n_Off = 0` bergantung pada definisi
  `session_label` yang beku di `_eda_common.py:17-38` (Tokyo 9-18 Asia/Tokyo).
  Kalau definisi ini berubah, kriteria-(a) ikut berubah.
  Sudah terproteksi fingerprint assert (`sh4.py:121-126`), jadi aman.

---

## K. SELF-AUDIT

**Kesalahan di sisi auditor yang ditemukan dan dikoreksi sendiri (dinyatakan
terbuka, bukan disembunyikan):**

1. **Hash dokumen disalahartikan.** Auditor sempat menghitung sha256 mentah
   (`218c0685...`), melihat ketidakcocokan dengan gate `f06a8e27...`, dan
   menyimpulkan dokumen berubah. Setelah diperiksa, hash di brief adalah
   **git-blob SHA-1**, bukan sha256. `git hash-object` = `f06a8e27b916172f5824
   43acd545614360d3b57` -- cocok. Kesalahan sepele, sudah dikoreksi, tidak
   memengaruhi hasil.
2. **Tiga label pembanding fiktif pada probe.** Versi pertama `r2_sel.py`
   mencantumkan angka pembanding yang **tidak diambil dari JSON coder**
   (`Off = 58`, retensi `0.7917...`, London `n_hari = 108`, Q4-ALL
   `0.00384...`/`0.3548`). Probe sempat melaporkan empat "TIDAK COCOK" palsu.
   Setelah JSON dibaca langsung, ground truth-nya: `Off = 0`, London
   `n_hari_universe = 110` (108 adalah `ci_nb04_style.n_hari`, metrik
   berbeda), Q4-ALL `diff 0.003102545800618639 / p 0.4373`. Ketiganya
   **cocok**. Empat "TIDAK COCOK" tersebut artefak mislabeling auditor,
   **bukan temuan**, dan tidak masuk laporan ini sebagai temuan.
3. **Tiga bug pada probe sendiri** (key counter `TS` vs `time_stop`,
   `KeyError: hour_utc`, `window must be an integer`). Semua diperbaiki dan
   seluruh output di atas berasal dari run setelah perbaikan.

**Rantai bukti yang dipakai:** spec (4a46b815) -> kode produksi
(`build_features.py`, `_eda_common.py`, `_build_eda05.py`) -> parquet beku
(7 sha256) -> probe auditor independen (4 skrip di %TEMP%, tanpa impor skrip
coder) -> replikasi harness ulang. Tidak ada angka yang dipercaya dari
narasi coder saja.

**Probe auditor** (sementara, di luar repo -- sesuai C2):
`%TEMP%\opencode\l3h4h5_audit\r1_top6.py`, `r1_ev.py`, `r2_sel.py`,
`r34_extra.py`, `doc_audit.py`, `read_artefacts.py`, `repro_sh4.py`,
`repro_sh5.py` beserta stdout/stderr. **Nol file produksi ditulis.**

**Yang TIDAK dilakukan (sesuai scope):** tidak menetapkan vonis H4/H5; tidak
mengubah ambang, lock, atau redaksi; tidak menulis/mengubah kode, data, atau
konfigurasi; tidak commit/push; tidak memulai batch berikutnya; tidak
mengulang EDA M1-M5 sebagai audit ulang; tidak menguji hipotesis secara
metodis (bukan wewenang auditor).

**Sisa risiko yang dinyatakan:** nilai `share_LondonNY_massa_top6` 0,6833 di
dokumen sudah benar, tetapi prosa yang mengiringinya berlawanan. Jika
arsitek hanya membaca prosa dan tidak `[O6]`, simpulan yang salah bisa
terambil. Karena itu TEMUAN-1 meski non-penentu harus dilaporkan ke
konsumen hilir (S-R: "Anotasi P0/E0/B0 sebagai jangkar komparabilitas mesin
= BOLEH").

---

## L. VERDICT EKSEKUSI

```
C1  gerbang hash/HEAD/staged            LULUS   (f06a8e27, 4a46b815, staged 0)
C2  nol tulis file produksi             LULUS   (0 file di src/scripts/data/configs/tests)
C3  hash beku + sha256 data + konstanta LULUS   (15 blob + 7 sha256 + cost by_session)
C4  tabel klaim 14 butir                LULUS   (K1..K14)
C5  determinisme                        LULUS   (3 run, byte-identik)
C6  serah-terima 6 item                 LULUS
C7  C8 self-hash                        LULUS secara reproduksi / VACUOUS (TEMUAN-2)
C8  karakter asing                      LULUS   (0 non-ASCII, ASCII murni)
C9  gate pytest + ruff                  LULUS   (254 passed rc=0; check rc=0; format rc=0)

R1  angka S-H4                          COCOK   (bit-exact, median 15 digit desimal)
R2  angka S-H5                          COCOK   (bit-exact, 4 p + 4 CI95 digit-per-digit)
R3  larangan tukar Q4                   COCOK   (tidak ada tukar; kedua bacaan diuji)
R4  temuan angka & timestamp            COCOK   (3114=6x519; 108 vs 110 dua definisi)
R5  gate penuh                          COCOK
R6  replikasi byte-identik              COCOK   (sh4 & sh5 identik; toolchain identik)
R7  struktur dokumen                    COCOK
R8  kepatuhan S-B                       13 COMPLIANT, 1 VIOLATED (S-B.10 -> TEMUAN-2)

TEMUAN : 2 MEDIUM (TEMUAN-1, TEMUAN-2) + 4 LOW (TEMUAN-3 s.d. TEMUAN-6)
EKSKALASI: EKS-1 s.d. EKS-4 ke Arsitek

== VERDICT: LULUS DENGAN TEMUAN ==
Eksekusi Batch-2 jujur dan dapat direproduksi penuh; SELURUH angka penentu
terverifikasi independen. Dua MEDIUM adalah cacat narasi dan cacat desain
kontrol, bukan cacat perhitungan: tidak ada satu pun angka penentu yang
salah, dan tidak ada indikator penentu yang bergeser karena keduanya.
Status vonis resmi tetap MENUNGGU putusan arsitek terpisah.
```

**Hash dokumen ini** disengaja **tidak** ditulis di dalam berkas, dan dihitung
**setelah** tulis final, lalu dilaporkan ke kanal luar dokumen. Alasannya
sengaja: pola C8 self-hash yang di critiqu pada TEMUAN-2 tidak boleh
diulang. Laporan ini tidak mengikat dirinya ke nilai yang tidak bisa
 diverifikasi pihak ketiga.

```
sha256 reaudit-lapisan3-H4H5.md  =  (dihitung setelah tulis final; dilaporkan di luar dokumen)
git blob                         =  (dihitung setelah tulis final; dilaporkan di luar dokumen)
```

**STATUS: RE-AUDIT SELESAI. STOP -- tidak ada commit, tidak ada push, tidak
memulai batch berikutnya.**
