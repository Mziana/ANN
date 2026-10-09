# Prompt re-audit Batch-2 (S-H4 + S-H5) untuk Auditor — 2026-10-09

## Konteks (fakta, bukan instruksi)

Eksekusi coder Batch-2 selesai. Dokumen hasil:
`reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md`
(1299 baris / 50219 byte / LF-only / ASCII murni — asisten verifikasi ke disk:
full-blob `f06a8e27b916172f5824438acd545614360d3b57`,
C8 `9cef2998867fc10c295a4ac53825aa9ad39e4cab`,
HEAD `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` tetap, staged 0).
Keluaran formula coder (BUKAN vonis): **S-H4 = TAHAN, S-H5 = GUGUR**.
Spec kontrak: `reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md`
(hash `4a46b815`, 461 baris). Tugasmu: RE-AUDIT SEMPIT hasil eksekusi vs spec —
verifikasi klaim dari artefak (parquet/kode/harness), bukan dari narasi coder.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

- Kamu AUDITOR adversarial (kontrak bersama `.ai/AGENTS.md` §18, §20, §21, §26):
  memverifikasi kebenaran dan kejujuran klaim dengan bukti independen.
  Replikasi angka dari sumber (parquet/kode/harness), bukan dari dokumen.
- Kamu BUKAN coder: DILARANG menulis/mengubah kode. SATU-SATUNYA tulis yang
  diizinkan adalah file audit di bawah. Pengecualian: skrip probe SEMENTARA
  hanya di `%TEMP%\opencode\l3h4h5_audit\` (tidak di repo, tidak di-commit,
  dilaporkan path-nya) — dan hanya bila hitung-ulang butuh eksekusi.
- Kamu BUKAN arsitek: DILARANG menilai kualitas metode sebagai pilihan
  arsitektur (mis. "seharusnya FDR", "seharusnya sel lain"). Yang diaudit:
  apakah eksekusi sesuai spec + apakah klaim jujur. Keraguan metode =
  eskalasi arsitek, bukan temuan.
- Kamu BUKAN asisten.
- Workdir: `D:\ANN`. Interpreter: `venv/Scripts/python.exe` (yang punya scipy).

## Hash titik-awal (verifikasi dulu, TIDAK cocok → STOP)

- Dokumen hasil: `f06a8e27b916172f5824438acd545614360d3b57` (1299 baris / 50219 byte)
- Spec: `4a46b815` (461 baris)
- HEAD: `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`
- Harness + JSON di `%TEMP%\opencode\l3h4h5`: `sh4.py`, `sh5.py`;
  trio-sha terverifikasi asisten: sh4 `b1b69d33` (3/3, 1399453 B),
  sh5 `7a7f5ee7` (3/3, 13442 B)
- Hash beku acuan (spec S-C C3, cocokkan ulang): trio+D1/D2+Batch-1+builder
  prefix `2561efd5` / `dc07a7e6` / `bc17e5de` / `34530854` / `399e64b3` /
  `ed7ac435` / `07402f40` / `fc29f6fa` / `1550209f` / `e4143132` / `641210e7` /
  `e29e18c7`; D4 sha256 `47d15c41…`; M15 features `cd6a85e4…`;
  M1/M5 2024-2025 `69b2c026`/`fce65a3a`/`da5e8944`/`a999a4bb`

## Lingkup re-audit (hanya ini — bukan audit ulang EDA/nb00-nb05/lock)

Setiap butir: COCOK / TIDAK COCOK / BELUM DIVERIFIKASI + bukti file:baris/output.
Tanpa bukti = bukan temuan. Bedakan: tidak-sama ≠ tidak-sesuai-spec ≠
salah-hitung ≠ kesimpulan-salah. False positive yang kamu batalkan sendiri
DICATAT terbuka.

**R1 — S-H4 hitung-ulang independen dari nol (P0/P1/E0/E1).**
Replikasi dari parquet + `sh4.py` (baca kodenya baris-per-baris, seperti §D
re-audit H3): (a) top-6 hitung-ulang OOS M2 2024-2025 — klaim coder
`[14,13,0,15,12,1]` vs lock P0 `[14,13,0,15,12,7]`; (b) n_Off pada top-6
hitung-ulang — klaim 0; (c) join-gate M15 vs store (klaim n 47721==47721,
sekuens identik, ATR exact); (d) EV-after-cost pool — klaim median
`0.014399999999998407`, mean `0.010463395724378413`, n=3114,
%positif `0.5211946050096339`, per-tahun 2024 `0.04834999999999022` (n 1560)
dan 2025 `-0.005049999999992838` (n 1554). Tiap angka: COCOK digit-terakhir
atau temuan.

**R2 — S-H5 hitung-ulang independen dari nol (B0/B1/Holm).**
Replikasi dari parquet + `sh5.py`: cutoff kuartil expanding blok-tahunan —
klaim `1.5216964285714296` (2024) dan `1.6039464285714264` (2025), dihitung
sekali SEBELUM evaluasi (cek tidak ada threshold-peeking: tidak ada cutoff
full-sample/2024-2025/in-eval di kode); n event Q4 = 2672 (100 + 34 hari);
tabel 4 sel (London diff `-0.0015803147973013076` p `0.5176` n 110;
Tokyo diff `0.015934029831132124` p `0.291` n 92;
NewYork diff `-0.03347701149425286` p `0.7658` n 77;
Sydney diff `0.04325279234100754` p `0.244` n 46);
prosedur Holm α=0,01 dengan ambang per-urutan
0.0025/0.003333/0.005/0.010 dan hasil nol-reject.
Verifikasi bootstrap = paired-day B=10000 PERSIS nb04 (seed, unit resample,
estimator diff — bukan CI-terpisah-sebagai-penentu).

**R3 — Penanganan top-6 vs larangan tukar Q4 (DEV-B2-1).**
Spec Q4 (`spesifikasi-lapisan3-H4H5.md:148-192`) + S-B.3 melarang tukar
jam-tetap ↔ top-6 dua arah. Putuskan: (i) apakah uji EV berjalan pada jam
tetap lock `[14,13,0,15,12,7]` dan uji pola pada hitung-ulang — sesuai klaim
coder "temuan sah kriteria-(a)"; (ii) apakah kriteria-(a) negatif pada KEDUA
bacaan (lock maupun hitung-ulang); (iii) bila ada pembacaan yang membuat
kriteria-(a) positif → temuan + eskalasi arsitek (ini ambang vonis, bukan
vonis auditor).

**R4 — DEV-B2-2, DEV-B2-3, DEV-B2-4.**
DEV-B2-2: `n_trade_pool` 3114 = 6 jam × 519 hari, 0 bar-FLAT — verifikasi
dari data; putuskan temuan vs catatan. DEV-B2-3: CI nb04-style memakai
`n_hari` berbeda dari universe bootstrap (London 108 vs 110) — verifikasi
penjelasan "unit resample berbeda" dari kode; putuskan materialitas
(keduanya non-penentu?) atau temuan. DEV-B2-4: `find -newermt` memakai
timestamp mulai-tugas `2026-10-09T03:11:41` — jalankan ulang perintah find
dengan timestamp eksplisit itu; putuskan sah vs temuan proses.

**R5 — Gate C1–C5, C9 dijalankan ulang oleh auditor.**
Asisten DILARANG run test, jadi angka gate coder belum terverifikasi
independen. WAJIB jalankan sendiri dan tempel output mentah + rc + cakupan:
(a) `pytest` PENUH (bukan satu file) — klaim coder 254 passed rc=0;
(b) `ruff check .` dan `ruff format --check .` cakupan repo — klaim rc=0;
(c) `python scripts/check_foreign_chars.py
reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md` — klaim rc=0;
(d) C2: jalankan ulang `git status --porcelain -uall -- src/ tests/ data/
configs/ reports/eda/` + daftar-C2 spec `:330` dan `find src tests data
configs -type f -newermt "2026-10-09T03:11:41"` — cocokkan dengan BEFORE/AFTER
coder; (e) C1/C9: `git rev-parse HEAD` + `git diff --cached --name-only`.
Frase "[N] files already formatted" hanya sah bila rc=0 (pelajaran butir-10).

**R6 — Determinisme harness (C5) + run-ulang.**
Jalankan ulang `sh4.py` dan `sh5.py` (atau salah satunya + justifikasi
tertulis bila biaya prohibitif — S-H4 JSON 1,4 MB; minimal S-H5 wajib
run-ulang penuh). Bandingkan sha256 vs trio `b1b69d33` / `7a7f5ee7`.
Bila run-ulang S-H4 dilewatkan: ganti dengan rekomputasi independen angka
penentu R1 dari parquet tanpa impor kode coder + review sumber `sh4.py`
baris-per-baris. Klaim byte-identik menyebut versi toolchain
(py3.12.8/pandas 2.2.3/numpy 1.26.4/scipy 1.17.1/pytest 8.3.3/ruff 0.6.9);
bila beda toolchain → catat eksplisit sebagai metadata, bukan temuan.

**R7 — Sapu kepatuhan S-B.1–S-B.14 + S-R.**
Verifikasi dari dokumen + kode: tidak ada vonis/bangkit H1/H2/H3 (S-B.1);
tepat 4 sel + 1 agregat, tanpa sel tambahan penentu (S-B.2);
tanpa TAU_alt/optimasi kuartil (S-B.3); 2026 nol kemunculan di tabel penentu
MAUPUN deskriptif (S-B.4 — grep independen); cutoff dihitung sekali pre-eval
(S-B.5); satu-satunya koreksi = Holm (S-B.6); eksklusi hanya yang ditetapkan
+ dilaporkan n-nya (S-B.7); biaya hanya by_session, satuan JPY-0.01 (S-B.8);
tanpa kalibrasi ulang (S-B.9); provenans exact-comparison/toleransi eksplisit
(S-B.10, pelajaran P-1); tanpa output-parsial-berlabel-penuh (S-B.11);
grain hari-broker tunggal, tanpa `utc.normalize()` (S-B.12 — grep independen);
daftar-C2 tak tersentuh (S-B.13 — dari R5d); tanpa ubah redaksi/ambang lock
(S-B.14). Pelanggaran S-B.13 = gagal total.

**R8 — Integritas dokumen (ringan; gerbang asisten sudah LOLOS).**
Konfirmasi struktural: blok [O1]..[O18] ada dan bernomor; tabel Klaim & Bukti
14 baris; self-audit 3 putaran; tabel §8b C1–C9; serah-terima 6 item;
C8 `9cef2998…` mereproduksi via `head -n -1 | git hash-object --stdin`.
Hanya laporkan bila ada yang retak.

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

Tulis laporan re-audit sebagai file .md:
`reports/governance/2026-10-07/Audit/reaudit-lapisan3-H4H5.md`
berisi: tabel Klaim & Bukti per R1–R8 + verdict per butir + temuan bernomor
(H/M/L) + eskalasi arsitek yang eksplisit (DEV-B2-1 dan apa pun yang
menyentuh ambang/vonis) + verdict keseluruhan
(LULUS / LULUS DENGAN CATATAN / GAGAL) + hash file dihitung SETELAH tulis
final + STOP. DILARANG commit/push. DILARANG memulai batch berikutnya.
DILARANG menulis vonis H4/H5 (itu wewenang arsitek) — verdict-mu tentang
kebenaran eksekusi, bukan tentang nasib hipotesis.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap angka replikasi bersumber file:baris/output
mentah; R5/R6 output ditempel (bukan "dijelaskan"); hash audit setelah final.
Putaran 2 — Bias & Asumsi: apakah kamu menilai metode (arsitek) atau kejujuran
klaim (auditor)? Apakah butir di luar R1–R8 ikut divonis? Apakah severity
temuan proporsional dengan dampak ke vonis?
Putaran 3 — Meta-check: objek benar (hasil `f06a8e27` + spec `4a46b815`)?
Hanya file audit (+ probe `%TEMP%` bila ada) yang ditulis? ADM fail = file
tak ada / klaim tanpa bukti / di luar lingkup tanpa label?

STOP. Putusan arsitek H4/H5 HANYA atas perintah terpisah.
