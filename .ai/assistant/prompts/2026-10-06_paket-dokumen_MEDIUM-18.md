TUGAS KODE LANJUTAN — PAKET DOKUMEN + TEMUAN KLENZ (SEBELUM LANGKAH 6).

Keputusan user: verdict Klenz = LULUS dengan syarat. Selesaikan syarat itu dulu.
DILARANG masuk Langkah 6 (commit) sebelum paket ini direview OK.

Sebelum eksekusi:
1. Pre-Flight: baca ulang singkat .ai/AGENTS.md (§4, §5, §8, §16, §20, §21),
   .ai/RULES.md, STATE.md, SESSION_LOG (entry terakhir), dan WAJIB
   reports/governance/2026-10-06/decisions/eda_design_v3.1.md
   + laporan audit Klenz (minta user paste bila belum kamu terima).
   Sebut 3 aturan WAJIB paling relevan, lalu STOP tunggu konfirmasi saya sebelum edit.

=== PAKET A — MEDIUM-18 (sinkronisasi dokumen, WAJIB sebelum commit) ===
A1. `.ai/STATE.md`: perbarui klaim basi —
    17/17 assertion → 31/31 (nb03 hasil fix);
    20/20 → 30/30 (nb04 hasil fix);
    BUANG klaim "|ACF| ≤ 0,012 di semua TF" (terbantahkan: maks 0,0226 di B M15 lag 50);
    tulis temuan sign-ACF + ekstensi lag 21–60 sebagai temuan baru.
A2. `reports/eda/progress/audit_kesesuaian_nb00_nb04.md`: update §F —
    Langkah 1–5 selesai + verdict Klenz LULUS-bersyarat; catat konfirmasi D11 Klenz.
A3. Tulis laporan mini Langkah 2 (rework nb03 D1–D5) sebagai file BARU
    reports/eda/progress/laporan_tahap_10_autocorr_fix.md
    (bukan addendum; format §5/§20: tabel Klaim & Bukti, gate, self-audit ringkas).
A4. `.ai/SESSION_LOG.md`: tambah entri ronde fix (Langkah 1–5 + audit Klenz),
    format §0.2/§17.

=== PAKET B — LOW-34 (dead code nb02, pilih satu, konsisten) ===
File: scripts/_build_eda02.py baris 691–694.
Pilih SALAH SATU dan nyatakan pilihan di laporan:
  opsi 1 — HAPUS variabel mati mean_by_session_full + komentarnya; atau
  opsi 2 — PAKAI _full di fragmen dan biarkan Off: null eksplisit.
Setelah pilih: regenerate sel terkait nb02 bila perlu; gate ulang;
verifikasi spread_fragment.yaml tetap byte-identik (syarat lama tetap berlaku).

=== PAKET C — LOW-35 (catat R1/R2 di nb04) ===
File: scripts/_build_eda04.py (~baris 549–550, sel §3).
Tambah 2 baris markdown: agreement literal primer-vs-sekunder TIDAK akan pernah
tercapai karena offset struktural −1 (R1); hanya divergensi MELEBIHI geseran
yang = temuan (R2). Regenerate nb04; gate ulang; assertion count boleh naik,
DILARANG melemahkan assertion lama.

=== ATURAN PAKET INI ===
- Reuse-First: edit builder, regenerate via nbconvert. JANGAN edit .ipynb langsung.
- DILARANG menyentuh: nb01/nb03/nb05, figures/, audit verdict Spark, D11,
  laporan_tahap_5 (tetap menunggu Langkah 6), configs/, src/, data.
- DILARANG commit atau amend e4efbfd.
- Gate penuh per regenerate (ruff check, ruff format --check, pytest,
  validate_data, check_foreign_chars).
- Setiap sub-paket (A/B/C) = seksi sendiri di laporan + self-audit 3× ringkas.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness
Putaran 2 — Bias & Asumsi
Putaran 3 — Meta-check

=== FORMAT LAPORAN ===
File diubah (path + baris) / pilihan LOW-34 + alasan / gate output asli per
regenerate / self-audit 3× / yang belum diverifikasi / STOP.
Laporan paket ini = chat + (opsional) addendum di masing-masing file yang diubah.

=== MULAI ===
1. Pre-Flight + sebut 3 aturan WAJIB.
2. STOP — tunggu konfirmasi saya.
3. Kerjakan A → B → C berurutan.
4. Lapor + STOP. Setelah ini: re-audit sempit Klenz (3 item), baru Langkah 6.
