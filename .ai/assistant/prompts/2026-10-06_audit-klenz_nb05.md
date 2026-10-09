PENGINGAT ATURAN + RE-ORIENTASI.
Konteks kamu ter-reset. Baca ulang:
- .ai/AGENTS.md (fokus §5 Laporan, §18 Template Audit, §20 Anti-Halusinasi, §21 Empiris, §26 Workflow Multi-AI — kamu AUDITOR, bukan coder)
- .ai/RULES.md
- .ai/CONTEXT.md
- .ai/STATE.md (bagian Lapisan 2 / Langkah 7 — nb05)
- .ai/SESSION_LOG.md (terbaru)

WAJIB BACA RANCANGAN:
reports/governance/2026-10-06/decisions/eda_design_v3.1.md (§3 tujuh pertanyaan, §5 metrik, §11 H1–H5 + ambang falsifikasi, A1)

Konfirmasi:
- [ ] AGENTS.md dibaca
- [ ] RULES.md dibaca
- [ ] CONTEXT.md dibaca
- [ ] STATE.md dibaca
- [ ] SESSION_LOG.md dibaca
- [ ] eda_design_v3.1.md dibaca

3 aturan WAJIB paling relevan:
1. <sebut>
2. <sebut>
3. <sebut>

=== ATURAN DISIPLIN AUDIT (WAJIB) ===

1. Kamu AUDITOR. Tugas: MENCARI YANG SALAH. DILARANG menulis kode.
2. Setiap temuan WAJIB bukti (file:baris + output). Tanpa bukti = bukan temuan.
3. "Tidak sesuai rancangan" ≠ "perhitungannya salah" ≠ "kesimpulannya salah". Pakai hanya klaim yang didukung bukti.
4. Kalau ragu → tulis BELUM DIVERIFIKASI + Pertanyaan untuk Coder. Jangan mengarang.
5. DILARANG memuji tanpa data. DILARANG "sepertinya OK".

=== STATUS ===

✅ nb00–nb04 selesai + ter-commit (HEAD `cb08cd5`).
✅ 12 deviasi di-fix + ter-commit (A=`4c914b0`, B=`a826ef8`, C=`cb08cd5`).
✅ nb05 C1→C4 selesai (untracked): builder + notebook 25 sel + tahap 11/12/13/14 + report.md + FIG-04..07.
✅ Verifikasi disk asisten: 7/7 hash MATCH, HEAD utuh (bukan audit angka — itu jatahmu).
🚧 Tugasmu: audit adversarial nb05 + report.md sebelum commit.

=== FILE (path lengkap, ada di disk) ===

- D:\ANN\scripts\_build_eda05.py (blob `cc73f7943077`)
- D:\ANN\notebooks\scalping\eda_05_regimes.ipynb (blob `1155e6de3de6`)
- D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_11_regime.md (`4f7aea67fdc8`)
- D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_12_sintesis.md (`e9c23cc69d3b`)
- D:\ANN\reports\eda\2026-10-06\report.md (`51d14a352fb0`)
- D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_13_report.md (`ad6652b7a0aa`)
- D:\ANN\reports\eda\2026-10-06\figures\FIG-04.png (`3420bca32643`)
- D:\ANN\reports\eda\2026-10-06\figures\FIG-05.png (`fedd896ff8a2`)
- D:\ANN\reports\eda\2026-10-06\figures\FIG-06.png (`124867c6620c`)
- D:\ANN\reports\eda\2026-10-06\figures\FIG-07.png (`a90a16b0e40d`)
- D:\ANN\reports\eda\progress\06-regimes\laporan_tahap_14_figures.md (`85b958d133db`)

=== KLAIM CODER (JANGAN percaya — verifikasi satu per satu) ===

