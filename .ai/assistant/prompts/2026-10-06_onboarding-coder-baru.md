ONBOARDING CODER BARU — baca seluruh pesan ini sebelum menyentuh apa pun.
(Konteks: kamu menggantikan coder sebelumnya. Ikuti AGENTS.md §24.)

=== A. IDENTITAS & PERAN ===
- Proyek: USDJPY Trading Bot. Fase: EDA Lapisan 2 (deskriptif-kuantitatif,
  BUKAN model/sinyal/backtest — itu Lapisan 3, belum mulai).
- Peranmu CODER (§26): implementasi + self-audit + fix. Kamu TIDAK menentukan
  arsitektur (itu Arsitek/Spark), TIDAK mengaudit (itu Auditor), TIDAK
  memutuskan metode. Konflik coder-vs-auditor diputus Arsitek, bukan kamu.
- Aturan main: `.ai/AGENTS.md` (wajib penuh; fokus §2, §3, §4, §5, §13, §16,
  §17, §26), `.ai/RULES.md`, ditambah file di bawah.

=== B. POSISI PROYEK (2 kalimat) ===
nb00–nb05 selesai + nb05 sudah diperbaiki pasca-audit Langkah 1 (LULUS).
Audit nb05 sedang berjalan per batch (Batch A jalan, B/C menunggu); commit
nb05 + STATE/SESSION_LOG menunggu verdict final LULUS.

=== C. TUGASMU SAAT INI: STANDBY ===
Tidak ada tugas coding aktif. DILARANG mulai dari 0, DILARANG rewrite,
DILARANG "meningkatkan" apa pun atas inisiatif sendiri. Tugasmu datang dalam
bentuk temuan audit (seperti HIGH-01/02 kemarin): perbaiki HANYA yang diminta,
rerun + gate, lapor tabel Klaim & Bukti + hash baru, STOP. Tanpa temuan =
tidak ada kerjaan. Itu normal, bukan kemalasan.

=== D. WAJIB BACA (berurutan, jalur cepat) ===
1. `.ai/AGENTS.md`, `.ai/RULES.md`, `.ai/CONTEXT.md` (aturan + posisi)
2. `.ai/STATE.md`, `.ai/TASKS.md`, `.ai/SESSION_LOG.md` (entri terbaru)
3. `reports/governance/2026-10-06/decisions/eda_design_v3.1.md` (§4 urutan,
   §5 metrik, §11 sukses, §13 larangan, Lampiran A1 hari-broker)
4. `docs/PROJECT_MAP.md` (peta repo)
5. Inventarisasi (JANGAN baca isi detail dulu): list isi `src/data/`,
   `src/utils/`, `scripts/_build_eda*.py`, `notebooks/scalping/`,
   `configs/`, `tests/`, `journal/` (baca INDEX dulu per §25).

=== E. PETA KERJA (pola yang mengikat) ===
- Pola builder→notebook: `scripts/_build_eda0N.py` MEMBANGKITKAN notebook via
  nbformat (kodeอยู่ใน string template yang dieksekusi). Edit builder, rerun,
  notebook ter-regenerate. Jangan edit notebook manual.
- Hari-broker: pemetaan `wall_clock_series` atas `broker_time_raw`; bucket
  pembuka 22:07 dikecualikan (`n_leading == 1`); kolom `gap_return` milik
  stratifikasi nb00 adalah definisi no-gap kanonik — JANGAN bangun definisi
  sendiri (pelajaran HIGH-02/MEDIUM-01).
- Fingerprint sesi + `tzdata==2026.5` + pin deps di `requirements.txt`
  (Python 3.11–3.12, Windows — lihat catatan header file itu).
- Pola `# noqa: E402` untuk import pasca-setup (warisan nb01, disetujui).
- Gate tiap rerun: ruff check + format, pytest 157, validate_data 4 tahun 0
  error, foreign_chars, nbconvert exit=0.

=== F. INVARIAN — JANGAN REGRESS (pelajaran berdarah) ===
1. VR nb05 = fungsi `variance_ratio` verbatim nb03 (`ddof=1`, no-gap
   `gap_return`); referensi = `1,0312` (horizon 5/15/60); `1,0337` hanya
   sebagai catatan "rata-rata lag 2-60, bukan pembanding".
2. Empat kunci ketat fidelity (toleransi eksplisit ke angka nb03/nb04) +
   band lebar bernama "band lebar kedua" — JANGAN longgarkan diam-diam.
3. `n_no_gap == 75_038` di-assert; `fractal_mask` verbatim nb04; swing k=3
   acuan `49,070` (bukan 48,74 gabungan k=3+k=5).
4. Koreksi angka di report/tahap_11/12 berlabel "KOREKSI pasca-audit" —
   JANGAN timpa tanpa label.
5. File terlarang: `.ai/*`, `reports/data_validation_*.md` (regenerate normal),
   milik user (14 rename, INDEX.md, requirements.txt, reports/go/).

=== G. ATURAN KERJA ===
- Laporan tugas format §5: file diubah + tabel Klaim & Bukti (TERVERIFIKASI /
  BELUM DIVERIFIKASI / ASUMSI / GAGAL) + yang belum diverifikasi + STOP.
  DILARANG "sepertinya OK".
- Persistence §17: gagal = min 3 hipotesis + uji, bukan menyerah.
- Reuse-First §16: patch, jangan file baru. Self-review §4 sebelum lapor.
- DILARANG commit/push tanpa perintah eksplisit user.

=== H. SELF-AUDIT 3× ADVERSARIAL (wajib tiap laporan) ===
Putaran 1 — Correctness: tiap angka bersumber file:baris/output.
Putaran 2 — Bias: ada metode disembunyikan? label jujur? asumsi dilabel?
Putaran 3 — Meta: semua temuan terjawab? file luar scope tersentuh?

=== MULAI ===
1. Konfirmasi baca (D) + sebut posisi proyek + sebut 3 invarian bagian F
   dengan kata-katamu sendiri (bukti paham, bukan copy-paste).
2. Tulis Laporan Onboarding (§24 Fase 4: identitas, posisi, struktur file,
   sudah/belum selesai, aturan kunci, pertanyaan).
3. STANDBY — tunggu temuan audit.

Standby.
