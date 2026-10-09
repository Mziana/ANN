# Re-audit Adversarial - Lapisan 3-H3

**Uji**: materialitas `gap_f2_flag` pada klasifikasi H1 (Uji-1) + sensitivitas TAU (Uji-2)
**Auditor**: sesi re-audit adversarial, independen dari Coder
**Tanggal audit**: 2026-10-08
**HEAD saat audit**: `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`
**Spesifikasi**: blob `dacd07087f4e1f66154dcc75a259ecfcdb769043` (13.467 byte)
**Dokumen hasil**: blob penuh `fd52d72242109a74bbb9a9d5425033604b04145a` (44.919 byte)
**Harness** (di luar repo): `C:\Users\Fajar\AppData\Local\Temp\opencode\l3h3`
**Skrip auditor** (di luar repo): `C:\Users\Fajar\AppData\Local\Temp\opencode\l3h3_audit`

---

## Section A. Vonis dan Ringkasan

### A.1 Vonis auditor

> **LULUS DENGAN CATATAN.** Lima temuan (F-1 s.d. F-5). **Tidak satu pun mengubah vonis**
> Uji-1 (`IMMATERIAL`) maupun Uji-2 (`TIDAK STABIL`). Dua temuan (F-1, F-2) **dieskalasikan ke
> Arsitek** karena menyangkut desain dan calibre bukti di spec, bukan eksekusi Coder.

### A.2 Yang diverifikasi

| Komponen | Vonis Coder | Hasil rekomputasi auditor | Status |
|---|---|---|---|
| Uji-1 M1 (primer) | GUGUR / GUGUR, jadi tidak material | identik sampai digit terakhir | TERBUKTI |
| Uji-1 M2 (sekunder) | IMMATERIAL (p=0,629431) | identik; IMMATERIAL **invarian** terhadap 5 nilai B dan 7 seed | TERBUKTI |
| Uji-1 M3 (konsistensi) | bukan anomali | `ratio_path` **bit-exact** dari rekonstruksi sendiri | TERBUKTI |
| Uji-1 hasil | IMMATERIAL | IMMATERIAL | TERBUKTI |
| Uji-2 baseline terkunci | TAU/AUC/n cocok | TAU **bit-exact**; AUC beda 1 ULP (DEV-3 sah) | TERBUKTI |
| Uji-2 A1..A4 | tabel 4 alternatif | **setiap float cocok digit terakhir** | TERBUKTI |
| Uji-2 K1/K2/K3 | TIDAK STABIL | identik; kedua pembacaan agreement sama | TERBUKTI |
| C1..C9 | semua LULUS | C1, C2(substansi), C3, C4, C5, C6, C7, C8, C9 **LULUS** | TERBUKTI |

### A.3 Yang TIDAK dilakukan auditor

Auditor **tidak** memvonis H1/H2/H3/H4/H5, **tidak** menambah alternatif, ambang, atau definisi
baru, **tidak** mengubah ambang lock, dan **tidak** memberi izin kalibrasi ulang. Pernyataan
"H3 GUGUR via S4b" di bagian 4.4 dokumen hasil diperlakukan sebagai **kutipan aturan spec**,
bukan vonis Coder. Coder sendiri juga secara eksplisit menandainya sebagai wewenang Arsitek
(`hasil-lapisan3-H3.md:776-779`). Penegasan itu benar.

---

## Section B. Prasyarat dan Identitas Dokumen

### B.1 Verifikasi blob

| Objek | Klaim | Aktual | Status |
|---|---|---|---|
| Spec blob | `dacd07087f4e1f66154dcc75a259ecfcdb769043` | sama | COCOK |
| C8 (hasil, tanpa baris terakhir) | `c5cb5177eba1b084177e7560953c34875fceee9c` | sama | COCOK |
| Hasil blob penuh | (tidak diklaim) | `fd52d72242109a74bbb9a9d5425033604b04145a` | - |

**Catatan koreksi metodologis.** C8 adalah *git blob*, yaitu `b"blob <len>\0" + isi`, bukan
SHA-1 polos. Percobaan awal auditor memakai SHA-1 polos dan menghasilkan ketidakcocokan yang
**salah**; setelah memakai definisi git-blob, kecocokan penuh (bit-exact). Kesalahan ini dicatat
terbuka agar tidak diulang auditor berikutnya.

### B.2 Dokumen dibaca penuh

Kedua dokumen dibaca utuh sebelum audit (AGENTS.md bagian 20: klaim tanpa baca penuh = temuan).
Kedua skrip harness dibaca utuh baris-per-baris sebelum auditor menyatakan apa pun tentangnya.

---

## Section C. Verifikasi C1 sampai C9

