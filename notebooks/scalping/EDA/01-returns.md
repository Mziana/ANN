# EDA 01 — Distribusi Return (Q1)

**Notebook:** `../eda_01_returns.ipynb` · **Status:** 23/23 assertion PASS

---

## Apa ini

Mengukur **bentuk distribusi return** USDJPY di tiga timeframe — M1, M5, M15 — dengan
stratifikasi A/B/C yang sudah dikunci di EDA-00.

Ini murni deskripsi. Tidak ada yang diprediksi, tidak ada yang dipilih.

---

## Apa yang diteliti

- Muat M1, M5, M15 dan hitung return `r_t = ln(close_t / close_{t-1})`
- Audit stratifikasi per timeframe (A/B/C tidak tumpang tindih, A+B+C = total)
- Tabel utama: skew, ekses kurtosis, kuantil, pangsa di atas 3σ dan 5σ
- QQ-plot terhadap distribusi normal
- Karakterisasi ekor (dikonversi ke **pip** dengan benar) dan **massa nol**
- Jam pergerakan terbesar — untuk cek apakah ekor terkonsentrasi di jadwal berita

---

## Definisi yang dikunci (tidak diubah di notebook ini)

- `close` = **harga BID** (bukan BID/ASK)
- Spread diperlakukan sebagai **biaya terpisah**, bukan bagian dari return
- Tidak ada imputasi

---

## Hasil: angka utama (stratum A)

| Timeframe | σ | skew | ekses kurtosis | q0,1% | q99,9% |
|---|---|---|---|---|---|
| **M1** | 1,609e-04 | **−0,744** | **195,476** | −9,673e-04 | +9,167e-04 |
| **M5** | 3,566e-04 | **−1,456** | **102,848** | −2,182e-03 | +2,057e-03 |
| **M15** | 6,120e-04 | **−1,225** | **51,176** | −4,043e-03 | +3,499e-03 |

### Cara membacanya

1. **Ekor sangat tebal.** Kurtosis 195 di M1 itu ~200× lebih gemuk dari normal.
   Distribusi return aset keuangan memang begitu — tapi angka ini berlaku penuh.
2. **Asimetri negatif konsisten di semua timeframe.** Skew −0,7 sampai −1,5 berarti
   ada lebih banyak gerakan turun ekstrem daripada naik. Gerak besar ke bawah lebih sering.
3. **Ekor asimetris.** Di M1, q0,1% = −9,67e-04 tapi q99,9% = +9,17e-04. Turunnya
   sedikit lebih dalam. Di M15 lebih jelas: −4,04e-03 vs +3,50e-03.

---

## Temuan: massa nol

```
78.582 bar dari 1.347.847  =  5,83%
  stratum A: 66.817  (5,88%)
  stratum B: 10.572  (5,71%)
```

Sekitar **1 dari 17 bar M1** punya return persis nol. Ini wajar secara microstructure —
bid dan ask tidak bergerak, jadi close tidak berubah dari menit sebelumnya.

Dikonfirmasi ulang independen di EDA-05 (T-01) dan dicatat di laporan final sebagai
karakteristik data, bukan bug.

---

## Temuan negatif: atribusi kurtosis

Ekor M1 punya **dua** sumber yang belum dipisahkan:

1. Berita makro (12:30 UTC = 08:30 ET)
2. Gap pembukaan sesi (21–22 UTC)

Hipotesis awalnya: "kurtosis tinggi = microstructure noise". **Hasilnya: TIDAK DIDUKUNG.**

Ini dicatat eksplisit sebagai `TIDAK DIDUKUNG` — sudah diuji dan ditolak, bukan
"belum diverifikasi". Perbedaannya penting: yang pertama menutup topik, yang kedua
membuka pekerjaan baru.

---

## Putusan R1–R4 (kalender UTC vs broker)

Dicatat di notebook ini sebagai keputusan arsitek atas temuan SA-03, berlaku mulai Q6/Q7:

> **R1** — "hari-UTC" = label kalender murni dengan offset struktural −1. **DILARANG**
> menggeser data agar "sepakat".
>
> **R2** — Syarat "wajib sepakat" ditafsir ulang menjadi *sepakat-dengan-kesadaran-geser*.
> Hanya divergensi **melebihi** geseran struktural yang menjadi temuan.
>
> **R3** — Seluruh pekerjaan level-hari dikunci pada **tanggal-broker**.
> Hari-UTC sekunder saja.
>
> **R4** — Tanpa redesain, tanpa penundaan. Aturan dicatat di EDA-04 dan EDA-05.

**Dampak ke Q1:** nol. Q1 bekerja pada level bar, bukan hari. Aturan ini baru mengikat
di EDA-04 dan EDA-05.

---

## Batas keras notebook ini

- Tidak ada P&L, equity, atau simulasi profit
- Tidak ada sinyal, model, atau pemilihan metode
- Tidak menulis `configs/`
- Tidak ada imputasi
- **Inferensi sinyal tidak diambil dari M1** — hanya untuk deskripsi

---

## Nasihat untuk EDA-06 ke depan

- **Ekses kurtosis M1 (195) ≫ M15 (51)** adalah bukti kuantitatif bahwa M1 tidak boleh
  dipakai untuk inferensi sinyal. Ini input hipotesis, bukan kesimpulan.
- **Jangan pakai kurtosis sebagai alasan.** Market microstructure menghasilkan
  kurtosis tinggi secara normal; angka ini tidak menunjuk apa pun tanpa pemisahan
  news-spike, dan itu di luar scope EDA.
- Skew negatif seragam di semua TF → kalau nanti ada hipotesis bias arah, cek dulu
  apakah itu cuma artefak news, bukan sinyal.
