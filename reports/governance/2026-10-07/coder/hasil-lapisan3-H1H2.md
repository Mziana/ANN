# Hasil Lapisan 3 Batch-1 — Eksekusi S-H1 + S-H2 (Coder)

**Peran pelaksana:** Coder (`.ai/AGENTS.md` v3.0 §26: implementasi + self-audit; DILARANG audit sendiri, DILARANG memutus arsitektur). Semua label "GUGUR/TAHAN" di dokumen ini adalah **keluaran formula lock yang dihitung skrip**, bukan putusan coder. Vonis resmi + penilaian adversarial atas dokumen ini tetap wewenang Auditor/Arsitek (§26–§27).

**Tanggal eksekusi:** 2026-10-09 (mulai 01:33:44 +07). **HEAD:** `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` (tidak berubah; [O1]).

**Brief/spec tunggal:** `reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md`, blob `fc29f6fa3595a89b918627dbdc71cfff82d8ebed`.

**Gate spec:** hash spec di disk == nilai yang disyaratkan prompt/spec → **COCOK**; eksekusi diizinkan (§2.1). Bila berbeda satu hex, tugas berhenti + eskalasi — tidak terjadi.

**Kontrak:** `.ai/AGENTS.md` v3.0 §5 (tabel Klaim & Bukti), §20 (anti-halusinasi; output asli ditempel), §21 (uji dulu, simpulkan kemudian), §26 (peran). Aturan besi spec: **klaim tanpa output mentah = GAGAL**.

---

## 0. Ringkasan hasil (angka mentah di §4–§5)

| Uji | Hasil (keluaran formula) | Angka penentu | Blok |
|---|---|---|---|
| S-H1 — vonis H1 real-time (identifikasi H+1 pagi, data t-1 saja) | **GUGUR** | Kriteria (i): CI95 selisih median drift `[-0.02668182694022586, +0.05242264543726398]` memuat 0 → kriteria (i) terpenuhi. Kriteria (ii): chi2 = 3.333835311042838, p = 0.18882820311496487 ≥ 0.01 → tidak terpenuhi | [O5][O6] |
| S-H2 — backtest strategi Q2 + VR OOS | **GUGUR** | Kriteria EV: median EV-per-trade ≤ 0 pada **3/3 tahun** (2023 `-0.016099999999990906`; 2024 `-0.06060000000000443`; 2025 `-0.044099999999982493`) → terpenuhi. Kriteria VR: rata-rata VR = `1.0265420777270247` > 1 → tidak terpenuhi | [O11][O12] |
| Gate S1 (prasyarat S-H1) | **LULUS presisi penuh** | 9/9 checks bit-exact vs angka referensi [O8] dokumen H3 (n 330/324; median; CI95; chi2; p; verdict) | [O5] |
| Divergence check Q1 | **Tidak ada divergensi** | Real-time GUGUR searah M1 GUGUR → M1 disitir sebagai anotasi (Uji-1 IMMATERIAL: gap-flag bukan penggerak); tidak memicu eskalasi wajib | [O8] |

Catatan arah: kedua GUGUR adalah hasil formula dari kriteria yang sudah terkunci sebelum data evaluasi dilihat (spec :179-241); **tidak ada** ambang/rule/split/varian/strategi yang ditambah pasca-lihat-hasil (S-B.3). S-H2 memakai konfirmasi `day_label` beku D4 T-1, bukan label real-time S-H1 (S-B.10; kopling dua arah tidak ada).

---

## 1. Manifest parameter (§3a) — setiap nilai punya sumber; nilai tanpa sumber = GAGAL

Baris "spec" = `spesifikasi-lapisan3-H1H2.md` (blob `fc29f6fa…`); "lock" = `hipotesis_lock_v1.md` (blob `9720280320…`); "cfg" = `configs/data.yaml` (blob `e277d67e…`); "int" = keputusan operasional yang ditetapkan **sebelum** run dan dilaporkan (§4.3/§7). Angka desimal disalin, bukan diketik dari ingatan.

| # | parameter | nilai yang dipakai | sumber (spec §/baris) |
|---|---|---|---|
| 1 | jam entry / bar sinyal | bar M15 yang **tutup** 15:00 UTC; kolom `time` = waktu buka → bar `time` = 14:45 UTC | spec Q2(a) :98 |
| 2 | frekuensi entry | 1x per hari-broker; bar tidak ada (gap) → FLAT, dihitung hari-tanpa-sinyal | spec :99-100 |
| 3 | syarat entry | `close > open` pada bar sinyal | spec :99 |
| 4 | konfirmasi | `day_label` **BEKU D4** hari T-1 == "trending" (bukan label real-time S-H1) | spec :101 + S-B.10 |
| 5 | harga entry | close bar sinyal | spec :105 |
| 6 | ATR | `atr_14_d1` hari T-1, satuan harga **JPY mentah** | spec :105-106 |
| 7 | SL | entry − 1× ATR | spec :106 |
| 8 | TP | entry + 2× ATR | spec :106 |
| 9 | monitoring | mulai bar M15 **sesudah** bar entry, sampai batas hari-broker | spec :108 |
| 10 | prioritas intra-bar | SL > TP > sinyal-exit | spec :112 |
| 11 | exit sinyal | bar `close < open` → exit pasar pada close bar itu | spec :110-111 |
| 12 | time-stop | exit pada close bar M15 terakhir hari T | spec :111-112 |
| 13 | cost London | 0.61 pip | spec :115-117 + cfg `cost_basis.by_session` |
| 14 | cost NewYork | 0.69 pip | idem |
| 15 | cost Tokyo | 0.62 pip | idem |
| 16 | cost Sydney | 0.8 pip | idem |
| 17 | fallback label "Off" | 0.65 pip (`cost_basis.default`) | spec :116-117 + cfg |
| 18 | pip_size USDJPY | 0.01 → JPY: pip × 0.01 (London 0.0061 JPY) | spec :119 + cfg `spread.pip_size` |
| 19 | EV per trade | `exit − entry − cost_JPY` | spec :118-119 |
| 20 | pengecualian hari H2 | TIDAK ADA (karantina & gap-flag tetap ditradingkan; overlay hanya deskriptif) | spec :120-123 |
| 21 | universe H2 | bar M15 store B1, tahun `date_broker` 2023/2024/2025 (2026 dikecualikan penuh) | spec :96-97, :211 |
| 22 | populasi H1 | INK 974 hari-broker (varian tunggal per Uji-1 IMMATERIAL) | spec :147 + :32 |
| 23 | ambang real-time S-H1 | median expanding `ratio_path` & `range_atr` atas hari SEBELUM T (strictly past), dari `daily_metrics` runtime jalur D1 read-only | spec :151-155 |
| 24 | burn-in S-H1 | riwayat minimum 60 hari-broker; hari tanpa riwayat = non-evaluable, dilaporkan n + rentang | spec :157-159 |
| 25 | klasifikasi real-time | trending = `>` kedua median; range = `<=` kedua median; else normal; NaN → normal | spec :160-162 |
| 26 | drift S-H1 | kolom `london_drift_norm` BEKU D4, bertanda | spec :161 |
| 27 | dropna | per kolom uji (identik M1) | spec :163 |
| 28 | karantina S-H1 | inklusif identik M1 (mask dipertahankan) | spec :163 |
| 29 | bootstrap kriteria (i) | percentile hari-level, dua himpunan disjoin — label "unpaired (disjoint)" | spec :180-182 + P-2 |
| 30 | B bootstrap | 10000 | spec :182 |
| 31 | seed bootstrap | 20261006 | spec :182 |
| 32 | alpha | 0.01 (kriteria ii; alpha lapor sign test) | spec :186, :191 |
| 33 | koreksi Yates | TANPA koreksi | spec :187 |
| 34 | tahun kriteria (ii) S-H1 | tahun utuh 2023–2025 (2026 parsial dikecualikan) | spec :186-187 |
| 35 | ambang (i) S-H1 | CI95 memuat 0 → GUGUR | spec :183 |
| 36 | ambang (ii) S-H1 | p < 0.01 → GUGUR | spec :187 |
| 37 | hasil S-H1 | GUGUR bila salah satu kriteria; TAHAN bila keduanya negatif | spec :189-190 |
| 38 | ambang EV H2 | median EV-per-trade ≤ 0 pada ≥ 2 tahun → GUGUR (deskriptif wajib: n, mean, % positif) | spec :229-232 |
| 39 | ambang VR H2 | rata-rata VR OOS ≤ 1 → GUGUR (satu angka penentu) | spec :240 |
| 40 | resep VR (verbatim EDA) | r = ln(C_t/C_t-1); no-gap = buang baris `utc.diff() > 15 menit`; `variance_ratio` cumsum overlapping ddof=1; horizon 5/15/60; rata-rata = mean ketiganya | spec :234-238 (`scripts/_build_eda03.py:177-181,421-448`) |
| 41 | angka referensi [O8] (gate S1) | n_trending 330; n_pembanding 324; median 0.02948996641114935 / 0.015065793016650224; CI95 [-0.02729045556350576, +0.052787080233690914]; chi2_2xk 0.7666041417663041; p_2xk 0.6816069745648556; verdict GUGUR | spec :166-170 (identik `hasil-lapisan3-H3.md` [O8]) |
| 42 | tahun = | `date_broker` store B1 (bukan UTC; `utc.normalize()` dilarang) | spec :113 + S-B.9 |
| 43 | grain | satu-satunya grain = hari-broker tunggal | spec :147, S-B.9 |
| 44 | jenjang label bootstrap | "unpaired (disjoint)" day-level; resampling terpisah dua himpunan | spec :180-182 + standing rule P-2/F-3 |
| 45 | nilai batch tambahan | tidak ada: TAU_alt/varian/ambang/rule/strategi baru = 0 | spec S-B.1-3 |

