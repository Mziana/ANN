PERTANYAAN SCOPE AUDIT nb05 UNTUK ARSITEK (Q1 + Q2 — butuh putusan)

=== PERAN + BACA DULU (kamu dalam sesi baru/reset — wajib sebelum menjawab) ===
1. Peranmu ARSITEK (§26): rancang + putuskan konflik/scope. Kamu TIDAK
   mengaudit angka (itu Auditor), TIDAK menulis kode (itu Coder).
   ABAIKAN aturan asisten (.ai/ASSISTANT_RULES.md bukan untukmu).
2. Workdir: `D:\ANN`.
3. Baca: `.ai/AGENTS.md` §1, §26, §27 (peran + arbitrase) → `.ai/STATE.md`
   + `.ai/TASKS.md` (posisi proyek) → rancangan
   `reports/governance/2026-10-06/decisions/eda_design_v3.1.md` `:80` + §8
   (sumber data) → ringkasan audit
   `.ai/assistant/verifications/2026-10-06_reaudit-batchB.md`.

Konteks: audit adversarial nb05 berjalan per batch. Langkah 1–2 LULUS,
Langkah 3 LULUS (re-audit `c8031693…`), Batch B (Langkah 4–6) LULUS DENGAN
SISA 1 LOW (`62215cb4…`, 2.113 baris). Batch C (Langkah 7–10) menunggu.
Angka hitungan nb05 benar semua; temuan Batch B soal kesesuaian klaim↔metrik.
Dokumen audit: `reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md`.
Rancangan: `reports/governance/2026-10-06/decisions/eda_design_v3.1.md`.

=== Q1 — BOLEHKAH AUDIT MEMBUKA nb01–nb04 READ-ONLY? ===
Fakta: ~16 angka di `report.md` (Q1–Q6: `:10-14`, `:28-30`, `:41-43`,
`:54-58`, `:64-66`, `:72-74`, `:103-107`) bersumber dari notebook nb00–nb04
yang di luar objek audit Batch B. Statusnya kini BELUM DIVERIFIKASI (di luar
objek) — bukan berarti salah, tapi Langkah 5 tidak akan pernah LULUS penuh
tanpa trace ini.
Pertanyaan: bolehkah auditor membuka nb01–nb04 read-only, HANYA untuk trace
angka pasif (tanpa perubahan, tanpa membuka temuan audit lama sebagai bukti)?
Rekomendasi asisten: IZINKAN (read-only, angka-saja).
Butuh putusan: YA (dengan batas apa?) / TIDAK (maka Q1–Q6 dicatat limitasi
permanen laporan).

=== Q2 — KALENDER LIBUR NYSE/TSE MASUK SCOPE ATAU DITUTUP? ===
Fakta: item #2 ("kalender libur") terputus sebagian — yang bisa dihitung dari
data sudah dihitung (824/825 hari A punya marker; 1 hari anomali 2024-08-12
perlu penjelasan missing-data; 6 hari volume-rendah terdaftar). Yang tersisa:
pencocokan ke kalender libur eksternal NYSE/TSE (sumber luar repo, tidak bisa
diaudit adversarial secara offline). Rancangan `:80` sudah mencatatnya
sebagai limitasi.
Pertanyaan: bolehkah kalender libur (sumber eksternal) masuk scope audit,
atau item ini DITUTUP permanen sebagai limitasi (`eda_design_v3.1.md:80`)?
Rekomendasi asisten: TUTUP permanen.
Butuh putusan: MASUK SCOPE (dengan sumber apa?) / TUTUP (maka item #2
ditutup dengan status limitasi).

=== BATAS PERAN ===
Kamu Arsitek: putuskan arsitektur/scope, bukan mengaudit ulang angka.
Jawab YA/TIDAK per pertanyaan + batas/syaratnya. STOP setelah menjawab.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness: jawaban merujuk fakta di atas.
Putaran 2 — Bias: tidak mengambil alih tugas auditor.
Putaran 3 — Meta: dua pertanyaan terjawab eksplisit?
