# RE-AUDIT INDEPENDEN H4b - STABILITAS LINTAS-TAHUN

**Ronde:** re-audit adversarial H4b (A1-A7)
**Tanggal audit:** 2026-10-09
**Branch:** `codex/ANN`
**HEAD saat audit:** `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`
**Auditor:** independen, replikasi dari nol (tidak mengimpor `h4b.py`)
**Status dokumen:** LULUS DENGAN CATATAN

> Dokumen ini sengaja ditulis ASCII/LF-only agar pengikatan eksternal
> (sha256 + git hash-object) stabil lintas mesin.

---

## 0. Pengikatan Input (S0) - LOLOS

Sesi auditor mengukur ulang sendiri (bukan menyalin angka coder).
Mismatch = STOP. Hasil: 8/8 cocok.

| Objek | Nilai terukur sesi auditor |
|---|---|
| `HEAD` | `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` |
| Branch | `codex/ANN` |
| `git hash-object` dokumen coder H4b | `6410b1800f6dc46ec511949e1311fcda853b0807` |
| `git hash-object` spec H4b | `0437b563c85e578567eb58b8cfe6b0dd3ef02b47` |
| `git hash-object` spec lapisan3 H4H5 | `4a46b815211e6b0b050cbb6f3e98ce5e27904069` |
| `git hash-object` hasil coder lapisan3 H4H5 | `f06a8e27b916172f5824438acd545614360d3b57` |
| `git hash-object` reaudit lapisan3 H4H5 | `8a4d21090f27dd53555b3a12583ec337819efb2f` |
| `git hash-object` putusan lapisan3 H4H5 | `e02a203b96879d73e90339f2d78a37d15834a23a` |

Gate staged: `git diff --cached --name-only` menghasilkan **tepat 2** file
T6, tidak tersentuh oleh ronde ini:

```
src/features/build_labels.py
tests/test_build_labels.py
```

Blob staged terukur sesi ini:

- `src/features/build_labels.py` = `2561efd552544feeb9af0b6733711015b83f43dd`
- `tests/test_build_labels.py` = `dc07a7e651d38f07a5cabbe4e693b10681312d25`

Input beku (spec H4b baris 38-51), diverifikasi ulang sebelum hitung:

| Input | sha256 |
|---|---|
| M1 2024 | `69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac` |
| M1 2025 | `fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af` |
| M15 store | `cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb` |
| D4 labels | `47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c` |

Harness coder (`%TEMP%\opencode\h4b`):
`h4b.py` = `1bbaf42703825339380fca2aa99dfe32ae25c0af32ff794faaeff1b33a5216c7`

---

## 1. Ringkasan Verdict per A1-A7

| # | Butir | Verdict |
|---|---|---|
| A1 | Replikasi angka inti | **COCOK** |
| A2 | Gate anti-intip | **COCOK** (1 catatan LOW) |
| A3 | Definisi Off beku + verifikasi lock | **COCOK** (1 eskalasi arsitek) |
| A4 | Larangan data 2026 / tanpa H6 | **COCOK** |
| A5 | Cross-validation ke Batch-2 | **SAH** |
| A6 | Determinisme artefak | **COCOK** |
| A7 | Provenance / integritas dokumen | **COCOK** (1 catatan LOW) |

**Verdict audit keseluruhan: LULUS DENGAN CATATAN.**

Tidak ada temuan severity MEDIUM/HIGH. Dua catatan LOW dan satu eskalasi
arsitek tercatat di bagian 9. Tidak ada vonis resmi yang Auditor
terbitkan; vonis resmi tetap wewenang arsitek.

---

## 2. A1 - Replikasi Angka Inti (COCOK)

Metode: skrip auditor `a1_replika.py` membangun ulang pool dari parquet
M1/M15/D4 memakai resep mesin beku (`build_features`, `_eda_common.add_labels`,
config), **tanpa** mengimpor atau memanggil `h4b.py`. Sesi, cost, dan
join-gate diperiksa ulang sebelum statistik.

