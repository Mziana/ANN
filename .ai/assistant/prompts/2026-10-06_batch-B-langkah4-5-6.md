BATCH B — LANGKAH 4 + 5 + 6 AUDIT nb05 (HANYA tiga langkah ini)

Konteks: Langkah 1 LULUS (`2db14c9e…`), Langkah 2 LULUS, Langkah 3 LULUS
(re-audit `c8031693…`, 5/5 temuan tertutup + bonus L2-02). Fondasi, ACF, dan
leakage dianggap beres. Tugasmu sekarang tiga lapisan berikutnya. DILARANG
menyentuh Langkah 7–10 dan DILARANG membuka materi lama (A/B/C, D1–D12,
MEDIUM/LOW lama). Dasar tiap langkah ada di
`.ai/assistant/notes/2026-10-06_peta-langkah-audit_nb05.md` — acu peta itu.

Catatan utang (JANGAN diaudit ulang, hanya dicatat): L3-06 LOW masih terbuka
(label "CI95" polos di `tahap_11:34-35` vs "CI95-iid" di `report.md:85`) —
diperbaiki digabung putaran fix berikutnya.

=== LANGKAH 4 — H1–H5 {klaim·metrik·uji·ambang} ===
Sumber: [KLAIM] C2 coder + [RANCANGAN] `eda_design_v3.1.md` §11 Kriteria
Sukses (hipotesis falsifiable).

Untuk SETIAP hipotesis H1–H5, uji empat sisi dengan bukti file:baris:
1. Klaim: apakah pernyataan hipotesisnya falsifiable (bisa salah)?
2. Metrik: apakah metrik yang dipakai mengukur klaimnya (bukan proksi yang
   melenceng)?
3. Uji: apakah uji statistiknya tepat untuk metrik itu (asumsi uji terpenuhi
   atau pelanggarannya di-disclose)?
4. Ambang: apakah ambang keputusan ditetapkan SEBELUM hasil (atau jujur
   dinyatakan ex-post bila tidak)? Waspadai ambang yang tampak "dipasang
   setelah melihat angka".

=== LANGKAH 5 — report.md ANGKA-PER-ANGKA ===
Sumber: [KLAIM] C3 + [ATURAN] AGENTS §5 (tabel Klaim & Bukti).

Telusuri SETIAP angka di `report.md` kembali ke sumbernya (output notebook /
builder / tahap_11/12): apakah angkanya sama persis (pembulatan wajar
di-disclose)? Adakah angka yang tidak punya sumber, atau sumber yang tidak
mendukung kalimatnya (mis. "tidak berbeda" padahal CI tidak memuat 0, atau
sebaliknya)? Status TERVERIFIKASI/BELUM DIVERIFIKASI di report: apakah
statusnya jujur?

=== LANGKAH 6 — 8 ITEM "BELUM DIVERIFIKASI" ===
Sumber: [KLAIM] laporan coder C3 (coder sendiri menulisnya) + [ATURAN] §20.

Coder menyatakan 8 item belum diverifikasi. Untuk tiap item: apakah masih
berstatus BELUM DIVERIFIKASI dengan benar, atau sebenarnya sudah bisa
diputus (ke TERVERIFIKASI atau ke temuan)? Jangan biarkan label "belum
diverifikasi" menjadi tempat sembunyi masalah yang sudah bisa diputus.

Di luar tiga langkah di atas: JANGAN melebar (mis. jangan menilai kualitas
metode sebagai pilihan arsitektur — itu bukan audit).

=== ATURAN BATCH (mengikat) ===
1. Objek HANYA file nb05 + blob baru (`ca997cc9…`, `8158d5b5…`,
   `2f86eed6…`, `131e8222…`, `e48c8b32…`).
2. Setiap temuan WAJIB file:baris + angka/output. Tanpa bukti = bukan temuan.
3. "Tidak sesuai rancangan" ≠ "perhitungannya salah" ≠ "kesimpulannya salah".
4. Ragu → BELUM DIVERIFIKASI + Pertanyaan untuk Coder.
5. Append ke `D:\ANN\reports\governance\2026-10-06\audit\eda_nb05_audit_v1.md`.
   Hitung hash SETELAH tulis final, sebut di chat.
6. Verdict per langkah (LULUS / PERLU PERBAIKAN) + verdict batch.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap angka/temuan bersumber file:baris/output.
Putaran 2 — Bias: apakah kamu menilai pilihan metode (tugas arsitek)
  alih-alih kebenaran/kejujuran klaim (tugas auditor)? Temuan di luar
  scope 4–6?
Putaran 3 — Meta: objek benar (nb05)? Langkah 7–10 dan materi lama tak
  tersentuh? Hash setelah final?

STOP. Batch C (Langkah 7–10) HANYA atas perintah terpisah.
