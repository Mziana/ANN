# Laporan Tahap 11 — C1: nb05 Q7 Regime (Rancangan EDA v3.1 §5 + Lampiran A1)

**Tanggal:** 2026-10-06 · **Builder:** `scripts/_build_eda05.py` blob `e29e18c7eb98…` (KOREKSI NL2, 2026-10-07: builder +1 langkah pasca-proses EOL sesudah nbconvert (putusan Q2) → blob `e29e18c7eb98…`, sebelumnya `dd3d684a5a95…`; KOREKSI B9-03, 2026-10-07: pin builder dimutakhirkan ke blob aktif pasca Batch C; pin basi `ba11f0792823…` tetap tercatat sebagai riwayat di baris KOREKSI Batch C)
**Notebook:** `notebooks/scalping/eda_05_regimes.ipynb` blob `661c0aeb2357…` (KOREKSI NL2, 2026-10-07: regen LF deterministik 0 CR — KOREKSI M1 2026-10-07: pin lama `2cb57ad9ec1a…` dipensiunkan karena merge chunking output pada regen NL2 — bukan karena era CRLF (provenance)), 26 sel (19 kode), **68 assertion PASS**, nbconvert exit=0 top-to-bottom, output tersimpan.
(KOREKSI pasca-audit Batch A: blob, mtime & count dimutakhirkan — sebelumnya `cc73f794…`/`1155e6de…`/53. KOREKSI pasca-audit Batch B: blob & count dimutakhirkan lagi — sebelumnya `ca997cc9b70a…`/`8158d5b57b20e…`/59; +8 assertion baru: spread per-bar notna ×2, cross-check cost_basis, flag M4, CI/z ACF1 ×2, M3 ×3 — guard M2 B4-03 menggantikan assertion lama sehingga net nol. KOREKSI B7-01: 68 → 67. KOREKSI Batch C: blob & count dimutakhirkan — sebelumnya `ba11f0792823…`/`2d8f600acade…`/67; +1 guard regresi `hour_utc` (B9-01) & koreksi endpoint `placebo_hl` sel H5 (B8-04) — seluruh angka lain identik (deterministik, diverifikasi diff per-sel).)

## File yang dibuat/diubah
- `scripts/_build_eda05.py` (baru) — generator + executor, pola `_build_eda04.py`.
- `notebooks/scalping/eda_05_regimes.ipynb` (baru, di-regenerate via nbconvert — TIDAK diedit langsung).
- `reports/eda/2026-10-06/figures/FIG-04..07.png` (baru; registry = tepat FIG-01..07, verifikasi registry lulus).

## Ringkasan
Q7 dijawab dengan **metrik §5 v3.1** pada granularitas **hari-broker** (R3): bucket D1
kalender-broker (974 bucket, paritas `m1_bars` 974/974) × agregat M1 per hari; strata
A/B/C = pola nb01–nb04 (hari A=825, B=130, C=19; bar A=1.136.401, B=185.248, C=26.198 —
semua di-assert). Tipologi hari (trending/normal/range) dari rasio |ret_day|/Σ|r| dan
range/ATR; ambang = median strata A full-sample 825 hari (`ratio_path=0,0268`, `range_atr=88,7885`) —
deterministik, bukan tuning; label bersifat ex-post/deskriptif, BUKAN ambang real-time
(KOREKSI label pasca-audit L3-01 opsi b; angka tak berubah). Perbandingan A-vs-B level-hari: KS + Mann-Whitney +
Cliff's delta + CI bootstrap beda median; block bootstrap sirkular (block 20 hari,
10.000 resample, seed 20261006) untuk metrik marginal.

