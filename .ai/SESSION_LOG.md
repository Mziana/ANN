# SESSION_LOG.md â€” Log Sesi

## Sesi 2026-10-05 â€” Setup Fondasi

**Fokus:** Struktur folder + state files.

**Selesai:**
- Checkpoint 01: Struktur folder
- Checkpoint 05: State files

**Belum:**
- Checkpoint 06-09d
- Setup environment
- Git init

**Catatan:**
- User pakai Freebuff + Hermes + DeepSeek V4.
- Proyek di D:\ANN.
- Metode strategi belum dipilih (tunggu EDA).

**Langkah berikutnya:**
- Jalankan Checkpoint 06.

---

## Sesi 2026-10-05 (kedua) — Onboarding AI Baru + Phase A

**Fokus:** Onboarding AI baru (Prompt 0 / AGENTS.md §24) + koreksi state files.

**Kemajuan:**
- Onboarding 6 fase selesai: baca aturan, baca state, inventarisasi, laporan.
- Laporan onboarding diterima user.
- Empiris: verifikasi broker via MT5 API langsung.

**Temuan terverifikasi (empiris, bukan asumsi):**

| Temuan | Bukti |
|---|---|
| `src/` kosong (0 baris logika) | hanya `__init__.py` 0 byte |
| Checkpoint 06-09d **sudah** dijalankan | output-nya ada di working tree |
| `git init` **sudah** | 2 commit, pre-commit terpasang |
| Environment **sudah** siap | venv 3.12.8, 134 paket |
| Simbol = `USDJPY`, bukan `USDJPYm` | `symbols_get()` 82 simbol |
| **Timezone broker = UTC+3** | now UTC 02:48 vs last bar 05:48 |
| Spread live = 0,8 pip | tick 157.851 / 157.859 |
| Data 3,75 tahun tersedia | 1.348.135 bar M1 |
| `trade_allowed = False` | akun belum login trading |

**Keputusan user:**
- M1 dulu, 1 TF, verifikasi, baru expand.
- Simpan CSV per tahun: `data/raw/M1/usdjpy_m1_<year>.csv`.
- Update state files = in scope.
- Broker UTC+3 confirmed -> update `configs/data.yaml`.

**Selesai sesi ini:**
- TASK 1: state files diupdate ke kondisi faktual.
- TASK 2: `broker_timezone` -> `Etc/GMT-3`.

**Temuan TASK 2 (empiris):**
- Offset saat ini **+3.00 jam**, dua pengukuran independen (tick time & bar time).
- **Offset HISTORIS tidak terverifikasi.** Pola gap harian tidak cocok dengan
  offset tetap: 2023-01 tanpa daily break sama sekali, 2026-03 ada gap di jam
  server 0 **dan** 1. Browse web tidak menemukan info Finex-spesifik.
- Konsekuensi: `fetch_data.py` WAJIB menyimpan timestamp broker mentah
  bersama timestamp UTC, supaya konversi bisa diaudit ulang.

**Belum:**
- TASK 4: docstring Google Style, `.gitattributes`, Black dihapus, line ending.

**Catatan TASK 4:**
- `.gitattributes` dibuat: `* text=auto eol=lf`, `*.ps1`/`*.bat` crlf, biner binary.
- 22 file teks dinormalisasi CRLF -> LF; 3 `.ps1` -> CRLF penuh.
- Black dihapus (pre-commit + pyproject). Hanya ruff + ruff-format.
- Gate hijau: `ruff check` "All checks passed", `ruff format --check`
  "4 files already formatted".
- Docstring ditambahkan ke 4 fungsi `verify_claims.py` + `main()` di
  `check_state.py`. Docstring ditulis bahasa Inggris sesuai RULES.md §4.
- Catatan: `verify_claims.py` sengaja pakai `print()`, dicatat di module
  docstring karena output konsol justru produknya (RULES.md §9).
- hati-HATI: `git ls-files -z | xargs -0 grep -lU $'\r$'` memberi hasil
  PALSU (meng melaporkan semua file CRLF). Verified pakai hitung byte langsung.
- TASK 5: `docs/PROJECT_MAP.md` dibuat (181 baris). **PHASE A SELESAI.**

