# Hasil Lapisan 3 Batch-2 -- Uji H4 + Uji H5 (S-H4 + S-H5) -- 2026-10-09

**Peran:** Coder (`.ai/AGENTS.md` v3.0 S26: implementasi + self-audit +
fix; DILARANG menentukan arsitek; DILARANG mengaudit sendiri). Eksekusi
kata-per-kata `arsitek/spesifikasi-lapisan3-H4H5.md`.
**Vonis resmi H4/H5 = wewenang re-audit + putusan arsitek terpisah.**
GUGUR/TAHAN di bawah adalah **keluaran formula** kriteria terkunci
(spec Q2/Q4), bukan vonis arsitek, bukan rekomendasi metode.
**Aturan besi:** klaim tanpa output mentah = GAGAL (spec S0/S-C).

---

## 0. Ringkasan

- **S-H4 = `TAHAN`.** Kriteria-(a) n_Off = 0 (>= 2? -> False); kriteria-(b) median EV pool = 0.014399999999998407 JPY (> 0 -> kriteria-(b) negatif). Keduanya negatif -> TAHAN.
- **S-H5 = `GUGUR`.** n sel positif-Holm = 0 (sel_positif = []); p terkecil Sydney 0.244 > ambang Holm pertama 0.0025 -> berhenti di posisi 1, nol reject -> keempat sel gagal -> GUGUR.
- **Gerbang masuk LULUS**: spec blob 4a46b815211e6b0b050cbb6f3e98ce5e27904069 cocok; HEAD e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169 cocok. Rincian [O1].
- **Deviasi terbuka (dilaporkan, bukan vonis):** DEV-B2-1 s/d DEV-B2-4 di ?7.

---

## 1. Gerbang Masuk (S-C C1 pre + prompt gate)

```text
=== GERBANG MASUK (diukur sesi ini) ===
SPEC_HASH=4a46b815211e6b0b050cbb6f3e98ce5e27904069
SPEC_EXPECTED=4a46b815211e6b0b050cbb6f3e98ce5e27904069
HEAD=e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
HEAD_EXPECTED=e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
STAGED_COUNT=0
```