Verifikasi pra-hitung (output mentah `a1_out.txt`):

```
pip size            : 0.01
cost London         : 0.61
cost NewYork        : 0.69
cost Tokyo          : 0.62
cost Sydney         : 0.8
cost default(Off)   : 0.65
sha M1 2024         : 69b2c026...cac  COCOK
sha M1 2025         : fce65a3a...8af  COCOK
sha M15             : cd6a85e4...0fb  COCOK
sha D4              : 47d15c41...d6c  COCOK
join-gate n bar     : 47721 == 47721  COCOK
sequens broker_day  : identik          COCOK
```

Maju (train 2024 -> uji 2025):

```
top6 jam train       : [14, 13, 12, 0, 15, 7]
n_trade             : 1554
exit SL/TP/time_stop : 71 / 6 / 1477   (71+6+1477 = 1554 COCOK)
n_Off / any / maj   : 0 / 0 / 0
median EV           : -0.005049999999992838
mean   EV           : -0.0039283324140465484
fraksi positif      : 0.49356499356499356
counter hari        : 259 ; slot 1554 ; flat 0 ; n_trade 1554
quarantine trade    : 0 ; ATR NaN 0
lock arah           : a True (n_Off<=1), b False (median>0) -> gagal
```

Mundur (train 2025 -> uji 2024):

```
top6 jam train       : [14, 13, 0, 15, 1, 12]
n_trade             : 1560
exit SL/TP/time_stop : 94 / 12 / 1454   (94+12+1454 = 1560 COCOK)
n_Off / any / maj   : 0 / 0 / 0
median EV           : 0.05439999999999045
mean   EV           : 0.028821062271061976
fraksi positif      : 0.5551282051282052
counter hari        : 260 ; slot 1560 ; flat 0 ; n_trade 1560
quarantine trade    : 30 ; ATR NaN 0
lock arah           : a True, b True -> lolos
```

Per-jam off/n diverifikasi ulang **nol untuk ke-12 sel**:

```
Maju   14:0/15539 13:0/15537 12:0/15535 0:0/15534 15:0/15538 7:0/15535
Mundur 14:0/15595 13:0/15593 0:0/15599 15:0/15600 1:0/15600 12:0/15598
```

Selisih jam teratas dua arah (simetris): `{1, 7}`.

**Kesimpulan A1:** angka median, mean, fraksi, n, exit-cause, dan counter
karantina yang coder laporkan **cocok digit-per-digit** dengan replikasi
independen. Tidak ditemukan salah hitung.

---

## 3. A2 - Gate Anti-Intip (COCOK, 1 catatan LOW)

Struktur `h4b.py` (343 baris):

- `top6_train_only(train_year)` - `h4b.py:207-213`. Memfilter `pool_m1_full`
  ke `broker_day.dt.year == train_year` **sebelum** ranking, lalu assert
  kemurnian tahun di `h4b.py:209-211`.
- `run_arah(train_year, test_year)` - `h4b.py:234-260`. Mengsnapshot
  `hours_snapshot` di `h4b.py:237`, memfilter pool uji ke tahun uji di
  `h4b.py:238`, assert kemurnian di `h4b.py:239-241`, menjalankan trade di
  `h4b.py:242`, assert trade berada di jam terkunci di `h4b.py:245-247`,
  dan assert ranking train tidak berubah di `h4b.py:248-250`.
- `off_metrics(pool_test, hours)` - `h4b.py:216-231`, memakai `hours_snapshot`.

Uji sabotage yang Auditor kerjakan sendiri (membuktikan gate **tidak**
dekoratif):

Sabotase A - hapus filter tahun-train pada `top6_train_only`:

```
rc = 1
h4b.py:209  AssertionError: GATE ANTI-INTIP: pool M2 train 2024 bocor tahun lain
```

Sabotase B - ganti loop jam terkunci dengan `range(24)`:

```
rc = 1
h4b.py:245  AssertionError: GATE ANTI-INTIP: ada trade di luar 6 jam terkunci
```