## Tabel Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Strata hari A/B/C = 825/130/19; bar = 1.136.401/185.248/26.198 | TERVERIFIKASI | output nb05: `PASS: stratifikasi hari-broker terkunci`; B/C = regression lock Lapisan 1 |
| Bucket D1 = hari broker M1 (kalender tunggal, R3) | TERVERIFIKASI | assertion `set(d1.broker_day) == A∪B∪C`; paritas `m1_bars` 974/974 |
| Warmup ATR14 = 14 hari (semua stratum B) → tipologi dijalankan pada 960 hari | TERVERIFIKASI | `warmup ATR14: 14 hari stratum B` ; n-B tipologi = 116 (drop dilaporkan, nol imputasi) |
| Distribusi tipe hari (n-A=825, n-B=116, n-C=19) | TERVERIFIKASI | crosstab: A = 278/268/279 (33,7/32,5/33,8%); B = 45/30/41 (38,8/25,9/35,3%); C = 7/7/5 |
| Chi-square tipe-hari A vs B | TERVERIFIKASI | chi2=2,248, dof=2, p=0,325 → tidak ada perbedaan komposisi yang terdeteksi |
| RV harian B > A (uji level-hari) | TERVERIFIKASI | median 3,648e-5 vs 2,292e-5 (rasio 1,59×); Cliff δ=−0,384 (konvensi: δ=P(A>B)−P(B>A); negatif = B lebih besar — KOREKSI B4-08); KS p=1,2e-11; CI95-iid beda [1,0e-5, 2,0e-5] (KOREKSI L3-06: sufiks -iid) |
| Σ\|r\| harian B > A | TERVERIFIKASI | beda median 0,0284, CI95-iid [0,0192, 0,0392] (KOREKSI L3-06), δ=−0,394 |
| range/ATR A vs B tidak berbeda | TERVERIFIKASI | beda 2,61, CI95-iid [−7,02, 12,59] (KOREKSI L3-06), δ=−0,010, MW p=0,86 → "tidak terdeteksi pada n ini" (n-B=116) |
| ratio_path A vs B tidak berbeda | TERVERIFIKASI | beda −0,00038, CI95-iid [−0,00515, 0,00335] (KOREKSI L3-06), δ=+0,028, MW p=0,61 |
| Block bootstrap metrik marginal (kedua sisi) | TERVERIFIKASI | range_atr CI-block(kedua sisi) [−7,63, 13,72]; ratio_path [−0,0038, 0,0028] → kesimpulan tidak berubah (tetap memuat 0). KOREKSI pasca-audit L3-02: CI lama satu-sisi-A [−1,72, 6,81]/[−0,0028, 0,0010] cacat (B tak di-resample). Kolom CI utama diganti `ci95_beda_iid` (L3-03) |
| Daya uji + clustering dicatat | TERVERIFIKASI | teks CATATAN DAYA / CATATAN CLUSTERING di output sel #6 |

## Interpretasi singkat (deskriptif, tanpa klaim metode)
Komposisi tipe hari A dan B **tidak terdeteksi berbeda** (chi2 p=0,325), tetapi
**intensitas** harinya berbeda nyata (RV ×1,59, Σ|r| ×1,23) — regime H1-2023 adalah
regime volatilitas, bukan regime bentuk-hari yang lain. Ini menjadi basis H1/H3 di
tahap sintesis (laporan tahap 12).

## Gate pasca rerun (output asli)
```
ruff check          → All checks passed!
ruff format --check → 32 files already formatted
pytest tests/ -q    → 157 passed
validate_data       → 0 error ×4 tahun (LOLOS 2023/2024/2025/2026)
check_foreign_chars → OK: 79 file discan
```

## Riwayat iterasi (kejujuran proses)
nbconvert gagal 3× sebelum lulus — semua assertion-kunci bekerja seperti dirancang:
(1) bucket M15/M5 pembuka `2023-01-01 22:00 UTC` mendahului bar M1 pertama →
`merge_asof` menghasilkan NaN; diganti pencarian interval + assert pengecualian == 1;
(2) replika `fractal_mask` salah (OR per-pasangan → 495/hari vs referensi ≈49) →
diganti salinan verbatim nb04 → 40.483 swing = 49,07/hari (COCOK);
(3) KeyError `hour_utc` (kolom dibuat di salinan) → satu baris diperbaiki;
(4) gate ruff merah (F541 + E402 ×2) → diperbaiki (pola `# noqa: E402` nb01) → rerun
ke-6 lulus penuh. Sign-ACF lag-1 M15-A no-gap = −0,022005 (referensi nb03 −0,022624) ✓.
(Status final pasca-audit Langkah 1: −0,022624 identik nb03, metode eksak no-gap kolom
`gap_return` — lihat KOREKSI tahap 12 H2; angka −0,022005 di atas riwayat iterasi pra-audit.)

