# Gerbang Hasil Coder EDA-06 (verifikasi asisten dari artefak, 2026-10-10)

HEAD: b18992b5e57d45c125aacf3ca868c2f9e135d9d1 (tak berubah).
Status: nol stage/commit oleh ronde ini; builder + notebook + laporan +
14 CSV + 5 FIG berstatus untracked (sah, menunggu keputusan commit user).

## Hash (git hash-object, diukur ulang dari disk sesi ini)

- scripts/_build_eda06.py: fab369e674321867666356d031132a7f20ef854e (klaim
  fab369e6 COCOK prefix).
- notebooks/scalping/eda_06_biaya_breakeven.ipynb:
  dd0f229d6a18dbbdbe69d2f6022bba445cff64a7 (klaim dd0f229d COCOK prefix).
- Referensi tak tersentuh: 6a6c6516bc96e7e9a7845a13b1909927cc718e75 dan
  6724c37ec5493b821d0179d0d00768fbd343a485 (COCOK persis dengan brief).

## Eksekusi notebook (diukur ulang dari file, bukan dari laporan)

- 27 sel (16 kode), execution_count 1-16 berurutan, 0 output error.
- Klaim 27/27 VERBATIM diterima sebagai klaim coder (TERVERIFIKASI sebagian:
  sel cocok dengan referensi per laporan; audit penuh = wewenang auditor).

## Gerbang K1-K4 (dihitung ulang dari CSV di disk sesi ini)

- T-06-7_gerbang_tercile.csv: 144 baris, LOLOS 23.
- T-06-7_gerbang_sesi.csv: 48 baris, LOLOS 7.
- Klaim funnel K1: 32 -> K1&K2: 23 -> +K3: 23 -> +K4: 23 diterima sebagai
  klaim coder; konsistensi LOLOS 23+7 dengan CSV TERVERIFIKASI.
- Artefak: 14 CSV + FIG-08..12 (5 file) di reports/eda/2026-10-10/ (COCOK).
- B = 185.248 dan 5 semester A diterima sebagai klaim coder (cek penuh =
  wewenang auditor via parquet).

## Mutu (klaim coder, belum dihitung ulang sesi ini)

- pytest 254 passed; builder ruff/format/foreign_chars PASS; ruff notebook =
  14 temuan pra-ada referensi (GAGAL-dengan-sebab, dikunci VERBATIM).

## Putusan gerbang

LOLOS (bersyarat audit): angka gerbang konsisten antara CSV, notebook, dan
laporan; tidak ada divergensi material yang terlihat. Syarat: re-audit
independen (replikasi + anti-intip + holdout + strata + hitung-ulang K1-K4)
sebelum arsitek menulis spec EDA-07 dari 23+7 irisan lolos. LOLOS bukan
bukti edge.

Berikutnya: brief re-audit auditor EDA-06 (sudah disiapkan, menunggu
perintah paste user).
