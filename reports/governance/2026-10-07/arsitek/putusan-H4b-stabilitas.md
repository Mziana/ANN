# Putusan Arsitek -- H4b Stabilitas Lintas-Tahun (Vonis Resmi + ESK-1)

**Peran:** Arsitek (S26-S27: merancang + memutus; DILARANG tulis/ubah
kode produksi, data, config). **BUKAN coder/auditor.** Verifikasi S-V
dikerjakan sendiri sesi ini -- memutus HANYA atas bahan yang saya
periksa sendiri. **Tanggal:** 2026-10-09. **HEAD sesi ini:**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
**Lingkup TERTUTUP:** V-1 (vonis H4b), V-2 (ESK-1), V-3 (LOW-1/LOW-2),
V-4 (anti-merambat). DILARANG vonis di luar V. DILARANG commit/push/
H6/batch baru. **Aturan besi:** klaim angka WAJIB output mentah (S5).

---

## S0. Gerbang hash sesi ini (8/8 COCOK, mismatch 0)

```
0437b563c85e578567eb58b8cfe6b0dd3ef02b47  spec-H4b (108 baris)
6410b1800f6dc46ec511949e1311fcda853b0807  hasil-H4b (259 baris)
e3530477948a677f3e8f244dcabc64c018b85c8e  reaudit-H4b (18199 B / 476)
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec-B2
f06a8e27b916172f5824438acd545614360d3b57  hasil-B2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit-B2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan-B2 (H4 TAHAN FINAL)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD (staged tepat 2 T6)
```

| Klaim | Status | Bukti |
|---|---|---|
| 7 blob + HEAD cocok rujukan | TERVERIFIKASI | `git hash-object` + `rev-parse` + `status --porcelain` sesi ini |
| Lock H4b :21-24 tak berubah | TERVERIFIKASI | blob spec `0437b563` (spec tulisan saya) |
| `h4b.py` = skrip yang diaudit | TERVERIFIKASI | sha256 `1bbaf42703825339...` cocok sitiran reaudit A2 |
| Median Maju/Mundur + n_Off | TERVERIFIKASI | baca langsung JSON sesi ini (S-V(b)) |
| ESK-1 dari data | TERVERIFIKASI | probe sesi ini (S-V(d)) |
| Staged 2 T6, worktree lain tak tersentuh | TERVERIFIKASI | `diff --cached --name-only` sesi ini |

---

## S-V. Verifikasi arsitek (sebelum V-1)

**(a) Lock + kode -- COCOK.** Lock :21-24 diterapkan verbatim
(GUGUR bila SATU PUN tahun-uji: (a) >=2 jam Off ATAU (b) median
EV <= 0). `h4b.py` identik via sha256 dengan yang auditor bedah
baris-per-baris + sabotase (`:207-213, :216-231, :234-260`;
sabotase A/B keduanya menggigit, rc=1 -- bukti gate substantif,
saya telaah outputnya, bukan klaimnya).
**(b) Angka -- COCOK digit-per-digit.** Baca langsung JSON sesi
ini: Maju median `-0.005049999999992838` (n 1554, SL/TP/time
71/6/1477, n_Off 0, karantina 0); Mundur median
`+0.05439999999999045` (n 1560, 94/12/1454, n_Off 0, karantina
30). Git-blob JSON (`7975db73`, `138d9025`) cocok R-4 coder;
meta JSON memuat 4 sha parquet beku. Top-6:
`[14,13,12,0,15,7]` vs `[14,13,0,15,1,12]`, selisih `{1,7}`.
**(c) Tidak run-ulang -- diputus per butir.** Nol keraguan angka:
tiga rekaman sepakat penuh (JSON coder, replikasi auditor dari
nol A1, bacaan langsung saya); A6 byte-identik + toolchain
identik. S27 tidak terpicu. Probe ESK-1 saya kerjakan sendiri
di `%TEMP%\h4b_arsitek\` (bukan run-ulang harness).
**(d) ESK-1 dari data -- TERKONFIRMASI.** Probe sesi ini
(definisi Off beku `_eda_common.py:17-38,69-74`):
`2023 n_Off= 2894 (jam 21 UTC semua); 2024/2025/2026 n_Off= 0`.
Kriteria (a) struktural inoperatif pada data beku 2024-2025.

---

## V-1. Vonis resmi H4b -- GUGUR (DIPUTUS)

Maju memenuhi (b) (`-0.00505 <= 0`); "satu pun" cukup. Mundur
lolos keduanya. Penerapan mekanis lock verbatim, tanpa statistik
tambahan.

> **Vonis resmi H4b: GUGUR.**

Ini BUKAN vonis ulang H4. Makna mengikat: efek H4 TIDAK stabil
antar-tahun pada data beku 2024-2025. Bobot konfirmatori terbatas
(pertanyaan termotivasi EKS-3 -- tercatat jujur di spec).

## V-2. ESK-1 OFF-INOPERATIF -- BEKUKAN + CATAT (DIPUTUS)

Memilih (i): kriteria (a) DIBEKUKAN APA ADANYA + dicatat sebagai
peringatan desain permanen. Menolak (ii) dengan pasal: revisi
lock pasca-eksekusi = perubahan ambang pasca-hoc, DILARANG oleh
pra-registrasi + P-5; dan revisi tidak mengubah satu angka pun
(vonis ditentukan kriteria (b)). Syarat bila lock gaya-H4b kelak
dipakai generalisasi: kriteria (a) WAJIB dibuat operatif atau
dibuang lewat spec pra-registrasi BARU. DILARANG sentuh H4
Batch-2. DILARANG vonis luar V.

## V-3. LOW-1 / LOW-2 -- TETAP LOW (DIPUTUS)

LOW-1 (`h4b.py:248-250`, guard dokumentatif): tetap LOW -- tidak
ada bukti kebocoran, dua lapis lain terbukti menggigit. LOW-2
(penomoran run): tetap LOW -- determinisme terbukti ulang A6.
DILARANG naikkan severity tanpa pasal (tidak ada pasal).

## V-4. Anti-merambat (DIPUTUS)

H4 TAHAN + H1/H2/H3/H5 FINAL tak tersentuh sejengkal pun.
GUGUR(H4b) BUKAN retak pada H4. H6+ DITOLAK (tidak dirumuskan).
P-5 putusan-B2 mengikat dua arah: H5-gagal dilarang tafsir-ulang,
H4-TAHAN dilarang diklaim kebal.

---

## Self-audit 3x (sebelum STOP)

**P1 Correctness:** 8/8 hash sesi ini; lock diterapkan verbatim
pada angka bacaan-sendiri; ESK-1 diprobe dari data (bukan
dikutip); tiap V berpasangan bukti mentah.
**P2 Bias & Asumsi:** ambang tidak dilonggarkan/diketatkan agar
vonis "bagus" (Maju GUGUR mekanis meski Mundur positif);
inoperativitas (a) tidak dipakai mendiskon (b); severity tak
diubah tanpa pasal; keterbatasan EKS-3-ter-motivasi dicatat,
bukan disembunyikan.
**P3 Meta-check:** lock/spec/ambang Batch-2 utuh tanpa addendum;
ruang coder/auditor tak diambil (hanya vonis + disposisi);
aturan proses baru = nihil (pengikatan eksternal dipakai:
dokumen TANPA self-hash, hash di kanal luar); STOP menutup H4b.

STOP. H4b TERTUTUP oleh putusan ini.
