# Gerbang Hasil L3-1 (verifikasi asisten dari artefak, 2026-10-13)

## Hash + HEAD (diukur ulang sesi ini)

- Builder BD5B12415937 (58262 B, ASCII), NB 67F5FE628712
  (8 sel / 7 kode tereksekusi 1-7 / 0 error / kesimpulan ada),
  CSV 45D034823AFC, FIG-18 50DAA2612C06, manifest 599C7FFDFC8B
  (BERKOLOM path - T-1 tutup), log 0A4E5D4FBDDF: SEMUA COCOK.
- HEAD b18992b tak bergerak, staged nol.

## Isi (dihitung ulang independen dari CSV)

- 103 baris (67 brier + 36 mse); vonis 68/35; diskret 56/11,
  kontinu 12/24. M1 true 103/103.
- Aturan M3 direkonstruksi = vonis 103/103 (nol selisih).
  Margin diskret tak dilanggar (min 0,00306 > 0,001; median
  0,00549 - ada headroom, bukan menempel ambang). Kontinu min
  perbaikan relatif 11,2% (ambang 1%).
- Twin C-3: 5/5 round_d identik kembaran native (angka+vonis).
  Flag punya_round_d_invers = 12 (7 native + 5 round_d).
- run_l31.log: EXIT=0 terbaca, TETAPI masih UTF-16LE + CRLF +
  wrapper NativeCommandError PowerShell (perintah redirect
  langsung adendum TAK dijalankan; T-6 berulang sebagai temuan
  format - isi utuh, keterbacaan tercemar).

## Putusan gerbang

L3-1 LOLOS gerbang asisten dengan satu catatan format (log).
Tanpa model selain baseline/marginal terdaftar, tanpa P&L.
Berikutnya: reaudit independen L3-1, lalu vonis dagang B-4.
