# AUDIT LAPISAN 3 — FOUNDATION FEATURES

> **Catatan arsiparis (bukan bagian laporan):** berkas ini salinan laporan
> audit fondasi B1 dari chat sesi 2026-10-07. Isi analitik tidak diubah,
> kecuali 3 sisipan Han (artefak probe auditor) yang diganti placeholder
> kode Unicode agar lolos gate `check_foreign_chars.py`:
> `Setelah[HAN U+7684 U+63A7 U+5236] volatilitas`,
> `hanya[HAN U+673A U+5236 U+7684]`,
> `ditangani[HAN U+663E U+5F0F]`.
> Pemulihan eksak: ganti tiap placeholder dengan karakter Han pada kode
> yang tercantum, tanpa spasi tambahan.

**Objek** (hash terverifikasi, tidak berubah selama audit):
- `src/features/build_features.py` → `1c9da4b4d6d108de…` (397 baris)
- `tests/test_build_features.py` → `f0171c2756729700…`
- `data/features/M15/usdjpy_m15_features.parquet` → `07402f40478aaed9…` (90.041 × 11)

**Metode**: 17 probe independen di luar suite coder, plus gate repo. Tidak ada file produksi yang diubah.

---

## A. PERFORMA

Build penuh2,61 s pada data nyata (1.347.847 bar M1).

| Tahap | Waktu |
|---|---|
| `load_processed M1` | 0,62 s |
| `load_processed M15` | 0,04 s |
| `daily_metrics` | 2,14 s |
| `session_flags` (4× `tz_convert`) | 1,62 s |
| `_assert_daily_is_previous_day` | 0,30 s (11,5% total) |

Memori: M1 186 MiB, M15 13 MiB, fitur9,5 MiB, parquet 0,92 MiB.

**Tidak ada temuan performa.** Guard3.896 panggilan `np.allclose` pada array ~92 elemen adalah 11,5% dari runtime — mahal relatif, tetapi tidak material pada 2,6 s.

**CATATAN (saran proses, bukan temuan):** `build_features` memanggil `prepare_bars(m15)` di baris 279, dan `daily_metrics` memanggilnya lagi di baris 234. M15 disalin + di-sort dua kali per build (~0,25 s). Module 397/400 baris dan `daily_metrics` 49/50 baris — keduanya di bawah batas, tapi tidak ruang untuk fitur B2. Rekomendasi: pecah `daily_metrics` menjadi `_daily_ohlc` + `_daily_intraday` saat B2 dimulai. Bukan temuan severity.

---

## B. ANALISIS EDGE

**Kalender & paritas** — lulus penuh:
- M1 dan M15 masing-masing 974 broker-day, himpunan identik.
- OHLC agregat M15 identik dengan D1 untuk seluruh 974 hari.
- Index UTC monotonik, tanpa duplikat, `date_broker` naive.

**Attach D−1 posisional** — 973 hari diperiksa tanpa aritmetika kalender:

```
mismatches per column: {'atr_14_d1': 0, 'rv_roll_20d': 0,
                         'range_atr': 0, 'ratio_path': 0}
```

**Weekend shift** — 199 transisi dengan gap >1 hari (2/3/4 hari). Senin 2023-01-09 membawa persis nilai Jumat 2023-01-06 di keempat kolom (`ratio_path` identik 14 digit). Positional attach benar: gap kalender diabaikan, hari perdagangan terakhir yang menjadi jangkar.

**Bucket M15 parsial** — 1.281 dari 90.041 (1,42%). Terverifikasi ulang: 1.281 = 357 day-final + 327 day-first + 597 mid-day. Distribusi `m1_bars`: 14→771, 13→274, 8→101. Bucket `m1_bars=8` adalah artefak sesi FX 23 jam (22:00→23:00 broker), normal, bukan defect.

