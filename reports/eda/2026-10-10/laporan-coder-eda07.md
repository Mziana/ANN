# Laporan Tugas Coder EDA-07 — Bangun + Eksekusi Label-Fitur (STOP pra-registrasi)

Tanggal: 2026-10-10. Peran: Coder (bukan arsitek, bukan auditor). Brief:
`.ai/assistant/prompts/2026-10-10_eksekusi-eda07-coder.md`. STOP setelah
serah-terima. Bahasa: Indonesia.

## Ringkasan eksekutif

- Builder + notebook 19 sel selesai ditulis; gate mutu builder hijau.
- Eksekusi penuh berjalan: sel 01–15 tereksekusi (60 target LA + 200 target
  label-waktu terskrining, anti-leakage dan rerun di sel 13/15 lewat indikator
  tak-langsung — lihat keterbatasan).
- **STOP pra-registrasi di gerbang kontrol sel 15**: fitur kontrol lolos
  kriteria G2 identik-fitur → `ASSERT GAGAL: nol kontrol lolos-G2`. Coder
  TIDAK mem-bypass (KONTRAK_07: "ALARM STOP").
- Akar sebab TERBUKTI dengan kode asli di data null murni (bukan spekulasi):
  perbandingan "MI semester vs lantai pooled" bias-naik sistematis
  (Miller-Madow), null lolos 5/5 pada semua n. Lihat § Bukti bias.
- Sel 16–18 (verdict/T-07/FIG/kesimpulan) BELUM pernah tereksekusi. Tidak ada
  artefak T-07/FIG-13..16. Keputusan arsitek diperlukan sebelum run ulang.

## File yang dibuat/diubah

- `scripts/_build_eda07.py` (baru, 1445 baris, 66536 byte) — generator +
  executor nbconvert pola `_build_eda06.py` (lock eksekusi-tunggal,
  `verify_registry` FIG-01..16 + 4 CSV T-07); 19 sel (1 markdown + 18 code).
- `notebooks/scalping/eda_07_label_fitur.ipynb` (baru, 75511 byte) — versi
  generate BELUM tereksekusi (0 output tersimpan; `--inplace` tidak menulis
  saat gagal). Hash di bawah = versi terakhir (pasca semua fix).
- Laporan ini: `reports/eda/2026-10-10/laporan-coder-eda07.md`.
- Referensi/spec/putusan TIDAK diubah.

## Apa yang dilakukan

1. S-0: baca brief, spec EDA-07, putusan EDA-06, rancangan EDA_06_07,
   design eksekusi, builder EDA-05/06, `_eda_common.py`.
2. Tulis builder 19 sel (kontrak, setup, parameter, muat, scope, ATR, entri,
   LA normal+stres, label waktu, fitur-29, mesin MI, leakage, evaluator LA,
   skrining waktu+kontrol+rerun, verdict+T-07, FIG-13..16, kesimpulan) +
   `verify_registry` + `build()` + lock O_EXCL.
3. Smoke sel 12: MI sinyal 0.3718 > lantai 0.0052; noise 0.0031 < 0.0048;
   lift CI [0.9897, 1.0] > 0.
4. Smoke mock sel 15–18 (`smoke1518.py`, kode ASLI + data sintetis, REPORT_DIR
   temp): PASS — 8 artefak mock tertulis, rerun bit-identik PASS.
5. Full-run berulang, tiap gagal tepat satu sel (diperbaiki satu per satu):
   - Run A: sel 15 `TypeError` sort campuran int/`"ALL"` → kunci
     `key=(sesi, str(tercile))` deterministik.
   - Run B: sel 15 `IndexError` (mask ganda `y_full[mask]` + `mask`) →
     teruskan array penuh seperti sel 14.
   - Mock menemukan 2 bug yang PASTI kena full-run: `ev["sem"]` tertimpa
     array (rows semester hilang) → kunci `sem_rows` + pakai di T-07-4/FIG-15;
     sel 18 merujuk `len(CELLS)` (variabel builder) → literal `19 sel`.
   - Bug non-fatal lain: `MID_FIGURE_DIR` belum di sel notebook; bentuk
     `a5full`/`ema`/`h1`; `del WH, WL`; 2 char Cyrillic; kurung
     `concatenate`/lambda; `mi_dd` tanpa `minlength`; `z60` rolling-warmup
     (~1e-8) → batch eksplisit, validasi 5 titik OK.
6. Run C (detached via Task Scheduler, rantai foreground tunggal — Start-Process
   foreground berulang diduplikat harness): sel 01–15 selesai ±70 mnt
   (kernel ~100% 1 core), lalu STOP di gerbang kontrol. `nbconvert exit=1`.
7. Simulasi bias null (`simbias.py`, kode MI ASLI): lolos 5/5 pada semua n.
8. Gate mutu builder: `ruff check` PASS; `check_foreign_chars.py` OK;
   `check_cells.py` 19 sel OK. `pytest`/format tidak dijalankan ronde ini.

## Peristiwa STOP (verbatim)

```text
AssertionError: ASSERT GAGAL: nol kontrol lolos-G2 (alarm=[('LA ATR_k0.75_rr2 Tokyo t3 buy', 'round_d', 5), ('LA ATR_k1.5_rr1 NewYork t3 sell', 'round_d', 5), ('LA ATR_k1.5_rr1 NewYork t3 sell', 'round_d', 5)])
nbconvert exit=1
```

