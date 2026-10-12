# Laporan Tugas — Coder I-2: Penyelesaian EDA-07 (G1-G4 Penuh + 7 Kandidat)

## File yang dibuat/diubah

- `scripts/_build_eda07_i2.py` (baru, 1672 baris, 81200 byte, SHA256 `A388472581CA7C9032FF2A3E07EBD3A739AD9C63FF75D8BF85BE02F6E34FBAE9`)
- `notebooks/scalping/eda_07_i2.ipynb` (baru, 22 sel = 1 markdown + 21 kode, 21 tereksekusi, 0 error, 162728 byte, SHA256 `442720BA70BD1333C6B77D1921FF84A002858FCB7808C9996B809DD8E173085E`)
- `reports/eda/2026-10-12/T-07-1_balance.csv` (baru, 260 baris data)
- `reports/eda/2026-10-12/T-07-2_mi_lantai.csv` (baru, 6767 baris data)
- `reports/eda/2026-10-12/T-07-3_lift.csv` (baru, 1315 baris data)
- `reports/eda/2026-10-12/T-07-4_stabilitas.csv` (baru, 1335 baris data)
- `reports/eda/2026-10-12/FIG-13_mi_lantai.png` (36798 byte), `FIG-14_lift_desil.png` (25013 byte), `FIG-15_stabilitas.png` (19435 byte), `FIG-16_balance.png` (14626 byte)
- `reports/eda/2026-10-12/_gate_G2_alarm_i2.csv` (87 baris), `_gate_G2_skrining_i2.csv` (781 baris), `_ckpt_LA_i2.csv`, `_ckpt_T_i2.csv`, `eda07_i2_progress.log` (+ duplikat `eda07_progress.log`, lihat C4), `run_i2.log`
- File run 9 / I-1 / G2: TAK tersentuh (13/13 hash SEBELUM vs SESUDAH sama, tabel di bawah)

## Apa yang dilakukan

Full-run penyelesaian I-2 (mandat V-6 mengikat): salin `scripts/_build_eda07.py` -> `_build_eda07_i2.py`, terapkan 12 edit terdokumentasi (docstring I-2, NB_PATH i2, REPORT_DIR 2026-10-12 + REPORT_FROZEN beku, log/ckpt `_i2`, regresi V-6 ganti STOP, KONTRAK_I2 sel 01b, K24 24/24 sel 03b, sel 15b kandidat 7xG1/G2, T-07/VDF_CAND sel 16, KESIMPULAN_I2 sel 18, verify_i2 + lock i2 + assert 22 sel). Sel 01-15 dipertahankan verbatim run 9 (data/strata/ATR/entri/LA/label-waktu/fitur/MI/lift/leakage/sampel/skrining; SEED07, ambang A-3, N, bin, theta TAK berubah). Stream baru tercatat: lift kandidat `new_rng("lift_base", 10000+eidx)` (rentang disjoint dari run 9); MI kandidat dihitung-ulang dengan stream kontrol identik (`floor_base`, 10000+eidx) lalu diassert bit-identik. Eksekusi detached via Task Scheduler (`venv` Python 3.12.8, nbconvert timeout 5400, exit=0, 14:22 -> 16:29 WIB ~2h07m; task dihapus pasca-run, `Last Result: 0`).

