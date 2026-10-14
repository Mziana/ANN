# AUDIT ADDENDUM - R4-M15-native (2026-10-14)

Status: TAMBAHAN terhadap audit independen. Tidak membatalkan spec beku.
Vonis: TOLAK 9/9 sel. Tidak berubah oleh addendum ini.

Alasan addendum: owner yang melaporkan bahwa `WR A + WR B` tidak mendekati
100% dan meminta verifikasi cermin. Verifikasi menemukan 3 hal: 1 kesalahan
pelabelan metrik, 1 cacat struktural exit, dan 1 ambang impas yang salah.

---

## A1. Kesalahan pelabelan metrik win-rate

Lokasi: `evidence/r4_m15.py` baris 607-608.

```python
wrA = float(countsA["TP"] / decA)   # decA = countsA["TP"] + countsA["SL"]
wrB = float(countsB["TP"] / decB)
```

Nilai ini adalah `TP / (TP + SL)` dengan **outcome TIME dibuang dari pembilang
dan penyebut**. Ini bukan peluang profit. Label "winrate" pada ringkasan dan
laporan sebelumnya menyesatkan dan harus diperbaiki.

Konsekuensi langsung: invarian cermin `P(profit_A) + P(profit_B) = 100%`
tidak pernah berlaku untuk metrik ini, karena TIME dikeluarkan dari kedua sisi
dan karena A serta B dapat resolve pada waktu berbeda.

## A2. Definisi WR yang direvisi (permintaan owner, 2026-10-14)

Owner menetapkan: pada timeout, posisi untung = WIN, posisi rugi = LOSS.
Artinya definisi yang benar adalah:

```
P_profit = P(gross > 0)     # mencakup outcome TP, SL, dan TIME
P_loss   = P(gross < 0)
P_time   = P(outcome = TIME) # dilaporkan terpisah, bukan dibuang
```

Definisi ini bersifat POST-HOC: ditetapkan setelah hasil terlihat. Dicatat
demi kejujuran metodologis. Tidak ada gate vonis yang memakai WR (lihat A4),
sehingga definisi ini tidak dapat mengubah vonis.

Tabel lengkap:

| sel | n_eval | WR_lama_A | WR_lama_B | P_profit_A | P_profit_B | TIME% |
|---|---|---|---|---|---|---|
| E1_N3_k1.0 | 398 | 17.32 | 27.15 | 35.18 | 45.45 | 36.2 |
| E1_N3_k1.5 | 189 | 20.97 | 24.35 | 33.33 | 43.92 | 34.4 |
| E1_N4_k1.0 | 315 | 19.29 | 28.42 | 36.19 | 44.62 | 37.5 |
| E1_N4_k1.5 | 186 | 13.71 | 32.46 | 27.96 | 50.54 | 33.3 |
| E1_N6_k1.0 | 121 | 18.57 | 34.25 | 42.98 | 42.62 | 42.1 |
| E1_N6_k1.5 | 104 | 15.25 | 33.87 | 41.35 | 43.81 | 43.3 |
| E2_W12_k1.5 | 5422 | 24.91 | 21.88 | 42.40 | 41.22 | 41.9 |
| E2_W12_k2.5 | 3637 | 24.76 | 22.45 | 41.68 | 42.04 | 41.7 |
| E3_W16 | 136 | 26.79 | 27.19 | 35.29 | 34.56 | 17.6 |

Semua nilai dalam persen. Ties (gross = 0) sangat jarang: 0,00% pada 7 dari 9
sel, maksimum 0,83% pada E1_N6_k1.0.

## A3. Ambang impas 33,33% adalah salah

Spec mendefinisikan TP = 3,0 x ATR dan SL = 1,5 x ATR sehingga rasio nominal 1:2
dan impas nominal 33,33%. Angka itu tidak berlaku pada data ini karena
outcome TIME menutup banyak posisi dengan nilai kecil dan asimetris.

Perhitungan impas nyata memakai rata-rata observatif:

```
WR_impas = |mean_loss| / (mean_win + |mean_loss|)
```

| sel | mean_win (pip) | mean_loss (pip) | RR nyata | impas % | P_profit_A | selisih |
|---|---|---|---|---|---|---|
| E1_N3_k1.0 | 26.82 | 21.30 | 1.26 | 44.3 | 35.18 | -9.09 |
| E1_N3_k1.5 | 34.63 | 21.56 | 1.61 | 38.4 | 33.33 | -5.04 |
| E1_N4_k1.0 | 27.33 | 20.74 | 1.32 | 43.2 | 36.19 | -6.96 |
| E1_N4_k1.5 | 35.42 | 21.27 | 1.67 | 37.5 | 27.96 | -9.57 |
| E1_N6_k1.0 | 29.47 | 22.57 | 1.31 | 43.4 | 42.98 | -0.39 |
| E1_N6_k1.5 | 28.23 | 23.34 | 1.21 | 45.3 | 41.35 | -3.92 |
| E2_W12_k1.5 | 23.36 | 21.14 | 1.11 | 47.5 | 42.40 | -5.10 |
| E2_W12_k2.5 | 24.46 | 21.96 | 1.11 | 47.3 | 41.68 | -5.62 |
| E3_W16 | 21.51 | 19.67 | 1.09 | 47.8 | 35.29 | -12.47 |

RR terealisasi hanya 1,09 sampai 1,67, bukan 2,00. Impas nyata 37,5% sampai
47,8%. **9 dari 9 sel berada di bawah impas nyata.** Setelah biaya (median
0,99 pip) selisihnya makin lebar: -2,18 sampai -14,88 poin persentase.

Kesimpulan: definisi WR yang direvisi(owner) tidak melemahkan vonis, tetapi
menguatkannya. 8 dari 9 sel tampak melewati impas nominal 33,33% dan
sebenarnya gagal.

