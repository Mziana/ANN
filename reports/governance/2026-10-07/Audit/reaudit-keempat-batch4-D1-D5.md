# RE-AUDIT KEEMPAT — BATCH-4 D1–D5

> Auditor independen, read-only. Tidak ada file produksi yang ditulis,
> tidak ada commit, tidak ada staging.
>
> Tanggal eksekusi: 2026-10-08
> Baseline: `reaudit-ketiga-batch3-D1-D5.md` (`VERDICT: GAGAL`, 1 dari 14
> syarat tersisa terbuka, yaitu butir 5 / B guard provenans).
> Lingkup: 5 butir-fix batch-4 + regresi 13 syarat yang sudah tertutup.
>
> **VERDICT: LULUS**

---

## 0. RUPAAN, GERBANG INTEGRITAS, DAN METODE

### 0.1 Enam sumber wajib

| # | Sumber | Blob (prefix) |
|---|---|---|
| S1 | `coder/laporan-fix-batch4-D1-D5.md` | `56d3f2d6` |
| S2 | `.ai/assistant/verifications/2026-10-08_pra-audit-batch4.md` | `64a0ed7c` |
| S3 | `Audit/reaudit-ketiga-batch3-D1-D5.md` | `673ffb15` |
| S4 | `arsitek/putusan-adjudikasi-reaudit-kedua.md` | `295303a4` |
| S5 | `arsitek/putusan-arsitek-fix-D1-D5.md` | `ca57e764` |
| S6 | `.ai/assistant/PROMPT_DISIPLIN.md` | `37522027` |

Keenam sumber dibaca sebelum pengujian. S4 menetapkan tiga kasus yang
diputus untuk adjudikasi B butir 4: `1.0`, `88.79`, `close-avg`.

### 0.2 Gerbang 0 — keberadaan dan identitas

- `HEAD` = `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` (tidak berubah sepanjang audit)
- Staged = `0`
- 6/6 sumber wajib ada, blob prefix cocok dengan S1–S6.

### 0.3 Gerbang 1 — kontrak hash

Kedelapan hash di bawah dicocokkan terhadap klaim dan **8/8 cocok**:

| Peran | File | `git hash-object` |
|---|---|---|
| D1 | `src/features/build_labels.py` | `2561efd552544feeb9af0b6733711015b83f43dd` |
| D2 | `tests/test_build_labels.py` | `dc07a7e651d38f07a5cabbe4e693b10681312d25` |
| D3 | `coder/protokol-H1-H2-H3.md` | `bc17e5de6cfefb355fe7418acd2a3a0d8b461212` |
| D5 | `coder/laporan-final-fase1.md` | `345308540d27c38534b77cdcd278e32eb15735ec` |
| patch B3 | `coder/laporan-fix-batch3-D1-D5.md` | `b5a9d2a8776915896eeeea65a4d7074d7e2d8981` |
| beku | `src/features/build_features.py` | `399e64b372e430b6def79b4fa8324a4e8e629918` |
| beku | `tests/test_build_features.py` | `ed7ac43520c4431519d4d7065504866ae9b3ad95` |
| beku | `data/features/M15/usdjpy_m15_features.parquet` | `07402f40478aaed9391203f5db3237d636f5a959` |

Ketiga hash beku dihitung ulang **setelah** seluruh pengujian dan tetap
identik — lihat §12.

### 0.4 Metode dan batasan

- Klaim coder diperlakukan sebagai hipotesis. Semua angka di bawah dihitung
  ulang dengan perintah sendiri, bukan dibaca dari dokumen.
- Eksekusi `pytest` memakai plugin mutasi in-memory di luar worktree
  (`%TEMP%\opencode\b4`), sehingga `src/` dan `tests/` tidak pernah ditulis.
- `main()` untuk uji D4 dijalankan dengan `out_dir` temporer; D4 di disk
  tidak pernah ditimpa.
- Tidak ada vonis H4/H5 pada audit ini.

---

## 1. RINGKASAN VERDICT PER BUTIR

| Butir | Severity | Klaim | Hasil auditor | Status |
|---|---|---|---|---|
| 1 | BLOCKING | Referensi ATR dari store terpisah + sabotase jalur produksi | Terbukti: 9/9 RAISED, kontrol membedaikan sumber | **TERBUKTI** |
| 2 | MEDIUM | Format rc=0 pada file batch-4; 9 file pra-ada di luar scope | Terbukti; 1 angka basi (lihat T-1) | **TERBUKTI** |
| 3 | MEDIUM | `RV_WINDOW_DAYS` terikat data kalibrasi | TAU bit-identik; mutasi 20->10 merah | **TERBUKTI** |
| 4 | LOW | D4 nilai per kolom identik lintas toolchain | 6/6 + 10/10 identik; byte berbeda (lihat T-2) | **TERBUKTI** |
| 5 | LOW | Fixture N>32: N=60 bukan ambil-semua | 0.64 vs 0.74 tereproduksi | **TERBUKTI** |
| Regresi | — | 13 syarat batch-3 tetap tertutup | Tidak ada regresi | **TERBUKTI** |

