# Laporan Fix Batch Keempat D1–D5 — penutup 5 butir §11 re-audit ketiga

**Tanggal:** 2026-10-08
**Peran:** Coder. Mengerjakan **hanya 5 butir §11** re-audit ketiga (mandat sempit);
tidak ada scope tambahan, tidak ada vonis, tidak ada backtest.
**Hasil:** seluruh 5 butir **TERTUTUP** dengan bukti mentah (§1 peta, §2–§6 detail,
§9 peta klaim).

## 0. Sumber wajib yang dibaca penuh (hash git blob, terukur di sesi ini)

| Sumber | git blob terukur |
|---|---|
| `Audit/reaudit-ketiga-batch3-D1-D5.md` (sumber tunggal + §3/§8/§11) | `673ffb151f4453a86e7a9b031eb35e6fdad2bbf4` |
| `arsitek/putusan-adjudikasi-reaudit-kedua.md` (§B butir 4 mengikat) | `295303a46dfd9dd3b0b047a0b931895e7fd2eed3` |
| `arsitek/putusan-arsitek-fix-D1-D5.md` (Q1–Q4; fix:86-87 dicabut) | `ca57e7647e955ee0dfe68579db5dbef6216a427b` |
| `coder/laporan-fix-batch3-D1-D5.md` (basis; di-patch 5 butir, bukan rewrite) | basis `ba5ab603a5b2d24a483dac8ec1a95bd7f4e6f554` → sesudah patch `b5a9d2a8776915896eeeea65a4d7074d7e2d8981` |
| `.ai/assistant/PROMPT_DISIPLIN.md` butir 9–12 | `37522027cec5021373495845619756e01527850b` |

Larangan lama dipatuhi: nol sentuh 3 artefak lama (`399e64b3…`/`ed7ac435…`/
`07402f40…` identik), impor satu arah, **nol commit/stage**, pagu 400/50, nol
vonis H3/H4/H5, nol backtest.

## 1. ARTEFAK YANG DITULIS + HASH (diukur SESUDAH penulisan terakhir)

| Artefak | Hash git blob / sha256 | Keterangan |
|---|---|---|
| `src/features/build_labels.py` | `2561efd552544feeb9af0b6733711015b83f43dd` | D1: referensi provenans dari store terpisah; **399 baris**, `main` AST 40 |
| `tests/test_build_labels.py` | `dc07a7e651d38f07a5cabbe4e693b10681312d25` | D2: **713 baris, 60 test** |
| `reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md` | `bc17e5de6cfefb355fe7418acd2a3a0d8b461212` | D3: + penguncian data `RV_WINDOW_DAYS`; 298 baris |
| `reports/governance/2026-10-07/coder/laporan-final-fase1.md` | `345308540d27c38534b77cdcd278e32eb15735ec` | D5: angka + klaim gate rc/cakupan diperbarui (488 baris) |
| `reports/governance/2026-10-07/coder/laporan-fix-batch3-D1-D5.md` | `b5a9d2a8776915896eeeea65a4d7074d7e2d8981` | laporan batch-3 + patch 5 butir (§7) |
| `data/labels/usdjpy_day_labels.parquet` | sha256 `47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c` (29121 B) | git blob `a01694e3eafafa9c9e2e14ca3d8396706b4f2857`; **tidak ditulis ulang** (rebuild byte-identik) |
| `data/labels/usdjpy_h2_trades.parquet` | sha256 `32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f` (7837 B) | git blob `7138325d278283056d09974cbf93fddbb2926b40` |
| laporan ini | mustahil di-embed konsisten; diukur setelah penulisan terakhir dan dilaporkan di pesan penutup | — |

## 2. BUTIR 1 [BLOCKING] — REFERENSI TERPISAH + SABOTASE JALUR PRODUKSI

### 2.1 Akar masalah (re-audit ketiga §3.2–§3.5)

Batch-3 `main()` mengirim `atr_reference = daily['atr_14_d1']` — kolom yang
sama dengan pembagi → guard mengevaluasi `allclose(X, X)`, benar untuk setiap
X. Terukur di produksi: 3/10 (yang diputus wajib meledak justru lolos).

### 2.2 Perbaikan (D1)

- Fungsi baru `_read_atr_reference_from_store(path)` **membaca ulang file
  store parquet B1** (`date_broker`, `atr_14_d1`), `groupby(...).last()` →
  `shift(-1)` (invers attach anti-look-ahead `daily.shift(1)`
  build_features) — bukan kolom dari frame pembagi.
- `main()` baris 377–378: `store_path = FEATURES_DIR / "M15" / {...}` →
  `atr_reference = _read_atr_reference_from_store(store_path)`; disertai
  assert keselarasan hari (`atr_reference.index.equals(daily.index)`) sebelum
  reindex. Fungsi pengganti batch-3 yang lama (rekonstruksi dari M15)
  **dihapus** — sumbernya harus file store.
