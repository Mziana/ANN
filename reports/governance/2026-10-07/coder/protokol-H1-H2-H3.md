# Protokol H1-H2-H3 — Lapisan 3

**Tanggal:** 2026-10-07 (revisi batch-3: 2026-10-08; revisi batch-4: 2026-10-08)
**Status:** DOKUMEN PROTOKOL — bukan vonis
**Sumber:** hipotesis_lock_v1.md + putusan arsitek F-1 + B1-3 + B1-4 +
          putusan-arsitek-H1-H5.md (S1–S6) + putusan-adjudikasi-reaudit-kedua.md (A/B/C)

---

## 0. Sumber kutipan S1–S6 (wajib ada di protokol)

S1–S6 dikutip kata-per-kata dari `arsitek/putusan-arsitek-H1-H5.md`
(hash git `e8eb03daf994051600258cf412ec9e9af65d800c`).
Tanpa kutipan ke dokumen itu = gagal (temuan re-audit #17).

> S1 (H1-H5:4-5): H1 kuatkan; redaksi + ambang + catatan risiko + klausul
> anti-penyelamatan + izin eksplorasi disahkan tanpa perubahan.
>
> S2 (H1-H5:6-8): H2 terima; (a) median = median EV-per-trade-after-cost
> dalam-tahun (2023/2024/2025; gugur bila ≤0 pada ≥2 tahun); (b) strategi
> diagnostik wajib pra-registrasi di Lapisan 3 sebelum uji.
>
> S3 (H1-H5:15-16): AUC = kalibrasi in-sample span terkunci, bukan klaim OOS.
>
> S4 (H1-H5:16-17): uji drawdown vs strategi diagnostik L3 pertama; filter
> DILARANG aktif sebelum S4 dievaluasi.
>
> S5 (H1-H5:18-19): EV memakai 6 jam tetap [14,13,0,15,12,7] + `cost_basis`
> fragmen 4b; uji pola OOS memakai 6 jam teratas hitung-ulang; dicatat
> terpisah.
>
> S6 (H1-H5:20-21): wajib lapor jumlah sel; klaim sel mana pun wajib koreksi
> multiplicity bernama (atau replikasi independen); tanpa itu = eksplorasi.

---

## 1. PRA-REGISTRASI H2 (WAJIB sebelum backtest)

DILARANG menjalankan backtest H2 sebelum dokumen ini selesai dan disetujui.
Batch ini berhenti di dokumen — eksekusi backtest menunggu persetujuan protokol.

### Nama strategi
H2 M15 momentum (deskripsi: trend-following M15 sederhana)

### Entry
- Masuk saat close > open di jam terakhir (jam 15 UTC) dengan konfirmasi
  bahwa hari sebelumnya diawali tren (hari trending menurut H1).
- Entry adalah satu observasi per hari-broker, **1x** per hari.

### Exit
- Keluar saat close < open di jam terakhir, atau
- Hari habis tanpa konfirmasi lanjut.

### SL-ATR
- Stop-loss = **1x** ATR 14-hari (`atr_14_d1`, **satuan harga JPY**).
- SL menggunakan ATR mentah (satuan harga JPY), **bukan normalisasi harga/harga**.
  Normalisasi harga/harga adalah paritas satuan drift (B1-3), bukan spesifikasi ATR.

### TP (Take Profit)
- Take-profit = 2x ATR 14-hari (`atr_14_d1`, satuan harga JPY).
- Rasio risiko-imbal = 2:1.

### Biaya
- Biaya = `cost_basis` mean sesi (fragmen 4b).
- DILARANG menggunakan spread yang berbeda tanpa justifikasi.

### Kriteria vonis H2
Dari hipotesis_lock_v1.md §H2:

**Ambang gugur:**
- EV-after-cost median ≤ 0 di ≥2 dari 3 tahun utuh 2023–2025 OOS
  (2026 parsial dikecualikan sebagai tahun berjalan; ambang 4-tahun penuh
  MENUNGGU DATA), ATAU
- rata-rata VR OOS ≤ 1.

**Catatan:** Ambang ini berasal dari lock, bukan dari data evaluasi.
Tidak ada optimasi ambang di batch ini.

---

## 2. ATURAN VONIS H1/H2/H3 (petakan 1-ke-1 ke ambang lock)

### H1 — Regime tipe-hari

**Ambang klasifikasi (dari hipotesis_lock_v1.md §H1):**
- Trending: ratio_path > 0.0268 AND range_atr > 88.79
- Range (tenang): ratio_path ≤ 0.0268 AND range_atr ≤ 88.79
- Normal: sisanya

**Sumber ambang:**
- 0.0268 = median ratio_path stratum A (lock, hipotesis_lock_v1.md)
- 88.79 = median range/ATR stratum A (lock, hipotesis_lock_v1.md)

**Ambang gugur H1 (dari hipotesis_lock_v1.md §H1):**
- Selisih drift median CI95 memuat 0, ATAU
- Share trending tak stabil antar tahun (chi-square antar-tahun p<0.01).

**Status:** BELUM DIUJI di batch ini. Test classify_day_label hanya
memeriksa label, bukan vonis H1.

### H2 — Mikro-momentum M15

**Ambang klasifikasi:** Tidak ada klasifikasi — H2 adalah strategi,
bukan label hari.

**Ambang gugur (dari hipotesis_lock_v1.md §H2):**
- EV-after-cost median ≤ 0 di ≥2 dari 3 tahun utuh 2023–2025 OOS, ATAU
- rata-rata VR OOS ≤ 1.

**Status:** PRA-REGISTRASI saja (dokumen ini). Backtest belum dieksekusi.

### H3 — Filter regime volatilitas

**Ambang klasifikasi (dari kontrak B1-4 + hipotesis_lock_v1.md §H3):**
- `rv_roll_20d` = Σ rv_day 20 hari-broker (sum, bukan mean, min_periods=20).
- `rv_score` = `rv_roll_20d` / 20 (mean, turunan label; store tetap sum
  per B1-4). /20 adalah transformasi label, bukan perubahan store.
  Menyebut hasil-bagi sebagai "sum" = gagal (temuan re-audit #18).
- `rv_regime_flag` = 1[`rv_score` > TAU_2023].
  TAU_2023 = ambang Youden (maksimum sensitivitas + spesifisitas − 1) dari
  ROC `rv_score` versus label-periode pada span kalibrasi terkunci
  2023-01-01..2023-12-31, dengan label B = broker-day dalam
  2023-01-01..2023-06-30 dan label A = broker-day dalam 2023-07-01..2023-12-31.
  Hari tanpa `rv_roll_20d` penuh (warmup NaN) dikecualikan dari kalibrasi
  dan berflag NaN — DILARANG default False.
- AUC yang dilaporkan = AUC in-sample span tersebut; DILARANG klaim OOS.
  DILARANG mengkalibrasi ulang pada span lain. DILARANG memilih ambang dari
  performa OOS. Nilai TAU_2023 + AUC + n per kelas wajib tertulis di protokol
  sebagai hasil kalibrasi, bukan sebagai ambang lock.
- S3 (sumber `arsitek/putusan-arsitek-H1-H5.md:15-16`): AUC = kalibrasi
  in-sample span terkunci, bukan klaim OOS.

**Hasil kalibrasi Q1(a) — DIEKSEKUSI 2026-10-08 (angka riil, output mentah
di `coder/laporan-fix-batch3-D1-D5.md` §5):**

| Besaran | Nilai |
|---|---|
| Span terkunci | 2023-01-01..2023-12-31 (broker-day store) |
| `rv_score` | `rv_roll_20d` / 20 |
| n kalibrasi | 240 (dari 259 hari-2023; 19 warmup NaN dikecualikan) |
| n per kelas | n_B = 111 (positif, hari-B = Jan–Jun 2023); n_A = 129 |
| **TAU_2023 (Youden, `>` strict)** | **2.5951672079821496e-05** |
| Sensitivitas / Spesifisitas pada TAU | 1.0000000000 / 0.6046511628 |
| J maksimum (sens+spec−1) | 0.6046511627906976 |
| **AUC in-sample (klasifikasi hari-B)** | **0.8173755150499336** |
| Hari ber-flag dalam span | 162/240 (B 111/111; A 51/129) |
| NaN warmup di seluruh D4 | 19/974 (min_periods=20) |

Kelas positif = hari-B, konsisten lock §H3 ("AUC klasifikasi hari-B") dan
basis lock (median RV harian B = 3,648e-5 > A = 2,292e-5; angka itu hanya
basis lock §H3, bukan ambang pakai). TAU_2023 bukan ambang lock — ia hasil
kalibrasi in-sample yang ditulis di sini sebagai hasil, dan dikunci sebagai
konstanta `TAU_2023` di `src/features/build_labels.py`.

Penguncian regresi (batch-4 butir 3, DISIPLIN 12): `RV_WINDOW_DAYS` terikat
kalibrasi lewat test DATA `test_rv_window_terikat_kalibrasi_ulang` di
`tests/test_build_labels.py` — TAU Youden dihitung ULANG dari kolom rv store
memakai jendela kode; mengubah jendela tanpa TAU hitung-ulang membuat test
MERAH (mutasi 20→10 → 1 failed). Perbandingan konstanta-vs-konstanta tetap
ada sebagai penjaga sinkron protokol, tetapi BUKAN penguncian.

**Ambang gugur H3 (dari hipotesis_lock_v1.md §H3):**
- AUC ≤ 0,7, ATAU
- Filter memotong >40% hari A tanpa mengurangi drawdown.

**Status:** BELUM DIUJI. `rv_regime_flag` berisi nilai (955/974 non-NaN; 19
NaN warmup) dengan TAU_2023 di atas. Status BELUM DIUJI tetap: vonis H3
(dan H4/H5) hanya lewat S4 + uji terpisah; batch ini tidak memvonis.

---

## 3. REDAKSI EKSAK F-1 (kata-per-kata dari putusan-arsitek-F1.md)

Dari putusan arsitek F-1 butir 2 (protokol B2-H4/H5):

> *"Bar pada 19 broker_day anomali (2024-10-28..11-01, 2026-03-10..03-27)
> dikecualikan dari agregasi sesi; uji sensitivitas wajib menjalankan kedua
> varian (inklusi vs eksklusi) dan melaporkan selisihnya."*

**Grep bukti:** Kalimat ini disalin verbatim dari
`reports/governance/2026-10-07/arsitek/putusan-arsitek-F1.md` **baris 73-75**
(kutipan L73-75; L36-38 berisi klausa lain — "Kolom harian … invarian-bit").
Path lama `2026-10-07/putusan-arsitek-F1.md` sudah usang; berkas kini di
`arsitek/`. Tidak ada perubahan redaksi.

---

## 4. STATUS BELUM DIUJI DAN LARANGAN EKSLUSI BUTA

### Status BELUM DIUJI

1. **gap_f2_flag:** Status BELUM DIUJI. Definisi Q3(a) dipertahankan
   kata-per-kata (bucket parsial = `m1_bars` < 15 DAN bukan bucket
   pertama/terakhir hari-broker) dan dieksekusi pada grain broker-day
   tunggal (putusan C). **Recount independen pada grain tunggal =
   tepat 234 hari-broker / 597 bucket mid-day parsial** — identik dengan
   angka B1 (`audit/audit-fondasi-B1.md:122`: "1.281 bucket parsial; 597
   di antaranya mid-day … spread di 234 hari broker").
   Rekonsiliasi (raw output di `coder/laporan-fix-batch3-D1-D5.md` §4):
   - Angka **479 DITOLAK sebagai artefak** grain campur (`utc.normalize()`,
     1174 hari-UTC); 479/479 hari-flag lama adalah hari-UTC tanpa identitas
     broker (ghost). Dilarang dipakai sebagai target, pembanding, atau pembenar.
   - Kontribusi grain UTC→broker: 1126 bucket/479 hari-UTC → 597 bucket/234
     hari-broker.
   - Kontribusi edge-rule: pada grain broker-day, Q3(a) BATAS HARI
     mereproduksi 597/234; varian BATAS SESI (run-label) = 578 bucket/230 hari
     — dilaporkan sebagai sensitivitas, bukan definisi.
   - Angka **234 tetap referensi orde + jangkar B1** (aturan `fix:86-87`
     "selisih = gagal" sudah DICABUT butir A); nuansa F-2 tetap berlaku:
     223 dari 234 hari ber-counterfactual.
   Status BELUM DIUJI dipertahankan sampai uji sensitivitas klasifikasi H1
   pada hari-hari itu ada; eksklusi buta TETAP DILARANG.

2. **rv_regime_flag:** Status BELUM DIUJI. Kolom berisi nilai (955/974
   non-NaN; 19 NaN warmup) dengan TAU_2023 hasil kalibrasi Q1(a) yang
   tertulis di §2 di atas. Status BELUM DIUJI dipertahankan sampai ada uji
   berkas hasil (S4).

3. **Konsumen B2-H1/H5:** Status BELUM DIUJI. Klaim "tak terpengaruh
   material" di test F-2 hanya prosa, bukan assertion (dari re-audit F-2).

### Larangan eksklusi buta

DILARANG menggunakan gap_f2_flag untuk eksklusi buta (tidak ada uji
sensitivitas). Eksklusi harus melalui protokol F-1: dua varian
(inklusi vs eksklusi) dengan pelaporan selisih.

**Tabel selisih varian eksklusi (dilaporkan via test, bukan artefak permanen):**
D4 sekarang hanya dua file nama kontrak (`usdjpy_day_labels.parquet` +
`usdjpy_h2_trades.parquet`); varian eksklusi dibuktikan via test
`TestDuaVarianEksklusi`, `TestQuarantineMask`, dan `TestMainEndToEnd` di
`tests/test_build_labels.py`, bukan lewat file `usdjpy_day_labels_excluded.parquet`
permanen. File `usdjpy_day_labels_excluded.parquet` dari Fase 1 sebelumnya
sudah dihapus dari `data/labels/`.

**Hasil test varian eksklusi (buktikan via pytest):**
- `TestQuarantineMask::test_19_hari_dua_jendela_terhitung`: mask karantina
  menandai tepat 19 hari-broker pada sintetis weekday yang memuat KEDUA
  jendela F-1 (5 hari 2024-10-28..11-01 + 14 hari 2026-03-10..03-27).
- `TestMainEndToEnd::test_day_labels_grain_dan_row_key`: pada D4 produksi,
  `quarantine_mask` dtype bool dengan True count = 19 dari 974 hari.
- `TestDuaVarianEksklusi::test_inklusi_vs_eksklusi_berbeda_di_hari_anomali`:
  selisih varian inklusi vs eksklusi = 5 hari (jendela 1) — >0, terhitung.

---

## 5. PENUNDAAN VONIS H3 (S4) + LARANGAN VONIS H4/H5

### Penundaan vonis H3 (Syarat S4)

Syarat S4 (sumber `arsitek/putusan-arsitek-H1-H5.md:16-17`):

- Uji drawdown vs strategi diagnostik L3 pertama.
- **Filter DILARANG aktif sebelum S4 dievaluasi**.

Status: PENUNDAAN sampai strategi diagnostik H3 dipilih dan diuji.
DILARANG memvonis H3 LULUS/GAGAL sebelum:
1. Strategi diagnostik H3 dipilih
2. Strategi diuji dengan data yang cukup
3. AUC (in-sample span terkunci) dihitung dan dibandingkan dengan ambang 0,7

Atribusi yang dibenarkan: S4 ← `arsitek/putusan-arsitek-H1-H5.md:16-17`.
L144 protokol lama yang menunjuk `hipotesis_lock_v1.md §H3` SALAH — lock
tidak memuat label S4.

### Larangan vonis H4/H5

Sumber larangan: `arsitek/putusan-arsitek-H1-H5.md:18-21`.

- **Protokol H4/H5 DILARANG divonis final** sebelum butir 2 diimplementasi
  (dua varian inklusi/eksklusi) dan hasil kedua varian tercatat.
- Karantina gugur hanya via putusan Arsitek baru atas bukti Finex/jangkar.

DILARANG memvonis H4/H5 LULUS/GAGAL di batch ini. H4/H5 hanya boleh
dijalankan dengan protokol karantina yang sudah terimplementasi.

Atribusi yang dibenarkan: larangan H4/H5 ← `arsitek/putusan-arsitek-H1-H5.md:18-21`.
L156 protokol lama yang menunjuk F-1 butir 2 SALAH — F-1 hanya mengatur
mekanisme karantina + garis B2.

---

## 6. CATATAN PENTING

1. Tidak ada backtest yang dijalankan di batch ini.
2. Tidak ada optimasi ambang dari data evaluasi. TAU_2023 adalah hasil
   kalibrasi in-sample pada span terkunci (Q1(a)), ditulis sebagai hasil —
   bukan ambang lock, bukan vonis.
3. Semua ambang lain yang dipakai berasal dari lock/putusan, bukan dari data.
4. H6+ tidak dibuat (D0 + putusan H1-H5).
5. File lama (build_features.py, test_build_features.py, parquet) tidak
   disentuh — hash `399e64b3…`/`ed7ac435…`/`07402f40…` identik sesudah batch.
6. Typo lama "EKSKLSI" telah dikoreksi menjadi "eksklusi".
7. Sumber kutipan S1–S6 wajib ada di protokol (Section 0); tanpa itu
   protokol gagal syarat blocking 5.
8. Grain tunggal (putusan C): seluruh rantai label memakai broker-day store
   (`prepare_bars`), `utc.normalize()` dihapus dari kode; `_daily_from_m15`
   (kode mati, sumber grain kedua) dihapus.