| # | Syarat | Verifikasi auditor | Status |
|---|---|---|---|
| C1 | HEAD tak berubah | `git rev-parse HEAD` = `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` | LULUS |
| C2 | Nol tulis produksi dan lindung | lihat Section F.1 | LULUS (substansi) |
| C3 | Hash D1/D2/D3/D5 + trio beku | 7/7 `git hash-object` + 2/2 `sha256` label | LULUS |
| C4 | Gate hijau | `pytest` **254 passed** rc=0; `ruff check .` rc=0; `ruff format --check .` rc=0 (37 files) | LULUS |
| C4d | Karakter asing | `OK: 1 file discan, tidak ada karakter asing` rc=0 | LULUS |
| C4e | `ruff format --check` pada .md | `.venv` (0.16.10) -> `1 file already formatted` rc=0 | LULUS |
| C5 | Determinisme 2x | lihat Section C.1 | LULUS |
| C6 | Uji-1 selesai dan diputus | eksekusi LULUS **dan** hasil IMMATERIAL, dilaporkan terpisah | LULUS |
| C7 | Uji-2 selesai dan diputus | eksekusi LULUS **dan** hasil TIDAK STABIL | LULUS |
| C8 | Dokumen final + hash | recompute = `c5cb5177eba1b084177e7560953c34875fceee9c` | LULUS |
| C9 | Staged = 0, tanpa commit | lihat Section C.2 | LULUS |

### C.1 C5 - Determinisme dibuktikan ulang

Kedua skrip dijalankan ulang dari sumber yang sama, di luar repo:

```
uji1 rc=0    uji2 rc=0    stderr keduanya 0 byte
uji1_hasil  re-run = 23c29b0f2927d28d940a3ec21339ac80a0ecca160198f34f6bbe13dd42cc26ef
uji2_hasil  re-run = d7927fb92edb836a4173c1fc5077ba885e451632faa6313392f7c2600fea1c62
```

Keduanya identik dengan klaim dokumen dan dengan berkas yang disalin sebelum re-run.

### C.2 C9 - Staged = 0, diperiksa terhadap kemungkinan salah baca

Dokumen memakai `git status --porcelain | grep -c "^[MADRC]"` = 0. Auditor sempat menduga
salah baca, sebab repo nyata berisi 27 baris berstatus `M` atau `D`. Kolomnya diperiksa
eksplisit:

```
baris dengan KOLOM-INDEX (X) != ' '   = 0     <- inilah "staged"
baris dengan KOLOM-WORKTREE (Y) != ' ' = 27    <- pre-ada, BUKAN staged
?? versi collapsed (default)          = 67
?? versi -uall (per berkas)            = 114
Contoh: X=[ ] Y=[M]  .ai/AGENTS.md
        X=[ ] Y=[D]  reports/eda/progress/audit_kesesuaian_nb00_nb04.md
```

Selisih 67 vs 114 bukan inkonsistensi: `--porcelain` menutup direktori untracked menjadi satu
entri, sedangkan `-uall` menghitung tiap berkas. Untuk audit terhadap penambahan berkas baru,
`-uall` adalah angka yang benar (lihat Section H.3).

`^[MADRC]` mencocokkan kolom **index** (X). 27 baris M/D adalah status *worktree* yang pre-ada
dari reorganisasi repo sebelumnya. **Klaim C9 benar**; keraguan awal auditor yang salah, dan
dicatat terbuka.

### C.3 C3 - Hash beku, 9 dari 9 cocok

```
COCOK  src/features/build_labels.py                    2561efd552544feeb9af0b6733711015b83f43dd
COCOK  tests/test_build_labels.py                      dc07a7e651d38f07a5cabbe4e693b10681312d25
COCOK  reports/governance/2026-10-07/coder/protokol    bc17e5de6cfefb355fe7418acd2a3a0d8b461212
COCOK  reports/governance/2026-10-07/coder/laporan     345308540d27c38534b77cdcd278e32eb15735ec
COCOK  src/features/build_features.py                   399e64b372e430b6def79b4fa8324a4e8e629918
COCOK  tests/test_build_features.py                    ed7ac43520c4431519d4d7065504866ae9b3ad95
COCOK  data/features/M15/usdjpy_m15_features.parquet    07402f40478aaed9391203f5db3237d636f5a959
COCOK  data/labels/usdjpy_day_labels.parquet  (sha256) 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c
COCOK  data/labels/usdjpy_h2_trades.parquet   (sha256) 32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f
```

Tiga hash terakhir adalah trio beku yang sudah dipulihkan di re-audit keempat dan tetap utuh.

### C.4 C4e - Kronologi rc=2 lalu rc=0