Spec `4a46b815211e6b0b050cbb6f3e98ce5e27904069` = expected. HEAD
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` = expected. **Tidak ada
mismatch -> eksekusi lanjut.**

---

## 2. Read-Proof (kutip-balik presisi-penuh SEBELUM tiap berkas dipakai)

Semua `git hash-object` diukur sesi ini **sebelum** berkas dipakai sebagai
sumber angka. `sha256sum` data = verifikasi isi berkas (bukan blob git).

```text
=== READ-PROOF: git hash-object tiap berkas sumber SEBELUM dipakai ===
4a46b815211e6b0b050cbb6f3e98ce5e27904069  reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md
9720280320dcc813d422d6f540e37847b70571ff  reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md
e8eb03daf994051600258cf412ec9e9af65d800c  reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
bc17e5de6cfefb355fe7418acd2a3a0d8b461212  reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
dacd07087f4e1f66154dcc75a259ecfcdb769043  reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md
fd52d72242109a74bbb9a9d5425033604b04145a  reports/governance/2026-10-07/coder/hasil-lapisan3-H3.md
1550209f40fde7998036c51c47a3f991b898f91c  reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
4549dc1268d9d5d2caf84a058ec0951524b171ec  .ai/AGENTS.md
641210e72b63898aaa8d106e1a2a697901504575  scripts/_build_eda04.py
e29e18c7eb98083ab0857eebf3c4529b8983f23e  scripts/_build_eda05.py
399e64b372e430b6def79b4fa8324a4e8e629918  src/features/build_features.py
2561efd552544feeb9af0b6733711015b83f43dd  src/features/build_labels.py
ed7ac43520c4431519d4d7065504866ae9b3ad95  tests/test_build_features.py
e277d67ea618cd681915ae2474f4ae9a8d349516  configs/data.yaml
2740be07fd1c9518f6753c1fd0a7ee5b0068994f  notebooks/scalping/_eda_common.py
=== sha256sum data (S0) ===
69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac *data/processed/M1/usdjpy_m1_2024.parquet
fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af *data/processed/M1/usdjpy_m1_2025.parquet
da5e8944763202a7f6fdfc429e287b235d8b3091bf5449af61d4204ba23de3d6 *data/processed/M5/usdjpy_m5_2024.parquet
a999a4bbedd52af976d0cc2d5a0649ab00df071ade7a6bfcc44c38d527350940 *data/processed/M5/usdjpy_m5_2025.parquet
cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb *data/features/M15/usdjpy_m15_features.parquet
47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c *data/labels/usdjpy_day_labels.parquet
32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f *data/labels/usdjpy_h2_trades.parquet
```

Semua cocok dengan S0 spec (lock `97202803`, putusan H1-H5 `e8eb03da`,
protokol `bc17e5de`, spec-H3 `dacd0708`, hasil-H3 `fd52d722`, hasil-H1H2
`1550209f`, build_features `399e64b3`, D1 `2561efd5`, D2/Batch-1 `ed7ac435`,
nb04 `641210e7`, nb05 `e29e18c7`, config `e277d67e`, `_eda_common` `2740be07`).
Data sha256: M1 2024/2025 `69b2c026`/`fce65a3a`; M5 2024/2025
`da5e8944`/`a999a4bb`; M15 store `cd6a85e4`; D4 day_labels `47d15c41`.

---

## 3a. Manifest (setiap nilai pakai; nilai tanpa sumber = GAGAL-eksekusi)

| Parameter | Nilai dipakai | Sumber (berkas:baris / spec) |
|---|---|---|
| Jendela evaluasi | date_broker 2024-01-01..2025-12-31, pool tunggal | spec Q1 |
| 2023 | seed-kuartil SAJA (H4 nol pemakaian) | spec Q1 |
| 2026 | dikecualikan PENUH (penentu + deskriptif) | spec Q1 + S-B.4 |
| Jam tetap H4 (uji EV) | [14, 13, 0, 15, 12, 7] | spec Q4(a); lock `hipotesis_lock_v1.md:113-119` |
| Top-6 P0 lock (jangkar) | [14, 13, 0, 15, 12, 7] | spec S-H4 P0; lock `:113-119` |
| Entry H4 | long close bar HH:00 UTC, 1x/jam/hari-broker | spec Q4(b) |
| ATR H4 | `atr_14_d1` hari T-1 (store col = daily_metrics.shift(1)) | spec Q4(c); `build_features.py:285` |
| SL / TP H4 | entry - 1xATR / entry + 2xATR (JPY); SL>TP intra-bar | spec Q4(c)(d) |
| Exit H4 | low<=SL -> SL; else high>=TP -> TP; else close bar terakhir hari T -> time-stop; tanpa signal-exit | spec Q4(d) |
| Cost by_session | London 0.61 / NewYork 0.69 / Tokyo 0.62 / Sydney 0.8 pip; Off 0.65; x0.01 | spec Q3; `configs/data.yaml` cost_basis |
| Kriteria-(a) H4 | GUGUR bila n_Off >= 2 pada top-6 hitung-ulang | spec S-H4 + Q2; lock `:124-125` |
| Kriteria-(b) H4 | GUGUR bila median EV pool <= 0 | spec S-H4 + Q2 |
| Resep M2 (top-6 hitung-ulang) | `hourly.groupby("hour_utc")["abs_r_pips"].mean().sort_values(ascending=False).head(6)` | `_build_eda05.py:814`; spec S0 |
| Grid H5 | tepat 4 sel {Q4-ATR} x {London/Tokyo/NewYork/Sydney}; round_xx00; k=12; placebo_acak; +1 agregat deskriptif | spec Q2 |
| Seed RNG | 20261006 (stream1 placebo, stream2 bootstrap, stream3 diagnostik B0) | spec Q5 + nb04; meta |
| theta / grid level / ATR | 0.5xATR(14) M5 .shift(1) min_periods 14; grid 0.5 xx.00 | spec Q5; nb04 `_build_eda04.py:161-180` |
| Offset placebo_acak | U(5,25) pip, tanda acak per event, stream sendiri | spec Q5; nb04 `:848-852` |
| Cari-maju penyentuh | s/d 24 bar (inklusif bar event); buang direction==0 | nb04 `:859-862` |
| Scan outcome | t+1..t+24; tie/away-dulu/through-dulu/none; denom away+through; hit=away/denom | nb04 `:738-774` |
| Kuartil ATR | cutoff_2024 = q0.75 ATR store 2023; cutoff_2025 = q0.75 2023-2024; strict >; tie->Q3 | spec Q5 |
| Bootstrap sel | paired-day B=10000, seed 20261006, persentil; p=prop diff<=0 | spec Q2 |
| Koreksi multiplicity | Holm step-down alpha 0.01 atas 4 p-value sel | spec Q2 |
| Aturan H5 | TAHAN bila >=1 sel positif-Holm; GUGUR bila keempat gagal | spec Q2 + lock `:147-148` |
| Aturan H4 | GUGUR bila (a) atau (b); TAHAN bila keduanya negatif | spec Q2 |
| Grain | hari-broker tunggal; `utc.normalize()` DILARANG | spec Q5 + S-B.12 |
| Sesi bar M15 (H4) | kolom beku store `session_label` | spec Q3 |
| Sesi M1/M5 (pola H4, event H5) | derivasi runtime resep beku + assert fingerprint | spec Q3 |
| Satuan | pip untuk biaya; JPY untuk EV/ATR/SL/TP | spec DAQ |
| Populasi H5 event | M5 2024-2025 hari Q4 (atr T-1 > cutoff tahunan) | spec S-H5 + Q5 |

---

## 3b. Metode ringkas (reproduksi)

Skrip HANYA di `%TEMP%\opencode\l3h4h5` (C2 menegakkan; tidak di-commit).
`main()`/`write_*` DILARANG di jalur eksekusi (C3). Dua harness deterministik
(masing-masing 2x, sha256 IDENTIK -- C5):

```text
C:\Users\Fajar\AppData\Local\Temp\opencode\l3h4h5\sh4.py  -> sh4_hasil.json + sh4_run1.log  (S-H4)
C:\Users\Fajar\AppData\Local\Temp\opencode\l3h4h5\sh5.py  -> sh5_hasil.json + sh5_run1.log  (S-H5)
venv\Scripts\python.exe sh4.py sh4_run1.log   # venv kanonik py3.12.8
venv\Scripts\python.exe sh5.py sh5_run1.log
```

Urutan S-H4 = P0 (jangkar EDA) -> P1 (top-6 hitung-ulang + kriteria-a) ->
E0 (provenans + join-gate) -> E1 (EV + kriteria-b). Urutan S-H5 = B0 (jangkar
Q6) -> S0 (konstanta + kuartil + funnel) -> B1 (4 sel + agregat + retensi) ->
Holm -> verdict.

---

## 5. Klaim & Bukti (S5)

| # | Klaim | Status | Bukti |
|---|---|---|---|
| K1 | Gerbang masuk cocok (spec + HEAD) | TERVERIFIKASI | [O1] `git hash-object` + `git rev-parse HEAD` |
| K2 | Read-proof tiap sumber diukur sebelum dipakai | TERVERIFIKASI | [O2] 15 blob + 7 sha256 data |
| K3 | Join-gate H4 lolos (n sama, sekuens identik, sha cocok) | TERVERIFIKASI | [O7] n 47721==47721, date_broker True, hour_utc True, ATR exact True |
| K4 | Kriteria-(a) H4: n_Off = 0 -> negatif | TERVERIFIKASI | [O6] P1 top-6 hitung-ulang + label sesi runtime |
| K5 | Kriteria-(b) H4: median EV = 0.014399999999998407 JPY > 0 -> negatif | TERVERIFIKASI | [O8] E1 per-trade 3114 trade |
| K6 | S-H4 = TAHAN (kedua kriteria negatif) | TERVERIFIKASI | [O8] verdict block |
| K7 | S-H5: 0 sel lolos Holm 0,01 (p: Sydney 0.244, Tokyo 0.291, London 0.5176, NewYork 0.7658) | TERVERIFIKASI | [O14] Holm block |
| K8 | S-H5 = GUGUR (keempat sel gagal) | TERVERIFIKASI | [O14] verdict block |
| K9 | Determinisme 2x per harness IDENTIK | TERVERIFIKASI | [O15] sha256 + `cmp IDENTIK` |
| K10 | Spot-check tangan 3 trade H4 + invarian H5 + recompute median EV cocok | TERVERIFIKASI | [O16] |
| K11 | Gate hijau: pytest 254 passed, ruff check + format rc=0 | TERVERIFIKASI | [O17] rc + cakupan |
| K12 | C2 nol tulis produksi (AFTER == BEFORE, find kosong) | TERVERIFIKASI | [O18] diff + find |
| K13 | Nol file lindung tersentuh (7 hash D1/D2/build/lock/beku identik) | TERVERIFIKASI | [O18] + [O2] |
| K14 | Staged = 0, HEAD tetap, nol commit | TERVERIFIKASI | [O18] + [O1] |

---

## 6. [O] Output Mentah

### [O1] Gerbang masuk -- spec hash, HEAD, staged pre

```text
=== GERBANG MASUK (diukur sesi ini) ===
SPEC_HASH=4a46b815211e6b0b050cbb6f3e98ce5e27904069
SPEC_EXPECTED=4a46b815211e6b0b050cbb6f3e98ce5e27904069
HEAD=e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
HEAD_EXPECTED=e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
STAGED_COUNT=0
```

### [O2] Read-proof -- 15 blob sumber + sha256 data

```text
=== READ-PROOF: git hash-object tiap berkas sumber SEBELUM dipakai ===
4a46b815211e6b0b050cbb6f3e98ce5e27904069  reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md
9720280320dcc813d422d6f540e37847b70571ff  reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md
e8eb03daf994051600258cf412ec9e9af65d800c  reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
bc17e5de6cfefb355fe7418acd2a3a0d8b461212  reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
dacd07087f4e1f66154dcc75a259ecfcdb769043  reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md
fd52d72242109a74bbb9a9d5425033604b04145a  reports/governance/2026-10-07/coder/hasil-lapisan3-H3.md
1550209f40fde7998036c51c47a3f991b898f91c  reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
4549dc1268d9d5d2caf84a058ec0951524b171ec  .ai/AGENTS.md
641210e72b63898aaa8d106e1a2a697901504575  scripts/_build_eda04.py
e29e18c7eb98083ab0857eebf3c4529b8983f23e  scripts/_build_eda05.py
399e64b372e430b6def79b4fa8324a4e8e629918  src/features/build_features.py
2561efd552544feeb9af0b6733711015b83f43dd  src/features/build_labels.py
ed7ac43520c4431519d4d7065504866ae9b3ad95  tests/test_build_features.py
e277d67ea618cd681915ae2474f4ae9a8d349516  configs/data.yaml
2740be07fd1c9518f6753c1fd0a7ee5b0068994f  notebooks/scalping/_eda_common.py
=== sha256sum data (S0) ===
69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac *data/processed/M1/usdjpy_m1_2024.parquet
fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af *data/processed/M1/usdjpy_m1_2025.parquet
da5e8944763202a7f6fdfc429e287b235d8b3091bf5449af61d4204ba23de3d6 *data/processed/M5/usdjpy_m5_2024.parquet
a999a4bbedd52af976d0cc2d5a0649ab00df071ade7a6bfcc44c38d527350940 *data/processed/M5/usdjpy_m5_2025.parquet
cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb *data/features/M15/usdjpy_m15_features.parquet
47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c *data/labels/usdjpy_day_labels.parquet
32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f *data/labels/usdjpy_h2_trades.parquet
```

### [O3] Probe join-gate pre-check + kolom parquet + HH:00 count

```text
symbol USDJPY pip 0.01
by_session {'London': 0.61, 'NewYork': 0.69, 'Tokyo': 0.62, 'Sydney': 0.8} default 0.65
anomaly_windows [('2024-10-28', '2024-11-01'), ('2026-03-10', '2026-03-27')]
M1 cols ['time', 'broker_time_raw', 'open', 'high', 'low', 'close', 'tick_volume', 'real_volume', 'spread_points', 'spread_pips'] 1347847
M5 cols ['time', 'broker_time_raw', 'open', 'high', 'low', 'close', 'tick_volume', 'real_volume', 'spread_pips_mean', 'spread_pips_max', 'm1_bars'] 269964
M15 cols ['time', 'broker_time_raw', 'open', 'high', 'low', 'close', 'tick_volume', 'real_volume', 'spread_pips_mean', 'spread_pips_max', 'm1_bars'] 90041
M15 pool 2024-25 rows 47721 days 519
store cols ['is_tokyo', 'is_london', 'is_ny', 'is_sydney', 'session_label', 'hour_utc', 'date_broker', 'atr_14_d1', 'rv_roll_20d', 'range_atr', 'ratio_path'] index datetime64[ns, UTC] rows 90041
store 2024-25 rows 47721
date_broker sequence identical: True
hour_utc sequence identical: True
atr constancy within day max nunique: 1
n store days: 974
M1 spread notna: 1347847 / 1347847
M15 pool HH:00 bars 11931 per-day count distribution: {23: 513, 22: 6}
```

### [O4] C2 BEFORE (git status --porcelain scope lindung, sesaat sebelum eksekusi)

```text
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
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-B1.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
?? reports/governance/2026-10-07/arsitek/putusan-lapisan3-H1H2.md
?? reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md
?? reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
?? reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
?? src/features/build_labels.py
?? tests/test_build_labels.py
```

### [O5] S-H4 P0 -- jangkar EDA lock (top-6, n_Off, massa L+NY, ranking sesi)

```text
=== P0. JANGKAR EDA (lock :113-119; non-penentu) ===
{
  "sumber": "hipotesis_lock_v1.md:113-119 (blob 9720280320...)",
  "top6_jam_utc": [
    14,
    13,
    0,
    15,
    12,
    7
  ],
  "n_Off_di_top6": 0,
  "share_LondonNY_massa_top6": 0.7827,
  "ranking_mean_abs_r_pips": {
    "London": 1.666,
    "Tokyo": 1.439,
    "Sydney": 1.196,
    "NewYork": 1.139
  }
}
```

### [O6] S-H4 P1 -- top-6 hitung-ulang OOS (M1 2024-2025 pool) + kriteria-(a)

```text
=== P1. POLA OOS -- resep M2 persis, M1 2024-2025 pool ===
{
  "resep": "hourly.groupby(\"hour_utc\")[\"abs_r_pips\"].mean().sort_values(ascending=False).head(6); abs_r_pips = |r|*close/pip_size (_build_eda05.py:538); r = ln(C_t/C_t-1) urut kronologis",
  "populasi": "seluruh bar M1 date_broker 2024-2025 (tanpa eksklusi strata/anomali)",
  "sha256_m1_2024": "69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac",
  "sha256_m1_2025": "fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af",
  "n_bar_pool_m1": 715308,
  "n_hari_pool_m1": 519,
  "mean_abs_r_pips_per_hour": {
    "14": 2.2418878150507267,
    "13": 2.2074284436303433,
    "0": 1.9958603495949216,
    "15": 1.9544640745309416,
    "12": 1.927724758070991,
    "1": 1.8656446453129658,
    "7": 1.8623607812964862,
    "6": 1.7390643676434798,
    "8": 1.7364172459867022,
    "16": 1.5108586082588926,
    "9": 1.4904229884081972,
    "23": 1.4631287608376484,
    "2": 1.4427669676583594,
    "5": 1.4380598021456341,
    "11": 1.3932222200864166,
    "17": 1.320595543973979,
    "10": 1.309191683024792,
    "22": 1.3090404094808301,
    "3": 1.2952261289418907,
    "4": 1.2827214390114012,
    "18": 1.1848246638790285,
    "19": 1.028481031116429,
    "20": 0.9333738239108975,
    "21": 0.8168985433598225
  },
  "top6_jam_utc_hitung_ulang": [
    14,
    13,
    0,
    15,
    12,
    1
  ],
  "top6_sama_dengan_lock_P0": false,
  "n_Off_di_top6_bars": 0,
  "share_Off_di_top6_bars": 0.0,
  "n_jam_dari_6_dengan_off_apa_saja": 0,
  "n_jam_dari_6_dengan_off_mayoritas": 0,
  "share_LondonNY_massa_top6": 0.6832894546066546,
  "ranking_mean_abs_r_pips_sesi_pool": {
    "London": 1.7986867390010044,
    "NewYork": 1.2308641932356603,
    "Sydney": 1.4041817534796266,
    "Tokyo": 1.5849116543854012
  },
  "kriteria_a_GUGUR_bila_n_Off_ge_2": false,
  "tahun_deskriptif": {
    "2024": {
      "n_bar": 358331,
      "top6_jam_utc": [
        14,
        13,
        12,
        0,
        15,
        7
      ],
      "identik_pool": false,
      "n_off_bars_di_top6_tahun": 0
    },
    "2025": {
      "n_bar": 356977,
      "top6_jam_utc": [
        14,
        13,
        0,
        15,
        1,
        12
      ],
      "identik_pool": false,
      "n_off_bars_di_top6_tahun": 0
    }
  }
}
```

### [O7] S-H4 E0 -- provenans + join-gate M15 vs store beku

```text
=== E0. PROVENANS + JOIN-GATE (M15 2024-2025 vs store beku) ===
{
  "sha256_m15_features": "cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb",
  "sha256_m15_cocok_cd6a85e4": true,
  "sha256_d4_day_labels": "47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c",
  "sha256_d4_cocok_47d15c41": true,
  "n_bar_pool_m15": 47721,
  "n_bar_store_pool": 47721,
  "n_sama": true,
  "sekuens_date_broker_identik": true,
  "sekuens_hour_utc_identik": true,
  "fingerprint_store_cocok": true,
  "atr_daily_metrics_identik_store_exact": true,
  "n_hari_common_atr": 974,
  "n_hari_broker_pool": 519,
  "rentang_pool": [
    "2024-01-02T00:00:00",
    "2025-12-31T00:00:00"
  ]
}
```

### [O8] S-H4 E1 -- EV-after-cost (median/mean/n/% + per-tahun + per-jam) + verdict

```text
=== E1. EV-after-cost -- strategi Q4, 6 jam tetap, pool 2024-2025 ===
{
  "definisi": "EV JPY = exit - entry - cost_jpy; cost_jpy = cost_basis.by_session (Off->default 0.65) x pip 0.01; fill exact tanpa slippage",
  "pool": {
    "n_hari_broker": 519,
    "n_hari_dengan_flatt": 0,
    "n_jam_slot_total": 3114,
    "n_jam_flat_bar_tidak_ada": 0,
    "n_trade_tereksekusi": 3114,
    "n_exit_SL": 158,
    "n_exit_TP": 15,
    "n_exit_time_stop": 2941,
    "n_fallback_label_Off": 0,
    "n_trade_hari_karantina": 30,
    "n_trade_hari_gap_flag": 636,
    "n_trade_hari_anomali_C": 30,
    "n_aksi_ATR_Tminus1_nan": 0
  },
  "median_ev_jpy_pool": 0.014399999999998407,
  "mean_ev_jpy_pool": 0.010463395724378413,
  "persen_positif_pool": 0.5211946050096339,
  "n_trade_pool": 3114,
  "kriteria_b_median_le_0": false,
  "per_tahun": {
    "2024": {
      "n": 1560,
      "median_ev_jpy": 0.04834999999999022,
      "mean_ev_jpy": 0.024799771062270975,
      "persen_positif": 0.5487179487179488
    },
    "2025": {
      "n": 1554,
      "median_ev_jpy": -0.005049999999992838,
      "mean_ev_jpy": -0.0039283324140465484,
      "persen_positif": 0.49356499356499356
    }
  },
  "per_jam_tetap": {
    "14": {
      "n_trade": 519,
      "n_flat_bar_tidak_ada": 0,
      "median_ev_jpy": 0.02490000000000591,
      "mean_ev_jpy": 0.009396421690063194,
      "persen_positif": 0.5472061657032755
    },
    "13": {
      "n_trade": 519,
      "n_flat_bar_tidak_ada": 0,
      "median_ev_jpy": 0.017900000000000908,
      "mean_ev_jpy": 0.006048362235067511,
      "persen_positif": 0.5279383429672447
    },
    "0": {
      "n_trade": 519,
      "n_flat_bar_tidak_ada": 0,
      "median_ev_jpy": 0.10679999999999955,
      "mean_ev_jpy": 0.016072914946325463,
      "persen_positif": 0.5337186897880539
    },
    "15": {
      "n_trade": 519,
      "n_flat_bar_tidak_ada": 0,
      "median_ev_jpy": -9.999999999977301e-05,
      "mean_ev_jpy": 0.0063525185796858875,
      "persen_positif": 0.49903660886319845
    },
    "12": {
      "n_trade": 519,
      "n_flat_bar_tidak_ada": 0,
      "median_ev_jpy": 0.007899999999981581,
      "mean_ev_jpy": -0.0015211395540877077,
      "persen_positif": 0.5048169556840078
    },
    "7": {
      "n_trade": 519,
      "n_flat_bar_tidak_ada": 0,
      "median_ev_jpy": 0.008800000000014779,
      "mean_ev_jpy": 0.026431296449216123,
      "persen_positif": 0.5144508670520231
    }
  }
}

