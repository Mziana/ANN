TUGAS KODE LANJUTAN — LANGKAH 6 (UPDATE AUDIT + ADDENDUM + DUA COMMIT).

Keputusan user: re-audit Klenz = SYARAT TERPENUHI (3/3 OK). Lampu hijau Langkah 6.
DILARANG masuk nb05 sebelum dua commit mendarat.

=== PROSEDUR ANTI-RESET KONTEKS (WAJIB PERTAMA) ===
Konteks kamu mungkin ter-reset. Sebelum apa pun:
1. Baca: .ai/AGENTS.md (§4, §5, §8, §10 Git & Commit, §16, §20, §21),
   .ai/RULES.md, .ai/CONTEXT.md, .ai/STATE.md, .ai/TASKS.md,
   .ai/SESSION_LOG.md (entry terakhir), reports/eda/progress/laporan_tahap_*.md (7–10).
2. Baca rancangan: reports/governance/2026-10-06/decisions/eda_design_v3.1.md
   + verdict eda_review_deviations_v1.md (FINAL, DILARANG re-litigasi).
3. Baca laporan re-audit Klenz:
   reports/governance/2026-10-06/audit/eda_fix_d1-d12_reaudit_sempit_paketABC_v1.md.
4. Verifikasi baseline: `git log --oneline -1` (harus e4efbfd),
   `git status --short` (catat isi index vs worktree).
5. Sebut 3 aturan WAJIB paling relevan + ringkas posisi proyek dalam 3 baris
   (bukti konteks tersambung), lalu STOP tunggu konfirmasi saya.

=== TEMUAN INDEX BASI (ditemukan paket A/B/C — tangani eksplisit) ===
Index masih memuat versi pra-L3/L4 (status AM). Karena itu:
- DILARANG mengandalkan isi index. Commit A/B WAJIB men-stage ulang dari worktree
  (`git add <path spesifik>` per file di daftar bawah, lalu verifikasi
  `git diff --cached --stat` cocok dengan daftar SEBELUM commit).
- Tunjukkan output `git status --short` + `git diff --cached --stat` di laporan
  sebagai bukti isi commit.

=== BATCH DOKUMEN (sebelum commit) ===
D1. `reports/eda/progress/laporan_tahap_5_autokorelasi.md`: ADDENDUM (bukan rewrite) —
    angka pasca-fix (31/31, lag 1–60, Ljung-Box + aturan baca, VR 5/15/60, sign-ACF,
    strata A vs B, maks |ACF| 0,022639, klaim lama DICABUT). Tandai tanggal + "addendum".
D2. `reports/eda/progress/audit_kesesuaian_nb00_nb04.md`: tutup loop —
    status final per D1–D12 + verdict Klenz + re-audit SYARAT TERPENUHI.
D3. LOW-37 (1 kalimat + 1 rujukan): di §F audit + entri SESSION_LOG, ganti catatan
    "hasil audit tidak ada di disk" dengan path
    reports/governance/2026-10-06/audit/eda_fix_d1-d12_audit_v1.md.
D4. Backlog 1 kalimat: ratifikasi T-01 "massa nol" via laporan EDA final +
    atribusi ratifikasi nb01 (16/16→23/23) di STATE/SESSION_LOG.
D5. Gate penuh setelah batch dokumen (ruff, format, pytest, validate_data,
    check_foreign_chars + scan eksplisit file .md yang diubah).

=== DUA COMMIT (setelah batch dokumen direview — TUNGGU PERINTAH SAYA per commit) ===
Aturan umum: format pesan `type(scope): ...` (§10); DILARANG amend e4efbfd;
DILARANG ikutkan: .ai/backup/, .ai/assistant/, reports/data_validation_*.md,
checkpoints/, .venv/.

Commit A — nb04 baru (minta perintah saya dulu, lalu eksekusi, lalu lapor):
  notebooks/scalping/eda_04_swings_levels.ipynb
  scripts/_build_eda04.py
  reports/eda/progress/laporan_tahap_6_swing_level.md
  reports/eda/progress/laporan_tahap_7_swing_level_fix.md
  reports/eda/progress/laporan_tahap_10_autocorr_fix.md — TIDAK (itu Commit B)
  + .ai/STATE.md? TIDAK — STATE ikut Commit B (satu commit koreksi utuh).
  Pesan: feat(eda): nb04 swings-levels + fix D6/D7/BoJ (dst., jujur).

Commit B — koreksi nb01/nb02/nb03 + dokumen (minta perintah saya dulu):
  notebooks/scalping/eda_01_returns.ipynb + scripts/_build_eda01.py
  notebooks/scalping/eda_02_volatility.ipynb + scripts/_build_eda02.py
  notebooks/scalping/eda_03_autocorr.ipynb + scripts/_build_eda03.py
  reports/eda/2026-10-06/figures/FIG-01/02/03.png (rename R)
  reports/eda/progress/laporan_tahap_9_figures_fix.md
  reports/eda/progress/laporan_tahap_10_autocorr_fix.md
  reports/eda/progress/audit_kesesuaian_nb00_nb04.md
  reports/eda/progress/laporan_tahap_5_autokorelasi.md (addendum D1)
  .ai/STATE.md, .ai/SESSION_LOG.md (D3–D4 + entri commit)
  Pesan: fix(eda): koreksi nb01/nb02/nb03 pasca-review D1–D12 (dst., jujur).

SEBELUM tiap commit tunjukkan `git diff --cached --stat` untuk
konfirmasi saya; SETELAH tiap commit tunjukkan `git log --oneline -2` + `git status`.

=== DILARANG ===
- Commit sekaligus (satu commit besar). WAJIB dua commit terpisah.
- Amend e4efbfd atau commit lain.
- Masuk nb05 / konsumsi nb02–nb04 sebelum kedua commit mendarat.
- Klaim tanpa bukti; skip gate; skip konfirmasi per commit.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness (isi commit = daftar, dibuktikan diff --cached --stat)
Putaran 2 — Bias & Asumsi
Putaran 3 — Meta-check

=== MULAI ===
1. Prosedur anti-reset + ringkas posisi (3 baris) + sebut 3 aturan WAJIB.
2. STOP — tunggu konfirmasi saya.
3. Batch dokumen D1–D5 + gate. Lapor + STOP.
4. Tunggu perintah per commit (A lalu B).
