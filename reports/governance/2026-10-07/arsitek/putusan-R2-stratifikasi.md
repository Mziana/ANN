# Putusan Arsitek -- R-2 Stratifikasi Tahun (Vonis Resmi + T-1 HIGH)

**Peran:** Arsitek (S26-S27; DILARANG tulis/ubah kode/data/config,
DILARANG commit/push). S-V dikerjakan sendiri sesi ini -- tanpa itu
vonis buta. **Tanggal:** 2026-10-09. **HEAD:**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` (staged tepat 2 T6).
**Lingkup TERTUTUP:** V-1--V-4. BUKAN vonis ulang H4/H5, BUKAN H6,
BUKAN batch/desain baru. **Aturan besi:** angka WAJIB output mentah.

---

## S0. Gerbang sesi ini (9/9 COCOK + HEAD + staged 2 T6)

```
c04199cea2acfd692b731fcb7eacec16b0e4691d  spesifikasi-R2 (141 baris)
c2f799138593e7ea1a8f2da6901c9f818e60b731  hasil-R2 (226 baris / 9811 B)
24a929c7f83474db0b8603f677db6213407cd44f  reaudit-R2 (27235 B / 600 baris)
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec-B2
f06a8e27b916172f5824438acd545614360d3b57  hasil-B2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit-B2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan-B2 (H4 TAHAN FINAL)
7d125022cd14113325e5c5721da53a39be661f5c  disposisi-B (D-1--D-4)
fe11383b9bdd1e58819e32812eec75c52ab3aee9  putusan-H4b (GUGUR)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD (staged: build_labels.py + test_build_labels.py)
```
Tanpa commit/push/stash/checkout sesi ini. Mismatch = STOP; nol mismatch maka diputus.

| Klaim | Status | Bukti |
|---|---|---|
| 9 blob + HEAD + staged 2 cocok | TERVERIFIKASI | `git hash-object` + `rev-parse` + `status --porcelain=v1` sesi ini |
| Lock R-2 :55-57 + loop aktual benar | TERVERIFIKASI | S-V(a): spec :55-57, `r2.py:57/195`, jam unik == lock |
| Angka penentu = artefak + sha beku | TERVERIFIKASI | S-V(b): JSON sha `4664B4D8...E64A4`, 4 sha parquet ukur-sendiri |
| Tidak run-ulang, per butir | KEPUTUSAN | S-V(c): tiga rekaman sepakat, S27 tak terpicu |
| T-1 dari kode sendiri | TERVERIFIKASI | S-V(d): `r2.py:86` konstanta-vs-literal; S1b/S2 rc=0 |
| T-2/T-3/T-4 dari bahan | TERVERIFIKASI | S-V(e): reaudit :215-222/:352-371/:431-451/:510-514 |

---

## S-V. Verifikasi arsitek (sebelum V-1)

**(a) Lock + loop aktual -- COCOK.** Lock :55-57 dibaca verbatim (OR-gugur;
(a) n_Off dibekukan non-penentu). `r2.py:57` literal `[14,13,0,15,12,7]`;
loop aktual `r2.py:195` `for hh in sh4.FIXED_HOURS`; jam unik trades
`[0,7,12,13,14,15]` == lock (JSON meta + audit A1.3/A4.2); grain
`groupby("broker_day")`, nihil `normalize`. Fakta aktual benar -- TERPISAH
dari kekuatan assert (dinilai di (d)).
**(b) Angka -- COCOK digit-per-digit.** Ukur-sendiri dari `r2_hasil.json`
(sha `4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4`,
1356769 B): 2024 n 1560 median `0.04834999999999022` mean
`0.024799771062270975` exit 87/9/1464 Off 0 F1 30; 2025 n 1554 median
`-0.005049999999992838` mean `-0.0039283324140465484` exit 71/6/1477 Off 0
F1 0; join 47721==47721, ATR exact 974 hari, pool 519x6=3114. Parquet ukur-sendiri:
`69b2c026`/`fce65a3a`/`cd6a85e4`/`47d15c41` 4/4 cocok. Sepakat penuh coder+A1/A6.
**(c) Tidak run-ulang -- diputus per butir.** Nol keraguan angka: JSON coder
run1=run2 + re-run auditor byte-identik ke-3 + ekstraksi saya identik; S27 tak
terpicu (nol selisih vs dua rekaman); `%TEMP%\r2_arsitek\` TIDAK dibuat.
**(d) T-1 -- TERKONFIRMASI dari kode sendiri.** Dengan kata saya: assert
satu-satunya (`:86`) membandingkan dua benda mati -- konstanta impor vs
literal -- sekali sebelum loop; ia buta terhadap apa yang loop iterasi
sebab loop memakai `sh4.FIXED_HOURS` (`:195`), bukan `LOCK_HOURS`, dan tak
ada assert pasca-loop atas himpunan jam aktual trades. Maka top-6 dari data
uji (S1b: `09C88383...`, median `0.05439999999999045`/`-0.010000000000002502`)
dan `range(24)` (S2: `6F8A3E0E...`, n 5978/5953) lolos rc=0 -- gate tak menggigit.
**(e) T-2/T-3/T-4 -- dari bahan.** T-2: "tiga rekaman" = partisi aritmetik pool
3114 mesin sama (:431-451), bukti independen = A1/A6. T-3: 196 hari 2026
between-state, `atr_2024_2025_identik=True` bit-identik (:352-371). T-4: isi
:201 benar (nihil vonis), label lemah (:510-514).

---

## V-1. Vonis resmi R-2 -- GUGUR (DIPUTUS)

Terapkan lock :55-57 verbatim pada angka S-V(b) yang tiga pihak sepakati:
2024 median `0.04834999999999022` > 0 lolos; 2025 median
`-0.005049999999992838` <= 0 memenuhi klausul OR-gugur ("SATU PUN" cukup);
`tahun_gugur=[2025]`, tepat satu verdict. Mekanis, tanpa tafsir-ulang.

> **Vonis resmi R-2: GUGUR.**

Ini vonis atas PERTANYAAN R-2 (stabilitas antar-tahun jam-tetap), BUKAN vonis
ulang H4 Batch-2, BUKAN vonis H5. Disitir hanya angka output mentah di atas.

---

## V-2. Disposisi T-1 HIGH -- TERIMA DENGAN CATATAN, R-2 TERTUTUP (DIPUTUS)

Memilih (ii) dengan pasal. Alasan: (1) angka benar terbukti independen
(A1 26/26 dari nol + A6 byte-identik 3 JSON + S-V(b) ukur-sendiri) dan loop
aktual terbukti memakai lock (jam unik == lock) -- re-run gate-only tak
menambah satu bit informasi angka; (2) preseden P-4/T2 Batch-2 (ketegangan
kontrol-vs-kepatuhan diputus tanpa rework, pola diganti ke depan); (3) HIGH
tetap tercatat, kewajiban gate TIDAK dihapus -- dipensiunkan + diganti pola
mengikat. Dampak NOL dipakai membuktikan angka, BUKAN menghapus temuan.
**(i) ditolak** sebab menahan vonis sah demi teater proses.

**Pola pensiun (DILARANG sebagai satu-satunya gate jam):**
`assert list(KONSTANTA_IMPOR) == LITERAL` -- buta loop, S1b/S2 lolos rc=0.
**Pola pengganti mengikat semua spec mendatang:** assert pasca-loop atas
himpunan jam entry AKTUAL, mis. `assert set(jam_utc trades) == set(LOCK_HOURS)`,
+ sabotase S1b/S2 wajib `rc != 0`. DILARANG sentuh H4 Batch-2/H4b lewat pintu ini.

---

## V-3. Disposisi T-2/T-3/T-4 LOW (DIPUTUS satu-per-satu)

**T-2 -- TUTUP sebagai catatan (tanpa erratum).** Frasa `hasil:205-207`
"benar" hanya sebagai identitas aritmetik; kualifikasi resmi TERCATAT DI SINI:
bukti independen = A1 (26/26 dari nol) + A6 (byte-identik). Dokumen beku
DILARANG diedit (preseden P-4/T1); koreksi hidup di putusan ini.
**T-3 -- TUTUP sebagai catatan + KLARIFIKASI mengikat:** "2026 dikecualikan
PENUH" = NOL kontribusi ke angka penentu maupun deskriptif artefak (BUKAN
larangan menghitung between-state di loader); bila loader membaca store penuh,
uji kausal bit-identik WAJIB (pola A4.3). Perlakuan substantif sah (preseden H4b).
**T-4 -- TUTUP sebagai catatan (tanpa erratum).** Bacaan resmi baris :201 =
`TERVERIFIKASI (nihil vonis H4/H5/H6)`; label `BELUM DIVERIFIKASI` dibaca
tergantikan kalimat ini. DILARANG naikkan severity tanpa pasal (ketiganya tetap LOW).

---

## V-4. Kunci anti-merambat (DIPUTUS)

H4 TAHAN Batch-2 FINAL + H1/H2/H3/H5 + H4b + fondasi-B tak tersentuh sejengkal
pun. GUGUR(R-2) = efek tak stabil antar-tahun pada split jam-tetap (pertanyaan
berbeda); DILARANG dibaca retak H4. P-5 dua arah tetap mengikat: R-2-gagal
DILARANG ditafsir-ulang via sub-sel/ambang/window pasca-hoc; 2024-positif
DILARANG diklaim generalisasi tanpa uji pra-registrasi segar. H6+ DITOLAK.

---

## Self-audit 3x (sebelum STOP)

**P1 Correctness:** S-2d 9/9 ukur-sendiri; S-V(a)-(e) dikerjakan + dilaporkan;
run/tidak-run eksplisit per butir; tiap V berpasangan bukti (lock/median/T-1
kinetik/T-2/T-3/T-4 + baris); vonis satu kalimat dikutip; T-1..T-4 diputus eksplisit.
**P2 Bias & Asumsi:** lock verbatim (GUGUR dilaporkan apa adanya padahal 2024
positif); T-1 tak dipakai menyelamatkan/menggugurkan di luar lock; dampak NOL
tak menghapus kewajiban gate (pensiun + pengganti mengikat); nol pintu pasca-hoc
dua arah; prosa tak disitir sebagai bukti.
**P3 Meta-check:** H4 Batch-2/H1-H3/H5/H4b/fondasi-B utuh; ruang coder/auditor tak
diambil (nol tulis selain berkas ini); severity tak berubah tanpa pasal (HIGH + 3 LOW);
pengikatan eksternal (TANPA self-hash; hash di kanal luar); STOP menutup R-2.

STOP. R-2 TERTUTUP dengan catatan V-2 oleh putusan ini.
