# Re-audit R-2 -- Stratifikasi Tahun H4 (2024 vs 2025, jam-tetap lock)

**Peran penulis:** Auditor (AGENTS.md S26: audit formal; DILARANG menulis
kode produksi/data/config; DILARANG menentukan arsitektur; DILARANG vonis
H4/H5). **Status:** RE-AUDIT SELESAI. **Tanggal audit:** 2026-10-09.
**Spec:** `reports/governance/2026-10-07/arsitek/spesifikasi-R2-stratifikasi.md`
(blob `c04199cea2acfd692b731fcb7eacec16b0e4691d`).
**Dokumen yang diaudit:** `reports/governance/2026-10-07/coder/hasil-R2-stratifikasi.md`
(blob `c2f799138593e7ea1a8f2da6901c9f818e60b731`).
**Harness yang diaudit:** `%TEMP%/opencode/r2/r2.py`.

**PUTUSAN AUDIT (satu): GAGAL.** Alasannya TUNGGAL: gate lock jam R-2 yang
diwajibkan spec baris 92-93 tidak diimplementasikan sebagai gate (temuan
T-1, severity HIGH, eskalasi arsitek). Semua angka penentu, semua
perhitungan F-1/n_Off/2026, dan verdict mekanis `GUGUR(R-2)` sendiri
auditor verifikasi **benar** (A1 replikasi dari nol + A6 re-run penuh
byte-identik). Tidak ada angka yang salah dan tidak ada intip data pada
eksekusi aktual.

---

## 1. S-0. Gerbang sesi (9/9 COCOK + HEAD + staged 2)

```
c04199cea2acfd692b731fcb7eacec16b0e4691d  spesifikasi-R2-stratifikasi.md   (target)
c2f799138593e7ea1a8f2da6901c9f818e60b731  hasil-R2-stratifikasi.md          (target)
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec-B2
f06a8e27b916172f5824438acd545614360d3b57  hasil-B2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit-B2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan-B2 (H4 TAHAN FINAL)
ed436fddf607d3629fa226fd34d20ff60bf47232  protokol-B
0284f5f022ce1c147cefef6dd7780aded6acf820  hasil-B
7d125022cd14113325e5c5721da53a39be661f5c  disposisi-B (D-1--D-4)
fe11383b9bdd1e58819e32812eec75c52ab3aee9  putusan-H4b (GUGUR)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD
```

```
git rev-parse HEAD              -> e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  COCOK
git rev-parse --abbrev-ref HEAD -> codex/ANN                                  COCOK
git diff --cached --name-only   -> src/features/build_labels.py
                                   tests/test_build_labels.py  (tepat 2 T6) COCOK
blob staged build_labels.py     -> 2561efd552544feeb9af0b6733711015b83f43dd  COCOK
blob staged test_build_labels.py-> dc07a7e651d38f07a5cabbe4e693b10681312d25  COCOK
```

S-0 LOLOS. Tidak ada mismatch, tidak ada commit/push/stash/checkout oleh
sesi audit. Semua probe auditor di `%TEMP%/opencode/r2_audit/`.

---

## 2. Ringkasan temuan

| ID | Severity | Area | Ringkas |
|---|---|---|---|
| T-1 | **HIGH** | A2 | Gate "loop entry HANYA FIXED_HOURS" tidak ada; assert yang ada hanya membandingkan dua konstanta. Mutasi loop dan top-6 data-driven lolos `rc=0`. **Eskalasi arsitek.** |
| T-2 | LOW | A5 | Klaim "tiga rekaman sepakat" di `hasil-R2-stratifikasi.md:205-207` bukan tiga pembuktian independen (satu mesin, partisi aritmetik dari 3114 trade yang sama). |
| T-3 | LOW | A4 | `daily_metrics` menghitung 196 hari bertanggal 2026 sebagai between-state. Nol kontribusi ke angka mana pun (dibuktikan bit-identik), tetapi teks spec "2026 dikecualikan PENUH" perlu diklarifikasi. |
| T-4 | LOW | A7 | Baris tabel `hasil-R2-stratifikasi.md:201` melabeli "Vonis H4/H5 di dokumen ini" sebagai `BELUM DIVERIFIKASI`; auditor memverifikasi bahwa vonis itu memang tidak ada. |

Tidak ada temuan yang mengubah angka penentu atau verdict mekanis.

---

## 3. A1. Replikasi independen dari nol (COCOK, digit-per-digit)