---

## 2. Bukti baca (§2c) + kutip-balik angka (§3b) + satuan (§3c) + path/nama (§3d)

### 2.1 Bukti baca — ditempel SEBELUM [O1]

Dibaca utuh sebelum satu baris eksekusi dijalankan: `.ai/AGENTS.md` v3.0 (705 baris; §5 tabel Klaim & Bukti, §20 anti-halusinasi, §21 protokol empiris, §26 peran) dan spec Batch-1 (369 baris, satu-satunya sumber instruksi; bila prompt vs spec berselisih, spec menang). Sumber pendukung yang dibaca langsung: lock H1/H2, putusan H1-H5, protokol (pra-registrasi H2 :37-77), standing rule P-1/P-2/P-3, riwayat [O8] dokumen H3, resep VR di `scripts/_build_eda03.py`.

```
BUKTI BACA (git hash-object):

fc29f6fa3595a89b918627dbdc71cfff82d8ebed  reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md
9720280320dcc813d422d6f540e37847b70571ff  reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md
e8eb03daf994051600258cf412ec9e9af65d800c  reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
bc17e5de6cfefb355fe7418acd2a3a0d8b461212  reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
c643c1c934055d1b85d972f4e2e2f65d8d57a69f  reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md

Gate spec: menuntut fc29f6fa3595a89b918627dbdc71cfff82d8ebed -> COCOK (eksekusi diizinkan).
```

Catatan penentuan "putusan H3": dokumen yang dimaksud = `arsitek/putusan-lapisan3-H3.md` (blob `c643c1c934055d1b85d972f4e2e2f65d8d57a69f`). Spec S0 sendiri merujuk "Standing rule P-1/P-2/P-3, blob `c643c1c93…`" — hash bertemu nilai-ke-nilai, jadi tidak ada pemilihan dokumen pasca-hoc.

### 2.2 Kutip-balik angka presisi-penuh (§3b) — gate S1

Angka referensi disalin dari spec :166-170 (identik dengan [O8] dokumen H3, dibaca ulang, bukan dari ingatan):

- n_trending **330** / n_pembanding **324**
- median **0.02948996641114935** / **0.015065793016650224**
- CI95 **[−0.02729045556350576, +0.052787080233690914]**
- chi2_2xk **0.7666041417663041**, p_2xk **0.6816069745648556**
- verdict **GUGUR**

Hasil reproduksi S1: **LULUS bit-exact 9/9 checks** (blok [O5]) — mismatch apa pun = GAGAL-eksekusi (skrip menulis JSON alasan + `sys.exit(2)`, S2 tidak dijalankan); tidak terpicu. Literal yang dipakai skrip ada di konstanta `O8` `sh1.py` (disalin dari dokumen) dan dipakai sebagai pembanding `==` presisi penuh, bukan `isclose` (standing rule P-1).

### 2.3 Satuan dan waktu (§3c) — konversi ditulis tiap langkah

- **Jam entry = 15:00 UTC** (bar M15 yang TUTUP tepat pada 15:00 UTC). Kolom `time` processed = waktu **buka** bar (diverifikasi dari data: bar pertama broker-day = 22:00 UTC = 00:00 broker wall), sehingga bar sinyal = `time` **14:45 UTC**. Bukan jam broker, bukan `utc.normalize()`.
- **Tahun = `date_broker` store B1** (bukan tahun UTC). S-H1 memakai `date_broker` D4; S-H2 memakai `date_broker` bar store → tahun trade 2023/2024/2025.
- **ATR = `atr_14_d1` hari T-1, satuan harga JPY mentah** (bukan normalisasi harga/harga) → dipakai langsung pada SL/TP (JPY).
- **Biaya:** `cost_basis` dalam **pip** × `pip_size` USDJPY **0.01 JPY/pip**. Ditulis tiap langkah: London 0.61 × 0.01 = **0.0061 JPY**; NewYork 0.69 × 0.01 = 0.0069; Tokyo 0.62 × 0.01 = 0.0062; Sydney 0.8 × 0.01 = 0.0080; fallback "Off" 0.65 × 0.01 = 0.0065. **EV (JPY) = harga_exit − harga_entry − cost_JPY**.
- Sesi bar entry diambil dari kolom beku `session_label` store B1 pada bar 14:45 (semua 974 bar = London; terverifikasi di [O9]/deskriptif [O10]: n_fallback_label_Off = 0).
- Drift S-H1 = `london_drift_norm` (tak-berdimensi) bertanda; R1 memakai `london_drift_4h` (JPY mentah) sebagai non-penentu.

### 2.4 Path dan nama (§3d) + jalur read-only D1

- Dokumen ini: `reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md` (nama persis kontrak).
- Skrip analisis HANYA di `%TEMP%\opencode\l3h1h2` (mesin ini: `/tmp/opencode/l3h1h2`, git-bash): `sh1.py` (S-H1), `sh2.py` (S-H2), plus pembantu `_extract.py`/`_asm.py`. Tidak ada skrip yang ditulis ke repo (C2; [O16]).
- `main()`/`write_labels()` produksi **DILARANG di jalur eksekusi** — tidak pernah dipanggil; impor hanya fungsi baca (bukti grep):

```
$ grep -n "TAU\|rv_regime\|filter" sh1.py sh2.py
(kosong = tidak ada TAU/filter di jalur eksekusi)

$ grep -n "write_labels\|rt.main(\|build_labels.main\|build_features.main" sh1.py sh2.py
(kosong = write_labels/main() produksi DILARANG tidak dipanggil)

$ grep -n "from src" sh1.py sh2.py
sh1.py:32:from src.features.build_features import daily_metrics, load_processed  # noqa: E402
sh1.py:33:from src.features.build_labels import (  # noqa: E402
sh1.py:38:from src.utils.config import load_config  # noqa: E402
sh2.py:39:from src.features.build_features import (  # noqa: E402
sh2.py:45:from src.utils.config import load_config  # noqa: E402
```

- D4 di disk tidak ditimpa: sha256 + mtime before/after identik ([O3] vs [O17]).

---

## 3. Metode eksekusi (ringkas, agar auditor bisa mereproduksi)

1. **Gate hash spec** (§2.1): `git hash-object` spec == `fc29f6fa3595a89b918627dbdc71cfff82d8ebed` → lanjut. Tidak ada dokumen lain yang dibaca sebagai sumber instruksi.
2. **Harness** `sh1.py`: `load_config("data")` + M1/M15 (semua tahun) → `daily_metrics` + `_read_atr_reference_from_store` + `_build_daily_labels` (jalur D1 read-only, tanpa `main()`) → **S0** provenans bit-exact build vs D4 → **S1** gate reproduksi [O8] (STOP bila mismatch) → **S2** klasifikasi real-time + 2 kriteria → **S3** suplemen + divergence Q1. Harness `sh2.py`: **S0** provenans + deskriptif 778 hari → **S1** backtest 140 trade → **S2** VR.
3. **Determinisme:** tiap harness dijalankan **2x**; `sha256` berkas angka-hasil dibandingkan (`cmp` IDENTIK) — [O13]. Tidak ada timestamp di keluaran.
4. **Tanpa TAU/filter:** jalur eksekusi tidak mengimpor `TAU_2023`/`rv_regime_flag` dan tidak memuat kata "filter" (grep = 0; bukti di §2.4).
5. **Kronologi:** baca spec/lock/putusan/protokol → gate hash spec → tulis harness di `%TEMP%\opencode\l3h1h2` → sh1 run1+run2 → sh2 run1+run2 (satu koreksi pra-hasil: hari `close<=open` = FLAT sesuai Q2(a), bukan galat) → spot-check trade[0] → bukti C1/C2/C3 → tulis dokumen ini → gate C4 → [O14]-[O18] → C9 → C8.

**Blok [O1] — C1: HEAD + branch + waktu mulai (sebelum tugas):**

```
TASK START (local, +07): 2026-10-09 01:33:44

$ git rev-parse HEAD
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169

$ git branch --show-current
main
```

**Blok [O2] — C2 BEFORE (status porcelain -uall, jalur dalam lingkup; 42 baris):**