---

## 2. BUTIR 1 [BLOCKING] — REFERENSI TERPISAH + SABOTASE JALUR PRODUKSI

### 2.1 Struktur yang diaudit

`main()` (D1 baris 356–395) membentuk `daily = daily_metrics(m1, m15, pip_size)`
lalu membaca referensi ATR **dari file store terpisah**:

- D1:377 `store_path = FEATURES_DIR / "M15" / f"{symbol.lower()}_m15_features.parquet"`
- D1:378 `atr_reference = _read_atr_reference_from_store(store_path)`

`_read_atr_reference_from_store` (D1:336–353, 18 baris) membaca parquet,
melakukan `groupby("date_broker")["atr_14_d1"].last()`, mengurutkan, lalu
`.shift(-1)`. Hasilnya dikirim ke `_build_daily_labels` (D1:306–333) sebagai
argumen ketiga, terpisah dari kolom `daily["atr_14_d1"]`.

`_assert_atr_provenance` (D1:104–128, 25 baris) membandingkan `atr_used`
terhadap `atr_reference` dengan toleransi eksplisit. `_assert_smoke_bounds`
(D1:131–141, 11 baris) menjaga agar kedua sisi berada dalam rentang ekonomis
bermakna, sehingga reference yang digeser 1000x tidak bisa "lolos" hanya
karena bit-identik.

### 2.2 Baseline jalur produksi

`main()` nyata (bukan potongan) pada `venv` (pandas 2.2.3 / pyarrow 17):

```
baseline: NO RAISE
sha256 usdjpy_day_labels.parquet = 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c
                                    identik dengan file di disk
```

### 2.3 Sembilan sabotase pada jalur produksi

Pembagi ATR pada frame `daily` disabotase, sementara store dibiarkan utuh:

| Sabotase | Hasil |
|---|---|
| `1.0` | RAISED |
| `2.0` | RAISED |
| `88.79` | RAISED |
| `100.0` | RAISED |
| `12345.6` | RAISED |
| `1e6` | RAISED |
| `close-avg` | RAISED |
| `1e-3` | RAISED |
| `-5.0` | RAISED |

**9/9 RAISED.** Ketiga kasus yang diputus adjudikasi B butir 4 —
`1.0`, `88.79`, `close-avg` — semuanya RAISED, yang pada batch-3 luput.

### 2.4 Bukti bahwa guard benar-benar membedakan sumber

Dua harness terpisah:

- **Sabatase frame, store utuh** (`1.0`, `88.79`, `close-avg`) -> **RAISED**.
- **Kontrol: reference diambil dari frame yang sama** -> **NO RAISE** untuk
  ketiga kasus.

Jadi guard tidak sekadar "menolak angka aneh"; guard menolak ketika sumber
provenans bukan store terpisah. Ini persis cacat batch-3 yang sebelumnya
lolos.

Pada baseline, `daily` dan reference store bernilai identik (`max|diff| = 0`
pada 959 titik perbandingan; 974 titik, sisanya warmup/t.tail). Itu **benar**
dan bukan bukti bug: `shift(-1)` pada reference membalik arah attach
anti-look-ahead sehingga keduanya bertemu pada nilai yang sama. Yang
membedakan adalah arah disabotase, bukan nilai baseline.

### 2.5 Mutasi yang mengembalikan bug batch-3

`MUT=reference_sama_frame` membungkus `_build_daily_labels` agar mengabaikan
`atr_reference` dan memakai `daily["atr_14_d1"]` — persis bug lama.

```
MUT=reference_sama_frame -> exit=1 | 3 failed, 57 passed
FAILED TestGuardProvenansJalurProduksi::test_sabotase_produksi_meledak[atr_1.0_non_harga]
FAILED TestGuardProvenansJalurProduksi::test_sabotase_produksi_meledak[atr_88.79_tak_berdimensi]
FAILED TestGuardProvenansJalurProduksi::test_sabotase_produksi_meledak[atr_close_avg_harga_kuantitas_salah]
E   Failed: DID NOT RAISE <class 'AssertionError'>   (x3)
```

Tepat 3 merah, semuanya di jalur produksi, semuanya `DID NOT RAISE`.
Suite sekarang menangkap cacat yang dulu luput.

**STATUS BUTIR 1: TERBUKTI.**

---

## 3. BUTIR 2 [MEDIUM] — FORMAT + KLAIM rc/CAKUPAN

