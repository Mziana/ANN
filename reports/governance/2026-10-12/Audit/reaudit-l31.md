# Re-audit L3-1 — Baseline vs Null 103 Pasangan (Auditor Independen)

Peran: **Auditor independen** (bukan coder L3-1). Mode: read-only.
Tanggal: 2026-10-13. Mandat: `2026-10-12_reaudit-l31-auditor.md`.
Ruang lingkup: `scripts/_build_eda07_l31.py`,
`notebooks/scalping/eda_07_l31_baseline.ipynb`, `T-L3-1_baseline.csv`,
`FIG-18_baseline.png`, `_l31_manifest.csv`, `run_l31.log`.

> **Batas yang dihormati.** Tidak ada builder/notebook beku yang dieksekusi. Tidak ada file di
> `D:\ANN` yang ditulis selain laporan ini. Seluruh harness auditor berada di
> `C:\Users\Fajar\AppData\Local\Temp\opencode\audit-l31\`
> (`v1_s0.py`, `v2_abc.py`, `v3_def.py`, `v4_gh.py`, `v5_verbatim.py`, `v6_ijk.py`,
> `v7_k24.py`, `v9_k24ast2.py`, `v10_k24full.py`).
> Laporan ini **tidak memuat vonis edge, model, kelayakan-trade, atau profitabilitas** — dan
> tidak boleh dibaca demikian. L3-1 adalah tabel baseline-vs-null; vonis dagang adalah
> wewenang arsitek + user pasca-audit (B-4, S8A).

Kontrak yang dipakai: `AGENTS.md` (S18, S20), `spesifikasi-lapisan3.md` (S3-0..S3-5),
`putusan-l30-audit.md` (B-1..B-4), `amandemen-l31-metrik.md` (C-1..C-4), laporan coder
`laporan-coder-eda07-l31.md`, dan gerbang asisten
`2026-10-13_gerbang-hasil-l31.md` (dipakai sebagai pembanding, bukan sumber angka — seluruh
angka di bawah dihitung ulang oleh harness auditor).

> **Catatan metode.** Draf audit versi sebelumnya sudah ada di jalur ini. Auditor **tidak
> mempercayakannya**: setiap angka, tabel, dan klaim di bawah dihitung ulang dari nol.
> Empat koreksi material terhadap draf lama dan tiga upgrade kekuatan bukti ada di §5.

---

## 1. Vonis

# LOLOS PROSEDURAL

Kesebelas mandat **(a)–(k) lolos tanpa satu pun selisih angka**. Rekonstruksi aturan M3
mandiri menghasilkan **LOLOS 68 / GUGUR 35** dengan baris-per-baris **identik** dengan
`T-L3-1_baseline.csv`. Tidak ada temuan TINGGI. Tidak ada temuan MENENGAH.

| Peringkat | Jumlah | Sifat |
|---|---|---|
| TINGGI | 0 | — |
| MENENGAH | 0 | — |
| RENDAH | 4 | Format/ketertelusuran; **nol dampak ke angka mana pun** |
| INFORMATIF | 4 | Penjaga untuk putusan B-4 |

Rekomendasi: **hasil M3 L3-1 sah dipakai arsitek untuk vonis biner B-4** — tetapkan 4 butir
RENDAH sebagai aplikasi ronde berikutnya dan 4 INFORMATIF sebagai catatan putusan.
Daftar LOLOS-per-jenis (angka, bukan vonis dagang) ada di §7.

### Pemetaan §18 AGENTS.md (semua section wajib)

§18 meminta section A–H dengan metrik performa dagang (Sharpe, DD, WR, PF, Expectancy).
Untuk ronde baseline-vs-null tanpa P&L, section itu **tidak berlaku dan tidak mungkin
dihitung** — mengisi-nya justru akan melanggar S3-3 (larangan P&L/backtest/edge).
Pemetaan jujur (preseden sama seperti `reaudit-l30.md`):

| §18 | Isi | Status L3-1 |
|---|---|---|
| A | Performa Dasar (Sharpe/DD/WR/PF/Expectancy) | **N/A by design** — S3-3 melarang P&L; tidak ada trade/equity curve |
| B | Analisis Trade | **N/A by design** — nol transaksi; artefak skor per pasangan, bukan trade |
| C | Analisis Regime (sesi/hari/bulan) | **TERPENUHI sebagian** — M3(b) menang per-semester 2025H1&H2 per pasangan; bukan analisis regime umum |
| D | Robustness (sensitivity/walk-forward/MC) | **N/A by design** — tanpa bootstrap/CI (SEEDL31 tak dipakai, diizinkan B-3); stabilitas diwakili konjungsi (b) |
| E | Bias (look-ahead/survivorship/leakage/overfit) | **TERPENUHI** — §3 (g)(h) + K24 24/24 vs source run 9 |
| F | Biaya (spread/slippage/komisi/bid-ask) | **N/A by design** — tanpa P&L; delta_normal dibawa sebagai metadata `irisan`, tidak dihitung ulang |
| G | Kegagalan | **TERPENUHI** — §5 Temuan |
| H | Kesimpulan | **TERPENUHI** — §7 + §1 vonis |

---

## 2. S-0 — Gerbang masuk

| Pemeriksaan | Hasil | Status |
|---|---|---|
| HEAD | `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` | TERVERIFIKASI |
| Branch | `main` | TERVERIFIKASI |
| Staged (`git diff --cached --name-only`) | **0** | TERVERIFIKASI |
| SHA256 6 file L3-1 vs klaim coder | **6/6 COCOK** (prefix 12 hex + ukuran byte) | TERVERIFIKASI |
| Builder/CSV/manifest ASCII+LF+tail-LF | `nonASCII=0, CR=0, tailLF=True` | TERVERIFIKASI |
| FIG-18 PNG | magic `89504e470d0a1a0a`, 77.791 B | **N/A** — PNG biner; byte non-ASCII adalah isi gambar |
| `run_l31.log` | UTF-16LE BOM + 21 CR, `tailLF=False` | **TEMUAN R1** (format; isi utuh, §5) |

Rincian hash (`sha256` + `len` per file, harness `v1_s0.py`):

```
COCOK  BD5B12415937    58262  scripts/_build_eda07_l31.py
COCOK  67F5FE628712    79165  notebooks/scalping/eda_07_l31_baseline.ipynb
COCOK  45D034823AFC    35811  reports/eda/2026-10-12/T-L3-1_baseline.csv
COCOK  50DAA2612C06    77791  reports/eda/2026-10-12/FIG-18_baseline.png
COCOK  599C7FFDFC8B     1333  reports/eda/2026-10-12/_l31_manifest.csv
COCOK  0A4E5D4FBDDF     2642  reports/eda/2026-10-12/run_l31.log
--> cocok 6/6, tidak cocok 0/6
```

Notebook (parse `nbformat` independen, bukan klaim coder): **8 sel** (1 markdown + 7 kode),
`execution_count` 1–7 berurutan, **0 output error**, `KESIMPULAN_L31` hadir,
`ASSERT_LOG total: 1268` terbaca, serta `PASS: jangkar`, `PASS: C-3 konsistensi`,
`PASS: register 103`, `PASS: unit C-3`, `TAL intermediate`, dan `transcription-guard` —
semuanya hadir di output. Total output 11.050 karakter.

---

## 3. Hitung ulang independen (a)–(k)

Setiap tabel di bawah adalah hasil hitung ulang auditor **dari CSV beku + source**, bukan
dibaca dari output notebook. Output notebook hanya dipakai sebagai pembanding.

### (a) 103 = 98 peta98 + 5 Tokyo; 67 diskret + 36 kontinu

| Pemeriksaan | Hasil | Klaim | Status |
|---|---|---|---|
| Baris `T-L3-1_baseline.csv` | **103** | 103 | COCOK |
| `metrik_jenis` brier / mse | **67 / 36** | 67/36 | COCOK |
| Kind untuk `brier` | `{LB_bin 25, LC1 9, LC2 19, LD 14}` | — | COCOK (tanpa LB_rng) |
| Kind untuk `mse` | `{LB_rng}` saja | — | COCOK (tanpa diskret) |
| Baris 0–97 vs `T-L3-0_peta98.csv` | **mismatch 0/98**, urutan sama | 98 native | COCOK |
| Baris 98–102 vs 5 kandidat `round_d` Tokyo di `T-L3-0_arah.csv` | **himpunan sama 5/5** | 5 Tokyo | COCOK |
| Arah 5 Tokyo | `neg` 5/5 (cocok `tanda=neg` di arah.csv) | neg | COCOK |
| Lift `round_d` 5 Tokyo | `-0,0473 / -0,0549 / -0,7446 / -0,0279 / -1,5868` | identik L3-0 | COCOK |
| Kolom `M1` | **True 103/103** | 103/103 | COCOK |
| Nilai unik `vonis` | `{GUGUR, LOLOS}` | tunggal-makna | COCOK |

### (b) Aturan M3 → vonis 103/103 nol selisih

Rekonstruksi auditor: `vonis = LOLOS IFF (lolos_a & menang_h1 & menang_h2 & losers_c)`.
Konjungsi ini **wajib sama untuk kedua jenis** (B-3 utuh untuk diskret, C-2 mewarisi
kaki (b) untuk kontinu); hanya isi (a)/(c) yang berbeda per-jenis, dan perbedaan itu
tersimpan di kolom terpisah — bukan di dalam konjungsi.

|  | vonis CSV GUGUR | vonis CSV LOLOS |
|---|---|---|
| rekonstruksi GUGUR | **35** | 0 |
| rekonstruksi LOLOS | 0 | **68** |

Selisih rekonstruksi vs `vonis`: **0 baris**.

### (c) Margin tak dilanggar; distribusi ada headroom

- Diskret (C-2): `lolos_a == (metrik_null_pooled − metrik_mod_pooled > 0,001)` → **COCOK 67/67**.
- Kontinu (C-2): `lolos_a == (metrik_mod_pooled < metrik_null_pooled × 0,99)` → **COCOK 36/36**;
  `metrik_null_pooled > 0` **36/36** (pembagi aman, tak ada pembagian nol).

| Kelompok | n | min | p25 | median | p75 | max | ambang | min/ambang |
|---|---|---|---|---|---|---|---|---|
| Margin Brier (LOLOS) | 56 | **0,00306** | 0,00414 | 0,00549 | 0,00885 | 0,01022 | 0,001 | **3,06×** |
| Perbaikan relatif MSE (LOLOS) | 12 | **11,24 %** | — | 18,77 % | — | 56,29 % | 1 % | **11,2×** |

**Tidak ada satu pun baris LOLOS yang menempel ambang**: 0/56 Brier berada di
(0,001 ; 0,002], dan 0/12 MSE berada di (1 % ; 2 %]. Margin bukan hasil seragam di
tepat garis 0,001 — ada headroom terukur. Konjungsi juga mengikat: **29 baris GUGUR
lolos (a) tetapi gagal di (b)/(c)**, dan 8 baris GUGUR lolos (c).

### (d) Menang 2025H1 & 2025H2

| Pemeriksaan | Hasil | Status |
|---|---|---|
| LOLOS → `menang_h1 & menang_h2` semua | **68/68** | COCOK |
| GUGUR dengan h1&h2 menang | **12/35** | konsisten (bukan anomali) |
| …dari 12 itu, `lolos_a=True` | **12** | lolos (a), gagal tepat di kaki (c) |
| …dari 12 itu, `lolos_c=True` | **0** | konjungsi mengikat di kaki (c) |
| GUGUR menang h1 saja / h2 saja | 27 / 18 | konsisten |

Batas jujur: CSV **tidak menyimpan nilai metrik per-semester**, hanya boolean
`menang_h1/menang_h2` (kolom per-semester yang ada hanya `n_test_h1`, `n_test_h2`).
Konsistensi boolean TERVERIFIKASI; rekalkulasi nilai per-semester dari eksekusi ulang =
**BELUM DIVERIFIKASI** (§6; eksekusi dilarang untuk auditor).

### (e) Twin C-3: 5/5 identik hasil-M3

| Target | n | selisih hasil-M3 | arah native/round_d | wakil native | vonis |
|---|---|---|---|---|---|
| `LB_bin Tokyo t2 N15` | 2 | **0** | neg / neg | hour_sin | LOLOS |
| `LB_bin Tokyo tALL N15` | 2 | **0** | pos / neg | atr_m5 | LOLOS |
| `LB_bin Tokyo tALL N5` | 2 | **0** | pos / neg | rv60 | LOLOS |
| `LB_rng Tokyo tALL N15` | 2 | **0** | pos / neg | rv60 | GUGUR |
| `LB_rng Tokyo tALL N5` | 2 | **0** | pos / neg | rv60 | GUGUR |

Yang dibandingkan: `metrik_mod_pooled`, `metrik_null_pooled`, `sekunder_mod`,
`sekunder_null`, `lolos_a`, `menang_h1`, `menang_h2`, `lolos_c`, `vonis`, `n_train`,
`n_test_h1`, `n_test_h2`, `baseline`, `nullmodel`, `sekunder_jenis`, plus `kind`,
`metrik_jenis`, `jenis_target`, `irisan`, `sess`, `ter`, `N` → **selisih 0 untuk kelima
kembaran**. C-3 terpenuhi.

Kolom `arah` memang berbeda pada 4 dari 5 pasang — dan itu **justru yang diminta C-3**
("satu seri label, M1 + flag berbeda"): baris native memakai arah fitur aslinya, baris
`round_d` memakai arah `neg` sebagai kandidat invers. Lihat I4.

Verifikasi posisi: pasangan indeks kembaran selalu `(native < 98, Tokyo ≥ 98)` —
`(15,98) (19,101) (21,99) (52,102) (54,100)` — jadi pemisahan native/Tokyo pada baris
register bukan asumsi indeks.

### (f) Pagar T-5 (B-2): flag `punya_round_d_invers` = 12

| Pemeriksaan | Hasil | Status |
|---|---|---|
| Kolom `punya_round_d_invers` ada | ya (bool) | COCOK |
| `sum(flag)` | **12** | COCOK |
| Target unik berflag | **7** = **5 Tokyo** (masing-masing punya kembaran `round_d`) + **2 London native** | COCOK |
| 5 baris Tokyo semuanya berflag | ya | COCOK |
| 4 Tokyo ber-`arah=pos` via `rv60`/`atr_m5` | **4** — cocok persis redaksi B-2 T-5 | COCOK |
| Vonis pasangan berflag | LOLOS 6 / GUGUR 6 | COCOK |
| Kolom bypass/pengecualian | **tidak ada** — 103 pasangan diputus M3 tanpa pengecualian | COCOK |

Angka-angka magnitudo-volatilitas T-5 **tidak dipakai sebagai tiket lolos**: pasangan
berflag `LB_rng London t3 N5` (rv15) dan `LB_rng London tALL N5` (rv60) justru **GUGUR**.

### (g) Split tanpa bocor (desain + assert, bukan re-run)

Desain di source builder, diverifikasi literal:

```
SEM_A == ["2023H2", "2024H1", "2024H2", "2025H1", "2025H2"]   # chk: SEM_A eksak 5
TRAIN_SEMS = SEM_A[:3]                 # -> 2023H2, 2024H1, 2024H2
H1S, H2S   = SEM_A[3], SEM_A[4]        # -> 2025H1, 2025H2
```

Tidak ada `shuffle` lintas batas (sapu kata: nol); test ditentukan sebagai **komplemen
terkunci**, bukan dipindai. Angka split dari output notebook, dikonversi auditor dari
ns ke detik UTC:

| | UTC awal | UTC akhir |
|---|---|---|
| train | 1688339340 (2023-07-01) | 1735673400 (**2024-12-31T19:30**) |
| test | 1735776660 (**2025-01-02T00:11**) | 1767210840 (**2025-12-31T19:54**) |

| Pemeriksaan | Hasil | Status |
|---|---|---|
| `max-train < min-test` | 1735673400 < 1735776660 → **True**, selisih 1,195 hari | COCOK |
| Batas 2026 tak tersentuh | `test max` 2025-12-31T19:54 **< 2026-01-01** | COCOK |
| Batas bawah test | `test min` 2025-01-02 ≥ 2025-01-01 | COCOK |
| Chk mesin di builder | 3 assert (SEM_A eksak, train/test tak-kosong, max-train<min-test) | LOLOS saat run |

**Bukti kejadian chk ini bukan baris PASS yang tercetak** — `chk(cond, msg, loud=False)`
(builder baris 148) hanya mencetak bila `loud=True`, sedangkan ketiga assert S6 disebut
tanpa `loud`. Bukti bahwa semuanya LOLOS bersifat **inferensial tapi sah**: `chk`
memanggil `assert` tanpa syarat, jadi kegagalan akan menghentikan sel dan menghasilkan
`output_type: error`; output notebook menunjukkan **0 error** dan `execution_count` 1–7
berurutan. Dinyatakan jujur sebagai inferensi, bukan pembacaan baris log.

Bukti data-level (re-proof dari parquet) = **BELUM DIVERIFIKASI** (§6; butuh eksekusi).

### (h) Label verbatim run 9 (banding byte-per-byte, bukan spot-check substring)

Builder L3-1 menandai 9 blok dengan `# __VERBATIM_BEGIN selNN__`. Auditor mengekstrak
masing-masing blok dan membandingkannya **byte-per-byte** dengan sel run 9
(`eda_07_label_fitur.ipynb`):