Dokumen menampilkan dua percobaan `ruff format --check` pada berkas .md: `rc=2`
(`The system cannot find the file specified`) lalu `rc=0` (`1 file already formatted`).
Auditor menguji hipotesis "berbeda interpreter":

```
D:\ANN\venv\Scripts\python.exe   -> ruff 0.6.9   -> rc=2  "Failed to parse ...md:3:1: Expected an expression"
D:\ANN\.venv\Scripts\python.exe  -> ruff 0.16.10 -> rc=0  "1 file already formatted"
```

Jadi `rc=2` adalah (a) versi lama tidak bisa parse `.md`, dan (b) pada percobaan pertama berkas
hasil belum ada. Catatan dokumen `:955` menyebut 0.6.9 secara akurat. **Bukan temuan substantif**;
lihat F-5 untuk perbaikan redaksi.

---

## Section D. Source Review

Berkas: `uji1_materialitas_gap.py` (326 baris), `uji2_sensitivitas_tau.py` (318 baris).

### D.1 uji1_materialitas_gap.py

| Yang diperiksa | Penilaian |
|---|---|
| chi2 kriteria-(ii), tabel tahun x trending | `stats.chi2_contingency(..., correction=False)`; dof 2 benar. Guard `(tab.sum(axis=1)>0).all()` mencegah baris kosong. Auditor menghitung chi2 sendiri dari EXPECTED yang dihitung dari nol: **cocok scipy sampai 1e-12** |
| chi2 M2, tabel 2x3 | dof 2 benar; hitung ulang manual = scipy **bit-cocok** |
| Bootstrap CI95 M1 | percentile hari-level, B=10.000, seed=20261006; resample **terpisah** untuk dua himpunan *disjoin* (trending vs range), benar |
| Bootstrap delta-share M2 | resample **bersama** dari hari yang sama, **benar** untuk desain nested (lihat F-2) |
| Arah tanda `delta_share_trending` | `share_eks - share_ink` dihitung dan di-bootstrap dengan arah sama, **konsisten** |
| M3 median | `ratio_path` diambil dari runtime; D4 memang **tidak** menyimpan kolom turunan ini. Median bertanda sama dengan B1 |
| NaN warmup | `dropna()` pada drift dan span; `ratio_path` 0 NaN |
| FIX-1 (dtype) | cabang bool/object/float ada; lihat **F-1** soal kekuatan instrumen |
| FIX-2 (`nanmax`) | `np.nanmax` dipakai untuk selisih maks, tidak meledak pada all-NaN |
| Logika vonis | ANOMALI dicek lebih dulu, lalu MATERIAL bila M1 atau M2, else IMMATERIAL; `material_m1 = (verdict_ink != verdict_eks)` **persis** spec `:67` |
| Anti-bocor | `YEARS` tetap di luar fungsi; `ink` dan `eks` dibangun dari `built` **sebelum** Baseline, sesuai urutan "dihitung DULU" |

### D.2 uji2_sensitivitas_tau.py

| Yang diperiksa | Penilaian |
|---|---|
| `score_for` | `rolling(w).sum()/w` = mean; divalidasi terhadap `rv_roll_20d/20`: **0 beda**, `nanmax` selisih = **0.0**, `np.array_equal` **True** |
| AUC rank | Mann-Whitney dengan tie rata; audit ulang **pasangan-per-pasangan** (`auc_bruteforce`) identik |
| `auc_trapz` | `np.trapz(tv, fv)` = integral TPR dFPR = AUC; arah benar karena `tv` **naik**. Diuji manual pada kasus separasi sempurna = **1.0**; mereproduksi konstanta lock |
| Youden | kandidat = nilai observasi, `>` untuk B dan `<=` untuk A, ketat. Mereproduksi `TAU_2023` **bit-exact** |
| `flag_of` | NaN **tetap NaN**, tidak dipaksa 0 |
| `agreement` | irisan hari evaluable di kedua sisi; Cohen kappa dihitung manual, identik |
| `gagal_eksekusi_lt_200` | memakai n **primer**; min 230 (A4) di atas 200 |
| `putusan` MARJINAL | tepat satu gagal **dan** tipis; `thin["K3"]=False` keras (lihat Section F.4) |
| Jalur tulis | `OUT = Path(__file__).with_name(...)` menulis hanya ke direktori harness; repo dibaca via `read_parquet`. **READ-ONLY terhadap repo terbukti** |

### D.3 Degenerasi Youden A1 (2024) - bukan bug