```
 D reports/eda/progress/audit_kesesuaian_nb00_nb04.md
 D reports/eda/progress/laporan_fix_audit_fragmen.md
 D reports/eda/progress/laporan_revisi_fragmen_4b.md
 D reports/eda/progress/laporan_tahap_0_reuse_check.md
 D reports/eda/progress/laporan_tahap_10_autocorr_fix.md
 D reports/eda/progress/laporan_tahap_1_pin_deps.md
 D reports/eda/progress/laporan_tahap_2_nb00_setup.md
 D reports/eda/progress/laporan_tahap_3_returns.md
 D reports/eda/progress/laporan_tahap_4_volatility.md
 D reports/eda/progress/laporan_tahap_5_autokorelasi.md
 D reports/eda/progress/laporan_tahap_6_swing_level.md
 D reports/eda/progress/laporan_tahap_7_swing_level_fix.md
 D reports/eda/progress/laporan_tahap_8_volatility_fix.md
 D reports/eda/progress/laporan_tahap_9_figures_fix.md
?? reports/eda/progress/00-setup/laporan_tahap_0_reuse_check.md
?? reports/eda/progress/00-setup/laporan_tahap_1_pin_deps.md
?? reports/eda/progress/00-setup/laporan_tahap_2_nb00_setup.md
?? reports/eda/progress/01-returns/laporan_tahap_3_returns.md
?? reports/eda/progress/02-volatility/laporan_tahap_4_volatility.md
?? reports/eda/progress/02-volatility/laporan_tahap_8_volatility_fix.md
?? reports/eda/progress/03-autocorr/laporan_tahap_10_autocorr_fix.md
?? reports/eda/progress/03-autocorr/laporan_tahap_5_autokorelasi.md
?? reports/eda/progress/04-swings-levels/laporan_tahap_6_swing_level.md
?? reports/eda/progress/04-swings-levels/laporan_tahap_7_swing_level_fix.md
?? reports/eda/progress/05-figures/laporan_tahap_9_figures_fix.md
?? reports/eda/progress/06-regimes/.gitkeep
?? reports/eda/progress/06-regimes/laporan_tahap_13_report.md
?? reports/eda/progress/INDEX.md
?? reports/eda/progress/audit/audit_kesesuaian_nb00_nb04.md
?? reports/eda/progress/fragmen-spread/laporan_fix_audit_fragmen.md
?? reports/eda/progress/fragmen-spread/laporan_revisi_fragmen_4b.md
?? reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md
?? reports/governance/2026-10-07/arsitek/putusan-adjudikasi-reaudit-kedua.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-B1.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-F1.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-fix-D1-D5.md
?? reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md
?? src/features/build_labels.py
?? tests/test_build_labels.py
```

**Blok [O3] — C3 BEFORE: hash beku 7 berkas + config + D4 sha256 + mtime:**

```
C3 BEFORE (diambil sebelum tugas)

2561efd552544feeb9af0b6733711015b83f43dd  src/features/build_labels.py
399e64b372e430b6def79b4fa8324a4e8e629918  src/features/build_features.py
dc07a7e651d38f07a5cabbe4e693b10681312d25  tests/test_build_labels.py
ed7ac43520c4431519d4d7065504866ae9b3ad95  tests/test_build_features.py
bc17e5de6cfefb355fe7418acd2a3a0d8b461212  reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
345308540d27c38534b77cdcd278e32eb15735ec  reports/governance/2026-10-07/coder/laporan-final-fase1.md
07402f40478aaed9391203f5db3237d636f5a959  data/features/M15/usdjpy_m15_features.parquet
e277d67ea618cd681915ae2474f4ae9a8d349516  configs/data.yaml

47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c *data/labels/usdjpy_day_labels.parquet
32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f *data/labels/usdjpy_h2_trades.parquet

data/labels/usdjpy_day_labels.parquet | mtime=2026-10-08 15:04:01.255371600 +0700 | size=29121
data/labels/usdjpy_h2_trades.parquet | mtime=2026-10-08 15:04:01.255371600 +0700 | size=7837
```

---

## 4. S-H1 — vonis H1 real-time (spec :140-196)

### 4.1 S0 provenans: build runtime (D1 read-only) vs D4 beku — instrumen exact (P-1)

Instrumen: `np.array_equal(..., equal_nan=True)` + pola NaN + `max_abs_diff` per kolom — **bukan** `isclose`-toleransi-default (standing rule P-1). Hasil: **6/6 kolom `exact_equal=true`, `max_abs_diff=0.0`, index identik, 974 baris** ([O4]). Artinya D4 di disk = hasil build ulang D1 bit-exact; gate S1 di bawah boleh dihitung dari D4 beku.

**Blok [O4] — S0 provenans (excerpt log `sh1_run1.log`):**

```
=== S0. PROVENANS: build runtime (D1 read-only) vs D4 beku (exact) ===
{
  "baris_daily_runtime": 974,
  "baris_build": 974,
  "baris_d4": 974,
  "index_identik": true,
  "kolom_sama": true,
  "per_kolom": {
    "day_label": {
      "exact_equal": true
    },
    "london_drift_4h": {
      "exact_equal": true,
      "pola_nan_identik": true,
      "max_abs_diff": 0.0
    },
    "london_drift_norm": {
      "exact_equal": true,
      "pola_nan_identik": true,
      "max_abs_diff": 0.0
    },
    "gap_f2_flag": {
      "exact_equal": true,
      "pola_nan_identik": true,
      "max_abs_diff": 0.0
    },
    "rv_regime_flag": {
      "exact_equal": true,
      "pola_nan_identik": true,
      "max_abs_diff": 0.0
    },
    "quarantine_mask": {
      "exact_equal": true
    }
  },
  "sha256_d4_day_labels": "47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c",
  "sha256_store_m15": "cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb",
  "sha256_config_data": "1127514518aaf23cd48acac3e4f482159d14a25f37d05168b4444f2c38709dad"
}
```

### 4.2 S1 gate — reproduksi M1-INK dari D4 vs angka referensi [O8] (presisi penuh)

Formula = mirror harness H3 (`uji1_materialitas_gap.py`): trend/range dari D4 `london_drift_norm`, dropna per kolom; bootstrap percentile hari-level **unpaired** B=10000 seed=20261006 (rng baru per panggilan, urutan konsumsi identik H3); chi2 tahun×trending/bukan 2023–2025 tanpa Yates. Dihitung **dua kali**: dari D4 di disk dan dari build runtime (keduanya harus cocok — bukti tidak bergantung artefak rusak).

**Blok [O5] — S1 gate (excerpt log `sh1_run1.log`):**

```
=== S1 GATE: reproduksi M1-INK dari D4 vs [O8] (presisi penuh) ===
{
  "referensi_O8": {
    "n_trending": 330,
    "n_pembanding": 324,
    "median_trending": 0.02948996641114935,
    "median_pembanding": 0.015065793016650224,
    "ci95_lo": -0.02729045556350576,
    "ci95_hi": 0.052787080233690914,
    "chi2_2xk": 0.7666041417663041,
    "p_2xk": 0.6816069745648556,
    "verdict": "GUGUR"
  },
  "m1_dari_d4": {
    "drift_col": "london_drift_norm",
    "pembanding": "trending vs range",
    "n_trending": 330,
    "n_pembanding": 324,
    "median_trending": 0.02948996641114935,
    "median_pembanding": 0.015065793016650224,
    "selisih_median": 0.014424173394499126,
    "ci95_lo": -0.02729045556350576,
    "ci95_hi": 0.052787080233690914,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 0.7666041417663041,
    "p_2xk": 0.6816069745648556,
    "kriteria_ii_p_lt_alpha": false,
    "verdict": "GUGUR"
  },
  "m1_dari_built_runtime": {
    "drift_col": "london_drift_norm",
    "pembanding": "trending vs range",
    "n_trending": 330,
    "n_pembanding": 324,
    "median_trending": 0.02948996641114935,
    "median_pembanding": 0.015065793016650224,
    "selisih_median": 0.014424173394499126,
    "ci95_lo": -0.02729045556350576,
    "ci95_hi": 0.052787080233690914,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 0.7666041417663041,
    "p_2xk": 0.6816069745648556,
    "kriteria_ii_p_lt_alpha": false,
    "verdict": "GUGUR"
  },
  "checks_presisi_penuh": {
    "n_trending": true,
    "n_pembanding": true,
    "median_trending": true,
    "median_pembanding": true,
    "ci95_lo": true,
    "ci95_hi": true,
    "chi2_2xk": true,
    "p_2xk": true,
    "verdict": true
  },
  "gate_pass": true
}
```

Bacaan: **9/9 checks `true`, `gate_pass=true`** — S1 LULUS presisi penuh; S2 berjalan.

---

### 4.3 S2 — klasifikasi real-time + dua kriteria penentu

Prosedur (spec :151-163): untuk hari T terurut `date_broker`, ambang = median `ratio_path` dan `range_atr` atas hari-broker **selesai sebelum T** (strictly past, expanding, skipna default); burn-in 60 hari-broker pertama = non-evaluable (dilaporkan n + rentang); klasifikasi trending/range/normal (NaN → normal); drift = `london_drift_norm` D4 bertanda; dropna per kolom; karantina inklusif identik M1.

Pembacaan burn-in (operasional, ditetapkan sebelum lihat hasil — ASUMSI spec :157): "60 hari riwayat" = 60 **posisi** hari-broker; median expanding memakai skipna (14 hari warmup ATR tidak menyumbang nilai median `range_atr` tetapi tetap dihitung sebagai hari riwayat; blok di bawah melaporkan 46 nilai pada ambang pertama apa adanya). Tidak ada ambang/burn-in alternatif yang dihitung.

**Blok [O6] — S2 klasifikasi real-time + kriteria (excerpt `sh1_run1.log`):**