Metode: skrip `a1_replika.py` / `a1b_counter.py` di `%TEMP%/opencode/r2_audit/`.
`r2.py` dan `sh4.py` **TIDAK** diimpor; hanya dibaca sebagai spesifikasi.
Angka dihitung ulang dari parquet beku memakai API produksi
(`load_processed`, `prepare_bars`, `daily_metrics`,
`exclusive_session_label`) dan `src/utils/config.load_config`.

### A1.1 Input beku (diukur ulang auditor)

```
sha256 m1_2024 = 69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac  COCOK
sha256 m1_2025 = fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af  COCOK
sha256 m15     = cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb  COCOK
sha256 d4      = 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c  COCOK
pip_size = 0.01 | by_session London 0.61 / NewYork 0.69 / Tokyo 0.62 / Sydney 0.8
cost_basis.default (Off) = 0.65
```

### A1.2 Join-gate (output mentah replikasi auditor)

```json
{
  "n_bar_pool_m15": 47721,
  "n_bar_store_pool": 47721,
  "n_sama": true,
  "sekuens_date_broker_identik": true,
  "sekuens_hour_utc_identik": true,
  "atr_daily_metrics_identik_store_exact": true,
  "n_hari_common_atr": 974,
  "n_hari_broker_pool": 519,
  "rentang_pool": ["2024-01-02T00:00:00", "2025-12-31T00:00:00"]
}
```

Cocok byte-per-key dengan `R2_join_gate` di `r2_hasil.json` dan dengan blok
raw yang ditempel di `hasil-R2-stratifikasi.md:95-105`.

### A1.3 Loop jam-tetap (counter penuh)

```
jam yang pernah dipakai trade: [0, 7, 12, 13, 14, 15]   -> semua dalam lock [14,13,0,15,12,7]
{
  "n_hari_broker": 519, "n_hari_dengan_flatt": 0,
  "n_jam_slot_total": 3114, "n_jam_flat_bar_tidak_ada": 0,
  "n_trade_tereksekusi": 3114,
  "n_exit_SL": 158, "n_exit_TP": 15, "n_exit_time_stop": 2941,
  "n_fallback_label_Off": 0,
  "n_trade_hari_karantina": 30, "n_trade_hari_gap_flag": 636,
  "n_trade_hari_anomali_C": 30, "n_aksi_ATR_Tminus1_nan": 0
}
```

Aritmetika tertutup: 519 hari x 6 jam = 3114 slot = 3114 trade;
0 slot hilang; 0 ATR NaN; 158 + 15 + 2941 = 3114.

### A1.4 Stratifikasi tahun (replikasi mandiri)

```json
{
  "2024": {
    "n_trade": 1560,
    "median_ev_jpy": 0.04834999999999022,
    "mean_ev_jpy": 0.024799771062270975,
    "persen_positif": 0.5487179487179488,
    "n_exit_SL": 87, "n_exit_TP": 9, "n_exit_time_stop": 1464,
    "n_Off_deskriptif_sesi_Off": 0,
    "n_fallback_bukan_tabel_biaya": 0,
    "n_trade_hari_karantina_F1": 30
  },
  "2025": {
    "n_trade": 1554,
    "median_ev_jpy": -0.005049999999992838,
    "mean_ev_jpy": -0.0039283324140465484,
    "persen_positif": 0.49356499356499356,
    "n_exit_SL": 71, "n_exit_TP": 6, "n_exit_time_stop": 1477,
    "n_Off_deskriptif_sesi_Off": 0,
    "n_fallback_bukan_tabel_biaya": 0,
    "n_trade_hari_karantina_F1": 0
  }
}
```

Tepat 13 field per tahun x 2 tahun = 26 nilai; **26/26 identik** dengan
`r2_hasil.json` (representasi float dikonversi ke string repr sebelum
perbandingan). 87+9+1464 = 1560; 71+6+1477 = 1554.

### A1.5 Lock R-2 mekanis (replikasi)

```json
{"median_ev_2024": 0.04834999999999022,
 "median_ev_2025": -0.005049999999992838,
 "tahun_gugur": [2025],
 "verdict": "GUGUR(R-2)"}
```

Sesuai spec baris 55-57 (OR-gugur: satu tahun median <= 0 sudah cukup) dan
sesuai lock R-2 verbatim. Tidak ada ambang, statistik tambahan, atau
kalibrasi yang ditambahkan.

**A1 = COCOK.**

---

## 4. A2. Gate lock jam + sabotase ke jalur produksi (TEMUAN T-1, HIGH)

### A2.1 Spec yang diwajibkan

`spesifikasi-R2-stratifikasi.md:92-93`:

```
3. Assert: loop entry HANYA `FIXED_HOURS` lock (GAGAL bila tersentuh data);
   grain hari-broker tunggal (`utc.normalize()` DILARANG).
```

Dua kewajiban terpisah: (a) grain hari-broker tunggal tanpa
`utc.normalize()`; (b) **assert yang menggigit bila loop entry menyentuh
data**.

### A2.2 Yang benar-benar diimplementasikan

`r2.py:86` (satu-satunya assert lock):

```python
assert list(sh4.FIXED_HOURS) == LOCK_HOURS, "FIXED_HOURS Batch-2 != lock R-2"
```

Loop aktual `r2.py:195`:

```python
for hh in sh4.FIXED_HOURS:
```

Analisis: `sh4.FIXED_HOURS` adalah konstanta; `LOCK_HOURS` adalah literal
`[14, 13, 0, 15, 12, 7]` (`r2.py:57`). Assert membandingkan **dua sumber
yang tidak bergantung pada loop**: ia dijalankan sekali sebelum loop dan
tetap `True` untuk nilai konstanta apa pun yang tidak diubah, apa pun yang
benar-benar diiterasi loop. Tidak ada assertion sesudah loop (mis.
`set(jam_utc trades) == set(LOCK_HOURS)`), sehingga pengalihan ke data uji
tidak pernah terdeteksi.

### A2.3 Sabotase (semua lewat jalur eksekusi produksi)

Jalur produksi `r2.py` **tidak mendefinisikan `main()`**; entry-point
sesungguhnya adalah `if __name__ == "__main__": raise SystemExit(run())`
(`r2.py:342-343`). Karena itu semua mutasi dijalankan sebagai
`python <salin>/r2.py`, yaitu persis entry-point executable yang dipakai
coder. (Spec baris 108 melarang `main()` di jalur eksekusi, sehingga
pemilihan `run()` + guard `__main__` adalah kepatuhan, bukan penyimpangan.)

| Kasus | Yang dimutasi | rc | n 2024 | median 2024 | n 2025 | median 2025 | verdict |
|---|---|---|---|---|---|---|---|
| ASLI | - | 0 | 1560 | 0.04834999999999022 | 1554 | -0.005049999999992838 | GUGUR(R-2) |
| S1 | top-6 per tahun, suntik di dalam loop | 0 | 1560 | 0.05439999999999045 | 1554 | -0.010000000000002502 | GUGUR(R-2) |
| S1b | top-6 **dihitung dari data tahun-uji** | 0 | 1560 | 0.05439999999999045 | 1554 | -0.010000000000002502 | GUGUR(R-2) |
| S2 | `for hh in range(24)` | 0 | 5978 | 0.025100000000010687 | 5953 | -0.01910000000000523 | GUGUR(R-2) |
| S3 | guard diganti `allclose(X, X)` (nilai-vs-diri) | 0 | 1560 | 0.04834999999999022 | 1554 | -0.005049999999992838 | GUGUR(R-2) |
| S4 | guard konstanta dihapus seluruhnya | 0 | 1560 | 0.04834999999999022 | 1554 | -0.005049999999992838 | GUGUR(R-2) |

```
sha256 artefak ASLI                       = 4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4  (1356769 B)
sha256 artefak S1b (top-6 dari data uji)  = 09C883836EA88EA32E5480FDCC9C2C39F3E2CCD48925145337B1979DBB7B84E2  (1356473 B)
sha256 artefak S2 (range 24)              = 6F8A3E0EB4F1BF2D8642987104093C16FC584F1E461F29B70DF5C1CC310D072C  (5190418 B)
sha256 artefak S3 (guard nilai-vs-diri)   = 4664B4D8... (identik ASLI)
sha256 artefak S4 (guard dihapus)         = 4664B4D8... (identik ASLI)
```

Bacaan kinetik tiap kasus:

- **S2 adalah bukti penentu.** Loop dibebaskan ke 24 jam, jumlah trade
  naik 3114 -> 11931, kedua median berubah, artefak membesar 3.8x, dan
  proses **tetap keluar `rc=0` tanpa satu pun assert**. Spec menulis
  "GAGAL bila tersentuh data"; tidak ada yang bergigit.
- **S1b** membuktikan bahwa gate tidak membedakan konstanta lock dari
  pilihan jam yang dihitung dari data uji. Hasil S1b persis sama dengan
  S1 (`0.05439999999999045` / `-0.010000000000002502`): top-6 versi S1b
  adalah `[14,13,0,1,15,12]`, yaitu jam `1` masuk menggantikan jam `7`
  yang ada di lock `[14,13,0,15,12,7]`. Gate tetap `rc=0`.

