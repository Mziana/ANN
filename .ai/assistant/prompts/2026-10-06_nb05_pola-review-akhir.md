TUGAS KODE — nb05 REGIME + SINTESIS (POLA REVIEW-AKHIR).

Keputusan user: mulai nb05. Pola kerja BERUBAH: tidak ada review per checkpoint;
coder jalan C1→C4 berurutan, review + audit dilakukan SEKALI di akhir.
Syarat pola ini: bukti per checkpoint tetap wajib (laporan tanpa jejak = BATAL).

Sebelum eksekusi:
1. Pre-Flight: baca ulang .ai/AGENTS.md (§4, §5, §8, §16, §20, §21),
   .ai/RULES.md, STATE.md, SESSION_LOG (entry terakhir), dan WAJIB
   reports/governance/2026-10-06/decisions/eda_design_v3.1.md
   (§3: nb05 = Q7 + sintesis 3–5 hipotesis; §5: metrik regime; Lampiran A1: R1–R3).
   Sebut 3 aturan WAJIB paling relevan, lalu STOP tunggu konfirmasi saya.

SUBSTANSI (dari rancangan, DILARANG improvisasi):
- Q7 karakter per regime (definisi + metrik = §5 rancangan, bukan karangan).
- Sintesis seluruh rantai → draf 3–5 hipotesis H1–H5 + ambang falsifikasi.
- reports/eda/YYYY-MM-DD/report.md (isi = §3 rancangan: 7 jawaban + tabel
  Klaim & Bukti + tabel spread + H1–H5 + BELUM DIVERIFIKASI).
- Figures FIG-04+ sekuensial (skema terkunci D9: nb03→nb04→nb05; nb05 WAJIB
  verifikasi registry).
- R1–R3 Lampiran A1 wajib tercatat di nb05 (R1/R2 sudah di nb04; pastikan tidak
  hilang di nb05 + report final).
- Reuse-First: builder baru scripts/_build_eda05.py (sumber kebenaran);
  JANGAN edit .ipynb langsung. DILARANG konsumsi angka yang belum di-commit
  tanpa menyebut statusnya (nb02–nb04 sudah ter-commit A/B — boleh dipakai).

CHECKPOINT (WAJIB, tanpa STOP di antaranya — review di akhir):
- C1 regime → chat ringkas + file reports/eda/progress/06-regimes/laporan_tahap_11_regime.md
- C2 sintesis H1–H5 → chat ringkas + .../06-regimes/laporan_tahap_12_sintesis.md
- C3 report.md → chat ringkas + .../06-regimes/laporan_tahap_13_report.md
- C4 figures FIG-04+ + verifikasi registry → chat ringkas + .../06-regimes/laporan_tahap_14_figures.md
- Tiap file: tabel Klaim & Bukti checkpoint itu, angka rerun, gate per rerun,
  self-audit 3× ringkas, yang belum diverifikasi.
- ATURAN BERHENTI SENDIRI: gate merah di tengah → BERHENTI, lapor, JANGAN lanjut
  checkpoint berikutnya. Ini satu-satunya STOP di tengah jalan.

DILARANG:
- Commit atau amend (commit diputuskan terpisah setelah review akhir).
- Menulis laporan progres di luar 06-regimes/ (lihat INDEX folder progres).
- Mengubah desain/metrik/hipotesis tanpa dasar rancangan.
- Klaim tanpa bukti (path · baris · hash); skip gate.

=== SELF-AUDIT 3× (per checkpoint, ringkas) ===
Putaran 1 — Correctness / Putaran 2 — Bias & Asumsi / Putaran 3 — Meta-check

=== LAPORAN AKHIR (setelah C4) ===
Satu laporan chat konsolidasi: tabel per checkpoint (file .md + bukti +
status), gate output asli per rerun, self-audit 3×, daftar file baru/diubah,
yang belum diverifikasi, STOP menunggu review akhir + audit Klenz.

=== MULAI ===
1. Pre-Flight + sebut 3 aturan WAJIB. 2. STOP — tunggu konfirmasi saya.
3. C1→C4 berurutan (laporan .md per checkpoint, tanpa STOP).
4. Laporan akhir + STOP.
