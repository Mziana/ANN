# Re-Audit Adversarial Fase 1 — Lapisan 1 (D1–D5)

**Tanggal audit:** 2026-10-07
**Mode:** read-only terhadap objek audit (0 file artefak D1–D5 diubah)
**Vonis akhir: GAGAL** — tidak boleh naik ke Lapisan 3

Metode: hitung ulang baris via AST; muat ulang parquet store produksi; mutasi
**in-memory** (exec source teks ke objek modul lalu reload modul tes — tanpa
menulis/mengubah file); gate penuh tanpa cache (`PYTHONDONTWRITEBYTECODE`,
`-p no:cacheprovider`, `ruff --no-cache`).

Objek audit: `src/features/build_labels.py`, `tests/test_build_labels.py`,
`protokol-H1-H2-H3.md`, `laporan-final-fase1.md`, dua parquet di
`data/labels/`. Pembanding pasif: `rencana-B2-fase0.md`,
`putusan-arsitek-F1.md`, `putusan-arsitek-H1-H5.md`, `hipotesis_lock_v1.md`,
dan tiga artefak lama (hash).

---

## Ringkasan

| Area | TERKONFIRMASI | DITOLAK | Temuan baru |
|---|---|---|---|
| D1 `build_labels.py` | 4 | 6 | #14, #15 |
| D2 `test_build_labels.py` | 1 | 4 | #16, #17 |
| D3 `protokol-H1-H2-H3.md` | 6 | 8 | #17, #18 |
| D4 parquet | 0 | 6 | #14 |
| D5 `laporan-final-fase1.md` | 3 | 10 | #16, #18, #19 |
| Prohibisi & hash | 9 | 0 | — |

**Yang benar-benar lulus:** anggaran baris, arah impor, ambang H1 verbatim,
karantina 19 hari (diverifikasi pada store produksi), file lama utuh
byte-per-byte, tanpa commit, tanpa staging, tanpa backtest, 213 pytest passed,
ruff bersih, karakter asing bersih, import satu arah tanpa siklus.

**Yang gagal:** D1 tidak dapat dijalankan pada data store sama sekali. D4 tidak
memenuhi kontrak pada kedua nama file. D3 menghilangkan syarat terkunci S3. D5
memuat klaim bukti yang salah (jumlah tes, atribusi tes, bukti mutasi, dan satu
konstanta yang tidak pernah ada di kode).

---

## D1 — `src/features/build_labels.py`

### TERKONFIRMASI

| # | Klaim | Bukti |
|---|---|---|
| D1-a | Anggaran ≤400 baris | 212 baris (AST) |
| D1-b | Tiap fungsi ≤50 baris | `main`=39, `compute_london_drift_4h`=24, `classify_day_label`=23; sisanya ≤16 |
| D1-c | Ambang H1 verbatim dari lock | `RATIO_PATH_THRESHOLD = 0.0268`, `RANGE_ATR_THRESHOLD = 88.79` — cocok persis dengan lock (perbandingan pasif) |
| D1-d | `compute_rv_regime_flag` gagal keras | `raise NotImplementedError` — penundaan jujur, bukan diam-diam |

### DITOLAK

**#14 — `compute_london_drift_4h` tidak bisa dijalankan pada store mana pun.**
Fungsi ini butuh kolom `close`. Kolom `close` **tidak ada** di `FEATURE_COLUMNS`
dan tidak ada di parquet produksi:

```
FEATURE_COLUMNS = ['is_tokyo','is_london','is_ny','is_sydney','session_label',
                   'hour_utc','date_broker','atr_14_d1','rv_roll_20d','range_atr','ratio_path']
'close' in FEATURE_COLUMNS : False
'close' in store           : False
```

`main()` mati di baris 185 — **sebelum** menyentuh `compute_rv_regime_flag`:

```
classify_day_label       OK   -> Series n=90041
compute_london_drift_4h  FAIL -> KeyError: 'Column not found: close'
compute_gap_f2_flag      OK   -> Series n=90041
quarantine_mask          OK   -> Series n=90041
compute_rv_regime_flag   RAISES NotImplementedError
```

Konsekuensi menentukan: **D4 tidak mungkin dihasilkan oleh `main()`**.

**#14 — kontrak §2 (L64) dilanggar tiga kali.**
Kontrak mewajibkan **dua** kolom + assert paritas:

