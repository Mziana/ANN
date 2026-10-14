# Spesifikasi Discovery-R4-M15-native (M15 sebagai basis)

Tanggal: 2026-10-14. Status: **PRA-REGISTRASI, disetujui user ("oke eksekusi")**.
Bed: **2024**. 2025/2026 TERKUNCI (dilarang dibuka).

Menggantikan draf `spesifikasi-discovery-R4-M15.md` versi pip-based yang
TIDAK SAH (lihat `../../research/2026-10-14/discovery-R4-M15/evidence_TERCEMAR_tidak-sah/`).

## 1. Prinsip mengikat

**M15 adalah basis. M1 tidak boleh masuk sebagai sumber definisi.**

- M1 2024 HANYA boleh dibaca sebagai sumber bar untuk resample ke M15.
- Tidak ada konstanta, ambang, grid, atau hasil R1/R2/R3/P2 yang boleh
  dipakai di ronde ini. Vonis berdiri sendiri.
- **Semua ambang jarak bersatuan ATR, bukan PIP.** PIP hanya dipakai untuk
  konversi satuan harga ke pip pada perhitungan gross.

## 2. constructions M15 (frozen)

Sumber: `data/processed/M1/usdjpy_m1_2024.parquet`.
Resample bucket UTC 15min; **hanya bucket penuh 15/15 bar** (parsial
dianggap gap). Kolom: o=open pertama, h=max, l=min, c=close terakhir,
spread=`max(spread_pips)` per bucket (konservatif, wajib dicatat di QC).
Label sesi dari `notebooks/scalping/_eda_common.py` (`add_labels`), dengan
**assert `session_fingerprint() == EXPECTED_FINGERPRINT`**.

## 3. ATR(14) M15 - satu definisi untuk trigger DAN barrier

```
tr[i]  = max(h[i]-l[i], |h[i]-c[i-1]|, |l[i]-c[i-1]|)
atr[i] = ewm(tr, alpha=1/14, adjust=False).mean()
```

Kausal: `atr[i]` hanya memakai bar <= i, tersedia saat bar i TUTUP.
Tidak ada merge lintas-timeframe, tidak ada toleransi asof, tidak ada
ATR kedua. NaN sebelum tersedia -> cancel `ATR_NA`.

## 4. Delapan sel (grid beku, TIDAK boleh diubah setelah melihat output)

### E1 - exhaustion lalu berbalik (6 sel = N x k)

- Run: N candle M15 searah, `N in {3, 4, 6}` (45/60/90 menit).
- Displacement run: `|c[t0] - o[t0-N]| >= k * atr[t0]`, `k in {1.0, 1.5}`.
- t0: candle berlawanan dengan `|body| >= 0.5 * range`.
- `side` = arah candle t0.
- Window run = bar `t0-N .. t0-1` (N bar, t0 tidak termasuk).

### E2 - expansion, pullback dangkal, continuation (2 sel = k)

- Window ekspansi `W = 12` bar (3 jam). `disp[i] = c[i] - c[i-W]`.
- Ambang: `|disp[e]| >= k * atr[e]`, `k in {1.5, 2.5}`.
- `push_up = disp > 0`. Pencarian t0: `e = i - length`, `length in 1..5`,
  `e >= W`.
- t0 harus searah push (`c[i]>o[i]` bila push_up, `c[i]<o[i]` bila turun).
- Retrace: `hiW[e]`, `loW[e]` = rolling W max/min.
  `adv = hiW[e] - min(l[e+1..i])` (push up) atau
  `max(h[e+1..i]) - loW[e]` (push turun);
  syarat `adv <= 0.40 * (hiW[e] - loW[e])`.
- **Satu event per t0** (break pada pencocokan pertama).
- `side = +1` bila push_up, `-1` bila turun.

### E3 - kompresi lalu breakout (1 sel)

- Window kompresi `W = 16` bar (4 jam). `rng[i] = hi16[i] - lo16[i]`.
- Kompresi: `rng[i-1] <= 0.5 * med[i-1]`, dengan
  `med[i] = median(rng[i-16j], j=1..20)` (20 blok 16-bar, tidak overlap).
- Breakout: `c[i] >= hi16[i-1] + 0.5*atr[i]` -> side +1, atau
  `c[i] <= lo16[i-1] - 0.5*atr[i]` -> side -1.
- **Bar breakout dikecualikan dari jendela kompresi** (uji di i-1).
- Index awal: `i >= 16*20 + 16 = 336`.

## 5. Barrier, entry, exit (dimensionless - satu paket, tanpa ladder)