| Blok | Isi sel run 9 | Hasil | Byte builder/run 9 |
|---|---|---|---|
| sel01 | kontrak | **IDENTIK** | 3699 / 3699 |
| sel02 | setup | 1 baris hilang | 2441 / 2503 |
| sel03 | parameter | **IDENTIK** | 2283 / 2283 |
| sel04 | load | **IDENTIK** | 2721 / 2721 |
| sel05 | scope irisan | 4 baris hilang | 1413 / 1683 |
| sel06 | ATR | **IDENTIK** | 2862 / 2862 |
| sel07 | entries | **IDENTIK** | 1080 / 1080 |
| **sel10** | **label LB/LC/LD** | **IDENTIK** | **2571 / 2571** |
| **sel11** | **fitur kausal** | **IDENTIK** | **6797 / 6797** |

Dua blok yang tidak identik **hanya kehilangan baris non-komputasi**:

- sel02: 1 baris docstring `"""Setup lingkungan dan kunci versi + helper + stream RNG."""`.
- sel05: 4 baris display — 2× `show(IR_TER[…])` / `show(IR_SES[…])` dan 2 baris
  `for combo, sess in NEED_PAIRS: print(...)`. Setelah 4 baris display itu dibuang,
  **blok sel05 identik 1413 / 1413 byte**; deklarasi `DELTA_N` dan `DELTA_S` identik.

