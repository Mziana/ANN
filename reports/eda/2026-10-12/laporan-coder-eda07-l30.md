# Laporan Tugas — Coder L3-0: Peta Arah G3-Pass + 98 LOLOS (Deskriptif, Bukan Model)

## File yang dibuat/diubah

- `scripts/_build_eda07_l30.py` (baru, 530 baris, 23826 byte, SHA256 `E5468952EA0CFF3B5E2C265BCA94656951DDB6CAB06E036936DABC0B580DBF7E`)
- `notebooks/scalping/eda_07_l30_arah.ipynb` (baru, 8 sel = 1 markdown + 7 kode, 7 tereksekusi, 0 error, 36666 byte, SHA256 `723DA6C14855943DA54CB74AB00E7E9584953B7FE96A1ABDA2903BE6B1F1FA2A`)
- `reports/eda/2026-10-12/T-L3-0_arah.csv` (baru, 153 baris data, 23851 byte, SHA256 `F48323D2C671C0FA963B2B2C940ADF3A1DB12B83C3080B5821793EE508344D1F`)
- `reports/eda/2026-10-12/T-L3-0_peta98.csv` (baru, 98 baris data, 14340 byte, SHA256 `1F58D4DFE460CBCC7D436FCFD40401B0A6EE3F41AC13503C36BDD736D1BC95C5`)
- `reports/eda/2026-10-12/FIG-17_peta_arah.png` (baru, 43845 byte, SHA256 `CE7E4F5CA94414733CEB00F6D3923401EF20884A48196FB83F99D02FCB1F0EC5`)
- `reports/eda/2026-10-12/_l30_manifest.csv` (baru, bukti hash SEBELUM vs aktual 6/6, 976 byte, SHA256 `9EB860A4A7AB9B9C9AED6B0AE54E6F7AA372BCCBCA9AB36AAB8408D3E622D084`)
- `reports/eda/2026-10-12/run_l30.log` (baru, runner-log S3-4: pra-kompilasi + nbconvert + registry + `EXITCODE=0`, UTF-8/LF)
- File beku EDA-07/I-2 (T-07-1..4, T-06-7 x2, _gate_G2_alarm): TAK tersentuh (hanya dibaca; penjaga baris registry: 260/6767/1315/1335/86 sama)

## Apa yang dilakukan

Eksekusi L3-0 deskriptif S3-1 (mandat `2026-10-12_eksekusi-l30-coder.md` + `spesifikasi-lapisan3.md` S3-0..S3-5 + `putusan-eda07-audit.md` A-1..A-7 + `putusan-eda07-i2.md` C3-invers mengikat): bangun `scripts/_build_eda07_l30.py` reuse-first harness I-2 (lock tunggal, pre-kompilasi sel, nbconvert inplace, verify_registry, normalisasi CRLF->LF), tulis + eksekusi `eda_07_l30_arah.ipynb` langsung (tugas <30 mnt; `venv` Python 3.12.8, `nbconvert exit=0`, lock dilepas). Notebook MURNI baca CSV beku + pemetaan (tanpa RNG, tanpa model/latih/skor/null/backtest/PnL): K24 literal verbatim run 9 (transcription-guard, 24/24), manifest hash 6 input SEBELUM ditulis-dulu-lalu-diassert, scope T-06-7 + `assoc_irisan`/`scope_of` verbatim run 9, arah 153 G3-pass (tanda lift + irisan), bukti C3 (5 Tokyo negatif eksak + 2 baris kandidat round_d London G3=False), verdict native verbatim `ok = g1 and g2any and g3(wakil) and (g4 == NA or g4)` -> 98 LOLOS -> peta98 (diff himpunan kosong), FIG-17 pos/neg per sesi x horizon, kesimpulan 1 paragraf terkunci. `ASSERT_LOG total: 343`.

