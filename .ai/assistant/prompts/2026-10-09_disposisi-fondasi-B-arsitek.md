# Prompt disposisi fondasi-B (penutup diagnostik) — FINAL, siap paste — 2026-10-09

## Konteks (fakta, bukan instruksi)

Ronde eksekusi coder fondasi-B SELESAI + gerbang LOLOS
(`coder/hasil-telaah-fondasi-B.md`, 416 baris, blob `0284f5f0…`,
R-4 terverifikasi independen oleh asisten: hash-ulang `%TEMP%\fondasiB`
cocok 3/3 — u1 `2c76e2d0…`, u2 `ac9eed29…`, u3 `2ced2c88…`).
Headline verbatim coder: gate INKLUSI digit-per-digit
(`0.014399999999998407`, n=3114); EKSKLUSI 5 hari/30 trade, selisih pool
−0,0005, **2025 tidak balik tanda**, n_Off/any_off 0/0; biaya **1,46%**;
U-3 **"Bertepatan"**; **vonis H4 TETAP TAHAN**. Tugasmu: sahkan bacaan
cabang R-1–R-4 protokol + tutup fondasi-B resmi. BUKAN vonis ulang,
BUKAN H6. Tanpa verifikasi S-V sendiri = vonis buta.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

Kamu ARSITEK (kontrak bersama `.ai/AGENTS.md` §26–§27): merancang +
memutus konflik + tie-break. DILARANG menulis/mengubah kode produksi,
data, config. DILARANG commit/push dalam bentuk apa pun — soal commit
T6 adalah perintah manusia, bukan wewenangmu.
Kamu BUKAN coder, BUKAN auditor, BUKAN asisten. Namun verifikasi S-V di
bawah WAJIB — kamu memutus HANYA atas bahan yang kamu periksa sendiri
(kamu sudah menetapkan syarat ini sendiri).
Workdir: `D:\ANN`. Interpreter verifikasi: `venv/Scripts/python.exe`.

## S-2d. Gerbang hash (ukur sesi ini SEBELUM satu butir pun diputus)

Tempel output mentah perintah berikut SESUDAH pembacaan terakhir
(klaim tanpa output mentah = gagal):

```
git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/Audit/reaudit-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md
git hash-object reports/governance/2026-10-07/arsitek/protokol-telaah-fondasi-B.md
git hash-object reports/governance/2026-10-07/coder/hasil-telaah-fondasi-B.md
git hash-object reports/governance/2026-10-07/arsitek/putusan-H4b-stabilitas.md
git rev-parse HEAD
git status --porcelain=v1
```