Ketiga lapis assert (kemurnian train, kemurnian uji, kemurnian jam trade)
benar-benar menggigit. Gate anti-intip substantif dan berlapis.

**Catatan LOW-1** (`h4b.py:248-250`): assert "ranking train tidak berubah
sesudah loop uji" memanggil ulang `top6_train_only(train_year)` pada input
deterministik yang sama, lalu membandingkan hasilnya ke dirinya sendiri.
Guard ini secara logika **tidak mungkin gagal** kecuali ada
nondeterminisme. Ia tidak menambah keamanan; nilainya dokumentatif.
Ditempel karena dua lapis lain sudah kuat dan tidak ada bukti kebocoran
data, sehingga severity tetap LOW (bukan HIGH).

---

## 4. A3 - Definisi Off Beku + Verifikasi Lock (COCOK, eskalasi arsitek)

Definisi Off **diambil dari kode `_eda_common.py`, bukan dari prosa**:

- `SESSION_SPECS` dan prioritas sesi London > NewYork > Tokyo > Sydney >
  default Off - `_eda_common.py:17-38`.
- Fungsi `session_flags` memberi label default `Off` pada bar di luar
  jendela sesi mana pun - `_eda_common.py:41-74`.
- Definisi ini identik dengan P1 Batch-2.

Replikasi ulang `n_Off` dari pool M1 tahun-uji **memakai kode label yang
sama** menghasilkan 0 pada kedua arah dan 0 pada semua 12 sel per-jam
(lihat blok A1). Klaim `n_Off = 0` coder **terbukti benar**.

Penerapan lock H4b verbatim (spec baris 21-24), diverifikasi ulang:

```
GUGUR bila pada SATU PUN tahun-uji:
  (a) >= 2 dari 6 jam-teratas-train jatuh di Off, ATAU
  (b) median EV-after-cost pool tahun-uji <= 0.
TAHAN hanya bila KEDUA arah: n_Off <= 1 DAN median EV > 0.
```

Hasil: arah Maju (median `-0.00505 <= 0`) memenuhi (b); arah Mundur lolos
kedua kriteria. Karena "satu pun" cukup, lock = `GUGUR(H4b)`. Diterapkan
mekanis, tanpa statistik tambahan.

**Counter karantina F-1** (INKLUSI default, deskriptif saja):

```
D4 quarantine_mask total   : 19 hari
  2024 : 5 hari  (2024-10-28 .. 2024-11-01)
  2025 : 0 hari
  2026 : 14 hari (Maret 2026)  -> di luar pool uji, tidak dipakai
counter n_trade hari karantina : Maju 0, Mundur 30 (= 5 hari x 6 jam)
```

Ini **cocok** dengan klaim coder (0 dan 30).

**ESKALASI ARSITEK - OFF-INOPERATIF-2024-2025.** Kriteria (a) dirancang untuk
menangkap "jatuh di Off". Pengukuran Auditor terhadap seluruh store M1
menunjukkan label `Off` **hanya muncul pada 2023** (2.894 bar, semuanya jam
21 UTC, April 2023, celah DST Sydney/NY). Tahun 2024, 2025, dan 2026
memiliki `Off = 0` di **seluruh** bar, bukan hanya di 6 jam terkunci. Artinya
pada data beku yang dikunci spec, kriteria (a) **secara struktural tidak
pernah bisa gagal** - hanya kriteria (b) yang punya daya diskriminasi.

- Ini **bukan** kesalahan coder: `n_Off = 0` yang dilaporkan benar, dan lock
  diterapkan persis sesuai spec.
- Ini **desain lock** yang perlu diketahui arsitek: satu dari dua kriteria
  dalam aturan baca H4b tidak operatif pada data beku. Rekomendasi:
  eskalasi ke arsitek untuk memutuskan apakah (a) perlu revisi (misalnya
  definisi `Off` atau ambang lain) sebelum H4b dipakai untuk generalisasi.