## Self-audit 3×
1. **Correctness** — semua angka di atas dibaca dari output notebook tereksekusi di
   disk (nbformat), bukan dari draf; hash/mtime builder & notebook dicatat; registry
   figures di-assert di dalam nb05.
2. **Bias & asumsi** — ambang tipologi = median A full-sample (ex-post/deskriptif,
   dinyatakan eksplisit — L3-01 opsi b); KOREKSI Batch B: tidak ada lagi
   ASUMSI-PROKSI spread sesi — M4 memakai spread p95 per-bar M1 (kanon v3.1 §5),
   proksi mean-D1 lama hanya tercetak sebagai pembanding; effect-size selalu
   disandingkan p-value; kalimat "tidak terdeteksi" dipakai untuk hasil negatif B.
3. **Meta-check** — metrik ≠ karangan: ratio_path/range/ATR/tipologi/chi-square/KS/MW/
   Cliff/bootstrap semuanya tercantum di §5 v3.1; R1–R3 tercatat di markdown nb05 §5.

## Yang belum diverifikasi
- Kesesuaian makro terhadap rancangan belum diaudit (audit Klenz di akhir rantai).
- `report.md` (tahap 13) dan sintesis H1–H5 (tahap 12) SELESAI menyusul laporan ini
  (KOREKSI pasca-audit Batch A L3-01/L3-02/L3-03/L3-05 + L2-02 sudah diterapkan di
  ketiganya; menunggu re-audit Langkah 3).

---

## Koreksi pasca-audit Langkah 1 (replika nb03)
Setelah audit, metode replika VR & sign-ACF di nb05 DISAMAKAN dengan nb03 (ddof=1 +
no-gap via kolom `gap_return`, fungsi `variance_ratio` salinan verbatim `_build_eda03.py`),
sebagaimana rekomendasi konservatif auditor. Angka replika kini: ACF1 = +0,001793 (acf_all
nb03), rata-rata VR(5,15,60) = 1,0312 (referensi benar; 1,0337 = rata-rata VR lag 2–60),
sign-ACF = −0,022624 (identik nb03, n_no_gap 75.038). Angka lama pada baris di atas
(−0,022005) = metode adjacency lama yang diganti; assertion dikunci ketat terhadap angka
referensi + band lebar sebagai lapis kedua. Jumlah assertion notebook kini 59
(53 sebelumnya + 6 baru: paritas bar/gap M15-A, n_no_gap, dan 3 kunci ketat VR/ACF/sign).

## Koreksi pasca-audit Batch B (13 temuan B4-01…B4-12 + B6-04 + L3-06)
HIGH B4-04: M4 diganti spread p95 per-bar (London 2,0823 · Tokyo 1,5992 ·
NewYork 0,9488 · Sydney 0,7975; flag biaya-mendominasi = [NewYork, Sydney]) dengan
cross-check cost_basis fragmen 4b; MEDIUM B4-01 (definisi bucket "range" = hari tenang
+ uji drift relatif), B4-02 (metrik massa London+NY 0,7827 + caveat Tokyo),
B4-03 (guard M2 `n_Off < 2`), B4-05 (klausa kondisional H5 kini punya kontras),
B4-06 (ambang H2 = 3-tahun-utuh, 4-tahun menunggu data), B4-07 (z ACF1 0,494,
CI95 memuat 0 — "terukur" diturunkan), B4-12 (sel M3: DST vs xtab SETUJU);
LOW B4-08 (konvensi tanda δ), B4-09 (dua varian placebo terpisah),
B4-10 (contoh rasio = London), B4-11 (definisi drawdown + "6 jam masuk");
B6-04 + L3-06 ditangani di `report.md`/tabel di atas. Jumlah assertion kini 68
(59 + 8 Batch B + 1 guard regresi `hour_utc` B9-01, di-AST pada sel H4; riwayat:
KOREKSI B7-01 68 → 67, kini KOREKSI B9-01 67 → 68). Detail per-hipotesis = laporan tahap 12.