A1 (span 2024, W=20) melaporkan `J = 0` dan `TAU_alt = 1,3549e-4`. Auditor memprediksi sebelum
menghitung bahwa pada 2024 urutan stratum lock **terbalik** (B=Jan-Jun ber volatilitas rendah,
A=Jul-Des tinggi), sehingga `J = max(sens+spec-1) = 0` dan kandidat terbaik adalah **nilai
skor maksimum**. Rekomputasi mengonfirmasi persis:

```
tau_sama_max    : true          (tau == max score span)
flag_alt_1_span : 0             (seluruh span)
flag_alt_1_semua: 0
auc             : 0,15586721107757856   (= 1 - 0,8441327889224215)
median_b < median_a : true
```

Artinya `flag_alt` bernilai 0 sepanjang seri, sehingga **agreement A1 sebesar 0,3154 adalah
konsekuensi deterministik dari ambang yang degenerat**, bukan bukti diskriminasi yang hilang.
Dokumen hasil sudah menyebut ini dan kebenarannya terverifikasi. Tidak ditemukan logika salah.

---

## Section E. Rekomputasi Independen

Auditor menulis ulang seluruh statistik dari nol (chi2, bootstrap, Youden, AUC, agreement,
kappa, logika vonis) dan **tidak mengimpor** apa pun dari skrip Coder; hanya fungsi produksi
repo sebagai sumber data.

### E.1 M1 - cocok penuh

| Varian | INK p (chi2) | EKS p | verdict INK | verdict EKS |
|---|---|---|---|---|
| primer (`london_drift_norm` vs range) | 0,6816069745648556 | 0,9147241915659032 | GUGUR | GUGUR |
| R1 (`london_drift_4h`) | - | - | GUGUR | GUGUR |
| R2 (vs normal+range) | - | - | GUGUR | GUGUR |
| R3 (chi2 mengikutsertakan 2026) | 0,776530117500301 | 0,9514310311116166 | GUGUR | GUGUR |

CI95 memuat 0 pada **seluruh** varian. Contoh primer INK:
`[-0,02729045556350576 ; +0,052787080233690914]`. `material_m1 = false`. Semua robustness tidak
memisahkan INK dari EKS.

### E.2 M2 - cocok penuh, dan vonis ternyata tahan banting

```
chi2 = 0,9258779541662121   dof = 2   p = 0,629431041054359   (manual == scipy, bit-cocok)
tabel 2x3  INK = [330, 320, 324]   EKS = [265, 243, 232]
delta-share trending EKS-INK = +0,019299073200510553
bootstrap PAIRED   CI95 = [+0,0030084639086084292 ; +0,03523449994702561]  -> TIDAK memuat 0
bootstrap PAIRED   CI99                                          -> MEMUAT 0
bootstrap UNPAIRED CI95 = [-0,026050280259725833 ; +0,06464974471391308] -> memuat 0
two-proportion z (unpaired) p = 0,4057978029535061
```

Karena spec memutuskan pada **p < 0,01**, yang relevan adalah **CI99**, dan CI99 memuat 0.
Diuji pada 5 nilai B dan 7 seed:

| B | CI95 memuat 0? | CI99 memuat 0? |
|---|---|---|
| 1.000 | tidak | ya |
| 2.000 | tidak | ya |
| 5.000 | tidak | ya |
| 10.000 | tidak | ya |
| 50.000 | tidak | ya |

Tujuh seed (1, 7, 42, 101, 999, 2024, 31337): paired **7 dari 7** tidak memuat 0 pada 95%;
unpaired **7 dari 7** memuat 0. M1 `GUGUR` stabil pada seluruh nilai B.

> **Kesimpulan eksplisit.** Dugaan awal auditor bahwa CI95 paired yang tidak memuat 0 akan
> membalik vonis M2 **terbukti salah**. Pada alpha = 0,01 yang ditetapkan spec, `IMMATERIAL`
> **invarian** terhadap estimator (paired vs unpaired), jumlah B (1.000 sampai 50.000), dan
> seed. Lihat **F-2**: temuan tersisa bersifat metodologis, bukan pembalik vonis.

### E.3 M3 - `ratio_path` dihitung ulang dari nol, bit-exact

Auditor membangun ulang frame harian sendiri dari parquet M1 dan M15, tanpa memakai
`daily_metrics`:

```
bandingkan_ratio_path : n_common=974  bit_exact=true  max_abs_diff=0.0  nan_pola_sama=true
median_gap    = 0,025133520587895034
median_nongap = 0,027809705068563857
selisih       = -0,0026761844806688223     tanda sama dengan B1, jadi bukan ANOMALI
```

Angka ini cocok digit terakhir dengan laporan Coder, dan median dari rekonstruksi sendiri
identik dengan median dari `daily_metrics`.

### E.4 Uji-2 - bit-identik dengan JSON Coder