| Toolchain | Perintah | Keluaran | rc |
|---|---|---|---|
| venv, ruff 0.6.9 | `format --check src/features/build_labels.py tests/test_build_labels.py` | 2 files already formatted | **0** |
| venv, ruff 0.6.9 | `check` (D1+D2) | All checks passed! | **0** |
| venv, ruff 0.6.9 | `format --check .` | 37 files already formatted | **0** |
| venv, ruff 0.6.9 | `check .` | All checks passed! | **0** |
| .venv, ruff 0.16.10 | `format --check` (D1+D2) | 2 files already formatted | **0** |
| .venv, ruff 0.16.10 | `check` (D1+D2) | All checks passed! | **0** |
| .venv, ruff 0.16.10 | `format --check .` | 9 would be reformatted, 191 already formatted | **1** |
| .venv, ruff 0.16.10 | `check .` | All checks passed! | **0** |

### 3.1 Cakupan 9 file yang gagal format (ruff 0.16.10)

```
notebooks/scalping/eda_00_setup.ipynb
notebooks/scalping/eda_01_returns.ipynb
notebooks/scalping/eda_02_volatility.ipynb
notebooks/scalping/eda_03_autocorr.ipynb
notebooks/scalping/eda_04_swings_levels.ipynb
notebooks/scalping/eda_05_regimes.ipynb
reports/.../Audit/reaudit-adversarial-D1-D5.md
reports/.../Audit/reaudit-ketiga-batch3-D1-D5.md
src/features/build_features.py          <- BEKU
```

**Nol** dari 6 file batch-4 (D1, D2, D3, D5, patch B3) muncul di daftar.
Semua 9 adalah file pra-ada di luar lingkup batch-4.

Penurunan `10 -> 9` terkonfirmasi silang: `reaudit-ketiga` mencatat,
`10 files would be reformatted ... (rc=1)`; sekarang 9.

### 3.1b Mengapa repo-wide rc berbeda antara 0.6.9 dan 0.16.10

S1 §8 menjelaskan bahwa `ruff format --check .` dengan 0.6.9 "tidak
memindai `.md`/`.ipynb`". Pengukuran menunjukkan penjelasan itu **sebagian
salah**:

```
jumlah file di repo : 31 .py   166 .md   6 .ipynb

ruff 0.6.9   format --check .  ->  37 files already formatted   rc=0
                                  37 = 31 .py + 6 .ipynb   (.md dilewati)
ruff 0.6.9   format --check <file .md>
                             ->  rc=2  "Failed to parse ... Expected an expression"
                                  (0.6.9 tidak mengenal ekstensi .md)
ruff 0.16.10 format --check <file .md>  ->  rc=0  "1 file already formatted"
ruff 0.16.10 format --check .            ->  9 would be reformatted, 191 already
```

Jadi 0.6.9 **melewati `.md`** karena ekstensi itu tidak didukung, tetapi
**memindai `.ipynb`** (6 dari 37 file). Selisih skala 37 vs 200 seluruhnya
berasal dari dukungan `.md`.

Ini tidak mengubah status butir 2: pada 0.6.9 keenam notebook dilaporkan
sudah terformat, dan file yang format-nya tidak stabil adalah `.md` yang
justru tidak dipindai oleh 0.6.9.

### 3.2 Catatan

Dua angka/penjelasan basi ditemukan — lihat T-1 dan T-4. Klaim `rc=0` pada
file batch-4 dan cakupan file di luar scope **benar**.

**STATUS BUTIR 2: TERBUKTI** (dengan catatan T-1 dan T-4).

---

## 4. BUTIR 3 [MEDIUM] — `RV_WINDOW_DAYS` TERIKAT KALIBRASI (DATA)

### 4.1 Struktur penguncian

- D1:66 `RV_WINDOW_DAYS = 20`
- D1:47 `TAU_2023 = 2.5951672079821496e-05`
- D1:48 `CALIB_AUC_2023 = 0.8173755150499336`
- D1:49–50 `CALIB_N_B = 111`, `CALIB_N_A = 129`
- D1:220–223 `rv_score = daily["rv_roll_20d"] / RV_WINDOW_DAYS`;
  `flag = 1[rv_score > TAU_2023]`; hari NaN dibiarkan NaN (tanpa default False)

Test pengunci: `TestRvRegimeFlag::test_rv_window_terikat_kalibrasi_ulang`
memakai helper `_tau_youden_dari_store(window)` yang **membaca parquet store
M15**, bukan konstanta. Jadi penguncian_DATA_, bukan konstanta-vs-konstanta.

### 4.2 Hitung ulang independen dari store

```
TAU Youden (brute-force semua ambang observasi unik) : 2.5951672079821496e-05
TAU_2023 di kode                                     : 2.5951672079821496e-05
BIT-IDENTIK                                          : True   (selisih 0.000e+00)
n terpakai                                           : 240    (klaim 240)
n_B / n_A                                            : 111 / 129  (kode 111 / 129)
Youden J di TAU                                      : 0.6046511628
hari ber-flag                                        : 162/240  (B 111/111; A 51/129)
```