Hasil native: 260 pasangan dievaluasi (60 LA + 200 waktu), **98 LOLOS / 162 GUGUR**; irisan >=1 label lolos 29 dari 37 (penjelasan 37 di C1); FIG target `LB_bin Tokyo tALL N5` (wakil rv60). Kandidat V-5 7/7 dinilai (G4=NA ketujuh, non-LA): **5 LOLOS** (seluruh Tokyo) Slug **2 GUGUR** (seluruh London); seluruh lift kandidat NEGATIF — 5 Tokyo LOLOS dengan efek INVERS (peringatan C3, bukan edge positif).

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Notebook 22 sel, 21 kode tereksekusi, 0 error | TERVERIFIKASI | `nbconvert exit=0`; parse ipynb: `sel: 22`, `kode tereksekusi: 21`, `error: 0`; `lock dilepas; build selesai.` |
| Regresi kontrol V-6: alarm 86/86 + skrining 780/780 identik beku | TERVERIFIKASI | Output sel 17: `PASS: regresi kontrol 86/86 + skrining 780/780 identik beku -> lanjut verdict (V-6).`; komposisi alarm: 52 pdhl_d + 28 round_d + 6 noise (output sel 21); file `_i2` 87/781 baris (header + 86/780) |
| Nol kontrol BARU di luar 86 | TERVERIFIKASI | Output sel 21: `nol kontrol BARU di luar 86` |
| Rerun MI+lantai bit-identik (stream tunggal per blok) | TERVERIFIKASI | Output sel 17: `PASS: rerun MI+lantai bit-identik (stream RNG tunggal per blok).`; anti-leakage 200/200 identik (rtol=1e-9, lookback 20.000 bar, output sel 21) |
| 24/24 konstanta run 9 identik (nol drift) | TERVERIFIKASI | Output sel 05: `PASS: 24/24 konstanta run 9 identik (nol drift).`; diff threshold kosong (hanya K24 assert + pemakaian CTRL_COLS/YCODE/YPOS berubah) |
| n 260/260 == _ckpt_ (60 LA + 200 waktu, tidx ..259) | TERVERIFIKASI | Output sel 14/15/17: `LA selesai: 60 target`, `waktu selesai: 200 target (tidx ..259)`, `verdict target: 260 dievaluasi` |
| File beku 13/13 bit-identik SEBELUM vs SESUDAH | TERVERIFIKASI | SEBELUM `BD40E1A35E6A…/8775C8A2892F…/4F1F98E6A3E5…/F1488991593A…/589D4FF4B8DB…/DE39BEF0825B…/BF8B413DF31A…/68C7D33B3941…/DCDFF41882CB…/83046E121F6D…/A1BC480AEF3F…/D6BEDF8DDF20…/2E093460BBA3F…` — SESUDAH via `Get-FileHash` pasca-run: ketiga-belas SAMA persis |
| Kalibrasi: kontrol pooled 145/780 = 0.186 di atas lantai | TERVERIFIKASI | Output sel 17: `kontrol pooled di atas lantai: 145/780 = 0.186 (harapan ~= 0.05)` |
| Balance sum-to-1 untuk 220 target diskret | TERVERIFIKASI | Output sel 21: `PASS: balance sum-to-1 untuk 220 target diskret.` |
| Verdict native 98 LOLOS / 162 GUGUR; irisan 29/37 | TERVERIFIKASI | Output sel 19: `verdict target: 260 dievaluasi, LOLOS=98, GUGUR=162`; `irisan LOLOS (>=1 label): 29 dari 37`; TARGET-LOLOS 98 baris data |
| FIG target = LB_bin Tokyo tALL N5 (wakil rv60) | TERVERIFIKASI | Output sel 19: `FIG target: LB_bin Tokyo tALL N5 (irisan ('ses', 'ATR_k1.5_rr1.4', 'Tokyo', 0))`; FIG-13..16 tersimpan (output sel 20 + 4 PNG di atas) |
| TOP3 (irisan x label x fitur) | TERVERIFIKASI | Output sel 21: `LB_bin London t1 N5` (rv60, lift 0.3108, CI 0.2676-0.3505); `LB_rng London t1 N5` (rv60, 4.9216, 4.4724-5.3979); `LC1 London t1 N5` (rv60, 0.1297, 0.1015-0.1598) |
| 7 kandidat dinilai G1-G4; N_CAND_PASS=5 | TERVERIFIKASI | Output sel 18, 7/7 `G1=True G2a&G2b=True`; LOLOS: `LB_bin Tokyo t2 N15` (lift -0.0473, CI -0.0831..-0.0114), `LB_bin Tokyo tALL N5` (-0.0549, -0.0830..-0.0284), `LB_rng Tokyo tALL N5` (-0.7446, -1.2340..-0.2600), `LB_bin Tokyo tALL N15` (-0.0279, -0.0539..-0.0010), `LB_rng Tokyo tALL N15` (-1.5868, -2.4808..-0.6550); GUGUR: `LB_rng London t3 N5` (CI -1.1397..0.0168 memuat 0), `LB_rng London tALL N5` (CI -0.9397..0.0575 memuat 0); `G4=NA: ketujuh target-waktu non-LA` |
| T-07 x4 + FIG-13..16 + kesimpulan terkunci | TERVERIFIKASI | `verify_i2: registry figures FIG-13..16` + `registry CSV T-07 (4)`; output sel 21 `KESIMPULAN_I2 TERKUNCI:` 1 paragraf (>200 karakter, `chk` lolos); `ASSERT_LOG total: 569` |
| Builder ASCII/LF/tail-LF, pre-kompilasi 22/21 | TERVERIFIKASI | Shell pra-run: `nonASCII=0 hasCR=False tailLF=10 bytes=81200 lines=1672`; pre-kompilasi OK 22 sel (21 kode); `ruff PASS` via `venv -m ruff` |
| git: nol stage ronde ini, HEAD tak bergerak | TERVERIFIKASI | `git status --porcelain`: tanpa baris staged (`M` hanya state-file sesi lain + `??` untracked termasuk artefak I-2 baru); HEAD `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` |
| CSV I-2 LF murni (beda byte vs beku CRLF = normalisasi terdokumentasi) | TERVERIFIKASI | Byte-check: beku `_gate_G2_alarm.csv` CRLF 87/87 vs `_i2` LF 87/0; skrining beku CRLF 781/781 vs `_i2` LF 781/0; T-07-1 LF 261 (pola run 9/I-1, dinormalisasi di sel 18) |

## Yang belum diverifikasi

- Audit independen oleh Auditor (wajib multi-AI; coder DILARANG audit sendiri) — mencakup C1-C3 di bawah.
- Putusan arsitek atas Lapisan 3 (wewenang arsitek; I-2 hanya menilai layak/tidak-layak G1-G4).
- Rerun determinisme penuh notebook (satu eksekusi sukses; rerun bit-identik mengikuti pola run 9, belum diuji ulang di sini).

