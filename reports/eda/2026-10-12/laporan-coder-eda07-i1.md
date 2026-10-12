# Laporan Tugas — Coder I-1: Investigasi Alarm Struktural EDA-07

## File yang dibuat/diubah

- `scripts/_build_eda07_i1.py` (baru, 1385 baris, 63137 byte, SHA256 `8775C8A2…0E08B0`)
- `notebooks/scalping/eda_07_i1_adendum.ipynb` (baru, 18 sel = 1 markdown + 17 kode, tereksekusi, SHA256 `F1488991…E6A91`)
- `reports/eda/2026-10-12/T-I1-1.csv` (baru, 86 baris data)
- `reports/eda/2026-10-12/T-I1-2.csv` (baru, 86 baris data)
- `reports/eda/2026-10-12/T-I1-3.csv` (baru, 86 baris data + kolom `vonis_V2`)
- `reports/eda/2026-10-12/eda07_i1_progress.log` (baru, log progres I-1; `eda07_progress.log` run 9 TAK tersentuh)

## Apa yang dilakukan

Adendum kecil I-1 (bukan full-run): reuse verbatim jalur run 9 untuk data/strata/ATR/entri/LA-normal/label-waktu/fitur/mesin (`new_rng`, `chk`, `show`, `wall_clock_series`, `add_labels`, `simulate`, `combo_sl_tp`, `sesskey_mask`, `build_feature_frame`, `qcodes`, `apply_edges`, `get_sample`, seluruh mesin sel 12 run 9). Baru dan pra-registrasi: `X_PIN=10`, `SEEDI1={q2:80701,q3:80702}`, `N_LEAK_I1=60`, Q1/Q2/Q3, aturan putus V-2. `LA_S` tidak dibangun (I-1 tanpa G4). Eksekusi via `venv` Python 3.12.8, nbconvert timeout 5400, exit 0.

