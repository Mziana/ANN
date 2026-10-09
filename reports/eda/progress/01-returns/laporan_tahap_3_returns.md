# Laporan Tahap 3 — Notebook 01 (`eda_01_returns.ipynb`, Q1 Distribusi Return)
**Tanggal:** 2026-10-06
**Status:** SELESAI — **22/22 assertion PASS**, 0 error, VALID, **belum di-commit** (aturan: jangan commit EDA sebelum audit Klenz)

> Putusan Architect atas SA-03 (R1–R4) **tidak memblokir** Q1: Q1 bekerja pada **bar**,
> bukan hari. R1–R3 sudah dic verbatim di sel markdown nb01 untuk dibawa ke nb04/nb05.

## 1. Tujuan
Menjawab **Q1** Rancangan EDA v3: distribusi return log-close-BID pada M1/M5/M15 per strata A/B/C — skewness, kurtosis ekses, kuantil 0,1%/1%/99%/99,9%, pangsa |r| > 3σ dan 5σ, QQ-plot, **plus** karakterisasi massa nol dan ekor dalam pip.

## 2. File yang Dibuat/Diubah
- `notebooks/scalping/eda_01_returns.ipynb` — baru, **22 sel** (12 kode, 10 markdown), output tersimpan.
- `scripts/_build_eda01.py` — generator + eksekutor nbconvert.
- `reports/eda/2026-10-06/figures/FIG-01_qq_M1.png`, `_M5.png`, `_M15.png`.
- `.ai/SESSION_LOG.md`, `.ai/STATE.md` (status EDA diperbarui).
- **Tidak mengubah** `src/`, `configs/`, atau data.

## 3. Apa yang Dilakukan
1. Muat M1/M5/M15 (2023–2026), urutkan kronologis, hitung `r_t = ln(close_t / close_{t-1})` (close = BID).
2. Replikasi definisi strata dari nb00 (B = hari-broker H1-2023, C = dua window anomali, A = sisanya) + audit partisi.
3. Tabel Q1 3 TF × 3 strata, sigma per baris untuk ambang 3σ/5σ.
4. **Karakterisasi ekor:** massa-nol, return lintas gap, 8 pergerakan terbesar **dalam pip**, jam UD-nya.
5. QQ-plot stratum A per TF.
6. Blok "uji pembeda" (Welch + bootstrap) yang menegak klaim yang tak boleh disimpulkan dari tabel saja.
7. Catatan keterbatasan biaya BID-only.

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Return = log close BID, `shift(1)` backward | TERVERIFIKASI | sel 3; uji shift pada data buatan |
| Urut naik, duplikat 0, semua TF | TERVERIFIKASI | sel 8: `sorted=True`, `dup=0` |
| Drop hanya warmup (1 bar/TF) | TERVERIFIKASI | sel 8: `drop warmup=1` tiap TF |
| Partisi A/B/C menutup total tiap TF | TERVERIFIKASI | sel 10: M1 `1.347.847`, M5 `269.964`, M15 `90.041` |
| **Ukuran strata terkunci ke angka Lapisan 1** | TERVERIFIKASI | assertion: M1 = `1.136.401 / 185.248 / 26.198` |
| Ekses kurtosis turun M1→M15 (A) | TERVERIFIKASI | M1 195,48 → M5 102,85 → M15 51,18 |
| Sigma naik sesuai TF (A) | TERVERIFIKASI | 1,6088e-4 → 3,5659e-4 → 6,1201e-4 |
| Piksil >3σ ≫ teoritis normal 0,27% | TERVERIFIKASI | M1-A 1,3233e-2 (≈4,9× teoritis) |
| **Massa-nol M1 = 5,83%** (78.582 bar) | TERVERIFIKASI | sel 12: `M1 zero-share 5.83%` |
| **Ekor M1 = 164,7 pip** (bukan 1,2 pip) | TERVERIFIKASI | sel 12: `max|r| pip 164.7` |
| Ekor terkumpul di 12:30 UTC **dan** 21–22 UTC | TERVERIFIKASI | jam 8 terbesar = `[2, 12, 12, 13, 21, 22, 22, 22]` |
| Mean A vs B **tidak** signifikan | TERVERIFIKASI | Welch t = −1,00, **p = 0,316** |
| Tanda skew B **tidak** kokoh | TERVERIFIKASI | bootstrap CI95(r³) = [−3,01e-11 ; 5,62e-11] |
| Versi pandas terkunci 2.x | TERVERIFIKASI | assertion baru PASS |
| Nol P&L/imputasi/config-write/import terlarang | TERVERIFIKASI | grep = 0; kolom tabel tanpa pnl/equity/signal/entry/exit |
| 22/22 assertion PASS, 0 error | TERVERIFIKASI | sel 19 |