**T-1 (HIGH).** Spec `spesifikasi-R2-stratifikasi.md:92-93` mewajibkan assert yang menggigit saat loop entry menyentuh data. Yang diimplementasikan hanya konstanta-vs-literal. Konsekuensi terverifikasi: mutasi S1b dan S2 lolos `rc=0` dengan angka berbeda. **Eskalasi arsitek.**

Perbaikan yang disarankan (bukan diterapkan auditor): tambahkan
assertion pasca-loop yang menguji himpunan jam entry aktual terhadap lock,
misalnya `assert set(t["jam_utc"] for t in trades) == set(LOCK_HOURS)`
sehingga pengalihan ke data uji atau ke 24 jam memunculkan
`AssertionError`.

---

## 5. A3. Definisi beku n_Off / session label / voris H4-H5-H6 (COCOK)

### A3.1 Definisi Off beku (dibaca dari kode produksi)

`src/features/build_features.exclusive_session_label` (dipakai oleh
`_eda_common.py:74` dengan urutan prioritas London > NewYork > Tokyo >
Sydney > **Off**; default `Off` bila tidak ada flag yang menyala).
`SESSION_COLUMNS = [is_tokyo, is_london, is_ny, is_sydney]`.

Label store **dihitung ulang dari flag**, bukan dibaca apa adanya:
`A3_2_label_store_ada = true` untuk seluruh pool (23909 bar 2024 + 23812
bar 2025). 21800 bar memiliki lebih dari satu flag menyala; urutan
eksklusif yang mengikatnya.

### A3.2 n_Off dihitung dari nol, per tahun

```json
"2024": {"n_bar_pool": 23909, "n_bar_jam_lock": 1560,
         "n_Off_semua_bar_pool": 0, "n_Off_bar_jam_lock": 0,
         "n_fallback_label_di_luar_tabel_biaya": 0,
         "distribusi_label_pool": {"London": 8320, "Tokyo": 7720, "NewYork": 6130, "Sydney": 1739},
         "distribusi_label_jam_lock": {"London": 1040, "Tokyo": 370, "NewYork": 150}},
"2025": {"n_bar_pool": 23812, "n_bar_jam_lock": 1554,
         "n_Off_semua_bar_pool": 0, "n_Off_bar_jam_lock": 0,
         "n_fallback_label_di_luar_tabel_biaya": 0,
         "distribusi_label_pool": {"London": 8288, "Tokyo": 7688, "NewYork": 6120, "Sydney": 1716},
         "distribusi_label_jam_lock": {"London": 1036, "Tokyo": 368, "NewYork": 150}}
```

**Tidak ada satu pun bar Off di seluruh pool 2024 maupun 2025** -- bukan
hanya di jam lock. Karena itu `n_Off_deskriptif_sesi_Off = 0/0` dan
`n_fallback_bukan_tabel_biaya = 0/0` bersifat struktural, bukan hasil
kebetulan. Sesuai spec baris 61-63 dan 90, n_Off **non-penentu** dan
memang tidak dipakai vonis.

### A3.3 Verifikasi silang klaim ESK-1

Spec baris 46 mengutip putusan-H4b ter-hash: "2024/2025 n_Off=0; 2023
2894 bar jam 21 UTC". Auditor menghitung ulang dari store M1 dengan
`session_flags` + `exclusive_session_label` (resep produksi):

```
Off M1 per tahun UTC : {"2023": 2894}
Off M1 jam 21 per th  : {"2023": 2894}
Off M1 2023 total    : 2894   jam-21: 2894
Off M1 2024/2025/2026: 0
```

**2894 terverifikasi persis**, dan seluruhnya jam 21 UTC tahun 2023.
(Konteks M15: 220 bar Off, semuanya jam 21 UTC 2023. Angka 2894 adalah
hitungan bar M1; keduanya konsisten karena 220 x ~13 bar M1 per jam.)

### A3.4 Tidak ada voris H4/H5/H6 di dokumen coder

Semua kemunculan `H4`/`H5`/`H6` di `hasil-R2-stratifikasi.md` diperiksa
satu per satu (baris 1, 4, 161, 163, 201, 218, 223). Semuanya adalah
judul, larangan, rujukan kehati-hatian, atau self-audit -- **tidak ada satu
pun voris H4/H5 baru**. Nihil H6 dipatuhi. Ruang vonis tidak diambil.

**A3 = COCOK.**

---

## 6. A4. Larangan data 2026 / tanpa H6 / tanpa scope creep (COCOK, 1 catatan)