```
=== S2. KLASIFIKASI REAL-TIME (ambang median expanding strictly-past) ===
{
  "pra_registrasi_burn_in": {
    "burn_in_ditetapkan": 60,
    "n_non_evaluable": 60,
    "tanggal_non_evaluable_awal": "2023-01-02T00:00:00",
    "tanggal_non_evaluable_akhir": "2023-03-24T00:00:00",
    "hari_evaluable_pertama": "2023-03-27T00:00:00",
    "n_evaluable": 914,
    "nilai_non_nan_ratio_di_riwayat_hari_pertama": 60,
    "nilai_non_nan_range_di_riwayat_hari_pertama": 46,
    "med_ratio_hari_evaluable_pertama": 0.021980032682788166,
    "med_range_hari_evaluable_pertama": 90.29323100280322,
    "med_ratio_hari_terakhir": 0.02696382912894182,
    "med_range_hari_terakhir": 89.17910447761084,
    "distribusi_label_rt_evaluable": {
      "range": 314,
      "trending": 311,
      "normal": 289
    }
  },
  "kriteria_i_dan_ii": {
    "label_col": "label_rt",
    "drift_col": "drift_norm",
    "pembanding": "trending vs range",
    "tahun_kriteria_ii": [
      2023,
      2024,
      2025
    ],
    "n_trending": 311,
    "n_pembanding": 314,
    "median_trending": 0.0290361935746169,
    "median_pembanding": 0.013991553584495942,
    "selisih_median": 0.01504463999012096,
    "ci95_lo": -0.02668182694022586,
    "ci95_hi": 0.05242264543726398,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 3.333835311042838,
    "p_2xk": 0.18882820311496487,
    "kriteria_ii_p_lt_alpha": false,
    "verdict": "GUGUR"
  },
  "share_trending_per_tahun": {
    "2023": {
      "n_evaluable": 199,
      "n_trending": 79
    },
    "2024": {
      "n_evaluable": 260,
      "n_trending": 83
    },
    "2025": {
      "n_evaluable": 259,
      "n_trending": 86
    }
  }
}
```

Bacaan: n non-evaluable 60 (2023-01-02..2023-03-24), hari evaluable pertama 2023-03-27, **n evaluable 914**. Distribusi real-time: range 314 / trending 311 / normal 289. **Kriteria (i) terpenuhi** (CI95 `[-0.02668182694022586, +0.05242264543726398]` memuat 0) → **verdict formula = GUGUR**; kriteria (ii) tidak terpenuhi (chi2 3.333835311042838, p 0.18882820311496487). Share trending 2023 79/199 · 2024 83/260 · 2025 86/259.

### 4.4 S3 — suplemen non-penentu + divergence check Q1

**Blok [O7] — S3 suplemen non-penentu (excerpt `sh1_run1.log`):**

```
=== S3. SUPLEMEN (non-penentu) + divergence check Q1 ===
{
  "sign_test_trending_median_0": {
    "n_positif": 168,
    "n_negatif": 143,
    "n_nol": 0,
    "p_two_sided": 0.17344255582155393,
    "alpha_lapor": 0.01
  },
  "chi2_3_kolom_2023_2025": {
    "chi2": 5.542508433280522,
    "p": 0.23601814600793775,
    "dof": 4,
    "tabel": {
      "normal": {
        "2023": 57,
        "2024": 95,
        "2025": 80
      },
      "range": {
        "2023": 63,
        "2024": 82,
        "2025": 93
      },
      "trending": {
        "2023": 79,
        "2024": 83,
        "2025": 86
      }
    }
  },
  "R1_drift_4h_tanpa_norm": {
    "label_col": "label_rt",
    "drift_col": "drift_4h",
    "pembanding": "trending vs range",
    "tahun_kriteria_ii": [
      2023,
      2024,
      2025
    ],
    "n_trending": 311,
    "n_pembanding": 314,
    "median_trending": 0.04099999999999682,
    "median_pembanding": 0.014500000000012392,
    "selisih_median": 0.026499999999984425,
    "ci95_lo": -0.03099999999997749,
    "ci95_hi": 0.0589999999999975,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 3.333835311042838,
    "p_2xk": 0.18882820311496487,
    "kriteria_ii_p_lt_alpha": false,
    "verdict": "GUGUR"
  },
  "R2_pembanding_normal_range": {
    "label_col": "label_rt",
    "drift_col": "drift_norm",
    "pembanding": "trending vs normal+range",
    "tahun_kriteria_ii": [
      2023,
      2024,
      2025
    ],
    "n_trending": 311,
    "n_pembanding": 603,
    "median_trending": 0.0290361935746169,
    "median_pembanding": 0.02789976750193856,
    "selisih_median": 0.001136426072678342,
    "ci95_lo": -0.040334484530474134,
    "ci95_hi": 0.03759738849077979,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 3.333835311042838,
    "p_2xk": 0.18882820311496487,
    "kriteria_ii_p_lt_alpha": false,
    "verdict": "GUGUR"
  },
  "R3_kriteria_ii_muat_2026": {
    "label_col": "label_rt",
    "drift_col": "drift_norm",
    "pembanding": "trending vs range",
    "tahun_kriteria_ii": [
      2023,
      2024,
      2025,
      2026
    ],
    "n_trending": 311,
    "n_pembanding": 314,
    "median_trending": 0.0290361935746169,
    "median_pembanding": 0.013991553584495942,
    "selisih_median": 0.01504463999012096,
    "ci95_lo": -0.02668182694022586,
    "ci95_hi": 0.05242264543726398,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 3.752091854439169,
    "p_2xk": 0.28950804557521426,
    "kriteria_ii_p_lt_alpha": false,
    "verdict": "GUGUR"
  },
  "agreement_real_time_vs_ex_post": {
    "persen_sama": 0.9803063457330415,
    "n_pindah_keranjang": 18,
    "n_evaluable": 914,
    "crosstab": {
      "normal": {
        "normal": 281,
        "range": 2,
        "trending": 6
      },
      "range": {
        "normal": 9,
        "range": 305,
        "trending": 0
      },
      "trending": {
        "normal": 1,
        "range": 0,
        "trending": 310
      }
    }
  },
  "median_dan_n_evaluable_per_tahun": {
    "2023": {
      "n_evaluable": 199,
      "label_rt_counts": {
        "trending": 79,
        "range": 63,
        "normal": 57
      },
      "median_drift_trending": 0.006412773197230084,
      "median_drift_normal": 0.04352049737711444,
      "median_drift_range": 0.0
    },
    "2024": {
      "n_evaluable": 260,
      "label_rt_counts": {
        "normal": 95,
        "trending": 83,
        "range": 82
      },
      "median_drift_trending": 0.090499709471237,
      "median_drift_normal": 0.04271018091522414,
      "median_drift_range": -0.006752025301530919
    },
    "2025": {
      "n_evaluable": 259,
      "label_rt_counts": {
        "range": 93,
        "trending": 86,
        "normal": 80
      },
      "median_drift_trending": 0.03578626922790365,
      "median_drift_normal": 0.05266722944194416,
      "median_drift_range": 0.019601874961949664
    },
    "2026": {
      "n_evaluable": 196,
      "label_rt_counts": {
        "range": 76,
        "trending": 63,
        "normal": 57
      },
      "median_drift_trending": -0.02704152806095172,
      "median_drift_normal": 0.044624999999989416,
      "median_drift_range": 0.02309896953804834
    }
  }
}
```

**Blok [O8] — divergence check Q1 (excerpt `sh1_run1.log`):**

```
{
  "m1_verdict": "GUGUR",
  "real_time_verdict": "GUGUR",
  "searah_dengan_M1": true,
  "divergence_annotation": false,
  "eskalasi_sebelum_dipakai_ke_mana_pun": false
}
```

Bacaan: sign test dua-sisi median drift trending = 0 → p=0.17344255582155393 (n_pos 168 / n_neg 143 / n_zero 0; alpha lapor 0.01; tidak signifikan). chi2 3-kolom (2023-2025) p=0.23601814600793775. Robustness **R1** (`london_drift_4h` mentah), **R2** (pembanding normal+range), **R3** (kriteria-ii termasuk 2026): ketiganya **GUGUR** — verdict formula tidak berpindah di bawah satu pun pembacaan (R1-R3 BUKAN penentu). Agreement real-time vs ex-post 98.03% (914 hari, 18 pindah keranjang; keranjang bergerak: normal→trending 6, range→normal 9, normal→range 2, trending→normal 1). **Divergence Q1: real-time GUGUR searah M1 GUGUR → anotasi disitir (Uji-1 IMMATERIAL: gap-flag bukan penggerak), `eskalasi_sebelum_dipakai_ke_mana_pun=false`.**

---

## 5. S-H2 — backtest strategi Q2 + VR OOS (spec :205-241)

### 5.1 S0 — provenans + deskriptif per tahun (pra-EV)

**Blok [O9] — S0 provenans S-H2 (excerpt `sh2_run1.log`):**

