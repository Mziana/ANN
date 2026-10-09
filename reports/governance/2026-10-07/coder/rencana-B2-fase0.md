# Rencana B2 Fase 0 — Label + Protokol H1/H2/H3 + Pagar H4/H5 — 2026-10-07

**Sifat:** laporan rencana, BUKAN kode. Nol baris implementasi ditulis di batch
ini. Rencana yang disetujui = kontrak; penyimpangan = gagal.
**Mandat:** B2 = `build_labels.py` + protokol H1/H2/H3. H4/H5 pagar saja.

## 0. Keadaan aktual terverifikasi (tangan sendiri, 2026-10-07)

| Artefak | Hash git | Status vs mandat |
|---|---|---|
| `src/features/build_features.py` | `399e64b372e430b6def79b4fa8324a4e8e629918` | cocok |
| `tests/test_build_features.py` | `ed7ac43520c4431519d4d7065504866ae9b3ad95` | cocok |
| `data/features/M15/usdjpy_m15_features.parquet` | `07402f40478aaed9391203f5db3237d636f5a959` | cocok, DILARANG bergeser |

Anggaran via AST (`lineno–end_lineno`, hitung sendiri):

| Fungsi | Span | Baris | Budget |
|---|---|---|---|
| `daily_metrics` | 213–262 | 50 | 50/50, headroom 0 |
| `build_features` | 265–302 | 38 | — |
| `session_fingerprint/flags/label` | 92–138 | 13/15/15 | — |
| `require_columns/prepare_bars/load_processed` | 141–210 | 14/21/31 | — |
| `_assert_daily_is_previous_day` | 305–328 | 24 | — |
| `write_features/parse_args/main` | 331–396 | 15/13/34 | — |
| Modul | 1–400 | **400 fisik** | 400/400, headroom 0 |

Test: 357 baris fisik, 37 test (`TestDailyMetrics` 53 baris termasuk 2 test F-4;
`TestBuildFeatures` 67 baris termasuk `test_f2_*` 16 baris dengan status
BELUM DIUJI di docstring baris 331–333).
Sumber keputusan yang dibaca langsung: `hipotesis_lock_v1.md` (163 baris),
`putusan-arsitek-B1.md`, `putusan-arsitek-F1.md` (penulis sendiri),
`reaudit-F2-F3-F4.md` (438 baris), `konfirmasi-R1-R2-R3.md` (40 baris).

## 1. Rencana split — file lama NOL sentuh

**Pernyataan: label hidup 100% di file baru tanpa menyentuh file lama.**
Bukti: yang dibutuhkan label hanyalah *memanggil* — `daily_metrics`,
`load_processed`, `prepare_bars`, `session_flags`, `exclusive_session_label`,
konstanta `ATR_WINDOW/RV_WINDOW/DAILY_COLUMNS/FEATURE_COLUMNS/SESSION_*` —
semuanya importable dari `src.features.build_features` tanpa mengubah satu
barisnya (impor ≠ modifikasi; hash `399e64b3` wajib identik sesudah batch).
Arah impor satu arah: `build_labels → build_features`; `build_features`
tidak mengimpor modul label (impornya hari ini hanya `src.data.*` +
`src.utils.config`, baca baris 45–48). Tanpa siklus, by construction.

| Pecahan baru | Isi | Kontrak |
|---|---|---|
| `src/features/build_labels.py` (baru, ≤400 baris, tiap fungsi ≤50) | label hari H1, drift London 4h + assert paritas, flag rezim RV H3, `quarantine_mask()`, kerangka dua-varian H4/H5, `main()` + writer parquet baru | import dari `build_features` (reuse) + `load_config` (config); tidak ada import balik |
| `tests/test_build_labels.py` (baru) | test label sintetis-in-memory (gaya `test_build_features`: tanpa MT5, deterministik) + test eksklusi karantina + test dua-varian tercatat | tidak menyentuh `test_build_features.py` (357 baris tetap) |
| `reports/governance/2026-10-07/protokol-H1-H2-H3.md` (baru) | pra-registrasi H2 + aturan vonis H1/H2/H3 + redaksi eksak F-1 kata-per-kata | prosa mengikat sebelum angka jalan |
| `data/labels/usdjpy_day_labels.parquet` (baru) | label grain-hari H1/H3 | nama eksplisit; BUKAN tambalan store B1 |
| `data/labels/usdjpy_h2_trades.parquet` (baru) | trade log diagnostik H2 dari M5 langsung | nama eksplisit; sumber M5 per D0 |

**Fungsi yang pindah file: TIDAK ADA.** Fungsi baru semuanya di `build_labels`
(lihat §2). Anggaran sesudah: `build_features.py` 400→400, `daily_metrics`
50→50, `test_build_features.py` 357→357, parquet B1 `07402f40` identik —
ditagih ulang di Fase 1 dengan `git hash-object` + AST yang sama.

## 2. Peta label→hipotesis (kolom tanpa konsumen = tidak dibuat)