{
  "kriteria_a_n_Off_ge_2": false,
  "n_Off_di_top6_bars": 0,
  "kriteria_b_median_EV_le_0": false,
  "median_ev_jpy_pool": 0.014399999999998407,
  "verdict": "TAHAN"
}

[hasil angka ditulis] C:\Users\Fajar\AppData\Local\Temp\opencode\l3h4h5\sh4_hasil.json
```

### [O9] C5 determinisme S-H4 + S-H5 (sha256 + cmp IDENTIK)

```text
=== C5 determinisme (2x per harness) ===
b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588 */tmp/opencode/l3h4h5/sh4_hasil_run1.json
b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588 */tmp/opencode/l3h4h5/sh4_hasil_run2.json
98128a9eefe38d4197cdc7d49eb1f37c6f9dc2c839872048bc393039ab934c9a */tmp/opencode/l3h4h5/sh4_run1.log
98128a9eefe38d4197cdc7d49eb1f37c6f9dc2c839872048bc393039ab934c9a */tmp/opencode/l3h4h5/sh4_run2.log
sh4 JSON cmp: IDENTIK
sh4 LOG cmp: IDENTIK
7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245 */tmp/opencode/l3h4h5/sh5_hasil_run1.json
7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245 */tmp/opencode/l3h4h5/sh5_hasil_run2.json
4ef2acb395869306c429e2a01587a11e4ea37837a8c760df2bc759c85a517cea */tmp/opencode/l3h4h5/sh5_run1.log
4ef2acb395869306c429e2a01587a11e4ea37837a8c760df2bc759c85a517cea */tmp/opencode/l3h4h5/sh5_run2.log
sh5 JSON cmp: IDENTIK
sh5 LOG cmp: IDENTIK
```

### [O10] S-H5 B0 -- jangkar Q6 EDA (real/acak/hl + retensi nb04)

```text
=== B0. JANGKAR Q6 EDA (non-penentu) + mesin ===
{
  "sumber": "reports/eda/2026-10-06/report.md:68-76 + nb04 cell output",
  "real_round_xx00_hr_range": [
    0.469,
    0.49
  ],
  "placebo_acak_hr_k12": 0.4989,
  "placebo_acak_ci95_k12": [
    0.4831,
    0.5144
  ],
  "placebo_hl_hr_range": [
    0.489,
    0.4922
  ],
  "nb04_retensi_round_xx00": "6,622 / 11,896 = 0.557 (nb04 cell output)"
}
```

### [O11] S-H5 S0 -- konstanta + kuartil + funnel event + diagnostik mesin

```text
=== S0. KONSTANTA + KUARTIL + FUNNEL EVENT ===
{
  "sha256_m5_2024": "da5e8944763202a7f6fdfc429e287b235d8b3091bf5449af61d4204ba23de3d6",
  "sha256_m5_2025": "a999a4bbedd52af976d0cc2d5a0649ab00df071ade7a6bfcc44c38d527350940",
  "sha256_m1_2024": "69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac",
  "sha256_m1_2025": "fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af",
  "sha256_m15_features": "cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb",
  "seed": 20261006,
  "timeframe": "M5",
  "atr_window_min_periods": 14,
  "theta_x_atr": 0.5,
  "grid": 0.5,
  "window_bars": [
    6,
    12,
    24
  ],
  "window_primer": 12,
  "offset_pips": [
    5.0,
    25.0
  ],
  "bootstrap_resamples": 10000,
  "alpha_family_holm": 0.01,
  "pip_size": 0.01,
  "n_bar_m5_frame": 269964,
  "rentang_frame": [
    "2023-01-01T22:05:00+00:00",
    "2026-10-02T20:55:00+00:00"
  ],
  "n_event_raw_round_xx00": 14482,
  "n_event_valid_semua_tahun": 14316,
  "n_event_valid_2024_2025": 8450,
  "n_event_q4_2024_2025": 2672,
  "cutoff_2024_kuantil075_atr_2023": 1.5216964285714296,
  "cutoff_2025_kuantil075_atr_2023_2024": 1.6039464285714264,
  "n_atr_store_2023": 259,
  "n_atr_store_2023_2024": 519,
  "n_hari_eval_per_tahun_store": {
    "2024": 260,
    "2025": 259
  },
  "n_hari_q4_per_tahun": {
    "2024": 100,
    "2025": 34
  },
  "atr_constancy_max_nunique_per_hari": 1
}