```
=== S0. PROVENANS (S-H2) ===
{
  "sha256_d4_day_labels": "47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c",
  "sha256_d4_day_labels_cocok_47d15c41": true,
  "sha256_d4_h2_trades": "32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f",
  "sha256_d4_h2_trades_cocok_32eaf6b2": true,
  "sha256_configs_data_yaml": "1127514518aaf23cd48acac3e4f482159d14a25f37d05168b4444f2c38709dad",
  "pip_size_dipakai": 0.01,
  "pip_size_cocok_0_01": true,
  "cost_basis_by_session_dipakai": {
    "London": 0.61,
    "NewYork": 0.69,
    "Tokyo": 0.62,
    "Sydney": 0.8
  },
  "cost_basis_default_dipakai": 0.65,
  "cost_basis_cocok_per_nilai": true,
  "n_baris_m15_2023_2025": 72015,
  "n_baris_m15_per_tahun": {
    "2023": 24294,
    "2024": 23909,
    "2025": 23812
  },
  "n_baris_d4": 974,
  "n_baris_d4_h2_trades": 1,
  "kolom_d4_h2_trades": [
    "symbol",
    "strategy",
    "entry_rule",
    "exit_rule",
    "sl_atr",
    "tp",
    "biaya",
    "entry_time_utc",
    "entry_frequency",
    "price_unit"
  ],
  "index_daily_sama_dengan_d4": true,
  "rentang_d4": [
    "2023-01-02T00:00:00",
    "2026-10-02T00:00:00"
  ],
  "rentang_pool": [
    "2023-01-02T00:00:00",
    "2025-12-31T00:00:00"
  ]
}
```

**Blok [O10] — S0 deskriptif per tahun (excerpt `sh2_run1.log`):**

```
=== S0 DESKRIPTIF per tahun (pra-EV) ===
{
  "n_bar_sinyal_dipakai_total": 778,
  "per_tahun": {
    "2023": {
      "n_hari_broker": 259,
      "n_hari_tanpa_bar_sinyal": 0,
      "n_hari_bar_ada_tanpa_sinyal_entry": 127,
      "n_hari_sinyal_tanpa_konfirmasi": 85,
      "n_trade_tereksekusi": 47,
      "n_exit_SL": 0,
      "n_exit_TP": 0,
      "n_exit_sinyal": 47,
      "n_exit_time_stop": 0,
      "n_trade_hari_karantina": 0,
      "n_trade_hari_gap_flag": 15,
      "n_fallback_label_Off": 0
    },
    "2024": {
      "n_hari_broker": 260,
      "n_hari_tanpa_bar_sinyal": 0,
      "n_hari_bar_ada_tanpa_sinyal_entry": 125,
      "n_hari_sinyal_tanpa_konfirmasi": 93,
      "n_trade_tereksekusi": 42,
      "n_exit_SL": 0,
      "n_exit_TP": 0,
      "n_exit_sinyal": 42,
      "n_exit_time_stop": 0,
      "n_trade_hari_karantina": 1,
      "n_trade_hari_gap_flag": 5,
      "n_fallback_label_Off": 0
    },
    "2025": {
      "n_hari_broker": 259,
      "n_hari_tanpa_bar_sinyal": 0,
      "n_hari_bar_ada_tanpa_sinyal_entry": 117,
      "n_hari_sinyal_tanpa_konfirmasi": 91,
      "n_trade_tereksekusi": 51,
      "n_exit_SL": 0,
      "n_exit_TP": 0,
      "n_exit_sinyal": 51,
      "n_exit_time_stop": 0,
      "n_trade_hari_karantina": 0,
      "n_trade_hari_gap_flag": 8,
      "n_fallback_label_Off": 0
    }
  }
}
```

Bacaan: sha256 D4 kedua berkas **cocok nilai spec** (`47d15c41…` / `32eaf6b2…`); pip_size 0.01 dan tabel `cost_basis` cocok per nilai; 72015 baris M15 2023-2025 (24294/23909/23812); index `daily` = index D4. Deskriptif: 778 hari-broker; **n hari-tanpa-bar-sinyal = 0** (bar 14:45 ada di setiap hari); 369 hari bar-ada-namun-`close<=open` (FLAT, bucket akunting tambahan — §8 DEV-B2); 269 hari sinyal-tanpa-konfirmasi T-1; **140 trade tereksekusi** (47/42/51); exit: **sinyal 140, SL 0, TP 0, time-stop 0**; trade di hari gap-flag 28, di hari karantina 1; fallback "Off" 0. (Total baris = 0 + 369 + 269 + 140 = 778 per tahunnya: 259/260/259.)

### 5.2 S1 — EV-after-cost per tahun (kriteria penentu 1)

**Blok [O11] — S1 EV-after-cost (excerpt `sh2_run1.log`):**

```
=== S1. EV-after-cost per tahun (median penentu) ===
{
  "definisi": "EV JPY = exit - entry - cost_jpy; cost_jpy = cost_basis pip x pip_size 0.01",
  "per_tahun": {
    "2023": {
      "n": 47,
      "median_ev_jpy": -0.016099999999990906,
      "mean_ev_jpy": -0.015248936170214115,
      "persen_positif": 0.48936170212765956
    },
    "2024": {
      "n": 42,
      "median_ev_jpy": -0.06060000000000443,
      "mean_ev_jpy": -0.03138571428571253,
      "persen_positif": 0.23809523809523808
    },
    "2025": {
      "n": 51,
      "median_ev_jpy": -0.044099999999982493,
      "mean_ev_jpy": -0.025492156862744062,
      "persen_positif": 0.3333333333333333
    }
  },
  "tahun_median_le_0": [
    2023,
    2024,
    2025
  ],
  "tahun_tanpa_trade": [],
  "GUGUR_kriteria_EV": true
}
```

Bacaan: median EV-per-trade (JPY) 2023 `-0.016099999999990906` (n=47, mean `-0.015248936170214115`, positif 48.94%); 2024 `-0.06060000000000443` (n=42, mean `-0.03138571428571253`, positif 23.81%); 2025 `-0.044099999999982493` (n=51, mean `-0.025492156862744062`, positif 33.33%). **Median ≤ 0 pada 3/3 tahun → kriteria EV terpenuhi → bagian EV dari formula = GUGUR.** Tidak ada tahun tanpa trade.

### 5.3 S2 — VR OOS pool M15 2023-2025 (kriteria penentu 2)

**Blok [O12] — S2 VR + verdict (excerpt `sh2_run1.log`):**

```
=== S2. VR OOS (pool M15 2023-2025, resep verbatim EDA) ===
{
  "resep": "r=ln(C_t/C_t-1); gap=utc.diff()>15 menit dibuang; variance_ratio cumsum overlapping ddof=1; horizon 5/15/60; rata-rata = mean ketiganya",
  "n_bar_pool": 72015,
  "n_baris_gap_dibuang": 682,
  "n_nilai_clean_finite": 71332,
  "VR5": 1.0172182521892266,
  "VR15": 1.0236432801419544,
  "VR60": 1.0387647008498926,
  "rata_rata_VR": 1.0265420777270247,
  "GUGUR_kriteria_VR": false
}
{
  "kriteria_1_EV_median_le_0_pada_ge_2_tahun": true,
  "tahun_median_le_0": [
    2023,
    2024,
    2025
  ],
  "tahun_tanpa_trade": [],
  "kriteria_2_VR_rata_rata_le_1": false,
  "verdict": "GUGUR"
}
```

Bacaan: VR5 `1.0172182521892266`, VR15 `1.0236432801419544`, VR60 `1.0387647008498926`, rata-rata `1.0265420777270247` (> 1) → **kriteria VR tidak terpenuhi**. Verdict formula keseluruhan (salah satu terpenuhi) = **GUGUR**.

### 5.4 Verifikasi independen trade[0] (hitung tangan)

Spot-check dibaca ulang dari processed M15 (bukan dari JSON harness) dan dicocokkan: entry = close bar 14:45 = 131.065 (close > open 130.406 — sinyal sah); bar monitoring pertama 15:00 close 130.673 < open 131.069 → exit sinyal pada 130.673; SL 129.00464285714287 dan TP 135.18571428571428 tidak tersentuh (low 130.642 > SL; high 131.109 < TP); EV = 130.673 − 131.065 − 0.0061 = **−0.3981** cocok JSON `-0.3980999999999959`. Output di [O13].

---

## 6. Tabel Klaim & Bukti (§5 AGENTS.md) — auditor mencocokkan ulang, bukan membaca narasi

