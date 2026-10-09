LANJUTAN COMMIT C — STAGE + TAMPILKAN STAT, STOP SEBELUM COMMIT.

Keputusan user: pre-flight disetujui. Kerjakan sampai SIAP commit, JANGAN commit.

1. Stage persis 7 path ini (satu per satu atau sekaligus, lalu verifikasi):
- reports/eda/progress/laporan_tahap_8_volatility_fix.md
- reports/governance/2026-10-06/decisions/eda_design_v3.1.md
- reports/governance/2026-10-06/decisions/eda_review_deviations_v1.md
- reports/governance/2026-10-06/audit/eda_fix_d1-d12_audit_v1.md
- reports/governance/2026-10-06/audit/eda_fix_d1-d12_reaudit_sempit_paketABC_v1.md
- reports/governance/2026-10-06/audit/eda_fragmen_spread_4b_audit_v1.md
- reports/governance/2026-10-06/audit/eda_fragmen_spread_audit_revisi_LOW-27.1.md

2. Verifikasi stage: `git diff --cached --stat` + `git diff --cached --name-status`.
   Pastikan: tepat 7 file (6×A + INDEX? TIDAK — INDEX tidak ikut; hanya 7 di atas),
   nol file lain, nol modifikasi (semua harus A/new file).

3. TAMPILKAN kedua output di laporan apa adanya (bukan ringkasan), lalu STOP.
   DILARANG commit. DILARANG amend. DILARANG sentuh file lain.

=== SELF-AUDIT 3× RINGKAS ===
Putaran 1 — Correctness (7 path = daftar, dibuktikan stat)
Putaran 2 — Bias & Asumsi
Putaran 3 — Meta-check

=== FORMAT LAPORAN ===
stat + name-status (verbatim) / self-audit ringkas / STOP menunggu perintah commit.
