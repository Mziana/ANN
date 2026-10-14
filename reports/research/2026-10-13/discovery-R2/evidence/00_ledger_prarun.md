# LEDGER Pra-Run Discovery-R2 (D2-7 + Amandemen-R2-1 B2/B4/C1/C5)

Ditulis SEBELUM run pertama 2026-10-13. Tanpa ledger ini = run gagal.
Otoritas: `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R2.md`
(SHA-256 `C05D5E4F…80654C5`, cocok dengan objek tersertifikasi re-audit).
Prasyarat TERPENUHI: re-audit fokus R2 = LULUS 8/8 (SESSION_LOG 2026-10-13).

## Kunci beku pra-run

- Seed bootstrap: **1337**. 10.000 resample, cluster = hari-UTC t0.
  Ganti seed = ronde baru.
- Setting evaluasi beku (B2): **horizon race 10 bar SESUDAH bar entry**
  (t0+2..t0+11, TIME exit = close t0+11); **paket ATR tunggal**
  (SL=1,5xATR, TP=2,0xSL=3,0xATR, DIBEKUKAN saat entri); biaya
  **observed net**. Horizon deskriptif lain + Q1 peta = tidak mengangkat
  kandidat. k=1,5 / RR=2,0 / seed 1337 tetap (tanpa angka alternatif).
- Paruh stabilitas (B4 — DISALIN dari spec, bukan hitung-ulang):
  Paruh-1 = **2026-01-01 s.d. 2026-05-18**; Paruh-2 = **2026-05-19 s.d.
  2026-10-02** (anomali 10–27 Mar sudah keluar dari keduanya).
  Implementasi: `day < "2026-05-19"` = paruh-1.
- Kunci config spread (literal `configs/data.yaml`, SHA-256 `1127514518AA…`,
  identik objek ledger R1 — file tak berubah):
  `cost_basis.by_session` = {London: 0,61; NewYork: 0,69; Tokyo: 0,62;
  Sydney: 0,80}; `cost_basis.default` = 0,65 (fallback sesi tak terpetakan);
  `stress_bands.p95.by_session` = {London: 0,8; NewYork: 1,2; Tokyo: 0,9;
  Sydney: 1,5}; `p95.default` = 1,0 (fallback). DILARANG:
  `spread.default`, `by_year` (semua blok), `stress_multiplier`.
- Komisi = **0,3 pip round-turn per event** (R-6; total per round turn;
  ASUMSI). Slippage conservative +0,2 (ASUMSI), stress +0,3 (ASUMSI).
- Sesi = `exclusive_label(session_flags())` dari
  `notebooks/scalping/_eda_common.py` (`82F02CEB1975…`, tak berubah);
  prioritas London > NewYork > Tokyo > Sydney > Off.
- 1 pip USDJPY = 0,01 (`pip_size`, `price_digits` = 3).
- Anomali 2026-03-10..03-27 (19.119 bar, BELUM TERVERIFIKASI) KELUAR dari
  denominator (tanggal UTC t0) + jendela evaluasi yang menyeberanginya
  DIBUANG (`ANOMALY_CROSS`). Tanpa 2024/2025/2023 untuk evaluasi (B7:
  ketiganya membawa caveat kontaminasi, tak satu pun bed confirmation
  bersih — dicatat, tak diputuskan kini).
- Q0: sel evaluable (tanpa cancel) < 300 = DROPPED, tidak dinilai
  (preseden R1; E3 < 300 = GUGUR-dilaporkan, temuan bukan tuning).

## Cakupan sesi-2026 terukur (recon pra-run, bukan run)

M1-2026: 269.846 bar (2026-01-01T23:00Z .. 2026-10-02T20:57Z).
Sesi: London 94.068 / Tokyo 85.968 / NewYork 68.452 / Sydney 21.358 /
**Off 0 bar**. Semua sesi terpetakan di literal by_session → fallback
default diharapkan 0; bila muncul, dilapor (bukan diam-diam).

## Skala ATR-2026 terukur (recon pra-run; angka 2026 dihitung, bukan 2024)

Resep verbatim `_build_eda06.py:500-533` (bucket lantai-UTC 5min,
n>=3, TR guard kontiguitas, mean rolling-14 + guard span 100min,
merge_asof backward toleransi 15min, keputusan di AKHIR bar M1).
- ATR tersedia: 238.300 / 269.846 bar (88,3%; NaN = awal tahun + gap +
  konstruksi-M5 tanpa bar anomali + toleransi 15min).
- ATR M5(14): mean **5,1059** pip, median **4,2429** pip (2024: mean 6,74
  — 2026 lebih tenang; densely dicatat, bukan dipakai menyetel).
- Skala beku per event: SL = 1,5xATR (~766 point pada mean),
  TP = 3,0xATR (~1.532 point pada mean). Nilai aktual per event =
  ATR-t0 × {1,5; 3,0}, dibekukan, tersimpan di `atr/sl_pips/tp_pips`.
- Uji kausalitas: hitung-ulang dari prefix di 2 indeks tetap harus
  identik (assert di run; gagal = run gagal).

## Verifikasi `src/data/resample.py` (C5; untuk M15 lampiran D-8)

