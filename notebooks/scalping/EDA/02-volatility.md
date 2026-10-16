# EDA 02 — Volatilitas per Jam & Sesi (Q2/Q3) + Spread

**Notebook:** `../eda_02_volatility.ipynb` · **Status:** 30/30 assertion PASS

---

## Apa ini

Mengukur **bentuk volatilitas** (bukan profit) dan **biaya spread yang terukur**.

Tiga pertanyaan dijawab:

- **Q2** — realised volatility dan `mean|r|` per **jam dinding broker**, plus
  `tick_volume` sebagai proksi aktivitas
- **Q3** — volatilitas per **sesi UTC** (label eksklusif primer)
- **Spread** — p50/p95/p99/maks dan %>3 pip per sesi × jam × tahun

---

## Peringatan yang mengikat (dari EDA-01)

Ekor return M1 didorong **dua sumber**: berita makro (12:30 UTC) dan gap pembukaan sesi
(21–22 UTC). Volatilitas per jam di sini **tidak bisa memisahkan keduanya**, karena
kalender berita di luar scope EDA.

Konsekuensinya, setiap tabel juga melaporkan versi **tanpa return lintas gap** supaya
efek gap bisa dinilai, dan tidak ada klaim "sesi X lebih volatile karena" tanpa catatan ini.

---

## Temuan 1: ekor spread M1 vs M5 (D10)

| Sesi | p99 M1 | p99 M5-max | maks absolut |
|---|---|---|---|
| London | 1,20 | 1,40 | 4,60 |
| New York | 2,00 | 2,80 | **55,60** |
| Tokyo | 1,30 | 1,50 | 8,70 |
| Sydney | 2,70 | 3,40 | 24,10 |

**Ditemukan:** agregasi M5 **tidak menemukan ekor baru**. Maksimum absolutnya identik
dengan M1 di setiap bucket. M5 menaikkan p99 hanya karena satu bucket meringkas 5 menit
jadi satu nilai maksimum — tapi titik ekstremnya sudah tertangkap di M1.

**Artinya:** kalau butuh spread ekstrem, pakai M1. M5 tidak menambah informasi.

---

## Temuan 2: marker waktu terbukti DST-aware (D12)

| Marker | Hasil |
|---|---|
| Tokyo fix | 00:55 UTC — 825 bar = 825 hari (identik dengan jumlah hari berbar stratum A) |
| NYSE open | 824 bar — jam **13** UTC = 560 (EDT), jam **14** UTC = 264 (EST) |

Bar buka NYSE jatuh di **dua** jam UTC berbeda — persis yang seharusnya terjadi kalau
sesi benar-benar DST-aware. Ini bukti, bukan asumsi. Marker hadir tepat satu bar per hari
hari perdagangan, tidak ada bar ganda.

**Batas:** ini **bukan event-study**. Tidak ada return pasca-marker dihitung, tidak ada
reaksi yang diukur. Marker hanya flag deskriptif.

---

## Temuan 3 (paling penting): ekor spread 2023 adalah artefak stratum B

Lapisan 1 memakai premis **"2023 punya ekor spread terrible (p99 8,5 pip)"** untuk
memasang asumsi `spread.by_year[2023] = 3,0`.

Pengukuran di notebook ini menunjukkan premis itu **hanya berlaku untuk stratum B**
(H1-2023, regime SA-03):

| Stratum | p95 | p99 | %>3 pip |
|---|---|---|---|
| B — H1-2023 | **5,30** | **8,50** | 5,17% |
| A — H2-2023 | 0,60 | 1,10 | 0,23% |

Rasio p95 = **5,3×**. Di **stratum A** — yang dipakai analisis utama — spread 2023
sama normalnya dengan tahun lain.

**Konsekuensi:** asumsi lama 3,0 pip untuk 2023 adalah **5,9×** mean terukur di
stratum A 2023 (0,51). Angka ini dilaporkan sebagai temuan terukur.

