# Re-audit F-2, F-3, F-4 - `build_features.py`

Tanggal: 2026-10-07
Status: adjudikasi selesai, ketiga temuan memiliki vonis
Diff yang diaudit: `1c9da4b4` -> `2f9986bc`

## SCOPE

Hanya F-2, F-3, F-4. F-1 tidak dibuka ulang; angka EDA tidak disentuh;
keputusan arsitek di luar batch ini tidak diadjudikasi.

## VONIS RINGKAS

| Temuan | Kriteria terima | Vonis | Catatan |
|---|---|---|---|
| F-2 | angka efek verbatim, `m1_bars` di luar store, klaim konsumen berbukti | **TERTUTUP dgn residual** | angka efek 2 dari 4; klaim H1/H5 tanpa bukti |
| F-3 | janji palsu hilang, return 0, `FileNotFoundError` tak tertangkap | **TERTUTUP** | terbukti eksekusi; contract rapuh |
| F-4 | assertion bunyi saat imbalance, 974=974 tetap hijau | **TERTUTUP dgn DEFECT** | label pesan tertukar M1/M15 |
| Budget | module 400, `daily_metrics` 50 | **SAH-SEBAGAI-BATAS** | headroom nol, split B2 wajib |

## IDENTITAS ARTEFAK

| Artefak | Hash git | Catatan |
|---|---|---|
| `src/features/build_features.py` | `2f9986bcbaeedda6ce555fb06b649e5ded32c635` | cocok dengan mandat |
| `tests/test_build_features.py` | `96d06f6fc9bca31cd02362bb438fe6acaff8b4d9` | cocok dengan mandat |
| `data/features/M15/usdjpy_m15_features.parquet` | `07402f40478aaed9391203f5db3237d636f5a959` | tidak berubah |
| `reports/governance/2026-10-07/putusan-arsitek-B1.md` | `91d4c99307e3750e78802b5b424af579e2113249` | sumber blokir lama, kini ada |

Parquet: 90.041 baris x 11 kolom, 962.348 byte,
sha256 `cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb`.

Ketiga hash di atas diverifikasi ulang setelah semua probe selesai, dan
ketiganya masih cocok dengan mandat, jadi tidak ada probe yang mengubah
file produksi. Hash laporan ini sendiri tidak bisa dicantumkan di
dalamnya, karena setiap penulisan mengubah hash. Hitung ulang dengan
`git hash-object reports/governance/2026-10-07/reaudit-F2-F3-F4.md`.

---

## F-2 - `m1_bars` di luar feature store

### Kriteria dan bukti

**K1: angka efek diteruskan verbatim tanpa downgrade - LOLOS.**

`test_f2_m1_bars_not_in_feature_columns` (tests/test_build_features.py:295)
memuat dua dari empat angka asli:

```
median ratio_path +0.019% (audit fondasi B1, 597 bucket mid-day)
range_atr 0.000% karena OHLC D1 berasal dari M15, tidak terpengaruh
```

Saya ukur ulang sendiri di data produksi, pada himpunan 223 hari yang punya
counterfactual (hapus bar M1 bucket mid-day partial, hitung ulang):

| Besaran | Doktrin | Audit asli | Ukuran ulang |
|---|---|---|---|
| n hari | - | 223 | 223 |
| median `ratio_path` | +0,019% | +0.019% | **+0.019%** |
| p95 `ratio_path` | +0,28% | +0.280% | **+0.280%** |
| maks `ratio_path` | +1,06% | +1.055% | **+1.055%** |
| `range_atr` | 0,000% | 0.000% | **0.000000%** (n=221) |

Angka tereproduksi persis. Tidak ada penurunan derajat di dalam batch.

Catatan: probe awal saya melaporkan median +0.014% pada n=234. Itu
selisih hitungan, bukan selisih magnitudo. 234 hari memuat bucket mid-day
partial, tapi hanya 223 punya bar M1 yang bisa dihapus; pada 11 hari
lanjutan bucket justru partial KARENA bar M1-nya sudah absen di store
M1, jadi tidak ada counterfactual untuk dihapus. Setelah himpunan hari
dibatasi pada yang punya counterfactual, median tepat +0.019%.

**K2: `m1_bars` tetap di luar store - LOLOS.**