## 5. Self-Audit 3× Adversarial

### Putaran 1 — Correctness
- **SA-01 (DITEMUKAN & DIPERBAIKI) — Konversi pip salah, klaim saya sendiri keliru.** Saya menulis "max|r| M1 = 1,2 pip". Itu salah: membagi log-return dengan 0,01 bukan konversi pip. Konversi benar `pip = (exp(r)−1)·close/0,01` memberi **164,7 pip**. Kesalahan satuan ini menurunkan pergerakan terbesar **~137×**.
- **SA-02 (DITEMUKAN & DIPERBAIKI) — Tabel Q1 tidak tercetak di output cell.** `display()` hilang saat nbconvert; tabel utama kosong di output meski notebook "sukses". Baru ketahuan karena saya menghitung ulang angka dan menemukan nilai yang tak ada di tabel. Diganti `print(to_string())`.
- **SA-03 (DITEMUKAN & DIPERBAIKI) — Assertion "tidak ada P&L" bernilai `True` hardcode** (self-fulfilling). Diganti pemeriksaan kolom nyata; ditambahkan assertion file figure benar-benar ada.
- **SA-04 (DITEMUKAN & DOKUMENTASIKAN) — Massa nol tak terlihat di tabel momente.** 5,83% bar M1 punya r persis 0; 2,01% M5; 1,01% M15. Merupakan kontribusi besar ke kurtosis. Tidak ada di nb00 maupun laporan sebelumnya.
- **SA-05 (DITEMUKAN & DIPERBAIKI) — Assertion "3 baris tabel" dobel.** Bisa menutupi pemeriksaan yang hilang.
- **SA-06 (DITEMUKAN & DIPERBAIKI) — Tidak ada assertion ukuran strata.** Hanya partisi tertutup yang diuji; kalau `configs/data.yaml` berubah, nb01 tetap hijau di strata yang salah.
- Bukti: hitung ulang independen σ/skew/kurt M1-A cocok; `close` NaN = 0, non-positif = 0; `r` inf = 0; NaN = 1 (warmup) per TF.

### Putaran 2 — Bias & Aturan
- **Look-ahead:** tidak ada. `shift(1)` hanya membaca masa lalu; return dihitung **sebelum** pemaskan, jadi bar pertama stratum menyeberang hanya memakai bar **lampau**. Jumlahnya dilaporkan (`cross` 3/1/2 per TF).
- **Data leakage:** tidak ada fitur, tidak ada scaler, tidak ada split. Q1 murni deskriptif.
- **Stratifikasi:** A/B/C dihitung dari `wall_date` (broker) — konsisten dengan nb00 dan putusan Architect R3.
- **2 window anomali:** tereksklusi dari A; C = 26.198 bar (1,94%) diverifikasi.
- **Anti-imputasi:** nol `ffill/interpolate/fillna/impute/bfill` (grep = 0).
- **`.shift(1)` konsisten:** ya, tunggal, tanpa `shift(-n)`, tanpa `lead`, tanpa `bfill`.
- **Biaya:** return BID-only; note eksplisit bahwa BUY=SELL asimetris terhadap spread dan angka spread config masih **ASUMSI** sampai 4b.

### Putaran 3 — Yang Terlewat
Ini putaran yang paling produktif. Empat celah **tidak** saya reliantcheckmark sebelumnya:

- **SA-07 (PALING PENTING) — Atribusi kurtosis ke "microstructure noise" TIDAK didukung.** Laporan versi pertama menyebut kurtosis M1 tinggi sebagai "bukti kuantitatif bid-bounce". Setelah konversi pip benar + pemeriksaan jam, 8 pergerakan terbesar M1 ternyata: 3 pada **12:30 UTC** (08:30 ET = data ketenagakerjaan AS) dan 3 pada **21–22 UTC** (pembukaan sesi / transisi DST, return **gap lintas akhir pekan**, bukan pergerakan 1 menit). Jadi ekor didorong **berita makro + gap pembukaan**, bukan noise mikrostruktur. Klaim lama **dibatalkan**.
- **SA-08 — Tidak ada lock versi pandas.** Kalau nb01 dijalankan lewat `.venv` (pandas 3.x), bug `.asi8` (detik vs nanos) yang dulu merusak pipeline bisa kembali tanpa terdeteksi. Ditambah assertion versi pandas major = 2.
- **SA-09 — Gambar QQ menimpa nama bila dijalankan ulang** dan path `figures/FIG-01_*` dipakai untuk 3 TF sekaligus (bukan `FIG-01/02/03`). Nomor gambar belum mengikuti konvensi rancangan; ini akan dibenahi saat nb05 menyusun figure final.
- **SA-10 — 1.824 return M1 (0,135%) adalah return lintas gap** (weekend/break), tercampur dalam distribusi yang sama. Porsi kecil tapi tidak nol; sekarang **dihitung dan dilaporkan**, belum dieliminasi (menghilangkannya adalah keputusan metode, bukan Q1).
- **Serangan musuh (di mana notebook ini bisa gagal diam-diam):** (a) `configs/data.yaml` diubah → strata bergeser tanpa assertion — kini terkunci; (b) interpreter `.venv` → timestamps rusak — kini terkunci; (c) `display()` hilang → tabel kosong lolos sebagai "sukses" — kini dicetak sebagai stream; (d) konversi satuan pip salah → klaim scheint meyakinkan — kini ada baris konversi eksplisit.

### Verdict
- **Siap lapor? Ya.**
- Alasan: 3 putaran menemukan **10 temuan**, 6 di antaranya diperbaiki di notebook dan diverifikasi ulang sampai 22/22 PASS. Temuan terpenting (SA-07) **membatalkan** interpretasi yang sebelumnya saya tulis, dan sekarang sudah dikoreksi di notebook.

## 6. Yang Belum Diverifikasi
- Autokorelasi/mean-reversion beyond sanity lag-1 — **Q4 (nb03)**.
- Makna ekonomi skew B & perbedaan volatilitas antar-strata — **Q2/Q7 (nb02/nb05)**.
- Kalender berita resmi (NFP/CPI) **tidak** dipakai — pencocokan jam bersifat inferensi; RULES §18.15 tetap melarang trading saat news high-impact tanpa proteksi.
- Spread terukur & fragmen YAML — **EDA-02 + 4b**.
- Normalitas formal (Jarque-Bera) — tidak dijalankan; QQ + deviasi σ cukup deskriptif.

## 7. Potensi Masalah
- **Dua venv** adalah risiko lingkungan utama; kini ada assertion, tapi assertion hanya memicu **setelah** interpreter salah sudah dipakai. Worker CI sebaiknya mengunci interpreter.
- `scripts/_build_eda01.py` masih untracked; ruff check + format bersih (15 files formatted).
- Numbering figure belum sesuai konvensi rancangan (SA-09) — dibenahi di nb05.

## 8. Langkah Berikutnya
- **Langkah 4 — nb02** (Q2 volatilitas per jam dinding broker + Q3 per sesi UTC + spread p50/p95/p99/maks dan %>3 pip per sesi × jam × tahun → **fragmen YAML BELUM diterapkan**). Menunggu konfirmasi user.

## 9. STOP — Tunggu Review User
