# Hasil Telaah Fondasi B (U-1 - U-3) - Coder

- Peran: CODER (.ai/AGENTS.md v3.0 pasal 26) - implementasi + self-audit. Bukan penentu arsitek, bukan auditor.
- Brief: arsitek/protokol-telaah-fondasi-B.md (blob `ed436fddf607d3629fa226fd34d20ff60bf47232`).
- Tanggal eksekusi: 2026-10-09. Branch `main`, HEAD saat eksekusi `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
- Interpreter kanonik: `venv/Scripts/python.exe` (Python 3.12.8, pandas 2.2.3, numpy 1.26.4, scipy 1.17.1).
- File sementara: HANYA `%TEMP%\opencode\fondasiB\`. Nol tulis repo kecuali satu file laporan ini.
- Nol commit. DILARANG merumuskan H6. Vonis H1-H5 TIDAK diubah.

Status worktree saat eksekusi (`git status --porcelain`): staged = 2 berkas milik pihak lain
(`A src/features/build_labels.py`, `A tests/test_build_labels.py`) - TIDAK disentuh, TIDAK di-unstage.
Berkas modified/untracked lain (`.ai/*`, `reports/eda/progress/*`, penghapusan paket lama, dll.) juga
TIDAK disentuh. Laporan ini adalah satu-satunya tulisan-repo ronde ini.

---

## S0 - Gerbang hash (ukur ulang sesi coder, bukan salin sesi arsitek)

Perintah mentah:

```
$ git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md reports/governance/2026-10-07/Audit/reaudit-lapisan3-H4H5.md reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md reports/governance/2026-10-07/arsitek/protokol-telaah-fondasi-B.md
4a46b815211e6b0b050cbb6f3e98ce5e27904069
f06a8e27b916172f5824438acd545614360d3b57
8a4d21090f27dd53555b3a12583ec337819efb2f
e02a203b96879d73e90339f2d78a37d15834a23a
ed436fddf607d3629fa226fd34d20ff60bf47232
```

Tabel Klaim & Bukti (S0):

| # | Klaim (sesi arsitek) | Ukur sesi coder | Status |
|---|---|---|---|
| 1 | `4a46b815...` spesifikasi-lapisan3-H4H5.md | `4a46b815211e6b0b050cbb6f3e98ce5e27904069` | COOK |
| 2 | `f06a8e27...` hasil-lapisan3-H4H5.md | `f06a8e27b916172f5824438acd545614360d3b57` | COOK |
| 3 | `8a4d2109...` Audit/reaudit-lapisan3-H4H5.md | `8a4d21090f27dd53555b3a12583ec337819efb2f` | COOK |
| 4 | `e02a203b...` arsitek/putusan-lapisan3-H4H5.md | `e02a203b96879d73e90339f2d78a37d15834a23a` | COOK |
| 5 | `ed436fdd...` arsitek/protokol-telaah-fondasi-B.md | `ed436fddf607d3629fa226fd34d20ff60bf47232` | COOK |

Gerbang S0: LULUS 5/5.

Trio-sha JSON beku Batch-2 (verifikasi sebelum dipakai U-2/U-3):

```
$ sha256sum $TEMP/opencode/l3h4h5/sh4_hasil.json
b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588  (cocok spec)
$ sha256sum $TEMP/opencode/l3h4h5/sh5_hasil.json
7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245  (cocok spec)
```

Resep S-H4 (`sh4.py`/`sh5.py` + JSON) hidup di `%TEMP%\opencode\l3h4h5\` (harness Batch-2, luar repo) -
bukan "file tidak ada". Skrip ronde ini (`u1.py`, `u2.py`, `u3.py`) di `%TEMP%\opencode\fondasiB\`.

---

## U-1(b) - Varian EKSKLUSI (5 hari karantina dalam jendela 2024-10-28..2024-11-01)

### Perintah mentah (i): ANOMALY_WINDOWS dari configs/data.yaml

```
$ grep -n anomaly_windows configs/data.yaml
184:  anomaly_windows:
$ sed -n '184,198p' configs/data.yaml
  anomaly_windows:
    - start: "2024-10-28"
      end: "2024-11-01"
      note: >-
        Digit jam mundur 1 jam (buka 00:00) selama lima hari perdagangan,
        lalu kembali normal 4 Nov 2024. Offset jendela ini BELUM
        TERVERIFIKASI; jangan dipakai untuk fitur sesi Tokyo/London/NY
        sebelum sebabnya dikonfirmasi ke Finex.
    - start: "2026-03-10"
      end: "2026-03-27"
      note: >-
        Digit jam mundur 1 jam (buka 00:00) selama empat belas hari
        perdagangan, lalu kembali normal 30 Mar 2026. Offset jendela ini
        BELUM TERVERIFIKASI; jangan dipakai untuk fitur sesi Tokyo/London/NY
        sebelum sebabnya dikonfirmasi ke Finex.
```

### Perintah mentah (iii): sha256 tiap parquet yang dipakai

```
$ sha256sum data/processed/M1/usdjpy_m1_2024.parquet data/processed/M1/usdjpy_m1_2025.parquet data/features/M15/usdjpy_m15_features.parquet data/labels/usdjpy_day_labels.parquet
69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac  data/processed/M1/usdjpy_m1_2024.parquet
fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af  data/processed/M1/usdjpy_m1_2025.parquet
cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb  data/features/M15/usdjpy_m15_features.parquet
47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c  data/labels/usdjpy_day_labels.parquet
```

Keempatnya COOK vs S0 (M1 2024 `69b2c026`, M1 2025 `fce65a3a`, M15 store `cd6a85e4`, D4 `47d15c41`).
Skrip `u1.py` juga meng-assert keempat sha ini sebelum hitung (assert lulus, rc=0).

### Catatan eksekusi (bukan deviasi analitis)

Run-1 pertama GAGAL rc=1, `KeyError: 'date_broker'` pada baris pembacaan D4:
`d4.set_index(pd.to_datetime(d4["date_broker"]))`. Penyebab: parquet D4 menyimpan `date_broker`
SUDAH sebagai index (index name `date_broker`), bukan kolom. Perbaikan murni struktural (baca index
bawaan + `sort_index()`); tidak ada satu pun definisi/angka hitungan yang berubah. Replikasi INKLUSI
tetap dijalankan sebagai gate BLOKIR sebelum varian EKSKLUSI.

### Langkah (1)-(2): bangun ulang pool H4 persis sh4.py + gate INKLUSI (BLOKIR)

Mesin identik S-H4: 6 jam tetap [14, 13, 0, 15, 12, 1] (hasil hitung-ulang M2 Batch-2; daftar jam
TIDAK ditukar - larangan Q4 dua arah berlaku), ATR T-1 (`atr_14_d1.shift(1)`), SL 1x ATR, TP 2x ATR,
biaya by_session (Off -> default 0.65) x pip 0.01, fill exact. Join-gate posisional (n bar + sekuens
`date_broker` + ATR exact `np.allclose(rtol=0, atol=0)`) ikut dijalankan di dalam skrip (assert lulus).

Output mentah gate (run-1, `u1_run1.log`):

```
=== U-1 GATE INKLUSI (BLOKIR) ===
gate_inklusi_lulus: True median: 0.014399999999998407 n_trade: 3114
```

Gate KEWARASAN LULUS digit-per-digit: median pool INKLUSI = `0.014399999999998407` == nilai beku
`sh4_hasil.json` (`b1b69d33...`), n = 3114 == 3114. Varian EKSKLUSI boleh lanjut.

### Langkah (3)-(4): varian EKSKLUSI + perintah mentah (iv)

Prosedur: buang 5 `broker_day` karantina dalam-jendela dari pool M1 P1 DAN pool M15 E1, hitung-ulang
top-6 M2 + n_Off/any_off/mayoritas + median EV pool + median per-tahun + n trade. TANPA eksklusi
buta di luar 19 hari F-1 (hanya window1 2024-10-28..2024-11-01; window2 2026 di luar rentang data).

Output mentah (run-1, identik run-2/run-3):

```
=== PROVENANS karantina dalam-jendela (5 hari) + trade dibuang ===
tanggal_in_window: ['2024-10-28', '2024-10-29', '2024-10-30', '2024-10-31', '2024-11-01']
tanggal_present_in_pool: ['2024-10-28', '2024-10-29', '2024-10-30', '2024-10-31', '2024-11-01']
n_trade_dibuang (harus 30): 30
=== SELISIH digit-per-digit (inklusi vs eksklusi) ===
```

5 tanggal karantina dalam-jendela = persis 2024-10-28 s/d 2024-11-01; kelima-kelima hadir di pool;
cacah trade terbuang = 30 (== teori 5 hari x 6 jam, == counter `n_trade_hari_karantina` Batch-2).

### Tabel selisih digit-per-digit (inklusi vs eksklusi)

| Nilai | INKLUSI | EKSKLUSI | Selisih (eksklusi - inklusi) |
|---|---|---|---|
| median EV pool (JPY) | 0.014399999999998407 | 0.01390000000001023 | -0.0004999999999881766 |
| median EV 2024 (JPY) | 0.04834999999999022 | 0.049399999999994997 | +0.001049999999999776 |
| median EV 2025 (JPY) | -0.005049999999992838 | -0.005049999999992838 | 0 (identik) |
| median 2025 membalik tanda? | (negatif) | (negatif) | TIDAK membalik |
| n_Off (bar top-6 berlabel Off) | 0 | 0 | 0 |
| n_jam_dari_6_dengan_off_apa_saja (any_off) | 0 | 0 | 0 |
| n_jam_dari_6_dengan_off_mayoritas | 0 | 0 | 0 |
| top-6 jam M2 (hitung-ulang) | [14, 13, 0, 15, 12, 1] | [14, 13, 0, 15, 12, 1] | identik |
| n trade pool | 3114 | 3084 | -30 |

### Perintah mentah (ii): git hash-object artefak JSON U-1 (R-4)

```
$ git hash-object $TEMP/opencode/fondasiB/u1_hasil.json
2c76e2d0caeacd80d1003b66da89484cb2cab2f9
$ sha256sum $TEMP/opencode/fondasiB/u1_hasil.json   # run-2
ef3ddd610f457024ccae2443778c65b604119789b2bd47ab6eabcb2b0cd752d6
$ sha256sum $TEMP/opencode/fondasiB/u1_hasil.json   # run-3 (reproducible)
ef3ddd610f457024ccae2443778c65b604119789b2bd47ab6eabcb2b0cd752d6
$ cmp u1_hasil.json u1_hasil_run1.json && echo CMP_IDENTIK
CMP_IDENTIK
```

### Aturan baca TERTUTUP (U-1)

1. Median 2025 TIDAK membalik tanda: -0.005049999999992838 (inklusi) -> -0.005049999999992838
   (eksklusi), identik sampai digit terakhir.
2. Selisih median pool inklusi-vs-eksklusi = -0.0004999999999881766 JPY (eksklusi lebih rendah);
   median 2024 justru naik tipis +0.00105 JPY.
3. n_Off kedua varian = 0. Top-6 kedua varian identik, tanpa penukaran daftar jam.
4. **Vonis H4 TETAP TAHAN** apa pun hasilnya (aturan protokol); hasil ini tidak mengubah vonis apa pun.

---

## U-2 - Dekomposisi biaya H4 + H5

Sumber angka: HANYA dari JSON beku (DILARANG baca EV dari prosa hasil-lapisan3-H4H5 - pelajaran T1):
`sh4_hasil.json` trio-sha `b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588`
(git hash-object `8a5efd0830469f392505448c677677c9a4bb51ac`) dan `sh5_hasil.json` trio-sha
`7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245` (git hash-object
`86a87cd9fa805b80faaa7777e5bb4746739aee05`). Definisi tunggal: EV JPY = exit - entry - cost_jpy;
cost_jpy = cost_basis.by_session (Off -> default 0.65) x pip 0.01; fill exact tanpa slippage.

Cross-check internal (skrip u2): untuk ke-3114 trade, `(exit - entry) - cost_pip*0.01` vs `ev_jpy`
tersimpan => `max_abs_dev = 0.0` (exact, tanpa toleransi).

### H4: urai per sesi (pool 3114 trade, angka penuh dari u2_hasil.json)

| sesi | n | mean kaki bruto (JPY) | median kaki bruto | mean kaki biaya | median kaki biaya | mean EV | median EV | porsi biaya vs mean abs bruto | porsi biaya vs median pool 0.0144 |
|---|---|---|---|---|---|---|---|---|---|
| London | 2076 | 0.01753223919625645 | 0.022999999999996135 | 0.0060999999999999995 | 0.0061 | 0.011432239196256456 | 0.016899999999996133 | 0.015899630145429836 | 0.42361111111115796 |
| NewYork | 300 | 0.008334523809524796 | -0.0024999999999977263 | 0.0069000000000000025 | 0.0069 | 0.0014345238095248155 | -0.009399999999997726 | 0.027008614238143547 | 0.47916666666671986 |
| Tokyo | 738 | 0.017608304297328615 | 0.050499999999999545 | 0.006199999999999997 | 0.0062 | 0.011408304297328635 | 0.04429999999999955 | 0.010226053141365227 | 0.430555555555603 |
| Sydney | 0 | (n=0, tanpa metrik) | - | - | - | - | - | - | - |
| Off | 0 | (n=0, tanpa metrik) | - | - | - | - | - | - | - |
| ALL | 3114 | 0.016664166437287842 | 0.02049999999999841 | 0.00620077071290944 | 0.0061 | 0.010463395724378413 | 0.014399999999998407 | 0.014621990418018331 | 0.4306090772854254 |

mean EV ALL == `mean_ev_jpy_pool` JSON sh4 (0.010463395724378413, assert exact lulus); median EV ALL
== `median_ev_jpy_pool` JSON sh4 (0.014399999999998407, assert exact lulus). Pool H4 hanya berisi
London/Tokyo/NewYork (Sydney dan Off n=0 pada top-6 jam - konsisten n_Off=0).

**Kalimat kuantitatif (aturan baca U-2):** biaya menjelaskan **0.00620077071290944 JPY** dari
**0.42407158913661835 JPY** mean kaki bruto per trade (porsi 0.014621990418018331 = 1.46%);
mean biaya pool = 0.4306090772854254 x median pool +0.0144. Kepala-kepala sesi: porsi terbesar
NewYork 2.70% (mean biaya 0.0069 vs mean abs bruto 0.2555), terkecil Tokyo 1.02%.

### H5: per sel disandingkan (JSON sh5 + lock M4)

Rasio vol/spread kanon M4 VERBATIM dari `reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md:140-141`
(git hash-object `9720280320dcc813d422d6f540e37847b70571ff`, terverifikasi sesi ini):
"London 2,0823 - Tokyo 1,5992 - NewYork 0,9488 - Sydney 0,7975 -> flag 'biaya-mendominasi'
(rasio < 1) = [NewYork, Sydney]".

| sel | cost_basis pip sel | mean_spread_pips_m1_bar_event | rasio vol/spread M4 lock | flag biaya-mendominasi | diff hit-rate [O13] | CI95 [O13] | p | p Holm | threshold Holm | reject Holm | n hari |
|---|---|---|---|---|---|---|---|---|---|---|---|
| London | 0.61 | 0.6251606978879706 | 2.0823 | tidak | -0.0015803147973013076 | [-0.05872659395352819, +0.05636000580219017] | 0.5176 | 0.5176 | 0.005 | False | 110 |
| Tokyo | 0.62 | 0.6606280193236715 | 1.5992 | tidak | +0.015934029831132124 | [-0.04090302527350113, +0.07617016719289924] | 0.291 | 0.291 | 0.0033333333333333335 | False | 92 |
| NewYork | 0.69 | 0.6966417910447761 | 0.9488 | YA (rasio < 1) | -0.03347701149425286 | [-0.12378628342845534, +0.056104743483888206] | 0.7658 | 0.7658 | 0.01 | False | 77 |
| Sydney | 0.80 | 0.8662100456621002 | 0.7975 | YA (rasio < 1) | +0.04325279234100754 | [-0.07630180656343444, +0.16087213041946793] | 0.244 | 0.244 | 0.0025 | False | 46 |

`n_bar_event_tanpa_spread_m1` = 0 pada keempat sel. n_resampel_dipakai = 10000 pada keempat sel.
n_sel_positif_Holm = 0 (verdict S-H5 GUGUR - TIDAK diubah laporan ini). Tanpa statistik keputusan
baru: tidak ada ambang/uji/peringkat sel yang ditambahkan di ronde ini.

Output mentah u2 (run-1, rc=0; run-2/run-3 sha identik):

```
=== U-2 H4: dekomposisi per sesi (dari sh4_hasil.json trio-sha, n=3114) ===
cross-check EV = exit-entry-cost_jpy exact: max_abs_dev = 0.0
sesi       n  mean_bruto   med_bruto  mean_biaya   med_biaya     mean_ev     med_ev  porsi_vs_|bruto|  porsi_vs_0.0144
London       2076 0.0175322392 0.0230000000 0.0061000000 0.0061000000 0.0114322392 0.0169000000     0.0158996301        0.423611
NewYork       300 0.0083345238-0.0025000000 0.0069000000 0.0069000000 0.0014345238-0.0094000000     0.0270086142        0.479167
Tokyo         738 0.0176083043 0.0505000000 0.0062000000 0.0062000000 0.0114083043 0.0443000000     0.0102260531        0.430556
Sydney          0  (n=0, tanpa metrik)
Off             0  (n=0, tanpa metrik)
ALL          3114 0.0166641664 0.0205000000 0.0062007707 0.0061000000 0.0104633957 0.0144000000     0.0146219904        0.430609

Kalimat kuantitatif: biaya menjelaskan 0.0062007707 JPY dari 0.4240715891 JPY kaki bruto per trade (porsi 0.0146219904); mean biaya = 0.430609 x median pool +0.0144.

=== U-2 H5: per sel (JSON sh5 7a7f5ee7 + lock M4 rasio vol/spread) ===
London    cost_pip=0.61 spread_m1=0.6251606979 rasio_M4=2.0823 flag_biaya_mendominasi=False diff=-0.0015803147973013 CI95=[-0.0587265939535282,0.0563600058021902] p=0.5176 p_holm=0.5176 thr_holm=0.0050000000000000 reject=False n_hari=110 resampel=10000
Tokyo     cost_pip=0.62 spread_m1=0.6606280193 rasio_M4=1.5992 flag_biaya_mendominasi=False diff=0.0159340298311321 CI95=[-0.0409030252735011,0.0761701671928992] p=0.2910 p_holm=0.2910 thr_holm=0.0033333333333333 reject=False n_hari=92 resampel=10000
NewYork   cost_pip=0.69 spread_m1=0.6966417910 rasio_M4=0.9488 flag_biaya_mendominasi=True diff=-0.0334770114942529 CI95=[-0.1237862834284553,0.0561047434838882] p=0.7658 p_holm=0.7658 thr_holm=0.0100000000000000 reject=False n_hari=77 resampel=10000
Sydney    cost_pip=0.80 spread_m1=0.8662100457 rasio_M4=0.7975 flag_biaya_mendominasi=True diff=0.0432527923410075 CI95=[-0.0763018065634344,0.1608721304194679] p=0.2440 p_holm=0.2440 thr_holm=0.0025000000000000 reject=False n_hari=46 resampel=10000
n_sel_positif_holm = 0 (verdict S-H5 GUGUR)
```

### Aturan baca TERTUTUP (U-2)

1. Kuantifikasi headwind biaya, BUKAN jalur penyelamatan. Angka di atas memperkirakan besaran
   kepala-kepala biaya; tidak ada satu pun angka yang "menyelamatkan" H4/H5.
2. Keluaran ronde ini = tabel per-nilai + kalimat kuantitatif ("biaya menjelaskan 0.0062007707
   JPY dari 0.4240715891 JPY mean kaki bruto per trade, porsi 1.46%"). BUKAN rekomendasi mengubah
   biaya: `cost_basis.by_session` BEKU (S-B.8) - tidak diusulkan sentuh.
3. Gap Holm H5 TIDAK bisa ditutup biaya: selisih hit-rate per sel orde 0.016-0.043 dengan CI95
   melebar orde 0.06-0.12, sedangkan headwind biaya per bar event orde 0.61-0.80 pip vs mean spread
   0.63-0.87 pip - biaya menjelaskan sebagian kecil kaki bruto (1.0-2.7% per sesi), bukan orde
   magnitudo gap Holm (p terkecil 0.244 vs threshold 0.0025). P-5 (temuan negatif berkekuatan
   penuh) mengikat.
4. Vonis S-H5 GUGUR dan S-H4 TAHAN TIDAK diubah.

---

## U-3 - Cek regime deskriptif 2024 vs 2025

Sumber: M1 2024/2025 (kolom `spread_pips` beku, sha S0 cocok), M15 store (kolom `rv_roll_20d`
beku, sha S0 cocok), n trade + split tanda dari `sh4_hasil.json` beku (bukan prosa). Grain RV =
`date_broker` kolom store (`dt.year`); `utc.normalize()` TIDAK dipakai (S-B.12). TANPA
rv_regime_flag/rv_score/TAU sebagai filter; TANPA kalibrasi ambang; TANPA menulis store (skrip
hanya `read_parquet` + agregasi memori).

### Tabel per-nilai (angka penuh dari u3_hasil.json)

| Metrik | 2024 | 2025 | Selisih 2025-2024 |
|---|---|---|---|
| n bar M1 | 358331 | 356977 | -1354 |
| mean spread_pips (M1) | 0.7027441108981426 | 0.6735394717369292 | -0.029204639161213408 |
| median spread_pips (M1) | 0.6 | 0.6 | 0 |
| p95 spread_pips (M1) | 1.2000000000000002 | 1.0000000000000002 | -0.19999999999999996 |
| max spread_pips (M1) | 55.60000000000001 | 24.100000000000005 | -31.500000000000007 |
| n bar M15 (store) | 23909 | 23812 | -97 |
| n hari date_broker (store) | 260 | 259 | -1 |
| mean rv_roll_20d | 0.0008842739404643567 | 0.0007716445087086217 | -0.00011262943175573505 |
| median rv_roll_20d | 0.0007630109711974819 | 0.0006858614601473814 | -7.714951105060048e-05 |
| p95 rv_roll_20d | 0.0024729367446753774 | 0.0018341539103849294 | -0.000638782834290448 |
| n trade pool H4 | 1560 | 1554 | -6 |
| median EV H4 (JPY) | +0.04834999999999022 | -0.005049999999992838 | -0.05339999999999831 |
| mean EV H4 (JPY) | +0.024799771062270975 | -0.0039283324140465484 | -0.028728103476317523 |

Output mentah u3 (run-1, rc=0; run-2/run-3 sha identik):

```
=== U-3: regime deskriptif 2024 vs 2025 (data beku) ===
[sha256 M1]  {2024: '69b2c026d3ac52d4...', 2025: 'fce65a3a1fa71573...'} cocok S0
[sha256 M15] cd6a85e472dec353... cocok S0

-- M1 spread_pips (per file tahun; tanpa utc.normalize) --
2024: n_bar=358331 mean=0.7027441109 median=0.6000000000 p95=1.2000000000 max=55.6000000000
2025: n_bar=356977 mean=0.6735394717 median=0.6000000000 p95=1.0000000000 max=24.1000000000

-- M15 store rv_roll_20d (grain date_broker kolom beku) --
2024: n_bar_m15=23909 n_hari=260 mean=0.0008842739 median=0.0007630110 p95=0.0024729367 min=0.0002020620 max=0.0027097749
2025: n_bar_m15=23812 n_hari=259 mean=0.0007716444 median=0.0006858615 p95=0.0018341539 min=0.0003511855 max=0.0021035214

-- H4 split tanda (sh4_hasil.json beku) --
2024: n_trade=1560 median_ev_jpy=0.04834999999999022 mean_ev_jpy=0.024799771062270975
2025: n_trade=1554 median_ev_jpy=-0.005049999999992838 mean_ev_jpy=-0.0039283324140465484

selisih 2025-2024: mean_spread=-0.029204639161213408 p95_spread=-0.19999999999999996 mean_rv=-0.00011262943175573505 median_rv=-7.714951105060048e-05
```

Acuan metodologis (report.md:43): H1-2023 (B) spread p95 5,30 vs H2-2023 (A) 0,60 = 5,3x - kontras
antar-periode besar; pada M1 2024-vs-2025 kontras jauh lebih kecil (p95 1.2 vs 1.0).

### Aturan baca TERTUTUP (U-3) - SATU kalimat

**Bertepatan.** Secara deskriptif, pembalikan tanda median EV H4 (2024 +0.04835 -> 2025 -0.00505)
bertepatan dengan level RV yang lebih rendah pada 2025 (mean rv_roll_20d -12.7%, median -10.1%,
p95 -25.8% vs 2024) disertai spread yang juga lebih rendah (mean -4.2%, p95 -17%). Kalimat ini
murni deskriptif: tanpa konsekuensi keputusan, tanpa filter, tanpa ambang; **Vonis H4 TETAP TAHAN.**

---

## R-4 - Daftar hash artefak JSON ronde ini (wajib sebelum dibaca arsitek)

| Artefak | sha256 | git hash-object | Deterministik? |
|---|---|---|---|
| `%TEMP%\opencode\fondasiB\u1_hasil.json` | `ef3ddd610f457024ccae2443778c65b604119789b2bd47ab6eabcb2b0cd752d6` | `2c76e2d0caeacd80d1003b66da89484cb2cab2f9` | ya (run-2 == run-3, cmp IDENTIK) |
| `%TEMP%\opencode\fondasiB\u2_hasil.json` | `cf4cd14fe125fa56ee593d7334fd46bfa1c2291ac44733e8c85ff6bc91793400` | `ac9eed2947078cc406da008dd1c939a7dcaf70fc` | ya (run-2 == run-3, cmp IDENTIK) |
| `%TEMP%\opencode\fondasiB\u3_hasil.json` | `2f12fb5c219404128df2c1f21eddb394bfe9669d8ee89121755f3ab081920052` | `2ced2c88bd05d4f313b960fcf29f20b97b2b20e4` | ya (run-2 == run-3, cmp IDENTIK) |
| `%TEMP%\opencode\l3h4h5\sh4_hasil.json` (beku, dirujuk) | `b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588` | `8a5efd0830469f392505448c677677c9a4bb51ac` | beku Batch-2 |
| `%TEMP%\opencode\l3h4h5\sh5_hasil.json` (beku, dirujuk) | `7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245` | `86a87cd9fa805b80faaa7777e5bb4746739aee05` | beku Batch-2 |

Perintah mentah (ii) gabungan:

```
$ git hash-object $TEMP/opencode/l3h4h5/sh4_hasil.json $TEMP/opencode/l3h4h5/sh5_hasil.json $TEMP/opencode/fondasiB/u1_hasil.json $TEMP/opencode/fondasiB/u2_hasil.json $TEMP/opencode/fondasiB/u3_hasil.json
8a5efd0830469f392505448c677677c9a4bb51ac
86a87cd9fa805b80faaa7777e5bb4746739aee05
2c76e2d0caeacd80d1003b66da89484cb2cab2f9
ac9eed2947078cc406da008dd1c939a7dcaf70fc
2ced2c88bd05d4f313b960fcf29f20b97b2b20e4
```

---

## Ringkasan kepatuhan protokol

| Aturan protokol | Status |
|---|---|
| S0 ukur ulang sendiri (bukan salin) | dipatuhi (5/5 COOK, output mentah di atas) |
| U-1 gate INKLUSI BLOKIR digit-per-digit | dipatuhi; LULUS, EKSKLUSI lanjut |
| U-1 tanpa eksklusi buta di luar 19 hari F-1 | dipatuhi; hanya window1 (2024-10-28..2024-11-01) |
| U-1 larangan tukar daftar jam (Q4 dua arah) | dipatuhi; top-6 kedua varian [14,13,0,15,12,1] |
| U-1 Vonis H4 TETAP TAHAN | ditegaskan 2x (U-1 dan U-3) |
| U-2 hanya dari JSON beku trio-sha (bukan prosa) | dipatuhi; sha diverifikasi sebelum baca |
| U-2 tanpa statistik keputusan baru | dipatuhi; nol ambang/uji/peringkat baru |
| U-2 by_session beku (S-B.8), tanpa rekomendasi ubah biaya | dipatuhi |
| U-3 grain date_broker store; utc.normalize DILARANG | dipatuhi |
| U-3 tanpa filter rv_regime_flag/rv_score/TAU, tanpa kalibrasi ambang, tanpa tulis store | dipatuhi |
| R-4 semua JSON ronde ini ter-hash | dipatuhi (tabel R-4) |
| File sementara hanya %TEMP%\opencode\fondasiB | dipatuhi |
| Nol tulis repo kecuali laporan ini; staged=2 pihak lain tidak disentuh | dipatuhi |
| DILARANG commit/push, merumuskan H6, mengubah vonis H1-H5 | dipatuhi |

---

=== SELF-AUDIT 3x ADVERSARIAL ===

Putaran 1 - Correctness:
(a) Gate INKLUSI dibandingkan digit-per-digit terhadap literal protokol (0.014399999999998407) DAN
terhadap JSON sh4 beku; keduanya identik, n=3114 identik - replikasi mesin sh4 valid.
(b) Cross-check definisi tunggal EV: `(exit-entry) - cost_pip*0.01` vs `ev_jpy` tersimpan, exact
(max_abs_dev = 0.0) untuk 3114 trade; mean/median EV ALL di-assert == field JSON sh4 (exact).
(c) n_trade_dibuang = 30 cocok teori 5 hari x 6 jam; 5 tanggal persis jendela window1; kelima
tanggal hadir di pool (bukan asumsi).
(d) Run-1 awal u1 GAGAL (KeyError `date_broker`); akar penyebab = parquet D4 menyimpan kolom itu
sebagai index. Perbaikan struktural murni (baca index bawaan); tidak ada definisi/paramater/angka
yang diubah; gate blokir tetap dijalankan dan LULUS pada run perbaikan.
(e) Reproduksi: ketiga JSON ditulis ulang oleh run terpisah dan sha256 identik (cmp IDENTIK) -
tidak ada RNG tak terkendali (U-1/U-2/U-3 deterministik; U-5 bootstrap Batch-2 tidak diulang di sini).
(f) porsi biaya memakai mean(|kaki bruto|) sesuai definisi protokol; kaki bruto bisa negatif per
trade sehingga nilai |bruto| > nilai bruto - dilaporkan apa adanya (mean abs 0.424 vs mean bruto
0.0167).

Putaran 2 - Bias & Asumsi:
(a) Risiko narrative bias pada U-3: kalimat "bertepatan" dipilih SETELAH angka dilihat. Mitigasi:
protokol hanya mengizinkan dua kalimat eksklusif; angka lengkap (yang tak menguntungkan narasi
mana pun - spread 2025 LEBIH RENDAH, bukan lebih tinggi) ditempel utuh; tanpa konsekuensi keputusan.
(b) U-2 dijalankan tanpa peringkat sel/ambang baru; kepala-kepala biaya dilaporkan apa adanya
termasuk fakta bahwa Sydney/Off n=0 di pool H4 (tabel lengkap, bukan hanya sel "menarik").
(c) Eksklusi U-1 terbatas persis 5 hari dalam jendela (bukan 19 hari F-1 yang tidak diverifikasi);
tidak ada tuning parameter lain yang "kebetulan" menguntungkan.
(d) Tidak ada bacaan EV dari prosa hasil-H4H5 (T1 dicegah berulang); semua angka U-2/U-3 dari
JSON/parquet beku dengan sha diverifikasi lebih dulu.
(e) Asumsi grain M1 per tahun = partisi file (bukan rekonstruksi tanggal) - diungkap eksplisit;
tanpa utc.normalize() di mana pun.

Putaran 3 - Meta-check:
(a) Setiap klaim numerik di laporan ini punya pasangan output mentah yang ditempel; klaim tanpa
bukti = tidak ada.
(b) R-4 dipenuhi: 5 JSON (3 ronde ini + 2 beku dirujuk) ter-hash git + sha256, determinisme dibuktikan
dengan run terpisah + cmp.
(c) Disiplin worktree: git status sebelum & sesudah identik kecuali file laporan ini; staged=2
pihak lain tidak disentuh; nol commit.
(d) Ruang lingkup: nol usulan H6, nol perubahan vonis H1-H5, nol perubahan kode repo; perbaikan u1.py
hidup di temp, bukan di repo.
(e) Kejujuran keterbatasan: resep Batch-2 tetap di %TEMP% (risiko rantai-bukti bila temp terhapus -
dicatat sesuai brief); run-1 pertama u1 gagal dan diperbaiki - riwayat penuh dilaporkan, tidak
disembunyikan.

=== STOP ===

Laporan berhenti di sini. Vonis H4 TAHAN, H5 GUGUR, dan seluruh vonis H1-H5 lainnya TIDAK diubah.
Putusan tetap wewenang arsitek pasca re-audit.
