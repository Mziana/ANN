# Putusan Arsitek F-1 — Karantina 19 hari anomali (MEDIUM) — 2026-10-07

**Mandat:** user — putuskan temuan audit F-1 sebelum B2-H4/H5.
**Sumber auditor:** kutipan verbatim dalam mandat (berkas `audit-fondasi-B1.md`
tidak ditemukan di `reports/governance/2026-10-07/` — hanya ada
`hipotesis_lock_v1.md`, `putusan-arsitek-B1.md`, `putusan-arsitek-H1-H5.md`).
**Reproduksi:** tangan sendiri via `venv/Scripts/python.exe`
(pandas 2.2.3, numpy 1.26.4) atas `data/processed/M15` + `M1` 2023–2026 +
`src/features/build_features.py` (`git hash-object` = `1c9da4b4…`, sama dengan
yang disitir mandat — berkas tak berubah sejak B1).
Angka EDA lock / klaim auditor yang tidak direproduksi di bawah = di luar
putusan ini.

## Deep-dive 1 — Angka auditor cocok 8 dari 8 (PERLU VERIFIKASI → TERVERIFIKASI)

Jendela-1 2024-10-28..11-01: **460 bar / 5 hari** (92/hari).
Jendela-2 2026-03-10..03-27: **1288 bar / 14 hari** (92/hari).
Keduanya buka wall **00:00**, utc-pertama **21:00**.
Tetangga normal: 2024-10-25 buka 01:00/22:00; 2024-11-04 buka 01:00/23:00
(musim dingin +2, transisi DST 3 Nov — penanda offset bekerja);
2026-03-09 buka 01:00/22:00 (n=88, spring-forward 8 Mar — 4 bar hilang wajar);
2026-03-30 buka 01:00/22:00.
NaN-saat-ini: **0** di semua kolom kedua jendela (posisional D-1 utuh).
Simulasi −1 jam: W1 **pindah 20, NaN 4**
(00:00–00:45 tgl 28 → Minggu 27, absen dari indeks harian);
W2 **pindah 56, NaN 8** (00:00–00:45 tgl 16 dan 23 → Minggu 15 dan 22).
Simulasi +1 jam: **pindah 0** (hari anomali 00:00–22:45, tak ada bar 23:xx).

## Deep-dive 2 — Blast radius: formal-besar, material-kecil, terlokalisasi sesi

1. **H1-2023 adalah rezim, bukan anomali.** 120 hari weekday
   2023-01-02..2023-06-16 semuanya wall-open 00:00 (total 139 = 120 + 19).
   Ini strata B / regime SA-03 yang sudah di-stratifikasi EDA — BUKAN objek
   karantina. Predikat karantina = daftar tanggal eksplisit 19 hari, DILARANG
   memakai pola "wall-open 00:00".
2. **Kolom harian (input H1/H3) invarian-bit terhadap kebenaran offset.**
   `broker_day` turun dari digit wall teramati (fakta), bukan dari offset
   (inferensi) — pengelompokan harian identik di bawah hipotesis +3 maupun +2.
   M2 hitung-ulang M1 2023–2026 (1.347.847 bar, cocok dengan lock EDA):
   himpunan 6 jam teratas **identik** dengan/tanpa 19 hari
   ([14,13,12,15,0,7] vs [14,13,15,12,0,7] — hanya urutan 12/15 bertukar);
   Off-share 0,0 vs 0,0; Δ 26.198 bar.
3. **Yang berisiko hanya nilai-sesi 1748 bar jendela** (1,94% store),
   dan hanya di bawah hipotesis +2 (kebenaran offset BELUM TERVERIFIKASI —
   item TASKS.md terbuka, `data.yaml` "Menunggu jawaban Finex").
   Di bawah koreksi +1 jam: churn label eksklusif **228/1748 (13,0%)**
   (Sydney 228→152, NewYork 304→380; Tokyo/London tetap);
   sisi kuartil-ATR H5 invarian (attach harian tak bergerak).
4. **H4 imun agregat.** Tiap 6 jam top memuat tepat 76 bar jendela
   (19 hari × 4 bar, share 4,167% seragam) — rotasi +1 jam mempertahankan
   total per jam 456→456. Peringkat jam tak dapat bergeser oleh koreksi ini.
5. Sim −1h auditor dibaca sebagai **analisis sensitivitas arah-salah**:
   koreksi ke arah yang keliru menghasilkan tebing NaN (hari Minggu absen),
   bukan kesalahan sunyi — arah +2 adalah satu-satunya koreksi yang
   konsisten-sendiri (0 pindah hari). Kebenarannya tetap menunggu Finex.

## Putusan — opsi (a) karantina-presisi + opsi (b) larangan dipertahankan

Karantina dikenakan pada **nilai kolom sesi** (`is_tokyo/is_london/is_ny/
is_sydney`, `session_label`, `hour_utc`) pada **19 broker_day eksplisit**,
BUKAN pada baris, BUKAN pada kolom harian. Larangan `data.yaml`
("jangan dipakai untuk fitur sesi ... sebelum dikonfirmasi ke Finex")
**dipertahankan penuh** untuk 19 hari tersebut sampai Finex menjawab tertulis
atau jangkar independen membuktikan offset (penentu: Arsitek).

Syarat mengikat:

1. **Tanpa perubahan B1.** Karantina hidup di sisi konsumen (B2), bukan di
   `build_features.py` — berkas 397/400 baris DILARANG tersentuh putusan ini
   (satu kolom penanda pun memaksa split; tak ada yang membenarkannya).
   B2 membaca predikat dari `validation.anomaly_windows` di config.
2. Redaksi eksak protokol B2-H4/H5 (masuk dokumen protokol Lapisan 3):
   *"Bar pada 19 broker_day anomali (2024-10-28..11-01, 2026-03-10..03-27)
   dikecualikan dari agregasi sesi; uji sensitivitas wajib menjalankan kedua
   varian (inklusi vs eksklusi) dan melaporkan selisihnya."*
3. **H1/H2/H3 jalan tanpa gate F-1.** Kolom harian terbukti invarian (§2);
   H2 membaca parquet M5 langsung per doktrin D0 — bila aturan diagnostiknya
   memakai atribusi sesi, butir 2 berlaku untuknya juga (dinyatakan eksplisit
   di protokol, bukan diasumsikan bebas).
4. **H1-2023 dikecualikan eksplisit** dari karantina (rezim, bukan anomali).
5. Pencabutan karantina = putusan Arsitek baru atas bukti Finex/jangkar —
   DILARANG coder/auditor mencabut via "offset tampak +2".

## Dua batas tahap

1. **F-2/F-3/F-4 (LOW) boleh se-batch**, independen, non-blokir terhadap
   putusan ini maupun terhadap B2.
2. **Garis B2:** label + protokol H1/H2/H3 boleh selesai penuh; protokol
   H4/H5 DILARANG divonis final sebelum butir 2 diimplementasi dan hasil
   kedua varian tercatat. Karantina gugur hanya via butir 5.
