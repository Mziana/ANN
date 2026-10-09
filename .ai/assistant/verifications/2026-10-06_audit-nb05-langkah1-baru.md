# Verifikasi Langkah 1 auditor baru — 2026-10-06

## 1. File + hash
`reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md` — 17.439 byte,
315 baris, SHA256 `1d89eb90…3d721e` = MATCH dengan klaim chat. Pelajaran hash
dari Klenz SUDAH diterapkan (hitung setelah tulis final). ✓

## 2. Spot-check substansi ke `scripts/_build_eda05.py`
- :444 mencetak "(referensi nb03: 1,0337)" ✓ (HIGH-01 terkonfirmasi ada)
- :439-440 `var(ddof=0)` ✓ (HIGH-02 terkonfirmasi ada)
- Assert replika: :445 `abs(acf1)<0.05`, :446 `0.9<mean_vr<1.2`,
  :453 band sign-ACF, :543 `45<SWING<52` ✓ (MEDIUM-02 terkonfirmasi)
- Assert `abs(mean_vr - 1.0337) < 0.05` TIDAK ADA di file ✓ (draf lama
  memang mengarang — klaim pencabutan benar)
- :507-534 `fractal_mask` ✓, :436 vs :451 dua metrik terpisah ✓

## 3. Catatan
- Baris 445/446/453/543 terbaca di dalam blok string triple-quote (kemungkinan
  kode replika yang dieksekusi via mekanisme template) — pola struktur untuk
  Langkah 2+, bukan keberatan atas temuan Langkah 1.
- Verdict auditor: PERLU PERBAIKAN (2 HIGH, 2 MEDIUM, 3 LOW), 6 pertanyaan
  untuk coder. Bukan LULUS — commit nb05 TERTAHAN hingga perbaikan.
