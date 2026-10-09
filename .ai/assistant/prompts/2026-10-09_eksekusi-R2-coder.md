# Brief coder -- Eksekusi spec R-2 stratifikasi tahun H4 (FINAL, disetujui user 2026-10-09, siap paste)

## S-0. Kontrak bersama + mulai sesi (WAJIB PERTAMA, sebelum satu baris pun dieksekusi)

1. Baca `.ai/AGENTS.md` v3.0 PENUH dan patuhi sebagai kontrak bersama:
   S26 (peran coder: implementasi + self-audit + fix; DILARANG menentukan
   arsitektur; DILARANG audit formal gaya auditor; DILARANG ngobrol langsung
   dengan peran lain), S5 (format laporan: tabel Klaim & Bukti), S20
   (anti-halusinasi: tiap klaim angka WAJIB output mentah ditempel; klaim
   tanpa output mentah = GAGAL), S21 (uji dulu, jangan opini).
2. Tulis konfirmasi pre-flight SATU paragraf di kepala laporan: AGENTS.md
   dibaca, HEAD terukur, staged terukur. Tanpa konfirmasi = gerbang gagal.

## S-1. Substansi verbatim arsitek

Spec: `reports/governance/2026-10-07/arsitek/spesifikasi-R2-stratifikasi.md`
blob `c04199cea2acfd692b731fcb7eacec16b0e4691d` (141 baris, gerbang LOLOS
`.ai/assistant/verifications/2026-10-09_gerbang-spec-R2.md`).

**Status spec:** PRA-REGISTRASI -- dikunci SEBELUM eksekusi; setiap
penyimpangan = STOP. **Bukan vonis:** DILARANG memvonis H4/H5 di dokumen
hasil; vonis = putusan terpisah sesudah re-audit. H5 tak tersentuh;
H1/H2/H3 FINAL; H6 nihil.

**Pertanyaan tunggal:** "Apakah efek H4 stabil antar-tahun bila pool
2024-2025 dipecah stratifikasi tahun pada jam tetap lock?"

**Lock R-2 verbatim -- GUGUR bila pada SATU PUN tahun-uji (2024, 2025):
median EV-after-cost tahun <= 0. TAHAN hanya bila KEDUA tahun:
median EV > 0. Tanpa TAK-MENENTUKAN.**

Alasan OR-gugur: sejajar lock H4b; mencegah tahun-negatif disembunyikan
pool; tanpa angka/ambang baru selain pemecahan strata yang D-2 izinkan.
Kriteria (a) n_Off DIBEKUKAN non-penentu (ESK-1 sah: inoperatif struktural
2024-2025, n_Off 0/0); dilaporkan deskriptif per tahun; DILARANG menentukan
vonis.

**Jendela + anti-intip:** evaluasi = date_broker 2024-01-01..2025-12-31
dipecah 2024 vs 2025 (pool tunggal DILARANG sebagai penentu). 2023 =
seed/history SAJA (H4 tanpa pemakaian). 2026 dikecualikan PENUH (offset
belum terverifikasi). Jam uji = jam tetap lock `[14,13,0,15,12,7]`;
DILARANG top-6 per tahun sebagai penentu (hour-shopping); DILARANG
shopping-jendela.

**Keterbatasan jujur:** R-2 termotivasi EKS-3; bobot konfirmatori terbatas;
GUGUR(R-2) BUKAN retak H4 Batch-2; TAHAN(R-2) BUKAN klaim kebal (P-5 dua
arah mengikat).

## S-2. Input beku (sha di-assert SEBELUM hitung, mismatch = STOP)

- M1 2024/2025 sha `69b2c026...`/`fce65a3a...`; M15 store `cd6a85e4...`;
  D4 labels `47d15c41...` (awalan sesuai spec; nilai penuh 64-hex
  di-assert dari provenans Batch-2 sebelum hitung; tempel perintah assert
  + outputnya).
- Mesin S-H4 Batch-2: ATR T-1, SL 1xATR, TP 2xATR, biaya by_session
  (Off->0.65 x pip 0.01), fill exact, join-gate posisional. Biaya
  by_session ditempel nilai-per-nilai. NOL konstanta diubah.
- Varian default INKLUSI; karantina F-1 5 hari counter deskriptif per
  tahun (DILARANG eksklusi lain, diputus fondasi-B D-1).

## S-3. Prosedur (stratifikasi, satu mesin, tanpa intip)

1. Pool EV HANYA pada 6 jam tetap lock, pecah 2024 vs 2025 (ATR T-1 beku,
   biaya by_session, fill exact, time-stop close terakhir hari-T).
2. Per tahun: n trade, median + mean EV, fraksi positif, exit-cause
   (SL/TP/time_stop), n_Off deskriptif (definisi Off beku).
3. Assert: loop entry HANYA `FIXED_HOURS` lock (GAGAL bila tersentuh data);
   grain hari-broker tunggal (`utc.normalize()` DILARANG).
4. Determinisme: 2x run (sha256 + `cmp` IDENTIK) + seed/toolchain/venv
   diumumkan (python 3.12.8 + versi pandas/pyarrow ditempel).

## S-4. Gerbang + perintah mentah (tiap syarat punya pasangan perintah;
## outputnya ditempel di laporan; klaim tanpa output mentah = GAGAL)

- G0 HEAD: tempel output `git rev-parse HEAD` (wajib
  `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`); bergeser = STOP.