**Percobaan commit pertama DITOLAK pre-commit — 2 hook jadi bug:**
1. `mixed-line-ending --fix=lf` **berbalik mengubah** 3 `.ps1` dari CRLF ke LF,
   menabrak `*.ps1 text eol=crlf` di `.gitattributes`. Akan terulang tiap commit.
   -> Hook dihapus. Satu sumber kebenaran: `.gitattributes`.
2. `pytest-quick` gagal exit 5 (no tests collected) karena `tests/` kosong.
   -> Dibuat `scripts/run_tests.py`, cross-platform tanpa bash syntax.
   Entry hook: `python scripts/run_tests.py`.
3. Verifikasi `run_tests.py` tidak menutupi kegagalan nyata: test sengaja gagal
   -> exit 1 (tetap memblokir); test lulus -> exit 0; folder kosong -> exit 0.
4. `pre-commit run --all-files` -> 11/11 Passed, exit 0.
5. `.ps1` dipulihkan ke CRLF penuh; artefak `__pycache__`/`pytest_cache` dihapus.
6. **BELUM DI-COMMIT** atas permintaan user (mau review dulu).

**Catatan TASK 5:**
- `docs/` tadinya kosong; AGENTS.md §14 dan §24 sudah merujuk file ini,
  jadi membuatnya justified, bukan file asal.
- Semua klaim di PROJECT_MAP diverifikasi ulang terhadap kenyataan:
  jumlah `.py` di `src/` (1), `tests/` kosong, 2 script Python,
  3 PowerShell, 7 TF, 134 paket, venv 3.12.8.
- **ANGKA SALAH YANG KETEMU:** tulis "× 8 TF", padahal `configs/data.yaml`
  dan `data/raw/` sama-sama punya **7** TF (M1, M5, M15, M30, H1, H4, D1).
  Dikoreksi ke 7, lalu diverifikasi ulang.
- Kesalahan bahasa lain (`regionallyVerify`, `Description`) dikoreksi
  sebelum file ditutup.
- Phase B: fetch data M1.

**Catatan:**
- File `.ai/*.md` semula CRLF + BOM; STATE/TASKS/PROGRESS/SESSION_LOG
  dinormalisasi ke LF (RULES.md §1 + pre-commit `mixed-line-ending --fix=lf`).
- Dua karakter asing sempat nyasar saat menulis (Mandarin + typo "d alluded"),
  keduanya sudah dikoreksi sebelum file ditutup.
- Script sekali pakai `scripts/_tmp_dst_check.py` dibuat untuk uji DST lalu dihapus.

**Temuan TASK 3:**
- 26 file ber-BOM dihapus + 1 `.bak` = 27 file. Verifikasi: sha256 isi
  identik sebelum/sesudah, delta ukuran tepat 3 byte per file.
- Setelah dihapus, `ast.parse` dengan `encoding='utf-8'` polos berhasil untuk
  semua `.py` (sebelumnya `check_state.py` & `verify_claims.py` GAGAL).
- **BARU:** `black --check` & `ruff format --diff` GAGAL di 2 file karena
  100% CRLF di working copy. Penyebab: `core.autocrlf=true` tanpa
  `.gitattributes`, jadi autocrlf-assessment-runtime berbalik dengan hook
  `mixed-line-ending --fix=lf` dan kedua formatter.
- Catatan: pre-commit menjalankan `black` DAN `ruff-format` di file yang sama
  — dua formatter bisa saling bertabrakan.

**Langkah berikutnya:**
- **Phase B**: `src/data/fetch_data.py` + `__init__.py` + test.

---

## Fase B — fetch_data.py (2026-10-05)

**Dibuat (5 file):**
- `src/data/__init__.py`, `src/utils/__init__.py`
- `src/utils/config.py` (loader YAML, sesuai RULES §10 yang belum pernah ada)
- `src/data/fetch_data.py` (275 baris; fungsi terpanjang `main` 41 baris)
- `tests/test_fetch_data.py` (22 test, tanpa API live)

**Dua jebakan yang ditangani:**
1. `spread` dari MT5 bersatuan POINT (0.001), bukan PIP (0.01).
   Disimpan dua-duanya: `spread_points` + `spread_pips`.
2. Timestamp MT5 = jam broker. `time` = UTC, `broker_time_raw` = epoch asli.

