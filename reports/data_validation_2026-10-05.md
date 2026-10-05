# Laporan Validasi Data

**Verdict: LOLOS** (0 error, 6 peringatan)

| Tahun | Bar | Hari | Error | Peringatan |
|---|---|---|---|---|
| 2023 | 362,693 | 163 | 0 | 2 |
| 2024 | 358,331 | 260 | 0 | 2 |
| 2025 | 356,977 | 259 | 0 | 1 |
| 2026 | 269,846 | 196 | 0 | 1 |

## 2023

| Check | Severity | Status | Detail |
|---|---|---|---|
| Jumlah bar per hari | ERROR | LOLOS | 311 hari: 259 penuh, 52 parsial |
| Duplikat | ERROR | LOLOS | tidak ada timestamp duplikat |
| Monoton | ERROR | LOLOS | monoton naik |
| OHLC valid | ERROR | LOLOS | 362,693 bar konsisten (h>=l, h>=o/c, l<=o/c) |
| Gap | WARN | GAGAL | break harian 111, akhir pekan 50, tak wajar 2 | terbesar: 4381 mnt, 29 mnt |
| Spread 2023 | WARN | GAGAL | median 0.60 pip, p95 1.20, p99 8.50, maks 34.30 | config 3.00 pip (warn > 6.00, error > 15.00) |
| Jam break | WARN | LOLOS | jam dinding dominan 4, dipakai 100% dari 111 break |
| Anomali diketahui | WARN | LOLOS | tidak ada |

## 2024

| Check | Severity | Status | Detail |
|---|---|---|---|
| Jumlah bar per hari | ERROR | LOLOS | 314 hari: 260 penuh, 54 parsial |
| Duplikat | ERROR | LOLOS | tidak ada timestamp duplikat |
| Monoton | ERROR | LOLOS | monoton naik |
| OHLC valid | ERROR | LOLOS | 358,331 bar konsisten (h>=l, h>=o/c, l<=o/c) |
| Gap | WARN | GAGAL | break harian 206, akhir pekan 52, tak wajar 1 | terbesar: 1511 mnt |
| Spread 2024 | INFO | LOLOS | median 0.60 pip, p95 1.20, p99 1.70, maks 55.60 | config 1.50 pip (warn > 3.00, error > 7.50) |
| Jam break | WARN | LOLOS | jam dinding dominan 4, dipakai 98% dari 206 break |
| Anomali diketahui | WARN | GAGAL | 2024-10-29..2024-11-01 (break harian di jam dinding 3, bukan 4) |

## 2025

| Check | Severity | Status | Detail |
|---|---|---|---|
| Jumlah bar per hari | ERROR | LOLOS | 313 hari: 259 penuh, 54 parsial |
| Duplikat | ERROR | LOLOS | tidak ada timestamp duplikat |
| Monoton | ERROR | LOLOS | monoton naik |
| OHLC valid | ERROR | LOLOS | 356,977 bar konsisten (h>=l, h>=o/c, l<=o/c) |
| Gap | WARN | GAGAL | break harian 205, akhir pekan 52, tak wajar 1 | terbesar: 1501 mnt |
| Spread 2025 | INFO | LOLOS | median 0.60 pip, p95 1.00, p99 1.70, maks 24.10 | config 1.50 pip (warn > 3.00, error > 7.50) |
| Jam break | WARN | LOLOS | jam dinding dominan 4, dipakai 100% dari 205 break |
| Anomali diketahui | WARN | LOLOS | tidak ada |

## 2026

| Check | Severity | Status | Detail |
|---|---|---|---|
| Jumlah bar per hari | ERROR | LOLOS | 236 hari: 196 penuh, 40 parsial |
| Duplikat | ERROR | LOLOS | tidak ada timestamp duplikat |
| Monoton | ERROR | LOLOS | monoton naik |
| OHLC valid | ERROR | LOLOS | 269,846 bar konsisten (h>=l, h>=o/c, l<=o/c) |
| Gap | WARN | LOLOS | break harian 156, akhir pekan 39, tak wajar 0 |
| Spread 2026 | INFO | LOLOS | median 0.60 pip, p95 0.70, p99 1.20, maks 16.70 | config 1.50 pip (warn > 3.00, error > 7.50) |
| Jam break | WARN | LOLOS | jam dinding dominan 4, dipakai 92% dari 156 break |
| Anomali diketahui | WARN | GAGAL | 2026-03-10..2026-03-27 (break harian di jam dinding 3, bukan 4) |
