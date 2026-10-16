# Audit Perbaikan M1–M5 — Kontrak Broker FINEX

**Tanggal:** 2026-10-15 · **Jenis:** perbaikan_file + verifikasi_adversarial
**Ruang lingkup:** 5 temuan M1–M5 + 2 cacat sekunder yang ditemukan saat audit.
**Peran:** arsitek + asisten + coder (gabung, atas instruksi eksplisit pengguna;
§26 biasanya mewisahkan peran — lihat catatan di bawah).

---

## 1. Ringkasan

Semua M1–M5 diperbaiki dan terverifikasi ulang dari data parquet secara
independen. Regresi penuh tetap hijau (254/254). Selama audit ditemukan **6 cacat
di kerja sendiri**, termasuk 2 yang akan merusak dokumen secara sunyi kalau
gate tidak ada (lihat §4).

## 2. Temuan & Perbaikan

| ID | Temuan | Perbaikan | Verifikasi |
|---|---|---|---|
| M1 | Angka spread salah di `configs/broker.yaml` + `docs/broker-contract-finex.md`: offset jam broker ditambahkan dua kali, causinggeseslabel sesi ~2 jam, dan label spike `55,60` ditempel ke Sydney padahal itu NewYork | Tulis ulang seluruh blok `spread` dari hitung ulang independen; tambah kolom `n`; betulkan `spread_menyebar_pada_t.dp` → `.t` | Gate silang: mean per sesi di `data.yaml → cost_basis.by_session` = 0,61/0,69/0,62/0,80 **cocok** dengan `broker.yaml` (dua sumber independen) |
| M2 | `EDA/README.md`: 5 nilai dolar hilang (`$6,09`→`,09` dst.) | Pulihkan; biaya dihitung ulang dari nilai yang ditampilkan | Gate: 4 total + 4 "setara pip" cocok dengan `broker.yaml` |
| M3 | `EDA/02-volatility.md`: keputusan lama ditulis seolah masih berlaku padahal sudah diterapkan ke config | Tandai status "sudah diterapkan", hapus duplikasi "yang yang", koreksi "~5×" → 5,9× | `configs/data.yaml` memuat `warn_multiplier=3.0`, `error_multiplier=8.0` |
| M4 | `docs/broker-contract-finex.md`: section konflik spread basi masih ada sebagai-finding terbuka | Tulis ulang sebagai tertutup; nomor's pernyataan open yang memang masih terbuka (duplikasi sumber config) | Dibaca ulang; tidak ada angka basi tersisa |
| M5 | `EDA/05-regimes.md`: "68/68 assertion PASS" tampak seperti klaim tanpa sumber | Tambahkan provenance eksplisit | Angka ada di `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md:4` |
| X1 | Kata Indonesia tergarbling: `hariWednesday`, `bisabisa`, `terHopital` | Dibetulkan: `hari Wednesday`, `H1/H2 bisa menyeberang hari`, `terobservasi` | Gate karakter asing bersih |
| X2 | Karakter Mandarin bocor ke 6 baris (5 di antaranya **tulisanku sendiri**) | Semua dibetulkan | `check_foreign_chars.py`: 0 di file yang disentuh |

