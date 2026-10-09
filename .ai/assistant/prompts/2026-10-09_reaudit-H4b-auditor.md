# Brief auditor independen H4b — replikasi dari nol + audit adversarial — 2026-10-09

## Konteks (fakta, bukan instruksi)

Eksekusi coder H4b selesai + gerbang LOLOS.
Dokumen hasil: `reports/governance/2026-10-07/coder/hasil-H4b-stabilitas.md`
(259 baris / 14015 byte / LF-only / ASCII — asisten verifikasi ke disk:
blob `6410b1800f6dc46ec511949e1311fcda853b0807`,
HEAD `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` tetap di branch
`codex/ANN`, staged tetap 2 T6 tak tersentuh, nol commit).
Vonis mekanis coder (BUKAN vonis resmi): **GUGUR(H4b)** — Maju median
−0,005049999999992838 ≤ 0; Mundur +0,05439999999999045; n_Off 0/0;
top-6 selisih simetris {1,7}; tepat satu vonis; tanpa H6.
Spec kontrak: `arsitek/spesifikasi-H4b-stabilitas.md` (blob `0437b563`, 108 baris).
Tugasmu: AUDIT INDEPENDEN hasil eksekusi vs spec — replikasi angka dari
sumber (parquet/kode/harness), bukan dari narasi coder. Vonis resmi H4b
tetap wewenang arsitek pada ronde putusan terpisah.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

- Kamu AUDITOR adversarial (kontrak bersama `.ai/AGENTS.md` §18, §20,
  §21, §26): memverifikasi kebenaran dan kejujuran klaim dengan bukti
  independen. Replikasi angka dari sumber, bukan dari dokumen.
