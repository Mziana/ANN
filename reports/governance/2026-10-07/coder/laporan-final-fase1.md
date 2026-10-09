# Laporan Akhir Fase 1 — Fix D1–D5 (batch ke-2, direvisi batch ke-3, direvisi batch ke-4)

**Tanggal:** 2026-10-07 (revisi batch-3: 2026-10-08; revisi batch-4: 2026-10-08)
**Status:** SELESAI (dengan catatan) — bukti mentah di §8, di
`coder/laporan-fix-batch3-D1-D5.md` (patch 5 butir) dan di
`coder/laporan-fix-batch4-D1-D5.md`
**Persetujuan:** User menyetujui Fase 0, lanjut ke Fase 1

---

## 1. TABEL ANGGARAN (diukur, bukan diklaim)

| Objek | Nilai | Pagu | Status |
|-------|-------|------|--------|
| `src/features/build_labels.py` (fisik) | **399** | 400 | OK |
| `src/features/build_labels.py` — `main` (baris AST) | **40** | 50 | OK |
| `src/features/build_labels.py` — fungsi terpanjang (`main`) | **40** | 50 | OK |
| `tests/test_build_labels.py` (fisik) | 713 | — | dilaporkan apa adanya |
| `tests/test_build_labels.py` — jumlah test | 60 | — | dilaporkan apa adanya |
| `src/features/build_features.py` (fisik, TIDAK disentuh) | 400 | 400 | OK |
| `build_features.daily_metrics` (span AST, TIDAK disentuh) | 50 | 50 | OK |
| `tests/test_build_features.py` (fisik, TIDAK disentuh) | 357 | 357 | OK |
| parquet `07402f40…` (git blob, TIDAK disentuh) | cocok | identik | OK |

**Semua file lama identik — tidak ada perubahan.** D1 terdaftar di tabel
anggaran (temuan #28). Angka batch-3 (400 / 33 / 586 / 54) diperbarui batch-4
menjadi **399 / 40 / 713 / 60** dari output mentah §8.9.

---

## 2. HASH ARTEFAK BARU (diukur `git hash-object` SESUDAH penulisan terakhir)

| Artefak | Hash git blob | Keterangan |
|---------|---------------|------------|
| `src/features/build_labels.py` | `2561efd552544feeb9af0b6733711015b83f43dd` | D1 final batch-4 (referensi provenans dari store terpisah; 399 baris) |
| `tests/test_build_labels.py` | `dc07a7e651d38f07a5cabbe4e693b10681312d25` | D2 final batch-4, 60 test (713 baris) |
| `reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md` | `bc17e5de6cfefb355fe7418acd2a3a0d8b461212` | D3 final batch-4 (298 baris) |
| `reports/governance/2026-10-07/coder/laporan-fix-batch3-D1-D5.md` | `b5a9d2a8776915896eeeea65a4d7074d7e2d8981` | laporan batch-3 + patch 5 butir batch-4 |
| `reports/governance/2026-10-07/coder/laporan-final-fase1.md` | dilaporkan di `coder/laporan-fix-batch4-D1-D5.md` §1 | ditulis SESUDAH ini — hash mustahil di-embed konsisten |
| `data/labels/usdjpy_day_labels.parquet` | sha256 `47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c` (29121 B) | 974 baris, row key `date_broker`; git blob `a01694e3eafafa9c9e2e14ca3d8396706b4f2857` |
| `data/labels/usdjpy_h2_trades.parquet` | sha256 `32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f` (7837 B) | 1 baris spesifikasi; git blob `7138325d278283056d09974cbf93fddbb2926b40` |

**Hash 3 artefak lama (wajib identik):**

```
git hash-object src/features/build_features.py                399e64b372e430b6def79b4fa8324a4e8e629918
git hash-object tests/test_build_features.py                  ed7ac43520c4431519d4d7065504866ae9b3ad95
git hash-object data/features/M15/usdjpy_m15_features.parquet  07402f40478aaed9391203f5db3237d636f5a959
```

Ketiganya identik dengan kontrak — nol sentuh file lama.

---

## 3. RESIDUAL BARU BERNOMOR

DILARANG menimpa #1–#7 dari re-audit sebelumnya. Residual #8–#13 (status
diperbarui batch-4):