Dua jalur dihitung terpisah dan **memberi hasil identik**:

1. store M15 -> `groupby.last()` -> `.shift(-1)` -> `/window`
2. `daily_metrics(m1, m15, pip_size)` -> `/window` (frame runtime sebenarnya)

### 4.3 AUC — tiga metode independen

```
AUC trapezoid          : 0.8173755150499336   <- identik bit dengan kode
AUC rank/Mann-Whitney  : 0.8173755150499337   (1 ULP di atas)
AUC U-stat (math.fsum) : 0.8173755150499337   (1 ULP di atas)
CALIB_AUC_2023 di kode : 0.8173755150499336
```

Selisih 1 ULP = `1.110e-16` (relatif `1.36e-16`) adalah urutan penjumlahan
floating-point, bukan cacat. Ambang `>= 0.7` (S3) terpenuhi jauh.

Seri kalibrasi tanpa tie sama sekali (`240/240` nilai unik), sehingga ketiga
metode wajib konsisten sampai presisi mesin. Hasilnya: identik pada 15 digit
pertama, berbeda tepat 1 ULP pada digit terakhir — sesuai harapan untuk tiga
jumlah floating-point dengan urutan penjumlahan berbeda.

### 4.4 Mutasi jendela

```
MUT=rv_window_10 -> exit=1 | 1 failed, 59 passed
FAILED TestRvRegimeFlag::test_rv_window_terikat_kalibrasi_ulang
```

Tepat 1 merah. Mengubah `RV_WINDOW_DAYS` 20 -> 10 membuat ambang hasil
hitung-ulang tidak lagi sama dengan `TAU_2023` yang terkunci -> merah.
Kunci terbukti mengikat data.

**STATUS BUTIR 3: TERBUKTI.**

---

## 5. BUTIR 4 [LOW] — D4 / TOOLCHAIN

### 5.1 Byte-reproducibilitas dalam toolchain

`venv` (pyarrow 17.0.0), `main()` dua kali ke `out_dir` temp:

```
usdjpy_day_labels.parquet
  disk   sha256 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c  (29121 B)
  run1   sha256 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c  (29121 B)
  run2   sha256 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c  (29121 B)
  run1==run2 True   run1==disk True

usdjpy_h2_trades.parquet
  disk   sha256 32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f  (7837 B)
  run1   sha256 32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f  (7837 B)
  run2   sha256 32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f  (7837 B)
  run1==run2 True   run1==disk True
```

Byte-reproducible 2x **dan** identik dengan disk.

### 5.2 Nilai per kolom — lintas toolchain

`.venv` (pandas 3.0.6 / pyarrow 25.0.1) menghasilkan byte berbeda, seperti
dinyatakan klaim:

```
usdjpy_day_labels.parquet   run1 sha256 20cf4cdd720e620af4d01d44e557cc5c43c0ee73a5c361b99fe7fa704fc81899
usdjpy_h2_trades.parquet    run1 sha256 75938ad32bf35a209428ab449839b7331fba23a6c6c097214b1d621766bc6aa5
```

Perbandingan nilai kolom terhadap D4 di disk:

| File | Kolom nilai identik |
|---|---|
| `usdjpy_day_labels.parquet` | **6/6** |
| `usdjpy_h2_trades.parquet` | **10/10** |

Seluruh kolom sama nilai **dan** sama dtype, kecuali drift metadata yang
dinyatakan terang-terangan oleh klaim:

```
day_label       object -> str        (nilai identik)
gap_f2_flag     int32  -> int64      (nilai identik)
index           datetime64[ns] -> datetime64[ms]  (nilai & urutan identik)
```

Drift dtype ini berasal dari pandas/pyarrow, bukan dari logika label.

**STATUS BUTIR 4: TERBUKTI** (dengan catatan T-2).

---

## 6. BUTIR 5 [LOW] — FIXTURE N > 32

### 6.1 Masalah yang diikat

`LONDON_FIRST_N` memotong jendela London ke N bar **pertama**. Sesi London
8 jam = 32 bar M15, jadi fixture lama `n_bars=32` tidak bisa membedakan
"ambil N bar" dari "ambil semua". Fix: grid 5 menit dan 70 bar.

### 6.2 Reproduksi independen (fixture dibangun sendiri, bukan dari test)

Bar `k`: `open = 150 + 0.01k`, `close = open + 0.05`, sehingga
`drift(N) = 0.05 + 0.01*(N-1)` — berbeda untuk tiap N.

```
grid 5 menit, 70 bar London
N=16              -> 0.2000000000
N=60 (60 pertama) -> 0.6400000000    (= 0.05 + 0.01*59)
ambil-semua 70    -> 0.7400000000    (= 0.05 + 0.01*69)
selisih 60 vs semua: 0.10
```

**0.64 vs 0.74 tereproduksi persis.** Karena selisihnya 0.10, test tidak
lagi bisa lolos kalau implementasi berubah menjadi "ambil semua".