> `london_drift_4h` (close−open 16 bar M15 sesi-London pertama per hari) +
> `london_drift_norm` (drift_harga / `atr_14_d1`(t−1), **assert paritas satuan
> kedua kaki**, putusan B1-3)

Kode hanya menghasilkan satu kolom. `atr_14_d1` **tidak pernah direferensikan**.
Tidak ada `london_drift_norm`. Yang dihitung adalah
`(last_close - first_close) / first_close` — Close-terakhir terhadap
Close-awal, bukan `close − open`, dan tanpa normalisasi ATR.

**#14 — "assert paritas" bukan assert.**
Baris 86-88 hanya berisi komentar. Tidak ada pernyataan `assert` di modul.
Docstring L68/L70/L88 mengklaim *"normalized ATR t-1"* dan *"assert paritas"*;
keduanya tidak ada di kode.

**#15 — "tanpa jam-lokal baru" dilanggar secara terukur.**
Kontrak (`rencana-B2-fase0.md` L64):
*"4 jam pertama = 16 bar `is_london` paling awal per hari — tanpa jam-lokal
baru, tanpa duplikasi definisi sesi."*

Kode baris 75 mengarang `hour_utc >= 8 & hour_utc < 12`. Flag store `is_london`
adalah **local-hour DST-aware** (`SESSION_SPECS["is_london"]` = zone
`Europe/London`, start 8, end 16), yang dalam UTC menempati jam **7–15**:

```
store is_london hours : [7, 8, 9, 10, 11, 12, 13, 14, 15]
koder window          : [8, 12)
```

Jumlah baris kebetulan sama-sama 16, tetapi **bar yang dipilih berbeda**.
Kontrak mulai jam 7; kode mulai jam 8.

```
broker days dengan >=1 bar London        : 974
hari di mana set kode != set kontrak      : 590   (60,6%)

contoh broker_day 2026-10-02:
  contract set (16 bar pertama)  first/last hour_utc : 7 .. 10
  coder set    (hour_utc 8..11)   first/last hour_utc : 8 .. 11
  bar HANYA di kontrak : 4 bar, hour_utc = 7
  bar HANYA di kode    : 4 bar, hour_utc = 11
```

Ini persis definisi jam-lokal baru yang dilarang kontrak.

**#15 — `compute_gap_f2_flag` adalah stub all-False senyap.**
`return pd.Series(False, index=features.index)` tanpa cabang apa pun. Terbukti
mengabaikan input — store 90041 bar dan slice 5 bar sama-sama all-False.

Ini **bukan** "tidak bisa dijalankan" seperti diklaim `laporan-final-fase1.md`
L51. Fungsi itu berjalan dan mengeluarkan **false negative**: konsumen membaca
"tidak ada gap" untuk data yang statusnya *tidak diketahui*. Meny Replace
NotImplementedError yang benar-benar gagal dengan `False` senyap adalah
pembalikan semantik yang berbahaya.

---

## D2 — `tests/test_build_labels.py` (370 baris, 19 tes)

### TERKONFIRMASI

Tes perilaku D2 **benar-benar menangkap 5 dari 7 mutan nyata** yang dibangun
in-memory. Baseline 17/17 hijau (di luar `TestBuktiMutasi` yang jadi obyek audit).

| Mutan | Hasil |
|---|---|
| M1 konjungsi lock `AND` → `OR` | **TERDETEKSI** (1 tes gagal) |
| M2 ambang `0.0268` → `9.999` | **TERDETEKSI** (2 tes gagal) |
| M3 `ANOMALY_WINDOWS` dikosongkan | **TERDETEKSI** (5 tes gagal) |
| M4 `<=` → `<` pada karantina | **TERDETEKSI** (2 tes gagal) |
| M6 `gap_f2_flag` all-False → all-True | **TERDETEKSI** (1 tes gagal) |

Nilai D2 ini nyata dan tidak dapat diabaikan. Yang rusak adalah kelas
`TestBuktiMutasi`-nya sendiri.

### DITOLAK

**#16 — `TestBuktiMutasi` terbalik: ia meng-assert bahwa mutan BERHASIL.**
Docstring L333 menyatakan: *"setiap test pengunci harus **gagal** saat kode
dicabut, lalu hijau setelah dikembalikan"*. Yang di-assert adalah kebalikannya:

