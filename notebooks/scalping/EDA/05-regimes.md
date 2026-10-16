# EDA 05 — Regime Harian (Q7) & Sintesis Hipotesis H1–H5

**Notebook:** `../eda_05_regimes.ipynb` · **Status:** 68/68 assertion PASS
*(sumber angka: `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md` — notebook
menyimpan output "SEMUA ASSERTION PASS" tanpa mencetak jumlah)*

---

## Apa ini

**Penutup rantai EDA.** Dua bagian:

1. **Q7** — tipologi hari (regime) per strata
2. **Sintesis** — seluruh temuan EDA-01…04 dirangkum jadi **5 hipotesis kandidat** yang
   masing-masing punya ambang falsifikasi

Status akhir yang dinyatakan notebook ini sendiri:

> **BUKAN output EDA:** sinyal, model, backtest, P&L, dan keputusan metode.

---

## Metrik harian (semua dari bucket D1 kalender-broker, R3)

| Metrik | Definisi |
|---|---|
| `ret_day` | `ln(close/open)` bucket D1 — arah & besar hari |
| `sum_abs_r` | Σ\|r\| intraday dari M1 (jalur harga, bukan net) |
| `rv_day` | Σr² intraday dari M1 (realised volatility) |
| `ratio_path` | \|ret_day\| / Σ\|r\| → 1 = satu arah, ≈0 = bolak-balik |
| `range_atr` | (high−low)/ATR(14) D1 — rentang vs volatilitas wajar |
| `tick_vol_sum` | Σ tick_volume M1 — proksi aktivitas |

**Anti look-ahead:** ATR(14) D1 memakai `.shift(1)`. 14 hari pertama sampel (awal 2023,
semua stratum B) belum punya ATR → dikeluarkan, jumlahnya dilaporkan.

---

## Temuan 1: tipologi hari

Tipologi: `trending` bila `ratio_path` > median-A **dan** `range_atr` > median-A;
`range` bila keduanya ≤ median-A; selain itu `normal`.

Ambang median-A: `ratio_path = 0,0268` · `range/ATR = 88,79`

```
A: trending 33,7%  |  normal 32,5%  |  range 33,8%
```

Hampir **seimbang tiga** — tidak ada tipehari yang dominan.

---

## Temuan 2: komposisi hari A ≈ B

```
χ² = 2,248   dof = 2   p = 0,325
n-A = 825    n-B = 116
```

Tidak terdeteksi perbedaan komposisi. **Tapi:** n-B cuma 116 hari (14 hari hilang karena
ATR warmup), jadi ini "tidak terdeteksi pada n ini", bukan "sama".

---

## Temuan 3: B lebih *intens*, tapi bentuknya sama

| Aspek | A | B | Bacaan |
|---|---|---|---|
| RV median harian | 2,292e-5 | **3,648e-5** | B **1,59×** lebih volatil |
| Cliff's δ | — | **−0,384** | efek sedang, konsisten |
| KS | — | p = 1,2e-11 | kuat secara statistik |
| Σ\|r\| beda | — | 0,0284, CI95-iid [0,0192; 0,0392] | CI tidak memuat 0 |
| `range_atr` beda | — | CI95-iid **[−7,02; 12,59]** | **memuat 0** |
| `ratio_path` beda | — | CI95-iid **[−0,0052; 0,0034]** | **memuat 0** |

Konvensi Cliff's δ: δ = P(A>B) − P(B>A), jadi δ < 0 berarti **B cenderung lebih besar**.

Dikonfirmasi dengan block bootstrap sirkular (block 20 hari × 10.000 resample):

```
range_atr : [−7,63; 13,72]  → memuat 0
ratio_path: [−0,0038; 0,0028] → memuat 0
```

> **Kesimpulan: B lebih ribut, bukan lebih berbentuk berbeda.**
> Stratum B bukan "regime lain" — cuma volume yang lebih tinggi.

---

## Temuan 4: T-01 massa nol — diratifikasi

```
78.582 / 1.347.847  =  5,83%
  A: 66.817 (5,88%)
  B: 10.572 (5,71%)
```

Dihitung ulang independen dari parquet untuk menutup backlog EDA-01. Dicatat sebagai
karakteristik microstructure — implikasi biaya ditangani di `cost_basis`.

---

## ⚠️ Peringatan penting: ambang tipologi bersifat EX-POST

Ambang `ratio_path` dan `range_atr` dihitung dari **seluruh 825 hari A termasuk 2026**,
sehingga label hari-`t` memakai informasi hari-hari **setelah** `t`.

> *"label bersifat ex-post/deskriptif, **TIDAK real-time-safe**"*

Opsi ambang walk-forward per tahun **DITOLAK** untuk EDA (mengubah angka tipologi,
chi-square, dan H1 = keputusan arsitektur di luar scope).