### 6.3 Mutasi jendela

```
MUT=london_n_60 -> exit=1 | 7 failed, 53 passed
FAILED TestLondonDrift4h::test_formula_close_terakhir_minus_open_pertama
FAILED TestLondonDrift4h::test_norm_adalah_drift_per_atr_index_sama
FAILED TestLondonDrift4h::test_bar_luar_london_diabaikan
FAILED TestLondonDrift4h::test_dst_aware_musim_dingin_mulai_08_utc
FAILED TestJendelaLondonLock::test_konstanta_terkunci_16
FAILED TestJendelaLondonLock::test_n60_mengambil_60_bar_pertama_bukan_ambil_semua
FAILED TestGuardProvenansAtr::test_baseline_pembagi_kolom_store_lolos
```

**STATUS BUTIR 5: TERBUKTI.**

---

## 7. REGRESI — 13 SYARAT BATCH-3

### 7.1 Gate penuh

| Toolchain | Perintah | Hasil | rc |
|---|---|---|---|
| venv (pandas 2.2.3) | `pytest -q` | **254 passed** in 19.66s | **0** |
| .venv (pandas 3.0.6) | `pytest -q` | **254 passed** in 18.43s | **0** |
| venv | `pytest tests/test_build_labels.py` | 60 passed | **0** |

Koleksi: D2 = 60 test (54 method AST + parameterisasi), repo = 254 test.

### 7.1b Matriks mutasi spot-check

Empat kunci yang diminta brutally: guard, N, TAU, dan write-index.

| Mutasi | Efek yang diharapkan | Hasil | rc |
|---|---|---|---|
| `none` (baseline) | semua hijau | 60 passed | 0 |
| `guard_noop` | guard paritas mati | 7 failed, 53 passed | 1 |
| `reference_sama_frame` | referensi = kolom frame | 3 failed, 57 passed | 1 |
| `rv_window_10` | TAU tidak terikat jendela | 1 failed, 59 passed | 1 |
| `london_n_60` | fixture N=16 di-hardcode | 7 failed, 53 passed | 1 |
| `write_index` | row key D4 hilang saat tulis | **1 failed, 59 passed** | 1 |

Mutasi `write_index` membungkus `write_labels` sehingga `usdjpy_day_labels.parquet`
ditulis dengan `index=False`. Efeknya terukur langsung pada file hasil: `index.name`
menjadi `None` dan kolom `date_broker` **tidak ada sama sekali** (row key hilang
total, bukan berubah jadi kolom). Test yang menangkapnya adalah
`test_day_labels_grain_dan_row_key`:

```
AssertionError: row key #20 hilang
assert None == 'date_broker'
 + where None = RangeIndex(start=0, stop=974, step=1).name
```

Jadi row key #20 benar-benar terkunci oleh D2, bukan sekadar diklaim.

**Catatan harness (penting untuk auditor berikutnya).** Percobaan pertama
menjalankan mutasi di satu proses terpisah lalu `pytest` di proses lain; hasilnya
60 passed dan terlihat seperti "test tidak menangkap". Mutasinya ternyata tidak
aktif sama sekali. Mutasi wajib diimpor **in-process** (`pytest -p b4_mut` dengan
`PYTHONPATH`), dan sebelum film merah Smoking gun dihitung ulang pada file D4
hasil agar tidak melaporkan gap test yang sebenarnya tidak ada.

### 7.2 Kalibrasi Q1(a) dihitung ulang setelah perubahan D1

```
n terpakai : 240        n_B/n_A : 111/129
TAU bit-identik dengan kode : True
AUC vs kode : 1 ULP (trapezoid identik bit)
hari ber-flag : 162/240 (B 111/111; A 51/129)
```

D1 berubah dari 400 menjadi 399 baris. Karena itu kalibrasi dihitung ulang dari
data, bukan diambil ulang dari konstanta lama: `TAU_2023` dihitung dari frame
runtime `daily_metrics()` lalu dibandingkan bit-per-bit dengan nilai di protokol.
Hasil `True` di atas membuktikan penghapusan satu baris itu **tidak** menggeser
kalibrasi.

### 7.3 Invariant D4

```
baris x kolom        : 974 x 6
index unik           : True   name = date_broker
gap_f2_flag SUM      : 234        <- TARGET Q3-a
gap_f2_flag dtype    : int32   NaN = 0
quarantine True      : 19
london_drift_norm NaN: 14         (warmup 14)
rv_regime_flag NaN   : 19         (warmup 19)
day_label NaN        : 0
day_label unik       : ['normal', 'range', 'trending']
rv_regime_flag unik  : [0.0, 1.0]
rv_regime_flag dihitung ulang == D4 : True
```

### 7.4 Rekonsiliasi #23 gap F2 — dihitung ulang dari M15

