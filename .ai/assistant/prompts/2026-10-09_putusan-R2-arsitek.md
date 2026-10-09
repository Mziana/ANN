# Prompt putusan arsitek R-2-stratifikasi (vonis resmi + disposisi T-1 HIGH) -- FINAL, siap paste -- 2026-10-09

## Konteks (fakta, bukan instruksi)

Ronde coder R-2 + re-audit independen SELESAI, keduanya gerbang LOLOS sebagai
dokumen sah. Keluaran mekanis lock (BUKAN vonis resmi): **GUGUR(R-2), tepat
satu, tahun_gugur [2025]** -- 2024 n=1560 median `0.04834999999999022 > 0`
lolos; 2025 n=1554 median `-0.005049999999992838 <= 0` memenuhi klausul OR-gugur;
n_Off 0/0 kedua tahun (non-penentu, struktural); join-gate 47721=47721, ATR
exact 974 hari, pool 519 hari x 6 jam = 3114 trade. Verdict audit: **GAGAL atas
satu temuan kontrol, bukan atas angka** -- A1 COCOK 26/26 digit-per-digit, A6
COCOK byte-identik 3 JSON (`4664B4D8...E64A4`), A3 COCOK (2894 M1 jam 21 UTC
2023; n_Off 0/0 struktural), A4 COCOK + T-3 LOW, A5 COCOK + T-2 LOW, A7 COCOK +
T-4 LOW; **T-1 HIGH**: gate spec `:92-93` tak menggigit (`r2.py:86` hanya banding
konstanta-vs-literal; mutasi S1b top-6 data-uji + S2 `range(24)` lolos rc=0;
dampak angka aktual NOL). Tugasmu: VONIS RESMI R-2 + putuskan nasib gate T-1 +
disposisi T-2/T-3/T-4 + kunci anti-merambat. Verifikasi S-V WAJIB -- bukan vonis
buta di atas ringkasan.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

- Kamu ARSITEK (kontrak bersama `.ai/AGENTS.md` S26-S27): merancang +
  memutus konflik + tie-break. DILARANG menulis/mengubah kode produksi,
  data, config.
- Kamu BUKAN coder, BUKAN auditor, BUKAN asisten. Namun verifikasi S-V di
  bawah WAJIB -- kamu memutus HANYA atas bahan yang kamu periksa sendiri.
- Workdir: `D:\ANN`. Interpreter verifikasi: `venv/Scripts/python.exe`
  (py3.12.8).

## S-2d. Gerbang hash (ukur sesi ini SEBELUM satu butir pun diputus)

Tempel output mentah perintah berikut SESUDAH pembacaan terakhir
(klaim tanpa output mentah = gagal):

```
git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-R2-stratifikasi.md
git hash-object reports/governance/2026-10-07/coder/hasil-R2-stratifikasi.md
git hash-object reports/governance/2026-10-07/Audit/reaudit-R2-stratifikasi.md
git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/Audit/reaudit-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/arsitek/disposisi-fondasi-B.md
git hash-object reports/governance/2026-10-07/arsitek/putusan-H4b-stabilitas.md
git rev-parse HEAD
git status --porcelain=v1
```

Nilai rujukan (mismatch = STOP, bukan vonis):

```
c04199cea2acfd692b731fcb7eacec16b0e4691d  spesifikasi-R2 (141 baris)
c2f799138593e7ea1a8f2da6901c9f818e60b731  hasil-R2 (226 baris / 9811 B)
24a929c7f83474db0b8603f677db6213407cd44f  reaudit-R2 (27235 B / 600 baris logis, tailLF False)
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec Batch-2
f06a8e27b916172f5824438acd545614360d3b57  hasil Batch-2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit Batch-2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan Batch-2 (H4 TAHAN FINAL -- tak tersentuh)
7d125022cd14113325e5c5721da53a39be661f5c  disposisi-B (D-1--D-4; R-2 DIBUKA sah)
fe11383b9bdd1e58819e32812eec75c52ab3aee9  putusan-H4b (GUGUR)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD (rujukan; staged tetap 2 T6)
```

## S-V. Verifikasi arsitek (WAJIB, sebelum V-1)

Vonis tanpa pemeriksaan sendiri = GAGAL. Laporkan ringkas per huruf
(COCOK / TIDAK COCOK + bukti file:baris/output):