**DST** — `Europe/London` BST→GMT tiap Oktober terakhir: 2023-10-29, 2024-10-27, 2025-10-26, 2026-10-25. Transisi broker Finex (Maret/Nov) jatuh pada hari libur — tanpa bar, sehingga tidak ada efek transisi pada flag sesi. Flag berbasis `tz_convert` sehingga benar secara konstruktif, bukan hanya secara empiris.

**Label vs prioritas** — 0 pelanggaran dari 90.041 bar pada kelima label, memakai aturan yang benar (label L ⟺ flag_L aktif dan tidak ada flag prioritas lebih tinggi).

---

## E. BIAS / LOOK-AHEAD / LEAKAGE

### E1. Anti-look-ahead: LULUS

Truncation input pada tiga titik — `2024-06-28`, `2025-03-14`, `2026-03-20` — menghasilkan prefix yang identik dengan build penuh. Broker-day terakhir `2026-10-02` membawa nilai `2026-10-01`.

Probe same-day: 19 dari 974 hari bernilai sama dengan nilai harinya sendiri — **semuanya artefak warmup NaN** (`atr` 14 hari, `rv` 19 hari, semuanya di stratum B awal 2023). `ratio_path` sendiri-equal0 hari. Tidak ada leak.

### E2. Reproduksi kontrak ambang: LULUS

Stratum kanon direkonstruksi persis dari `scripts/_build_eda05.py:181-192` (B = 2023-01-01…2023-06-30, C = dua anomaly window, A = sisanya):

```
hari A=825  B=130  C=19          (notebook: 825/130/19 ✓)
bar  A=1.136.401  B=185.248  C=26.198  (notebook ✓)
```

| | `build_features` | D1 (sumber EDA) | Lock |
|---|---|---|---|
| median A `ratio_path` | 0,026810 | 0,026810 | 0,0268 |
| median A `range_atr` | 88,7885 | 88,7885 | 88,79 |
| shares A | trending 33,7% / normal 32,5% / range 33,8% | — | identik |

Seluruh 14 hari warmup ATR berada di stratum B, sesuai `_build_eda05.py:279`. Kontrak H1 tereproduksi tanpa deviasi. Angka EDA tidak dinilai ulang.

### E3. Kontras rv_day H3: LULUS

`rv_roll_20d` terbukti **rolling sum**, bukan mean (`np.allclose` terhadap sum: True, terhadap mean: False). Kontras stratum pada satuan yang benar: A = 2,2917e-5, B = 3,6477e-5, rasio **1,5917** — lock 1,59. ✓

---

## TEMUAN

### F-1 · MEDIUM — Jendela anomali tidak dikuarantinasi di feature store

**Klaim**: config menandai19 hari broker sebagai terlarang untuk fitur sesi, dan store memakainya tanpa penanda.

**Bukti** — `configs/data.yaml:184-198` menyatakan untuk kedua jendela: *"jangan dipakai untuk fitur sesi Tokyo/London/NY sebelum sebabnya dikonfirmasi ke Finex."* Kode tidak membaca `anomaly_windows` sama sekali.

```
window 2024-10-28..2024-11-01: 460 bar, 5 hari, 0,51% store
window 2026-03-10..2026-03-27: 1288 bar, 14 hari, 1,43% store
NaN di kolom harian pada kedua jendela: 0
kolom penanda di store: TIDAK ADA
```

**Nuance yang diverifikasi**: flag sesi sendiri **tidak** korup — `session_flags` membaca `utc` (baris 119), bukan jam broker. Yang bergeser adalah `date_broker`, sehingga attach baris harian yang berbeda: simulasi offset salah 1 jam → 20 bar (jendela 1) dan 56 bar (jendela 2) attaching hari berbeda, 4 dan 8 bar jadi NaN.

**Konsumen**: B2 H4 (EV-after-cost per jam sesi) dan H5 (placebo bersyarat kuartil-ATR × sesi) — keduanya menghitung statistik per sesi pada hari-hari ini. B2 hanya bisaDeadline untuk patas dengan membaca ulang config dan mem-mask `date_broker`; store tidak mem_ENABLE check.

