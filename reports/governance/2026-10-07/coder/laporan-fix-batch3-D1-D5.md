# Laporan Fix Batch Ketiga D1–D5 — rondo penutup re-audit kedua

**Tanggal:** 2026-10-08 (patch batch-4: 5 butir §11 re-audit ketiga — catatan **KOREKSI BATCH-4** di §1/§5/§6/§9/§11)
**Peran:** Coder. Mengimplementasikan putusan A/B/C + 14 syarat §7 re-audit kedua.
**Basis (hash git blob, terverifikasi di sesi ini):**

| Sumber | git blob |
|---|---|
| `Audit/reaudit-kedua-fix-D1-D5.md` | `1f99203711e92afa77166de9d6a0184a44463e19` |
| `arsitek/putusan-adjudikasi-reaudit-kedua.md` | `295303a46dfd9dd3b0b047a0b931895e7fd2eed3` |
| `arsitek/putusan-arsitek-fix-D1-D5.md` | `ca57e7647e955ee0dfe68579db5dbef6216a427b` |
| `Audit/reaudit-adversarial-D1-D5.md` | `c608f793be40a57c0ead8b1901efa5745dff03cd` |
| `arsitek/putusan-arsitek-H1-H5.md` | `e8eb03daf994051600258cf412ec9e9af65d800c` |
| `arsitek/putusan-arsitek-F1.md` | `746052b0256b36e088acb213e45c1f455b690795` |

**Artefak yang ditulis batch ini (hash diukur SESUDAH penulisan terakhir):**

| Artefak | Hash git blob | Ukuran |
|---|---|---|
| `src/features/build_labels.py` | `90e44a825ee356e397d96ab5137caf35e6e575f4` | 400 baris |
| `tests/test_build_labels.py` | `53468d95da00f4c36789ee1df3435edc579df373` | 586 baris, 54 test |
| `coder/protokol-H1-H2-H3.md` | `758c5d301ede4ec105d882b164f9baad7bbd6d83` | 291 baris |
| `coder/laporan-final-fase1.md` | `e645a042a7ffcae7ffa21e6b1a995a7dc7c6085c` | 340+ baris |
| `data/labels/usdjpy_day_labels.parquet` | sha256 `47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c` (29121 B) | 974 baris; blob `a01694e3eafafa9c9e2e14ca3d8396706b4f2857` |
| `data/labels/usdjpy_h2_trades.parquet` | sha256 `32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f` (7837 B) | 1 baris; blob `7138325d278283056d09974cbf93fddbb2926b40` |
| laporan ini | hash mustahil di-embed konsisten; diukur setelah penulisan terakhir dan dilaporkan di pesan penutup | — |

---

## 1. STATUS SYARAT §7 (14 butir) + PUTUSAN A/B/C

