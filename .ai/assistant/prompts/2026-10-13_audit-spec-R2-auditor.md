# Brief Audit Spec Discovery-R2 — Auditor Eksternal (2026-10-13)

## Otoritas + scope
Spec: `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R2.md`
(status SPEC EKSEKUSI, R2-1..R2-6 diratifikasi paket). Fondasi:
spec R1 + Amandemen-1 + Amandemen-2 (sudah audit penuh GAGAL →
amandemen → re-audit fokus LULUS). Maka audit ini BUKAN audit penuh:
bagian warisan R1 (event, biaya, kontrak eksekusi, kriteria,
paper, bukti) TIDAK diaudit ulang. Yang diaudit HANYA delta R2
(butir B1–B8). Temuan di luar delta = CATATAN, tidak mengubah verdict
kecuali cacat FATAL baru (definisikan eksplisit).

## Butir audit
- **B1 — Resep ATR sahih?** (D2-2 vs `scripts/_build_eda06.py:74-75,
  497-508`.) kausal (bar M5 terakhir selesai ≤ t0)? beku saat entri?
  aturan buang (ATR tak tersedia/gap/anomali/Off) lengkap + nol
  imputasi? SL=1,5xATR / TP=2xSL tunggal tanpa ladder? Coder dapat
  menulis tanpa mengarang?
- **B2 — Disiplin satu paket?** Tidak ada ladder, tidak ada aturan
  pemilihan, Q2-tanpa-ladder konsisten dengan "aturan pemilihan =
  TIDAK ADA"? Tidak ada celah seleksi pasca-hasil?
- **B3 — Bed segar ganda?** Klaim: EDA-06 memakai 2023–2025
  (`_build_eda06.py:69,147`; 2026 holdout tak dimuat), R1 memakai
  2024. Verifikasi klaim tahun dari kode. Eksklusi anomali
  2026-03-10..03-27 tanpa re-entry? "Satu bed satu ronde" eksplisit?
  Larangan 2024/2025/2023 untuk evaluasi ada?
- **B4 — Aturan paruh operasional?** Belahan kalender dari rentang
  usable + batas exact di ledger pra-run — cukup untuk coder tanpa
  mengarang?
- **B5 — E3 tipis ditangani jujur?** Estimasi ~500–600 berdasar
  densitas 2024 dinyatakan sebagai estimasi? Gagal-gate = GUGUR
  dilaporkan tanpa kompensasi ambang?
- **B6 — Segel terpisah?** Lampiran dihitung-ulang di 2026 + segel
  baru; segel R1 (`5bc324aa…67df963`) dilarang dibuka/dibaca R2?
- **B7 — Caveat confirmation jujur?** Bed confirmation BELUM
  diputuskan + caveat kontaminasi 2025 dinyatakan terbuka (bukan
  disembunyikan, bukan diputuskan diam-diam)?
- **B8 — Justifikasi D2-9 akurat?** Klaim ranking (ATR_k1.5_rr2
  2,49 5/12; FIX_100_140 2,74 6/12; FIX_30_45 8,03 0/12;
  E_normal>0 = 0/144; LOLOS = izin lanjut bukan edge; unconditional
  stride-5) cocok dengan
  `reports/eda/2026-10-10/T-06-7_gerbang_tercile.csv`? Tidak ada
  klaim profitabilitas yang tak didukung tabel?

## Format jawaban (sama seperti audit R1)
- Per butir: LULUS / GAGAL + bukti (file:baris).
- Verdict: LULUS / CATATAN (lulus bersyarat — sebut syarat) / GAGAL
  (sebut butir + alasan + perbaikan minimal).
- Larangan: tidak merancang ulang, tidak mengusulkan k/RR alternatif,
  tidak menyentuh data (2026 holdout tetap tertutup untuk auditor).