| | A1 (2024,W20) | A2 (2025,W20) | A3 (2023,W10) | A4 (2023,W30) |
|---|---|---|---|---|
| TAU_alt | 1,3548874602906333e-04 | 3,5844222823113623e-05 | 2,5041018330339243e-05 | 2,8106701591701573e-05 |
| AUC | 0,15586721107757856 | 0,957418893129771 | 0,7886475751169197 | 0,8393583544400952 |
| J | 0,0 | 0,8361164122137406 | 0,5963866999807803 | 0,5736434108527133 |
| n_b / n_a | 129 / 131 | 128 / 131 | 121 / 129 | 101 / 129 |
| nan_span | 0 | 0 | 9 | 29 |
| agreement primer | 0,3153846153846154 | 0,6718146718146718 | 0,9125 | 0,9304347826086956 |
| kappa primer | 0,0 | 0,39159872875500906 | 0,8012304779933743 | 0,8428425008541167 |
| K3 (median B di atas A) | false | true | true | true |

Baseline terkunci: `TAU_2023 = 2,5951672079821496e-05` **bit-cocok** dengan konstanta lock;
`n_b=111`, `n_a=129`, `nan_span(2023)=19`, `flag_ref` **bit-exact** terhadap D4 (0 beda).

Putusan: `K1 GAGAL`, `K2 GAGAL` pada pembacaan primer **dan** robust, `K3 GAGAL`, maka
**`TIDAK STABIL`**. `kedua_pembacaan_sama = true`, `ada_gagal_eksekusi_lt200 = false`.
Seluruh nilai di atas identik dengan `uji2_hasil.json` milik Coder.

---

## Section F. Asumsi (A) dan Deviasi (DEV)

### F.1 DEV-1 / C2 - PUTUSAN EKSPLISIT AUDITOR

Dokumen sendiri menyatakan pola C2 gagal secara literal: output perintah C2 **tidak kosong**
karena `src/features/build_labels.py` dan `tests/test_build_labels.py` berstatus `??`
(untracked, sejalan larangan commit), dan 14 `reports/eda/progress/*.md` sudah berstatus ` D`
**sebelum** tugas. Auditor menilai **substansi**, bukan polanya:

| Unggahan bukti DEV-1 | Verifikasi auditor | Hasil |
|---|---|---|
| Output C2 sebelum sama dengan sesudah | tidak dapat diulang (tidak ada snapshot before) | - |
| `git diff HEAD` berkas lindung hanya penghapusan pre-ada | kolom index bersih; 27 baris semuanya kolom worktree | TERBUKTI |
| `find ... -newermt "2026-10-08 22:00"` kosong | tidak ada berkas di src/tests/data/configs yang lebih baru dari 22:00; mtime terakhir `tests/test_build_labels.py` = 18:30:12, **persis** sama dengan `stat` di `hasil:903` | TERBUKTI |
| Hash isi D1/D2 + trio beku tak berubah | 9 dari 9 hash identik (Section C.3) | TERBUKTI |
| Harness tak menulis ke repo | `OUT = Path(__file__).with_name(...)`; repo dibaca via `read_parquet` | TERBUKTI |

> ### PUTUSAN C2 (wajib, karena DEV-1 elisip auditor)
>
> **C2 = LULUS (substansi) / GAGAL (pola literal).**
>
> - **Substansi LULUS.** Nol tulis produksi dan nol sentuh lindung terbukti dari empat jalur
>   independen: mtime, hash isi, status kolom index, dan jejak `OUT` di kode harness.
> - **Pola literal GAGAL.** Pola "kedua output kosong" memang tidak terpenuhi. Coder sendiri
>   yang pertama kali melaporkan ini dan **eskalasi ke Arsitek** (`hasil:816-817`). Coder tidak
>   menutupi, tidak memalsukan, dan tidak mengklaim pola lolos.
> - **Tanggung jawab.** Kegagalan pola ada pada **desain perintah C2 di spec**, bukan pada
>   Coder. Perbaikan (batasi berkas tracked, atau bandingkan before/after) adalah wewenang
>   Arsitek.

### F.2 DEV-2 - subset 223-counterfactual

Diverifikasi terhadap spec: `:47` "**Populasi terkunci:** 234 hari-broker ber-flag"; `:49`
"primer pada 234 penuh; subset 223-counterfactual hanya sebagai cek". Jadi Coder **benar** bahwa
223 non-penentu. Identitas 11 hari pembeda memang tidak disediakan spec.

**Penilaian**: tidak dapat dihitung tanpa mengarang definisi; keputusan Coder untuk tidak
mengarang sudah benar. Status **tetap BELUM DIVERIFIKASI** dan **tidak boleh** dianggap lolos.
Bukan temuan terhadap Coder; dicatat sebagai gap input yang harus ditutup Arsitek.

