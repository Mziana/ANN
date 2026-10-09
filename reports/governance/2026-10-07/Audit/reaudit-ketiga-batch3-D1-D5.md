# RE-AUDIT KETIGA — BATCH-3 D1–D5 (2026-10-08)

Auditor:Asisten (peran auditor adversarial — tidak menulis kode produksi).
Dasar singkat: `reports/governance/2026-10-07/Audit/reaudit-adversarial-D1-D5.md` blob
`c608f793be40a57c0ead8b1901efa5745dff03cd`.
Mandat: re-audit ketiga atas klaim batch-3 secara read-only terhadap worktree.
Read-only total dipatuhi: satu-satunya file yang ditulis adalah laporan ini.

---

## 0. RINGKASAN EKSEKUTIF

Batch-3 menutup majority temuan re-audit kedua secara nyata dan terukur. Grain
tunggal broker-day benar-benar terbentuk, rekonsiliasi gap A bersih bucket-per-bucket,
kalibrasi Q1(a) tereproduksi bit-perfect, dan 4 hash kontrak cocok.

Namun **Lubang 1 / blocking 2 (putusan B) TIDAK tertutup**. Guard provenans yang
diperkenalkan batch-3 membandingkan `daily["atr_14_d1"]` terhadap `daily["atr_14_d1"]`
— deret yang sama pada jalur produksi `main()`. Klaim "9 sabotase RAISED" benar
hanya untuk harness yang mengirim `atr_reference` berbeda dari kolom yang disabotase;
ketika sabotase diarahkan ke jalur produksi seperti `main()` memanggilnya, **7 dari 9
sabotase LOLOS**, termasuk ketiga kasus yang diputus wajib meledak (`1.0`, `88.79`,
`close-avg`).

Ada satu klaim dokumen yang salah: `ruff format --check .` claimed exit=0 / "37
files already formatted", sedangkan D1 yang ditulis batch-3 sendiri gagal
`ruff format --check`.

**VERDICT: GAGAL** — syarat B-4 (putusan adjudikasi §B butir 4) tidak terpenuhi.

---

## 1. VERIFIKASI INTEGRITAS (prasyarat)

### 1.1 Git state saat audit

```
HEAD                              : e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169   (tetap, nol commit)
git diff --cached --name-only     : 0 entri   (DIPATUHI)
git status --porcelain            : 91 entri   {' M':4, ' D':21, '??':66}
entri staged menurut XY           : 0   (tidak ada karakter di kolom-1 yang terisi)
```

Koreksi terhadap hitungan yang saya catat sebelumnya: tidak ada entri `M ` (staged)
sama sekali. Keempat entri ` M` adalah modifikasi **di worktree, belum di-stage**;
`git diff --cached --name-only` yang kosong adalah bukti otoritatifnya, bukan
sekadar hasil turunan. Laporan ini sendiri tidak muncul sebagai entri tersendiri
karena seluruh direktori `reports/governance/2026-10-07/Audit/` masih untracked
(`??`) sehingga git meringkasnya jadi satu baris direktori — bukan karena file-nya
tidak ada.

