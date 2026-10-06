# Laporan Revisi Fragmen Spread (Langkah 4b)
**Tanggal:** 2026-10-06
**Status:** SELESAI — **belum diterapkan ke config**, menunggu audit Klenz

## File yang Diubah

| File | Perubahan |
|---|---|
| `reports/eda/progress/../2026-10-06/spread_fragment.yaml` | **Diubah total** — skema baru `cost_basis` + `stress_bands` + `_sesi` |
| `reports/eda/progress/laporan_tahap_4_volatility.md` | Fix typo rasio **5,30× → 8,83×** (2 tempat) |
| `configs/data.yaml` | **HANYA komentar `by_year`** — konfirmasi: ya, hanya komentar |
| `scripts/_build_eda02.py` | Generator fragmen diperbarui |
| `notebooks/scalping/eda_02_volatility.ipynb` | Ter-regenerate, 20/20 PASS |

**Konfirmasi eksplisit `configs/data.yaml`:** `git diff` menunjukkan **0 baris nilai berubah** — seluruh 11 baris +/- adalah prefixed `#` (komentar). Nilai terverifikasi tetap: `default: 1.5`, `by_year: {2023: 3.0, 2024: 1.5, 2025: 1.5, 2026: 1.5}`, `stress_multiplier: 2.0`, `pip_size: {USDJPY: 0.01, default: 0.0001}` (dict). `cost_basis`/`stress_bands` **tidak ada** di config.

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Config lama utuh (by_year 2023 tetap 3,0) | TERVERIFIKASI | `yaml.safe_load` → `{2023: 3.0, 2024: 1.5, 2025: 1.5, 2026: 1.5}` |
| `pip_size` tetap dict | TERVERIFIKASI | `{USDJPY: 0.01, default: 0.0001}` |
| `cost_basis` = MEAN, basis strata A | TERVERIFIKASI | default **0,65**; by_year 2023=**0,51** · 2024=0,70 · 2025=0,67 · 2026=0,62 |
| `cost_basis.by_session` = MEAN | TERVERIFIKASI | London 0,61 · NewYork 0,69 · Tokyo 0,62 · Sydney 0,80 |
| `stress_bands` p95 & p99 terpisah | TERVERIFIKASI | p95 default 1,0 (by_year 0,6/1,2/1,0/0,7); p99 default 1,6 |
| `stress_bands.p95.by_session` | TERVERIFIKASI | London 0,8 · NY 1,2 · Tokyo 0,9 · Sydney 1,5 |
| Baris `_sesi` + syarat backtest ada | TERVERIFIKASI | assertion "Fragment punya deklarasi _sesi + syarat backtest" PASS |
| `pip_size` di fragmen tetap dict | TERVERIFIKASI | assertion `isinstance(fragment["pip_size"], dict)` PASS |
| Fragmen tidak bocor ke config | TERVERIFIKASI | kunci config `spread` = by_news, by_session, by_year, default, *_multiplier, pip_size — tanpa cost_basis/stress_bands |
| Comment `by_year` ditulis ulang | TERVERIFIKASI | 11 baris komentar baru, menjelaskan p99 file utuh vs semesta dagang |
| **Typo rasio diperbaiki 8,83×** | TERVERIFIKASI | 5,30/0,60 = **8,8333**; laporan kini menulis 8,83× + penjelasan asal angka 5,30× |
| **Gate: validate_data exit 0** | TERVERIFIKASI | 2023: 2 peringatan · 2024: 2 · 2025: 1 · 2026: 1, semua **LOLOS**, 0 error |
| **Gate: ruff check + format** | TERVERIFIKASI | All checks passed · 16 files already formatted · exit 0 |
| **Gate: check_foreign_chars** | TERVERIFIKASI | OK, 51 file, exit 0 |
| **Gate: pytest** | TERVERIFIKASI | **157 passed**, exit 0 |
| **Gate: nb02 masih valid** | TERVERIFIKASI | `nbconvert exit=0`, `builder_exit=0`, **20/20 assertion PASS** |
| Tidak ada commit | TERVERIFIKASI | `git log -1` masih `9a60995` |

## Semantik penerapan fragmen (MEDIUM-28)

Keputusan yang dipakai — **Opsi A: fragmen MENAMBAH sub-kunci, tidak mengganti blok `spread`.**

