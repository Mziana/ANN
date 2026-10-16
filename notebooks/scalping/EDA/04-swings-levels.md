# EDA 04 — Struktur Swing (Q5) & Level dengan Placebo (Q6)

**Notebook:** `../eda_04_swings_levels.ipynb` · **Status:** 30/30 assertion PASS

---

## Apa ini

Mengukur **struktur bentuk** harga — bukan sinyal. Dua bagian:

- **Q5** — struktur swing/fraktal di M5 (k=3 dan k=5 per sisi), ukuran dinormalisasi
  ATR(14), sebaran per sesi dan per tahun
- **Q6** — apakah level (round-number, prior-day high/low) benar-benar "dihormati" pasar,
  diukur lewat **touch & reaksi** dan dibandingkan terhadap **kontrol placebo**

---

## Kontrak placebo (dikunci di EDA-00)

Parameter protokol di notebook ini **bukan pilihan baru** — dibaca langsung dari
`eda_00_setup.ipynb` dan di-*assert* sama persis. Kalau EDA-00 berubah, EDA-04 **gagal
dengan sengaja**, bukan diam-diam memakai protokol berbeda.

Seed: `20261006` · Timeframe: M5

---

## Q5 — Struktur swing

| Metrik | Nilai |
|---|---|
| Swing k=3 high / low | 20.169 / 20.314 |
| Swing k=5 high / low | 12.787 / 13.070 |
| Ukuran median (satuan ATR) | 0,648 / 0,722 / 0,667 / 0,779 |
| **Frekuensi swing gabungan per hari** | **48,74** (median 49; p10 43; p90 54; min 37; maks 61) |
| Tahan median antar swing, k=3 | 10 bar = 50 menit |
| Tahan median antar swing, k=5 | 15 bar = 75 menit |
| Tahan median gabungan | 5 bar = 25 menit |

### Temuan: D7 punya dua wajah, keduanya dilaporkan

Jarak antar fraktal **sejenis** mengikuti `k` (10 bar untuk k=3, 15 bar untuk k=5).
Tapi **gabungan** hanya 5 bar karena didominasi pergantian high-low.

Tabel per sesi memakai definisi gabungan, sehingga mediannya seragam 5 bar
(25 menit) — itu **keterbatasan yang dinyatakan**, bukan temuan sesi.

### Batas penting

- Fraktal baru terkonfirmasi `k` bar **setelah** terbentuk → Q5 deskriptif, **bukan
  fitur real-time**. Tidak bisa dipakai sebagai sinyal apa adanya.
- **D7 bukan durasi posisi.** Yang diukur jarak antar indeks fraktal, bukan waktu tahan trade.

---

## Q6 — Level & placebo: temuan negatif yang kokoh

### Level yang diuji

- **Round-number:** grid kelipatan 0,50 (`xx.00` primer, `xx.50` alternatif)
- **Prior-day high/low:** primer = bucket D1 **broker**, sekunder = hari-UTC (R3)
- **Touch:** bar M5 dengan `low ≤ L ≤ high`
- **Sisi datang:** `sign(close_{t-1} − L)`; bar dengan `close_{t-1} == L` dilewati
  (tie dilaporkan terpisah)

### Hasil: nyata **tidak** mengalahkan placebo

| Kontrol | Nyata | placebo_acak | placebo_hl |
|---|---|---|---|
| `hl_broker` | 0,4799 | 0,5050 | 0,4922 |
| `hl_utc` | 0,4905 | — | 0,4890 |
| `round_xx00` | 0,4694 | 0,4989 | — |
| `round_xx50` | 0,4892 | — | — |

Ringkasnya: **0,469 – 0,490 vs placebo 0,483 – 0,514.**

Hit-rate asli **tidak melampaui** placebo. Lenovo seperti apa pun level yang dipilih,
hasilnya tidak lebih baik dari acak.

> **Kesimpulan: level TIDAK terbukti "dihormati" pasar.**

### Aturan pembacaan yang mengikat

> Bila hit-rate level nyata **tidak** melampaui placebo di luar CI, maka **tidak ada
> klaim** bahwa level itu "dihormati" pasar. Level yang tampak bekerja hanya boleh
> diangkat sebagai hipotesis bila ia memisahkan diri dari placebo.

Ini sudah diketahui **sebelum** hasil dilihat, karena protokolnya di-preregistrasi di EDA-00.

---

## Temuan: zona BoJ 150/155/160 (D12) — deskriptif saja

| Level | Touch eksak | Band 25 pip |
|---|---|---|
| 150 | 728 bar (53 hari) | 8.474 bar |
| 155 | 518 bar (51 hari) | 5.770 bar |
| 160 | 151 bar (20 hari) | 3.587 bar |

Sebaran: touch terbanyak di sesi **London** (282/228/78), **2024** mendominasi
(150: 508; 155: 179; 160: 7). **2026 hanya menyentuh 155 (153) dan 160 (144); level 150 nol.**

> **Tidak ada return pasca-event yang dihitung.**

Eksposur ini murni deskriptif. Tidak ada reaksi, tidak ada event study.

---

## Assertion yang lulus (30/30)

```
PASS Protokol placebo identik preregistrasi nb00
PASS Seed placebo == 20261006
PASS Placebo bukan artefak (hit-rate tidak >0,95 di semua level)
PASS Placebo 1 tidak kosong (event touch genuine)
PASS CI tidak runtuh (ci_low < ci_hi)
PASS Semua baris CI punya >= 30 hari
PASS D12: tidak ada kolom pasca-marker (bukan event-study)
PASS D6: swing gabungan per hari > 0
PASS D7: waktu tahan median > 0 dan finite di semua kombinasi
```

---

## Batas keras notebook ini

- Tidak ada P&L, equity, backtest, atau pemilihan metode
- Tidak menulis `configs/` atau `src/`
- Tidak ada imputasi
- Anti look-ahead: semua rolling pakai `.shift(1)`
- **Tanpa bukti = tanpa klaim**
- **Fibonacci tidak diuji** — hanya boleh diuji dengan protokol placebo identik ini

---

## Nasihat untuk EDA-06 ke depan

1. **Jangan pernah menaikkan level ke hipotesis tanpa placebo.** Protokolnya sudah ada
   dan sudah di-preregistrasi. Deviasi dari sini langsung membatalkan klaim.
2. **Temuan "level tidak bekerja" harus dipakai.** Ini closes H5 sebagian — sub-populasi
   vol/spread tinggi masih belum diuji, tapi baseline-nya sudah negatif.
3. **Fraktal bukan fitur real-time.** Butuh `k` bar konfirmasi. Kalau nanti ada
   hipotesis berbasis swing, itu hipotesis *delay*, bukan *prediksi*.
4. **Angka 48,74 swing/hari berguna untuk power analysis.** Itu memberi tahu kepadatan
   event yang realistis untuk protokol apa pun — banyak hipotesis yang tidak realistis
   dengan kepadatan segini.