## 3. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Angka spread per-sesi | TERVERIFIKASI | Hitung ulang independen (tanpa `add_labels`) cocok persis; gate silang `data.yaml` cocok |
| 55,60 pip = NewYork, bukan Sydney | TERVERIFIKASI | 6 bar terbesar seluruhnya NewYork, 2024-12-24 (malam Natal) |
| Skenario Cheap/Mid salah | TERVERIFIKASI | kolom "2 sisi" dihitung 1 sisi: `0,61×2×6,6935+2` = **$10,17** (bukan $6,09) |
| "meleset 4×" salah | TERVERIFIKASI | $10,70 / $2,00 = **5,35×**, understatement spread 81,3% |
| Skenario Cheap = "lantai" | TERVERIFIKASI (dilemma) | Justru **mean London+NewYork 2026** = `0,6146` (n=152.461) — tahun termurah **di dalam stratum A**; label "lantai" diperjelas |
| 2023 → ERROR disengaja | TERVERIFIKASI | `0,51×8 = 4,08` < p99 stratum B `8,50` |
| 68 assertion benar | TERVERIFIKASI | `laporan_tahap_11_regime.md:4`; output notebook memang tidak mencetak angka |
| `broker.yaml` = satu-satunya otoritas | **GAGAL (dibongkar sendiri)** | `git grep broker.yaml -- '*.py'` → nihil. `check_spread` (`src/data/validate_data.py:256`) masih `load_config()` → `configs/data.yaml`. Header sudah dikoreksi |
| `pip = $6,6935/lot` | TERVERIFIKASI | `0,01 × 100.000 / 149,3987` |
| `2.255 / 1.136.401 > 3 pip` | TERVERIFIKASI | 0,1984% |
| Regresi | TERVERIFIKASI | 254 passed |
| Dokumen ≡ data | TERVERIFIKASI | gate 80 pemeriksaan, 0 gagal |

### Metodologi verifikasi

Hitung ulang **independen** disengaja: tidak mengimpor `add_labels()`,
`session_flags()`, `exclusive_label()`, atau `wall_clock_series()`. Label sesi
dihitung ulang dengan `zoneinfo` + `if/elif`, statistik dengan `numpy.quantile`,
anomaly window dari `configs/data.yaml`, dan data mentah `spread_pips`.

## 4. Cacat di kerja sendiri (6)

| # | Cacat | Dampak | Penangkap |
|---|---|---|---|
| 1 | `ANOMALY_WINDOWS` ditebak 2025 (sebenarnya 2024-10 & 2026-03) | Stratum C = 19.313 vs 26.198 — angka salah | **Gate strata**, sebelum ditulis ke dokumen |
| 2 | `edit` tool merusak YAML (indentasi `deskripsi:` hilang → tidak lagi anak `slippage:`) | YAML tak valid | Baca ulang file, bukan percaya laporan sukses |
| 3 | `mean_digits=4` ke `row()` padahal `stats()` sudah 3 desimal | 2025 tampil 0,6740 | Baca output debug |
| 4 | Regex gate sendiri: `[^|]*\$?([\d,]+)` menangkap "7" dari "$10,17" | Gate bohong | Gate melaporkan gagal → diselidiki |
| 5 | Karakter Mandarin bocor ke teks yang saya tulis sendiri (U+5E74, U+7528 U+6237, U+6839 U+6E90, U+5C5E U+6027) | Semua dibetulkan | `check_foreign_chars.py`: 0 di file yang disentuh |
| 6 | Output gate dipotong `Select-Object -Last 25` | 3 kontaminasi tersembunyi (entries baris 52/60) | Gate dijalankan ulang penuh |

Cacat #1 adalah yang paling berbahaya: tanpa gate, hitungan salah akan
tertanam di dokumen sebagai fakta.

## 5. Self-audit 3× adversarial

**Putaran 1 — Correctness.** Menangkap cacat #1–#4 di atas. Konteks tambahan:
eksplorasi zscore mencakup anomali 2023 sehingga total 1.347.847 = A+B+C
(konsisten dengan config).

**Putaran 2 — Bias & asumsi.**
- Rekognisi sirkularitas: verifikasi pertama sempat memakai `add_labels()` —
  fungsi yang sama dengan notebook → hanya membuktikan determinisme. Ditulis ulang.
- Asumsi tanpa label sempat mau ditulis sebagai fakta terukur ("pipe spread ~80%") —
  dikonfirmasi lewat kolom `spread_pips`.
- `_komisi_per_sisi_usd` = 1,00 adalah **ASUMSI** (lihat §6).
- Duplikasi config: `data.yaml` ternyata sudah benar sejak awal → bug M1 hanya di
  file tulisanku. Mengurangi dampak, bukan mengurangi kesalahan.