Konstruktor label yang dipinjam L3-1 (`TLAB` 5 jenis + `YCODE`/`YPOS`) berasal dari
blok sel10/sel12; keenam fragmen `YCODE` (`LB_rng: None`, `LA`, `LB_bin`, `LC1`, `LC2`,
`LD`) **6/6 hadir identik** di kedua sisi.

**K24 — dikonfirmasi independen 24/24 vs source run 9 (redaksi wajib B-2 T-2).**
Auditor mengekstrak 24 literal dari blok `K24` di builder lewat AST, lalu mencocokkannya
dengan literal yang benar-benar tertulis di sel parameter run 9 (mencakup bentuk
multi-target `G1_BIN_LO, G1_BIN_HI = 0.10, 0.90` dan dict `SEED07` di sel02):

```
K24: 24 entri (harus 24)   -> identik 24/24, beda 0, tak ditemukan 0
selisih K24 builder L3-1 vs builder L3-0 : 0
```

Redaksi baku B-2 T-2 dengan demikian **terpenuhi persis**: "transcription-guard,
dikonfirmasi independen 24/24 vs source run 9; bukan bukti komputasi". Yang perlu
dippertahankan: konstanta ini memang tak dipakai satu pun dalam hitungan L3-1, jadi ini
pemeriksaan transkripsi, bukan bukti komputasi.

