# Laporan Tahap 9 — Fix Deviasi nb01 (D9: Rename Figure + Kunci Skema) — LANGKAH 5

**Tanggal:** 2026-10-06
**Status:** SELESAI — **23/23 assertion PASS**, 0 error, VALID, gate hijau, belum di-commit
**Pilihan format laporan:** **FILE BARU** (`reports/eda/progress/laporan_tahap_9_figures_fix.md`),
bukan addendum — konsisten pola tahap 7/8.

**Rujukan:** `eda_review_deviations_v1.md` baris 21 (D9: "3 file → FIG-01/02/03 (M1/M5/M15);
nomor bebas berikutnya = FIG-04 ke atas, diklaim sekuensial oleh nb03, nb04, nb05; nb05
memverifikasi registry; setiap plot yang ditampilkan wajib disimpan") dan Rancangan EDA v3.1
baris 46 (`figures/FIG-01.png` s/d `FIG-NN.png`, satu grafik satu pesan, bernomor).

---

## 1. File yang Diubah

| File | Perubahan | Bukti |
|---|---|---|
| `reports/eda/2026-10-06/figures/FIG-01_qq_M1.png` → `FIG-01.png` | `git mv` (provenance rename eksplisit di indeks) | status `R` |
| `reports/eda/2026-10-06/figures/FIG-01_qq_M5.png` → `FIG-02.png` | `git mv` | status `R` |
| `reports/eda/2026-10-06/figures/FIG-01_qq_M15.png` → `FIG-03.png` | `git mv` | status `R` |
| `scripts/_build_eda01.py` | sumber kebenaran: `enumerate(Q1_TIMEFRAMES, start=1)` + `f"FIG-{nomor:02d}.png"` + assertion pengunci skema; komentar penjelas tanpa nama lama | blob `94b2c70b…` |
| `notebooks/scalping/eda_01_returns.ipynb` | **hasil regenerate** (22 sel: 12 kode, 10 markdown) — output `tersimpan:` kini menunjuk FIG-01/02/03 | blob `ec448a59…` |

Tidak menyentuh nb02/nb03/nb04/nb05, `configs/`, `src/`, data, audit kesesuaian,
laporan_tahap_5/2/3/6/7/8. Backup 3 PNG pra-rename: `/tmp/tmp.1ZXwaBEMIZ/` (di luar repo).

## 2. Verdict vs Eksekusi

| # | Verdict | Status | Bukti |
|---|---|---|---|
| **D9** | INVALID | **FIXED** | `ls figures/` = **tepat 3 file** (FIG-01.png, FIG-02.png, FIG-03.png); output nb01 `tersimpan:` menunjuk ketiganya; assertion **"PASS Skema FIG-01/02/03 terkunci (D9)"**; `grep -rl FIG-01_qq` = **0 hit** di `notebooks/` dan **0 file tracked** di `scripts/` (satu-satunya sisa match adalah `__pycache__/*.pyc` yang di-gitignore, bukan source) |

## 3. Pilihan Metode (dinyatakan, sesuai keputusan user)

**Opsi A: `git mv` dulu → regenerate.** Alasan: provenance rename eksplisit di indeks (bukan
bergantung deteksi-similaritas git), `figures/` tidak pernah berisi 6 file di keadaan antara,
dan mode gagal regenerasi bersih (satu perintah revert). Regenerasi kemudian menimpa ketiga PNG
dengan gambar hasil eksekusi.

**Rename murni vs rename+refresh (hash):** sha256 PNG hasil regenerate **identik byte-per-byte**
dengan file hasil `git mv`:
`FIG-01 cab23cb0…`, `FIG-02 66dbdb66…`, `FIG-03 01722863…` → **rename murni**, tidak ada
refresh konten (matplotlib deterministik di build ini).

## 4. Skema FIG yang DIKUNCI (deliverable langkah ini)

| Nomor | Pemilik | Isi |
|---|---|---|
| FIG-01 | nb01 | QQ-plot M1 stratum A vs normal |
| FIG-02 | nb01 | QQ-plot M5 stratum A vs normal |
| FIG-03 | nb01 | QQ-plot M15 stratum A vs normal |
| FIG-04 dan seterusnya | diklaim **sekuensial**: nb03 → nb04 → nb05 | satu grafik satu pesan; **nb05 wajib memverifikasi registry** nomor saat sintesis report.md |

Dijaga assertion di builder nb01: `[p.name for p in figures] == ["FIG-01.png","FIG-02.png","FIG-03.png"]`
→ regenerasi mendatang tidak bisa diam-diam mengembalikan penamaan lama (kelas regresi SA-41).

## 5. Gate (output asli, dijalankan setelah edit terakhir)

```
== ruff check ==            All checks passed!                              rc=0
== ruff format --check ==   29 files already formatted                     rc=0
== pytest ==                157 passed in 1.15s                            rc=0
== validate_data (informasional, tidak diwajibkan perintah ini)
                            2023: 0 error, 2 peringatan -> LOLOS
                            2024: 0 error, 2 -> 2025: 0 error, 1 -> 2026: 0 error, 1   rc=0
== check_foreign_chars ==   OK: 68 file discan, tidak ada karakter asing.   rc=0
```
Riwayat build: pass-1 `nbconvert exit=0` (23/23) → komentar direword → pass-2 `nbconvert exit=0`
(23/23, hash PNG identik). Tidak ada build merah. Laporan baru ini lolos pemindai eksplisit
`check_foreign_chars.py <file>` (rc=0) — gate default hanya memindai file tracked.

## 6. Self-Audit 3× Adversarial

**Putaran 1 — Correctness**
- Urutan FIG mengikuti `Q1_TIMEFRAMES = ("M1","M5","M15")` (baris 234) → FIG-01=M1, FIG-02=M5,
  FIG-03=M15, persis perintah user dan putusan D9.
- 22/22 sel kode? **12 sel kode** dengan `execution_count` [1..12] berurutan, 0 error,
  `nbformat` VALID; `RINGKASAN: 23/23 assertion PASS untuk Q1` (naik dari 22 → 23 karena satu
  assertion skema baru, bukan assertion lama yang dilemahkan).
- Angka statistik nb01 tidak berubah: patch hanya menyentuh penamaan file figure + komentar +
  1 assertion; tabel Q1 dan angka di markdown ringkasan tidak disentuh.

**Putaran 2 — Bias & Asumsi**
- Klaim "0 hit" saya perketat setelah grep pertama menemukan 3 sisa match: (a) komentar penjelas
  di sel kode — **direword** lalu di-regenerate, (b) `.pyc` di `__pycache__/` — **di-gitignore**,
  bukan source, dilaporkan terbuka di sini, (c) rujukan historis di `laporan_tahap_3_returns.md`
  — **sengaja tidak disentuh** (DILARANG oleh perintah).
- Tidak ada klaim "rename murni" sebelum hash compare membuktikannya.
- Backup `/tmp` dibuat sebelum `git mv` (bukti: `ls` di log), di luar repo.

**Putaran 3 — Meta-check**
- Urutan dipatuhi: hanya langkah 5; tidak commit/amend `e4efbfd`; skema FIG dicatat di laporan
  ini sebagai deliverable (bukan catatan tempel), termasuk kewajiban verifikasi registry nb05.
- Status akhir konsisten: 3 `R` (rename) + builder + notebook berubah; tidak ada file lain.
- `git mv` = staging rename, bukan commit — disiplin batch tetap terjaga.

## 7. Yang Belum Diverifikasi

- **Registry FIG-04+ belum ada** — nomor itu baru diklaim saat nb03/nb04/nb05 membuat figure;
  nb05 nanti wajib memverifikasi (putusan D9). Yang terkunci hari ini hanya pemilik FIG-01..03.
- **Isi visual PNG** tidak diinspeksi (hash identik dengan hasil eksekusi nb01 sebelumnya yang
  sudah direview user; tidak ada perubahan plot).
- `laporan_tahap_3_returns.md` masih menyebut nama lama — sengaja, per perintah (diperbarui di
  langkah 6 bila diminta).
- `figures/` saat ini hanya milik nb01; jika nb03/nb04 kelak menyimpan figure, penomoran
  sekuensialnya baru bisa diuji saat itu.
- Gate dijalankan pada repo dengan perubahan langkah 1–5 yang belum di-commit; `tests/` tidak
  disentuh sehingga 157 passed tetap relevan.

## 8. STOP — Tunggu Review User

Langkah 5 selesai. Berikutnya **tidak** saya kerjakan (sesuai perintah): update audit kesesuaian
dan Commit A/B = **langkah 6**; nb05 tetap terlarang sebelum commit koreksi mendarat.
