# Laporan Tahap 10 — Rework nb03 (D1–D5, Q4 autokorelasi)

**Tanggal:** 2026-10-06
**Jenis:** laporan mini Langkah 2 (rework + regenerate). **Bukan addendum** — menggantikan
bagian `laporan_tahap_5_autokorelasi.md` yang berubah pasca-verdict Spark.
**Rancangan acuan:** `reports/governance/2026-10-06/decisions/eda_design_v3.1.md` §5 (baris 65–66).
**Verdict acuan:** `reports/governance/2026-10-06/decisions/eda_review_deviations_v1.md` — D1–D5 INVALID.

## File yang diubah

| File | Blob SEBELUM (HEAD `e4efbfd`) | Blob SESUDAH (worktree) | mtime |
|---|---|---|---|
| `scripts/_build_eda03.py` (sumber kebenaran) | `80280952b976eb47b0209b1fc3d1e647e4d9db21` | `7536fd221fcab0912795de98f93e7e593775d76c` | 2026-10-06 14:23:43 |
| `notebooks/scalping/eda_03_autocorr.ipynb` (artefak) | `57f020815c55eeb0a974a0c738d05e0fae7c25b5` | `0158ca994db9b335db9bc0c2eddba0ee939d1af0` | 2026-10-06 14:24:10 |

nb03 = **25 sel (12 sel kode)**. Notebook **tidak** diedit langsung; diregenerasi top-to-bottom
via nbconvert di dalam `build()` builder (Reuse-First §16).

## Apa yang dilakukan

Menutup 5 deviasi nb03 (D1–D5) dengan mengubah builder lalu mengeksekusi ulang:

- **D1** — ACF diperluas dari lag 1–20 ke **lag 1–60**.
- **D2** — **uji Ljung-Box** diimplementasikan manual via scipy (tanpa dependensi baru).
- **D3** — variance-ratio dilaporkan pada **horizon kontrak 5/15/60** (di samping kurva penuh 1–60).
- **D4** — **sign-autocorrelation lag-1** (ACF dari tanda return) ditambahkan.
- **D5** — seluruh metrik headline diulang untuk **strata A dan B** + tabel selisih A vs B.

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| D1: lag 1–60 | TERVERIFIKASI | `scripts/_build_eda03.py:247` `LAGS = list(range(1, 61))`; output nb03 sel 7 memuat baris lag 1..60; assertion "ACF dihitung untuk 60 lag (1-60)" PASS |
| D2: Ljung-Box manual scipy | TERVERIFIKASI | `_build_eda03.py:321` `def ljung_box(...)`; `:348` `p = float(stats.chi2.sf(q, h))`; output sel 9 memuat h=5/15/60 untuk A **dan** B |
| D3: VR horizon 5/15/60 | TERVERIFIKASI | output sel 13 blok "VR pada horizon kontrak (5, 15, 60)"; assertion "VR memuat horizon kontrak 5/15/60" PASS |
| D4: sign-ACF lag-1 | TERVERIFIKASI | markdown §2c (md sel 10); kolom `sign_acf1` di builder `:500`/`:516`; output sel 11 — semua sel negatif |
| D5: strata A vs B | TERVERIFIKASI | `_build_eda03.py:209` `STRATA_B` + `:218` `STRATA = {"A":..., "B":...}`; output sel 21 tabel "Delta A vs B (B - A)"; assertion "Tabel delta A vs B lengkap (3 TF)" PASS |
| Ringkasan assertion | TERVERIFIKASI | output sel 23: `RINGKASAN: 31/31 assertion PASS untuk Q4 autokorelasi.` |
| Klaim lama "\|ACF\| ≤ 0,012 di semua TF" | **GAGAL/DICABUT** | terbantahkan oleh data sendiri |
| Maks \|ACF\| lintas strata/TF/lag 1–60 = **0,022639** (strata B, M15, lag 50, no-gap) | TERVERIFIKASI | output nb03 sel 7, tabel ACF strata B (M15) baris lag 50: `acf_no_gap = -0.022639` |

## Angka kunci (no-gap, lag 1–60)