### (i) Manifest + input beku

Kolom manifest: `path, file, sha256_sebelum, sha256_aktual, cocok` — **BERKOLOM path
relatif-root** (T-1 tutup). Semua path relatif-root (tak mulai `C:/` atau `..`) dan path
memang memuat direktori, bukan basename saja. Rekomputasi auditor `sha256` aktual:

| Baris manifest | Klaim `cocok` | Rekonsiliasi auditor |
|---|---|---|
| 5 input beku (`T-07-1`, 2× `T-06-7`, `T-L3-0_arah`, `T-L3-0_peta98`) | True | **5/5 COCOK** |
| `FIG-18_baseline.png` (output) | True | COCOK (PNG tak dinormalisasi) |
| `T-L3-1_baseline.csv` (output) | True | **BEDA** — lihat R3/R4 |

### (j) FIG-18: cakupan + keterpisahan panel

| Pemeriksaan | Hasil | Status |
|---|---|---|
| PNG valid (magic + 77.791 B) | ya | COCOK |
| Sel FIG re-read CSV **dari disk** + `chk(len == 103)` | di source builder | COCOK |
| `chk(len(D) == 67 and len(C) == 36)` | di source builder | COCOK |
| Dua panel terpisah, label satuan tak-sebanding ("TAK sebanding panel-a") | di source builder | COCOK |
| Sumbu memakai nama eksplisit `metrik_null_pooled`/`metrik_mod_pooled` (perbaikan FIG-18 coder) | di source builder | COCOK |