## Potensi masalah

1. **C1 — peringkat irisan 37 baris, bukan 30 (dijelaskan, bukan cacat).** Scope G2 = 23 irisan ter LOLOS (dari 144) + 7 irisan sesi LOLOS (dari 48) = 30. Tujuh baris ekstra adalah pseudo-irisan `("ter", combo, sess, 0)` dari target LA berkind-ses (tercile 0): cabang LA `assoc_irisan`/`scope_of` tak memeriksa kind dan memetakan `tval "0"` -> `("ter", ...)` — perilaku VERBATIM run 9 (fungsi identik di builder beku baris 1173-1185, saya verifikasi yer; salinan saya di sel 16 notebook tereksekusi juga identik). Rekalkulasi independen dari `T-07-1_balance.csv` + CSV T-06-7 menghasilkan PERSIS 37 irisan dengan 7 ekstra yang sama. Dampak: hanya tampilan peringkat (7 baris tambahan dengan n_lolos masing-masing); verdict per-target, gerbang regresi, kandidat, dan FIG pick TAK terpengaruh (FIG target dari peringkat-1 sah `(ses, ATR_k1.5_rr1.4, Tokyo, 0)`). Bukan konflik V-4/V-5/V-6 -> bukan STOP; diteruskan ke auditor apa adanya.
2. **C2 — kesimpulan tercetak "notebook 19 sel" (kosmetik).** Sisa literal template run 9 (notebook run 9 = 19 sel / 18 kode; I-1 = 18/17; I-2 aktual = 22/21). Angka hasil tak terpengaruh; f-string di builder I-2 tak saya parameterisasi karena sel kesimpulan verbatim. Auditor: abaikan angka sel dalam teks kesimpulan, pakai parse ipynb (22/21/0).
3. **C3 — seluruh lift kandidat NEGATIF; 5 LOLOS Tokyo = efek INVERS.** Aturan G3 pra-registrasi = CI tak memuat 0 (tanpa syarat arah). Kelima CI Tokyo sepenuhnya negatif: desil atas `round_d` berasosiasi dengan rate label LEBIH RENDAH. Ini LOLOS prosedural, BUKAN edge positif, dan arahnya berlawanan dengan intuisi sinyal. Arsitek WAJIB membaca arah sebelum putusan Lapisan 3; DILARANG memakai 5 LOLOS sebagai dasar sinyal long/label.
4. **C4 — duplikat log progres identik.** `eda07_progress.log` (nama verbatim run 9) dan `eda07_i2_progress.log` (nama I-2) berisi byte identik (8911). Direktori `reports/eda/2026-10-12/` berstatus untracked sehingga tak ada file beku yang tertimpa; hanya observasi kebersihan, bukan cacat hasil.
5. Pra-run jujur: (a) `SyntaxError` kurung kurawal dict T073 tertangkap pre-kompilasi — diperbaiki sebelum build; (b) banding boolean kolom CSV skrining dinormalisasi via `str()==True`; (c) `.venv` DITOLAK (pandas 3.0.6 + tanpa nbformat/pip) -> pakai `D:\ANN\venv` (Python 3.12.8, pandas 2.2.3, nbformat OK); (d) normalisasi CRLF->LF byte CSV I-2 sebelum assert ASCII (pola I-1/run 9).
6. File run 9/I-1/G2 berstatus untracked di HEAD `b18992b` — sehingga bukti "tak tersentuh" bertumpu pada hash SEBELUM vs SESUDAH 13/13 (ditempel keduanya), bukan `git diff`.

## Saran berikutnya

1. Auditor: verifikasi kepatuhan I-2 — (a) regresi 86/86 + 780/780 dari `_gate_G2_*_i2.csv` vs beku; (b) stream kandidat (`lift_base` 10000+eidx disjoint; MI rerun bit-identik); (c) aturan G3 verbatim termasuk arah lift negatif (C3); (d) rekalkulasi C1 (37 = 30 + 7) dari T-07-1 + T-06-7; (e) kelengkapan T-07 x4 + FIG-13..16 + KESIMPULAN_I2.
2. Arsitek: putusan Lapisan 3 hanya atas pasangan LOLOS + fitur wakilnya (98 native + 5 kandidat Tokyo dengan catatan INVERS C3); 162 GUGUR + 2 kandidat London = BERHENTI (rumuskan ulang target, DILARANG baseline).
3. DILARANG: model/backtest/P&L/vonis edge dari hasil ini; DILARANG generalisasi sesi (konsentrasi Tokyo/London menempel); DILARANG promosikan `round_d`/`pdhl_d` jadi fitur sinyal; Lapisan 3 tetap terkunci hingga arsitek + auditor selesai.

Status: TERVERIFIKASI (eksekusi) — vonis isi mengikuti V-6/V-5 apa adanya (98/162 native; 5/7 kandidat LOLOS-invers, 2 GUGUR), tanpa vonis edge.