- C1: nb05 25 sel/18 kode, 53 assertion PASS, nbconvert exit=0; strata 825/130/19 hari; chi2 p=0,325; RV B/A=1,59× (δ=−0,384); block bootstrap marginal.
- Replica: ACF lag-1 M15-A besaran +0,0018; sign-ACF −0,022005 (ref nb03 −0,022624, "dalam band"); VR 1,0277 (ref 1,0337); swing 49,07/hari (ref nb04).
- Insiden ACF: −0,022624 ternyata sign-ACF (metrik tanda, D4 nb03), bukan ACF besaran. Resolusi: kunci KEDUA angka.
- Gate final: ruff bersih 31 file · pytest 157 passed · validate 0 error ×4 tahun · foreign_chars OK 79 file. (Rerun #4 sempat ruff MERAH F541+E402 ×2 → diperbaiki pola `# noqa: E402` nb01.)
- C2: H1–H5 {klaim·metrik·uji·ambang falsifikasi}, nol hipotesis tanpa metrik (§11).
- C3: report.md = 7 jawaban + tabel Klaim & Bukti + tabel spread + H1–H5 + ratifikasi T-01 (5,83%) + 8 item BELUM DIVERIFIKASI + catatan R1–R4.
- C4: registry tepat FIG-01..07; FIG-01..03 byte-identik blob HEAD.
- Temuan jujur: ranking sesi Tokyo 1,439 > NewYork 1,139; proksi spread mean-D1 = ASUMSI-PROKSI; temuan negatif Q6 dipertahankan.
- Riwayat 4 perbaikan: (1) bucket pembuka M15/M5 pra-bar-M1 → pencarian interval + assert pengecualian=1; (2) fractal_mask salah → salinan verbatim nb04; (3) KeyError hour_utc → 1 baris; (4) ruff → lihat gate.
- HEAD tetap cb08cd5, semua deliverable untracked.

=== URUTAN AUDIT ===

1. Replica fidelity: cocokkan ACF +0,0018 / sign-ACF −0,022005 / VR 1,0277 / swing 49,07 dengan output nb03/nb04 di disk (baca langsung, jangan percaya klaim).
2. Insiden salah-baca ACF: resolusi "dua metrik berbeda" benar, atau masih ada inkonsistensi tersembunyi?
3. Look-ahead/leakage: pelabelan regime, block bootstrap, agregasi hari-broker.
4. H1–H5: tiap hipotesis punya {klaim·metrik·uji·ambang}? Adakah tanpa metrik?
5. report.md: telusuri tiap angka ke output notebook; tandai yang tak tertelusur.
6. 8 item BELUM DIVERIFIKASI: wajar, atau seharusnya sudah bisa diverifikasi?
7. Registry FIG-01..07 tepat? FIG-01..03 tak tersentuh?
8. Temuan jujur (ranking sesi, proksi spread, Q6 negatif): adil atau ada framing?
9. Perbaikan akar 4 bug riwayat: benar dan tuntas, atau ada sisa?
10. Konvensi RULES.md, anti-pattern (§19), Reuse-First (§16).

=== OUTPUT WAJIB (arsip audit) ===

Simpan laporan audit final ke:
D:\ANN\reports\governance\2026-10-06\audit\eda_nb05_audit_v1.md
(pola nama sama seperti eda_fix_d1-d12_audit_v1.md; bila revisi → _v2, dst.
DILARANG menimpa file audit lama.)

Laporan di chat = ringkasan + verdict; versi lengkap WAJIB tersimpan di file itu.
STOP baru sah setelah file tersimpan (sebutkan path + blob hash-nya di chat).

=== FORMAT LAPORAN ===

## Laporan Audit nb05

### Ringkasan
- File: <list>
- Jumlah temuan: <N>
- Verdict: LULUS / PERLU PERBAIKAN / TOLAK

### Temuan
[CRITICAL-01] <judul>
Lokasi: <file>:<baris>
Masalah: <deskripsi>
Bukti: <bukti>
Dampak: <akibat>
Saran: <perbaikan>

[HIGH-01] ... / [MEDIUM-01] ... / [LOW-01] ...

### Yang Sudah Benar
- <singkat, dengan alasan>

### Pertanyaan untuk Coder
- <kalau ada>

### STOP — Tunggu Keputusan User

=== DILARANG ===
- Menulis kode (peranmu AUDITOR, §26).
- Verdict tanpa bukti per temuan.
- "Sepertinya OK" / memuji tanpa data.
- Skip item urutan audit.
- Mengarang angka atau isi file.

=== MULAI (wajib bertahap — DILARANG sekaligus) ===

Kerjakan HANYA LANGKAH 1 dulu, lalu STOP dan tunggu perintah:
1. Konfirmasi baca 6 file (termasuk rancangan).
2. Sebut 3 aturan WAJIB.
3. Langkah 1 (replica fidelity) + simpan progres ke eda_nb05_audit_v1.md
   (boleh parsial, tandai "DRAF LANGKAH 1").
4. STOP, tunggu perintah langkah 2.

Langkah 2–10 HANYA atas perintah eksplisit per langkah.

=== ANTI-RELAPS (pelajaran 2 putaran gagal) ===
- A/B/C, D1–D12, MEDIUM-18, LOW-34/35/36/37, Langkah 6: SUDAH SELESAI, ARSIP
  FINAL. Menyebutnya lebih dari SATU kalimat = pelanggaran perintah.
- Setiap respons WAJIB memuat minimal 1 bukti baca file nb05 (kutip
  file:baris + angka dari output). Respons tanpa bukti baca = belum bekerja.

Standby.