**Bug yang ditemukan test (bukan saya):**
- `float(Series)` di `spread_points_to_pips` melempar TypeError. Diubah ke
  aritmetika yang jalan untuk skalar maupun Series.
- Assertion offset saya salah metode: `fromtimestamp(..., tz).timestamp()`
  mengembalikan epoch yang SAMA (konversi instant harus idemtif), jadi offset
  hanya terlihat di jam dinding broker vs UTC, bukan di epoch.

**Test 1 bulan:**
- Rentang `2026-10-01 s/d 10-05` menghasilkan 2.754 bar dan **tidak bisa
  membuktikan gap akhir pekan**: range berakhir di tengah akhir pekan, jadi
  tidak ada bar sesudah gap untuk dibandingkan.
- Diperpanjang ke `s/d 10-06` → 3.134 bar, **7/7 verifikasi LOLOS**,
  gap akhir pekan 2.944 menit (~49 jam) terlihat.
- Spread terukur: median 6 point (0,6 pip), maks 39 point (3,9 pip).
- Ambang bar saya perbaiki dari "~4.320" menjadi "3.000-4.500"; hasil aktual
  3.134 karena range mulai 01:01 UTC (bukan tengah malam).

**Full fetch BELUM dijalankan** — menunggu approval user.

## validate_data.py + config spread

**Config:** ditambah `spread.by_year` (2023=3,0; 2024-2026=1,5).
Dasar: p99 spread 2023 = 8,5 pip vs 1,2-1,7 tahun lain. `by_session`,
`by_news`, `pip_size` dipertahankan.

**`src/data/validate_data.py`** (445 baris, fungsi terpanjang 39):
delapan check murni (bar/hari, duplikat, monoton, OHLC, gap, spread,
jam break, anomali dikenal) + laporan Markdown ke `reports/`.
33 test di `tests/test_validate_data.py`.

**Dua bug yang tertangkap test, keduanya di kode produksi:**
1. `check_bar_count` group by TIMESTAMP bukan TANGGAL -> tiap hari berisi
   "1 bar" -> semua hari masuk kategori parsial -> check selalu LOLOS tanpa
   memeriksa apa pun. False negative yang diam-diam lolos semua data.
2. Ambang `(1200, 1400)` bar/hari salah bukti. Data nyata bimodal: 200 hari
   parsial (118-180 bar) dan 774 hari penuh (1341-1433 bar), dengan celah
   KOSONG antara 180 dan 1100. Ambang lama akan menandai 17% hari yang sah
   sebagai rusak. Sekarang: hari di rentang kosong = ERROR, parsial = sah.

**Validasi data nyata: LOLOS, 0 error, 5 peringatan di 4 tahun.**
Dua jendela anomali terdeteksi otomatis (2024-10-29..11-01, 2026-03-10..27).

**Gate menangkap slip saya sendiri:** `check_foreign_chars.py` menolak
karakter Mandarin (U+7684 U+5B9E U+73B0) yang nyasar ke komentar
`configs/data.yaml`. Sudah diperbaiki. Gate ini langsung membuktikan
dirinya berguna. Menolak commit ini untuk kedua kalinya — kedua-kalinya
karena slip saya sendiri.

**LENGTH_EXCEPTION:** file 445 baris, melewati batas RULES §15. Disetujui user
dengan syarat: kalau nambah fungsi, pecah jadi check vs render.

## Fetch 2026 + hook karakter asing

**`scripts/check_foreign_chars.py`** (draft YAML dari user ditulis ulang jadi Python valid):
- Pindai 10 blok skrip: CJK, kana, Han, Hangul, Cyrillic, Arab, Ibrani, fullwidth.
- Exclude `checkpoints/`, `archive/`, `.ai/backup/`.
- 16 test dengan positive control; karakter asing di test ditulis sebagai
  escape sequence (`"\u9a8c"`) supaya test tidak menggagalkan hook-nya sendiri.
- Hook `check-foreign-chars` ditambahkan. `pre-commit run --all-files` 12/12 hijau.

**Fetch 2026 (2026-01-01 s/d 2026-10-05): 269.846 bar, 3,9 detik, 21,5 MB.**