Cakupan data-level terverifikasi lewat `chk` yang mengunci 103/67/36 di source dan lewat
pembacaan ulang CSV oleh harness ini. Kecocokan piksel PNG = **BELUM DIVERIFIKASI** (§6).

### (k) Kepatuhan S3-3 / S8A (tanpa P&L/backtest/edge/vonis dagang)

Sapu istilah atas builder + source notebook L3-1 (`pnl` 0, `equity` 0, `sharpe` 0,
`drawdown` 0, `win rate` 0, `expectancy` 0, `profit fold` 0, `paper-trade` 0,
`profitabilitas` 0). `backtest` 4, `p&l` 4, `edge` 6 — **semuanya kalimat penolakan**:
"BUKAN strategi, BUKAN backtest, BUKAN P&L, tanpa klaim edge, tanpa vonis dagang" dan
"Tanpa vonis dagang, tanpa klaim edge, tanpa P&L/backtest; vonis dagang wewenang
arsitek+user pasca-audit L3-1". Angka ganda karena source sel muncul di builder dan di
JSON notebook. `KESIMPULAN_L31` memuat redaksi yang sama. **COCOK.**

Tanpa fitur/label/irisan baru: konstruktor label (TLAB/YCODE) verbatim run 9 (§3h), dan
`irisan` dibawa sebagai metadata (delta_normal) tanpa dihitung ulang. Tanpa threshold-scan:
ambang hanya muncul sebagai dua literal — `mod < nul * 0.99` (builder baris 827) dan
`b_mod < b_null - 0.001` (baris 879) — tanpa loop pemindaian ambang.

