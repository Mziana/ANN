PERBAIKAN nb05 ATAS TEMUAN BATCH A — Langkah 2 LULUS (tanpa kerjaan),
Langkah 3 PERLU PERBAIKAN (2 HIGH · 2 MEDIUM · 1 LOW)

=== BACA DULU (wajib sebelum menyentuh kode) ===
1. Workdir absolut: `D:\ANN`. Semua path di bawah relatif terhadap ini.
2. Verifikasi titik awal — cocokkan hash ini dengan file di disk (git
   hash-object). Bila TIDAK cocok, STOP dan laporkan:
   - `scripts/_build_eda05.py` → `8ac848ce2f7d1b70e78074963730b451663cf6af`
   - `notebooks/scalping/eda_05_regimes.ipynb` → `93ea76955742028f6505c7b5d1a9434362ffad12`
   - `reports/eda/2026-10-06/report.md` → `72e837778dfc0ecf8966a6c9f84344843b548fc0`
   - `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md` → `6ab21459e91e198bc038beae3aa1ac3ae35b3afe`
   - `reports/eda/progress/06-regimes/laporan_tahap_12_sintesis.md` → `eae21308c04dcca31387e5a350a24d323d4a0d2c`
3. Baca: prompt onboarding coder (`2026-10-06_onboarding-coder-baru.md`,
   harus sudah dikonfirmasi) + rancangan §11 (makna tipologi/H — penting
   untuk memutuskan L3-01a vs L3-01b) + temuan lengkap di
   `reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md` (§3.1–3.3).

Prasyarat: onboarding coder selesai dulu. Ini tugas koding pertamamu. Invarian bagian F onboarding tetap berlaku —
perbaikan ini MENAMBAH invarian, bukan melonggarkan yang lama.

Konteks: angka hitunganmu (dari coder sebelumnya) sebagian besar BENAR —
auditor menegaskan L3-05 "bukan kesalahan aritmetika pada angka yang
dilaporkan" dan kesimpulan report.md:85 tetap benar. Yang diminta: tutup
kebocoran, lengkapi resample, jujurkan label. 2 LOW Langkah 2 (L2-01 akar
insiden, L2-02 penanda dict `acf1_M15_A`) bersifat dokumentasi — kerjakan bila
murah, laporkan bila tidak.

=== TEMUAN + SARAN (verbatim auditor, Space Bunny) ===

[L3-01 HIGH] Ambang tipologi = median 825 hari A penuh (`:277-278`,
diterapkan `:298-300`): label hari-t bergantung hari setelah t = look-ahead
pada label. `:234` dan tahap_11:66 hanya bilang "deterministik" — tidak
menyatakan ambang full-sample sehingga tidak real-time-safe.
Saran (pilih satu, dengan alasan tertulis):
(a) hitung ambang walk-forward per tahun (subset terbuka); atau
(b) nyatakan eksplisit di `:234`, `:929-935`, report.md, tahap_11/12 bahwa
ambang full-sample → label bersifat ex-post, tidak real-time-safe.
PERINGATAN: opsi (a) mengubah analisis dan angka turunan (tipologi, chi2,
H1?) — bila ragu antara (a)/(b), STOP dan eskalasi lewat user ke Arsitek
(kamu DILARANG memutuskan arsitektur). Opsi (b) aman dan cukup bila tipologi
dinyatakan deskriptif.

[L3-02 HIGH] `:389` `boots[i] = median(b_vals) - median(a_vals[idx])`:
`b_vals` tak pernah di-resample → median B konstanta 10.000 iterasi → CI
block 2,3× lebih sempit dari CI iid, disajikan sahih di report.md:85.
(Kesimpulan "memuat 0" tetap benar; yang cacat CI-nya.)
Saran (pilih satu): resample `b_vals` dengan blok 20 juga
(`starts_b = b_rng.integers(0, b_vals.size, size=n_blocks_b)`), ATAU hapus
label "block bootstrap beda median B-A" → ganti "block bootstrap sisi A
saja; B dipegang pada median observasinya — CI lebih sempit, hanya mengukur
sensitivitas A".

[L3-03 MEDIUM] CI utama (`:347-352`, kolom `:361`) adalah iid tanpa penanda;
berdampingan dengan CI block di report.md:85 tanpa pembeda jenis.
Perbaikan: tandai "iid" pada kolom/output/report; dependensi sudah diakui
(`:326`, `:929-931`) — tinggal presisi label.

[L3-05 MEDIUM] Jalur M5 (`:543` tanpa `broker_time_raw`, `:556`/`:559`
searchsorted) = skema yang `:427-431` nyatakan salah untuk M15. Terukur 287
bar/287 hari bergeser (auditor hitung ulang, 269.964 bar); angka 40.483 TETAP
BENAR di kedua pemetaan; `:558` lulus tapi tak menutup 287 bar itu.
Saran: tambah `broker_time_raw` ke `:543`, pakai `wall_clock_series` +
`dt.normalize()` seperti M15, ganti `:558` dengan assertion paritas bar M5
per hari terhadap pemetaan eksak (pola `:444-445`).

[L3-04 LOW] `:381` `n_block = 20` tanpa justifikasi/sensitivitas (skema
moving-block-nya sendiri benar). Perbaikan: satu kalimat alasan +/atau uji
sensitivitas panjang blok.

=== BATAS KERJA ===
- Ubah HANYA yang diminta. Opsi yang mengubah angka (L3-01a) → eskalasi dulu.
- Rerun penuh + gate (ruff, format, pytest, validate, foreign_chars,
  nbconvert exit=0). Lapor tabel Klaim & Bukti + hash blob baru + aritmetika
  ulang yang relevan (apakah CI/angka berubah? bila ya, koreksi report dengan
  label "KOREKSI pasca-audit" seperti pola sebelumnya).
- DILARANG commit. Menunggu re-audit Langkah 3.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness: tiap angka bersumber file:baris/output.
Putaran 2 — Bias: ada metode/disclosure disembunyikan? label jujur?
Putaran 3 — Meta: 5 temuan terjawab? file luar scope tersentuh?

STOP — tunggu re-audit Langkah 3 oleh auditor.
