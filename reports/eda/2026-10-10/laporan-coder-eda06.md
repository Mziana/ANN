# Laporan Tugas Coder EDA-06 — Port + Eksekusi Gerbang Biaya

Tanggal: 2026-10-10. Peran: Coder (bukan arsitek, bukan auditor). Brief:
`.ai/assistant/prompts/2026-10-10_eksekusi-eda06-coder.md`. STOP setelah
serah-terima. Bahasa: Indonesia.

## File yang dibuat/diubah

- `scripts/_build_eda06.py` (baru, 1115 baris, 50959 byte) — generator +
  executor nbconvert pola `_build_eda05.py`; template = 27 sel referensi
  VERBATIM; registry FIG-01..12 + 14 CSV; lokasi output opsi-2
  `reports/eda/2026-10-10/`.
- `notebooks/scalping/eda_06_biaya_breakeven.ipynb` (baru, hasil generate +
  eksekusi penuh, 365784 byte) — 27 sel, 16 sel kode tereksekusi 1-16,
  0 error.
- `reports/eda/2026-10-10/` (baru) — 14 CSV T-06 + FIG-08..12 (5 file).
- Laporan ini: `reports/eda/2026-10-10/laporan-coder-eda06.md`.
- Referensi TIDAK diubah (2 hash cocok, bukti di bawah).

## Apa yang dilakukan

1. S-0: baca AGENTS.md, design `2026-10-10-eda06-eksekusi-design.md`,
   rancangan EDA_06_07 bagian 0-2, notebook referensi (27 sel).
2. Tulis builder pola `_build_eda05.py`; emit awal 27/27 VERBATIM;
   `ruff check` + `ruff format` PASS; ASCII/LF/tail-LF PASS.
3. Run 1: notebook tereksekusi penuh (nbconvert exit=0) tetapi
   `verify_registry` gagal pada URUTAN list (bug bungkus sendiri:
   `sorted()` vs urutan TABLES) — BUKAN kesalahan referensi.
   Perbaikan bungkus: bandingkan `sorted()`; re-verify PASS.
4. Re-verify penuh pasca-compact: semua angka di bawah dibaca ulang dari
   artefak (bukan dari memori).