---

## 4. Klaim lain yang diuji ulang

| Klaim coder | Hasil auditor | Status |
|---|---|---|
| `ASSERT_LOG total: 1268` (≥100) | terbaca di output notebook; 69 call site `chk(`, sebagian beriterasi (jangkar 200, K24 24) sehingga 1268 masuk akal secara struktural tapi **tidak direproduksi** tanpa eksekusi | COCOK (terbaca); angka = S6 |
| Hash 5/5 input sama SEBELUM | §3(i) 5/5 COCOK | COCOK |
| S8B beku utuh + registry | `verify_l31` mengunci angka 260/6767/1315/1335/86 + arah 153 + peta98 98; `assert` dan `chk` di builder; output `penjaga beku/L3-0: 5 beku + arah(153) + peta98(98) tak berubah` terbaca | COCOK (level provenance; bukan re-hash file beku satu per satu) |
| 3 perbaikan builder terdokumentasi | (1) FIG kolom-nama eksplisit, (2) `)` berlebih, (3) C-3 berbasis posisi-register — ketiganya konsisten dengan source akhir dan §3(e)(j) | COCOK |
| Register 103 = 98 native + 5 Tokyo | `chk(len(REG) == 103)`; `chk(REG[98:] == REG_TOKYO)`; diverifikasi urutan oleh auditor di §3(a) | COCOK |
| `run_l31.log` berisi EXIT=0 | **Isi log TIDAK memuat `EXITCODE`/`EXIT=`**; yang ada `nbconvert exit=0`. Bukti exit proses berasal dari tool-report run, bukan dari isi log | **TEMUAN R1** |

---

## 5. Temuan

### RENDAH (nol dampak ke angka)