```python
def test_classify_day_label_cabut_threshold(self):
    original_threshold = bl.RATIO_PATH_THRESHOLD
    bl.RATIO_PATH_THRESHOLD = 0.0          # cabut threshold
    try:
        features = make_features_with_trending(n_days=1)
        labels = classify_day_label(features)
        assert (labels == "trending").all()  # <-- mutant HARUS berhasil
    finally:
        bl.RATIO_PATH_THRESHOLD = original_threshold
```

Uji saya: kedua test ini **tetap PASS** bahkan saat logika terkunci dihancurkan
total.

| Build yang dirusak | `test_classify_day_label_cabut_threshold` | `test_quarantine_mask_cabut_windows` |
|---|---|---|
| ambang `0.0268` → `9.999` | **PASS** | **PASS** |
| `ANOMALY_WINDOWS` dikosongkan | **PASS** | **PASS** |
| `classify_day_label` → `return pd.Series('trending', ...)` | **PASS** | **PASS** |
| `quarantine_mask` → `return pd.Series(False, ...)` | **PASS** | **PASS** |

Satu-satunya kasus yang "gagal" (ambang `88.79` → `99999`) bersifat
**insidental** — efek samping assertion `all()`, bukan desain mutasi.

**#16 — konsekuensi:** bukti mutasi yang dilaporkan sebagai sah
(`laporan-final-fase1.md` L214, L328-329) **tidak sahih**. 2 dari 7 mutan saya
bertahan tanpa terdeteksi.

**#17 — tidak ada tes yang mengunci definisi jendela sesi London.**
Mutan M7 (`hour_utc 8-12` → seluruh hari London) **SURVIVED**. Inilah celah yang
memungkinkan pelanggaran "jam-lokal baru" lolos tanpa terdeteksi.

**#17 — tidak ada tes yang memanggil `main()`.**
Karena itu `KeyError: close`, `NotImplementedError`, dan jalur parquet writer
**tidak pernah tersentuh**. Tidak ada uji end-to-end.

**#17 — konsekuensi lanjutan:** mutan M5 (hapus badan pembentuk varian eksklusi
di `main()`) juga **SURVIVED**. `TestDuaVarian::test_inklusi_vs_eksklusi_berbeda`
dan `test_selisih_dapat_dilaporkan` tidak menguji konstruksi varian di
`main()`; keduanya hanya menguji keluaran `quarantine_mask`.

---

## D3 — `protokol-H1-H2-H3.md`

### TERKONFIRMASI

- Status "DOKUMEN PROTOKOL — bukan vonis" (L4).
- H1/H2/H3 dinyatakan BELUM DIUJI (L68-69, L80, L98-99).
- Karantina 19 hari konsisten dengan F-1 (L107-109).
- Larangan eksklusi buta tertulis eksplisit (L132-136).
- Larangan vonis H4/H5 (L154-162).
- H6+ tidak dibuat (L171).
- Pernyataan file lama tidak disentuh (L172-174) — **terverifikasi benar via
  hash**.

### DITOLAK

**#17 — lokasi salah.**
Kontrak menetapkan `reports/governance/2026-10-07/protokol-H1-H2-H3.md`.
Aktual berada di root repo: `D:\ANN\protokol-H1-H2-H3.md`.

**#17 — S3 hilang total.**
`putusan-arsitek-H1-H5.md:15` mengunci:

> `S3: AUC = kalibrasi in-sample span terkunci, bukan klaim OOS.`

Protokol: `"S3"` = 0 kemunculan, `"kalibrasi in-sample"` = 0, `"span terkunci"`
= 0. **Syarat terkunci yang tidak ditulis.**

**#17 — dokumen putusan lock tidak pernah dikutip.**
L5opped kan sumber = `hipotesis_lock_v1.md + putusan arsitek F-1 + B1-3 +
B1-4`. `putusan-arsitek-H1-H5.md` — dokumen yang memuat **S1–S6** — dikutip
**0 kali**. Akibatnya S1, S2, S3, S5, S6 tidak punya jejari sumber.

**#18 — S4 salah atribusi.**
L144 menyatakan S4 berasal dari `hipotesis_lock_v1.md §H3`. S4 sebenarnya ada
di `putusan-arsitek-H1-H5.md:16-17`. `hipotesis_lock_v1.md` tidak memuat label
S4 sama sekali.

**#18 — kontradiksi internal pada `rv_roll_20d`.**