### A4.1 Grep terlarang pada `r2.py` (343 baris, dibaca penuh)

| Pola | Kemunculan |
|---|---|
| `utc.normalize(` | 0 |
| `top[\s_-]?6` | 0 |
| `regime` | 0 |
| `TAU` | 0 |
| `threshold` / `ambang` | 0 |
| `grid` | 0 |
| `calibr` | 0 |
| `quantile` | 0 |
| `H6` | 0 |

Dua baris saja yang cocok pola "filter EV" adalah rumus lock itu sendiri
(`r2.py:9` docstring dan `r2.py:310` field `aturan`) -- itu lock verbatim,
bukan filter pasca-hoc. Grain hari-broker tunggal dijaga lewat
`groupby("broker_day")`; `utc.normalize()` tidak ada.

### A4.2 2026 pada artefak

```
kemunculan teks "2026" di r2_hasil.json          : 0
kunci tahun di R2_stratifikasi_tahun            : ["2024", "2025"]
tahun unik pada trades                          : ["2024", "2025"]
meta.years_eval                                 : [2024, 2025]
meta.fixed_hours                                : [14, 13, 0, 15, 12, 7]
jam unik pada trades                            : [0, 7, 12, 13, 14, 15]
kemunculan teks "2026" di r2.py                 : 1 (baris 12, pernyataan larangan)
```

Nol kemunculan 2026 di seluruh hitungan maupun deskriptif artefak.

### A4.3 Uji kausal 2026 (TEMANAN T-3)

Loader memang membaca store penuh, sehingga `daily_metrics` menghitung
196 hari bertanggal 2026 sebagai between-state (n bar M1 turun dari
1347847 menjadi 1078001 saat dipangkas pada 2025-12-31). Auditor menguji
apakah itu bocor:

```
n_hari_diperiksa                : 519   (seluruh hari pool 2024-2025)
n_hari_daily_full               : 959
n_hari_daily_trunc_leq_2025     : 763
n_hari_hanya_di_full            : 196   (semuanya 2026)
atr_2024_2025_identik           : True  (np.array_equal, equal_nan=True)
```

Nol kontribusi, terbukti bit-per-bit. Sesuai treatment H4b yang sudah
terkunci (`reaudit-H4b-stabilitas.md:262-281`), ini **patuhi secara
substantif**. **T-3 (LOW)** dicatat karena frasa spec "2026 dikecualikan
PENUH" (baris 67) dapat dibaca sebagai larangan menghitung sama sekali;
rekomendasi klarifikasi arsitek, bukan pelanggaran coder.

**A4 = COCOK dengan catatan T-3.**

---

## 7. A5. Sumber F-1, default INKLUSI, dan "tiga rekaman" (COCOK, 1 catatan)

### A5.1 Sumber F-1 primer (terpisah dari jalur config)

`src/features/build_labels.py:53-56` -- `ANOMALY_WINDOWS`, dua jendela
dari putusan F-1 butir 2:

```json
{"berkas": "src/features/build_labels.py:53-56",
 "windows": [["2024-10-28","2024-11-01"], ["2026-03-10","2026-03-27"]],
 "hari_per_window": {"2024-10-28..2024-11-01": 5, "2026-03-10..2026-03-27": 18},
 "total_hari_kalender": 23}
```

Komentar kode menyebut "19 hari anomali". Ini **tidak**kontradiksi: D4
hanya memuat hari-broker (akhir pekan absen), sehingga
`quarantine_mask` di D4 berisi **tepat 19 hari** -- 5 hari 2024 + 14 hari
2026. Auditor menghitung ulang dari D4:

```
n_hari_D4_karantina            : 19
karantina yang masuk pool       : ["2024-10-28","2024-10-29","2024-10-30","2024-10-31","2024-11-01"]
n_hari_karantina_di_pool       : 5
window 2026 masuk pool?        : false
hari 2026 di D4                 : 14
```

Jalur kedua (`config["validation"]["anomaly_windows"]`, dipakai
`r2.py:73` untuk counter `n_trade_hari_anomali_C`) **identik** dengan
`ANOMALY_WINDOWS` (`identik_dengan_ANOMALY_WINDOWS: true`), sehingga kedua
counter F-1 agrees secara struktural -- bukan dua sumber bebas.

### A5.2 Bukti INKLUSI (tidak ada eksklusi)

