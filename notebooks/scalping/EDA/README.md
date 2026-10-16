# EDA USDJPY 2023–2026

Dokumentasi hasil Exploratory Data Analysis atas data USDJPY per menit (M1).

Semua angka di halaman ini **diambil langsung dari output notebook yang sudah dieksekusi**,
bukan estimasi. Setiap notebook punya assertion yang memverifikasi angkanya sendiri
(11/11 sampai 68/68 PASS).

---

## Rantai EDA

| # | Notebook | Pertanyaan | Verdict |
|---|---|---|---|
| 00 | [Setup & Kontrak](00-setup.md) | Data-nya valid? Aturannya apa? | 11/11 PASS |
| 01 | [Distribusi Return](01-returns.md) | Q1 —(return) seperti apa? | 23/23 PASS |
| 02 | [Volatilitas & Spread](02-volatility.md) | Q2/Q3 — kapan & di mana paling bergerak? Biaya? | 30/30 PASS |
| 03 | [Autokorelasi](03-autocorr.md) | Q4 — ada pola serial yang bisa dieksploitasi? | 31/31 PASS |
| 04 | [Swing & Level](04-swings-levels.md) | Q5/Q6 — apakah level "dihormati"? | 30/30 PASS |
| 05 | [Regime & Sintesis](05-regimes.md) | Q7 — tipe hari + 5 hipotesis kandidat | 68/68 PASS |

---

## Dua facts yang harus selalu diingat

### 1. Data ini dimuat sampai Oktober 2026

```
2023-01-01 22:07 UTC  ──▶  2026-10-02 20:57 UTC
1.347.847 bar M1  ·  974 hari broker
```

| Tahun | Bar M1 |
|---|---|
| 2023 | 362.693 |
| 2024 | 358.331 |
| 2025 | 356.977 |
| **2026** | **269.846 (20,0%)** |

Dari 974 hari broker: **A = 825** (utama), **B = 130** (H1-2023, regime spread ribut),
**C = 19** (jendela anomali).

**Konsekuensi:** 220 dari 825 hari stratum A adalah hari 2026. EDA-01…05 menganalisis
2026 secara langsung, dan ambang tipologi hari di EDA-05 dihitung dari seluruh 825 hari
(termasuk 2026). Akibatnya **2026 tidak bisa lagi dipakai sebagai holdout murni**.

---

### 2. Tiga temuan negatif yang kokoh

Ini bukan "belum diperiksa" — ini **sudah diuji dan hasilnya tidak mendukung sinyal arah**:

| Temuan | Angka | Sumber |
|---|---|---|
| Autokorelasi ≈ nol | `max|ACF| = 0,0226` | EDA-03 |
| Level tidak beat placebo | nyata `0,469–0,490` vs placebo `0,483–0,514` | EDA-04 |
| Komposisi hari A ≈ B | χ² = 2,248, dof 2, p = 0,325 | EDA-05 |

Ditambah EDA-05 H2 yang sudah tertulis eksplisit:
> "Momentum M15 lemah, **tak terbedakan dari iid**"

---

## Yang TIDAK dikerjakan di tahap ini

Sengaja, dan tercatat di setiap notebook:

- Tidak ada P&L, equity curve, atau simulasi profit
- Tidak ada sinyal, model, atau pemilihan metode strategi
- Tidak ada penulisan ke `configs/` atau `src/` (kecuali fragmen spread yang sudah
  disetujui terpisah pada langkah 4b)
- Tidak ada imputasi — data yang dibuang selalu dilaporkan jumlahnya

**Status akhir EDA:** berhenti di hipotesis. Metode belum dipilih.

---

## Data biaya broker

Angka spread di dokumentasi ini (terutama [02-volatility.md](02-volatility.md))
berasal dari configs/broker.yaml dan bisa diaudit ulang dari parquet M1.

Ringkasan biaya round-turn per 1 lot:

| Skenario | Spread | Total | Setara pip |
|---|---|---|---|
| Cheap (mean London/NY 2026) | 0,61 | $10,17 | 1,52 |
| **Mid (default backtest)** | **0,65** | **$10,70** | **1,60** |
| Expensive (Sydney p95) | 1,50 | $22,08 | 3,30 |
| Krisis (H1-2023 p95) | 5,30 | $72,95 | 10,90 |

Komisi $1,00/lot per sisi hanya ~19% dari total; spread ~81%.
Rincian dan daftar yang masih perlu diverifikasi: [docs/broker-contract-finex.md](../../../docs/broker-contract-finex.md)

## Struktur folder

```
notebooks/scalping/
├── eda_00_setup.ipynb          ← notebook (dieksekusi)
├── eda_01_returns.ipynb
├── eda_02_volatility.ipynb
├── eda_03_autocorr.ipynb
├── eda_04_swings_levels.ipynb
├── eda_05_regimes.ipynb
├── _eda_common.py              ← helper bersama (fingerprint sesi)
├── EDA/                        ← dokumentasi ini
└── archive/
    └── eda-06-07/              ← EDA-06/07 dipensiunkan, baca README-nya
```

---

## Cara menjalankan ulang

```powershell
venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute `
  --output-dir notebooks/scalping notebooks\scalping\eda_00_setup.ipynb
```

Notebook berjalan top-to-bottom tanpa gerbang per sel. Gerbang keputusan ada di bagian akhir.
Butuh `venv/` (Python 3.12.8, pandas 2.2.3, `tzdata==2026.5`).
