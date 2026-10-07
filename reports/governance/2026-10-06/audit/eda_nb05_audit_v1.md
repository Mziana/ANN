# Laporan Audit nb05

> Status dokumen: **DRAF** - memuat Langkah 1 (putaran 1 + re-audit putaran 2).
> Langkah 2-10 menunggu perintah eksplisit per langkah. Auditor: Space Bunny
> (pengganti). Tanggal: 2026-10-06.
>
> Semua angka di dokumen ini dibaca langsung dari output notebook di disk
> (`notebooks/scalping/eda_05_regimes.ipynb`, `eda_03_autocorr.ipynb`,
> `eda_04_swings_levels.ipynb`) dan dari `scripts/_build_eda05.py` pada disk.
> Nomor sel memakai indeks **0-based** sesuai urutan di `cells[]` notebook.
>
> **Riwayat revisi dokumen ini**
>
> | Putaran | Builder blob | Notebook blob | Verdict |
> |---|---|---|---|
> | 1 (audit awal) | `cc73f7943077` | `1155e6de3de6` | PERLU PERBAIKAN |
> | 2 (re-audit perbaikan) | `8ac848ce2f7d` | `93ea76955742` | **LULUS (Langkah 1)** |

---

## Ringkasan

- **File audited**: `scripts/_build_eda05.py`, `notebooks/scalping/eda_05_regimes.ipynb`,
  `reports/eda/2026-10-06/report.md`, `reports/eda/2026-10-06/figures/FIG-04..07.png`,
  `reports/eda/progress/06-regimes/laporan_tahap_11..14`.
- **Cakupan putaran ini**: RE-AUDIT LANGKAH 1 terhadap perbaikan coder -
  verifikasi ulang 4 temuan (HIGH-01, HIGH-02, MEDIUM-01, MEDIUM-02) satu per
  satu dari disk, dan verifikasi 6 jawaban pertanyaan auditor.
- **Jumlah temuan**: 7 di putaran 1 -> **0 terbuka** di putaran 2
  (2 HIGH ditutup, 2 MEDIUM ditutup, 3 LOW tetap tertutup).
- **Verdict LANGKAH 1: LULUS.**
  Keempat temuan HIGH/MEDIUM **tertutup dengan bukti `file:baris` dan output sel**,
  bukan dengan penjelasan naratif. Keempat angka replika kini **cocok digit
  terakhir dengan nb03/nb04** (ACF 0,001793; VR 1,0312; sign-ACF -0,022624;
  swing 40.483). Methodologi VR dan definisi no-gap **disamakan secara
  struktural** dengan nb03 (fungsi verbatim + kolom `gap_return`), bukan hanya
  dikoreksi labelnya. Assertion fidelitas berubah dari band lebar menjadi kunci
  ketat dengan toleransi eksplisit.
  Catatan: verdict ini **hanya untuk Langkah 1**. Langkah 2-10 belum diaudit.

### Bukti pembuka re-audit (blok baru yang diverifikasi ulang)

| Objek | Blob git (disk) | Bytes |
|---|---|---|
| `scripts/_build_eda05.py` | `8ac848ce2f7d1b70e78074963730b451663cf6af` | 42.763 |
| `notebooks/scalping/eda_05_regimes.ipynb` | `93ea76955742028f6505c7b5d1a9434362ffad12` | 68.980 |
| `reports/eda/2026-10-06/report.md` | `72e837778dfc0ecf8966a6c9f84344843b548fc0` | 10.067 |
| `laporan_tahap_11_regime.md` | `6ab21459e91e198bc038beae3aa1ac3ae35b3afe` | 6.030 |
| `laporan_tahap_12_sintesis.md` | `eae21308c04dcca31387e5a350a24d323d4a0d2c` | 5.638 |
| `laporan_tahap_13_report.md` | `ad6652b7a0aa87ad8d96e0b453316c513cc7d1e8` | 3.035 (tak berubah) |
| `laporan_tahap_14_figures.md` | `85b958d133db6854de0fae52ee2fed10fc42847b` | 2.303 (tak berubah) |

Struktur notebook (dihitung ulang dari `cells[]`, bukan dari klaim):
25 sel / 18 sel kode / **0 output bertipe `error`** / `execution_count`
`[1..18]` monoton naik (bukti urutan eksekusi top-to-bottom) /
**59 baris assertion**.

### Catatan koreksi terhadap draf sebelumnya

Draf `eda_nb05_audit_v1.md` versi sebelum audit ini memuat klaim yang **tidak
benar dan harus dicabut**:

1. Draf baris 22 mengklaim ada `assert abs(mean_vr - 1.0337) < 0.05`. **Assert
   itu tidak ada di `_build_eda05.py`.** Assert VR yang sebenarnya adalah
   `assert 0.9 < mean_vr < 1.2` (`_build_eda05.py:446`).
2. Draf membandingkan 49,07 swing/hari dengan `mean 48,74` dan `median 49,00`
   nb04 - keduanya adalah statistik **kombinasi k=3+k=5**, bukan k=3 saja.
3. Draf memakai label "EXACT MATCH" pada baris yang sama dengan "selisih 0,33
   (0,7%)" - kontradiktif sendiri dan memakai kata yang dilarang.
4. Draf baris 29 memakai bukti samar `baris ~t15`.

---

## Langkah 1 - Replica Fidelity

### 1.1 Tabel hasil (angka dihitung ulang oleh auditor dari output disk)

| # | Metrik | nb05 (output) | Referensi nb03/nb04 (output) | Selisih | Relatif |
|---|--------|---------------|------------------------------|---------|---------|
| 1 | ACF lag-1 M15-A | **0.001789** | nb03 `acf_all` = **0.001793** | 0.000004 | 0,22 % |
| 2 | Sign-ACF lag-1 M15-A (no-gap) | **-0.022005** | nb03 SIGN_ACF_TABLE A/M15 = **-0.022624** | 0.000619 | 2,74 % |
| 3 | Rata-rata VR horizon (5,15,60) M15-A | **1.0277** | nb03 tabel horizon M15: 1.0160 / 1.0119 / 1.0657, rata-rata **1.0312** | 0.0035 | 0,34 % |
| 3b | idem, terhadap angka yang dicetak nb05 | 1.0277 | **1.0337** = rata-rata VR **lag 2-60** nb03, bukan horizon 5/15/60 | - | - |
| 4 | Swing M5 k=3 high+low (A) | **40.483** menjadi 49,07/hari | nb04 `high_k3` 20.169 + `low_k3` 20.314 = **40.483**; 24.447+24.623 = **49,070**/hari | **0** | **0 %** |

Sumber angka:

- nb05 sel 9 (0-based) output: `ACF lag-1 = 0.001789` - `VR(5)=1.0111,
  VR(15)=1.0096, VR(60)=1.0624` - `rata-rata VR(5,15,60) = 1.0277` -
  `sign-ACF lag-1 M15 (A, no-gap) = -0.022005`.
- nb05 sel 11 (0-based) output: `swing M5 k=3 high+low (A) = 40,483 -> 49.07 swing/hari`.
- nb03 sel ACF M15 (stratum A): tabel `=== ACF M15 (stratum A, lag 1-60) ===`,
  baris `lag 1`: `acf_all 0.001793`, `acf_no_gap 0.003496`, `p_value_no_gap
  0.338177`, `n_no_gap 75038`.
- nb03 sel sign-ACF: `=== Sign-ACF lag 1 (no-gap) ===` - `M15  A -0.022624`.
- nb03 sel VR: `--- VR pada horizon kontrak (5, 15, 60) (stratum A) ---`,
  kolom M15: lag 5 = `1.0160`, lag 15 = `1.0119`, lag 60 = `1.0657`;
  baris ringkasan `A M15: rata-rata VR(lag 2-60) = 1.0337`.
- nb04 sel Q5/D6: `=== D6: frekuensi swing per HARI (stratum A) ===`
  - `high_k3 20169 / 24.447`, `low_k3 20314 / 24.623`,
    `gabungan 40207 / 48.736`; sebaran gabungan per hari `mean 48.74`,
    `50% 49.00`.

### 1.2 Verifikasi aritmetika yang saya hitung ulang sendiri

- `20169 + 20314 = 40483` - cocok bulat dengan `swings` nb05.
- `40483 / 825 = 49,0709` - tercetak `49.07` (`_build_eda05.py:540-541`).
- `20169/825 = 24,4473` menjadi `24.447`; `20314/825 = 24,6230` menjadi `24.623`;
  `24.447 + 24.623 = 49,070` - cocok sampai 3 desimal dengan nb05.
- `(1.0160 + 1.0119 + 1.0657) / 3 = 1,0312` - inilah referensi VR yang
  apples-to-apples terhadap `mean_vr` nb05.
- `0.001793 - 0.001789 = 0,000004`; `0.022624 - 0.022005 = 0,000619`.

---

## Temuan

### [HIGH-01] Referensi VR yang dicetak di nb05 menunjuk statistik yang berbeda

- **Lokasi**: `scripts/_build_eda05.py:444` (dan output sel 9 nb05).
- **Masalah**: `_build_eda05.py:444` mencetak
  `f"rata-rata VR(5,15,60) = {mean_vr:.4f} (referensi nb03: 1,0337)"`.
  Angka `1,0337` di nb03 adalah **rata-rata VR pada lag 2-60** (59 titik),
  bukan rata-rata VR pada tiga horizon kontrak (5, 15, 60).
- **Bukti**:
  - nb03 sel VR, baris ringkasan: `A M15: rata-rata VR(lag 2-60) = 1.0337 | (lag 2-20 = 1.0127)`.
  - nb03 sel VR, tabel horizon: `lag 5 -> 1.0160`, `lag 15 -> 1.0119`,
    `lag 60 -> 1.0657`; rata-rata = `1,0312`.
  - Satu-satunya angka yang cocok dengan label "rata-rata VR(5,15,60)" adalah
    `1.0312`, bukan `1.0337`.
- **Dampak**: ini **bukan** perbedaan perhitungan - `1.0277` yang dihitung nb05
  memang rata-rata atas VR(5), VR(15), VR(60). Yang salah adalah **rujukan
  pembandingnya**, sehingga pembaca menyimpulkan selisih 0,6% padahal selisih
  terhadap basis yang sama adalah 0,34%. Angka `1.0277` vs `1.0337` (0,58%)
  **tidak boleh dipakai sebagai bukti fidelity apa pun**.
- **Saran**: ganti string referensi menjadi `1,0312` (rata-rata atas horizon
  5/15/60) dan tambahkan baris kedua yang menyebut `1.0337` sebagai rata-rata
  lag 2-60 dari nb03, supaya dua statistik tidak tertukar lagi. Assertion
  (lihat MEDIUM-02) harus diarahkan ke `1.0312`.

### [HIGH-02] Metode hitung VR nb05 berbeda dari nb03 - replika tidak pernah bisa identik

- **Lokasi**: `scripts/_build_eda05.py:438-440` (dan sel 9 nb05).
- **Masalah**: nb05 menghitung VR sebagai
  `rolling(k).sum().dropna().var(ddof=0) / (k * r15.var(ddof=0))` atas seri
  `r15` **penuh** (tanpa membuang gap). nb03 menghitung
  `np.var(lag_sum, ddof=1) / (lag * var1)` atas seri **no-gap**
  (`subset.loc[~subset["gap_return"], "r"]`).
- **Bukti**:
  - `scripts/_build_eda05.py:435` `r15 = m15_a["r"].dropna()`;
    `_build_eda05.py:439-440` `rolling_sum = r15.rolling(k).sum().dropna()` /
    `vr[k] = float(rolling_sum.var(ddof=0) / (k * r15.var(ddof=0)))`.
  - nb03 sel VR, fungsi `variance_ratio`: `var1 = float(np.var(values, ddof=1))`,
    `var_lag = float(np.var(lag_sum, ddof=1))`; pemanggil:
    `clean = subset.loc[~subset["gap_return"], "r"]`.
  - Dua perbedaan independen: (a) `ddof=0` vs `ddof=1`;
    (b) menyertakan bar gap vs no-gap.
- **Dampak**: nilai `1.0277` **secara konstruksi tidak boleh** dibandingkan
  dengan nilai nb03 sebagai replika identik. Selisih 0,34% yang terukur adalah
  gabungan efek sampling, bukan bukti fidelity. Metode ini **tidak disclosed**
  di docstring sel maupun di output - pembaca yang melihat kata "replica nb03"
  pada `_build_eda05.py:422, 443, 444` akan menyimpulkan replika dengan cara
  yang identik.
- **Saran**: pilih satu dan nyatakan eksplisit. Rekomendasi konservatif:
  samakan `variance_ratio` nb05 dengan nb03 (fungsi yang sama, `ddof=1`,
  no-gap), lalu assertion `1.025 < mean_vr < 1.038` dengan referensi `1.0312`.
  Jika tetap memakai versi `ddof=0` penuh, ubah label output dari
  `"replica nb03"` menjadi `"indikator VR (metode nb05, bukan nb03)"`.

### [MEDIUM-01] Replika sign-ACF memakai definisi adjacency berbeda dan meleset 2,74 %

- **Lokasi**: `scripts/_build_eda05.py:448-453`.
- **Masalah**: nb05 menentukan pasangan no-gap lewat selisih waktu
  `np.diff(t15) == np.timedelta64(900, "s")` di atas pemetaan `broker_day`
  yang **dibangun ulang sendiri**. nb03 memakai kolom `gap_return` milik
  stratifikasi nb00. Dua definisi "no-gap" berbeda.
- **Bukti**:
  - `scripts/_build_eda05.py:450-451`:
    `pair_ok = np.diff(t15) == np.timedelta64(900, "s")` /
    `sign_acf1 = np.corrcoef(np.sign(v15[:-1][pair_ok]), np.sign(v15[1:][pair_ok]))[0, 1]`.
  - nb03 sel sign-ACF:
    `row = acf_table(sign_frame, [1], ~subset["gap_return"]).iloc[0]`.
  - Angka: nb05 `-0.022005` vs nb03 `-0.022624`, selisih `0,000619` = 2,74 %
    dari `|-0,022624|`.
- **Dampak**: bukan salah aritmetika - arah dan tanda benar, dan 2,74% masuk akal
  untuk perbedaan definisi himpunan pasangan. Yang tidak dapat diverifikasi
  adalah klaim "replika" tanpa catatan bahwa metodenya berbeda. `n_no_gap` nb03
  untuk M15-A lag 1 = `75038`; nb05 **tidak mencetak n** untuk metrik ini,
  sehingga selisih 2,74% tidak bisa diatribusi.
- **Saran**: cetak `n_no_gap` di output, dan tambahkan satu kalimat yang
  menyatakan sumber definisi no-gap (adjacency timestamp, bukan kolom
  `gap_return`).

### [MEDIUM-02] Keempat assertion replika adalah band lebar, bukan kunci fidelity

- **Lokasi**: `scripts/_build_eda05.py:445, 446, 453, 543`.
- **Masalah**: keempat assertion yang dimaksudkan mengunci replika hanya
  rentang lebar yang akan lolos pada nilai yang benar maupun pada nilai yang
  salah secara substansial.
- **Bukti** (lebar band vs jarak ke referensi):
  - `_build_eda05.py:445` `assert abs(acf1_m15_a) < 0.05` - referensi
    `0.001793`; band 0,05 = **sekitar 2.800 % dari nilai acuan**. Lolos pada
    ACF 10x lipatnya.
  - `_build_eda05.py:446` `assert 0.9 < mean_vr < 1.2` - referensi `1.0312`;
    batas atas +16,4 %, batas bawah -12,7 %, dan **tidak menyebut `1.0312`
    sama sekali**. Lolos pada VR 0.90 maupun VR 1.20.
  - `_build_eda05.py:453` `assert -0.030 < sign_acf1 < -0.015` - referensi
    `-0.022624`; batas bawah +32,6 %, batas atas -33,7 %. Lolos pada sign-ACF
    yang medannya nol.
  - `_build_eda05.py:543` `assert 45.0 < SWING_PER_DAY_K3 < 52.0` - referensi
    `49.070`; batas bawah -8,3 %, batas atas +6,0 %. Lolos pada selisih 3
    swing/hari.
- **Dampak**: skor "53 assertion PASS" pada klaim coder C1 **tidak membuktikan
  fidelity empat metrik ini**. Empat assertion tersebut hanya membuktikan
  bahwa output berada di rentang yang wajar. Draf audit sebelumnya justru
  menafsirkan kelolosan band-band ini sebagai "replika lolos toleransi
  referensi", yang merupakan inferensi salah.
- **Saran**: ubah menjadi kunci ketat dengan toleransi yang dinyatakan eksplisit,
  misalnya `abs(acf1_m15_a - 0.001793) < 0.0005`,
  `abs(mean_vr - 1.0312) < 0.005`, `abs(sign_acf1 + 0.022624) < 0.001`,
  `abs(SWING_PER_DAY_K3 - 49.070) < 0.05`. Band lebar boleh **tetap ada
  sebagai assertion kedua**, tetapi harus diberi nama berbeda agar tidak dibaca
  sebagai pembuktian fidelity.

### [LOW-01] Draf sebelumnya memakai referensi ACF dari kolom yang salah

- **Lokasi**: draf `eda_nb05_audit_v1.md:14` (baris tabel "ACF lag-1 M15-A").
- **Masalah**: draf membandingkan `0.0018` nb05 dengan `+0.0035` dan
  menyebutnya "selisih 0.0017". Nilai `+0.003496` adalah kolom **`acf_no_gap`**
  nb03; nb05 menghitung ACF atas seri penuh (tanpa filter gap) sehingga
  pasangannya adalah kolom **`acf_all` = `0.001793`**.
- **Bukti**: nb03 tabel ACF M15 strata A, baris lag 1 =
  `acf_all 0.001793` / `acf_no_gap 0.003496` / `p_value_no_gap 0.338177` /
  `n_no_gap 75038`. Band assert nb05 `_build_eda05.py:445` juga mengindikasikan
  seri penuh, bukan no-gap.
- **Dampak**: secara faktual **berpihak pada coder** - selisih sebenarnya hanya
  `0.000004` (0,22 %), bukan 0.0017. Draf tersebut melapor terlalu buruk
  sehingga memunculkan temuan semu. Dicatat agar tidak diwariskan ke audit
  berikutnya.
- **Saran**: tidak ada perbaikan kode; koreksi ini sudah diterapkan di tabel 1.1.

### [LOW-02] Angka swing: replika justru identik, tetapi draf membandingkan statistik yang salah dan memakai kata terlarang

- **Lokasi**: draf `eda_nb05_audit_v1.md:17, 23`.
- **Masalah**: draf membandingkan `49,07` dengan `mean 48,74` dan
  `median 49,00` nb04. Keduanya berasal dari distribusi **gabungan k=3+k=5**
  (`gabungan 40207 / 48.736`), bukan k=3 saja. Draf juga memberi label
  `EXACT MATCH` pada baris yang sama dengan "selisih 0,33 (0,7%)".
- **Bukti**:
  - nb04 D6: `high_k3 20169 -> 24.447`, `low_k3 20314 -> 24.623`;
    `gabungan 40207 -> 48.736`; sebaran gabungan `mean 48.74`, `50% 49.00`.
  - `20169 + 20314 = 40483` = nilai `swings` persis di nb05 sel 11.
  - `24.447 + 24.623 = 49.070` = nilai `49.07` nb05 sampai 3 desimal.
  - Catatan nb05 sendiri sudah benar, `_build_eda05.py:542`:
    `"referensi nb04: k=3 high 20.169 / low 20.314 (sekitar 49/hari); gabungan k=3+k=5 = 48,74/hari"`.
- **Dampak**: kesimpulan fidelity swing **benar** dan lebih kuat dari draf -
  cocok sampai angka bulat. Yang salah adalah tabel pembanding draf dan pemakaian
  kata yang dilarang.
- **Saran**: tidak ada perbaikan kode; terapkan baris 4 tabel 1.1.

### [LOW-03] Draf sebelumnya memuat bukti baris samar

- **Lokasi**: draf `eda_nb05_audit_v1.md:29` -
  `` `_build_eda05.py` baris replikasi: sign-ACF assert (baris ~t15) ``.
- **Masalah**: nomor baris tidak dipatoki sehingga pembaca tidak dapat
  memverifikasi.
- **Bukti**: `baris ~t15` bukan nomor baris yang valid pada `_build_eda05.py`;
  baris 15 file itu berisi hal lain yang tidak terkait.
- **Dampak**: bukti tidak dapat diperiksa ulang - melanggar AGENTS.md §20 butir 9
  ("paste output asli") dan butir 7 (self-audit klaim).
- **Saran**: seluruh bukti di dokumen ini memakai `file:baris` eksak.

---

## Yang Sudah Benar

- **Hitungan swing nb05 identik dengan nb04** - `40483 = 20169 + 20314` bulat,
  dan `49,070 = 24.447 + 24.623` sampai 3 desimal. Fungsi `fractal_mask` di
  `_build_eda05.py:507-534` adalah **salinan verbatim** dari
  `scripts/_build_eda04.py` dan menghasilkan hitungan yang cocok. Ini bukti
  fidelity terkuat di antara keempat metrik.
- **Rujukan swing di nb05 sendiri sudah jujur** - `_build_eda05.py:542`
  menyebutkan angka k=3 dan k=3+k=5 terpisah, sehingga kode tidak menyesatkan;
  kesalahan pembacaan ada di draf audit, bukan di builder.
- **ACF lag-1 nb05 cocok sampai 4 desimal** dengan `acf_all` nb03
  (`0.001789` vs `0.001793`) pada basis perhitungan yang sama (seri penuh).
- **Dua metrik ACF memang dipisahkan secara eksplisit** di builder:
  `acf1_m15_a` (besaran, `_build_eda05.py:436`) dan `sign_acf1` (tanda,
  `_build_eda05.py:451`). Insiden salah-baca "-0,022624 adalah ACF besaran"
  **tidak terulang** - komentar `_build_eda05.py:447` menyebutnya sebagai
  "headline D4 nb03" dan mengaitkannya ke variabel `sign_acf1`. (Detail insiden
  ini adalah materi Langkah 2; di sini hanya saya konfirmasi tidak ada
  pencampuran variabel.)
- **Struktur notebook sah** - `eda_05_regimes.ipynb` `nbformat 4.5`,
  25 sel / 18 sel kode, **0 output bertipe `error`** (dihitung ulang oleh
  auditor dari `cells[]`, bukan diambil dari klaim C1).
- **Pemetaan hari M15/M5 ke hari broker diaudit eksplisit** -
  `assert n_leading == 1` (`_build_eda05.py:430`) dan
  `assert n_leading5 == 1` (`_build_eda05.py:500`) mengunci pengecualian bucket
  pembuka; keduanya berjalan tanpa error pada output sel 9 dan sel 11.

---

## Pertanyaan untuk Coder

1. **VR (HIGH-01 + HIGH-02)** - pertahankan hitungan VR versi nb05 (`ddof=0`,
   seri penuh) atau samakan dengan nb03 (`ddof=1`, no-gap)? Jika mempertahankan
   versi nb05, apakah label output `"replica nb03"` pada
   `_build_eda05.py:422, 443, 444` akan diubah menjadi label non-replika?
2. **VR** - apakah angka `1,0337` di `_build_eda05.py:444` dan sel 9 nb05 akan
   diganti ke `1,0312`, atau kedua angka dicetak berdampingan dengan keterangan
   masing-masing?
3. **Swing (LOW-02, konfirmasi)** - apakah Coder concurring bahwa referensi yang
   benar adalah `high_k3 24.447 + low_k3 24.623 = 49,070`, bukan `48,74` yang
   berasal dari kombinasi k=3+k=5?
4. **Sign-ACF (MEDIUM-01)** - mengapa `n_no_gap` tidak dicetak? Apakah selisih
   2,74 % bisa direduksi dengan menyamakan definisi no-gap ke kolom `gap_return`?
5. **Assertion (MEDIUM-02)** - Coder akan memasang kunci ketat seperti usulan di
   atas, atau mempertahankan band lebar dengan alasan tertulis?
6. **Draf sebelumnya** - apakah ada salinan lain dari draf audit yang memuat klaim
   `assert abs(mean_vr - 1.0337) < 0.05`, agar tidak ikut tersalin ke laporan lain?

---

## Yang Belum Diverifikasi (Langkah 1)

- Klaim C1 selain 4 angka replika: `53 assertion PASS`, `nbconvert exit=0`,
  `chi2 p=0,325`, `RV B/A = 1,59x`, `strata 825/130/19 hari`, dan gate
  `ruff` / `pytest` / `validate` / `foreign_chars`. Semua **di luar Langkah 1**.
  Yang sudah saya konfirmasi tanpa menerima klaim: 25 sel / 18 kode / 0 error.
- Klaim C2 (H1-H5 lengkap), C3 (isi `report.md`), C4 (registry FIG-01..07 dan
  byte-identik FIG-01..03) - **belum disentuh**.
- Presisi digit `chi2 p=0,325`: output sel 7 nb05 mencetak `p={p_chi:.4g}` yang
  menghasilkan `0.325`, sehingga digit terakhir pembulatan tidak dapat
  dipastikan tanpa membaca `report.md`. Ditunda ke langkah terpisah.

---

# RE-AUDIT LANGKAH 1 (putaran 2, 2026-10-06)

Objek: builder `8ac848ce2f7d`, notebook `93ea76955742`. Metode: setiap temuan
putaran 1 diverifikasi ulang **langsung dari disk** - bukan dengan membaca
jawaban Coder, dan bukan dengan menganggap perbaikan sudah benar.

## A. Verifikasi 4 temuan, satu per satu

### [HIGH-01] TERTUTUP - referensi VR dikoreksi ke `1,0312`

- **Lokasi perbaikan**: `scripts/_build_eda05.py:486` dan `:487`.
- **Bukti kode**:
  - `_build_eda05.py:486`
    `print(f"rata-rata VR(5,15,60) = {mean_vr:.4f} (referensi nb03: 1,0312)")`
  - `_build_eda05.py:487`
    `print("catatan: 1,0337 pada nb03 = rata-rata VR LAG 2-60, bukan pembanding horizon 5/15/60")`
  -`_build_eda05.py:667` `"referensi_vr_nb03": 1.0312,` (di blok H2)
  - `_build_eda05.py:670` catatan pada `h2["metrik_pendukung"]`:
    `"1,0337 pada nb03 = rata-rata VR lag 2-60, bukan pembanding horizon."`
- **Bukti output** (nb05 sel 9, 0-based):
  ```
  VR per horizon: VR(5)=1.0160, VR(15)=1.0119, VR(60)=1.0657
  rata-rata VR(5,15,60) = 1.0312 (referensi nb03: 1,0312)
  catatan: 1,0337 pada nb03 = rata-rata VR LAG 2-60, bukan pembanding horizon 5/15/60
  ```
- **Verifikasi silang**: `1.0160 + 1.0119 + 1.0657 = 3,0936`; `/3 = 1,03120`
  -> tercetak `1.0312`. Band VR per horizon pada output nb05 kini **identik
  digit** dengan tabel horizon nb03 (lihat §1.1 turn 1: nb03 M15 lag
  5/15/60 = 1.0160 / 1.0119 / 1.0657).
- **Status**: TERTUTUP. Kedua statistik kini dicetak berdampingan dengan
  keterangan masing-masing, sesuai usulan.

// placeholder baris 1

### [HIGH-02] TERTUTUP - metode VR disamakan secara struktural dengan nb03

Ini temuan paling serius di putaran 1 karena pada prinsipnya harus mengubah
perhitungan, bukan hanya label. Yang dilakukan Coder adalah **menyalin fungsi
nb03 secara verbatim** dan menjalankannya di atas seri no-gap yang didefinisikan
dengan kolom `gap_return`.

- **Lokasi perbaikan**: `scripts/_build_eda05.py:450-476` (fungsi),
  `:479-483` (pemanggilan), `:432-433` (pemetaan hari M15).
- **Bukti kode**:
  - Docstring `:409-415` menyatakaneksplisit:
    `"Metode replika = METODE EKSAK nb03 (bukan varian nb05): VR memakai salinan verbatim fungsi variance_ratio nb03 (ddof=1, jumlah bertumpang tindih via cumsum) di atas seri NO-GAP berbasis kolom gap_return ... - sama seperti pemanggilan nb03."`
  - `:468` `var1 = float(np.var(values, ddof=1))` - **ddof=1**, bukan lagi ddof=0.
  - `:473-475` jumlah bertumpang tindih via `cumsum`, bukan `rolling().sum()`:
    `cumulative = np.concatenate(([0.0], np.cumsum(values)))` /
    `lag_sum = cumulative[lag:] - cumulative[:-lag]` /
    `var_lag = float(np.var(lag_sum, ddof=1))`.
  - `:479-482`
    `no_gap = ~m15_a["gap_return"]` / `clean = m15_a.loc[no_gap, "r"]` /
    `vr = {k: variance_ratio(clean, k) for k in (5, 15, 60)}` - **no-gap**,
    bukan seri penuh.
  - `:441` `m15["gap_return"] = m15["utc"].diff() > pd.Timedelta(minutes=15)`
  - `:450` `def variance_ratio(...)` dengan docstring
    `"SALINAN VERBATIM dari scripts/_build_eda03.py (sumber kebenaran Q4)"`.
- **Verifikasi silang ke nb03** (bukan klaim Coder):
  - nb03 sel VR, fungsi `variance_ratio`: `var1 = float(np.var(values, ddof=1))`,
    `cumulative = np.concatenate(([0.0], np.cumsum(values)))`,
    `lag_sum = cumulative[lag:] - cumulative[:-lag]`,
    `var_lag = float(np.var(lag_sum, ddof=1))`,
    `return var_lag / (lag * var1)`.
  - nb03 pemanggil: `clean = subset.loc[~subset["gap_return"], "r"]` lalu
    `variance_ratio(clean, lag)`.
  - nb03 definisi gap: `out["gap_return"] = out["utc"].diff() > pd.Timedelta(minutes=TF_MINUTES[tf])`.
  - **Kesimpulan**: baris `:466-476` nb05 identik dengan nb03 baris demi baris,
    dan `:479-482` identik dengan pemanggilan nb03. Yang berubah bukan hanya
    kebetulan angka.
- **Tambahan yang tidak diminta tetapi benar**: pemetaan `broker_day` M15 juga
  diubah dari aproksimasi `searchsorted` ke `wall_clock_series` -
  `_build_eda05.py:432-433`
  `m15["wall"] = wall_clock_series(m15["broker_time_raw")` /
  `m15["broker_day"] = m15["wall"].dt.normalize()`.
  Ini persis `load_timeframe` nb03. Alasan dicatat di `:427-431`: aproksimasi
  lama "menggeser bucket pembuka hari yang M1-nya terlambat (mis. 22:07) ke hari
  sebelumnya, sehingga himpunan bar A dan hitungan gap_return tidak identik nb03".
  Di-bukti dengan dua assertion paritas baru (lihat bagian C).
- **Status**: TERTUTUP.

### [MEDIUM-01] TERTUTUP - definisi no-gap disamakan, `n_no_gap` dicetak, parity di-assert

- **Lokasi perbaikan**: `scripts/_build_eda05.py:436-441`, `:479-481`,
  `:498-507`.
- **Bukti kode**:
  - `:441` `m15["gap_return"] = m15["utc"].diff() > pd.Timedelta(minutes=15)`
    - kolom stratifikasi, bukan adjacency timestamp yang dibangun ulang.
  - `:436-440` komentar menyatakan alasan: `"Definisi no-gap = kolom gap_return
    milik stratifikasi nb00 ... BUKAN adjacency timestamp yang dibangun ulang.
    Versi adjacency lama menghasilkan sign-ACF -0,022005 (meleset 2,74% dari
    nb03) karena himpunan pasangannya berbeda"`.
  - `:498-503` sign-ACF sekarang memakai rumus `acf_table` nb03 yang
    diduplikasi (centered dot product), bukan `np.corrcoef(np.sign(...))`:
    `values = sign_frame.loc[no_gap, "r"]` ... `values = values - values.mean()` /
    `sign_acf1 = float(np.dot(values[:-1], values[1:])) / denom`.
  - `:504-505` output mencantumkan sumber definisi:
    `"sign-ACF lag-1 M15 (A, no-gap kolom gap_return)"` dan
    `"  (referensi nb03: -0,022624)"`.
  - `:506` `print(f"n_no_gap M15-A = {n_no_gap:,} bar (nb03: 75.038); definisi no-gap = kolom gap_return")`
  - `:507` `assert n_no_gap == 75_038, "n no-gap M15-A tidak cocok dengan nb03 - definisi no-gap berbeda"`
- **Bukti output** (nb05 sel 9):
  ```
  replica nb03: sign-ACF lag-1 M15 (A, no-gap kolom gap_return) = -0.022624
    (referensi nb03: -0,022624)
  n_no_gap M15-A = 75,038 bar (nb03: 75.038); definisi no-gap = kolom gap_return
  ```
- **Verifikasi silang**: nb03 tabel `=== ACF M15 (stratum A, lag 1-60) ===`
  baris lag 1 mencatat `n_no_gap 75038`; nb03 sel sign-ACF mencatat
  `A M15: sign-ACF(1) = -0.022624`. Output nb05 kini **identik pada 6 desimal
  dan pada n**.
- **Status**: TERTUTUP. Selisih 2,74 % yang saya laporkan pada putaran 1
  **telah hilang sepenuhnya** - bukan dikecilkan, melainkan nol.

### [MEDIUM-02] TERTUTUP - kunci ketat dipasang, band lebar jadi lapis kedua bernama

- **Lokasi perbaikan**: `scripts/_build_eda05.py:488-496`, `:507-511`,
  `:601-604`, `:682-685`.
- **Bukti kode - kunci ketat (lapis pertama)**vs**band lebar (lapis kedua, diberi nama)**:

  | Metrik | Kunci ketat (baru) | Band lebar (lapis kedua) | Shader ke bandwidth lama |
  |---|---|---|---|
  | ACF1 | `:489` `abs(acf1_m15_a - 0.001793) < 0.0005` | `:492` `abs(acf1_m15_a) < 0.05` | 0,05 -> 0,0005 (100x lebih ketat) |
  | mean VR | `:493` `abs(mean_vr - 1.0312) < 0.005` | `:496` `1.025 < mean_vr < 1.038` | tidak menyebut acuan -> menyebut `1.0312` |
  | sign-ACF | `:508` `abs(sign_acf1 + 0.022624) < 0.001` | `:511` `-0.030 < sign_acf1 < -0.015` | 33% -> 0,001 absolut |
  | swing | `:601` `abs(SWING_PER_DAY_K3 - 49.070) < 0.05` | `:604` `45.0 < SWING_PER_DAY_K3 < 52.0` | 7% -> 0,05 absolut |

  Band lebar **dipertahankan** (sesuai usulan auditor di `:Saran`) tetapi
  diberi nama eksplisit `"band lebar kedua: ..."` di semua empat assertion,
  sehingga tidak lagi bisa dibaca sebagai pembuktian fidelity.
- **Verifikasi silang**: keempat nilai kunci ketat berasal dari angka nb03/nb04
  yang saya kutip sendiri di putaran 1 - `0.001793` (nb03 `acf_all`),
  `1.0312` (rata-rata tabel horizon nb03 yang saya hitung),
  `-0.022624` (nb03 SIGN_ACF_TABLE), `49.070` (nb04 D6 `24.447+24.623`).
  Tidak ada angka kunci yang tidak berasal dari sumber.
- **Tambahan**: assertion yang sama diulang di blok H2 (`:673` `abs(mean_vr - 1.0312) < 0.005`
  dengan `:674` sebagai band lebar kedua), sehingga metrik pendukung H2 juga
  terkunci ketat, bukan hanya sel replikanya.
- **Status**: TERTUTUP.

## B. Verifikasi 6 pertanyaan

| # | Pertanyaan | Jawaban Coder di disk | Verifikasi auditor | Status |
|---|---|---|---|---|
| 1 | Pertahankan VR versi nb05 atau samakan dengan nb03? | `laporan_tahap_11_regime.md:80-81` "metode replika VR & sign-ACF di nb05 DISAMAKAN dengan nb03 (ddof=1 + no-gap via kolom `gap_return`, fungsi `variance_ratio` salinan verbatim `_build_eda03.py`)" | Konfirmasi dari kode: `:468` ddof=1, `:473-475` cumsum, `:479-482` no-gap, `:450` docstring "SALINAN VERBATIM". Cocok dengan jawaban. | Terjawab & diterapkan |
| 2 | `1,0337` diganti `1,0312` atau keduanya berdampingan? | `laporan_tahap_11_regime.md:83-84` "rata-rata VR(5,15,60) = 1,0312 (referensi benar; 1,0337 = rata-rata VR lag 2-60)" | `:486` pakai `1,0312`; `:487` mencetak `1,0337` sebagai catatan; `:670` mengulang di H2. **Keduanya** - lebih baik dari salah satu. | Terjawab & diterapkan |
| 3 | Konfirmasi referensi swing `49,070` bukan `48,74`? | Tidak dijawab eksplisit di laporan; `_build_eda05.py:601-604` memakai `49.070` di kunci ketat | Konfirmasi dari kode: `:601` `abs(SWING_PER_DAY_K3 - 49.070) < 0.05` mengonfirmasi `49.070` adalah acuan yang benar. Numerik swap **tidak pernah terjadi** - angka swing tidak berubah sama sekali antar putaran (`40,483 -> 49.07` di kedua putaran). | Terjawab oleh kode |
| 4 | Mengapa `n_no_gap` tidak dicetak? Bisakah 2,74% direduksi? | `laporan_tahap_11_regime.md:84-85` "sign-ACF = -0,022624 (identik nb03, n_no_gap 75.038). Angka lama ... = metode adjacency lama yang diganti" | `:506` mencetak n, `:507` meng-assert `== 75_038`. Selisih 2,74% **telah dihilangkan** (`-0.022624`). | Terjawab & diterapkan |
| 5 | Kunci ketat atau pertahankan band lebar? | `laporan_tahap_11_regime.md:85-86` "assertion dikunci ketat terhadap angka referensi + band lebar sebagai lapis kedua" | 4 kunci ketat + 4 band lebar bernama "band lebar kedua" - persis usulan auditor. | Terjawab & diterapkan |
| 6 | Ada salinan lain dari draf bermasalah? | Tidak ada jawaban eksplisit | **BELUM DIVERIFIKASI.** Ini soal proses, bukan isi file; tidak dapat diverifikasi dari disk. Yang dapat diverifikasi: tidak ada lagi(assert `abs(mean_vr - 1.0337) < 0.05)` di builder mana pun yang saya pindai - hanya `_build_eda05.py` yang relevan dan isinya bersih. | Tidak dapat diverifikasi |

## C. Temuan tambahan yang muncul saat re-audit

### [CLOSED-NOTED] Dua assertion paritas baru strengthens replika M15

- **Lokasi**: `scripts/_build_eda05.py:444-445`.
- **Isi**: `assert len(m15_a) == 75_863, "bar M15-A harus 75.863 (paritas nb03)"` dan
  `assert int(m15_a["gap_return"].sum()) == 825, "gap_return M15-A harus 825 (paritas nb03)"`.
- **Efek**: mengunci himpunan bar M15-A **dan** definisi no-gap terhadap nb03,
  termasuk jumlah `gap_return` yang harus cocok dengan nb03 (`M15=825` pada
  nb03 baris `gap_return: M1=1,603, M5=836, M15=825`).
- Ini menutup celah yang saya tandai di HIGH-02: perubahan pemetaan hari M15
  bisa saja menggeser himpunan bar tanpa terdeteksi. Sekarang terkunci.
- **Catatan**: strengthen, bukan temuan baru - tidak menaikkan hitungan temuan.

### [CLOSED-NOTED] Jumlah assertion 53 -> 59, dan hitungannya dihitung ulang

`laporan_tahap_11_regime.md:86-87` menyebut "Jumlah assertion notebook kini 59
(53 sebelumnya + 6 baru: paritas bar/gap M15-A, n_no_gap, dan 3 kunci ketat
VR/ACF/sign)". Verifikasi: hitungan baris `assert` pada 18 sel kode = **59**,
dan `execution_count` = `[1..18]` monoton tanpa error. Angka 59 **terverifikasi**.

## D. Angka replika final (putaran 2)

| # | Metrik | nb05 putaran 2 | Referensi nb03/nb04 | Selisih putaran 1 -> 2 |
|---|---|---|---|---|
| 1 | ACF lag-1 M15-A (besaran) | **0.001793** | nb03 `acf_all` 0.001793 | 0.000004 -> **0** |
| 2 | Sign-ACF lag-1 M15-A (no-gap) | **-0.022624** | nb03 -0.022624 | 0.000619 -> **0** |
| 3 | Rata-rata VR(5,15,60) M15-A | **1.0312** | nb03 tabel horizon -> 1.0312 | 0.0035 -> **0** |
| 4 | Swing M5 k=3 high+low (A) | **40.483** / 49.07 per hari | nb04 20.169+20.314 = 40.483 / 49.070 | 0 -> **0** |

Keempat angka kini cocok sampai digit terakhir dengan referensi. Empat di antaranya
(HIGH-01, HIGH-02, MEDIUM-01, MEDIUM-02) **tertutup**.

## E. Yang tetap belum diverifikasi (putaran 2)

Tidak berubah dari putaran 1, dan **tetap di luar Langkah 1**:

- Klaim C1 lain: `nbconvert exit=0`, `chi2 p=0,325`, `RV B/A = 1,59x`,
  `strata 825/130/19 hari`, gate `ruff` / `pytest` / `validate` / `foreign_chars`.
  Yang sudah dikonfirmasi tanpa menerima klaim: 25 sel / 18 kode / 0 error /
  59 assertion / `execution_count` monoton.
- Klaim C2 (H1-H5 lengkap), C3 (`report.md` angka-per-angka), C4 (registry
  FIG-01..07 byte-identik FIG-01..03).
- Pertanyaan 6 (apakah ada salinan draf lain) - tidak dapat diverifikasi dari disk.
- Prediksi look-ahead/leakage padaNb05 - **ini adalah Langkah 3**, belum disentuh.

---

## STOP - Tunggu Keputusan User

**Langkah 1: LULUS.** Verdict ini tidak mencakup Langkah 2-10.

Langkah 2-10 **tidak** dikerjakan. Menunggu perintah batch eksplisit.
Daftar: (2) insiden ACF - (3) look-ahead/leakage - (4) H1-H5 -
(5) `report.md` angka-per-angka - (6) item BELUM DIVERIFIKASI -
(7) registry FIG - (8) temuan jujur - (9) bug riwayat - (10) konvensi §19/RULES.

---

# BATCH A - LANGKAH 2 + LANGKAH 3 (2026-10-06)

Objek audit (blob terverifikasi dari disk):
`scripts/_build_eda05.py` = `8ac848ce2f7d`, `notebooks/scalping/eda_05_regimes.ipynb`
= `93ea76955742`, `reports/eda/2026-10-06/report.md` = `72e837778dfc`,
`laporan_tahap_11_regime.md` = `6ab21459e91e`,
`laporan_tahap_12_sintesis.md` = `eae21308c04d`.
Langkah 4-10 dan seluruh materi lama tidak dibuka.

---

# LANGKAH 2 - INSIDEN SALAH-BACA ACF (resolusi "dua metrik")

## 2.1 Klaim yang diuji

Klaim Coder: "-0,022624 adalah sign-ACF (metrik tanda, D4 nb03), bukan ACF besaran;
builder mengunci keduanya terpisah (acf1_m15_a vs sign_acf1)".

**HASIL UJI: KLAIM BENAR.** Diverifikasi dari sumber, bukan dari label.

### Bukti bahwa -0,022624 memang sign-ACF, bukan ACF besaran

- `eda_03_autocorr.ipynb` sel 11 output, tabel `=== Sign-ACF lag 1 (no-gap) ===`:
  baris `M15` kolom A = `-0.022624`; baris teks
  `A M15: sign-ACF(1) = -0.022624 -> mean-reversion`.
- `eda_03_autocorr.ipynb` sel 7 output, blok
  `=== ACF M15 (stratum A, lag 1-60) ===`, baris `lag 1`:
  `acf_all = 0.001793`, `acf_no_gap = 0.003496`.
  Kedua-duanya **positif**; tidak ada kolom besaran bernilai -0,022624.
- `eda_03_autocorr.ipynb` sel 0 markdown "Yang dijawab": butir
  `**Sign-autocorrelation lag-1** (ACF dari tanda return) - D4`.
  Jadi kode rancangan **D4 memang metrik tanda**.

Kesimpulan: untuk M15 stratum A, ACF besaran = +0,001793 (all) atau +0,003496
(no-gap); -0,022624 adalah ACF tanda. Klaim terkonfirmasi.

## 2.2 Rujukan komentar "headline D4 nb03" - AKURAT

`_build_eda05.py:497`:

    # Sign-ACF lag-1 (no-gap) = headline D4 nb03 (-0,022624 M15 A) - kunci replikanya.

Rujukan ini akurat pada tiga hal sekaligus: (a) D4 = sign-ACF, sesuai sel 0 nb03;
(b) -0,022624 adalah nilai M15 A, sesuai `SIGN_ACF_TABLE` sel 11; (c) "headline"
sah karena sel 23 nb03 mencetak ulang `-0.022624` pada blok ringkasan penutup
`sign-ACF lag-1 (no-gap)`. Tidak ada komentar yang salah rujuk.

## 2.3 Jejak pemakaian variabel - tidak ada pencampuran

| Variabel | Definisi | Semua pemakaian |
|---|---|---|
| `acf1_m15_a` (besaran) | `:447` `float(r15.autocorr(lag=1))`, seri penuh termasuk gap | `:484` print, `:489` assert ketat, `:492` assert band, `:655` teks klaim H2, `:661` dict H2 |
| `sign_acf1` (tanda) | `:503` rumus `acf_table` nb03 di atas seri no-gap | `:504` print, `:508` assert ketat, `:511` assert band, `:662` dict H2 |

Himpunan pemakaian kedua variabel **saling lepas**. Tidak ada satu pun baris yang
memakai `acf1_m15_a` bersama acuan -0,022624, atau `sign_acf1` bersama acuan
0,001793. Kunci numeriknya terpisah dan tidak tertukar.

## 2.4 Konsistensi label di semua lima permukaan

| Lokasi | Angka | Label | Benar? |
|---|---|---|---|
| `_build_eda05.py:413-414` (docstring) | - | "ACF lag-1 = ACF BESARAN seri penuh (padanan `acf_all` ... bukan `acf_no_gap`)" | ya |
| `_build_eda05.py:489-490` | 0,001793 | "ACF1 M15 A menyimpang dari acf_all nb03" | ya |
| `_build_eda05.py:508-509` | -0,022624 | "sign-ACF lag-1 M15 A keluar dari referensi nb03" | ya |
| nb05 sel 9 output baris 1 | 0,001793 | "replica nb03 M15 (stratum A): ACF lag-1" | ya (lihat L2-02) |
| nb05 sel 9 output baris 5 | -0,022624 | "sign-ACF lag-1 M15 (A, no-gap kolom gap_return)" | ya |
| `report.md:56` | -0,022624 | "Sign-ACF lag-1 ... terbaca di TANDA, bukan besaran" | ya |
| `report.md:93` | -0,022624 | "sign-ACF no-gap" | ya |
| `report.md:116` | -0,022624 | "sign-ACF -0,022624 (metode eksak nb03)" | ya |
| `laporan_tahap_11_regime.md:84` | -0,022624 | "sign-ACF = -0,022624 (identik nb03)" | ya |
| `laporan_tahap_11_regime.md:60` | -0,022005 | angka lama, ditandai usang di `:84-85` | ya (ter-disclose) |
| `laporan_tahap_12_sintesis.md:25` | 0,001793 dan -0,022624 | "ACF1 M15-A = +0,001793 (nb03 acf_all); sign-ACF(1) no-gap = -0,022624" | ya |

**Tidak ada satu pun tempat** di mana besaran dan tanda tertukar. Angka lama
-0,022005 dan 1,0277 masih muncul di `report.md:94` dan `laporan_tahap_11_regime.md:60`,
keduanya eksplisit ditandai sebagai "metode berbeda yang kini diganti".

## 2.5 Konsistensi catatan 1,0337

Tiga tempat diminta + dua tambahan, semuanya konsisten:

- `_build_eda05.py:487` "catatan: 1,0337 pada nb03 = rata-rata VR LAG 2-60, bukan pembanding horizon 5/15/60"
- nb05 sel 9 output baris 4, identik dengan `_build_eda05.py:487`
- `_build_eda05.py:670` (dict H2) "1,0337 pada nb03 = rata-rata VR lag 2-60, bukan pembanding horizon"
- `report.md:57` "rata-rata VR(2-60): ... A M15 1,0337" - konsisten
- `report.md:95` "referensi lama 1,0337 = rata-rata VR **lag 2-60** nb03" - konsisten

Verifikasi silang ke sumber: `eda_03_autocorr.ipynb` sel 21 output
`DELTA_AB` baris `M15` kolom `vrmean_A` = `1.033710`, dan kode sel 21 adalah
`a_vr = float(VR["A"][tf].loc[2:60].mean())`. Jadi 1,0337 memang rata-rata VR
lag 2-60. Tidak ada sisa label lama yang belum terganti.

## 2.6 TEMUAN LANGKAH 2

### [L2-01] LOW - Proksimit pembulatan 4 desimal antara dua metrik berbeda

- **Lokasi**: `report.md:54` vs `report.md:56`; sumbernya sel 7 dan sel 11 nb03.
- **Bukti angka**:
  - `report.md:54`: "maks |ACF| = 0,022639 (B M15 lag 50; no-gap)" - **terverifikasi
    benar**. Hitung ulang dari `=== ACF M15 (stratum B, lag 1-60) ===` sel 7 nb03:
    baris `lag 50` kolom `acf_no_gap` = `-0.022639`, dan itu memang maksimum
    |acf_no_gap| lintas seluruh strata/TF/lag.
  - `report.md:56`: sign-ACF M15 A = `-0,022624`.
- **Masalahnya**: kedua angka berbeda **1,5e-5** - tidak dapat dibedakan pada
  pembulatan 4 desimal. Keduanya negatif, keduanya no-gap, keduanya "ACF".
  Lebih buruk, `eda_03_autocorr.ipynb` sel 23 mencetak ringkasan
  `|ACF| maksimum lintas strata/TF = 0.0226` (4 desimal), dan `-0.022624` juga
  membulat menjadi `0.0226`. **Inilah akar insiden salah-baca ACF**: satu label
  bulat, dua metrik berbeda dengan stratum dan lag berbeda (B M15 lag 50 besaran
  vs A M15 lag 1 tanda).
- **Penanganan saat ini benar**: `report.md:54` dan `:56` masing-masing melabeli
  metrik, strata, dan lag dengan benar. Tidak ada tertukar di laporan.
- **Sifat temuan**: bukan kesalahan nb05, melainkan **risiko residuel yang masih
  hidup secara struktural** karena sumbernya sendiri mencetak 4 desimal. Dicatat
  agar tidak terulang di audit berikutnya dan agar tidak ada yang menyimpulkan
  "0,0226 = ACF M15 A" di masa depan.
- **Saran**: cetak 6 desimal pada ringkasan maks |ACF|, atau tambahkan sufiks
  metrik pada ringkasan sel 23 nb03.

### [L2-02] LOW - Kunci dict `acf1_M15_A` tidak membawa penanda all/no-gap

- **Lokasi**: `_build_eda05.py:661`, dibandingkan `:662`.
- **Bukti**: `:661` `"acf1_M15_A": round(acf1_m15_a, 6)` bernilai `0.001793`, yaitu
  **ACF besaran seri penuh** (`acf_all`, sesuai definisi `:447` dan docstring
  `:413`). `:662` `"sign_acf1_M15_A_nogap"` justru membawa sufiks `_nogap`.
  Kunci pertama tidak, padahal keduanya berbeda versi no-gap.
- **Risiko**: pembaca hilir yang membandingkan `acf1_M15_A` = 0,001793 dengan
  `acf_no_gap` M15-A nb03 = **0,003496** akan menyimpulkan ada bug replika,
  padahal yang dibandingkan berbeda versi. Nilai yang tersimpan sendiri **benar**.
- **Mitigasi sudah ada**: docstring `:413-414` menyatakan bedanya secara eksplisit.
  Jadi ini kekurangan penanda pada output, bukan kesalahan.
- **Saran**: ubah kunci menjadi `acf1_M15_A_all` atau tambahkan field
  `catatan_acf1_versi` pada dict H2. Baris print `:484` dan teks klaim `:655`
  juga sebaiknya menyebut "ACF lag-1 (all)".

## 2.7 Verdict LANGKAH 2: LULUS

Klaim "dua metrik" **terbukti benar** dan implementasinya benar di kelima
permukaan. Dua temuan LOW di atas adalah penguatan label/disclosure, bukan
kebocoran dan bukan kesalahan aritmetika. Tidak ada hambatan atas LULUS.

## 2.8 Catatan batas - DI LUAR LANGKAH 2 (untuk Batch B)

`_build_eda05.py:655` memakai `ACF lag-1 = 0,0018` sebagai salah satu bukti
pendukung klaim H2 "struktur horizon-pendek yang lemah tapi terukur". ACF 0,0018
hampir nol, sehingga tidak dapatcredited sebagai "terukur"; bukti substantifnya
adalah VR 1,0312 dan sign-ACF -0,0226 (yang ada di dict `:662` tetapi tidak
dikutip di teks klaim). **Menilai apakah bukti mendukung klaim H2 adalah tugas
Langkah 4 (H1-H5), yang dilarang disentuh pada batch ini.** Tidak saya laporkan
sebagai temuan; dicatat untuk Batch B.

---

# LANGKAH 3 - LOOK-AHEAD / LEAKAGE

Tiga permukaan yang diuji: (1) pelabelan regime + tipologi, (2) block bootstrap,
(3) agregasi hari-broker.

## 3.1 Permukaan 1 - Pelabelan regime dan tipologi

### Yang benar (terverifikasi, bukan temuan)

- `_build_eda05.py:258` `daily["atr14"] = tr.shift(1).rolling(14).mean()` dengan
  komentar `:256` "tanpa look-ahead: high-low hari t, dirata-rata 14 hari SEBELUM t".
  Metric per-hari tidak menengok hari berikutnya.
- `:260` `ratio_path = |ret_day| / sum_abs_r` - seluruhnya agregat hari yang sama.
- `:249` `daily = d1.set_index("broker_day").join(per_day_m1, how="inner")` -
  kedua sisi agregat hari-t yang sama, join per hari.
- `:270-274` warmup ATR 14 hari dilaporkan/di-assert dan semuanya stratum B.
- `:261-268` label strata berasal dari `DAY_SETS`, yaitu kalender tetap R3, bukan
  statistik yang dihitung dari data.

### [L3-01] HIGH - Ambang tipologi memakai median SELURUH sampel A = look-ahead pada label

- **Lokasi**: `_build_eda05.py:277-278`, diterapkan di `:298-300`.
- **Bukti kode**:
  - `:277` `med_a = daily.loc[daily["strata"] == "A", ["ratio_path", "range_atr"]].median()`
  - `:278` `TH_RATIO, TH_RANGE = float(med_a["ratio_path"]), float(med_a["range_atr"])`
  - `:298-300` threshold tersebut dipakai untuk men-*label* setiap hari valid,
    termasuk hari Wayback 2023-01.
- **Angka terkunci**: output sel 5
  `ambang tipologi (median A, terkunci): ratio_path=0.0268 range_atr=88.7885`.
  Median di atas dihitung dari 825 hari A yang membentang 2023-01 sampai 2026.
- **Analisis**: metrik `ratio_path` dan `range_atr` hari-t sendiri bebas
  look-ahead, tetapi **keanggotaan label `trending`/`range` hari-t bergantung
  pada hari-hari setelah t**. Jadi label bukan fungsi informasi hari-t saja.
  Ini persis bentuk look-ahead yang diminta diuji.
- **Status disclosure - TIDAK ADEQUAT**:
  - `:234` "ambang = median strata A, deterministik setelah dihitung - bukan tuning"
  - `laporan_tahap_11_regime.md:66` "ambang tipologi = median A (deterministik, dinyatakan)"
  - `laporan_tahap_12_sintesis.md:23-28` tidak menyebut look-ahead.
  Tidak satu pun menyatakan bahwa ambang dihitung dari seluruh sampel sehingga
  **tidak dapat dire_real-time**. Kata "deterministik" menyiratkan sifat lain,
  bukan keterbatasan temporal.
- **Kontras yang memperkuat temuan**: coder justru **sadar** dan mengunci
  look-ahead pada metrik (`shift(1)` + label "anti look-ahead" di `:230`, `:256`).
  Disiplin yang sama tidak diterapkan pada ambangnya. Ini bukan kelalaian acak.
- **Kategori**: kebocoran (label hari-t bukan fungsi informasi hari-t).
  Catatan: bila tipologi murni deskriptif (asosiasi, bukan prediksi), dampaknya
  lebih tepat disebut "tidak sesuai rancangan untuk pemakaian real-time" - bukan
  aritmetika salah.tetap tidak ter-disclose di kedua pembacaan.
- **Saran**: hitung ambang dari subset **terbuka** (walk-forward per tahun), atau
  nyatakan eksplisit di `:234`, `:929-935`, `report.md`, dan tahap_11/12 bahwa
  ambang full-sample sehingga label bersifat ex-post dan tidak real-time-safe.

## 3.2 Permukaan 2 - Block bootstrap

### [L3-02] HIGH - Block bootstrap tidak me-resample stratum B sama sekali

- **Lokasi**: `_build_eda05.py:377-391`, khusus `:389`.
- **Bukti kode**:
  - `:380` `b_vals = daily.loc[daily["strata"] == "B", metric].dropna().to_numpy()`
  - `:386-388` indeks block diacak **hanya pada rentang A**:
    `starts = b_rng.integers(0, a_vals.size, size=n_blocks)` lalu
    `idx = ((starts[:, None] + np.arange(n_block)[None, :]) % a_vals.size).ravel()`
  - `:389` `boots[i] = np.median(b_vals) - np.median(a_vals[idx])`
    `b_vals` **tidak pernah diacak**. `np.median(b_vals)` adalah konstanta pada
    seluruh 10.000 resample. Ketidakpastian sampling sisi B **nol**.
- **Bukti empiris dari output sel 7** (menunjukkan efeknya):
  - CI IID yang memang me-resample kedua sisi (`:349-350`):
    `range_atr` `ci95_beda = [-7.02480, 12.58644]` (lebar 19,61)
  - CI block yang di presentersebut "CI95-block":
    `range_atr: beda median B-A CI95-block=[-1.71744, 6.80551]` (lebar 8,52)
  - CI block **2,3x lebih sempit**, dan seluruhnya karena variansi B dibekukan,
    bukan karena block bootstrap lebih baik.
- **Bukan kebocoran antar-strata**: tidak ada kontaminasi A ke B atau B ke A.
  Atresample di dalam A saja. Yang rusak adalah **ketidaklengkapan** resample,
  bukan kontaminasi.
- **Status disclosure - TIDAK ADEQUAT**:
  - `:391` hanya mencetak `CI95-block=[...]` tanpa catatan apa pun.
  - `_build_eda05.py:929-931` menyebut block bootstrap sebagai lapisan kedua
    ketergantungan tanpa menyebut bahwa B tidak di-resample.
  - `report.md:85` menulis "block bootstrap 20-hari x10.000 **konsisten**",
    menyajikannya sebagai pemeriksaan ketahanan yang sahih.
- **Apakah kesimpulan|report.md:85 ikut salah?**: tidak. Kedua CI memuat nol
  (`[-1,72, 6,81]` dan `[-0,00276, 0,00096]`), sehingga "konsisten" tetap benar
  dan CI95 IID yang dikutip memuat nol seperti seharusnya. Yang salah adalah
  **CI block itu sendiri**: ia tidak mengukur apa yang deklarasikan namanya.
- **Kategori**: perhitungannya salah (CI bukan bootstrap beda-median B-A yang
  dideklarasikan) + kejujuran disclosure (disajikan seolah definitif).
- **Saran**: resample `b_vals` dengan blok sepanjang 20 juga
  (`starts_b = b_rng.integers(0, b_vals.size, size=n_blocks_b)`), atau hapus
  label "block bootstrap beda median B-A" dan ganti dengan
  "block bootstrap sisi A saja; B dipegang pada median observasinya - CI
  block-bootstrap satu-sisi lebih sempit dan hanya mengukur sensitivitas A".

### [L3-03] MEDIUM - CI utama berlabel "CI bootstrap" adalah IID, tanpa penanda

- **Lokasi**: `_build_eda05.py:347-352`, header kolom `:361` `ci95_beda`.
- **Bukti kode**:
  - `:349` `sa = rng.choice(a_vals, size=a_vals.size, replace=True)`
  - `:350` `sb = rng.choice(b_vals, size=b_vals.size, replace=True)`
  Resampling **iid per hari**, tanpa blok, tanpa consideration atas urutan
  temporal. Ini mengabaikan volatility clustering sepenuhnya.
- **Status disclosure - PARSIAL**:
  - `:326` "CATATAN CLUSTERING: hari saling bergantung (volatility clustering);
    uji level-hari mengurangi - tidak menghapus - dependensi; block bootstrap
    menyusul bila marginal."
  - `:929-931` mengulanginya di markdown.
  Jadi **dependensi sudah diakui** - ini bukan kebocoran tersembunyi. Yang hilang
  adalah penanda bahwa CI yang dikutip sebagai "CI95" di `report.md:85` adalah
  iid, bukan block. Angka IID `[... , ...]` dan angka block `[..., ...]` muncul
  berdampingan di `report.md:85` tanpa perbedaan jenis yang dinyatakan.
- **Kategori**: kejujuran disclosure (precision), bukan kebocoran tersembunyi.

### [L3-04] LOW - Panjang blok 20 hari di-hardcode tanpajustifikasi dependensi

- **Lokasi**: `_build_eda05.py:381` `n_block = 20`.
- **Analisis**: skema bandul sirkular dengan panjang blok tetap dan urutan di
  dalam blok dipertahankan (`:387` indeks `starts+j` berurutan) adalah
  implementasi moving-block bootstrap yang benar. Karena statistik yang dipakai
  adalah **median** (order-invariant), penempatan blok secara tidak kronologis
  tidak berpengaruh - jadi skema ini **menghormati dependensi temporal** di
  tingkat implementasi.
- Yang tidak ada: alasan atau dasar pemilihan 20 hari, dan uji sensitivitas
  terhadap panjang blok lain. Untuk deret volatilitas FX harian, 20 hari (~4
  minggu) masuk akal, tetapi tidak ada dasarnya di kode maupun markdown.
- **Kategori**: disclosure, severity LOW.

## 3.3 Permukaan 3 - Agregasi hari-broker

### Yang benar (terverifikasi)

- **M15 sudah diperbaiki**: `_build_eda05.py:432-433`
  `m15["wall"] = wall_clock_series(m15["broker_time_raw"])` /
  `m15["broker_day"] = m15["wall"].dt.normalize()` - identik `load_timeframe`
  nb03, dengan alasan migrasi tercatat di `:427-431`.
- **D1 dan M1 sudah benar sejak awal**: `:148-150` dan `:172-173` memakai
  `wall_clock_series` + `dt.normalize()`.
- **DST aman secara konstruksi**: `src/data/broker_time.py:166-175`
  `wall_clock_series(raw) = pd.to_datetime(raw, unit="s")` mengembalikan **jam
  dinding broker sendiri tanpa offset**, sehingga `.dt.normalize()` langsung
  menghasilkan tanggal-broker dan **tidak dapat salah karena DST**. Dokstring
  `:12-15` menyatakan ketujuh transisi 2023-2026 jatuh pada Minggu tanpa bar;
  jadwalnya ada di `configs/data.yaml:23 broker_dst_schedule`. **Tidak ada
  temuan DST** - dan DST bukan penyebab bar yang bergeser di bawah.

### [L3-05] MEDIUM - Jalur M5 masih memakai pemetaan lama yang oleh coder dinyatakan salah

- **Lokasi**: `_build_eda05.py:543`, `:553-560`.
- **Bukti kode**:
  - `:427-431` (komentar M15) menyatakan versi lama **salah**:
    "Versi sebelumnya memakai aproksimasi searchsorted terhadap awal-hari M1;
    itu menggeser bucket pembuka hari yang M1-nya terlambat (mis. 22:07) ke hari
    sebelumnya, sehingga himpunan bar A dan hitungan gap_return tidak identik nb03."
  - M15 diperbaiki di `:432-433`.
  - **M5 tidak diperbaiki**: `:556`
    `idx5_raw = np.searchsorted(starts5, m5["utc"].to_numpy(), side="right") - 1`
    lalu `:559` `m5["broker_day"] = days5[np.maximum(idx5_raw, 0)]`.
    Skema identik dengan yang dinyatakan salah untuk M15.
  - **Akar masalahnya**: `:543` `M5_COLS = ["time", "high", "low"]` - kolom
    `broker_time_raw` **tidak pernah dimuat**, padahal kolom itu tersedia di
    parquet M5 (terverifikasi: `broker_time_raw` ada di
    `data/processed/M5/usdjpy_m5_2023.parquet`) dan justru dibutuhkan
    `wall_clock_series`. Jadi perbaikan M15 secara struktural tidak bisa
    diterapkan ke jalur M5 apa adanya.
- **Bukti empiris (diukur ulang di disk, 269.964 bar M5, 4 tahun)**:
  - Pemetaan eksak `wall_clock_series` vs pemetaan `searchsorted` yang dipakai
    kode: **287 bar berbeda, pada 287 hari** (2023: 113 hari, 2024: 1 hari,
    2026: 173 hari).
  - Polanya persis seperti yang diprediksi komentar `:429`: bar pembuka
    **22:05 UTC** tiap hari terdampak terategorikan ke hari broker sebelumnya.
    Contoh: `2023-01-02 22:05 UTC` -> hari-wall `2023-01-03`, hari-searchsorted
    `2023-01-02`.
  - 114 dari 287 bar tersebut melintasi batas stratum A (masuk atau keluar A).
- **Dampak pada angka yang dilaporkan: NOL.** Dihitung ulang dengan pemetaan
  eksak:
  - kode sekarang (`searchsorted`): 227.567 bar, 825 hari, swings **40.483**,
    49,0703/hari
  - pemetaan eksak (`wall_clock_series`): 227.568 bar, 825 hari, swings **40.483**,
    49,0703/hari
  Kunci `:601` `abs(SWING_PER_DAY_K3 - 49.070) < 0.05` **tetap berlaku** dan
  angka 40.483 yang dilaporkan **benar**. Yang bergeser hanya 1 bar masuk A.
- **Masalah assertion yang memberi rasa aman semu**: `:558`
  `assert n_leading5 == 1` hanya menutupi bar paling depan. Nilai 1 memang benar
  (terverifikasi), tetapi assertion ini **tidak** menutup 287 bar pembuka hari
  yang bergeser, sehingga lulusnya assertion tidak berarti pemetaannya benar.
- **Kategori**: kebocoran/tidak sesuai rancangan - jalur lain masih memakai
  pemetaan lama (persis yang diminta diuji), **bukan** kesalahan aritmetika
  pada angka yang dilaporkan. Tidak ter-disclose di `:929-935` maupun
  `report.md`/`tahap_11`/`tahap_12`.
- **Saran**: tambahkan `broker_time_raw` ke `:543`, pakai
  `wall_clock_series` + `dt.normalize()` seperti M15, dan ganti assertion
  `:558` dengan assertion paritas yang membandingkan hitungan bar M5 per hari
  terhadap pemetaan eksak (pola yang sama denganassertion paritas bar M15 di
  `:444-445`).

## 3.4 Verdict LANGKAH 3: PERLU PERBAIKAN

Dua HIGH (L3-01 look-ahead ambang tipologi yang tidak ter-disclose; L3-02 block
bootstrap tanpa resample sisi B) plus dua MEDIUM (L3-03 penanda CI iid; L3-05
jalur M15 masih memakai pemetaan lama yang dinyatakan salah) dan satu LOW
(L3-04 justifikasi panjang blok). Tidak ada kebocoran yang*"tersembunyi tanpa
disclosure penuh"* pada M15/D1/M1 maupun pada DST - keduanya benar dan
terverifikasi.

---

# VERDICT BATCH A

| Langkah | Verdict |
|---|---|
| LANGKAH 2 - insiden salah-baca ACF | **LULUS** (2 catatan LOW: L2-01, L2-02) |
| LANGKAH 3 - look-ahead / leakage | **PERLU PERBAIKAN** (2 HIGH, 2 MEDIUM, 1 LOW) |
| **BATCH A** | **PERLU PERBAIKAN** |

Ringkasan temuan:

| ID | Severity | Lokasi | Inti |
|---|---|---|---|
| L2-01 | LOW | `report.md:54`, `:56`, nb03 sel 7/11/23 | 0,022639 dan -0,022624 beda 1,5e-5; tidak dapat dibedakan pada 4 desimal - akar insiden |
| L2-02 | LOW | `_build_eda05.py:661` | kunci `acf1_M15_A` tanpa penanda all/no-gap,-lawannya `:662` punya |
| L3-01 | HIGH | `_build_eda05.py:277-278`, `:298-300` | ambang tipologi = median A full-sample; label hari-t bergantung pada hari setelah t; tidak ter-disclose |
| L3-02 | HIGH | `_build_eda05.py:389` | `b_vals` tidak di-resample; CI block 2,3x lebih sempit dari CI iid; disajikan sebagai sahih |
| L3-03 | MEDIUM | `_build_eda05.py:347-352`, `report.md:85` | CI utama iid tanpa penanada "iid" |
| L3-04 | LOW | `_build_eda05.py:381` | panjang blok 20 di-hardcode tanpa justifikasi/sensitivitas |
| L3-05 | MEDIUM | `_build_eda05.py:543`, `:553-560` | jalur M5 masih `searchsorted`; 287 bar bergeser; angka 40.483 tetap benar |

Tidak ada temuan di luar LANGKAH 2-3 yang dilaporkan. Langkah 4-10 tidak
disentuh. Materi lama tidak dibuka.

## SELF-AUDIT 3x (adversarial)

**Putaran 1 - Correctness.** Tiap angka ditelusuri ke sumber primer, bukan ke
ringkasan: 0,001793 / 0,003496 dari sel 7 nb03 (blok M15 A, baris lag 1);
-0,022624 dari sel 11 nb03 (`SIGN_ACF_TABLE`) dan dikonfirmasi ulang oleh sel 21
(`DELTA_ROWS`, kolom `sign_A`) serta sel 23; 1,0337 dari sel 21 nb03
(`vrmean_A`, kode `.loc[2:60].mean()`); 0,022639 dihitung ulang dengan
memindai keenam tabel ACF nb03 (maksimum |acf_no_gap| = 0,022639 pada B M15 lag
50); 49,0703 dihitung ulang dengan menjalankan ulang `fractal_mask` pada kedua
pemetaan; 287 bar M5 diukur ulang dari parquet 4 tahun. Klaim "block bootstrap
tidak me-resample B" dibaca langsung dari `:389` dan dikuatkan oleh selisih lebar
CI iid vs CI block pada output sel 7.

**Putaran 2 - Bias.** Dipertimbangkan apakah L3-01 (ambang median A) dan L3-04
(panjang blok 20) adalah penilaian pilihan metode milik Arsitek, bukan tugas
auditor. Ditolak untuk keduanya: L3-01 dinilai **hanya** atas dasar apakah
disclose atau tidak - kata "deterministik, dinyatakan" di `:234` dan
`laporan_tahap_11_regime.md:66` tidak menyatakan bahwa ambang full-sample dan
tidak real-time-safe; findinya adalah **tidak ter-disclose**, bukan bahwa
medianstrata A adalah ambang yang salah. L3-04 dicatat LOW hanya karena
tidak ada justifikasi tertulis, bukan karena 20 hari adalah pilihan yang keliru.
 Sebaliknya, ditolak secara tegas untuk tidak melaporkan hal-hal di luar scope:
H4 `top6_jam_utc` (`:731-732`) juga dipilih dari mean full-sample, dan `uji_lapisan3`
H4 di `:758` sudah menyebut pengujian out-of-sample - tetapi pemilihan jam bukan
pelabelan regime/tipologi, jadi **tidak** saya laporkan sebagai temuan. Hal sama:
penilaian apakah ACF 0,0018 cukup mendukung klaim H2 (catatan 2.8) sengaja
ditinggalkan untuk Langkah 4.

**Putaran 3 - Meta.** Objek = hanya `scripts/_build_eda05.py`,
`notebooks/scalping/eda_05_regimes.ipynb`, `report.md`, `laporan_tahap_11`,
`laporan_tahap_12` (blob derenoloj `8ac848ce2f7d` / `93ea76955742` /
`72e837778dfc` / `6ab21459e91e` / `eae21308c04d`) plus `src/data/broker_time.py`
dan `configs/data.yaml` hanya untuk memverifikasi `wall_clock_series` dan jadwal
DST. `laporan_tahap_13/14` hanya disebut sebagai "tak berubah" sesuai pernyataan
user, tidak dibaca. Tidak ada satu pun file nb00-nb04, arsip, atau materi lama
(A/B/C, D1-D12) yang dibuka. Langkah 4-10 tidak dijalankan. Tidak ada kode yang
ditulis atau dimodifikasi - satu-satunya file yang berubah adalah dokumen audit ini.
Hash dihitung setelah tulisan final.

---

# STOP - Tunggu perintah Batch B (Langkah 4-6)


---

# RE-AUDIT LANGKAH 3 (putaran 3, 2026-10-06)

Objek: blob baru, seluruhnya diverifikasi ulang dari disk:
`scripts/_build_eda05.py` = `ca997cc9b70a28294dfd663deed17f2b76e8b96f` (44.585 byte),
`notebooks/scalping/eda_05_regimes.ipynb` = `8158d5b57b20e038164b613ab2284194d5c06992`
(71.401 byte), `reports/eda/2026-10-06/report.md` = `2f86eed66ea4fcf3f455b2b23ffabe447b4d0587`,
`laporan_tahap_11_regime.md` = `131e8222a58b781f11593894a4c1fe14a6bc2f0a`,
`laporan_tahap_12_sintesis.md` = `e48c8b321ccdd92d6c08c38ee8612b16bc1cbce9`.

Struktur notebook dihitung ulang: 25 sel / 18 sel kode / **0 output bertipe error** /
`execution_count` `[1..18]` monoton / **59 baris assertion**. Angka 59 yang
diquoted `report.md:15` cocok dengan hitungan independen. Tidak ada regresi
struktur notebook dari putaran sebelumnya.

## 4.1 L3-01 - Verifikasi opsi b (label ex-post, angka tak berubah)

### Pertanyaan yang harus dijawab: cukup, atau tetap perlu opsi a (walk-forward)?

**JAWABAN: OPSI b CUKUP. Tidak perlu opsi a. Verdict LULUS.**

Coder memilih opsi b: mempertahankan ambang full-sample dan **mendisclose bahwa
label bersifat ex-post dan tidak real-time-safe**. Ini persis dua jalan yang saya
terima di temuan saya, dan saya sudah menyatakan sendiri di
L3-01 bahwa mengubah ambang akan "mengubah angka tipologi/chi-square/H1 =
keputusan arsitektur, di luar scope fix". Auditor tidak boleh mengambil
keputusan arsitektur itu. Yang menjadi tugas auditor adalah memastikan
ketidakreal-time-an **ter-disclose**, dan itu kini terpenuhi di lima tempat.

### Bukti disclosure (lima permukaan)

1. **Markdown sel 1 (definisi tipologi)** `_build_eda05.py:237-243`:
   "**Ex-post (temuan audit L3-01, opsi b):** ambang dihitung dari SELURUH 825
   hari A (2023-01-2026, full-sample), sehingga label hari-t memakai informasi
   hari-hari setelah t -> label bersifat ex-post/deskriptif, **TIDAK
   real-time-safe**."
   Kalimat kedua memberi **alasan** opsi a ditolak: "Opsi ambang walk-forward
   per tahun DITOLAK untuk EDA (mengubah angka tipologi/chi-square/H1 =
   keputusan arsitektur, di luar scope fix; rancangan 2/11: EDA deskriptif,
   metode belum dipilih). Identifikasi tipe-hari secara real-time milik uji
   Lapisan 3 (H1: identifikasi H+1 pagi dengan data t-1 saja)."
2. **Print ambang** `:286`:
   `ambang tipologi (median A full-sample 825 hari, ex-post - bukan ambang real-time): ratio_path=... range_atr=...`
   Print ini masuk output sel 5 sehingga terlihat di log eksekusi.
3. **Markdown 5 (Keterbatasan)** `:948-951` butir **"Tipologi ex-post (L3-01,
   opsi b)"**: "ambang = median SELURUH 825 hari A (full-sample) -> label hari-t
   memakai info hari setelah t: deskriptif ex-post, TIDAK real-time-safe.
   Walk-forward per tahun ditolak untuk EDA (mengubah angka = keputusan
   arsitektur); identifikasi real-time milik uji Lapisan 3 (H1)."
4. **`report.md:82`** butir tabel Q7:
   "ambang = median full-sample 825 hari A -> label ex-post/deskriptif, **BUKAN
   ambang real-time** (KOREKSI label pasca-audit L3-01; angka tak berubah)."
5. **`laporan_tahap_11_regime.md:18-19`**:
   "deterministik, bukan tuning; label bersifat ex-post/deskriptif, BUKAN ambang
   real-time (KOREKSI label pasca-audit L3-01 opsi b; angka tak berubah)."
6. **`laporan_tahap_12_sintesis.md:18-20`** (H1): "**Catatan ex-post (L3-01 opsi
   b):** ambang tipologi = median full-sample A -> share di atas deskriptif
   ex-post, bukan hasil klasifikasi real-time; uji Lapisan 3 memakai identifikasi
   H+1 pagi real-time (data t-1 saja), bukan ambang ini."

### Bukti angka tidak berubah (dihitung ulang, bukan diterima)

Hitung ulang dari parquet disk memakai pipeline yang sama persis dengan builder
(`PIP_SIZE = 0.01` dari `configs/data.yaml`, ATR `shift(1).rolling(14)`, median
seluruh 825 hari A):

| Ambang | Nilai output lama (putaran 2) | Hitung ulang baru | Status |
|---|---|---|---|
| `TH_RATIO` | `0.0268` | `0.0268` | tak berubah |
| `TH_RANGE` | `88.7885` | `88.7885` | tak berubah |

Angka turunan di sel 6 juga identik dengan putaran 2 (A trending 278 / normal
268 / range 279; B 45/30/41; C 7/7/5; persen 33,7/32,5/33,8; chi2=2,248
dof=2 p=0,325). Klaim "angka tak berubah" di `report.md:82` dan
`tahap_11:19` **terverifikasi**, bukan sekadar pernyataan.

### Sisa yang masih jujur dan masih ada

`laporan_tahap_11_regime.md:70-71` (self-audit coder) kini menulis "ambang
tipologi = median A full-sample (ex-post/deskriptif, dinyatakan eksplisit -
L3-01 opsi b)". Konsisten.

**Tidak ada temuan baru pada L3-01.**

## 4.2 L3-02 - Verifikasi resample dua sisi

### Bukti kode

- `_build_eda05.py:391` `n_blocks_b = int(np.ceil(b_vals.size / n_block))` -
  **baru ada**, tidak ada di versi lama.
- `:398-400` **baru**:
  `starts_b = b_rng.integers(0, b_vals.size, size=n_blocks_b)` /
  `idx_b = ((starts_b[:, None] + np.arange(n_block)[None, :]) % b_vals.size).ravel()` /
  `idx_b = idx_b[: b_vals.size]`
- `:401` **diperbaiki** dari `np.median(b_vals) - ...` menjadi
  `np.median(b_vals[idx_b]) - np.median(a_vals[idx])`.
  Sisi B kini di-resample blok sepanjang 20 hari dengan pola sirkular yang sama
  seperti sisi A.
- `:384` print header kini menyebut "**KEDUA sisi A dan B di-resample blok -
  KOREKSI L3-02**".
- `:403` label output kini `CI95-block(kedua sisi)`, bukan `CI95-block` polos.

### Replikasi independen dari disk

Saya menulis ulang loop `:394-401` dengan seed 20261006 dan 10.000 resample pada
data parquet, lalu membandingkan dengan angka yang diklaim Coder:

| Metrik | Klaim Coder | Replikasi auditor | Selisih |
|---|---|---|---|
| `range_atr` | `[-7.62542, 13.71568]` | `[-7.62542, 13.71568]` | **0** |
| `ratio_path` | `[-0.00383, 0.00283]` | `[-0.00383, 0.00283]` | **0** |

Kedua CI **terduplikasi digit terakhir**. Klaim Coder benar.

### Apakah cacat substantifnya benar-benar hilang?

Ya. Bandingkan lebar CI (lebar - relevan karena kedua sisi kini diacak):

| Versi | `range_atr` CI | lebar | `ratio_path` CI | lebar |
|---|---|---|---|---|
| CI iid (lapis utama, resample iid) | `[-7.02, 12.59]` | 19,61 | `[-0.0052, 0.0034]` | 0,0086 |
| CI block **lama** (B dibekukan) | `[-1.72, 6.81]` | 8,52 | `[-0.0028, 0.0010]` | 0,0038 |
| CI block **baru** (dua sisi) | `[-7.63, 13.72]` | 21,35 | `[-0.0038, 0.0028]` | 0,0066 |

CI block baru **lebih lebar dari CI iid pada kedua metrik** - justru tanda yang
benar: block bootstrap menghormati clustering sehingga harus lebih lebar dari
IID yang mengabaikan dependensi. Versi lama yang lebih sempit adalah gejalanya.
Interpretasi ini konsisten dengan teori block bootstrap dan cocok dengan arah
perubahan yang terukur.

### Disclosure

- `_build_eda05.py:944-947` markdown 5: "block bootstrap sirkular 20-hari (≈1
  bulan dagang, menutup musiman mingguan) hanya bila hasil marginal, dan
  **me-resample KEDUA sisi A dan B (KOREKSI L3-02)**."
- `report.md:85`: "block bootstrap 20-hari x10.000 **kedua-sisi** memuat 0
  (range/ATR [-7,63, 13,72]; ratio_path [-0,0038, 0,0028]). KOREKSI pasca-audit
  L3-02: CI-block lama satu-sisi-A ([-1,72, 6,81]/[-0,0028, 0,0010]) cacat karena
  B tak di-resample."
- `laporan_tahap_11_regime.md:36`: "Block bootstrap metrik marginal (**kedua
  sisi**) ... **KOREKSI pasca-audit L3-02**: CI lama satu-sisi-A
  [-1,72, 6,81]/[-0,0028, 0,0010] cacat (B tak di-resample)."

Perbaikan ini melampaui yang diminta: angka CI block lama yang cacat **tetap
dinyatakan sebagai superseded** di `report.md:85` dan `tahap_11:36`, sehingga
pembaca lama tidak akan mengutipnya tanpa melihat koreksi. Angka lama yang saya
laporkan di L3-02 sudah tidak lagi Presented sebagai CI yang sahih.

Angka `[-1,72, 6,81]` dan `[-0,0028, 0,0010]` yang dikutip di kedua dokumen
terverifikasi identik dengan output putaran 2 yang saya kutip di L3-02.
Tidak ada satu pun temuan tersisa pada L3-02.

## 4.3 L3-03 - Verifikasi penanda CI iid

### Bukti kode

- `_build_eda05.py:368` kolom **diubah nama** dari `ci95_beda` menjadi
  **`ci95_beda_iid`**. Ini perubahan nama kolom yang membuat jenis bootstrap
  tidak mungkin lagi tidak terbaca di tabel mana pun yang mengimpor kolom itu.
- `:377` print banner tambahan:
  "(kolom `ci95_beda_iid` = bootstrap IID per hari; dependensi temporal diakui -
  lihat CATATAN CLUSTERING)"
- `:944-945` markdown 5: "**CI utama tabel = bootstrap IID per hari (kolom
  `ci95_beda_iid`)**; block bootstrap sirkular 20-hari ... hanya bila hasil
  marginal".
- `:376` header tabel kini memuat kolom `ci95_beda_iid` - terverifikasi di output
  sel 7 yang dicetak ulang.

### Disclosure di dokumen turunan

- `report.md:85`: "**CI95-iid** memuat 0 (range/ATR [-7,02, 12,59]; ratio_path
  [-0,0052, 0,0034]) ... kolom CI utama kini `ci95_beda_iid` (L3-03)".
  Kedua jenis CI kini dibedakan secara eksplisit dalam satu kalimat.
- `laporan_tahap_11_regime.md:34-35` mengutip angka IID sebagai "CI95" (tanpa
  sufiks) - **tetap**. Baris `:36` langsung berikutnya menandai CI block sebagai
  "kedua sisi" dan menyebut koreksi L3-03 di kalimat penutup.
- `laporan_tahap_11_regime.md:20`: "block bootstrap sirkular (block 20 hari,..."

### Penilaian ketat

Huruf kecil yang jujur: `tahap_11:34-35` masih menulis "CI95" polos untuk nilai
iid, sementara `report.md:85` sudah mengatakannya "CI95-iid". Inkonsistensi
kecil ini **tidak** membatalkan temuan: konteks kalimanya sudah jelas (`:36`
membedakan keduanya dan menyebut koreksi L3-03), dan angka iid sendiri sudah
benar. Namun konsistensi label adalah hal yang saya sendiri toleransi
ketika menyoroti L2-01 (proksimit pembulatan antar metrik) - saya tidak bisa
meminta ketelitian label dari laporan tetapi memaafkannya di dokumen lain.

**Catatan LOW baru: [L3-06] label "CI95" tanpa sufiks iid di `tahap_11:34-35`.**
Severity LOW, bukan penahan LULUS, karena: (a) jenis bootstrap dinyatakan benar
di sumbernya (`:368`, `:377`, `:944`), (b) `tahap_11:36` memisahkan kedua jenis
dengan jelas, (c) tidak ada claim yang salah. Disarankan sufiks "-iid" untuk
konsistensi dengan `report.md:85`.

**Tidak ada temuan MEDIUM/HIGH tersisa pada L3-03.**

## 4.4 L3-04 - Verifikasi justifikasi panjang blok

Temuan awal saya adalah: panjang blok 20 di-hardcode **tanpa justifikasi**.
Kode baru menambahkan rujukan dan alasan:

- `_build_eda05.py:384` print header:
  "block 20 hari **≈ 1 bulan dagang, menutup musiman mingguan - Kontrak 00**"
- `:946` markdown 5: "block bootstrap sirkular 20-hari (**≈1 bulan dagang,
  menutup musiman mingguan**)"

### Apakah rujukan "Kontrak 00" akurat terhadap rancangan?

**Ya, dan ini terverifikasi.** `reports/governance/2026-10-06/decisions/eda_design_v3.1.md:69`
mengubah kata blueprint dengan nyaris identik: "block bootstrap sirkular (**block
20 hari dagang ≈ 1 bulan menutup musiman mingguan**, 10.000 resample) `[KD]`" dan
`:115` mengulang "block bootstrap sirkular (block 20 hari dagang, 10.000
resample) hanya bila hasil marginal".

Jadi block 20 + 10.000 resample **bukan pilihan coder**, melainkan parameter yang
ditetapkan rancangan. Rujukan "Kontrak 00" di `:384` **benar**, dan alasan
"≈1 bulan dagang, menutup musiman mingguan" **diambil persis dari teks
rancangan**, bukan karangan. Ini menutup temuan L3-04 sepenuhnya: temuan awal
saya adalah "tidak ada dasar", dan sekarang dasar itu ada serta tertelusur ke
sumber.

Tidak ada temuan tersisa pada L3-04.

## 4.5 L3-05 - Verifikasi perbaikan pemetaan hari M5

Ini adalah temuan dengan bukti empiris terkuat di Batch A, jadi paling diprioritykan
untuk diperiksa ulang.

### Bukti kode

- `_build_eda05.py:555` **`M5_COLS` kini memuat `broker_time_raw`**:
  `["time", "broker_time_raw", "high", "low"]`. Akar masalah yang saya laporkan
  (kolom tidak dimuat) **beres**.
- `:564-569` komentar koreksi mencatat temuan saya dengan angkanya:
  "Pemetaan searchsorted lama terhadap awal-hari M1 **DIHAPUS**: ia menggeser
  **287 bar pembuka-hari (22:05 UTC)** ke hari sebelumnya (terukur: **287
  bar/287 hari; 114 melintasi batas A**). Angka **40.483 tidak berubah**, tetapi
  assertion lama (`n_leading5 == 1`) memberi rasa aman semu sehingga diganti
  paritas absolut di bawah."
  Coder mengutip temuan saya dengan benar dan mengoreksi sub-klausa "rasa aman
  semu" yang saya angkat.
- `:570-571` pemetaan eksak: `m5["wall"] = wall_clock_series(m5["broker_time_raw"])` /
  `m5["broker_day"] = m5["wall"].dt.normalize()` - identik pola M15 (`:444-445`).
- `:558` assertion `n_leading5 == 1` **DIHAPUS** (tidak ada lagi di file).
  Diganti `:576` `assert len(m5_a) == 227_568, "bar M5-A eksak harus 227.568"`
  - assertion paritas **absolut**, pola yang sama dengan assertion paritas bar
  M15 di `:455`.
- `:575` `assert int(m5_a["broker_day"].nunique()) == 825` dipertahankan.
- **Tidak ada lagi `searchsorted` di seluruh file.** Saya grep keyword itu: hanya
  tersisa **dua** kemunculan, keduanya di dalam **komentar** (`:440` menjelaskan
  M15 pernah memakainya, `:565` menjelaskan M5 mengapusnya). Tidak ada satu pun
  pemakaian eksekusi. Jalur agregat lama benar-benar tertutup.

### Replikasi independen dari disk

Saya muat ulang M5 4 tahun dari parquet, bandingkan pemetaan `wall_clock_series`
dengan pemetaan `searchsorted` versi lama, lalu jalankan ulang `fractal_mask`:

| Uji | Nilai | Assertion di kode | Status |
|---|---|---|---|
| `len(m5_a)` | **227.568** | `:576` = 227.568 | LULUS |
| hari M5-A | **825** | `:575` = 825 | LULUS |
| swings k=3 high+low | **40.483** | kunci `abs(SWING_PER_DAY_K3 - 49.070) < 0.05` | LULUS |
| per hari | **49,0703** | 49,070 | LULUS |

Angka `227.568` yang quoted di `:576` **terverifikasi** - ini persis nilai yang
saya hitung independen di Batch A sebagai "pemetaan eksak" (turn 2 menemukan
227.567 untuk pemetaan lama, 227.568 untuk eksak). Assertion paritas baru
mengunci **pemetaan eksak** yang benar.

Angka 40.483 tetap benar, konsisten dengan:yakin Batch A yang sudah
memverifikasi bahwa kedua pemetaan menghasilkan swings identik.

Tidak ada temuan tersisa pada L3-05.

## 4.6 Regresi - apakah ada yang rusak saat memperbaiki?

| Aspek | Status |
|---|---|
| Struktur notebook | 25 sel / 18 kode / 0 error / 59 assertion / exec monoton - sama seperti putaran 2 |
| Angka ACF/VR (sel 9) | `0.001793`, `-0.022624`, `1,0312`, `75,038` - semua masih hadir di sel 9 |
| Angka swing (sel 11) | `40,483` / `49.07` - masih hadir |
| Angka H2 (sel 14) | `0.001793` dan `-0.022624` - masih hadir |
| Angka tipologi (sel 6) | A 278/268/279, chi2 p=0,325 - identik |
| `report.md:15` | blob notebook `8158d5b57b20e` cocok dengan disk; count 59 cocok dengan hitungan independen |
| L2-01 (proksimit 0,0226) | **tidak diubah** - bukan bagian Batch A, masih terbuka sebagai catatan LOW |
| L2-02 (kunci dict) | **diperbaiki** di luar scope: `:675` kini `"acf1_M15_A_all"` (bukan `acf1_M15_A`), `:496` print kini "ACF lag-1 (all)", `:669` teks klaim H2 kini "ACF lag-1 (all)". Ketiganya konsisten. L2-02 tertutup. |

Tidak ada regresi. Perbaikan L3 tidak merusak angka kunci LANGKAH 1.

## 4.7 Status temuan

| ID | Severity lama | Status | Bukti |
|---|---|---|---|
| L3-01 | HIGH | **TERTUTUP** | opsi b adopted; disclosure 6 permukaan; angka `0.0268`/`88.7885` tak berubah (hitung ulang) |
| L3-02 | HIGH | **TERTUTUP** | `:391`, `:398-400`, `:401` resample dua sisi; CI `[-7.62542, 13.71568]` & `[-0.00383, 0.00283]` **terduplikasi digit akhir** |
| L3-03 | MEDIUM | **TERTUTUP** | `:368` kolom `ci95_beda_iid`; `:377` banner; `:944-945` markdown; `report.md:85` "CI95-iid" |
| L3-04 | LOW | **TERTUTUP** | `:384` + `:946` rujukan "Kontrak 00"; `eda_design_v3.1.md:69` & `:115` mengonfirmasi block 20 + 10.000 + alasan musiman mingguan |
| L3-05 | MEDIUM | **TERTUTUP** | `:555` muat `broker_time_raw`; `:570-571` eksak; `:558` dihapus; `:576` paritas 227.568 LULUS; nol `searchsorted` eksekusi |
| **L3-06** | **LOW (baru)** | **TERBUKA** | `laporan_tahap_11_regime.md:34-35` masih "CI95" polos untuk nilai iid, sementara `report.md:85` sudah "CI95-iid" |

## 4.8 Verdict LANGKAH 3 (re-audit): LULUS

Kelima temuan L3-01 s.d L3-05 **tertutup**, masing-masing dengan bukti
`file:baris` plus replikasi independen dari parquet, bukan dengan menerima
pernyataan Coder. Dua di antaranya (L3-02 CI block, L3-05 pemetaan M5) saya
replikasi secara bit-level melalui pengulangan kode sendiri dan hasilnya cocok
digit terakhir.

Terdapat satu catatan LOW baru (L3-06) yang **tidak** menahan LULUS karena
tidak ada klaim yang salah dan jenis bootstrap dinyatakan benar di sumber.

## VERDICT RE-AUDIT LANGKAH 3: LULUS

Tambahan: L2-02 (kunci dict `acf1_M15_A` tanpa penanda all/no-gap) **ikut
tertutup** di putaran ini - kunci menjadi `acf1_M15_A_all` di `:675`, dan print
`:496` serta teks klaim `:669` sama-sama menyebut "(all)". Niat baik coder
melebihi scope.

## SELF-AUDIT 3x (adversarial) - re-audit LANGKAH 3

**Putaran 1 - Correctness.** Tiap angka diverifikasi ulang dari disk:
(1) `TH_RATIO=0.0268` dan `TH_RANGE=88.7885` saya hitung ulang dengan pipeline
yang sama dengan builder termasuk `PIP_SIZE=0.01` dari `configs/data.yaml`
(percobaan pertama saya salah karena lupa membagi dengan pip size dan memberi
0,8879 - hasil itu tidak saya pakai, saya koreksi lalu cocok ke 88,7885);
(2) kedua CI block saya replikasi dengan loop sendiri dan seed 20261006 -
`[-7.62542, 13.71568]` dan `[-0.00383, 0.00283]` cocok digit akhir;
(3) `len(m5_a)=227.568`, hari 825, swings 40.483, per hari 49,0703 - semua
dihitung ulang dari parquet M5 4 tahun; (4) nol pemakaian `searchsorted`
eksekusi - diverifikasi dengan grep terhadap SELURUH file, dua hit adalah
komentar; (5) struktur notebook 25/18/0/59 dihitung ulang; (6) "Kontrak 00"
akurat - diverifikasi terhadap `eda_design_v3.1.md:69` dan `:115`, bukan
diterima secara bulat; (7) angka CI block lama yang masih quoted di `report.md:85` dan
`tahap_11:36` dicocokkan ke output putaran 2 yang saya kutip di L3-02.

**Putaran 2 - Bias.** Dipertimbangkan apakah saya sekarang terlalu longgar karena
menerima opsi b setelah sebelumnya menandainya HIGH. Dicek: temuan L3-01 saya
sendiri sudah menyatakan dua jalan yang saya terima ("perahankan angka tapi
disclose" vs "ubah ke walk-forward"), dan saya tegas menyatakan mengubah ambang
adalah keputusan arsitektur di luar scope auditor. Jadi menerima opsi b **bukan**
melonggarkan standar, melainkan memindahkan standar ke tempat yang benar: saya
menilai disclosure, bukan pilihan ambang. L3-06 saya laporkan meski sedang
memberikan LULUS - tidak ada temuan yang saya sembunyikan demi verdict. L3-04
ditutup karena "Kontrak 00" ternyata benar terhadap teks rancangan; jika rujukan
itu palsu saya akan menolak. Tidak ada temuan baru di luar LANGKAH 3 yang saya
buru - L2-01 sengaja tidak saya periksa ulang kecuali untuk memastikan tidak ada
regresi dari perbaikannya (tidak ada: L2-01 tidak disentuh).

**Putaran 3 - Meta.** Objek = hanya lima file blob baru di atas (verified dengan
`git hash-object`), plus `configs/data.yaml` dan
`reports/governance/2026-10-06/decisions/eda_design_v3.1.md` **hanya** untuk
memverifikasi `PIP_SIZE` dan akurasi rujukan "Kontrak 00" - keduanya pembacaan
terarah untuk verifikasi temuan, bukan audited sebagai objek. Langkah 1 dan 2
tidak diulang (hanya dicek regresi). Langkah 4-10 tidak dijalankan. Materi lama
(A/B/C, D1-D12) tidak dibuka. `laporan_tahap_13/14` tidak dibaca. Tidak ada kode
ditulis atau dimodifikasi - satu-satunya file yang berubah adalah dokumen audit
ini. Hash dihitung setelah tulisan final.

---

# STOP - Tunggu perintah Batch B (Langkah 4-6)
---

# RE-AUDIT BATCH B — LANGKAH 4, 5, 6 (2026-10-07)

Putaran ini adalah **Batch B** dari peta `D:\ANN\.ai\assistant\notes\2026-10-06_peta-langkah-audit_nb05.md`.
Objek dibatasi tegas pada nb05 + lima blob baru. **Langkah 7–10 tidak dijalankan.**
Semua materi audit lama (batch A/B/C, temuan D1–D12, MEDIUM/LOW lama) **tidak dibuka
dan tidak dipakai sebagai bukti**.

## 0. Objek audit & identitas blob

| Peran | Path | git hash-object (SHA-1, 12) | Status |
|---|---|---|---|
| Builder | `D:\ANN\scripts\_build_eda05.py` | `ca997cc9b70a` | 44.585 byte |
| Notebook | `D:\ANN\notebooks\scalping\eda_05_regimes.ipynb` | `8158d5b57b20e` | 71.401 byte |
| Laporan | `D:\ANN\reports\eda\2026-10-06\report.md` | `2f86eed66ea4` | 10.547 byte |
| Tahap 11 | `D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_11_regime.md` | `131e8222a58b` | 93 baris |
| Tahap 12 | `D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_12_sintesis.md` | `e48c8b321ccd` | 102 baris |

> **[Koreksi metadata 2026-10-07]** Judul kolom di atas tadinya `sha256 (12)`. Nilai-
> nilai itu **bukan** SHA-256; semuanya adalah `git hash-object` (SHA-1). Bukti internal
> pada dokumen yang sama, baris 1326: *"verified dengan `git hash-object`"*. Konvensi ini
> dikonfirmasi ulang pada putaran perbaikan (lihat §0 berikutnya): kelima hash baru
> yang diberikan initiator cocok digit demi digit dengan `git hash-object`, sementara
> SHA-256 mentahnya sama sekali berbeda. Ini koreksi **label**, bukan temuan — tidak
> ada perubahan blob yang dituduh.

Rujukan kanonik yang **boleh** dipakai: `D:\ANN\reports\governance\2026-10-06\decisions\eda_design_v3.1.md`
(terutama `:64` M1–M4, `:80` kalender libur, `:69`/`:115` Kontrak 00) dan
`D:\ANN\notebooks\scalping\_eda_common.py` (definisi sesi bersama, yang **diperbolehkan**
karena merupakan dependensi runtime nb05, bukan materi audit lama).

Interpreter yang dipakai untuk replika: `D:\ANN\venv\Scripts\python.exe` (scipy 1.17.1).
`D:\ANN\.venv\Scripts\python.exe` **tidak** memiliki scipy dan tidak boleh dipakai —
catatan ini untuk initiator berikutnya, bukan temuan audit.

---

# LANGKAH 4 — Audit hipotesis H1–H5 (empat sisi)

Empat sisi yang dinilai: **(a) klaim falsifiable? (b) metrik mengukur klaimnya atau proksi
yang melenceng? (c) uji Layer 3 sesuai? (d) ambang yang ditetapkan sebelum hasil dan dapat
dieksekusi?**

## H1 — Regime tipe-hari (`_build_eda05.py:629-661`, `report.md:115`, `laporan_tahap_12_sintesis.md:8-20`)

**(a) Klaim falsifiable — YA.** "Kelanjutan arah pada hari trending layak diuji" +
ambang drift-median CI95 + chi-square antar-tahun.

**(b) Metrik — TIDAK.** Claim yang mendefinisikan `:633-634` hanya mendefinisikan `trending`
("ratio_path dan range/ATR di atas median A") lalu menulis "**vs hari range**" tanpa
mendefinisikan `range`. Definisi sebenarnya ada di `:236`: `range` bila **keduanya ≤ median-A**.
Replika eksak (venv, definisi baris demi baris):

| Tipe | n | mean range/ATR | mean Σ\|r\| | mean ratio_path |
|---|---|---|---|---|
| trending | 278 | **153,1379** | 0,1439 | 0,0571 |
| normal | 268 | 96,9112 | 0,1337 | 0,0280 |
| range | 279 | **61,3183** | 0,1136 | 0,0127 |

Artinya bucket bernama "range" adalah bucket **volatilitas & range TERENDAH**
(2,50× lebih rendah dari trending pada range/ATR), bukan "hari choppy/range lebar".
Labelnya mengajak pembaca melakukan pembacaan yang persis terbalik, dan claim tidak menyebutinya.
Karena `trending` mensyaratkan **dua** metrik di atas median secara simultan (`:305`),
kontras trending-vs-range tercemar level volatilitas: Σ\|r\| sudah 1,27× lebih besar.
Rencana uji `:649-651` ("drift berarah rata-rata M15 4 jam pertama") memakai drift
**absolut dalam pip**, yang skalanya ikut level volatilitas — sehingga tidak memisahkan
"kelanjutan arah" dari "pergerakan lebih besar". → **B4-01**.

**(c) Uji — SECARA STRUKTUR BISA DIJALANKAN** (sign test + bootstrap CI, identifikasi
tipe H+1 dari data t-1). Tidak ada temuan.

**(d) Ambang — SAH & EKSECUTABLE, tidak terpicu.** `:653-655`; hitung ulang
chi-square tipe × tahun (stratum A):

```
        normal  range  trending
2023       40      40        49
2024       92      80        83
2025       83      88        88
2026       53      71        58
chi2 = 4,945  dof = 6  p = 0,55086
```

Ambang `p<0,01` **tidak** terpicu → share dianggap stabil. Ambang ini jujur dan dapat
dihitung ulang. **Bukan temuan** — dicatat sebagai konfirmasi positif.

## H2 — Mikro-momentum M15 (`_build_eda05.py:664-700`, `report.md:57,92-95,116`)

**(a) Klaim falsifiable — YA.**

**(b) Metrik — ANGKA BENAR, KLAIM "TERUKUR" TIDAK DIDUKUNG.** Replika eksak
(fungsi `variance_ratio` baris demi baris + kolom `gap_return` `:453`):

```
n_no_gap = 75.038   (cocok :519)
ACF1(all)          =  0,001793   (cocok 0,001793)
VR(5)/VR(15)/VR(60)= 1,0160 / 1,0119 / 1,0657  -> mean 1,0312  (cocok 1,0312)
sign-ACF1(no-gap)  = -0,022624   (cocok -0,022624)
```

Jadi **seluruh angka H2 benar** — tidak ada temuan aritmetika. Namun klaim `:667-673`
menyebut "struktur horizon-pendek yang lemah tapi **terukur**", dan tidak ada satu pun
uji signifikansi yang menopang kata itu. Hitung ulang:

```
ACF1 = 0,001793 ; SE = 1/sqrt(75.863) = 0,003631 ; z = 0,494 ; CI95 [-0,00532, +0,00891] → memuat 0
VR(5)  z = 0,90  VR(15) z = 0,20  VR(60) z = 0,26   → semua TIDAK signifikan vs iid
Ljung-Box Q(60)/n = 0,001371  vs sigma ACF1 = 0,003631 → z = 0,378, TIDAK signifikan
```

`report.md:55` sendiri menyatakan "p-value BUKAN kesimpulan", jadi posisi "p-value"
bukan argumen yang kuat; masalahnya adalah kata **"terukur"** disandarkan pada statistik yang
seluruhnya tak berbeda dari iid. → **B4-07** (MEDIUM) + pertanyaan untuk Coder
(makna "terukur": signifikansi atau sekadar "terhitung"?).

**(c) Uji — BERSYARAT.** `:687-689` menyebut `cost_basis mean sesi (fragmen 4b)`; nilai
itu memang ada di `configs/data.yaml` (`spread.cost_basis.by_session` =
London 0,61 / NewYork 0,69 / Tokyo 0,62 / Sydney 0,80) dan cocok dengan rerata
`spread_pips` per-bar M1 yang saya hitung (0,6076 / 0,6924 / 0,6151 / 0,7959).
→ **BUKAN temuan** (dependency siap pakai).

**(d) Ambang — TIDAK DAPAT DIJALANKAN.** `:691-694` dan `laporan_tahap_12_sintesis.md:35-36`:
"GUGUR bila EV-after-cost median ≤ 0 di **≥3 dari 4 tahun out-of-sample**".
Span data aktual:

```
broker_day min = 2023-01-02   max = 2026-10-02   → 3,75 tahun kalender
hari per tahun: 2023=259, 2024=260, 2025=259, 2026=196 (tahun berjalan, s/d 2 Oktober)
```

Hanya **3 tahun utuh** (2023–2025) + 1 tahun parsial 196 hari, dan itu pun sebelum
walk-forward membakar in-sample. Empat tahun out-of-sample tidak pernah terbentuk,
sehingga ambang "≥3 dari 4" tidak pernah bisa dievaluasi — hipotesis tidak dapat
digugurkan maupun dipertahankan lewat ambangnya sendiri. → **B4-06** (MEDIUM).

## H3 — Filter regime volatilitas (`_build_eda05.py:701-738`, `report.md:84,117`)

**(a) Klaim falsifiable — YA.** Beda intensitas A-vs-B + detektor real-time.

**(b) Metrik — BENAR, TAPI KONVENSI TANDA TAK DINYATAKAN.** `:351-352` menulis
`mannwhitneyu(a_vals, b_vals)` sehingga δ = P(A>B) − P(B>A). Replika:

```
rv_day      medianA=2,29166e-05  medianB=3,64772e-05  rasio=1,5917  cliff(A-first)=-0,3837  KS p=1,173e-11
sum_abs_r   medianA=0,122087     medianB=0,150529                  cliff=-0,3942  KS p=1,16e-14
range_atr   medianA=88,7885      medianB=91,4027                   cliff=-0,0101  KS p=0,422
ratio_path  medianA=0,0268103    medianB=0,026431                  cliff=+0,0280  KS p=0,635
```

`report.md:84` dan `laporan_tahap_12_sintesis.md:41` menampilkan `δ=−0,384` tepat
di sebelah "RV median B > A", sehingga pembaca wajar menyimpulkan δ negatif =
"B lebih rendah". Justru sebaliknya. Tidak ada satu pun baris di builder/report/tahap
11/12 yang menyatakan konvensi tanda. → **B4-08** (LOW).

**(c) Uji — STRUKTUR BISA DIJALANKAN** (AUC detektor RV rolling). → bukan temuan.

**(d) Ambang — SEBAGIAN TIDAK TERDEFINISI.** `:731-733` / `tahap_12:48-49`:
"AUC ≤ 0,7, ATAU filter memotong >40% hari A **tanpa mengurangi drawdown**".
"Drawdown" tidak dirinci: harian, strategi, atau aset? `report.md:4` menyatakan
"Metode BELUM dipilih", jadi objeknya belum ada. → **B4-11** (LOW, lihat gabung H4/H5).

## H4 — Sesi sebagai alpha (`_build_eda05.py:741-779`, `report.md:118`, `tahap_12:51-64`)

**(a) Klaim falsifiable — YA.**

**(b) Metrik — TIDAK MENGUKUR KLAIM.** Klaim `:756-759`:
"Volatilitas terkonsentrasi di jam-jam sesi **London/NY**". Metrik pendukungnya
`share_Off_di_top6` (`:748`, `:763`) hanya mengukur "di dalam sesi berlabel" — proksi
yang juga terpenuhi penuh oleh Tokyo dan Sydney. Replika komposisi top-6
(`[14, 13, 0, 15, 12, 7]`, identik dengan klaim):

```
jam 14 : London 100,00%
jam 13 : London 100,00%
jam 00 : Tokyo  100,00%   ← di luar London/NY sepenuhnya
jam 15 : NewYork 63,04% · London 36,96%
jam 12 : London 100,00%
jam 07 : London 63,02% · Tokyo 36,98%
share_Off_di_top6 = 0,0000  (klaim 0,0 ✓)
TOTAL London+NewYork = 77,17%   ·   Tokyo+Sydney = 22,83%
```

Jam 00 UTC peringkat ke-3 (mean|r| 1,8148 pip) 100% Tokyo; jam ke-6 (1,7307) hanya 63% London/NY.
`share_Off = 0` benar secara aritmetika tetapi **tidak pernah menguji "London/NY"**.
Sebaliknya `ranking_mean_abs_r` justru **menggugurkan** arah London/NY:
London 1,6658 > Tokyo 1,4393 > **Sydney 1,1962** > NewYork 1,1386, dan
`ranking_sesuai_prior_USDJPY = False` (`:754`, terverifikasi).
`report.md:121` & `tahap_12:58-61` **sudah jujur** membocorkan deviasi ini — jadi
report tidak berbohong; yang berlebihan adalah **teks klaim H4** sendiri. → **B4-02** (MEDIUM).

**(c) Uji — BERSYARAT** (EV-after-cost per jam + stabilitas antar-tahun). → bukan temuan.

**(d) Ambang — BERBEDA DUA TINGKAT DARI KANON M2, DAN ASSERTIONNYA LEBIH LONGGAR.**
Kanon `eda_design_v3.1.md:64` berbunyi: *"M2 — enam jam UTC bervolatilitas tertinggi
harus berada di dalam sesi berlabel, **jika dua jam atau lebih jatuh di Off** maka
batas direvisi [KD]"*. Bandingkan tiga lapis yang ada di nb05:

| Lapis | Kalimat | Toleransi Off |
|---|---|---|
| Kanon M2 (`eda_design_v3.1.md:64`) | "jika **dua jam atau lebih** jatuh di Off maka batas direvisi" | ≥2 Off |
| Klaim H4 (`:757-758`) | "6 jam teratas **harus** di dalam sesi berlabel" | 0 Off |
| Ambang H4 (`:772-773`) | "GUGUR bila **> 1** dari 6 jam teratas jatuh di Off" | ≥2 Off (cocok kanon) |
| Assertion mesin (`:776`) | `assert share_off_top6 < 0.5` | **hingga 2 Off lolos** |

Assertion boleh lolos pada 2 jam Off, padahal M2 menyatakan 2 jam Off sudah memicu
revisi batas → **guard-rail 1 jam lebih longgar dari kriteria preregistrasi**. Dampaknya
hari ini nol (share_Off = 0,0000), jadi angka tidak berubah; yang rusak adalah
*pengaman mesin*. → **B4-03** (MEDIUM).

## H5 — Reaksi level syarat biaya rendah (`_build_eda05.py:782-815`, `report.md:119,123-124`, `tahap_12:66-79`)

**(a) Klaim falsifiable — YA** (ambang CI95/bootstrap day-cluster, seed 20261006).

**(b) Metrik — TIDAK MENGUKUR KLAIM (PELANGGARAN KANON M4).** Kanon
`eda_design_v3.1.md:64` mendefinisikan **M4 = rasio mean|r| terhadap `spread_p95`**.
nb05 memakai mean-spread D1 harian (`_build_eda05.py:532-533`) dan membela diri di
`:543`: *"spread per bar M1 **tidak di skema nb03**; proksi = mean D1 harian"*.
Alasan itu **tidak berlaku untuk nb05** — skema parquet M1 memuat
`spread_points` dan `spread_pips` **per bar** (diverifikasi langsung pada
`usdjpy_m1_2024.parquet`). Konsekuensinya bukan presentasi, tapi angka:

| Sesi | mean\|r\| | spread mean-D1 (**dipakai**) | rasio mean-D1 | spread per-bar | rasio per-bar mean | **spread p95 (kanon M4)** | **rasio p95** |
|---|---|---|---|---|---|---|---|
| London | 1,6658 | 0,6457 | **2,5798** | 0,6076 | 2,7416 | — | **2,0823** |
| Tokyo | 1,4393 | 0,6476 | **2,2225** | 0,6151 | 2,3399 | — | **1,5992** |
| Sydney | 1,1962 | 0,6390 | **1,8720** | 0,7959 | 1,5030 | — | **0,7975** |
| NewYork | 1,1386 | 0,6448 | **1,7658** | 0,6924 | 1,6444 | — | **0,9488** |

Tiga konsekuensi konkret:

1. **Proksi hampir datar.** Rentang spread antar sesi pada proksi D1 hanya
   **0,0086 pip** (0,6390–0,6476), sedangkan spread per-bar sebenarnya
   **0,1883 pip** (0,6076–0,7959) dan `config cost_basis.by_session` 0,19 pip.
   Sekitar 96% variasi spread antar-sesi hilang, sehingga rasio yang dihitung
   **hanya identik dengan ranking mean|r|** — dimensi "spread" pada klaim H5
   praktis tidak terukur sama sekali.
2. **Flag M4 justru tertindih.** `flag_biaya_mendominasi = []` (`:798`, nol sesi
   ter-flag) dicatat di `report.md`/`tahap_12:73-75` sebagai fakta pendukung.
   Dengan spread **p95** sesuai kanon M4, **dua dari empat sesi** ter-flag
   (NewYork 0,9488 dan Sydney 0,7975 < 1). Jadi "tidak terpicu" adalah **artefak
   proksi**, bukan temuan data. → **B4-04** (HIGH).
3. **Urutan sesi berubah.** Proksi D1 memberi urutan London > Tokyo > Sydney > NewYork;
   spread per-bar (mean maupun p95) memberi London > Tokyo > **NewYork > Sydney**.
   Metrik "vol/spread" karena itu tidak unik — dia hanya mengurutkan ulang vol. → ikut **B4-04**.

Tambahan: klaim `:788-789` "hanya dapat dieksploitasi bila biaya rendah relatif
pergerakan", tetapi `flag_biaya_mendominasi = []` berarti **tidak ada satu pun sesi**
dalam data yang punya biaya rendah relatif pergerakan — tidak ada kontras yang
mendukung klausa kondisional tersebut. → **B4-05** (MEDIUM).

**(c) Uji — BERSYARAT** dan justru benar disiplin: `:801-804` mewajibkan protokol
placebo nb04 "PERSIS" + p95 fragmen 4b. → bukan temuan.

**(d) Ambang — SATU-SISI AMBANG, TAPI TERNYATA TEGAS.** `:806-810` gugur bila pada
**setiap** sub-populasi real ≤ placebo (CI95 memuat 0). Ini kriteria falsifikasi
asimetris yang benar (butuh bukti positif agar hipotesis bertahan). → bukan temuan.

Dua catatan kecil pada ambang: (i) H3/H4/H5 merujuk objek yang belum ada —
"tanpa mengurangi drawdown" (H3) dan "EV-after-cost **semua jam**" (H4, jam mana? 24
atau 6 teratas?) → **B4-11**; (ii) `q6_hit_rate_placebo = "0,499-0,505"` (`:796`)
adalah rentang **dirakit dari dua varian berbeda**: 0,499 ≈ titik estimasi
`placebo_acak` (`report.md:73` = 0,4989) sedangkan 0,505 = batas **atas** `placebo_hl`
(0,5050); batas **bawah** `placebo_hl` (0,4890) yang tumpang tindih dengan batas atas
real (0,490) justru dihilangkan, sehingga perbandingan terlihat lebih bersih dari
angka aslinya → **B4-09** (LOW). (iii) `rasio_vol_over_spread_Tokyo = 2,2224`
(`:797`) dipilih sebagai contoh "sesi ber-rasio tinggi" padahal London 2,5798 lebih
tinggi → **B4-10** (LOW).

## B4-12 — M3 preregistrasi tidak pernah dijalankan (MEDIUM)

Kanon `eda_design_v3.1.md:64` M3: *"ranking sesi harus sepakat antara pelabelan
DST-aware dan cross-tab UTC-tetap, jika berbeda maka dilaporkan sebagai sensitivitas
dengan pelabelan DST-aware tetap primer [KD]"*.

`_eda_common.py:96` memang menghitung `session_label_xtab`, tetapi
`grep 'xtab|M3|cross_tab'` pada builder, notebook, `report.md`, tahap 11, tahap 12
→ **0 sel notebook** menyentuh `xtab`; satu-satunya sebutan "cross-tab" di `report.md`
adalah `:139` yang tidak terkait. M3 tidak muncul di laporan mana pun, dan **tidak
juga** masuk daftar 8 item `BELUM DIVERIFIKASI`.

Saya hitung sendiri (bukti independen, agar initiator punya angka):

```
             DST-aware      cross-tab
London         1,6658         1,6516
Tokyo          1,4393         1,4635
Sydney         1,1962         1,1962
NewYork        1,1386         1,0877
urutan ke-4: DST = L,Tokyo,Sydney,NY ; cross-tab = L,Tokyo,Sydney,NY  → SETUJU
top6 jam: [14,13,0,15,12,7] identik ; share_Off = 0,0000 pada keduanya
```

Artinya M3 **akan LULUS**, jadi dampaknya nol terhadap angka — tetapi item
preregistrasi `[KD]` tetap hilang tanpa jejak. Laporan yang MENYATAKAN seluruh
Klaim & Bukti tanpa satu baris M3 adalah celah proses. → **B4-12** (MEDIUM, dampak
angka nol).

## Rekap LANGKAH 4

| ID | Sev | Lokasi | Ringkas |
|---|---|---|---|
| B4-04 | **HIGH** | `_build_eda05.py:532-546,543,785-798` | H5 memakai proksi spread mean-D1 yang **hampir datar** (rentang 0,0086 pip vs 0,1883 pip sebenarnya); kanon `eda_design_v3.1.md:64` M4 menetapkan `spread_p95`. Akibatnya `flag_biaya_mendominasi` nol palsu — dengan p95, **NewYork 0,9488 & Sydney 0,7975 ter-flag**. Alasan pembela `:543` ("spread per bar tidak ada di skema") **tidak berlaku**: M1 punya `spread_pips` per bar. |
| B4-01 | MEDIUM | `:233-236, 632-638, 648-651` | Bucket "range" = **range/ATR TERENDAH** (61,32 vs trending 153,14 = 2,50×); claim tak mendefinisikannya dan kontras trending-vs-range tercemar level volatilitas, sementara uji memakai drift absolut. |
| B4-02 | MEDIUM | `:743-765`, `report.md:118` | `share_Off_di_top6` mengukur "di dalam sesi", bukan "London/NY": 77,17% L+NY, jam 00 UTC 100% Tokyo, jam 07 36,98% Tokyo. `ranking_sesuai_prior_USDJPY=False` juga aktif. |
| B4-03 | MEDIUM | `:776` vs `eda_design_v3.1.md:64` | Assertion `share_off_top6 < 0.5` meloloskan **2 jam** Off; M2 kanon memicu revisi pada ≥2 jam Off. Pengaman 1 jam lebih longgar. |
| B4-05 | MEDIUM | `:545-546, 798`, `tahap_12:73-75` | `flag_biaya_mendominasi = []` → nol sesi punya biaya rendah relatif pergerakan; klausa kondisional "hanya … bila biaya rendah" tanpa kontras pendukung. |
| B4-06 | MEDIUM | `:691-694`, `tahap_12:35-36` | Ambang "≥3 dari 4 tahun OOS" tidak dapat dieksekusi: span 2023-01-02→2026-10-02 = 3,75 tahun; 2026 hanya 196 hari. |
| B4-07 | MEDIUM | `:667-673, 499-508`, `report.md:55` | Klaim "struktur … **terukur**" tanpa uji signifikansi: ACF1 z=0,494; VR z=0,90/0,20/0,26; Ljung-Box z=0,378. Angka H2 sendiri **benar semua**. |
| B4-12 | MEDIUM | `eda_design_v3.1.md:64`, 0 sel nb05 | M3 (DST-aware vs cross-tab) tidak dijalankan/dilaporkan; hitung ulang menunjukkan SETUJU (dampak angka nol). |
| B4-08 | LOW | `:351-352`, `report.md:84` | Konvensi tanda Cliff's delta tak dinyatakan; δ=−0,384 dibaca sebagai "B lebih rendah" padahal A ditulis lebih dulu. |
| B4-09 | LOW | `:790, 795-796`, `report.md:73` | Rentang placebo "0,499-0,505" dirakit dari 2 varian; batas bawah `placebo_hl` 0,4890 (tumpang tindih real 0,490) dihilangkan. |
| B4-10 | LOW | `:785, 797` | Metrik pendukung menyebut Tokyo 2,2224 sebagai "rasio tinggi" padahal London 2,5798. |
| B4-11 | LOW | `:731-733, 771-773` | Ambang H3/H4 merujuk objek belum ada ("drawdown" tanpa strategi; "semua jam" ambigu) saat metode BELUM dipilih. |

**Konfirmasi positif (bukan temuan):** semua angka H1/H2/H3/H4/H5 yang diperiksa ulang
**benar** (0,001793 / 1,0312 / −0,022624 / 75.038 / 40.483 / 88,7885 / 0,026810 /
2,248 / 0,325 / 78.582 / 2,5798 / 2,2225 …); ambang H1 (`chi2 antar-tahun p=0,55086`)
terhitung dan tidak terpicu; M1 kanon (deviasi ranking vs prior S5) dilaporkan
jujur sesuai `eda_design_v3.1.md:64`; label sesi `_eda_common` fingerprint cocok.

---

# LANGKAH 5 — Trace angka `report.md` ke sumbernya

## 5.1 Angka bersumber nb05 (di dalam objek) — semua diverifikasi ulang

| Baris | Angka | Sumber | Hasil replika (venv) |
|---|---|---|---|
| :15 | blob `8158d5b57b20e`, 59 assertion | notebook | 59 assertion, 25 sel/18 kode, 0 error ✓ |
| :17-18 | 1.347.847 / 974 / 825 (1.136.401) / 130 (185.248) / 19 (26.198) | builder `:188-211` | ✓ persis |
| :31 | 78.582 (A 66.817=5,88%; B 10.572=5,71%); total 5,83% | builder | 78.582/1.347.847=5,8302%; A 5,8797%; B 5,7069%; C 1.193=4,5538% ✓ |
| :45 | fragmen `6596adf2…` | `reports/eda/2026-10-06/spread_fragment.yaml` | sha256 `6596adf2969d…` ✓ |
| :45-46 | `cost_basis` (MEAN) + `stress_bands` p95/p99 | `configs/data.yaml` | ✓ keduanya ada; `stress_bands` = p95, p99 |
| :47 | `by_year[2023]=3,0` | `configs/data.yaml` | `spread.by_year.2023 = 3.0` ✓ (blok legacy; `cost_basis.by_year['2023']=0,51` — konsisten dengan komentar interpretasi) |
| :64 | replika nb05 k=3 = 40.483 = 49,07/hari | builder `:553-618` | ✓ (terverifikasi Batch A L3-05) |
| :82 | median 0,0268 / 88,79; share 33,7/32,5/33,8% | builder `:284-322` | 0,026810 / 88,7885; A = 278/268/279 → 33,73/32,48/33,82% ✓ |
| :83 | chi2=2,248 dof=2 p=0,325 (n-B=116) | builder `:326-329` | 2,248 / 2 / 0,325 ✓ |
| :84 | RV 3,648e-5 vs 2,292e-5 (1,59×); δ=−0,384; KS p=1,2e-11; Σ\|r\| beda 0,0284 CI95 [0,0192, 0,0392] | builder `:336-366` | 3,64772e-5 / 2,29166e-5 / 1,5917; δ=−0,3837; KS p=1,173e-11; beda 0,02844; CI95 ✓ (Batch A) |
| :85 | CI95-iid [−7,02, 12,59] / [−0,0052, 0,0034]; CI-block [−7,63, 13,72] / [−0,0038, 0,0028] | builder | ✓ Batch A L3-02/L3-03 (replika ulang saya memakai urutan metrik berbeda sehingga seed bergeser; **angka builder sudah dikunci Batch A** — bukan temuan) |
| :92-93 | VR(5)=1,0160 / VR(15)=1,0119 / VR(60)=1,0657; mean 1,0312; sign-ACF −0,022624; n 75.038 | builder `:462-523` | ✓ persis, metode eksak |
| :115 | share 33,7/32,5/33,8 (trending/normal/range) | notebook sel 13 | ✓ urutan label benar |
| :116 | VR 1,0312; sign-ACF −0,022624 | notebook sel 14 | ✓ |
| :117 | RV 1,59×; δ=−0,384 | notebook sel 7 | ✓ (konvensi tanda → B4-08) |
| :118 | Off=0,0% | notebook sel 16 | 0,0000 ✓ (tetapi lihat **B4-02**) |
| :119 | ambang H5 | builder `:806-810` | ✓ konsisten |
| :121 | Tokyo (1,439) > NewYork (1,139) | notebook sel 10 | 1,4393 / 1,1386 ✓ |
| :123 | proksi spread mean-D1 | builder `:532-543` | ✓ **tetapi lihat B4-04** |
| :128-131 | T-01 diratifikasi | builder | ✓ |
| :149 | paritas 974/974 | builder `:257-259` | ✓ |

## 5.2 Angka bersumber nb00–nb04 — DI LUAR OBJEK audit ini

`:10-14`, `:28-30` (Q1), `:41-43` (Q2/Q3 + D12 + H1-2023), `:54-58` (Q4),
`:64-66` (Q5 + D6/D7), `:72-74` (Q6 BoJ + placebo + Kontrak 00), `:103-107` (tabel
spread p99) seluruhnya berasal dari notebook nb00–nb04, yang **tidak termasuk objek
Batch B**. Saya tidak membukanya.

→ Status: **BELUM DIVERIFIKASI (di luar objek audit ini)** — bukan berarti salah.
→ Pertanyaan untuk Coder: apakah audit LANGKAH 5 Batch B boleh membuka nb01–nb04
  hanya untuk trace angka pasif (read-only, tanpa perubahan), atau angka Q1–Q6 harus
  tetap di luar cakupan dan dicatat sebagai limitasi laporan?

Dua pembanding yang **tetap bisa saya putuskan** karena hanya memakai angka di dalam
objek:

- `report.md:42` "NYSE open jam 13 UTC ×560 (EDT) + jam 14 ×264 (EST)".
  Hitung ulang: marker NY 09:30 ada di **824 dari 825** hari A
  (560 EDT → jam 13 UTC, 264 EST → jam 14 UTC). Angka 560/264 **benar**; totalnya
  memang 824, bukan 825, dan `report.md` tidak mengklaim 825. → **BUKAN temuan.**
- `report.md:42` "Tokyo fix 00:55 UTC ×825 hari" → hitung ulang 825/825 ✓ **BUKAN temuan.**
  (Saya sempat menganggap 560+264 ≠ 825 sebagai temuan; pemeriksaan byte-level
  menunjukkan `report.md` tidak melakukan assert 825 = 560+264. Dicatat di self-audit #3.)

---

# LANGKAH 6 — 8 item `BELUM DIVERIFIKASI` (`report.md:133-142`)

| # | Item | Putusan audit | Dasar |
|---|---|---|---|
| 1 | Angka sekunder S5/S6 | **TETAP BELUM DIVERIFIKASI** — label benar | Angka S5 (London 66 > NY 59 > Tokyo 51 pip) & S6 (London 43%) didefinisikan di `eda_design_v3.1.md:15,32,120` dan diberi label sekunder di `tahap_12:59-61`. Tidak ada sumber eksternal dalam objek. Pertanyaan: apakah perlu rujukan URL/arsip agar "sekunder" dapat diaudit? |
| 2 | Kalender libur NYSE/TSE | **PARTIEL TERPUTUS** — bisa diputus untuk bagian yang dapat, sisanya tetap BELUM | Kapasitas deteksi ada: `_eda_common` `is_ny` + kolom M1. Hasil hitung ulang: **824/825** hari A punya marker NYSE-open 09:30 NY (560 EDT → 13 UTC, 264 EST → 14 UTC). Tepat **1** hari A tanpa marker: **2024-08-12 (Senin)**, 1.364 bar, `tick_volume_sum` 136.001 = **percentile 91,4** (di atas median hari A 77.555) → inferensi "tanpa marker = hari libur" **kontradiktif** untuk kasus ini. Dan 6 hari bervolume terendah di A = 2023-10-18 (17.163), 2023-09-04 (23.520), 2023-07-04 (24.354), 2026-04-03 (27.110), 2026-06-02 (28.792), 2026-05-25 (29.085). **Yang bisa diputus:** daftar hari volume-rendah dapat dihitung deterministik dari data dan 2024-08-12 perlu penjelasan missing-data, bukan dianggap libur. **Yang tetap BELUM:** pencocokan ke kalender libur NYSE/TSE (2023-09-04, 2023-07-04, 2026-05-25, 2026-04-03 terlihat Holiday AS; **2023-10-18 & 2026-06-02 tidak saya pastikan** karena kalender libur bukan objek audit). Pertanyaan: bolehkah kalender libur (sumber eksternal) masuk scope audit, atau item ini ditutup sebagai limitasi permanen `eda_design_v3.1.md:80`? |
| 3 | Offset jendela anomali 2024-10-28 & 2026-03-10 | **TETAP BELUM DIVERIFIKASI** untuk Finex; bagian internal **TERVERIFIKASI** | `configs/data.yaml validation.anomaly_windows` = (2024-10-28→2024-11-01) dan (2026-03-10→2026-03-27) = 5 + 14 = **19 hari**, persis `C = 19` (`builder :200-203`). Jadi offset internal konsisten dengan mask strata. Yang belum: verifikasi ke sumber Finex (di luar objek, `eda_design_v3.1.md:87`). |
| 4 | Atribusi kurtosis M1 pada mikrostruktur | **SALAH LABEL — harus pindah ke hasil negatif** | `report.md:32` memberi status `BELUM DIVERIFIKASI` sementara kolom bukti sendiri berbunyi: *"nb01: atribusi 'microstructure noise' untuk kurtosis **TIDAK didukung Q1**"*. Suatu klaim yang sudah diuji dan **ditolak** adalah temuan negatif, bukan "belum diverifikasi". Ini persis pola yang dilarang peta: label `BELUM DIVERIFIKASI` dipakai untuk menyembunyikan masalah yang sebenarnya sudah bisa diputus. → **B6-04** (MEDIUM). Tidak saya ubah (batch ini read-only pada file sumber); status yang benar: `TIDAK DIDUKUNG / GAGAL`. |
| 5 | Granularitas level .50 & tutup London 16:00 vs 17:00 lokal | **TETAP BELUM DIVERIFIKASI** — label benar & jujur | `eda_design_v3.1.md:90,114` sudah diklasifikasikan sebagai PV ("sisa hal bertanda PV … diuji lewat cross-tab, uji robustness"), dan `report.md:139` menyatakan eksplisit "bukan klaim final". Tidak ada klaim yang bergantung padanya di H1–H5. Bukan temuan. |
| 6 | Seluruh H1–H5 belum diuji | **TETAP BELUM DIVERIFIKASI** — label benar | Benar dan sesuai `report.md:4` ("Metode BELUM dipilih"). Catatan audit: kebenarannya **bergantung pada ambang** — lihat **B4-06** (ambang H2 tidak bisa dieksekusi), sehingga "belum diuji" H2 tidak hanya tertunda, tapi **tidak dapat diuji dengan ambangnya sendiri**. |
| 7 | Daya uji strata B (n=130; 116 untuk ATR) | **TETAP BELUM DIVERIFIKASI** — label benar & sudah ada catatan di output | `n-B tipologi = 116 = 130 − 14 warmup` terverifikasi; `CATATAN DAYA` (`builder :331`) dan `CATATAN CLUSTERING` (`:332-333`) tercetak di output sel #6 dan dikutip `report.md:83`. Bukan temuan. |
| 8 | Proksi spread sesi (mean-D1) | **TERPUTUS — jadi temuan B4-04 (HIGH)** | Bukan lagi "pengukuran final masih di Lapisan 3": (a) M1 **sudah punya** spread per bar (`spread_pips`, `spread_points`) — jadi data final **sudah ada di repo**; (b) `configs/data.yaml` **sudah** memuat angka terukur per sesi (`cost_basis.by_session` 0,61/0,69/0,62/0,80, identik dengan rerata spread per-bar yang saya hitung); (c) `stress_bands` p95/p99 juga sudah ada; (d) kanon `eda_design_v3.1.md:64` M4 justru menetapkan `spread_p95`. Yang **benar-benar** tersisa tinggal p95 per sesi (untuk H5) — itu hanya selisih p95, bukan "semua pengukuran final". Dan dampaknya material: dengan p95, 2 dari 4 sesi ter-flag "biaya-mendominasi" yang terlewat oleh proksi. → **B4-04** |

**Rekap LANGKAH 6:** 5 item tetap BELUM DIVERIFIKASI dengan label yang benar (#1, #3-finex, #5, #6, #7); #2 diputus **sebagian** (memunculkan temuan baru 2024-08-12 + daftar 6 hari volume-rendah, sisanya tetap BELUM); #4 **diputus sebagai salah label** (MEDIUM); #8 **diputus menjadi temuan HIGH** B4-04.

---

# Self-audit 3×

1. **Correctness.** Setiap angka di LANGKAH 4–6 dihitung ulang dari parquet dengan
   `D:\ANN\venv\Scripts\python.exe` (scipy 1.17.1), bukan dibaca dari dokumen. Semua
   definisi ditiru baris demi baris dari `_build_eda05.py` (`:188-211`, `:250-266`,
   `:284-322`, `:336-366`, `:453`, `:462-488`, `:491-522`, `:535-548`, `:741-776`)
   dan `_eda_common.py`. Hash kelima blob dicatat di §0. Yang **tidak** saya klaim: angka
   Q1–Q6 `report.md` (di luar objek, §5.2).

2. **Bias & asumsi.** Tiga hal saya periksa eksplisit:
   (a) **Tidak** saya perlakukan penyimpatan metodologis sebagai bug. Substitusi
   `ratio_path`/`range_atr` saya tulis ulang dan angka saya kembali cocok persis
   (0,026810 / 88,7885 / 278/268/279) → metodologi builder **benar**, temuan saya
   hanya pada **label & kontras**, bukan perhitungan.
   (b) **Tidak** saya laporkan "korusi karakter" — `report.md` dan `_build_eda05.py`
   keduanya `decode utf-8 strict` **OK**, `U+FFFD = 0`. Tampilan U+FFFD yang muncul di
   terminal adalah artefak codepage PowerShell 5.1, bukan isi file. Belum pernah
   saya laporkan sebagai temuan (lihat #3).
   (c) Saya **tidak** memakai materi audit lama sebagai bukti apa pun; satu-satunya
   rujukan lintas dokumen adalah kanon `eda_design_v3.1.md` yang diizinkan peta, dan
   `_eda_common.py` sebagai dependensi runtime nb05.

3. **Meta-check / kalibrasi.** Ada **satu** insidens false-positive yang tertangkap
   sebelum masuk naskah: saya sempat menghitung `560 + 264 = 824 ≠ 825` di
   `report.md:42` dan hampir saya laporkan sebagai temuan. Setelah membaca baris penuhnya,
   `report.md` memang tidak mengklaim 825 untuk NYSE — jadi **bukan temuan**, dan
   dicatat eksplisit di §5.2 agar initiator berikutnya tidak mengulang kekeliruan
   yang sama. Kalibrasi kedua: CI bootstrap yang saya hitung ulang bergeser tipis
   dari `report.md:85` karena urutan metrik saya berbeda sehingga aliran `rng`
   (`seed 20261006`) bergeser — **saya menolak melaporkannya sebagai temuan** karena
   Batch A sudah mengunci angka builder dengan urutan identik. Kalibrasi ketiga:
   interpreter `.venv` tidak punya scipy; setelah saya menemukan hal ini saya pindah ke
   `venv/` dan semua angka di atas dihitung ulang dari nol — **tidak ada temuan yang
   bergantung pada angka dari `.venv`**.

---

# VERDICT BATCH B

- **LANGKAH 4 (H1–H5): GAGAL.** 1 temuan HIGH (B4-04), 7 MEDIUM, 4 LOW.
  Angka H1–H5 sendiri semua benar; yang runtuh adalah **kesesuaian metrik↔klaim**
  (B4-01, B4-02, B4-05, B4-09, B4-10) dan **kelayakan ambang** (B4-03, B4-06,
  B4-07, B4-11). Item preregistrasi M3 hilang tanpa jejak (B4-12).
- **LANGKAH 5 (trace `report.md`): GAGAL.** Seluruh angka bersumber nb05
  (≈20 baris) **terverifikasi ulang tanpa satu pun selisih**. Angka bersumber
  nb00–nb04 **di luar objek** → 1 blok `BELUM DIVERIFIKASI (di luar objek)` +
  1 pertanyaan ke Coder.
- **LANGKAH 6 (8 item): GAGAL.** #4 salah label (MEDIUM), #8 jadi temuan HIGH,
  #2 terputus sebagian; 5 item lain labelnya benar dan dipertahankan.
- **VERDICT BATCH B: GAGAL.** Bagian Lapisan 4–6 belum layak ditutup; 13 temuan baru
  (1 HIGH) harus masuk daftar tindak lanjut, dan `report.md`/tahap 12 tidak boleh
  dianggap "final" tanpa perbaikan minimal pada **B4-04** (proksi spread H5) dan
  **B4-03** (assertion M2) karena keduanya berubah apa yang dibaca pembaca.

## Tindak lanjut untuk Coder (urutan prioritas)

1. **B4-04 (HIGH)** — ganti proksi mean-D1 M4 dengan `spread_pips` per-bar M1 (sudah
   ada) dan p95 sesuai kanon M4; perbarui `rasio_vol_over_spread_*`,
   `flag_biaya_mendominasi`, serta teks H5 di builder/`report.md`/`tahap_12`.
2. **B4-03** — ubah assertion `:776` agar menegakkan M2 kanon (gugur pada ≥2 Off),
   atau tuliskan alasannya bila pelonggaran disengaja.
3. **B4-01, B4-02** — definisikan ulang/rename bucket "range" (atau jelaskan di teks
   klaim), dan ganti `share_Off_di_top6` dengan metrik yang benar-benar menguji
   London/NY.
4. **B4-06** — turunkan ambang H2 dari "≥3 dari 4 tahun OOS" ke bentuk yang dapat
   dieksekusi pada span 3,75 tahun, atau nyatakan eksplisit bahwa ambang menunggu data.
5. **B4-07** — putuskan makna "terukur" (tambah uji signifikansi/CI, atau turunkan kata).
6. **B4-12** — jalankan M3 di nb05 dan laporkan sebagai sensitivitas sesuai
   `eda_design_v3.1.md:64`.
7. **B4-08, B4-09, B4-10, B4-11** — perbaikan redaksional/konvensi di builder + report.
8. **B6-04** — pindahkan `report.md:32` dari `BELUM DIVERIFIKASI` ke `TIDAK DIDUKUNG`.
9. **Jawab 2 pertanyaan** di §5.2 dan §6#1–#2 (cakupan nb01–nb04; kalender libur).
10. **L3-06** tetap utang LOW — **tidak diaudit pada batch ini** sesuai perintah.

## STOP

Batch B selesai pada LANGKAH 4–6 saja. **Langkah 7–10 tidak dijalankan.**
Batch C hanya berjalan atas perintah eksplisit terpisah.
---

# RE-AUDIT BATCH B — PERBAIKAN CODER (LANGKAH 4-6, putaran 2026-10-07)

Putaran ini **hanya** memeriksa apakah 13 temuan Batch B (B4-01…B4-12, B6-04) plus
L3-06 benar-benar tertutup pada lima blob baru. **Langkah 7-10 tidak dijalankan.**
Q1-Q6 dan kalender libur **tetap di luar objek** atas perintah eksplisit initiator.

## 0. Identitas objek baru

| Peran | Path | git hash-object (SHA-1, 12) | SHA-256 (12, pembeda) | Ukuran |
|---|---|---|---|---|
| Builder | `D:\ANN\scripts\_build_eda05.py` | `ba11f0792823` | `ca3cbda1b7c1` | 51.783 byte / 1.132 baris |
| Notebook | `D:\ANN\notebooks\scalping\eda_05_regimes.ipynb` | `2d8f600acade` | `1d33b6023b89` | 82.841 byte / 1.648 baris JSON |
| Laporan | `D:\ANN\reports\eda\2026-10-06\report.md` | `0c361137f15f` | `b1cdd40a7a6e` | 11.985 byte / 157 baris |
| Tahap 11 | `D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_11_regime.md` | `6a89ed49fd37` | `fd9d3fda9b39` | 8.181 byte / 107 baris |
| Tahap 12 | `D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_12_sintesis.md` | `2dfd7bb7dae8` | `9bf3d9d1f48a` | 8.872 byte / 137 baris |

Kelima `git hash-object` **cocok digit demi digit** dengan yang diberikan initiator.
Untuk tahap 12 initiator menulis 13 karakter (`2dfd7bb7dae8f`); 12 karakter pertamanya
adalah `2dfd7bb7dae8`, jadi tidak ada konflik identitas. SHA-256 dicantumkan berdampingan
karena percakapan awal sempat salah menduga hash itu SHA-256 — kini kedua algoritma
ditampilkan supaya initiator berikutnya tidak mengulangi kekeliruan yang sama.

Tidak ada satu pun file sumber yang saya ubah; objek bersifat read-only. Satu-satunya
file yang berubah adalah dokumen audit ini dan `D:\ANN\.ai\STATE.md`.

**Efek samping yang harus disclosed.** Menjalankan notebook berarti sel figures
menjalankan `savefig`, sehingga `reports/eda/2026-10-06/figures/FIG-04.png` sampai
`FIG-07.png` **ditulis ulang di tempat** pada 2026-10-07 02:32:56 (FIG-01..FIG-03 tidak
tersentuh, tetap 2026-10-06 15:49). Keempat file itu adalah output, bukan file sumber,
dan tidak ada di antara lima blob yang diaudit. Isinya deterministik dari notebook yang
sama, dan assertion registry (#66, #67) lulus setelah penulisan ulang. Saya laporkan
supaya tidak ada yang mengira gambar itu tidak pernah ditulis ulang oleh auditor.

**Metode verifikasi.** Notebook **dijalankan sungguhan** dari parquet
(`D:\ANN\venv\Scripts\python.exe`, scipy 1.17.1), bukan hanya dibaca. Hasil: 19 sel kode
+ 7 sel markdown = 26 sel, seluruh sel dieksekusi top-to-bottom **tanpa error**, stdout
120 baris, seluruh assertion lulus. Angka H1-H5, M2/M3/M4, T-01, dan registry figures
diambil dari output eksekusi itu, lalu dicocokkan ulang dengan replika independen dari
parquet yang meniru definisi builder baris demi baris.

---

# LANGKAH 4 — Verifikasi 12 temuan B4 (H1-H5)

| Temuan | Severitas lama | Status | Bukti penutup (semua di blob baru) |
|---|---|---|---|
| B4-04 spread H5 | HIGH | **TUTUP** | `_build_eda05.py:531,539,546-547`; output sel 10; replika |
| B4-01 definisi "range" | MEDIUM | **TUTUP** | `tahap_12:14-15,19-21`; `report.md:115` |
| B4-02 metrik massa | MEDIUM | **TUTUP** | `tahap_12:69-83`; `report.md:118`; output sel 16 |
| B4-03 guard M2 | MEDIUM | **TUTUP** | `_build_eda05.py:853` (assertion #58) |
| B4-05 kontras H5 | MEDIUM | **TUTUP** | `tahap_12:91-95`; `report.md:119` |
| B4-06 ambang H2 | MEDIUM | **TUTUP** | `_build_eda05.py:741-743`; `report.md:116`; `tahap_12:45-49` |
| B4-07 arti "terukur" | MEDIUM | **TUTUP** | `_build_eda05.py:698,711,722-724`; output sel 14; `tahap_12:30-33` |
| B4-12 M3 | MEDIUM | **TUTUP** | `_build_eda05.py:859`; output sel 17; assertion #60-62 |
| B4-08 konvensi delta | LOW | **TUTUP** | `report.md:84,117`; `tahap_12:54-55` |
| B4-09 dua placebo | LOW | **TUTUP** | `tahap_12:96-98`; `report.md:119` |
| B4-10 contoh rasio | LOW | **TUTUP** | `report.md:119`; `tahap_12:102` |
| B4-11 drawdown/6 jam | LOW | **TUTUP** | `report.md:117-118`; `tahap_12:62-65,86-87` |

## 4.1 B4-04 (HIGH) — closure

Kode kanon M4 (`eda_design_v3.1.md:64`, `spread_p95`) kini benar-benar dipakai:

- `_build_eda05.py:539` mengunci `m1_a["spread_pips"].notna().all()` (assertion #41).
- `_build_eda05.py:546-547` menghitung `spread_mean_bar_pips=("spread_pips","mean")`
  dan `spread_p95_bar_pips=("spread_pips", lambda s: float(s.quantile(0.95)))`.
- Rasio memakai p95 per-bar tersebut, bukan rata-rata D1.
- `_build_eda05.py:531` menyatakan proksi mean-D1 lama diganti; kolomnya masih tercetak
  **hanya sebagai pembanding** (`spread_mean_D1_lama_pips`), bukan dipakai klaim,
  persis seperti diminta (lihat `tahap_12:114-116`).

Output eksekusi sel 10 (replika independen dari parquet cocok di semua digit):

| Sesi | n_bar | mean\|r\| | spread mean/bar | **spread p95/bar** | mean-D1 lama | rasio |
|---|---|---|---|---|---|---|
| London | 395.884 | 1,6658 | 0,6076 | **0,8** | 0,6457 | **2,0823** |
| NewYork | 293.134 | 1,1386 | 0,6924 | **1,2** | 0,6448 | **0,9488** |
| Tokyo | 364.696 | 1,4393 | 0,6151 | **0,9** | 0,6476 | **1,5992** |
| Sydney | 82.687 | 1,1962 | 0,7959 | **1,5** | 0,6390 | **0,7975** |

Flag `rasio p95 < 1` = **`['NewYork', 'Sydney']`**, sesuai assertion #46. Cross-check
terhadap `configs/data.yaml cost_basis.by_session` (0,61 / 0,69 / 0,62 / 0,80) cocok
seluruhnya (selisih < 0,02). **B4-04 ditutup.** Tidak ada regresi: angka lama
2,5798/2,2224 tidak lagi muncul di ketiga dokumen yang diaudit.

## 4.2 B4-01, B4-02, B4-03 — closure

- **B4-01.** Bucket "range" kini didefinisikan di teks klaim, bukan hanya di kode:
  `tahap_12:14-15` ("hari TENANG — kedua metrik <= median-A: volatilitas & range
  terendah — bukan 'choppy lebar'") dan `report.md:115`. Uji Lapisan 3 dinaikkan ke
  **drift relatif** ternormalisasi ATR (`tahap_12:19-21`) sehingga tidak lagi terkunci
  pada level volatilitas. Output sel 13: trending 33,7% / range 33,8% / normal 32,5%.
  Catatan: ambang median full-sample A tetap ex-post — itu **L3-01**, sudah ditutup pada
  Batch A lewat disclosure, bukan temuan baru di sini.
- **B4-02.** Metrik yang diuji sekarang benar-benar massa, bukan share jam:
  `share_LondonNY_massa_top6` = 0,7827 dengan definisi tercetak "Sigma |r| pip per sesi
  pada 6 jam teratas" (`tahap_12:70-71`), disertai caveat parsial dan deviasi Tokyo>NY
  (`tahap_12:72-83`). Top-6 = [14, 13, 0, 15, 12, 7].
- **B4-03.** Guard mesin tegas: `_build_eda05.py:853`
  `assert n_off_top6 < 2, "M2 kanon: 2 jam Off atau lebih di top6 memicu revisi batas"`.
  Output: `n_Off_di_top6 = 0`, `share_Off = 0,0`. Assertion lama `share<0,5` hilang.

## 4.3 Angka 78,27% vs 77,17% — diputuskan: BUKAN temuan

Initiator sempat mengira ini kandidat discrepancy. Setelah saya periksa ulang, keduanya
**benar menurut definisi masing-masing**:

| Angka | Definisi | Hitung |
|---|---|---|
| **78,2745%** (baru, dipakai) | massa \|r\| London+NY **dibobot massa** pada 6 jam teratas | 69,4998 + 8,7747 = **78,2745** |
| **77,1700%** (lama, tidak dipakai) | rata-rata **tanpa bobot** dari share 6 jam | (100+100+0+100+100+63,02)/6 = **77,1700** |

Selisih **1,1045** poin persentase murni efek pembobotan. Angka baru justru **lebih
tepat** untuk klaim "konsentrasi volatilitas", karena bobot massa menyatakan berapa
banyak volatilitas benar-benar ada per jam — bukan sekadar hitungan jam mana yang masuk
label. Tidak ada dokumen yang masih mengklaim 77,17 sebagai hasil saat ini.
**Bukan temuan; tidak ada tindakan.**

## 4.4 B4-05, B4-06, B4-07, B4-12 — closure

- **B4-05.** Klausa kondisional H5 kini punya kontras eksplisit (`tahap_12:91-95`):
  Q6 = TIDAK melampaui placebo **secara agregat**, sehingga hipotesis mempersempit ke
  sub-populasi volatilitas tinggi. `report.md:119` memakai bentuk yang sama.
- **B4-06.** Ambang H2 kini dapat dieksekusi pada span 3,75 tahun
  (`_build_eda05.py:741-743`): "GUGUR bila EV-after-cost median <= 0 di 2 dari 3 tahun
  utuh 2023-2025 out-of-sample (2026 parsial 196 hari dikecualikan sebagai tahun
  berjalan; ambang 4 tahun penuh **MENUNGGU DATA**), ATAU rata-rata VR OOS <= 1".
  Ambang 4 tahun juga sudah disclosed, bukan disembunyikan. `report.md:116` dan
  `tahap_12:45-49` sama.
- **B4-07.** Kata "terukur" **diturunkan**. Output sel 14: ACF1 = 0,001793,
  z = 0,494, CI95 [-0,005323, +0,008909] **memuat 0**, `signifikan_vs_iid = False`.
  Assertion #53 mengunci "CI95 ACF1 harus memuat 0", #54 mengunci "z ACF1 harus < 1".
  Teks kini "tak terbedakan dari iid ... SEBAGAI HIPOTESIS EKSPLORATORI".
- **B4-12.** M3 akhirnya dijalankan di nb05 sel 17. Output: urutan DST-aware =
  `['London','Tokyo','Sydney','NewYork']` **identik** dengan cross-tab,
  `share_Off xtab = 0,0000`, sehingga "M3 SENSITIVITAS: SETUJU (DST-aware tetap
  primer)". Tiga assertion (#60, #61, #62) mengunci urutan DST, urutan xtab, dan share
  Off xtab. Artinya M3 kini punya output, bukan lagi klaim preregistrasi tanpa bukti.

## 4.5 B4-08 sampai B4-11 — closure (redaksional, diverifikasi ada di teks)

- **B4-08.** Konvensi tanda dinyatakan eksplisit di tiga permukaan: `report.md:84`
  ("delta = P(A>B) - P(B>A); delta<0 = B cenderung lebih besar"), `report.md:117`,
  `tahap_12:54-55`.
- **B4-09.** Dua varian placebo kini **terpisah**, bukan rentang rakitan
  (`tahap_12:96-98`): `placebo_acak 0,4989 [0,4831-0,5144]` vs
  `placebo_hl 0,4890-0,5050`, dengan interpretasi tumpang-tindih batas bawah hl
  terhadap batas atas real.
- **B4-10.** Contoh sesi ber-rasio tinggi kini **London** (tertinggi), bukan Tokyo:
  `report.md:119`, `tahap_12:102`.
- **B4-11.** Drawdown didefinisikan sebagai max peak-to-trough pada kurva ekuitas
  strategi Lapisan 3 (`report.md:117`, `tahap_12:62-65`); "semua jam" diklarifikasi
  menjadi **6 jam masuk H4**, bukan 24 jam (`report.md:118`, `tahap_12:86-87`).

## 4.6 B6-04 dan L3-06 — closure

- **B6-04 (MEDIUM).** `report.md:32` kini berstatus **`TIDAK DIDUKUNG (temuan negatif)`**
  dengan dasar "nb01: atribusi 'microstructure noise' untuk kurtosis TIDAK didukung Q1 -
  klaim yang sudah diuji dan ditolak, bukan 'belum diverifikasi'". Diperkuat di
  `report.md:139`. Klasifikasi benar.
- **L3-06 (LOW).** Kolom CI utama kini bernama `ci95_beda_iid` (`_build_eda05.py:368`)
  dan disclaimer temporal-clustering tercetak di baris 377 dan 1062: "bootstrap IID per
  hari; dependensi temporal diakui". Suffiks `-iid` muncul di `report.md:84-85`,
  `tahap_11:32-36`, dan `tahap_12` — label tidak lagi menyamar jadi CI bootstrap umum.
  Catatan cakupan: pada Batch B pertama L3-06 sengaja **tidak** diaudit (tindak lanjut
  #10). Putaran ini mengauditnya karena initiator secara eksplisit memasukkan L3-06 ke
  daftar yang harus diverifikasi.

## 4.7 TEMUAN BARU — [B7-01] LOW: jumlah assertion diklaim 68, aktual 67

Ini satu-satunya temuan terbuka pada putaran ini, dan sifatnya dokumenter.

**Fakta terukur (bukan tafsir):**

- Notebook `2d8f600acade`: 19 sel kode, **67** pernyataan `ast.Assert` yang benar-benar
  dieksekusi. Dihitung dengan AST, bukan regex, sehingga tidak salah hitung dari kata
  "assert" yang muncul di dalam string.
- Builder `ba11f0792823`: 67 assertion pada 19 sel kode — **cocok 1:1** dengan
  notebook. Tidak ada assertion yang hilang saat generasi.
- Eksekusi penuh: 67 dari 67 lulus, tanpa error.
- Klaim dokumen: `report.md:15` = **68**; `tahap_11:4` = "**68** assertion PASS";
  `tahap_11:106-107` = "68 (59 + 9 baru, dirinci di header)".
- Rincian `tahap_11:5` menyebut: spread per-bar notna x2, cross-check cost_basis,
  flag M4, CI/z ACF1 x2, guard M2, M3 x3 = **10 item**, bukan 9. Saya konfirmasi
  kesepuluhnya benar-benar ada (assertion #41, #42, #45, #46, #53, #54, #58, #60,
  #61, #62). Jadi "+9" tidak cocok dengan rinciannya (10), dan 59 + 10 = 69 pun tidak
  cocok dengan aktual 67.

**Dampak:** nol pada hasil analitik. Tidak ada angka H1-H5, M2/M3/M4, T-01, atau
figures yang bergantung pada hitungan ini. Yang terdistorsi adalah **provenance** —
`report.md:15` menyatakan 68 assertion lulus, padahal 67 yang lulus.

**Saran perbaikan (bukan tindakan auditor):** set `67` di `report.md:15` dan
`tahap_11:4,106`, lalu ubah "+9" menjadi angka yang cocok dengan basis terverifikasi
(67 - 59 = +8), atau hapus klaim delta dan biarkan enumerasi item sebagai satu-satunya
catatan.

---

# LANGKAH 5 — Trace `report.md` ke sumbernya

## 5.1 Angka bersumber nb05 (di dalam objek) — semua cocok digit demi digit

| # | Angka di `report.md` | Sumber terverifikasi | Status |
|---|---|---|---|
| 1 | share tipe-hari 33,7/32,5/33,8% | output sel 13 | COCOK |
| 2 | ACF1 0,001793 · sign-ACF -0,022624 | output sel 9 | COCOK |
| 3 | VR 1,0312 | output sel 9 | COCOK |
| 4 | RV median B 3,648e-5 vs A 2,292e-5 · rasio 1,59x · delta -0,384 | output sel 7 | COCOK |
| 5 | KS p=1,2e-11 | output sel 7 | COCOK |
| 6 | M4 p95 London 2,08 · Tokyo 1,60 · NY 0,95 · Sydney 0,80 · flag NY+Sydney | output sel 10 | COCOK |
| 7 | cross-check cost_basis < 0,02 | output sel 10 | COCOK |
| 8 | top-6 jam [14,13,0,15,12,7] · Off 0,0 | output sel 16 | COCOK |
| 9 | massa London+NY 0,7827 | output sel 16 | COCOK |
| 10 | z ACF1 0,494 · CI95 memuat 0 | output sel 14 | COCOK |
| 11 | M3 SETUJU | output sel 17 | COCOK |
| 12 | T-01 5,83% (78.582/1.347.847) | output sel 20 | COCOK |
| 13 | CI95-iid range/ATR [-7,02, 12,59] · ratio_path [-0,0052, 0,0034] | output sel 7 | COCOK |
| 14 | registry FIG-01..FIG-07 | output sel 23 | COCOK |
| 15 | blob notebook `2d8f600acade` | `git hash-object` | COCOK |
| 16 | **jumlah assertion 68** | AST: **67** | **B7-01** |

15 dari 16 baris trace bersih. Baris ke-16 gagal dengan selisih **satu** — bukan salah
arah metrik dan bukan angka analitik. Lihat §4.7.

## 5.2 Angka bersumber nb00-nb04 (Q1-Q6) — TETAP DI LUAR OBJEK

Atas perintah eksplisit initiator ("Q1-Q6 + kalender libur tetap di luar objek sampai
user putuskan"), saya **tidak** membuka `eda_01` sampai `eda_04` untuk trace pasif pada
putaran ini, dan **tidak** mengambil sumber kalender libur eksternal. Status semua angka
Q1-Q6 tetap **BELUM DIVERIFIKASI - di luar objek**, sama seperti putaran sebelumnya;
saya tidak menghitungnya sebagai temuan maupun sebagai clearance.

---

# LANGKAH 6 — 8 item `BELUM DIVERIFIKASI` (`report.md:134-145`)

| # | Item | Putaran ini | Dasar |
|---|---|---|---|
| 1 | Angka sekunder S5/S6 | **TETAP BELUM** — label benar | tetap berlabel sekunder; sumber eksternal di luar objek |
| 2 | Kalender libur NYSE/TSE | **TIDAK DIAUDIT** | di luar objek atas perintah initiator; tidak saya putuskan |
| 3 | Offset jendela anomali 2024-10-28 & 2026-03-10 | **TETAP BELUM** untuk Finex | verifikasi Finex tetap di luar objek |
| 4 | Atribusi kurtosis ke mikrostruktur | **TUTUP (B6-04)** | kini `TIDAK DIDUKUNG` di `report.md:32` dan `:139` |
| 5 | Granularitas .50 & tutup London 16:00 vs 17:00 | **TETAP BELUM** — label benar | bukan klaim final; PV di `eda_design_v3.1.md:90,114` |
| 6 | H1-H5 belum diuji | **TETAP BELUM** — label benar | metode belum dipilih (`report.md:4`) |
| 7 | Daya uji strata B (n=130/116) | **TETAP BELUM** — label benar | `CATATAN DAYA` tercetak di output sel 6 |
| 8 | Spread sesi | **TUTUP (B4-04)** | spread p95 per-bar sudah diukur; hanya biaya eksekusi final milik Lapisan 3 |

**Catatan item 6:** pada putaran lalu item ini saya tandai "tidak dapat diuji dengan
ambang-nya sendiri" karena B4-06. Karena B4-06 kini tertutup, catatan itu **dicabut** —
H2 punya ambang yang dapat dieksekusi, dan "belum diuji" murni karena urutan kerja
(metode belum dipilih), bukan cacat dokumen.

**Catatan item 2:** pada putaran lalu saya sudah menghitung sebagian (824 dari 825 hari A
punya marker NYSE-open; 2024-08-12 tanpa marker namun tick_volume percentile 91,4).
Hitungan itu **tidak saya ulang dan tidak saya jadikan dasar status baru** pada putaran
ini, karena kalender libur dinyatakan di luar objek. Statusnya tetap sama seperti
putaran lalu: sebagian bisa diputus, pencocokan ke sumber kalender tetap BELUM.

---

# VERDICT RE-AUDIT BATCH B

- **LANGKAH 4: LULUS.** Dua belas temuan B4 **tertutup dengan bukti `file:baris` plus
  output sel eksekusi**, bukan penjelasan naratif. B4-04 yang HIGH sudah diganti ke
  kanon p95 dan angka lengkapnya cocok digit demi digit dengan replika independen.
  Selisih 78,27 vs 77,17 diputuskan bukan temuan. Satu temuan LOW baru (B7-01) muncul,
  tetapi tidak membuka kembali satu pun temuan lama.
- **LANGKAH 5: LULUS DENGAN CATATAN.** 15 dari 16 angka `report.md` yang bersumber nb05
  tertrace bersih ke output sel. Satu baris (jumlah assertion, 68 vs 67) gagal dengan
  selisih **satu** dan harus dikoreksi sebelum dokumen ini dipanggil final. Tidak ada
  angka analitik yang salah.
- **LANGKAH 6: LULUS DENGAN CATATAN.** #4 dan #8 tertutup; #2 tidak diaudit karena di
  luar objek; #1, #3, #5, #6, #7 tetap BELUM DIVERIFIKASI dengan label yang benar.
  Tidak ada item yang salah label lagi.
- **VERDICT RE-AUDIT BATCH B: LULUS DENGAN SISA 1 LOW.** Lapisan 4-6 layak ditutup;
  satu-satunya utang terbuka adalah **B7-01** (jumlah assertion 68 harus menjadi 67),
  perbaikan dokumenter satu kalimat di tiga tempat. Q1-Q6 dan kalender libur tetap
  menunggu keputusan cakupan initiator.

## Self-audit 3x

1. **Correctness.** Angka H1-H5, M2/M3/M4, T-01, registry figures, dan CI-iid diambil
   dari output eksekusi nb05, lalu dicocokkan ulang dengan replika independen dari
   parquet memakai venv kanonik dan definisi builder baris demi baris. B7-01 dihitung
   dengan AST pada builder **dan** notebook, bukan regex, setelah hitungan regex awal
   terlihat tidak stabil. Tidak ada angka yang saya terima dari dokumen tanpa output.
2. **Bias & asumsi.** (a) Saya **tidak** melaporkan selisih pembulatan sebagai temuan:
   selisih 78,27 versus 77,17 saya telusuri sampai ke pembobotan dan menghakimi **bukan
   temuan**, karena keduanya sah menurut definisi masing-masing. (b) Saya **tidak**
   mengarang temuan demi kesan audit yang enak dibaca: angka H1-H5 ternyata sudah benar
   sejak awal, yang runtuh di Batch B pertama hanya label dan kontras, dan itu sudah
   diperbaiki. (c) B7-01 saya laporkan meskipun verdict LULUS.
3. **Meta-check.** Satu insidens false-positive tertangkap sebelum masuk naskah: saya
   sempat menduga count 67 versus 68 sebagai "assertion hilang saat generasi builder ke
   notebook", tetapi setelah mencocokkan per sel ternyata keduanya identik 67. Penyebabnya
   adalah dokumentasi, bukan generasi — dan itu saya rumuskan sebagai B7-01 LOW, bukan
   HIGH "assertion hilang".

## STOP

Batch B selesai. **Langkah 7-10 tidak dijalankan.** Batch C hanya berjalan atas perintah
eksplisit terpisah.

---

# TRACE Q1-Q6 READ-ONLY + PENUTUPAN ITEM KALENDER (2026-10-07)

Putusan arsitek yang menjadi dasar bagian ini: (Q1) trace **pasif** angka Q1-Q6
yang sebelumnya dinyatakan di luar objek **diizinkan dengan batas**, dan (Q2) item
kalender libur #2 **ditutup sebagai limitasi permanen**.

## A. Batas yang dipatuhi

- **Read-only mutlak** atas `eda_00_setup.ipynb` sampai `eda_04_swings_levels.ipynb`.
  Metode hanya `json.loads` + `ast.parse` + pembacaan output tersimpan. **Tidak ada**
  `nbconvert --execute`, tidak ada penulisan notebook, tidak ada audit ulang sumber.
  Bukti: `git hash-object` keempat notebook identik dengan klaim `report.md:11-14`
  setelah trace, dan `git status --porcelain` kosong untuk kelima notebook.
- **Daftar tertutup.** Hanya angka pada `report.md:10-14`, `:28-30`, `:41-43`,
  `:54-58`, `:64-66`, `:72-74`, `:103-107`. Tidak ada angka lain yang disentrakkan.
- **Hasil akhir hanya di dokumen ini.** Mismatch dicatat sebagai "klaim tak tertrace"
  pada audit nb05, **bukan** dengan membuka ulang audit nb01-nb04.
- **Tanpa atribusi nama libur.** Item kalender ditutup dengan fakta in-data saja.
- Tidak ada satu pun file sumber (notebook, builder, config, `report.md`) yang
  ditulis ulang pada putaran ini. Koreksi dokumen saya ajukan sebagai saran,
  bukan pekerjaan yang saya jalankan sendiri.

## B. Metode dan identitas sumber

Notasi "sel N" = indeks sel `code` **0-based** pada `cells` JSON, sama dengan
konvensi yang dipakai untuk nb05.

| Notebook | `git hash-object` (12) | Klaim `report.md` | Konvensi hitung "N/N" | Sel ringkasan |
|---|---|---|---|---|
| `eda_00_setup.ipynb` | `87318ba7e3ff` | `(preregistrasi Kontrak 00)`, `11/11` | 11 baris PASS + `RINGKASAN: 11/11 audit PASS` | sel 16 |
| `eda_01_returns.ipynb` | `ec448a593c1b` | `23/23` Q1 | `len(checks) = 23` | sel 19 |
| `eda_02_volatility.ipynb` | `8ff4358d4175` | `30/30` Q2/Q3/spread | `len(checks) = 30` | sel 25 |
| `eda_03_autocorr.ipynb` | `0158ca994db9` | `31/31` Q4 | `len(checks) = 31` | sel 23 |
| `eda_04_swings_levels.ipynb` | `4ac4566f5f6c` | `30/30` Q5/Q6/placebo | `len(checks) = 30` | sel 19 |

**Catatan metode yang sering disalahpahami:** nb01-nb04 menghitung "N/N" dari list
bernama `checks` yang dicetak per item sebagai `PASS ...`. Jumlah bare `ast.Assert`
di file itu hanya 8/10/10/8 dan **bukan** angka yang diklaim. Jadi verifikasi angka
23/30/31/30 adalah verifikasi list `checks`, bukan verifikasi `assert`.
Tidak ada `output_type: error` di kelima notebook.

## C. Hasil trace per blok daftar tertutup

### C1. `report.md:10-14` - identitas dan assertion count - TERVERIFIKASI

| Klaim | Sumber stored | Status |
|---|---|---|
| nb00 `11/11` | sel 16: 11 baris `PASS` (strata A/B/C = 1.136.401/185.248/26.198, A+B+C = 1.347.847, C window 6.899+19.299, H1-2023 = 130 hari, 2025 bersih, tzdata 2026.5, D1 2024 = 260 bucket, protokol placebo Q6 + seed terkunci) dan `RINGKASAN: 11/11 audit PASS; strata & definisi terkunci.` | TERVERIFIKASI |
| nb01 `ec448a593c1b` + `23/23` | `git hash-object` = `ec448a593c1b835fabe1aca363c97004481894df`; sel 19 `len(checks) = 23` + `RINGKASAN: 23/23 assertion PASS untuk Q1.` | TERVERIFIKASI |
| nb02 `8ff4358d4175` + `30/30` | `8ff4358d4175457ad9a823aefc3c7e5048e13015`; sel 25 `len(checks) = 30` + `RINGKASAN: 30/30 assertion PASS untuk Q2/Q3/spread.` | TERVERIFIKASI |
| nb03 `0158ca994db9` + `31/31` | `0158ca994db9b335db9bc0c2eddba0ee939d1af0`; sel 23 `len(checks) = 31` + `RINGKASAN: 31/31 assertion PASS untuk Q4 autokorelasi.` | TERVERIFIKASI |
| nb04 `4ac4566f5f6c` + `30/30` | `4ac4566f5f6cc63f07960f04c583602889e51f4b`; sel 19 `len(checks) = 30` + `RINGKASAN: 30/30 assertion PASS untuk Q5/Q6/placebo.` | TERVERIFIKASI |

### C2. Q1 `report.md:28-30` - TERVERIFIKASI dengan 1 koreksi digit (Q-TR-01)

Sumber: nb01 sel 21 (ringkas per TF) dan sel 14 (tabel Q1 + CI bootstrap).

| Klaim | Nilai stored | Status |
|---|---|---|
| kurtosis ekses M1/M5/M15 = `195,5 / 102,8 / 51,2` | sel 21 `kurt_excess=195.476 / 102.848 / 51.176`; tabel sel 14 `1.954764e+02 / 1.028481e+02 / 5.117605e+01` | TERVERIFIKASI |
| sigma = `1,61e-4 / 3,57e-4 / 6,12e-4` | sel 21 `sigma=1.609e-04 / 3.566e-04 / 6.120e-04` | TERVERIFIKASI |
| skew = `-0,74 / -1,46 / -1,23` | sel 21 `skew=-0.744 / -1.456 / -1.225`; nilai penuh sel 14 `-1.224980e+00` | **1 digit terakhir salah** (lihat Q-TR-01) |
| q0,1% M1 = `-9,67e-4` | sel 21 `q0.1%=-9.673e-04`; sel 14 `-9.672903e-04` | TERVERIFIKASI |
| q99,9% M1 = `+9,17e-4` | sel 21 `q99.9%=9.167e-04`; sel 14 `9.166768e-04` | TERVERIFIKASI |
| q0,1% M15 = `-4,04e-3` | sel 21 `-4.043e-03`; sel 14 `-4.042704e-03` | TERVERIFIKASI |
| q99,9% M15 = `+3,50e-3` | sel 21 `3.499e-03`; sel 14 `3.498755e-03` | TERVERIFIKASI |
| CI95 skew B = `[-3,0e-11, 5,6e-11]` | sel 14 `skew B bootstrap 95% CI = [-3.010e-11, 5.615e-11]` | TERVERIFIKASI |

### C3. Q2/Q3 `report.md:41-43` - TERVERIFIKASI dengan 1 koreksi penyebut (Q-TR-02)

| Klaim | Nilai stored | Sumber | Status |
|---|---|---|---|
| `maks M1 = maks M5-max di 17/17 bucket` | tabel D10 = **16** bucket tahun x sesi (2023-2026 x London/NewYork/Tokyo/Sydney), `max_M1 == max_M5max` pada **16/16**; blok agregat 4 sesi juga sama | nb02 sel 17 | **penyebut 17 tak tertrace** (lihat Q-TR-02); properti yang diklaim HOLDS |
| London p99 `1,20 -> 1,40` | sel 17 `p99 M1=1.20 | p99 M5-max=1.40 | maks M1=4.60 | maks M5-max=4.60` | nb02 sel 17 | TERVERIFIKASI |
| NY p99 `2,00 -> 2,80` | sel 17 `p99 M1=2.00 | p99 M5-max=2.80 | maks M1=55.60 | maks M5-max=55.60` | nb02 sel 17 | TERVERIFIKASI |
| Tokyo p99 `1,30 -> 1,50` | sel 17 `p99 M1=1.30 | p99 M5-max=1.50 | maks M1=8.70 | maks M5-max=8.70` | nb02 sel 17 | TERVERIFIKASI |
| Sydney p99 `2,70 -> 3,40` | sel 17 `p99 M1=2.70 | p99 M5-max=3.40 | maks M1=24.10 | maks M5-max=24.10` | nb02 sel 17 | TERVERIFIKASI |
| Tokyo fix `00:55 UTC x 825 hari` | sel 20 jam 0 `n_tokyo_fix = 825`, marker `Tokyo fix 00:55 UTC` | nb02 sel 20 | TERVERIFIKASI |
| NYSE open jam `13 UTC x 560` (EDT) | sel 20 jam 13 `n_nyse_open = 560`, marker `NYSE open (EDT: 13:30 UTC)` | nb02 sel 20 | TERVERIFIKASI |
| NYSE open jam `14 UTC x 264` (EST) | sel 20 jam 14 `n_nyse_open = 264`, marker `NYSE open (EST: 14:30 UTC)` | nb02 sel 20 | TERVERIFIKASI |
| H1-2023 (B) p95/p99/%>3pip = `5,30 / 8,50 / 5,17%` | sel 13 `H1-2023 (B): p95=5.30 p99=8.50 %>3pip=5.1709%` | nb02 sel 13 | TERVERIFIKASI |
| H2-2023 (A) = `0,60 / 1,10 / 0,23%` | sel 13 `H2-2023 (A): p95=0.60 p99=1.10 %>3pip=0.2333%` | nb02 sel 13 | TERVERIFIKASI |
| rasio p95 = `5,30x` | sel 13 `Rasio p95 spread B terhadap A = 5.30x` | nb02 sel 13 | TERVERIFIKASI |

### C4. Q4 `report.md:54-58` - TERVERIFIKASI (dengan catatan definisi)

| Klaim | Nilai stored | Status |
|---|---|---|
| maks `|ACF| = 0,022639` (B M15 lag 50; no-gap) | definisi notebook (source sel 23): `acf_max_abs = max(float(ACF[s][tf]["acf_no_gap"].abs().max()) ...)` -> tercetak `|ACF| maksimum lintas strata/TF = 0.0226 (semua lag 1-60)`; tabel sel 7 blok `ACF M15 (stratum B)` baris lag 50: `acf_all=-0.011704`, **`acf_no_gap=-0.022639`**, `n_no_gap=12395` | TERVERIFIKASI |
| sign-ACF A: `M1 -0,017702 / M5 -0,009805 / M15 -0,022624` | sel 11 dan sel 23: `-0.017702 / -0.009805 / -0.022624` | TERVERIFIKASI |
| sign-ACF B: `-0,013226 / -0,012994 / -0,017336` | sel 11 dan sel 23: `-0.013226 / -0.012994 / -0.017336` | TERVERIFIKASI |
| VR(2-60) A: `0,9796 / 0,9942 / 1,0337` | sel 13 `0.9796 / 0.9942 / 1.0337` | TERVERIFIKASI |
| VR(2-60) B: `0,9848 / 1,0332 / 1,0236` | sel 13 `0.9848 / 1.0332 / 1.0236` | TERVERIFIKASI |

**Catatan definisi (bukan temuan).** Hitung saya atas varian `acf_all` (termasuk
bar dengan gap) mencapai `|0.025524|` pada B M15 lag 29, lebih besar dari
`0,022639`. Angka `0,022639` tetap benar untuk statistik yang didefinisikan
notebook, yaitu varian `acf_no_gap`, dan `report.md:54` menyebut kualifikasi
"no-gap" secara eksplisit. Saya tidak menaikkan ini menjadi temuan, tetapi pembaca
perlu tahu bahwa "maks |ACF|" di naskah berarti maks varian no-gap.

### C5. Q5 `report.md:64-66` - TERVERIFIKASI

Sumber nb04 sel 7 (`=== Q5`, `=== D6`, `=== D7`).

| Klaim | Nilai stored | Status |
|---|---|---|
| k=3 high `20.169` / low `20.314` | sel 7 `3 high 20169`, `3 low 20314` pada kolom `n_swing` | TERVERIFIKASI |
| k=5 `12.787 / 13.070` | sel 7 `5 high 12787`, `5 low 13070` | TERVERIFIKASI |
| gabungan `48,74` swing/hari | sel 7 D6 `gabungan 40207 48.736` | TERVERIFIKASI |
| median harian `49`; p10 `43`; p90 `54` | sel 7 sebaran gabungan: `mean 48.74`, `std 4.18`, `min 37.00`, `10% 43.00`, `50% 49.00`, `90% 54.00`, `max 61.00` | TERVERIFIKASI |
| k=3 `10 bar (50 mnt)` | sel 7 D7 `high_k3 10.0 bar / 50.0 menit` dan `low_k3 10.0 / 50.0` | TERVERIFIKASI |
| k=5 `15 bar (75 mnt)` | sel 7 D7 `high_k5 15.0 / 75.0` dan `low_k5 15.0 / 75.0` | TERVERIFIKASI |
| gabungan `5 bar (25 mnt)` | sel 7 D7 `gabungan 5.0 bar / 25.0 menit` | TERVERIFIKASI |

### C6. Q6 `report.md:72-74` - TERVERIFIKASI dengan 1 koreksi endpoint (Q-TR-03)

| Klaim | Nilai stored | Sumber | Status |
|---|---|---|---|
| touch eksak 150: `728 bar / 53 hari` | `150.0 728 ... 53 ...` | nb04 sel 9 | TERVERIFIKASI |
| touch eksak 155: `518 / 51` | `155.0 518 ... 51 ...` | nb04 sel 9 | TERVERIFIKASI |
| touch eksak 160: `151 / 20` | `160.0 151 ... 20 ...` | nb04 sel 9 | TERVERIFIKASI |
| band 10/25/50 pip pada 150: `3.532 / 8.474 / 16.376` | sel 9 `3532 8474 16376` | nb04 sel 9 | TERVERIFIKASI |
| real `0,469-0,490` | sel 19 tabel `nyata`: `round_xx00 0.4694`, `hl_broker 0.4799`, `round_xx50 0.4892`, `hl_utc 0.4905` -> min 0,4694 max 0,4905 | nb04 sel 19 | TERVERIFIKASI |
| placebo_acak `0,4989 [0,4831-0,5144]` | sel 17 `placebo_acak round_xx00 12 0.4989 0.4831 0.5144 643` | nb04 sel 17 | TERVERIFIKASI |
| placebo_hl `0,4890-0,5050` | sel 19 kolom `placebo_hl`: `hl_broker 0.4922`, `hl_utc 0.4890` -> rentang sebenarnya **0,4890-0,4922**; nilai `0.5050` ada di kolom `placebo_acak` untuk `hl_broker` | nb04 sel 19 | **endpoint atas salah label** (lihat Q-TR-03) |
| seed `20261006` | sel 3 `PLACEBO_SEED : 20261006`; sel 19 `PASS Seed placebo == 20261006` | nb04 sel 3, 19 | TERVERIFIKASI |

### C7. Tabel spread `report.md:103-107` - TERVERIFIKASI

Sumber nb02 sel 17 (blok `Ekor per SESI`) dan sel 13.

| Sesi | Klaim p99 M1 / p99 M5-max / maks | Nilai stored | Status |
|---|---|---|---|
| London | `1,20 / 1,40 / 4,60` | sel 17 `p99 M1=1.20`, `p99 M5-max=1.40`, `maks M1=4.60` | TERVERIFIKASI |
| NewYork | `2,00 / 2,80 / 55,60` | sel 17 `p99 M1=2.00`, `p99 M5-max=2.80`, `maks M1=55.60` | TERVERIFIKASI |
| Tokyo | `1,30 / 1,50 / 8,70` | sel 17 `p99 M1=1.30`, `p99 M5-max=1.50`, `maks M1=8.70` | TERVERIFIKASI |
| Sydney | `2,70 / 3,40 / 24,10` | sel 17 `p99 M1=2.70`, `p99 M5-max=3.40`, `maks M1=24.10` | TERVERIFIKASI |
| H1-2023 (B) | p95 `5,30` / p99 `8,50` / %>3pip `5,17%` | sel 13 `p95=5.30 p99=8.50 %>3pip=5.1709%` | TERVERIFIKASI |

## D. Temuan trace (3)

| ID | Sev | Lokasi | Klaim | Nilai stored | Vonis |
|---|---|---|---|---|---|
| Q-TR-01 | LOW | `report.md:28` | skew M15 `-1,23` | `-1.224980e+00` (nb01 sel 14; sel 21 `skew=-1.225`) | **Klaim tak tertrace pada digit terakhir.** Pembulatan dua desimal yang benar dari `-1,224980` adalah `-1,22`. Kemungkinan besar angka di naskah dibaca dari tampilan tiga desimal `-1.225` lalu dibulatkan lagi. Tidak mengubah tanda, dan tidak mengubah Q1 mana pun: mean-reversion tetap hanya terbaca di tanda, bukan besaran. Perbaikan: satu karakter di `report.md`. |
| Q-TR-02 | MEDIUM | `report.md:41` | `maks M1 = maks M5-max di 17/17 bucket` | tabel D10 tersimpan = **16** bucket tahun x sesi, `max_M1 == max_M5max` pada **16/16**; blok agregat 4 sesi juga sama; assertion nb02 hanya `len(TAIL_M5) >= 12` | **Penyebut tidak tertrace.** Angka "17" tidak ada di output tersimpan nb02 dan tidak ada bucket ke-17 di tabel D10. Properti yang diklaim HOLDS pada seluruh bucket yang ada, sehingga koreksinya hanya penyebut: `16/16`. Saya tidak mengganti angka di `report.md`. |
| Q-TR-03 | MEDIUM | `report.md:73` | `placebo_hl 0,4890-0,5050` | nb04 sel 19: `placebo_hl` = `hl_broker 0.4922` dan `hl_utc 0.4890`; `0.5050` ada di kolom `placebo_acak` untuk `hl_broker` | **Endpoint atas salah label.** Rentang `placebo_hl` yang benar adalah `0,4890-0,4922`. Arah kesalahan: nilai null tampak lebih tinggi dari sebenarnya, sehingga kesimpulan `report.md:73` "level TIDAK terbukti dihormati" justru lebih lemah dari yang seharusnya, bukan lebih kuat. Keterangan dalam tanda kurung pada baris yang sama menyebut "batas bawah hl 0,4890"; `0,4890` adalah **titik estimasi** `hl_utc`, bukan batas bawah CI (batas bawah CI `placebo_hl` = `0,4748` dan `0,4798`). Ketidaktumpang-tindingan yang dimaksud tetap ada karena real max `0,4905` lebih besar dari `0,4890`. |

Ketiganya adalah cacat **dokumenter di `report.md`**, bukan cacat di notebook: pada
ketiga kasus nilai yang benar ada utuh di output tersimpan. Tidak ada klaim Q1-Q6
yang dibatalkan oleh tiga temuan ini, dan tidak ada file sumber yang saya ubah.

## E. Penutupan item kalender libur (Langkah 6 #2) - TUTUP

**Status: TUTUP sebagai limitasi permanen.** Alasannya persis kanon yang sudah
mengatur hal ini di `eda_design_v3.1.md:80`:

> "Kalender libur NYSE/TSE di luar scope EDA (dependensi data baru);
> keterbatasannya dicatat sebagai 'missing event' di laporan - hari bervolume
> rendah terlihat di data tetapi tak teratribusi."

`report.md:137` sudah menjalankan kanon itu ("hari bervolume rendah terlihat tapi
tak teratribusi ('missing event')"), jadi tidak ada status yang menggantung. Syarat
in-data yang dicatat, tanpa atribusi nama libur:

1. **Marker 824/825.** 824 dari 825 hari strata A punya marker NYSE-open 09:30 NY
   (560 hari EDT -> 13 UTC, 264 hari EST -> 14 UTC; nb02 sel 20). Marker Tokyo fix
   penuh 825/825. Konsekuensi: marker yang hilang **tidak boleh** dipakai sebagai
   definisi "hari libur".
2. **Flag missing-data 2024-08-12.** Tepat satu hari A tanpa marker: `2024-08-12`
   (Senin), 1.364 bar M1, `tick_volume_sum` 136.001 = **percentile 91,4**, jauh di
   atas median hari A (77.555). Jadi inferensi "tanpa marker = hari libur"
   kontradiktif untuk kasus ini; perlakukan sebagai **missing-data flag**, sesuai
   aturan missing-data `eda_design_v3.1.md:79`.
3. **Enam hari bervolume terendah di A** (angka deterministik dari data, bukan
   atribusi): `2023-10-18` (17.163), `2023-09-04` (23.520), `2023-07-04` (24.354),
   `2026-04-03` (27.110), `2026-06-02` (28.792), `2026-05-25` (29.085). Tanggal
   dicatat apa adanya. **Saya tidak menyatakan tanggal mana yang hari libur**, dan
   EDA tidak punya dependensi untuk membuktikannya.

Dengan tiga syarat di atas, item #2 ditutup tanpa membuka sumber kalender eksternal
dan tanpa menutupi klaim apa pun. Sisa item Langkah 6 (#1, #3-finex, #5, #6, #7)
**tidak berubah statusnya** dan tetap di luar Batch C ini.

## F. Verdict Langkah 5 (final)

**LULUS DENGAN CATATAN.** Trace pasif Q1-Q6 selesai untuk seluruh daftar tertutup:
tujuh blok, semua angka terpetakan ke `file:sel:nilai`, dengan **3 temuan dokumenter**
(Q-TR-01 LOW, Q-TR-02 MEDIUM, Q-TR-03 MEDIUM) yang seluruhnya berada di `report.md`
dan tidak membatalkan satu pun klaim. Item kalender libur #2 ditutup sebagai
limitasi permanen sesuai `eda_design_v3.1.md:80`.

Yang **tidak** berubah: B7-01 (dokumentasi 68 versus 67 pada nb05) tetap LOW seperti
tertulis; angka di luar daftar tertutup tetap di luar objek; Batch C hanya atas
perintah eksplisit.

Saran tindak lanjut (memerlukan persetujuan, **tidak saya kerjakan**):
(1) `report.md:28` satu digit; (2) `report.md:41` penyebut `17/17` menjadi `16/16`;
(3) `report.md:73` `placebo_hl 0,4890-0,5050` menjadi `0,4890-0,4922`. Ketiganya
satu baris dokumen, tanpa menyentuh notebook.

## G. Self-audit 3 putaran

1. **Kebenaran.** Setiap angka di tabel C diberi pasangan `file:sel` dan nilai
   stored apa adanya. Tiga angka yang semula saya ragukan saya periksa ulang ke
   definisi di source, bukan ke tampilan: (a) `maks |ACF| = 0,022639` saya cek ke
   baris source nb03 sel 23 yang mendefinisikan `acf_no_gap` (bukan `acf_all`),
   sehingga angka `0,025524` yang lebih besar tidak saya laporkan sebagai temuan;
   (b) `17/17 bucket` saya hitung ulang dengan mem-parsing baris tabel D10 yang
   tersimpan dan menghasilkan 16, bukan dengan mengingat-ingat; (c) rentang
   placebo saya baca dari tabel `PERBANDINGAN NYATA vs PLACEBO` sel 19, bukan dari
   tabel CI sel 17, karena keduanya menaruh `0.5050` di tempat berbeda.
2. **Bias.** Saya tidak melaporkan selisih pembulatan sebagai temuan bila keduanya
   sah menurut definisi masing-masing, kecuali Q-TR-01, di mana pembulatan pada
   `report.md` sendiri yang salah dan koreksinya satu karakter, jadi saya laporkan
   sebagai LOW. Saya juga tidak mengarang temuan demi kesan audit yang enak dibaca:
   dari daftar tertutup, **empat blok penuh bersih tanpa koreksi** (`:10-14`,
   `:54-58`, `:64-66`, `:103-107`). Saat membaca output nb02 sel 11 saya melihat
   angka M2/M3 yang berada **di luar daftar tertutup**; saya tidak menelusurinya,
   tidak membandingkannya ke sumber lain, dan tidak membawanya ke dalam naskah ini.
3. **Meta-check.** Read-only dibuktikan dua kali: `git hash-object` keempat notebook
   sama dengan klaim `report.md:11-14` **setelah** trace selesai, dan
   `git status --porcelain` kosong untuk kelima notebook. Tidak ada
   `nbconvert --execute` yang dijalankan pada putaran ini. Efek samping gambar
   FIG-04 sampai FIG-07 berasal dari eksekusi nb05 pada putaran sebelumnya, bukan
   dari trace ini. Semua helper yang saya pakai hanya membaca, dan berada di direktori
   sementara.

## STOP

Trace Q1-Q6 read-only dan penutupan item kalender selesai. Tidak ada file sumber
yang diubah. **Batch C hanya berjalan atas perintah eksplisit terpisah.**
---

# BATCH C — LANGKAH 7, 8, 9, 10 (2026-10-07)

Peran: AUDITOR adversarial. Sumber langkah = peta audit
(`.ai/assistant/notes/2026-10-06_peta-langkah-audit_nb05.md:23-26`):
Langkah 7 = [KLAIM] C4 · Langkah 8 = [KLAIM] bagian "temuan jujur" ·
Langkah 9 = [KLAIM] riwayat iterasi · Langkah 10 = [ATURAN] penuh.

Semua temuan di bawah bertumpu pada enam objek yang sama seperti Batch A/B
(tidak membuka `nb01`-`nb04`, tidak mengulang temuan lama D1–D12/MEDIUM/LOW).

## 0. Identitas objek (verified ulang, bukan diterima)

Dihitung ulang dengan `git hash-object` + SHA-256 pada file yang ada di disk.

| Peran | Path | git hash-object | SHA-256 (12) | Byte | Baris |
|---|---|---|---|---|---|
| Builder | `D:\ANN\scripts\_build_eda05.py` | `ba11f0792823` | `ca3cbda1b7c1` | 51.783 | 1.132 |
| Notebook | `D:\ANN\notebooks\scalping\eda_05_regimes.ipynb` | `2d8f600acade` | `679fb0b5f7c0` | 81.193 | 1.648 |
| Laporan | `D:\ANN\reports\eda\2026-10-06\report.md` | `918f2afa48c5` | `3df0e1325f49` | 12.265 | 157 |
| Tahap 11 | `D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_11_regime.md` | `f012df4f7ec6` | `6922c71911d8` | 8.287 | 107 |
| Tahap 12 | `D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_12_sintesis.md` | `2dfd7bb7dae8` | `9bf3d9d1f48a` | 8.872 | 137 |

### [B8-03] MEDIUM — Tabel identitas `:1819-1825` sudah basi: 2 dari 5 objek berubah setelahnya

Tabel identitas di blok Batch B (`:1819-1825`) tidak lagi menggambarkan file
yang ada. Saya bandingkan klaim sana terhadap disk:

| Peran | sha1 klaim | sha1 aktual | sha256 klaim (12) | sha256 aktual | Byte klaim | Byte aktual | Status |
|---|---|---|---|---|---|---|---|
| Builder | `ba11f0792823` | `ba11f0792823` | `ca3cbda1b7c1` | `ca3cbda1b7c1` | 51.783 | 51.783 | COCOK |
| Notebook | `2d8f600acade` | `2d8f600acade` | `1d33b6023b89` | `679fb0b5f7c0` | 82.841 | 81.193 | **EOL saja** |
| Laporan | `0c361137f15f` | `918f2afa48c5` | `b1cdd40a7a6e` | `3df0e1325f49` | 11.985 | 12.265 | **ISI BERUBAH** |
| Tahap 11 | `6a89ed49fd37` | `f012df4f7ec6` | `fd9d3fda9b39` | `6922c71911d8` | 8.181 | 8.287 | **ISI BERUBAH** |
| Tahap 12 | `2dfd7bb7dae8` | `2dfd7bb7dae8` | `9bf3d9d1f48a` | `9bf3d9d1f48a` | 8.872 | 8.872 | COCOK |

Dua kasus berbeda dan tidak boleh dicampur:

- **Notebook — EOL saja, isi utuh.** `git hash-object` (yang menormalisasi EOL)
  **tidak berubah**; selisih byte −1.648 = **tepat jumlah baris** dan file
  berisi **0 byte CR**. Jadi ini konversi CRLF→LF, bukan perubahan isi.
- **`report.md` & `tahap_11` — isi benar-benar berubah** (+280 dan +106 byte).
  Jejak koreksi yang masuk: `report.md` memuat `Q-TR-03` (1×) dan
  `tahap_11:5` memuat `B7-01` ("68 → 67"). Keduanya adalah koreksi **pasca**
  tabel Batch B.

**Mengapa ini temuan, bukan catatan administratif:** tabel identitas adalah
satu-satunya pengikat bukti audit ini ke file konkret. Kalau pengikatnya salah,
maka setiap "TERVERIFIKASI" di blok Batch B **tidak dapat diaudit ulang** tanpa
menebak blob mana yang dimaksud. Saya sendiri harus menghitung ulang dari nol.
Perbaikan murah (5 angka), dampaknya mahal.

**Severity: MEDIUM.** Bukan HIGH karena dua objek yang berubah (builder,
tahap 12) tetap identik, dan isi notebook terbukti utuh — jadi tidak ada
bukti yang salah *nilai*, hanya pengikat yang salah. Bukan LOW karena tiga
dari lima baris tabel salah dan blok Batch B masih disajikan sebagai
rujukan valid.

### Disclosed — audit ini sendiri berbeda EOL dari baseline initiator

`git hash-object` audit = `c0876a4fa0a8e60ba2d8ba23c9ed7d8633281983`, tetapi
baseline yang diberikan initiator adalah SHA-256
`0d793902d4796f85db6c932f441dcddd3bc05fbf46342979381a17b389a78162`
(146.711 byte / 2.348 baris). File aktual 144.364 byte / 2.348 baris.
Selisih **tepat 2.347 byte** = jumlah carriage-return yang hilang; isi
ternormalisasi identik (hash git sama). Penyebabnya bukan saya dan bukan kode:
seluruh file repo ber-mtime identik `2026-10-07 10:42:00`, termasuk
`configs/data.yaml`, `src/data/broker_time.py`, `pyproject.toml`, `.ai/RULES.md`
— ciri operasi penggantian massal line ending (`git config core.autocrlf` =
`true`). Saya tidak mengembalikan file ke CRLF karena itu akan menimpa objek
dan melanggar aturan append-only.

Satu konsekuensi yang **harus** dibaca bersama B8-03: karena notebook sekarang
0-CR sementara tabel `:1822` mencatat ukuran berbasis CRLF, **perbandingan byte
tidak boleh dipakai sebagai uji integritas** pada repo ini — hanya
`git hash-object` (yang menormalisasi) yang sah.

## LANGKAH 7 — Registry FIG-01..07 + FIG-01..03 tidak tersentuh

### 7.1 Registry tepat FIG-01..07 — TERVERIFIKASI

| Klaim | Sumber | Bukti independen | Status |
|---|---|---|---|
| Notebook mengklaim FIG-04..07 | `report.md:87-89` | 4× `fig.savefig` ke `FIG-04.png` … `FIG-07.png` (`_build_eda05.py:992,1006,1022,1034`) + 4× `FIG-0n.png` yang benar-benar ada di disk | TERVERIFIKASI |
| Assertion registry mengunci 7 file | `_build_eda05.py:1043-1049` | `expected = [f"FIG-{i:02d}.png" for i in range(1,8)]`; `assert registry == expected` | TERVERIFIKASI |
| Assertion benar-benar lulus | output nb05 sel kode 17 (json idx 23) | `registry figures: ['FIG-01.png' … 'FIG-07.png']` + `PASS: registry figures tepat FIG-01..FIG-07` | TERVERIFIKASI |
| Direktori tidak punya figure extra | `laporan_tahap_14_figures.md:12` | `rglob("FIG-*.png")` di seluruh repo = **tepat 7**; tidak ada `FIG-08`+ di mana pun | TERVERIFIKASI |

### 7.2 FIG-01..03 tidak tersentuh — TERVERIFIKASI (hash), dengan catatan mtime

| File | git hash-object worktree | git hash-object `HEAD:` | Identik | Ukuran | Dimensi IHDR |
|---|---|---|---|---|---|
| `FIG-01.png` | `709db8ae0d64` | `709db8ae0d64` | **YA** | 28.695 B | 720×720 |
| `FIG-02.png` | `e55fc1f5294b` | `e55fc1f5294b` | **YA** | 31.344 B | 720×720 |
| `FIG-03.png` | `73d65368398b` | `73d65368398b` | **YA** | 32.883 B | 720×720 |

`git status --porcelain -- reports/eda/2026-10-06/figures` hanya memunculkan
`?? FIG-04.png` … `?? FIG-07.png`. FIG-01..03 **tidak muncul** = tidak ada
perubahan terhadap `HEAD` (`a826ef8`, 2026-10-06 19:00:18). Meaning: isi ketiga
file byte-identik dengan versi yang di-commit sebelum nb05 ada.

Hash FIG-04..07 juga saya hitung ulang dan cocok digit demi digit dengan blok
`laporan_tahap_14_figures.md:19-27` (`3420bca32643`/`fedd896ff8a2`/`124867c6620c`/
`a90a16b0e40d`, ukuran `31927`/`27778`/`21101`/`23351`). Dimensi PNG saya baca
langsung dari byte IHDR: FIG-04/05/06 = 840×540, FIG-07 = 960×540 — sesuai
`figsize=(7,4.5)` dan `(8,4.5)` @ dpi 120 di `_build_eda05.py:977,997,1012,1027`.

### 7.3 [B8-01] LOW — Bukti "mtime tetap 15:49:27" sudah tidak dapat diuji

**File:baris** — `reports/eda/progress/06-regimes/laporan_tahap_14_figures.md:13`
("mtime tetap 15:49:27") dan blok yang sama `:20-22` (baris `15:49:27` ×3).

**Bukti.** Ketujuh PNG sekarang ber-mtime identik `2026-10-07 10:42:00`. Pola
yang sama berlaku untuk file non-figure (`configs/data.yaml`,
`src/data/broker_time.py`, `pyproject.toml`, `.ai/RULES.md`, `.ai/STATE.md`
semuanya `10:42:00`). Jadi kludik mtime "tetap" sudah **tidak dapat dibuktikan
atau disangkal** lagi — ia dinetralkan oleh operasi massal, bukan oleh tindakan
nb05. Yang masih berdiri kokoh adalah jalur hash (§7.2), dan jalur hash sudah
cukup untuk substansi klaim ("isi FIG-01..03 tidak berubah").

**Severity: LOW.** Tidak ada angka klaim yang salah; hanya salah satu dari dua
bukti pendukung yang jadi tidak dapat diulang. Saya **tidak** menaikkan ini ke
MEDIUM karena klaimnya sendiri ("tidak tersentuh rerun nb05") tetap terbukti
melalui `git hash-object`.

### 7.4 One-figure-one-message — TERVERIFIKASI

`FIG-04` range/ATR A-vs-B, `FIG-05` RV harian log10, `FIG-06` proporsi tipe hari
per strata, `FIG-07` mean|r| per jam UTC. Masing-masing satu `fig, axis =
plt.subplots()` tunggal di `_build_eda05.py:977,997,1012,1027`; tidak ada figure
komposit, dan setiap `fig.savefig(..., dpi=120)` tepat satu (`_build_eda05.py:992,
1006, 1022, 1034`). `report.md:87-89` menyebut keempatnya dengan pesan yang sama.

Tidak ada figure yang menampilkan inferensi sinyal atau P&L — saya periksa label
sumbu langsung dari builder, bukan dari laporan: sumbu-y hanya `densitas`
(`:988`, `:1002`), `% hari` (`:1018`), dan `mean |r| (pip/bar)` (`:1031`); tidak
ada satu pun label sumbu berisi P&L, equity, atau profit.

### 7.5 Verdict LANGKAH 7: **LULUS** (1 catatan LOW B8-01, 1 catatan MEDIUM B8-03)

---

## LANGKAH 8 — Tiga temuan jujur

Saya menguji **kejujuran** disclosure, bukan pilihan metode (§C prompt: "tidak
salah menilai kualitas metode sebagai pilihan arsitektur").

### 8.1 Temuan jujur (a) — deviasi ranking sesi terhadap prior S5

**Klaim** (`report.md:121-122`, `laporan_tahap_12_sintesis.md:78-83`):
ranking empiris mean|r| = **London 1,666 > Tokyo 1,439 > Sydney 1,196 >
NewYork 1,139**; berbeda dari prior sekunder S5 (London 66 > NY 59 > Tokyo 51 pip);
prior tidak dipakai memaksa kesimpulan.

| Yang diklaim | Output nb05 sel kode 7 (M4 kanon) | Status |
|---|---|---|
| London 1,666 | `London 395884 … 1.6658` | TERVERIFIKASI |
| Tokyo 1,439 | `Tokyo 364696 … 1.4393` | TERVERIFIKASI |
| Sydney 1,196 | `Sydney 82687 … 1.1962` | TERVERIFIKASI |
| NewYork 1,139 | `NewYork 293134 … 1.1386` | TERVERIFIKASI |
| Urutan London>Tokyo>Sydney>NY | cocok dengan baris di atas | TERVERIFIKASI |

Klaim "ranking Tokyo > NewYork menyimpang dari S5" juga terverifikasi silang
dari sel kode 12 (H4): `'ranking_sesuai_prior_USDJPY': False`.

**Penilaian kejujuran: JUJUR.** Deviasi dilaporkan di tiga permukaanindependen
(`report.md:121-122`, `tahap_12:80-83`, dan output sel H4), prior S5 tetap
diberlabel sekunder (`report.md:136`), dan tidak ada tempat yang memakai S5
untuk menopang H4. Angka ranking di `tahap_12:78-79` juga cocok dengan output.

### 8.2 Temuan jujur (b) — proksi spread mean-D1 diganti spread p95 per-bar

**Klaim** (`report.md:123-125`, `tahap_12:99-102,113-116`): proksi mean-D1 lama
hampir datar → **DIGANTI** spread p95 per-bar M1 (kanon `eda_design_v3.1.md:64`);
proksi lama hanya **TERCETAK sebagai pembanding**, bukan dipakai klaim.

**Kode** (`_build_eda05.py:530-534,546-550`):
- kolom pembanding `spread_mean_D1_lama_pips=("spread_mean_day","mean")` MASIH
  ada dan ikut tercetak — sesuai klaim "dipertahankan tercetak";
- rasio kanon dihitung dari `spread_p95_bar_pips`, bukan dari mean-D1:
  `ses["rasio_vol_over_spread"] = ses["mean_abs_r_pips"] / ses["spread_p95_bar_pips"]`.

**Output sel kode 7** menunjukkan kedua kolom berdampingan —
`spread_p95_bar_pips` = 0,8/1,2/0,9/1,5 vs `spread_mean_D1_lama_pips` =
0,6457/0,6448/0,6476/0,6390. Selisih antar-sesi pada proksi lama = 0,0086 pip
(hampir datar), persis seperti yang diklaim di `report.md:530-531` builder dan
`tahap_12:100`.

**Penilaian kejujuran: JUJUR.** Klaim "proksi lama diganti, bukan dipakai" dapat
saya buktikan dari kode, bukan dari dokumen: tidak ada satupun baris yang
membagi `mean_abs_r_pips` dengan kolom mean-D1. Ada cross-check mesin
(`_build_eda05.py:564-567`) yang membandingkan mean per-bar dengan
`config["spread"]["cost_basis"]["by_session"]` dan meng-assert selisih < 0,02.

### 8.3 Temuan jujur (c) — Q6 negatif

**Klaim** (`report.md:73`, `tahap_12:91-95`): hit-rate level **TIDAK** melampaui
placebo secara agregat; H5 justru mempersempit ke sub-populasi berbiaya rendah.
Kata "terbukti dihormati" dipakai negated, bukan sebagai klaim positif.

| Klaim | Bukti | Status |
|---|---|---|
| real 0,469–0,490 | `tahap_12:96` + `audit:2240` (`hl_utc 0.4905` → min `0,4890`, maks `0,490`) | TERVERIFIKASI |
| H5 tidak mengklaim level "bekerja" | `tahap_12:91-95` "hipotesis ini mempersempit"; ambang gugur `tahap_12:106-107` | TERVERIFIKASI |
| T-01 ikut diratifikasi sebagai karakteristik data, bukan sinyal | `report.md:129-131`; output sel kode 15 `78,582/1,347,847 = 5.83%` | TERVERIFIKASI |

Angka T-01 di `tahap_12:103` (66.817 A / 10.572 B) juga cocok dengan output
sel kode 15, dan `t01_massa_nol_pct = 5,83` di `_build_eda05.py:916` cocok
dengan pembulatan yang sama.

**Penilaian kejujuran: JUJUR pada arah kesimpulan.** Temuan negatif
dipertahankan, tidak dibalik menjadi sinyal, dan tidak ada kata triumphal di
surface mana pun untuk Q6. **Tapi angka pendukungnya tidak konsisten antar
objek — lihat B8-04 di bawah.**

### [B8-04] MEDIUM — Koreksi Q-TR-03 hanya masuk `report.md`; notebook & tahap 12 masih angka basi

Ini temuan **terpenting** di Batch C: angka di `report.md` ≠ angka di notebook
≠ angka di tahap 12, untuk metrik yang sama.

| Surface | Angka `placebo_hl` | Benar? | Lokasi |
|---|---|---|---|
| `report.md:73` | `0,4890–0,4922` | **YA** — ada anotasi `KOREKSI Q-TR-03 pasca-trace: … bukan 0,4890–0,5050 — 0,5050 milik placebo_acak; 0,4890 = titik estimasi hl_utc, bukan batas bawah CI` | `report.md:73` |
| Notebook (source sel) | `0,4890-0,5050` | **TIDAK** | `eda_05_regimes.ipynb:1340` (kode_sel 14, json idx 18, baris 24 dalam sel) |
| Notebook (output sel) | `0,4890-0,5050` | **TIDAK** | `eda_05_regimes.ipynb:1312` (baris output 2 sel kode 14) |
| `tahap_12:98` | `0,4890–0,5050` | **TIDAK** | `tahap_12:98` |

**Angka benar = `0,4890–0,4922`**,rementuk dari `audit:2242` yang membaca
kolom `placebo_hl` di sel 19 nb04: `hl_broker 0.4922`, `hl_utc 0.4890`.

**Root cause — inilah yang membuatnya MEDIUM dan bukan LOW.** Angka basi
tersebut bukan ketikan manual di notebook; ia **dihardcode di builder**:

```
_build_eda05.py:909-911
  "q6_hit_rate_placebo": (
      "placebo_acak 0,4989 [0,4831-0,5144]; placebo_hl 0,4890-0,5050 "
      "(batas bawah hl tumpang tindih batas atas real 0,490)"
  ),
```

Notebook dibangkitkan dari builder ini, jadi **rerun berikutnya akan
memproduksi ulang kesalahan yang sama** dan menimpa koreksi yang sudah benar
di `report.md`. Perbaikannya harus di `_build_eda05.py:910` (+ turunkan ke
notebook & `tahap_12:98`), **bukan**diedit di notebook saja.

**Mengapa MEDIUM dan bukan LOW/HIGH:**

- Bukan HIGH: **kesimpulan tidak berubah.** entailed apa pun, `placebo_hl`
  batas bawahnya 0,4890 (atau CI bawah sebenarnya 0,4748/0,4798) **tetap
  tumpang tindih** dengan batas atas real 0,490 → Q6 tetap negatif. Tidak ada
  hipotesis yang dibalik.
- Bukan LOW: ini **ketidakkonsisten faktual antar-objek** pada artefak yang
  diserahkan sebagai satu paket, dan sumbernya (builder) masih menyimpan
  nilai salah → **lokal, deterministik, pasti terjadi lagi**. Kesalahan angka
  yang merambat ke artefak diserahkan layak MEDIUM.
- Catatan tambahan: nilai `0,5050` **memang benar ada di repo** — tapi hanya
  sebagai batas atas `placebo_acak` di `eda_04`/`_build_eda04.py`/tahap 6-7
  nb04. Jadi nilainya bukan karangan; yang keliru adalah **labelnya**
  (`placebo_hl`), dan `report.md:73` sudah menyebut hal ini dengan tepat.

Ini **bukan** reopening temuan Q-TR-03 (yang sudah ditutup di `report.md`).
Ini temuan baru: **propagasi koreksi tidak tuntas**, dengan root cause
berada di luar file yang sebelumnya diperbaiki. **Perbaikan harus di
`_build_eda05.py:910`**, lalu notebook dan `tahap_12:98` diperbarui
menurutnya — menyunting notebook secara manual akan hilang pada regenerasi
 berikutnya.

**Penilaian kejujuran: JUJUR.** Temuan negatif dipertahankan, bukan
dibalik menjadi sinyal. Tidak ada kata triumphal di surface mana pun untuk Q6.

### 8.5 Verdict LANGKAH 8: **LULUS DENGAN CATATAN** — arah kesimpulan ketiga temuan jujur terbukti jujur, tetapi angka pendukung Q6 tidak konsisten antar-objek (B8-04, MEDIUM)

---

## LANGKAH 9 — Lima bug historis

Peta menyebut lima (empat dari daftar awal + bug pemetaan hari rerun-1 pada
Langkah 1). Untuk setiap bug saya uji dua hal terpisah: **(a) apakah fix-nya
benar-benar ada di kode sekarang**, dan **(b) apakah ada bukti regresi yang
mencegah bug yang sama kembali** — bukan sekadar "tidak ada error".

### 9.1 Bug 1 — Bucket pembuka hari (M15/M5)

**Riwayat** (`tahap_11:56-57`): `merge_asof` menghasilkan NaN karena bucket
M15/M5 pembuka `2023-01-01 22:00 UTC` mendahului bar M1 pertama → diganti
pencarian interval + assert pengecualian.

| Aspek | Bukti | Status |
|---|---|---|
| Fix ada | `_build_eda05.py:445-446` M15 dan `:590-591` M5 memakai `wall_clock_series(...).dt.normalize()` — **bukan** `merge_asof`/`searchsorted` | TERVERIFIKASI |
| `merge_asof` benar-benar hilang | `rg "merge_asof\|searchsorted\|n_leading5" _build_eda05.py` → hanya 3 hit, **semuanya komentar** (`:441`, `:585`, `:588`), nol eksekusi | TERVERIFIKASI |
| Assertion rasa-aman-semu dihapus | komentar `:588-589` mencatat `assert n_leading5 == 1` diganti paritas absolut; `rg n_leading5` tidak menemukan assertion | TERVERIFIKASI |
| **Regresi (paritas absolut M15)** | `:456-458` `assert 825 hari`, `assert len(m15_a) == 75_863`, `assert gap_return.sum() == 825` | TERVERIFIKASI |
| **Regresi (paritas absolut M5)** | `:595-596` `assert 825 hari`, `assert len(m5_a) == 227_568` | TERVERIFIKASI |

Kunci penting: paritas **absolut** (`75_863` / `227_568` bar) mengunci himpunan
bar, sehingga regresi pemetaan hari tidak bisa lolos diam-diam seperti pada
`n_leading5 == 1`.

### 9.2 Bug 2 — `fractal_mask` salah (OR per-pasangan)

**Riwayat** (`tahap_11:58-59`): replika menghasilkan ~495/hari vs referensi ≈49
→ diganti salinan verbatim nb04 → 40.483 swing = 49,07/hari.

| Aspek | Bukti | Status |
|---|---|---|
| Fix = salinan verbatim | banding diffrence-bodied `fractal_mask` `_build_eda04.py:313-336` vs `_build_eda05.py:599-626` → **body identik = True** (hanya docstring nb05 yang ditambah catatan sumber) | TERVERIFIKASI |
| Angka hasil | output sel kode 8: `40,483 → 49.07 swing/hari` | TERVERIFIKASI |
| **Regresi kunci ketat** | `:635-637` `assert abs(SWING_PER_DAY_K3 - 49.070) < 0.05` (kunci ketat) + `:638` band lebar `45.0 < … < 52.0` (lapis kedua) | TERVERIFIKASI |

### 9.3 Bug 3 — KeyError `hour_utc`

**Riwayat** (`tahap_11:60`): kolom dibuat di salinan → satu baris diperbaiki.

| Aspek | Bukti | Status |
|---|---|---|
| Fix ada | `_build_eda05.py:807` `hourly["hour_utc"] = hourly["utc"].dt.hour` — dibuat **sebelum** dipakai di `:808`, `:810`, `:813` | TERVERIFIKASI |
| Benar secara semantik | `dt.hour` dari `utc` = jam UTC, konsisten dengan label "per jam UTC" di `FIG-07` (`_build_eda05.py:1029-1031`) | TERVERIFIKASI |

**Catatan jujur saya:** untuk bug ini saya **tidak** menemukan assertion
regresi khusus. Kaidahnya bersifat struktural (kolom harus ada sebelum dipakai),
dan `dt.hour` tidak bisa "salah diam-diam" — kalau kolom hilang, eksekusi
gagal. Saya catat sebagai **kelemahan bukti yang jujur**, bukan temuan: tidak
ada guard yang menahan regresi nilai (mis. tanpa-`tz`), tapi itu di luar lima
bug yang diaudit.

### 9.4 Bug 4 — Gate ruff merah (F541 + E402 ×2)

**Riwayat** (`tahap_11:61-62`): gate merah → diperbaiki (pola `# noqa: E402`
nb01) → rerun ke-6 lulus.

| Aspek | Bukti | Status |
|---|---|---|
| Fix ada | 5 penanda `# noqa` di builder (`_build_eda05.py:93,94,97,966,969`) | TERVERIFIKASI |
| Gate benar-benar hijau **sekarang** | `ruff check scripts/_build_eda05.py` → `All checks passed!` exit 0; `ruff format --check` → `1 file already formatted` exit 0 | TERVERIFIKASI |
| Gate repo | `ruff check src/ tests/ scripts/` → `All checks passed!` exit 0; `ruff format --check` → `24 files already formatted` exit 0 | TERVERIFIKASI |
| Normalisasi format sebagai kelas regresi | `_build_eda05.py:1105-1110` menjalankan `ruff format` pada notebook **sebelum** eksekusi — menutup kelas bug SA-41 | TERVERIFIKASI |

### 9.5 Bug 5 — Pemetaan hari (perbaikan rerun-1, Langkah 1)

**Riwayat** (`report.md:91-95`, `tahap_11:86-94`, peta `:25,29-30`): versi lama
menggeser bucket pembuka hari sehingga replika nb03 tidak identik.

| Aspek | Bukti | Status |
|---|---|---|
| Metode disamakan | `_build_eda05.py:463-489` `variance_ratio` **body identik** dengan `_build_eda03.py` (banding diffrence → True); `:449-454` no-gap via kolom `gap_return`, bukan adjacency | TERVERIFIKASI |
| Angka replika final | output sel kode 6: `ACF lag-1 (all) = 0.001793`, `rata-rata VR(5,15,60) = 1.0312`, `sign-ACF = -0.022624`, `n_no_gap = 75,038` | TERVERIFIKASI |
| **Regresi (paling ketat dari semua bug)** | `:502` `abs(acf1 - 0.001793) < 0.0005` · `:506` `abs(mean_vr - 1.0312) < 0.005` · `:520` `n_no_gap == 75_038` · `:521` `abs(sign_acf1 + 0.022624) < 0.001` — masing-masing **dengan band lebar kedua** sebagai lapis cadangan (`:505`, `:509`, `:524`) | TERVERIFIKASI |
| Angka lama ditandai, bukan dihapus diam-diam | `report.md:91-95` menyebut angka lama 1,0277/−0,0220 eksplisit beserta alasan penggantiannya | TERVERIFIKASI |

### 9.6 Verdict LANGKAH 9: **LULUS** (5/5 bug ter-fix, 4/5 punya guard regresi)

---

## LANGKAH 10 — Konvensi RULES.md + §19 + Reuse-First §16 + §15.1

### 10.1 RULES.md §5 type hints & §6 docstring Google

| Fungsi | Type hints | Docstring | n baris |
|---|---|---|---|
| `md()` `_build_eda05.py:29` | lengkap (`: str`, `-> None`) | **TIDAK ADA** | 2 |
| `code()` `:33` | lengkap | **TIDAK ADA** | 2 |
| `build()` `:1089` | lengkap (`-> None`) | ADA (Google, 1 baris) | 40 |
| `find_project_root()` (dalam template) `:81` | lengkap | ADA | — |
| `variance_ratio()` (template) `:463` | lengkap | ADA, Google lengkap (Args/Returns) | — |
| `fractal_mask()` (template) `:599` | lengkap | ADA, Google lengkap (Args/Returns) | — |

Module docstring `:1-13` ADA. Fungsi >50 baris: **tidak ada** (`build()` = 40).
CC >10: tidak diukur (butuh analisis terpisah; tidak saya klaim sudah dicek).

**Preseden, bukan pembenaran.** `md()`/`code()` tanpa docstring identik di
`_build_eda02.py:23,27`, `_build_eda03.py:23,27`, `_build_eda04.py:24,28`. Jadi
ini **gaya proyek yang sudah ada**, bukan regresi baru. Saya **tidak** menaikkan
ini menjadi temuan: RULES §6 mengikat "fungsi publik", dan dua helper
pendek ini berada di bawah standar "helper pendek" yang RULES §5 sendiri
akui boleh tanpa anotasi berat. Saya catat sebagai **observasi**, bukan temuan.

### 10.2 RULES §8 error handling · §10 config · §9 logging · path

| Aturan | Hasil | Status |
|---|---|---|
| `except: pass` / bare `except` | **0 hit** (`rg` di `_build_eda05.py`) | TERVERIFIKASI |
| `pathlib` bukan string | `Path` dipakai di `:23-24`, `:1100-1101`; **0 path absolut hardcode** | TERVERIFIKASI |
| Config di `configs/` | `:119` `config = load_config("data")`; nb05 **tidak menulis** `configs/` | TERVERIFIKASI |
| UTC bukan local | `:439` `pd.to_datetime(m15["time"], utc=True)`, `:583` sama untuk M5 | TERVERIFIKASI |
| `print()` (§19 "print() produksi") | **2 baris** di luar template — `:1103` (`notebook ditulis: …`) dan `:1127` (`nbconvert exit=…`); 71 sisanya ada **di dalam string template** (output notebook, bukan produksi). Klasifikasi pakai `tokenize`, bukan tebakan. Preseden identik di `_build_eda03.py:837,865` dan `_build_eda04.py:1204,1228` | TERVERIFIKASI |
| Magic number | 1 kandidat di luar template: `:1122` `timeout=1800` (argumen nbconvert, bukan parameter metrik). Angka di dalam template (`assert` fidelity, band lebar) justru **wajib** ada per §15.1 syarat 4 | TERVERIFIKASI |

### 10.3 §19 anti-pattern substantive

| Anti-pattern | Status | Catatan |
|---|---|---|
| Look-ahead bias | TERVERIFIKASI-wajar | `:263` "ATR(14) … dirata-rata 14 hari SEBELUM t"; ambang tipologi full-sample **secara eksplisit** ditandai ex-post di `:1065-1068` dan `report.md:82` — bukan look-ahead yang disembunyikan |
| Data leakage | TERVERIFIKASI | tidak ada split acak; tidak ada P&L/backtest di nb05 (dilarang by design, `report.md:157`) |
| Duplikasi | **TERBUKA, siehe-sieha** | `fractal_mask` & `variance_ratio` diduplikasi ke nb05. **Sengaja dan ter-disclosure** (`:466-469`, `:602-604` "SALINAN VERBATIM … agar replika benar-benar se-metode"). Argumennya sah untuk audit fidelity: menyatukan ke `src/` akan menyentuh nb03/nb04 yang ter-gate. Lihat §10.6 |
| `print()` produksi | TERVERIFIKASI | lihat §10.2 |
| File >400 baris tanpa alasan | **DILEGALKAN §15.1** | lihat §10.4 |
| Fungsi >50 baris | TERVERIFIKASI | `build()` = 40 baris |
| Hardcode | TERVERIFIKASI | lihat §10.2 |

### 10.4 §15.1 — empat syarat pengecualian file generator

Builder = **1.132 baris**, melewati §15 soft limit 400. Pengecualian §15.1
hanya berlaku bila **keempatnya** terpenuhi; tanpa salah satu, pengecualian
gugur.

| # | Syarat §15.1 | Bukti | Status |
|---|---|---|---|
| 1 | Referensi baris stabil | Baris builder pada audit `:1821` (`ba11f0792823`, 51.783 byte / 1.132 baris) **masih cocok byte demi byte** dengan file sekarang — syarat ini diuji khusus pada builder, dan builder memang tidak berubah. Referensi baris dalam audit **resolve benar** ke isi yang diklaim: `:539` → `assert m1_a["spread_pips"].notna()`; `:546-547` → `spread_mean_bar_pips`/`spread_p95_bar_pips`; `:853` → `assert n_off_top6 < 2`; `:368` → `ci95_beda_iid`. Tidak ada rewrite massal tanpa jejak. **Catatan:** tabel identitas yang sama basi untuk 3 objek lain — lihat B8-03; syarat ini tetap terpenuhi karena subjeknya builder | TERVERIFIKASI |
| 2 | Diff kecil per batch | Riwayat blob terdokumentasi di `tahap_11:5` (`cc73f794` → `ca997cc9b70a` → `ba11f0792823`; 53 → 59 → 67 assertion) dan di `tahap_12:5-6` (`8158d5b57b20e`, sel #13–#17 → #13–#18). Perubahan = tambahan assertion + teks koreksi, bukan rewrite | TERVERIFIKASI |
| 3 | Output deterministik | `_build_eda05.py:339` dan `:393` `np.random.default_rng(20261006)` — seed tetap, sesuai Kontrak 00; tidak ada `np.random` tanpa seed (`rg` → 2 hit, keduanya ber-seed) | TERVERIFIKASI |
| 4 | Assertion mesin | **67 `assert`** terhitung dari notebook **yang benar-benar dieksekusi** (`json.loads` + hitung `^\s*assert`), dengan sebaran: sel 0→3, 1→4, 2→9, 3→6, 4→6, 5→1, 6→10, 7→7, 8→5, 9→1, 10→4, 11→1, 12→2, 13→3, 14→2, 15→1, 16→1, 17→1. `execution_count` **urut** dan **0 output error**. Angka penting (VR, sign-ACF, swing/hari, n_no_gap, paritas bar, flag M4, CI, T-01) terkunci `assert`, bukan hanya tertulis di dokumen | TERVERIFIKASI |

**Kesimpulan §15.1: keempat syarat terpenuhi.** Pengecualian builder **berdiri**;
1.132 baris bukan pelanggaran.

### 10.5 §16 Reuse-First

| Aspek | Bukti | Status |
|---|---|---|
| Tidak ada modul baru di `src/` | `git status --porcelain` → tidak ada entri `?? src/…`; yang ada hanya ` M src/data/__init__.py`, ` M src/utils/__init__.py`, ` M configs/data.yaml` yang **cosmetic** — `git diff --name-only` hanya menghasilkan `.ai/AGENTS.md`, `.ai/STATE.md`, `requirements.txt`, jadi tiga file itu **tidak punya diff konten** (artefak `core.autocrlf`) | TERVERIFIKASI |
| Reuse yang dipakai | `src.data.broker_time.wall_clock_series`, `src.utils.config.load_config`, dan dari `notebooks/scalping/_eda_common.py`: `EXPECTED_FINGERPRINT`, `SESSION_ORDER`, `add_labels`, `session_fingerprint` | TERVERIFIKASI |
| Fingerprint di-assert (kunci reuse) | `:113` `assert session_fingerprint() == EXPECTED_FINGERPRINT, "definisi sesi berubah - hentikan"` | TERVERIFIKASI |
| Larangan "file baru kalau bisa patch" | `_build_eda05.py` memang **file baru**, tapi tidak ada file lama yang bisa di-patch untuk_jobs ini (membangkitkan notebook baru); polanya identik `_build_eda01..04` | TERVERIFIKASI |

### 10.6 Catatan transparan tentang duplikasi (tidak saya jadikan temuan)

`fractal_mask` dan `variance_ratio` diulang di nb05 alih-alih diekstrak ke
`_eda_common.py`. Ini tampak seperti §19 "Duplikasi", tapi **argumen coder
layak dan tertulis**: menyatukan helper ke modul bersama harusnya menyentuh
nb03/nb04, yang alters output notebook yang sudah ter-gate dan ter-audit.
`_eda_common.py` memang **tidak** memuat kedua fungsi (saya cek: keduanya
`False`), jadi ini **duplication sadar, bukan kelalaian**. Saya mencatatnya
terbuka untuk batch berikutnya; **bukan** temuan Batch C karena tidak ada
konsekuensi kebenaran yang terukur.

### 10.7 Gate yang diverifikasi ulang read-only

Tidak ada pipeline yang saya jalankan yang menulis ke objek.

| Gate | Perintah | Hasil |
|---|---|---|
| pytest | `pytest tests/ -q` | **157 passed** in 2,17 s, exit 0 |
| ruff check | `ruff check src/ tests/ scripts/` | `All checks passed!`, exit 0 |
| ruff format | `ruff format --check src/ tests/ scripts/` | `24 files already formatted`, exit 0 |
| foreign chars | `scripts/check_foreign_chars.py` | `OK: 79 file discan, tidak ada karakter asing`, exit 0 |
| validate_data | **TIDAK DIJALANKAN** | `src/data/validate_data.py:521-523` menulis `reports/data_validation_<tanggal>.md` → violates "no run that overwrites". Sebagai gantinya saya baca artefak yang sudah ada: `reports/data_validation_2026-10-06.md` (sha256 `beee80bc5a122d1d`) = **LOLOS, 0 error ×4 tahun** (2023/2024/2025/2026), cocok klaim `tahap_11:50` |

**Catatan tentang angka "32 files".** `tahap_11:48` menulis
`ruff format --check → 32 files already formatted`. Angka itu **tepat** —
`ruff format --check .` (seluruh repo) = `32 files already formatted`, dan
`src/ tests/ scripts/` = 24. Jadi angka coder benar; cakupannya seluruh repo.

---

## RINGKASAN TEMUAN BATCH C

| ID | Severity | Langkah | Ringkasan | Lokasi |
|---|---|---|---|---|
| **B8-04** | **MEDIUM** | 8 | **Koreksi Q-TR-03 hanya masuk `report.md`; notebook (source + output) dan `tahap_12:98` masih `0,4890–0,5050`. Root cause di `_build_eda05.py:910` → rerun akan mereproduksi kesalahan. Kesimpulan Q6 tetap negatif (tumpang tindih tetap ada)** | `_build_eda05.py:909-911`; `eda_05_regimes.ipynb:1312,1340`; `tahap_12:98` |
| **B8-03** | **MEDIUM** | 7 | Tabel identitas audit `:1819-1825` basi: **2 dari 5 objek berubah isi** setelahnya (`report.md` +280 B, `tahap_11` +106 B); notebook hanya EOL. Pengikat bukti Batch B tidak dapat diaudit ulang tanpa menghitung ulang | `audit:1819-1825` |
| **B8-01** | LOW | 7 | Bukti pendukung "mtime tetap 15:49:27" sudah tidak dapat diuji (bulk EOL sync 10:42:00 menetralkan seluruh mtime repo); jalur hash tetap membuktikan isi FIG-01..03 tak berubah | `laporan_tahap_14_figures.md:13,20-22` |
| **B8-02** | LOW | 7 | Rujukan sel output di `tahap_14` ("sel #21"/"sel #22") **tidak dipatok ke blob notebook** — dokumen ini tidak menyebut hash notebook sama sekali, padahal `tahap_12:5` eksplisit merekam blob berubah (`8158d5b57b20e` → `2d8f600acade`, sel #13–#17 → #13–#18). Akibatnya rujukan `tahap_14` kini **stale +2 sel** (figures & registry ada di json idx 22/23) dan **tidak dapat diaudit ulang** | `laporan_tahap_14_figures.md:11-12` |
| **B9-01** | LOW | 9 | Bug KeyError `hour_utc` ter-fix dan benar secara struktural, tapi **tidak punya assertion regresi** — empat bug lainnya punya | `laporan_tahap_11_regime.md:60`; `_build_eda05.py:807` |
| **B10-01** | LOW | 10 | `md()`/`code()` tanpa docstring, menyimpang dari RULES §6; **prevalen di builder lain** (`_build_eda02/03/04`), jadi gaya proyek bukan regresi — tidak dinaikkan | `_build_eda05.py:29,33` |

**Temuan yang saya batalkan sendiri (dicatat terbuka, §C prompt):**

- **False positive #1 — "duplikasi helper"**: awalnya saya tandai `fractal_mask`/
  `variance_ratio` sebagai pelanggaran §19 Duplikasi. Setelah memeriksa
  `_eda_common.py` dan argumen disclosure di `:466-469`/`:602-604`, saya
  membatalkannya: duplikasi sadar dan beralasan fidelity, bukan kemalasan.
  Dicatat di §10.6, **bukan** temuan.
- **False positive #2 — "referensi baris audit tidak resolve"**: awalnya saya
  menduga referensi baris di blok lama audit sudah basi. Setelah dihitung, blok
  re-audit (`:1811`+) yang dirujuk memang ditulis terhadap blob `ba11f079`
  yang sama dengan blob sekarang, dan semua referensinya **resolve benar**
  (§10.4 syarat 1). Dibatalkan.
- **False positive #3 — "penomoran sel di tahap_14 salah konvensi"** (draft
  awal): saya sempat menulis bahwa `tahap_14` salah memakai konvensi penomoran
  sel. Setelah memeriksa `tahap_12:5` — blob notebook **berubah** pasca-audit
  Batch B (`8158d5b57b20e` → `2d8f600acade`, sel #13–#17 → #13–#18) —
  penjelasan yang benar adalah `tahap_14` **tidak meng-cite blob notebook sama
  sekali**, sehingga rujukan selnya ikut basi +2 sel. Akar masalahnya
  **traceability**, bukan salah konvensi. B8-02 saya tulis ulang dengan framing
  itu (severity tetap LOW, tidak dinaikkan).

---

## VERDICT BATCH C

| Langkah | Asal | Verdict |
|---|---|---|
| 7 — Registry FIG-01..07 + FIG-01..03 | [KLAIM] C4 | **LULUS** (registry tepat 7, FIG-01..03 byte-identik vs HEAD; 1 LOW + 1 MEDIUM B8-03) |
| 8 — Tiga temuan jujur | [KLAIM] laporan coder | **LULUS DENGAN CATATAN** (ketiganya jujur secara arah; **MEDIUM B8-04**: angka Q6 tidak konsisten antar-objek) |
| 9 — Lima bug historis | [KLAIM] riwayat coder | **LULUS** (5/5 ter-fix, 4/5 berguard regresi; 1 LOW B9-01) |
| 10 — Konvensi + §19 + §16 + §15.1 | [ATURAN] penuh | **LULUS** (4 syarat §15.1 terpenuhi; 1 LOW gaya) |

### **VERDICT BATCH C: LULUS DENGAN CATATAN — 2 MEDIUM, 4 LOW. Tidak ada HIGH/CRITICAL**

Batch C **tidak** bersih tanpa catatan. Dua temuan MEDIUM:

- **B8-04** (Langkah 8) adalah yang substansial: paket artefak yang diserahkan
  **tidak konsisten dengan dirinya sendiri** pada satu angka, dan builder masih
  menyimpan angka basi sehingga kesalahan **ter Deterministik akan berulang**.
  Yang meredakan: **tidak ada hipotesis yang terbalik** — Q6 tetap negatif.
- **B8-03** adalah substantif soal bukti: entri Batch B tidak dapat ditelusuri
  ulang apa adanya karena tabel identitasnya salah untuk 2 dari 5 objek.

Tidak ada klaim yang saya **FOUND** salah hitung pada perhitungan, dan tidak
ada kesimpulan metodologis yang saya **FOUND** keliru. Yang saya temukan adalah
**ketidakkonsisten naratif antar-artefak** — jenis cacat yang justru sulit
tertangkap kalau auditor berhenti di satu dokumen saja.

**Perbaikan yang saya rekomendasikan (urut nilai):**

1. `_build_eda05.py:910` → `0,4890-0,4922`; regenerate notebook; `tahap_12:98`
   disinkronkan. (B8-04 — satu baris kode menutup tiga permukaan.)
2. Perbarui tabel identitas `:1819-1825` dengan hash aktual di §0 dokumen ini,
   dan **tetapkan konvensi byte**: pakai `git hash-object`, bukan ukuran
   file, karena repo ini sudah pernah mengalami bulk konversi EOL. (B8-03)

### Yang belum diverifikasi (jujur, bukan ditutup)

1. **Keterbacaan visual figure** untuk manusia — di luar kemampuan audit
   tekstual; angka dasarnya sudah terverifikasi (§7.4) — sama seperti yang
   dicatat `tahap_14:38-41`.
2. **CC >10** fungsi builder — tidak diukur di Batch C; butuh analisis terpisah.
3. **Nilai `gap_return` M15** Klaim "terverifikasi offline sebelum rerun"
   (`_build_eda05.py:453`) — saya percaya assertion `:458`
   (`gap_return.sum() == 825`) yang mengunci hitungannya, tapi tidak
   mereplikasi definisi `utc.diff() > 15 menit` bar-per-bar secara independen.
4. **Angka Q1–Q6** berasal nb00–nb04 — di luar objek; tidak dibuka (§C prompt).

### Pertanyaan untuk Coder (Batch D / tcp)

1. Apakah indeks sel di laporan tahap 14 ("#21"/"#22") dimaksudkan sebagai
   0-indexed sel-kode? Kalau ya, seharusnya #16/#17. Kalau 1-indexed sel-kode,
   seharusnya #17/#18. Mohon konfirmasi konvensinya agar referensi sel di
   seluruh dokumen bisa ditelusuri tanpa tebakan.
2. Bug `hour_utc` (B9-01) — apakah perlu assertion regresi yang mengunci
   kolomnya, atau kaidahnya dianggap cukup struktural?
3. Apakah ada rencana untuk mengekstrak `fractal_mask`/`variance_ratio` ke
   `_eda_common.py` di batch terpisah (duplikasi sadar §10.6), atau dibiarkan
   sebagai tradeoff fidelity yang disengaja?
4. **B8-04 (MEDIUM, perlu keputusan):** apakah koreksi cukup di
   `_build_eda05.py:910` + regenerate notebook + `tahap_12:98`, atau perlu
   diperluas ke dokumen lain yang menyebut rentang `placebo_hl`?
5. **B8-03 (MEDIUM, perlu keputusan):** apakah tabel identitas sebaiknya ditulis
   ulang sebagai daftar **riwayat** (v0/v1/v2) alih-alih satu baris "kini",
   supaya perubahan berikutnya tidak lagi membuat tabel prioritas basi?

## SELF-AUDIT 3× (adversarial)

1. **Correctness.** Semua temuan punya `file:baris` + angka/output. Yang saya
   klaim benar dihitung ulang dari sumber, bukan dari dokumen: 67 `assert` dari
   JSON notebook yang benar-benar dieksekusi (`execution_count` 1..19 berurutan,
   0 output error, dihitung per sel — bukan regex); klasifikasi `print()` lewat
   **AST**, bukan tebakan; 7 hash PNG via `git hash-object`; dimensi PNG dari
   byte IHDR; body `fractal_mask`/`variance_ratio` via `difflib`.

   **Bukti saya yang saya distroksi sendiri, secara terbuka:**

   (a) Baseline SHA-256 audit dari initiator **tidak cocok** dengan file aktual
   — dilaporkan di §0, bukan diam-diam.
   (b) **Tiga** false positive saya batalkan dan saya catat (§Ringkasan).
   (c) Yang paling penting: klaim "hash objek cocok" yang saya tulis di draft
   pertama **ternyata hanya benar untuk builder, tahap 12, dan notebook
   (setelah normalisasi EOL)**. Menyelidiki kembali karena byte notebook tidak
   cocok, saya menemukan `report.md` dan `tahap_11` **berubah isi** — dan itu
  melahirkan temuan B8-03. Jadi calibration saya terhadap tabel identitas Batch B
   terlalu cepat; saya perbaiki dan sekarang mengulang seluruh §0.

2. **Bias.** Apakah saya menilai metode alih-alih kejujuran? Tidak: di Langkah 8
   saya hanya menguji apakah disclosure jujur dan angka cocok — bukan apakah
   ambang tipologi full-sample itu metodologis ideal (sudah diputuskan L3-01 di
   Batch A, di luar scope). Apakah saya sedang di luar scope? Saya **tidak**
   membuka `nb01`-`nb04`, **tidak** mengulang temuan D1–D12/MEDIUM/LOW lama.

   **Tarik-ulur severity — kedua arah, saya catat keduanya:**

   - Places saya **menolak menaikkan** meski bukti ada: B8-01 (mtime) karena
     jalur hash sudah membuktikan substansi; B10-01 (docstring) karena
     prevalen di empat builder.
   - Place saya **menolak menurunkan** meski argumen meredakannya ada:
     B8-04 saya tahan di MEDIUM meski "kesimpulan tidak berubah", karena
     argumen "kesimpulan tidak berubah, jadi ringan" sebenarnya **tidak**
     berlaku di sini: argumen itu hanya sah kalau tabel kontrolnya benar,
     sedangkan justru kontrolnya yang berubah.

   Yang saya sengaja **tidak** lakukan: menaikkan B8-04 dengan alasan
   "angka Q6 salah hitung" — karena `0,5050` itu **memang nilai sah**
   (batas atas `placebo_acak`), yang keliru adalah labelnya. Kalau saya
   menulis "perhitungan salah", saya berbohong.
3. **Meta.** Objek benar? Ya — lima blob + dokumen audit, diverifikasi ulang
   dan **hash aktual dicantumkan di §0** (termasuk koreksi terhadap tabel
   Batch B). Hash akhir dihitung **setelah** append. Batch ini hanya Batch C
   (Langkah 7–10). Tidak ada commit. Objek sumber tidak saya ubah satu byte
   pun: satu-satunya file yang saya tulis adalah dokumen audit ini (append-only,
   gaya LF sesuai file saat ini). Tidak ada pipeline yang saya jalankan yang
   menulis ke objek — `validate_data` sengaja **tidak** saya jalankan karena ia
   menulis file, dan saya ganti dengan membaca artefaknya.

---

## STOP — Menunggu perintah Batch berikutnya

Batch C selesai. Tidak ada batch berikutnya tanpa perintah terpisah
(`PERAN-auditor.md:38`). Semua file sumber read-only; tidak ada commit.

## Lampiran — Hash final (dihitung SETELAH append)

Dicantumkan pada pesan penutup di chat setelah append final, agar angka di
dalam dokumen tidak berubah oleh penambahan/hash ini sendiri.
---

# RE-AUDIT FIX BATCH C — F-B804 + F-B802 + F-B901 + PENUTUP B8-03

Putaran ini **read-only terhadap sumber**. Satu-satunya file yang saya tulis adalah
dokumen audit ini (append-only, gaya LF sesuai file saat ini). Tidak ada commit.

Coder melaporkan "6 file diubah + semua gate hijau + STOP tanpa commit"
(`2026-10-07_reaudit-batchC-fix-auditor.md:3`). Saya tidak mempercayai laporan itu:
setiap angka di bawah dihitung ulang dari disk, dari AST, dan dari output sel yang
benar-benar tereksekusi. Yang tidak bisa saya buktikan, saya tulis **tidak terbukti** —
bukan "kemungkinan benar".

## 0. Gate 0 — verifikasi 7 hash titik-awal (HARUS LOLOS, kalau tidak STOP)

Dijalankan **sebelum** membaca artefak lain. Metode: `git hash-object` untuk SHA-1 blob,
`hashlib.sha256` untuk pembeda, hitung byte dan CR langsung dari disk.

| Peran | SHA-1 klaim | SHA-1 aktual | Cocok | Byte klaim | Byte aktual | Cocok |
|---|---|---|---|---|---|---|
| Builder | `dd3d684a5a95` | `dd3d684a5a95` | ya | 52.203 | 52.203 | ya |
| Notebook | `2cb57ad9ec1a` | `2cb57ad9ec1a` | ya | 83.611 | 83.611 | ya |
| Laporan | `afeb1b1cb0db` | `afeb1b1cb0db` | ya | 12.335 | 12.335 | ya |
| Tahap 11 | `118baf140130` | `118baf140130` | ya | 8.621 | 8.621 | ya |
| Tahap 12 | `094d90d20e25` | `094d90d20e25` | ya | 9.227 | 9.227 | ya |
| Tahap 14 | `b4269a97361d` | `b4269a97361d` | ya | 4.184 | 4.184 | ya |
| Audit (pra-append) | `f7a5a9f8b894` | `f7a5a9f8b894` | ya | 183.892 | 183.892 | ya |

**7/7 cocok, Gate 0 LOLOS, proceed.** SHA-256 aktual: builder `d820eed2c5d0`,
notebook `94c2d798f063`, laporan `b4f1c62b858f`, tahap 11 `8d5827640c13`,
tahap 12 `4ff07656e912`, tahap 14 `660b4023f1c2`.

## 1. B8-03 (2 dari 2) — konvensi byte: `git hash-object`, bukan ukuran file

Rekomendasi `:2870-2871` saya jalankan sebagai **kesimpulan faktual**, bukan anjuran
lagi. Repository ini punya `.gitattributes:13` (`* text=auto eol=lf`) dan
`core.autocrlf=true`, jadi `git hash-object` menormalisasi EOL sebelum hashing.
Bukti langsung:

```
notebook disk (CRLF)    = 83.611 B  ->  sha1 blob RAW = 529cbf2092a7
notebook LF-normalisasi = 81.948 B  ->  sha1 blob LF  = 2cb57ad9ec1a
git hash-object                        = 2cb57ad9ec1a   (cocok dengan LF)
git hash-object --no-filters           = 529cbf2092a7
```

Konsekuensinya tegas: **ukuran byte berubah 1.663 byte hanya karena EOL**, sementara
isi Markdown-nya sama. Jadi byte size **tidak sah** sebagai gate integritas di repo ini;
`git hash-object` **sah**. Ini persis jebakan yang mengaktifkan B8-03, dan sekarang terkunci.

## 2. B8-03 (1 dari 2) — PENUTUP: tabel identitas ditulis ulang sebagai RIWAYAT v0/v1/v2

Tabel `:1821-1825` saya biarkan utuh (append-only) dan saya tambahkan tabel riwayat
di bawah. v0 = baris tabel yang salah; v1 = aktual saat audit Batch C bagian 0;
v2 = aktual fix ini. Kolom `git` adalah gate; kolom byte bersifat historis.

| Objek | v0 git (tabel `:1821-1825`) | v1 git (saat audit B-C) | v2 git (fix ini) | selisih byte v1 ke v2 | selisih baris v1 ke v2 |
|---|---|---|---|---|---|
| Builder | `ba11f0792823` | `ba11f0792823` | **`dd3d684a5a95`** | +420 | +8 |
| Notebook | `2d8f600acade` | `2d8f600acade` | **`2cb57ad9ec1a`** | +2.418 | +15 |
| Laporan | `0c361137f15f` | `918f2afa48c5` | **`afeb1b1cb0db`** | +70 | 0 |
| Tahap 11 | `6a89ed49fd37` | `f012df4f7ec6` | **`118baf140130`** | +334 | +1 |
| Tahap 12 | `2dfd7bb7dae8` | `2dfd7bb7dae8` | **`094d90d20e25`** | +355 | +4 |

v0 ke v2: **5 dari 5 objek berubah isi**. Tidak satu pun byte yang berubah menyentuh
Q6 atau hit-rate — semuanya teks koreksi dan satu guard baru. Builder +420 B = satu blok
assert 6 baris (`_build_eda05.py:808-813`) plus string H5; tahap 11 +334 B = satu blok
riwayat koreksi; tahap 12 +355 B = 4 baris koreksi Q6 plus catatan regenerasi.

**Notebook: pisahkan EOL dari isi.** v1 = 81.193 B / 0 CR; v2 = 83.611 B / **1.663
CRLF**. Selisih 2.418 B terurai menjadi **+755 B isi** (81.193 ke 81.948 setelah
normalisasi LF) plus **1.663 B carriage-return**. Jadi kenaikan isi nyata hanya 755 B;
sisanya artefak EOL. Saya menghitung ini karena tabel byte akan membingungkan kalau
tidak dipisah.

**B8-03 ditutup.** Bukan karena kode berubah, tapi karena tabelnya sekarang punya
riwayat dan konvensinya eksplisit — perubahan berikutnya tidak akan membuat tabel
prioritas basi tanpa jejak.

## 3. R1 — F-B804: endpoint `placebo_hl` di hulu

**TERVERIFIKASI.** `_build_eda05.py:916-920` kini memuat:

```
916:  "placebo_acak 0,4989 [0,4831-0,5144]; placebo_hl 0,4890-0,4922 "
917:  "(KOREKSI Q-TR-03/B8-04: sebelumnya 0,4890-0,5050 - 0,5050 milik "
918:  "placebo_acak; 0,4890 = titik estimasi hl_utc, bukan batas bawah CI "
919:  "[0,4748/0,4798]; titik estimasi 0,4890 tumpang tindih batas atas real 0,490)"
```

Dua fakta wajib ada dan keduanya ada: (a) `0,5050` milik `placebo_acak`, (b) `0,4890`
adalah **titik estimasi**, bukan batas bawah CI. Label `KOREKSI Q-TR-03/B8-04` ada.

Regenerasi terbukti di output: sel **json idx 18** (`kode_sel #15`, `execution_count 15`)
mencetak `q6_hit_rate_placebo` dengan string baru **persis**, bukan hanya di source.
Jadi koreksi benar-benar melewati builder lalu notebook, bukan disentuh manual.

Grep negatif repo-wide untuk literal `placebo_hl 0,4890-0,5050`: **nol di keenam blob
pascifix**. Sisa yang sah hanya di (a) dua file prompt `.ai/assistant/prompts/`
(`:16`, `:46`, `:19` — teks instruksi historis), (b) audit lama di
`eda_nb05_audit_v1.md:1957/2263/2315/2586` — append-only, tidak boleh saya ubah, dan
(c) `thoughts/ledgers/CONTINUITY_ses_eedd.md:56` yang di luar scope. Di builder, angka
lama masih muncul di `:917` **tanpa** prefiks `placebo_hl` — itu **catatan koreksi**, dan
justru itu yang jujur: ia menyebut angka lama supaya jejaknya tidak hilang.

## 4. R2 — notebook benar-benar hasil regenerate, bukan edit manual

**TERVERIFIKASI** lewat bukti tidak langsung yang kuat. Saya tidak boleh rerun, jadi
saya buktikan lewat konsistensi arah lain.

- Builder mendefinisikan 26 sel (19 kode, 7 md) lewat `md()`/`code()`; notebook punya
  **26 sel (19 kode, 7 md)** — cocok per jenis.
- **11 dari 26 sel berbeda source** antara string builder dan notebook (8 sel kode identik
  string). Itu sendiri terlihat seperti regresi, jadi saya telusuri: bandingkan
  `ast.dump()` keduanya, hasilnya **11 dari 11 AST IDENTIK**. Bedanya murni line-wrap.
  Penyebabnya ada di builder sendiri: `build()` menulis lewat `nbf.write` (`:1109-1110`)
  lalu menjalankan `ruff format` pada notebook (`:1114-1118`, `check=True`) sebelum
  eksekusi. Edit manual **tidak akan** menghasilkan 11 sel yang AST-nya identik dengan
  builder. Ketujuh sel markdown justru identik string tanpa satu pun perlu diformat.
- `ruff format --check notebooks/scalping/eda_05_regimes.ipynb` rc=0,
  `1 file already formatted`. Jadi tidak ada perapian manual yang menampakkan di diff.
- `execution_count` = 1..19, tanpa gap, urut sesuai posisi sel kode.
- **0 output bertipe `error`** di seluruh 19 sel kode.
- Penutup `=== nb05 SELESAI: SEMUA ASSERTION PASS` ada di builder **dan** di sel
  json idx 25 — hasil runtime, bukan teks yang bisa diketik tangan.
- Rantai pembuktian lain: output sel H5 (idx 18) memuat angka desimal `2.0823`,
  `1.5992`, `0.9488`, `0.7975`; M2 `0.7827`; T-01 `5.83`; ACF1 `0.001793`;
  `n_no_gap 75.038`. Semua dibaca dari output dan cocok dengan dokumen.

## 5. R3 — `tahap_12` sinkron, kesimpulan Q6 tidak bergeser

**TERVERIFIKASI.** `tahap_12:100-102` memuat `placebo_hl 0,4890–0,4922` dengan label
`KOREKSI B8-04` dan dua fakta yang sama seperti builder — cermin `report.md:73`
(sudah punya `KOREKSI Q-TR-03` sejak Batch C). Keempat permukaan sekarang identik:
`report.md:73`, `tahap_12:100-102`, `_build_eda05.py:916-919`, dan output sel idx 18.

Kesimpulan Q6 **tidak berubah** di mana pun — saya periksa secara negatif:

| Artefak | Baris | Pernyataan |
|---|---|---|
| `report.md` | 73 | "TIDAK terbukti 'dihormati'" |
| `tahap_12` | 111 | "level dinyatakan tak dieksploitasi" |
| `_build_eda05.py` | 909 | "Q6 menemukan hit-rate TIDAK melampaui placebo" |
| `_build_eda05.py` | 933 | "dinyatakan tak dieksploitasi" |

Tidak ada arah yang bergeser. Label koreksi juga **tidak** mengklaim temuan baru — ia
menyatakan endpoint yang dikoreksi, bukan bahwa level dieksploitasi. Ini yang saya
tegakkan di batch lalu: koreksi tidak boleh menjadi pintu untuk mengubah kesimpulan.
Batch ini tidak mengubahnya.

## 6. R4 — F-B802: rujukan sel `tahap_14` dipatok ke blob

**TERVERIFIKASI.** `tahap_14:7-10` menyebut blob penuh
`2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` plus tanggal regenerasi 2026-10-07. Hash itu
**cocok dengan `git hash-object` aktual**. `tahap_14:41-52` mendeklarasikan konvensinya
eksplisit: **json idx** (0-indexed di array `cells`), lalu menyandingkannya dengan
`kode_sel` dan `execution_count` supaya tidak ada tebakan.

Saya bangun pemetaan sendiri dari JSON dan cek klaim (yang dirujuk `tahap_14:16-17`):

| Klaim `tahap_14` | json idx aktual | kode_sel aktual | execution_count aktual | Hasil |
|---|---|---|---|---|
| figures = json idx 22, kode_sel #17, exec 17 | 22 | **#17** | **17** | COCOK |
| registry = json idx 23, kode_sel #18, exec 18 | 23 | **#18** | **18** | COCOK |

Output sel idx 22 = `tersimpan: FIG-04.png …FIG-07.png` (4 baris); sel idx 23 =
`PASS: registry figures tepat FIG-01..FIG-07`. Keduanya sesuai klaim.

Jawaban auditor Q1 (`:2887-2890`) sekarang **terjawab eksplisit** di `tahap_14:41`:
konvensinya json idx. Untuk memastikan tidak menyesatkan, saya cek dokumen lain yang
sudah memakai angka sama:

- `tahap_12:4` "sel #13–#18" — json idx 13, 14, 15, 16, 17, 18 = H1, H2, H3, H4, M3,
  H5 (urutan diambil dari docstring tiap sel) ✓
- `tahap_12:122` "M3 di sel #17" — json idx 17 = M3 ✓
- `tahap_12:128` "sel #7/#9/#10/#13–#18" — json idx 9 = replica ACF/VR, 10 = replica
  mean|r| dan spread, 11 = frekuensi swing, 13-18 = H1..H4, M3, H5 ✓

Jadi `tahap_12` **konsisten** dengan konvensi yang kini dideklarasikan `tahap_14`.
Tidak ada dokumen yang saling bertentangan — ini perbaikan sungguhan, bukan sekadar
menambahkan kalimat.

Klaim `tahap_14:50` bahwa blob lama tidak ada di Git saya cek: `git cat-file -e` rc=128
untuk `8158d5b57b20e`, `2d8f600acade`, `ca997cc9b70a`, `cc73f794`, `ba11f0792823`, dan
`1155e6de` — **semua hilang**. Klaim itu benar, dan konsekuensinya saya catat di bagian 15.

## 7. R5 — F-B901: assertion regresi `hour_utc`

**TERVERIFIKASI.** Count via AST (bukan grep baris), sadar-multiline:

- Total `ast.Assert` di 19 sel kode = **68**.
- Assert yang memuat `hour_utc` = **TEPAT SATU**.
- Lokasi: **json idx 16 = kode_sel #13 = exec 13**, source baris 10-15 sel itu
  (baris 9 = assignment `hourly["hour_utc"] = ...`).
- Builder `:808-813`, tepat sesudah assignment `:807` seperti diminta.
- **Top-level**, bukan di dalam `if`, `for`, `try`, atau fungsi — jadi benar-benar dieksekusi.

Predikat (4 kondisi, digabung `and`):

| Kerusakan | Kondisi | Menangkap? |
|---|---|---|
| Kolom hilang | `"hour_utc" in hourly.columns` | ya |
| DataFrame kosong | `len(hourly) > 0` | ya |
| NaN atau null | `hourly["hour_utc"].notna().all()` | ya |
| Nilai di luar 0-23 | `hourly["hour_utc"].between(0, 23).all()` | ya |

Pesannya: `hour_utc hilang/rusak - regresi B9-01 (KeyError hour_utc pada riwayat nb05)` —
menyebut bug aslinya, jadi jejaknya tetap terbaca. **B9-01 ditutup.**

## 8. R6 — ripple count 67 ke 68 dan evaluasi sisa angka 67

**TERVERIFIKASI via AST.** 68 (lihat bagian 7), 0 error, `execution_count` 1..19
berurutan.

Penyebut count di setiap artefak:

| Artefak | Baris | Isi |
|---|---|---|
| `report.md` | 15 | count **68** plus `KOREKSI B9-01: 67 ke 68 (+1 guard regresi hour_utc)` |
| `tahap_11` | 4 | **68 assertion PASS** |
| `tahap_11` | 106 | "Jumlah assertion kini 68" |
| `tahap_11` | 108 | "KOREKSI B7-01 68 ke 67, kini KOREKSI B9-01 67 ke 68" |
| `tahap_14` | 9 | "68 assertion PASS" |

**Tidak ada 67 yang masih aktif.** Tiga kemunculan `67` yang tersisa semuanya berlabel
`67 ke 68` dalam konteks riwayat — itu benar dan justru dibutuhkan agar B7-01 dari batch
lalu tidak hilang jejaknya. `tahap_14:9` menyebut 68 tanpa menyebut "B9-01" khusus; itu
**minor dan tidak saya naikkan**, karena `tahap_14` tidak pernah menyebut 67 juga. Dan
grep `67` di `_build_eda05.py` = **NOL**, jadi tidak ada komentar count basi tertinggal
di builder.

Pelajaran B7-01 **tidak terulang**: tidak ada klaim 68 yang isinya 67. Saya hitung AST,
saya tidak percaya dokumen.

## 9. R7 — determinisme figure dan klaim disclosure

**Hash 7 dari 7 COCOK** (`git hash-object`, dibaca ulang dari disk):

| Figure | SHA-1 aktual | Klaim | Byte | Dimensi IHDR |
|---|---|---|---|---|
| FIG-01 | `709db8ae0d64` | `709db8ae0d64` | 28.695 | 720x720 |
| FIG-02 | `e55fc1f5294b` | `e55fc1f5294b` | 31.344 | 720x720 |
| FIG-03 | `73d65368398b` | `73d65368398b` | 32.883 | 720x720 |
| FIG-04 | `3420bca32643` | `3420bca32643` | 31.927 | 840x540 |
| FIG-05 | `fedd896ff8a2` | `fedd896ff8a2` | 27.778 | 840x540 |
| FIG-06 | `124867c6620c` | `124867c6620c` | 21.101 | 840x540 |
| FIG-07 | `a90a16b0e40d` | `a90a16b0e40d` | 23.351 | 960x540 |

Ukuran dan dimensi yang diklaim `tahap_14:24-31` cocok semua. FIG-01..03 identik dengan
HEAD (`git rev-parse HEAD:...` menghasilkan hash yang sama), jadi nb05 tidak mem-bypass
skema D9. FIG-04..07 memang untracked, sehingga "IDENTIK" di `tahap_14:28-31` tidak bisa
diuji terhadap HEAD; yang bisa diuji — hash, ukuran, dimensi — cocok.

**Disclosure per-sel: TIDAK DAPAT DIVERIFIKASI, dan saya tidak menyamarkannya.**
Coder mengklaim sumber berubah hanya di json idx 16 dan 18, output hanya di sel Q6 dan
sel idx 9 (chunking stream). Untuk mengujinya saya butuh notebook pra-fix — dan
`2d8f600acade` **tidak ada** di Git (bagian 6). Jadi klaim itu saya tandai
**tidak terbukti, bukan terbukti**. Yang bisa saya pastikan: 19 dari 19 sel kode AST-identik
dengan builder dan 7 dari 7 sel markdown identik string (bagian 4), 0 error,
`execution_count` urut, 68 dari 68 assert. Itu konsisten dengan "perubahan semantis
hanya di dua sel", tapi tidak membuktikannya.

## 10. R8 — gate dijalankan ulang oleh auditor

**DILARANKAN ULANG oleh saya sendiri**, bukan diambil dari laporan coder:

| Gate | Perintah | rc | Output |
|---|---|---|---|
| Lint | `ruff check .` | 0 | `All checks passed!` |
| Format | `ruff format --check .` | 0 | `32 files already formatted` |
| Karakter asing | `scripts/check_foreign_chars.py` | 0 | `OK: 79 file discan, tidak ada karakter asing.` |
| Test | `pytest -q` | 0 | `157 passed in 1.23s` |

**`validate_data`: tidak dijalankan, dan alasan coder itu saya nilai SAH — dengan
bukti, bukan@Repository.** Alasan yang diklaim coder adalah "`src/data`/config tak
tersentuh" (`reaudit:26`). Saya periksa `src/data/validate_data.py`:

- Satu-satunya efek tulisnya `REPORTS_DIR / f"data_validation_{today}.md"` (`:521-523`).
  Tidak ada `to_parquet`, tidak ada `to_csv`; data mentah tidak dimodifikasi.
- Masukan gate itu raw MT5 plus `configs/data.yaml`. **Semua** file `src/data/` dan
  `configs/` ber-mtime `10:42:00` — di luar jendela Batch C (bagian 11).
- `reports/data_validation_2026-10-07.md` **sudah ada** (mtime `10:42:00`), jadi gate
  hari ini sudah terpenuhi sebelum Batch C mulai.

Artinya menjalankan ulang hanya akan menulis ulang path yang sama dengan isi yang sama:
nol sinyal baru, dengan risiko mengotori mtime file terlacak. Jadi **alasan coder sah dan
keputusan tidak menjalankannya benar**. Catatan jujur: saya **tidak** menjalankan ulang
karena read-only, jadi "isi akan identik" adalah deduksi dari `:521-523` plus mtime,
bukan hasil membandingkan dua file.

## 11. R9 — eksklusi dihormati

**TERVERIFIKASI.** Saya petakan seluruh repo berdasarkan mtime dalam jendela kerja
Batch C (setelah 10:50 pada 2026-10-07). Hasilnya **15 file**, dan setiap file bisa saya
namai:

| File | mtime | Siapa |
|---|---|---|
| `eda_nb05_audit_v1.md` | 11:18:01 | append audit Batch C (putaran lalu, punya saya) |
| `2026-10-07_fix-nb05-batchC.md` | 11:31:57 | prompt |
| `thoughts/ledgers/CONTINUITY_ses_ef0b.md` | 11:32:58 | ledger kontinuitas sesi (untracked, alat bantu) |
| `_build_eda05.py` | 11:41:47 | coder |
| FIG-04/05/06/07.png | 11:42:24 | coder (hasil rerun) |
| `eda_05_regimes.ipynb` | 11:42:25 | coder (hasil rerun) |
| `report.md` | 11:49:18 | coder |
| `laporan_tahap_11_regime.md` | 11:49:18 | coder |
| `laporan_tahap_12_sintesis.md` | 11:49:18 | coder |
| `laporan_tahap_14_figures.md` | 11:50:51 | coder |
| `2026-10-07_reaudit-batchC-fix-auditor.md` | 12:00:59 | prompt |
| `thoughts/ledgers/CONTINUITY_ses_eef7.md` | 12:05:16 | ledger kontinuitas sesi (untracked, alat bantu) |

Jadi isi yang benar-benar berubah oleh coder = **1 builder + 1 notebook + 4 dokumen
terlacak + 4 figure hasil rerun = 10 path**, yang cocok dengan "6 file berubah" yang
dilaporkan coder bila figure dihitung sebagai hasil turunan. Sisanya adalah 2 prompt,
audit lama, dan dua ledger kontinivitas untracked yang ditulis alat bantu — bukan
tangan coder. Tidak ada file lain di luar daftar itu. Secara khusus:

- **nb01 sampai nb04 tidak disentuh** — keempatnya mtime `10:42:00` (bulk EOL sync), di
  luar jendela. `eda_00_setup` dan `eda_04_swings_levels` yang muncul ` M` di
  `git status` juga `10:42:00`, jadi penandaan itu bukan dari Batch C.
- **Tidak ada rename** — entri `R` atau `RM` di `git status` adalah rename lama yang
  terjadi sebelum jendela ini.
- **`requirements.txt`, `.ai/*`, `reports/go/` tidak tersentuh** — semuanya `10:42:00`.
- **B8-01 tidak dikerjakan** — tidak ada pemulihan mtime; `tahap_14:34-37` justru
  menjelaskan kenapa dia tidak bisa.
- **B10-01 tidak dikerjakan** — `md()` (`:29-30`) dan `code()` (`:33-34`) masih
  dua baris tanpa docstring, persis seperti sebelum fix.
- **Ekstrak `_eda_common.py` tidak dikerjakan** — `variance_ratio` (`:463`) dan
  `fractal_mask` (`:599`) masih didefinisikan inline di builder, sesuai penundaan.
- **File audit tidak disentuh coder** — hash-nya `f7a5a9f8b894` saat Gate 0, identik
  dengan nilai yang diberikan initiator, dan mtime-nya 11:18:01, sebelum prompt fix
  dibuat pukul 11:31:57.

Coder keluar dari scope yang diberikan. Tidak ada kebocoran.

## 12. R10 — tiga temuan yang saya buktikan sendiri

Ketiganya saya uji dari aktual, bukan saya ambil dari dokumen.

### A1 — header `tahap_11:3` masih pin blob builder lama, menjadi TEMUAN BARU B9-03

`tahap_11:3` menulis `Builder: scripts/_build_eda05.py blob ba11f0792823...`. Aktual:
`dd3d684a5a95`. Provenansi builder **salah**. Yang membuat ini ironis: `tahap_11:4`
sudah benar (`2cb57ad9ec1a...`, 68 assertion) dan `tahap_11:5` sudah bercerita bahwa
`ba11f0792823` itu **"sebelumnya"** — jadi dokumen ini mengontradiksi dirinya sendiri
di baris 3 versus baris 5.

Mengapa saya rendah ke LOW, bukan MEDIUM seperti B8-03: di `tahap_11` jejaknya **masih
ada** (baris 5), jadi pembaca bisa pulih sendiri; di B8-03 jejaknya hilang total.
Satu field, satu file.

### A2 — chunking stream sel idx 9, TIDAK DAPAT DIVERIFIKASI

Klaimnya: output berubah di sel idx 9 karena chunking stream. Fakta aktual: sel idx 9
(`exec 7`) punya **2 output `stream`**, bukan 1 — jadi memang ada chunking. Tapi
**tanpa** notebook pra-fix saya tidak bisa membuktikan bahwa bentuk 2-chunk itu
*baru*, bukan sudah ada sebelumnya. Klaim yang bisa saya buktikan separuhnya:
gabungan teks sel idx 9 utuh dan koheren (`replica nb03 M15 (stratum A): ACF lag-1
(all) = 0.001793` sampai `n_no_gap M15-A = 75,038 bar`). Tidak ada indikasi teks terpotong
atau berantakan. Status: **tidak terbukti, dan tidak ada bukti yang bertentangan**.

### A3 — `tahap_14:28-31` mengubah mtime FIG-04..07, RIPPLE SAH, bukan temuan

Empat baris itu memang di luar scope F-B802 yang sempit. Tapi isinya **benar dan
terverifikasi**: mtime aktual keempat figure `2026-10-07 11:42:24` (identik dengan waktu
rerun, bagian 11), hash cocok, ukuran cocok, dan label `(baru; mtime diperbarui rerun
Batch C, hash IDENTIK)` jujur. Menandai mtime di baris yang sama saat angka lain tidak
berubah **lebih jujur** daripada membiarkan angka basi tanpa catatan. Saya terima
sebagai konsekuensi rerun yang disclosed.

## 13. Temuan baru

### B9-02 (LOW) — notebook kembali CRLF; klaim "LF" di `tahap_14:8` salah fakta

**Bukti.** `eda_05_regimes.ipynb` di disk: **1.663 CRLF, 0 lone-LF, 0 lone-CR** —
CRLF murni, 83.611 B. `tahap_14:8` menulis blob itu dengan anotasi
"(`git hash-object`, LF)" dan tabel hash titik-awal juga menandai "LF". Keduanya
**salah**. Bukti pendukung: `git hash-object --no-filters` = `529cbf2092a7`, tidak sama
dengan `git hash-object` = `2cb57ad9ec1a`; blob SHA-1 LF-normal = `2cb57ad9ec1a`.

**Penyebab, dan ini penting: bukan kesalahan Batch C.** `_build_eda05.py:1109` menulis
lewat `NB_PATH.open("w", encoding="utf-8")` — text mode tanpa `newline=`, jadi di
Windows Python `\n` menjadi `\r\n`. Pola yang **sama persis** ada di
`_build_eda01.py:677`, `_build_eda02.py:928`, `_build_eda03.py:835`, dan
`_build_eda04.py:1202`. Jadi ini **bug laten di kelima builder**, yang selama ini tertutup
oleh bulk EOL sync `10:42:00` yang pernah mengubah repo ke LF. Rerun Batch C membongkar
menutupan itu. Coder mengikuti pola proyek yang sudah ada; saya **tidak** menyalahkan dia.

**Mengapa LOW.** Tidak ada angka atau kesimpulan yang salah. `git hash-object` —
konvensi yang baru saja saya tetapkan di bagian 1 — **tetap cocok** dengan yang dipatok
di `tahap_14:7`, jadi jejaknya utuh. Commit berikutnya akan menormalkan ke LF dan hash
tetap sama. Satu kata yang salah di satu dokumen.

**Yang tidak bisa saya tepis: tidak ada gate yang menangkapnya.** `ruff format --check`
tetap rc=0 pada file CRLF (saya uji di salinan di luar repo). Hook `mixed-line-ending`
sudah dihapus 2026-10-05 (`.pre-commit-config.yaml:27-29`). Jadi file ini akan tetap CRLF
sampai ada yang menyentuhnya. Rekomendasi: `newline=""` di kelima builder, plus koreksi
satu kata di `tahap_14:8`. Keduanya di luar scope fix ini.

### B9-03 (LOW) — `tahap_11:3` provenance builder stale

Sudah diuraikan di bagian 12 A1. Kelas cacat sama dengan B8-03 (pin yang tidak
dimutakhirkan) tapi lebih ringan karena jejaknya masih ada di `tahap_11:5`.

## 14. Temuan yang saya batalkan sendiri

- **Draft pertama saya menuduh "regresi 11 sel"** setelah membandingkan string builder
  dengan source notebook. Itu salah baca. Setelah saya bandingkan `ast.dump()`, 11 dari
  11 identik — penyebabnya `ruff format` di `build()`. Saya batalkan; kalau saya
  laporkan apa adanya, itu temuan palsu.
- **Saya sempat hampir menaikkan B9-02 ke MEDIUM** dengan alasan "tahap_14 salah fakta
  soal EOL, sama seperti B8-03 salah fakta soal byte". Setelah saya cek substansinya: di
  B8-03 yang salah adalah **pengikat bukti**; di B9-02 pengikatnya (`git hash-object`)
  **benar**. Yang salah hanya keterangan tambahan. Saya tahan di LOW dan catat
  alasannya, supaya kalibrasi severity saya bisa diaudit.
- **Saya sempat hampir menyalahkan coder atas CRLF.** Tidak saya lakukan: kelima builder
  memakai pola tulis yang sama, dan notebook lain masih LF hanya karena belum di-rerun
  setelah bulk sync. Menyalahkan coder di sini akan jadi catatan palsu.

## 15. Yang belum diverifikasi (jujur, ditutup terbuka)

1. **Diff per-sel notebook pra-fix terhadap pasc-fix** — tidak bisa. `2d8f600acade` tidak
   ada di Git. Klaim "hanya idx 16 dan 18 berubah" tetap **tidak terbukti**.
2. **Chunking sel idx 9** — bentuk 2-stream terverifikasi, kemunculan barunya tidak.
3. **Keterbacaan visual FIG-04..07** untuk manusia — di luar audit tekstual. Dasar
   angkanya sudah terverifikasi (bagian 9).
4. **Angka Q1 sampai Q6** berasal nb00 sampai nb04 — tidak saya buka.
5. **`validate_data`**: tidak dijalankan — menulis laporan berdate di `reports/`, jadi di
 luar read-only; setelah itu saya buktikan sendiri bahwa keputusan itu benar (bagian 10).
6. **Kenaikan isi notebook (+755 B setelah normalisasi LF)** saya tahu angkanya tapi
   **tidak saya atribusi per-baris**, karena v1 tidak tersedia untuk dibandingkan. Yang
   saya pastikan: 19 dari 19 sel kode AST-identik dengan builder, jadi tidak ada
   perubahan semantik tersembunyi.

## 16. Self-audit 3x (adversarial)

1. **Correctness.** Semua angka dihitung ulang dari disk atau AST, bukan dari dokumen:
   68 assert via `ast.walk` per sel kode (bukan regex — pelajaran B7-01); 7 hash PNG
   via `git hash-object`; dimensi dari byte IHDR; 11 sel builder terhadap notebook via
   `ast.dump`; konvensi sel via pemetaan json idx, kode_sel, dan `execution_count` yang
   saya bangun sendiri; SHA-256 dengan `hashlib`; blob SHA-1 dihitung manual
   (`SHA1("blob <len>" + NUL + data)`) untuk membuktikan normalisasi EOL. Gate 0
   dijalankan **sebelum** artefak lain dibaca.

   **Bukti saya yang saya distroksi sendiri:** (a) tabel identitas v2 saya tulis ulang
   **setelah** satu skrip helper menghasilkan SHA-256 yang salah — penyebabnya `\0`
   tertulis sebagai dua karakter, bukan byte NUL; saya perbaiki dan hitung ulang seluruh
   kolom. (b) Draft pertama saya menuduh 11 sel regresi (bagian 14). (c) Angka +2.418 B
   notebook saya **awalnya** saya laporkan sebagai kenaikan isi; setelah diurai ternyata
   +755 isi plus +1.663 EOL. Salah baca kedua saya perbaiki.

2. **Bias.** Scope: hanya R1 sampai R10 plus B8-03, hanya 6 artefak plus dokumen ini. Saya
   tidak membuka nb01 sampai nb04, tidak mengulang temuan lama, tidak menilai metode.

   **Menolak menaikkan meski argumen meredakkan:** B9-02 saya tahan LOW meski "dokumen
   salah fakta" terdengar serius, karena argumen itu hanya sah kalau pengikatnya ikut
   salah — dan pengikatnya benar. Menolak menaikkan tidak selalu berarti menahan diri
   berlebihan; kadang memang itu yang terjadi kalau letak kerusakannya sudah dipetakan.

   **Menolak menurunkan meski bukti ada:** A2 dan R7 saya tulis "tidak terbukti" meski
   tidak ada bukti yang bertentangan. Ketiadaan bukti bukan bukti yang menguntungkan,
   dan di sini saya tidak punya blob untuk membuktikannya. Saya tidak mengarang
   "kemungkinan besar benar" untuk menutup celah.

   **Yang saya sengaja tidak lakukan:** tidak menaikkan B9-02 dengan alasan "notebook
   rusak". Isinya utuh — 19 dari 19 sel kode AST-identik dengan builder, 0 error,
   68 dari 68 PASS, dan `git hash-object` cocok dengan pin. Yang rusak hanya metadata
   EOL.

3. **Meta.** Objek benar? Ya — **6 blob pasca-fix** (builder, notebook, report, tahap 11,
   tahap 12, tahap 14). Gate 0 **7 dari 7** termasuk audit, dan setiap klaim di bagian 3
   sampai 12 saya rujuk ke `file:baris` atau output numerik yang bisa diulang. Append-only:
   isi lama utuh, tabel `:1819-1825` tidak saya sentuh, gaya LF. Tidak ada pipeline yang
   saya jalankan menulis ke sumber; satu-satunya tulisan saya adalah dokumen ini lewat
   skrip append biner yang memverifikasi ulang ukuran prefix dan hash prefix. Tidak ada
   commit. Batch berikutnya tidak dimulai.

## 17. Tabel Klaim & Bukti (R1–R10)

| Butir | Klaim | Status | Bukti |
|---|---|---|---|
| R1 | F-B804 endpoint `placebo_hl 0,4890-0,4922` + 2 fakta + label | TERVERIFIKASI | `_build_eda05.py:916-920`; output json idx 18 (`q6_hit_rate_placebo`); grep repo-wide literal lama = nol di 6 blob pasca-fix |
| R2 | Notebook hasil regenerate builder, bukan edit manual | TERVERIFIKASI | 26 sel (19 kode/7 md) dua sisi; 11 beda source → **11/11 `ast.dump()` identik**; md 7/7 identik string; `ruff format --check` notebook rc=0 |
| R3 | `tahap_12` sinkron, kesimpulan Q6 tidak bergeser | TERVERIFIKASI | `tahap_12:100-102`; `report.md:73`; `_build_eda05.py:909,933`; `tahap_12:111` |
| R4 | F-B802 patok blob penuh + konvensi json idx | TERVERIFIKASI | `tahap_14:7-10` (blob cocok `2cb57ad9ec1a`), `:16-17`, `:41-52`; pemetaan aktual idx 22=#17/exec17, idx 23=#18/exec18; `git cat-file -e` 6 blob lama rc=128 |
| R5 | Tepat satu assert `hour_utc`, logikanya menangkap 4 kerusakan | TERVERIFIKASI | AST: 68 assert, 1 memuat `hour_utc`, di idx 16 top-level; `_build_eda05.py:808-813` sesudah `:807` |
| R6 | Count 68, 0 error, exec 1..19, tanpa 67 basi | TERVERIFIKASI | AST 68; 0 output error; `report.md:15`, `tahap_11:4/106/108`, `tahap_14:9`; grep `67` di builder = nol |
| R7 | 7 hash figure cocok; disclose per-sel | TERVERIFIKASI; disclose **tidak terbukti** | 7/7 SHA-1 + byte + IHDR cocok; disclose per-sel **tidak terbukti** (`2d8f600acade` tidak ada di Git) |
| R8 | 4 gate dijalankan ulang auditor | TERVERIFIKASI | `ruff check` rc=0; `ruff format --check .` 32 file; `check_foreign_chars.py` 79 file; `pytest -q` 157 passed. `validate_data` tidak dijalankan — **alasan coder dinilai SAH** (bagian 10) |
| R9 | Eksklusi dihormati | TERVERIFIKASI | 15 file dalam jendela mtime, semua teridentifikasi; nb01–nb04 `10:42:00`; `md()`/`code()` `:29-34` tanpa docstring; `variance_ratio:463`, `fractal_mask:599` masih inline |
| R10 | A1 stale header → **B9-03 LOW** | TERVERIFIKASI | `tahap_11:3` tulis `ba11f0792823` vs aktual `dd3d684a5a95`; bertentangan dengan `tahap_11:5` |
| R10 | A2 chunking sel idx 9 | TIDAK DAPAT DIVERIFIKASI | 2 output `stream`, teks gabungan koheren (`ACF lag-1 (all)` … `n_no_gap M15-A`); kemunculannya baru tidak dapat diuji tanpa blob pra-fix |
| R10 | A3 mtime FIG-04..07 | DITERIMA (ripple berlabel) | mtime `11:42:24` = waktu rerun; `tahap_14:28-31` berlabel dan angkanya benar |

## 18. VERDICT

| Temuan | Severity | Status |
|---|---|---|
| **F-B804** — endpoint `placebo_hl` di hulu | MEDIUM (wajib) | **TERVERIFIKASI TUTUP** |
| **F-B802** — rujukan sel `tahap_14` dipatok blob + konvensi | LOW (wajib) | **TERVERIFIKASI TUTUP** |
| **F-B901** — assertion regresi `hour_utc` | LOW (wajib) | **TERVERIFIKASI TUTUP** |
| **B8-04** (MEDIUM, Batch C) | MEDIUM | **TERTUTUP** (terverifikasi bagian 3) |
| **B8-03** (MEDIUM, Batch C) | MEDIUM | **TERTUTUP** (riwayat v0/v1/v2 + konvensi `git hash-object`) |
| **B9-01** (LOW, Batch C) | LOW | **TERTUTUP** (assert `hour_utc`, bagian 7) |
| **B8-02** (LOW, Batch C) | LOW | **TERTUTUP** (patokan blob, bagian 6) |
| **B8-01** | LOW | Dikecualikan — tetap terbuka |
| **B10-01** | LOW | Dikecualikan — tetap terbuka |
| **B9-02** (baru) | LOW | **TERBUKA** — notebook CRLF vs klaim "LF" di `tahap_14:8`; bug laten kelima builder |
| **B9-03** (baru) | LOW | **TERBUKA** — `tahap_11:3` provenance builder stale |

### VERDICT FIX BATCH C: LOLUS — 3 dari 3 wajib tertutup, 2 LOW baru. Tidak ada HIGH/CRITICAL/MEDIUM

Ketiga perbaikan wajib **tertutup dan terbukti**, bukan hanya diklaim. Yang paling
berpimpact adalah **B8-03**: tabel identitasnya bukan sekadar diperbarui, tapi diubah
bentuknya menjadi riwayat v0/v1/v2 plus konvensi integritas eksplisit — sehingga kelas
cacat yang sama tidak akan bisa muncul diam-diam di putaran berikutnya. Dan `F-B802`
menutup masalah traceability yang saya angkat sendiri di Batch C: sekarang tidak ada sel
yang disebut tanpa blob, dan konvensinya bisa diuji silang ke `tahap_12`.

Dua LOW baru **bukan hasil kerja coder** dan saya nyatakan terbuka: B9-02 adalah bug
laten di kelima builder yang baru terlihat karena rerun, dan B9-03 adalah header
provenance yang tertinggal karena di luar scope. Keduanya tidak merusak angka, tidak
membalikkan kesimpulan, dan tidak merusak jejak bukti.

**Tidak ada temuan MEDIUM atau lebih tinggi pada putaran ini.** Klaim disclosure per-sel
R7 dan A2 tetap **tidak terbukti** — bukan karena ada yang salah, tetapi karena blob
pra-fix tidak ada di Git. Saya lebih memilih menandai itu terbuka daripada mengarang
verifikasi.

### VERDICT BATCH C MUTAKHIR: LULUS DENGAN CATATAN — 0 MEDIUM terbuka

Batch C ursprüngnya LULUS DENGAN CATATAN dengan **2 MEDIUM + 4 LOW**. Sesudah fix ini:

| Kelas | Jumlah terbuka | Rincian |
|---|---|---|
| HIGH/CRITICAL | **0** | — |
| MEDIUM | **0** | B8-03 dan B8-04 tertutup |
| LOW | **4** | B8-01, B10-01 (dikecualikan, tetap terbuka) + B9-02, B9-03 (baru) |
| Tervalidasi tertutup | 7 | F-B804, F-B802, F-B901, B8-03, B8-04, B9-01, B8-02 |

Tidak ada lagi MEDIUM. Empat LOW tersisa **semuanya LOW**, dan dua di antaranya (B8-01,
B10-01) sudah dikecualikan eksplisit oleh prompt (`reaudit:3`). B9-02 dan B9-03 saya
serahkan ke prompt fix terpisah — keduanya satu-dua baris, keduanya tanpa dampak angka,
dan keduanya butuh tindakan berbeda: B9-02 menyentuh lima builder (di luar scope ini),
B9-03 menyentuh satu baris dokumen (bisa masuk scope mana pun).

## STOP — Menunggu perintah Batch berikutnya

Tidak ada commit. Sumber read-only. Satu-satunya file yang saya tulis adalah dokumen
audit ini (append-only). Batch berikutnya hanya atas perintah terpisah
(`PERAN-auditor.md:38`).
## Identitas dokumen audit PASCA-APPEND

Nilai di bawah dihitung **setelah** append bagian 0 sampai 18 selesai, atas file tepat
pada saat itu — **sebelum** blok ini ditambahkan. Karena itu hash di sini tidak
menggambarkan file final; ia menggambarkan file pada akhir bagian 18. Menambahkan blok
ini mengubah hash itu, dan itu wajar pada dokumen yang mencatat hash dirinya sendiri.
Untuk verifikasi file final, jalankan ulang:

```
git hash-object reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md
```

| Properti | Nilai |
|---|---|
| `git hash-object` (akhir bagian 18) | `7e3b0294aadd6d83091d33d93d7d87b2f5aa9622` |
| SHA-256 (akhir bagian 18) | `c8270c8b5cfdfda84d84516c4233168f25edbfda4dbf9260874cc989de694e64` |
| Byte (akhir bagian 18) | 216,605 |
| Baris (akhir bagian 18) | 3,514 |
| Prefix pra-append | 183.892 B, `f7a5a9f8b894`, 2.964 baris — **utuh** |
| CR | 0 — LF penuh, gaya file asal dipertahankan |
| Gate pasca-append | `check_foreign_chars.py` rc=0, 79 file discan |
| Commit | tidak ada |

Blok ini menutup putaran. Batch berikutnya hanya atas perintah terpisah.
---

# KONFIRMASI A3 UNTUK AUDITOR — status `tahap_14:28-34` (mtime FIG-04..07)

Putaran ini **read-only terhadap sumber**: DILARANG rerun builder/nbconvert, DILARANG
nb01-nb04 sebagai bukti, DILARANG commit. Satu-satunya tulisan saya adalah dokumen ini
(append-only). Data mtime dibaca dari `os.stat` di disk, bukan dari dokumen.

## Gate 0 — verifikasi hash titik-awal dulu

| Objek | Hash titik-awal | Aktual | Byte | Status |
|---|---|---|---|---|
| `eda_nb05_audit_v1.md` | `2308e005f2b9c3f63e140d2c48789afc1fc9a58e` | sama | 217.702 / 3.539 baris / LF penuh, CR=0 | **7/7 LOLOS** |
| `laporan_tahap_14_figures.md` | `b4269a97361d3a7414cb6cc60c95852ef29dbc22` | sama | 4.184 | **LOLOS** |
| FIG-04..07 | 12-char klaim | identik | lihat (a) | **LOLOS** |

Tidak ada mismatch → lanjut. Tidak ada yang perlu STOP.

## Q-A3 — Tabel Klaim & Bukti

### (a) Apakah mtime aktual FIG-04..07 cocok dengan `:28-31`?

| File | Klaim `:28-31` | Aktual `os.stat` | Hash 12 | Ukuran | Status |
|---|---|---|---|---|---|
| FIG-04.png | `11:42:24 2026-10-07` | `2026-10-07 11:42:24` | `3420bca32643` ✓ | 31.927 ✓ | **COCOK** |
| FIG-05.png | `11:42:24 2026-10-07` | `2026-10-07 11:42:24` | `fedd896ff8a2` ✓ | 27.778 ✓ | **COCOK** |
| FIG-06.png | `11:42:24 2026-10-07` | `2026-10-07 11:42:24` | `124867c6620c` ✓ | 21.101 ✓ | **COCOK** |
| FIG-07.png | `11:42:24 2026-10-07` | `2026-10-07 11:42:24` | `a90a16b0e40d` ✓ | 23.351 ✓ | **COCOK** |

**4 dari 4 cocok**, termasuk kolom hash dan ukuran di baris yang sama — bukan cuma mtime.

**Konteks yang harus jujur disebut:** baris `:25-27` (FIG-01..03) mengklaim mtime
`15:49:27`, sedangkan aktual `2026-10-07 10:42:00` — **TIDAK COCOK**. Ini bukan temuan
baru dari putaran ini: `:34-37` sudah menyatakannya terbuka dan menolak memperbaruinya
karena B8-01 dikecualikan (bulk EOL sync `10:42:00` menetralkan mtime sebagai bukti).
Saya menghitung ulang agar statusnya jelas, lalu **tidak** mengulang informasi yang
sama dua kali.
### (b) Apakah hash FIG-04..07 benar identik dengan klaim (tidak berubah isi)?

**Dua sub-pertanyaan, jawabannya berbeda — saya tidak menyamakan keduanya.**

**b1. "Isi saat ini = hash yang ditulis" → TERVERIFIKASI.**
Byte PNG saya baca sendiri lalu saya hitung sebagai objek Git
(`SHA1("blob <len>" + NUL + data)`), bukan sekadar percaya `git hash-object`:

| File | hash Git (hitung ulang) | hash klaim `:28-31` | SHA-256 (16) |
|---|---|---|---|
| FIG-04 | `3420bca32643` | `3420bca32643` ✓ | `b47ba5db0ef77d91` |
| FIG-05 | `fedd896ff8a2` | `fedd896ff8a2` ✓ | `4aa62169c60a669d` |
| FIG-06 | `124867c6620c` | `124867c6620c` ✓ | `98bd42982e8a6ca4` |
| FIG-07 | `a90a16b0e40d` | `a90a16b0e40d` ✓ | `e76b7c5da5d1e6a1` |

Hitungan manual = `git hash-object` untuk keempat file → tidak ada filter yang
mengubah isi (PNG biner, `text=auto` tidak menyentuhnya).

**b2. "Isi tidak berubah dibanding sebelum rerun" → KORROBORASI, BUKAN BUKTI BYTE.**
Empat catatan yang mtime-nya `10:42:00` — jauh **sebelum** jendela kerja Batch C
(`11:41:47`) — sudah menulis keempat hash yang sama:
`.ai/assistant/prompts/2026-10-06_audit-klenz_nb05.md`,
`.ai/assistant/prompts/2026-10-06_onboarding-auditor-baru_nb05.md`,
`.ai/assistant/verifications/2026-10-06_nb05_final.md`. Konsistensi silang empat catatan
sebelum-jendela = bukti yang kuat bahwa isi tidak berubah.

**Tapi batasnya saya nyatakan terang:** (i) tidak ada satu pun salinan byte FIG-04..07
di luar `reports/eda/2026-10-06/figures/` — saya telusuri seluruh worktree, hasilnya
tepat 4 file dan semuanya di lokasi itu; (ii) FIG-04..07 **untracked**, dan `tahap_14`
juga untracked, jadi tidak ada riwayat Git untuk dibandingkan; (iii) bukti bahwa *kode
sel figure* tidak berubah tidak bisa saya peroleh karena blob pra-fix `2d8f600acade`
hilang (bagian 15 audit utama). Jadi "hash IDENTIK" **akurat dan berkoroborasi**, tapi
bentuk bukti terkuat yang ada hari ini adalah **tekstual, bukan byte-level**. Saya tidak
meningkatkan ini jadi "terbukti-penuh".

### (c) Apakah kausalitasnya benar — rerun nb05 yang menulis file itu?

**TERBUKTI, bukan kemungkinan.** Empat bukti independen:

1. **Sekitar berkas.** Seluruh repo (`.git`/`venv`/`cache` dikecualikan) saya telusuri
   untuk tulisan pada `11:42:21`–`11:42:29`. Hanya **5 file**: FIG-04, FIG-05, FIG-06,
   FIG-07 (`11:42:24`) dan `eda_05_regimes.ipynb` (`11:42:25`). Tidak ada proses lain
   yang menulis apa pun saat itu.
2. **Urutan waktu** persis seperti `python _build_eda05.py` → nbconvert:

   | Jam | File | Peran |
   |---|---|---|
   | 11:41:47 | `scripts/_build_eda05.py` (52.203 B) | builder ditulis coder |
   | 11:42:24 | FIG-04 → FIG-07 (rentang 323 ms) | sel idx 22 `savefig` |
   | 11:42:25 | `eda_05_regimes.ipynb` (83.611 B) | nbconvert menulis .ipynb |

   Empat selisih antar-`savefig` = **152,1 / 79,5 / 91,6 ms** (total 323 ms) — pola
   empat tulisan berurutan dalam satu proses. Bandingkan bulk sync `10:42:00` yang
   berjarak ~4,1 dan ~4,6 s. Bedanya nyata, jadi ini bukan salinan massal.
3. **Kode sel json idx 22** menulis tepat empat nama itu dan tidak lebih:
   baris 33/34, 47/48, 63/64, 75/76 masing-masing
   `path = FIGURE_DIR / "FIG-0X.png"` lalu `fig.savefig(path, dpi=120)` untuk X = 04–07;
   `FIGURE_DIR` didefinisikan di idx 2 = `PROJECT_ROOT / "reports/eda/2026-10-06/figures"`.
   Output sel idx 22 (exec 17) memuat empat baris
   `tersimpan: reports\eda\2026-10-06\figures\FIG-0X.png`.
4. **Tidak ada penulis lain.** Scan seluruh worktree (bukan `git grep` — yang melewatkan
   untracked) menemukan hanya **dua** file yang menyebut FIG-04: notebook itu sendiri dan
   `scripts/_build_eda05.py` yang menghasilkannya. Tidak ada `.py`/`.bat` lain yang menulis
   nama FIG-0X ke folder tersebut.

**Satu bukti tambahan yang saya ambil dari sini:** `st_ctime` (creation time Windows) keempat
file tetap `2026-10-07 10:42:00` — tidak berubah saat rerun. Artinya file **ditimpa di
tempat**, bukan dibuat ulang. Ini justru **menguatkan** label "mtime diperbarui": yang
diubah hanya `mtime`, isi tetap. (Kalau file baru dibuat, `ctime` akan ikut `11:42:24`.)

## PUTUSAN: **CATATAN** — diterima, tanpa temuan baru

Bukan DITERIMA tanpa catatan, karena ada dua hal yang perlu tercatat supaya Findings
Bukan DITERIMA tanpa catatan, karena ada dua hal yang perlu tercatat supaya penemuan

1. **Batas kekuatan bukti "hash IDENTIK"** (b2): akurat dan berkoroborasi oleh empat
   catatan pra-jendela, tapi tanpa salinan byte pra-rerun maupun riwayat Git, dan
   diff per-sel pra-fix tidak dapat dilakukan. Bentuknya: **teks**, bukan **byte**.
   Kalau suatu saat ada yang menawarkan "hash IDENTIK" hanya dengan satu catatan, itu belum
   cukup untuk ukuran keyakinan yang sama.
2. **Kata "baru" di label `:28-31` agak longgar.** `st_ctime` membuktikan file sudah ada
   sebelum rerun (lahir `10:42:00`), jadi yang "baru" hanyalah nilai `mtime`/baris
   dokumennya, bukan file-nya. Tidak merusak apa pun, tapi kalau kata "baru" dibaca
   sebagai "file baru dibuat", itu tidak tepat. Saran: tulis "mtime diperbarui" saja
   tanpa "baru". Dua kata — masuk scope mana pun nanti.

**Bukan TEMUAN LOW baru**, dan saya nyatakan alasannya: tidak ada satu pun `file:baris`
di `:28-31` yang salah fakta. Yang bermasalah hanya baris `:25-27` (FIG-01..03), dan itu
persis B8-01 yang sudah dikecualikan serta sudah didisclose di `:34-37`. Menghitungnya
lagi sebagai temuan baru akan menjadi penghitungan ganda atas temuan yang sama.

**Preseden yang saya catat:** "ripple berlabel diizinkan" punya contoh terverifikasi —
ketiga — `tahap_14:28-31` (baris data mtime diperbarui, isi dan hash dipertahankan,
alasan ditulis di baris yang sama, bagian luar scope F-B802 dinyatakan terang). Ripple
yang label dan angkanya benar **tidak otomatis jadi temuan**; yang menentukan adalah
apakah angkanya cocok dengan disk dan apakah labelnya jujur soal apa yang berubah.

## Self-audit 3x (adversarial)

**Putaran 1 — Correctness.** Semua angka dihitung ulang dari disk atau dari byte sumber:
mtime/ctime/ino/dev via `os.stat`; hash dihitung ulang dengan `SHA1("blob <len>"+NUL+data)`
dan dicocokkan ke `git hash-object`; SHA-256 via `hashlib`; telusur seluruh repo via walk;
worktree; baris kode sel dari JSON notebook; Gate 0 diverifikasi sebelum artefak lain.
**Dua kesalahan saya sendiri yang saya batalkan:**
(a) skrip pertama saya gagal `assert` karena membandingkan `git hash-object` dengan
SHA-1 mentah — `git hash-object` adalah hash *objek Git* (`"blob <len>"+NUL+data`),
bukan hash isi. Assertion saya salah, datanya tidak; saya perbaiki hitungannya dan
hasilnya cocok untuk keempat file.
(b) saya sempat memakai `git grep` untuk mencari penulis FIG-04; perintah itu **melewatkan
file untracked**, termasuk `_build_eda05.py` yang justru aku cari. Saya ganti dengan
walk worktree, dan kesimpulannya ikut berubah (bukan "tidak ada penulis", tapi "dua
penulis: notebook + generator-nya"). Kesimpulan yang benar sering datang dari
memperbaiki alatnya sendiri.

**Putaran 2 — Bias.** Tidak menghukum inisiatif transparan. Coder justru menyentuh baris
di luar scope F-B802 — dan itu **berlebihan** kalau tidak berlabel; di sini label ada di
baris yang sama, angkanya saya konfirmasi benar 4 dari 4, dan alasan batasannya ditulis
terbuka. Mematahkan inisiatif seperti ini justru mendorong coder menyembunyikan
batch berikutnya. Sebaliknya saya tidak memaklumi begitu saja: dua catatan di atas saya
tulis justru supaya klaim serupa di masa depan tidak terdengar lebih kuat dari yang
bisa dibuktikan. Saya juga menahan diri tidak menaikkan ke temuan LOW yang sebenarnya
sudah tercatat di B8-01 — menghitungnya lagi akan menggandakan hitungan LOW dan
menutupi temuan yang asli.

**Putaran 3 — Meta.** Objek benar? Ya: hanya FIG-01..07, `tahap_14`, notebook idx 22/23,
dan dokumen ini. Hanya file ini yang saya tulis — append-only, prefix 217.702 B diverifikasi
ulang sebelum menulis; tidak ada commit, tidak ada push; tidak ada batch fix B9-02/B9-03
yang dimulai; tidak ada rerun builder atau nbconvert.
## STOP

Hash pasca-append dihitung setelah tulis final dan dilaporkan di pesan penutup chat,
mengikuti konvensi lampiran `:2961-2964` — menulis hash sendiri ke dokumen yang sedang
dihash membuat angkanya tidak pernah benar. Batch berikutnya (termasuk fix B9-02/B9-03)
hanya atas perintah terpisah.

---

# RE-AUDIT FIX B9-02 + B9-03 (label dokumen saja) — F-B902 + F-B903

Peran: **AUDITOR**. Read-only terhadap sumber; satu-satunya tulisan dokumen ini
(append-only). Tidak ada rerun builder/nbconvert, tidak ada commit.

## Titik-awal — dikorroborasi dari catatan saya sendiri

Klaim coder "5/5 hash titik-awal cocok" saya bandingkan dengan angka yang **saya**
ukur sendiri pada putaran sebelumnya (bukan dengan klaim coder):

| Objek | Klaim coder | Catatan saya sendiri | Coroborasi |
|---|---|---|---|
| `scripts/_build_eda05.py` | `dd3d684a…` | `dd3d684a5a95…` | **cocok** |
| `notebooks/scalping/eda_05_regimes.ipynb` | `2cb57ad9…` | `2cb57ad9ec1a…` | **cocok** |
| `laporan_tahap_11_regime.md` | `118baf14…` | `118baf140130…` | **cocok** |
| `laporan_tahap_14_figures.md` | `b4269a97…` | `b4269a97361d…` | **cocok** |
| `eda_nb05_audit_v1.md` | `e9e3e292…` / 228.064 B | `e9e3e2924882…` / 228.064 B / 3.710 baris | **cocok** |

Batch ini jadi benar-benar berlabuh pada keadaan yang saya ukur sendiri. Titik-awal sah.

## Tabel Klaim & Bukti (a) F-B902 · (b) F-B903

| # | Klaim coder | Status | Bukti (file:baris + output auditor) |
|---|---|---|---|
| 1 | **F-B903** `tahap_11:3` pin builder → `dd3d684a5a95…` + label KOREKSI B9-03 | **TERVERIFIKASI** | `tahap_11:3` berbunyi `blob `dd3d684a5a95…` (KOREKSI B9-03, 2026-10-07: pin builder dimutakhirkan ke blob aktif pasca Batch C; pin basi `ba11f0792823…` tetap tercatat sebagai riwayat di baris KOREKSI Batch C)`. Prefix yang ditulis **benar** (12 char, cocok dengan `git hash-object`) |
| 2 | `tahap_11:5` (riwayat "sebelumnya") tak tersentuh | **TERVERIFIKASI** | byte-level: file naik 8.621 → 8.788 B (**+167 B**) dan jumlah baris **tetap 108** — tidak ada baris yang hilang, jadi `:5` utuh |
| 3 | **F-B902** `tahap_14:8` klaim EOL → `EOL aktual **CRLF**` + KOREKSI B9-02 | **TERVERIFIKASI** | `tahap_14:8` berbunyi `2cb57ad9ec1a… (`git hash-object`, EOL aktual **CRLF** — KOREKSI B9-02, 2026-10-07)`. Pin blob 40-char **tidak** berubah |
   `LF`/`CRLF`/`EOL` = hanya `:8`, catatan koreksi, dan satu penyebut B8-01 yang tidak terhubung |
| 5 | Fakta EOL: 83.611 B = 1.663 CRLF + 0 LF-only | **TERVERIFIKASI** | hitung byte ulang dari disk: byte **83.611**, CRLF **1.663**, LF-only **0**, CR-only **0** |
| 6 | Fakta (a): binding hash tetap benar (LF-normalized) | **TERVERIFIKASI** | uji empiris ulang: hash konten LF = `2cb57ad9ec1a…` = `git hash-object`; hash raw CRLF = `529cbf2092a7…` ≠. Normalisasi EOL memang tidak merusak pin |
| 7 | Fakta (b): akar di 5 builder tanpa `newline=` | **TERVERIFIKASI** | `_build_eda01.py:677`, `_build_eda02.py:928`, `_build_eda03.py:835`, `_build_eda04.py:1202`, `_build_eda05.py:1109` — kelimaanya `with NB_PATH.open("w", encoding="utf-8") as handle:`, nol `newline=`. **Nomor baris persis seperti klaim** |
| 8 | `tahap_14` +665 B = 1 baris patokan + 9 baris catatan | **TERVERIFIKASI** | 4.184 → 4.849 B = **+665 B**; baris 66 → 75 = **+9** |
| 9 | Hash baru `tahap_11` / `tahap_14` | **TERVERIFIKASI** | `97cf27e111964b830e3e6dcb6d40e85af142f11e` (8.788 B) dan `bf20587df9f7918f577202e434faf182316acfdd` (4.849 B) — keduanya cocok byte-for-byte |
| 10 | 6 blob + audit tak tersentuh | **TERVERIFIKASI** | builder `dd3d684a5a95…`, nb05 `2cb57ad9…`, report `afeb1b1cb0d…`, tahap_12 `094d90d2…`, tahap_13 `ad6652b7…`, audit `e9e3e292…` — 6/6 identik. FIG-01..07 juga 7/7 identik |
| 11 | Hanya 2 file `.md` yang ditulis | **TERVERIFIKASI** | telusuri seluruh worktree untuk mtime > 12:56: hanya 5 file — 2 prompt (13:04, alat bantu), audit (13:01 = append A3 **milik saya**), dan `tahap_11` + `tahap_14` (13:11:09). Tidak ada file lain |
| 12 | EOL kedua `.md` tetap pure LF | **TERVERIFIKASI** | `tahap_11` CRLF=0, LF-only=108; `tahap_14` CRLF=0, LF-only=75; CR-only=0 keduanya |
| 13 | Gate `check_foreign_chars.py` rc=0 | **TERVERIFIKASI** | saya jalankan sendiri: rc=0, `OK: 79 file discan, tidak ada karakter asing.` |
| 14 | Tidak ada commit/push | **TERVERIFIKASI** | HEAD tetap `cb08cd5`; reflog `HEAD@{0}` masih commit lama, tidak ada entri baru |

**Sapu-bersih — hitung ulang presisi (auditor).** Semua pin basi tersisa **bersifat
riwayat**, tidak satu pun merujuk artefak aktif:

| Lokasi | Kemunculan | Sifat |
|---|---|---|
| `tahap_11:3` | 1 (`ba11f0792823…`) | riwayat — disebut eksplisit di dalam catatan KOREKSI B9-03 |
| `tahap_11:5` | 2 (`ba11f0792823…` + `2d8f600acade…`) | riwayat ("sebelumnya") |
| `tahap_12:7` | 1 (`2d8f600acade…`) | riwayat ("sebelumnya") |
| `tahap_14:59` | 1 (`2d8f600acade…`) | riwayat (`git cat-file -e` → tidak ada) |
| `report.md` | **0** | tidak disentuh — sesuai klaim |

**Hitungannya: 4 baris berisi pin, 5 kemunculan pin.** Laporan coder menyebut "4
kemunculan" — angka itu menghitung **baris**, sedangkan tabelnya memetakan **5
kemunculan**. Isinya lengkap, hanya basis hitungnya tidak disebut. Catatan kecil,
bukan temuan.

## CATATAN — hash builder di laporan coder tidak valid (TIDAK masuk file)

Di tabel "Konfirmasi 6 blob" laporan chat, coder menulis hash builder sebagai:

| | Nilai |
|---|---|
| Ditulis coder | `dd3d684a9513a379693b406ee329969d3bd541` — **38 karakter** |
| Aktual (`git hash-object`) | `dd3d684a5a9513a379693b406ee329969d3bd541` — **40 karakter** |

Selisihnya karakter `5a` hilang setelah `dd3d684a`, sehingga geser semua digit
berikutnya. Konsekuensinya bukan cuma "salah ketik": **prefix 12 karakter yang ditulis
(`dd3d684a9513`) juga tidak cocok** dengan yang asli (`dd3d684a5a95`), jadi tanda
`centang hijau` di baris itu **tidak bisa berasal dari perbandingan nyata** — string 38 karakter
mustahil sama dengan keluaran `git hash-object`.

**Mengapa ini CATATAN, bukan TEMUAN.** Aturan audit repo ini menuntut setiap temuan
berupa `file:baris` + angka; cacat ini **tidak ada di file mana pun** — saya grep
seluruh worktree (termasuk `.ai/`, `thoughts/`, `reports/`) dan hasilnya **0
kemunculan** untuk prefix `dd3d684a9513` maupun string 38 karakter itu. Pin yang
benar justru ada di file: `tahap_11:3` memakai `dd3d684a5a95…` yang **tepat**. Jadi
artefaknya bersih; yang cacat hanya laporan chat.

**Residu risikonya saya catat:** string yang tidak valid ini sekarang hidup di arsip
percakapan. Kalau nanti disalin ke dokumen sebagai pin, kelas cacatnya persis B8-03
(pin yang tidak cocok) — dan B8-03 justru kita tutup_batch ini karena sekarang sudah
ada konvensinya. Nilai yang benar untuk dipakai: `dd3d684a5a9513a379693b406ee329969d3bd541`.

## VERDICT

| Temuan | Severity | Status |
|---|---|---|
| **F-B902** — `tahap_14:8` klaim EOL salah (`LF` → `CRLF`) | LOW (wajib) | **TERVERIFIKASI TUTUP** |
| **F-B903** — `tahap_11:3` provenance builder stale | LOW (wajib) | **TERVERIFIKASI TUTUP** |

### VERDICT FIX B9-02 + B9-03: **LOLUS** — 2 dari 2 wajib tertutup, tanpa temuan baru

Kedua perbaikan bukan sekadar menempelkan label: angkanya **saya hitung ulang dari disk
dan cocok** (83.611 B / 1.663 CRLF / 0 LF-only; prefix builder tepat; nomor baris kelima
builder tepat), dan delta byte-nya cocok dengan klaim (+167 B dan +665 B) tanpa baris
yang hilang. B9-02 ditutup dengan akar masalah yang menyebut lima file, bukan hanya satu —
sedangkan perbaikannya sengaja ditunda dan dinyatakan terbuka, bukan disembunyikan.

**Yang tersisa terbuka, tidak berubah:** B8-01 (dikecualikan), B10-01 (dikecualikan),
dan bug laten `newline=` di kelima builder yang kini **tereksplisit di `tahap_14:13-18`**
sebagai pekerjaan tertunda. Penundaan yang tertulis lebih baik daripada perbaikan yang
diam-diam keluar dari scope.

**Batch C mutakhir tetap: 0 MEDIUM terbuka, 4 LOW terbuka** — tidak ada temuan baru
yang ditambahkan putaran ini.

## Self-audit 3x (adversarial)

**Putaran 1 — Correctness.** Semua angka dihitung ulang dari disk: hash lewat
`git hash-object`, EOL lewat hitung byte (`CRLF`/`LF-only`/`CR-only` dipisah, bukan
`grep -c` yang bisa false-positive seperti yang terjadi di sesi coder), EOL notebook
lewat penghitungan ulang `LF-normal` vs `raw` dari byte asli, nomor baris builder dari
isi file, sweep pin dari penelusuran seluruh worktree, gate dari eksekusi saya sendiri.
Titik-awal batch dikorroborasi terhadap catatan saya sendiri, bukan terhadap klaim
**Bukti saya yang saya distroksi sendiri:** saya sempat menyalin string hash salah ketik itu
ke skrip saya sendiri, dari laporan coder — itu membuat skrip saya menandai builder sebagai GAGAL.
Setelah saya periksa, **yang salah adalah string di laporan coder, bukan datanya**;
saya hampir melaporkannya sebagai temuan. Ternyata hanya salah ketik di chat. Kalau saya
tidak telusuri apakah string itu masuk file, saya akan melaporkan temuan palsu terhadap
artefak yang sebenarnya benar.

**Putaran 2 — Bias.** Dua tarikan yang saya tolak. Pertama, godaan menaikkan string hash
salah di laporan chat menjadi TEMUAN LOW — padahal aturan repo sendiri mensyaratkan
`file:baris`, dan tidak ada file yang terdampak; menaikkaninya cuma menambah LOW
palsu dan menutupi B9-02/B9-03 yang memang sudah tertutup. Kedua, godaan menyalahkan
karena kesalahannya sangat kecil — ini bukan kelalaian: 7 dari 8 hash benar, delta byte cocok,
sweep lengkap, dan gate dijalankan dua kali; satu string salah ketik di tabel konfirmasi
adalah kekeliruan manusia, bukan pelanggaran scope. Yang saya lakukan adalah mencatatnya
apa adanya beserta nilai yang benar, supaya tidak diwariskan ke batch berikutnya.

**Putaran 3 — Meta.** Objek benar? Ya: dua `.md` yang dikoreksi, notebook, kelima
builder, `report.md`, tahap_12, tahap_13, audit, dan 7 PNG. Hanya dokumen ini yang saya
tulis, append-only, prefix 228.064 B diverifikasi ulang sebelum menulis; tidak ada
commit atau push; tidak ada batch berikutnya yang dimulai; tidak ada NB01–nb04 dibuka;
tidak ada rerun builder maupun nbconvert.

## STOP

Hash pasca-append dihitung setelah tulis final dan dilaporkan di pesan penutup chat
(konvensi lampiran `:2961-2964`). Batch berikutnya hanya atas perintah terpisah.
---

# RE-AUDIT FIX F-NL + F-NL2 (akar masalah `newline=` ditutup)

Peran: **AUDITOR**. Read-only terhadap sumber; satu-satunya tulisan dokumen ini
(append-only). Nol rerun builder, nol nbconvert, nol commit.

## Titik-awal — angka milik saya sendiri

Gate 0 saya uji terhadap hash yang **saya** ukur setelah append F-B902/F-B903
sendiri, bukan terhadap klaim coder:

| Objek | Angka saya (turno lalu) | Sekarang | Hasil |
|---|---|---|---|
| `eda_nb05_audit_v1.md` | `4eafbdb2eb6e…` / 238.097 B / 3.851 baris | identik | audit **tak tersentuh** |

## Tabel Klaim & Bukti

| # | Klaim coder | Verdict | Bukti auditor |
|---|---|---|---|
| 1 | 5/5 hash builder | **LULUS** | `_build_eda01` `5ba47ba8ae95`/34.167 B · `eda02` `05b6c26bbb0a`/41.019 B · `eda03` `27e801c1709d`/36.905 B · `eda04` `641210e72b63`/48.763 B · `eda05` `e29e18c7eb98`/52.627 B — 5/5 hash **dan** ukuran cocok |
| 2 | nb05 `661c0aeb2357`, 81.851 B | **LULUS** | hash dan ukuran cocok; hitung byte sendiri: `bytes=81851 CRLF=0 CR=0 LF_only=1656` |
| 3 | 4 dokumen (hash + CRLF=0) | **LULUS** | `report.md` `f529da8f4e7c`/12.488 B · `tahap_11` `09d78431c1a1`/9.058 B · `tahap_12` `6555c1be97f2`/9.430 B · `tahap_14` `fa3a21705e5a`/5.149 B — CRLF=0 keempatnya |
| 4 | Audit `4eafbdb2eb6e` tak tersentuh | **LULUS** | hash, byte, dan baris identik dengan angka saya sendiri |
| 5 | **Item 2** — teks output gabungan identik | **LULUS** | ini inti, saya hitung ulang dari snapshot `D:/_nl_batch_snap/pra_nl2_eda_05_regimes.ipynb`: **26 dari 26 sel** punya teks gabungan identik; `source` identik di semua sel; urutan `cell_type` identik; 0 output error |
| 6 | Merge chunking sel idx 9 (56+383 = 439) | **LULUS** | pra = 2 output stream `[56, 383]`, post = 1 output stream `[439]`; teks gabungan 439 = 439 **identik**; 5 karakter terakhir sama-sama `'turn\n'` |
| 7 | **Item 3** — invarian struktural | **LULUS** | 26 sel -> 26 sel; `cell_type` urut identik; `source` identik; `execution_count` berubah **0** sel; 0 output error |
| 8 | **Item 4** — assertion 68 (bukan 67) | **LULUS** | hitung sendiri dari isi sel: **68**; sebaran per sel `3,4,9,6,6,1,10,7,5,1,4,1,3,3,2,1,1,1` — sama persis dengan klaim. `report.md:15` = 68 |
| 9 | **Item 5** — FIG-04..07 identik pin | **LULUS** | `3420bca32643` `fedd896ff8a2` `124867c6620c` `a90a16b0e40d` — 4/4 cocok (FIG-01..03 juga 3/3) |
| 10 | **Item 8** — nb01..04 tak tersentuh | **LULUS** | `eda_01` `ec448a593c1b` · `eda_02` `8ff4358d4175` · `eda_03` `0158ca994db9` · `eda_04` `4ac4566f5f6c` — 4/4 = titik-awal. FIG-01..03 mtime `13:55:26` tetap |
| 11 | **F-NL2** — 7 baris pasca-proses seragam x5 | **LULUS** | blok pasca-proses **1 varian unik** di kelima builder (identik byte); `NB_PATH` berpola sama;kedua `NB_PATH.open` di tiap builder memakai `newline="\n"` |
| 12 | Kode F-NL2 benar | **LULUS** | `read_bytes().replace(b"\r\n", b"\n")` lalu tulis `newline="\n"` (tanpa translasi) — benar dan idempoten |
| 13 | Gate `ruff check` / `format` / `foreign` / `pytest` | **LULUS** | saya jalankan sendiri: ruff check rc=0; ruff format rc=0; foreign rc=0 (79 file); **pytest 157 passed** |
| 14 | Byproduct validator = pola lama | **LULUS** | `data_validation_2026-10-07.md` 3.489 B; pola ini memang sudah ada: `2026-10-05.md` 3.427 B dan `2026-10-06.md` 3.427 B |
| 15 | "byte-identik" hanya di `tahap_14` | **LULUS** dengan catatan | satu-satunya kemunculan memang di `tahap_14` dan menunjuk FIG-01..03 (artefak byte-stabil) — sah. Nomor barisnya salah, lihat C2 |

## M1 (MEDIUM) — provenance "era CRLF" salah kausal di EMPAT dokumen

Ini satu-satunya temuan, dan puncaknya bertumpu pada bukti yang saya hitung sendiri.

**Bukti akar.** `.gitattributes` repo memuat `* text=auto eol=lf`, jadi
`git hash-object` menormalkan CRLF ke LF sebelum menghitung hash. Saya buktikan
dengan menghitung sendiri:

| Bentuk | Ukuran | Hash blob |
|---|---|---|
| Snapshot CRLF apa adanya | 83.611 B | `529cbf2092a7…` |
| Snapshot setelah dikonversi ke LF | 81.948 B | `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` |
| `git hash-object` atas file CRLF | - | `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` |

Kedua baris terakhir **identik**. Artinya pin lama `2cb57ad9ec1a` adalah hash dari
konten yang sudah dinormalkan LF — pin itu **tidak pernah merekam CRLF**, dan
mengganti EOL **tidak mengubah** pin.

**Maka apa yang sebenarnya mengubah pin?**_delta antara snapshot-if-LF (81.948 B)
dan file baru (81.851 B) adalah **-97 B**, dan itu berasal dari merge chunking
(hapus 97 B overhead JSON dua entri output), bukan dari EOL. Pin `661c0aeb2357`
datang dari **perubahan konten**, bukan dari perbaikan EOL. Kalau perbaikan EOL
dijalankan tanpa merge, `git hash-object` akan tetap mengembalikan `2cb57ad9ec1a`.

**Yang tertulis di dokumen — keempatnya salah sebab:**

| Lokasi | Frasa |
|---|---|
| `reports/eda/2026-10-06/report.md:15` | pin lama `2cb57ad9ec1a` "era CRLF dipensiunkan" |
| `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md:4` | idem |
| `reports/eda/progress/06-regimes/laporan_tahap_12_sintesis.md:5` | idem |
| `reports/eda/progress/06-regimes/laporan_tahap_14_figures.md:10` | idem |

**Dampak.** Dokumen menyimpan model sebab-akibat yang salah tentang konvensi hash
tengah repo ini. Pembaca berikutnya bisa menyimpulkan dua hal yang sama-sama keliru:
bahwa perubahan EOL mewajibkan re-pin (padahal tidak), atau conversely bahwa pin
yang cocok sudah membuktikan EOL benar (padahal tidak — `529cbf2092a7` vs
`2cb57ad9ec1a` justru membuktikan pin buta thd EOL). Repo ini sudah dua kali
terbakar masalah konvensi EOL/hash yang persis sama — B9-02 (klaim `LF` salah)
dan B9-03 (pin builder basi). Menulis model yang keliru ke dalam provenance
adalah cara paling murah untuk Menyulam model keliru ke dalam provenance.

**Perbaikan yang diminta** (satu frasa per file): pin lama `2cb57ad9ec1a`
dipensiunkan **karena merge chunking output pada regen NL2** — bukan karena era
CRLF. Pernyataan bahwa EOL aktual kini LF deterministik (sudah benar di
`tahap_14:8-10`) **tetap dipertahankan**.

## CATATAN (bukan temuan)

**C1 — angka `Writing 81667 bytes` pada item 7 tidak reka dengan file mana pun.**
Bentuk LF yang saya ukur = 81.851 B (cocok dengan file di disk). Bentuk CRLF
yang harusnya ditulis nbconvert = 83.507 B. Log berbunyi 81.667 B — meleset
**-184 B** dari bentuk LF dan **-1.840 B** dari bentuk CRLF, dan bukan pula ukuran
snapshot 83.611 B. Karena F-NL2 hanya mengecilkan file (CRLF -> LF), ukuran akhir
**tidak mungkin lebih besar** dari yang dilaporkan nbconvert. Jadi kutipan log itu
bukan ukuran yang dapat diandalkan. Data tidak terpengaruh: byte-count item 1
benar karena saya ukur file-nya langsung, bukan dari log.

**C2 — `byte-identik` ada di `tahap_14:70`, bukan `:69`.** Baris 69 berisi kalimat
lain ("figure yang menampilkan inferensi sinyal"). Penyebabnya baris tambahan
KOREKSI NL2 menggeser baris (75 -> 76). Klaimnya sendiri benar secara substansi;
hanya nomor barisnya basi, dan nomor itu tidak masuk ke dokumen mana pun.

**C3 — `ruff format --check` 31 file (klaim) vs 32 file (saya).** Selisih cakupan
saja,(rc=0) sehingga tidak berdampak.

**C4 — 4 dari 5 builder belum pernah dieksekusi.** `eda01` s/d `eda04` membawa
kode F-NL2 tetapi tidak dijalankan; hanya `eda05` yang benar-benar dieksekusi.
Kebenaran kode bertumpu pada tiga hal yang **saya verifikasi sendiri**: blok
pasca-proses 1 varian unik di kelima builder, `NB_PATH` berpola sama, dan
logika yang terbukti idempoten. Cukup masuk akal, tapi jalur runtime 4 builder
masih belum terbukti. Ini risiko tersisa yang harus dinyatakan terbuka, bukan
temuan.

**Catatan Gate 0.** Klaim "15/15" tidak saya buktikan seluruhnya: satu titik —
hash awal `eda_00_setup.ipynb` — tidak punya catatan independen dari saya, karena
nb00 memang tidak pernah saya sentuh di putaran mana pun. 14 titik lain saya
bandingkan terhadap angka saya sendiri.

## VERDICT

| Item | Severity | Status |
|---|---|---|
| **F-NL** — `newline="\n"` pada penulisan nbf | (akar M1) | **TERVERIFIKASI TUTUP** |
| **F-NL2** — normalisasi EOL pasca-nbconvert x5 | (akar M1) | **TERVERIFIKASI TUTUP** |
| **M1** — provenance "era CRLF" salah kausal x4 dokumen | **MEDIUM (baru)** | **PERLU DIPERBAIKI** |

### VERDICT FIX F-NL + F-NL2: **LOLUS BERSYARAT** — 2 dari 2 wajib tertutup, 1 MEDIUM baru

Kerja fungsionalnya benar dan bukti saya hitung ulang, bukan menerima: nb05 kini
81.851 B dengan **0 CR**, teks output gabungan identik di **26 dari 26 sel**,
merge chunking terbukti tidak kehilangan satu karakter pun (439 = 439), 68
assertion cocok, 4 notebook lain dan 7 figure tidak tersentuh, empat gate hijau
dan pytest 157. Akar masalah laten yang sejak B9-02 sengaja ditunda **sekarang
benar-benar tertutup** — dan ditutup di hulu, di kelima builder, bukan ditambal
di satu file.

Yang belum bersih adalah **provenance**, bukan datanya: empat dokumen mengatribute
perpindahan pin ke EOL, padahal EOL terbukti tidak memengaruhi pin sama sekali.
Itu satu kalimat per file, dan selama belum diperbaiki, tidak boleh ada batch
berikutnya yang memakai model sebab-akibat itu.

**Batch C mutakhir: 1 MEDIUM terbuka, 4 LOW terbuka** — MEDIUM ini baru dan
ditambahkan pada putaran ini.

## Self-audit 3x (adversarial)

**Putaran 1 — Correctness.** Semua angka provenance saya hitung sendiri dari
`.gitattributes` dan dari hitungan blob manual (`SHA1("blob <len>\0" + data)`),
bukan dengan menerima penjelasan coder. Snapshot saya baca langsung dari
`D:/_nl_batch_snap/pra_nl2_eda_05_regimes.ipynb` dan saya pastikan ada di luar
repo (`str.startswith("d:\\ann")` = False), sehingga perbandingan pra/pasca
memang sah. Gerbang saya jalankan ulang sendiri dengan rc asli. **Distorsi yang
hampir saya buat:** saya curiga klaim "3 kategori (EOL, cell.id, timestamp)"
menutupi kategori keempat, karena `metadata` sel ikut berubah. Setelah saya
bedah isinya, **`metadata` itu persis berisi timestamp** `iopub.*` dan
`shell.execute_reply` pada 19 sel kode — jadi klaim coder **benar** dan dugaan
saya yang salah. Saya hampir reporting temuan palsu berdasarkan dugaan.

**Putaran 2 — Bias.** Dua tarikan saya tolak. Pertama, godaan menaikkan
Kedua, godaan menaikkan ketidakrekonsiliasi angka log `81667` menjadi temuan,
benar sudah saya verifikasi langsung dan data tidak tersentuh; itu masalah
tapi byte-count file yang benar sudah saya verifikasi langsung dan data tidak
satu frasa per file — padahal yang keliru bukan angkanya melainkan invarian
verifikasi repo ini, dan repo sudah dua kali tersandar ke misunderstanding yang
sama. M1 saya tahan di MEDIUM.

**Putaran 3 — Meta.** Objek benar? Ya: 5 builder, nb05, 4 dokumen, 4 notebook
sebelumnya, 7 figure, audit, `.gitattributes`, byproduct validator. Hanya dokumen
ini yang saya tulis, append-only, prefix 238.097 B diverifikasi ulang sebelum
menulis. Nol builder maupun nbconvert dijalankan ulang oleh saya; snapshot hanya
dibaca. Nol commit, nol push. `nb00` saya sebut belum terkoroborasi karena memang
tidak ada catatan saya — saya lebih suka mengatakannya terus terang daripada
mengarang angka.

**Cacat milik saya sendiri, ditemukan oleh guard.** Append F-B902/F-B903 pada
putaran sebelumnya menutup file tanpa newline akhir (saya sudah terlanjur
mengultureksnya sebagai factsaya, sekarang diperbaiki: file ini ditulis setelah
saya tambahkan satu newline pemisah). Dampaknya nol pada isi — tidak ada baris
yang hilang atau berubah, prefix tetap utuh — tapi memang pembulatan kasar yang
patut disebut, bukan disembunyikan.

## STOP

Hash pasca-append dihitung setelah tulis final dan dilaporkan di pesan penutup chat.
Batch berikutnya hanya atas perintah terpisah.
---

# RE-AUDIT PENUTUPAN M1 (provenance "era CRLF")

Peran: **AUDITOR**. Baca `.ai/assistant/prompts/PERAN-auditor.md` lebih dulu.
Read-only terhadap sumber; satu-satunya tulisan dokumen ini (append-only). Nol
regen, nol rerun builder, nol nbconvert, nol commit.

Putusan yang mengikat (kebijakan yang saya tegakkan, sekarang diverifikasi ulang):
pin lama `2cb57ad9ec1a` dipensiunkan **karena merge chunking output pada regen
NL2** — bukan karena era CRLF; pernyataan LF deterministik (`tahap_14:8-10`)
**tetap dipertahankan**.

## Gate 0 — hitung ulang sendiri, bukan terima klaim

Empat dokumen pasca-fix, `git hash-object` + ukuran dari disk:

| Lokasi | Hash (hitung ulang) | Ukuran | Cocok |
|---|---|---|---|
| `reports/eda/2026-10-06/report.md` | `15ecb37dcfc62df6…` | 12.569 B | ya |
| `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md` | `03c28afb1afd3577…` | 9.143 B | ya |
| `reports/eda/progress/06-regimes/laporan_tahap_12_sintesis.md` | `4a9357d04806ea5e…` | 9.512 B | ya |
| `reports/eda/progress/06-regimes/laporan_tahap_14_figures.md` | `1e3097f7483cb02a…` | 5.228 B | ya |

Audit: `97ae2f18103783fa2970fcdd107904ced35158e6` / 249.786 B / 4.034 baris —
**cocok persis** dengan hash yang saya ukur sendiri pada append F-NL/F-NL2, bukan
dengan angka yang diklaim assistant, bukan dengan angka saya sendiri.

Set larang: 5 builder (`5ba47ba8…/05b6c26b…/27e801c1…/641210e7…/e29e18c7…`),
nb05 `661c0aeb2357…`, nb01–04 (`ec448a59…/8ff4358d…/0158ca99…/4ac4566f…`),
FIG-01..07 — **16/16 cocok**; mtime FIG-01..03 tetap `13:55:26`, FIG-04..07
`14:32:34`. Tidak ada satu pun file terlarang tersentuh.

## Tabel Klaim & Bukti

| Klaim | Status | Bukti (hitung sendiri) |
|---|---|---|
| Frasa target ada tepat 1x per lokasi | **TERVERIFIKASI** | `dipensiunkan karena merge chunking output pada regen NL2` = 1x di `report.md:15`, `tahap_11:4`, `tahap_12:5`, `tahap_14:10`; frasa `bukan karena era CRLF` = 1x di keempatnya |
| Frasa basi M1 = 0 | **TERVERIFIKASI** | `era CRLF dipensiunkan` = **0** di keempat file; regex `2cb57ad9ec1a…era CRLF` dan `era CRLF…dipensiunkan\b(?! \()` → **TIDAK ADA** di keempat file |
| Label `KOREKSI M1 2026-10-07` tepat 1x | **TERVERIFIKASI** | 1x di `report.md:15`, `tahap_11:4`, `tahap_12:5`, `tahap_14:10` |
| Pernyataan LF deterministik utuh | **TERVERIFIKASI** | `tahap_14:8` masih berbunyi `EOL **LF** deterministik dari builder — KOREKSI NL2, 2026-10-07`; `:9` (26 sel, 19 kode, 68 assertion) utuh |
| Pin lama tetap tercatat (provenance) | **TERVERIFIKASI** | `2cb57ad9ec1a` masih ada 1x di tiap file — **tidak dihapus** |
| Pin/angka/count/verdict tak berubah | **TERVERIFIKASI** | pin baru `661c0aeb2357` masih ada di keempat file; `report.md:15` count masih **68**; builder `e29e18c7eb98` di `tahap_11` 2x; delta baris keempat file **0** (157/108/141/76) — jadi tidak ada baris lain yang bergeser |
| EOL `.md` LF | **TERVERIFIKASI** | CRLF=0 dan CR=0 di keempat dokumen |
| Gate `check_foreign_chars` | **TERVERIFIKASI** | saya jalankan sendiri **sesudah** fix: rc=0, `OK: 79 file discan` |

## Disposisi butir 5 — "klaim EOL era KOREKSI B9-02 ikut dipensiunkan"

**Terima sebagai sah.** Alasannya, bukan karena kalimatnya "kecil":

`KOREKSI B9-02` (lihat `tahap_14:12-17`) berisi klaim bahwa EOL notebook **CRLF**
dan menyebut akar masalah `NB_PATH.open("w", encoding="utf-8")` tanpa `newline=`.
Regen NL2 kemudian **menulis ulang patokan** menjadi `EOL LF deterministik dari
builder` (`:8`). Jadi klaim B9-02 memang **usang** — bukan karena salah sejak
awal, tapi karena **digantikan oleh keadaan baru**. `dipensiunkan` di situ tepat
sasaran: yang usang adalah klaim EOL lama, bukan pin lama.

Yang membuat saya tidak sambil lalu: dua kalimat itu tidak saling bertentangan.
`:8` menyatakan **keadaan sekarang** (LF), `:10` mencatat bahwa klaim lama
dipensiunkan. Keduanya tetap dapat dibaca bersamaan tanpa kontradiksi.

Dua hal yang membuat kalimat itu tidak berlebihan: kata **"ikut"** ada di
`tahap_14:10` setelah `dipensiunkan` — jadi ia ditandai jelas sebagai turunan,
bukan klaim utama; dan frasa itu berada **di luar** frasa target M1, terpisah
tanda titik koma dan frasa `(provenance Q4.2)`. Saya sudah mengecek bahwa kalimat
ini **tidak** mengulang atribusi salah yang M1 tegur: yang dinaturalisasi adalah
*pensiun klaim EOL*, bukan *alasan pin berubah*.

## Disposisi butir 6 — coder mempertahankan blob penuh 40 karakter

**Terima, bukan temuan.** Verifikasi saya:

- `tahap_14` memakai hash **penuh** secara konsisten: 2 kemunculan 40-char
  (`661c0aeb…` di `:8`, `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` di `:10`) dan
  0 abreviasi.
- `tahap_11` memakai abreviasi secara konsisten: 0 penuh, 9 abreviasi
  `12…` — termasuk `2cb57ad9ec1a…` **dan** pin baru `661c0aeb2357…` di baris
  yang sama (`:4`).
- `tahap_12`: 0 penuh, 4 abreviasi.

Jadi coder **tidak mengubah kebijakan**; ia mengikuti kebiasaan yang sudah ada per
file. Feather test: `tahap_14` tidak bisa memakai abreviasi tanpa mengurangi
informasi, karena `:8` sudah memuat hash penuh dan `:10` Immediately mengulang
pin yang sama sebagai provenance — memakai abreviasi di sana justru membuat
pembaca memperoleh dua bentuk untuk satu pin yang sama.

Nilai penuhnya sendiri saya verifikasi ulang: `SHA1("blob 81948\0" + LF-snapshot)`
= `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` — **cocok** dengan yang tertulis.

## Yang belum diverifikasi

- `validate_data` **tidak** saya jalankan pada putaran ini; bukan relevan (hanya
  dokumen `.md` berubah, `validate_data` menyentuh data + menulis byproduct
  bertanggal). `ruff check` (rc=0) dan `pytest` (157 passed) saya jalankan
  sebagai pembatas Vedikti umum, meski keduanya tidak tersentuh fix ini.
- pasadasana "15/15" versi coder: pada scope M1 yang relevan adalah 4 dokumen +
  audit + set larang, dan semuanya saya verifikasi. Klaim 15/15 yang merujuk
  seluruh repo tidak saya audit ulang per poin — di luar scope penugasan ini.
- Butir 5 dan 6 saya disposisikan atas **konsistensi dokumen + nilai yang saya
  hitung ulang**, bukan atas keputusan yang diprakarsakan.

## Potensi masalah

- Tidak ada temuan baru. M1 tertutup sesuai putusan.
- Yang tersisa terbuka (bukan Provinces M1): `data_validation_2026-10-07.md`
byproduct (3.489 B) masih di worktree dari batch NL2 — sudah dijelaskan, tidak
  berubah.
- Ke depan: frasa "dipensiunkan" kini punya dua sasaran berbeda di `tahap_14:10`
  (pin lama, klaim EOL lama). Keduanya ditandai eksplisit dan tidak tumpang tindih.

## Verdict

**M1 — TERVERIFIKASI TUTUP.** Empat dari empat lokasi memakai frasa yang saya
tetapkan; nol frasa basi tersisa; label, pin, angka, count, dan verdict tak
berubah; set larang utuh; gate hijau.

### Status Batch C mutakhir

**0 MEDIUM terbuka, 4 LOW terbuka.** MEDIUM yang saya buka pada append
F-NL/F-NL2 (provenance "era CRLF") kini tertutup. Tidak ada temuan baru pada
putaran ini.

## Self-audit 3x (adversarial)

**Putaran 1 — Correctness.** Tiap angka saya hitung dari disk: `git hash-object`
untuk 4 dokumen, audit, dan 16 file terlarang; ukuran file; hitungan kemunculan
frasa (bukan grep longgar — saya pakai daftar frasa basi eksplisit **dan** regex
yang coached untuk menangkap pola `pin lama X era CRLF`); Gate 0 audit dicocokkan
ke hash saya sendiri dari append sebelumnya. Observasi butir 5 dan catatan
keputusan butir 6 **keduanya saya disposisikan eksplisit** dengan bukti — tidak
saya lewati. Nilai blob penuh di `tahap_14:10` saya hitung ulang dari
snapshot LF dan cocok.

**Putaran 2 — Bias.** Dua tarikan saya tolak. Pertama, godaan menaikkan
"klaim EOL ikut dipensiunkan" menjadi temuan karena terdengar seperti frasa basi
lagi — tapi setelah membaca `tahap_14:8` bersama `:12-20`, jelas itu catatan
zaman yang benar dan ditandai "ikut", bukan pengulangan atribusi keliru. Menaikkannya
justru akan menambah LOW palsu. Kedua, godaan menyalahkan Retention blob penuh
sebagai inkonsistensi — tapi `tahap_14` memang asyncimum memakai penuh dan
`harian_11` memang abreviasi; itu kebijakan per-file yang sudah ada, dan nilainya
benar. Saya tidak mengarang temuan untuk mengejar angka, dan tidak meloloskan M1
dengan alasan "hanya ganti frasa" — closure saya bertumpu pada grep yang benar-benar nol.

**Putaran 3 — Meta.** Hanya `eda_nb05_audit_v1.md` yang saya tulis (append-only,
prefix 249.786 B diverifikasi byte sebelum menulis). Nol eksekusi builder,
nol nbconvert, nol edit notebook/figure/dokumen sumber. Nol commit, nol push.
Hash pasca-append dihitung **setelah** tulis final. Batch berikutnya hanya atas
perintah terpisah.

## STOP

Hash pasca-append dihitung setelah tulis final dan dilaporkan di pesan penutup chat.
