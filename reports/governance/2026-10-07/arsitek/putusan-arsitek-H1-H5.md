# Putusan Arsitek H1–H5 — 2026-10-07

**Mandat:** user — putuskan nasib H1–H5 sebelum lock final.
**Bahan:** `hipotesis_lock_v1.md` · `laporan_tahap_12_sintesis.md:12–111` ·
`report.md` (2026-10-06) · putusan H1 reversal-day 2026-10-07 (opsi iii).
**Batas:** menilai redaksi & desain uji; angka EDA terkunci blob `661c0aeb2357`.

## Putusan

- **H1 — KUATKAN.** Redaksi + ambang + catatan risiko + klausul anti-penyelamatan
  + izin eksplorasi disahkan tanpa perubahan.
- **H2 — TERIMA.** S2: (a) median = median EV-per-trade-after-cost dalam-tahun
  (2023/2024/2025; gugur bila ≤0 pada ≥2 tahun); (b) aturan strategi diagnostik
  wajib pra-registrasi di Lapisan 3 sebelum uji.
- **H3 — TERIMA, vonis TERBUKA.** S3: AUC = kalibrasi in-sample span terkunci,
  bukan klaim OOS. S4: uji drawdown vs strategi diagnostik L3 pertama; filter
  DILARANG aktif sebelum S4 dievaluasi.
- **H4 — TERIMA.** S5: EV memakai 6 jam tetap [14,13,0,15,12,7] + `cost_basis`
  fragmen 4b; uji pola OOS memakai 6 jam teratas hitung-ulang; dicatat terpisah.
- **H5 — TERIMA.** S6: wajib lapor jumlah sel; klaim sel mana pun wajib koreksi
  multiplicity bernama (atau replikasi independen); tanpa itu = eksplorasi.
- **H6+ — DITOLAK.** S7: (i) batas 3–5 rancangan; (ii) sisa pola sudah
  terdisposisi; (iii) tak ada usulan berambang konkret.

## Alasan ringkas

H1: redaksi unconditional + uji real-time + dua ambang konkret; putusan (iii)
termaktub verbatim; tak ada alasan baru untuk revisi/cabut. H2: satu-satunya
hipotesis eksploratori yang jujur; ambang pasca-B4-06 dapat dieksekusi. H3:
basis intensitas kokoh; kelemahan (AUC in-sample saja; drawdown tergantung
strategi-masa-depan) diikat S3–S4 agar tak lulus prematur. H4: ambang M2
mewarisi kanon desain; deviasi S5 dicatat jujur. H5: penyempitan yang benar
atas temuan negatif; multiplicity diikat S6.