### F.3 DEV-3 - selisih 1 ULP pada AUC

Diverifikasi: `np.nextafter(0.8173755150499336, 1.0) == 0.8173755150499337`, jadi **benar 1 ULP**;
selisih `1,1102230246251565e-16`. Metode trapesium atas data yang sama mereproduksi konstanta
lock **bit-identik**, sehingga murni artefak penjumlahan float. Penilaian **INFO, bukan temuan**;
tidak memengaruhi K1 (ambang 0,70). Klasifikasi Coder benar.

### F.4 A-6 - celah MARJINAL K3-gagal-tunggal

`putusan` memakai `thin["K3"] = False` secara keras: K3 gagal tunggal tidak pernah bisa diberi
label MARJINAL. Tidak terpicu di sini (tiga kriteria gagal). Coder melaporkannya sebagai celah
(`hasil` bagian 7 butir 5). Benar dan jujur. Tidak ditemukan kegagalan penahoraan.

### F.5 A-2 - konvensi seed

Klaim "seed=20261006, konvensi lock H5" **terverifikasi**:
`reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md:145`
"kuartil-atas ATR hari & sesi; CI bootstrap day-cluster seed 20261006". Bootstrapping Coder
memang day-level ("day-cluster").

---

## Section G. Temuan Bernomor

### F-1 - Instrumen pembuktian S0 lebih lemah dari klaimnya (MEDIUM, eskalasi Arsitek)

**Lokasi**: `uji1_materialitas_gap.py:158-164`
**Klaim dokumen**: `hasil` bagian 3.1 [O6] - mismatch per kolom = 0, direproduksi tanpa satu pun
sel berbeda dari artefak D4 beku.
**Masalah**: pembanding numerik memakai `np.isclose(..., equal_nan=True)` dengan tolerance
default (`rtol=1e-5`, `atol=1e-8`). Selisih relatif sampai `1e-5` tidak akan terdeteksi. Jadi
"0 mismatch" yang dibuktikan instrumen itu tidak menyiratkan reproduksi bit-exact, padahal itu
justru yang dituntut oleh konsep artefak **beku**.
**Dampak**: tidak ada. Klaimnya **benar** - auditor membuktikannya dengan instrumen yang tepat:
`np.array_equal` menunjukkan bit_exact untuk keempat kolom float, `max_abs_diff = 0.0` pada
`london_drift_4h`, `london_drift_norm`, `gap_f2_flag`, `rv_regime_flag`, dengan nan pattern
identik.
**Saran**: pakai `pd.testing.assert_series_equal(..., check_exact=True)` atau `np.array_equal`,
atau sebutkan tolerance secara eksplisit di dokumen.

### F-2 - chi2 M2 melanggar asumsi independensi; kontras CI vs p tidak ditutup pada alpha spec (MEDIUM, eskalasi Arsitek)

**Lokasi**: spec `:73` dan `uji1_materialitas_gap.py:244`
**Isu**: spec menetapkan dua level yang tidak konsisten dalam satu kalimat - "**MATERIAL bila
p < 0,01.** delta-share_trending + **CI95** bootstrap WAJIB". Keputusan pada 1 persen (berarti
CI99), laporan efek pada 95 persen (berarti CI95).
Uji chi2 pada tabel 2x3 memperlakukan `EKS` sebagai subset `INK` (nested, 740 dari 974 hari)
sebagai sampel **independen**. Asumsi independensi dilanggar; uji ini konservatif.
Efeknya terlihat: CI95 paired `+0,003008 ; +0,035234` tidak memuat 0, yang oleh pembacaan naif
akan dibaca sebagai "bukan homogen" - apparent kontradiksi dengan `p=0,629431`.
**Yang menutupi**: pada **alpha spec 0,01** kontradiksi itu **menghilang**. CI99 paired memuat 0
pada 5 dari 5 nilai B dan 7 dari 7 seed; CI95 unpaired memuat 0 pada 7 dari 7 seed;
two-proportion z `p=0,406`. `IMMATERIAL` invarian.
**Dampak**: tidak ada pada vonis. Yang tersisa adalah kekurangan disclosure.
**Saran**: (a) laporkan CI99 berdampingan dengan CI95 supaya apparent kontradiksi tertutup;
(b) pada pengulangan, ganti chi2 M2 dengan estimator paired yang valid untuk desain nested, atau
nyatakan eksplisit bahwa homogenitas diuji pada sampel bersarang.

### F-3 - Dua konvensi bootstrap berbeda dipakai tanpa diberi nama (LOW)