```
FEATURE_COLUMNS = ['is_tokyo','is_london','is_ny','is_sydney','session_label',
                   'hour_utc','date_broker','atr_14_d1','rv_roll_20d',
                   'range_atr','ratio_path']
'm1_bars' in FEATURE_COLUMNS = False
parquet columns              = 11 kolom, sama persis
'm1_bars' in parquet         = False
```

**K3: parquet tidak berubah - LOLOS.** Hash git identik dengan baseline.

**K4: klaim "B2-H1/H5 tidak terpengaruh material" - GAGAL DIBUKTIKAN.**

Docstring test pada baris 305-306 menyatakan:

```
Konsumen B2-H1 (tipologi) dan B2-H5 (kuartil ATR) tak terpengaruh
material karena efeknya kecil (LOW, bukan MEDIUM).
```

Satu-satunya pernyataan eksekutable di test itu adalah:

```python
assert "m1_bars" not in FEATURE_COLUMNS
```

Tidak ada test yang mengukur `ratio_path`, tidak ada test yang menjalankan
klasifikasi H1, tidak ada test yang memeriksa kuartil H5, tidak ada test
yang mengunci angka +0.019%. Klaim materialitas adalah prosa di dalam
docstring, bukan assertion. Saya tidak bisa menutupnya sendiri dan tidak
perlu mengulang build store dengan M1 yang dimodifikasi untuk menutupnya:
itu akan menulis ulang parquet, yang dilarang mandat.

Yang saya ukur sebagai ganti: dari store, 959 hari broker dapat
diklasifikasi dengan ambang H1, campuran 330 trending / 324 range /
305 normal. Ambang dan mekanisme klasifikasi itu ada dan bisa diuji.
Yang belum ada adalah pembuktian bahwa 234 hari gap tersebut jatuh ke
bucket yang sama dengan data lengkap.

### Vonis F-2

**TERTUTUP dengan residual.** Yang ditutup adalah keputusan store: `m1_bars`
tetap di luar `FEATURE_COLUMNS` dan parquet, dan angka efeknya sendiri
terbukti benar serta tidak diturunkan. Yang tidak ditutup adalah klaim
materialitas konsumen, karena dalilnya hanya prosa.

Residual F-2:
1. Klaim materialitas B2-H1/H5 belum berbukti. Perlu test klasifikasi pada
   234 hari gap, atau klaim itu dilabel "belum diuji" di repo.
2. p95 (+0.28%) dan maksimum (+1.06%) tidak dibawa ke docstring test.
   Bukan penurunan, tapi jejak audit jadi tidak lengkap di tempat yang
   akan dibaca orang berikutnya.

---

## F-3 - kontrak return dan exit `main()`

### Kriteria dan bukti

**K1: janji palsu hilang - LOLOS.** Tujuh pola dikecolom:

| Pola | Hit |
|---|---|
| `returns 1` | 0 |
| `return 1` | 0 |
| `status 1` | 0 |
| `exit code 1` | 0 |
| `keluar 1` | 0 |
| `exit code 1 if` | 0 |
| `returns 1 if` | 0 |

Docstring `main()` kini jujur: "Selalu 0. `FileNotFoundError` dari
`load_processed` tidak tertangkap dan akan membuat interpreter keluar
dengan kode 1 - perilaku yang diperoleh secara kebetulan, bukan yang
dijanjikan."

**K2: jalur sukses mengembalikan 0 - LOLOS, via eksekusi.**

```
argv        : -m src.features.build_features --out <temp>
exit code   : 0
temp file exists : True
```

**K3: data hilang menghasilkan `FileNotFoundError` tak tertangkap dan
exit 1 - LOLOS, via eksekusi.** Loader asli diarahkan ke direktori kosong
lewat `load_processed.__defaults__`, lalu `main()` dipanggil tanpa
penangkap:

```
PROCESSED_DIR rebound to : <temp>\processed
directory contents       : [] (empty)
exit code                : 1
Traceback (most recent call last):
  File "src/features/build_features.py", line 382, in main
    m1 = load_processed("M1", symbol)
  File "src/features/build_features.py", line 205, in load_processed
    raise FileNotFoundError(
FileNotFoundError: Tidak ada parquet M1 untuk USDJPY di <temp>\processed\M1

FileNotFoundError raised  : True
main() returned normally  : False
output file created       : False
```