5. Gate mutu: pytest 254 passed; ruff notebook = 14 temuan pra-ada
   referensi (dilaporkan GAGAL-dengan-sebab, tidak diperbaiki karena
   kunci VERBATIM + larangan-1).

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Builder ada, ASCII/LF-only/tail-LF | TERVERIFIKASI | `git hash-object scripts/_build_eda06.py` = `fab369e674321867666356d031132a7f20ef854e`; byte=50959 baris=1115; nonASCII=0 CRLF=0 tail=`b'    build()\n'` |
| Notebook tereksekusi penuh ada | TERVERIFIKASI | `git hash-object notebooks/scalping/eda_06_biaya_breakeven.ipynb` = `dd0f229d6a18dbbdbe69d2f6022bba445cff64a7`; byte=365784; 27 sel, exec_counts=[1..16], errors=0 |
| 27/27 sel VERBATIM vs referensi | TERVERIFIKASI | Perbandingan `(kind, source)` per sel: diff NIHIL (skrip cek di sesi, output `CELLS len: 27 \| diff: NIHIL`) |
| Referensi tak diubah | TERVERIFIKASI | `git hash-object thoughts/shared/references/eda06/eda_06_biaya_breakeven.ipynb` = `6a6c6516bc96e7e9a7845a13b1909927cc718e75`; `.../EDA_06_07_rancangan.md` = `6724c37ec5493b821d0179d0d00768fbd343a485` (sesuai brief) |
| Tanpa stage/commit ronde ini, HEAD tetap | TERVERIFIKASI | `git status --porcelain=v1` hanya `M` tak-stage (file sesi pra-ada) + `??` (file ronde ini); `git rev-parse HEAD` = `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` |
| B = 185.248; 5 semester A; tanpa Off di A; tanpa 2026 | TERVERIFIKASI | Output code#4: `PASS: strata konsisten dengan Lapisan 1 (B=185.248), partisi utuh, tanpa bar Off di A, tanpa 2026.` + `semester strata A: ['2023H2','2024H1','2024H2','2025H1','2025H2']` |
| Fingerprint sesi cocok | TERVERIFIKASI | Output code#2: `PASS: definisi sesi identik dengan Notebook 00 (sidik jari cocok).` |
| cost_basis konsisten | TERVERIFIKASI | Output code#5: `PASS: cost_basis config konsisten dengan data 2023-2025 (toleransi 0,15 pip; config memuat 2026).` |
| ATR 12/12 identik tanpa look-ahead | TERVERIFIKASI | Output code#9: `PASS: ATR di 12 timestamp acak identik bila hanya memakai data sampai T (tanpa look-ahead).` |
| Simulator vektor = naif 400x2 | TERVERIFIKASI | Output code#11: `PASS: simulator vektorisasi identik dengan implementasi naif (400 entri x 2 sisi).` |
| T-06-4 A+B terpisah | TERVERIFIKASI | `T-06-4_grid_pstar.csv`: strata=['A','B'], 32 baris |
| 14 CSV tersimpan satu lokasi | TERVERIFIKASI | `reports/eda/2026-10-10/`: T-06-1a,1b,1c,1d,2a,2b,3,4,5_B,5_desil,5_sesi,6,7_sesi,7_tercile (=14); code#16: `tersimpan 14 tabel CSV dan 5 gambar di reports\eda\2026-10-10` |
| FIG-08..12 sekuensial, FIG-01..07 utuh | TERVERIFIKASI | Baru: `FIG-08_ekor_spread_per_jam.png, FIG-09_spread_vs_volatilitas.png, FIG-10_heatmap_pstar.png, FIG-11_stabilitas_semester.png, FIG-12_delta_vs_atr.png`; lama `FIG-01..07.png` tepat di `reports/eda/2026-10-06/figures/` |
| Gerbang: 144+48 diuji; lolos 23 + 7; VERDICT LOLOS | TERVERIFIKASI | Output code#15: `irisan diuji: (combo x sesi x tercile) = 144 \| (combo x sesi) = 48`; `LOLOS semua gerbang: tercile=23 dari 144 \| sesi=7 dari 48`; `K1 saja: 32 \| K1&K2: 23 \| K1&K2&K3: 23 \| semua (+K4): 23`; `KEPUTUSAN: ADA IRISAN LOLOS...`; CSV cek ulang: tercile 144 baris/23 lolos, sesi 48 baris/7 lolos; code#16: `VERDICT gerbang: LOLOS` |
| Builder lolos ruff + format + foreign_chars | TERVERIFIKASI | `ruff check` = `All checks passed!`; `ruff format --check` = `1 file already formatted`; `check_foreign_chars.py` = `OK: 1 file discan, tidak ada karakter asing.` |
| pytest full hijau | TERVERIFIKASI | `254 passed in 18.93s` |
| Notebook lolos ruff | GAGAL | `Found 14 errors`: E402x9 (cell 3), SIM300x3 (cell 13x2, 15), B023 (cell 18), B905 (cell 26) — SAMA PERSIS dengan temuan referensi pra-eksekusi. Sebab: kunci VERBATIM + larangan-1 brief (dilarang ubah pasca-run). Bukan regresi eksekusi. |
| LOLOS = bukti edge | GAGAL (ditolak) | KONTRAK_06 + output code#15: `LOLOS bukan bukti edge, hanya izin fokus EDA-07`. Tidak diklaim. |

### Output mentah kunci (tempel, bukan ringkasan)

