# EDA 03 — Autokorelasi Return (Q4)

**Notebook:** `../eda_03_autocorr.ipynb` · **Status:** 31/31 assertion PASS

---

## Apa ini

Ini **temuan paling menentukan** di seluruh rantai EDA.

Pertanyaannya: *apakah return M1/M5/M15 menunjukkan autokorelasi yang bisa dieksploitasi,
dan apakah polanya (mean-reversion atau momentum) bergantung pada timeframe dan sesi?*

---

## Apa yang diteliti

| Metrik | Horizon | Kenapa |
|---|---|---|
| ACF | lag 1–60 | autocorrelation function, versi `all` dan `no-gap` |
| Ljung-Box (manual, via scipy) | h = 5/15/60 | uji serialitas tanpa dependensi baru |
| Variance Ratio | k = 5/15/60 + kurva 1–60 | distinguishing random walk dari trending/momentum |
| Sign-autocorrelation | lag 1 | arah (bukan besaran) — apakah berbalik |
| Pemotongan | per sesi, per tahun, A vs B | stabilitas |

---

## Aturan baca yang mengikat

Ini keputusan arsitek atas keberatan coder, dan mengikat seluruh interpretasi:

1. **Nilai p tidak dipakai sebagai kesimpulan.** Pada n > 1 juta bar, reject hampir pasti.
2. Yang dibaca adalah **`Q/n`** (besaran per bar) dan **ukuran efek `rho_k`** itu sendiri.
3. **Slice adalah bacaan utama** (per sesi, per tahun). Agregat hanya konteks.
4. Ljung-Box dihitung pada seri **tanpa return lintas gap**, sama seperti ACF.

---

## Hasil: angka kunci (no-gap, lag 1–60)

| Metrik | A M1 | A M5 | A M15 | B M1 | B M5 | B M15 |
|---|---|---|---|---|---|---|
| ACF lag-1 | −0,004372 | −0,011582 | **+0,003496** | −0,000864 | −0,005795 | +0,005980 |
| sign-ACF lag-1 | −0,017702 | −0,009805 | **−0,022624** | −0,013226 | −0,012994 | −0,017336 |
| rata-rata VR(lag 2–60) | 0,9796 | 0,9942 | 1,0337 | 0,9848 | 1,0332 | 1,0236 |
| VR pada k=60 | 0,9809 | 0,9992 | **1,0657** | 0,9916 | 1,0564 | 0,9631 |

`VR(1) = 1,0000` di semua sel (definisi).VR ≈ 1 artinya **random walk**.

---

## Temuan 1: autokorelasi praktis nol

```
max |ACF| lintas stratum / timeframe / lag = 0,0226
```

Angka ini **2,3%**. Lipschitz seragam. Tidak ada autokorelasi di sini yang bisa
dieksploitasi — baik untuk momentum maupun untuk mean-reversion.

### Klaim lama dicabut

Klaim sebelumnya **"|ACF| ≤ 0,012 di semua lag"** **TIDAK BERLAKU LAGI**.

Ekstensi ke lag 1–60 menemukan nilai lebih besar, sebagian besar jatuh di **lag 21–60
yang sebelumnya tidak pernah diperiksa**:

| Lokasi | Nilai |
|---|---|
| B M15 lag 50 | **0,0226** |
| A M15 lag 2 | 0,0148 |
| A M15 lag 30 | 0,0125 |

Dicabut eksplisit, bukan disembunyikan. Ini praktik yang benar.

---

## Temuan 2: arah dan besaran bilang hal berbeda

```
sign-ACF lag-1  :  negatif di SEMUA sel (-0,0098 s/d -0,0226)
ACF besaran M15 A:  +0,0035, VR > 1  →  momentum
```

Tanda ACF negatif berarti **arah cenderung berbalik sementara besarnya tidak**. Jadi ada
sedikit mean-reversion di arah, tapi tanpa dukungan besaran.

Di M15 A keduanya justru **berlawanan arah**: ACF besaran bilang momentum (+0,0035,
VR > 1), tapi sign-ACF bilang mean-reversion (−0,0226).