Hasil: **T-L3-0_arah.csv 153 baris (pos 120 / neg 33)** + **T-L3-0_peta98.csv 98 baris (arah pos 78 / neg 20)** + FIG-17. Lima Tokyo hadir SEMUA bertanda negatif (INVERS, dilarang jadi sinyal). Dua baris kandidat round_d London G3=False (CI memuat 0; gugur sbg kandidat) — sementara kedua targetnya tetap LOLOS via wakil asli (rv15/rv60 pos). Satu-satunya keluaran: TABEL ARAH go/no-go administratif ke L3-1; tanpa vonis model, tanpa klaim edge.

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Notebook 8 sel, 7 kode tereksekusi, 0 error | TERVERIFIKASI | `nbconvert exit=0`; parse ipynb: `sels: 8`, `exec_count: [1..7]`, `errors: []`; `lock dilepas; build selesai.` + `EXITCODE=0` di `run_l30.log` |
| Deterministik tanpa RNG; K24 24/24 nol drift | TERVERIFIKASI | Output sel 01: `PASS: 24/24 konstanta run 9 identik (nol drift).` + `L3-0 deterministik tanpa RNG (murni baca CSV beku + pemetaan).`; K24 literal didokumentasikan sbg transcription-guard + provenance (I-2 24/24 + verifikasi independen auditor), bukan hitungan |
| Hash 6/6 input beku sama SEBELUM | TERVERIFIKASI | Output sel 02: `PASS: hash 6/6 input beku sama SEBELUM (bukti di _l30_manifest.csv)`; `_l30_manifest.csv` 6 baris `cocok=True` (T-07-3 `27784A92…`, T-07-2 `67BE1A52…`, T-07-1 `7DFF3D15…`, T-06-7-ter `E03EA9AB…`, T-06-7-ses `2DD86BC7…`, alarm `DE39BEF0…`) |
| Scope 23 TER + 7 SES + assoc verbatim | TERVERIFIKASI | Output sel 02: `T-06-7 tercile 144 baris`, `sesi 48 baris`, `irisan tercile lolos = 23`, `irisan sesi lolos = 7`, `scope + assoc_irisan verbatim run 9 siap (23+7).` |
| T-L3-0_arah.csv tepat 153 (pos 120 / neg 33), re-read | TERVERIFIKASI | Output sel 03: `split arah: pos=120 neg=33` + `PASS: T-L3-0_arah.csv 153 baris, split 120/33 (re-read dari disk).`; pasangan (target,fitur) unik di set (kunci arah tunggal, diassert) |
| 5 Tokyo negatif eksak; 2 kandidat London G3=False | TERVERIFIKASI | Output sel 04: `PASS: C3 - 5 Tokyo negatif eksak, 2 kandidat London GUGUR G3 (S3-0/W-2/C3-invers).`; Tokyo: -0.0473/-0.0549/-0.7446/-0.0279/-1.5868 (4 desimal persis, tanda neg); London round_d: G3 False 2/2, CI memuat 0 (-1.1397..0.0168; -0.9397..0.0575); konteks tercetak: target London punya baris G3-pass fitur asli (rv15/rv60) — yg gugur = baris round_d |
| Verdict verbatim 98 LOLOS / 162 GUGUR; FIG_KEY + TOP3 anggota | TERVERIFIKASI | Output sel 05: `PASS: verdict verbatim 98 LOLOS / 162 GUGUR.`; `LB_bin Tokyo tALL N5` + TOP3 London (`LB_bin t1`, `LB_rng t1`, `LC1 t1`) anggota LOLOS; 260 target dievaluasi; 1 wakil native/target; G4 LA tunggal, waktu all-NA |
| T-L3-0_peta98.csv tepat 98; diff himpunan kosong | TERVERIFIKASI | Output sel 05: `diff peta-vs-LOLOS: lebih=[] kurang=[]` + re-read 98 baris; arah tunggal-makna {pos,neg}: pos 78 / neg 20 (cek CSV langsung) |
| FIG-17 mencakup penuh 153 (120/33) | TERVERIFIKASI | Output sel 06: pivot sesi x horizon tercetak + `FIG tersimpan: ['FIG-17_peta_arah.png']` (43845 byte); chk 120/33 lolos |
| Kesimpulan 1 paragraf terkunci; ASSERT_LOG 343 | TERVERIFIKASI | Output sel 07: `KESIMPULAN_L30 TERKUNCI:` 1 paragraf (>200 karakter, chk lolos); `ASSERT_LOG total: 343` (>= 20); tanpa vonis model/edge, tanpa buka L3-1 |
| Builder ASCII/LF, ruff PASS, pre-kompilasi 7 sel | TERVERIFIKASI | Shell pra-run tiap eksekusi: `nonASCII: 0 hasCR: False`; `ruff: All checks passed!`; `pra-kompilasi 7 sel kode: OK`; notebook 8 sel diassert builder |
| File beku tak berubah | TERVERIFIKASI | Registry builder: penjaga baris 260/6767/1315/1335/86 sama pasca-run; CSV L3-0 LF murni (pola I-1/I-2) |
| Kedua target London LOLOS via wakil asli (rv15/rv60 pos) | TERVERIFIKASI | Cek CSV langsung: peta98 baris `LB_rng London t3 N5` (wakil rv15, pos) + `LB_rng London tALL N5` (wakil rv60, pos); konsisten verdict verbatim (g3 pakai wakil, bukan kandidat) |