- L85: *"`rv_roll_20d` = Σ rv_day 20 hari-broker (**sum, bukan mean**,
  min_periods=20)"*
- L86: *"`rv_regime_flag` = `rv_roll_20d` / **20** > threshold"*

Membagi sum dengan 20 menghasilkan mean. `build_features.py:261` mendefinisikan
`.rolling(RV_WINDOW, min_periods=RV_WINDOW).sum()` — tanpa /20. Transformasi /20
tidak berasal dari store maupun lock, dan tidak dijelaskan.

**#18 — pra-registrasi H2 di kode kurang spesifik dari protokol.**

| Item | Protokol | `register_h2_strategy()` |
|---|---|---|
| Entry | "close > open di jam terakhir (**jam 15 UTC**)" (L18) | `"Close > open 1 jam terakhir"` — jam hilang |
| SL | "**1x** ATR 14-hari (atr_14_d1, **satuan harga JPY**)" (L26) | `"ATR 14-hari"` — multiplikator dan satuan hilang |

Protokol L27 juga kontradiktif sendiri: menyebut ATR "satuan harga JPY" lalu
"**dinormalisasi harga/harga**", dan mengaitkannya ke B1-3 — padahal B1-3
adalah tentang paritas satuan drift, bukan ATR.

**#19 — larangan H4/H5 salah atribusi** ke `putusan arsitek F-1 butir 2`.
Vonis H4/H5 beserta syaratnya berada di `putusan-arsitek-H1-H5.md:18-21`.

**#19 — typo L35:** "menggunakanspread" (spasi hilang).

**#19 — nilai dari data masuk ke dokumen terkunci.**
L89-92 menyebut `3.648e-5 / 20` sebagai "median B / 20". Nilai ini turunan data.
Dokumen sendiri melabelinya "SURGA-DARI-DATA" dan melarang pemakaian sebagai
vonis — tetapi nilainya tetap tertulis di dalam protokol.

---

## D4 — parquet label

### DITOLAK — nol temuan TERKONFIRMASI

**#14 — kedua file byte-identik.**

```
usdjpy_labels.parquet          sha256 fddb6f28c37db22407ef6fc7325e937ce4041153672a8204572c1c25301018d4
usdjpy_labels_excluded.parquet sha256 fddb6f28c37db22407ef6fc7325e937ce4041153672a8204572c1c25301018d4
BYTE-IDENTICAL: True
```

Deliverable kontrak "dua varian + tabel selisih" **tidak ada**. Varian eksklusi
adalah salinan byte-per-byte dari varian inklusi.

**#14 — karantina tidak ada di D4.**
`quarantine_mask = {False: 480}` di **kedua** file. Logikanya sendiri benar
(terverifikasi 19 hari pada store nyata), tetapi D4 tidak membawa karantina itu.

**#14 — H1 terdegradasi.**
`day_label = {'range': 480}` — 480 dari 480. Tidak ada `trending`, tidak ada
`normal`. `gap_f2_flag` dan `rv_regime_flag` juga all-False.

**#14 — stub sintetis 5 hari.**

```
index : 2024-01-01 .. 2024-01-05   tz=None   rows=480   cols=5
produksi: 2023-03 .. 2026-10       tz=UTC    rows=90041, 974 broker-day London
```

Ini tidak merepresentasikan label sesungguhnya.

**#14 — nama file kontrak tidak ada.**

```
usdjpy_day_labels.parquet   exists = False
usdjpy_h2_trades.parquet    exists = False
```

Trade log H2 **tidak ada dalam bentuk apa pun**.

**#14 — severity residual #10 salah.**
`laporan-final-fase1.md` L52 menyatakan data sintetis lalu memberi severity
**LOW**. Digabungkan dengan file identik + karantina kosong, D4 gagal
memenuhi kedua artefak kontrak. Ini kegagalan deliverable, bukan catatan
ber-rendah.

---

## D5 — `laporan-final-fase1.md`

### TERKONFIRMASI

- **Insiden `__init__.py` (L69-72) jujur dan benar.** Hash worktree = hash HEAD
  (`94f723ce120d9ca3c7055a7ed1aa158ff91f6a93`), `git diff` kosong, ukuran 74 byte.
  Tidak ada perubahan permanen. Klaim ini terverifikasi.
- **Penomoran residual #8–#13 tidak menimpa #1–#7** (L46), sesuai mandat.

### DITOLAK