Dua edge-rule dibandingkan, `BATAS HARI` (dipakai D1) dan `BATAS SESI`
(blok sesi berurutan dalam hari, label eksklusif prioritas
London > NewYork > Tokyo > Sydney > Off):

```
baris M15                       : 90.041
broker_day unik                 : 974
total bucket parsial (m1_bars<15): 1.281   [ref B1: 1.281]

edge-rule BATAS HARI
  bucket parsial mid-day        :   597    [ref B1: 597]
  hari ter-flag                 :   234    [ref B1: 234]

edge-rule BATAS SESI
  bucket parsial mid-day        :   578
  hari ter-flag                 :   230

rekonsiliasi bucket
  di kedua edge-rule            :   578
  hanya BATAS SESI              :     0
  hanya BATAS HARI              :    19
                                 -----
  total BATAS HARI              :   597    (578 + 19 OK)

rekonsiliasi hari
  hari SESI / HARI / selisih    : 230 / 234 / +4
  hari hilang saat HARI         :     0    (HARI superset dari SESI: True)
```

Tidak ada hari hantu: `prepare_bars` menghasilkan 974 broker-day unik dari
90.041 bar M15, dan himpunan hari ter-flag dari fungsi D1 identik dengan
himpunan `BATAS HARI` maupun dengan `gap_f2_flag` di D4 disk. Rekonsiliasi
`597 = 578 + 19` **tertutup**, dan tidak ada regresi setelah perubahan D1.

### 7.5 Kontrak D4 dan larangan backtest

```
data/labels/ berisi tepat 2 file kontrak:
  usdjpy_day_labels.parquet   29121 B
  usdjpy_h2_trades.parquet     7837 B

kolom usdjpy_h2_trades.parquet:
  symbol, strategy, entry_rule, exit_rule, sl_atr, tp, biaya,
  entry_time_utc, entry_frequency, price_unit
```

Tidak ada kolom `pnl`, `ev`, `return`, atau `sharpe`. H2 tetap
pra-registrasi, belum dieksekusi. Larangan backtest di `build_labels`
terjaga.

### 7.6 Klaim struktural

| Klaim | Terukur | Status |
|---|---|---|
| D1 399 baris | 399 | cocok |
| `main` AST 40 | `main` membentang 40 baris (356–395) | cocok |
| D2 713 baris | 713 | cocok |
| D2 60 test | 60 terkoleksi (54 method AST + parameterisasi) | cocok |

**3 artefak beku** (harus `IDENTIK`, bukan sekadar MATCH):

| Artefak | Hash aktual | Status |
|---|---|---|
| `src/features/build_features.py` | `399e64b372e430b6def79b4fa8324a4e8e629918` | IDENTIK |
| `tests/test_build_features.py` | `ed7ac43520c4431519d4d7065504866ae9b3ad95` | IDENTIK |
| `data/features/M15/usdjpy_m15_features.parquet` | `07402f40478aaed9391203f5db3237d636f5a959` | IDENTIK |

Tiga artefak beku tidak bergerak: D1/D2 batch-4 tidak menyentuh pipeline
terdahulu maupun store M15.

Tambahan yang diukur tetapi tidak diklaim: D2 punya 14 kelas test, dan
`main()` punya 223 simpul AST (`stmt` = 18, `Call` = 17). Angka "AST 40"
pada klaim dibaca sebagai **rentang baris** `main`, bukan jumlah simpul — jika
dibaca sebagai jumlah simpul, klaim itu tidak cocok.

**STATUS REGRESI: TERBUKTI — tidak ada regresi pada 13 syarat.**

---

## 8. TEMUAN BARU

Lima temuan. Tidak satu pun mengubah verdict; semuanya LOW atau informasional.

### T-1 [LOW] Angka jumlah file format yang basi

S1 §8 menyatakan `189 files already formatted` untuk ruff 0.16.10 repo-wide.
Terukur: **191**.

- Yang benar dan material: `rc=1`, `9 files would be reformatted`, dan
  nol file batch-4 di daftar.
- Yang basi: total file yang sudah terformat (189 vs 191), karena
  `laporan-fix-batch4-D1-D5.md` sendiri ditambahkan setelah angka itu diukur.

Tidak ada dampak pada butir 2, yang statusnya ditentukan `rc` dan cakupan.

### T-2 [INFO] Sub-klaim `Index.equals` tidak tereproduksi

S1 §5 menyatakan `Index.equals apa adanya False (ns vs ms)`. Terukur pada
kedua toolchain: `.equals()` mengembalikan **True** — pandas membandingkan
nilai instants, bukan unit. Dtype tetap berbeda (`ns` vs `ms`), urutan dan
nilai identik. Tidak ada dampak pada kesimpulan butir 4.

### T-3 [LOW] Prosedur kalibrasi Q1(a) kurang eksplisit di teks protokol

Ini temuan yang paling layak dicatat untuk auditor berikutnya.