- G-S0: tempel output `git hash-object` atas 9 file ini (bukan salin):
  spec R-2 + `reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md`
  + `reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md`
  + `reports/governance/2026-10-07/Audit/reaudit-lapisan3-H4H5.md`
  + `reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md`
  + `reports/governance/2026-10-07/arsitek/protokol-telaah-fondasi-B.md`
  + `reports/governance/2026-10-07/coder/hasil-telaah-fondasi-B.md`
  + `reports/governance/2026-10-07/arsitek/disposisi-fondasi-B.md`
  + `reports/governance/2026-10-07/arsitek/putusan-H4b-stabilitas.md`.
  8 hash S0 wajib `4a46b815...`/`f06a8e27...`/`8a4d2109...`/`e02a203b...`/
  `ed436fdd...`/`0284f5f0...`/`7d125022...`/`fe11383b...`; mismatch = STOP.
- G-staged: tempel output `git diff --cached --name-only` (wajib tepat 2 T6:
  `src/features/build_labels.py` + `tests/test_build_labels.py`) dan
  `git status --porcelain` (tunjukkan worktree). Staged != 2 = STOP sebelum
  hitung. DILARANG stage/commit/push/stash/checkout oleh sesi ini.
- G-nol-tulis: `git status --porcelain` SESUDAH vs SEBELUM identik kecuali
  satu file laporan S-5; file sementara HANYA di harness. Tempel keduanya.
- G-pytest: `venv\Scripts\python.exe -m pytest tests -q --no-header`
  FULL-SUITE (DILARANG satu file berlabel penuh); tempel rc + tail output.
- G-ruff: `venv\Scripts\python.exe -m ruff check <cakupan>` dan
  `venv\Scripts\python.exe -m ruff format --check <cakupan>` dengan cakupan
  = tiap file harness yang ditulis; tempel rc + cakupan eksplisit.
- G-foreign: `venv\Scripts\python.exe scripts\check_foreign_chars.py <file
  laporan + file harness>`; wajib rc=0; tempel rc.
- G-det: 2x run; tempel kedua sha256 + hasil `cmp` IDENTIK + toolchain.
- C8: TANPA self-hash di dokumen; hash dilaporkan di kanal luar (laporan
  + pesan serah-terima). Tempel hitung `0x` hash-artefak di isi (= 0).

## S-5. Deliverable (perintah .md + lokasi file eksplisit)

- Harness HANYA `%TEMP%\opencode\r2\` (`r2.py` -> `r2_hasil.json` + log);
  buat direktori bila belum ada. `r2_hasil.json` tinggal di harness +
  hash ditempel (pola R-4). Interpreter satu-satunya:
  `D:\ANN\venv\Scripts\python.exe` (py3.12.8).
- DILARANG tulis `src/`/`configs/`/`data/`; DILARANG `main()` di jalur
  eksekusi; DILARANG commit/push dalam bentuk apa pun.
- Laporan: `reports/governance/2026-10-07/coder/hasil-R2-stratifikasi.md`
  berisi: konfirmasi S-0, tabel Klaim & Bukti (S5), output mentah per tahun,
  hash artefak, self-audit 3x (correctness / bias & asumsi / meta-check),
  STOP. Tanpa vonis arsitek.

## S-6. Larangan bentuk-spesifik (mengikat; pelanggaran = GAGAL)

B1 tanpa vonis di dokumen hasil; B2 tanpa filter regime/sub-sel/ambang/window
pasca-hoc penentu; B3 tanpa ubah lock/ambang/vonis Batch-2/fondasi-B/H4b tanpa
addendum BARU; B4 tanpa H6; B5 tanpa `utc.normalize()`/rekonstruksi UTC; B6 tanpa
guard nilai-vs-diri (termasuk terbungkus komentar/docstring); B7 tanpa fixture
seragam klaim sensitif / test tanpa assertion yang dihitung; B8 tanpa output
parsial berlabel penuh / klaim "diuji via X" + "belum ada test X" di dokumen
sama; B9 tanpa kutip path/baris tanpa verifikasi ulang / naik severity tertutup;
B10 provenans dari sumber terpisah + sabotase ke jalur produksi persis `main()`;
B11 klaim gate format/lint sebut rc + cakupan, klaim byte-identik sebut toolchain;
B12 konstanta kalibrasi dikunci test (mutasi tanpa hitung-ulang = merah).

## S-7. Aturan baca TERTUTUP

1. Terapkan lock R-2 verbatim; tepat satu vonis: **GUGUR(R-2)** / **TAHAN(R-2)**.
2. GUGUR = tak stabil antar-tahun (satu tahun gagal cukup); DILARANG merembet
   ke TAHAN(H4 Batch-2); DILARANG tafsir-ulang via sub-sel/ambang.
3. TAHAN = stabil pada split 2024/2025 jam-tetap; DILARANG dibaca kebal umum.
4. Tanpa statistik tambahan; tanpa H5; tanpa kalibrasi; tanpa H6.

## S-8. Usulan asisten (DISETUJUI user 2026-10-09 -- bagian mengikat brief ini)

1. Lokasi resep: `sh4.py` S-H4 Batch-2 hidup di `%TEMP%\opencode\l3h4h5\`
   (terverifikasi asisten 2026-10-09: `sh4.py` 20909 B ada,
   `sh4_hasil_run1.json`/`sh4_hasil_run2.json` @1399453 B). Jangan klaim
   "file tidak ada".
2. `%TEMP%\opencode\r2\` belum ada (terverifikasi 2026-10-09) -- coder
   yang membuatnya; DILARANG menaruh file kerja di lokasi lain.
3. S0 WAJIB ukur-ulang sesi ini (S-4 G-S0); T6 staged milik
   asisten-atas-perintah-user; coder DILARANG menyentuhnya maupun menambah
   stage.

**Status:** FINAL. Siap paste ke coder -> eksekusi MASUK -> gerbang -> ronde re-audit.