```
hari pool per tahun            : 2024 = 260, 2025 = 259   (total 519)
n_trade per tahun artefak      : 2024 = 1560, 2025 = 1554
n_trade_2024 = hari x 6        : true
n_trade_2025 = hari x 6        : true
n_trade_total                  : 3114  (= 519 x 6, tanpa satu trade pun hilang)
n_trade_hari_karantina         : 30     (5 hari x 6 jam)
karantina_sama_dengan_5_hari_x_6: true
n_trade_karantina 2024 / 2025  : 30 / 0
n_trade_anomali_C               : 30
n_jam_flat_bar_tidak_ada        : 0
n_aksi_ATR_Tminus1_nan          : 0
n_trade_hari_gap_flag           : 636
jam unik trade karantina       : [0,7,12,13,14,15] = lock (true)
```

Tidak ada `filter`, `drop`, atau eksklusi apa pun di `r2.py`; 30 trade
karantina **tetap masuk** angka penentu, sesuai fondasi-B D-1 dan
`protokol-telaah-fondasi-B.md:62-71`. Varian default = INKLUSI, terverifikasi.

### A5.3 "Tiga rekaman sepakat" -- valid sebagai apa (TEMANAN T-2)

Nilai di tiga tempat memang identik:

```json
{"r2_2024_median": 0.04834999999999022, "batch2_2024_median": 0.04834999999999022, "median_2024_identik": true,
 "r2_2025_median": -0.005049999999992838, "batch2_2025_median": -0.005049999999992838, "median_2025_identik": true,
 "r2_2024_n": 1560, "batch2_2024_n": 1560, "n_2024_identik": true,
 "r2_2025_n": 1554, "batch2_2025_n": 1554, "n_2025_identik": true,
 "pool_total_r2": 3114, "pool_total_batch2": 3114}
```

Spec `spesifikasi-R2-stratifikasi.md:36-41` (S-V(b)) mengutip angka yang
sama. Namun ketiganya **bukan pembuktian independen**: R-2 adalah partisi
tahun dari pool 3114 trade yang sama, dihitung oleh mesin S-H4 Batch-2
yang sama, dengan `FIXED_HOURS` yang sama. Kesepakatan median per tahun
adalah **identitas aritmetik**, bukan konfirmasi empiris --nol peluang
kebetulan, tetapi juga nol kekuatan bukti tambahan. `hasil-R2-stratifikasi.md:205-207`
menyebutnya "tiga rekaman sepakat" tanpa kualifikasi ini.
**T-2 (LOW).** Pembuktian independen yang sesungguhnya adalah A1 (dan
A6), yang dilakukan auditor di sini.

**A5 = COCOK dengan catatan T-2.**

---

## 8. A6. Determinisme dan toolchain (COCOK, byte-identik)

Auditor menjalankan ulang `r2.py` **penuh** dari salinan terisolasi
(`%TEMP%/opencode/r2_audit/repro/r2.py` + `r2_audit/l3h4h5/sh4.py`),
tidak menyentuh direktori coder.

```
r2.py  sha256 (salinan auditor) = 667EB4DFFFEE604724A577F29231F96BD09D5156A6CD8426E7870D02A0B9EEB1
sh4.py sha256 (salinan auditor) = 544E3D3F3D85EC047693E1D3C5354623D21B4E3C56228F88185D0BC64D463EEE

re-run auditor  r2_hasil.json     = 4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4  (1356769 B)
coder  run1     r2_hasil_run1.json= 4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4
coder  run2     r2_hasil_run2.json= 4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4
cmp re-run auditor vs coder      : byte-identik (fc /b -> rc 0)
```

Toolchain dideklarasikan dalam `meta` artefak, diukur ulang auditor:

```
python 3.12.8 | numpy 1.26.4 | pandas 2.2.3 | scipy 1.17.1 | pyarrow 17.0.0
interpreter: D:\ANN\venv\Scripts\python.exe
meta hasil re-run auditor identik dengan meta artefak coder : True
```

Sesuai spec baris 94 dan 104-105 (determinisme; sebut toolchain saat
menyebut byte-identik). Klaim "254 passed" pada
`hasil-R2-stratifikasi.md:179` diuji ulang auditor: **254 passed**, rc 0.

**Catatan operasional (bukan temuan):** `r2.py:51` me-resolve `sh4.py`
dari `R2DIR.parent`, jadi harness tidak portabel bila dipindah. Auditor
menyesuaikan tata letak salinan; ini keterbatasan harness `%TEMP%`, bukan
cacat R-2.

**A6 = COCOK.**

---

## 9. A7. Gate laporan coder (COCOK dengan 1 catatan)