| Metrik | A M1 | A M5 | A M15 | B M1 | B M5 | B M15 |
|---|---|---|---|---|---|---|
| ACF lag-1 | −0,004372 | −0,011582 | +0,003496 | −0,000864 | −0,005795 | +0,005980 |
| sign-ACF lag-1 | −0,017702 | −0,009805 | −0,022624 | −0,013226 | −0,012994 | −0,017336 |
| rata-rata VR(lag 2–60) | 0,9796 | 0,9942 | 1,0337 | 0,9848 | 1,0332 | 1,0236 |
| VR pada k=60 | 0,9809 | 0,9992 | 1,0657 | 0,9916 | 1,0564 | 0,9631 |

`VR(1) = 1,0000` di semua strata/TF (definisi). **sign-ACF negatif di semua sel** dan
magnitudonya **lebih besar** daripada ACF mentah absen-gap (mis. A M1: 0,017702 vs 0,004372)
→ mean-reversion jangka sangat pendek lebih terbaca di tanda daripada di besaran.
**Struktur tetap muncul di lag 21–60** (mis. A M1 lag 23 = +0,005862; lag 30 = −0,004757),
di luar jendela lama 1–20.

## Aturan baca Ljung-Box (mengikat)

`ATURAN BACA: p bukan kesimpulan; baca Q/n + besaran rho_k; slice = bacaan utama.`
(`_build_eda03.py:364`; keputusan Architect atas keberatan coder, `:308`). Pada n > 1 juta bar,
reject hampir pasti → **p-value BUKAN temuan**. Contoh Q/n(h=15) A M1 = 0,000143 vs B M15 = 0,001423.

## Keterbatasan daya strata B (unbalanced)

B = H1-2023, hanya ±6 bulan; n kecil (M15 B = 12.430). Ljung-Box B M15 h=60 → p = 0,2995.
Hasil negatif di B dibaca **"tidak terdeteksi pada n ini"**, bukan bukti kesamaan
(`_build_eda03.py:646`; md sel 20).

## Gate (dijalankan ulang pasca regenerate; output nyata)

- `ruff check notebooks/scalping/eda_03_autocorr.ipynb scripts/_build_eda03.py` → `All checks passed!` (rc=0)
- `ruff format --check notebooks/scalping/eda_03_autocorr.ipynb scripts/_build_eda03.py` → `2 files already formatted` (rc=0)
- `ruff check src/ tests/ scripts/ notebooks/` (repo) → `All checks passed!`; `ruff format --check` → `29 files already formatted`
- `pytest tests/ -q` (repo) → **157 passed**
- `python -m src.data.validate_data` (repo) → 0 error untuk 4 tahun (2023–2026) → LOLOS
- `python scripts/check_foreign_chars.py` → `OK: 68 file discan, tidak ada karakter asing.`

## Self-audit adversarial 3×

1. **Correctness** — setiap klaim di atas berjangkar file:baris atau output sel (sel 7/9/11/13/21/23).
   Blob before/after diambil dari `git hash-object` (worktree) dan `git show HEAD:… | git hash-object`
   (baseline `e4efbfd`), bukan dari ingatan.
2. **Bias & asumsi** — tidak ada klaim teori statistik baru; horizon VR (5/15/60) diambil persis
   dari rancangan §5, bukan dipilih sendiri. p-value tidak dipakai sebagai kesimpulan (aturan baca).
   Angka sign-ACF/VR dilaporkan apa adanya, termasuk yang lemah (M15 momentum tipis).
3. **Meta-check** — klaim lama `|ACF| ≤ 0,012` **dicabut**, bukan dibiarkan. Tidak ada file di
   luar scope tersentuh. (Catatan: temuan koreksi-diri "SA-47" — assertion tanda delta yang sempat
   terbalik — **dilaporkan pada sesi L2**; **tidak ada log di disk** untuk memverifikasi ulang
   nomor pass-nya. Status: BELUM DIVERIFIKASI, bukan klaim.)

## Yang belum diverifikasi

- Kebenaran teori di balik metrik (ACF/Ljung-Box/VR/sign-ACF) — wilayah desain, sudah diputuskan;
  di luar scope laporan ini.
- Angka per-lag penuh 60×6 sel tidak dikutip satu-satu di sini; dirujuk ke output nb03 sel 7.