- Tidak mengubah verdict eksekusi, tidak mengubah angka, tidak mengubah
  apa pun yang dihitung ulang.

---

## 5. A4 - Larangan Data 2026 / Tanpa H6 (COCOK)

Grep independen pada `h4b.py` (word-boundary) dan dokumen hasil:

| Token | h4b.py | dokumen coder | Catatan |
|---|---|---|---|
| `rv_regime_flag` | 0 | 0 | tidak dipakai (kolom D4 tidak disentuh) |
| `regime` | 0 | 0 | tidak dipakai |
| `TAU` | 0 | 1 | substring pada kata "ATAU" di prosa, bukan parameter |
| `H6` | 0 | 4 | semuanya prohibitive ("tanpa H6") |
| `2026` | n/a | 5 | path/date + pernyataan "DILARANG" / "tak dipakai" |
| `grid` / `searchsorted` / `calibrat` / `quantile` / `threshold` | 0 | 0 | tidak ada grid, pencarian, atau kalibrasi ambang |

Data 2026 memang **dimuat ke memori** oleh loader, **tetapi nol kontribusi.**
Bukti kausal yang Auditor jalankan sendiri (`a4_atr_kausal.py`):

```
bar M15 tahun 2026 : 18026
bar M1  tahun 2026 : 269846
hari ATR 2024-2025 : 519
n NaN ATR 2024-2025 : 0

acak 100% nilai M1+M15 tahun 2026 -> hitung ulang ATR 2024-2025
  ATR 2024-2025 berubah?  : False   (nilai tetap identik)
kontrol: acak tahun 2025  -> hitung ulang ATR 2025
  ATR 2025 berubah?       : True    (membuktikan harness sensitif)

hapus 2026 dari pool, hitung ulang abs_r_pips 2024-2025 (715308 bar)
  identik tanpa 2026? : True
```

Kesimpulan A4: larangan "data 2026" **dipatuhi secara substantif** - tidak ada
jalur kausal yang membocorkan 2026 ke `abs_r_pips`, ATR, atau EV 2024-2025.
Tanpa H6, tanpa filter regime, tanpa statistik tambahan.

---

## 6. A5 - Cross-Validation ke Batch-2 (SAH)

Pertanyaan: apakah `median/mean EV uji 2025` yang identik digit-per-digit
dengan artefak Batch-2 adalah cross-validasi sah, atau klaim yang
dijadikan bukti secara keliru?

Tiga sumber independen diverifikasi Auditor.

Sumber 1 - ranking ulang M1 per jam (`abs_r_pips` mean per jam):

```
14: 2.255004437361 | 13: 2.250965573419 | 12: 1.954452999481
 0: 1.912916024460 | 15: 1.889440192617 |  7: 1.844345556694

top6 2024 = [14,13,12,0,15,7]  -> SET {0,7,12,13,14,15}
top6 2025 = [14,13,0,15,1,12]  -> SET {0,1,12,13,14,15}
```

Sumber 2 - `hipotesis_lock_v1.md:113` daftar lock P0 `[14,13,0,15,12,7]`.
Sebagai **set** = `{0,7,12,13,14,15}`, identik dengan top6 hitung ulang 2024.

Sumber 3 - JSON Batch-2 `per_tahun 2025` di `sh4_hasil.json`:

```
n              : 1554
median_ev_jpy  : -0.005049999999992838
mean_ev_jpy    : -0.0039283324140465484
persen_positif : 0.49356499356499356
```

Nilai H4b Maju cocok **persis** pada ketiga metrik dengan Batch-2.

Kebenaran secara material: SET jam uji 2025 Maju = SET lock P0 E1 Batch-2.
EV pool hanya bergantung pada **set jam**, bukan urutan - jadi menghitung
ulang EV atas set yang sama **wajib** menghasilkan angka yang sama. Kecocokan
deterministik, bukan bug dan bukan kebetulan.

**Kesimpulan A5: SAH.** Klaim coder (dokumen baris 163-169 dan 217-223)
tentang cross-validation **terdukung bukti**, bukan sekadar jargon.