| # | Lokasi | Klaim laporan | Kenyataan terukur |
|---|---|---|---|
| #16 | L26 / L27 / L28 | 219 / 247 / 108 baris | **212 / 370 / 174** |
| #16 | L157 | "194 passed (191 lama + **3 baru**)" | **213 total, 19 baru** |
| #16 | L311-329 | 19 tes dikutip sebagai `test_build_features.py::` | **semuanya ada di `test_build_labels.py`** |
| #18 | L40 | "data/labels/ **tidak ada di .gitignore**" | `.gitignore:24` = `data/labels/` — justru **di**-ignore |
| #18 | L88 / L244 / L250 | `RV_REGIME_THRESHOLD` / `RV_REGIME_THRESHOLD_PLACEHOLDER` = `3.648e-5 / 20` "tertulis di kode" | **identifier dan nilainya nol kemunculan** di `build_labels.py` |
| #18 | L214 | "setiap test pengunci gagal saat kode dicabut" | **FALSE** — 2 dari 7 mutan bertahan |
| #19 | L37 / L305 | tabel hash | diisi "(cek dengan git hash-object)" — bukan hash |
| #19 | L51 | residual #9 = MEDIUM | harus **HIGH** (false negative senyap) |
| #19 | L52 | residual #10 = LOW | harus **BLOCKER** |
| #19 | L1 | judul "Fase 1 - F-2/F-3/F-4" | label scope tidak konsisten dengan isi (D1–D5) |

**Detail atribusi tes (L311-329).** Laporan mengutip 19 nama tes sebagai
`tests/test_build_features.py::...`. Verifikasi string di kedua berkas:

```
TestClassifyDayLabel       build_features=False  build_labels=True
TestLondonDrift4h          build_features=False  build_labels=True
TestGapF2Flag              build_features=False  build_labels=True
TestRvRegimeFlag           build_features=False  build_labels=True
TestQuarantineMask         build_features=False  build_labels=True
TestDuaVarian              build_features=False  build_labels=True
TestKarantinaEksklusi      build_features=False  build_labels=True
TestBuktiMutasi            build_features=False  build_labels=True
TestRegisterH2Strategy     build_features=False  build_labels=True
```

`test_build_features.py` byte-identik dengan HEAD dan **tidak memuat satu pun**
dari kelas tersebut.

**Detail konstanta fiktif (L88/244/250).** `build_labels.py` baris 30-33 hanya
memuat komentar menyatakan ambang belum ditentukan:

```
30  # Ambang H3 (rv_roll_20d / 20 hari-broker; sum, bukan mean; dari B1-4)
31  # TIDAK ADA di lock → ditulis di protokol sebagai "belum ditentukan"
32  # DILARANG memakai nilai dari data sebagai vonis.
33  # Placeholder ini HANYA untuk protokol, TIDAK untuk vonis.
```

Tidak ada konstanta, tidak ada angka `3.648`, tidak ada `_PLACEHOLDER`.
Pernyataan laporan "nilai ini … hanya tertulis di kode sebagai dokumentasi"
berlawanan dengan isi berkas.

---

## Prohibisi & hash — TERKONFIRMASI (9 dari 9)

| Prohibition | Status | Bukti |
|---|---|---|
| File lama tak tersentuh | DIPATUHI | `build_features.py` `399e64b372e430b6def79b4fa8324a4e8e629918` = HEAD; `test_build_features.py` `ed7ac43520c4431519d4d7065504866ae9b3ad95` = HEAD |
| Parquet produksi tak ditulis ulang | DIPATUHI | `07402f40478aaed9391203f5db3237d636f5a959` cocok kontrak |
| Tak ada backtest H2 | DIPATUHI | nol kode backtest/equity/pnl/win_rate; hanya komentar larangan (L3, L137, L173) |
| Tak ada eksklusi buta via `gap_f2_flag` | DIPATUHI | `quarantine_mask` hanya memakai `ANOMALY_WINDOWS` |
| Tak ada vonis H4/H5 | DIPATUHI | protokol L154-162 |
| H6+ tidak dibuat | DIPATUHI | tidak ada artefak H6 |
| Tak ada file ke-6 | DIPATUHI | 5 deliverable + 1 laporan, persis |
| Tak ada commit | DIPATUHI | HEAD masih `e0b2b9f` (pre-batch) |
| Tak ada staging | DIPATUHI | `git diff --cached --name-only` kosong |