**Lokasi**: `uji1_materialitas_gap.py:71-78` (M1) versus `:250-257` (M2)
M1 me-resample dua himpunan **disjoin** secara terpisah; M2 me-resample **bersama** dari kumpulan
hari yang sama. **Keduanya benar** untuk desainnya masing-masing. Namun keduanya dilaporkan di
bawah satu label "bootstrap" dan dokumen tidak menyebut bahwa estimator-nya berbeda. Pembaca
bisa salah mengira satu konvensi berlaku seragam.
**Dampak**: tidak ada pada angka. **Saran**: beri label eksplisit "unpaired (disjoint)" dan
"paired (nested)".

### F-4 - B=10000 tidak terkunci di mana pun (LOW)

**Lokasi**: `uji1_materialitas_gap.py:40` dan docstring `:11-12`
Lock `:145` hanya menyebut **seed**; `B` tidak ada di lock maupun spec. Paragraf docstring
mengaitkan hanya seed ke "lock H5", jadi tidak ada klaim palsu, tetapi B adalah parameter bebas
yang tidak dideklarasikan sebagai pilihan pelaksana.
**Dampak**: tidak ada - vonis stabil pada B = 1.000, 2.000, 5.000, 10.000, 50.000 (Section E.2).
**Saran**: nyatakan B sebagai **deklarasi pelaksana** yang terisolasi, bukan konvensi lock.

### F-5 - Blok rc=2 pada C4e tanpa label kronologi (LOW, redaksi)

**Lokasi**: `hasil:932-936` versus `:952-954`
Dua percobaan `ruff format --check` pada berkas .md ditampilkan berurutan tanpa catatan bahwa
yang pertama terjadi **sebelum berkas ada** dan memakai ruff 0.6.9 yang tidak bisa parse `.md`.
Pembaca yang tidak tahu akan mengira ada hasil yang bertentangan.
**Dampak**: tidak ada. Auditor mengonfirmasi `.venv` (0.16.10) -> rc=0 "1 file already formatted",
persis seperti klaim, dan `venv` (0.6.9) -> rc=2 "Expected an expression", jadi catatan yang
sudah ada di `:955` akurat.
**Saran**: tambahkan label "sebelum berkas ditulis / versi 0.6.9" pada blok pertama.

---

## Section H. Batasan dan Self-Audit 3x

### H.1 Batasan auditor

1. **Tidak** menghitung ulang cek robustness subset-223 (identitas 11 hari tidak ada di spec);
   status tetap **BELUM DIVERIFIKASI**.
2. **Tidak** memvonis H1/H2/H3/H4/H5; "H3 GUGUR via S4b" tetap kutipan aturan spec.
3. **Tidak** menyetujui kalibrasi ulang (Q1(a) tetap); tidak mengubah ambang lock maupun K1-K3.
4. **Tidak** menguji sensitivitas di luar A-1..A-6 dan F-1..F-5.
5. **Tidak** menjalankan ulang harness terhadap HEAD berbeda; audit pada `e0b2b9f` sesuai
   dokumen.
6. DEV-1 "output sebelum sama dengan sesudah" tidak dapat direproduksi ulang (tidak ada
   snapshot before); diganti bukti substitusi yang lebih kuat: mtime, hash isi, status, dan
   jejak `OUT`.
7. Angka diambil dari JSON yang diverifikasi ulang serta dari disk, bukan dari tabel markdown
   dokumen, agar tidak kehilangan presisi.

### H.2 Self-audit 3x

**Putaran 1 - Correctness.** Seluruh statistik ditulis ulang tanpa melihat keluaran Coder lebih
dulu, lalu diverifikasi ulang. Dugaan "M2 flipped" dari Putaran 0 **diuji dan dibuang**
(Section E.2). `ratio_path` dihitung dari nol, bukan dari `daily_metrics`. Tidak ditemukan
kesalahan eksekusi Coder.

**Putaran 2 - Bias.** Dua godaan diperiksa. (a) Godaan mencari bug agar terlihat tajam: degenerasi
Youden A1 **diterangkan sebagai sifat data yang benar**, bukan dipaksakan jadi bug. (b) Godaan
membenarkan C2 karena Coder sudah mengetahuinya: **pola literal tetap dinyatakan GAGAL**. Kedua
pembacaan agreement (primer dan robust) dihitung, bukan hanya yang gagal. S4b **tidak**
dieksekusi sebagai vonis.