**Perbaikan**: tambah kolom `is_anomaly_window` (bool) dari `configs/data.yaml:184`, atau hapus larangan dari config bila offset sudah dikonfirmasi Finex.

### F-2 · LOW — Kelengkapan bucket M15 (`m1_bars`) dibuang

**Klaim**: 597 bucket M15 mid-day kekurangan bar M1, dan store tidak menyimpan penandanya.

**Bukti**: `m1_bars` ada di parquet M15 tapi tidak ada di `FEATURE_COLUMNS` (baris 68). 1.281 bucket parsial; 597 di antaranya mid-day (bukan boundary sesi) — spread di 234 hari broker. Uji kausal: menghapus tepat bar M1 bermasalah lalu hitung ulang, `ratio_path` berubah median **+0,019%**, p95 +0,28%, maks +1,06%; `range_atr` **0,000%** (OHLC D1 berasal dari M15, tidak terpengaruh). Efeknya kecil karena log-return bersifat teleskopik — menghapus satu bar menyatukannya ke return berikutnya, sehingga jumlah `|r|` nyaris kekal.

Pernyataan "gap elevate `ratio_path`" yang saya duga di probe sebelumnya **salah**: median hari bergap justru lebih rendah (0,0251 vs 0,0280), karena hari bergap lebih tenang. Setelah[HAN U+7684 U+63A7 U+5236] volatilitas (desil), rasio 1,076 — confounding, bukan efek gap.

**Konsumen**: B2 H1 (klasifikasi tipologi) dan H5 (kuartil ATR). Dampak kecil sehingga LOW, bukan MEDIUM.

### F-3 · LOW — Docstring `main()` menjanjikan exit code yang tidak ada

**Klaim**: baris 369 bled, cabang tidak pernah dieksekusi.

**Bukti**:
```
return statements in main(): [32]
constant return values: [0]
```
Tidak ada `try:` di `main()`. `load_processed` melempar `FileNotFoundError` (baris 205) yang tak tertangkap. Interpreter memberi exit code **1** — kebetulan sama dengan yang dijanjikan, jadi perilaku yang teramati benar, hanya[HAN U+673A U+5236 U+7684]. Kategori LOW: cacat dokumentasi, bukan perilaku. Caller yang hanya mengecek `returncode != 0` tidak terpengaruh.

### F-4 · LOW — `daily_metrics` tidakMDAkits cek panjang

**Klaim**: join `how="inner"` (baris 252) membuang hari secara senyap bila cakupan tahun M1 ≠ M15.

**Bukti**: M1 dipotong → `daily` menyusut974 → 145, **829 hari hilang tanpa peringatan**. Tidak ada assertion panjang. Tidak terpicu pada data sekarang, dan direktori kosong memicu `FileNotFoundError` bergema. Baru relevan bila file parquet satu timeframe hilang sementara timeframe lain ada — skenario yang harus ditangani[HAN U+663E U+5F0F].

---

## CATATAN (bukan temuan)

- **`rv_roll_20d` adalah SUM20 hari**, sedangkan basis lock H3 adalah `rv_day` (2,292e-5 vs 3,648e-5). Konsumen B2 harus membagi 20 agar skala cocok. Sudah terdokumentasi di docstring modul baris 13 dan 16-18.
- **`n_Off` H4 terkonfirmasi.** Klaim lock "share Off = 0,0; n Off = 0" merujuk ke **6 jam teratas** — diverifikasi 0 bar Off di `[14,13,0,15,12,7]`. Store punya 220 bar Off di luar6 jam itu; itu bukan pelanggaran kontrak.
- **Tidak ada kolom spread/cost** di store — ini kepatuhan B1-1 yang disengaja (baris 60). M15 menyediakan `spread_pips_mean`/`spread_pips_max` untuk placebo H5; M1 menyediakan `spread_pips`. Keduanya dibaca langsung per doktrin D0.
- **H1-H5 sufficiency**: H1sufficient (4 kolom harian + join M15). H2 sufficient (M5 by direct read, `cost_basis.by_session` ada). H3 sufficient dengan caveat satuan. H4 sufficient. H5 sufficient via `spread_pips_max`.
- **Pipeline** deterministik: M15 di-shuffle → output identik (`prepare_bars` sort mergesort, baris 177).