| # | Temuan | Severity | Status |
|---|--------|----------|--------|
| 8 | `compute_rv_regime_flag` hidup; TAU_2023 + AUC + n per kelas angka riil (dieksekusi Q1(a), protokol §2) | INFO | **TERTUTUP** (butir §7-4 / #24) |
| 9 | `compute_gap_f2_flag` hidup dari M15 sumber; definisi Q3(a) pada grain broker-day tunggal; recount = 234 hari / 597 bucket mid-day (identik B1) | HIGH | Terbuka sebagai **uji materialitas** — status BELUM DIUJI; eksklusi buta DILARANG |
| 10 | D4 tepat dua file nama kontrak, dua varian berbeda (bukan byte-identik), karantina 19 hari terbawa, `h2_trades` TANPA kolom hasil, 974 baris broker-day + row key | — | **TERTUTUP** (bukan BLOCKER: severity tidak naik karena cacat sudah hilang — koreksi §1 #19) |
| 11 | Protokol H2 pra-registrasi lengkap (jam 15 UTC, 1x, satuan harga JPY); backtest belum dieksekusi | INFO | Backtest ditunda sampai persetujuan protokol |
| 12 | H4/H5 tidak divonis — sesuai putusan arsitek H1-H5 (S4, larangan H4/H5) | INFO | Vonis ditunda |
| 13 | H6+ tidak dibuat — sesuai D0 + putusan H1-H5 | INFO | H6+ ditolak |

Residual batch-4 (temuan baru dari re-audit ketiga §8) ditutup di §9, kecuali
dua yang memang bukan mandat: (a) materialitas `gap_f2_flag` pada 234 hari
(uji H1/H5, status BELUM DIUJI), (b) vonis H3/H4/H5.

---

## 4. VERIFIKASI DILARANG §3 (APA ADANYA, SESUDAH UNSTAGE)

### DILARANG: Commit/stage

**STATUS:** DIPATUHI **sesudah perbaikan**. Batch-2 melanggar klaim ini
(23 entri staged di indeks milik pekerjaan lain); batch-3 menjalankan
`git reset` (unstage seluruh indeks; **working tree tidak disentuh**).
Output mentah batch-4 (terkini):

```
=== git status --porcelain (ringkasan kolom XY) ===
     21  D
      4  M
     66 ??
total: 91
staged: 0
=== git diff --cached --name-only ===
0
=== HEAD ===
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
```

Tujuh rename governance tampil sebagai `D` (path lama) + target
`arsitek/`/`audit/` sebagai direktori untracked — **semua file tetap ada di
disk** dan tidak ada satu commit pun dibuat. 4 entri ` M` (`.ai/AGENTS.md`,
`.ai/SESSION_LOG.md`, `.ai/assistant/README.md`, `requirements.txt`) dan
21 ` D` bukan pekerjaan coder; tidak disentuh isinya. Jumlah `??` bergerak
65 → 66 murni karena git meng-collapse/expand direktori untracked — bukan
karena file coder hilang.

### DILARANG: Menyentuh file lama

**STATUS:** DIPATUHI — hash `399e64b3…`/`ed7ac435…`/`07402f40…` identik (§2).

### DILARANG: Menulis ulang parquet produksi

**STATUS:** DIPATUHI — git blob `07402f40478aaed9391203f5db3237d636f5a959`
identik dengan HEAD; D4 ditulis ke `data/labels/` saja. Build batch-4
diarahkan ke direktori tmp (di luar repo) — bahkan disk D4 tidak ditulis ulang
karena rebuild terbukti byte-identik (§8.11).

### DILARANG: Mengoptimasi ambang dari data evaluasi

**STATUS:** DIPATUHI.
- `RATIO_PATH_THRESHOLD = 0.0268`, `RANGE_ATR_THRESHOLD = 88.79` dari lock.
- `ANOMALY_WINDOWS` dari putusan F-1 butir 2.
- `TAU_2023 = 2.5951672079821496e-05` **bukan ambang lock** — hasil kalibrasi
  in-sample Q1(a) pada span terkunci 2023 (prosedur yang diperintahkan
  arsitek), ditulis di protokol §2 sebagai hasil kalibrasi. Tidak ada tuning
  pada data evaluasi/OOS.

### DILARANG: Menjalankan backtest H2

**STATUS:** DIPATUHI — nol kode backtest; `usdjpy_h2_trades.parquet` berisi
spesifikasi saja (10 kolom teks, tanpa pnl/ev).

### DILARANG: Klaim tanpa tempelan output mentah

**STATUS:** DIPATUHI — setiap angka di laporan ini, di laporan batch-3
(patch) dan di laporan batch-4 ditempel dari output mentah (§8).

### DILARANG: File di luar D1–D4

**STATUS:** DIPATUHI — file yang dibuat/diedit: D1 `build_labels.py`,
D2 `test_build_labels.py`, D3 `protokol-H1-H2-H3.md`, D4 dua parquet kontrak,
D5 laporan ini, laporan batch-3 (patch 5 butir), laporan batch-4. Scratch
kerja batch-4 (harness sabotase/mutasi/rebuild) berada **di luar repo**
(`C:\Users\Fajar\AppData\Local\Temp\b4\`), sehingga `ruff check .` dan
`format --check .` tidak terpengaruh berkas scratch.

### Koreksi .gitignore

**STATUS:** DIPATUHI — `.gitignore:24` = `data/labels/`; parquet di
`data/labels/` tidak di-track git (hash diukur dengan sha256 isi file, dan
git blob tetap dilaporkan sebagai info).

---

## 5. PEMERIKSAAN BERULANG

### Putaran baca-1 (sebelum test)

**classify_day_label:** terikat lock via `RATIO_PATH_THRESHOLD`/`RANGE_ATR_THRESHOLD`. Benar.
**compute_london_drift_4h:** grain broker-day store (`prepare_bars`), jendela 16 bar `is_london` pertama (session_flags, DST-aware), formula close-terakhir − open-pertama, `london_drift_norm = drift / atr_14_d1` index sama + guard provenans terhadap referensi dari **file store terpisah**. Benar.
**compute_gap_f2_flag:** grain broker-day, `m1_bars < 15` ∧ bukan bucket tepi. Benar.
**compute_rv_regime_flag:** rv_score = rv_roll_20d/20, flag = 1[rv_score > TAU_2023], NaN warmup dipertahankan. Benar.
**quarantine_mask:** predikat eksplisit 19 hari, dtype bool murni. Benar.
**register_h2_strategy:** jam 15 UTC, 1x, satuan harga JPY. Benar.
**Guard provenans ATR:** `allclose` vs deret referensi yang DIBACA ULANG dari store parquet (`_read_atr_reference_from_store`), toleransi eksplisit; klausa tautologis batch-2 dihapus, jalur produksi `main()` memakai sumber terpisah. Benar.

### Putaran baca-2 (setelah suite hijau) — rc + cakupan eksplisit

```
venv    pytest penuh                  : 254 passed in 19.35s        rc=0  (repo)
venv    pytest test_build_labels.py   : 60 passed                   rc=0  (file)
.venv   pytest penuh                  : 254 passed in 17.93s        rc=0  (repo)
venv    ruff check .                  : All checks passed!          rc=0  (repo)
venv    ruff format --check .         : 37 files already formatted  rc=0  (repo)
.venv   ruff check .                  : All checks passed!          rc=0  (repo)
.venv   ruff format --check .         : 9 files would be reformatted rc=1 (repo;
        9 PRA-ADA di luar scope: 6 notebook EDA + reaudit-adversarial +
        reaudit-ketiga + build_features.py yang BEKU)
.venv   ruff format --check <file batch-4> : rc=0 (build_labels.py, test_build_labels.py,
        protokol, laporan batch-3, laporan ini)*
check_foreign_chars                   : 16 passed                   rc=0  (repo)
3 hash artefak lama                   : identik                     rc=0
git staged                            : 0
D4 byte-reprodusibel 2×               : True (venv run1=run2=disk)
```

\* Catatan toolchain (DISIPLIN 10–11): `ruff format --check` **repo** dengan
ruff 0.6.9 (venv) = rc=0 karena 0.6.9 hanya menemukan berkas Python; ruff
0.16.10 (.venv) juga mem-format blok `python` di `.md`/`.ipynb` sehingga
rc=1 repo. Untuk `.md`, rc per-file hanya bermakna pada 0.16.10; D1/D2
diukur rc=0 pada KEDUA ruff.

**Koreksi #31 (dipertahankan):** batch-2 menulis "Pytest penuh: 36 passed"
padahal output mentahnya hanya memuat 1 berkas. Nilai batch-3: **248 total /
54 baru**; batch-4: **254 total / 60 baru**.

### Putaran silang (ambang di kode vs di protokol)

| Ambang di kode | Sumber | Status |
|----------------|--------|--------|
| `RATIO_PATH_THRESHOLD = 0.0268` | hipotesis_lock_v1.md §H1 | COCOK |
| `RANGE_ATR_THRESHOLD = 88.79` | hipotesis_lock_v1.md §H1 | COCOK |
| `LONDON_FIRST_N = 16` | kontrak Q2-b + putusan C | COCOK |
| `M1_BARS_MIN = 15` | definisi Q3(a) | COCOK |
| `RV_WINDOW_DAYS = 20` | putusan Q4-ii; dikunci test DATA | COCOK (terkunci) |
| `TAU_2023 = 2.5951672079821496e-05`, AUC `0.8173755150499336`, n_B 111, n_A 129 | protokol §2 hasil kalibrasi Q1(a) | COCOK |
| `ATR_PROVENANCE_RTOL/ATOL = 1e-9` | putusan B butir 3 | COCOK |
| `ANOMALY_WINDOWS` | putusan F-1 butir 2 | COCOK |

### Putaran akhir (verifikasi DILARANG)

Semua DILARANG §3 diverifikasi satu per satu dengan bukti di §4 (status apa
adanya, termasuk pengakuan pelanggaran batch-2 pada klaim "tanpa stage" yang
sudah diperbaiki).

---

## 6. SELF-AUDIT 3×

### Putaran 1 — Correctness

- D1: setiap fungsi ≤ 50 baris AST (terpanjang `main` = 40); modul 399 baris
  (pagu 400).
- D2: 60 test; bukti mutasi memakai binding lokal (`HERE`) dan terbukti merah
  saat fungsi dicabut (7 merah `guard_noop`); fixture jendela London sensitif
  (N=4/8/60 merah) + test N=60 dengan 70 bar (60 bar PERTAMA ≠ ambil-semua);
  tidak ada test `pass`.
- D3: TAU/AUC/n per kelas angka riil; kutipan F1 baris 73-75 + path
  `arsitek/`; angka gap 234/597; penguncian `RV_WINDOW_DAYS` via test DATA.
- D4: 974 baris broker-day, row key `date_broker`, `day_label` tanpa None,
  mask bool murni, NaN norm 14 (warmup ATR), byte-reprodusibel 2× + identik
  lintas nilai dengan build toolchain lain (§8.11).
- D5: hash diukur sesudah penulisan terakhir; angka test dari output mentah.

### Putaran 2 — Bias & Asumsi

- Klaim "guard diperkuat" diuji **pada jalur produksi** `main()`: baseline
  NO RAISE + **9/9 sabotase RAISED** (`1.0`, `2.0`, `88.79`, `100.0`,
  `12345.6`, `1e6`, `close-avg`, `1e-3`, `-5.0`) — 10/10 klaim cocok
  (batch-3 hanya 3/10; re-audit ketiga §3.2).
- Klaim "test mengunci bug nyata" diuji: mutasi `reference_sama_frame`
  (mengembalikan referensi ke kolom frame yang sama — bug batch-3) → **3 merah**
  pada `TestGuardProvenansJalurProduksi`.
- Klaim "bukti mutasi sahih": 6 mutan in-memory (`guard_noop` 7 merah,
  `reference_sama_frame` 3, `rv_window_10` 1, `london_n_60` 7, `classify`,
  `quarantine`), baseline hijau.
- Klaim "234 hari" tidak dipakai sebagai pembenar: recount independen pada
  grain tunggal = 234/597 karena datanya begitu; 479 ditolak sebagai artefak.
- Klaim hash dicek ulang dengan `git hash-object` setelah penulisan terakhir.

### Putaran 3 — Meta-check

- Read-only terhadap file lama: hash 3 artefak lama diukur ulang, identik.
- Tidak menulis kode produksi selain D1/D2; nol commit; indeks git bersih dari
  stage.
- Nol vonis H3/H4/H5; status BELUM DIUJI dipertahankan di protokol §2/§4.
- Nol backtest; `h2_trades` tetap spesifikasi.

---

## 7. POTENSIAL MASALAH & SARAN

1. **H3 tetap BELUM DIUJI.** TAU_2023 = 2.5951672079821496e-05 menandai
   162/240 hari span 2023 (B 111/111, A 51/129) — flag rate tinggi; vonis H3
   menunggu S4 (uji drawdown vs strategi diagnostik), bukan diputus di sini.
2. **`gap_f2_flag` 234 hari masih tanpa uji materialitas H1/H5** — status
   BELUM DIUJI; eksklusi buta tetap dilarang.
3. **Varian BATAS SESI** pada grain broker-day memberi 578 bucket/230 hari —
   dilaporkan sebagai sensitivitas di protokol §4; definisi resmi tetap
   Q3(a) BATAS HARI.
4. **Non-repro lintas toolchain (bukan cacat).** D4 disk dibangun venv
   (pandas 2.2.3/pyarrow 17.0.0); build .venv (pandas 3.0.6/pyarrow 25.0.1)
   memberi byte berbeda, **nilai semua kolom identik** (per kolom 6/6 + 10/10,
   index elemen-ke-elemen True; `.equals` False hanya karena unit ns vs ms).
   Dicatat agar tidak dibaca sebagai non-determinisme pipeline (DISIPLIN 11).
5. 4 modifikasi tracked lama (`.ai/AGENTS.md`, `.ai/SESSION_LOG.md`,
   `.ai/assistant/README.md`, `requirements.txt`) dan 21 penghapusan laporan
   EDA bukan milik batch ini; dibiarkan apa adanya (tidak di-stage ulang,
   tidak di-revert).

---

## 8. LAMPIRAN: OUTPUT MENTAH

### 8.1 Pytest penuh (repo) — venv

```
platform win32 -- Python 3.12.8, pytest-8.3.3, pluggy-1.6.0
rootdir: D:\ANN
configfile: pyproject.toml
plugins: anyio-4.15.1, platformdirs-4.12.3, cov-5.0.0
collected 254 items

============================ 254 passed in 19.35s =============================
```

Cross-toolchain (env auditor, pandas 3.0.6):

```
platform win32 -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0
collected 254 items

============================ 254 passed in 17.93s =============================
```

### 8.2 Per-berkas

```
pytest --collect-only -q                            -> 254 tests collected in 0.50s
pytest --collect-only -q tests/test_build_labels.py  -> 60 tests collected in 0.45s
```

### 8.3 Ruff (rc + cakupan)

```
venv   ruff 0.6.9    check .            -> All checks passed!             rc=0 (repo)
venv   ruff 0.6.9    format --check .   -> 37 files already formatted     rc=0 (repo)
.venv  ruff 0.16.10  check .            -> All checks passed!             rc=0 (repo)
.venv  ruff 0.16.10  format --check .   -> 9 files would be reformatted,
                                           189 files already formatted    rc=1 (repo)
```

9 file gagal 0.16 format — **seluruhnya pra-ada dan di luar scope batch-4**:

```
notebooks\scalping\eda_00_setup.ipynb:cell 12:11:61
notebooks\scalping\eda_01_returns.ipynb:cell 2:33:8
notebooks\scalping\eda_02_volatility.ipynb:cell 2:41:8
notebooks\scalping\eda_03_autocorr.ipynb:cell 2:41:8
notebooks\scalping\eda_04_swings_levels.ipynb:cell 2:41:8
notebooks\scalping\eda_05_regimes.ipynb:cell 2:40:8
reports\governance\2026-10-07\Audit\reaudit-adversarial-D1-D5.md:165:36
reports\governance\2026-10-07\Audit\reaudit-ketiga-batch3-D1-D5.md:165:48
src\features\build_features.py:326:32
```

`build_labels.py:149` (kegagalan batch-3, re-audit ketiga §8.2) **tidak lagi
ada di daftar** — D1 kini rc=0 di kedua ruff, begitu pula D2 dan seluruh
berkas `.md` yang ditulis batch-4 (diukur per-file dengan 0.16.10, rc=0).
`build_features.py` BEKU (hash `399e64b3…`) sehingga kegagalannya tidak boleh
dan tidak diperbaiki di batch ini.

### 8.4 check_foreign_chars

```
tests\test_check_foreign_chars.py ................                       [100%]
16 passed in 0.05s
```

### 8.5 Hash (mentah)

```
git hash-object src/features/build_labels.py
2561efd552544feeb9af0b6733711015b83f43dd
git hash-object tests/test_build_labels.py
dc07a7e651d38f07a5cabbe4e693b10681312d25
git hash-object reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
bc17e5de6cfefb355fe7418acd2a3a0d8b461212
git hash-object reports/governance/2026-10-07/coder/laporan-fix-batch3-D1-D5.md
b5a9d2a8776915896eeeea65a4d7074d7e2d8981

git hash-object data/labels/usdjpy_day_labels.parquet data/labels/usdjpy_h2_trades.parquet
a01694e3eafafa9c9e2e14ca3d8396706b4f2857
7138325d278283056d09974cbf93fddbb2926b40

git hash-object src/features/build_features.py tests/test_build_features.py data/features/M15/usdjpy_m15_features.parquet
399e64b372e430b6def79b4fa8324a4e8e629918
ed7ac43520c4431519d4d7065504866ae9b3ad95
07402f40478aaed9391203f5db3237d636f5a959
```

### 8.6 D4 (produksi) — kontrak, grain, byte-reprodusibel

```
usdjpy_day_labels.parquet  sha256=47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c bytes=29121
usdjpy_h2_trades.parquet   sha256=32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f bytes=7837
day rows: 974 index: date_broker cols: ['day_label', 'london_drift_4h', 'london_drift_norm', 'gap_f2_flag', 'rv_regime_flag', 'quarantine_mask']
trades rows: 1 cols: ['symbol', 'strategy', 'entry_rule', 'exit_rule', 'sl_atr', 'tp', 'biaya', 'entry_time_utc', 'entry_frequency', 'price_unit']
day_label counts: {'trending': 330, 'range': 324, 'normal': 320}   # nol None
quarantine_mask dtype: bool  True count: 19
drift NaN: 0   norm NaN: 14   gap flagged: 234   rv NaN: 19/974
BYTE-IDENTIK run1 vs run2 vs disk: True (kedua file)
```

Byte-reprodusibilitas juga dikunci sebagai test tetap:
`TestMainEndToEnd::test_d4_deterministik_byte_identik`.

### 8.7 SABOTASE GUARD PADA JALUR PRODUKSI `main()` (batch-4 butir 1)

Patch `bl.daily_metrics` → kolom `atr_14_d1`, lalu `bl.main()` dijalankan apa
adanya (referensi provenans = store parquet yang dibaca ulang):

```
baseline                         -> NO RAISE
baseline sha256 usdjpy_day_labels.parquet: 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c
baseline sha256 usdjpy_h2_trades.parquet: 32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f
1.0                              -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
2.0                              -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
88.79                            -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
100.0                            -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
12345.6                          -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
1e6                              -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
close-avg                        -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
1e-3                             -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
-5.0                             -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) - putusan B
```

**10/10 klaim cocok** (batch-3: 3/10 karena `main()` mengirim
`atr_reference = daily['atr_14_d1']`). Baseline juga membuktikan output D4
tidak berubah oleh perbaikan referensi (sha256 = disk). Catatan encoding:
konsol Windows menampilkan em dash sebagai `?`; byte berkas sumber UTF-8 valid.

### 8.8 Bukti mutasi suite (in-memory, patch binding modul + globals test)

```
MUT=none                  -> exit=0 | ============================= 60 passed in 10.48s =============================
MUT=guard_noop            -> exit=1 | ========================= 7 failed, 53 passed in 10.96s ========================
MUT=reference_sama_frame  -> exit=1 | ========================= 3 failed, 57 passed in 11.00s ========================
MUT=rv_window_10          -> exit=1 | ========================= 1 failed, 59 passed in 10.40s ========================
MUT=london_n_60           -> exit=1 | ========================= 7 failed, 53 passed in 10.42s ========================
```

Nama test yang merah (butir §11 yang dikunci):

```
MUT=guard_noop            : TestGuardProvenansAtr::test_sabotase_pembagi_meledak[3 kasus]
                            TestGuardProvenansAtr::test_guard_unit_membedakan_deret
                            TestGuardProvenansJalurProduksi::test_sabotase_produksi_meledak[3 kasus]
MUT=reference_sama_frame  : TestGuardProvenansJalurProduksi::test_sabotase_produksi_meledak[3 kasus]
MUT=rv_window_10          : TestRvRegimeFlag::test_rv_window_terikat_kalibrasi_ulang
MUT=london_n_60           : Termasuk TestJendelaLondonLock::test_n60_mengambil_60_bar_pertama_bukan_ambil_semua
```

### 8.9 Pagu & AST D1 (mentah)

```
baris fisik D1 : 399
main            : 40
terpanjang      : ('main', 40)
semua <=50      : True
tests/test_build_labels.py : 713 baris (60 test)
```

### 8.10 git status (sesudah semua penulisan)

```
     21  D
      4  M
     66 ??
total: 91      staged: 0      HEAD: e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
```

### 8.11 Toolchain & D4 lintas versi (batch-4 butir 4)

```
venv   : python=3.12.8  pandas=2.2.3  pyarrow=17.0.0  numpy=1.26.4
.venv  : python=3.12.13 pandas=3.0.6  pyarrow=25.0.1  numpy=2.5.3

rebuild venv run1 : day sha256=47d15c41... bytes=29121 | trades sha256=32eaf6b2... bytes=7837
rebuild venv run2 : day sha256=47d15c41... bytes=29121 | trades sha256=32eaf6b2... bytes=7837
sha256 DISK       : day sha256=47d15c41... bytes=29121 | trades sha256=32eaf6b2... bytes=7837
run1==run2 IDENTIK (kedua file) ; run1==disk IDENTIK (kedua file)

rebuild .venv     : day sha256=20cf4cdd720e620af4d01d44e557cc5c43c0ee73a5c361b99fe7fa704fc81899 bytes=27292
                    trades sha256=75938ad32bf35a209428ab449839b7331fba23a6c6c097214b1d621766bc6aa5 bytes=6766

per kolom (disk vs .venv): day_label OK, london_drift_4h OK, london_drift_norm OK,
    gap_f2_flag OK (int32 vs int64), rv_regime_flag OK, quarantine_mask OK
-> SEMUA KOLOM IDENTIK NILAINYA: True   (trades 10/10 OK: True)
index: elemen == elemen True ; setara setelah cast-ns True ; Index.equals apa adanya False (ns vs ms)
```

Hash build `.venv` (`20cf4cdd…` / `75938ad3…`) **identik dengan rebuild yang
dilaporkan re-audit ketiga §8.4** — reproduksi independen lintas sesi.

---

## 9. BATCH-4 — PETA 5 BUTIR §11 RE-AUDIT KETIGA → BUKTI

| Butir §11 | Status | Bukti mentah |
|---|---|---|
| 1. [BLOCKING] `atr_reference` dari sumber terpisah + sabotase jalur produksi | **TERTUTUP** | D1 `_read_atr_reference_from_store` dipanggil `main()` baris 377-378 (baca store parquet, file terpisah); §8.7 (10/10 cocok: baseline NO RAISE, 9 RAISED), §8.8 (`reference_sama_frame` → 3 merah), fixture `_guard_fixture` dari store parquet, `TestGuardProvenansJalurProduksi` |
| 2. [MEDIUM] format L149 + klaim gate rc+cakupan | **TERTUTUP** | §8.3: D1/D2 rc=0 di kedua ruff; `build_labels.py:149` hilang dari daftar gagal; D5 klaim rc+cakupan eksplisit (repo vs file) + 9 pra-ada didaftarkan |
| 3. [MEDIUM] `RV_WINDOW_DAYS` terikat kalibrasi | **TERTUTUP** | §8.8 `rv_window_10` → 1 merah pada `test_rv_window_terikat_kalibrasi_ulang` (TAU dihitung ulang dari data store, bukan konstanta-vs-konstanta) |
| 4. [LOW] D4 / toolchain | **TERTUTUP** | §8.11: rebuild venv 2× byte-identik + identik disk; versi kedua toolchain dicatat; nilai semua kolom identik lintas toolchain; status non-repro-lintas-pyarrow eksplisit |
| 5. [LOW] fixture N>32 | **TERTUTUP** | §8.8: `make_london_rising(step_minutes=…)`; `test_n60_mengambil_60_bar_pertama_bukan_ambil_semua` (70 bar, drift 0.64 = 60 bar pertama ≠ 0.74 ambil-semua) merah saat `london_n_60` |

---

**END OF REPORT**
