# Laporan Tahap 0 — Reuse-Check (§16 AGENTS.md)
**Tanggal:** 2026-10-06 (laporan ditulis ulang pada sesi yang sama; verifikasi ulang 2026-10-06 10:11)
**Status:** SELESAI — seluruh dependensi reuse tersedia & berfungsi; **tidak ada file baru di `src/`**

> Catatan metodologi: laporan ini **diverifikasi ulang langsung ke disk/venv**, bukan menyalin
> `SESSION_LOG.md`. Klaim yang tidak saya verifikasi ulang ditandai eksplisit sebagai
> "tidak diulang" — lihat §6.

## 1. Tujuan
Sebelum menulis notebook EDA mana pun, buktikan setiap dependensi reuse yang diminta Rancangan v3 benar-benar ada dan berfungsi: `load_config`, `BrokerSchedule` + `wall_clock_series` + `utc_series`, kelengkapan parquet per timeframe, `tzdata==2026.5` untuk `zoneinfo`, dan konfirmasi `src/` tidak berubah (§16 butir 4-5: tulis Laporan Reuse, tunggu konfirmasi).

## 2. File yang Dibuat/Diubah
- **Tidak ada.** Langkah 0 murni inventaris + verifikasi; tidak ada file yang ditulis, tidak ada
  perubahan pada `src/`, `configs/`, maupun data.
- File deliverable: `reports/eda/progress/laporan_tahap_0_reuse_check.md` (laporan ini).

## 3. Apa yang Dilakukan
1. Inventaris simbol reuse di `src/utils/config.py` dan `src/data/broker_time.py`.
2. Hitung baris setiap parquet per timeframe + rincian D1 per tahun.
3. Verifikasi format kolom `time` dan `zoneinfo` pada 4 zona IANA.
4. Cek `git ls-files src/` untuk memastikan tidak ada file baru.
5. Investigasi anomali "weekend" pada bucket D1 (lihat SA-03).

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| `load_config` tersedia di `src/utils/config.py` | TERVERIFIKASI | file tracked di `git ls-files src/`; dipakai `src.data.validate_data` yang jalan exit 0 |
| `BrokerSchedule` + `wall_clock_series` + `utc_series` tersedia | TERVERIFIKASI | `broker_time.py`: `class BrokerSchedule` baris 45, `def offset_seconds` baris 86, `def wall_clock_series` baris 166, `def utc_series` baris 178 |
| Offset broker seasonal 2 h / 3 h | TERVERIFIKASI | `configs/data.yaml`: `broker_utc_offset_hours: standard: 2` / `daylight: 3`; docstring `broker_time.py:49-50` menyebut 7200/10800 |
| Jadwal DST = 4 window | TERVERIFIKASI | `configs/data.yaml` `broker_dst_schedule`: 2023-03-12..11-05, 2024-03-10..11-03, 2025-03-09..11-02, 2026-03-08..11-01 |
| M1 = 1.347.847 bar | TERVERIFIKASI | 4 file: 362.693 / 358.331 / 356.977 / 269.846, total **1.347.847** (dihitung ulang dari parquet) |
| M5 = 269.964 · M15 = 90.041 · M30 = 45.024 · H1 = 22.513 · H4 = 5.844 · D1 = 974 | TERVERIFIKASI | inventaris 4 file per TF (dihitung ulang). M30/H4 tidak dipakai EDA |
| D1 per tahun = 259 / 260 / 259 / 196 (total 974) | TERVERIFIKASI | dibaca per file: `usdjpy_d1_2023..2026.parquet` |
| D1-2024 = 260 bucket | TERVERIFIKASI | `len(df) = 260` |
| `time` disimpan sebagai string ISO-8601 UTC (bukan timestamp parquet) | TERVERIFIKASI | nilai contoh `'2024-01-01T22:00:00+0000'` |
| `tzdata==2026.5` terpasang | TERVERIFIKASI | `importlib.metadata.version('tzdata')` = `2026.5` di venv kanonik |
| Tidak ada file baru di `src/` | TERVERIFIKASI | `git ls-files src/` → **9 file tracked**, sama seperti Lapisan 1; tidak ada entri baru |

## 5. Self-Audit Adversarial

### Checklist
- [x] Reuse registry lengkap (semua simbol dari rancangan v3 dicek keberadaannya).
- [x] Tidak ada file baru dibuat di `src/`.
- [x] Angka dihitung ulang dari parquet, bukan disalin dari catatan sesi sebelumnya.
- [x] Tidak ada klaim tanpa bukti baris-per-baris.