Untuk merekonstruksi `rv_score` yang dipakai runtime dari store M15, seri
`rv_roll_20d` **wajib** dibaca sebagai
`groupby("date_broker").last().sort_index().shift(-1)`. Tanpa `shift(-1)`:

```
tanpa shift : n = 239, n_B = 110, Youden maks J = 0.99225,
              argmax tau = 1.2019462260623688e-05
dengan shift: n = 240, n_B = 111, Youden J = 0.60465,
              tau = 2.5951672079821496e-05  (bit-identik dengan kode)
```

Artinya auditor yang mengikuti teks protokol §2 secara literal akan
menghasilkan ambang yang **berbeda** dan Youden yang justru lebih tinggi
(0.99225 vs 0.60465) — dan bisa menyimpulkan kalibrasi salah, padahal
kode dan test sudah konsisten.

Kode (`compute_rv_regime_flag`) dan test (`_tau_youden_dari_store`) sudah
satu suara; yang kurang hanya **prose** D3 §2 yang tidak menyebut langkah
`shift(-1)` secara eksplisit. Saran perbaikan (di luar lingkup audit ini):
tambahkan satu kalimat di D3 §2 menyatakan bahwa seri store dibaca dengan
`shift(-1)` agar cocok dengan frame runtime.

### T-4 [INFO] Penjelasan cakupan `.md`/`.ipynb` di S1 §8 kurang tepat

S1 §8 menulis bahwa `ruff format --check .` dengan 0.6.9 "tidak memindai
`.md`/`.ipynb`". Terukur: 0.6.9 memang **melewati `.md`**, tetapi
**memindai `.ipynb`** (6 dari 37 file yang dipindai). Lihat §3.1b.

Tidak ada dampak pada butir 2: angka `rc` dan daftar 9 file tetap benar,
dan justru tidak stabilnya format `.md`lah yang membuat `rc=1` muncul pada
0.16.10.

### T-5 [INFO] Pointer baris S4 tidak resolve ke isi gap F2

S4 butir 6 menulis status `BELUM DIUJI` gap F2 dengan pointer
`protokol:170-174`. Baris 170-174 `protokol-H1-H2-H3.md` sebenarnya berisi
"3. REDAKSI EKSAK F-1" (butir H2/H4/H5), bukan status gap F2. Letak yang
benar adalah §4 "STATUS BELUM DIUJI DAN LARANGAN EKSLUSI BUTA"
(`protokol:188-213`, butir `gap_f2_flag` di `protokol:192-211`).

