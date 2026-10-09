TUGAS KODE BARU.

Tugas: Perbaiki 12 deviasi EDA nb00–nb04 sesuai verdict Architect
Spark v1 (reports/governance/2026-10-06/decisions/eda_review_deviations_v1.md).

Pre-Flight Check (section 0.1 AGENTS.md) — baca dulu:
- .ai/AGENTS.md (§4, §5, §8, §16, §20, §21)
- .ai/RULES.md
- .ai/CONTEXT.md
- .ai/STATE.md
- .ai/SESSION_LOG.md (entry terakhir)
- RANCANGAN EDA V.3 (checkpoints/) + eda_design_v3.1.md
- reports/eda/progress/audit_kesesuaian_nb00_nb04.md

Sebut 3 aturan WAJIB paling relevan, lalu tunggu konfirmasi saya.

=== VERDICT SPARK (TIDAK DIUBAH) ===

D1 INVALID — ACF lag 1–60 (LAGS=range(1,21) di nb03:385 → extend; assertion :824 ikut)
D2 INVALID — tegakkan Ljung-Box (scipy manual, tanpa dep baru; aturan baca:
  p tidak menyimpulkan, pakai Q/n + besaran; informatif di slice)
D3 PARTIAL — VR horizon 60 ikut ekstensi D1
D4 INVALID — tambah sign-ACF lag-1
D5 INVALID — hasil per strata A vs B (b_mask: gunakan)
D6 INVALID — frekuensi swing per hari (groupby sesi+tahun :487/:493)
D7 INVALID — waktu tahan median antar swing
D8 INVALID — rename eda_04_swing_level.ipynb → eda_04_swings_levels.ipynb
D9 INVALID — FIG-01_qq_{M1,M5,M15}.png → FIG-01/02/03.png; skema FIG-04+ sekuensial
D10 INVALID — spread_pips_max M5 untuk ekor (hanya ada di nb00 sekarang); laporkan
  berdampingan tail M1
D11 VALID — interpretasi coder sah; CATAT saja, tanpa perubahan kode
D12 PARTIAL — flag Tokyo fix 00:55 UTC + buka NYSE di nb02; eksposur zona BoJ di nb04;
  studi event KELUAR scope

=== KEPUTUSAN ===
- D2: tegakkan, jangan revisi rancangan
- D11: prasangka coder dicatat, preregistrasi tidak diubah
- D12: marker wajib minimal, event-study dilewatkan

=== URUTAN WAJIB ===
1. D8 rename + catat D11 (nol komputasi)
2. Batch nb03: D2/D4 + D1/D3 (satu konstanta) + D5 → rerun
3. nb04: D6/D7 + BoJ (D12) → rerun
4. nb02: D10 + flag fix/NYSE → rerun sel terkait
5. D9 rename + kunci skema figure
6. Update audit → review → DUA commit
   A: nb04 baru
   B: koreksi nb03/nb01/nb02
   DILARANG amend e4efbfd
   DILARANG ikutkan reports/data_validation_2026-10-06.md dan .ai/backup/
7. nb05 DILARANG konsumsi nb03 sebelum commit koreksi

=== DAMPAK KE nb03 ===
Provisional sampai commit koreksi. Arah headline mungkin stabil; kualifikasi
hampir pasti berubah; A-vs-B + lag 21–60 = info genuinely baru.
Besaran perubahan TIDAK diklaim — butuh komputasi ulang (wilayah self-audit
kamu + Klenz).

=== CATATAN TAMBAHAN ===
- Dokumen kanonik = governance; bundle checkpoints/ = scratch
- _eda_common.py DITERIMA dengan assert wajib
- figures/ saat ini hanya 3 file (tabrakan terkecil)

=== FORMAT LAPORAN (§5 AGENTS.md) ===
Laporan Fix Deviasi
- File dibuat/diubah: <path> (baru/diubah, N baris)
- Verdict vs Eksekusi: tabel D1–D12 {verdict, status FIXED/DICATAT/SKIP, bukti}
- D11: dicatat, kode tidak berubah
- Gate: ruff check, pytest, validate_data (output asli)
- Yang belum diverifikasi
- Potensi masalah
- Status: TERVERIFIKASI / BELUM DIVERIFIKASI / ASUMSI / GAGAL

=== LARANGAN ===
- Improvisasi di luar urutan
- Amend commit
- Lanjut nb05 sebelum commit koreksi
- Klaim tanpa bukti, skip self-audit, skip gate

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness
Putaran 2 — Bias & Asumsi
Putaran 3 — Meta-check

=== MULAI ===
1. Konfirmasi baca 8 file.
2. Sebut 3 aturan WAJIB paling relevan.
3. Tunggu konfirmasi saya sebelum langkah 1.
