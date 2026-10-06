# Laporan Tahap 7 — Fix Deviasi nb04 (D6, D7, D12-BoJ) — LANGKAH 3

**Tanggal:** 2026-10-06
**Status:** SELESAI — **30/30 assertion PASS**, 0 error, VALID, gate hijau, **belum di-commit**
**Pilihan format laporan:** **FILE BARU** (`reports/eda/progress/laporan_tahap_7_swing_level_fix.md`),
bukan addendum di `laporan_tahap_6_swing_level.md` — dipilih agar jejak eksekusi per langkah
terpisah dari laporan tahap 6 yang sudah direview user.

**Rujukan:** `eda_review_deviations_v1.md` (D6/D7/D12), Rancangan EDA v3.1 §5 baris 66 (Swing)
dan §2 baris 33 (event marker), keputusan user 2026-10-06 (langkah 2 selesai) + jawaban batch
(fragmen spread byte-identical; D9 tidak disentuh).

---

## 1. File yang Diubah

| File | Perubahan | Bukti |
|---|---|---|
| `scripts/_build_eda04.py` | builder = sumber kebenaran: `SWING_MASKS`, sel D6 (frekuensi/hari), sel D7 (holding median), sel §2b BoJ, 10 assertion baru, ringkasan markdown | blob `a7e4a77…` |
| `notebooks/scalping/eda_04_swings_levels.ipynb` | hasil regenerate (21 sel: 10 kode, 11 markdown) | blob `1ad2ad1e…` → `7199de8a…` |

Tidak menyentuh `src/`, `configs/`, data, nb00–nb03, nb05, D9, audit kesesuaian, laporan_tahap_5.
Nb04 pra-step-3 dapat dipulihkan dari indeks: `git show :notebooks/scalping/eda_04_swings_levels.ipynb`
(blob `1ad2ad1e…`) — file itu sudah staged sejak langkah 1, jadi tidak ada risiko kehilangan.

## 2. Verdict vs Eksekusi (LANGKAH INI SAJA)

| # | Verdict | Status | Bukti |
|---|---|---|---|
| **D6** | INVALID | **FIXED** | Sel Q5 menambah `SWING_MASKS` + tabel `SWING_FREQ` (5 kombinasi) dan `per_hari` (825 hari berbar); assertion D6 (3 buah) **PASS**; jumlah swing identik dengan sebelumnya (20.169/20.314/12.787/13.070 → **tidak ada perubahan definisi**) |
| **D7** | INVALID | **FIXED** | `SWING_HOLD` = `np.diff(np.flatnonzero(mask))` per kombinasi (bar/p90/menit) + `HOLD_SESI`; assertion D7 **PASS**; dinyatakan eksplisit "bukan durasi posisi, bukan P&L" |
| **D12 (bagian nb04)** | PARTIAL | **FIXED** | Sel §2b: touch eksak (`low <= L <= high`, aturan Q6 yang sama) + eksposur band 10/25/50 pip + tabel per tahun + per sesi; 5 assertion D12 **PASS**; **tanpa** return pasca-event (aturan "bukan event-study" tertulis di markdown dan di dalam sel) |
| D1–D5 | — | **di luar langkah ini** (selesai di langkah 2) | — |
| D8, D11 | — | **di luar langkah ini** (selesai/dicatat di langkah 1) | — |
| D9, D10 | — | **BELUM** (D10 = langkah 4; D9 = langkah 5, tidak disentuh sesuai perintah) | — |

## 3. Angka Hasil Rerun (stratum A, M5, 227.568 bar)

**D6 — frekuensi swing per hari** (`825` hari broker berbar):

| kombinasi | n_swing | swing/hari | per 1000 bar |
|---|---|---|---|
| high_k3 | 20.169 | 24,447 | 88,628 |
| high_k5 | 12.787 | 15,499 | 56,190 |
| low_k3 | 20.314 | 24,623 | 89,266 |
| low_k5 | 13.070 | 15,842 | 57,433 |
| **gabungan** | **40.207** | **48,736** | **176,681** |

Sebaran per hari broker: mean 48,74 · std 4,18 · min 37 · p10 43 · median 49 · p90 54 · maks 61.