Temuan:
- Offset +3 jam **konsisten di Jan-Okt 2026** (10/10 bulan).
- 39 gap akhir pekan, semua Senin ~04:00, 2.941-2.963 mnt (49 jam). Normal.
- 156 gap harian, median 63 mnt.
- **Jam break harian BERUBAH**: W02-W10 jam 4 (UTC 01:00) -> W11-W13 jam 3
  (UTC 00:00) -> W14+ kembali jam 4. Permanen 3 minggu di Maret 2026.
  TIDAK cocok Moscow DST (29 Mar) maupun US DST (8 Mar): perubahannya
  mulai di US DST dan berakhir di Moscow DST.
- Spread: median 0,6 pip, p95 0,7, p99 1,2, p99,9 2,3, maks 16,7 pip.
  151 bar (0,056%) > 3 pip, hampir semua di jam UTC 23-01 (dekat break).
- `configs/data.yaml` `spread.default: 1,5` menutup ~p99. Agak optimistic
  untuk ekor, perlu dipertimbangkan saat backtest.

**KESIMPULAN PENTING soal DST:** uji "offset per bulan" itu **sirkular** —
ia membandingkan jam broker dengan UTC yang sendiri dihitung dari asumsi
offset +3, jadi tidak bisa mendeteksi perubahan offset historis.
Satu-satunya sinyal nyata pergeseran jadwal di Maret 2026. Butuh data
Oktober-Maret (2023-2025) untuk melihat pola musiman, khususnya transisi
Oktober saat DST Moskwa berakhir.

## Investigasi DST 2023-2026 (SETELAH fetch penuh)

**Fetch:** 2023 = 362.693, 2024 = 358.331, 2025 = 356.977 bar.
Total 2023-2026 = **1.347.847 bar**, identik dengan `copy_rates_range` awal.

**Proxy break harian (jam dinding broker):**

| Bulan | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Jan | - | 4 | 4 | 4 |
| Feb | - | 4 | 4 | 4 |
| Mar | - | 4 | 4 | **3,4** |
| Apr | - | 4 | 4 | 4 |
| Mei | - | 4 | 4 | 4 |
| Jun | 4 | 4 | 4 | 4 |
| Jul | 4 | 4 | 4 | 4 |
| Agu | 4 | 4 | 4 | 4 |
| Sep | 4 | 4 | 4 | 4 |
| Okt | 4 | **3,4** | 4 | 4 |
| Nov | 4 | **3,4** | 4 | - |
| Des | 4 | 4 | 4 | - |

**Karakterisasi 2 anomali (break di jam dinding 3):**
- 2024-10-29 s/d 2024-11-01 — 4 hari (Sel-Rab)
- 2026-03-10 s/d 2026-03-27 — 12 hari (Sel-Rab)
- Total 16 dari 678 break. Sisanya 662 di jam 4.

**KESIMPULAN: broker TIDAK ikut DST. `Etc/GMT-3` tetap benar untuk
2023-2026.** Alasan:
1. DST berulang annually. Dua anomali ini terjadi SEKALI, di bulan berbeda,
   dengan durasi berbeda, dan tidak terjadi di 4 transisi DST lainnya.
2. 40 dari 47 bulan break di jam dinding 4 — tanpa pola musiman sama sekali.
3. Moscow menghapus DST sejak Oktober 2014 -> MSK permanen UTC+3.
4. Pengukuran live hari ini +3,00 jam, dua kali independen.

**BUKAAN (jujur):** ini berbasis proxy. Bukti mutlak butuh anchor UTC
eksternal (feed broker lain, atau timestamp berita yang diketahui). Proxy
gagal kalau broker mengompensasi jadwal break saat clock-nya bergeser.
Tapi tidak ada bukti yang mengarah ke DST.

**Catatan lain:**
- 2023 Jan-Mei: **nol** break harian. Broker menambahkan break ~Juni 2023.
  Bukaan pasar juga bergeser 03:07 -> 04:01 (+4 menit).
- Spread p99 per tahun: 2023 = 8,5 pip (!), 2024 = 1,7, 2025 = 1,7, 2026 = 1,2.
  2023 punya ekor spread jauh lebih buruk. Max 2024 = 55,6 pip.
- `configs/data.yaml` `spread.default: 1,5` belum diubah (sesuai instruksi user).
