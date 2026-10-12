# Re-audit L3-0 — Peta Arah G3-Pass + 98 LOLOS (Auditor Independen)

Peran: **Auditor independen** (bukan coder L3-0). Mode: read-only.
Tanggal: 2026-10-12. Mandat: `2026-10-12_reaudit-l30-auditor.md`.
Ruang lingkup: `scripts/_build_eda07_l30.py`, `notebooks/scalping/eda_07_l30_arah.ipynb`,
`T-L3-0_arah.csv`, `T-L3-0_peta98.csv`, `FIG-17_peta_arah.png`, `_l30_manifest.csv`, `run_l30.log`.

> **Batas yang dihormati.** Tidak ada builder/notebook beku yang dieksekusi. Tidak ada file di
> `D:\ANN` yang ditulis selain laporan ini. Seluruh harness auditor berada di
> `C:\Users\Fajar\AppData\Local\Temp\opencode\audit-l30\`.
> Laporan ini **tidak memuat vonis edge, model, kelayakan-trade, atau profitabilitas** — dan
> tidak boleh dibaca demikian. L3-0 adalah fase deskriptif; fase model adalah L3-1 dan masih
> terkunci.

---

## 1. Vonis

# LOLOS PROSEDURAL

Kedelapan mandat **(a)–(h) lolos tanpa satu pun selisih angka**. Rekonstruksi verdict
mandiri menghasilkan **98 LOLOS / 162 GUGUR** dengan himpunan target **identik** dengan
`T-L3-0_peta98.csv`. Tidak ada temuan TINGGI. Tidak ada temuan MENENGAH.

| Peringkat | Jumlah | Sifat |
|---|---|---|
| TINGGI | 0 | — |
| MENENGAH | 0 | — |
| RENDAH | 4 | Kosmetik/ketertelusuran; **nol dampak ke angka mana pun** |
| INFORMATIF | 2 | Penjaga untuk L3-1 |

Rekomendasi: **L3-1 layak dibuka secara prosedural** oleh arsitek — tetapkan 4 butir RENDAH
sebagai aplikasi, 2 INFORMATIF sebagai watch-item wajib pada brief L3-1.

### Pemetaan §18 AGENTS.md (semua section wajib)

§18 meminta section A–H dengan metrik performa dagang (Sharpe, DD, WR, PF, Expectancy).
Untuk ronde deskriptif tanpa P&L, section itu **tidak berlaku dan tidak mungkin dihitung** —
mengisi-nya justru akan melanggar S3-3 (larangan P&L/backtest/edge). Pemetaan jujur:

| §18 | Isi | Status L3-0 |
|---|---|---|
| A | Performa Dasar (Sharpe/DD/WR/PF/Expectancy) | **N/A by design** — S3-3 melarang P&L; tidak ada trade/equity curve |
| B | Analisis Trade | **N/A by design** — nol transaksi; artefak lift per pasangan, bukan trade |
| C | Analisis Regime (sesi/hari/bulan) | **TERPENUHI** — FIG-17 + pivot sesi × horizon (25 sel) |
| D | Robustness (sensitivity/walk-forward/MC) | **N/A by design** — tanpa model; Mondrian & bootstrap milik run 9/I-2, bukan L3-0 |
| E | Bias (look-ahead/survivorship/leakage/overfit) | **TERPENUHI** — §3 h3–h6 + regresi beku §3 h5 |
| F | Biaya (spread/slippage/komisi/bid-ask) | **N/A by design** — tanpa P&L; delta_normal per irisan (acuan biaya) dibawa sebagai metadata `irisan`, tidak dihitung ulang |
| G | Kegagalan | **TERPENUHI** — §5 Temuan |
| H | Kesimpulan | **TERPENUHI** — §7 + §1 vonis |

Preseden yang sama: `reaudit-lapisan3-H1H2.md` dan `reaudit-lapisan3-H4H5.md` (ronde deskriptif
sebelumnya) memakai struktur huruf yang disesuaikan isi ronde, bukan template A–H dagang.

---

## 2. S-0 — Gerbang masuk

| Pemeriksaan | Hasil | Status |
|---|---|---|
| HEAD | `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` | TERVERIFIKASI |
| Branch | `main` | TERVERIFIKASI |
| Staged (`git diff --cached --name-only`) | **0** | TERVERIFIKASI |
| SHA256 6 file L3-0 vs klaim coder | **6/6 COCOK** (penuh 64 hex) | TERVERIFIKASI |
| Ukuran byte 6 file | **6/6 COCOK** | TERVERIFIKASI |
| ASCII/LF/tail-LF | 5 file teks: `nonASCII=0, CRLF=0, tailLF=True` | TERVERIFIKASI |
| FIG-17 PNG | `nonASCII=22325, CRLF=4, tailLF=False` | **N/A** — PNG biner; byte non-ASCII adalah isi gambar, bukan pelanggaran format |

Rincian hash:

```
COCOK  E5468952EA0CFF3B  ok  23826  scripts/_build_eda07_l30.py
COCOK  723DA6C14855943D  ok  36666  notebooks/scalping/eda_07_l30_arah.ipynb
COCOK  F48323D2C671C0FA  ok  23851  reports/eda/2026-10-12/T-L3-0_arah.csv
COCOK  1F58D4DFE460CBCC  ok  14340  reports/eda/2026-10-12/T-L3-0_peta98.csv
COCOK  CE7E4F5CA9441473  ok  43845  reports/eda/2026-10-12/FIG-17_peta_arah.png
COCOK  9EB860A4A7AB9B9C  ok    976  reports/eda/2026-10-12/_l30_manifest.csv
--> cocok 6/6, tidak cocok 0/6
```

`run_l30.log` (artefak S3-4, menutup temuan T-2 ronde EDA-07): 1407 byte, UTF-8 **dengan BOM**,
0 CRLF, 21 LF, tail-LF. Isi memuat `nbconvert exit=0`, `pra-kompilasi 7 sel kode: OK`,
`registry L3-0: ...`, penjaga beku, `lock dilepas; build selesai.`, dan `EXITCODE=0`.

Seluruh deliverable L3-0 berstatus `??` (untracked) — **tidak ada yang ter-commit, tidak ada yang
ter-stage**. Delapan file ` M` yang tersisa adalah `.ai/*` dan `journal/thoughts` yang sudah
termodifikasi sebelum audit ini dimulai dan tidak disentuh auditor.

---

## 3. Hitung ulang independen (a)–(h)

Setiap tabel di bawah adalah hasil hitung ulang auditor **dari CSV beku + source**, bukan
dibaca dari output notebook. Output notebook hanya dipakai sebagai pembanding.

### (a) 153 = filter G3 T-07-3 + split 120/33 dari tanda lift

| Pemeriksaan | Hasil | Klaim | Status |
|---|---|---|---|
| Baris `G3=True` di `T-07-3_lift.csv` | **153** | 153 | COCOK |
| Baris `T-L3-0_arah.csv` | **153** | 153 | COCOK |
| Pasangan unik `(target,fitur)` arah.csv | **153** | — | tanpa duplikat |
| Pasangan unik `G3=True` T-07-3 | **153** | — | tanpa duplikat |
| Himpunan arah.csv vs himpunan G3-pass | **SAMA PERSIS**, simetris diff = **0** | — | COCOK |
| Split dari **tanda lift** (`lift>0` / `lift<0`) | **pos 120 / neg 33** | 120/33 | COCOK |
| Baris `lift == 0` | **0** | 0 | COCOK |
| Kolom `tanda` vs tanda lift | **0 baris beda** | — | COCOK |
| Nilai `lift` arah.csv vs T-07-3 | **0 baris beda** | — | COCOK |
| Nilai unik kolom `tanda` | `{neg, pos}` | tunggal-makna | COCOK |

Split dihitung ulang **dari tanda lift**, bukan dari kolom `tanda` — sesuai amanat. Keduanya
identik, sehingga arah tidak bergantung pada kolom turunan mana pun.

### (b) 5 Tokyo: 4-desimal + negatif eksak

| Target | lift CSV | Klaim | Cocok | 4 desimal | Negatif | `ci_hi < 0` | `tanda` |
|---|---|---|---|---|---|---|---|
| `LB_bin Tokyo t2 N15` | -0.0473 | -0.0473 | ya | ya | ya | -0.0114 | neg |
| `LB_bin Tokyo tALL N5` | -0.0549 | -0.0549 | ya | ya | ya | -0.0284 | neg |
| `LB_rng Tokyo tALL N5` | -0.7446 | -0.7446 | ya | ya | ya | -0.2600 | neg |
| `LB_bin Tokyo tALL N15` | -0.0279 | -0.0279 | ya | ya | ya | -0.0010 | neg |
| `LB_rng Tokyo tALL N15` | -1.5868 | -1.5868 | ya | ya | ya | -0.6550 | neg |

Kelima CI **seluruhnya di bawah nol** — bukan sekadar lift negatif. Baris `round_d` di
`arah.csv` berjumlah tepat 5 dan **bertanda `neg` 5/5**.

### (c) 2 baris kandidat `round_d` London: G3=False + CI memuat 0

Baris `round_d` di `T-07-3_lift.csv` dengan sesi London: **tepat 2**.

| Target | G3 | lift | CI | CI memuat 0 | Ada di `arah.csv`? |
|---|---|---|---|---|---|
| `LB_rng London t3 N5` | **False** | -0.5562 | (-1.1397, 0.0168) | **ya** | **tidak** |
| `LB_rng London tALL N5` | **False** | -0.4129 | (-0.9397, 0.0575) | **ya** | **tidak** |

Kedua lift negatif tetapi CI-nya memuat nol, jadi gagal ambang G3 (CI harus menyingkirkan 0).
Karena `arah.csv` = himpunan G3-pass, keduanya absen dari sana. Semua konsisten.

#### ⚠ KUALIFIKASI WAJIB — dua tingkat, jangan diringkas

Pernyataan "2 London absen" **benar hanya di tingkat BARIS kandidat `round_d`**. Di tingkat
**TARGET**, keduanya justru LOLOS:

| Target | Baris G3-pass fitur **asli** | Peta98 | Wakil | Arah |
|---|---|---|---|---|
| `LB_rng London t3 N5` | `rv15` → lift **13.8349** | **ADA** | `rv15` | **pos** |
| `LB_rng London tALL N5` | `rv60` → lift **14.1417** | **ADA** | `rv60` | **pos** |

Artinya:

- Yang **gugur** = 2 baris kandidat `round_d` London.
- Yang **LOLOS** = 2 target London tersebut, via wakil **rv15/rv60** (fitur asli, bukan `round_d`).

Mekanikanya benar dan bukan kebetulan: sel 2 notebook membangun `wakil` dari
`nat2 = T-07-2[t2.fitur != "round_d"]`, sehingga `round_d` **dikeluarkan dari kolam wakil**
meskipun ditandai `wakil=True` di CSV beku. Kualifikasi ini **wajib** diulang di setiap
laporan turunan; ringkasan tanpa kualifikasi akan salah baca.

### (d) Rekonstruksi verdict verbatim → 98

Auditor membangun ulang verdict **dari nol** dari tiga CSV beku, memakai rumus verbatim run 9
`ok = g1 AND g2any AND g3(wakil) AND (g4 == NA OR g4)`:

| Pemeriksaan | Hasil | Klaim | Status |
|---|---|---|---|
| Baris `T-07-1_balance.csv` (G1) | 260 target | 260 | COCOK |
| Target dengan tepat 1 wakil native | **260/260** | — | COCOK |
| Target dievaluasi | **260** | 260 | COCOK |
| **LOLOS hasil rekonstruksi auditor** | **98** | 98 | COCOK |
| **GUGUR = 260 − 98** | **162** | 162 | COCOK |
| Target unik `peta98.csv` | **98** | 98 | COCOK |
| Himpunan rekonstruksi == peta98 | **True** | — | COCOK |
| Kurang (di peta saja) | `[]` | — | KOSONG |
| Lebih (di rekonstruksi saja) | `[]` | — | KOSONG |

Independensi: skrip auditor **tidak mengimpor** helper apa pun dari builder/notebook coder;
`g1`, `g2any`, `g3w`, `g4` dihitung ulang dari isi CSV. Jalur `g2any` sengaja dibatasi baris
native (`fitur != "round_d"`) agar identik dengan `nat2` di sel 6.

### (e) Diff peta-vs-LOLOS kosong + arah = tanda wakil 98/98

| Pemeriksaan | Hasil | Status |
|---|---|---|
| `peta98` baris / target unik | 98 / 98 | TERVERIFIKASI |
| `wakil` peta98 == kolom `wakil` T-07-2 | **98/98** | TERVERIFIKASI |
| `arah` peta98 == tanda lift witnessed | **98/98** | TERVERIFIKASI |
| Pasangan `(target,wakil)` yang tak ada di `arah.csv` | **0** | TERVERIFIKASI |
| Split `arah` peta98 | **{pos 78, neg 20}** | Klaim 78/20 COCOK |

Arah peta98 diturunkan **hanya** dari tanda lift wakil. Tidak ada sumber arah lain.

### (f) FIG-17 mencakup penuh 153

FIG-17 memplot pivot `groupby(["sesi","horizon","tanda"]).size()` di atas seluruh 153 baris.
Auditor menghitung ulang pivot itu dari `arah.csv` dan membandingkannya sel-per-sel dengan
pivot yang dicetak notebook:

| Pemeriksaan | Hasil |
|---|---|
| Sel pivot terbaca dari output notebook | **25** |
| Sel pivot hitung ulang auditor | **25** |
| Sel **berbeda** | **0 (kosong)** |
| Total pos/neg pivot auditor | **120 / 33 = 153** |
| Tiap baris `arah.csv` masuk tepat 1 sel | **ya** |
| Signature PNG valid | ya |
| Dimensi PNG | **1400 × 500 px** = `figsize(14,5)` × `dpi=100` ✓ |
| Chunk `IEND` penutup | ada (file tak terpotong) |

Karena isi pivot yang diplot **identik** dengan hitung ulang auditor, FIG-17 secara data
memuat seluruh 153 baris. Verifikasi ini pada level **data**, bukan piksel — lihat §6.

### (g) Manifest 6/6 + `EXITCODE=0`

| File input beku | Hash aktual == hash tertanam | Flag `cocok` |
|---|---|---|
| `T-07-3_lift.csv` | ya | True |
| `T-07-2_mi_lantai.csv` | ya | True |
| `T-07-1_balance.csv` | ya | True |
| `T-06-7_gerbang_tercile.csv` | ya | True |
| `T-06-7_gerbang_sesi.csv` | ya | True |
| `_gate_G2_alarm.csv` | ya | True |

**6/6 COCOK.** Auditor menghitung ulang hash keenam file dari disk pada sesi ini — hasilnya sama
dengan yang tertanam di `_l30_manifest.csv`, jadi tidak ada file beku yang berubah sesudah L3-0.

Penjaga baris juga dihitung ulang (bukan dipercaya dari log):

| File | Dihitung ulang | Penjaga di `run_l30.log` |
|---|---|---|
| `T-07-1_balance.csv` | 260 | 260 ✓ |
| `T-07-2_mi_lantai.csv` | 6767 | 6767 ✓ |
| `T-07-3_lift.csv` | 1315 | 1315 ✓ |
| `T-07-4_stabilitas.csv` | 1335 | 1335 ✓ |
| `_gate_G2_alarm.csv` | 86 | 86 ✓ |

`run_l30.log` memuat literal `EXITCODE=0` dan `nbconvert exit=0`. **TERVERIFIKASI.**

### (h) Kepatuhan batas S3

#### h1 — Scope `irisan` verbatim run 9

| Pemeriksaan | Hasil | Klaim |
|---|---|---|
| `T-06-7_gerbang_tercile.csv` baris / LOLOS | 144 / **23** | 144 / 23 ✓ |
| `T-06-7_gerbang_sesi.csv` baris / LOLOS | 48 / **7** | 48 / 7 ✓ |
| Kolom `irisan` `arah.csv` == hitung ulang auditor | **153/153** | — |
| Kolom `irisan` `peta98.csv` == hitung ulang auditor | **98/98** | — |

Auditor membangun ulang `assoc_irisan()` sendiri dari T-06-7 (termasuk cabang `LA`/`ALL`).
Nol selisih pada 251 baris. Scope benar-benar verbatim, bukan disalin mentah.

#### h2 — K24: transcription-guard, dan AUDITOR MENINGKATKANNYA

Klaim coder sudah jujur: K24 L3-0 adalah **transcription-guard, bukan bukti komputasi** —
konstanta tidak dipakai satu pun dalam perhitungan L3-0. Auditor menguji apakah itu berlebihan.

Isi sel 2: `chk(got == exp, ...)` membandingkan setiap konstanta terhadap literal **yang ditulis
ulang di notebook yang sama**. Itu self-check yangReferential, persis kelemahan yang pernah
ditemukan di sel 6 I-2 ( Putusan A-4: "self-check terhadap literal turunan TIDAK CUKUP").

Auditor membaca 24 konstanta itu dengan **AST** dari sel 2, lalu membandingkannya dengan definisi
**aktual di notebook run 9** (`eda_07_label_fitur.ipynb`), termasuk tuple-assign dan dict seed:

```
konstanta terbaca dari K24 sel2 L3-0 : 24 (klaim 24)
konstanta PERSIS sama dgn definisi run 9 (AST) : 24/24
-> 24/24 konstanta K24 L3-0 cocok definisi run 9: True
```

**Nol drift, upgrading klaim coder dari self-check ke verifikasi independen.** Catatan kehati-hatian
tetap berlaku: ini membuktikan **transkripsi**, bukan hitungan — tidak ada satu pun konstanta K24
yang ikut dihitung dalam L3-0.

#### h3 — Larangan S3-3: tanpa model / skor / null / 2026

| Kategori | notebook L3-0 | builder L3-0 | laporan coder |
|---|---|---|---|
| model/fit (`.fit(`, sklearn, torch, MLP, split) | **0** | **0** | **0** |
| skor/metrik (`score`, `accuracy`, `brier`, `predict`) | **0** | 2 (teks larangan) | 3 (teks larangan) |
| null-model (`null_model`, majority-class, baseline) | **0** | **0** | **0** |
| P&L / backtest / edge | 2 (teks larangan) | 5 (teks larangan) | 4 (tekscharacters) |
| akses data 2026 | **0** | **0** | 5 (nama folder) |

Semua hit berada di **teks prohibitions** ("BUKAN model, BUKAN latih, BUKAN skor, BUKAN null"),
bukan di kode komputasi. Nol variabel acak: `np.random` 0, `random.` 0, `RandomState` 0,
`default_rng` 0, `seed(` 0 — determinisme by-construction terkonfirmasi.

**Akses data 2026 mustahil secara struktural**: ketiga CSV beku yang dibaca
(`T-07-1`, `T-07-2`, `T-07-3`) **tidak punya satu pun kolom waktu/tanggal**, jadi tidak ada
jalur kode untuk menyentuh holdout 2026. Nama `2026-10-12` yang muncul hanyalah nama folder.

#### h4 — 5 Tokyo: apakah dipakai sebagai sinyal?

Baris `round_d` — bagian yang **dilarang** — bertanda `neg` **5/5**. Tidak ada satu pun
disalin menjadi `arah=pos`. Auditor memeriksa lebih dalam, karena `peta98` menandai 4 dari 5
target Tokyo sebagai `arah=pos`:

| Target | `arah` peta98 |erexRepresentative yang dipakai | `lift` mewakil |
|---|---|---|---|
| `LB_bin Tokyo t2 N15` | **neg** | `hour_sin` | — |
| `LB_bin Tokyo tALL N5` | **pos** | `rv60` (**bukan** `round_d`) | 0.4162 |
| `LB_rng Tokyo tALL N5` | **pos** | `rv60` (**bukan** `round_d`) | 11.9112 |
| `LB_bin Tokyo tALL N15` | **pos** | `atr_m5` (**bukan** `round_d`) | 0.2722 |
| `LB_rng Tokyo tALL N15` | **pos** | `rv60` (**bukan** `round_d`) | 19.3823 |

**Penilaian auditor: BUKAN pelanggaran S3-0.** Alasannya, dengan rujukan teks:

1. S3-0 melarang kandidat **Tokyo** sebagai sinyal long/label arah positif "dalam bentuk apa
   pun". Efek INVERS adalah sifat **fitur `round_d` pada target itu** (C3/A-2: dekat level bulat
   → besaran lebih kecil), bukan sifat target secara keseluruhan.
2. S3-1 justru **menganggarkan** "Maksimal pasangan fase L3-1 = 5 Tokyo + subset 98 yang lolos
   S3-2". Spec itu sendiri justru mengondisikan keberadaan pasangan Tokyo di L3-1 - banned reading
   yang melarang target Tokyo sepenuhnya akan membuat anggaran S3-1 tak masuk akal.
3. Rumus verdict di-*mandat* verbatim run 9 memakai **wakil**, dan S3-0 membawa
   "98 LOLOS native = deskriptif, BELUM dibaca arahnya (W-3b)". Membaca arah adalah mandat L3-0
   (S3-1); tidak membacanya akan membuat fase ini hampa.

Karena itu `arah` pada peta98 diambil dari fitur native lain, **bukan** dari baris `round_d` yang
dilarang. Laporan ini tetap menandai isu ini sebagai **INFORMATIF/watch-item** (T-5) karena
CSV-nya sendiri tidak membawa penanda apa pun.

#### h5 — Tanpa fitur/irisan/target baru

| Pemeriksaan | Hasil |
|---|---|
| Target unik `arah.csv` | 148 (153 baris; 5 target punya 2 fitur) |
| Target unik `T-07-3` | 260 — himpunan arah ⊂ himpunan beku |
| Fitur unik `arah.csv` | 15, **seluruhnya** ⊂ 26 fitur beku `T-07-3` |
| Pasangan `(target,fitur)` arah.csv ⊆ pasangan G3-pass | **ya** |

Nol fitur baru, nol irisan baru, nol target baru. `pdhl_d` dan `noise` tidak muncul di mana pun
—artefak struktural tetap di luarOmong kosong (S3-0).

#### h6 — Jalur input: L3-0 **tidak** mewarisi bug T-1

Temuan T-1 ronde EDA-07: builder run 9 menulis ke `2026-10-10` sementara artefaknya di
`2026-10-12`. L3-0 **tidak** mengulangi kesalahan itu — sel 2 mendefinisikan **dua** path dan
memakainya tepat sesuai lokasi nyata:

| Path | Isi | Verifikasi |
|---|---|---|
| `REPORT_DIR` = `reports/eda/2026-10-12` | `T-07-1..4`, `_gate_G2_alarm` | 5/5 file ada di sini ✓ |
| `REPORT_10` = `reports/eda/2026-10-10` | `T-06-7_gerbang_tercile/­sesi` | 2/2 file ada di sini ✓ |

Semua jalur input terbukti menunjuk file yang benar-benar ada. Ini perbaikan nyata, bukan
pengulangan.

---

## 4. Klaim lain yang diuji ulang

| Klaim coder | Hasil auditor | Status |
|---|---|---|
| Notebook 8 sel = 1 markdown + 7 kode | 1 + 7 | COCOK |
| 7 sel kode tereksekusi, `exec_count` 1..7 | `[1,2,3,4,5,6,7]` | COCOK |
| 0 error | 0 output `error` | COCOK |
| `pra-kompilasi 7 sel kode: OK` | 7/7 `compile()` sukses | TERVERIFIKASI ULANG |
| `ruff: All checks passed!` | **auditor menjalankan ulang** → `rc=0`, "All checks passed!" | TERVERIFIKASI ULANG |
| `ASSERT_LOG total: 343` | rekonstruksi statis **344** (selisih 1) | LIHAT T-4 |
| Laporan coder 55 baris | 55 baris, UTF-8 valid | COCOK |
| Builder 530 baris | **529** baris | LIHAT T-3 |

`FIG_KEY` (`LB_bin Tokyo tALL N5`) dan `TOP3` I-2 (`LB_bin London t1 N5`, `LB_rng London t1 N5`,
`LC1 London t1 N5`)Ikut berada di himpunan 98 hasil rekonstruksi auditor — sesuai klaim.

---

## 5. Temuan

Tidak ada temuan TINGGI atau MENENGAH. Semua temuan di bawah **nol dampak ke angka mana pun**.

### T-1 (RENDAH) — Manifest menyimpan basename tanpa path; 2 dari 6 input ada di folder lain

`_l30_manifest.csv` kolomnya `file,sha256_aktual,sha256_sebelum,cocok` — **tanpa kolom path**.
Dua input bukan ada di folder yang sama dengan manifest:

| Input | Ditemukan auditor di | Hash cocok manifest? |
|---|---|---|
| `T-06-7_gerbang_tercile.csv` | `reports/eda/2026-10-10/` | **ya** |
| `T-06-7_gerbang_sesi.csv` | `reports/eda/2026-10-10/` | **ya** |
| 4 input lainnya | `reports/eda/2026-10-12/` | ya |

**Dampak**: klaim "6/6" tetap **benar** — auditor menghitung ulang keenam hash dan semuanya
cocok. Yang rusak adalah **ketertelusuran**: pembaca yang mengikuti manifest di foldernya sendiri
akan gagal menemukan 2 file dan risked menyimpulkan manifest salah. Baris sumber notebook
(`MANIFEST_PATHS`) memang benar dan memakai `REPORT_10`, jadi tidak ada program yang salah.

**Rekomendasi**: tambah kolom `path` (relatif terhadap root) ke `_l30_manifest.csv`. Murah,
menutup kelas celah yang sama dengan T-1 ronde EDA-07.

### T-2 (RENDAH) — Status "K24 24/24 nol drift = TERVERIFIKASI" dilebihkan di kolom status

Tabel klaim menulis "Deterministik tanpa RNG; K24 24/24 nol drift | **TERVERIFIKASI**". Bukti
yang dirujuk adalah output sel 2, yaitu perbandingan literal-terhadap-literal **di dalam file
yang sama** — bukti yang menurut Putusan A-4 **tidak cukup**.

**Koreksi-konteks, bukanNOVATION substansi**: isi kolom bukti sudah mengatakannya dengan benar
("K24 literal didokumentasikan sbg transcription-guard + provenance ... bukan hitungan"), dan
"Potensi masalah #3" makin tegas. Jadi **tidak ada overselling dalam substansi** — hanya
redaksi kolom status yang mengikuti jargon notebook.

**Nilai tambah auditor**: klaim itu kini benar secara independen. AST-vs-source run 9
→ **24/24 identik**. Rekomendasi redaksi: "K24 24/24 transcription-guard, dikonfirmasi
independen auditor 24/24 vs source run 9; bukan bukti komputasi."

### T-3 (RENDAH) — Jumlah baris builder 529, klaim 530

`len(splitlines()) == 529`, 529 LF, tail-newline ada. Klaim "530 baris"off by one.
Kosmetik; hash file tetap cocok, jadi tidak ada artefak yang salah.

### T-4 (RENDAH) — `ASSERT_LOG total: 343` vs rekonstruksi statis 344

Auditor menghitung panggilan `chk()` dari AST: 49 statis, 42 di luar loop. Iterasi runtime:

```
42 (luar loop) + 24 (loop K24) + 15 (5 CAND_TOKYO x 3) + 260 (groupby target) + 3 (TOP3) = 344
Klaim coder                                                                   : 343
Selisih                                                                       : 1
```

Penyebab selisih 1 **tidak dapat ditentukan tanpa mengeksekusi notebook**, yang dilarang mandat
read-only. Tidak ada `chk` yang terebungkus kondisi eksternal di level modul, sehingga tidak
ada kandidat penjelas yang terlihat. Metrik ini kosmetik dan tidak memengaruhi satu pun angka
deliverable. Dinyatakan **BELUM DIVERIFIKASI** untuk nilai presisi, bukan GAGAL.

### T-5 (INFORMATIF / watch-item) — 4 dari 5 target Tokyo ber-`arah=pos` di peta98 tanpa penanda

Empat target Tokyo masuk peta98 dengan `arah=pos` karena wakil **native**-nya (bukan
`round_d`). Penilaian auditor di §h4: **bukan pelanggaran S3-0** — S3-1 Sendiri menganggarkan
"5 Tokyo" sebagai pasangan L3-1 yang sah, dan efek INVERS adalah milik fitur `round_d`.

**Yang perlu diwaspadai**: `T-L3-0_peta98.csv` tidak membawa kolom apa pun yang memberi tahu
bahwa target-target itu **juga** memiliki baris `round_d` negatif yang dilarang. Pembaca
lanjutan yang hanya memegang CSV itu bisa salah membaca `LB_rng Tokyo tALL N15 | rv60 | pos`
sebagai sinyal arah Tokyo — persis yang S3-0 larang. Kekhawatiran berlipat: keempat `lift`
witness-nya besar (0.4162 / 11.9112 / 0.2722 / 19.3823), kategori **magnitudo-volatilitas**
yang S3-3 sudah larang dipakai sebagai bukti prediktabilitas arah. L3-0 hanya memakai **tanda**,
bukan magnitudo — jadi patuh; tetapi keduanya harus dijaga di L3-1.

**Rekomendasi**: tambah kolom penanda `punya_round_d_invers` (bool) pada `peta98`, atau
seksi penelas di ringkasan peta. Tanpa itu, pagar S3-0 hanya hidup di prosa laporan.

### T-6 (INFORMATIF) — `run_l30.log` memuat artefak format PowerShell

Isi log memuat blok `python.exe : [NbConvertApp] ...` / `CategoryInfo : NotSpecified:
(...RemoteException)` —-wrapper galat NativeCommandError PowerShell yang muncul karena stderr
di-*pipe* lewat `Tee-Object`, plus BOM UTF-8. Isi log sendiri utuh: `EXITCODE=0`,
`nbconvert exit=0`, dan penjaga beku semuanya ada dan terbaca.

**Dampak**: nol pada verdict. Hanya gangguan keterbacaan: pembaca mungkin mengira build
gagal karena ada blok galat. Kekotoran ini memang sudah dilaporkan coder sebagai "Potensi masalah #4"
dan sudah dinormalisasi ke UTF-8/LF — normalisasinya benar, sisa cosmetics wrapper-nya tidak.

---

## 6. S6 — Yang BELUM DIVERIFIKASI

| Butir | Alasan | Dampak |
|---|---|---|
| **Pembacaan piksel FIG-17** (label sumbu, tinggi batang, legenda) | Auditor tidak melakukan OCR/vision. Verifikasi dilakukan pada level **data**: pivot 25/25 sel identik dengan hitung ulang, signature/dimensi/`IEND` PNG valid | Implikasinya: isi data FIG terbukti; tampilan visual tidak |
| **Rerun determinisme bit-identik** | Menjalankan ulang builder/notebook dilarang mandat read-only. Klaim "deterministik by-construction" didukung bukti kode (nol RNG) + re-read dari disk, **bukan** oleh pembuktian ulang |_runner_; lihat T-4 |
| **Nilai presisi `ASSERT_LOG`** | Butuh eksekusi. Rekonstruksi statis 344 vs klaim 343 | Kosmetik |
| **Provenance menit-per-menit build L3-0** | Tidak ada log builder run 9/8 yang baik (T-2 ronde EDA-07 ditutup arsitek). `run_l30.log` *adalah* bukti yang diminta S3-4 dan **ada** | Nol |
| **Replikasi penuh di lingkungan bersih** | Di luar batas read-only yang dispec-kan | Nol |

Tidak satu pun butir di atas memengaruhi angka penentu. Semua angka deliverable
(153/120/33, 98/162, 78/20, 23+7, 6/6, EXITCODE=0) terverifikasi **langsung dari CSV beku dan
source**, bukan dari log.

---

## 7. Kesimpulan dan rekomendasi

### Vonis

**LOLOS PROSEDURAL.** Delapan mandat (a)–(h) terpenuhi tanpa selisih. Rekonstruksi verdict
mandiri menghasilkan 98 LOLOS dengan himpunan identik. Empat temuan RENDAH seluruhnya
kosmetik/ketertelusuran; dua INFORMATIF adalah pagar untuk L3-1. **Tidak ada temuan yang
membatalkan hasil L3-0.**

### Yang harus arsitek teruskan ke brief L3-1

1. **T-1** — kolom `path` di `_l30_manifest.csv` (biaya satu baris kode, menutup kelas celah T-1).
2. **T-2** — redaksi status K24: "transcription-guard, dikonfirmasi independen 24/24 vs source
   run 9", bukan "nol drift TERVERIFIKASI".
3. **T-3/T-4** — koreksi hitung baris builder (529) dan `ASSERT_LOG` (rekonstruksi statis 344).
   Keduanya non-blocking.
4. **T-5** — **wajib** sebagai watch-item: penanda `punya_round_d_invers` di peta, dan larangan
   eksplisit memakai magnitudo-volatilitas (0.4162 / 11.9112 / 0.2722 / 19.3823; London
   13.8349 / 14.1417) sebagai bukti prediktabilitas arah di L3-1.
5. **T-6** — jalankan log lewat redirect langsung (bukan `Tee-Object`) agar runner-log tidak
   tercemar wrapper galat PowerShell.

### Yang TIDAK boleh terjadi

- Laporan ini **tidak** mengesahkan L3-1 secara substantif. Membuka L3-1 adalah wewenang
  arsitek, dan urutan M1/M2/M3 S3-2 belum dijalankan siapa pun.
- Angka 98, 78/20, dan seluruh lift di sini adalah **deskriptif**. Tidak ada satu pun yang
  menyatakan kelayakan-trade, edge, atau profitabilitas. FITUR `pdhl_d`/`noise` tetap artefak
  struktural dan tetap dilarang masuk sebagai fitur/label.

### STATUS

**L3-0 LOLOS PROSEDURAL. Menunggu putusan arsitek atas buka/tutup L3-1.**
Auditor berhenti di sini — **STOP**. L3-1 tetap terkunci sampai ada putusan arsitek.
