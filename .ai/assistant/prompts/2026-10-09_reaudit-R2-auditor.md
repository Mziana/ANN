# Brief auditor independen R-2 -- replikasi dari nol + audit adversarial (FINAL, disetujui user 2026-10-09, siap paste)

## Konteks (fakta, bukan instruksi)

Eksekusi coder R-2 selesai + gerbang LOLOS.
Dokumen hasil: `reports/governance/2026-10-07/coder/hasil-R2-stratifikasi.md`
(226 baris / 9811 byte / LF-only / ASCII -- asisten verifikasi ke disk:
blob `c2f799138593e7ea1a8f2da6901c9f818e60b731`,
HEAD `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` tetap,
staged tetap 2 T6 tak tersentuh, nol commit).
Vonis mekanis coder (BUKAN vonis resmi): **GUGUR(R-2)** -- tahun_gugur
[2025]; 2024 n 1560 median +0.04834999999999022 (87/9/1464);
2025 n 1554 median -0.005049999999992838 (71/6/1477); n_Off 0/0 per tahun;
F1 30 trade (2024) / 0 trade (2025); tepat satu vonis; tanpa H6.
Spec kontrak: `arsitek/spesifikasi-R2-stratifikasi.md` (blob `c04199ce`, 141 baris).
Tugasmu: AUDIT INDEPENDEN hasil eksekusi vs spec -- replikasi angka dari
sumber (parquet/resep/harness), bukan dari narasi coder. Vonis resmi R-2
tetap wewenang arsitek pada ronde putusan terpisah.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

- Kamu AUDITOR adversarial (kontrak bersama `.ai/AGENTS.md` S18, S20,
  S21, S26): memverifikasi kebenaran dan kejujuran klaim dengan bukti
  independen. Replikasi angka dari sumber, bukan dari dokumen.
