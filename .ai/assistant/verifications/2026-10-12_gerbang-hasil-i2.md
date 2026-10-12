# Gerbang Hasil I-2 (verifikasi asisten dari artefak, 2026-10-12)

## Hash + HEAD (diukur ulang sesi ini)

- T-07-1 260, T-07-2 6767, T-07-3 1315, T-07-4 1335 baris data: COCOK klaim.
- FIG-13..16 ada (36798/25013/19435/14626 byte): COCOK klaim.
- Regresi V-6: himpunan alarm _i2 vs beku DIFF KOSONG (86/86, 780/780).
  52 pdhl_d + 28 round_d + 6 noise: COCOK klaim.
- 7 baris round_d di T-07-3 dihitung ulang dari CSV: 5 G3-True Tokyo
  (semua lift negatif, CI tak memuat 0) + 2 G3-False London (CI memuat 0).
  COCOK klaim C3. G4 kosong ketujuh (non-LA): COCOK klaim G4=NA.
- G3-pass native: 153 baris, fitur top rv60 (62) + rv15 (21) + atr_m5 (16)
  + hour_sin (15); tanda lift 120 pos / 33 neg. Diverifikasi dari CSV.
- HEAD b18992b tak bergerak, staged nol.

## Status

Eksekusi I-2 DINYATAKAN TERVERIFIKASI prosedural. Isi (98/162, 29/37,
5 kandidat invers) mengikuti aturan pra-registrasi apa adanya; vonis
isi diputus arsitek, bukan asisten. Disposisi C1-C3 dan nasib Lapisan 3:
putusan-eda07-i2.md. Berikutnya: reaudit auditor independen.