## Yang belum diverifikasi

- Audit independen L3-0 oleh Auditor (wajib; coder DILARANG audit sendiri) — mencakup: rekonstruksi verdict dari CSV, ketepatan 5 nilai Tokyo, status G3=False 2 London, kelengkapan 153/98/FIG-17/manifest/runner-log, kepatuhan batas S3 (tanpa model/skor/null/2026).
- Putusan arsitek pasca-audit L3-0 untuk membuka L3-1 (wewenang arsitek; L3-0 berakhir di TABEL ARAH).
- Rerun determinisme penuh (satu eksekusi sukses exit=0; L3-0 tanpa RNG sehingga rerun deterministik by-construction, belum diuji ulang di sini).

## Potensi masalah

1. **Presisi C3 diperketat saat build (jujur, sudah diperbaiki).** Asumsi awal "2 London absen dari set G3-pass" SALAH di level target: yang absen/G3=False = 2 BARIS kandidat round_d; kedua target London justru LOLOS via wakil asli rv15/rv60 (pos). Ketidaktepatan tertangkap assertion mesin sel 04 sebelum hasil apa pun ditulis, lalu sel + kesimpulan diperbaiki dan re-run exit=0. Versi terkunci sudah presisi; ringkasan sesi lama yang menyebut "2 GUGUR London" tanpa kualifikasi harus dibaca sebagai "gugur sbg kandidat round_d".
2. **Dua bug kode tertangkap assertion mesin pra-hasil (sudah diperbaiki).** (a) `print(..., loud=True)` 2x (TypeError; `loud` hanya milik `chk`) — tertangkap review pra-run ke-2; (b) filter `r["wakil"]` (kolom bool) vs `r["fitur"]` (string) di loop verdict -> IndexError iloc pada pasangan yg tak cocok — tertangkap run; merge 260/260 yg benar jadi petunjuk. Keduanya tak menghasilkan artefak salah (gagal sebelum tulis).
3. **K24 L3-0 = transcription-guard, bukan bukti nol-drift komputasi.** L3-0 tak memakai konstanta dalam hitungan (murni baca CSV); nilai K24 literal verbatim run 9 yg diassert menjaga salah-salin + rantai provenance (I-2 24/24 + verifikasi independen auditor). Tidak dilebihkan di laporan sebagai verifikasi komputasi.
4. **Runner-log awal UTF-16LE campur ASCII (sudah dinormalisasi).** `Tee-Object` menulis UTF-16LE + baris EXITCODE ASCII -> dikonversi ke UTF-8/LF utuh (`EXITCODE=0` terverifikasi byte-level); isi tak berubah.
5. Tiga eksekusi build total (2 gagal pra-hasil + 1 sukses); kegagalan tak menulis artefak parsial (lock dilepas tiap run; CSV hanya ditulis sel 03+ yg lolos; cek `Test-Path` pasca-gagal: manifest/arah/peta98 absen). File final berasal dari run sukses terakhir.

## Saran berikutnya

1. Auditor: verifikasi L3-0 — (a) 153 = filter G3-pass T-07-3 + split 120/33 dari tanda lift; (b) 5 nilai Tokyo 4-desimal + tanda neg; (c) 2 baris round_d London G3=False + CI memuat 0; (d) rekonstruksi verdict verbatim -> 98 (bandingkan daftar target vs I-2); (e) diff peta-vs-LOLOS kosong + arah = tanda wakil; (f) FIG-17 mencakup 153; (g) manifest 6/6 + runner-log EXITCODE=0; (h) kepatuhan S3 (tanpa model/skor/null/2026; 5 Tokyo tak dipakai sbg sinyal).
2. Arsitek: putusan buka/tutup L3-1 pasca-audit L3-0 (go = terdaftar di peta; no-go model = gagal M2/M3 nanti).