- Fixture test `_guard_fixture(tmp_path)` diperbaiki: referensi ditulis ke
  parquet store semu (mekanisme attach `shift(1)`) lalu **dibaca ulang** —
  mensabotase kondisi produksi (referensi ikut dari sumber terpisah), BUKAN
  snapshot daily sebelum sabotase (re-audit ketiga §3.4).

### 2.3 Bukti pada JALUR PRODUKSI persis `main()` (output mentah)

Patch `bl.daily_metrics` → kolom `atr_14_d1`, lalu `bl.main()` dijalankan
apa adanya (bukan harness yang menyusun ulang langkah):

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

**10/10 klaim cocok** (re-audit ketiga: 3/10). Tiga kasus yang diputus
adjudikasi §B butir 4 (`1.0`, `88.79`, `close-avg`) semuanya RAISED; baseline
NO RAISE dan sha256 output = disk. Konsol Windows menampilkan em dash sebagai
`-`/`?` (artefak konsol; byte sumber UTF-8 valid).

### 2.4 Kunci suite (bukan hanya harness)

Test baru `TestGuardProvenansJalurProduksi` (fixture module-scope `prod_guard_frames`
memuat m15/m1/daily + referensi dari store terpisah) dengan
`_build_daily_labels(m15, daily, reference)` — panggilan yang sama dipakai
`main()`: 1 baseline lolos + 3 sabotase parametrized (`1.0`, `88.79`,
close-avg) RAISE. `TestGuardProvenansAtr` (fixture sintetis) kini memakai
store parquet terpisah juga.

## 3. BUTIR 2 [MEDIUM] — FORMAT + KLAIM GATE rc/CAKUPAN

- D1 `:149` (satu-satunya kegagalan format tulisan batch-3) diperbaiki dengan
  bentuk variabel pesan; D1/D2 kini **rc=0 di kedua ruff** (check + format).
- Dua blok `python` di laporan batch-3 yang gagal 0.16 juga ditulis ulang
  (§7) → seluruh berkas `.md` coder kini rc=0 di 0.16, dan repo-wide 0.16
  turun **10 → 9** file gagal (semuanya pra-ada/luar scope).
- Klaim gate D5 §8.3 diperbarui: **rc + cakupan eksplisit** (repo vs file),
  9 kegagalan pra-ada didaftarkan dengan nama, dan catatan bahwa `.md`
  per-file hanya bermakna pada ruff 0.16.10.

## 4. BUTIR 3 [MEDIUM] — `RV_WINDOW_DAYS` TERIKAT KALIBRASI (DATA)

Test baru `TestRvRegimeFlag::test_rv_window_terikat_kalibrasi_ulang`
menghitung ULANG TAU Youden dari kolom `rv_roll_20d` store (span terkunci
2023-01-01..12-31, B=Jan–Jun, A=Jul–Des, aturan `>`) memakai jendela kode dan
membandingkannya dengan `TAU_2023` + `CALIB_N_B`/`CALIB_N_A`. Bukan
konstanta-vs-konstanta (DISIPLIN 12). Bukti merah saat jendela diubah:

```
MUT=rv_window_10          -> exit=1 | 1 failed, 59 passed in 10.40s
FAILED tests/test_build_labels.py::TestRvRegimeFlag::test_rv_window_terikat_kalibrasi_ulang
```

## 5. BUTIR 4 [LOW] — D4 / TOOLCHAIN

Versi terukur: venv = python 3.12.8 / pandas 2.2.3 / pyarrow 17.0.0 /
numpy 1.26.4; .venv = python 3.12.13 / pandas 3.0.6 / pyarrow 25.0.1 /
numpy 2.5.3.

```
rebuild venv run1 : day=47d15c41... (29121 B) | trades=32eaf6b2... (7837 B)
rebuild venv run2 : day=47d15c41... (29121 B) | trades=32eaf6b2... (7837 B)
sha256 DISK       : day=47d15c41... (29121 B) | trades=32eaf6b2... (7837 B)
run1==run2 IDENTIK (cmp) ; run1==disk IDENTIK (cmp)
rebuild .venv     : day=20cf4cdd720e620af4d01d44e557cc5c43c0ee73a5c361b99fe7fa704fc81899 (27292 B)
                    trades=75938ad32bf35a209428ab449839b7331fba23a6c6c097214b1d621766bc6aa5 (6766 B)
```

Nilai **per kolom** (disk/venv vs build .venv) — seluruhnya identik:

```
day_label OK | london_drift_4h OK | london_drift_norm OK | gap_f2_flag OK (int32 vs int64)
rv_regime_flag OK | quarantine_mask OK   -> SEMUA KOLOM IDENTIK NILAINYA: True
trades: 10/10 kolom OK                    -> SEMUA KOLOM IDENTIK NILAINYA: True
index: elemen == elemen True ; setara setelah cast-ns True ; Index.equals apa adanya False (ns vs ms)
```

Hash `.venv` (`20cf4cdd…`/`75938ad3…`) identik dengan rebuild yang dilaporkan
re-audit ketiga §8.4 — reproduksi independen. Status dinyatakan eksplisit:
**non-repro lintas toolchain** (perbedaan metadata parquet), BUKAN
non-determinisme pipeline; D4 di disk tetap hasil venv (byte-repro 2×).

## 6. BUTIR 5 [LOW] — FIXTURE N>32

`make_london_rising` kini menerima `step_minutes`; test baru
`TestJendelaLondonLock::test_n60_mengambil_60_bar_pertama_bukan_ambil_semua`
memakai **70 bar London** (grid 5 menit, 07:00–12:45 UTC) dan mengunci:
N=16 → drift 0.20, N=60 → 0.64 (= 60 bar PERTAMA, `0.05 + 0.01*59`), dan
**≠ 0.74** (ambil-semua 70). Merah saat `london_n_60` (§8).

## 7. PATCH LAPORAN BATCH-3 (5 butir saja — DILARANG rewrite)

Patch berupa catatan **KOREKSI BATCH-4** yang menempel di klaim lama (klaim
lama tidak dihapus, statusnya dikoreksi):

| Butir §11 | Lokasi patch di laporan batch-3 | Isi |
|---|---|---|
| 1 | §1 tabel syarat-5 + §6.3 | klaim "9 sabotase lewat pipeline" BATAL (3/10); akar masalah + perbaikan + bukti batch-4 |
| 2 | §9.3 | klaim `exit=0` salah untuk 0.16.10 (rc=1, 10 file, termasuk `build_labels.py:149`); sesudah patch rc=0 per-file |
| 3 | §5 | penguncian batch-3 konstanta-vs-konstanta bukan penguncian; test DATA ditambahkan |
| 4 | §9.7 | versi toolchain + status non-repro lintas pyarrow; nilai kolom identik |
| 5 | §11 putaran 2 | batas "N=60 memakai 32 bar" ditutup oleh fixture 70 bar batch-4 |

Dua blok kode `python` di laporan itu yang gagal format 0.16 ikut ditulis
ulang (bagian dari patch butir 1/2); hasil: file rc=0 di 0.16 dan rep-wide
0.16 turun 10 → 9 file gagal.

## 8. GATE §3 — OUTPUT MENTAH (rc + cakupan)

```
venv    pytest penuh                  : 254 passed in 19.35s         rc=0  (repo)
venv    pytest test_build_labels.py   : 60 passed                    rc=0  (file)
.venv   pytest penuh                  : 254 passed in 17.93s         rc=0  (repo, pandas 3.0.6)
venv    pytest --collect-only -q      : 254 tests collected in 0.50s rc=0
venv    pytest --collect-only -q tests/test_build_labels.py : 60 tests collected in 0.45s
venv    ruff 0.6.9    check .         : All checks passed!           rc=0  (repo)
venv    ruff 0.6.9    format --check .: 37 files already formatted   rc=0  (repo)
.venv   ruff 0.16.10  check .         : All checks passed!           rc=0  (repo)
.venv   ruff 0.16.10  format --check .: 9 files would be reformatted,
                                        189 files already formatted  rc=1  (repo)
venv    check_foreign_chars           : 16 passed in 0.05s           rc=0  (repo)
3 hash artefak lama                   : 399e64b3 / ed7ac435 / 07402f40 (identik)
git staged                            : 0          HEAD: e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
git status                            : 21 D / 4 M / 66 ??  (total 91)
D4 byte-repro 2x (se-toolchain)       : True + identik disk (§5)
```

9 file gagal 0.16 format — seluruhnya pra-ada/luar scope (6 notebook EDA,
`reaudit-adversarial-D1-D5.md`, `reaudit-ketiga-batch3-D1-D5.md`,
`build_features.py` yang BEKU). **Nol** file yang ditulis batch-4 ada di
daftar itu. Notasi cakupan: `ruff format --check .` **repo** dengan 0.6.9
tidak memindai `.md`/`.ipynb`, sehingga rc=0; untuk `.md` rc per-file diukur
dengan 0.16.10 (semua rc=0).

AST D1 (mentah):

```
baris fisik D1 : 399
main            : 40
terpanjang      : ('main', 40)
semua <=50      : True
```

## 9. PETA KLAIM → OUTPUT MENTAH