| Gate | Verifikasi auditor | Status |
|---|---|---|
| Struktur: S-0, S-2/S-3/S-4, R2-4, S-7, G-det, Klaim & Bukti, Self-audit, STOP | `hasil-R2-stratifikasi.md:9-226` | COCOK |
| Output mentah per tahun | blok JSON `hasil-R2-stratifikasi.md:94-106` dan `:110-137`; `R2_lock` `:148-156` | COCOK |
| S-0 9 hash + HEAD + staged | `:21-52` | COCOK |
| C4 pytest rc + cakupan | klaim 254 passed rc 0; auditor: 254 passed rc 0 (`pytest tests -q --no-header`, full-suite) | COCOK |
| C4 ruff check / format --check | klaim rc 0; auditor: `All checks passed!` rc 0; `1 file already formatted` rc 0 | COCOK |
| C4 foreign chars | klaim rc 0; auditor `check_foreign_chars.py` pada laporan + r2.py: `OK: 2 file discan` rc 0 | COCOK |
| ASCII-only, LF-only | auditor: 9811 B, ascii_only True, crlf 0, lf 226 | COCOK |
| C8 tanpa self-hash | kemunculan pola `0x[0-9a-f]{7,}` = 0 | COCOK |
| C6/C7 vonis mekanis tunggal | hanya `GUGUR(R-2)`, dihitung dari median sendiri | COCOK |
| C1/C2/C9 HEAD tetap, nol tulis, staged 2 | HEAD & staged diukur ulang di S-0; tidak ada perubahan oleh sesi audit | COCOK |
| B10 provenans terpisah + sabotase jalur produksi | 4 sha di-assert sebelum hitung (`r2.py:101-113`) dan output mentahnya ditempel | COCOK |
| B8 tidak ada klaim "diuji via X" tanpa test | tidak ditemukan | COCOK |
| Status baris vonis H4/H5 | `:201` berlabel `BELUM DIVERIFIKASI` padahal auditor memverifikasi tidak ada vonis | **T-4 (LOW)** |

Catatan T-4 hanya soal label: isi baris itu benar (memang tidak ada vonis
H4/H5), tetapi label `BELUM DIVERIFIKASI` lebih lemah dari yang faktanya
dan menyisakan ruang apkuran yang tidak perlu.

**A7 = COCOK dengan catatan T-4.**

---

## 10. Ringkasan A1-A7

| Item | Verdict | Catatan |
|---|---|---|
| A1 replikasi independen | COCOK | 26/26 nilai tahun + 7 field gate identik |
| A2 gate lock + sabotase | **GAGAL** | T-1 HIGH; angka aktual tetap benar |
| A3 definisi Off + ESK-1 + tanpa vonis | COCOK | 2894 terverifikasi persis; n_Off 0/0 struktural |
| A4 larangan 2026 / tanpa H6 | COCOK | T-3 LOW; uji kausal bit-identik |
| A5 sumber F-1 + INKLUSI | COCOK | T-2 LOW; 5 hari, 30 trade, nol eksklusi |
| A6 determinisme + toolchain | COCOK | byte-identik 3 JSON |
| A7 gate laporan coder | COCOK | T-4 LOW |

**PUTUSAN AUDIT: GAGAL** -- atas nama T-1 (HIGH), bukan atas nama angka.
Eskalasi ke arsitek: gate `spesifikasi-R2-stratifikasi.md:92-93` menuntut
assert dependen-data; implementasi yang ada adalah identitas konstanta.

---

## 11. Aturan baca TERTUTUP (dipakai auditor)

1. Terapkan lock R-2 verbatim; satu vonis mekanis: `GUGUR(R-2)`.
2. `GUGUR(R-2)` = efek H4 tidak stabil antar-tahun pada split jam-tetap.
   Bukan retak H4 Batch-2; bukan vonis baru atas H4/H5.
3. Angka penentu diverifikasi ulang oleh auditor (A1/A6) dan **benar**.
   Penegasan ini tidak mengubah vonis mekanis R-2.
4. Dilarang statistik tambahan, kalibrasi, H5, H6, rekonstruksi UTC,
   filter pasca-hoc.
5. Temuan kontrol (T-1) dinilai berdasarkan **kekuatan implementasinya**,
   bukan berdasarkan dampak angka. Dampak angka terbukti nol dan
   dinyatakan terbuka.

---

## 12. Klaim & Bukti (S5/S20)