**Putaran 3 — Meta-check.**
- **Negative control:** 3 angka dikorupkan (`mean_NewYork`, `n_Tokyo`,
  `total_mid`) → gate **3/3 tertangkap**, file dipulihkan utuh. Gate bisa
  dibuktikan berguna, bukan sekadar selalu hijau.
- Cross-check antar sumber (`data.yaml` ↔ `broker.yaml` ↔ dokumen ↔ README).
- Tidak ada angka lama yang dibiarkan menetap.

## 6. Yang belum diverifikasi (jangan dipakai untuk keputusan dagang)

| Item | Status | Catatan |
|---|---|---|
| Komisi $1/lot: **per side atau per lot total** | **[INPUT] TERVERIFIKASI** | User konfirmasi 2026-10-15: **per side**, dibebankan saat buka + tutup = **$2,00 round-turn**. Bukan spec sheet Finex. |
| Contract size 100.000 | **[SPESIFIKASI]** | Spec Finex USD/JPY dari user 2026-10-15 (1,0 lot = 100.000 USD; 0,1 = 10.000; 0,01 = 1.000; base USD; pip 0,01; maks 50 lot/order; leverage 1:500). Cocok silang anchor user di `scripts/archive/eda-06-07/_build_eda06.py:411` (`USD_PER_POINT_001 = 1.6/251`). Dibalik-balikkan: kontrak 100.000 -> kurs implisit 156,88 (di dalam rentang data 127,26-163,97); 10.000 -> 15,69 dan 1.000.000 -> 1.568,75 (keduanya mustahil). Koreksi atas klaim "tanpa sumber" yang saya tulis di putaran sebelumnya. |
| Kurs saat pengamatan anchor (156,88) | **BELUM TERVERIFIKASI** | Tidak tercatat saat anchor `$1,6` diamati. Rate pembagi tabel biaya tetap 149,3987 (mean 2023-2026, terukur). |
| Free swap berlaku di akun Standard | **[VERIFIKASI]** | Input menyebut Standard; free swap disebut sebagai properti Islami |
| Leverage 1:500, min lot 0,01, maks 50 lot/order (akun Standard) | **[SPESIFIKASI]** | Spec Finex dari user 2026-10-15. Regulasi BAPPEBTI/JFX/KBI dan klaim eksekusi tetap **[VERIFIKASI]** — belum dikonfirmasi ke dokumen broker |

## 7. Tindakan lanjutan

1. ~~**Konfirmasi komisi per side vs round-turn ke user**~~ — **SELESAI**
   2026-10-15; blocker dihapus.
2. **Putuskan sumber otoritas**: samakan konsumen `broker.yaml`, atau turunkan
   `broker.yaml` menjadi dokumentasi yang hanya-baca. Saat ini belum ada kode yang membacanya.
3. `check_spread` 2023 ERROR — putuskan intentional atau perbaiki ambang.
4. ~~**Konfirmasi contract size ke spec sheet Finex**~~ — **SELESAI**
   2026-10-15; spec Finex dari user (kontrak 100.000, base USD, pip 0,01,
   maks 50 lot/order, leverage 1:500) + cocok silang anchor.
5. `reports/governance/2026-10-07/Audit/reaudit-kedua-fix-D1-D5.md` dan
   `thoughts/ledgers/CONTINUITY_ses_ef37.md` punya karakter Mandarin **sudah di HEAD** —
   di luar scope sesi ini.

---

## Catatan kepatuhan

- Pemisahan peran §26 dilewati **atas instruksi eksplisit pengguna** yang meminta
  satu AI bertindak sebagai arsitek + asisten + coder. Self-audit 3× dijalankan
  sebagai gantinya agar standar bukti tetap terjaga.
- Tidak ada commit dibuat.
- Gate yang dipakai: `scripts/check_foreign_chars.py` (resmi), `pytest tests/`,
  plus gate dokumen sementara `C:\Users\Fajar\AppData\Local\Temp\opencode\gate_docs.py`
  (80 pemeriksaan, disertai negative control).