| Klaim | Output mentah |
|---|---|
| Referensi dari store terpisah (D1 `main()` L377-378) | §2.2 + hash D1 §1 |
| Baseline NO RAISE + sha256 = disk | §2.3 |
| 9/9 sabotase RAISED (10/10 klaim cocok) | §2.3 |
| Kunci suite: `reference_sama_frame` → 3 merah | §10 (mutasi) |
| D1/D2 rc=0 di kedua ruff; repo 0.16 10→9 | §3, §8 |
| `RV_WINDOW_DAYS` merah saat 20→10 (1 test) | §4 |
| D4 byte-repro 2× + nilai per kolom identik lintas toolchain | §5 |
| Fixture 70 bar: N=60 = 60 bar pertama | §6, §10 |
| D2 60 test / 713 baris; D1 399 baris, main AST 40 | §1, §8 |
| staged 0; 3 hash lama identik | §8 |

## 10. BUKTI MUTASI SUITE (in-memory, patch binding modul + globals test)

```
MUT=none                  -> exit=0 | 60 passed in 10.48s
MUT=guard_noop            -> exit=1 | 7 failed, 53 passed in 10.96s
MUT=reference_sama_frame  -> exit=1 | 3 failed, 57 passed in 11.00s
MUT=rv_window_10          -> exit=1 | 1 failed, 59 passed in 10.40s
MUT=london_n_60           -> exit=1 | 7 failed, 53 passed in 10.42s
```

Nama test merah (yang mengunci butir §11):

```
MUT=guard_noop            : TestGuardProvenansAtr::test_sabotase_pembagi_meledak[3 kasus]
                            TestGuardProvenansAtr::test_guard_unit_membedakan_deret
                            TestGuardProvenansJalurProduksi::test_sabotase_produksi_meledak[3 kasus]
MUT=reference_sama_frame  : TestGuardProvenansJalurProduksi::test_sabotase_produksi_meledak[3 kasus]
MUT=rv_window_10          : TestRvRegimeFlag::test_rv_window_terikat_kalibrasi_ulang
MUT=london_n_60           : TestLondonDrift4h (4 test), TestJendelaLondonLock::test_konstanta_terkunci_16,
                            TestJendelaLondonLock::test_n60_mengambil_60_bar_pertama_bukan_ambil_semua,
                            TestGuardProvenansAtr::test_baseline_pembagi_kolom_store_lolos
```

`reference_sama_frame` adalah mutasi yang MENGEMBALIKAN bug batch-3
(referensi = kolom frame yang sama): tepat 3 test produksi MERAH — suite kini
menangkap cacat yang dulu luput.

## 11. SELF-AUDIT 3× (ala auditor)

**Putaran 1 — Correctness.** Setiap butir §1 menunjuk output mentah:
butir 1 → §2.3/§2.4/§10; butir 2 → §3/§8 (rc + cakupan + daftar 9 file);
butir 3 → §4/§10; butir 4 → §5 (sha256 + versi + per kolom); butir 5 →
§6/§10. Tidak ada klaim tanpa eksekusi; angka mutasi berasal dari run pytest
dengan patching terbukti (baris `PATCH …` ikut terekam).

**Putaran 2 — Bias & asumsi.** Klaim coder diperlakukan sebagai hipotesis dan
diuji pada arah yang tidak menguntungkan: (i) "referensi terpisah" diuji
dengan mengembalikan bug lama (`reference_sama_frame` → 3 merah); (ii) "10/10
sabotase" diuji pada `main()` nyata, bukan potongan; (iii) "jendela terkunci"
diuji dengan mutasi 20→10; (iv) "byte-repro" diuji 2× dan LINTAS toolchain —
perbedaan byte diakui (metadata) dan nilai dibuktikan per kolom; (v) "fixture
N>32" diuji dengan 70 bar dan dibedakan dari ambil-semua. Batas yang tidak
ditutup tetap ditulis: materialitas `gap_f2_flag` pada 234 hari (BELUM DIUJI),
vonis H3/H4/H5.

**Putaran 3 — Meta-check.** Read-only terhadap 3 artefak lama (hash identik);
nol commit; indeks tanpa entri staged; nol backtest; `h2_trades` tetap
spesifikasi; nol vonis; impor satu arah; scratch di luar repo
(`…\Temp\b4\`); D4 tidak ditulis ulang (rebuild byte-identik).

## 12. YANG TIDAK DIKERJAKAN (bukan mandat batch ini)

1. Vonis H3/H4/H5 dan backtest — dilarang.
2. Materialitas `gap_f2_flag` pada 234 hari (uji H1/H5) — status BELUM DIUJI.
3. Perbaikan 9 kegagalan format pra-ada (notebook EDA, 2 berkas audit,
   `build_features.py` beku) — di luar scope.

**END OF REPORT**
