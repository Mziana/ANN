# Spesifikasi Discovery-R6-conditioning (satu variabel baru)

Tanggal: 2026-10-14. Status: **DRAF ARSITEK, menunggu audit spec sebelum eksekusi**.
Bed: **2024** (sudah terbakar = bed search, sah dipakai ulang). 2025/2026 TERKUNCI.

## 0. Alasan ronde ini ada (bukan "coba lagi")

R1-R4 menguji **pola mana** pada barrier tetap. R6 menguji **satu hal lain**:
apakah kondisi pasar saat sinyal bisa mengangkat kualitas arah (Edge) melewati
titik impas setelah biaya.

Dasar kuantitatif (dari `addendum-R4-M15.md` dan dekomposisi event R4):

- Pada TP:SL = 2:1, random walk tanpa drift memiliki `P(+2R sebelum -1R) = 1/3`.
  Artinya **sinal tanpa edge arah TEPAT imas sebelum biaya**.
- Biaya ~1 pip menaikkan ambang ke `WR > (SL + c) / (TP + SL) = 35,2%`
  dengan SL 17,6 pip.
- R4 mengukur `WR_decisive` 13,7-26,8%, median **23,9%**. Edge 0,372-0,503.
- Dekomposisi P&L kaki A seluruh sel: TP +56.654, SL -102.038, TIME +28.107
  pip. **Exit TIME justru profit; yang membunuh adalah bucket SL (45% event).**

Maka: hipotesis R6 bukan "perbaiki barrier" (sudah diuji, RR turun hanya
memperburuk) dan bukan "perpanjang horizon" (TIME sudah profit). Hipotesisnya
**kondisional**.

## 1. Prinsip mengikat

- **Satu variabel baru saja**: conditioning. Pola, barrier, entry, exit, biaya,
  cancel, gate TIDAK berubah dari R4.
- Tidak ada konstanta/ambang/grid/hasil R1-R2-R3-P2-R4 yang boleh dipakai
  untuk membentuk definisi sel. Vonis berdiri sendiri.
- Semua ambang jarak bersatuan ATR.
- R6 ini **ronde terakhir untuk kelas hipotesis E1/E2/E3 fixed-barrier**.

## 2. Yang diwarisi VERBATIM dari spec R4-M15 (tidak boleh diubah)

- §2 konstruksi M15 (bucket UTC 15min, hanya bucket penuh 15/15).
- §3 ATR(14) Wilder `ewm(alpha=1/14, adjust=False)`.
- §4 definisi E1 (6 sel), E2 (2 sel), E3 (1 sel) - grid 9 sel beku.
- §5 barrier: `SL = 1.5*atr[t0]`, `TP = 3.0*atr[t0]` (RR 1:2), race 10 bar,
  entry = OPEN bar `t0+1`, `mid` dilarang, bar-kembar = `AMBIGUOUS`.
- §6 tabel biaya 3 lapis (obs/cons/stress) per sesi t0.
- §7 aturan cancel (GAP, ATR_NA, OFF_SESSION) dan urutannya.
- §8 shadow pair kaki B = cermin.
- §9 gate (i)-(iv).
- §10 anti-drift whitelist path (hanya `usdjpy_m1_2024.parquet`).
- §11 ledger pra-run + manifest SHA-256 sebelum run, timeout 120 menit.

## 3. Variabel conditioning (BARU, pra-registrasi, 4 buah)

Semua dihitung **kausal** dari bar `<= t0`. Semua wajib finite pada `t0`;
kalau tidak -> cancel `COND_NA`.

### V1 `EXT` - ekstensi harga dari mean

```
sma20[i] = mean(c[i-19 .. i])
EXT[t0]  = (c[t0] - sma20[t0]) / atr[t0]
```

Rasio: E1 adalah pola exhaustion. Hipotesis: sinyal hanya berguna saat harga
belum terlalu jauh menyimpang dari mean.

### V2 `VOLR` - regime volatilitas

```
tr[i]  = max(h[i]-l[i], |h[i]-c[i-1]|, |l[i]-c[i-1]|)
af[i]  = ewm(tr, alpha=1/5,  adjust=False).mean()
as[i]  = ewm(tr, alpha=1/20, adjust=False).mean()
VOLR[t0] = af[t0] / as[t0]
```

Rasio: perilaku sinyal saat vol ekspansif berbeda dari kontraktif.

### V3 `PREMOVE` - besar impuls bar tepat sebelum t0

```
PREMOVE[t0] = |c[t0] - c[t0-1]| / atr[t0]
```

Rasio: E1 mensyaratkan displacement sebelumnya; **besarnya** mungkin menentukan
seberapa habis pasar setelah impuls itu.

### V4 `SESS` - sesi

Label sesi `t0` (sudah ada di R4). London / NewYork / Tokyo / Sydney.
`Off` sudah tercancel di §7.

## 4. Binning (PRA-REGISTRASI, boleh diedit SEBELUM melihat output)

