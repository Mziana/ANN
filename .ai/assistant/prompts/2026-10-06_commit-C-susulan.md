TUGAS GIT — COMMIT C SUSULAN (DOKUMENTASI RONDE FIX, TERAKHIR SEBELUM nb05).

Keputusan user: Commit A (4c914b0) + Commit B (a826ef8) sudah mendarat benar.
Sisa: laporan_tahap_8 + 6 file governance belum ter-commit. Satu commit susulan,
lalu STOP. DILARANG masuk nb05.

Sebelum eksekusi:
1. Pre-Flight: baca ulang singkat .ai/AGENTS.md (§4, §5, §8, §10 Git & Commit,
   §16, §20, §21), .ai/RULES.md, STATE.md, SESSION_LOG (entry terakhir).
   Sebut 3 aturan WAJIB paling relevan, lalu STOP tunggu konfirmasi saya.
2. Verifikasi baseline: `git log --oneline -3` (harus a826ef8 ← 4c914b0 ← e4efbfd),
   `git status --short` (tahap_8 + 6 governance masih ??).

COMMIT C — stage persis 7 file ini dari worktree (DILARANG file lain):
- reports/eda/progress/laporan_tahap_8_volatility_fix.md
- reports/governance/2026-10-06/decisions/eda_design_v3.1.md
- reports/governance/2026-10-06/decisions/eda_review_deviations_v1.md
- reports/governance/2026-10-06/audit/eda_fix_d1-d12_audit_v1.md
- reports/governance/2026-10-06/audit/eda_fix_d1-d12_reaudit_sempit_paketABC_v1.md
- reports/governance/2026-10-06/audit/eda_fragmen_spread_4b_audit_v1.md
- reports/governance/2026-10-06/audit/eda_fragmen_spread_audit_revisi_LOW-27.1.md
DILARANG ikutkan: .ai/backup/, .ai/assistant/, ASSISTANT_RULES.md,
reports/data_validation_*.md, checkpoints/, .venv/, src/, configs/, data,
notebook/builder apa pun.

Urutan: `git add` 7 path → `git diff --cached --stat` TAMPILKAN + STOP tunggu
konfirmasi saya → commit pesan `docs(eda): laporan tahap 8 + governance ronde fix D1-D12`
→ tampilkan `git log --oneline -3` + `git status --short`.

DILARANG:
- Amend commit mana pun (e4efbfd, 4c914b0, a826ef8).
- Masuk nb05 / konsumsi nb02–nb04 sebelum Commit C terverifikasi.
- Klaim tanpa bukti; skip konfirmasi sebelum commit.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness (isi commit = 7 path, dibuktikan diff --cached --stat)
Putaran 2 — Bias & Asumsi
Putaran 3 — Meta-check

=== FORMAT LAPORAN ===
diff --cached --stat (sebelum) / log -3 + status (sesudah) /
self-audit 3× ringkas / yang belum diverifikasi / STOP.

=== MULAI ===
1. Pre-Flight + baseline + sebut 3 aturan WAJIB.
2. STOP — tunggu konfirmasi saya.
3. Stage + tampilkan stat. STOP — tunggu konfirmasi commit.
4. Commit + tampilkan log/status. Lapor + STOP.