(a) **Baca lock pada titik penentu** (bukan narasi): spec R-2 `:55-57` --
GUGUR bila SATU PUN tahun-uji (2024, 2025) median EV-after-cost tahun <= 0;
TAHAN hanya bila KEDUA tahun median > 0; tanpa TAK-MENENTUKAN; kriteria (a)
n_Off DIBEKUKAN non-penentu. Verifikasi dari `r2.py` bahwa loop aktual memakai
jam lock dan jam unik trades == `[14,13,0,15,12,7]` (fakta aktual), TERPISAH
dari penilaian kekuatan assert di (d).
(b) **Spot-check angka penentu vs artefak** (bukan vs prosa): median/mean/
fraksi/n/exit-cause per tahun + counter F-1 (30/0) + join-gate cocokkan melawan
JSON harness `%TEMP%\opencode\r2\r2_hasil.json` (sha
`4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4`) dan sha
parquet beku (M1-2024 `69b2c026...`, M1-2025 `fce65a3a...`, M15 `cd6a85e4...`,
D4 `47d15c41...`). Tempel output mentah yang kamu ukur.
(c) **Run-ulang bila perlu.** Bila (a)/(b) menimbulkan KERAGUAN: jalankan
ulang skrip/probe SEMENTARA hanya di `%TEMP%\r2_arsitek\` (dilarang tulis
repo/commit), laporkan path + hash. Bila meyakinkan tanpa run-ulang: tulis
eksplisit per butir MENGAPA tidak run-ulang. Bila verifikasimu MENEMUKAN
selisih terhadap dua rekaman sepakat (coder+auditor) -> hitung-ulang penuh
WAJIB + catat temuan baru (tie-break S27 terpicu).
(d) **Verifikasi T-1 dari kode sendiri sebelum memutus V-2**: baca
`spesifikasi-R2-stratifikasi.md:92-93` (assert dependen-data + larang
`utc.normalize()`), `r2.py:57` (LOCK_HOURS literal), `r2.py:86` (satu-satunya
assert), `r2.py:195` (loop aktual). Nyatakan dengan kata-katamu sendiri MENGAPA
assert yang ada tak menggigit (konstanta-vs-literal, sekali-sebelum-loop, tanpa
assert pasca-loop atas himpunan jam aktual). Konfirmasi S1b/S2 dari tabel audit
`:215-222` sebagai bukti kinetik, bukan opini.
(e) **Verifikasi T-2/T-3/T-4 dari bahan**: T-2 (`:431-451`, partisi aritmetik
vs A1/A6 independen); T-3 (`:352-371`, 196 hari 2026 between-state, ATR
2024-2025 bit-identik); T-4 (`:510-514`, label `:201`). Putuskan V-3 hanya
sesudah (e).

## Bahan (dibaca UTUH langsung, bukan ringkasan)

1. `arsitek/spesifikasi-R2-stratifikasi.md` -- pertanyaan tunggal + lock
   OR-gugur + anti-intip + S-B + aturan baca TERTUTUP.
2. `coder/hasil-R2-stratifikasi.md` -- 2024 (1560, 87/9/1464, Off 0, F1 30) +
   2025 (1554, 71/6/1477, Off 0, F1 0) + join + lock `GUGUR(R-2)` tepat satu.
3. `Audit/reaudit-R2-stratifikasi.md` -- A1-A7 + T-1 HIGH (`:169-251`) +
   T-2/T-3/T-4 LOW + Klaim & Bukti (`:553-574`) + self-audit (`:577-596`).
4. `arsitek/putusan-lapisan3-H4H5.md` + `arsitek/disposisi-fondasi-B.md` +
   `arsitek/putusan-H4b-stabilitas.md` -- rantai pengikat (P-5 dua arah, D-2
   R-2 DIBUKA, V-4 anti-merambat; semua tak tersentuh putusan ini).

## Butir putusan (TERTUTUP -- hanya ini)

**V-1. Vonis resmi R-2 (DIPUTUS).** Terapkan lock spec `:55-57` verbatim
pada angka yang dua pihaknya sepakati (S-V(a)-(b)): 2025 median <= 0 memenuhi
klausul OR-gugur -> GUGUR(R-2) mekanis -> sahkan atau tolak dengan pasal.
Vonis satu kalimat tunggal yang dikutip. Nyatakan eksplisit: ini vonis atas
PERTANYAAN R-2 (stabilitas antar-tahun jam-tetap), BUKAN vonis ulang H4
Batch-2, BUKAN vonis H5. DILARANG menyitir prosa sebagai bukti -- wajib angka
+ output mentah.

**V-2. Disposisi T-1 HIGH (DIPUTUS).** Gate `:92-93` menuntut assert
dependen-data; implementasi hanya identitas konstanta (S-V(d)). Pilih satu
dengan pasal, tidak boleh diam: (i) PERBAIKAN WAJIB -- perintahkan assert
pasca-loop atas himpunan jam entry aktual (mis.
`set(jam_utc trades) == set(LOCK_HOURS)`) + uji sabotase S1b/S2 wajib lolos
ditolak-rc-non-0 + re-run + re-audit gate-only sebelum R-2 dinyatakan TERTUTUP
(vonis V-1 tetap sah bersyarat atau ditahan -- nyatakan); atau (ii) TERIMA
DENGAN CATATAN -- sahkan R-2 TERTUTUP apa adanya atas dasar A1/A6 (dampak
angka NOL terbukti), bekukan pola assert-konstanta sebagai POLA PENSIUN +
wajibkan pola assert-dependen-data di semua spec mendatang (tulis rumusan pola
pengganti). DILARANG revisi diam-diam. DILARANG mengubah vonis H4 Batch-2 /
H4b lewat pintu ini. DILARANG vonis di luar V-1--V-4.

**V-3. Disposisi T-2/T-3/T-4 LOW (DIPUTUS satu-per-satu).** T-2: tutup sebagai
catatan (frasa "tiga rekaman" = identitas aritmetik; bukti independen = A1/A6)
atau perintahkan erratum. T-3: klarifikasi teks spec "2026 dikecualikan PENUH"
(larang hitung sama sekali vs nol-kontribusi cukup -- pilih + tulis rumusan)
atau tutup sebagai catatan. T-4: tutup sebagai catatan atau perintahkan
erratum label `:201`. Putuskan tiap butir eksplisit. DILARANG menaikkan
severity tanpa pasal.

**V-4. Kunci anti-merambat (DIPUTUS).** H4 TAHAN Batch-2 FINAL + H1/H2/H3/H5 +
H4b tak tersentuh putusan ini. GUGUR(R-2) DILARANG dibaca sebagai retak H4
(efek tak stabil antar-tahun pada split jam-tetap, pertanyaan berbeda); TAHAN
pun DILARANG dibaca kebal umum. H6+ tetap DITOLAK. P-5 Batch-2 (kunci dua arah)
tetap mengikat: kegagalan R-2 DILARANG ditafsir-ulang via sub-sel/ambang
pasca-hoc; keberhasilan satu tahun DILARANG diklaim generalisasi tanpa uji
pra-registrasi segar.

## Tugas tulis (satu-satunya tulis yang diizinkan)

Tulis putusan sebagai **file .md**:
`reports/governance/2026-10-07/arsitek/putusan-R2-stratifikasi.md`
berisi: S0 (hash terukur sesi ini + tabel Klaim & Bukti) + V-1--V-4 +
self-audit 3x adversarial + STOP. SINGKAT (target <150 baris).
Tempel output `git hash-object` file putusan SESUDAH penulisan terakhir.
DILARANG commit/push. DILARANG vonis di luar V-1--V-4. DILARANG
merumuskan H6. DILARANG membuka batch/desain baru.

=== SELF-AUDIT 3x ADVERSARIAL (sebelum STOP) ===
Putaran 1 -- Correctness: hash S-2d diukur sesi ini (bukan disalin);
S-V(a)-(e) dikerjakan + dilaporkan (run/tidak-run diputus eksplisit per
butir); tiap V berpasangan bukti mentah (lock/median/T-1/T-2/T-3/T-4 + baris);
vonis R-2 satu kalimat dikutip; T-1 + T-2/T-3/T-4 diputus eksplisit.
Putaran 2 -- Bias & Asumsi: lock diterapkan verbatim (tidak dirapikan agar
GUGUR/TAHAN tertentu); T-1 tidak dipakai menyelamatkan atau menggugurkan di
luar lock; dampak NOL tidak dipakai menghapus kewajiban gate; tidak ada pintu
pasca-hoc dua arah; prosa tidak disitir sebagai bukti.
Putaran 3 -- Meta-check: H4 Batch-2 + H1/H2/H3/H5 + H4b + fondasi-B tak
tersentuh; ruang coder/auditor tidak diambil; severity lama tak berubah tanpa
pasal; klaim tanpa output mentah = gagal.

STOP. R-2 TERTUTUP oleh putusan ini (dengan atau tanpa syarat V-2 -- nyatakan).