| Kolom label baru | H | Sumber baca | Catatan terima |
|---|---|---|---|
| `day_label` (trending/normal/range, ambang lock ratio_path 0,0268 & range/ATR 88,79, grain hari-broker D-1) | H1 | `daily` via `daily_metrics` (reuse) | ambang dari lock; identifikasi H+1 pagi real-time, bukan ex-post |
| `london_drift_4h` (close−open 16 bar M15 sesi-London pertama per hari) + `london_drift_norm` (drift_harga / `atr_14_d1`(t−1), **assert paritas satuan kedua kaki**, putusan B1-3) | H1 | store B1 (flag `is_london` + `date_broker`; 4 jam pertama = 16 bar `is_london` paling awal per hari — tanpa jam-lokal baru, tanpa duplikasi definisi sesi) | sign test + CI95 = prosedur protokol, bukan kolom |
| `gap_f2_flag` (1 = hari mengandung bucket mid-day partial, 234 hari) | H1 | M15 `m1_bars` + dokumen efek (+0,019% median / +0,28% p95 / +1,06% maks, `range_atr` 0%) | **DINYATAKAN di protokol: ditandai + uji sensitivitas inklusi/eksklusi; klaim materialitas BELUM DIUJI** (residual F-2 #2). Eksklusi buta DILARANG (24% sampel). Prosa tanpa status = gagal |
| strategi diagnostik H2 pra-registrasi (entry/exit/SL-ATR/TP + biaya per trade, dokumen) | H2 | — (dokumen, syarat lock S2, ditulis SEBELUM satu pun backtest) | tanpa dokumen ini backtest = gagal |
| trade log (`usdjpy_h2_trades.parquet`: entry/exit/hasil/trade-cost) | H2 | **parquet M5 langsung** per D0 (B1-2); biaya = `cost_basis` fragmen 4b (mean sesi), BUKAN `spread.default` | bila diagnostik memakai atribusi sesi → karantina F-1 berlaku (dinyatakan eksplisit di protokol) |
| `rv_regime_flag` (`rv_roll_20d`/20 > ambang; skala /20 agar cocok basis lock orde `rv_day` 3,648e-5 vs 2,292e-5) | H3 | `daily` via `daily_metrics` (reuse) | prosedur penetapan ambang di protokol: formula tertutup/kalibrasi span in-sample terkunci — DILARANG mengoptimasi di data evaluasi; ambang gugur AUC ≤ 0,7 dari lock |
| `quarantine_mask` (19 broker_day) + kolom `run_variant` (inklusi/eksklusi) | H4/H5 pagar | predikat dari `validation.anomaly_windows` (config, bukan hardcode) | **VONIS FINAL DILARANG di batch ini** |

Tidak dibuat: kolom spread agregat (B1-1, H5 baca M1 langsung), kolom turunan-M5
grain-hari (B1-2), kolom karantina di store B1 (F-1 butir 1), label H6+
(DITOLAK S7).

## 3. Mekanisme karantina H4/H5 (pagar, bukan vonis)

1. **Di mana predikat dibaca:** `load_config("data")["validation"]
   ["anomaly_windows"]` → 19 tanggal eksplisit. DILARANG pola "wall-open 00:00"
   (120 hari H1-2023 cocok pola itu dan BUKAN anomali — putusan F-1 §2.1).
2. **Di titik mana eksklusi diterapkan:** fungsi `quarantine_mask()` di
   `build_labels.py`, dipakai oleh agregasi sesi konsumen (H4 per-jam, H5
   placebo-per-sel) — **sisi konsumen, BUKAN store B1** (F-1 butir 1;
   `build_features.py` dan parquet `07402f40` tak tersentuh).
3. **Dua varian:** setiap agregasi sesi dijalankan 2× (`run_variant` =
   `inklusi` / `eksklusi`); kedua hasil ditulis + tabel selisih masuk protokol.
   Test mengunci: eksklusi membuang tepat bar 19 hari, varian tercatat beda.
4. Redaksi eksak berikut masuk `protokol-H1-H2-H3.md` **kata-per-kata**:
   "Bar pada 19 broker_day anomali (2024-10-28..11-01, 2026-03-10..03-27)
   dikecualikan dari agregasi sesi; uji sensitivitas wajib menjalankan kedua
   varian (inklusi vs eksklusi) dan melaporkan selisihnya."

## 4. Kontrak Fase 1 (atas persetujuan eksplisit)

Kode + test + protokol H1/H2/H3 + pagar H4/H5, lalu verifikasi mandiri:
`pytest` (lama 37 hijau + baru hijau), `ruff check`, `ruff format --check`,
`check_foreign_chars` semua artefak, `git hash-object` (lama identik +
baru tercatat), tabel anggaran §0 dihitung ulang, residual baru dinamai
eksplisit (#8, #9, … — tidak menimpa #1–#7). Tanpa itu = belum selesai.
DILARANG commit.

---

**STOP.** Menunggu persetujuan eksplisit user atas §1–§4 sebelum satu baris
implementasi pun ditulis.