(nama target ketiga terpotong di log; daftar alarm penuh hanya 3 pertama yang
tercetak `CTRL_ALARM[:3]` lalu kernel mati — daftar penuh HILANG, lihat
keterbatasan. Ketiga yang terlihat: kontrol `round_d`, ok_n=5/5 semester.)

## Bukti bias (simulasi null murni, kode sel 12 asli, N_PERM=100)

X dan label biner = derau murni independen; bandingkan MI semester (`mi_dd`,
n_sem) vs lantai pooled (`mi_floor_all` p95, n_tot) — persis logika G2:

```text
  n_sem   n_tot   lantai  bias_MM~ lolos/sem (null murni, harapan ~=0.05)
    300    1500  0.01015   0.03167 5/5
   1000    5000  0.00296   0.00950 5/5
   3000   15000  0.00109   0.00317 5/5
  10000   50000  0.00031   0.00095 5/5
  30000  150000  0.00010   0.00032 5/5
```

- MI semester membawa bias Miller-Madow ~= sel-terisi/(2·n_sem), sementara
  lantai pooled menyusut dengan n_tot. Rasio bias ≈ n_tot/n_sem = 5×.
- Pada null MURNI pun lolos 5/5 di semua n — kriteria "MI semester >
  lantai-pooled" tidak memisahkan sinyal dari null.
- Dengan syarat arah-sama (acak per semester, P≈1/16 per pasangan per
  kontrol) dan ratusan pasangan (target × 3 kontrol), alarm dalam skala
  lusinan DIHARAPKAN di bawah null global. Gerbang kontrol tidak pernah
  berpeluang lolos — alarm ini sinyal metodologi yang bekerja, bukan sial.
- Catatan: bias ini juga melonggarkan G2 fitur (LOLOS berlebih; di mock
  21/62 LOLOS pada derau murni) — satu akar, dua gejala.

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Builder ada, ID/EN-only | TERVERIFIKASI | `git hash-object scripts/_build_eda07.py` = `007be86706d56171149d365a28bed608c8ec383e`; 1445 baris, 66536 byte; `ruff check` = `All checks passed!`; foreign_chars = `OK: 1 file discan`; `check_cells` = `sel total: 19 / sel code OK` |
| Notebook 19 sel tertulis (belum tereksekusi) | TERVERIFIKASI | `git hash-object notebooks/scalping/eda_07_label_fitur.ipynb` = `0af22ccb740dc30d60ec70db9b6dfefb5ffc42b9`; 75511 byte; 19 sel, 0 output tersimpan |
| Sel 01–15 tereksekusi di run C | TERVERIFIKASI | run7.log: `lock diperoleh`, `notebook ditulis (19 sel)`, `Converting notebook`; kernel ~3345 dtk CPU lalu `nbconvert exit=1` TEPAT di assert kontrol sel 15 (artinya skrining 60+200 target + rerun selesai tanpa assert-gagal) |
| STOP = respons pra-registrasi, bukan crash | TERVERIFIKASI | KONTRAK_07: "ALARM STOP hanya bila kontrol lolos kriteria G2"; kode assert persis itu; coder tidak mengubah ambang |
| Akar = bias-n struktural, bukan bug kode | TERVERIFIKASI | Tabel simulasi di atas (kode asli, null murni); loop kontrol memakai kriteria IDENTIK evaluator (verifikasi baris-per-baris); mock null juga alarm |
| Artefak T-07-1..4 / FIG-13..16 | GAGAL (belum ada) | Sel 16–18 belum pernah tereksekusi; `verify_registry` belum pernah hijau |
| LOLOS = bukti edge | DITOLAK | KONTRAK_07 + kesimpulan terkunci: LOLOS hanya izin ke Lapisan 3 |

## Terhenti (butuh putusan arsitek — coder tidak mengubah gerbang sepihak)

1. Pilih perbaikan S8-G2 vs lantai-pooled (opsi non-eksklusif, arsitek yang
   memutuskan): (a) lantai per-semester (bandingkan MI semester dengan
   lantai di n yang sama); (b) koreksi bias Miller-Madow pada MI sebelum
   banding; (c) revisi ambang/kriteria G2 di spec; (d) perlakukan kontrol
   struktural (`round_d`, `pdhl_d`) terpisah dari `noise` di aturan alarm.
2. Setelah putusan: coder ubah builder (+ mock smoke ulang) lalu full-run
   ulang ±70–90 mnt detached, verifikasi registry, tulis S5.

## Keterbatasan bukti ronde ini

- Daftar alarm penuh + tabel skrining (60 LA + 200 waktu) hilang bersama
  kernel (`--inplace` tidak menyimpan saat gagal); hanya 3 alarm pertama +
  exit code yang terekam di run7.log/err.
- Laju kontrol pooled ("X/Y di atas lantai") ikut hilang.
- Estimasi ±70 mnt didasarkan CPU kernel satu run; variansi antar-run belum
  diukur (seed terkunci → deterministik, rerun bit-identik di-assert di
  sel 15 sebelum gerbang).
- Task Scheduler `EDA07Build` masih terdaftar (Ready, sudah selesai); boleh
  dihapus: `schtasks /delete /tn EDA07Build /f`.