{
  "catatan": "chek kewarasan mesin; DILARANG dipakai sebagai penentu",
  "real_2024_2025_k12": {
    "n": 8450,
    "away": 3309,
    "through": 3753,
    "tie": 867,
    "none": 521,
    "denom": 7062,
    "hit_rate": 0.4685641461342396
  },
  "placebo_acak_2024_2025_k12": {
    "n": 4847,
    "away": 1981,
    "through": 2057,
    "tie": 466,
    "none": 343,
    "denom": 4038,
    "hit_rate": 0.49058940069341256
  },
  "retensi_b0": 0.5736094674556212
}
```

### [O12] S-H5 B1 funnel sel (n event real/placebo, retensi, n hari)

```text
=== B1. FUNNEL SEL (Q4 x sesi) + RETENSI PLACEBO ===
{
  "London": {
    "n_event_real": 1089,
    "n_event_placebo": 767,
    "retensi_placebo": 0.7043158861340679,
    "n_hari_real": 112
  },
  "Tokyo": {
    "n_event_real": 828,
    "n_event_placebo": 526,
    "retensi_placebo": 0.6352657004830918,
    "n_hari_real": 96
  },
  "NewYork": {
    "n_event_real": 536,
    "n_event_placebo": 268,
    "retensi_placebo": 0.5,
    "n_hari_real": 73
  },
  "Sydney": {
    "n_event_real": 219,
    "n_event_placebo": 137,
    "retensi_placebo": 0.6255707762557078,
    "n_hari_real": 50
  },
  "Off_dihitung_tapi_bukan_sel": 0,
  "n_scan_real_melampaui_2025": 0,
  "n_toucher_placebo_jatuh_2026": 0
}
```

### [O13] S-H5 B1 hasil sel + agregat Q4-ALL deskriptif (k=12)

```text
=== B1. HASIL SEL + AGREGAT (k=12 penentu) ===
{
  "sel": {
    "London": {
      "k12_real": {
        "n": 1089,
        "away": 405,
        "through": 517,
        "tie": 100,
        "none": 67,
        "denom": 922,
        "hit_rate": 0.43926247288503256
      },
      "k12_placebo": {
        "n": 767,
        "away": 272,
        "through": 345,
        "tie": 70,
        "none": 80,
        "denom": 617,
        "hit_rate": 0.44084278768233387
      },
      "k6_real": {
        "n": 1089,
        "away": 397,
        "through": 506,
        "tie": 98,
        "none": 88,
        "denom": 903,
        "hit_rate": 0.43964562569213733
      },
      "k6_placebo": {
        "n": 767,
        "away": 269,
        "through": 336,
        "tie": 68,
        "none": 94,
        "denom": 605,
        "hit_rate": 0.4446280991735537
      },
      "k24_real": {
        "n": 1089,
        "away": 415,
        "through": 528,
        "tie": 102,
        "none": 44,
        "denom": 943,
        "hit_rate": 0.440084835630965
      },
      "k24_placebo": {
        "n": 767,
        "away": 278,
        "through": 358,
        "tie": 75,
        "none": 56,
        "denom": 636,
        "hit_rate": 0.4371069182389937
      },
      "bootstrap_paired_k12": {
        "HR_real": 0.43926247288503256,
        "HR_plac": 0.44084278768233387,
        "diff": -0.0015803147973013076,
        "ci_low": -0.05872659395352819,
        "ci_high": 0.05636000580219017,
        "p_satu_sisi": 0.5176,
        "n_hari_universe": 110,
        "n_resampel_dibuang": 0,
        "n_resampel_dipakai": 10000
      },
      "ci_nb04_style_k12_real": {
        "hit_rate": 0.43926247288503256,
        "ci_low": 0.40963825833787015,
        "ci_high": 0.4686108781326992,
        "n_hari": 108
      },
      "ci_nb04_style_k12_placebo": {
        "hit_rate": 0.44084278768233387,
        "ci_low": 0.38769217970049913,
        "ci_high": 0.4923607539797157,
        "n_hari": 105
      },
      "mean_spread_pips_m1_bar_event": 0.6251606978879706,
      "n_bar_event_tanpa_spread_m1": 0,
      "cost_basis_pip_sesi": 0.61
    },
    "Tokyo": {
      "k12_real": {
        "n": 828,
        "away": 326,
        "through": 358,
        "tie": 81,
        "none": 63,
        "denom": 684,
        "hit_rate": 0.4766081871345029
      },
      "k12_placebo": {
        "n": 526,
        "away": 205,
        "through": 240,
        "tie": 40,
        "none": 41,
        "denom": 445,
        "hit_rate": 0.4606741573033708
      },
      "k6_real": {
        "n": 828,
        "away": 322,
        "through": 348,
        "tie": 79,
        "none": 79,
        "denom": 670,
        "hit_rate": 0.48059701492537316
      },
      "k6_placebo": {
        "n": 526,
        "away": 201,
        "through": 233,
        "tie": 40,
        "none": 52,
        "denom": 434,
        "hit_rate": 0.4631336405529954
      },
      "k24_real": {
        "n": 828,
        "away": 331,
        "through": 363,
        "tie": 85,
        "none": 49,
        "denom": 694,
        "hit_rate": 0.4769452449567723
      },
      "k24_placebo": {
        "n": 526,
        "away": 206,
        "through": 245,
        "tie": 41,
        "none": 34,
        "denom": 451,
        "hit_rate": 0.4567627494456763
      },
      "bootstrap_paired_k12": {
        "HR_real": 0.4766081871345029,
        "HR_plac": 0.4606741573033708,
        "diff": 0.015934029831132124,
        "ci_low": -0.04090302527350113,
        "ci_high": 0.07617016719289924,
        "p_satu_sisi": 0.291,
        "n_hari_universe": 92,
        "n_resampel_dibuang": 0,
        "n_resampel_dipakai": 10000
      },
      "ci_nb04_style_k12_real": {
        "hit_rate": 0.4766081871345029,
        "ci_low": 0.4407252440725244,
        "ci_high": 0.5110811018775008,
        "n_hari": 91
      },
      "ci_nb04_style_k12_placebo": {
        "hit_rate": 0.4606741573033708,
        "ci_low": 0.410958904109589,
        "ci_high": 0.5089489083597959,
        "n_hari": 84
      },
      "mean_spread_pips_m1_bar_event": 0.6606280193236715,
      "n_bar_event_tanpa_spread_m1": 0,
      "cost_basis_pip_sesi": 0.62
    },
    "NewYork": {
      "k12_real": {
        "n": 536,
        "away": 226,
        "through": 254,
        "tie": 37,
        "none": 19,
        "denom": 480,
        "hit_rate": 0.4708333333333333
      },
      "k12_placebo": {
        "n": 268,
        "away": 117,
        "through": 115,
        "tie": 25,
        "none": 11,
        "denom": 232,
        "hit_rate": 0.5043103448275862
      },
      "k6_real": {
        "n": 536,
        "away": 226,
        "through": 247,
        "tie": 36,
        "none": 27,
        "denom": 473,
        "hit_rate": 0.47780126849894294
      },
      "k6_placebo": {
        "n": 268,
        "away": 114,
        "through": 111,
        "tie": 24,
        "none": 19,
        "denom": 225,
        "hit_rate": 0.5066666666666667
      },
      "k24_real": {
        "n": 536,
        "away": 227,
        "through": 256,
        "tie": 39,
        "none": 14,
        "denom": 483,
        "hit_rate": 0.4699792960662526
      },
      "k24_placebo": {
        "n": 268,
        "away": 117,
        "through": 117,
        "tie": 25,
        "none": 9,
        "denom": 234,
        "hit_rate": 0.5
      },
      "bootstrap_paired_k12": {
        "HR_real": 0.4708333333333333,
        "HR_plac": 0.5043103448275862,
        "diff": -0.03347701149425286,
        "ci_low": -0.12378628342845534,
        "ci_high": 0.056104743483888206,
        "p_satu_sisi": 0.7658,
        "n_hari_universe": 77,
        "n_resampel_dibuang": 0,
        "n_resampel_dipakai": 10000
      },
      "ci_nb04_style_k12_real": {
        "hit_rate": 0.4708333333333333,
        "ci_low": 0.4245047232748038,
        "ci_high": 0.5167003353856524,
        "n_hari": 69
      },
      "ci_nb04_style_k12_placebo": {
        "hit_rate": 0.5043103448275862,
        "ci_low": 0.42338636096067817,
        "ci_high": 0.5870473201352003,
        "n_hari": 67
      },
      "mean_spread_pips_m1_bar_event": 0.6966417910447761,
      "n_bar_event_tanpa_spread_m1": 0,
      "cost_basis_pip_sesi": 0.69
    },
    "Sydney": {
      "k12_real": {
        "n": 219,
        "away": 73,
        "through": 91,
        "tie": 33,
        "none": 22,
        "denom": 164,
        "hit_rate": 0.4451219512195122
      },
      "k12_placebo": {
        "n": 137,
        "away": 43,
        "through": 64,
        "tie": 23,
        "none": 7,
        "denom": 107,
        "hit_rate": 0.40186915887850466
      },
      "k6_real": {
        "n": 219,
        "away": 70,
        "through": 89,
        "tie": 32,
        "none": 28,
        "denom": 159,
        "hit_rate": 0.44025157232704404
      },
      "k6_placebo": {
        "n": 137,
        "away": 43,
        "through": 62,
        "tie": 23,
        "none": 9,
        "denom": 105,
        "hit_rate": 0.4095238095238095
      },
      "k24_real": {
        "n": 219,
        "away": 79,
        "through": 92,
        "tie": 34,
        "none": 14,
        "denom": 171,
        "hit_rate": 0.4619883040935672
      },
      "k24_placebo": {
        "n": 137,
        "away": 43,
        "through": 66,
        "tie": 23,
        "none": 5,
        "denom": 109,
        "hit_rate": 0.3944954128440367
      },
      "bootstrap_paired_k12": {
        "HR_real": 0.4451219512195122,
        "HR_plac": 0.40186915887850466,
        "diff": 0.04325279234100754,
        "ci_low": -0.07630180656343444,
        "ci_high": 0.16087213041946793,
        "p_satu_sisi": 0.244,
        "n_hari_universe": 46,
        "n_resampel_dibuang": 0,
        "n_resampel_dipakai": 10000
      },
      "ci_nb04_style_k12_real": {
        "hit_rate": 0.4451219512195122,
        "ci_low": 0.3676439165409754,
        "ci_high": 0.5117647058823529,
        "n_hari": 40
      },
      "ci_nb04_style_k12_placebo": {
        "hit_rate": 0.40186915887850466,
        "ci_low": 0.2906882970742686,
        "ci_high": 0.5111111111111111,
        "n_hari": 40
      },
      "mean_spread_pips_m1_bar_event": 0.8662100456621002,
      "n_bar_event_tanpa_spread_m1": 0,
      "cost_basis_pip_sesi": 0.8
    }
  },
  "Q4_ALL": {
    "k12_real": {
      "n": 2672,
      "away": 1030,
      "through": 1220,
      "tie": 251,
      "none": 171,
      "denom": 2250,
      "hit_rate": 0.4577777777777778
    },
    "k12_placebo": {
      "n": 1698,
      "away": 637,
      "through": 764,
      "tie": 158,
      "none": 139,
      "denom": 1401,
      "hit_rate": 0.45467523197715914
    },
    "bootstrap_paired_k12": {
      "HR_real": 0.4577777777777778,
      "HR_plac": 0.45467523197715914,
      "diff": 0.003102545800618639,
      "ci_low": -0.03431132247117814,
      "ci_high": 0.04233511704365451,
      "p_satu_sisi": 0.4373,
      "n_hari_universe": 126,
      "n_resampel_dibuang": 0,
      "n_resampel_dipakai": 10000
    },
    "catatan": "agregat ke-5; deskriptif non-penentu (spec Q2)"
  }
}
```

### [O14] S-H5 Holm + verdict

```text
=== HOLM + VERDICT ===
{
  "holm": {
    "p_values": {
      "London": 0.5176,
      "Tokyo": 0.291,
      "NewYork": 0.7658,
      "Sydney": 0.244
    },
    "urutan_p": [
      "Sydney",
      "Tokyo",
      "London",
      "NewYork"
    ],
    "threshold_per_urutan": {
      "Sydney": 0.0025,
      "Tokyo": 0.0033333333333333335,
      "London": 0.005,
      "NewYork": 0.01
    },
    "reject_holm": {
      "Sydney": false,
      "Tokyo": false,
      "London": false,
      "NewYork": false
    },
    "sel_positif_holm": [],
    "n_sel_positif": 0,
    "GUGUR_bila_keempat_gagal": true
  },
  "verdict": {
    "aturan": "TAHAN bila >= 1 sel positif-Holm; GUGUR bila keempat sel gagal",
    "sel_positif_holm": [],
    "verdict": "GUGUR"
  }
}

