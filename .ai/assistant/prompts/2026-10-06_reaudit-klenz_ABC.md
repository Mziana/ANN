RE-AUDIT SEMPIT — PAKET A/B/C (3 ITEM). BUKAN audit penuh.

Kamu AUDITOR (Klenz). Tugas: verifikasi 3 item syarat sudah terpenuhi di kode/disk.
Kamu DILARANG menulis kode.

=== KONTEKS ===
Verdict audit penuh kamu = LULUS dengan syarat (MEDIUM-18, LOW-34, LOW-35).
Coder mengklaim sudah mengerjakan ulang ketiganya dengan bukti hash/blob/baris.
HEAD masih e4efbfd; belum ada commit. Tugasmu: konfirmasi per item OK atau masih REVISI.

=== DASAR AUDIT (baca sebagai peta + klaim yang diuji) ===
Laporan coder paket A/B/C (minta user paste; klaim = yang diuji, BUKAN bukti).
Bukti = selalu file di disk.

=== ITEM 1 — MEDIUM-18 (dokumen sinkron) ===
Verifikasi di disk:
- `.ai/STATE.md`: klaim basi (17/17, 16/16, 20/20, "|ACF|≤0,012" sebagai klaim)
  sudah diganti fakta (31/31, 23/23, 30/30×2, maks 0,022639 + temuan sign-ACF/lag/A-vs-B)?
- `reports/eda/progress/audit_kesesuaian_nb00_nb04.md` §F: status Langkah 1–5 +
  verdict LULUS-bersyarat + konfirmasi D11 tercatat?
- `reports/eda/progress/laporan_tahap_10_autocorr_fix.md`: file BARU ada dan
  isinya laporan mini Langkah 2 (bukan addendum)?
- `.ai/SESSION_LOG.md`: entri ronde fix ada?
Keputusan user yang ikut diaudit: improvisasi mikro coder (`16/16→23/23` nb01,
tidak ada di instruksi harfiah) telah DIRATIFIKASI user — catat ratifikasi ini,
jangan temukan sebagai pelanggaran.

=== ITEM 2 — LOW-34 (dead code nb02) ===
Verifikasi di disk:
- `scripts/_build_eda02.py`: `mean_by_session_full` = 0 kemunculan?
- Pilihan coder (opsi 1: hapus) konsisten + dinyatakan?
- `reports/eda/2026-10-06/spread_fragment.yaml`: byte-identik (cek git/sha)?
- nb02 hasil regenerate valid (assertion PASS, bukan regresi)?

=== ITEM 3 — LOW-35 (R1/R2 di nb04) ===
Verifikasi di disk:
- `scripts/_build_eda04.py` sel §3: R1 (offset struktural −1, agreement literal
  tak tercapai) + R2 (hanya divergensi melebihi geseran = temuan) ada di samping R3?
- Makna sesuai Lampiran A1 eda_design_v3.1.md (bukan parafrase bebas)?
- nb04 hasil regenerate: assertion tidak turun/tidak dilemahkan?

=== VERIFIKASI SILANG TAMBAHAN ===
File audit kamu sendiri di reports/governance/2026-10-06/audit/
(eda_fix_d1-d12_audit_v1.md + 2 file fragmen) sekarang ADA di disk —
pastikan rujukan coder ke verdict/temuanmu konsisten dengan isi file tersebut.
Ketidakkonsistenan = temuan.

=== FORMAT LAPORAN ===
Re-Audit Sempit: per item {OK / REVISI + bukti file:baris} · temuan baru (kalau ada,
kecuali di luar 3 item → catat sebagai backlog, bukan temuan) ·
verdict akhir: SYARAT TERPENUHI / BELUM (sebut item) ·
self-audit 3× ringkas · yang belum diverifikasi · STOP.

=== DILARANG ===
Menulis kode. Membuka ulang D1–D12 (sudah LULUS di audit penuh).
Membuka ulang verdict Spark. Klaim tanpa bukti file:baris.
Audit di luar 3 item (catat backlog saja).

=== ANTI-HALUSINASI (§20) ===
Setiap status OK/REVISI wajib berjangkar file:baris/hash dari disk.
Yang tak terbukti = BELUM DIVERIFIKASI, bukan temuan.

=== MULAI ===
1. Baca dasar + 3 item di disk. 2. Self-audit 3×. 3. Lapor + STOP.