Dampak: nihil pada status. Pernyataan substantif S4 ("pertahankan sampai uji
sensitivitas klasifikasi H1 ada") benar dan didukung `protokol:211`; hanya
rujukan barisnya yang stale. Laporan §9 memakai rujukan yang sudah
diperbaiki.

---

## 9. YANG TETAP BELUM DIUJI

Sesuai S4 (`putusan-adjudikasi-reaudit-kedua.md` butir 6) dan status resmi
di `protokol-H1-H2-H3.md` §4 (`protokol:188-213`), hal berikut **bukan**
temuan dan tetap `BELUM DIUJI`:

1. **Materialitas `gap_f2_flag` pada 234 hari** (syarat H1/H5). Angka 234
   kini terbukti benar secara aritmetika **dan** rekonsiliasi
   `597 = 578 + 19` tertutup (§7.4; cocok pula dengan `protokol:206` yang
   menyebut varian BATAS SESI = 578 bucket/230 hari). Nuansa F-2 tetap
   berlaku: **223 dari 234** hari punya counterfactual, sedangkan pada 11
   hari bucket justru partial karena bar M1-nya sudah absen di store M1
   (`reaudit-F2-F3-F4.md`:55-73). Status `BELUM DIUJI` (`protokol:211`)
   dipertahankan sampai **uji sensitivitas klasifikasi H1 pada hari-hari itu
   ada**. Eksklusi buta tetap dilarang (`protokol:224`).
2. **Sensitivitas TAU** terhadap span/window alternatif
   (`protokol:214-217`; vonis H3 belum keluar).

Keduanya adalah prasyarat prosedur **Lapisan 3-H3** (S4 butir "Lubang 2"),
bukan syarat batch-4.

---

## 10. VERDICT AKHIR

**LULUS.**

Dasar:
- 5/5 butir batch-4 **TERBUKTI** dengan bukti eksekusi independen.
- 13/13 syarat yang sudah tertutup pada batch-3 **tetap tertutup**; tidak ada
  regresi pada gate penuh (254 passed di dua toolchain), kalibrasi
  (TAU bit-identik), gap 234 beserta rekonsiliasi `597 = 578 + 19`,
  quarantine 19, warmup NaN, kontrak D4, atau larangan backtest.
- Lima temuan (T-1, T-2, T-3, T-4, T-5) LOW/informasional, tidak menyentuh
  rc, cakupan, nilai, atau hemat.

**Dengan LULUS ini, Fase 1 MAYOLEH naik ke Lapisan 3**, dengan dua hal
tersebut sebagai prasyarat Lapisan 3-H3 dan bukan sebagai temuan:

- uji materialitas `gap_f2_flag` pada 234 hari (H1/H5),
- uji sensitivitas TAU terhadap span/window alternatif.

Audit ini **tidak** memberi vonis H4 maupun H5.

---

## 11. SELF-AUDIT 3x

**Putaran 1 — Kebenaran.** Setiap angka di laporan ini berasal dari eksekusi
yang dapat diulang, bukan dari dokumen. Klaim dipetakan ke bukti:
butir 1 -> §2.2–§2.5; butir 2 -> §3; butir 3 -> §4.2–§4.4; butir 4 -> §5;
butir 5 -> §6; regresi -> §7.1–§7.6 dan matriks mutasi §7.1b. Klaim atau
penjelasan yang **tidak** tereproduksi ditulis apa adanya sebagai T-1, T-2, T-4,
dan T-5, bukan disembunyikan.

**Putaran 2 — Bias dan asumsi.** Klaim coder diuji pada arah yang tidak
menguntungkan: (i) "referensi terpisah" diuji dengan mengembalikan bug lama
lewat mutasi `reference_sama_frame`; (ii) "9/9 sabotase" diuji pada `main()`
nyata, bukan potongan; (iii) "nilai per kolom identik" diuji lintas toolchain
pyarrow 17 vs 25, di mana byte memang berbeda dan itu diakui; (iv) "jendela
terkunci" diuji dengan mutasi 20->10 dan 16->60; (v) "fixture N>32" diuji
dengan membangun ulang 70 bar sendiri, bukan menyalin test; (vi) kalibrasi
dihitung ulang dari parquet store, bukan dari konstanta.

Kesalahan di pihak auditor sendiri ditemukan dan dikoreksi, bukan
dipoles: (a) rekonstruksi awal tanpa `shift(-1)` memberi 239/110 dan ambang
yang salah — ditemukan lewat ketidakcocokan `CALIB_N_B`; (b) trapezoid AUC pertama
menghitung sumbu TPR/FPR terbalik dan memberi `1 - AUC`; (c) rank AUC
pertama salah-alignment indeks; (d) mutasi `write_index` sempat dijalankan di
proses terpisah sehingga tampak hijau palsu — baru ketahuan karena efek mutasi
diperiksa langsung pada file D4 hasil, bukan karena `pytest`. Semuanya
dikoreksi dan hasil akhirnya disilog di §4.2–§4.3 dan §7.1b.

**Putaran 3 — Batasan dan ruang lingkup.** Yang **tidak** diklaim laporan ini:
- tidak memberi vonis atas H4/H5;
- tidak menilai apakah 234 hari material secara ekonomi;
- tidak menilai sensitivitas TAU;
- tidak memverifikasi masa depan data di luar 2026-10-02;
- prosedur kalibrasi pada T-3 harus selalu dibaca dengan `shift(-1)`;
  ini catatan dokumentasi, bukan cacat kode.
Tidak ada temuan yang dipalsukan, tidak ada angka yang diambil dari
asumsi. Batasan read-only terbukti pada §12.

---

## 12. BUKTI READ-ONLY

Diperiksa ulang **setelah** seluruh pengujian:

```
HEAD                          : e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169   (tidak berubah)
staged                        : 0
src/features/build_labels.py  : 2561efd552544feeb9af0b6733711015b83f43dd  (tidak berubah)
tests/test_build_labels.py    : dc07a7e651d38f07a5cabbe4e693b10681312d25  (tidak berubah)
coder/protokol-H1-H2-H3.md    : bc17e5de6cfefb355fe7418acd2a3a0d8b461212  (tidak berubah)
coder/laporan-final-fase1.md  : 345308540d27c38534b77cdcd278e32eb15735ec  (tidak berubah)
src/features/build_features.py: 399e64b372e430b6def79b4fa8324a4e8e629918  (BEKU, identik)
tests/test_build_features.py  : ed7ac43520c4431519d4d7065504866ae9b3ad95  (BEKU, identik)
data/features/M15/...parquet  : 07402f40478aaed9391203f5db3237d636f5a959  (BEKU, identik)
```

Tidak ada file produksi yang ditulis. Semua harness berada di
`%TEMP%\opencode\b4`. Tidak ada commit dan tidak ada staging. D4 di disk
tidak pernah ditimpa — `main()` selalu diberi `out_dir` temporer.

---

*Laporan ini ditulis oleh auditor independen pada 2026-10-08. Verdict
LULUS berlaku hanya untuk lingkup 5 butir batch-4 dan regresi 13 syarat;
tidak berlaku untuk Lapisan 3 atau H4/H5.*