Catatan float: mean EV bergantung urutan hanya pada digit ke-17 (urutan lock
`...12,7` versus urutan top6 `...0,15,7` menyumbang selisih sekitar
`1.0e-16` JPY lewat penjumlahan floating-point). Ini artefak pembulatan
IEEE-754 normal, **bukan** bug, dan **tidak** mengubah klasifikasi median
maupun verdict. Tidak dinaikkan menjadi temuan.

---

## 7. A6 - Determinisme Artefak (COCOK)

Salinan `repro_h4b.py` dijalankan ulang dari nol oleh Auditor:

```
rc = 0

h4b_maju.json   sha256 : 799c9e0197483fb33e072143fd6f779a1599a1bde41ae89a9dfbbfdc62722d5d
                 blob   : 7975db73490d787132ac60ff5ec0cf3db6fd416c

h4b_mundur.json sha256 : ca40d32655583ccdf61f1d2b83af0df87c297e9831b5f0a7d4258ac3798ee86d
                 blob   : 138d902531866771e0607895e90ec1f8b9c61a8b
```

Byte-identik dengan artefak coder. stdout `h4b_run1.log` identik dengan
`h4b_run2.log` (sha256
`9c7fc168ff026ae7dc322ca3b44318fd304ada88a43225fbeb11e2b4e7635920`,
diff 0 baris).

Toolchain identik antara sesi coder dan replikasi Auditor:

```
Python 3.12.8 | numpy 1.26.4 | pandas 2.2.3 | scipy 1.17.1
tanpa RNG; meta JSON sama
```

Artefak JSON **tidak memuat** string `2026`, `rv_regime`, atau parameter di
luar scope (grep bersih selain label deskriptif `definisi_mesin`).

---

## 8. A7 - Provenance / Integritas Dokumen (COCOK, 1 catatan LOW)

Struktur dokumen coder:

```
14.015 bytes | 259 baris | ASCII | LF-only | berakhir LF
git hash-object : 6410b1800f6dc46ec511949e1311fcda853b0807
```

Provenance (dokumen baris 163-190): sumber angka dipetakan ke artefak beku
plus `sh4_hasil.json`; hash tidak dilampirkan di dalam dokumen (TANPA
self-hash, sesuai spec baris 91) - pengikatan eksternal diterapkan.

Jumlah vonis: **tepat satu**. `GUGUR(H4b)` muncul di baris 154 (vonis utama)
dan diringkas di baris 258 (baris penutup) - keduanya **menyebut vonis
yang sama**, bukan dua vonis berbeda. Tidak ada statistik tambahan yang
diperlakukan sebagai vonis.

Klaim tak berunsur (misalnya klaim pytest atau ruff) **tidak ada** di
dokumen, sehingga tidak perlu diuji.

Staged T6 tetap 2 dan tidak disentuh (lihat S0). Hanya satu file laporan
audit ini yang ditulis ke repo pada ronde ini.

**Catatan LOW-2** (dokumen baris 175-176 dan 231): laporan menyebut
determinisme "run-2 == run-3" (SHA) dan "stdout run-2 == run-1". Di direktori
`%TEMP%\opencode\h4b` terdapat `h4b_run1.log` dan `h4b_run2.log` (2 log),
serta `h4b_maju_run1.json` / `h4b_mundur_run1.json` yang identik dengan
file final. Penamaan run **konsisten** dengan bukti yang ada dan
determinisme terverifikasi ulang oleh Auditor pada A6. Inkonsistensi
penomoran run yang kecil di dalam laporan **bukan kebocoran data atau
manipulasi**; severity LOW, tidak memengaruhi verdict.

---

## 9. Daftar Temuan

Tidak ada temuan MEDIUM/HIGH. Seluruh catatan berseverity **LOW**, dan satu
butir adalah **eskalasi arsitek** (bukan temuan eksekusi coder).

