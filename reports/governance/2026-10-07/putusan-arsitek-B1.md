# Putusan Arsitek B1 — `build_features.py` (4 butir) — 2026-10-07

**Mandat:** user — putuskan 4 ambiguitas fondasi fitur B1 sebelum audit.
**Sumber dibaca langsung:** `src/features/build_features.py` 397/397 baris.
Angka lock / hasil test coder (34 hijau) diadopsi dari laporan coder, tidak
dihitung/diuji ulang — sesuai batas wewenang.

**Doktrin pengatur D0** (mengikat butir 1–2 sebagai satu kesatuan): *setiap
input timeframe wajib memiliki kolom output yang menurunkannya; input tanpa
konsumen = dihapus (preseden LOW-34); kebutuhan bar-grain milik uji strategi
(M5 untuk H2, spread M1 untuk H5) dipenuhi via baca-langsung parquet
sumber-EDA, bukan via kolom fitur.* Butir 1 dan 2 adalah dua penerapan doktrin
yang sama — bukan dua keputusan lepas.

## Butir 1 — Kolom spread H5 yang hilang → opsi (b): H5 baca `spread_pips` M1 langsung

Fakta sumber: `M1_REQUIRED` tidak memuat `spread_pips` (padahal kolomnya ada di
parquet per S10); `DAILY_COLUMNS` dan docstring cakupan tidak mengenal spread.
Menambah agregasi spread-per-sesi ke file 397/400 baris = split paksa untuk
SATU kolom tanpa konsumen kedua.

Syarat mengikat:

1. Protokol placebo H5 di Lapisan 3 membaca `spread_pips` dari parquet M1
   processed **langsung** — sumber yang sama dengan perhitungan M4 di nb05
   (`report.md`: M4 = spread p95 per sesi dari kolom `spread_pips` M1). Paritas
   sumber = reproduksibilitas terkuat; duplikasi kolom mentah ke store turunan
   justru memutusnya.
2. `M1_REQUIRED` tetap apa adanya (tanpa spread). Pemicu revisit: kebutuhan
   terkunci KEDUA atas kolom turunan-spread ber-grain-hari yang menyebut
   konsumennya.
3. Redaksi eksak disposisi REVIEW (coder menutup REVIEW dengan kalimat ini,
   bukan menghapus jejak): *"Kolom spread tidak ditambahkan (putusan arsitek B1-1): H5 membaca `spread_pips` M1 langsung per doktrin D0."*

## Butir 2 — Input M5 tanpa konsumen → opsi (a): buang M5 dari input

Fakta sumber: nol kolom output menurunkan M5 — dan memang tidak bisa: store ini
ber-grain M15-bar + fitur harian; satu-satunya konsumen M5 yang terkunci (H2,
"strategi M5/M15 momentum", EV-per-trade) butuh M5 **bar-grain untuk backtest
strategi**, yang tidak bisa dilayani baris fitur harian. H2 pasti membaca
parquet langsung — sama seperti H5 di butir 1. Argumen "validasi kontrak
fail-closed" gugur: kontrak yang divalidasi (ketersediaan M5 *untuk pipeline
ini*) menjadi vakum tanpa konsumen; validasi M5 tetap milik Lapisan 1
(`validate_data`/`resample`).

Syarat mengikat:

1. Hapus M5 dari input (blok konstanta, parameter, pemuatan, penerusan). Ganti
   dengan satu kalimat doktrin di docstring (redaksi eksak): *"M5 sengaja bukan
   input (putusan arsitek B1-2): tak ada kolom yang menurunkannya; H2 membaca parquet M5 langsung per doktrin D0."*
2. Pemicu revisit: kebutuhan terkunci atas kolom turunan-M5 ber-grain-hari yang
   menyebut konsumennya — sampai saat itu M5 tetap di luar.
3. Konsekuensi (bukan alasan): split file tertunda — TETAP: batch berikut (B2)
   wajib membuka dengan rencana baris (split vs tambah) SEBELUM implementasi,
   karena headroom kecil. Ini syarat proses, bukan vonis isi B2.

## Butir 3 — Satuan `atr_14_d1` + normalisasi H1 → SAHKAN harga (JPY), status quo, dengan kontrak satuan

Fakta sumber: `range_pips` (pip) × `atr_14_d1` (harga) → `range_atr` =
pip/harga, konvensi campuran yang MENGUNCI median 88,79. Mengubah ATR ke pip
tanpa menyentuh pembilang = 0,8879 (geser 100× persis peringatan coder);
mengubah keduanya = 0,8879 juga. Jadi yang dilindungi bukan "harga lebih
baik", melainkan **stabilitas klasifikasi tipologi** (ambang 88,79 → keranjang
trending/range identik EDA).

Syarat mengikat:

1. `atr_14_d1` tetap JPY; `range_pips` tetap pip; `range_atr` tetap pip/harga.
   Redaksi eksak kontrak satuan (masuk docstring modul): *"Satuan terkunci:
   `atr_14_d1` = JPY (harga, faithful nb05); `range_pips` = pip; `range_atr` =
   pip/harga (konvensi campuran, median lock 88,79); `ratio_path`, `rv_day`,
   `rv_roll_20d` = tak-berdimensi. DILARANG rasio kaki-campur selain
   `range_atr`."*
2. Normalisasi drift H1 di Lapisan 3 disahkan **harga/harga** (kaki sama-satuan,
   bebas jebakan 100×): `drift_harga / atr_14_d1(t-1)`. Sah untuk vonis H1
   karena ambangnya ("CI95 memuat 0") invarian-skala — satuan memengaruhi
   keterbacaan, bukan kelulusan.    Redaksi eksak untuk protokol L3: *"Drift dinormalisasi = drift searah (satuan harga) dibagi `atr_14_d1` hari-t-1 (satuan harga); implementasi wajib assert paritas satuan kedua kaki."*
3. Kolom pip di masa depan wajib sufiks `_pip` + uji invariansi rasio
   (kebalikan 100× = gagal).

## Butir 4 — Semantik `rv_roll_20d` → SAHKAN apa adanya (sum + 20 hari-broker + min_periods=20)

Fakta sumber: `.rolling(20, min_periods=20).sum()`; hari = kalender broker
(konsisten R3; 20 hari-broker ≈ 1 bulan, konsisten konvensi blok-20 v3.1). Sum
adalah definisi (RV = Σr²); mean akan mereskala 20× dan memutus komparabilitas
dengan orde EDA (3,648e-5 vs 2,292e-5). `min_periods=20` = hanya jendela penuh
(19 NaN warmup); jendela parsial akan menghasilkan jumlah tak-sebanding —
ditolak.

Syarat mengikat — redaksi eksak kontrak (masuk docstring `daily_metrics`):
*"`rv_roll_20d` = Σ `rv_day` 20 hari-broker penuh (sum, bukan mean),
`min_periods=20` → 19 bar awal NaN (warmup, jumlahnya dilaporkan, bukan
diisi); kalender hari-broker."* Log hitung NaN di `main()` wajib dipertahankan
sebagai bukti warmup.
