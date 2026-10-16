# EDA 00 — Setup & Kontrak Data

**Notebook:** `../eda_00_setup.ipynb` · **Status:** 11/11 assertion PASS

---

## Apa ini

Bukan analisis. Ini **fondasi** — semua aturan yang dipakai notebook 01–05 dikunci di sini
dan tidak boleh diubah di notebook mana pun.

Kalau aturan di sini berubah, notebook 01–05 gagal dengan sengaja — bukan diam-diam
memakai definisi berbeda.

---

## Apa yang diaudit

1. Cetak Kontrak 00 verbatim
2. Audit file parquet + konfigurasi
3. Audit hitungan strata A/B/C terhadap total 1.347.847 bar
4. Pemetaan sesi primer (DST-aware) vs cross-tab UTC-tetap
5. Matriks ketersediaan kolom per timeframe + audit missing-data
6. Definisi return / volatilitas / swing / level + aturan anti look-ahead
7. **Preregistrasi protokol placebo Q6** — ditulis sebelum hasil apa pun dilihat
8. Ringkasan audit

---

## Temuan: stratifikasi data

Data dipisah menjadi tiga strata yang tidak boleh bocor satu sama lain:

| Strata | Definisi | Bar | Hari |
|---|---|---|---|
| **A** (utama) | sisa setelah B dan C dieksklusi | 1.136.401 | 825 |
| **B** | H1-2023 (regime spread berbeda) | 185.248 | 130 |
| **C** | jendela anomali | 26.198 | 19 |
| | **TOTAL** | **1.347.847** | **974** |

Jendela anomali (C):
- `2024-10-28 .. 2024-11-01` → 6.899 bar (5 hari)
- `2026-03-10 .. 2026-03-27` → 19.299 bar (14 hari)

**Penting:** pemetaan bar → stratum memakai **tanggal dinding broker**
(`broker_time_raw`), bukan tanggal UTC. Untuk stratum C ini krusial karena gejalanya
memang artefak jam dinding broker.

---

## Temuan: definisi sesi (DST-aware)

Dua pelabelan dihitung. **DST-aware adalah primer**, UTC-tetap hanya pembanding:

| Sesi | Zona IANA | Window lokal (primer) | Cross-tab UTC-tetap |
|---|---|---|---|
| Tokyo | Asia/Tokyo | 09:00–18:00 | 00:00–09:00 |
| London | Europe/London | 08:00–16:00 | 08:00–16:00 |
| New York | America/New_York | 08:00–17:00 | 13:00–22:00 |
| Sydney | Australia/Sydney | 08:00–16:00 | 21:00–06:00 |

Flag per bar bersifat **non-eksklusif** (`is_tokyo`, `is_london`, …) karena sesi
tumpang tindih. Untuk tabulasi dipakai label eksklusif dengan prioritas:

```
London > New York > Tokyo > Sydney > Off
```

Sesi yang tidak bertahan di kedua pelabelan diklasifikasikan **artefak batas**, bukan temuan.

---

## Preregistrasi placebo Q6

Protokol placebo (parameter, seed, timeframe, window yang diuji) **dikunci di sini**,
sebelum hasil apa pun dilihat. EDA-04 membacanya langsung dari notebook ini dan
*assert* sama persis.

Kalau EDA-00 berubah, EDA-04 gagal dengan sengaja.

---

## Assertion yang lulus (11/11)

```
PASS Strata A/B/C = 1.136.401 / 185.248 / 26.198
PASS A+B+C = TOTAL 1.347.847
PASS Window C = 6.899 (5 hari) + 19.299 (14 hari)
PASS H1-2023 = 130 hari berbar
PASS 2025 = tahun referensi bersih (0 bar anomali)
PASS tzdata == 2026.5
PASS D1 2024 = 260 bucket + nol bucket weekend
PASS Semua TF: file lengkap, kolom wajib, 0 NaN
PASS utc_series == parse(time) penuh M1 2025
PASS 4 zona DST-aware + 4 blok cross-tab terkunci
PASS Protokol placebo Q6 + seed terkunci
```

---

## Yang sengaja TIDAK dikerjakan

- Tidak menulis `configs/` atau `src/`
- Tidak ada dump data mentah ke output
- Tidak ada imputasi

---

## Nasihat untuk EDA-06 ke depan

1. **Fingerprint sesi di sini adalah kontrak.** Notebook baru wajib assert
   `Definisi sesi == Notebook 00`.
2. **Stratum B bukan pembanding utama** — hanya 130 hari dan hanya 6 bulan. Hasil negatif
   di sana berarti "tidak terdeteksi pada n ini", bukan "tidak ada".
3. **Stratum C deskriptif saja.** Gejalanya artefak jam broker dan offset jendela
   **belum terverifikasi** terhadap Finex.
4. **Data 2026 termuat di sini** (269.846 bar, 236 hari). Kalau butuh holdout,
   harus ada setelah `2026-10-02`.
