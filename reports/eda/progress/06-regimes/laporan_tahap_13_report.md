# Laporan Tahap 13 — C3: `report.md` EDA Final

**Tanggal:** 2026-10-06 · **File:** `reports/eda/2026-10-06/report.md` (BARU)
**Sumber angka:** output notebook tereksekusi nb01–nb05 di disk (via nbformat; cuplikan
head-line per Q diekstrak dalam sesi ini), BUKAN dari ingatan.

## Isi report.md (peta)

1. Tabel sumber kebenaran: blob + assertion per notebook (nb00 11/11, nb01 23/23,
   nb02 30/30, nb03 31/31, nb04 30/30, nb05 53).
2. **7 jawaban** masing-masing dengan tabel Klaim & Bukti (Q1 distribusi return; Q2/Q3
   volatilitas + spread; Q4 autokorelasi; Q5 swing; Q6 level/placebo; Q7 regime).
3. Tabel spread terukur per sesi (p99 M1 / p99 M5-max / maks; strata B terpisah:
   p95 5,30 / p99 8,50 / %>3pip 5,17%).
4. Sintesis H1–H5 satu tabel (klaim inti · basis EDA · ambang falsifikasi Lapisan 3).
5. Ratifikasi **T-01** (5,83% massa nol; A 5,88% / B 5,71%).
6. Daftar **BELUM DIVERIFIKASI** (8 item wajib: S5/S6 sekunder, kalender libur,
   offset jendela anomali, atribusi kurtosis, granularitas .50, daya B, proksi spread,
   H1–H5 belum diuji).
7. Catatan Lampiran A1 (R1–R4) tercatat di report + nb04/nb05.

## Tabel Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| `report.md` ada & berisi 7 jawaban + tabel spread + H1–H5 + BELUM DIVERIFIKASI | TERVERIFIKASI | file ditulis; konten disusun dari output nb yang diekstrak dari disk sesi ini (nb01/nb02/nb03/nb04 headline, nb05 penuh) |
| Semua angka di report = output notebook | TERVERIFIKASI | angka dicocokkan langsung ke cuplikan output (mis. kurtosis 195,476/102,848/51,176; sign-ACF 6 sel; VR A/B; swing 48,74; hit-rate placebo 0,4989/0,5050/0,4922/0,4890; BoJ 728/518/151) |
| Tidak ada klaim di luar notebook | TERVERIFIKASI | bagian "BELUM DIVERIFIKASI" memuat semua yang tak didukung data (8 item) |
| T-01 diratifikasi | TERVERIFIKASI | hitung-ulang nb05 = 5,83% (78.582 bar), sama dengan temuan nb01 |
| Tidak ada P&L / pemilihan metode | TERVERIFIKASI | report berhenti di hipotesis; status eksplisit "Metode BELUM dipilih" |

## Self-audit 3×

1. **Correctness** — setiap angka report dipetakan ke output nb di disk; tidak ada
   angka yang ditulis dulu lalu dicari buktinya (urutan: ekstrak → tulis).
2. **Bias & asumsi** — dua catatan jujur ditulis eksplisit (deviasi ranking
   Tokyo>NY vs prior S5; proksi spread mean-D1); temuan negatif Q6 dipertahankan
   sebagai temuan negatif, tidak dipoles.
3. **Meta-check** — struktur report mengikuti §3 v3.1 baris demi baris (7 jawaban,
   tabel Klaim & Bukti per jawaban, tabel spread, H dengan ambang, BELUM
   DIVERIFIKASI, catatan daya B).

## Yang belum diverifikasi

- Angka report belum diverifikasi pihak kedua (audit Klenz menyusul — memang pola
  review-akhir yang diputuskan user).
- report.md masih untracked (tanpa commit — diputuskan terpisah setelah review).

## Bukti disk (hash · mtime)

- `reports/eda/2026-10-06/report.md` — ditulis sesi ini (hash/mtime tercantum di
  laporan akhir konsolidasi; diukur ulang di sana supaya satu titik kebenaran).