```
fab369e674321867666356d031132a7f20ef854e   <- scripts/_build_eda06.py
dd0f229d6a18dbbdbe69d2f6022bba445cff64a7   <- notebooks/.../eda_06_biaya_breakeven.ipynb (post-exec)
6a6c6516bc96e7e9a7845a13b1909927cc718e75   <- referensi ipynb (cocok brief)
6724c37ec5493b821d0179d0d00768fbd343a485   <- referensi md (cocok brief)
b18992b5e57d45c125aacf3ca868c2f9e135d9d1   <- HEAD (tak berubah)
254 passed in 18.93s                        <- pytest tests
```

## Yang belum diverifikasi

- Isi sel Kesimpulan notebook (sel 26, `isi manual setelah membaca tabel`)
  dibiarkan untuk pembaca/arsitek — coder tidak mengisi (bukan vonis).
- Determinisme rerun (run 2x identik) tidak diuji ulang; seed terkunci
  20261010 di referensi, builder deterministik by-construction.
- Review auditor independen atas ronde ini (di luar peran coder).

## Potensi masalah

1. Ruff notebook 14 temuan pra-ada (E402/SIM300/B023/B905) — bawaan
   referensi; setiap perbaikan = pelanggaran VERBATIM. Bila arsitek ingin
   bersih, keputusan ada di arsitek (bukan coder pasca-run).
2. `run 1` gagal di `verify_registry` karena bug urutan di bungkus
   (diperbaiki, bukan referensi). Final state PASS, tercatat di sini agar
   tidak diulang.
3. Lokasi output memakai opsi-2 `reports/eda/2026-10-10/` (opsi-1
   `2026-10-06/figures/` tidak dipakai) — FIG-01..07 tetap di lokasi lama.

## Saran berikutnya

1. Auditor: verifikasi independen 27/27 + angka gerbang dari CSV
   (`T-06-7_gerbang_tercile.csv` 144/23, `T-06-7_gerbang_sesi.csv` 48/7).
2. Arsitek: tulis spec EDA-07 dengan scope = 23 irisan tercile + 7 irisan
   sesi lolos (daftar di output code#15 notebook).
3. Isi sel Kesimpulan notebook setelah telaah tabel (peran pembaca,
   bukan coder).

## SELF-AUDIT 3x ADVERSARIAL

Putaran 1 Correctness: 27/27 sel `(kind,source)` NIHIL diff — bungkus hanya
menambah pemanggil builder. Holdout: asersi `max(utc) < 2026-01-01` PASS
(code#4, tanpa 2026). B=185.248 PASS (asersi strata). Fingerprint PASS.
ATR 12/12 PASS. Simulator 400x2 PASS. FIG-08..12 sekuensial, FIG-01..07
tak tersentuh. CSV tepat 14. Tidak ada yang gagal kecuali ruff-notebook
yang memang dikunci VERBATIM.

Putaran 2 Bias: tidak ada ambang digeser (K1 3,0/5,0pp, K2 >=4/5, K3
1000/100 hari, K4 <=50% — semua dari referensi, sebelum run pertama).
B tidak masuk K2 (T-06-5_B dan T-06-4 strata B terpisah; kriteria K2 hanya
semester A). 2026 tidak dimuat sama sekali. Delta kecil tidak diklaim
sebagai edge (KEPUTUSAN eksplisit: bukan bukti edge). Tidak ada irisan
sekunder dipromosikan (rekomendasi = tepat irisan LOLOS).

Putaran 3 Meta-check: file baru hanya builder + notebook + outputs
`reports/eda/2026-10-10/` + laporan ini. Referensi 2 hash cocok.
Builder ASCII/LF/tail-LF. Nol stage/commit/push (porcelain bersih dari
tindakan ronde ini; HEAD `b18992b` tak berubah). Nol vonis baru
(H1/H2/H3/H5/H4b/R-2 GUGUR, H4 TAHAN tak disentuh). Nol tulis governance
selain laporan tugas ini. Nol dependensi baru. Nol tulis
configs/src/data.
