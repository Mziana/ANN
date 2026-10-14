# LEDGER Pra-Run Discovery-R1 (D-4.1 + A-C1 + A-C5)

Ditulis SEBELUM run pertama 2026-10-13. Tanpa ledger ini = run gagal.
Otoritas: `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R1.md`
(`c85340ef08af`, 21.307 B).

## Kunci beku pra-run

- Seed bootstrap: **1337** (A-C1). 10.000 resample, cluster = hari-UTC t0.
  Ganti seed = ronde baru.
- Setting evaluasi beku: horizon **H+10 M1 dari t0 close**; barrier **TP 2,5 /
  SL 2,5 pip**; biaya **observed net**. Horizon/ladder lain = pemetaan
  deskriptif, tidak mengangkat kandidat (A-H2).
- Kunci config spread (literal `configs/data.yaml`, `1127514518aa`):
  `cost_basis.by_session` = {London: 0,61; NewYork: 0,69; Tokyo: 0,62;
  Sydney: 0,80}; `cost_basis.default` = 0,65 (fallback sesi Off);
  `stress_bands.p95.by_session` = {London: 0,8; NewYork: 1,2; Tokyo: 0,9;
  Sydney: 1,5}; `p95.default` = 1,0 (fallback Off). DILARANG:
  `spread.default`, `by_year`, `stress_multiplier`.
- Komisi = **0,3 pip round-turn per event** (R-6; bacaan: total per round
  turn; ASUMSI). Slippage conservative +0,2 (ASUMSI), stress +0,3 (ASUMSI).
- Sesi = `exclusive_label(session_flags())` dari
  `notebooks/scalping/_eda_common.py` (`82f02ceb1975`); prioritas
  London > NewYork > Tokyo > Sydney > Off.
- 1 pip USDJPY = 0,01 (`pip_size`, `price_digits` = 3).
- Anomali 2024-10-28..11-01 KELUAR dari denominator (tanggal UTC t0).
  SA-03 = 2023-H1, tak relevan untuk run 2024-only. Tanpa 2025/2023-H2/2026.
- H1/H2 = belahan kalender UTC (Jan–Jun / Jul–Des). Cluster bootstrap =
  tanggal UTC t0 (judgment tercatat, bukan spec).

## Verifikasi `src/data/resample.py` (A-C5)

`54fc73693b0f`, 351 baris. `resample_frame(M1-2024, M15)` menghasilkan
23.909 bucket, OHLC identik 23.909/23.909 vs
`data/processed/M1/M15/usdjpy_m15_2024.parquet`, `m1_bars` sum = 358.331 =
input (nol bar sintetis). Konvensi: bucket jam-dinding broker, label awal
interval, harga = bid. Dipakai hanya untuk bias M15 lampiran D-8.

## Baris ledger (§9.1)

| event_id | mekanisme | definisi informasi-sampai-t0 | arah | feature diizinkan | outcome | biaya | horizon | unit bootstrap | eksklusi | alasan ilmiah | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1-N{4,5,6}-D{2.5,3.5} (6 sel, 1 family) | Exhaustion-to-reversal: reversal selesai t0 close hasilkan gerak lawan cukup besar sebelum adverse+biaya | N tutup searah beruntun sebelum t0 (bar t0−N..t0−1, doji putus); displacement signed (close[t0−1]−open[t0−N]) ≥ D pip; t0 lawan arah, body ≥ 50% range (range>0) | arah bar t0 (lawan push) | OHLC M1 ≤ t0, ATR14, sesi, spread histori | barrier TP/SL + horizon tetap + MFE/MAE + AMBIGUOUS | 3 lapis D-3.3 | evaluasi H+10; peta +1/+2/+3/+5/+15/+20 | hari-UTC t0 | anomali 28 Okt–1 Nov; sel <300 event dropped | falsifikasi §7: reversal butuh future swing, atau MFE tak lewati biaya/MAE | PRA-RUN |
| E2 (1 sel, 1 family) | Pullback-then-continuation: pullback kecil selesai t0 kembali searah dorongan sebelum invalidasi | expansion: \|close[e]−close[e−20]\| ≥ 1,0×ATR14(e), e∈[t0−5,t0−1] (terdekat dipakai); retrace maks adverse dari ekstrem expansion atas bar e+1..t0 ≤ 40% range expansion; t0 tutup searah dorongan | arah expansion | sama | sama | sama | sama | sama | sama + e<t0 ketat | falsifikasi §7: arah awal pakai future high/low, atau net tak kalahkan stres | PRA-RUN |
| E3 (1 sel, 1 family) | Compression-to-expansion: break t0 punya continuation netto sebelum false break | W = 30 bar t0−30..t0−1; range(W) ≤ 0,5×median 20 window 30-bar non-overlap sebelumnya (t0−630..t0−31); break: close[t0] ≥ maxHigh(W)+1,0pip (LONG) atau ≤ minLow(W)−1,0pip (SHORT) | arah break | sama | sama | sama | sama | sama | sama | falsifikasi §7: break pakai range sesudah t0, atau barrier net tak lebih baik dari baseline | PRA-RUN |

ATR14 = Wilder RMA-14 true range, nilai pada bar terakhir selesai sebelum
titik ukur. Event tidak lahir dari contoh chart pasca-outcome (D-4.1).

## Kontrak eksekusi per event (D-3.1/D-3.2)

- Entry = OPEN bar t0+1 (bar hilang → CANCEL NO_ENTRY_BAR). Horizon dari t0
  close; exit horizon = close bar t0+H sisi keluar.
- Bid = OHLC tersimpan; ask = bid + spread_pips×0,01 per bar (rekonstruksibel).
  BUY: entry ASK, exit BID. SELL: entry BID, exit ASK. Spread nol dilarang
  (tak ada spread nol di eksekusi; biaya config selalu >0). Mid dilarang.
- BUY: TP tersentuh bila bid_high − entry_ask ≥ TP; SL bila bid_low −
  entry_ask ≤ −SL. SELL: TP bila entry_bid − ask_low ≥ TP; SL bila
  entry_bid − ask_high ≤ −SL (ask_high − entry_bid ≥ SL).
- Kedua barrier satu bar tanpa urutan = AMBIGUOUS_SEQUENCE (buang + hitung
  eksplisit per kombinasi, D-3.1).
- Jendela horizon berlubang (bar hilang t0+1..t0+H) → CANCEL GAP.

## Manifest input (SHA-256, pra-run)

`00_manifest.json`: M1-2024 parquet `69b2c026d3ac…` (7.186.113 B);
`configs/data.yaml` `1127514518aa…`; `resample.py` `54fc73693b0f…`;
`_eda_common.py` `82f02ceb1975…`; spec `c85340ef08af…`.