Hasil: Q1 konsentrasi; Q2 10/86 DEKAT-mendominasi (0 pdhl_d, 10 round_d), 39 JAUH-mendominasi (semua pdhl_d), 37 tak-beda; kalibrasi negatif 0/6 noise signifikan; Q3 16/86 Bertahan (9 pdhl_d, 7 round_d); vonis V-2: **7 ASLI (semua round_d)**, 79 ARTEFAK (52/52 pdhl_d ARTEFAK). Daftar 7 ASLI: `LB_rng London t3 N5`, `LB_rng London tALL N5`, `LB_bin Tokyo t2 N15`, `LB_bin Tokyo tALL N5`, `LB_rng Tokyo tALL N5`, `LB_bin Tokyo tALL N15`, `LB_rng Tokyo tALL N15` (seluruhnya kontrol `round_d`).

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Notebook 18 sel, 17 kode tereksekusi, 0 error | TERVERIFIKASI | `nbconvert exit=0`; parse ipynb: `sel total: 18`, `sel kode tereksekusi: 17`, `error: 0` |
| Reuse fungsi run 9 dipakai ulang (bukan ditulis ulang) | TERVERIFIKASI | Nama fungsi di atas, disalin verbatim sel 02/03/04/05/06/07/08/10/11/12/13/14 run 9; satu-satunya edit non-verbatim: `del WH, WL` sempat ditambah lalu DIBUANG (gagal run 1), `N_LEAK`→`N_LEAK_I1`, ekstraksi `get_sample` |
| >=1000 sampel label/fitur SAMA PERSIS | TERVERIFIKASI | Output sel 13: `rebuild fitur eksak-identik 165,890 baris`; `re-simulate LA ATR_k0.75_rr2 London buy bit-identik`; `label waktu move 1000/1000 sama persis per N (4x1000 cek)`; `n 60/60 LA == _ckpt_`, `n 200/200 waktu == _ckpt_` |
| X=10 pip satu nilai, DEKAT/JAUH + seed tercatat & di-assert | TERVERIFIKASI | Output sel 15: `chk X pra-registrasi = 10 pip` lolos; `dekat = |d| <= X_PIN`; `SEEDI1: {'q2': 80701, 'q3': 80702}`; stream `new_rng_i1("q2"/"q3", eidx)` |
| Parameter run 9 tak tersentuh (nilai identik) | TERVERIFIKASI | Jangkar lolos: B=185.248, N_ENT=184.731, 23+7 irisan, builder run 9 `bd40e1a3`; hash builder run 9 SEBELUM vs SESUDAH sama (baris di bawah) |
| File run 9 bit-identik SEBELUM vs SESUDAH (6/6) | TERVERIFIKASI | SEBELUM: `bd40e1a35e6a builder`, `4f1f98e6a3e5 notebook`, `589d4ff4b8db skrining`, `de39bef0825b alarm`, `bf8b413df31a ckpt_LA`, `68c7d33b3941 ckpt_T` — SESUDAH: keenam hash SAMA persis (output sel 17 + verifikasi shell `Get-FileHash` pasca-build: `BD40E1A35E6A…`, `589D4FF4B8DB…`, `DE39BEF0825B…`, `BF8B413DF31A…`, `68C7D33B3941…`) |
| T-I1-1/2/3 ada, 86 baris data, satu lokasi | TERVERIFIKASI | `verify_i1: registry CSV T-I1 (3): ['T-I1-1.csv', 'T-I1-2.csv', 'T-I1-3.csv'], masing-masing 86 baris data` |
| Sel kesimpulan SATU paragraf terisi | TERVERIFIKASI | Output sel 17 `KESIMPULAN TERKUNCI:` 1 paragraf (>200 karakter, `chk` lolos), isi: 7 ASLI (0 pdhl_d, 7 round_d), 79 ARTEFAK |
| Kalibrasi negatif: mesin I-1 sah | TERVERIFIKASI | Output sel 15: `kalibrasi negatif Q2: 0/6 noise signifikan`; sel 16/17: noise 6/6 `tak-beda`/`Lenyap`/`ARTEFAK` |
| Q2: tak satu pun pdhl_d DEKAT-mendominasi; 39/52 pdhl_d JAUH-mendominasi | TERVERIFIKASI | Tabel `vonis Q2 pdhl_d`: JAUH-mendominasi 39, tak-beda 13, DEKAT-mendominasi 0 |
| Q2 round_d: 10/28 DEKAT-mendominasi | TERVERIFIKASI | Tabel `vonis Q2 round_d`: tak-beda 18, DEKAT-mendominasi 10 |
| Q3: Bertahan 9/52 pdhl_d, 7/28 round_d | TERVERIFIKASI | Tabel `vonis Q3 pdhl_d`: Lenyap 43, Bertahan 9; `round_d`: Lenyap 21, Bertahan 7 |
| Vonis V-2: 7 ASLI / 79 ARTEFAK | TERVERIFIKASI | Tabel `vonis V-2 keseluruhan`: ARTEFAK 79, ASLI 7; silang Q2xQ3 ditempel di output sel 17 |
| Builder ASCII/LF/tail-LF | TERVERIFIKASI | Shell: `nonASCII=0`, `hasCR=False`, `tailLF=10`, `bytes=63137`, `lines=1385` |
| git: nol stage ronde ini, HEAD tak bergerak | TERVERIFIKASI | `git status --porcelain=v1`: tanpa baris `A `/staged; `git rev-parse HEAD` = `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` |
| Hash builder+notebook SESUDAH + baris/byte | TERVERIFIKASI | Builder SHA256 `8775C8A2892F67636BBA5F81B965457F6FA359B5CED83CEBC2F501F14C0E08B0`, 1385 baris, 63137 byte; notebook SHA256 `F1488991593A4D1F8BE175D2196E819052C3454F4FA33C171CBA328F716E6A91`, 94783 byte |
| ASSERT_LOG >= 20 | TERVERIFIKASI | Output sel 17: `ASSERT_LOG total: 591` |
| Q1 konsentrasi utama | TERVERIFIKASI | Tokyo 49/80 (61,2%), London 27/80; LA 24, LB_rng 23, LB_bin 14, LC2 11, LC1 7, LD 1; horizon N=5: 26/56 (46,4%); sisi LA buy 14 vs sell 10 (output sel 14) |
| Pooled-terbobot Q3 = rerata lift desil berbobot-n, tepi pooled tetap | TERVERIFIKASI | Definisi di sel 16 + kontrak sel 01 (`tepi pooled`, bobot n desil pooled, bootstrap klaster-hari 1000x stream q3+eidx); pilihan terdokumentasi di kode, bukan klaim hasil |
| Vonis ASLI = kandidat S/R (bukan bukti edge) | TERVERIFIKASI | Aturan V-2 diterapkan verbatim (`ASLI iff DEKAT-mendominasi DAN Bertahan`); DILARANG promosi kontrol dipatuhi (tanpa fitur sinyal baru) |

