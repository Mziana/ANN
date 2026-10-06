# Laporan Tahap 8 — Fix Deviasi nb02 (D10, D12-flag) — LANGKAH 4

**Tanggal:** 2026-10-06
**Status:** SELESAI — **30/30 assertion PASS**, 0 error, VALID, gate hijau,
**fragmen spread byte-identical**, belum di-commit
**Pilihan format laporan:** **FILE BARU** (`reports/eda/progress/laporan_tahap_8_volatility_fix.md`),
bukan addendum di laporan tahap 2/3 — dipilih agar jejak eksekusi per langkah terpisah dan
tidak mengubah laporan yang sudah direview.

**Rujukan:** `eda_review_deviations_v1.md` (D10, D12), Rancangan EDA v3.1 §5 ("dari M5 dipakai
`spread_pips_max` untuk ekor per bucket") dan §2 baris 33 (Tokyo fix 00:55 UTC; NYSE 09:30
lokal NY), Lampiran A2 (caveat sampling last-tick), keputusan user batch 2026-10-06
(**fragmen byte-identical = syarat**; D10 hanya di tabel notebook).

---

## 1. File yang Diubah

| File | Perubahan | Bukti |
|---|---|---|
| `scripts/_build_eda02.py` | builder = sumber kebenaran: sel §5b (D10), sel §5c (D12 flags), 12 assertion baru, ringkasan markdown diperbarui | blob `c0a80e8…` |
| `notebooks/scalping/eda_02_volatility.ipynb` | hasil regenerate (27 sel: 14 kode, 13 markdown) | blob `f8b6018…` → `a240314…` |

**Tidak diubah:** sel fragmen YAML (tidak diperkaya `spread_pips_max` M5), `configs/data.yaml`,
`reports/eda/2026-10-06/spread_fragment.yaml` (byte-identical), nb00/nb01/nb03/nb04/nb05, D9,
audit kesesuaian, laporan_tahap_5.

## 2. Verdict vs Eksekusi (LANGKAH INI SAJA)

| # | Verdict | Status | Bukti |
|---|---|---|---|
| **D10** | INVALID | **FIXED** | Sel §5b memuat M5 (`spread_pips_max`) dengan mask/strata & label sesi yang sama (A=227.568 / B=37.152 / C=5.244 bar); tabel `TAIL_M5` = 4 tahun × sesi, berdampingan dengan tail M1; 4 assertion D10 **PASS**; **tidak** masuk fragmen (sesuai syarat user) |
| **D12 (bagian nb02)** | PARTIAL | **FIXED** | Sel §5c: flag per bar Tokyo fix `00:55 UTC` + buka NYSE `09:30` lokal NY (DST-aware), tabel `MARKERS`, tabel jam UTC berkolom `marker` (0, 13, 14), 6 assertion D12 **PASS**, tanpa return pasca-marker |
| D6, D7, D12-BoJ | — | selesai di **langkah 3** | `laporan_tahap_7_swing_level_fix.md` |
| D9 | — | **BELUM** (langkah 5, tidak disentuh sesuai perintah) | — |

## 3. Angka Hasil Rerun

**D10 — ekor per bucket (strata A), M1 `spread_pips` vs M5 `spread_pips_max`:**

| sesi | p99 M1 | p99 M5-max | maks M1 | maks M5-max |
|---|---|---|---|---|
| London | 1,20 | 1,40 | 4,60 | 4,60 |
| NewYork | 2,00 | 2,80 | 55,60 | 55,60 |
| Tokyo | 1,30 | 1,50 | 8,70 | 8,70 |
| Sydney | 2,70 | 3,40 | 24,10 | 24,10 |

Contoh per bucket: 2024 NewYork p99 M1 1,90 vs M5-max 2,30; 2023 Sydney 4,00 vs 5,30.
**Maksimum absolut identik M1 vs M5 di setiap bucket** (17 bucket terisi).

**D12 — marker deskriptif (strata A):**

| marker | n_bar | n_hari | jam UTC | tahun |
|---|---|---|---|---|
| tokyo_fix_0055 | 825 | 825 | 0 | 2023,2024,2025,2026 |
| nyse_open | 824 | 824 | 13, 14 | 2023,2024,2025,2026 |

Bar buka NYSE per jam UTC: **13 → 560** (EDT) dan **14 → 264** (EST) → bukti DST-aware.
Self-check JST: `00:55 UTC == 09:55 Asia/Tokyo` (assertion di dalam sel, PASS).

**Integritas fragmen:**
`spread_fragment.yaml` sha256 sebelum = sesudah = `6596adf2…6018d16`, `git status` bersih untuk
path itu, dan **output fragmen di notebook identik dengan file tersimpan** (dicek per-string).

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| D10 dihitung pada strata & label sesi yang sama dengan M1 | TERVERIFIKASI | pola mask `broker_day` + `add_labels`; M5-A = 227.568 bar (cocok nb03/nb04) |
| Ekor M5 "tidak menemukan ekor baru" | TERVERIFIKASI | `max_M1 == max_M5max` di 17/17 bucket; p99 M5 ≥ p99 M1 (efek agregasi) |
| D12 DST-aware, bukan asumsi | TERVERIFIKASI | jam UTC 13 (560) + 14 (264); self-check JST 09:55; satu bar per hari |
| D12 bukan event-study | TERVERIFIKASI | tidak ada kolom return pasca-marker; assertion "bukan event-study" PASS |
| Fragmen tidak diperkaya rerun ini | TERVERIFIKASI | sha256 identik + `git status` bersih + output notebook == file |
| nb02: 30/30 PASS, 0 error, urut, VALID | TERVERIFIKASI | `RINGKASAN: 30/30`, error 0, `execution_count` [1..14], `nbformat.validate` |