---

## BLOKIR: KEPATUHAN B1 TIDAK DAPAT DITUTUP

Putusan arsitek B1 berisi 4 butir + 4 redaksi eksak **tidak ada di repository**:

```
git log --all -S 'B1-3|B1-4'  ->  0 commits
file pernah di-commit matching b1/arsitek/putusan:
  .ai/assistant/prompts/2026-10-07_tanya-arsitek-determinisme-full.md
  .ai/assistant/prompts/2026-10-07_tanya-arsitek-determinisme.md
  .ai/assistant/prompts/PERAN-arsitek.md
  reports/governance/2026-10-07/putusan-arsitek-H1-H5.md   (H1-H5, bukan B1)
```

Hanya dua klaim yang dapat diverifikasi dari artefak:

| Klaim | Lokasi | Status |
|---|---|---|
| B1-1 — kolom spread tidak ditambahkan; H5 baca `spread_pips` M1 langsung per D0 | `build_features.py:60` | **TERPENUHI** — tidak ada kolom spread di store |
| B1-2 — M5 bukan input; H2 baca parquet M5 langsung per D0 | `build_features.py:20-21`, signature `build_features(m1, m15, pip_size)` | **TERPENUHI** |
| B1-3 | — | **TIDAK DAPAT DIADJUDIKASI** |
| B1-4 | — | **TIDAK DAPAT DIADJUDIKASI** |
| Doktrin D0 | rujukan di baris 21, 60 | Definisi D0 tidak ada di repo; hanya implementasi lewat B1-1/B1-2 yang terverifikasi |

Saya tidak menyusun ulang isi B1 dari komentar kode. Butir 3 dan 4 tetap terbuka sampai sumbernya disediakan.

---

## GATE REPO

```
pytest                     191 passed
pytest test_build_features  34 passed
ruff check                 All checks passed
ruff format --check        2 files already formatted
check_foreign_chars OK, no foreign characters
```

Hash ketiga objek tidak berubah selama audit. Tidak ada file produksi yang disentuh.

---

## SELF-AUDIT

**Putaran 1 — koreksi**: empat klaim awal saya salah dan sudah dikoreksi lewat probe ulang, bukan lewat penalaran: logika weekend-shift terbalik (`t2`→`t3`); nama kolom spread M15 (`t6`); arah bias gap (`t11`→`t12`); exit code (`t6`→`t17`). Klaim "guard vakum" **dibantah**: guard terbukti_bits shoot pada injeksi same-day maupun future-day pasca-warmup.

**Putaran 2 — bias**: setiap temuan_downgrade setelah uji yang bisa menyalahkannya — `m1_bars` turun dari MEDIUM ke LOW setelah uji kausal menunjukkan efek +0,019%; exit code turun ke LOW setelah terlihat interpreter sudah memberi 1; F-1 tetap MEDIUM karena larangan config eksplisit. Tidak ada angka EDA yang dievaluasi ulang; ambang hanya diverifikasi sebagai kontrak pada stratum A.

**Putaran 3 — meta**: verifikasi dilakukan lewat probe sendiri, bukan lewat suite coder. Butir B1 yang hilang saya nyatakan terbuka, bukan direkonstruksi. Residual: `write_features` (kompresi/partitioning) tidak diaudit karena tidak ada kontrak yang ditemukan, dan paritas D1-vs-M15 hanya diuji agregat (lulus), bukan per tahun.

**Vonis: 0 HIGH, 1 MEDIUM, 3 LOW.** Fondasi layak dipakai B2; F-1 perlu diputuskan sebelum H4/H5 dijalankan, karena keduanya menghitung statistik per sesi pada hari-hari yang config tandai terlarang.