| Klaim | Status | Bukti |
|---|---|---|
| Blob spec di disk == `fc29f6fa3595a89b918627dbdc71cfff82d8ebed` (gate sebelum eksekusi) | TERVERIFIKASI | §2.1 (output `git hash-object`) |
| Bukti baca 5 dokumen: spec + lock + putusan H1-H5 + protokol + putusan H3 (semua hash diukur) | TERVERIFIKASI | §2.1 |
| HEAD tetap `e0b2b9f9…`; nol commit | TERVERIFIKASI | [O1] + [O18] (`git log --oneline -1`) |
| C2 nol tulis produksi + nol sentuh berkas lindung (BEFORE == AFTER + `find -newermt` kosong) | TERVERIFIKASI | [O2] vs [O16] |
| C3 7/7 hash beku cocok + config `e277d67e…` + D4 sha256/mtime tidak berubah | TERVERIFIKASI | [O3] vs [O17] |
| S1 gate reproduksi angka [O8] dokumen H3: **9/9 bit-exact** (bukan isclose) | TERVERIFIKASI | [O5] |
| S-H1 S2: verdict-formula **GUGUR** — kriteria (i) CI95 memuat 0; kriteria (ii) p=0.18882820311496487 ≥ 0.01 | TERVERIFIKASI | [O6] |
| S-H1 burn-in dilaporkan: n=60 non-evaluable (2023-01-02..2023-03-24), evaluable 914 | TERVERIFIKASI | [O6] |
| S-H1 S3: sign test p=0.17344255582155393; chi2 3-kolom p=0.23601814600793775; R1/R2/R3 GUGUR; agreement 98.03% (18/914) | TERVERIFIKASI | [O7] |
| Divergence Q1: searah M1 → anotasi; tidak ada eskalasi wajib | TERVERIFIKASI | [O8] |
| S-H2 S0: sha256 D4 kedua berkas cocok; cost_basis cocok per nilai; pip_size 0.01; 72015 baris M15 | TERVERIFIKASI | [O9] |
| S-H2 S0 deskriptif: 778 hari-broker; 0 hari-tanpa-bar-sinyal; 140 trade; 140 exit sinyal; 28 trade gap; 1 trade karantina | TERVERIFIKASI | [O10] |
| S-H2 S1: median EV ≤ 0 pada 3/3 tahun → kriteria EV terpenuhi → **GUGUR** (bagian formula) | TERVERIFIKASI | [O11] |
| S-H2 S2: VR5/15/60 + rata-rata 1.0265420777270247 > 1 → kriteria VR tidak terpenuhi | TERVERIFIKASI | [O12] |
| Kopling H2↔H1 tidak ada: konfirmasi H2 = `day_label` D4 T-1; S-H1 tidak memakai hasil S-H2 | TERVERIFIKASI | [O9]/[O10] (kode `sh2.py` memakai `label_shift` dari D4) |
| Determinisme: sha256 hasil sh1 ×2 identik (`41b3630c…`); sh2 ×2 identik (`c818aad3…`); `cmp` IDENTIK | TERVERIFIKASI | [O13] |
| Spot-check independen trade[0] cocok hitung-tangan (EV −0.3981) | TERVERIFIKASI | [O13] |
| D4 tidak ditimpa: sha256 + mtime before/after identik | TERVERIFIKASI | [O3] vs [O17] |
| C4 gate hijau: pytest 254 passed; `ruff check .` All checks passed; `ruff format --check .` 37 files; cek asing dokumen (2x) | TERVERIFIKASI | [O14] + [O15] + (ulang pasca-C8 di chat) |
| C9: staged = 0 (tanpa commit) | TERVERIFIKASI | [O18] |
| Tanpa vonis H3/H4/H5; tanpa TAU/filter di jalur eksekusi; tanpa shopping ambang/rule/varian | TERVERIFIKASI | §2.4 (grep) + §7 self-audit putaran 2-3 |
| Pembacaan burn-in 60 = 60 posisi (skipna median) — bila maksud spec adalah 60 nilai non-NaN, batas bergeser dan perlu rerun | ASUMSI (dilaporkan) | §4.3; tidak dihitung sebagai varian |
| Cakupan data hanya s/d 2026-10-02 (isi store/D4); tidak ada verifikasi di luar itu | BELUM DIVERIFIKASI | §8 butir 4 |
| Lingkungan auditor `.venv` (ruff 0.16.10) akan melaporkan 9 berkas pra-ada "would be reformatted" — bukan dari batch ini | BELUM DIVERIFIKASI | §8 butir 5 (catatan, bukan klaim lulus) |

---

## 7. Self-audit adversarial 3 putaran (sebelum serah)

**Putaran 1 — Correctness.** (a) Angka [O8] di konstanta `O8` `sh1.py` dicocokkan karakter-per-karakter dengan spec :166-170 dan blok [O8] dokumen H3; gate menuntut `==` presisi penuh (bukan isclose) dan lulus 9/9 → tidak ada angka yang "dirapikan". (b) Nama file hasil + lokasi persis kontrak (`coder/hasil-lapisan3-H1H2.md`); skrip hanya di `%TEMP%\opencode\l3h1h2`. (c) Setiap syarat C1-C9 punya pasangan perintah mentah + output ([O1]-[O19]); C4 dijalankan juga atas dokumen ini ([O15]). (d) Semua angka di §0/§4/§5 bisa dilacak ke blok [On] yang berisi keluaran mesin, bukan narasi.

**Putaran 2 — Bias & Asumsi (celah salah-ketik).** (a) **Jebakan 14:45 vs 15:00**: bar ber-label `time`=14:45 TUTUP pada 15:00 UTC; dipakai bar 14:45, diverifikasi terhadap data (bar pertama hari-broker 22:00 UTC) dan terhadap spot-check trade[0]. (b) **Jebakan sesi/biaya 0.61 vs 0.69**: pada 14:45 UTC label store = London sepanjang tahun (winter 14:45, summer 15:45 lokal, keduanya < 16:00) — 974/974 bar; fallback "Off" 0 kali; bukan NewYork. (c) **Jebakan satuan**: biaya pip→JPY ditulis tiap langkah (§2.3); ATR JPY mentah; tahun date_broker; tidak ada `utc.normalize()`. (d) **Jebakan burn-in**: pembacaan "60 posisi, median skipna" ditetapkan sebelum lihat hasil dan dilaporkan apa adanya (46 nilai pada ambang pertama) — bukan ambang yang "dirapikan". (e) Tidak ada ambang/rule/varian baru pasca-lihat-hasil; R1-R3 heterogen (bukan fixture seragam) dan non-penentu.

**Putaran 3 — Meta-check.** (a) Spec = satu-satunya sumber instruksi; prompt vs spec tidak berselisih material (keduanya sinkron pada Q2/C1-C9/S-B). (b) Ruang vonis tidak diambil coder: semua GUGUR/TAHAN = keluaran formula; tidak ada vonis H3/H4/H5; TAU/filter tidak dipakai dalam bentuk apa pun. (c) Lulus-eksekusi dipisahkan dari hasil: S-H1 lulus-eksekusi (gate S1 lulus presisi penuh + 2 kriteria terhitung) **dan** hasil GUGUR; S-H2 lulus-eksekusi (140 trade terhitung, VR terhitung) **dan** hasil GUGUR. (d) Tidak mengaudit sendiri: §9-§10 adalah bukti + pembacaan angka; penilaian adversarial atas dokumen ini milik Auditor.

## 8. Yang belum diverifikasi / batasan (DEV)

1. **DEV-B1 — pembacaan burn-in.** "60 hari riwayat" dibaca sebagai 60 posisi hari-broker dengan median expanding skipna (spec :157 tidak menyebut min_periods nilai). Bila maksud Arsitek adalah 60 **nilai non-NaN** (libatkan warmup ATR 14 hari), hari evaluable pertama bergeser (+14 hari); tidak dihitung di batch ini (bukan varian terdaftar). Angka ambang pertama apa adanya ada di [O6].
2. **DEV-B2 — bucket akunting tambahan.** Daftar deskriptif spec (:215-218) memuat "n hari-tanpa-bar-sinyal"; hari dengan bar ada tetapi `close<=open` bukan trade dan bukan "tanpa bar" — saya laporkan sebagai bucket tersendiri (`n_hari_bar_ada_tanpa_sinyal_entry`, 369 hari) agar total per tahun tetap 259/260/259 dan tidak ada hari yang hilang senyap. Tidak memengaruhi verdict.
3. **DEV-B3 — distribusi exit.** 140/140 exit jenis "sinyal" (0 SL / 0 TP / 0 time-stop). Ini konsekuensi mekanis aturan Q2(d)(iii): exit saat `close<open` dicek pada TIAP bar monitoring, sehingga SL/TP (jarak ≥1× ATR) nyaris tidak pernah tersentuh lebih dulu. Dilaporkan apa adanya; 1 trade diverifikasi tangan ([O13]). Bukan klaim tambahan, bukan varian.
4. **DEV-B4 — cakupan data.** Store/D4 berakhir 2026-10-02; S-H1 evaluable mencakup 2026 parsial (dilaporkan per tahun di [O7]); S-H2 hanya 2023-2025. Tidak ada klaim di luar cakupan itu.
5. **DEV-B5 — lingkungan auditor.** `.venv` (ruff 0.16.10) memformat `.md` berbeda dari venv kanonik (0.6.9) dan akan melaporkan 9 berkas pra-ada "would be reformatted" (6 notebook + 2 `.md` reaudit + `build_features.py:326`) — tidak ada yang berasal dari batch ini; venv kanonik `ruff format --check .` = 37 files already formatted ([O14]). Cek asing dijalankan dengan venv kanonik atas dokumen ini.
6. **DEV-B6 — hash dokumen.** Hash penuh dokumen final (setelah baris C8) dilaporkan di chat; baris terakhir dokumen = hash `head -n -1` (reproduksi §11). Ini mengikuti pola yang sudah diterima pada batch H3.
7. **DEV-B7 — verdict bukan vonis.** S-H1/S-H2 "GUGUR" di dokumen ini = keluaran formula lock; keputusan tahap berikut + validasi adversarial milik Arsitek/Auditor.

---

## 9. Kriteria selesai Batch-1 (C1-C9)