Saat akhirnya diterapkan, `configs/data.yaml` -> `spread` akan menjadi:

```yaml
spread:
  default: 1.5            # TETAP (tidak diganti)
  by_year: {2023: 3.0, ...}  # TETAP
  by_news: ...            # TETAP
  warn_multiplier: ...    # TETAP
  error_multiplier: ...   # TETAP
  stress_multiplier: 2.0  # TETAP
  pip_size: {...}         # TETAP (identik dengan fragmen, tidak perlu diubah)
  cost_basis: {...}       # BARU - ditambahkan
  stress_bands: {...}     # BARU - ditambahkan
```

Aturan yang mengikat:
1. Fragmen **menambah** `cost_basis` + `stress_bands`; **tidak pernah** mengganti
   atau menghapus kunci lama.
2. `pip_size` **tidak** diganti - nilainya sudah identik dengan config
   (`{USDJPY: 0.01}`); fragmen menyalinnya hanya agar fragmen mandiri.
3. `by_year`, `by_news`, `warn_multiplier`, `error_multiplier` **tetap** apa adanya.
4. **Opsi B ditolak**: menyertakan `pip_size` penuh di fragmen dengan nilai
   `default` tambahan akan menduplikasi isi dengan config dan berisiko berbeda
   diam-diam bila salah satu diedit. Duplikasi sumber kebenaran lebih berbahaya
   daripada singkatnya fragmen.

**Ketegangan yang harus diputuskan terpisah saat penerapan:** `cost_basis.default`
= 0,65 (MEAN) berdampingan dengan `spread.default` = 1,5. Keduanya akan hidup
bersamaan. Kode mana yang jadi otoritas saat menghitung biaya traded adalah
**keputusan penerapan**, bukan keputusan data.

## Penyimpangan dari spesifikasi Spark (perlu persetujuan Klenz)

Struktur fragmen **11/11 sesuai** spesifikasi (terverifikasi `yaml.safe_load`), tapi ada **2 penyimpangan** yang harus diputuskan, bukan diasumsikan benar:

| Spec Spark | Implementasi | Alasan |
|---|---|---|
| `by_session: {London, NY, Tokyo, Sydney, Off: <mean>}` | `{London, NewYork, Tokyo, Sydney}` — **Off tidak dimasukkan** | Bar berlabel `Off` di strata A = **0 bar** (empat sesi menutup 24 jam), sehingga MEAN-nya **tidak terdefinisi**. Memasangnya sebagai angka akan mengarang nilai. Di seluruh data `Off` hanya 2.894 bar (0,2147%). |
| Nama kunci ditulis `NY` | Kunci memakai `NewYork` | Konsisten dengan label sesi di nb00 (`SESSION_ORDER = [London, NewYork, Tokyo, Sydney, Off]`) dan dengan `_sesi.label_eksklusif`. Menyamakan ke `NY` justru menimbulkan ketidakkonsistenan antara fragmen dan notebook. |

Kedua penyimpangan disengaja dan **dinyatakan terbuka** — bukan diam-diam.

## Self-Audit 3× Adversarial

### Putaran 1 — Correctness
- **SA-22 (DITEMUKAN) — Spark menemukan kesalahan aritmetika saya.** Laporan saya menulis rasio H1-vs-H2 = 5,30×; padahal 5,30/0,60 = **8,83**. Angka 5,30× adalah hasil hitung **lain** (B vs strata A penuh: 5,30/1,00) yang memang dicetak notebook. **Fix:** laporan ditulis 8,83× dengan penjelasan eksplisit asal angka 5,30×, supaya tidak ada dua angka yang saling bertentaran tanpa konteks.
- **SA-23 (DITEMUKAN) — Assertion lama mengacu ke struktur fragmen lama.** Setelah fragmen dipecah jadi `cost_basis`/`stress_bands`, assertion `fragment["by_year"]` dan `fragment["by_session_p95"]` melempar `KeyError` → nbconvert exit 1. **Fix:** assertion ditulis ulang ke skema baru + ditambah 5 assertion baru (by_session 4 sesi, stress_bands p95&p99, deklarasi `_sesi`, `pip_size` bertipe dict).
- **SA-24 (DIKOREKSI oleh audit Klenz) — Token ASCII lolos hook, bukan karena hook tidak memindai YAML.** Diagnosis awal saya salah. `scripts/check_foreign_chars.py` memindai `.yaml` (`SCANNED_SUFFIXES` memuat `.yaml`, `.yml`, `.md`, dan lainnya) dan **Klenz sudah menjalankan hook ke `configs/data.yaml` → OK**. Yang lolos adalah token **`separationPer indefinitely`** — terdiri dari karakter **ASCII** murni, sehingga berada **di luar cakupan** apa yang hook deteksi (hook menangkap skrip non-Latin: CJK, kana, Hangul, Cyrillic, Arab, fullwidth). Jadi ini **lolos by design**, bukan bug hook. **Mitigasi yang benar:** setelah edit manual di YAML, **re-read** baris yang diubah (atau jalankan hook lalu tetap baca hasilnya), karena hook tidak akan menangkap token ASCII rusak.
- Verifikasi ulang nilai config **setelah** edit komentar (bukan sebelum) — karena `yaml.safe_load` dijalankan ulang, hasilnya cocok.