### Karantina 19 hari — TERKONFIRMASI pada store produksi

```
ANOMALY_WINDOWS : [('2024-10-28','2024-11-01'), ('2026-03-10','2026-03-27')]
flagged broker-days : 19
flagged bars        : 1748 / 90041
```

Daftar hari cocok persis dengan F-1: 5 hari Oktober 2024 + 14 hari Maret 2026.
Ini klaim D1 yang paling kuat dan harus dipertahankan.

### Gate

```
pytest penuh        : 213 passed in 11.00s, nol skip/deselect/xfail
komposisi           : 37 + 19 + 16 + 29 + 35 + 31 + 46 = 213
ruff check .        : All checks passed  (seluruh repo)
ruff format --check : 2 files already formatted
check_foreign_chars : OK: 4 file discan, tidak ada karakter asing
```

Mojibake `�?` / `�%` yang muncul di konsol PowerShell hanyalah artefak
encoding terminal. Byte berkas valid UTF-8; hanya mengandung simbol legitimate
(em dash, section sign, `≤`, `≥`, Sigma, arrow).

---

## Temuan Baru bernomor (lanjutan #13)

Penomoran dilanjutkan dari #13 sesuai mandat; tidak ada nomor yang ditimpa.

| # | Severity | Temuan |
|---|---|---|
| **#14** | **BLOCKER** | D1 tidak dapat dijalankan pada store (`KeyError: close`); `london_drift_norm` + assert paritas tidak ada; D4 kedua file byte-identik, karantina kosong, nama kontrak tidak terpenuhi |
| **#15** | **HIGH** | Pelanggaran "tanpa jam-lokal baru": jendela 8–12 UTC berbeda dari 16 bar `is_london` pertama pada **60,6%** broker-day; `compute_gap_f2_flag` false negative senyap |
| **#16** | **HIGH** | `TestBuktiMutasi` terbalik — meng-assert mutan berhasil, tidak pernah gagal pada logika terkunci yang diggut |
| **#17** | **HIGH** | S3 hilang dari protokol; dokumen putusan S1–S6 tidak pernah dikutip; tidak ada tes `main()`; jendela sesi London dan varian eksklusi tidak terkunci |
| **#18** | **MEDIUM** | Laporan: jumlah tes salah (194/3 vs 213/19), 19 tes salah diatribusikan ke `test_build_features.py`, konstanta `RV_REGIME_THRESHOLD` fiktif, klaim .gitignore terbalik, kontradiksi rv_roll_20d, S4 & larangan H4/H5 salah atribusi |
| **#19** | **MEDIUM** | Severity residual #9/#10 salah (MEDIUM→HIGH, LOW→BLOCKER); tabel hash tidak diisi; judul tidak konsisten; pra-registrasi H2 di kode kurang spesifik dari protokol; typo L35 |

*Observasi (bukan vonis):* `data/labels/` memuat 7 subdirektori
(`D1, H1, H4, M1, M15, M30, M5`) berisi `.gitkeep` 1 byte. Tidak ada di HEAD dan
ter-ignore, sehingga provenance-nya tidak dapat diverifikasi lewat git.
Materialitas rendah.

---

## VERDICT AKHIR: GAGAL

Fase 1 **tidak boleh** naik ke Lapisan 3. Alasannya bukan kosmetik:

1. **D1 tidak hidup.** Pipeline label tidak dapat dieksekusi pada data store.
   Artefak D4 karena itu tidak mungkin berasal dari kode yang dikirim.
2. **D4 tidak memenuhi kontrak** pada kedua nama file; deliverable "dua varian"
   hanya satu file yang diduplikasi.
3. **D3 kehilangan syarat terkunci S3** dan tidak pernah merujuk dokumen yang
   memuat S1–S6.
4. **D5 evidentiary claims false** — jumlah tes, atribusi tes, bukti mutasi, dan
   satu konstanta fiktif. Laporan ini tidak dapat dipakai sebagai dasar
   persetujuan.

Yang **tidak boleh** ikut diruntuhkan: ambang H1 `0.0268`/`88.79`, karantina 19
hari, arah impor tanpa siklus, anggaran baris, hashes file lama, larangan optimasi
ambang dari data, larangan eksklusi buta, dan larangan backtest. Semua itu benar
dan terbukti.

---

## Syarat sebelum Lapisan 3

### Blocking — kode & protokol

