# Spesifikasi Pra-Registrasi -- Uji H4b-Stabilitas Lintas-Tahun

**Peran penulis:** Arsitek (AGENTS.md S26: merancang; DILARANG menulis
kode produksi, DILARANG commit/push). **Status:** PRA-REGISTRASI --
dikunci SEBELUM eksekusi coder; setiap penyimpangan = gagal gate.
**Tanggal lock:** 2026-10-09. **Disetujui user:** 2026-10-09 (desain
dua-arah atas data beku, tanpa 2026, tanpa H6).
**Bukan vonis ulang:** vonis H4 TAHAN Batch-2
(`putusan-lapisan3-H4H5.md`) tak tersentuh putusan apa pun dari ronde
ini. Ronde ini memutus H4b saja.
**Aturan besi:** tiap klaim angka WAJIB ditempel output mentah (S5);
klaim tanpa output mentah = GAGAL.

---

## H4b. Pertanyaan + lock verbatim (DIPUTUS, mengikat)

**Pertanyaan tunggal:** "Apakah efek H4 bertahan lintas-tahun pada
data beku 2024-2025?"

**Lock H4b verbatim -- GUGUR bila pada SATU PUN tahun-uji: (a) >= 2
dari 6 jam-teratas-train jatuh di Off, ATAU (b) median EV-after-cost
pool tahun-uji <= 0. TAHAN hanya bila KEDUA arah: n_Off <= 1 DAN
median EV > 0.**

Tahun-uji = 2025 pada arah Maju, 2024 pada arah Mundur (lihat
prosedur). Struktur lock ini sejajar lock H4 (`:124-125`); tanpa
angka/ambang baru.

**Keterbatasan yang dicatat jujur (mengikat interpretasi):**
pertanyaan ini termotivasi temuan EKS-3 (tanda 2025 negatif pada
pool gabungan) sehingga bobot konfirmatorinya terbatas; vonis H4b
tetap sah dan mengikat sebagai vonis atas H4b. GUGUR(H4b) TIDAK
meruntuhkan TAHAN(H4 Batch-2). TAHAN(H4b) BUKAN klaim kebal umum.

---

## Input beku (sha diverifikasi SEBELUM hitung, mismatch = STOP)

- M1 2024: `data/processed/M1/usdjpy_m1_2024.parquet`
  sha256 `69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac`
- M1 2025: `data/processed/M1/usdjpy_m1_2025.parquet`
  sha256 `fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af`
- M15 store: `data/features/M15/usdjpy_m15_features.parquet`
  sha256 `cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb`
- D4 labels: `data/labels/usdjpy_day_labels.parquet`
  sha256 `47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c`
- Resep mesin S-H4: `sh4.py` Batch-2 (jam tetap, ATR T-1, SL 1x ATR,
  TP 2x ATR, biaya by_session Off->0.65 x pip 0.01, fill exact,
  join-gate posisional). DILARANG mengubah satu pun konstanta.
- Data 2026 DILARANG dipakai (offset belum terverifikasi).

---

## Prosedur (dua arah, anti-intip)

**Arah Maju (train 2024 -> uji 2025):**
1. M2: hitung top-6 jam HANYA dari bar 2024. Kunci daftar 6 jam.
2. E1: bangun pool EV HANYA dari bar 2025 pada 6 jam terkunci
   (ATR T-1 dari store beku, biaya by_session, fill exact).
3. Hitung: n trade, n_Off/any_off/maj_off (definisi Off beku),
   median + mean EV pool-uji, fraksi positif, exit-cause counts.
4. Assert: loop entry HANYA memakai 6 jam-terkunci (gate anti-intip;
   skrip GAGAL bila daftar tersentuh data uji).

**Arah Mundur (train 2025 -> uji 2024):** cerminan persis langkah
1-4 dengan tahun ditukar.

**Karantina F-1:** 5 hari dalam-jendela 2024-10-28..11-01
dilaporkan sebagai counter deskriptif per arah (pertanyaan
eksklusi sudah diputus fondasi-B); DILARANG eksklusi buta di luar
19 hari F-1; varian default = INKLUSI.

**Determinisme:** coder run 2x (sha256 artefak identik) +
auditor replikasi independen dari nol. Seed dan toolchain
diumumkan di laporan.

---

## Gate + deliverable coder

- **S0:** `git hash-object` spec ini + 4 blob Batch-2 diukur ulang
  sesi coder (bukan salin); mismatch = STOP.
- **SHA:** keempat sha256 input di-assert sebelum hitung.
- **Artefak:** JSON per arah (`h4b_maju.json`, `h4b_mundur.json`)
  + `git hash-object` tiap artefak ditempel (pola R-4).
- **Laporan:** `coder/hasil-H4b-stabilitas.md` berisi tabel Klaim &
  Bukti, output mentah kedua arah, kedua daftar top-6 + selisihnya,
  aturan baca terisi, self-audit 3x, STOP. Nol tulis repo lain.
- **Dokumen ronde ini memakai pengikatan eksternal (P-4/T2):**
  TANPA self-hash di dalam dokumen; hash dilaporkan di kanal luar.

---

## Aturan baca TERTUTUP (dua sisi hasil)

1. Terapkan lock H4b verbatim pada angka kedua arah; tepat satu
   vonis: **GUGUR(H4b)** atau **TAHAN(H4b)**.
2. GUGUR(H4b) = efek tidak stabil antar-tahun; vonis tegas dan
   final atas H4b; DILARANG merembet ke vonis H4 Batch-2.
3. TAHAN(H4b) = stabil pada split beku dua-arah; DILARANG dibaca
   sebagai klaim kebal/robust umum (tanpa uji pra-registrasi segar
   di data segar).
4. Tanpa statistik keputusan tambahan; tanpa filter regime
   (`rv_regime_flag`/TAU DILARANG diaktifkan -- putusan H3
   mengikat); tanpa kalibrasi ambang; tanpa H6.

STOP. Spec terkunci; menunggu ronde coder.
