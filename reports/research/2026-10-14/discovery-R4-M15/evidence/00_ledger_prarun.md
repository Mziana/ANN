# Ledger Pra-Run - Discovery R4-M15-native

Tanggal: 2026-10-14
Bed: **2024** (khusus). 2023/2025/2026 TERKUNCI, tidak dibuka.
Spesifikasi beku: `reports/governance/2026-10-14/arsitek/spesifikasi-discovery-R4-M15.md` (status PRA-REGISTRASI, disetujui user "oke eksekusi").

Pernyataan ini ditulis **sebelum** eksekusi run final.

## 1. Ringkasan spec yang dijalankan

**Basis.** M15 adalah basis tunggal. `data/processed/M1/usdjpy_m1_2024.parquet` dibaca HANYA sebagai sumber bar untuk resample ke M15 (whitelist; guard `pd.read_parquet` menolak path lain). Resample bucket `floor("15min")` UTC; hanya bucket `n == 15` dipakai. Kolom turunan: `o=open first`, `h=max`, `l=min`, `c=close last`, `spread=max(spread_pips)` (konservatif), `raw0=broker_time_raw first`.

**Sesi.** Diimpor dari `notebooks/scalping/_eda_common.py`; assert `session_fingerprint() == EXPECTED_FINGERPRINT` sebelum dipakai.

**ATR.** `tr[i]=max(h[i]-l[i],|h[i]-c[i-1]|,|l[i]-c[i-1]|)`; `atr[i]=ewm(tr, alpha=1/14, adjust=False).mean()`. Kausal, definisi tunggal untuk trigger maupun barrier.

**Grid 8 sel (beku).**
- E1 (6 sel): N in {3,4,6} x k in {1.0,1.5}; run N candle searah pada `t0-N..t0-1`; displacement `|c[t0]-o[t0-N]| >= k*atr[t0]`; t0 berlawanan dengan run dan `|body| >= 0.5*range`; `side` = arah candle t0.
- E2 (2 sel): W=12, k in {1.5,2.5}; `disp[e]=c[e]-c[e-12]`; `e=i-length`, `length in 1..5`, `e>=W`; t0 searah push; `adv <= 0.40*(hiW[e]-loW[e])`; satu event per t0 (pecah pada pencocokan pertama); `side` = arah push.
- E3 (1 sel): W=16; kompresi `rng[i-1] <= 0.5*med[i-1]`, `med[i]=median(rng[i-16j], j=1..20)`; breakout `c[i] >= hi16[i-1]+0.5*atr[i]` (side +1) atau `c[i] <= lo16[i-1]-0.5*atr[i]` (side -1); bar breakout dikecualikan dari jendela kompresi; `i >= 336`.

**Barrier/race.** `SL=1.5*atr[t0]`, `TP=3.0*atr[t0]` (RR 1:2). Entry = OPEN bar `t0+1`. Race `j = t0+1 .. t0+10` (bar entry termasuk). Bar-kembar TP+SL pada bar yang sama = `AMBIGUOUS` (buang + hitung eksplisit). `TIME` exit = close bar ke-10 sisi keluar (BUY bid close, SELL ask close). Sisi keluar: BUY TP=h/SL=l, SELL TP=ask_low/SL=ask_high. `gross = side_sign*(exit-entry)/PIP`; `net = gross - cost`.

**Biaya 3 lapis (tabel beku, per sesi t0).** `obs = COST_OBS[sesi]+0.3`; `cons = obs+0.2`; `stress = COST_P95[sesi]+0.6`. `COST_OBS = {London .61, NewYork .69, Tokyo .62, Sydney .80, default .65}`; `COST_P95 = {London .8, NewYork 1.2, Tokyo .9, Sydney 1.5, default 1.0}`.

**Cancel (urutan tetap).** (1) `GAP` - jendela `[t0+1,t0+10]` melewati batas bar atau memuat bar tidak kontigu (`diff(raw0) != 900`); (2) `ATR_NA` - `atr[t0]` bukan finite; (3) `OFF_SESSION` - `session_label[t0] == "Off"`.

**Shadow (kaki B cermin).** Entry, waktu, barrier, dan biaya IDENTIK dengan kaki A. Keluaran wajib per sel: matriks joint A x B (TP/SL/TIME/AMBIGUOUS), distribusi selisih berpasangan `netA-netB` (median + share>0), dan ekskursi tanpa barrier dari OPEN entry termasuk bar entry (MFE_A/B, MAE_A/B dalam pip; MFE dalam R dibagi TP). Shadow tidak mengubah vonis sel.