| Klaim auditor | Status | Bukti |
|---|---|---|
| S-0 9/9 + HEAD + staged 2 | TERVERIFIKASI | blok S-0 bagian 1; `git rev-parse`, `git diff --cached` sesi ini |
| Angka 2024/2025 penentu benar | TERVERIFIKASI | A1.4: 26/26 nilai identik dengan `r2_hasil.json` |
| Gate join-gate + ATR exact benar | TERVERIFIKASI | A1.2: 47721/47721, sekuens identik, ATR exact 974 hari |
| Loop jam-tetap lock benar secara aktual | TERVERIFIKASI | A1.3 jam unik `[0,7,12,13,14,15]`; A4.2 jam unik trades sama |
| Grain hari-broker, tanpa `utc.normalize()` | TERVERIFIKASI | grep A4.1 = 0; `groupby("broker_day")` di `r2.py:189` |
| n_Off 0/0 struktural, non-penentu | TERVERIFIKASI | A3.2: nol bar Off di SELURUH pool 2024/2025 |
| Klaim ESK-1 "2894 bar M1 jam 21 UTC" | TERVERIFIKASI | A3.3: hitung ulang = 2894, semua jam 21 UTC 2023 |
| 2026 nol kontribusi ke angka | TERVERIFIKASI | A4.3: `atr_2024_2025_identik = True` atas 519 hari |
| F-1 5 hari + 30 trade karantina, INKLUSI | TERVERIFIKASI | A5.2: 5 x 6 = 30, total trade tetap 3114, nol eksklusi |
| Determinisme byte-identik | TERVERIFIKASI | A6: 3 JSON sha sama; re-run auditor fc/b rc 0 |
| Verdict mekanis `GUGUR(R-2)` | TERVERIFIKASI | A1.5; sesuai spec:55-57 tanpa ambang tambahan |
| Gate lock jam benar-benar ada | **TIDAK TERVERIFIKASI (T-1)** | A2.3: S1b/S2 lolos `rc=0`; `r2.py:86` hanya banding konstanta |
| Nihil voris H4/H5/H6 di dokumen coder | TERVERIFIKASI | A3.4: 7 kemunculan, semua rujukan/larangan |
| Gate mutu laporan coder (pytest/ruff/foreign/ASCII/C8) | TERVERIFIKASI | A7 tabel; 254 passed rc 0; ascii_only; 0 hash `0x...` |
| Klaim "tiga rekaman" independen | **TIDAK TERVERIFIKASI (T-2)** | A5.3: partisi aritmetik dari mesin yang sama |
| Eksklusi 2026 total (bukan sekadar nol kontribusi) | **TIDAK TERVERIFIKASI (T-3)** | A4.3: 196 hari 2026 tetap dihitung sebagai between-state |
| Status baris vonis H4/H5 di `:201` | **TERLAMBAT (T-4)** | A7: facts benar, label `BELUM DIVERIFIKASI` |

---

## 13. Self-audit 3x (auditor)

1. **Correctness.** S-0 9/9; spec dibaca penuh 141 baris; `r2.py` dibaca
   penuh 343 baris; dokumen coder dibaca penuh 226 baris; A1 menghitung
   ulang seluruh angka penentu dari parquet tanpa mengimpor kode coder;
   A6 mengulang eksekusi penuh dan menghasilkan byte identik; A2 menguji
   gate dengan empat mutasi nyata pada entry-point executable.
2. **Bias.** Tidak ada ambang, filter, sub-sel, atau statistik yang
   ditambahkan. T-1 dinaikkan ke HIGH karena brief mengikat temuan gate ke
   HIGH, dengan dampak angka dinyatakan terbuka (nol) agar severity tidak
   dibaca berlebihan; T-2/T-3/T-4 diturunkan karena tidak mengubah angka
   maupun vonis. Kewajiban "tiga rekaman" tidak dipakai sebagai bukti
   independen justru karena auditor memverifikasinya sebagai identitas
   aritmetik. EKS-3 dicatat, tidak disembunyikan.
3. **Meta.** Ruang arsitek tidak diambil (rekomendasi perbaikan gate
   ditulis sebagai usulan, tidak diterapkan); ruang coder tidak diambil
   (tidak ada satu pun baris diubah di `%TEMP%/opencode/r2/`, di `src/`,
   di `configs/`, atau di `data/`); satu-satunya berkas repo yang ditulis
   oleh auditor adalah laporan ini; tidak ada commit, push, stage,
   stash, atau checkout; staged tetap 2 T6 dengan blob tidak berubah.

STOP. Re-audit R-2 selesai. Hash dokumen ini TIDAK ditempel di isi
(pengikatan eksternal); dilaporkan di kanal luar. Putusan R-2 resmi
adalah berkas tersendiri di luar lingkup auditor ini.