## 5. Gate (output asli, dijalankan setelah edit terakhir)

```
== ruff check ==            All checks passed!                              rc=0
== ruff format --check ==   29 files already formatted                     rc=0
== pytest ==                157 passed in 1.26s                            rc=0
== validate_data ==         2023: 0 error, 2 peringatan -> LOLOS
                            2024: 0 error, 2 -> 2025: 0 error, 1 -> 2026: 0 error, 1   rc=0
== check_foreign_chars ==   OK: 68 file discan, tidak ada karakter asing.   rc=0
```
Riwayat build: pass-1 `nbconvert exit=0` (30/30, fragmen tetap identik) → pass-2 `nbconvert exit=0`
(ringkasan markdown berisi angka hasil eksekusi, fragmen tetap identik). Tidak ada build merah.

## 6. Self-Audit 3× Adversarial

**Putaran 1 — Correctness**
- M5 strata A = **227.568** bar — sama persis dengan M5 stratum A di nb03/nb04 → stratifikasi
  konsisten lintas notebook (bukan implementasi mask kedua yang berbeda).
- Ordering ekor diuji: `p95 ≤ p99 ≤ maks` per bucket M5 (assertion PASS); `n_M5 < n_M1` di semua
  bucket (skala ~1/5, assertion PASS).
- Marker: `n_bar == n_hari` untuk kedua marker (satu bar per hari) dan `n_hari ≥ 700`
  (825 dan 824) → tidak ada duplikasi/hilang.
- **Sel tanpa output ditemukan dan diperiksa:** satu sel kode (`_flatten_numbers`) tidak
  menghasilkan output. Dibandingkan dengan versi HEAD: **sudah begitu sebelumnya** (sel definisi
  fungsi, tanpa print) → bukan regresi rerun ini. 13/14 sel lainnya beroutput normal.
- Notebook tereksekusi: `execution_count` [1..14] berurutan, 0 error, `nbformat` VALID.

**Putaran 2 — Bias & Asumsi**
- **Syarat user dipatuhi ketat:** D10 **tidak** masuk fragmen; fragmen dibuktikan byte-identical
  dua kali (sebelum/sesudah, dan sesudah pass-2) — bukan klaim dari ingatan.
- **Temuan saya sendiri yang menuntut koreksi (SA-48):** ringkasan nb02 masih menulis "Fragmen
  spread **belum** diterapkan; menunggu 4b", padahal fragmen **sudah diterapkan** (commit
  `cb84717`, Lampiran A2). Kalimat itu dikoreksi di rerun ini dan perubahannya dinyatakan di
  ringkasan notebook (bukan diubah diam-diam).
- **Tafsir "flag saja"** (bukan event-study) saya patuhi: hanya flag + hitungan; tidak ada
  jendela lebar yang saya karang (user tidak menetapkan lebar jendela), dan tidak ada return
  pasca-marker.
- Angka lama Q2/Q3 (HOURLY, SESSIONAL, M4) tidak berubah karena sel lama tidak disentuh; kalibrasi
  M1–M4 tetap seperti sebelumnya.

**Putaran 3 — Meta-check**
- Urutan perintah dipatuhi: langkah 3 (termasuk laporannya) tuntas sebelum langkah 4; D9 tidak
  disentuh; audit kesesuaian & laporan_tahap_5 tidak disentuh; tidak ada commit/amend.
- File yang berubah di langkah ini: 2 (builder nb02 + notebook nb02) + 1 laporan baru. Tidak ada
  file lain (dibuktikan `git status`).
- Asumsi yang dinyatakan: unit ekor = pip (`spread_pips`/`spread_pips_max`); marker memakai bar
  M1 (bukan M5); label sesi primer DST-aware.

## 7. Yang Belum Diverifikasi

- **Semantik `spread_pips_max` di parquet M5**: saya hanya memverifikasi kolom & nilainya; tidak
  memverifikasi ulang pipeline resample yang membuatnya (itu Lapisan 1, sudah diaudit). Caveat
  last-tick per bucket sudah dicatat di Lampiran A2 dan diulang di sel §5b.
- **D10 belum dipakai untuk mengubah config**: memang tidak boleh (syarat user); interpretasi
  p99-M5 vs max di atas adalah bacaan saya, bukan keputusan biaya.
- **Marker D12 tidak diuji dampaknya** ke volatilitas/spread (itu event-study, di luar scope).
- **Rujukan hilir**: nb05 belum boleh mengonsumsi nb03/nb04 sebelum commit koreksi; nb02 juga
  menunggu commit B.
- Gate dijalankan pada repo dengan perubahan langkah 2–4 yang belum di-commit; `tests/` tidak
  disentuh sehingga 157 passed tetap relevan.

## 8. STOP — Tunggu Review User

Langkah 3 dan 4 selesai. Berikutnya **tidak** saya kerjakan (sesuai perintah): langkah 5 (rename
figure D9 + kunci skema FIG), update audit kesesuaian, dan commit A/B. Menunggu review.