**Putaran 3 - Meta.** Tabel hasil di dokumen diperiksa ulang terhadap JSON dan disk (Section C
dan E). C9 diperiksa ulang karena curiga salah baca kolom porcelain - **keraguan saya sendiri
yang salah**, dan itu dicatat terbuka (Section C.2). C4e diperiksa ulang karena muncul dua rc
berbeda - ternyata dijelaskan oleh versi interpreter, bukan konflik (Section C.4). Kesimpulan:
**LULUS DENGAN CATATAN**, F-1 dan F-2 ke Arsitek, tanpa perubahan vonis Uji-1 maupun Uji-2.

### H.3 Bukti read-only auditor

```
HEAD                                          : e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169 (tak berubah)
staged (kolom index)                          : 0
9 dari 9 hash beku                            : identik
berkas di src/tests/data/configs lebih dari 22:00 : tidak ada
skrip auditor                                 : hanya di %TEMP%\opencode\l3h3_audit
pycache dan berkas produksi/lindung          : tidak disentuh
berkas entropy tinggi / parquet / lock / spec: tidak disentuh
```

**Pernyataan cakupan yang tepat.** Auditor menulis **satu** berkas ke dalam pohon repo, yaitu
laporan ini: `reports/governance/2026-10-07/Audit/reaudit-lapisan3-H3.md`. Berkas itu **baru dan
untracked** (`git status --porcelain=v1 -uall` = `?? reports/governance/2026-10-07/Audit/reaudit-lapisan3-H3.md`;
`git ls-files` tidak mengenali; `git check-ignore` tidak mengabaikannya). Tambahan ini tertutup
kebetulan oleh keadaan: direktori `Audit/` sudah untracked sebelum tugas, sehingga hitungan `??`
versi *collapsed* tetap 67 dan perubahan ini akan tersembunyi bila status diperiksa tanpa
flag `-uall`.

Di luar laporan ini, **tidak ada** berkas repo yang ditulis atau dimodifikasi: tidak ada
`git add`, tidak ada `git commit`, tidak ada stash, tidak ada checkout. Klaim lama "tidak ada
berkas repo yang ditulis" **tidak** diklaim; yang diklaim adalah nol sentuh pada produksi,
lindung, dan artefak beku - dibuktikan oleh status kolom index, mtime, 9 dari 9 hash, dan
`HEAD` yang tetap.

---

## Section I. Ringkasan Putusan

| Item | Vonis |
|---|---|
| Uji-1 `IMMATERIAL` | **TERBUKTI** (M1 tidak material, M2 tidak material; robust terhadap B dan seed) |
| Uji-2 `TIDAK STABIL` | **TERBUKTI** (K1, K2, K3 gagal; kedua pembacaan agreement sama) |
| C1 sampai C9 | **LULUS** (C2 substansi LULUS, pola literal GAGAL) |
| A-2 (seed lock) | **TERVERIFIKASI** |
| A-6 (celah K3 MARJINAL) | **DILAPORKAN BENAR**, tidak terpicu |
| DEV-1 (C2) | **PUTUSAN: LULUS substansi / GAGAL pola literal**, eskalasi Arsitek |
| DEV-2 (subset-223) | **BELUM DIVERIFIKASI** - tidak dapat dihitung tanpa definisi 11 hari |
| DEV-3 (1 ULP AUC) | **INFO** - 1 ULP dikonfirmasi |
| DEV-4 (jalur C3/C4) | **INFO** - tidak ada perbedaan objek yang diperiksa |

**Temuan**: F-1 (MEDIUM), F-2 (MEDIUM), F-3 (LOW), F-4 (LOW), F-5 (LOW).
**Eskalasi ke Arsitek**: F-1, F-2, dan perbaikan pola C2 (DEV-1).
**Perubahan vonis oleh auditor**: tidak ada.

---

## Lampiran A - Skrip Verifikasi (di luar repo, read-only terhadap D:\ANN)

```
%TEMP%\opencode\l3h3_audit\
  rekomputasi_independen.py   rekomputasi_hasil.json
  m3_crosscheck.py            m3_crosscheck.json
  b_sensitivity.py            b_sensitivity.json
  final_check.py
  uji1_hasil.CODER.json       uji2_hasil.CODER.json
  rerun1.log/err  rerun2.log/err  rekom.log/err  bsens.log/err  m3cc.log/err
  pytest.log/err  ruffcheck.log/err  rufffmt.err  ruff fmt.log  ruffmd.log/err
  ruffmd2.log/err  rf3.log/err  rf4.log/err  fc.log/err .. fc4.log/err
  collect.log/err
```

## Lampiran B - SHA-256 Berkas Angka (terverifikasi ulang)

```
uji1_hasil.json  23c29b0f2927d28d940a3ec21339ac80a0ecca160198f34f6bbe13dd42cc26ef
uji2_hasil.json  d7927fb92edb836a4173c1fc5077ba885e451632faa6313392f7c2600fea1c62
```