## A4. Dampak ke gate vonis: nol

Gate yang dipakai pada verdict_reason, diverifikasi langsung dari `summary.json`:

- `i_median_net_obs_A_gt0`
- `ii_ci_lower_gt0`

Tidak ada gate yang memakai win-rate. Median net dan bootstrap CI tidak
disentuh oleh perubahan definisi di atas. Status tetap **TOLAK 9/9**.

## A5. Cacat struktural exit spread (ditemukan saat verifikasi cermin)

Lokasi: `evidence/r4_m15.py` baris 326.

```python
time_exit = C[:, RACE - 1] + np.where(up[:, 0], 0.0, SPR[:, RACE - 1])
```

Untuk exit TIME, kaki SELL menutup pada BID (`close + spread`) dan kaki BUY
menutup pada ASK (`close`). Kedua kaki keluar pada harga yang berbeda, terpisah
selisih spread. Akibatnya `grossA + grossB` tidak pernah nol.

Verifikasi:

- `grossB == -grossA` berlaku pada 0,0% event di 7 dari 9 sel, dan 0,08-0,11%
  pada dua sel E2 (selisih pembulatan presisi floating point saja).
- Event dengan exit bersamaan (TIME/TIME) hanya 19,8% dari 10.563 event.
- Pada event TIME/TIME, `grossA + grossB` bernilai median -0,8 pip (bukan 0),
  yang persis sama dengan spread.
- 19,0% event pada E1_N3_k1.0 mengalami kedua kaki rugi bersamaan, karena
  pergerakan harga lebih kecil daripada spread. 0,0% event kedua kaki menang
  bersamaan.

Catatan penting: invarian cermin pada **PnL** hanya berlaku untuk exit
bersamaan. Dengan barrier aktif, kaki A dan B dapat resolve pada bar berbeda,
sehingga invarian itu **tidak dapat dipenuhi** dan tidak boleh diuji sebagai
bukti bug. Yang terbukti benar dan konsisten adalah invarian lintasan:
`MFE_A ~= MAE_B` dan `MFE_B ~= MAE_A` di 9 dari 9 sel, dengan selisih
-4,8% sampai -8,3% yang berasal dari spread.

## A6. Metrik arah yang kebal spread (rekomendasi)

Untuk keputusan-keputusan berikutnya, arah sinyal sebaiknya dinilai dengan
metrik yang tidak bergantung pada PnL:

`Edge = MFE / (MFE + MAE)`, netral pada 0,5.

| sel | MAE/MFE A | Edge A | MAE/MFE B | Edge B |
|---|---|---|---|---|
| E1_N3_k1.0 | 1.45 | 0.408 | 0.79 | 0.560 |
| E1_N3_k1.5 | 1.21 | 0.452 | 0.90 | 0.526 |
| E1_N4_k1.0 | 1.17 | 0.462 | 0.97 | 0.509 |
| E1_N4_k1.5 | 1.68 | 0.372 | 0.66 | 0.602 |
| E1_N6_k1.0 | 1.45 | 0.408 | 0.76 | 0.568 |
| E1_N6_k1.5 | 1.48 | 0.403 | 0.74 | 0.576 |
| E2_W12_k1.5 | 1.03 | 0.493 | 1.10 | 0.477 |
| E2_W12_k2.5 | 1.03 | 0.492 | 1.08 | 0.480 |
| E3_W16 | 0.99 | 0.503 | 1.20 | 0.454 |

Bacaan: E1 kaki A di bawah 0,5 pada 6 dari 6 sel, kaki B di atas 0,5 pada 6 dari
6 sel. Arah sinyal E1 terbalik, konsisten dan tidak bergantung pada definisi WR.
E2 simetris. E3 kaki A sedikit di atas 0,5 dan kaki B di bawahnya; ini koreksi
atas pernyataan "netral" pada laporan sebelumnya.

## A7. Batasan yang harus dipatuhi untuk ronde berikutnya

1. Bed 2024 sudah tidak bersih: pernah dibuka oleh run pip-based yang dikarantina
   dan oleh run native ini. Menjalankan ulang grid yang sama dengan aturan exit
   berbeda di bed yang sama dilarang.
2. Exit mid-price **tidak boleh** dipakai untuk laporan PnL. Mid-price adalah
   idealisasi, bukan eksekusi nyata. Mid hanya sah untuk tes arah tanpa barrier.
3. Jika tes cermin dijalankan, barrier harus dilepas seluruhnya dan kedua kaki
   harus keluar pada bar yang sama. Dengan barrier, tes tersebut tidak bermakna.
4. Semua laporan win-rate berikutnya wajib mencantumkan definisi eksplisit dan
   persentase TIME secara berdampingan.
5. Angka impas wajib dihitung dari mean_win dan mean_loss observatif, bukan
   dari rasio nominal TP/SL.

## A8. Temuan audit sebelumnya yang tetap berlaku

Tidak ada yang dibatalkan oleh addendum ini. Tetap tercatat: penyimpangan
toleransi doji pada E1 yang tidak dideklarasikan coder, spec yang menulis
"delapan sel" padahal grid berisi sembilan sel, ledger tersegel 92 detik sebelum
edit kode terakhir, bootstrap balanced-cluster yang bukan varian textbook,
`failure_map.median_net_B_obs` null akibat propagasi NaN, determinisme hanya
diuji pada 1 dari 9 sel, serta lubang data 21:00-21:45 UTC.

---

Dihasilkan: 2026-10-14. Sumber data: `reports/research/2026-10-14/discovery-R4-M15/evidence/`.
Semua angka pada dokumen ini dihitung ulang dari `events.parquet` dan
`summary.json`, bukan disalin dari laporan sebelumnya.
