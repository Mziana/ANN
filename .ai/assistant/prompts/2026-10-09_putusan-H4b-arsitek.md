# Prompt putusan arsitek H4b-stabilitas (vonis resmi + ESK-1) — FINAL, siap paste — 2026-10-09

## Konteks (fakta, bukan instruksi)

Ronde coder H4b + re-audit independen SELESAI, keduanya gerbang LOLOS.
Keluaran mekanis lock (BUKAN vonis resmi): **GUGUR(H4b), tepat satu** —
Maju (train 2024 → uji 2025) median `-0.005049999999992838 ≤ 0` memenuhi
kriteria (b); Mundur (train 2025 → uji 2024) median `+0.05439999999999045`
lolos; n_Off 0/0 kedua arah; selisih jam teratas simetris `{1, 7}`.
Verdict audit: **LULUS DENGAN CATATAN** — A1 COCOK (digit-per-digit),
A2 COCOK+LOW-1, A3 COCOK+ESK-1, A4 COCOK, A5 SAH, A6 COCOK, A7 COCOK+LOW-2;
0 MEDIUM/HIGH. Tugasmu: VONIS RESMI H4b + putuskan ESK-1 + disposisi
LOW-1/LOW-2 + kunci anti-merambat. Verifikasi S-V WAJIB — bukan vonis
buta di atas ringkasan.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

- Kamu ARSITEK (kontrak bersama `.ai/AGENTS.md` §26–§27): merancang +
  memutus konflik + tie-break. DILARANG menulis/mengubah kode produksi,
  data, config.
- Kamu BUKAN coder, BUKAN auditor, BUKAN asisten. Namun verifikasi S-V di
  bawah WAJIB — kamu memutus HANYA atas bahan yang kamu periksa sendiri.
- Workdir: `D:\ANN`. Interpreter verifikasi: `venv/Scripts/python.exe`.

## S-2d. Gerbang hash (ukur sesi ini SEBELUM satu butir pun diputus)

Tempel output mentah perintah berikut SESUDAH pembacaan terakhir
(klaim tanpa output mentah = gagal):

```
git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-H4b-stabilitas.md
git hash-object reports/governance/2026-10-07/coder/hasil-H4b-stabilitas.md
git hash-object reports/governance/2026-10-07/Audit/reaudit-H4b-stabilitas.md
git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/Audit/reaudit-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md
git rev-parse HEAD
git status --porcelain=v1
```

Nilai rujukan (mismatch = STOP, bukan vonis):

```
0437b563c85e578567eb58b8cfe6b0dd3ef02b47  spesifikasi-H4b (108 baris)
6410b1800f6dc46ec511949e1311fcda853b0807  hasil-H4b (259 baris)
e3530477948a677f3e8f244dcabc64c018b85c8e  reaudit-H4b (18199 B / 476 baris)
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec Batch-2
f06a8e27b916172f5824438acd545614360d3b57  hasil Batch-2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit Batch-2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan Batch-2 (H4 TAHAN FINAL — tak tersentuh)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD (rujukan; staged tetap 2 T6)
```

## S-V. Verifikasi arsitek (WAJIB, sebelum V-1)

Vonis tanpa pemeriksaan sendiri = GAGAL. Laporkan ringkas per huruf
(COCOK / TIDAK COCOK + bukti file:baris/output):