- V1, V2, V3: **tercil atas seluruh event valid yang lolos cancel**, 3 bin.
  Ambang bin dicatat di `qc.json`.
- V4: 4 level natural.

Total **13 bin** per keluarga. Dihitung **terpisah per keluarga** (E1, E2, E3)
DAN **dipool seluruh 9 sel** (pool = "Efek regime", bukan "Efek sel").

## 5. Metrik per bin (WAJIB, semua wajib dihitung)

Untuk setiap bin (13 x 3 keluarga + 13 pooled = 52 bin):

- `n_raw`, `n_cancel`, `n_eval`, rincian cancel.
- `median(net_obs_A)`, `median(net_cons_A)`, `median(net_stress_A)`.
- CI 95% bootstrap **cluster-per-hari**, 10.000 resample, seed 1337.
- **Edge** = `median(mfeA_pips) / (median(mfeA_pips) + median(maeA_pips))`.
- **Baseline acak searah** = median MFE entry acak horizon 10 bar, sisi BUY dan
  SELL, dihitung DALAM run yang sama (kontrol anti-drift). R4 acak BUY 13,50 pip.
- **WR benar (koreksi R4-addendum)**:
  `P_profit = P(gross>0)`, `P_loss = P(gross<0)`, `P_time = P(outA=="TIME")`,
  `TIME%`, `P_flat`. WAJIB alongside `winrate_decisive`, tidak menggantikannya.
- Tanda sama paruh-1 vs paruh-2 2024.

## 6. Gate R6 (angka beku)

**Gerbang utama per bin** - keempat syarat HARUS benar:

- (G1) `n_eval >= 500`;
- (G2) `Edge >= 0.56`;
- (G3) `median(net_obs_A) > 0`;
- (G4) CI 95% cluster-per-hari batas bawah `> 0`.

**Gerbang konsistensi** - untuk setiap bin yang lolos G1-G4:

- (G5) bin yang sama menunjukkan `Edge >= 0.53` di **minimal 3 dari 9 sel**,
  atau terkonsentrasi di 1 keluarga dengan **minimal 3 sel** di keluarga itu
  yang semua `Edge >= 0.53`.

**Gerbang anti-overfit (WAJIB, ini yang membedakan R6 dari R1-R4)**:

- (G6) jumlah bin yang lolos G1-G5 **harus <= 3**.
- Bila > 3 bin lolos -> vonis `INKONSISTEN` (kemungkinan besar noise).

## 7. Vonis (satu dari tiga, BERAKHIR, tanpa usulan ronde berikutnya)

| Vonis | Kondisi | Arti |
|---|---|---|
| `KANDIDAT_VALIDASI` | 1-3 bin lolos G1-G5, G6 terpenuhi | Ada subset layak; langkah berikutnya validasi 2025 (butuh persetujuan user terpisah) |
| `MATI-KELAS` | 0 bin lolos G1-G5 | Kelas hipotesis E1/E2/E3 fixed-barrier **selesai permanen** |
| `INKONSISTEN` | >3 bin lolos G1-G5 | Terlalu banyak yang "lolos" = noise; kelas hipotesis selesai permanen |

`BELUM JELAS` **TIDAK ADA** di R6. R6 tidak boleh berakhir terbuka.

## 8. Stop rule mengikat (§8A AGENTS.md)

- R6 adalah **ronde terakhir kelas hipotesis ini**.
- `MATI-KELAS` atau `INKONSISTEN` -> **tidak ada R7 tanpa persetujuan user baru**,
  dan bukan hanya dengan persetujuan itu: perlu hipotesis baru yang berbeda
  strukturnya, bukan ulang E1/E2/E3 dengan filter lain.
- `KANDIDAT_VALIDASI` -> **bukan** izin langsung memakai 2025. Butuh persetujuan
  eksplisit user membuka 2025 sebagai bed validasi.

## 9. Anti-drift (diwarisi + tambahan R6)

- Whitelist path: hanya `usdjpy_m1_2024.parquet`. Assert 2023/2025/2026 tidak
  diakses. Log nama file yang benar-benar dibaca.
- QC tambahan: distribusi 13 bin (jumlah event + ambang tercile), jumlah event
  per sel, baseline acak yang dihitung in-run.
- Regresi determinisme: 50 event pertama kaki-A dicek vektor-vs-skalar.
- **Tidak boleh** menambahkan variabel conditioning kelima. Empat saja.

## 10. Eksekusi dan artefak

- Ledger pra-run + manifest SHA-256 (input + kode) **sebelum** run.
- Timeout 120 menit. stdout ke `run_stdout.log`. Run terpotong = TIDAK SAH.
- Output ASCII, LF. Tanpa operasi git.
- Artefak: `00_ledger_prarun.md`, `00_manifest.json`, `r6_condition.py`,
  `run_stdout.log`, `qc.json`, `events.parquet`, `summary.json`, dan
  `tabel_gate.csv` (52 bar, satu per bin, untuk audit cepat).
- Auditor terpisah sebelum vonis. Auditor WAJIB skeptis atas (G6).
