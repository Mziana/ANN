PERBAIKAN nb05 ATAS TEMUAN BATCH B — Langkah 4–6 GAGAL
(1 HIGH · 7 MEDIUM · 4 LOW + B6-04 MEDIUM + utang L3-06 LOW)

Dasar audit (sumber kebenaran, baca sebelum kerja):
`reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md` baris 1340–1800
(RE-AUDIT BATCH B, hash file `b0c98b497a6b…`). Ringkasan verifikasi asisten:
`.ai/assistant/verifications/2026-10-06_batch-B.md`.

=== BACA DULU (wajib — kamu dalam keadaan reset konteks) ===
1. Workdir absolut: `D:\ANN`. Semua path relatif terhadap ini.
2. Verifikasi titik awal — cocokkan hash ini (git hash-object). TIDAK cocok
   → STOP dan laporkan:
   - `scripts/_build_eda05.py` → `ca997cc9b70a28294dfd663deed17f2b76e8b96f`
   - `notebooks/scalping/eda_05_regimes.ipynb` → `8158d5b57b20e038164b613ab2284194d5c06992`
   - `reports/eda/2026-10-06/report.md` → `2f86eed66ea4fcf3f455b2b23ffabe447b4d0587`
   - `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md` → `131e8222a58b781f11593894a4c1fe14a6bc2f0a`
   - `reports/eda/progress/06-regimes/laporan_tahap_12_sintesis.md` → `e48c8b321ccd92d6c08c38ee8612b16bc1cbce9`
3. Baca berurutan:
   a. `.ai/STATE.md`, `.ai/TASKS.md`, `.ai/CONTEXT.md`, entri terbaru
      `.ai/SESSION_LOG.md` (posisi proyek + apa yang sudah dikerjakan —
      JANGAN kerjakan ulang yang sudah selesai);
   a. `.ai/STATE.md`, `.ai/TASKS.md`, `.ai/CONTEXT.md`, entri terbaru
      `.ai/SESSION_LOG.md` (posisi proyek + apa yang sudah dikerjakan —
      JANGAN kerjakan ulang yang sudah selesai);
   b. prompt onboarding coder
      (`.ai/assistant/prompts/2026-10-06_onboarding-coder-baru.md`,
      invarian F tetap mengikat);
   c. peta audit (`.ai/assistant/notes/2026-10-06_peta-langkah-audit_nb05.md`)
      + verifikasi asisten
      (`.ai/assistant/verifications/2026-10-06_batch-B.md`);
   d. rancangan `eda_design_v3.1.md` §11 + `:64` (M1–M4) + `:80`
      (kalender libur) → audit Batch B (baris 1340–1800).

Prasyarat: onboarding selesai (konfirmasi baca + 3 invarian dengan
kata-katamu sendiri) SEBELUM menyentuh kode.

Konteks: ANGKA hitunganmu BENAR semua (auditor replikasi ~20 baris tanpa
selisih). Yang diminta: perbaiki KESESUAIAN klaim↔metrik dan KELAYAKAN
ambang. Jangan "memperbaiki" angka yang sudah benar.

=== TEMUAN (disarikan dari audit, lokasi persis) ===