| ID | Severity | Lokasi | Ringkasan |
|---|---|---|---|
| LOW-1 | LOW | `h4b.py:248-250` | Assert "ranking train tetap" memanggil ulang fungsi deterministik pada input identik lalu membandingkan ke dirinya sendiri; guard tidak mungkin gagal, tidak menambah keamanan. |
| LOW-2 | LOW | dokumen coder baris 175-176 dan 231 | Penomoran run tidak persis konsisten dengan berkas yang tersedia; determinisme tetap terbukti ulang oleh auditor. |
| ESK-1 | eskalasi arsitek | kunci (a) H4b, spec baris 21-24 | Kriteria (a) `n_Off` tidak operatif pada data beku 2024-2025 (`Off` hanya ada di 2023). Vonis H4b tidak dirusak; perlu keputusan arsitek apakah kriteria (a) perlu revisi. |

Tidak ada salah hitung, tidak ada kebocoran data, tidak ada manipulasi
determinisme, tidak ada vonis yang merembet ke H4 atau H6, tidak ada klaim
tanpa bukti.

---

## 10. Perintah Reproduksi (independen)

Semua probe Auditor berada di `%TEMP%\opencode\h4b_audit\` (di luar repo):

```
a1_replika.py              : replikasi angka inti tanpa h4b.py
a3_a4_scope.py             : grep scope 2026/H6/regime + definisi Off
a4_scope.py                : hitung label Off di seluruh store per tahun
a4_atr_kausal.py           : uji kausal 2026 + kontrol 2025
a5_crossval.py             : cross-validation set jam 2024/2025 vs P0 & Batch-2
buat_sabotase.py           : buat 2 skrip sabotage gate anti-intip
sabotase_A_bocor_tahun.py  : sabotase filter tahun-train
sabotase_B_jam_bebas.py    : sabotase loop jam 24
repro_h4b.py               : salinan h4b.py untuk uji determinisme
```

Output mentah: `a1_out.txt`, `a3a4_out.txt`, `a4_out.txt`, `a4atr_out.txt`,
`a5_out.txt`, `a6_out.txt` (semua di direktori yang sama).

---

## 11. Self-Audit Auditor

Putaran 1 - Ketelitian:

- (a) Klaim A1-A7 diverifikasi ulang dari sumber (parquet dan kode),
  bukan dari angka coder. Tidak ada output parsial yang dipakai sebagai
  bukti.
- (b) Setiap temuan memiliki file:baris plus output; tidak ada temuan tanpa
  bukti.
- (c) Severity tidak dinaikkan tanpa alasan: LOW-1 dan LOW-2 tetap LOW
  karena tidak ada bukti kebocoran; eskalasi Off dipisah dari temuan
  karena itu masalah desain, bukan eksekusi.

Putaran 2 - Bias:

- (a) Sisi negatif diuji: sabotage A dan B keduanya menggigit, sehingga
  "gate lolos" bukan klaim kosong.
- (b) Angka penentu tidak diasumsikan: median negatif Maju yang menentukan
  `GUGUR` dihitung ulang dari nol, bukan dibaca dari JSON coder.
- (c) Cross-validation diuji skeptis (bisa jadi kebetulan) - diverifikasi
  lewat tiga sumber independen plus pemeriksaan sensitivitas urutan.

Putaran 3 - Meta:

- (a) Tidak ada vonis resmi yang Auditor terbitkan; dokumen ini verdict
  audit saja.
- (b) Staged T6 = 2, tidak disentuh; nol commit; nol push; satu-satunya
  tulis repo adalah file laporan ini.
- (c) Pengikatan eksternal: dokumen TANPA self-hash; sha256 dan
  `git hash-object` dilaporkan di kanal luar setelah penulisan final.

---

=== STOP ===

Re-audit H4b selesai. Verdict audit: **LULUS DENGAN CATATAN** (2 catatan
LOW, 1 eskalasi arsitek, 0 MEDIUM/HIGH). Vonis resmi atas H4b tetap
wewenang arsitek; dokumen ini tidak menggantikan dan tidak mengulang vonis
tersebut.