1. Perbaiki `compute_london_drift_4h` agar tidak bergantung pada kolom `close`
   yang tidak ada di store — atau usulkan penambahan `close` ke store sebagai
   perubahan arsitektur terpisah dengan persetujuan arsitek.
2. Implementasikan `london_drift_norm` dan `assert` paritas satuan yang
   sebenarnya, sesuai putusan B1-3.
3. Ganti jendela `hour_utc 8–12` dengan "16 bar `is_london` paling awal per hari"
   sesuai kontrak §2.
4. Tulis ulang D4 dengan nama kontrak `usdjpy_day_labels.parquet` dan
   `usdjpy_h2_trades.parquet`, dibangun dari store produksi, dengan kedua varian
   benar-benar berbeda dan tabel selisih terlampir.
5. Tambahkan S3 ke protokol dan kutip `putusan-arsitek-H1-H5.md` sebagai sumber
   S1–S6.
6. Pindahkan D3 ke `reports/governance/2026-10-07/`.
7. Tulis ulang `TestBuktiMutasi` agar benar-benar **gagal** pada kode rusak;
   tambahkan tes untuk jendela sesi London, varian eksklusi di `main()`, dan satu
   uji end-to-end `main()`.

### Blocking — integritas laporan

8. Perbaiki D5: jumlah tes (213 total / 19 baru), atribusi 19 tes ke
   `tests/test_build_labels.py`, hapus klaim `RV_REGIME_THRESHOLD`, koreksi klaim
   `.gitignore`, isi tabel hash dengan nilai sebenarnya.
9. Naikkan severity residual #9 ke HIGH dan #10 ke BLOCKER.

### Pasca pemblokiran 1-7

`compute_gap_f2_flag` dan `compute_rv_regime_flag` harus **tetap gagal keras**
sampai tersedia akses M1 dan penentuan ambang RV. Jangan diubah menjadi nilai
default senyap.

---

## Lampiran A — Hash objek yang diaudit (jejak integritas)

Diukur saat audit, setelah seluruh pemeriksaan selesai.

| Objek | Git blob hash (16 depan) | Status |
|---|---|---|
| `src/features/build_labels.py` | `16d3ca239e669e4c` | tidak diubah oleh audit |
| `tests/test_build_labels.py` | `492c164f4f8699c2` | tidak diubah oleh audit |
| `protokol-H1-H2-H3.md` | `d045ab0d598c1eff` | tidak diubah oleh audit |
| `laporan-final-fase1.md` | `13d703b58453dfe4` | tidak diubah oleh audit |
| `data/labels/usdjpy_labels.parquet` | sha256 `fddb6f28c37db224…` | identik dengan varian eksklusi |
| `data/labels/usdjpy_labels_excluded.parquet` | sha256 `fddb6f28c37db224…` | identik dengan varian inklusi |

Artefak lama pembanding (byte-identik dengan `HEAD`):

| Objek | Hash | Cocok HEAD |
|---|---|---|
| `src/features/build_features.py` | `399e64b372e430b6def79b4fa8324a4e8e629918` | Ya |
| `tests/test_build_features.py` | `ed7ac43520c4431519d4d7065504866ae9b3ad95` | Ya |
| `data/features/M15/usdjpy_m15_features.parquet` | `07402f40478aaed9391203f5db3237d636f5a959` | Ya (kontrak) |
| `src/features/__init__.py` | `94f723ce120d9ca3c7055a7ed1aa158ff91f6a93` | Ya |

## Lampiran B — Hash dokumen ini

| Berkas | Baris | SHA-256 |
|---|---|---|
| `reports/governance/2026-10-07/Audit/reaudit-adversarial-D1-D5.md` | 507 | `4c180fe62b8906657ee668110c42846cc35ed2a5710b23b8b55d1d6bc2ea8ce4` |

Gate `check_foreign_chars.py`: **OK** (0 karakter asing).

## Catatan integritas audit

Tidak ada file artefak audit (D1–D5) yang diubah oleh audit ini. Seluruh
mutasi dijalankan in-memory. Status akhir repo tetap 4 file untracked baru
(`build_labels.py`, `test_build_labels.py`, `protokol-H1-H2-H3.md`,
`laporan-final-fase1.md`), tanpa staging, tanpa commit, `HEAD` masih `e0b2b9f`.
Berkas di dalam `Audit/` adalah satu-satunya hasil yang ditulis.