# Verifikasi perbaikan coder atas temuan Langkah 1 — 2026-10-06

## 1. Hash (git hash-object, disk)
- `_build_eda05.py` → `8ac848ce…` ✓ MATCH klaim
- nb05 notebook → `93ea7695…` ✓
- report.md → `72e83777…` ✓
- tahap_11 → `6ab21459…` ✓, tahap_12 → `eae21308…` ✓
- tahap_13/14 tidak berubah ✓ (`ad6652b7…` / `85b958d1…`)
- FIG-01..07 byte-identik ✓ (7/7 prefix cocok)

## 2. Isi kode (spot-check)
- :486 referensi `1,0312` + :487 catatan 1,0337 = lag 2-60 ✓ (HIGH-01)
- :450 `variance_ratio`, :479 `no_gap = ~m15_a["gap_return"]` ✓ (HIGH-02)
- Kunci ketat: :489 ACF, :493 VR→1.0312, :508 sign-ACF, :601 swing,
  :507 `n_no_gap == 75_038` ✓ + band lebar kedua bernama eksplisit
  (:492, :511, :604) ✓ (MEDIUM-02)
- Output notebook: VR rata-rata `1.0312 (referensi nb03: 1,0312)` ✓,
  sign-ACF `-0.022624` identik ✓, `n_no_gap 75,038` ✓
- Notebook: 25 sel / 18 kode / 0 error; tight asserts ikut tereksekusi
  tanpa error → nilai dalam toleransi kunci ketat. ✓

## 3. Catatan kecil (bukan temuan, untuk auditor)
- Hitungan assertion: regex saya `^assert ` → 56; coder klaim 59.
  Selisih metode hitung, bukan indikasi masalah. Auditor boleh hitung ulang
  dengan metode eksplisit saat re-audit.
- Pola struktur: sebagian assert berada dalam blok string template yang
  dieksekusi (catatan sejak verifikasi sebelumnya) — auditor menilai
  apakah pola ini sah saat re-audit.