### Temuan

- **[SA-03] — STATUS: RESOLVED (2026-10-06). Bucket D1 bergeser satu hari kalender antara
  label UTC dan hari broker.**
  **Putusan Architect (Spark):** R1 "hari-UTC" = label kalender murni dengan offset struktural
  −1 yang didokumentasikan, DILARANG menggeser data agar "sepakat"; R2 syarat "sepakat"
  ditafsir ulang menjadi **sepakat-dengan-kesadaran-geser** (hanya divergensi MELEBIHI geseran
  struktural yang menjadi temuan); R3 seluruh pekerjaan level-hari (Q6 prior-day primer + Q7
  regime) dikunci pada **tanggal-broker**, hari-UTC sekunder saja; R4 tanpa redesain, tanpa
  penundaan, aturan dicatat di nb04/nb05 + laporan final. Keputusan ini juga dicantumkan di nb01 (sel markdown).

  Bukti asal (tetap berlaku sebagai fakta): batas bucket D1 = tengah malam broker
  (21:00 UTC summer / 22:00 UTC winter), sehingga baris `'2024-01-01T22:00:00+0000'`
  sebenarnya hari **Senin** 2 Januari.

  | Frame pengukuran | Distribusi dayofweek | Jumlah "weekend" |
  |---|---|---|
  | Tanggal **broker** (wall clock) | Sen 52 · Sel 53 · Rab 51 · Kam 52 · Jum 52 | **0** |
  | Label **UTC** | Sen 53 · Sel 51 · Rab 52 · Kam 52 · **Min 52** | **52** |

  Konsekuensi: pengukuran mana pun yang memakai label UTC harus menambahkan offset struktural −1 secara
  eksplisit; ketidaksepakatan sebesar 1 hari **bukan** kegagalan. Temuan ini **ditutup** dan tidak
  lagi menjadi blokir nb01–nb05.

- **[SA-01] Angka "460.194 bar" pada audit equivalence tidak diulang.** `SESSION_LOG.md` menyebut
  `wall_clock_series`/`utc_series` identik dengan kolom `time` untuk M1/M5/M15/H1/D1 2024
  (460.194 bar). Angka itu **tidak saya hitung ulang** pada laporan ini. Yang terverifikasi: nb00
  audit `PASS utc_series == parse(time) penuh M1 2025`, jadi ekuivalensi minimal terkonfirmasi untuk M1
  2025. Status angka 460.194: **tidak diulang** (lihat §6).

- **[SA-02] "157 test hijau di kedua env" hanya terverifikasi di venv kanonik.** `.venv/` (env bantu
  uv) **tidak** saya uji ulang di sesi ini; klaim itu diteruskan dari catatan sesi sebelumnya.

## 6. Yang Belum Diverifikasi
- Angka 460.194 (equivalence lintas TF 2024) — **tidak diulang**; ekuivalensi terkonfirmasi untuk
  M1 2025 lewat audit nb00.
- `jupyter` / `ipykernel` terpasang di venv kanonik — **tidak diulang** pada sesi ini.
- `.venv/` (env bantu uv, Python 3.12.13, pandas 3.0.6) — **tidak diuji ulang**; status "dibiarkan,
  bukan kanonik" dari keputusan user sebelumnya.
- Zona IANA per Musim (Tokyo/London/NY/Sydney pada 4 tanggal uji) — **tidak diulang**; versi
  `tzdata` terverifikasi dan audit nb00 mengunci 4 zona.

## 7. Potensi Masalah
- SA-03 **sudah RESOLVED** (putusan Architect R1–R4). Tidak lagi jadi blokir nb01–nb05;
  aturan R1–R3 sudah dicantumkan di nb01 dan akan dipakai di nb04/nb05.
- Tidak ada blocking issue untuk Langkah 1/2/3 dari reuse-check ini.

## 8. Langkah Berikutnya
- Laporan ini menutup **Langkah 0**. Langkah 1 (pin `tzdata`) sudah dikerjakan & ter-commit
  (`9a60995`) — lihat `laporan_tahap_1_pin_deps.md`.
- Langkah 2 (notebook 00) sudah selesai — lihat `laporan_tahap_2_nb00_setup.md`.

## 9. STOP — Tunggu Review User