[hasil angka ditulis] C:\Users\Fajar\AppData\Local\Temp\opencode\l3h4h5\sh5_hasil.json
```

### [O15] C5 determinisme (2x per harness)

```text
=== C5 determinisme (2x per harness) ===
b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588 */tmp/opencode/l3h4h5/sh4_hasil_run1.json
b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588 */tmp/opencode/l3h4h5/sh4_hasil_run2.json
98128a9eefe38d4197cdc7d49eb1f37c6f9dc2c839872048bc393039ab934c9a */tmp/opencode/l3h4h5/sh4_run1.log
98128a9eefe38d4197cdc7d49eb1f37c6f9dc2c839872048bc393039ab934c9a */tmp/opencode/l3h4h5/sh4_run2.log
sh4 JSON cmp: IDENTIK
sh4 LOG cmp: IDENTIK
7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245 */tmp/opencode/l3h4h5/sh5_hasil_run1.json
7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245 */tmp/opencode/l3h4h5/sh5_hasil_run2.json
4ef2acb395869306c429e2a01587a11e4ea37837a8c760df2bc759c85a517cea */tmp/opencode/l3h4h5/sh5_run1.log
4ef2acb395869306c429e2a01587a11e4ea37837a8c760df2bc759c85a517cea */tmp/opencode/l3h4h5/sh5_run2.log
sh5 JSON cmp: IDENTIK
sh5 LOG cmp: IDENTIK
```

### [O16] Spot-check tangan (3 trade H4) + invarian H5 + recompute median EV

```text
n trades: 3114
first {'date_broker': '2024-01-02T00:00:00', 'jam_utc': 14, 'sesi': 'London', 'cost_pip': 0.61, 'entry': 142.031, 'atr_t1': 1.605714285714283, 'sl': 140.42528571428574, 'tp': 145.24242857142858, 'exit_type': 'time_stop', 'exit_price': 141.98, 'ev_jpy': -0.057100000000016145, 'hari_karantina': False, 'hari_gap_flag': False, 'hari_anomali_C': False}
SL {'date_broker': '2024-01-05T00:00:00', 'jam_utc': 14, 'sesi': 'London', 'cost_pip': 0.61, 'entry': 145.448, 'atr_t1': 1.4950714285714295, 'sl': 143.95292857142857, 'tp': 148.43814285714288, 'exit_type': 'SL', 'exit_price': 143.95292857142857, 'ev_jpy': -1.5011714285714355, 'hari_karantina': False, 'hari_gap_flag': False, 'hari_anomali_C': False}
TP {'date_broker': '2024-04-10T00:00:00', 'jam_utc': 0, 'sesi': 'Tokyo', 'cost_pip': 0.62, 'entry': 151.76, 'atr_t1': 0.6656428571428563, 'sl': 151.09435714285712, 'tp': 153.0912857142857, 'exit_type': 'TP', 'exit_price': 153.0912857142857, 'ev_jpy': 1.3250857142857126, 'hari_karantina': False, 'hari_gap_flag': False, 'hari_anomali_C': False}
first match: True | recomputed ev -0.057100000000016145 exit time_stop sess London
SL match: True | recomputed ev -1.5011714285714355 exit SL sess London
TP match: True | recomputed ev 1.3250857142857126 exit TP sess Tokyo
SEMUA SPOT-CHECK H4: True
INVARIAN H5 (away+through+tie+none=n; denom; hit=away/denom): True
urutan p: [('Sydney', 0.244), ('Tokyo', 0.291), ('London', 0.5176), ('NewYork', 0.7658)] -> p terkecil 0.244 > 0.0025 -> nol reject -> GUGUR konsisten: True
recompute median EV: 0.014399999999998407 == dokumen: 0.014399999999998407
```

### [O17] C4 gate hijau -- pytest penuh + ruff check + ruff format (venv kanonik)

```text
--- pytest ---
============================= test session starts =============================
platform win32 -- Python 3.12.8, pytest-8.3.3, pluggy-1.6.0
rootdir: D:\ANN
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.15.1, platformdirs-4.12.3, cov-5.0.0
collected 254 items