[B4-04 HIGH] H5 pakai proksi spread mean-D1 (`:532-533`, rentang antar-sesi
hanya 0,0086 pip — praktis datar) padahal M1 punya `spread_pips`/
`spread_points` PER BAR (rentang nyata 0,1883 pip) dan kanon M4 menetapkan
`spread_p95`. Akibat: `flag_biaya_mendominasi = []` palsu; dengan p95, NewYork
0,9488 & Sydney 0,7975 ter-flag. Pembela `:543` ("spread per bar tidak ada di
skema") TIDAK berlaku. Perbaikan: ganti proksi dengan spread per-bar +
p95 sesuai M4; perbarui `rasio_vol_over_spread_*`, flag, teks H5 di
builder/report.md/tahap_12. ANGKA BERUBAH → labeli "KOREKSI pasca-audit"
(pola Batch A). Data pendukung siap: `cost_basis.by_session`
(London 0,61/NY 0,69/Tokyo 0,62/Sydney 0,80) + `stress_bands` p95/p99 di
`configs/data.yaml`.

[B4-01 MEDIUM] Bucket "range" = volatilitas TERENDAH (61,32 vs 153,14),
tak didefinisikan di teks klaim (`:632-638`); uji drift absolut ikut skala
volatilitas. Perbaikan: rename bucket (mis. "volatilitas-rendah") ATAU
jelaskan eksplisit di teks klaim. JANGAN ubah angka tipologi/ambang.

[B4-02 MEDIUM] `share_Off_di_top6` mengukur "di dalam sesi", bukan
"London/NY" (jam 00 UTC 100% Tokyo; L+NY total 77,17%). Perbaikan: TAMBAH
metrik yang benar-benar menguji London/NY di samping metrik lama (jangan
hapus angka lama); sesuaikan teks klaim H4. Bila ragu bentuk metriknya →
STOP, eskalasi ke Arsitek lewat user.

[B4-03 MEDIUM] Assertion `:776` (`< 0.5`, lolos 2 Off) lebih longgar dari
kanon M2 (revisi pada ≥2 Off). Perbaikan: ketatkan assertion menegakkan M2,
ATAU tulis alasan pelonggaran bila disengaja (maka jadi pertanyaan arsitek,
bukan keputusanmu).

[B4-05 MEDIUM] `flag_biaya_mendominasi = []` → klausa "hanya … bila biaya
rendah" tanpa kontras. Perbaikan ikut B4-04: setelah p95 dipakai, tulis
ulang klausa sesuai fakta (ada/tidak sesi yang memenuhi).

[B4-06 MEDIUM] Ambang H2 "≥3 dari 4 tahun OOS" tak tereksekusi (span 3,75
tahun; 2026 = 196 hari). Perbaikan AMAN: nyatakan eksplisit ambang menunggu
data (bentuk menunggu, bukan mengubah aturan main). Bentuk ambang lain yang
mengubah kriteria → eskalasi ke Arsitek.

[B4-07 MEDIUM] Kata "terukur" (`:667-673`) tanpa uji signifikansi (semua z <
1). Perbaikan: TAMBAH uji/CI pendukung kata itu, ATAU turunkan katanya
(mis. "terhitung"). Pilih satu, tulis alasan.

[B4-12 MEDIUM] M3 (DST-aware vs cross-tab, kanon `:64`) tak dijalankan/
dilaporkan. Perbaikan: jalankan di nb05, laporkan sebagai sensitivitas
(M3 auditor hitung sendiri dan SETUJU — dampak angka nol, tapi jejak
prosesnya wajib ada).

[B4-08/09/10/11 LOW + B6-04 MEDIUM + L3-06 LOW] Redaksional, kerjakan semua:
- B4-08: nyatakan konvensi tanda Cliff's delta (A-first) di builder+report.
- B4-09: perbaiki rentang placebo (jangan rakit 2 varian; tampilkan batas
  bawah 0,4890 yang tumpang tindih real 0,490).
- B4-10: contoh "rasio tinggi" = London 2,5798 (bukan Tokyo).
- B4-11: perjelas "drawdown" (objek apa) dan "semua jam" (24 atau 6 teratas),
  atau nyatakan menunggu metode dipilih.
- B6-04: `report.md:32` → `TIDAK DIDUKUNG` (bukan BELUM DIVERIFIKASI).
- L3-06 (utang Batch A): samakan label `tahap_11:34-35` ↔ `report.md:85`
  ("CI95-iid").

=== JANGAN SENTUH (menunggu putusan user/arsitek) ===
- Angka Q1–Q6 + item #1 (S5/S6 sekunder), #2 (kalender libur), #3-bagian-Finex:
  tetap BELUM DIVERIFIKASI. DILARANG membuka nb01–nb04 atau sumber eksternal.
- Item #5, #6, #7: labelnya BENAR — tidak ada kerjaan (catatan: "belum diuji"
  H2 ikut B4-06).

=== BATAS KERJA ===
- Ubah HANYA yang diminta. Yang mengubah kriteria/aturan main (B4-02 bentuk
  metrik, B4-03 pelonggaran disengaja, B4-06 ambang baru) → eskalasi, bukan
  keputusanmu.
- Rerun penuh + gate (ruff, format, pytest, validate, foreign_chars,
  nbconvert exit=0). Lapor tabel Klaim & Bukti + hash blob baru + angka yang
  berubah (B4-04 pasti berubah — laporkan lama→baru).
- DILARANG commit. Menunggu re-audit Batch B.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness: tiap angka bersumber file:baris/output.
Putaran 2 — Bias: ada metode/disclosure disembunyikan? label jujur?
Putaran 3 — Meta: 13+2 temuan terjawab? file luar scope tersentuh?

STOP — tunggu re-audit oleh auditor.