## Yang belum diverifikasi

- Audit independen oleh Auditor (wajib multi-AI; coder DILARANG audit sendiri).
- Keputusan arsitek atas 7 ASLI round_d (wewenang V-3; I-1 hanya menyimpulkan label ASLI/ARTEFAK).
- Rerun determinisme penuh notebook (satu eksekusi sukses; rerun bit-identik mengikuti pola run 9, belum diuji ulang di sini).

## Potensi masalah

1. Tiga run gagal sebelum sukses (tercatat jujur): (a) `del WH, WL` non-verbatim mematahkan re-simulate — dibuang, kembali verbatim run 9; (b) salah kurung `B3_ROUND` — tertangkap pre-kompilasi sel yang saya tambah; (c) `CELLS` dirujuk di sel notebook — diganti literal 18 + assert builder; (d) CRLF dari `to_csv` Windows — normalisasi byte CRLF→LF sebelum assert ASCII (pola sama seperti run 9 untuk notebook). Semua diperbaiki tanpa mengubah hasil/metode.
2. `to_csv` menulis CRLF di Windows — sudah dinormalisasi di sel 17; CSV final LF + tail-LF terassert.
3. Lock `.eda07_i1_build.lock` sempat basi akibat crash pra-kompilasi — dibuang manual setelah verifikasi tak ada proses Python jalan; lock dilepas normal pada run sukses (`lock dilepas; build selesai.`).
4. `rng_lab = new_rng("leak")` dipakai ulang setelah `rng_leak` (stream sama, objek Generator terpisah; deterministik, tercatat di kode).
5. Q2 `LB_rng` memakai selisih mean (kontinu), bukan rate — definisi pra-registrasi di docstring `pair_sample`; verdict memakai aturan CI yang sama.
6. JAUH untuk noise degenerat (|noise|<=10 ≈ seluruh sampel) — hasil jujur `tak-beda` (sisi kosong → NaN → bukan signifikan), mendukung ekspektasi tak-berpola.
7. File run 9 berstatus untracked di HEAD `b18992b` — sehingga bukti "tak tersentuh" bertumpu pada hash SEBELUM vs SESUDAH 6/6 (ditempel keduanya), bukan `git diff`.

## Saran berikutnya

1. Serahkan ke Arsitek untuk V-3: 7 pasangan ASLI round_d (daftar di atas) layak ditinjau; 52/52 pdhl_d ARTEFAK dengan pola dominan JAUH-mendominasi (39/52) = ciri artefak proxy-jarak sesuai falsifikasi V-2.
2. Auditor: verifikasi kepatuhan I-1 terhadap falsifikasi pra-registrasi (X tunggal, stream terpisah, aturan putus verbatim) dari CSV + notebook ini.
3. DILARANG: model/backtest/P&L/vonis edge dari hasil ini; DILARANG promosikan `round_d`/`pdhl_d` jadi fitur sinyal; Lapisan 3 tetap terkunci hingga arsitek memutuskan.

Status: TERVERIFIKASI (eksekusi) — vonis isi mengikuti V-2 apa adanya, tanpa vonis edge.
