# RE-AUDIT ADVERSARIAL KEDUA — Fix D1–D5

**Tanggal audit:** 2026-10-08
**Peran:** Auditor adversarial, deep dive. Tidak menulis kode. Read-only total terhadap worktree.
**Pengendali:** `arsitek\putusan-arsitek-fix-D1-D5.md` — git blob `ca57e7647e955ee0dfe68579db5dbef6216a427b` (terverifikasi). Menang atas ringkasan mana pun.
**Banding:** `Audit\reaudit-adversarial-D1-D5.md` (#14–#19, blocking 1–9), `arsitek\putusan-arsitek-H1-H5.md` (S1–S6), kontrak Fase 0, 3 artefak lama.

---

## 0. VERDICT

# **GAGAL**

Temuan #14, #15, #16, #17, #18, #19 **tidak ada yang tertutup penuh**. Blocker arsitek #2 (assert NYATA) **terbuka**. 16 temuan baru bernomor #20–#36, tiga di antaranya BLOCKER.

Yang benar-benar tertutup: keputusan (c), keputusan (d), fides-fidelitas jendela London, reaktivitas `compute_gap_f2_flag`, 3 hash artefak lama, gate ruff/pytest/foreign-chars, dan redaksi protokol S1–S6//20/H2.

---

## 1. TABEL PENUTUPAN #14–#19

### #14 — D1 hidup + D4 kontrak → **TERBUKA** (4 dari 7 sub-item gagal)

| Sub-item | Status | Bukti |
|---|---|---|
| `main()` selesai tanpa `KeyError` | ✅ TERTUTUP | `a2_02_main.py`: `main() COMPLETED without exception` |
| `london_drift_4h` = close-terakhir − open-pertama | ✅ TERTUTUP | `build_labels.py:212-214`; mutasi `drift_sign_flip` → **8 test merah** |
| `london_drift_norm` ada + `atr_14_d1` direferensikan | ⚠ TERBUKA | ada di `:220`, tetapi 214/1174 NaN — lihat #22 |
| **assert paritas NYATA (blocking 2)** | ❌ **TERBUKA** | **tautologi** — lihat §4 Lubang 1 |
| D4 tepat dua file kontrak, tidak byte-identik | ✅ TERTUTUP | sha256 `3507ff18…` vs `32eaf6b2…` |
| `day_label` tidak degenerate | ✅ TERTUTUP | trending 330 / range 324 / normal 320 / None 200 |
| `gap_f2_flag` tepat 234 hari | ❌ **TERBUKA** | **479** — lihat #23 |
| `rv_regime_flag` hidup via Q1(a) | ❌ **TERBUKA** | **0/1174 non-NaN** — lihat #24 |
| karantina 19 hari terbawa | ✅ TERTUTUP | `quarantine_mask==True` = 19 |

Reprodusibilitas D4独立 terkonfirmasi: run `main()` saya ke tmp **byte-identik** dengan yang di disk (`3507ff18f465fdc325c3bcda08e20e2b5e7661f8d786e65e37246f80517395fe`). Jadi D4 bukan sintetis — kelemahannya bukan fabrikasi.

---

### #15 — Jendela London + gap jujur → **TERBUKA**

**Bagian jendela: TERTUTUP penuh.**

```
is_london kode (local-hour 8-16) vs flag STORE  : 90041 / 90041  (100.00%)
disagreements                                   : 0
first-16 bar per broker-day IDENTIK             : 974 / 974  (100.00%)
'hour_utc' di D1                                : 1 kemunculan — hanya KOMENTAR di :52
compute_gap_f2_flag pada slice semua-penuh : 0 flagged (reaktif)
compute_gap_f2_flag pada slice semua-nol         : 1174 flagged (reaktif)
```

Tidak ada referensi fungsional `hour_utc` 8–12. Aturan 16-bar=100% benar-benar terbukti pada store produksi.

**Bagian gap: TERBUKA.** `gap_f2_flag` = **479 hari**, target arsitek **234**.详细内容 di #23.

---

### #16 — Bukti mutasi sahih → **TERBUKA**

Mutasi **nyata** (patch di kedua binding: modul + globals test module, via pytest plugin in-memory):

```
MUT=none exit=0   36 passed
MUT=classify_all_trending exit=1    4 failed, 32 passed   ✅
MUT=quarantine_all_false  exit=1    4 failed, 32 passed   ✅
MUT=threshold_9999        exit=1    4 failed, 32 passed   ✅
MUT=window_hour_utc_8_12  exit=1    1 failed, 35 passed   ✅ (tipis)
MUT=rv_not_implemented    exit=1    5 failed, 31 passed   ✅
MUT=tau_zero exit=1    2 failed, 34 passed   ✅
MUT=gap_all_zero exit=1    1 failed, 35 passed   ✅
MUT=london_first_n_60     exit=0   36 passed   ❌ TIDAK TERKEKANG
MUT=london_first_n_1/4/8/15  exit=0   36 passed ❌ SEMUA LOLOS
MUT=norm_all_zero         exit=1    8 failed, 28 passed   ✅
MUT=drift_sign_flip       exit=1    8 failed, 28 passed   ✅
```

Tiga cacat yang membuat #16 gagal meski12 mutasiosi greens:

**(a) 4 test `TestBuktiMutasi` adalah no-op.** `tests/test_build_labels.py:16` mengimpor `classify_day_label` dan `quarantine_mask` langsung. Test mem-patch `bl.classify_day_label` (atribut modul) lalu memanggil nama lokal — yang **tidak terjangkau**.

```
--- test_classify_day_label_cabut_all_trending_merah ---
value returned : 'range'
assert labels == 'range'  -> PASSES (test GREEN)
=> mutasi gut TIDAK PERNAH DIPANGGIL. Bukti ini tidak membuktikan apa pun.
--- test_quarantine_mask_cabut_all_false_merah ---
mask value : True    assert -> PASSES (GREEN); mutasi tidak pernah dipanggil
```

Empat test yang ditulis justru untuk membuktikan "test HARUS MERAH saat fungsi dicabut" justru **hijau saat fungsi dicabut**. Lihat #25.

**(b) `LONDON_FIRST_N` tidak terkunci sama sekali.** N = 1, 4, 8, 15, 60 → **semua 36 test hijau**. Hanya N = 0 (jendela kosong) yang merah. Semua fixture `make_m15_london` memakai `open=150.0, close=151.0` seragam, sehingga jendela mana pun menghasilkan drift = 1.0. Test tidak punya daya sensitivitas terhadap pemilihan jendela — persis kelas cacat yang #15本站i. Lihat #26.

**(c) 1 test tanpa assertion sama sekali.** `test_status_belum_diuji` (`test_build_labels.py:243-245`) hanya `pass`. Dihitung dalam 36. Lihat #27.

Gate: `230 passed in 19.61s`, nol skip/deselect/xfail, nol error sintaks/import ✅.

---

### #17 — Protokol lengkap → **TERBUKA** (14 dari 18 strlen ✅)

```
S1=5  S2=1  S3=2  S4=8  S5=1  S6=5
"kalibrasi in-sample"=2   "span terkunci"=3
"transformasi label"=2   "jam 15 UTC"=1   "1x"=2   "satuan harga JPY"=3
putusan-arsitek-H1-H5.md:16-17  = 2      (atribusi S4)            ✅
putusan-arsitek-H1-H5.md:18-21  = 2      (larangan H4/H5)        ✅
H1-H5:15-16 /16-17 / 18-19 / 20-21                                    ✅
"menggunakanspread" = 0  ✅ "3,648e-5" = 1  (dengan tag lock) ✅
RV_REGIME_THRESHOLD di D1 = 0 ✅   di protokol = 0 ✅
hash e8eb03daf994… (L13) = e8eb03daf994… ✅ MATCH
```

**Yang gagal:**

1. **Lubang 2 tidak diisi.**扫 grep: `n_B=0, n_A=0, sensivitas=0`, dan `numeric assignments found: NONE`. `TAU_2023 =` muncul 1× (sebagai definisi), `AUC =` 2× (sebagai definisi), `n per kelas` 3× (sebagai **persyaratan**). Arsitek L38-39 mewajibkan "Nilai TAU_2023 + AUC + n per kelas **wajib tertulis** di protokol sebagai hasil kalibrasi". Tidak ada satu pun angka.
2. **Klaim internal palsu.** `:177-178` "TAU_2023 + AUC + n per kelas **tertulis di bawah**" — tidak ada yang tertulis di bawahnya.
3. **`rv_regime_flag` "HAYAT"** (`:146`, `:147`, `:192`) — bertentangan dengan 1174/1174 NaN.
4. **"234 hari"** (`:171-174`) — bertentangan dengan D4 = 479.
5. **Kutipan F1 salah atribusi baris.** `:161` mengklaim "baris 36-38". F1 L36-38 berisi "Kolom harian (input H1/H3) invarian-bit terhadap kebenaran offset". Teks yang dikutip **benar-benar ada di L73-75**, tapi rujukan baris salah, dan **path-nya usang** (`2026-10-07\putusan-arsitek-F1.md`; file sudah pindah ke `arsitek\`). Lihat #33.

---

### #18 — Angka D5 jujur → **TERBUKA**

| Artefak | Diklaim D5 | Dihitung ulang saya | Status |
|---|---|---|---|
| `build_labels.py` | `b70dc179b8a1…` | `b70dc179b8a1…` | ✅ |
| `test_build_labels.py` | `c50870aa1657…` | **`83ef0efb215a…`** | ❌ **MISMATCH** |
| `protokol-H1-H2-H3.md` | `75168a8d6f07…` | `75168a8d6f07…` | ✅ |
| `laporan-final-fase1.md` | `10eb2d0a83ee…` | **`fc122959059e…`** | ❌ **MISMATCH** |
| `usdjpy_day_labels.parquet` | `3507ff18f465fdc3…` | `3507ff18f465fdc3…` | ✅ |
| `usdjpy_h2_trades.parquet` | `32eaf6b206c5107b…` | `32eaf6b206c5107b…` | ✅ |

D5 `:32` mengklaim "diukur dengan `git hash-object` **sesudah penulisan terakhir**". Klaim itu **salah untuk 2 dari 4 file**. Lihat #30.

**"213/19" (arsitek butir 8):** makna terverifikasi — `Audit\reaudit-adversarial-D1-D5.md:339,412` → full-suite = 213, baru = 19. Nilai kini seharusnya **230 / 36**.

```
full suite        : 230 tests collected
test_build_labels : 36 tests collected
D5 L151 mengklaim : "Pytest penuh: 36 passed"
```

Angka **36 adalah benar untuk `test_build_labels.py`, salah untuk "pytest penuh"**. Raw output D5 `:311-322` memang hanya berisi 1 file — jadi D5WEIHS mengetikai output parsial sambil melabelinya penuh. Lihat #31.

**Atribusi per-kelas: BENAR.** AST hitung = 4/4/5/3/2/2/6/2/4/1/3 = **36**, identik dengan D5 §6. Atribusi ini tertutup ✅.

**3 artefak lama: BENAR.**

```
build_features.py  399e64b372e4 == klaim == HEAD ✅
test_build_features.py ed7ac43520c4 == klaim == HEAD ✅
usdjpy_m15_features.parquet 07402f40478a == klaim ✅
```

---

### #19 — D5 jujur (narasi) → **TERBUKA**

**Tertutup:**

- `register_h2_strategy` membawa "jam 15 UTC" / "1x" / "satuan harga JPY" ✅ (`entry_time_utc='15'`, `entry_frequency='1x per broker-day'`, `price_unit='JPY'`, `sl_atr='1x ATR 14-hari (atr_14_d1, satuan harga JPY)'`)
- `.gitignore:24 = data/labels/` ✅, dan `check-ignore` mengonfirmasi kedua parquet ter-ignore ✅
- severity **#9 HIGH** ✅ (`:58`) dan **#10 BLOCKER** ✅ (`:59`) tercatat ✅
- SL dipisah dari normalisasi ✅ (`sl_atr` =1× ATR mentah satuan JPY)

**Yang gagal — klaim D5 yang salah:**

| D5 | Klaim | Bukti |
|---|---|---|
| `:114` | "Commit/stage: **DIPATUHI** — tidak ada stage" | ❌ **23 entri staged** |
| `:120` | "File luar D1-D4: **DIPATUHI** — hanya 5 file" | ❌ **87 entri status** |
| `:147` | "assert paritas "gagal bila pembagi bukan harga (**diuji via bukti mutasi**)" | ❌ **tidak diuji; dan tidak gagal** |
| `:197` | "_assert… assert paritas **nyata** (gagal bila pembagi bukan harga). **Benar.**" | ❌ klaim Scientist-level salah |
| `:159` | "Ruff format --check: **2 files** already formatted" |OCKER 2 file, bukan repo; repo = 37 ✅ |

`:147` dan `:197` bertentangan langsung dengan pengakuan coder sendiri di `:237` dan `:270` ("belum ada test terpisah yang membuktikan assert gagal saat atr disabot"). Pengakuan di §7 jujur, tetapi §5 dan §6 ocultar Sustained-nya. Ini persis pola yang harus saya hapl — klaim dulu, pengakuan belakangan.

**Bonus — inkonsistensi severity #10:** `:59` menaikkan LOW → **BLOCKER** **karena masalahnya sudah SELESAI** ("dua parquet identik sudah dihapus dan diganti dua varian berbeda"). Severity tidak boleh naik saat cacat hilang.

---

## 2. KEPUTUSAN (c) / (d)

### (c) `usdjpy_h2_trades.parquet` spec-only → **TERTUTUP** ✅

```
shape   : (1, 10)     dtypes: semua object
symbol = 'USDJPY'
strategy        = 'H2 M15 momentum'
entry_rule      = 'Close > open di jam terakhir (jam 15 UTC), 1x per hari-broker'
exit_rule       = 'Close < open di jam terakhir (jam 15 UTC)'
sl_atr          = '1x ATR 14-hari (atr_14_d1, satuan harga JPY)'
tp              = '2x ATR 14-hari (atr_14_d1, satuan harga JPY)'
biaya           = 'cost_basis mean sesi'
entry_time_utc  = '15'
entry_frequency = '1x per broker-day'
price_unit      = 'JPY'

banned result-token hits in column names : []
banned result-token hits in values        : []
any numeric result-bearing value?         : []
```

Nol kolom hasil dalam bentuk apa pun; bahkan nol nilai numerik. **Murni spesifikasi.** Tidak ada backtest yang bocor.

### (d) Tidak ada legacy/excluded di mana pun → **TERTUTUP** ✅

Scan repo-wide (`rglob`, excluding `.git`/`venv`):

```
usdjpy_labels.parquet             : TIDAK ADA
usdjpy_labels_excluded.parquet    : TIDAK ADA
usdjpy_day_labels_excluded.parquet: TIDAK ADA
*labels*.parquet                  : hanya data/labels/usdjpy_day_labels.parquet
```

Bersihan di disk dikonfirmasi asisten ✅. Catatan higiene (bukan pelanggaran): `data/labels/` masih memuat 7 sub-direktori kosong (`D1, H1, H4, M1, M15, M30, M5`, 0 B).

---

## 3. GATE + INTEGRITAS

```
pytest penuh            : 230 passed in 19.61s   ✅ 0 skip / 0 deselect / 0 xfail
ruff check              : All checks passed!     ✅ exit=0
ruff format --check .   : 37 files already formatted ✅ exit=0
check_foreign_chars.py  : exit=0  "OK: 103 file discan, tidak ada karakter asing" ✅
HEAD                    : e0b2b9e4b3…  ✅ cocok mandate, nol commit
3 hash artefak lama     : identik ✅
.gitignore:24 = data/labels/ ✅
```

**GAGAL — "tanpa stage"** (`git status --porcelain`: 87 entri = 23 staged + 64 untracked; nol unstaged):

```
R  reports/governance/2026-10-07/hipotesis_lock_v1.md        -> arsitek/hipotesis_lock_v1.md
R  reports/governance/2026-10-07/putusan-arsitek-B1.md        -> arsitek/putusan-arsitek-B1.md
R  reports/governance/2026-10-07/putusan-arsitek-F1.md        -> arsitek/putusan-arsitek-F1.md
R  reports/governance/2026-10-07/putusan-arsitek-H1-H5.md     -> arsitek/putusan-arsitek-H1-H5.md
R  reports/governance/2026-10-07/audit-fondasi-B1.md          -> audit/audit-fondasi-B1.md
R  reports/governance/2026-10-07/konfirmasi-R1-R2-R3.md       -> audit/konfirmasi-R1-R2-R3.md
R  reports/governance/2026-10-07/reaudit-F2-F3-F4.md          -> audit/reaudit-F2-F3-F4.md
  + requirements.txt, .ai/AGENTS.md, 14× reports/eda/progress/* (M, staged)
```

Gate "hanya file kontrak + D4" juga gagal — 87 entri, 0 dari 4 objek teks yang ter-track. Lihat #32.

---

## 4. LUBANG 1 — ASSERT PARITAS → **TERBUKA** (blocking 2 TIDAK terpenuhi)

Mandate: "mutasi sabotase ATR (pembagi non-harga): assert HARUS meledak."

**Kode (`build_labels.py:126-174`)**, tiga klausa:

```
:153  assert (atr_vals >= 0).all()          → hanya menangkap atr NEGATIF
:161  assert (np.abs(ratio) < 1e3).all()    → hanya menangkap |norm| ≥ 1000
:169  for r, d, a in zip(...):
:170      if a > 0:
:171          expected = d / a
:172          assert abs(r - expected) < 1e-6
```

Dan `:220`: `out["london_drift_norm"] = out["london_drift_4h"] / atr` — jadi `norm` **didefinisikan** sebagai `d/a`. Maka `:172` membandingkan `d/a` dengan `d/a`. **Tautologi murni untuk setiap `a > 0`.**

**Uji sabotase melalukan pipeline asli** (`daily["atr_14_d1"]` diganti konstanta, lalu `compute_london_drift_4h` dijalankan):

```
baseline: atr asli (harga)                    NO RAISE
sabotase: atr = 1.0 konstanta                 NO RAISE  ← pembagi non-harga LOLOS
sabotase: atr = 2.0 konstanta                 NO RAISE  ← LOLOS
sabotase: atr = 88.79 konstanta               NO RAISE  ← median lock, TAK BERDIMENSI, LOLOS
sabotase: atr = 100.0 konstanta               NO RAISE  ← LOLOS
sabotase: atr = 12345.6 konstanta             NO RAISE  ← LOLOS
sabotase: atr = 1e6 konstanta                 NO RAISE  ← LOLOS
sabotase: atr = close-avg (harga, kuantitas salah) NO RAISE ← LOLOS
sabotase: atr = 1e-3 konstanta                RAISED   ← hanya karena |norm|>1e3
sabotase: atr = -5.0 konstanta                RAISED   ← hanya karena negatif
```

Yang "melemak" hanya dua kasus yang tidak terkait satuan: negatif (klausus 1) dan pembagi sangat kecil (klausus 2). **Klausus 3 tidak pernah有价值.**

Paling membuktikan: **`atr = 88.79` — median `range/ATR` yang_dimensionsless_ dari lock — lolos tanpa meledak.** Justru inilah煞 yang seharusnya ditolak.

Docstring `:138-141` mengklaim: *"fungsi ini harus MELEDAK bila atr yang diberikan bukan harga (mis. … diganti ke besaran non-negatif acak atau ke harga lain yang tidak cocok)"*. Klaim itu **false**, dan persis terkontradiksi bukti di atas.

**Kesimpulan: syarat blocking 2 ("assert NYATA") BELUM tertutup. Lubang 1 = TERBUKA.**

---

## 5. LUBANG 2 — ANGKA KALIBRASI → **TERBUKA sebagai prasyarat Lapisan 3-H3**

Bukan kegagalan coder. Prosedur Q1(a) sudah ditulis lengkap dan benar di protokol `:119-131`: span2023-01-01..2023-12-31, label B = 2023-01-01..06-30, label A = 2023-07-01..12-31, Youden, warmup NaN dikecualikan, AUC in-sample, larangan OOS. Arsitek sudah memutus Boutique-nya.

Yang kurang hanya **eksekusi**: run prosedur, hitung `TAU_2023` + `AUC` + `n` per kelas, tulis angka riil ke protokol sebagai hasil kalibrasi. Grepekturasinya `NONE`.

Saya **tidak** memutus arsitektur di sini; ini登记 sebagai prasyarat yang tersisa.

---

## 6. TEMUAN BARU #20–#36

| # | Severity | Temuan | Bukti |
|---|---|---|---|
| **#20** | **BLOCKER** | **D4 tanpa row key.** `write_labels` memakai `to_parquet(index=False)` sehingga `DatetimeIndex date_broker` dibuang. 1174 bar daily tanpa satu pun kolom tanggal/broker. Tidak dapat dipakai hilir mana pun — bar tidak punya identitas. | `a2_02_main.py`: `columns in file: [6 kolom, nol kolom tanggal]`, `contains a date/broker column: False` |
| **#21** | **BLOCKER** | **200 bar hantu.** `compute_london_drift_4h` mengelompokkan per **UTC midnight** (`bars["broker_day"] = bars["utc"].dt.normalize()`, `:200`), sedangkan `daily_metrics` memakai **broker-day**. Hasilnya: 200 hari ada di grain UTC tapi absen di grain broker-day → 194 Minggu + 6 hari parsial (3–12 bar). Akibatnya **200 `day_label=None` + 200 `london_drift_4h=NaN` + 200 `quarantine_mask=None`** (dtype `object`), dan 12 di antaranya tetap membawa `gap_f2_flag=1`. Jumlah bar **1174 einzeln 200** dari 974 hari broker nyata. | `drift index n=1174` vs `daily index n=974`, `intersection=974`, `drift-only=200`; weekday `{6:194, 0:2, 2:2, 3:2}`; `days with >=1 London bar: 0/200` |
| **#22** | **HIGH** | **`london_drift_norm` marching band buta.** `:219` `atr = daily["atr_14_d1"].reindex(out.index)` — ATR ber-grain broker-day di-reindex ke index UTC-day. Drift hari-X dipasangkan dengan ATR hari-X yang **bukan hari yang sama**. 214 NaN (200 grain + 14 warmup). | `norm NaN=214/1174`, `non-NaN=960`; baseline 960 vs sabotase-konstanta 974 (konstanta tak punya warmup NaN) |
| **#23** | **HIGH** | **`gap_f2_flag` = 479, target 234.** Implementasi **cocok persis** dengan definisi arsitek (`m1_bars<15` ∧ bukan bucket tepi): hitung ulang independen saya = 479 juga. Tetapi tidak ada varian yang mereproduksi 234: definisi-arsitek=479, tanpa-exclude-edge=607, broker-day+exclude-edge=0. Arsitek L86-87: "**selisih = gagal**". | `a2_03_gap.py` + `a2_11`:479 / 607 / 0 vs target 234 |
| **#24** | **HIGH** | **`rv_regime_flag` 1174/1174 NaN.** `_tau_2023_from_protocol()` (`:293`) `return None`. Kolom ada tapi **nol informasi** — persis pola "parquet tanpa kolom RV bermakna" yang Q1(a) harus hilangkan (arsitek L16-20). Test justru **mengunci** keadaan mati (`test_tau_none_from_protocol`, `test_returns_nan_when_tau_not_set`). | `rv_regime_flag non-NaN : 0/1174`; `RV_REGIME_THRESHOLD` = 0 ✅ (konstanta fiktif benar dihapus) |
| **#25** | **MEDIUM** | **4 test `TestBuktiMutasi` adalah no-op.** Patch `bl.X` tidak terjangkau direct-import di `:16`; test hijau justru saat fungsi dicabut. | `a2_07_mutasi_binding.py`: "PASSES (test GREEN) → mutasi gut TIDAK PERNAH DIPANGGIL" |
| **#26** | **MEDIUM** | **`LONDON_FIRST_N` nol coverage.** N = 1/4/8/15/60 → 36 hijau. Fixture `make_m15_london` open/close seragam ⇒ semua jendela = 1.0. | `london_first_n_*` exit=0 semua |
| **#27** | **MEDIUM** | **`test_status_belum_diuji` tanpa assertion** (`pass`), dihitung dalam 36. | AST: `tests with NO assert = 1` |
| **#28** | **MEDIUM** | **Pagu baris dilanggar.** D1 = **474** baris (pagu 400, "anggaran tak bergerak" L62); `main` = **66** baris AST (pagu 50). D5 §1 **tidak mendaftarkan `build_labels.py` sama sekali** di tabel anggaran. | AST: `physical474 *** OVER by 74 ***`, `('main', 66)` |
| **#29** | **MEDIUM** | **`_daily_from_m15` 39 bar kode mati.** Definisi `:85`, dirujuk **hanya** di docstring `:193`. Docstring itu juga **menyesatkan**: menyatakan `daily` berasal dari `_daily_from_m15`, padahal yang sampai ke guard adalah `daily_metrics`. | grep: hanya L85 (def) + L193 (docstring) |
| **#30** | **MEDIUM** | **2 hash D5 salah.** `test_build_labels.py` dan `laporan-final-fase1.md` sendiri. | `c50870aa…` vs `83ef0efb…`; `10eb2d0a…` vs `fc122959…` |
| **#31** | **MEDIUM** | **"Pytest penuh: 36 passed" salah.** Full suite = 230. Raw output D5 hanya berisi 1 file. | `230 collected` vs `36 collected (test_build_labels.py only)` |
| **#32** | **HIGH** | **"Tanpa stage: DIPATUHI" salah.** 23 entri staged, termasuk 7 rename governance + `requirements.txt` + 14 laporan EDA. | `git status --porcelain` |
| **#33** | **LOW** | **Kutipan F1 salah atribusi baris + path usang.** Klaim "baris 36-38"; isi sebenarnya di **73-75**. Path menunjuk `2026-10-07\putusan-arsitek-F1.md`, sudah pindah ke `arsitek\`. | `F1 L36-38` = "Kolom harian … invarian-bit"; kalimat kutipan di `L73-75` |
| **#34** | **LOW** | **Typo "HIUGO"** (harusnya "HIJAU") muncul 3× di docstring test baru. | `grep HIUGO` = 3 |
| **#35** | **LOW** | **`FutureWarning` pandas** di `build_labels.py:253` saat runtime (`fillna` on object). Tidak tertangkap ruff/test. | 3× warning pada setiap eksekusi |
| **#36** | **LOW** | `data/labels/` menyisakan 7 sub-direktori kosong. | listing `D1 H1 H4 M1 M15 M30 M5` 0 B |

---

## 7. SYARAT TERSISA YANG EKSPLISIT DAN MINIMAL

Tidak mengulang yang sudah tertutup.

**Prasyarat data/kontrak**
1. Pulihkan row key D4: tulis `date_broker` sebagai kolom (atau `index=True`) sehingga setiap bar daily punya identitas. — #20
2. Satukan grain ke **broker-day** tunggal di seluruh rantai (`compute_london_drift_4h`, `compute_gap_f2_flag`, `atr_14_d1` reindex); vars `broker_day` harus berisi broker-day sungguhan. Hilangkan 200 bar hantu; hasil*D4 harus 974 hari broker. — #21, #22
3. **Adjudikasi arsitek untuk #23:** implementasi cocok definisi Q3(a) tetapi menghasilkan 479, bukan 234, dan 234 tidak tereproduksi dari data mana pun dengan definisi mana pun yang saya coba. Arsitek harus memutuskan: koreksi definisi, koreksi target, atau rumuskan ulang. Auditor tidak memutus ini.

**Prasyarat prosedur (bukan kegagalan coder)**
4. Jalankan prosedur Q1(a): hitung `TAU_2023` (Youden, span 2023-01-01..12-31, B=Jan–Jun, A=Jul–Des), `AUC` in-sample, `n` per kelas; **tulis angka riil** ke `protokol-H1-H2-H3.md` §2 sebagai hasil kalibrasi; hapus kalimat "tertulis di bawah" yang tidak terpenuhi dan klaim "rv_regime_flag HAYAT" sampai kolom berisi nilai. — Lubang 2, #24

**Prasyarat kualitas kode**
5. Guard satuan yang **sabenar**: klausus `norm == d/a` harus dihapus atau diganti pemeriksaan yang benar-benar membedakan pembagi harga dari pembagi non-harga (mis. zmadz Profil ATR store terhadap pembagi, dengan toleransi); minimal ada **satu test** yang menyabot `atr` ke konstanta non-harga (1.0, 88.79) dan meng（或）assert meledak. — Lubang 1 / blocking 2, #22
6. Perbaiki 4 test `TestBuktiMutasi` agar benar-benar menguji (patch nama di globals test module, atau `monkeypatch.setattr(test_module, ...)`), lalu buktikanuite merah pada mutasi gut-total. — #25
7. Kunci `LONDON_FIRST_N = 16` dengan fixture yang **sensitif** terhadap jendela (open/close berbeda antar bar di dalam & di luar jendela16) sehingga N = 4/8/60 merah. — #26
8. Hapus `test_status_belum_diuji` atau beri assertion nyata. — #27
9. Turunkan D1 ke ≤ 400 baris dan `main` ke ≤ 50 baris AST; hapus `_daily_from_m15` (kode mati) dan perbaiki docstring `:193`. — #28, #29
10. Perbaiki `FutureWarning` `build_labels.py:253`. — #35

**Prasyarat dokumen & integritas**
11. Hitung ulang dan tempelkan 4 hash git yang benar **setelah** penulisan terakhir; perbaiki "Pytest penuh" menjadi **230 total / 36 baru**. — #30, #31
12. Perbaiki atribusi baris kutipan F1 ke **73-75** dan path ke `arsitek\putusan-arsitek-F1.md`; sinkronkan angka "234 hari" dengan hasil adjudicasi #23. — #33
13. **Unstage全部 23 entri** (atau dapatkan persetujuan eksplisit untuk rename governance), lalu jalankan ulang `git status` dan perbarui D5 §4 "Commit/stage: DIPATUHI". — #32
14. Perbaiki severity #10 di D5 — BLOCKER pada temuan yang sudah tertutup adalah inkonsistensi logis; beri status jelas (TERTUTUP) atau turunkan. — §1 #19

---

## 8. SELF-AUDIT 3× ADVERSARIAL

**Putaran 1 — Correctness.** Tiap item tertaut ke temuan bernomor: jendela London → #15-bagian-1; gap → #23; mutasi → #25/#26/#27; protokol → #17; hash/angka → #18/#30/#31; (c)/(d) → §2; Lubang 1 → §4; Lubang 2 → §5. Setiap "TERTUTUP" bertumpu pada bukti eksekusi independen: run `main()` byte-identik, patch kedua-binding via pytest plugin, scan 90.041 bar flag sesi, `git hash-object` + `sha256` dihitung ulang, `rglob` repo-wide, AST untuk pagu dan komposisi test. Tidak ada "TERTUTUP" yang berbasis narasi.

**Putaran 2 — Bias & Asumsi.** Klaim coder diperlakukan sebagai hipotesis: "assert diperkuat" saya uji dengan 9 sabotase; "diuji via bukti mutasi" saya buktikan no-op; "berkas mutasi sahih" saya buktikan tidak mengunci N; "TAU+AUC+n tertulis" saya buktikan `NONE`; "234 hari" saya buktikan 479; "tanpa stage" saya buktikan 23 staged; "hash setelah penulisan terakhir" saya buktikan 2 mismatch.lubang 1/2 **tidak** diasumsikan tertutup meski D5 §5 §6 mengklaim "Benar". Pengakuan coder di §7 (dua lubang) saya **terima** dancfc kan sebagai pembuka, bukan tuduhan — tapi pengakuan itu dikontradiksi oleh §5/§6, dan kontradiksi itulah yang saya laporkan._

**Putaran 3 — Meta-check.** Read-only total dip upheld: seluruh output rebuild diarahkan ke `C:\Users\Fajar\AppData\Local\Temp\opencode\rf234\`; semua mutasi in-memory via monkeypatch/substitusi Series pada salinan di memori; **tidak satu byte pun** di worktree berubah — 3 hash artefak lama tetap `399e64b3`/`ed7ac435`/`07402f40`, `HEAD` tetap `e0b2b9f`. Tidak menulis kode produksi. **Tidak memutus arsitektur**: #23 saya eskalasikan sebagai adjudikasi arsitek, Lubang 2 saya nyatakan prasyarat Lapisan 3-H3 (prosedur sudah diputus arsitek; yang kurang eksekusi), bukanvonis. Tidak ada vonis H4/H5, tidak menyentuh H6+/EDA/lock, tidak melebar ke `hipotesis_lock_v1.md`.

---

**RE-AUDIT KEDUA — VERDICT: GAGAL**