`main()` tidak pernah balik. Traceback keluar dari
`load_processed` di baris 205, menembus `main()` di baris 382, lalu
interpreter mati dengan kode 1. Tidak ada file output yang dibuat.

### Vonis F-3

**TERTUTUP.** Semua tiga kriteria terpenuhi dan dibuktikan dengan
eksekusi, bukan pembacaan docstring.

Residual F-3:
1. Kontrak ini rapuh secara konstruksi. `return 0` di baris 396 adalah
   literal tanpa cabang; tidak ada branch sukses/gagal di `main()` sama
   sekali. Exit 1 bergantung sepenuhnya pada exception yang lolos. Siapa
   pun yang nanti membungkus `main()` dalam `try/except` akan mengubah
   exit code tanpa satu pun test yang menangkapnya.
2. Tidak ada test yang memanggil `main()` sama sekali. Kontrak ini tidak
   terkunci regresi.

---

## F-4 - assertion panjang join

### Kriteria dan bukti

**K1: assertion membunyakan alarm keras saat imbalance - LOLOS.**

Assertion di `src/features/build_features.py:249-253`:

```python
daily = daily_bars.join(intraday, how="inner")
if len(daily) != len(daily_bars) or len(daily) != len(intraday):
    raise ValueError(
        f"daily_metrics: join hilang - M1 {len(daily_bars)}, M15 {len(intraday)}, "
        f"join {len(daily)}. Cek cakupan tahun."
    )
```

Empat bentuk imbalance diuji pada data produksi:

| Skenario | Hasil |
|---|---|
| potong M1 saja | `ValueError: join hilang - M1 974, M15 145, join 145` |
| potong M15 saja | `ValueError: join hilang - M1 145, M15 974, join 145` |
| satu hari broker hilang dari M1 | `ValueError: join hilang - M1 974, M15 973, join 973` |
| dua hari broker hilang dari M1 | `ValueError: join hilang - M1 974, M15 972, join 972` |

Termasuk kasus satu hari, jadi ini bukan hanya deteksi pemotongan
year-to-date. Tetap keras pada asimetri kecil.

**K2: data seimbang tetap hijau dan output identik - LOLOS.**

```
M1 days = 974, M15 days = 974
daily rows = 974
build_features OK: 90041 rows x 11 cols
parquet hash sebelum = sesudah = 07402f40478aaed9391203f5db3237d636f5a959
```

**K3: DEFECT - label pada pesan tertukar.**

`daily_bars` dibangun dari M15 di baris 238. `intraday` dibangun dari M1
di baris 244. Tapi baris 251 mencetak `daily_bars` sebagai "M1" dan
`intraday` sebagai "M15". Bukti, dari skenario potong M1 saja:

```
ground truth  : true M1 days = 145, true M15 days = 974
pesan yang keluar: "M1 974, M15 145"
```

Kedua angka dicetak, tapi keduanya terpasang ke timeframe yang salah.
Operator yang menyelidiki gap cakupan akan diberi tahu timeframe yang
memang pendek justru yang terlihat penuh.

Ini defect baru yang diperkenalkan batch ini, di dalam ruang lingkup F-4
sendiri, dan ia menetralkan tujuan diagnostic sebuah assertion. Bukan
selera rasa: pesan yang salah membuat diagnosis yang salah.

### Vonis F-4

**TERTUTUP dengan DEFECT.** Seluruh kriteria terima lolos: assertion
benar-benar membunyakan alarm pada empat bentuk imbalance, data seimbang
tetap hijau, output identik. Yang belum selesai adalah defect pada kode
baru itu sendiri: label M1/M15 di baris 251 harus ditukar. Perbaikan
satu baris, tidak mengubah perilaku assertion.

Residual F-4:
1. **MEDIUM - action wajib.** Tukar argumen di baris 251 agar
   `M1 {len(intraday)}, M15 {len(daily_bars)}`.
2. Tidak ada test yang mengunci assertion ini. Jumlah test naik 34 -> 35,
   dan satu-satunya tambahan adalah test F-2. `TestDailyMetrics` tidak
   punya kasus imbalance. Assertion ini bisa dihapus tanpa test gagal.

---

## BUDGET - verdict eksplisit

| Objek | Budget | Aktual | Status |
|---|---|---|---|
| `src/features/build_features.py` | 400 baris | **400** baris fisik | batas, headroom 0 |
| `daily_metrics` | 50 baris | **50** baris (213-262, span AST) | batas, headroom 0 |