- `SL = 1.5 * atr[t0]`, `TP = 3.0 * atr[t0]` (RR 1:2). ATR = M15, definisi tunggal.
- Entry = OPEN bar `t0+1` (BUY: ask open, SELL: bid open). `mid` dilarang.
- Race 10 bar M15 (2,5 jam) = `j = t0+1 .. t0+10`, **BAR ENTRY IKUT DIUKUR**.
- Bar-kembar TP+SL pada bar sama = `AMBIGUOUS` (buang + hitung eksplisit).
- Sisi keluar: BUYTp=high, BUY SL=low, SELL TP=ask_low, SELL SL=ask_high.
- `TIME` exit = close bar ke-10 sisi keluar (BUY bid close, SELL ask close).
- `gross = side_sign * (exit - entry) / PIP`; `net = gross - cost`.

## 6. Biaya 3 lapis (tabel beku, per sesi t0)

```
obs    = COST_OBS[sesi] + 0.3
cons   = obs + 0.2
stress = COST_P95[sesi] + 0.3 + 0.3
COST_OBS = {London .61, NewYork .69, Tokyo .62, Sydney .80, default .65}
COST_P95 = {London .8, NewYork 1.2, Tokyo .9, Sydney 1.5, default 1.0}
```

## 7. Cancel (beralasan, urutan tetap)

1. `GAP` - jendela `[t0+1, t0+10]` melewati batas bar ATAU memuat bar
   tidak kontigu (`diff(raw0) != 900`).
2. `ATR_NA` - `atr[t0]` bukan finite.
3. `OFF_SESSION` - label sesi t0 == `"Off"`.

## 8. Shadow pair (kaki B = cermin, per event)

Kaki A (sisi sinyal) dan kaki B (sisi lawan) memakai entry, waktu, barrier,
dan biaya IDENTIK. Keluaran wajib per sel:
- Matriks joint 2x2: (A-TP,B-TP), (A-TP,B-SL), (A-SL,B-TP), (A-SL,B-SL),
  plus pasangan TIME dan AMBIGUOUS.
- Distribusi selisih berpasangan `netA - netB`: median, share > 0.
- Ekskursi berpasangan TANPA barrier dari OPEN entry (bar entry termasuk):
  MFE_A vs MFE_B, MAE_A vs MAE_B (pip), dan MFE dalam satuan R (dibagi TP).
- Shadow **tidak mengubah vonis sel**; ia menjelaskan vonis
  (arah-buta vs pagar-salah vs biaya).

## 9. Gate & vonis

- `n_eval < 30` per sel = **TAK-TERUJI** (bukan gagal, bukan lolos).
- `n_eval >= 30`, lalu 4-syarat (angka beku, diwarisi R2 D2-6):
  - (i) `median(net_obs_A) > 0`;
  - (ii) CI 95% bootstrap **cluster-per-hari**, 10.000 resample,
    seed 1337, batas bawah > 0;
  - (iii) tanda sama di paruh-1 vs paruh-2 2024;
  - (iv) failure map lengkap (semua sesi hadir, tanpa gap tak terjelas).
- `KANDIDAT` bila (i)-(iv) semua benar; `TOLAK` bila (i)/(ii)/(iii) gagal;
  `BELUM JELAS` hanya bila (iv) gagal sementara (i)-(iii) benar.

## 10. Anti-drift (wajib dijalankan, logged ke `qc.json`)

- **Whitelist path**: hanya `usdjpy_m1_2024.parquet` boleh dibuka.
  Assert bahwa 2023/2025/2026 tidak diakses (cek `os.path` / log nama file).
- QC logged: jumlah bar M1 sumber, jumlah bucket penuh/parsial, jumlah bar
  M15, % kontiguitas, statistik spread, % ketersediaan ATR, jumlah event
  per sel, rincian cancel per sel.
- Regresi determinisme: 50 event pertama kaki-A dicek vektor-vs-skalar.

## 11. Eksekusi

- Ledger pra-run + manifest SHA-256 (input + kode) **sebelum** run.
- Timeout perintah run: **7.200.000 ms (120 menit)**; stdout di-redirect
  ke `run_stdout.log`. Run yang terpotong = **TIDAK SAH**, jalankan ulang penuh.
- Output ASCII, line ending LF.
- Tanpa operasi git (commit/push dikerjakan Command).

## 12. Artefak

Spec ini + `../evidence/`: `00_ledger_prarun.md`, `00_manifest.json`,
`r4_m15.py` (kode), `run_stdout.log`, `qc.json`, `events.parquet`,
`summary.json`. Auditor terpisah sebelum vonis.