> **Status keputusan (diperbarui):** temuan ini sudah **diterapkan** di
> `configs/data.yaml` → `spread.by_year['2023'] = 0.51` (bukan 3,0), dengan
> `warn_multiplier = 3,0` dan `error_multiplier = 8,0`. Angka asli 3,0 tidak lagi
> ada di config; penyebutan di atas hanya catatan sejarah Premis Lapisan 1.

> Status sekarang: fragmen spread **sudah diterapkan** ke `configs/data.yaml` sebagai
> sub-kunci `spread.cost_basis` + `spread.stress_bands` (commit `cb84717`).

---

## Temuan 4: biaya mendominasi di New York dan Sydney (M4)

Rasio `mean|r|` (dalam pip) terhadap `spread_p95` per sesi:

| Sesi | Rasio | Flag |
|---|---|---|
| London | 2,08 | — |
| Tokyo | 1,60 | — |
| **New York** | **0,95** | biaya-mendominasi |
| **Sydney** | **0,80** | biaya-mendominasi |

Di New York dan Sydney, pergerakan rata-rata per bar **lebih kecil dari spread p95**.
Artinya: banyak bar yang bergerakannya lebih kecil dari biaya untuk masuknya.

**Peringatan eksplisit di notebook:** ini bahan hipotesis
("jangan entry di jam spread lebar"), **bukan** keputusan filter.

---

## Ranking empiris sesi (mean|r|, label eksklusif)

```
London 1,666  >  Tokyo 1,439  >  Sydney 1,196  >  NewYork 1,139
```

**Ini berbeda dari prior sekunder S5** yang dipakai di EDA-00 (London > NewYork > Tokyo).
Yang menang adalah **pengukuran empiris**. Prior tak dipakai untuk memaksa kesimpulan —
dicatat apa adanya.

---

## Assertion yang lulus (30/30)

Semuanya PASS, termasuk yang palingload-bearing:

```
PASS Definisi sesi == Notebook 00
PASS Strata A/B/C = 1.136.401 / 185.248 / 26.198
PASS Label sesi mempartisi bar strata A tanpa sisa/rumpang
PASS Bar 'Off' di strata A = 0 (4 sesi menutup 24 jam)
PASS 2023 di strata A TIDAK lebih lebar dari 2024 (premis lama terbantah)
PASS Temuan: p95 spread strata B >> strata A
PASS D10: maksimum M1 vs M5-max identik di setiap bucket
PASS D12: NYSE open di jam 13 DAN 14 UTC (bukti DST-aware)
PASS D12: tidak ada kolom pasca-marker (bukan event-study)
PASS Fragment ditulis ke reports/, bukan configs/
```

---

## Batas keras notebook ini

- Tidak ada P&L, equity, backtest, atau pemilihan metode
- Fragmen spread hanya **dicetak** di notebook; penerapannya ke `configs/` adalah
  keputusan terpisah (sudah terjadi, commit `cb84717`)
- Tidak ada imputasi
- Inferensi sinyal tidak diambil dari M1

---

## Nasihat untuk EDA-06 ke depan

1. **Biaya tidak konstan antar sesi.** Angka spread yang dipakai di simulasi apa pun
   harus per-sesi, bukan angka global. Tokyo ~1,3 pip, New York ~2,0 pip pada p99.
2. **New York dan Sydney "biaya-mendominasi".** Kalau ada hipotesis yang butuh
   pergerakan besar, kedua sesi itu kandidat terburuk — rasio volatilitas/biaya-nya di bawah 1.
3. **Jangan pakai M5 untuk mengukur spread.** M1 sudah menangkap semua titik ekstrem (D10).
4. **Jangan klaim apa pun tentang *kenapa* suatu sesi lebih volatile.** Kalender berita
   di luar scope, dan atribusi itu belum pernah diuji.
5. **Stratum B 5,3× lebih mahal.** Kalau nanti ada analisis yang menyentuh data B,
   angka ekspektansinya tidak bisa dibandingkan langsung dengan A.