**Kedua label dilaporkan berdampingan, tidak ada yang dipilih diam-diam.**

---

## Temuan 3: tanda ACF tidak stabil antar tahun

```
tanda ACF1 M1 : 2023:−  2024:+  2025:−  2026:−   → TIDAK stabil
tanda ACF1 M5 : 2023:+  2024:−  2025:−  2026:−   → TIDAK stabil
tanda ACF1 M15: 2023:+  2024:+  2025:+  2026:+   → stabil, tapi sangat kecil (maks 0,0079)
```

Perubahan tanda dari tahun ke tahun pada M1 dan M5. Kalau ada hipotesis
"mean-reversion di M1", ia **tidak bertahan lintas tahun**.

---

## Temuan 4: label "Sydney momentum" runtuh saat dibaca dari tanda

```
ACF1 per sesi (M1, stratum A):
  London  −0,0063
  NewYork −0,0041
  Tokyo   −0,0032
  Sydney  +0,0027   ← satu-satunya positif
```

Sydney terlihat punya momentum dari ACF **besaran**. Tapi sign-ACF Sydney =
**−0,0238**, justru **paling negatif** dari semua sesi.

> *"Label 'Sydney momentum' berasal dari besaran dan **hilang** saat dibaca dari tanda."*

Ini contoh paling jelas di proyek ini kenapa satu metrik tidak cukup.

---

## Temuan 5: A vs B

| | A | B |
|---|---|---|
| max \|ACF\| di M15 | 0,0148 | 0,0226 (lebih besar) |
| ACF lag-1 M1 | −0,00437 | −0,00086 (lebih kecil) |

B hanya 6 bulan (n M15 = 12.395). **"Tidak terdeteksi" tidak sama dengan "sama".**

---

## Temuan 6: Ljung-Box — konsisten dengan "hampir nol"

```
A M1 : Q/n(h=5) = 5,1e-5  →  Q/n(h=60) = 4,1e-4
A M15: Q/n(h=5) = 3,3e-4  →  Q/n(h=60) = 2,0e-3
B M15: Q/n(h=5) = 2,8e-4  →  Q/n(h=60) = 5,3e-3
```

p-value nyaris selalu 0 di A karena n > 1 juta — persis seperti diprediksi aturan baca.
Yang dibaca `Q/n`, dan `Q/n` kecil. Slice terbesar: **Sydney M15 (0,0225)** dan M1
2023/2026 (0,00117 / 0,00124) vs 2024/2025 (~0,0003).

---

## Batas keras notebook ini

- Tidak ada P&L, equity, backtest, atau pemilihan metode
- **Autokorelasi bukan bukti profitabilitas** — biaya spread (mean ~0,65 pip) belum
  dikurangkan di semua angka di sini
- Tidak menulis `configs/`, tidak ada imputasi

---

## Nasihat untuk EDA-06 ke depan

**Ini titik paling penting untuk seluruh seluruh rantai ke depan:**

1. **Autokorelasi ≈ 0,02 itu batas keras.** Setiap efek yang diklaim harus punya
   mekanisme yang bisa menghasilkan efek di urutan besaran itu. Efek 5–9 poin persen
   di M15 **tidak mungkin** datang dari struktur serial yang setipis ini.
2. **Jangan pakai variabel yang sebanding.** Kalau sebuah fitur punya korelasi 0,02
   dengan label, pasti bukan sinyal — itu noise yang kebetulan berkorelasi.
3. **ACF tidak mengukur heteroskedasticity.** Volatilitas yang bisa diprediksi (lihat
   EDA-02) **tidak akan muncul di sini**. Autokorelasi nol **tidak berarti** tidak ada
   apa-apa yang bisa diprediksi — hanya tidak ada yang bisa diprediksi **dari return itu sendiri**.
4. Pengecekan yang lebih jujur untuk "apa yang sebenarnya bisa diprediksi dari data ini"
   ada di EDA-06/07 lama — dan hasilnya: **hanya besaran (volatilitas), bukan arah.**
   Itu bukan alasan untuk skip, tapi itu batasnya.