Nilai rujukan (mismatch = STOP, bukan disposisi):

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec-B2
f06a8e27b916172f5824438acd545614360d3b57  hasil-B2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit-B2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan-B2 (H4 TAHAN FINAL — tak tersentuh)
ed436fddf607d3629fa226fd34d20ff60bf47232  protokol-B (218 baris)
0284f5f022ce1c147cefef6dd7780aded6acf820  hasil-B (416 baris)
fe11383b9bdd1e58819e32812eec75c52ab3aee9  putusan-H4b (119 baris; H4b GUGUR — stabilitasnya)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD (rujukan; staged tetap 2 T6)
```

## S-V. Verifikasi arsitek (WAJIB, sebelum D-1)

Menandatangani tanpa pemeriksaan sendiri = vonis buta. Laporkan ringkas
per huruf (COCOK / TIDAK COCOK + bukti file:baris/output):

(a) **Baca hasil-B UTUH** (`hasil-telaah-fondasi-B.md` 416 baris) pada
titik penentu: R-1 (eksklusi 5 hari/30 trade, tanda 2025, selisih pool),
R-2 ("Bertepatan"), R-3 (porsi biaya 1,46%), R-4 (trio hash `%TEMP%`).
(b) **Spot-check angka penentu vs artefak** (bukan vs prosa): INKLUSI
`0.014399999999998407` n=3114, eksklusi Δ−0,0005, n_Off/any_off 0/0 —
cocokkan melawan artefak `%TEMP%\fondasiB` + sha parquet beku. Tempel
output mentah yang kamu ukur.
(c) **Run-ulang bila perlu.** Bila (a)/(b) menimbulkan KERAGUAN: jalankan
ulang skrip/probe SEMENTARA hanya di `%TEMP%\fondasiB_arsitek\`
(dilarang tulis repo/commit), laporkan path + hash. Bila meyakinkan tanpa
run-ulang: tulis eksplisit per butir MENGAPA tidak run-ulang. Bila
verifikasimu MENEMUKAN selisih terhadap dua rekaman sepakat
(coder+asisten-gerbang) → hitung-ulang penuh WAJIB + catat temuan baru
(tie-break S27 terpicu).
(d) **Tanpa (a)–(c) = vonis buta.** Tulis satu baris konfirmasi bahwa
S-V dikerjakan sesi ini.

## Bahan (dibaca UTUH langsung, bukan ringkasan)

1. `arsitek/protokol-telaah-fondasi-B.md` — cabang R-1–R-4 + STOP;
   diagnostik, BUKAN vonis ulang; H6+ tetap DITOLAK.
2. `coder/hasil-telaah-fondasi-B.md` — headline di Konteks + R-4 3/3 +
   atribusi staged=2 = T6 (coder tak menyentuh).
3. `arsitek/putusan-lapisan3-H4H5.md` — H4 TAHAN FINAL + P-5 dua arah
   (mengikat butir ini).
4. `arsitek/putusan-H4b-stabilitas.md` — H4b GUGUR + ESK-1 dibekukan
   (konteks kerapuhan-tahun untuk D-2).

## Butir disposisi (TERTUTUP — hanya ini)

**D-1. Sahkan bacaan R-1 (DIPUTUS).** Eksklusi tidak membalik tanda
2025 → EKS-3 DITUTUP sebagai noise tahunan murni, atau tolak dengan
pasal. Vonis H4 TETAP. DILARANG sitir prosa sebagai bukti — wajib angka
+ output mentah.

**D-2. Sahkan bacaan R-2 (DIPUTUS).** "Bertepatan" dicatat; ronde desain
berikut BOLEH mempertimbangkan stratifikasi tahun pra-registrasi
(BUKAN filter regime — filter tetap DILARANG tanpa spec baru + uji
stabilitas LULUS). Atau putuskan sebaliknya dengan pasal. R-2 tetap
terblokir sampai butir ini diputus.

**D-3. Sahkan bacaan R-3 (DIPUTUS).** Porsi 1,46% < 50% → H4 TANPA flag
biaya-sensitif; H5 tanpa cabang aksi (GUGUR telak final). Atau putuskan
sebaliknya dengan pasal.

**D-4. Tutup fondasi-B (DIPUTUS).** Nyatakan ronde diagnostik SELESAI:
vonis H1–H5 tetap seluruhnya (termasuk H4b GUGUR); H6 tidak dirumuskan;
satu-satunya warisan ronde ini = (a) opsi R-2 untuk ronde desain,
(b) risiko rantai-bukti `%TEMP%` yang sudah dicatat. DILARANG membuka
butir baru. DILARANG vonis di luar D-1–D-4. DILARANG menaikkan severity
tertutup tanpa pasal.

## Tugas tulis (satu-satunya tulis yang diizinkan)

Tulis disposisi sebagai **file .md**:
`reports/governance/2026-10-07/arsitek/disposisi-fondasi-B.md`
berisi: S0 (hash terukur sesi ini + tabel Klaim & Bukti) + D-1–D-4 +
self-audit 3x adversarial + STOP. SINGKAT (target <100 baris).
Tempel output `git hash-object` file disposisi SESUDAH penulisan terakhir.
DILARANG commit/push. DILARANG vonis ulang. DILARANG merumuskan H6.
DILARANG membuka batch/desain baru (brief desain menyusul SESUDAH
disposisi ini).

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: hash S-2d diukur sesi ini (bukan disalin);
S-V(a)–(d) dikerjakan + dilaporkan (run/tidak-run diputus eksplisit per
butir); tiap D berpasangan bukti mentah (R-1/R-2/R-3/R-4 + baris);
D-1–D-4 masing-masing diputus eksplisit; klaim tanpa output mentah = gagal.
Putaran 2 — Bias & Asumsi: bacaan tidak dirapikan agar vonis tertentu;
"Bertepatan" tidak dipakai membuka filter diam-diam; prosa tidak disitir
sebagai bukti.
Putaran 3 — Meta-check: vonis H1–H5/H4b tak tersentuh; ruang coder/auditor
tidak diambil; severity lama tak berubah tanpa pasal.

STOP. Fondasi-B TERTUTUP oleh disposisi ini.