- Kamu BUKAN coder: DILARANG menulis/mengubah kode. SATU-SATUNYA tulis
  yang diizinkan adalah file audit di bawah. Pengecualian: skrip probe
  SEMENTARA hanya di `%TEMP%\opencode\r2_audit\` (tidak di repo, tidak
  di-commit, dilaporkan path-nya) -- dan hanya bila hitung-ulang butuh
  eksekusi.
- Kamu BUKAN arsitek: DILARANG menilai kualitas lock OR-gugur sebagai
  pilihan arsitektur (mis. "seharusnya ambang lain", "seharusnya
  TAK-MENENTUKAN"). Yang diaudit: apakah eksekusi sesuai spec + apakah
  klaim jujur. Keraguan desain = eskalasi arsitek, bukan temuan.
- Kamu BUKAN asisten.
- Workdir: `D:\ANN`. Interpreter: `venv/Scripts/python.exe` (py3.12.8).

## Hash titik-awal (verifikasi dulu, TIDAK cocok -> STOP)

- Dokumen hasil: `c2f799138593e7ea1a8f2da6901c9f818e60b731` (226 baris / 9811 byte)
- Spec R-2: `c04199cea2acfd692b731fcb7eacec16b0e4691d` (141 baris)
- 8 hash S0: `4a46b815` / `f06a8e27` / `8a4d2109` / `e02a203b` /
  `ed436fdd` / `0284f5f0` / `7d125022` / `fe11383b`
- HEAD: `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`
- Harness + JSON di `%TEMP%\opencode\r2`: `r2.py` (14211 B);
  artefak terverifikasi asisten: `r2_hasil.json` = run1 = run2 @1356769 B,
  sha `4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4`
- Input beku (assert ulang nilai penuh): M1 2024 `69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac`,
  M1 2025 `fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af`,
  M15 store `cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb`,
  D4 `47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c`

## Lingkup audit (hanya ini)

Setiap butir: COCOK / TIDAK COCOK / BELUM DIVERIFIKASI + bukti
file:baris/output. Tanpa bukti = bukan temuan. Bedakan: tidak-sama !=
tidak-sesuai-spec != salah-hitung != kesimpulan-salah. False positive
yang kamu batalkan sendiri DICATAT terbuka.

**A1 -- Replikasi independen dari nol, kedua tahun.**
Bangun ulang dari parquet + resep S-H4 (baca `r2.py` dan `sh4.py`
baris-per-baris, JANGAN impor kode coder untuk replikasi):
(a) join-gate -- klaim n 47721=47721, sekuens identik, ATR exact 974 hari,
pool 519 hari-broker; (b) per tahun -- klaim 2024 n 1560 (87/9/1464)
median `0.04834999999999022` vs 2025 n 1554 (71/6/1477) median
`-0.005049999999992838` digit-terakhir, plus mean dan fraksi positif;
(c) n_Off deskriptif + n_fallback -- klaim 0/0 kedua tahun;
(d) counter F1 -- klaim 30 trade (2024) / 0 trade (2025) + 5 tanggal
`2024-10-28..11-01`. Tiap angka: COCOK atau temuan.

**A2 -- Gate anti-intip benar-benar menggigit.**
Verifikasi dari kode: loop entry HANYA `FIXED_HOURS` lock yang di-assert
`== [14,13,0,15,12,7]`; grain hari-broker tunggal; `utc.normalize()`
nol kemunculan; pool tunggal tidak dipakai sebagai penentu (grep +
review kode). Uji adversarial: apakah ada jalur baca data tahun-uji
sebelum penguncian; apakah top-6 per tahun dihitung ulang sebagai
penentu tersembunyi. Putuskan: gate efektif vs dekoratif. Temuan
gate = HIGH + eskalasi arsitek.

**A3 -- Definisi Off beku + penerapan lock.**
Verifikasi definisi Off = P1 Batch-2 (bar session_label "Off" pada jam
terkunci) dari kode, bukan dari prosa; hitung-ulang n_Off per tahun
dari pool M1. Verifikasi penerapan lock verbatim: tepat satu vonis
GUGUR(R-2) mengikuti "SATU PUN tahun-uji"; tidak ada statistik
keputusan tambahan di laporan coder.

**A4 -- Batas scope (anti-merambat).**
Verifikasi: GUGUR(R-2) tidak merembet ke TAHAN(H4 Batch-2) di seluruh
dokumen (cek tiap kemunculan "H4"); "H6" hanya sitir larangan (verifikasi
ulang path/baris, bisa bergeser); data 2026 nol kemunculan di hitungan
MAUPUN deskriptif (grep independen); filter regime/`rv_regime_flag`/TAU
tidak diaktifkan (grep + review kode); tanpa kalibrasi ambang.

**A5 -- Karantina F-1 + klaim tiga-rekaman-sepakat.**
Verifikasi counter deskriptif 30 (2024) / 0 (2025) dari data; INKLUSI
default (tanpa drop di kode); 5 tanggal = jendela F-1 fondasi-B
`2024-10-28..11-01` (sumber terpisah, bukan kalimat coder). Periksa
klaim "tiga rekaman sepakat" (JSON run ini + JSON Batch-2 + bacaan
spec S-V(b)): bangun angka dari ketiga sumber secara independen;
putuskan penjelasan sah vs kebetulan yang diklaim-menjadi-bukti.
Kecocokan digit-per-digit adalah hal yang paling wajib dicurigai,
bukan paling boleh dipercaya.

**A6 -- Determinisme (run-ulang).**
Jalankan ulang `r2.py` (atau bangun-ulang independen + justifikasi
tertulis bila biaya prohibitif -- JSON ~1.35 MB, jadi run-ulang penuh
diharapkan). Bandingkan sha256 vs
`4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4`.
Klaim byte-identik menyebut versi toolchain; bila beda -> catat
sebagai metadata, bukan temuan.

**A7 -- Integritas dokumen (ringan; gerbang asisten sudah LOLOS).**
Konfirmasi struktural: S-0 + gerbang + SHA + mesin + output per tahun +
karantina + aturan baca + mutu + Klaim & Bukti + self-audit 3x + STOP;
pengikatan eksternal (tanpa self-hash di dokumen). Hanya laporkan bila
ada yang retak.

## Larangan bentuk-spesifik (mengikat; disalin eksplisit dari pelajaran audit)

1. DILARANG `utc.normalize()` / merekonstruksi hari dari UTC.
2. DILARANG membandingkan nilai dengan dirinya sendiri dalam guard
   (`allclose(X, X)` benar untuk setiap X) -- termasuk via oper kolom frame sama.
3. DILARANG fixture seragam untuk test sensitif-parameter; DILARANG test tanpa
   assertion masuk total klaim.
4. DILARANG menempel output parsial (satu file) berlabel proses penuh.
5. DILARANG klaim "diuji via X" di satu bagian sambil "belum ada test X" di bagian lain.
6. DILARANG menaikkan severity temuan yang sudah tertutup.
7. DILARANG kutipan baris/path tanpa verifikasi ulang.
8. Guard provenans WAJIB baca referensi dari sumber terpisah dari objek yang
   diperiksa; sabotase pembuktian WAJIB lewat jalur produksi persis `main()`.
9. Klaim gate WAJIB rc + cakupan (repo vs file).
10. Klaim byte-identik WAJIB sebut versi toolchain.
11. Konstanta kalibrasi WAJIB terikat test (mutasi harus merah).
12. Temuan WAJIB file:baris + angka/output.

## Tugas tulis (satu-satunya tulis yang diizinkan)

Tulis laporan audit sebagai file .md:
`reports/governance/2026-10-07/Audit/reaudit-R2-stratifikasi.md`
berisi: tabel Klaim & Bukti per A1--A7 + verdict per butir + temuan
bernomor (H/M/L) + eskalasi arsitek yang eksplisit (apa pun yang
menyentuh ambang/vonis) + verdict keseluruhan
(LULUS / LULUS DENGAN CATATAN / GAGAL) + hash file dihitung SETELAH
tulis final + STOP. DILARANG commit/push. DILARANG memulai ronde
berikutnya. DILARANG menulis vonis resmi R-2 (itu wewenang arsitek
pada ronde putusan) -- verdict-mu tentang kebenaran eksekusi, bukan
tentang nasib R-2.

=== SELF-AUDIT 3x ADVERSARIAL (sebelum STOP) ===
Putaran 1 -- Correctness: tiap angka replikasi bersumber file:baris/output
mentah; A6 output ditempel (bukan "dijelaskan"); hash audit setelah final.
Putaran 2 -- Bias & Asumsi: apakah kamu menilai desain (arsitek) atau kejujuran
klaim (auditor)? Apakah butir di luar A1--A7 ikut divonis? Apakah severity
temuan proporsional dengan dampak ke vonis?
Putaran 3 -- Meta-check: objek benar (hasil `c2f79913` + spec `c04199ce`)?
Hanya file audit (+ probe `%TEMP%` bila ada) yang ditulis? ADM fail = file
tak ada / klaim tanpa bukti / di luar lingkup tanpa label?

STOP. Putusan resmi R-2 HANYA atas perintah terpisah.

=== USULAN TAMBAHAN DARI ASISTEN ===

(DISETUJUI user 2026-10-09 -- U-1-U-3 digabung sah, bagian mengikat brief ini):

1. Probe SEMENTARA hanya di `%TEMP%\opencode\r2_audit\` (bukan `r2` --
   direktori coder jangan dipakai ulang agar artefak tidak tercampur).
   Alasan: isolasi artefak ronde; R-4 R-2 tetap murni.

2. S0 sesi auditor WAJIB hash titik-awal di atas (dok hasil `c2f79913` +
   spec R-2 `c04199ce` + 8 hash S0 + HEAD `e0b2b9f9` + branch aktif
   ditempel); staged wajib tetap 2 berkas T6 tak tersentuh --
   bila staged != 2, STOP dan laporkan sebelum audit.
   Alasan: T6 staged milik asisten-atas-perintah-user; auditor dilarang
   menyentuhnya maupun menambah stage.

3. Klaim "tiga rekaman sepakat" (A5) wajib diperlakukan sebagai klaim yang
   diaudit, BUKAN fakta diterima -- auditor membangun angka dari ketiga
   sumber secara independen.
   Alasan: pelajaran T1 (prosa != angka); kecocokan digit-per-digit
   adalah hal yang paling wajib dicurigai, bukan paling boleh dipercaya.

**Status:** FINAL. Siap paste ke auditor -> audit MASUK -> gerbang -> ronde putusan arsitek.