- **R1 — `run_l31.log` UTF-16LE + CRLF + wrapper `NativeCommandError`, tanpa token EXITCODE
  di isi.** Konfirmasi independen catatan gerbang asisten — **BANTUANNYA DITERIMA, bukan
  dibantah**: `BOM FF FE = True`, 21 `CR`, `tailLF=False`, decode `utf-16-le` menghasilkan
  1.321 karakter, `NativeCommandError: True`, `nbconvert exit=0: True`,
  `EXITCODE/EXIT= : False`, `lock dilepas: True`, `Traceback: False`. Isi lengkap dan utuh
  (lock, pra-kompilasi 7 sel OK, notebook 8 sel, registry 103, penjaga beku,
  normalisasi CRLF→LF, lock dilepas). **Dampak: keterbacaan tercemar untuk tool ASCII;
  isi dan angka utuh.** Konfirmasi bahwa perbaikan T-6 (redirect langsung) indeed
  **tidak dijalankan** di ronde ini. Aplikasi: T-6 tetap terbuka untuk ronde berikutnya.
- **R2 — Dua blok verbatim run 9 kehilangan baris non-komputasi**: sel02 (1 baris docstring)
  dan sel05 (4 baris display). Setelah baris display dibuang, blok sel05 identik
  1413/1413 byte; sel10 (label) dan sel11 (fitur) identik penuh. Dampak nol; aplikasi:
  redaksi verbatim ronde berikutnya menyebut pengecualian display secara eksplisit.
- **R3 — Hash output CSV di manifest dicatat pra-normalisasi EOL, dan sekarang
  **terbukti reproducible**. Manifest mencatat `2D46B0F97C85…` untuk
  `T-L3-1_baseline.csv`; hash on-disk `45D034823AFC…`. Auditor menghitung ulang:
  `sha256(CSV dengan LF→CRLF) = 2D46B0F97C85B01628F1828364E521A77F221F2646ECD968C09172F4ED2787A8`
  — **cocok persis**. Jadi penjelasan coder (ASUMSI TERDOKUMENTASI) naik status menjadi
  **fakta terverifikasi**, bukan asumsi. FIG tetap cocok karena PNG tak dinormalisasi.
  Dampak nol; aplikasi: catat hash ganda (pra + pasca normalisasi) di ronde berikutnya.
- **R4 — Kolom `cocok` manifest tidak reproducible untuk baris output CSV.** Manifest
  menulis `cocok=True` pada `T-L3-1_baseline.csv`, padahal re-hash aktual berbeda
  (karena R3). Manifest lain (5 input + FIG) reproducible. Dampak nol ke angka; aplikasi:
  kolom `cocok` untuk baris output sebaiknya diisi apa adanya atau diberi kolom catatan
  normalisasi, agar tidak menyesatkan saat re-audit.

### INFORMATIF (penjaga putusan B-4)

- **I1 — `SEEDL31` (31001/31002) tak dipakai**: tanpa bootstrap/CI, didokumentasikan di
  builder ("SEEDL31 tak dipakai karena CI tak dihitung"). Diizinkan B-3 ("boleh", bukan
  "wajib"). Stabilitas diwakili konjungsi M3(b). Bukan temuan.
- **I2 — sel14/sel15 run 9 (evaluator G1–G4 + skrining label waktu) sengaja tidak
  dibawa**: L3-1 by design mengonsumsi output beku run 9, bukan mengeksekusi ulang
  analisisnya. Bukan celah.
- **I3 — Konjungsi M3 mengikat di semua kaki**: 29 baris GUGUR lolos (a) tapi gagal (b)/(c);
  8 baris GUGUR lolos (c); 12 baris GUGUR menang H1&H2 tapi gagal tepat di kaki (c). Bukti
  konjungsi bekerja, bukan hiasan.
- **I4 — Kembaran C-3: hasil-M3 identik tetapi `arah` berbeda pada 4 dari 5 pasang**
  (`pos` native vs `neg` round_d). Ini persis desain C-3 dan sekaligus embody sinyal invers
  yang dijaga B-2 T-5. Catatan untuk B-4: jangan salah baca kolom `arah` yang berbeda
  sebagai ketidakkonsistenan.

### Koreksi terhadap draf audit sebelumnya

Draf versi sebelumnya di jalur ini sudah ada sebelum sesi ini. Empat poin dipperbaiki dan
tiga bukti di-upgrade berdasar hitung ulang independen:

1. **§(f) "7 target unik"**: draf lama menulis "2 Tokyo-LB + 5 round_d" (redaksi kacau).
   Koreksi: 7 = **5 Tokyo** (masing-masing punya kembaran `round_d`) + **2 London native**.
2. **§(g) bukti max-train**: draf lama menyebut "4 titik max-train" seolah ada bukti
   tercetak. Koreksi: hanya **3 assert**, ketiganya `loud=False` sehingga tidak mencetak
   PASS; bukti LOLOS bersifat inferensial dari 0-error output (§3g).
3. **§(h) angka "443/443"**: tidak reproducible. Angka yang benar dan terukur ulang:
   blok sel05 identik **1413/1413 byte** setelah 4 baris display dibuang; 7 dari 9 blok
   verbatim identik byte-per-byte.
4. **§(i) headline "5/5 COCOK"**: dipertahankan, tetapi R4 (kolom `cocok` manifest tak
   reproducible untuk baris output) ditambahkan secara objektif.
5. **Upgrade bukti**: (i) K24 kini **24/24 terkonfirmasi AST vs source run 9** (draf lama
   hanya "transcription-guard, bukan bukti komputasi"); (ii) R3 naik dari asumsi menjadi
   **fakta reproducible** (`sha256` LF→CRLF = `2D46B0F9…`); (iii) verbatim diuji
   byte-per-byte (draf lama spot-check substring).

---

## 6. S6 — Yang BELUM DIVERIFIKASI

1. **Nilai metrik per-bar per-semester vs eksekusi ulang independen** — hanya konsistensi
   boolean (d) + margin/threshold CSV (c) yang terverifikasi; re-eksekusi butuh
   menjalankan builder/notebook (dilarang untuk auditor).
2. **Determinisme rerun bit-identik (S3-4)** — tidak diuji ulang (butuh eksekusi).
3. **Kecocokan piksel FIG-18 vs nilai CSV** — terverifikasi level source (re-read + chk
   103/67/36) + PNG valid, bukan inspeksi piksel.
4. **Re-hash satu-per-satu file beku S8B** — tercakup via penjaga registry
   (260/6767/1315/1335/86) di level provenance.
5. **Jumlah assertion `ASSERT_LOG total: 1268`** — terbaca di output, tidak direproduksi
   statis (69 call site, sebagian beriterasi).
6. **Putusan dagang atas TABEL M3** — wewenang arsitek + user (B-4, S8A); auditor tidak
   memutus.

---

## 7. Kesimpulan dan rekomendasi

**LOLOS PROSEDURAL.** TABEL M3 103 pasangan sah sebagai keluaran L3-1. Daftar LOLOS-per-jenis
(angka, bukan vonis dagang):

| Jenis | Kind | LOLOS | GUGUR | total |
|---|---|---|---|---|
| Diskret | LB_bin | 25 | 0 | 25 |
| Diskret | LC1 | 7 | 2 | 9 |
| Diskret | LC2 | 13 | 6 | 19 |
| Diskret | LD | 11 | 3 | 14 |
| Kontinu | LB_rng | 12 | 24 | 36 |
| **Total** | | **68** | **35** | **103** |

LOLOS kontinu (12, semuanya `t1/t2 × N5–N60` London+Tokyo): `LB_rng London t1 N5/N15/N30/N60`,
`LB_rng Tokyo t1 N5/N15/N30/N60`, `LB_rng Tokyo t2 N5/N15/N30/N60`. (Dibaca dari CSV, tanpa
interpretasi.)

Rekomendasi:

1. Arsitek lanjut ke **vonis biner B-4** atas TABEL M3 ini (ada 68 LOLOS → cabang (a):
   minta persetujuan user untuk spec pemodelan; marginal-rate bukan sinyal).
2. Terapkan 4 RENDAH di ronde berikutnya: T-6 encoding log (R1), redaksi verbatim yang
   menyebut pengecualian display (R2), catat hash ganda pra+pasca normalisasi (R3), dan
   kolom `cocok` manifest yang jujur untuk baris output (R4).
3. I1–I4 sebagai catatan putusan (tanpa CI; tanpa re-eksekusi run 9; konjungsi mengikat;
   `arah` kembaran berbeda by-design).

STOP setelah serah-terima ini (S8A). Tidak ada vonis dagang di laporan ini.