**Gate & vonis.** `n_eval < 30` = TAK-TERUJI. Jika `n_eval >= 30`: (i) `median(net_obs_A) > 0`; (ii) CI 95% bootstrap cluster-per-hari, 10.000 resample, seed 1337, batas bawah > 0; (iii) tanda sama di paruh-1 vs paruh-2 2024; (iv) failure map lengkap (semua sesi hadir, tanpa gap tak terjelas). KANDIDAT bila (i)-(iv) benar; TOLAK bila (i)/(ii)/(iii) gagal; BELUM JELAS hanya bila (iv) gagal sementara (i)-(iii) benar.

**Anti-drift.** Whitelist path dijalankan (guard + log nama file); QC di-`qc.json`: bar M1 sumber, bucket penuh/parsial, bar M15, % kontiguitas, statistik spread, % ketersediaan ATR, event per sel, cancel per sel. Regresi determinisme: 50 event pertama kaki-A dicek vektor-vs-skalar, toleransi < 1e-9, gagal = AssertionError.

**Eksekusi.** Timeout 7.200.000 ms; stdout+stderr di-redirect ke `run_stdout.log`. Output ASCII, line ending LF. Tanpa operasi git.

## 2. Keputusan bindingsian yang diambil sebelum run

1. **Label sesi t0** diambil dari waktu awal bucket M15 (`bucket`, UTC). Dicatat di `qc.json`.
2. **`tr[0] = h[0] - l[0]`** (Wilder standar; `c[-1]` tidak ada). Dicatat di `qc.json` sebagai `atr_note` / `atr_first_valid_index`.
3. **E2 `hiW/loW`** = rolling 12 pada indeks `e` (yaitu `[e-11, e]`), sesuai `rolling(W)`.
4. **E3 `med`** dihitung pada jendela `[i-320, i]` dengan mengambil kolom `i-16, i-32, ..., i-320` (20 blok 16-bar non-overlap).
5. **`n_eval`** = event yang lolos cancel dan kaki A-nya determinate (bukan AMBIGUOUS). Kaki B AMBIGUOUS tetap direkam di matriks joint dan dihitung eksplisit, tetapi tidak masuk denominator utama.
6. **Pasangan netA-netB** dihitung hanya atas event dengan kedua kaki determinate.
7. **`PIP = 0.01`** (satuan pip USDJPY), dipakai hanya untuk konversi satuan harga ke pip. Semua ambang jarak tetap bersatuan ATR.

## 3. Disclosure revisi kode sebelum run final

Beberapa revisi kode terjadi **sebelum run final**, ketika belum ada hasil yang dihasilkan. Tidak ada satu pun revisi yang mengubah parameter, grid, ambang, barrier, biaya, atau aturan vonis. Rincian:

1. **API pandas 2.2** (`grp["size"]` tidak valid, panjang vektor groupby) - perbaikan mekanis, definisi tidak berubah.
2. **Bug indeks pada scan E2** - penugasan event t0 memakai indeks salah; diperbaiki ke `t0[i[take]] = i[take]`. Logika syarat E2 tidak berubah.
3. **Bug kolom `cancel_reason`** - event yang lolos cancel tidak diberi label `"NONE"` sehingga `evald` kosong dan semua sel salah menjadi `n_eval=0`. Diperbaiki ke label eksplisit `"NONE"`.
4. **Satuan pip (koreksi kesatuan satuan, bukan parameter)** - `PIP` awalnya 0.0001 (konvensi pair non-JPY). Diverifikasi terhadap data sumber: median range bar M1 = 0.021 satuan harga dan median `spread_pips` = 0.6; kombinasi itu hanya konsisten bila **1 pip USDJPY = 0.01 satuan harga** (rasio range/spread = 3.5). Dengan 0.0001, nilai gross tergambar 100 kali dan spread ditambahkan dalam satuan pip, bukan satuan harga. Diperbaiki ke `PIP = 0.01` plus konversi `spread_price = spread_pips * PIP` pada seluruh aritmetika harga sisi ask (`ask_low`, `ask_high`, ask close). Dicatat di `qc.json.pip_definition`.
5. **Bug bootstrap cluster-per-hari** - cluster yang terambil lebih banyak kali daripada jumlah eventnya menghilangkan event (baris terisi NaN), menggeser median bootstrap. Diperbaiki ke pengulangan siklis `occ % counts[hari]` sehingga setiap resample berisi tepat D cluster-event. Ditambah assertion `mx == D` dan assertion tiap cluster punya >= 1 event.

Setelah revisi di atas, run final dieksekusi penuh, exit code 0, tanpa perubahan parameter.

## 4. Urutan

kode (`r4_m15.py`) -> manifest (`00_manifest.json`, SHA-256 + bytes input dan kode) -> run final.