Dihitung ulang dari file, bukan dari klaim. Module berakhir dengan newline.
Tidak ada fungsi lain di file yang mencapai 40 baris atau lebih.

**Vonis: SAH-SEBAGAI-BATAS.** Tidak ada hak menambah satu baris pun ke
`build_features.py` maupun `daily_metrics`. Zero headroom bukan
pelanggaran, tapi setiap perubahan berikutnya wajib lewat pemecahan
fungsi, bukan penambahan inline.

Konsekuensi yang harus diterima sekarang: pemisahan yang diwajibkan di
B2 bukan pilihan operasional melainkan jalan satu-satunya. Batch berikutnya
yang menyentuh file ini akan menabrak batas ini pada perubahan pertama.

Perlu dicatat: assertion F-4 sendiri memakan budget. Ia hidup di baris
249-253, di dalam fungsi yang sudah tepat di 50/50.

---

## GATE

```
venv\Scripts\python.exe -m pytest -q
  192 passed in 8.71s                                    EXIT=0

venv\Scripts\python.exe -m pytest tests/test_build_features.py -q
  35 passed in 7.90s                                     EXIT=0

venv\Scripts\python.exe -m ruff check src/features/build_features.py tests/test_build_features.py
  All checks passed!                                     EXIT=0

venv\Scripts\python.exe -m ruff format --check src/features/build_features.py tests/test_build_features.py
  2 files already formatted                              EXIT=0

venv\Scripts\python.exe scripts/check_foreign_chars.py src/features/build_features.py tests/test_build_features.py
  OK: 2 file discan, tidak ada karakter asing.            EXIT=0

venv\Scripts\python.exe scripts/check_foreign_chars.py reports/governance/2026-10-07/reaudit-F2-F3-F4.md
  OK: 1 file discan, tidak ada karakter asing.            EXIT=0
```

Baseline audit-fondasi-B1: 191 passed, 34 di `test_build_features`.
Sekarang: 192 dan 35. Delta +1 test, dan itu test F-2. Nol test baru untuk
F-3 dan F-4.

Probe independen yang dijalankan di luar suite pytest: 7 berkas, 2 di antaranya
mandatory (F-4 imbalance, F-3 eksekusi). Daftar lengkap ada di bagian bawah.

---

## STATUS BLOKIR B1 (hanya status, tanpa penilaian ulang)

Blokir lama pada `audit-fondasi-B1.md:157` berbunyi "BLOKIR: KEPATUHAN B1
TIDAK DAPAT DITUTUP", dengan B1-3 dan B1-4 tercatat "TIDAK DAPAT
DIADJUDIKASI" karena sumbernya tidak ada di repository.

Blokir itu kini tertutup sebagai blokir sumber. `putusan-arsitek-B1.md`
sudah ada di repository (5.474 byte, hash
`91d4c99307e3750e78802b5b424af579e2113249`) dan memuat keempat butir,
termasuk Butir 3 (satuan `atr_14_d1` dan normalisasi H1) serta Butir 4
(semantik `rv_roll_20d`).

Saya tidak menilai ulang isi B1-3 atau B1-4 di sini, sesuai batas mandat.
Yang dicatat hanya: sumber yang dulu hilang sudah tersedia, sehingga
adjudikasi B1-3/B1-4 kini tidak lagi terblokir.

---

## KETERBATASAN VERIFIKASI

**Diff byte-level lama ke baru tidak dapat dibuat.** Blob lama sudah hilang
dari object database dan kedua file untracked:

```
fatal: bad revision '1c9da4b4'
fatal: Not a valid object name 1c9da4b4d6d108de
```

Adjudikasi karena itu dijalankan terhadap state aktual file, hash aktual,
kriteria terima di `audit-fondasi-B1.md`, dan docstring yang dibawa coder,
bukan terhadap diff yang dibangkitkan git. Angka efek F-2 saya turunkan
sendiri dari data produksi, sehingga tidak bergantung pada diff.

**Probe F-3 pertama menimpa parquet produksi.** `load_processed` punya
`base: Path = PROCESSED_DIR` sebagai default argument di baris 183. Default
dievaluasi sekali saat fungsi didefinisikan, jadi `bf.PROCESSED_DIR = <temp>`
tidak mengubah apa pun. Loader tetap membaca produksi dan `main()` menulis
ulang store.