- Kamu BUKAN coder: DILARANG menulis/mengubah kode. SATU-SATUNYA tulis
  yang diizinkan adalah file audit di bawah. Pengecualian: skrip probe
  SEMENTARA hanya di `%TEMP%\opencode\h4b_audit\` (tidak di repo, tidak
  di-commit, dilaporkan path-nya) — dan hanya bila hitung-ulang butuh
  eksekusi.
- Kamu BUKAN arsitek: DILARANG menilai kualitas desain dua-arah sebagai
  pilihan arsitektur (mis. "seharusnya tiga tahun", "seharusnya ambang
  lain"). Yang diaudit: apakah eksekusi sesuai spec + apakah klaim
  jujur. Keraguan desain = eskalasi arsitek, bukan temuan.
- Kamu BUKAN asisten.
- Workdir: `D:\ANN`. Interpreter: `venv/Scripts/python.exe`.

## Hash titik-awal (verifikasi dulu, TIDAK cocok → STOP)

- Dokumen hasil: `6410b1800f6dc46ec511949e1311fcda853b0807` (259 baris / 14015 byte)
- Spec H4b: `0437b563c85e578567eb58b8cfe6b0dd3ef02b47` (108 baris)
- 4 blob Batch-2: `4a46b815` / `f06a8e27` / `8a4d2109` / `e02a203b`
- HEAD: `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` (branch `codex/ANN`)
- Harness + JSON di `%TEMP%\opencode\h4b`: `h4b.py`;
  artefak terverifikasi asisten: maju blob `7975db73490d787132ac60ff5ec0cf3db6fd416c`,
  mundur blob `138d902531866771e0607895e90ec1f8b9c61a8b`
- Input beku (assert ulang): M1 2024 `69b2c026…`, M1 2025 `fce65a3a…`,
  M15 store `cd6a85e4…`, D4 `47d15c41…`

## Lingkup audit (hanya ini)

Setiap butir: COCOK / TIDAK COCOK / BELUM DIVERIFIKASI + bukti
file:baris/output. Tanpa bukti = bukan temuan. Bedakan: tidak-sama ≠
tidak-sesuai-spec ≠ salah-hitung ≠ kesimpulan-salah. False positive
yang kamu batalkan sendiri DICATAT terbuka.

**A1 — Replikasi independen dari nol, kedua arah.**
Bangun ulang dari parquet + resep mesin (baca `h4b.py` baris-per-baris,
JANGAN impor kode coder untuk replikasi): (a) top-6 train — klaim Maju
`[14,13,12,0,15,7]` vs Mundur `[14,13,0,15,1,12]`, selisih simetris
`{1,7}`; (b) pool uji — klaim n 1554 (71/6/1477) vs 1560 (94/12/1454);
(c) median EV — klaim `−0.005049999999992838` vs `+0.05439999999999045`
digit-terakhir; (d) n_Off/any_off/maj_off — klaim 0/0/0 kedua arah +
rincian per-jam off/n. Tiap angka: COCOK atau temuan.

**A2 — Gate anti-intip benar-benar menggigit.**
Verifikasi 3 lapis assert dari kode (pool train/uji murni per tahun;
daftar terkunci sebagai tuple; pasca-loop trade ∈ jam terkunci +
ranking identik ulang). Uji adversarial: apakah ada jalur baca data
uji sebelum penguncian (mis. ranking dihitung dari pool gabungan lalu
difilter)? Putuskan: gate efektif vs dekoratif. Temuan gate = HIGH +
eskalasi arsitek.

**A3 — Definisi Off beku + penerapan lock.**
Verifikasi definisi Off = P1 Batch-2 (bar session_label "Off" pada jam
terkunci) dari kode, bukan dari prosa; hitung-ulang n_Off kedua arah
dari pool M1 tahun-uji. Verifikasi penerapan lock verbatim: tepat satu
vonis GUGUR(H4b) mengikuti "SATU PUN tahun-uji"; tidak ada statistik
keputusan tambahan di laporan coder.

**A4 — Batas scope (anti-merambat).**
Verifikasi: GUGUR(H4b) tidak merembet ke TAHAN(H4) di seluruh dokumen
(cek tiap kemunculan "H4"); "H6" hanya sitir larangan (klaim coder:
4 kemunculan `:12,:156,:205,:250` — verifikasi ulang, path/baris bisa
bergeser); data 2026 nol kemunculan di hitungan MAUPUN deskriptif
(grep independen); `rv_regime_flag`/TAU tidak diaktifkan (grep +
review kode); tanpa kalibrasi ambang.

**A5 — Karantina F-1 + klaim cross-validasi.**
Verifikasi counter deskriptif Maju 0 / Mundur 30 dari data; INKLUSI
default (tanpa drop di kode). Periksa klaim "pool Maju = set jam E1
Batch-2 → angka identik = cross-validasi": verifikasi SET jam dari
kedua sumber independen (bukan dari kalimat coder); putuskan
penjelasan sah vs kebetulan yang diklaim-menjadi-bukti. Diagnostik
jam-1-vs-7 coder = skrip terpisah di temp, verifikasi keberadaannya +
bahwa ia tidak memengaruhi artefak vonis.

**A6 — Determinisme (run-ulang).**
Jalankan ulang `h4b.py` (atau bangun-ulang independen + justifikasi
tertulis bila biaya prohibitif — JSON hanya ~2 KB, jadi run-ulang
penuh diharapkan). Bandingkan sha256 vs `799c9e01…` / `ca40d326…`.
Klaim byte-identik menyebut versi toolchain; bila beda → catat
sebagai metadata, bukan temuan.

**A7 — Integritas dokumen (ringan; gerbang asisten sudah LOLOS).**
Konfirmasi struktural: S0 + SHA + mesin + output 2 arah + top-6 +
karantina + aturan baca + R-4 + ringkasan + self-audit 3× + STOP;
pengikatan eksternal (tanpa self-hash di dokumen). Hanya laporkan bila
ada yang retak.

## Larangan bentuk-spesifik (mengikat; disalin eksplisit dari pelajaran audit)

1. DILARANG `utc.normalize()` / merekonstruksi hari dari UTC.
2. DILARANG membandingkan nilai dengan dirinya sendiri dalam guard
   (`allclose(X, X)` benar untuk setiap X) — termasuk via oper kolom frame sama.
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
`reports/governance/2026-10-07/Audit/reaudit-H4b-stabilitas.md`
berisi: tabel Klaim & Bukti per A1–A7 + verdict per butir + temuan
bernomor (H/M/L) + eskalasi arsitek yang eksplisit (apa pun yang
menyentuh ambang/vonis) + verdict keseluruhan
(LULUS / LULUS DENGAN CATATAN / GAGAL) + hash file dihitung SETELAH
tulis final + STOP. DILARANG commit/push. DILARANG memulai ronde
berikutnya. DILARANG menulis vonis resmi H4b (itu wewenang arsitek
pada ronde putusan) — verdict-mu tentang kebenaran eksekusi, bukan
tentang nasib H4b.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap angka replikasi bersumber file:baris/output
mentah; A6 output ditempel (bukan "dijelaskan"); hash audit setelah final.
Putaran 2 — Bias & Asumsi: apakah kamu menilai desain (arsitek) atau kejujuran
klaim (auditor)? Apakah butir di luar A1–A7 ikut divonis? Apakah severity
temuan proporsional dengan dampak ke vonis?
Putaran 3 — Meta-check: objek benar (hasil `6410b180` + spec `0437b563`)?
Hanya file audit (+ probe `%TEMP%` bila ada) yang ditulis? ADM fail = file
tak ada / klaim tanpa bukti / di luar lingkup tanpa label?

STOP. Putusan resmi H4b HANYA atas perintah terpisah.

=== USULAN TAMBAHAN DARI ASISTEN ===

Butuh konfirmasi user (dengan paste brief ini, usulan dianggap disetujui):

1. Probe SEMENTARA hanya di `%TEMP%\opencode\h4b_audit\` (bukan
   `l3h4h5_audit` — direktori Batch-2 jangan dipakai ulang agar artefak
   tidak tercampur). Alasan: isolasi artefak ronde; R-4 H4b tetap murni.

2. S0 sesi auditor WAJIB 8 hash (dok hasil `6410b180` + spec H4b
   `0437b563` + 4 blob Batch-2 + HEAD `e0b2b9f9` + branch aktif
   `codex/ANN` ditempel); staged wajib tetap 2 berkas T6 tak tersentuh —
   bila staged ≠ 2, STOP dan laporkan sebelum audit.
   Alasan: T6 staged milik asisten-atas-perintah-user; auditor dilarang
   menyentuhnya maupun menambah stage.

3. Klaim cross-validasi (A5) wajib diperlakukan sebagai klaim yang
   diaudit, BUKAN fakta diterima — auditor membangun SET jam dari kedua
   sumber secara independen.
   Alasan: pelajaran T1 (prosa ≠ angka); kecocokan digit-per-digit
   adalah hal yang paling wajib dicurigai, bukan paling boleh dipercaya.

Tunggu konfirmasi sebelum kirim ke AI tujuan.