`data/labels/` berisi tepat 2 file kontrak, tanpa subdirektori kosong (#36 TERTUTUP).

### 1.2 Hash — 4 artefak kontrak + 3 artefak lama

| Artefak | Klaim | Aktual | Status |
|---|---|---|---|
| `src/features/build_labels.py` | `90e44a825ee3…` | `90e44a825ee3…` | MATCH |
| `tests/test_build_labels.py` | `53468d95da00…` | `53468d95da00…` | MATCH |
| `reports/…/coder/protokol-H1-H2-H3.md` | `758c5d301ede…` | `758c5d301ede…` | MATCH |
| `reports/…/coder/laporan-final-fase1.md` | `e645a042a7ff…` | `e645a042a7ff…` | MATCH |
| `reports/…/coder/laporan-fix-batch3-D1-D5.md` | `ba5ab603a5b2…` | `ba5ab603a5b2…` | MATCH |
| `src/features/build_features.py` | `399e64b372e4…` | `399e64b372e4…` | IDENTIK |
| `tests/test_build_features.py` | `ed7ac43520c4…` | `ed7ac43520c4…` | IDENTIK |
| `data/features/M15/usdjpy_m15_features.parquet` | `07402f40478a…` | `07402f40478a…` | IDENTIK |
| `arsitek/putusan-adjudikasi-reaudit-kedua.md` | (wajib) | `295303a46dfd…` | MATCH |

Read-only terbukti: ketiga artefak lama tidak berubah, HEAD tidak bergerak,
tidak ada file staged.

---

## 2. A — #23 GAP F2: REKONSILIASI PADA GRAIN BROKER-DAY TUNGGAL

### 2.1 Hitung ulang independen (grain broker-day, edge-rule Q3(a))

```
total bucket parsial (m1_bars < 15)        : 1.281   [B1 ref: 1.281]  OK
bucket parsial mid-day, edge-rule BATAS HARI:   597   [B1 ref: 597]    OK
hari broker ter-flag, edge-rule BATAS HARI  :   234   [B1 ref: 234]    OK
```

Grain tunggal: `prepare_bars` menghasilkan 974 broker-day unik dari 90.041 bar M15.
Tidak ada hari hantu UTC. Ini **TERHUBUNG langsung** dengan fix grain #21/#22.

### 2.2 Rekonsiliasi bucket-per-bucket (syarat A butir 4)

```
di kedua edge-rule (HARI & SESI)             : 578
hanya BATAS SESI                             :   0
hanya BATAS HARI (kontribusi SESI->HARI)      :  19
                                                ----
                                            597  (578 + 19 OK)
hari SESI: 230   hari HARI: 234   selisih: +4
hari yang hilang saat edge-rule HARI         : 0  (HARI superset of SESI)
```

Kontribusi 19 bucket, rinci per hari (semuanya bucket `m1_bars` 10–14):

| broker_day | session_label | m1_bars |
|---|---|---|
| 2023-01-02 | Sydney | 12 |
| 2023-07-05 | Sydney | 14 |
| 2023-08-15 | Sydney | 14 |
| 2023-08-21 | Sydney | 14 |
| 2023-08-29 | Sydney | 14 |
| 2023-09-04 | Sydney | 14 |
| 2023-09-15 | Sydney | 13 |
| 2023-10-11 | Sydney | 13 |
| 2023-10-13 | Tokyo | 14 |
| 2023-10-16 | Sydney | 14 |
| 2023-10-18 | Sydney | 13 |
| 2023-11-14 | Sydney | 14 |
| 2023-11-17 | Sydney | 10 |
| 2024-03-14 | NewYork | 12 |
| 2024-08-08 | Sydney | 13 |
| 2025-06-03 | London | 12 |
| 2025-07-02 | Sydney | 14 |
| 2025-12-31 | London | 14 |
| 2026-04-03 | Sydney | 14 |

Selisih hari +4 (234 vs 230) berasal dari 19 bucket tersebut yang jatuh pada 19 hari
 berbeda, sementara 4 di antaranya hari yang tidak ter-flag pada edge-rule SESI.

**Koinksidensi yang dinyatakan tegas:** angka "19" ini **BUKAN** 19 hari quarantine.
Irisan = **0**. Keduanya berbeda asal (edge-rule vs anomali F-1).

### 2.3 479 DITOLAK (A butir 5)

```
varian Q3(a) HARI x broker-day  : 597 bucket / 234 hari   <- target final
varian tanpa exclude-edge       : 1.281 bucket / 540 hari
varian Q3(a) HARI x UTC-day     : 1.126 bucket / 525 hari
hari UTC total 1.174 vs broker 974 -> 200 hari hantu (#21) terkonfirmasi hilang
```

479 tidak muncul sebagai target, pembanding, maupun pembenar di mana pun dalam
audit ini. Sumbernya (grain campuran HEAD-era) teridentifikasi: `build_labels.py`
belum ada di `HEAD` (`fatal: path 'src/features/build_labels.py' exists on disk,
but not in 'HEAD'`), sehingga re-audit kedua menghitungnya dari file untracked.

**Status A: TERTUTUP** — target-uji terkunci 234 hari pada grain broker-day tunggal,
rekonsiliasi bucket-per-bucket lengkap.

---

## 3. B — LUBANG 1 / BLOCKING 2: GUARD PROVENANS ATR

### 3.1 Apa yang cambiado (terbaca dari kode)

- Klausul tautologi `norm == d/a` **DIHAPUS** (A butir 1 terpenuhi). Verifikasi
  tekstual: `d / a` = 0, `d/a` = 0, `expected` = 0, `1e-6` = 0.
- Guard pengganti `_assert_atr_provenance` (L113–139) membandingkan deret pembagi
  terhadap `atr_reference` via `np.allclose(rtol=1e-9, atol=1e-9)`.
- Smoke bounds dipisah dan diberi label jujur "batas kewajaran, BUKAN bukti satuan"
  (A butir 2 terpenuhi).
- Docstring ditulis ulang, tidak lagi menjanjikan "MELEDAK" berbasis nilai (A butir 5).

### 3.2 Bukti penentu — 9 sabotase pada JALUR PRODUKSI

Sabotase diarahkan ke `daily_metrics` -> kolom `atr_14_d1`, lalu `_build_daily_labels`
dipanggil **persis seperti `main()` L383**:

```python
labels = _build_daily_labels(m15, daily, daily['atr_14_d1'])
```

| kasus | produksi aktual | klaim batch-3 | cocok |
|---|---|---|---|
| baseline (ATR store asli) | NO RAISE | NO RAISE | OK |
| atr = 1.0 konstanta | **NO RAISE** | RAISED | **BATAL** |
| atr = 2.0 konstanta | **NO RAISE** | RAISED | **BATAL** |
| atr = 88.79 konstanta (lock tak-berdimensi) | **NO RAISE** | RAISED | **BATAL** |
| atr = 100.0 konstanta | **NO RAISE** | RAISED | **BATAL** |
| atr = 12345.6 konstanta | **NO RAISE** | RAISED | **BATAL** |
| atr = 1e6 konstanta | **NO RAISE** | RAISED | **BATAL** |
| atr = close-avg (harga, kuantitas salah) | **NO RAISE** | RAISED | **BATAL** |
| atr = 1e-3 konstanta | RAISED | RAISED | OK |
| atr = -5.0 konstanta | RAISED | RAISED | OK |

**Cocok dengan klaim: 3/10.**

Yang membuat `1e-3` dan `-5.0` meledak bukan provenans — melainkan smoke bounds:
`-5.0` melanggar `atr >= 0`; `1e-3` menghasilkan `|norm| >= 1e3`. Keduanya adalah
klausa kewajaran nilai yang **`reaudit-kedua §4` sudah tetapkan sebagai TIDAK
membuktikan satuan**. Keduanya meledak karena alasan yang salah.

### 3.3 Akar masalah — identitas reference

Bukti runtime pada index yang dievaluasi guard:

```
atr_used  : n=974 dtype=float64
atr_ref   : n=974 dtype=float64
index used == index ref ?        True
used.loc[common] == ref.loc[common] ?  True
allclose(rtol=1e-9, atol=1e-9)   :  True
```

Pada jalur `main()`, `atr_reference` adalah `daily['atr_14_d1']` — kolom yang
sama persis dengan sumber pembagi. Guard mengevaluasi `allclose(X, X)`, yang
**benar untuk setiap X**: `1.0`, `88.79`, `close-avg`, `1e6`. Guard ini tidak
membedakan apa pun di produksi.

### 3.4 Mengapa test suite hijau tetapi produksi gagal

`tests/test_build_labels.py:463` (`test_sabotase_pembagi_meledak`):

```python
m15, daily, reference = _guard_fixture()   # reference = .copy() ATR ASLI
daily["atr_14_d1"] = sabotage(daily)       # hanya kolom yang disabotase
compute_london_drift_4h(m15, daily, reference)
```

`reference` diambil **sebelum** sabotase, jadi guard membandingkan dua deret
berbeda dan meledak. Test valid sebagai uji guard — tetapi ia menguji kondisi yang
tidak pernah terjadi di produksi.

Bukti tambahan dari matrix mutasi (§5): mutasi "guard provenans: dimatikan total
(NO-OP)" -> MERAH 3 test; "guard dihapus" -> MERAH 3 test; "reference diganti ATR
acak" -> MERAH 11 test. Artinya suite memang hinges pada deret yang berbeda, sehingga
**tidak mungkin menangkap kondisi produksi** di mana keduanya identik.

### 3.5 Verdict B

Butir 4 putusan adjudikasi mengikat secara eksplisit: sabotase `atr -> 1.0` HARUS
meledak; `atr -> 88.79` HARUS meledak; `atr -> close-avg` HARUS meledak.
**Ketiganya LOLOS di produksi. Syarat terima B-4 GAGAL.**

Yang sudah benar dan dihargai: bentuk guard (provenans, bukan tautologi) sesuai
putusan, docstring jujur, dan test guard benar-benar menguji guard. Yang belum:
guard belum menangkap upstream saboteur. Perbaikan diperlukan: `atr_reference`
harus dibaca dari sumber terpisah (store di disk yang dibaca ulang), bukan dari
kolom pada frame yang sama.

**Status B: TERBUKA** — Lubang 1 belum tertutup.

---

## 4. C — KRITERIA TERIMA D4 DAN #20 ROW KEY

### 4.1 Kriteria terima (putusan C butir 3)

```
rows                                  : 974    OK
kolom                                 : 6 kolom kontrak   OK
index.name                            : date_broker       OK
index unique                          : True             OK
day_label NaN/None                    : 0                 OK
day_label values                      : normal/range/trending  OK  (330/324/320 = 974)
quarantine_mask dtype                 : bool              OK
quarantine_mask NaN                   : 0                 OK
quarantine_mask True                  : 19                OK
london_drift_4h NaN                   : 0                 OK
london_drift_norm NaN                 : 14 (warmup ATR)   OK
gap_f2_flag NaN / dtype / sum         : 0 / int64 / 234   OK
rv_regime_flag NaN / non-NaN          : 19 / 955          OK
```

Verifikasi NaN hanya warmup:
- `london_drift_norm` NaN: 14 hari, `2023-01-02` … `2023-01-19` — blok kontigu awal,
  konsisten warmup ATR 14 hari.
- `rv_regime_flag` NaN: 19 hari, `2023-01-02` … `2023-01-26`, **kontigu dari baris
  pertama** — konsisten `rv_roll_20d` warmup (20-1 = 19), bukan default False.

`_daily_from_m15` tidak ada di kode; tidak ada `normalize()` call di AST. Impor
satu arah terjaga (`build_features` tidak mengimpor `build_labels`).

### 4.2 #20 row key — vonis Auditor

Kriteria mandat: row key dinilai **fungsional**, bukan sekadar keberadaan nama.

```
reindex / .loc lookup 1 bar                    : BISA
merge hilir on date_broker (1:1)                : BISA  (day_label='trending')
set_index("date_broker") -> .loc                 : BISA
round-trip parquet index utuh                   : BISA
```

`write_labels` default `index=True`; `main()` menulis day_labels dengan default
tersebut (h2_trades `index=False` benar — 1 bar spek tanpa index).
`date_broker` terbaca sebagai index bernama, bukan kolom, dan dapat di-merge 1:1.

Catatan transparan: index dtype di disk `datetime64[ns]` vs rebuild
`datetime64[ms]` — perbedaan presisi toolchain, bukan data (nilai index identik,
`index.equals` True).

**Status #20: TERTUTUP (TERIMA)** — row key fungsional, bukan sekadar kosmetik.

### 4.3 Kalibrasi Q1(a) — syarat #4 / Lubang 2

Hitung ulang independen pada span terkunci 2023-01-01..12-31, B = Jan–Jun, A = Jul–Des:

```
span              : 2023-01-02 .. 2023-12-29  (259 hari)
n terpakai        : 240   (19 warmup rv_roll_20d di-exclude)
n_B / n_A         : 111 / 129        kode: 111 / 129       MATCH
TAU_2023 (Youden) : 2.5951672079821496e-05
                    kode: 2.5951672079821496e-05          MATCH (rel diff 0.000e+00)
  Youden max = 0.6046511628 pada k=162, TPR=1.000000, FPR=0.395349
AUC              : 0.8173755150499337 (rank) / 0.8173755150499336 (trapezoid)
                    / 0.8173755150499337 (U-stat langsung)
                    kode: 0.8173755150499336               MATCH (3 metode)
```

Ketiga metode AUC independen saling cocok satu digit terakhir. Verifikasi
`rv_regime_flag` di D4 identik dengan `1[rv_score > TAU_2023]`, flag=1 sebanyak
619 hari.

**Catatan metodologis yang saya catat untuk batch berikutnya:** NAIF Youden pada
span ini menghasilkan TPR=1.000 (skor B dan A tidak tumpang tindih sama sekali),
sehingga ambang berada pada batas bawah. Nilai TAU tetap benar secara aritmetika
dan bit-perfect, tetapiıkatan sensitivitasnya belum diuji — bukan temuan, hanya
catatan keterbatasan bukti.

**Status #24 / Lubang 2: TERTUTUP.**

### 4.4 Reproduksibilitas D4

Dua run `main()` ke direktori terpisah -> **byte-identik**:

```
usdjpy_day_labels.parquet  sha256_run1=20cf4cdd720e620a  run2=20cf4cdd720e620a  IDENTIK
usdjpy_h2_trades.parquet   sha256_run1=75938ad32bf35a20  run2=75938ad32bf35a20  IDENTIK
```

 reproducible secara konsisten terhadap toolchain yang sama.

---

## 5. MATRIX MUTASI (20 mutasi, suite `test_build_labels.py`)

Baseline: **54 passed** (configs + data ter-mount di salinan di luar repo; worktree
tidak disentuh).

| mutasi | hasil |
|---|---|
| classify_day_label: syarat trending dimatikan | MERAH 2 |
| classify_day_label: range ikut jadi trending | MERAH 3 |
| quarantine_mask: tidak pernah menandai | MERAH 6 |
| quarantine_mask: hanya jendela pertama | MERAH 2 |
| LONDON_FIRST_N 16 -> 4 | MERAH 6 |
| LONDON_FIRST_N 16 -> 8 | MERAH 6 |
| LONDON_FIRST_N 16 -> 60 | MERAH 6 |
| M1_BARS_MIN 15 -> 14 | MERAH 3 |
| M1_BARS_MIN 15 -> 20 | MERAH 4 |
| **RV_WINDOW_DAYS 20 -> 10** | **HIJAU 0** |
| TAU_2023 dinaikkan 10% | MERAH 1 |
| RANGE_ATR_THRESHOLD 88.79 -> 1.0 | MERAH 4 |
| RATIO_PATH_THRESHOLD 0.0268 -> 0.0 | MERAH 3 |
| write_labels: index=False | MERAH 1 |
| guard provenans -> no-op (compare(atr, atr)) | MERAH 3 |
| guard provenans dihapus | MERAH 3 |
| **smoke bounds dihapus** | **HIJAU 0** |
| guard reference diganti ATR acak | MERAH 11 |
| drift = close-awal (bukan close-akhir) | MERAH 7 |
| norm pakai ATR konstanta 1.0 | MERAH 4 |

**18/20 terbunuh. 2 mutasi hidup.**

Catatan transparan tentang syarat 6 (#25): temuan asli menyebut "4 test
`TestBuktiMutasi`". Pada HEAD sekarang kelas itu berisi **3 method**
(`test_mutasi_classify_day_label_membuat_test_range_merah`,
`test_mutasi_quarantine_mask_membuat_test_jendela_merah`, dan
`test_patch_bl_tidak_terjangkau_binding_lokal`). Dua yang pertama adalah test
mutasi nyata; yang ketiga adalah test dokumentasi binding. Yang disyaratkan
substantif — patch harus mencapai binding yang benar-benar dipakai test, dan suite
harus merah pada mutasi gut-total — keduanya terbukti di sini: ketiga mutasi guard
pada tabel di atas semuanya MERAH, termasuk patch no-op `compare(atr, atr)` yang
persis meniru kondisi produksi. Penurunan jumlah method dari 4 ke 3 saya laporkan
apa adanya; saya tidak mengarang test keempat untuk mengejar angka.

- `RV_WINDOW_DAYS 20 -> 10`: konstanta berubah tapi `TAU_2023` tetap hardcoded, dan
  test tidak mengunci bahwa kalibrasi harus dihitung ulang bila jendela rv berubah.
  `test_tau_dan_angka_kalibrasi_terkunci` hanya membandingkan konstanta ke konstanta.
- smoke bounds dihapus: memang tidak ada test yang mengunci klausa kewajaran —
  konsisten dengan keputusan arsitek bahwa klausa itu bukan bukti satuan, jadi ini
  **residual yang acceptable**, bukan finding. Dicatat agar tidak hilang.

Sensitivitas `LONDON_FIRST_N` via pytest (`TestJendelaLondonLock`):

```
N= 4  -> 1 failed, 4 passed   MERAH  (expected)
N= 8  -> 1 failed, 4 passed   MERAH  (expected)
N=60  -> 1 failed, 4 passed   MERAH  (expected)
N=16  -> 5 passed             HIJAU  (expected)
```

**#26 TERTUTUP.** Fixture sensitif terhadap jendela; N terkunci.

---

## 6. 14 SYARAT §7 `reaudit-kedua` — STATUS AKHIR

| # | syarat | status | bukti |
|---|---|---|---|
| 1 | Pulihkan row key D4 (#20) | **TERTUTUP** | DatetimeIndex `date_broker`, merge 1:1 + reindex + set_index lolos (§4.2) |
| 2 | Satukan grain broker-day (#21, #22) | **TERTUTUP** | 974 broker-day, 0 hari hantu, 0 `normalize()` call, `_daily_from_m15` dihapus (§2, §4.1) |
| 3 | Adjudikasi arsitek #23 | **TERTUTUP** | Target 234 terkunci; rekonsiliasi 597=578+19 lengkap; 479 ditolak (§2) |
| 4 | Jalankan Q1(a), tulis angka riil (#24) | **TERTUTUP** | TAU/AUC/n bit-perfect, 3 metode AUC cocok (§4.3) |
| 5 | Guard satuan yang sabenar (B) | **TERBUKA** | Guard = `allclose(X, X)` di produksi; 7/9 sabotase LOLOS termasuk 1.0/88.79/close-avg (§3) |
| 6 | Perbaiki 4 test `TestBuktiMutasi` (#25) | **TERTUTUP** | Patch `HERE` (binding yang benar-benar dipakai test); 18/20 mutasi mati termasuk 3 mutasi guard (§5) |
| 7 | Kunci `LONDON_FIRST_N` (#26) | **TERTUTUP** | N=4/8/60 merah, N=16 hijau (§5) |
| 8 | Hapus/`assert` `test_status_belum_diuji` (#27) | **TERTUTUP** | `test_status_belum_diuji` tidak ada; 0 test tanpa assertion dan tanpa `pytest.raises` |
| 9 | D1 <=400, main <=50, hapus `_daily_from_m15` (#28/#29) | **TERTUTUP** | D1 = 400 baris fisik (tepat pagu), main = 33 AST, fungsi terpanjang 41, `_daily_from_m15` nol |
| 10 | Perbaiki `FutureWarning` (:253) (#35) | **TERTUTUP** | `fillna` = 0 di D1; dipakai `reindex(days, fill_value=False)`; run `-W error` exit 0 |
| 11 | Hitung ulang 4 hash + "pytest penuh" (#30/#31) | **TERTUTUP** | 4 hash cocok; D5 kini tulis `248 passed`, `248 collected`, `54 collected` (§7) |
| 12 | Kutipan F1 73-75 + path `arsitek/`; sinkron gap (#33) | **TERTUTUP** | `36-38` = 0; `73-75` di D5 = 1, di B3 = 2; path `arsitek/putusan-arsitek-F1.md` di B3 = 2; sumber F1 L73-75 diverifikasi berisi kutipan anomali 19 hari |
| 13 | Unstage 23 entri, jalankan ulang `git status` (#32) | **TERTUTUP** | staged = 0; D5 tulis `staged: 0` dan menjelaskan 7 staged yang diukur sesi ini |
| 14 | Perbaiki severity #10 (#19) | **TERTUTUP** | B3 §"14. Severity #10 = TERTUTUP (#19)" tertaut ke D5 §3 |

**13 dari 14 tertutup. Syarat 5 (Lubang 1) terbuka.**

---

## 7. #20–#36 — STATUS AKHIR

| # | severity | temuan | status | bukti |
|---|---|---|---|---|
| 20 | HIGH | D4 kehilangan row key | **TERTUTUP** | index `date_broker` fungsional: merge 1:1, reindex, set_index (§4.2) |
| 21 | HIGH | 200 bar hantu dari grain UTC | **TERTUTUP** | 974 broker-day; hari UTC 1.174 vs broker 974 -> hantu hilang (§2.3) |
| 22 | HIGH | ATR broker-daily di-reindex ke UTC-day | **TERTUTUP** | grain tunggal; guard provenans ditambahkan (§3.1) — *tapi guard sendiri TIDAK efektif, lihat #5 syarat* |
| 23 | HIGH | gap 479 vs 234 | **TERTUTUP** | target 234 terkunci, rekonsiliasi lengkap, 479 ditolak (§2) |
| 24 | HIGH | RV 100% NaN | **TERTUTUP** | non-NaN 955; kalibrasi riil tertulis & tereproduksi (§4.1, §4.3) |
| 25 | MED | 4 test bukti mutasi no-op | **TERTUTUP** | patch pada `HERE`; 18/20 mutasi mati (§5) |
| 26 | MED | `LONDON_FIRST_N` tidak terkunci | **TERTUTUP** | N=4/8/60 merah (§5) |
| 27 | MED | 1 test tanpa assertion | **TERTUTUP** | dihapus (`test_status_belum_diuji` nol) |
| 28 | MED | pagu 474/66 | **TERTUTUP** | 400/33; fungsi terpanjang 41 |
| 29 | MED | `_daily_from_m15` kode mati | **TERTUTUP** | nol kemunculan |
| 30 | MED | 2 hash D5 mismatch | **TERTUTUP** | 4 hash + 3 lama cocok (§1.2) |
| 31 | MED | "pytest penuh" = 36 | **TERTUTUP** | terukur 248 passed / 248 collected / 54 collected |
| 32 | HIGH | 23 entri staged | **TERTUTUP** | staged = 0 |
| 33 | LOW | kutipan F1 salah | **TERTUTUP** | 73-75 + path `arsitek/` |
| 34 | LOW | typo `HIUGO` | **TERTUTUP** | 0 kemunculan |
| 35 | LOW | `FutureWarning` | **TERTUTUP** | `fillna` nol; `-W error` exit 0 |
| 36 | LOW | 7 subdirektori kosong | **TERTUTUP** | tepat 2 file kontrak |

---

## 8. TEMUAN BARU (di luar 14 syarat)

### 8.1 [BLOCKING] Guard provenans inoperatif di jalur produksi — §3

Detail di §3.1–3.5. Ringkas: `main()` L383 mengirim `atr_reference = daily['atr_14_d1']`,
yaitu kolom yang sama dengan sumber pembagi, sehingga guard mengevaluasi
`allclose(X, X)`. Ketiga sabotase yang diputus wajib meledak (`1.0`, `88.79`,
`close-avg`) LOLOS.

### 8.2 [MEDIUM] Klaim `ruff format --check` salah

```
klaim D5  : ruff format --check . -> 37 files already formatted (exit=0)
fakta     : 10 files would be reformatted, 187 files already formatted  (rc=1)
```

D1 yang ditulis batch-3 **sendiri** gagal format:

```
--> src/features/build_labels.py:149:13
   assert (
       np.abs(norm.dropna()) < SMOKE_NORM_ABS_MAX
   ).all(), "|london_drift_norm| >= 1e3 (batas kewajaran, bukan bukti satuan)"
```

`ruff check .` memang lulus (`All checks passed!`, rc=0). Yang salah hanya
`format --check`, dan D5 mencatat exit=0 padahal rc=1 pada file yang sama.

Catatan: 7 file lain yang gagal format adalah artefak di luar scope batch-3
(notebook EDA x6, `reaudit-adversarial-D1-D5.md`, `build_features.py`) —
sebagian di antaranya sudah gagal sebelum batch-3. Yang relevan batch-3 adalah
`build_labels.py`.

### 8.3 [MEDIUM] `RV_WINDOW_DAYS` tidak terikat kalibrasi

Mutasi `RV_WINDOW_DAYS 20 -> 10` lolos. `TAU_2023` di-hardcode; test kalibrasi
hanya membandingkan konstanta terhadap konstanta. Mengganti jendela rv tanpa
rekalibrasi akan menghasilkan `rv_regime_flag` yang berbeda tanpa test Reds.
Tidak menutupi kalibrasi §4.3 (yang bit-perfect pada konfigurasi saat ini),
tetapi celah regresi.

### 8.4 [LOW] D4 di disk dibuat dengan toolchain berbeda

```
sha256 D4 disk     : day=47D15C41…  trades=32EAF6B2…
sha256 rebuild     : day=20CF4CDD…  trades=75938AD3…
pyarrow saat disk   : 17.0.0      pyarrow sekarang: 25.0.1
pandas saat disk    : (unicode/object)  pandas sekarang: 3.0.6 (str)
```

Isi **nilai** seluruh kolom identik (`gap_f2_flag` int32 vs int64, index ns vs ms,
tetapi `index.equals` True dan semua nilai kolom cocok). Perbedaan byte berasal
dari metadata parquet. Gate §3 (byte-reproducible) tetap **lolos** terhadap
toolchain yang sama, tapi D4 di disk bukan hasil run toolchain sekarang.
Dicatat agar tidak disalahbaca sebagai non-determinisme pipeline.

### 8.5 [LOW] `LONDON_FIRST_N = 60` melampaui fixture

`make_london_rising` default `n_bars=32`, sehingga N=60 menjangkau seluruh hari.
Test tetap merah (benar), tetapi sensitivitas yang diuji untuk N=60 adalah
"ambil semua bar", bukan "ambil 60 bar pertama". Adequat untuk membuktikan
penguncian, tidak setara sensitivitas jendela di data nyata. Dicatat sebagai
batasan bukti, bukan temuan.

---

## 9. GATE AKHIR

```
pytest penuh                 : 248 passed in 15.29s      rc=0
pytest --collect-only        : 248 tests collected       rc=0
test_build_labels collect    : 54 tests collected        rc=0
ruff check .                 : All checks passed!        rc=0
ruff format --check .        : 10 would be reformatted   rc=1   <- klaim D5 exit=0 SALAH
check_foreign_chars.py       : OK: 96 file discan, tidak ada karakter asing  rc=0
git staged                   : 0   (git diff --cached --name-only kosong)
git status                   : 91 entri   {' M':4, ' D':21, '??':66}
```

Status 91 entri seluruhnya di luar cakupan D1-D5: 4 modifikasi worktree belum
di-stage, 21 penghapusan, 66 untracked. Tidak ada entri staged sama sekali — kolom-1
pada `git status --porcelain` tidak pernah terisi dan `git diff --cached` kosong,
sehingga angka "1 staged" yang sempat saya catat adalah salah baca dan sudah
dikoreksi di §1.1. Direktori `Audit/`, `arsitek/`, dan `coder/` masih untracked
(`??`) sehingga git meringkasnya menjadi satu entri per direktori.

Tidak ada entri untuk artefak batch-3 yang ter-stage.

---

## 10. SELF-AUDIT 3x

### Putaran 1 — Correctness

Tiap status TERTUTUP bertumpu pada eksekusi independen: hitung ulang gap dari
`prepare_bars` pada 90.041 bar M15 (bukan dari angka batch-3); 20 mutasi disuntik ke
salinan di luar repo dengan baseline 54 hijau; sabotase diarahkan ke jalur
`main()`; kalibrasi dihitung ulang dengan tiga metode AUC independen; `git
hash-object` dihitung ulang untuk 9 artefak. Tidak ada TERTUTUP berbasis narasi.
`B` tidak saya tutup meski `bukti-mutasi atr_guard_disabled` hijau, karena saya
memverifikasi bahwa suite hanya bergantung pada deret berbeda — bukti yang membuat
penutasan itu saya tolak.

### Putaran 2 — Bias & asumsi

Saya menguji klaim batch-3 dalam arah yang tidak menguntungkan batch-3. Klaim
"9 sabotase RAISED" saya buktikan 3/10 benar pada jalur produksi. Klaim "ruff format
exit=0" saya buktikan rc=1. Klaim "248/54" saya hitung ulang dan benar, tetapi
`RV_WINDOW_DAYS` yang saya laporkan tidak terkunci. Klaim "LULUS" batch-3 saya tolak.
Saya juga mengoreksi **dua kesalahan harness saya sendiri** yang cenderung ke arah
sebaliknya: (a) Youden awal saya prepend `(1.0, 0.0)` sehingga TAU tampak meleset
53% — setelah diperbaiki, TAU cocok **bit-perfect**; (b) test row-key awal saya
memanggil `set_index` pada frame yang `date_broker`-nya sudah jadi index — setelah
diperbaiki, row key **fungsional**. Kesalahan saya tidak saya biarkan menjadi
temuan palsu.

### Putaran 3 — Meta-check

Read-only total dipatuhi. Semua output rebuild diarahkan ke
`C:\Users\Fajar\AppData\Local\Temp\opencode\rf234\`; mutasi disuntik ke salinan
`mutcheck/` di luar repo (configs di-copy, `data` di-mount sebagai junction);
semua sabotase in-memory via monkeypatch pada frame, tidak menyentuh file worktree.
Verifikasi akhir: `build_features.py`, `test_build_features.py`, dan parquet M15
tetap `399e64b3`/`ed7ac435`/`07402f40`; `HEAD` tetap `e0b2b9f`; staged = 0.
Tidak ada byte worktree yang saya ubah selain laporan ini.
Tidak memutus arsitektur: saya tidak mengubah definisi Q3(a), tidak mengoreksi
target 234, tidak menyentuh H4/H5/H6+, lock, EDA, atau fondasi B1. Residual
`RV_WINDOW_DAYS` saya laporkan sebagai temuan dengan bukti, bukan vonis
prinsip kalibrasi. Tidak ada temuan yang saya karang; dua di antaranya saya turunkan
setelah verifikasi ulang (smoke-bounds mutasi, `LONDON_FIRST_N=60`).

---

## 11. VERDICT

```
RE-AUDIT KETIGA — BATCH-3 D1–D5
VERDICT: GAGAL
```

**Dasar:** 13 dari 14 syarat §7 tertutup, 16 dari 17 temuan #20–#36 tertutup, A dan
C tertutup penuh, kalibrasi Q1(a) bit-perfect. Namun **syarat 5 / Lubang 1 / blocking 2
(Putusan adjudikasi §B butir 4) tetap TERBUKA**: guard provenans ATR membandingkan
deret dengan dirinya sendiri pada jalur produksi, sehingga ketiga sabotase yang
diputus wajib meledak (`1.0`, `88.79`, `close-avg`) justru LOLOS.

Sesuai mandat §4 butir 3, `LULUS` diberikan hanya bila 14 syarat §7 **dan** A/B/C
terbukti seluruhnya. A dan C terbukti; B tidak. Karena itu verdict **GAGAL** —
bukan karena pekerjaan batch-3 buruk (13 syarat tertutup nyata dan terukur), tetapi
karena satu syarat blocking yang eksplisit gagal.

**Sisa yang harus ditutup pada batch berikutnya (rambu minimal):**

1. **[BLOCKING]** `atr_reference` pada `main()` harus dibaca dari sumber terpisah dari
   kolom `atr_14_d1` yang jadi pembagi (mis. store parquet dibaca ulang), sehingga
   `allclose` benar-benar membandingkan dua deret berbeda; lalu buktikan ulang bahwa
   `1.0`, `88.79`, dan `close-avg` RAISE pada jalur produksi, dan baseline LOLOS.
2. **[MEDIUM]** Perbaiki format `build_labels.py:149` agar `ruff format --check` rc=0,
   lalu perbarui klaim gate D5 §8.3.
3. **[MEDIUM]** Kunci `RV_WINDOW_DAYS` terhadap kalibrasi: test harus gagal bila
   jendela rv berubah tanpa TAU yang dihitung ulang.
4. **[LOW]** D4 di disk perlu dibangun ulang dengan toolchain saat ini, atau
   dicatat bahwa hash D4 tidak reproducible lintas versi pyarrow.
5. **[LOW]** Fixture `LONDON_FIRST_N` sensitivity untuk N>32 perlu bar tambahan agar
   uji sensitivitas mencerminkan jendela nyata, bukan "ambil semua bar".