`54FC73693B0F…` (tak berubah dari R1), 351 baris.
`resample_frame(M1-2026, M15)` = 18.026 bucket; OHLC identik
18.026/18.026 vs `data/processed/M15/usdjpy_m15_2026.parquet`;
`m1_bars` sum = 269.846 = input (nol bar sintetis). Konvensi: bucket
jam-dinding broker, label awal interval, harga = bid. Dipakai hanya
untuk bias M15 lampiran D-8 R2. (M5-untuk-ATR memakai resep EDA-06
verbatim di atas, sesuai definisi D2-2; bukan resample_frame.)

## Judgment tercatat (bukan spec; terbuka veto arsitek)

- J1 (D2-5, loop-dari-k=1): race = 10 bar SESUDAH bar entry t0+1, yaitu
  t0+2..t0+11; kbar 1..10; TIME exit = close t0+11 (sisi keluar).
  Label "H+10" = 10 bar race, bukan exit t0+10. Peta horizon deskriptif
  H+1..H+20 (entry t0+1 → exit t0+H) dipertahankan gaya-R1 untuk Q1.
- J2: MFE/MAE + waktu dihitung sisi-keluar atas jendela race t0+2..t0+11
  (analog R1 yang memakai jendela race-nya t0+1..t0+10).
- J3: Q0 memakai n_eval (evaluable, tanpa cancel) — preseden R1.
- J4: cluster bootstrap = tanggal UTC t0 (judgment R1, dilanjutkan).
- J5: pemeriksaan gap memakai epoch broker mentah (diff != 60 dtk);
  jendela liputan t0+1..t0+20 (mencakup horizon peta + race).

## Baris ledger (§9.1 warisan, adaptasi R2)

| event_id | mekanisme | definisi informasi-sampai-t0 | arah | feature diizinkan | outcome | biaya | horizon | unit bootstrap | eksklusi | alasan ilmiah | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1-N{4,5,6}-D{2.5,3.5} (6 sel, 1 family) | Exhaustion-to-reversal (R1 D-1 verbatim) | N tutup searah beruntun sebelum t0 (bar t0−N..t0−1, doji putus); displacement signed ≥ D pip; t0 lawan arah, body ≥ 50% range (range>0) | arah bar t0 | OHLC M1 ≤ t0, ATR14-M1, ATR-M5 beku, sesi, spread histori | paket ATR tunggal + horizon peta + MFE/MAE + AMBIGUOUS | 3 lapis D2-4 | race 10 bar (J1); peta +1/+2/+3/+5/+10/+15/+20 | hari-UTC t0 | anomali 10–27 Mar (t0 + cross); sel <300 dropped | falsifikasi §7 warisan R1 | PRA-RUN |
| E2 (1 sel, 1 family) | Pullback-then-continuation (R1 D-1 verbatim) | expansion: \|close[e]−close[e−20]\| ≥ 1,0×ATR14-M1(e), e∈[t0−5,t0−1] terdekat; retrace adverse maks ≤ 40% range expansion; t0 tutup searah dorongan | arah expansion | sama | sama | sama | sama | sama | sama + e<t0 ketat | falsifikasi §7 warisan R1 | PRA-RUN |
| E3 (1 sel, 1 family) | Compression-to-expansion (R1 D-1 verbatim) | W = 30 bar t0−30..t0−1; range(W) ≤ 0,5×median 20 window non-overlap sebelumnya; break close[t0] ≥ edge+1,0pip / ≤ edge−1,0pip | arah break | sama | sama | sama | sama | sama | sama | falsifikasi §7 warisan R1 | PRA-RUN |

ATR14-M1 = Wilder RMA-14 (hanya definisi E2). ATR barrier = M5(14)
resep EDA-06, dibekukan saat entri. Event tidak lahir dari contoh chart
pasca-outcome (D-4.1 warisan).

## Kontrak eksekusi per event (D2-5)

- Entry = OPEN bar t0+1 (bar hilang → CANCEL NO_ENTRY_BAR). Exit horizon
  peta = close bar t0+H sisi keluar.
- Bid = OHLC tersimpan; ask = bid + spread_pips×0,01 per bar
  (rekonstruksibel). BUY: entry ASK, exit BID. SELL: entry BID, exit
  ASK. Spread nol dilarang. Mid dilarang.
- BUY race (j = t0+2..t0+11): TP bila bid_high − entry_ask ≥ TP;
  SL bila bid_low − entry_ask ≤ −SL. SELL: TP bila entry_bid − ask_low
  ≥ TP; SL bila ask_high − entry_bid ≥ SL.
- Kedua barrier satu bar tanpa urutan = AMBIGUOUS_SEQUENCE (buang dari
  evaluasi + hitung eksplisit; beda sadar dari EDA-06 yang menghitungnya
  SL — C1).
- Buang berurutan (nol imputasi, jumlah per alasan dilaporkan):
  GAP (jendela t0+1..t0+20 tak menit-berturut) → ANOMALY_CROSS →
  ATR_NA (ATR t0 NaN) → OFF_SESSION (sesi t0 Off).

## Manifest input (SHA-256, pra-run)

`00_manifest.json`: M1-2026 parquet `7F267BB94005…`; `configs/data.yaml`
`1127514518AA…`; `resample.py` `54FC73693B0F…`; `_eda_common.py`
`82F02CEB1975…`; spec R2 `C05D5E4FE94A…`; harness d1/d2/d3/d4/run
(tercantum penuh di manifest).
