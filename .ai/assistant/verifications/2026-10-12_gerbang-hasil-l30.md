# Gerbang Hasil L3-0 (verifikasi asisten dari artefak, 2026-10-12)

## Hash + HEAD (diukur ulang sesi ini)

- Builder E5468952EA0C, NB 723DA6C14855, arah F48323D2C671,
  peta98 1F58D4DFE460, FIG-17 CE7E4F5CA944, manifest 9EB860A4A7AB:
  SEMUA COCOK klaim coder.
- HEAD b18992b tak bergerak, staged nol.
- Builder 23826 byte, ASCII/LF/tail-LF.

## Isi (dihitung ulang independen dari CSV)

- T-L3-0_arah.csv = 153 baris, split 120/33, pasangan unik,
  himpunan (target,fitur) SAMA PERSIS dengan 153 baris G3=True
  T-07-3 (diff kosong kedua arah).
- 5 Tokyo round_d hadir semua-negatif eksak (-0,0473/-0,0549/
  -0,7446/-0,0279/-1,5868). 0 baris round_d London (kandidat
  GUGUR G3); kedua target London hadir via wakil asli rv15/rv60
  positif. Koreksi presisi coder DITERIMA (brief L3-0 saya yang
  kurang presisi di level target; mesin sel 04 menangkap).
- T-L3-0_peta98.csv = 98 target unik; 98/98 wakil cocok di T-07-3;
  98/98 tanda = tanda lift wakil; split 78/20.
- NB 8 sel / 7 kode tereksekusi 1-7 / 0 error / kesimpulan ada.
- run_l30.log EXITCODE=0; manifest 6/6 cocok; penjaga beku
  260/6767/1315/1335/86 tak berubah.

## Putusan gerbang

L3-0 LOLOS gerbang asisten. Tanpa model/skor/null/2026 di artefak.
Berikutnya: reaudit independen L3-0, lalu putusan buka L3-1.
