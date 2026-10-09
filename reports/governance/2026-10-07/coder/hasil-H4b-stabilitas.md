# Hasil Eksekusi H4b -- Stabilitas Lintas-Tahun (Coder)

- Peran: CODER (.ai/AGENTS.md v3.0 pasal 26) - implementasi + self-audit. Bukan penentu arsitek, bukan auditor.
- Instruksi tunggal: reports/governance/2026-10-07/arsitek/spesifikasi-H4b-stabilitas.md
  (blob `0437b563c85e578567eb58b8cfe6b0dd3ef02b47`, dibaca utuh sesi ini; spec PRA-REGISTRASI).
- Tanggal eksekusi: 2026-10-09. Branch `codex/ANN`, HEAD saat eksekusi
  `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
- Interpreter kanonik: `venv/Scripts/python.exe` (Python 3.12.8, pandas 2.2.3, numpy 1.26.4,
  scipy 1.17.1). **Seed/toolchain: TANPA RNG - deterministik penuh** (seed tidak berlaku;
  tidak ada bootstrap/sampling di ronde ini).
- File sementara: HANYA `%TEMP%\opencode\h4b\`. Nol tulis repo kecuali satu file laporan ini.
- Nol commit/push. Bukan vonis ulang: vonis H4 TAHAN Batch-2 tak tersentuh. Tanpa H6.
- Dokumen ronde ini memakai pengikatan eksternal (P-4/T2): TANPA self-hash di dalam dokumen;
  hash dokumen dilaporkan di kanal luar (chat).

Staged saat eksekusi = 2 berkas T6 (`A src/features/build_labels.py`, `A tests/test_build_labels.py`)
- TIDAK disentuh, TIDAK di-unstage. Worktree cabang `codex/ANN` berisi status worktree-pihak-lain
(berkas modified/untracked milik sesi lain) - tidak disentuh.

---

## S0 - Gerbang hash (ukur ulang sesi coder)

Perintah mentah:

```
$ git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-H4b-stabilitas.md reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md reports/governance/2026-10-07/Audit/reaudit-lapisan3-H4H5.md reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md
0437b563c85e578567eb58b8cfe6b0dd3ef02b47
4a46b815211e6b0b050cbb6f3e98ce5e27904069
f06a8e27b916172f5824438acd545614360d3b57
8a4d21090f27dd53555b3a12583ec337819efb2f
e02a203b96879d73e90339f2d78a37d15834a23a
$ git rev-parse HEAD
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
$ git status --porcelain | grep -c "^[AMDR]"
2
```

Tabel Klaim & Bukti (S0):

| # | Klaim (brief/spec) | Ukur sesi coder | Status |
|---|---|---|---|
| 1 | spec H4b `0437b563...` | `0437b563c85e578567eb58b8cfe6b0dd3ef02b47` | COOK |
| 2 | spec Batch-2 `4a46b815...` | `4a46b815211e6b0b050cbb6f3e98ce5e27904069` | COOK |
| 3 | hasil Batch-2 `f06a8e27...` | `f06a8e27b916172f5824438acd545614360d3b57` | COOK |
| 4 | reaudit Batch-2 `8a4d2109...` | `8a4d21090f27dd53555b3a12583ec337819efb2f` | COOK |
| 5 | putusan Batch-2 `e02a203b...` | `e02a203b96879d73e90339f2d78a37d15834a23a` | COOK |
| 6 | HEAD | `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` | COOK |

Gerbang S0: LULUS 6/6. Staged = 2 T6 (sesuai syarat; != 2 akan STOP sebelum hitung).

## SHA input beku (assert sebelum hitung; mismatch = STOP)

Perintah mentah:

```
$ sha256sum data/processed/M1/usdjpy_m1_2024.parquet data/processed/M1/usdjpy_m1_2025.parquet data/features/M15/usdjpy_m15_features.parquet data/labels/usdjpy_day_labels.parquet
69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac *data/processed/M1/usdjpy_m1_2024.parquet
fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af *data/processed/M1/usdjpy_m1_2025.parquet
cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb *data/features/M15/usdjpy_m15_features.parquet
47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c *data/labels/usdjpy_day_labels.parquet
```

Keempatnya COOK vs spec; keempatnya di-assert di dalam `h4b.py` sebelum hitung (assert lulus,
rc=0). Data 2026 TIDAK dipakai.

## Mesin + gate anti-intip

Mesin diadaptasi 1:1 dari sh4.py Batch-2 (jalur u1.py fondasi-B): ATR T-1
(`daily_metrics(...).shift(1)`, gate `np.allclose(rtol=0, atol=0)` vs kolom store lulus), SL 1x ATR,
TP 2x ATR, exit scan SL dulu > TP > time-stop close terakhir hari, biaya by_session
(Off -> default 0.65) x pip 0.01, fill exact, join-gate posisional (n bar + sekuens `date_broker`
identik, assert lulus). Konstanta tak diubah: pip 0.01, by_session London 0.61 / NewYork 0.69 /
Tokyo 0.62 / Sydney 0.80, default 0.65, fingerprint sesi src + _eda_common assert lulus.

Gate anti-intip (3 lapis, semuanya assert BLOKIR di skrip):
1. Pool M2 train tahun-train SAJA (assert `set(tahun) == {train_year}`);
   pool E1 uji tahun-uji SAJA (assert `set(tahun) == {test_year}`).
2. Daftar 6 jam dikunci sebagai tuple sebelum loop uji; loop entry `for hh in hours` memakai
   HANYA daftar terkunci.
3. Pasca-loop: assert semua trade berasal dari jam terkunci DAN ranking train dihitung ulang
   identik (daftar tak berubah tersentuh data uji). Keempat assert lulus di kedua arah
   (`gate_anti_intip: LULUS`).

## Output mentah arah MAJU (train 2024 -> uji 2025)

```
=== H4b MAJU (train 2024 -> uji 2025) ===
top6_jam_train_terkunci: [14, 13, 12, 0, 15, 7]
gate_anti_intip: LULUS
n_trade: 1554 | exit: {'SL': 71, 'TP': 6, 'time_stop': 1477}
n_Off_di_top6_bars_uji: 0 | any_off: 0 | maj_off: 0
per_jam (off/n): {'14': '0/15539', '13': '0/15537', '12': '0/15535', '0': '0/15534', '15': '0/15538', '7': '0/15535'}
median_ev_jpy: -0.005049999999992838 | mean: -0.0039283324140465484 | fraksi_positif: 0.49356499356499356
karantina_F1 n_trade (deskriptif): 0
lock per arah: {'kriteria_a_n_Off_le_1': True, 'kriteria_b_median_ev_gt_0': False, 'lolos_arah': False}
```

## Output mentah arah MUNDUR (train 2025 -> uji 2024)

```
=== H4b MUNDUR (train 2025 -> uji 2024) ===
top6_jam_train_terkunci: [14, 13, 0, 15, 1, 12]
gate_anti_intip: LULUS
n_trade: 1560 | exit: {'SL': 94, 'TP': 12, 'time_stop': 1454}
n_Off_di_top6_bars_uji: 0 | any_off: 0 | maj_off: 0
per_jam (off/n): {'14': '0/15595', '13': '0/15593', '0': '0/15599', '15': '0/15600', '1': '0/15600', '12': '0/15598'}
median_ev_jpy: 0.05439999999999045 | mean: 0.028821062271061976 | fraksi_positif: 0.5551282051282052
karantina_F1 n_trade (deskriptif): 30
lock per arah: {'kriteria_a_n_Off_le_1': True, 'kriteria_b_median_ev_gt_0': True, 'lolos_arah': True}
```

## Kedua top-6 + selisih

```
=== SELISIH top-6 (simetris) maju vs mundur ===
maju : [14, 13, 12, 0, 15, 7]
mundur: [14, 13, 0, 15, 1, 12]
jam_hanya_di_satu_sisi: [1, 7]
```

| Arah | Daftar top-6 train (terkunci) | Set jam |
|---|---|---|
| Maju (train 2024) | [14, 13, 12, 0, 15, 7] | {0, 7, 12, 13, 14, 15} |
| Mundur (train 2025) | [14, 13, 0, 15, 1, 12] | {0, 1, 12, 13, 14, 15} |
| Selisih simetris | - | {1, 7}: jam 7 hanya di Maju; jam 1 hanya di Mundur |

5 dari 6 jam identik antar tahun; satu jam bertukar (7 vs 1). n_Off/any_off/mayoritas = 0/0/0
pada kedua arah (definisi Off beku P1: bar pool M1 tahun-uji pada 6 jam terkunci ber-label Off;
per-jam rincian off/n di atas, semua 0).

## Karantina F-1 (counter deskriptif, varian default INKLUSI)

| Arah | n_trade pada 5 hari 2024-10-28..2024-11-01 | Catatan |
|---|---|---|
| Maju (uji 2025) | 0 | wajar: tanggal karantina di 2024, di luar pool uji |
| Mundur (uji 2024) | 30 | 5 hari x 6 jam terkunci, konsisten counter Batch-2 |

Tanpa eksklusi buta di luar 19 hari F-1; tidak ada eksklusi sama sekali (INKLUSI).

## Aturan baca TERTUTUP - vonis

Lock H4b verbatim: GUGUR bila pada SATU PUN tahun-uji (a) >= 2 dari 6 jam-teratas-train jatuh di
Off, ATAU (b) median EV-after-cost pool tahun-uji <= 0. TAHAN hanya bila KEDUA arah: n_Off <= 1
DAN median EV > 0.

Penerapan pada angka (tabel di atas):

| Arah | kriteria (a) n_Off <= 1 | kriteria (b) median EV > 0 | Lolos arah? |
|---|---|---|---|
| Maju (uji 2025) | LULUS (n_Off = 0) | GAGAL (median = -0.005049999999992838 <= 0) | TIDAK |
| Mundur (uji 2024) | LULUS (n_Off = 0) | LULUS (median = +0.05439999999999045 > 0) | YA |

**VONIS: GUGUR(H4b).** Arah Maju memenuhi syarat gugur (b); satu arah gagal cukup bagi lock
("GUGUR bila pada SATU PUN tahun-uji"). Tepat satu vonis; tanpa statistik tambahan; tanpa filter
regime; tanpa kalibrasi; tanpa H6.

Makna vonis (mengikat interpretasi spec): efek H4 TIDAK stabil antar-tahun pada data beku
2024-2025 - vonis tegas dan FINAL atas H4b. **DILARANG merembet ke vonis H4**: TAHAN(H4 Batch-2)
tetap berdiri; GUGUR(H4b) adalah temuan stabilitas lintas-tahun, bukan vonis ulang H4. Keterbatasan
spec tetap tercatat: pertanyaan termotivasi EKS-3 sehingga bobot konfirmatorinya terbatas.

Catatan konsistensi (provenance, bukan statistik baru): pool uji 2025 arah Maju memakai SET jam
{0,7,12,13,14,15} - identik sebagai SET dengan 6 jam E1 Batch-2 (daftar lock P0 [14,13,0,15,12,7];
ranking M2 Batch-2 hanya laporan DEV-B2-1, E1 memakai lock list). n/median/mean/fraksi 2025
angka-angka persis cocok dengan per_tahun 2025 JSON sh4 beku (`b1b69d33...`) - cross-validasi
deterministik, bukan duplikasi perhitungan keliru. Diagnostik terpisah (jam 1 vs jam 7 di 2025
dihitung sendiri: mean +0.001549 vs +0.000740) mengonfirmasi pool Mundur (dengan jam 1) berbeda
nyata dari pool Maju.

## R-4 - Artefak JSON (pola R-4)

| Artefak | sha256 | git hash-object | Deterministik? |
|---|---|---|---|
| `%TEMP%\opencode\h4b\h4b_maju.json` | `799c9e0197483fb33e072143fd6f779a1599a1bde41ae89a9dfbbfdc62722d5d` | `7975db73490d787132ac60ff5ec0cf3db6fd416c` | ya (run-2 == run-3, cmp IDENTIK) |
| `%TEMP%\opencode\h4b\h4b_mundur.json` | `ca40d32655583ccdf61f1d2b83af0df87c297e9831b5f0a7d4258ac3798ee86d` | `138d902531866771e0607895e90ec1f8b9c61a8b` | ya (run-2 == run-3, cmp IDENTIK) |

```
$ sha256sum h4b_maju.json h4b_mundur.json   # run-2
799c9e0197483fb33e072143fd6f779a1599a1bde41ae89a9dfbbfdc62722d5d  h4b_maju.json
ca40d32655583ccdf61f1d2b83af0df87c297e9831b5f0a7d4258ac3798ee86d  h4b_mundur.json
$ sha256sum h4b_maju.json h4b_mundur.json   # run-3 (reproducible)
799c9e0197483fb33e072143fd6f779a1599a1bde41ae89a9dfbbfdc62722d5d  h4b_maju.json
ca40d32655583ccdf61f1d2b83af0df87c297e9831b5f0a7d4258ac3798ee86d  h4b_mundur.json
$ cmp ... && echo CMP_IDENTIK_KEDUA
CMP_IDENTIK_KEDUA
$ git hash-object h4b_maju.json h4b_mundur.json
7975db73490d787132ac60ff5ec0cf3db6fd416c
138d902531866771e0607895e90ec1f8b9c61a8b
```

## Ringkasan kepatuhan spec

| Aturan spec | Status |
|---|---|
| S0 6 hash diukur ulang sesi coder; mismatch = STOP | dipatuhi (6/6 COOK) |
| SHA 4 input diverifikasi + assert sebelum hitung | dipatuhi |
| Resep sh4 konstanta tak diubah; join-gate posisional | dipatuhi (assert lulus) |
| Data 2026 DILARANG | dipatuhi (tak dipakai) |
| Dua arah anti-intip + gate assert blokir | dipatuhi (3 lapis, lulus) |
| Karantina F-1 counter deskriptif per arah; INKLUSI default | dipatuhi (0 dan 30) |
| Determinisme coder 2x sha identik | dipatuhi (cmp IDENTIK kedua artefak) |
| Artefak per arah + git hash-object ditempel | dipatuhi |
| Tepat satu vonis; GUGUR tak merembet ke H4 | dipatuhi |
| Tanpa statistik tambahan / filter regime / kalibrasi / H6 | dipatuhi |
| Nol tulis repo lain; nol commit; staged T6 tak tersentuh | dipatuhi |
| TANPA self-hash di dokumen (pengikatan eksternal) | dipatuhi |

---

=== SELF-AUDIT 3x ADVERSARIAL ===

Putaran 1 - Correctness:
(a) Gate anti-intip 3 lapis di-assert di skrip (pool train/uji murni per tahun; loop memakai
tuple terkunci; pasca-loop semua trade di jam terkunci + ranking train identik ulang). Kedua arah
LULUS; skrip gagal otomatis bila bocor.
(b) Keanehan awal diselidiki, bukan diabaikan: median/mean/fraksi uji 2025 arah Maju IDENTIK
digit-per-digit dengan per_tahun 2025 Batch-2 padahal peringkat top-6 berbeda. Diagnosis: SET jam
Maju {0,7,12,13,14,15} = SET 6 jam E1 Batch-2 (lock P0); EV pool hanya bergantung set, bukan
urutan - jadi kecocokan = cross-validasi beku yang benar, bukan bug. Diagnostik terpisah jam 1
(mean +0.0015487589630449469) vs jam 7 (+0.000740154440155222) pada 2025 mengonfirmasi pool
Mundur benar-benar berbeda dari pool Maju (median Mundur +0.0544 berbeda dari Maju -0.00505 -
sesuai harapan set jam berbeda).
(c) Mesin identik Batch-2 pada jalur yang sama (u1.py/sh4): ATR T-1 gate allclose lulus,
join-gate posisional lulus, exit-cause konsisten (SL+TP+time_stop = n_trade di kedua arah:
71+6+1477 = 1554; 94+12+1454 = 1560).
(d) Counter karantina: Maju 0 (benar - tahun uji 2025), Mundur 30 (5 hari x 6 jam - konsisten
counter Batch-2). n trade uji: 1554 = 259 hari x 6 jam; 1560 = 260 hari x 6 jam - sesuai jumlah
hari per tahun store.
(e) Reproduksi: kedua artefak ditulis ulang run terpisah, sha256 identik, cmp IDENTIK; stdout
run-2 == run-1 (diff bersih).

Putaran 2 - Bias & Asumsi:
(a) Risiko "p-hacking dua arah": desain dua arah PRA-REGISTRASI sebelum angka dilihat; vonis
mekanis dari lock verbatim (skrip mencetak VONIS_H4B mengikuti aturan, laporan hanya menerapkan
tabel). Tidak ada pemilihan arah/daftar jam/estimasi apapun oleh coder.
(b) Risiko merembet ke H4: laporan membatasi makna GUGUR(H4b) pada stabilitas lintas-tahun
saja, menegaskan TAHAN(H4) Batch-2 tak tersentuh - sesuai spec, dua kali ditegaskan.
(c) Asumsi terungkap: "jatuh di Off" dievaluasi pada pool M1 tahun-uji (definisi Off beku P1 =
bar session_label "Off" pada jam terkunci) - konsisten Batch-2; rincian per-jam off/n ditempel
sehingga auditor dapat menghitung ulang.
(d) Tidak ada pembacaan angka dari prosa; semua dari JSON/parquet beku + skrip yang hash-nya
ditempel. Debug diagnostik (jam 1 vs 7) skrip terpisah di temp, bukan bagian artefak spec, dan
hanya dipakai untuk menjelaskan kecocokan - tanpa pengaruh apa pun pada vonis.

Putaran 3 - Meta-check:
(a) Setiap klaim angka punya output mentah ditempel (S5): S0, SHA input, kedua arah, selisih
top-6, karantina, artefak. Klaim tanpa bukti = tidak ada.
(b) Ruang lingkup: 1 file laporan di repo (belum ada perubahan lain); skrip hanya %TEMP%;
nol commit; staged 2 T6 tidak disentuh; vonis H1-H5 tidak diubah; tanpa H6.
(c) Pengikatan eksternal: dokumen TANPA self-hash sesuai spec; blob dokumen dilaporkan di chat.
(d) Keterbatasan jujur: resep Batch-2 + artefak H4b hidup di %TEMP% (risiko bila temp terhapus
- sudah dicatat berulang); replikasi independen auditor dari nol adalah pemeriksaan lanjutan yang
belum bisa coder klaim.

=== STOP ===

Laporan berhenti di sini. Vonis ronde ini: GUGUR(H4b) - final atas H4b; tidak merembet ke H4.
Putusan resmi tetap wewenang arsitek.
