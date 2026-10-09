# Verifikasi fix Batch B coder — 2026-10-07

## 1. Hash (5/5 MATCH klaim)
builder `ba11f079…` ✓, notebook `2d8f600a…` ✓, report `0c361137…` ✓,
tahap_11 `6a89ed49…` ✓, tahap_12 `2dfd7bb7…` ✓.

## 2. Isi (spot-check)
- B4-04: M4 p95 per-bar di kode (`spread_p95_bar_pips` quantile 0.95) + assert
  flag == {NewYork, Sydney}; output notebook: rasio 2.0823/1.5992/0.9488/
  0.7975 PERSIS replika audit; flag `['NewYork', 'Sydney']`. ✓
- B4-12: sel M3 baru; output SETUJU, urutan identik, share_Off xtab 0. ✓
- B4-09: output pisah dua varian placebo + batas bawah 0,4890 tampil. ✓
- B4-06: ambang "≥2 dari 3 tahun utuh 2023–2025" di kode. ✓
- Notebook: 26 sel / 19 kode / 0 error. Assert: 67 (indent-aware) vs klaim
  68 — selisih metode hitung, tidak material.
- Catatan jujur coder (78,27% vs 77,17%, beda definisi pembobotan)
  dinyatakan eksplisit — pola kejujuran sehat, diserahkan ke auditor.

## 3. Yang TIDAK diverifikasi baris-per-baris
B4-01 (drift relatif), B4-02 (massa 0,7827), B4-03 (guard), B4-07 (assert z),
B4-08/10/11, B6-04, L3-06 — redaksional + klaim tabel; menjadi objek re-audit.

## Status: siap re-audit Batch B. Q1/Q2 (nb01–nb04 read-only? kalender libur?)
MASIH menunggu putusan user — coder tidak menyentuh keduanya, benar.