**Artinya:** tipe hari hanya bisa dihitung **setelah** hari itu terjadi. Memakai ini
secara real-time butuh pendekatan berbeda — dan itu milik H1.

---

## Sintesis: 5 hipotesis kandidat

| ID | Klaim inti | Basis EDA | Ambang falsifikasi |
|---|---|---|---|
| **H1** | Kelanjutan arah berbeda antara hari `trending` dan hari `range` (= hari tenang) | Q7: share 33,7 / 32,5 / 33,8% | drift **relatif** (normalisasi ATR) median CI95 memuat 0 **ATAU** share tak stabil antar tahun |
| **H2** | Momentum M15 lemah, **tak terbedakan dari iid** — *hipotesis eksploratori* | Q4: VR 1,0312; sign-ACF −0,022624 | EV-after-cost ≤ 0 di ≥2/3 tahun utuh 2023–2025 OOS **ATAU** VR OOS ≤ 1 |
| **H3** | Regime B = volatilitas tinggi, bisa dideteksi real-time | Q7: RV 1,59×, δ = −0,384 | AUC detektor ≤ 0,7 **ATAU** filter >40% hari tanpa mengurangi drawdown |
| **H4** | Sesi-pintu sebagai alpha kapasitas-rendah; konsentrasi London/NY parsial 78,3% | Q2/Q3 + M2 + M3 | ≥2 jam teratas jatuh `Off` OOS **ATAU** EV 6 jam masuk ≤ 0 |
| **H5** | Reaksi level hanya pada sub-populasi vol/spread tinggi | Q6 negatif + M4 (flag NY 0,95, Sydney 0,80) | hit-rate real ≤ placebo di **SEMUA** sub-populasi |

### Catatan jujur yang ikut tercatat

- **H2 sudah tahu hasilnya** sejak EDA-03: VR 1,0312 dan sign-ACF −0,022624. Ini
  hipotesis yang **diprediksi akan gagal oleh data yang mendasarinya**.
- Ranking empiris `mean|r|` sesi (**London 1,666 > Tokyo 1,439 > Sydney 1,196 >
  NewYork 1,139**) **berbeda dari prior sekunder S5**. Yang dipakai adalah pengukuran.
- M4 memakai `spread_p95` per bar M1 (kanon v3.1 §5), bukan proksi mean-D1 lama. Proksi
  lama menghasilkan rentang antar-sesi hanya 0,0086 pip — praktis datar, jadi dimensi
  "spread" tak terukur. Dicetak sebagai pembanding, **tidak dipakai klaim**.

---

## Assertion yang lulus (68/68)

Jumlah 68 diambil dari laporan resmi `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md`
(bukan dari output notebook, yang tidak mencetak angka). Riwayat revisinya: 53 → 59 → 67 → 68,
setiap kali assertion baru ditambahkan atau guard lama diganti.

Termasuk replika silang yang menutup celah antara notebook:

- Metode VR di EDA-05 kini **eksak sama dengan EDA-03** (ddof=1, no-gap via
  `gap_return`) → rata-rata VR(5,15,60) M15-A = **1,0312**
- sign-ACF no-gap = **−0,022624** (identik EDA-03; n_no_gap 75.038)
- Angka lama 1,0277 / −0,0220 = **metode berbeda**, kini diganti
- Registry figures tepat FIG-01..07

---

## Batas keras notebook ini

- Tidak ada P&L, equity, backtest, atau pemilihan metode
- Tidak menulis `configs/` atau `src/`
- Tidak ada imputasi
- p-value tanpa effect-size **dilarang** disimpulkan
- **Tanpa bukti = tanpa klaim**

---

## Nasihat untuk EDA-06 ke depan

1. **H1–H5 adalah legacy, bukan pekerjaan yang wajib dijalankan.** H2 secara eksplisit
   sudah diprediksi gagal oleh EDA-03. H5 sudah punya bukti negatif dari EDA-04.
2. **Yang benar-benar belum terjawab:** apakah ada **sinyal arah** yang bertahan setelah
   biaya. Tiga temuan negatif (ACF ≈ 0, level ≈ placebo, komposisi hari ≈ sama) konsisten
   mengarah ke jawaban: kemungkinan besar tidak.
3. **Tipologi hari tidak real-time-safe.** Kalau H1 mau diuji, harus disusun ulang
   dengan ambang walk-forward — itu perubahan metode, bukan perbaikan EDA.
4. **Yang terbukti bisa dipredisikan: besaran, bukan arah.** Ini diuji di EDA-06/07 lama
   dan hasilnya konsisten — tapi "besaran bisa diprediksi" ≠ "arah bisa diprediksi".
5. **Data 2026 sudah ikut menggarap ambang.** EDA-06 baru tidak bisa memperlakukannya
   sebagai holdout pristine.