| # | Syarat (spec :245-268) | Status | Bukti |
|---|---|---|---|
| C1 | HEAD tak berubah | **LULUS** | [O1]; diulang [O18] |
| C2 | Nol tulis produksi + nol sentuh berkas lindung (pola P-3: tracked-only + before/after; pola "output KOSONG" PENSIUN) | **LULUS** | [O2] vs [O16]: diff kosong + `find -newermt` kosong |
| C3 | Hash beku cocok + cost tercatat | **LULUS** | [O3] vs [O17]: 7/7 prefix cocok; D4 sha256 + mtime identik; tabel `cost_basis` cocok per nilai ([O9]) |
| C4 | Gate hijau | **LULUS** | [O14] (pytest 254 passed / ruff check / ruff format 37) + [O15] (cek asing atas dokumen ini) |
| C5 | Determinisme | **LULUS** | [O13]: sha256 kedua run identik per harness + `cmp` IDENTIK |
| C6 | S-H1 selesai + hasil diputus | **LULUS** | S1 [O5] + S2 [O6] + S3 [O7] + divergence [O8] |
| C7 | S-H2 selesai + hasil diputus | **LULUS** | S0 [O9][O10] + S1 [O11] + S2 [O12] |
| C8 | Dokumen hasil final + hash sesudah penulisan terakhir | **LULUS** | §11 (baris C8) + hash penuh di chat |
| C9 | Staged = 0, tanpa commit | **LULUS** | [O18] + verifikasi ulang di chat |

## 10. Output mentah tambahan

**Blok [O13] — C5 determinisme (sha256 2 run per harness + cmp + spot-check trade[0]):**

```
$ sha256sum sh1_hasil_run1.json sh1_hasil_run2.json
41b3630c27ed1d3756c7bbe4509b2feeb18c622ca02c02300b2684ccc9f7fd77 *sh1_hasil_run1.json
41b3630c27ed1d3756c7bbe4509b2feeb18c622ca02c02300b2684ccc9f7fd77 *sh1_hasil_run2.json

$ cmp sh1_hasil_run1.json sh1_hasil_run2.json && echo "cmp: IDENTIK"
cmp: IDENTIK

$ sha256sum sh2_hasil_run1.json sh2_hasil_run2.json
c818aad30681f9629616da783671506ce16c2477c31c553ef115c3857df3b8f0 *sh2_hasil_run1.json
c818aad30681f9629616da783671506ce16c2477c31c553ef115c3857df3b8f0 *sh2_hasil_run2.json

$ cmp sh2_hasil_run1.json sh2_hasil_run2.json && echo "cmp: IDENTIK"
cmp: IDENTIK

$ spot-check trade[0] (baca ulang bar M15 processed; hitung tangan)
trade[0]: {
 "date_broker": "2023-01-24T00:00:00",
 "tahun": 2023,
 "sesi": "London",
 "cost_pip": 0.61,
 "cost_jpy": 0.0061,
 "entry": 131.065,
 "atr_t1": 2.0603571428571406,
 "sl": 129.00464285714287,
 "tp": 135.18571428571428,
 "exit_type": "sinyal",
 "exit_price": 130.673,
 "ev_jpy": -0.3980999999999959
}
                           utc     open     high      low    close
1599 2023-01-24 14:00:00+00:00  130.431  130.494  130.401  130.456
1600 2023-01-24 14:15:00+00:00  130.456  130.512  130.350  130.371
1601 2023-01-24 14:30:00+00:00  130.371  130.458  130.341  130.405
1602 2023-01-24 14:45:00+00:00  130.406  131.116  130.406  131.065
1603 2023-01-24 15:00:00+00:00  131.069  131.109  130.642  130.673
1604 2023-01-24 15:15:00+00:00  130.672  130.712  130.324  130.351
1605 2023-01-24 15:30:00+00:00  130.350  130.461  130.211  130.220
1606 2023-01-24 15:45:00+00:00  130.219  130.282  130.041  130.089
1607 2023-01-24 16:00:00+00:00  130.085  130.243  129.977  130.031
1608 2023-01-24 16:15:00+00:00  130.032  130.097  129.874  129.918
1609 2023-01-24 16:30:00+00:00  129.919  130.072  129.865  130.030
1610 2023-01-24 16:45:00+00:00  130.034  130.153  129.993  130.079

verifikasi tangan: entry = close bar 14:45 = 131.065 (close 131.065 > open 130.406, sinyal sah);
bar berikut (15:00): close 130.673 < open 131.069 -> exit sinyal pada close 130.673;
SL 129.00464285714287 tidak kena (low 15:00 = 130.642 > SL); TP 135.18571428571428 tidak kena (high 15:00 = 131.109 < TP);
EV = 130.673 - 131.065 - 0.0061 = -0.3981 (JSON: -0.3980999999999959; selisih = float repr).
```

**Blok [O14] — C4 gate kode (venv kanonik; rc + cakupan):**

```
$ venv/Scripts/python.exe -m pytest -q  (venv kanonik)
rc=0
tests\test_fetch_data.py ...................................             [ 69%]
tests\test_resample.py ...............................                   [ 81%]
tests\test_validate_data.py ............................................ [ 99%]
..                                                                       [100%]

============================ 254 passed in 20.68s =============================

$ venv/Scripts/python.exe -m ruff check .
rc=0
All checks passed!

$ venv/Scripts/python.exe -m ruff format --check .
rc=0
37 files already formatted

$ venv/Scripts/python.exe -m ruff --version
ruff 0.6.9
```

**Blok [O15] — C4 cek asing atas dokumen ini (`check_foreign_chars.py`; dijalankan pada draf & diulang pada dokumen final):**

```
$ venv/Scripts/python.exe scripts/check_foreign_chars.py reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
OK: 1 file discan, tidak ada karakter asing.
rc=0

$ .venv/Scripts/python.exe -m ruff format --check reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md  (.venv = ruff 0.16.10, lingkungan auditor)
1 file already formatted
rc=0

$ .venv/Scripts/python.exe -m ruff --version
ruff 0.16.10

$ grep -c CR (baris dengan CR) - harus 0
0

$ head -6 reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
# Hasil Lapisan 3 Batch-1 — Eksekusi S-H1 + S-H2 (Coder)

**Peran pelaksana:** Coder (`.ai/AGENTS.md` v3.0 §26: implementasi + self-audit; DILARANG audit sendiri, DILARANG memutus arsitektur). Semua label "GUGUR/TAHAN" di dokumen ini adalah **keluaran formula lock yang dihitung skrip**, bukan putusan coder. Vonis resmi + penilaian adversarial atas dokumen ini tetap wewenang Auditor/Arsitek (§26–§27).

**Tanggal eksekusi:** 2026-10-09 (mulai 01:33:44 +07). **HEAD:** `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` (tidak berubah; [O1]).
```

**Blok [O16] — C2 AFTER + diff + find kosong:**

```
$ git status --porcelain -uall -- src/ tests/ data/ configs/ reports/eda/ reports/governance/2026-10-07/arsitek/
 D reports/eda/progress/audit_kesesuaian_nb00_nb04.md
 D reports/eda/progress/laporan_fix_audit_fragmen.md
 D reports/eda/progress/laporan_revisi_fragmen_4b.md
 D reports/eda/progress/laporan_tahap_0_reuse_check.md
 D reports/eda/progress/laporan_tahap_10_autocorr_fix.md
 D reports/eda/progress/laporan_tahap_1_pin_deps.md
 D reports/eda/progress/laporan_tahap_2_nb00_setup.md
 D reports/eda/progress/laporan_tahap_3_returns.md
 D reports/eda/progress/laporan_tahap_4_volatility.md
 D reports/eda/progress/laporan_tahap_5_autokorelasi.md
 D reports/eda/progress/laporan_tahap_6_swing_level.md
 D reports/eda/progress/laporan_tahap_7_swing_level_fix.md
 D reports/eda/progress/laporan_tahap_8_volatility_fix.md
 D reports/eda/progress/laporan_tahap_9_figures_fix.md
?? reports/eda/progress/00-setup/laporan_tahap_0_reuse_check.md
?? reports/eda/progress/00-setup/laporan_tahap_1_pin_deps.md
?? reports/eda/progress/00-setup/laporan_tahap_2_nb00_setup.md
?? reports/eda/progress/01-returns/laporan_tahap_3_returns.md
?? reports/eda/progress/02-volatility/laporan_tahap_4_volatility.md
?? reports/eda/progress/02-volatility/laporan_tahap_8_volatility_fix.md
?? reports/eda/progress/03-autocorr/laporan_tahap_10_autocorr_fix.md
?? reports/eda/progress/03-autocorr/laporan_tahap_5_autokorelasi.md
?? reports/eda/progress/04-swings-levels/laporan_tahap_6_swing_level.md
?? reports/eda/progress/04-swings-levels/laporan_tahap_7_swing_level_fix.md
?? reports/eda/progress/05-figures/laporan_tahap_9_figures_fix.md
?? reports/eda/progress/06-regimes/.gitkeep
?? reports/eda/progress/06-regimes/laporan_tahap_13_report.md
?? reports/eda/progress/INDEX.md
?? reports/eda/progress/audit/audit_kesesuaian_nb00_nb04.md
?? reports/eda/progress/fragmen-spread/laporan_fix_audit_fragmen.md
?? reports/eda/progress/fragmen-spread/laporan_revisi_fragmen_4b.md
?? reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md
?? reports/governance/2026-10-07/arsitek/putusan-adjudikasi-reaudit-kedua.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-B1.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-F1.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-fix-D1-D5.md
?? reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md
?? src/features/build_labels.py
?? tests/test_build_labels.py

$ diff <BEFORE> <AFTER>
(IDENTIK - tidak ada beda)

$ find src tests data configs -type f -newermt "2026-10-09 01:33:44"
(selesai; kosong = tidak ada berkas tersentuh)
```

