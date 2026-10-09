# Laporan Tahap 2 — Notebook 00 (`eda_00_setup.ipynb`)
**Tanggal:** 2026-10-06 01:52 SEAST
**Status:** SELESAI (terverifikasi di disk; belum di-commit — aturan: jangan commit sebelum audit Klenz EDA)

## 1. Tujuan
Bangun notebook fondasi EDA v3: load config+parquet, peta sesi (winter/summer primer vs cross-tab UTC-tetap), audit strata A/B/C, matriks kolom per TF, preregistrasi protokol placebo Q6 (seed tetap), kunci definisi, serta cetak **Kontrak 00 verbatim** sebagai output cell pertama. Top-to-bottom, semua output cell tersimpan.

## 2. File yang Dibuat
- `notebooks/scalping/eda_00_setup.ipynb` — baru; belum di-commit.
- `reports/eda/progress/laporan_tahap_2_nb00_setup.md` — laporan ini.

Catatan koreksi: versi pertama laporan ini menyebut `notebooks/scalping/_build_eda00.py` dan `run_nb00.py` sebagai file yang dibuat. **Keduanya tidak ada di disk** (diverifikasi `find . -name "_build_eda00*" -o -name "run_nb00*"` -> tidak ditemukan; `ls notebooks/scalping/` hanya berisi `eda_00_setup.ipynb`). Klaim tersebut dicoret sebagai salah (lihat SA-01).

## 3. Apa yang Dilakukan
- Reuse module: `load_config("data")`, `BrokerSchedule` (standard 7200 s / daylight 10800 s / 4 window DST), `wall_clock_series` + `utc_series`.
- Audit strata A/B/C langsung dari parquet M1 2023–2026 dengan assertion.
- Tabel sesi winter vs summer (primer IANA vs cross-tab UTC-tetap).
- Matriks kolom per timeframe (M1/M5/M15/M30/H1/H4/D1) + verifikasi 0 NaN kolom wajib.
- Preregistrasi placebo Q6 (offset acak + prior-HL digeser) + `SEED_PLACEBO = 42`.
- Kontrak 00 dicetak verbatim (lihat output cell pertama), termasuk errata E1–E3.

## 4. Klaim & Bukti
| Klaim | Status | Bukti |
|---|---|---|
| A+B+C = 1.347.847 bar | TERVERIKASI | cell idx 16: `PASS Strata A/B/C = 1.136.401 / 185.248 / 26.198` + `PASS A+B+C = TOTAL 1.347.847` |
| A = 1.136.401; B = 185.248 (H1-2023, 13,74%); C = 26.198 (2 window, 1,94%) | TERVERIKASI | cell idx 2, 16; angka muncul di output sel |
| 2025 = tahun referensi bersih (0 anomali) | TERVERIKASI | cell idx 16: `PASS 2025 = tahun referensi bersih` |
| 2 window C: 6.899 (5 hari) + 19.299 (14 hari) | TERVERIKASI | cell idx 16: `PASS Window C = 6.899 (5 hari) + 19.299 (14 hari)` |
| D1-2024 = 260 bucket, 0 bucket weekend | TERVERIKASI | cell idx 16: `PASS D1 2024 = 260 bucket + nol bucket weekend` |
| tzdata == 2026.5 | TERVERIKASI | cell idx 16 + sysinfo `tzdata : 2026.5`; CLI `importlib.metadata.version('tzdata')` = `2026.5` |
| Semua TF ada, kolom wajib, 0 NaN | TERVERIKASI | cell idx 16: `PASS Semua TF: file lengkap, kolom wajib, 0 NaN` |
| 4 zona IANA DST-aware + 4 blok cross-tab terkunci | TERVERIKASI | cell idx 16: `PASS 4 zona DST-aware + 4 blok cross-tab terkunci` |
| Protokol placebo + seed tetap | TERVERIKASI | cell idx 16: `PASS Protokol placebo Q6 + seed terkunci` |
| Kontrak 00 dicetak verbatim (termasuk errata E1–E3) | TERVERIKASI | execute_result idx 5 berisi teks penuh Kontrak 00 |
| Notebook dieksekusi top-to-bottom, exec_count 1..11 | TERVERIKASI | cell code urut 1..11, monotonically increasing |
| 0 error-output | TERVERIKASI | scan: `error_outputs = 0` |
| nbformat valid | TERVERIKASI | `nbformat.validate` mengembalikan list error kosong |
| venv kanonik: py 3.12.8 / pandas 2.2.3 / numpy 1.26.4 / matplotlib 3.10.9 / tzdata 2026.5 | TERVERIKASI | sysinfo cell + CLI `importlib.metadata` |