Dampaknya nihil pada konten: hash git tetap
`07402f40478aaed9391203f5db3237d636f5a959`, sha256 tetap
`cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb`, ukuran
tetap 962.348 byte. Tidak ada perubahan isi file produksi. Probe ditulis
ulang dengan `load_processed.__defaults__` dan `--out` ke direktori
temp, dan probe kedua memastikan hash tidak bergeser. Timestamp file
memang berubah karena penulisan ulang itu, dan itu satu-satunya jejak
yang tersisa.

---

## RESIDUAL KONSOLIDASI

| # | Temuan | Severity | Status |
|---|---|---|---|
| 1 | F-4 pesan tertukar M1/M15 (baris 251) | MEDIUM | action wajib, 1 baris |
| 2 | F-2 klaim materialitas H1/H5 hanya prosa | MEDIUM | perlu test klasifikasi 234 hari |
| 3 | Tidak ada test yang mengunci assertion F-4 | MEDIUM | `TestDailyMetrics` perlu kasus imbalance |
| 4 | Tidak ada test yang memanggil `main()` (F-3) | LOW | kontrak exit tidak terkunci |
| 5 | `return 0` hardcoded tanpa branch gagal | LOW | exit 1 bergantung pada exception yang lolos |
| 6 | p95 dan maksimum tidak dibawa ke docstring F-2 | LOW | jejak audit tidak lengkap |
| 7 | Budget 400/400 dan 50/50, headroom 0 | LOW | pemisahan B2 menjadi wajib |

Tidak ada residual yang memblokir vonis di atas.

---

## SELF-AUDIT

**Putaran 1 - konsistensi vonis dengan bukti.**
F-2 ditutup karena K1-K3 lolos dan K4 gagal; ini konsisten karena K4
saya nyatakan gagal eksplisit di Residual, bukan disembunyikan di vonis.
F-3 ditutup karena ketiga kriteria punya bukti eksekusi, bukan argumen
docstring. F-4 ditutup pada kriteria terima, dan DEFECT saya tulis di status
vonis bukan di paragraf pembuka, supaya tidak hilang. Tidak ada temuan yang
ditutup dengan "terbukti" tanpa probe yang benar-benar dijalankan.

**Putaran 2 - kehati-hatian klaim.**
Angka +0.019%/+0.280%/+1.055% dihitung ulang oleh saya dari data produksi,
jadi tidak bergantung pada docstring yang sedang diaudit. Parquet hash
dihitung ulang, bukan dipercaya. Budget dihitung ulang lewat AST. Yang
tidak saya klaim: bahwa F-2 menutup materialitas konsumen (tidak), bahwa
assertion F-4 punya regression test (tidak ada), bahwa diff lama bisa
dibuktikan (tidak bisa). Selisih median +0.014% vs +0.019% saya telusuri
sampai ke sebabnya dan saya laporkan, bukan saya bulatkan.

**Putaran 3 - kepatuhan aturan.**
Tidak ada file produksi yang saya ubah. Satu-satunya file yang saya tulis
adalah laporan ini dan probe di direktori temp. Karakter asing: hanya
huruf Latin dan tanda baca ASCII yang saya pakai; gate
`check_foreign_chars` dijalankan pada laporan ini juga dan hasilnya
dicantumkan di bagian GATE. Placeholder karakter Han yang tercatat di
`audit-fondasi-B1.md` tidak saya pulihkan ke sini. F-1 tidak saya sentuh.

---

## INVENTARIS PROBE

| Berkas | Isi |
|---|---|
| `p1_f4_fire.py` | budget AST, sumber assertion, 4 bentuk imbalance, baseline |
| `p2_f4_oneday.py` | verifikasi kasus satu hari broker |
| `p3_f2.py` | empat angka verbatim, klaim konsumen, hash parquet, ukur ulang efek |
| `p4_reconcile.py` | rekonsiliasi selisih 234 vs 223 hari |
| `p5_reconcile2.py` | pemisahan 223 hari ber-counterfactual vs 11 hari tanpa |
| `p6_f3_exec.py` | grep janji, jalur sukses, jalur gagal (menimpa parquet) |
| `p7_f3_exec_safe.py` | F-3 eksekusi ulang dengan patching aman |

Semua di `C:\Users\Fajar\AppData\Local\Temp\opencode\rf234\`.