(a) **Baca lock pada titik penentu** (bukan narasi): spec H4b `:21-24` —
GUGUR bila SATU PUN tahun-uji (a) ≥2 dari 6 jam-train jatuh Off ATAU
(b) median EV ≤ 0; TAHAN hanya bila KEDUA arah n_Off ≤ 1 DAN median > 0.
Verifikasi dari kode `h4b.py` (`top6_train_only :207-213`,
`run_arah :234-260`, `off_metrics :216-231`) bahwa ranking dikunci
train-only, pool uji difilter tahun-uji, trade di jam terkunci.
(b) **Spot-check angka penentu vs artefak** (bukan vs prosa): median/mean/
fraksi/n/exit-cause kedua arah + counter karantina (Maju 0, Mundur 30)
cocokkan melawan JSON harness `%TEMP%\h4b` (maju sha `799c9e01…` /
blob `7975db73…`; mundur sha `ca40d326…` / blob `138d9025…`) dan sha
parquet beku (M1-2024 `69b2c026…`, M1-2025 `fce65a3a…`, M15 `cd6a85e4…`,
D4 `47d15c41…`). Tempel output mentah yang kamu ukur.
(c) **Run-ulang bila perlu.** Bila (a)/(b) menimbulkan KERAGUAN: jalankan
ulang skrip/probe SEMENTARA hanya di `%TEMP%\h4b_arsitek\` (dilarang tulis
repo/commit), laporkan path + hash. Bila meyakinkan tanpa run-ulang: tulis
eksplisit per butir MENGAPA tidak run-ulang. Bila verifikasimu MENEMUKAN
selisih terhadap dua rekaman sepakat (coder+auditor) → hitung-ulang penuh
WAJIB + catat temuan baru (tie-break S27 terpicu).
(d) **Verifikasi ESK-1 dari data**: klaim Off hanya 2023 (2.894 bar jam 21
UTC; 2024/2025/2026 Off=0 seluruh bar) — konfirmasi sendiri sebelum
memutus V-2.

## Bahan (dibaca UTUH langsung, bukan ringkasan)

1. `arsitek/spesifikasi-H4b-stabilitas.md` — lock dua-arah + anti-intip +
   guard P-5; tindak lanjut R-2 yang sah, bukan H6.
2. `coder/hasil-H4b-stabilitas.md` — Maju n=1554 (71/6/1477), median
   `-0.005049999999992838`; Mundur n=1560 (94/12/1454), median
   `+0.05439999999999045`; n_Off 0/0; top6 Maju `[14,13,12,0,15,7]` vs
   Mundur `[14,13,0,15,1,12]`; vonis mekanis GUGUR(H4b) tepat satu.
3. `Audit/reaudit-H4b-stabilitas.md` — A1–A7 + LOW-1 (`h4b.py:248-250`
   guard tautologis) + LOW-2 (penomoran run `:175-176`/`:231`) + ESK-1
   (kriteria (a) tak operatif) + A5 SAH tiga sumber.
4. `arsitek/putusan-lapisan3-H4H5.md` — H4 TAHAN FINAL + P-5 kunci dua arah
   (mengikat ronde ini; lihat V-4).

## Butir putusan (TERTUTUP — hanya ini)

**V-1. Vonis resmi H4b (DIPUTUS).** Terapkan lock spec `:21-24` verbatim
pada angka yang dua pihaknya sepakati: Maju median ≤ 0 memenuhi (b) →
GUGUR(H4b) mekanis → sahkan atau tolak dengan pasal. Vonis satu kalimat
tunggal yang dikutip. Nyatakan eksplisit: ini vonis atas PERTANYAAN H4b
(EKS-3 terformalisasi dua-arah), BUKAN vonis ulang H4 Batch-2.
DILARANG menyitir prosa sebagai bukti — wajib angka + output mentah.

**V-2. Disposisi ESK-1 (DIPUTUS).** Kriteria (a) n_Off tak operatif pada
data beku (Off hanya 2023). Pilih satu dengan pasal: (i) biarkan lock
beku + catat (a) non-diskriminatif pada data ini (vonis H4b sah apa
adanya; revisi hanya via spec baru bila generalisasi diperlukan); atau
(ii) revisi kriteria (a) / definisi Off sekarang (tulis rumusan pengganti
+ syarat uji-ulang). DILARANG revisi diam-diam. DILARANG mengubah vonis
H4 Batch-2 lewat pintu ini. DILARANG vonis di luar V-1–V-4.

**V-3. Disposisi LOW-1/LOW-2 (DIPUTUS).** LOW-1: guard tautologis —
tutup sebagai catatan dokumentatif atau perintahkan perbaikan. LOW-2:
penomoran run — tutup sebagai catatan atau perintahkan erratum. Putuskan
satu-per-satu, tidak boleh diam. DILARANG menaikkan severity temuan yang
sudah tertutup tanpa pasal.

**V-4. Kunci anti-merambat (DIPUTUS).** H4 TAHAN Batch-2 FINAL + H1/H2/H3/H5
tak tersentuh putusan ini. GUGUR(H4b) DILARANG dibaca sebagai retak H4
(edge rapuh-tahun, pertanyaan berbeda). H6+ tetap DITOLAK. P-5 Batch-2
(kunci dua arah) tetap mengikat: kegagalan H4b DILARANG ditafsir-ulang
via sub-sel/ambang pasca-hoc; keberhasilan Mundur DILARANG diklaim
generalisasi tanpa uji pra-registrasi segar.

## Tugas tulis (satu-satunya tulis yang diizinkan)

Tulis putusan sebagai **file .md**:
`reports/governance/2026-10-07/arsitek/putusan-H4b-stabilitas.md`
berisi: S0 (hash terukur sesi ini + tabel Klaim & Bukti) + V-1–V-4 +
self-audit 3x adversarial + STOP. SINGKAT (target <150 baris).
Tempel output `git hash-object` file putusan SESUDAH penulisan terakhir.
DILARANG commit/push. DILARANG vonis di luar V-1–V-4. DILARANG
merumuskan H6. DILARANG membuka batch/desain baru.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: hash S-2d diukur sesi ini (bukan disalin);
S-V(a)–(d) dikerjakan + dilaporkan (run/tidak-run diputus eksplisit per
butir); tiap V berpasangan bukti mentah (lock/median/Off/ESK/LOW + baris);
vonis H4b satu kalimat dikutip; ESK-1 + LOW-1/LOW-2 diputus eksplisit.
Putaran 2 — Bias & Asumsi: lock diterapkan verbatim (tidak dirapikan agar
GUGUR/TAHAN tertentu); ESK-1 tidak dipakai menyelamatkan atau menggugurkan
di luar lock; tidak ada pintu pasca-hoc dua arah; prosa tidak disitir
sebagai bukti.
Putaran 3 — Meta-check: H4 Batch-2 + H1/H2/H3/H5 tak tersentuh; ruang
coder/auditor tidak diambil; severity lama tak berubah tanpa pasal;
klaim tanpa output mentah = gagal.

STOP. H4b TERTUTUP oleh putusan ini.