**D7 — waktu tahan median antar swing** (jarak antar indeks fraktal):

| kombinasi | n_jarak | median (bar) | p90 (bar) | median (menit) |
|---|---|---|---|---|
| high_k3 | 20.168 | 10 | 19 | 50 |
| high_k5 | 12.786 | 15 | 31 | 75 |
| low_k3 | 20.313 | 10 | 19 | 50 |
| low_k5 | 13.069 | 15 | 30 | 75 |
| gabungan | 40.206 | 5 | 10 | 25 |

Per sesi (definisi gabungan): London/NewYork/Tokyo/Sydney = **5 bar (25 menit)** di semua sesi —
keterbatasan yang dinyatakan (definisi gabungan didominasi pergantian high-low), bukan temuan sesi.

**D12 — eksposur zona BoJ** (deskriptif; setengah-lebar band dinyatakan 10/25/50 pip):

| level | touch eksak | % bar | hari touch | band 10 | band 25 | band 50 | tahun |
|---|---|---|---|---|---|---|---|
| 150,0 | 728 | 0,3199% | 53 | 3.532 | 8.474 | 16.376 | 2023,2024,2025 |
| 155,0 | 518 | 0,2276% | 51 | 2.235 | 5.770 | 11.527 | 2024,2025,2026 |
| 160,0 | 151 | 0,0664% | 20 | 1.242 | 3.587 | 8.206 | 2024,2026 |

Per tahun (touch / band-25): 150 → 44/2.502 (2023), 508/3.761 (2024), 176/2.211 (2025), 0/0 (2026);
155 → 0/0, 179/2.014, 186/2.383, 153/1.373; 160 → 0/0, 7/199, 0/0, 144/3.388.
Per sesi (touch 150/155/160): London 282/228/78 · NewYork 166/80/27 · Tokyo 241/197/21 · Sydney 39/13/25 · Off 0/0/0.

**Q6 tetap tidak bergeser** (bukti bahwa penambahan tidak menyentuh analisis lama):
hit-rate nyata 0,4694 / 0,4892 / 0,4799 / 0,4905 vs placebo 0,4989–0,5050; jumlah event nyata
identik dengan eksekusi sebelumnya (11.896 / 13.213 / 10.477 / 12.656).

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| D6 dihitung pada definisi fraktal yang sama dengan tabel Q5 | TERVERIFIKASI | `SWING_MASKS` membaca kolom `swing_*` yang sama; n_swing tabel D6 == tabel Q5 |
| D6 memakai hari broker (bukan hari UTC) | TERVERIFIKASI | `groupby("broker_day")`; 825 hari berbar; konsisten Lampiran A1 (level-hari = tanggal broker) |
| D7 = jarak antar indeks fraktal | TERVERIFIKASI | `np.diff(np.flatnonzero(mask))`; median k=3 (10) < k=5 (15) sesuai lebar jendela `k` |
| D12 memakai aturan touch yang sama dengan Q6 | TERVERIFIKASI | `low <= L <= high` di kedua sel; 728/518/151 touch |
| D12 bukan event-study | TERVERIFIKASI | tidak ada kolom return/reaksi pasca-event; assertion "bukan event-study" PASS; teks aturan tercetak |
| Band naik monoton dengan lebar (sanitas) | TERVERIFIKASI | assertion: `band10 >= touch`, `band25 >= band10`, `band50 >= band25` PASS di 3 level |
| nb04: 30/30 PASS, 0 error, urut, VALID | TERVERIFIKASI | `RINGKASAN: 30/30 assertion PASS`, error outputs 0, exec_count [1..10], `nbformat.validate` |
| Gate hijau setelah rerun | TERVERIFIKASI | §5 di bawah (exit 0 semua) |

## 5. Gate (output asli, dijalankan setelah edit terakhir)

```
== ruff check ==            All checks passed!                              rc=0
== ruff format --check ==   29 files already formatted                     rc=0
== pytest ==                157 passed in 1.32s                            rc=0
== validate_data ==         2023: 0 error, 2 peringatan -> LOLOS
                            2024: 0 error, 2 -> 2025: 0 error, 1 -> 2026: 0 error, 1   rc=0
== check_foreign_chars ==   OK: 68 file discan, tidak ada karakter asing.   rc=0
```
Riwayat build: pass-1 `nbconvert exit=0` (30/30, sebelum ringkasan markdown diperbarui) →
pass-2 `nbconvert exit=0` (ringkasan berisi angka hasil eksekusi). Tidak ada build merah.