**Blok [O17] — C3 AFTER (hash beku + config + D4 sha256 + mtime, ulang):**

```
C3 AFTER: hash beku + hash config (ulang)

2561efd552544feeb9af0b6733711015b83f43dd  src/features/build_labels.py
399e64b372e430b6def79b4fa8324a4e8e629918  src/features/build_features.py
dc07a7e651d38f07a5cabbe4e693b10681312d25  tests/test_build_labels.py
ed7ac43520c4431519d4d7065504866ae9b3ad95  tests/test_build_features.py
bc17e5de6cfefb355fe7418acd2a3a0d8b461212  reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
345308540d27c38534b77cdcd278e32eb15735ec  reports/governance/2026-10-07/coder/laporan-final-fase1.md
07402f40478aaed9391203f5db3237d636f5a959  data/features/M15/usdjpy_m15_features.parquet
e277d67ea618cd681915ae2474f4ae9a8d349516  configs/data.yaml

47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c *data/labels/usdjpy_day_labels.parquet
32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f *data/labels/usdjpy_h2_trades.parquet

data/labels/usdjpy_day_labels.parquet | mtime=2026-10-08 15:04:01.255371600 +0700 | size=29121
data/labels/usdjpy_h2_trades.parquet | mtime=2026-10-08 15:04:01.255371600 +0700 | size=7837
```

**Blok [O18] — C9 staged = 0 + HEAD + porcelain utuh (diambil sebelum penulisan dokumen; diulang setelah penulisan terakhir — hasil di chat):**

```
$ git diff --cached --name-only
(kosong di atas = nol staged)

$ git log --oneline -1
e0b2b9f feat(features): fondasi B1 TERTUTUP + governance audit (konfirmasi 3xYA)

$ git status --porcelain (utuh)
 M .ai/AGENTS.md
 M .ai/SESSION_LOG.md
 M .ai/STATE.md
 M .ai/TASKS.md
 M .ai/assistant/README.md
 D reports/eda/progress/audit_kesesuaian_nb00_nb04.md
 D reports/eda/progress/laporan_fix_audit_fragmen.md
 D reports/eda/progress/laporan_revisi_fragmen_4b.md
 D reports/eda/progress/laporan_tahap_0_reuse_check.md
 D reports/eda/progress/laporan_tahap_10_autocorr_fix.md
 D reports/eda/progress/laporan_tahap_1_pin_deps.md
 D reports/eda/progress/laporan_tahap_2_nb00_setup.md
 D reports/eda/progress/laporan_tahap_3_returns.md
 D reports/eda/progress/laporan_tahap_4_volatility.md
 D reports/eda/progress/laporan_tahap_5_autokorelasi.md
 D reports/eda/progress/laporan_tahap_6_swing_level.md
 D reports/eda/progress/laporan_tahap_7_swing_level_fix.md
 D reports/eda/progress/laporan_tahap_8_volatility_fix.md
 D reports/eda/progress/laporan_tahap_9_figures_fix.md
 D reports/governance/2026-10-07/audit-fondasi-B1.md
 D reports/governance/2026-10-07/hipotesis_lock_v1.md
 D reports/governance/2026-10-07/konfirmasi-R1-R2-R3.md
 D reports/governance/2026-10-07/putusan-arsitek-B1.md
 D reports/governance/2026-10-07/putusan-arsitek-F1.md
 D reports/governance/2026-10-07/putusan-arsitek-H1-H5.md
 D reports/governance/2026-10-07/reaudit-F2-F3-F4.md
 M requirements.txt
?? .ai/ASSISTANT_RULES.md
?? .ai/assistant/PROMPT_DISIPLIN.md
?? .ai/assistant/notes/
?? .ai/assistant/prompts/2026-10-06_audit-klenz_D1-D12.md
?? .ai/assistant/prompts/2026-10-06_audit-klenz_nb05.md
?? .ai/assistant/prompts/2026-10-06_batch-A-langkah2-3.md
?? .ai/assistant/prompts/2026-10-06_batch-B-langkah4-5-6.md
?? .ai/assistant/prompts/2026-10-06_commit-C-stage.md
?? .ai/assistant/prompts/2026-10-06_commit-C-susulan.md
?? .ai/assistant/prompts/2026-10-06_fix-nb05-batchA.md
?? .ai/assistant/prompts/2026-10-06_fix-nb05-batchB.md
?? .ai/assistant/prompts/2026-10-06_fix-nb05-langkah1.md
?? .ai/assistant/prompts/2026-10-06_fix_deviations.md
?? .ai/assistant/prompts/2026-10-06_langkah2_nb03.md
?? .ai/assistant/prompts/2026-10-06_langkah3-4_nb04-nb02.md
?? .ai/assistant/prompts/2026-10-06_langkah5_figures.md
?? .ai/assistant/prompts/2026-10-06_langkah6_dua-commit.md
?? .ai/assistant/prompts/2026-10-06_nb05_pola-review-akhir.md
?? .ai/assistant/prompts/2026-10-06_onboarding-auditor-baru_nb05.md
?? .ai/assistant/prompts/2026-10-06_onboarding-coder-baru.md
?? .ai/assistant/prompts/2026-10-06_paket-dokumen_MEDIUM-18.md
?? .ai/assistant/prompts/2026-10-06_persetujuan-ulang-ABC.md
?? .ai/assistant/prompts/2026-10-06_reaudit-klenz_ABC.md
?? .ai/assistant/prompts/2026-10-06_tanya-arsitek-Q1-Q2.md
?? .ai/assistant/prompts/2026-10-06_teguran-klenz-nb05.md
?? .ai/assistant/prompts/2026-10-06_teguran-paket-ABC.md
?? .ai/assistant/prompts/2026-10-08_spec-batch1-H1H2-arsitek.md
?? .ai/assistant/reviews/
?? .ai/assistant/verifications/2026-10-06_audit-nb05-langkah1-baru.md
?? .ai/assistant/verifications/2026-10-06_audit-nb05-langkah1.md
?? .ai/assistant/verifications/2026-10-06_batch-A.md
?? .ai/assistant/verifications/2026-10-06_batch-B.md
?? .ai/assistant/verifications/2026-10-06_batch-D1-D5.md
?? .ai/assistant/verifications/2026-10-06_commit-A-B.md
?? .ai/assistant/verifications/2026-10-06_commit-C.md
?? .ai/assistant/verifications/2026-10-06_fix-batchA.md
?? .ai/assistant/verifications/2026-10-06_fix-batchB.md
?? .ai/assistant/verifications/2026-10-06_fix-nb05-langkah1.md
?? .ai/assistant/verifications/2026-10-06_klaim_spark.md
?? .ai/assistant/verifications/2026-10-06_nb05_final.md
?? .ai/assistant/verifications/2026-10-06_reaudit-batchB.md
?? .ai/assistant/verifications/2026-10-06_reaudit-klenz_ABC.md
?? .ai/assistant/verifications/2026-10-06_reaudit-langkah3.md
?? .ai/assistant/verifications/2026-10-06_reaudit-nb05-langkah1.md
?? .ai/assistant/verifications/2026-10-06_respons-klenz-nb05.md
?? .ai/assistant/verifications/2026-10-06_stage-C.md
?? .ai/assistant/verifications/2026-10-08_gerbang-spec-H1H2.md
?? .ai/assistant/verifications/2026-10-08_pra-audit-batch3.md
?? .ai/assistant/verifications/2026-10-08_pra-audit-batch4.md
?? .ai/backup/
?? journal/daily/2026-10-08.md
?? reports/data_validation_2026-10-06.md
?? reports/eda/progress/00-setup/
?? reports/eda/progress/01-returns/
?? reports/eda/progress/02-volatility/
?? reports/eda/progress/03-autocorr/
?? reports/eda/progress/04-swings-levels/
?? reports/eda/progress/05-figures/
?? reports/eda/progress/06-regimes/.gitkeep
?? reports/eda/progress/06-regimes/laporan_tahap_13_report.md
?? reports/eda/progress/INDEX.md
?? reports/eda/progress/audit/
?? reports/eda/progress/fragmen-spread/
?? reports/go/
?? reports/governance/2026-10-07/Audit/
?? reports/governance/2026-10-07/arsitek/
?? reports/governance/2026-10-07/coder/
?? src/features/build_labels.py
?? tests/test_build_labels.py
?? thoughts/

jumlah baris porcelain:
97
```

---

## 11. C8 — Blob dokumen ini

Blok ini ditulis **setelah** seluruh isi di atas final. Baris **terakhir** berkas ini berisi blob dokumen **tanpa** baris tersebut — direproduksi dengan:

```
head -n -1 reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md | git hash-object --stdin
```

**[O19] — verifikasi pasca-penulisan terakhir:** baris terakhir di bawah adalah hash `head -n -1`; hash **penuh** dokumen (setelah baris C8) + `git status --porcelain` + `git log --oneline -1` diulang setelah penulisan terakhir dan dilaporkan di chat penyerahan (C8/C9 spec).
C8: 522c221c9d9f4ee3ad480282f13d0bf97a8942be
