# Laporan Tugas — Coder L3-1 Baseline vs Null (B-3 + Amandemen C)

## File yang dibuat/diubah

- `scripts/_build_eda07_l31.py` (diubah, 3 perbaikan pra/antar-run; sha256 `BD5B1241…47F3`, ASCII, 0 CR)
- `notebooks/scalping/eda_07_l31_baseline.ipynb` (baru, 8 sel, 0 error; sha256 `67F5FE62…6EA1`)
- `reports/eda/2026-10-12/T-L3-1_baseline.csv` (baru, 103 baris; sha256 `45D03482…EE1C`)
- `reports/eda/2026-10-12/FIG-18_baseline.png` (baru, 77.791 B; sha256 `50DAA261…82C9`)
- `reports/eda/2026-10-12/_l31_manifest.csv` (baru; sha256 `599C7FFD…95A6`)
- `reports/eda/2026-10-12/run_l31.log` (baru, runner-log via redirect; EXIT=0; sha256 `0A4E5D4F…A91F`)

## Apa yang dilakukan

Eksekusi adendum L3-1 (brief induk + Amandemen C mengikat bersama): 67 baris
diskret = M3 B-3 utuh (Brier margin 0,001 + menang 2025H1&H2 + akurasi,
prediksi argmax C-3); 36 baris LB_rng = M3-kontinu C-2 (MSE 1% relatif +
menang per-semester + MAE; Brier/akurasi tidak dihitung). Label per-bar
VERBATIM run 9 (jangkar T-07-1 200/200). Split train 2023H2-2024H2 / test
2025H1+H2, max-train < min-test di-assert. Hasil: **LOLOS 68 / GUGUR 35**
(diskret 56/11, kontinu 12/24). Tanpa vonis dagang, tanpa klaim edge. STOP
setelah serah-terima.

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Notebook 8 sel, 0 error, EXIT=0 | TERVERIFIKASI | `run_l31.log`: `nbconvert exit=0`, `registry L3-1: … (103) …`; parse nbformat independen: 8 sel, 0 output error |
| T-L3-1 103 baris (67 brier + 36 mse) | TERVERIFIKASI | `Import-Csv … .Count` = 103; sel4 `M3 selesai: 103 baris`; `metrik_jenis` = {brier, mse} |
| Label verbatim run 9 | TERVERIFIKASI | sel4 `PASS: jangkar T-07-1 200/200 (n eksak, kelas eksak, fraksi 1e-4)`; K24 `24/24 identik`; strata B=185.248, N_ENT=184.731 di-assert |
| Split tanpa bocor | TERVERIFIKASI | sel4 `split: train […] (UTC 1688…000..1735…000) \| test […] (1735…666..1767…084)` + chk max-train < min-test LOLOS |
| M3 per pasangan + vonis | TERVERIFIKASI | CSV: LOLOS 68/GUGUR 35; diskret 56/11, kontinu 12/24; `M1` True 103/103; kolom `lolos_a/menang_h1/menang_h2/lolos_c/vonis` per baris |
| Register 103 tepat | TERVERIFIKASI | sel4 `PASS: register 103 = 98 native + 5 Tokyo (diskret=67, kontinu=36)`; 5 Tokyo lift negatif eksak di-assert |
| C-3 twin 5 round_d = native | TERVERIFIKASI | sel4 `PASS: C-3 konsistensi 5 round_d = kembaran native (angka + vonis identik)`; unit argmax/tie 3/3 |
| Hash 5/5 input sama SEBELUM | TERVERIFIKASI | `_l31_manifest.csv`: 5/5 `cocok=True`; manifest BERKOLOM path (T-1) |
| S8B beku utuh + registry | TERVERIFIKASI | sel6 `PASS: S8B mtime+size 11/11 identik`; registry 260/6767/1315/1335/86 + arah 153 + peta98 98 |
| ASSERT_LOG 1268, kesimpulan terkunci | TERVERIFIKASI | sel7 `ASSERT_LOG total: 1268` (>=100), `KESIMPULAN_L31 TERKUNCI` (>200 karakter) |
| Builder ASCII/LF | TERVERIFIKASI | 0 CR, 0 non-ASCII |
| Nol stage ronde ini, HEAD utuh | TERVERIFIKASI | `git diff --cached --name-only` kosong; HEAD `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` |
| Hash output di manifest vs on-disk | ASUMSI TERDOKUMENTASI | sha output tercatat pra-normalisasi EOL (`2D46…`/`50DA…` sama untuk FIG karena PNG tak dinormalisasi); CSV on-disk pasca CRLF→LF (`45D0…`); jumlah baris 103 dibaca-ulang independen pasca-normalisasi — isi sama, hanya EOL (pola I-1/I-2/L3-0) |

## Perbaikan builder (3, terdokumentasi, bukan improvisasi spec)

1. FIG-18 memakai `_df.columns[17]/[16]` = (metrik_mod, kolom string nullmodel) → sumbu salah + `min/max` campur str/float pasti gagal. Diganti nama eksplisit `metrik_null_pooled` (x) / `metrik_mod_pooled` (y). Murni bug plot; angka M3 tak tersentuh.
2. `lol_c` kelebihan satu `)` → SyntaxError pra-kompilasi. Dihapus.
3. C-3 twin `RE[…wakil != round_d].iloc[0]` kosong → IndexError (bukti: `run_l31.log` baris 336-337/372-374 run gagal). Akar: kedua kemunculan target Tokyo sama-sama terlabel `round_d`. Perbaikan: wakil/arah berbasis posisi register (98..102 = Tokyo; chk tertib), C-3 bandingkan duplikat baris native (iloc[0]) vs Tokyo (iloc[1]) — intent arsitek tak berubah.

## Yang belum diverifikasi

- Isi sel per sel notebook oleh AUDITOR independen (wajib sebelum putusan).
- Putusan dagang atas TABEL M3 = wewenang arsitek + user pasca-audit (S8A).

## Potensi masalah

- Tidak ada. Seluruh chk mesin LOLOS; satu-satunya anomali (hash output manifest pra-normalisasi EOL) sudah dijelaskan di atas.

## Saran berikutnya

- AUDITOR independen L3-1, lalu arsitek putusan (LOLOS/GUGUR per pasangan → vonis dagang).
