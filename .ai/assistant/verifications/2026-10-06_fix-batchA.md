# Verifikasi perbaikan Batch A oleh coder baru — 2026-10-06

## 1. Hash (5/5 MATCH prefix klaim)
builder `ca997cc9…` ✓, notebook `8158d5b5…` ✓, report `2f86eed6…` ✓,
tahap_11 `131e8222…` ✓, tahap_12 `e48c8b32…` ✓.
(Catatan: builder BERUBAH dari `8ac848ce…` yang diaudit → wajar, fix
diterapkan. Re-audit wajib atas blob BARU ini.)

## 2. Isi kode (spot-check)
- L3-01b: label "ex-post — bukan ambang real-time" di print (:286),
  komentar (:239), dan bagian report (:948-949). Ambang angka tak berubah
  (0,0268 / 88,7885). Opsi walk-forward DITOLAK coder — tanpa eskalasi,
  sesuai batas (opsi b aman). ✓
- L3-02: `starts_b`/`idx_b` (:398-399) me-resample sisi B; print disclose
  "KEDUA sisi A dan B di-resample blok — KOREKSI L3-02" (:384). ✓
- L3-03: kolom `ci95_beda_iid` (:368, :377, :945). ✓
- L3-05: `M5_COLS` memuat `broker_time_raw` (:555) + `wall_clock_series`
  (:570). ✓
- L3-04: justifikasi "20 hari ≈ 1 bulan dagang, menutup musiman mingguan"
  (:384, :59) — cukup/tidaknya diputus auditor.

## 3. Output notebook (25 sel / 18 kode / 0 error)
- `CI95-block(kedua sisi)=[-7.62542, 13.71568]` dan `[-0.00383, 0.00283]` ✓
  cocok klaim; CI baru LEBIH LEBAR dari iid (masuk akal — kebalikan cacat lama).
- Kedua CI tetap memuat 0 → kesimpulan marginal tak berubah. ✓