## 6. Self-Audit 3× Adversarial

**Putaran 1 — Correctness**
- Angka D6/D7 dihitung dari mask yang **sudah diverifikasi** di tabel Q5: `n_swing` D6 == `n_swing`
  Q5 untuk keempat kombinasi (20.169 / 12.787 / 20.314 / 13.070) → tidak ada definisi kedua.
- Sanitas matematis D7: median k=3 (10 bar) < median k=5 (15 bar); p90 > median di semua kombinasi;
  `n_jarak` = `n_swing` − 1 (20.169 → 20.168 dst.) → indeks & diff konsisten.
- D12: total touch 728+518+151 = 1.397 bar dari 227.568 (0,61%) → tidak ada duplikasi bar ganda di
  satu level; band memuat touch dan naik monoton (assertion) → definisi band konsisten.
- Notebook tereksekusi: 10/10 sel kode beroutput, `execution_count` 1..10 berurutan, 0 error,
  `nbformat` VALID.

**Putaran 2 — Bias & Asumsi**
- **Risiko "D7 menyesatkan" saya tangkap sendiri dan laporkan:** holding gabungan 5 bar bukan
  "durasi swing" tetapi jarak antar tanda fraktal berurutan; itu sebabnya tabel per kombinasi
  (10/15 bar) juga dilaporkan. Dua definisi berdampingan, tidak ada yang disembunyikan.
- **Q6 diuji tidak bergeser** (angka identik) — bukti bahwa sel baru tidak diam-diam mengubah
  event/hit-rate lama.
- **Sebaran band BoJ (10/25/50) adalah pilihan saya** karena user tidak menetapkannya; dinyatakan
  sebagai pilihan di markdown notebook + laporan ini (mudah diubah kalau user mau lebar lain).
- Tidak ada event-study terselundup: tidak ada return pasca-event, tidak ada p-value, tidak ada
  klaim "BoJ di level X berdampak Y".

**Putaran 3 — Meta-check**
- Urutan perintah dipatuhi: langkah 3 tuntas (rerun + gate + laporan) sebelum langkah 4; D9 tidak
  disentuh; fragmen spread (nb02) belum disentuh pada langkah ini.
- Tidak ada commit/amend; nb04 kini `AM` (staged versi lama + worktree baru) menunggu Commit A.
- Asumsi yang saya buat dan **dinyatakan**: hari broker sebagai unit D6 (konsisten R3/A1);
  `BAR_MINUTES = 5` (protokol Q5 terkunci M5).

## 7. Yang Belum Diverifikasi

- **Kebenaran eksternal D6/D7**: tidak ada pustaka pembanding untuk deteksi fraktal; verifikasi
  hanya lewat konsistensi internal (n_swing vs Q5, n_jarak = n−1) dan sanitas median k=3 vs k=5.
- **Interpretasi "holding"** bisa berbeda bila Architect memaksudkan half-cycle high→low
  (bukan jarak sejenis); saya laporkan dua definisi sekaligus agar keputusan itu tidak tersembunyi.
- **Zona BoJ**: lebar band 10/25/50 pip adalah pilihan deskriptif, bukan angka kontrak; sentuhan
  terkait berita BoJ ikut terhitung (kalender berita di luar scope).
- **Rujukan hilir**: nb05 belum boleh mengonsumsi nb04 sebelum Commit A mendarat (aturan user).
- Gate dijalankan pada repo yang sama dengan perubahan langkah 2 yang belum di-commit — pytest
  157 passed tetap berlaku untuk `tests/` yang tidak disentuh.

## 8. STOP — Tunggu Review User

Langkah 3 selesai. Berikutnya (masih dalam perintah yang sama): **langkah 4 — nb02 (D10 + flag
Tokyo fix/NYSE)**, lalu laporan `laporan_tahap_8_volatility_fix.md`.