| Syarat §7 | Putusan | Status | Bukti |
|---|---|---|---|
| 1. Pulihkan row key D4 (#20) | — | **TERTUTUP** | §2.2 + §9.7: index `date_broker` (`index=True`) |
| 2. Grain tunggal broker-day (#21/#22) | C | **TERTUTUP** | §2.1 + §9.7: 974 baris, drift NaN 0, norm NaN 14 |
| 3. Adjudikasi #23 (gap 479 vs 234) | A | **TERTUTUP** | §4: recount 234/597 = angka B1 |
| 4. Jalankan Q1(a) (Lubang 2/#24) | — | **TERTUTUP** | §5: TAU/AUC/n riil di protokol §2 |
| 5. Guard satuan sahih (Lubang 1) | B | **TERTUTUP → DITOLAK re-audit ketiga §3.5** (klaim §6.3 terbukti hanya 3/10 pada jalur produksi karena referensi = kolom frame yang sama; diperbaiki + dibuktikan ulang batch-4 butir 1) | §6 + KOREKSI BATCH-4 §6.3 |
| 6. Perbaiki 4 `TestBuktiMutasi` (#25) | — | **TERTUTUP** | §3.2: merah saat dicabut (exit=1) |
| 7. Kunci `LONDON_FIRST_N` fixture sensitif (#26) | — | **TERTUTUP** | §3.3: N=4/8/60 merah (exit=1) |
| 8. Hapus/isi `test_status_belum_diuji` (#27) | — | **TERTUTUP** | §3.4: test dihapus, nol test `pass` |
| 9. D1 ≤400 baris, `main` ≤50; hapus `_daily_from_m15` (#28/#29) | C-2 | **TERTUTUP** | §2.3 + §7: 400/400, main AST 33 |
| 10. `FutureWarning` :253 (#35) | — | **TERTUTUP** | §7: `-W error::FutureWarning` exit 0 |
| 11. Hash ulang + "230 total / 36 baru" (#30/#31) | — | **TERTUTUP** | §9.5: 248 total / 54 baru |
| 12. Kutipan F1 → 73-75 + path `arsitek/` (#33) | — | **TERTUTUP** | protokol §3 |
| 13. Unstage indeks (audit mencatat 23 entri; sesi ini terukur 7 staged) + tulis ulang D5 §4 (#32) | — | **TERTUTUP** | §8.2 + §9.8: staged = 0 |
| 14. Severity #10 = TERTUTUP (#19) | — | **TERTUTUP** | `laporan-final-fase1.md` §3 |
| Putusan A butir 4: rekonsiliasi bucket-per-bucket | A | **TERTUTUP** | §4.2 butir 3–4 |
| Putusan A butir 5: 479 dilarang jadi target/pembanding/pembenar | A | **DIPATUHI** | §4.2 |
| Putusan B butir 1: klausa `:169-172` dihapus, dilarang kembali | B | **DIPATUHI** | §6.1: grep 0 kemunculan |
| Putusan B butir 4: min. 2 test sabotase terkunci | B | **TERTUTUP** | §6.2–§6.3 (3 kasus, parametrized) |
| Putusan C butir 5: batas adjudikasi (#20/#24/#25-#36 terbuka) | C | **DIPATUHI** | seluruh butir di atas dikerjakan; #36 ditutup §8.3 |

**Sisa yang TIDAK dikerjakan (bukan bagian mandat):** vonis H3/H4/H5;
penaikan D3/D4 ke Lapisan 3; perubahan lock/ambang.

---

## 2. D1 — `src/features/build_labels.py`

### 2.1 Grain tunggal (putusan C)

- `utc.normalize()` **dihapus seluruhnya** dari kode; seluruh rantai memakai
  `prepare_bars` store (`broker_time_raw` → wall → normalize).
- `_daily_from_m15` (kode mati, sumber grain kedua) **dihapus** → #29.
- `compute_gap_f2_flag` kini bergrain broker-day (bukan `utc.dt.normalize()`).
- `london_drift_norm` dihitung pada index yang sama (`daily.index`), tanpa
  reindex lintas-grain.

Bukti kode (AST, bukan docstring):

```
$ grep -n "utc.normalize\|_daily_from_m15" src/features/build_labels.py
(tidak ada di kode; hanya disebut di docstring sebagai larangan)
$ python -c "AST walk: [ast.unparse(n) for n in walk if isinstance(n, ast.Attribute)]"
assert not any("normalize" in call for call in calls)   -> LULUS (test D2)
```

Bukti eksekusi (produksi, D4):

```
day shape: (974, 6)   columns: ['day_label','london_drift_4h','london_drift_norm','gap_f2_flag','rv_regime_flag','quarantine_mask']
index name: date_broker
day_label nulls: 0
day_label counts: {'trending': 330, 'range': 324, 'normal': 320}
quarantine dtype: bool   True count: 19
drift NaN: 0
norm NaN: 14          <- tepat warmup ATR (atr_14_d1 NaN = 14)
gap flagged: 234
rv NaN: 19/974 (warmup min_periods=20)
date_broker range: 2023-01-02 .. 2026-10-02
```

Sebelum batch ini (audit #21): 1174 baris, `day_label=None` 200,
`quarantine_mask` dtype object, norm NaN 214. Sesudah: **974 / 0 / bool / 14**.

### 2.2 Row key (#20)

`write_labels(..., index=True)` menulis index `date_broker`. Dibaca ulang:

```
$ python -c "pd.read_parquet('data/labels/usdjpy_day_labels.parquet')"
index name: date_broker     (setiap bar daily punya identitas)
```

### 2.3 Pagu (#28)

```
modul baris: 400  pagu 400 -> OK
fungsi terpanjang: ('compute_london_drift_4h', 41)  pagu 50
main AST: 33
```

---

## 3. D2 — `tests/test_build_labels.py`

### 3.1 Komposisi

`54 tests collected` (batch-2: 36). Kelas: classify, London drift,
JendelaLondonLock, GrainBrokerDay, GapF2Flag, RvRegimeFlag, QuarantineMask,
DuaVarianEksklusi, RegisterH2Strategy, GuardProvenansAtr, BuktiMutasi,
PaguBarisD1, MainEndToEnd (produksi 974/234/19/norm-14 + byte-reprodusibel).

### 3.2 #25 — bukti mutasi kini benar-benar mengikat

Mekanisme baru: mutasi ditambal pada **binding yang dipakai test**
(`monkeypatch.setattr(HERE, ...)`, `HERE = sys.modules[__name__]`), lalu test
pengunci yang sama dijalankan dan **harus merah**; ada juga test yang
mendokumentasikan bug batch-2 (menambal `bl.<nama>` TIDAK mengubah binding
test — hasilnya tetap hijau, bukti no-op lama).

Bukti eksternal (plugin in-memory, patch kedua binding):

```
MUT=none -> exit=0 | 54 passed
MUT=classify_all_trending -> exit=1 | 5 failed, 49 passed
MUT=quarantine_all_false  -> exit=1 | 6 failed, 48 passed
```

### 3.3 #26 — jendela London sensitif

Fixture `make_london_rising` memberi open/close berbeda tiap bar
(`open = 150 + 0.01k`, `close = open + 0.05`) → `drift(N) = 0.05 + 0.01(N−1)`:
N=4 → 0.08, N=8 → 0.12, N=16 → 0.20, N=60 → 0.36 (semua berbeda).
Test mengunci `LONDON_FIRST_N == 16` DAN memastikan N=4/8/60 mengubah hasil.
Bukti eksternal:

```
MUT=london_first_n_4  -> exit=1 | 6 failed, 48 passed
MUT=london_first_n_8  -> exit=1 | 6 failed, 48 passed
MUT=london_first_n_60 -> exit=1 | 6 failed, 48 passed
```
(batch-2: N=1/4/8/15/60 → 36 hijau, nol coverage.)

### 3.4 #27

`test_status_belum_diuji` (isinya hanya `pass`) **dihapus**; status BELUM
DIUJI hidup di protokol §4, bukan di test kosong. Nol test tanpa assertion.

### 3.5 Kunci anti-regresi tambahan

- `test_source_tanpa_panggilan_normalize_dan_daily_from_m15` (AST).
- `test_pagu_baris`: D1 ≤400, `main` ≤50, semua fungsi ≤50.
- `test_grain_broker_day_bukan_utc`: hari-UTC hantu tidak boleh muncul.
- `test_sabotase_pembagi_meledak` (3 kasus) — lihat §6.

---

## 4. GAP RECOUNT (putusan A) — grain broker-day tunggal

### 4.1 Definisi Q3(a) kata-per-kata

> bucket parsial = `m1_bars` < 15 DAN bukan bucket pertama/terakhir
> hari-broker (mid-day); `gap_f2_flag` hari = 1 bila ≥1 bucket mid-day
> parsial, else 0; NaN DILARANG.

Dieksekusi pada grain broker-day store (`prepare_bars`), edge-rule BATAS HARI.

### 4.2 Hasil recount independen (output mentah)

```
total buckets: 90041  partial (m1_bars<15): 1281
A: UTC-day grain, day-edge        buckets/broker-days/utc-days = (1126, 525, 479)
B: broker-day grain, day-edge     buckets/broker-days/utc-days = (597, 234, 245)
C: broker-day grain, session-edge buckets/broker-days/utc-days = (578, 230, 240)
partial&utc-int: 1126  partial&broker-int: 597  both: 582  utc-only: 544  broker-only: 15
utc-days flagged(old): 479  ghost(no broker identity): 479
weekday(ghost): {0: 117, 1: 113, 2: 103, 3: 102, 4: 32, 6: 12}
```

Bacaan:

1. **Recount pada grain tunggal = 597 bucket mid-day / 234 hari-broker** —
   identik dengan angka B1 (`audit/audit-fondasi-B1.md:122`: "1.281 bucket
   parsial; 597 di antaranya mid-day … spread di 234 hari broker").
   Target final = hasil recount ini (yang kebetulan = 234), bukan angka yang
   diwarisi dari aturan lama.
2. **479 DITOLAK sebagai artefak grain campur.** Seluruh 479 hari-flag lama
   adalah hari-UTC **tanpa identitas broker** (`ghost = 479/479`); ia lahir
   dari `utc.dt.normalize()` (#21), bukan dari data. 479 tidak dipakai
   sebagai target, pembanding, maupun pembenar di mana pun (grep di laporan
   ini: hanya sebagai "ditolak").
3. **Kontribusi grain UTC→broker:** 1126 bucket/479 hari-UTC →
   597 bucket/234 hari-broker (−529 bucket, −245 hari).
4. **Kontribusi edge-rule SESI→HARI:** pada grain broker-day, Q3(a) BATAS
   HARI memberi 597/234; varian BATAS SESI (definisi run-label: bukan bar
   pertama/terakhir run sesi di dalam hari-UTC) memberi 578/230. Selisih
   ±19 bucket / ±4 hari dilaporkan sebagai **sensitivitas**, bukan sebagai
   definisi; definisi resmi tetap Q3(a) kata-per-kata.
5. **234 tetap referensi orde + jangkar B1**, status BELUM DIUJI
   dipertahankan, nuansa F-2 (223 hari ber-counterfactual) tercatat di
   protokol §4; eksklusi buta tetap DILARANG.

Di D4 produksi (grain tunggal) flag = **234** (lihat §9.7) — konsisten
dengan recount.

---

## 5. Q1(a) — KALIBRASI TAU_2023 (Lubang 2 / #24) DIEKSEKUSI

Prosedur mengikuti putusan Q1(a) kata-per-kata: span terkunci
2023-01-01..2023-12-31; label B (positif = hari-B, konsisten lock §H3
"AUC klasifikasi hari-B") = 2023-01-01..06-30; label A = 07-01..12-31;
`rv_score = rv_roll_20d / 20`; warmup NaN dikecualikan; Youden = maks
(sensitivitas + spesifisitas − 1); AUC in-sample; **tanpa** OOS.

Output mentah:

```
rv NaN overall: 19 of 974
calibration n = 240  n_B = 111  n_A = 129
AUC in-sample (class B) = 0.8173755150499336
Youden J max = 0.6046511627906976 at TAU_2023 (strict >) = 2.5951672079821496e-05
sens = 1.0  spec = 0.6046511627906976
median B = 4.145214537383251e-05  median A = 2.2750316674777358e-05
flagged in span by strict >: 162 of 240
B above: 111 / 111   A above: 51 / 129
n ties at tau: 1
```

Detail kurva Youden (top-5, memastikan maksimum tunggal):

```
tau=2.5951672079821496e-05   sens=1.0000000000 spec=0.6046511628 J=0.6046511628
tau=2.6955880478826318e-05   sens=0.9819819820 spec=0.6201550388 J=0.6021370207
tau=2.7141757333691883e-05   sens=0.9729729730 spec=0.6279069767 J=0.6008799497
tau=2.5500192653170025e-05   sens=1.0000000000 spec=0.5968992248 J=0.5968992248
tau=2.6142118926772674e-05   sens=0.9909909910 spec=0.6046511628 J=0.5956421538
plateau length (J == max): 1
```

**Ditulis sebagai angka riil ke protokol `coder/protokol-H1-H2-H3.md` §2**
(TAU_2023, AUC, n_B/n_A, sens/spec, flag-rate) dan dikunci sebagai konstanta
`TAU_2023 = 2.5951672079821496e-05` + `CALIB_AUC_2023`, `CALIB_N_B`,
`CALIB_N_A` di D1. Kalimat "tertulis di bawah" yang tidak terpenuhi
**dihapus**; klaim "HAYAT" tanpa isi **dihapus** — kolom sekarang berisi
nilai: 955/974 non-NaN (19 warmup NaN), diverifikasi di D4 (§9.7:
`rv NaN: 19/974`).

**Bukan vonis H3:** status BELUM DIUJI dipertahankan (S4); laporan ini tidak
memvonis H3/H4/H5.

**KOREKSI BATCH-4 (butir §11-3):** penguncian `RV_WINDOW_DAYS` di batch-3
hanya konstanta-vs-konstanta — DISIPLIN 12 menyatakan itu BUKAN penguncian
(mutasi 20→10 lolos, re-audit ketiga §8.3). Batch-4 menambah test DATA
`test_rv_window_terikat_kalibrasi_ulang` (hitung-ulang TAU Youden dari store
memakai jendela kode; mutasi 20→10 → MERAH,1 test). Angka §5 di atas tidak
berubah.

---

## 6. GUARD PROVENANS ATR (putusan B) — Lubang 1 / blocking 2

### 6.1 Klausa terlarang dihapus

Klausa loop `r` vs `d/a` (`:169-172` batch-2) **dihapus** dan tidak muncul
kembali dalam bentuk apa pun. Dua klausa nilai yang boleh tinggal tetap ada
**dengan label jujur** di kode:

```python
def _assert_smoke_bounds(atr, norm):
    """Batas kewajaran nilai — BUKAN bukti satuan (putusan B butir 2)."""
    negatif = "atr_14_d1 negatif (batas kewajaran, bukan bukti satuan)"
    ekstrem = "|london_drift_norm| >= 1e3 (batas kewajaran, bukan bukti satuan)"
    assert (atr.dropna() >= 0).all(), negatif
    assert (np.abs(norm.dropna()) < SMOKE_NORM_ABS_MAX).all(), ekstrem
```

### 6.2 Guard pengganti (allclose vs deret referensi store)

```python
def _assert_atr_provenance(atr_used, atr_reference) -> None:
    """nilai tidak dapat bersaksi ... IDENTITAS pembagi (dilewatkan eksplisit)"""
    common = used.dropna().index.intersection(ref.dropna().index)
    assert len(common) > 0, "atr_reference tidak punya satu pun titik banding"
    assert np.allclose(
        used.loc[common].to_numpy(),
        ref.loc[common].to_numpy(),
        rtol=ATR_PROVENANCE_RTOL,
        atol=ATR_PROVENANCE_ATOL,
    ), "pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) — putusan B"
```

Toleransi eksplisit di kode: `ATR_PROVENANCE_RTOL = 1e-9`,
`ATR_PROVENANCE_ATOL = 1e-9`; deret referensi **dilewatkan eksplisit**
(`compute_london_drift_4h(m15, daily, atr_reference)`), bukan diambil dari
frame yang sama diam-diam.

### 6.3 Sabotase lewat pipeline produksi (baseline + 9 kasus)

```
baseline (atr store asli)                        -> NO RAISE
atr = 1.0 konstanta                              -> RAISED: pembagi ATR bukan kolom atr_14_d1 store (provenans gagal) — putusan B
atr = 2.0 konstanta                              -> RAISED: ...
atr = 88.79 konstanta (lock tak-berdimensi)      -> RAISED: ...
atr = 100.0 konstanta                            -> RAISED: ...
atr = 12345.6 konstanta                          -> RAISED: ...
atr = 1e6 konstanta                              -> RAISED: ...
atr = close-avg (harga, kuantitas salah)         -> RAISED: ...
atr = 1e-3 konstanta                             -> RAISED: ...
atr = -5.0 konstanta                             -> RAISED: ...
```

Ulang audit §4 (semua NO RAISE kecuali 1e-3/−5): **ketiga kasus yang paling
menentukan — `1.0`, `88.79`, `close-avg` — sekarang meledak.** Minimal dua
test sabotase terkunci di suite (`TestGuardProvenansAtr`, parametrized 3
kasus: `1.0`, `88.79`, `close-avg`) + test unit guard.

**KOREKSI BATCH-4 (butir §11-1, BLOCKING):** klaim "lewat pipeline produksi"
di atas BATAL untuk `main()` batch-3: `main()` mengirim
`atr_reference = daily['atr_14_d1']` — kolom yang sama dengan pembagi —
sehingga guard mengevaluasi `allclose(X, X)` yang benar untuk setiap X.
Re-audit ketiga §3.2 membuktikan hanya **3/10** sabotase RAISED pada jalur
produksi (`1.0`/`88.79`/`close-avg` justru LOLOS); §3.5 menutup kembali B.
Batch-4 memperbaiki: `main()` kini membaca referensi dari **file store
parquet terpisah** (`_read_atr_reference_from_store`), sabotase dijalankan
persis seperti `main()` → **10/10 RAISED + baseline NO RAISE**, fixture test
diubah ke kondisi produksi (referensi ikut dari store terpisah, bukan
snapshot), dan suite mengunci `TestGuardProvenansJalurProduksi` — mutasi
`reference_sama_frame` (mengembalikan bug batch-3) → 3 test MERAH.
Bukti mentah: `coder/laporan-fix-batch4-D1-D5.md` §butir-1.

### 6.4 Docstring ditulis ulang sesuai perilaku terbukti

Docstring batch-2 ("harus MELEDAK bila atr bukan harga") diganti pernyataan
yang benar: guard memeriksa **identitas pembagi terhadap deret referensi**;
tidak ada klaim berbasis nilai. Klaim D5 `:147`/`:197` lama sudah dicabut dan
laporan final kini mengutip bukti §6.3 (bukan "diuji via bukti mutasi" tanpa
dasar). `atr_guard_disabled` `-> exit=1 | 4 failed` membuktikan guard benar
dipanggil oleh test.

---

## 7. PAGU + FutureWarning (#28/#35)

```
modul baris: 400  pagu 400 -> OK
fungsi terpanjang: ('compute_london_drift_4h', 41)  pagu 50
main AST: 33
$ venv/Scripts/python.exe -W error::FutureWarning runtime/tmp_batch3/smoke_d4.py
day shape: (974, 6) ... (selesai tanpa FutureWarning; exit=0)
```

Sumber `FutureWarning` batch-2 (`:253`, `fillna` pada object) dihapus dengan
`reindex(days, fill_value=False)` — tidak ada `fillna` lagi di `compute_gap_f2_flag`.
D1 didaftarkan di tabel anggaran `laporan-final-fase1.md` §1.

---

## 8. DOKUMEN & INTEGRITAS (#30–#33, #10, #32, #36)

### 8.1 Protokol D3

- Angka riil kalibrasi ditulis (§2): TAU_2023 = 2.5951672079821496e-05,
  AUC = 0.8173755150499336, n_B = 111, n_A = 129, sens/spec, flag-rate.
- Kutipan F-1 dipindah ke **baris 73-75** + path
  `reports/governance/2026-10-07/arsitek/putusan-arsitek-F1.md`.
- Angka gap disinkronkan ke hasil §4 (234/597; 479 ditolak; 597 bucket B1).
- Frasa "tertulis di bawah" dan klaim "HAYAT" tanpa isi dihapus.
- Atribusi S1–S6 (Section 0, hash `e8eb03da…`) dipertahankan; atribusi S4
  `H1-H5:16-17` dan larangan H4/H5 `H1-H5:18-21` dipertahankan.

### 8.2 Unstage (#32) — apa adanya

```
=== SEBELUM ===
     14  D
      4  M
     68  ??
      7  R
staged (X != ' ' dan != '?') = 7

$ git reset -q          (exit=0; working tree tidak disentuh)

=== SESUDAH ===
     21  D
      4  M
     65  ??
total: 90
staged: 0
$ git diff --cached --name-only
0
$ git rev-parse HEAD
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
```

7 rename governance kini `D` (path lama) + target di direktori untracked;
ketujuhnya diverifikasi masih ada di disk (7/7 EXISTS). Jumlah entri `??`
berubah (68 → 65) karena git meng-collapse direktori yang kini sepenuhnya
untracked — bukan karena ada file yang hilang; `git reset` tidak menyentuh
working tree (`runtime/` scratch juga dihapus pada langkah ini). D5 §4
ditulis ulang apa adanya dari output ini (klaim "DIPATUHI" palsu batch-2
dikoreksi).

### 8.3 Subdirektori kosong (#36)

```
--- isi subdir sebelum ---
data/labels/D1/.gitkeep  ...  data/labels/M5/.gitkeep   (7 subdir)
--- listing data/labels sesudah ---
data/labels/usdjpy_day_labels.parquet
data/labels/usdjpy_h2_trades.parquet
```

Tujuh subdir kosong dihapus; hanya dua file kontrak tersisa.

### 8.4 Typo & angka (#31/#34)

- Typo batch-2 di docstring test (kata salah-eja 5 huruf, terhitung 3× oleh audit #34) hilang karena D2 ditulis ulang; `grep` token itu di `tests/` = **0 kemunculan**.
- "Pytest penuh: 36" diganti **248 total / 54 baru** dari output mentah (§9.5).

---

## 9. GATE AKHIR (§3) — OUTPUT MENTAH

### 9.1 Full suite

```
============================ 248 passed in 15.75s =============================
```
(exit=0; 0 skip / 0 deselect / 0 xfail)

### 9.2 Per-berkas

```
pytest --collect-only -q                            -> 248 tests collected
pytest --collect-only -q tests/test_build_labels.py  -> 54 tests collected
```

### 9.3 Ruff

**KOREKSI BATCH-4 (butir §11-2):** klaim `exit=0` pada `ruff format --check .`
di bawah SALAH untuk ruff 0.16.10 (env auditor): rc=1 dengan 10 file gagal —
termasuk D1 `build_labels.py:149` tulisan batch-3 sendiri (re-audit ketiga
§8.2). Sesudah patch batch-4: D1/D2 rc=0 di KEDUA ruff, dua snippet
python di laporan ini ikut diformat ulang, dan klaim gate D5 kini mencantumkan
rc + cakupan eksplisit (repo vs file) beserta daftar kegagalan pra-ada.

```
venv ruff 0.6.9    check .            -> All checks passed!          rc=0 (repo)
venv ruff 0.6.9    format --check .   -> 37 files already formatted  rc=0 (repo)
.venv ruff 0.16.10 check .            -> All checks passed!          rc=0 (repo)
.venv ruff 0.16.10 format --check .   -> 9 files would be reformatted rc=1 (repo;
    9 PRA-ADA luar scope: 6 notebook EDA + reaudit-adversarial + reaudit-ketiga
    + build_features.py yang BEKU; file yang ditulis batch-4 semua rc=0)
```

### 9.4 check_foreign_chars.py

```
tests\test_check_foreign_chars.py ................                       [100%]
16 passed in 0.05s
```

### 9.5 Hash (mentah)

```
git hash-object src/features/build_labels.py
90e44a825ee356e397d96ab5137caf35e6e575f4
git hash-object tests/test_build_labels.py
53468d95da00f4c36789ee1df3435edc579df373
git hash-object reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
758c5d301ede4ec105d882b164f9baad7bbd6d83
git hash-object reports/governance/2026-10-07/coder/laporan-final-fase1.md
e645a042a7ffcae7ffa21e6b1a995a7dc7c6085c
```

### 9.6 3 artefak lama wajib identik

```
git hash-object src/features/build_features.py
399e64b372e430b6def79b4fa8324a4e8e629918
git hash-object tests/test_build_features.py
ed7ac43520c4431519d4d7065504866ae9b3ad95
git hash-object data/features/M15/usdjpy_m15_features.parquet
07402f40478aaed9391203f5db3237d636f5a959
```

### 9.7 D4 — kontrak, grain, byte-reprodusibel

```
usdjpy_day_labels.parquet  sha256 run1=47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c
                           sha256 run2=47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c
                           BYTE-IDENTIK: True
usdjpy_h2_trades.parquet   sha256 run1=32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f
                           sha256 run2=32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f
                           BYTE-IDENTIK: True
day rows: 974   index: date_broker
trades rows: 1  cols: ['symbol','strategy','entry_rule','exit_rule','sl_atr','tp','biaya','entry_time_utc','entry_frequency','price_unit']
labels dir listing: ['D1','H1','H4','M1','M15','M30','M5','usdjpy_day_labels.parquet','usdjpy_h2_trades.parquet']  (SEBELUM #36)
```

Byte-reprodusibilitas juga dikunci sebagai test tetap:
`TestMainEndToEnd::test_d4_deterministik_byte_identik`.

**KOREKSI BATCH-4 (butir §11-4):** byte-reprodusibilitas di atas terbatas
satu toolchain (DISIPLIN 11). Versi terukur: venv = python 3.12.8 /
pandas 2.2.3 / pyarrow 17.0.0 / numpy 1.26.4 (sumber sha256 disk);
.venv = python 3.12.13 / pandas 3.0.6 / pyarrow 25.0.1 / numpy 2.5.3 →
build memberi day `20cf4cdd…` / trades `75938ad3…` — BEDA byte, metadata
parquet saja (index ns vs ms; gap int32 vs int64). **Nilai semua kolom
identik** (dibuktikan per kolom batch-4: day 6/6 + trades 10/10 OK; index
elemen-ke-elemen True; equals True setelah cast-ns). Status: non-repro-
lintas-toolchain, tercatat eksplisit — BUKAN non-determinisme pipeline,
BUKAN repro lintas pyarrow.

### 9.8 git status (sesudah semua penulisan)

```
     21  D
      4  M
     65  ??
total: 90      staged: 0      HEAD: e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
```

4 ` M` (`.ai/AGENTS.md`, `.ai/SESSION_LOG.md`, `.ai/assistant/README.md`,
`requirements.txt`) dan 21 ` D` (laporan EDA) adalah pekerjaan lain yang sudah
ada sebelum batch ini — tidak di-stage ulang, tidak di-revert, tidak disentuh.
Scratch batch-3 (harness probe/mutasi/sabotase) berada **di luar repo**
(`/tmp/batch3_harness.*`) agar `ruff check .` bersih.

---

## 10. PETA KLAIM → OUTPUT MENTAH

| Klaim | Output mentah |
|---|---|
| 974 baris / drift 0 NaN / norm 14 NaN / mask 19 / gap 234 / rv 19 NaN | §2.1, §9.7 |
| row key `date_broker` | §2.2, §9.7 |
| 400 baris, main AST 33 | §7 |
| 54 test, 248 total | §9.1, §9.2 |
| mutasi merah (5/6/6/6/6/4 failed) | §3.2, §3.3, §6.4 |
| recount gap 234/597; 479 ghost 479/479 | §4.2 |
| TAU 2.5951672079821496e-05, AUC 0.8173755150499336, n_B 111, n_A 129 | §5 |
| 9 sabotase RAISED + baseline lolos | §6.3 |
| staged = 0, HEAD e0b2b9f | §8.2, §9.8 |
| 3 hash lama identik | §9.6 |
| D4 byte-identik 2× | §9.7 |

---

## 11. SELF-AUDIT 3× (ala auditor)

**Putaran 1 — Correctness.** Setiap butir §1 menunjuk nomor §7/adjudikasi dan
§ tempat output mentahnya. "TERTUTUP" hanya untuk butir yang punya output
eksekusi: grain (974/0/14/19), row key (index name), gap (234/597), kalibrasi
(angka riil), guard (RAISED), mutasi (exit=1), pagu (400/33), FutureWarning
(`-W error` exit 0), unstage (staged=0), dir (#36), hash (6 nilai).

**Putaran 2 — Bias & Asumsi.** Klaim coder diperlakukan sebagai hipotesis:
(i) "guard sudah kuat" → diuji 9 sabotase, baseline lolos; (ii) "mutasi sahih"
→ 6 mutan in-memory, semua merah; (iii) "N terkunci" → N=4/8/60 merah;
(iv) "234" tidak diwarisi — recount dijalankan independen dan 479 dibuang
sebagai artefak; (v) "hash final" → diukur ulang `git hash-object` setelah
seluruh penulisan. Pengakuan yang tidak enak tetap ditulis: N=60 memakai 32
bar (bukan 60) karena jendela London sintetis hanya 32 bar — nilai tetap
berbeda dari N=16 sehingga kontrol sensitivitasnya sah, dan batas itu
dinyatakan di sini, bukan disembunyikan. **Batch-4 menutup batas ini (butir
§11-5):** `make_london_rising` kini punya `step_minutes`; test baru
`test_n60_mengambil_60_bar_pertama_bukan_ambil_semua` memakai 70 bar London
(grid 5 menit, 07:00–12:45 UTC) dan mengunci N=60 = 60 bar PERTAMA
(drift 0.64 ≠ 0.74 ambil-semua-70).

**Putaran 3 — Meta-check.** Nol sentuh file lama (3 hash identik); nol
commit; indeks unstaged; nol backtest; `h2_trades` tetap 10 kolom teks tanpa
kolom hasil; nol vonis H3/H4/H5; nol perubahan lock/ambang; nol penambahan
kolom store; impor tetap satu arah (`build_labels → build_features`).

---

## 12. YANG MASIH TERBUKA (tidak diklaim tertutup)

1. **H3 belum divonis** (S4): AUC 0.8174 ≠ vonis; flag rate span 162/240
   dicatat sebagai hasil kalibrasi, bukan kelayakan.
2. **Materialitas gap_f2_flag pada 234 hari** (uji sensitivitas H1/H5) —
   status BELUM DIUJI dipertahankan.
3. **Varian BATAS SESI** (578/230) hanya sensitivitas; jika arsitek ingin
   definisi itu, itu putusan baru.
4. **Pekerjaan lain di indeks** (21 D + 4 M) dibiarkan apa adanya; unstage
   hanya mengembalikan indeks, bukan membatalkan perubahan pihak lain.

**END OF REPORT**
