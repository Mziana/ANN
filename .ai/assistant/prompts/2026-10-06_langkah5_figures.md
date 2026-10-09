TUGAS KODE LANJUTAN — LANGKAH 5 (RENAME FIGURE D9 + KUNCI SKEMA).

Keputusan user: Langkah 1–4 selesai, direview OK. Kerjakan Langkah 5 saja.
STOP setelah Langkah 5. Jangan update audit kesesuaian, jangan commit (itu Langkah 6).

Sebelum eksekusi:
1. Pre-Flight: baca ulang singkat .ai/AGENTS.md (§4, §5, §8, §16, §20, §21),
   .ai/RULES.md, STATE.md, SESSION_LOG (entry terakhir), dan WAJIB
   reports/governance/2026-10-06/decisions/eda_review_deviations_v1.md (D9)
   + eda_design_v3.1.md baris 46 (FIG-01.png s/d FIG-NN.png, satu grafik satu pesan).
   Sebut 3 aturan WAJIB paling relevan, lalu STOP tunggu konfirmasi saya sebelum edit.

LANGKAH 5 — D9 (nol komputasi statistik):
- Rename: reports/eda/2026-10-06/figures/FIG-01_qq_M1.png → FIG-01.png;
  FIG-01_qq_M5.png → FIG-02.png; FIG-01_qq_M15.png → FIG-03.png
  (urutan mengikuti loop Q1_TIMEFRAMES M1/M5/M15).
- Reuse-First: source of truth = scripts/_build_eda01.py (baris ~532:
  path = FIGURE_DIR / f"FIG-01_qq_{timeframe}.png"). Patch builder memakai
  penomoran berurutan (enumerate) agar regenerasi mendatang TIDAK mengembalikan
  nama lama. JANGAN edit .ipynb langsung.
- Regenerate nb01 via nbconvert (atau git mv + regenerate — pilih yang membuat
  builder dan file hasil konsisten; nyatakan pilihan di laporan).
- Perbarui rujukan nama di nb01 (sel markdown/output "tersimpan:", ~baris 963–965, 999)
  agar menunjuk FIG-01/02/03.
- Kunci skema: catat di laporan langkah ini bahwa FIG-01..03 = nb01 (M1/M5/M15),
  FIG-04+ = nb03 → nb04 → nb05 secara sekuensial. Skema ini mengikat builder
  nb03/nb04/nb05 berikutnya.
- Verifikasi: nama lama 0 hit di notebooks/ dan scripts/ (grep FIG-01_qq_);
  figures/ berisi tepat FIG-01/02/03.png; tidak ada file ganda.

DILARANG:
- Menyentuh nb02/nb03/nb04/nb05, audit_kesesuaian_nb00_nb04.md, laporan_tahap_5,
  laporan_tahap_2/3/6/7/8, configs/, src/, data.
- Commit atau amend e4efbfd.
- Klaim tanpa bukti; skip gate.

Gate: ruff check, ruff format --check, pytest, check_foreign_chars (termasuk file laporan baru bila ada).

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness
Putaran 2 — Bias & Asumsi
Putaran 3 — Meta-check

Format laporan: file yang diubah (path), tabel D9 FIXED + bukti (ls figures/, grep 0 hit),
skema FIG yang dikunci, gate output asli, self-audit 3×, yang belum diverifikasi, STOP.
Laporan .md langkah ini = file BARU di reports/eda/progress/
(laporan_tahap_9_figures_fix.md), bukan addendum.