### Putaran 2 — Bias & Aturan
- **Tidak menerapkan fragmen ke config** — `cost_basis`/`stress_bands` absen dari config; `git diff` hanya komentar.
- **Nilai lama tidak diubah** — by_year 2023 tetap 3,0, default tetap 1,5, stress_multiplier tetap 2,0, pip_size tetap dict.
- **Tidak ada commit** — `git log -1` masih `9a60995`.
- **Basis angka tetap strata A** — tidak ada pencampuran B/C, sesuai instruksi Spark.
- **Anti-halusinasi** — angka `cost_basis` dihitung ulang dari parquet, bukan Estimated.

### Putaran 3 — Yang Terlewat
- **SA-25 (DITEMUKAN, DI LUAR RUANG KERJA INI) — `requirements.txt` punya 3 dependensi tak tercatat.**
  `git status` menunjukkan `requirements.txt` **modified** dari sesi sebelumnya, menambah:
  `scipy==1.17.1`, `matplotlib==3.10.9`, `nbformat==5.11.1`.
  Ketiganya **benar-benar dipakai** notebook EDA (scipy untuk QQ/normal, matplotlib untuk figure, nbformat untuk builder). Versi terpasang cocok dengan pin. **TAPI `CHANGELOG.md` tidak menyebut satu pun** — melanggar RULES §13 (izin + pin + update CHANGELOG).
  Saya **tidak menambahkan** CHANGELOG karena itu di luar scope keputusan 4b dan menunggu audit; dicatat di sini agar Klenz mengetahuinya.
- **Risiko missed:** `check_foreign_chars` **tidak** memindai YAML, sehingga cacat karakter di `configs/data.yaml` lolos hook. Gates yang melindungi file YAML selama ini hanya `yaml.safe_load` + scan manual. Ini **cacat proses**, bukan hanya cacat file.
- **Fragmen masih dua nilai**: `cost_basis.default` 0,65 (MEAN) vs config `default` 1,5. Keduanya akan hidup berdampingan sampai diterapkan. Kalau ada kode yang membaca `spread.default` tanpa tahu bahwa fragmen merekomendasikan 0,65, hasilnya **berbeda 2,3×**. Perlu keputusan eksplisit di 4b: kode mana yang jadi otoritas.
- **Serangan musuh:** (a) ada yang menerapkan fragmen sebelum audit → assertion & status `_status: PROPOSAL REVISI` + tidak ada commit; (b) `by_year[2023]` diganti diam-diam → `git diff` hanya komentar; (c)Klenz membaca `cost_basis.by_year[2023]=0,51` dan mengira itu ganti `3,0` → `_catatan` menjelaskan perbedaan secara eksplisit.

### Verdict
- **Siap lapor? Ya.**
- Alasan: seluruh Bagian 1–3 terpenuhi dan diverifikasi; **2 temuan tak terduga** ditemukan (SA-24 charset, SA-25 requirements/CHANGELOG) dan dicatat, bukan disembunyikan. Semua gate hijau.

## Yang Belum Diverifikasi
- **Ke-berterimaan fragmen revisi** — menunggu audit Klenz.
- **CHANGELOG untuk scipy/matplotlib/nbformat** — belum ada (SA-25).
- **Rancangan Q2/Q3** — tidak diuji di sini; hanya gate regresi.

## STOP — Tunggu Audit Klenz