## 5. Self-Audit Adversarial
Checklist (dihasilkan, bukan diasumsusi):
- [x] Notebook dieksekusi top-to-bottom tanpa error (exec 1..11, 0 error-output).
- [x] Output cell tersimpan (semua cell code punya outputs).
- [x] Tidak ada dump data mentah (hanya agg/summary, bukan `df.head()` mentah).
- [x] Seed placebo tetap (`SEED_PLACEBO = 42`, tercetak).
- [x] Assertion strata (A+B+C) lulus (11/11 PASS termasuk strata).
- [x] Tidak ada look-ahead bias (semua `.shift(1)`; tidak ada forward-fill data).
- [x] Tidak ada data leakage (strata B/C eksplisit dipisahkan dari A; assertion `A ∩ B = ∅`, `A ∩ C = ∅`).
- [x] Stratifikasi H1-2023 benar (B via filter `year==2023`; 185.248 terkonfirmasi).
- [x] 2 window anomali dieksklusi dari A.
- [x] Semua angka ada bukti (lihat tabel).
- [x] Tidak ada klaim tanpa verifikasi.

**Temuan (yang salah):**

- **[SA-01] Laporan ini sendiri pernah memuat klaim file yang tidak ada.** Versi pertama §2 menyatakan `notebooks/scalping/_build_eda00.py` dan `run_nb00.py` dibuat. Verifikasi disk (`find`/`ls`) keduanya **tidak ada**; `notebooks/scalping/` hanya berisi `eda_00_setup.ipynb`. Penyebab: nama skrip ikut terbawa dari catatan sesi sebelumnya tanpa diverifikasi ulang ke disk (pelanggaran §20 anti-halusinasi, dan melanggar §0.6 "jangan andalkan memori AI, andalkan file"). Fix: §2 dikoreksi, kedua nama dihapus. Isi notebook dan angka hasil audit **tidak** berubah — keduanya diverifikasi ulang langsung dari `.ipynb` pada sesi ini.
- **[SA-02] (diverifikasi ulang, TANPA MASALAH) Soal `pyarrow`.** Versi pertama laporan ini sempat menandai entri `pyarrow` di `requirements.txt` sebagai "belum diverifikasi". Sudah dicek: `requirements.txt` baris 9 berisi `pyarrow==17.0.0`, dan `importlib.metadata.version('pyarrow')` di venv kanonik = `17.0.0` — **cocok**. Jadi catatan sesi sebelumnya (pyarrow sudah ter-pin) benar; tidak ada divergensi. TALLY: requirements.txt sinkron dengan venv kanonik.

**Yang Belum Diverifikasi (status asli, tidak diasumsusi):**
- Batas sesi secondary London close 16:00 vs 17:00 lokal — `PV`/BELUM DIVERIFIKASI di Kontrak 00.
- Granularitas level xx.50 — sensitivity, dikalibrasi EDA-02.
- Offset +2 windowanomali (Finex) — `BELUM TERVERIFIKASI`; tidak dipakai sesi Tokyo/London/NY (bukan blocker nb00).
- Angka sumber sekunder S5/S6 (London 43%, pip 66/59/51) — label sekunder, belum dikalibrasi data.
- Kalender libur NYSE/TSE — out of scope; dicatat sebagai missing-event.

## 6. Langkah Berikutnya
- **Langkah 3:** tulis `eda_01_returns.ipynb` (Q1 distribusi return M1/M5/M15 per strata) → STOP. **Menunggu konfirmasi user (GO).**
- Opsi cadangan (perlu persetujuan): commit nb00 sebagai artefak teraudit; siapkan skeleton `reports/eda/2026-10-06/`.

Tidak ada errata dependency yang tertunda: `requirements.txt` sudah sinkron dengan venv kanonik (lihat SA-02).

## 7. STOP — Tunggu Review User