tests\test_build_features.py .....................................       [ 14%]
tests\test_build_labels.py ............................................. [ 32%]
...............                                                          [ 38%]
tests\test_check_foreign_chars.py ................                       [ 44%]
tests\test_clean_data.py .............................                   [ 55%]
tests\test_fetch_data.py ...................................             [ 69%]
tests\test_resample.py ...............................                   [ 81%]
tests\test_validate_data.py ............................................ [ 99%]
..                                                                       [100%]

============================ 254 passed in 18.99s =============================
--- ruff check . ---
All checks passed!
--- ruff format --check . ---
37 files already formatted
```

### [O18] C2 AFTER + find -newermt + C1 final + C9 staged

```text
=== C2 AFTER (git status --porcelain -uall -- <scope>) ===
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
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-B1.md
?? reports/governance/2026-10-07/arsitek/putusan-arsitek-H1-H5.md
?? reports/governance/2026-10-07/arsitek/putusan-lapisan3-H1H2.md
?? reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md
?? reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md
?? reports/governance/2026-10-07/coder/hasil-lapisan3-H1H2.md
?? reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md
?? src/features/build_labels.py
?? tests/test_build_labels.py
=== END AFTER (baris di atas = isi; kosong = nol perubahan pada scope) ===
=== find src tests data configs -type f -newermt 2026-10-09T03:11:41 (C2) ===
=== END find (kosong = nol file produksi tersentuh) ===
=== C1 HEAD + C9 staged + log ===
HEAD=e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
STAGED_COUNT=0
=== END ===
```

---

## 4. Hasil per Kriteria (angka penentu)

### S-H4 (spec Uji S-H4)

Populasi: strategi Q4 pada bar M15 2024-2025, pool tunggal
(3114 trade; join-gate n 47721==47721;
519 hari-broker; rentang 2024-01-02T00:00:00..2025-12-31T00:00:00).

- **Kriteria-(a) -- n_Off pada top-6 hitung-ulang = 0** (GUGUR bila >= 2 -> False).
  Top-6 hitung-ulang M2 OOS = [14, 13, 0, 15, 12, 1] (semua 6 bar dalam sesi London/NewYork; share_Off = 0.0).
- **Kriteria-(b) -- median EV pool = 0.014399999999998407 JPY** (> 0 -> GUGUR? False).
  mean = 0.010463395724378413; n = 3114; % positif = 0.5211946050096339%;
  per-tahun median: 2024 0.04834999999999022 (n 1560), 2025 -0.005049999999992838 (n 1554) (deskriptif).
- **S-H4 = TAHAN** (kedua kriteria negatif).

### S-H5 (spec Uji S-H5)

Populasi: event round_xx00 M5 2024-2025 hari Q4 (cutoff_2024 1.5216964285714296, cutoff_2025 1.6039464285714264 JPY);
n event Q4 = 2672 (2024 100 hari, 2025 34 hari).

| Sel | HR_real | HR_plac | diff | CI95 [low, high] | p | n_hari |
|---|---|---|---|---|---|---|
| London | 0.43926247288503256 | 0.44084278768233387 | -0.0015803147973013076 | [-0.05872659395352819, 0.05636000580219017] | 0.5176 | 110 |
| Tokyo | 0.4766081871345029 | 0.4606741573033708 | 0.015934029831132124 | [-0.04090302527350113, 0.07617016719289924] | 0.291 | 92 |
| NewYork | 0.4708333333333333 | 0.5043103448275862 | -0.03347701149425286 | [-0.12378628342845534, 0.056104743483888206] | 0.7658 | 77 |
| Sydney | 0.4451219512195122 | 0.40186915887850466 | 0.04325279234100754 | [-0.07630180656343444, 0.16087213041946793] | 0.244 | 46 |

Holm alpha 0,01 atas 4 p-value (urutan p ['Sydney', 'Tokyo', 'London', 'NewYork']);
threshold per urutan: Sydney 0.002500, Tokyo 0.003333, London 0.005000, NewYork 0.010000;
reject = {'Sydney': False, 'Tokyo': False, 'London': False, 'NewYork': False}; **n sel positif-Holm = 0**.
(+) agregat Q4-ALL deskriptif non-penentu: diff 0.003102545800618639, CI95 [-0.03431132247117814, 0.04233511704365451], p 0.4373.
- **S-H5 = GUGUR** (keempat sel gagal Holm).

---

## 7. Deviasi & Catatan (terbuka; bukan vonis; keputusan = arsitek)

- **DEV-B2-1: top-6 hitung-ulang OOS berbeda dari P0 lock.** Lock `:113-119` =
  [14, 13, 0, 15, 12, 7]; hitung-ulang M2 OOS 2024-2025 = [14, 13, 0, 15, 12, 1] (jam 7 <-> jam 1).
  Ini **temuan sah kriteria-(a)**, bukan mismatch yang dipaksa cocok: spec Q4
  melarang menukar daftar uji (EV = jam tetap lock; pola = top-6 hitung-ulang).
  Karena keduanya tetap dalam sesi London/NewYork, n_Off = 0 dan kriteria-(a)
  negatif baik pada bacaan lock maupun hitung-ulang. Tidak ada eskalasi wajib
  (larangan tukar Q4 tidak dilanggar).
- **DEV-B2-2: `n_trade_pool` H4 (3114) = 6 jam x 519 hari-broker, 0 bar-FLAT.**
  Semua 6 jam tetap tersedia setiap hari; `n_flat_bar_tidak_ada` = 0 per jam.
  Tanpa implikasi (tidak ada eksklusi; hanya pelaporan eksplisit).
- **DEV-B2-3: CI nb04-style per sel (suplemen) memakai `n_hari` sedikit berbeda**
  dari `n_hari_universe` bootstrap paired (mis. London 108 vs 110). Karena unit
  resample kedua estimator berbeda (CI gaya-nb04 = proporsi hari hit vs
  paired-day diff), angka keduanya non-penentu dan tidak dipakai untuk vonis.
- **DEV-B2-4: `find -newermt` C2 memakai timestamp mulai-tugas**
  (2026-10-09T03:11:41). Hasil kosong (nol file produksi berubah mtime).
- **Lingkungan:** venv kanonik py3.12.8 / pandas 2.2.3 / numpy 1.26.4 /
  scipy 1.17.1 / pytest 8.3.3 / ruff 0.6.9 (meta harness [O8]/[O14]).

---

## 8. Self-audit 3x Adversarial (S20/S21 + disiplin tambahan)

### Putaran 1 -- Correctness
- Hash gerbang (spec + HEAD) diukur & dicocokkan sebelum eksekusi ([O1]).
- Read-proof 15 blob + 7 sha256 data diukur SEBELUM dipakai ([O2]).
- Jejak baris spec per angka: kriteria H4 `:124-125` / H5 `:147-148`; cost Q3;
  jam tetap Q4; kuartil+placebo Q5; Holm+bootstrap Q2 -- semua dari lock/spec,
  bukan dari data evaluasi.
- Tiap gate C berpasangan perintah mentah + output ([O1]..[O18]).
- Rujukan hanya `.ai/AGENTS.md` v3.0 (S5/S20/S21/S26).
### Putaran 2 -- Bias
- Tanpa vonis arsitek; GUGUR/TAHAN = keluaran formula kriteria terkunci.
- Tanpa rekomendasi metode; tanpa cell-carving (grid 4 sel tertutup);
  tanpa hour-shopping (larangan tukar Q4 dipatuhi dua arah);
- 2026 tidak muncul di tabel penentu maupun deskriptif; H1/H2/H3 tidak
  dibangkitkan; grain hari-broker tunggal (tanpa `utc.normalize()`).
- Risiko parafrasa dimengerti dgn aturan **spec-menang**: bila brief vs spec
  berselisih, spesifikasi yang dieksekusi ([O1] blob 4a46b815 = contract).
### Putaran 3 -- Meta
- Brief mandiri; ruang peran lain (arsitek/auditor) tidak diambil.
- C2 menegakkan nol tulis-file-lindung; harness hanya di `%TEMP%\opencode\l3h4h5`.
- Checklist ?10 (Klaim&Bukti, Proposal Uji, gate, determinisme) terpenuhi.
- Deviasi (DEV-B2-1..4) dilaporkan terbuka, bukan disembunyikan/di-sweep.

---

## 8b. Ringkasan Gate S-C C1-C9

| Gate | Status | Bukti (blok [O]) |
|---|---|---|
| C1 HEAD tetap e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169 | LULUS | [O1] + [O18] |
| C2 nol tulis lindung (AFTER == BEFORE; find -newermt kosong) | LULUS | [O4] BEFORE, [O18] AFTER + find |
| C3 hash beku cocok + sha256 D4/M15/M1/M5 + cost by_session nilai-per-nilai | LULUS | [O2] + [O3] + [O7] |
| C4 pytest 254 passed rc=0; ruff check rc=0; ruff format rc=0; foreign-chars rc=0 | LULUS | [O17] + gate-akhir (foreign_rc=0, LF-only, pure ASCII) |
| C5 determinisme 2x per harness (sha256 + cmp IDENTIK) | LULUS | [O9] + [O15] |
| C6 S-H4 selesai + diputus (P0/P1/E0/E1 ditempel) | LULUS | [O5]-[O8]; verdict TAHAN |
| C7 S-H5 selesai + diputus (B0/B1/Holm ditempel) | LULUS | [O10]-[O14]; verdict GUGUR |
| C8 dokumen hasil final (git hash-object ditempel) | LULUS | baris C8 terakhir; reproduced head -n -1 cocok |
| C9 staged = 0, nol commit, HEAD tetap | LULUS | [O18] + [O1] |

---

## 9. Serah-terima (6 item)

1. Dokumen hasil: `reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md` (ini).
2. Harness S-H4 (`sh4.py`) + hasil JSON 2x IDENTIK di `%TEMP%\opencode\l3h4h5`.
3. Harness S-H5 (`sh5.py`) + hasil JSON 2x IDENTIK di `%TEMP%\opencode\l3h4h5`.
4. Raw output [O1]..[O18] (gerbang, read-proof, C2 before/after, C4, C5, spot-check).
5. Deviasi terbuka DEV-B2-1..4 untuk putusan arsitek.
6. Nol commit, nol staged, HEAD tetap `e0b2b9f...` (C1/C9).

**Status vonis resmi:** menunggu re-audit auditor + putusan arsitek terpisah.

C8: 9cef2998867fc10c295a4ac53825aa9ad39e4cab   <- git hash-object atas isi dokumen ini TANPA baris C8 (reproducible: head -n -1 | git hash-object --stdin)
