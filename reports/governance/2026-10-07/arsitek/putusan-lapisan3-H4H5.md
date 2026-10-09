# Putusan Arsitek -- Lapisan 3 Batch-2 (Vonis Resmi H4/H5)

**Peran:** Arsitek (AGENTS.md S26-S27: merancang + memutus konflik +
tie-break; DILARANG menulis kode produksi). **BUKAN coder, BUKAN
auditor.** Namun verifikasi S-V di bawah dikerjakan sendiri sesi ini --
saya memutus HANYA atas bahan yang saya periksa sendiri.
**Tanggal:** 2026-10-09. **HEAD sesi ini:**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
**Lingkup TERTUTUP -- 5 butir saja:** P-1 (vonis H4), P-2 (vonis H5),
P-3 (disposisi EKS-1--EKS-4), P-4 (disposisi T1--T6 + standing rule C8),
P-5 (batas scope). DILARANG vonis di luar P-1--P-5. DILARANG memulai
batch berikutnya. Bukan ubah lock/ambang, bukan kalibrasi ulang, bukan
varian/ambang baru, bukan eksekusi ulang harness.
**Dokumen yang diputus (dibaca UTUH langsung, bukan ringkasan):**
`arsitek/spesifikasi-lapisan3-H4H5.md` (461 baris),
`coder/hasil-lapisan3-H4H5.md` (1299 baris),
`Audit/reaudit-lapisan3-H4H5.md` (707 baris),
`arsitek/putusan-lapisan3-H1H2.md` (296 baris, preseden pola).
Rujukan konsistensi: lock H4/H5 (`hipotesis_lock_v1.md:108-149`) +
`putusan-arsitek-H1-H5.md`.
**Kontrak:** AGENTS.md v3.0 S5 (Klaim & Bukti), S20 (klaim wajib bukti;
output asli ditempel), S21 (uji dulu, simpulkan kemudian), S26
(pemisahan peran), S27 (arbitrase). **Aturan besi (berlaku untuk
putusan ini juga): klaim tanpa output mentah = GAGAL.**

---

## S0. Bukti baca + Klaim & Bukti sesi ini (S5)

Gerbang S-2d brief: hash diukur sesi ini dengan `git hash-object` +
`git rev-parse HEAD` SEBELUM satu butir pun diputus. Hasil ukur:

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  arsitek/spesifikasi-lapisan3-H4H5.md (461 baris)
f06a8e27b916172f5824438acd545614360d3b57  coder/hasil-lapisan3-H4H5.md (1299 baris)
8a4d21090f27dd53555b3a12583ec337819efb2f  Audit/reaudit-lapisan3-H4H5.md (707 baris)
ca4e0b70d9dc4272347b74b1ea78d7a5f94593ee  arsitek/putusan-lapisan3-H1H2.md (296 baris)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD
```

Kelima nilai COCOK dengan S-2d brief (mismatch = 0). Staged = 0
(`git diff --cached --name-only` kosong). Gerbang LULUS; putusan
dilanjutkan.

Cara baca status: TERVERIFIKASI = saya ukur/baca/hitung sendiri sesi
ini; TERVERIFIKASI (rujukan) = hash-nya saya verifikasi + isinya ada di
dokumen ter-hash yang saya baca utuh; KEPUTUSAN = penilaian arsitek di
putusan ini.

| Klaim | Status | Bukti |
|---|---|---|
| HEAD = `e0b2b9f9...` | TERVERIFIKASI | `git rev-parse HEAD` sesi ini |
| Blob spec = `4a46b815...` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob hasil = `f06a8e27...` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob re-audit = `8a4d2109...` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob putusan H1H2 = `ca4e0b70...` | TERVERIFIKASI | `git hash-object` sesi ini |
| S-V(a): titik penentu sh4/sh5 sesuai spec | TERVERIFIKASI | S-V(a): `sh4.py:59,127,158-160,318-329,451`; `sh5.py:419-433,536-557,573-599`; grep `TAU_alt|normalize` nihil |
| S-V(b): angka penentu = artefak JSON + sha beku | TERVERIFIKASI | S-V(b): trio-sha `b1b69d33`/`7a7f5ee7` run1=run2; 6 sha parquet; ekstraksi JSON sesi ini |
| S-V(c): run/tidak-run diputus per butir | KEPUTUSAN | S-V(c): tidak run-ulang, rasional eksplisit; direktori `%TEMP%` arsitek tidak dibuat |
| S-V(d): T1 terkonfirmasi dari data | TERVERIFIKASI | S-V(d): probe M1 2024-2025 sesi ini; jam 0/1 = 100% Tokyo |
| Tie-break S27 tidak terpicu | KEPUTUSAN | S-V(c): tiga rekaman (JSON coder, dokumen hasil, rekomputasi auditor) sepakat penuh |
| Angka sitiran P-1 ([O6]/JSON) | TERVERIFIKASI | P-1: ekstraksi `sh4_hasil_run1.json` sesi ini + [O6] ter-hash |
| Angka sitiran P-2 ([O13]/[O14]/JSON) | TERVERIFIKASI | P-2: ekstraksi `sh5_hasil_run1.json` sesi ini + [O13]/[O14] ter-hash |
| Staged = 0, tanpa commit/stash/checkout oleh sesi ini | TERVERIFIKASI | `git diff --cached --name-only` kosong, sesi ini (S5) |

---

## S-V. Verifikasi arsitek (WAJIB, sebelum P-1)

**(a) Baca kode titik penentu -- COCOK.** `sh4.py` dibaca utuh (483
baris): `FIXED_HOURS = [14,13,0,15,12,7]` (`:59`) = lock `:113-119`,
ditegakkan `assert FIXED_HOURS == P0_LOCK` (`:127`); `per_hour`
dibangun HANYA dari `FIXED_HOURS` (`:318-320`); loop entry HANYA
`for hh in FIXED_HOURS` (`:329`) -- jam 1 tidak pernah masuk hitungan
EV; `gugur_a = bool(n_off_bars >= 2)` (`:451`) memakai `n_off_bars`
dari `top6` hitung-ulang (`:158-160`); prioritas intra-bar SL>TP
(`:350-356`); time-stop close terakhir (`:347-349`). `sh5.py` dibaca
utuh (629 baris): `cutoff_2024` dari ATR 2023 saja (`:419,421`) dan
`cutoff_2025` dari ATR 2023-2024 (`:420,422`), dihitung SEKALI
pre-eval (`:419-424`) sebelum event Q4 dibentuk (`:433`); `is_q4`
memakai ATR T-1 (`atr_prev`, `:424`) dengan strict `>` (`:431`,
tie -> Q3); loop bootstrap paired-day atas `CELLS` tetap
London->Tokyo->NewYork->Sydney lalu Q4-ALL (`:536-562`),
`p = prop diff <= 0` (`:316`); Holm step-down (`:579-584`,
`thr = 0.01/(4-i)`, berhenti pada reject pertama yang gagal).
Grep `TAU_alt|normalize|full-sample|in-eval` pada kedua skrip NIHIL
(hanya hit komentar "2026 dikecualikan" + `n_toucher_2026`
pelaporan-wajib + seed `20261006`). Maka: EV hanya jam tetap, pola
hanya top-6 hitung-ulang, cutoff dihitung sekali pre-eval, tanpa
TAU_alt/cutoff full-sample/in-eval.

**(b) Spot-check angka vs artefak -- COCOK.** Sha diverifikasi dulu:
`sh4_hasil_run1.json` = `sh4_hasil_run2.json` =
`b1b69d33115398e48516f1662d28f6d05dbbefac6f2e8bb857bfe59041c57588`;
`sh5_hasil_run1.json` = `sh5_hasil_run2.json` =
`7a7f5ee7b3258932af185abdea487d9a8fb1928ab8c2b0f273d483089dc8a245`
(cocok trio-sha brief + [O9]/[O15]). Sha256 parquet beku: M1
`69b2c026`/`fce65a3a`, M5 `da5e8944`/`a999a4bb`, M15 `cd6a85e4`, D4
`47d15c41` -- 6/6 cocok S0. Ekstraksi langsung dari JSON sesi ini:
top-6 hitung-ulang `[14,13,0,15,12,1]`; `n_Off = 0`, share 0.0,
any_off = 0, maj_off = 0; `share_LondonNY = 0.6832894546066546`;
median EV pool `0.014399999999998407` (mean `0.010463395724378413`,
n 3114, fraksi positif `0.5211946050096339`, exit 158/15/2941);
2024 median `0.04834999999999022` (n 1560), 2025 median
`-0.005049999999992838` (n 1554); join 47721==47721. H5: cutoff
`1.5216964285714296` / `1.6039464285714264`; n_q4 2672 (100/34 hari);
diff London `-0.0015803147973013076` p 0.5176 (110 hari), Tokyo
`0.015934029831132124` p 0.291 (92), NewYork `-0.03347701149425286`
p 0.7658 (77), Sydney `0.04325279234100754` p 0.244 (46); urutan Holm
`[Sydney,Tokyo,London,NewYork]`, reject 4x False, `sel_positif = []`;
verdict `TAHAN` / `GUGUR`; `scan_beyond = 0`, `touch2026 = 0`,
`off_q4 = 0`. Seluruhnya cocok digit-per-digit dengan [O6]/[O8]/
[O11]-[O14].

**(c) Run/tidak-run -- diputus eksplisit per butir, TIDAK run-ulang.**
(1) Tidak ada keraguan atas satu angka/klaim pun setelah (a)/(b):
logika titik penentu lurus tanpa cabang tersembunyi (assert +
loop tetap), dan seluruh angka penentu cocok bit-exact dengan
artefak. (2) Auditor sudah merekomputasi dari nol tanpa impor skrip
coder (R1/R2 bit-exact termasuk median 15 digit + 4 p + 4 CI95
digit-per-digit) dan mereplikasi kedua harness byte-identik 3x
dengan toolchain identik (R6) -- hitung-ulang ketiga oleh saya
tidak menambah informasi (preseden S0.1 putusan H1H2/H3).
(3) Probe independen saya (S-V(b) ekstraksi JSON + S-V(d) dari
parquet mentah) sudah merupakan verifikasi independen dari bahan
mentah, bukan dari prosa. Maka direktori
`%TEMP%\opencode\l3h4h5_arsitek\` TIDAK dibuat (tidak ada path/hash
untuk dilaporkan). **Tie-break S27 tidak terpicu:** tiga rekaman --
JSON coder, dokumen hasil, rekomputasi auditor -- plus probe saya
SEPAKAT penuh; tidak ada selisih sehingga hitung-ulang penuh tidak
wajib.

**(d) Verifikasi T1 dari data -- COCOK (TEMUAN-1 terkonfirmasi).**
Probe sesi ini (M1 2024-2025 + label sesi resep beku):

```
hour_utc  London  NewYork  Tokyo
0              0        0  31133  (100% Tokyo)
1              0        0  31138  (100% Tokyo)
7          17990        0  13140  (campur London/Tokyo)
12         31133        0      0  (100% London)
13         31130        0      0  (100% London)
14         31134        0      0  (100% London)
15         13139    17999      0  (campur London/NewYork)
```

Prosa `hasil:1197` "semua 6 bar dalam sesi London/NewYork" dan
`:1229` "keduanya tetap dalam sesi London/NewYork" terbukti SALAH:
2 dari 6 jam hitung-ulang (0, 1) adalah 100% Tokyo; pada bacaan lock
pun jam 0 = 100% Tokyo dan jam 7 campur. Lock `:111` sendiri
menyatakan "parsial, bukan eksklusif". Angka hitungan (`n_Off = 0`,
share 0,6833) tidak terpengaruh (Tokyo bukan Off) -- temuan
non-penentu, tetapi argumen kelayakan sesi-pintu yang menyesatkan.
P-1 WAJIB menyitir angka [O6], DILARANG menyitir prosa :1197/:1229.

---

## P-1. Vonis resmi H4 -- TAHAN (DIPUTUS)

**(a) Konfirmasi, bukan beda-pendapat.** Kriteria lock `:124-125`
verbatim ("GUGUR bila >=2 dari 6 jam teratas jatuh di Off pada data
OOS baru (kanon M2), ATAU EV-after-cost 6 jam masuk <= 0";
operasionalisasi spec `:100-103, :266, :270`) diterapkan pada angka
yang dua pihaknya sepakati: (i) kriteria-(a): `n_Off = 0` pada
KEDUA bacaan -- hitung-ulang `[14,13,0,15,12,1]` (JSON + [O6],
any_off = 0, maj_off = 0) maupun lock `[14,13,0,15,12,7]`
(re-audit R3: `n_Off = 0`) -- 0 < 2, negatif; tidak ada tukar
(R3: EV hanya jam tetap `sh4.py:329`, pola hanya top-6
`sh4.py:158-160`; jam 7 tercatat 519 trade EV, jam 1 nol trade).
(ii) kriteria-(b): median EV pool `0.014399999999998407` > 0
(JSON + [O8], n 3114, join-gate 47721==47721, exit 158/15/2941),
negatif. Keduanya negatif -> keluaran formula TAHAN disahkan.
PERINGATAN T1: sitiran angka yang sah adalah share LondonNY
`0.6832894546066546` + hitungan `n_Off` dari [O6]; prosa :1197/:1229
salah dan dilarang disitir (koreksi resmi tercatat di S-V(d)).

**(b) Vonis resmi H4, kalimat tunggal yang dikutip:**

> **Vonis resmi H4: TAHAN.**

**(c) Catatan kejujuran vonis:** TAHAN ini tipis dan bersyarat
konteks -- median pool +0,0144 JPY dengan tanda tahun berbalik
(2024 +0,04835 vs 2025 -0,00505; disposisi di EKS-3). Kriteria lock
memakai median pool (spec Q1 pool tunggal), sehingga vonis sah;
tetapi vonis ini DILARANG dibaca sebagai klaim ketahanan (lihat
P-5 klausul dua arah).

---

## P-2. Vonis resmi H5 -- GUGUR, TELAK (DIPUTUS)

**(a) Konfirmasi, bukan beda-pendapat.** Aturan lock `:147-148`
("pada setiap sub-populasi hit-rate real <= placebo -> tak
dieksploitasi"; operasionalisasi spec `:100, :310`: sel positif bila
lolos Holm alpha 0,01 atas 4 p, TAHAN bila >= 1 sel positif).
Hasil: p Sydney 0,244, Tokyo 0,291, London 0,5176, NewYork 0,7658
(JSON + [O13]/[O14]); urutan Holm `[Sydney,Tokyo,London,NewYork]`
dengan ambang 0,0025 / 0,00333 / 0,005 / 0,01 -- p terkecil 0,244 >
ambang pertama 0,0025 -> berhenti di posisi 1 -> nol reject ->
4/4 sel gagal. Agregat Q4-ALL deskriptif (diff 0,0031, p 0,4373)
non-penentu sesuai spec Q2. Tidak ada pasal lock yang mendukung
pembacaan berbeda.

**(b) Vonis resmi H5, kalimat tunggal yang dikutip:**

> **Vonis resmi H5: GUGUR.**

**(c) Ketelakan:** GUGUR-nya H5 TELAK, bukan tipis -- p terkecil
(0,244) sekitar 100x lipat ambang Holm pertama (0,0025); dua dari
empat diff bertanda negatif (London, NewYork); keempat CI95
memuat 0. Tidak ada sel yang mendekati signifikansi pada alpha
mana pun yang masuk akal pra-registrasi.

---

## P-3. Disposisi EKS-1--EKS-4 (DIPUTUS)

**EKS-1 -- selisih lock-vs-hitung-ulang (7->1): DIPUTUS sebagai
keputusan sadar, klaim coder ditolak.** Lock `:113-119` =
`[14,13,0,15,12,7]`; hitung-ulang OOS = `[14,13,0,15,12,1]`
(JSON sesi ini; `pool_identik_lock = False`); komposisi sesi
berbeda (jam 7 London+Tokyo vs jam 1 Tokyo 100% -- S-V(d)).
Klaim coder "tidak ada eskalasi wajib" (DEV-B2-1, `hasil:1230`)
DITOLAK eksplisit: auditor benar bahwa benda uji kriteria-(a)
berubah sehingga keputusan sadar arsitek wajib dicatat.
Keputusan: (i) "lock tetap dipakai" untuk uji EV dicatat sebagai
keputusan sadar -- EV dihitung HANYA pada 6 jam tetap lock
(`sh4.py:329`, jam 7 = 519 trade, jam 1 = 0 trade); (ii) uji pola
memakai top-6 hitung-ulang sesuai spec Q4 (larangan tukar dua
arah dipatuhi, R3); (iii) vonis tidak bergantung pada pilihan
bacaan karena `n_Off = 0` pada KEDUA bacaan (JSON + R3).
Eskalasi TERTUTUP oleh putusan ini.

**EKS-2 -- cutoff_2025 dari ATR 2024: DIPUTUS COMPLIANT,
bukan-peeking.** `cutoff_2025 = kuantil-0.75 ATR 2023-2024`
(`1.6039464285714264`, JSON sesi ini) adalah keputusan pra-registrasi
spec Q5 (expanding blok-tahunan, alasan: kuartil harus mencerminkan
rezim volatilitas berjalan), dihitung SEKALI pre-eval
(`sh5.py:419-422` sebelum `:433`), diizinkan S-B.5 ("2023(/2024)").
ATR 2024 yang dipakai adalah data rezim, bukan hasil evaluasi --
tidak ada informasi hasil yang bocor ke seleksi populasi. Sah
compliant; dicatat agar tak disalahpahami kelak.

**EKS-3 -- tanda 2024 (+) vs 2025 (-): DIPUTUS sebagai peringatan
stabilitas TERCATAT, tanpa konsekuensi vonis.** Median 2024
`+0,04834999999999022` (n 1560) vs 2025 `-0,005049999999992838`
(n 1554) -- tanda berbalik (JSON sesi ini). Ini BUKAN cacat
eksekusi (dilaporkan jujur sebagai deskriptif, `sh4.py:419-429`).
Kriteria lock memakai median pool (spec Q1 pool tunggal 2024-2025),
dan median pool +0,0144 > 0 -- vonis TAHAN tidak goyang. Tetapi
makna TAHAN digoyang sebagai klaim ketahanan: stabilitas antar
tahun GAGAL diamati; konsumen hilir DILARANG membaca TAHAN sebagai
bukti strategi stabil. Peringatan ini mengikat interpretasi, bukan
mengubah vonis.

**EKS-4 -- definisi Off beku + fingerprint: DIPUTUS AMAN.**
`n_Off = 0` bergantung pada `session_label` beku
(`_eda_common.py:17-38`, Tokyo 9-18 Asia/Tokyo) -- definisi yang
sama dipakai EDA, coder, auditor, dan probe saya. Terproteksi
assert fingerprint di kedua harness (`sh4.py:121-126`,
`sh5.py:366-367`) yang GAGAL-eksekusi bila definisi bergeser.
Sahkan aman; tidak ada tindak lanjut.

---

## P-4. Disposisi T1--T6 + standing rule C8 (DIPUTUS)

**T1 (MEDIUM, non-penentu) -- DIPUTUS: aturan sitir-angka-saja
mengikat, tanpa edit dokumen beku.** Prosa salah di `:1197/:1229`
tidak diperbaiki dengan mengedit `hasil-lapisan3-H4H5.md` --
dokumen beku TIDAK BOLEH diedit (hash `f06a8e27...` adalah jangkar
integritas rantai bukti). Sebagai gantinya: (i) koreksi resmi
tercatat di putusan ini (S-V(d): jam 0/1 = 100% Tokyo);
(ii) konsumen hilir WAJIB menyitir angka [O6]
(`share_LondonNY = 0.6832894546066546`, `n_Off = 0`), DILARANG
menyitir prosa :1197/:1229/:1230. Mekanisme yang dipilih: aturan
sitir mengikat, bukan adendum/erratum. Severity tetap MEDIUM.

**T2 (MEDIUM, non-penentu) -- DIPUTUS: S-B.10 TETAP BERLAKU,
C8 Batch-2 VACUOUS tetapi patuh-spec, pola diganti ke depan.**
Status: S-B.10 ("guard nilai-vs-diri dilarang") TETAP sebagai aturan;
re-audit benar menandai VIOLATED pada C8 coder. Namun coder patuh
pada gate C8 yang spec sendiri tetapkan -- ini ketegangan internal
spec, bukan kelalaian coder; severity TEMUAN-2 tetap MEDIUM,
tidak naik (bukan fabrikasi) dan tidak turun (kontrolnya sungguh
tidak mengikat apa pun: hash dapat dihitung ulang dari dokumen
yang sudah diubah). Pola pengganti C8 untuk batch berikutnya
(DIPUTUS, mengikat spec berikutnya): **pengikatan eksternal** --
dokumen TIDAK memuat self-hash; hash (git-blob + sha256) dihitung
SETELAH tulis final dan dilaporkan di kanal luar dokumen (pola
yang auditor Batch-2 pakai di re-audit `:695-704`, tanpa self-hash).
Dokumen putusan INI memakai C8 dengan lubangnya dinyatakan
(konsistensi rantai dengan preseden Batch-1) -- lihat bagian C8.

**T3 (LOW) -- DIPUTUS: tutup sebagai catatan.** `:1199`
"0.5211946050096339%" salah satuan (pecahan ditulis persen);
JSON artefak benar (pecahan). Murni prosa, tak dipakai sebagai
penentu di mana pun. Tutup; tidak ada tindak lanjut.

**T4 (LOW) -- DIPUTUS: tutup sebagai catatan.** 1 dari 715308 bar
pool mewarisi close 2023 untuk `r` (`sh4.py:152`); top-6 identik
dengan/without warisan (`[14,13,0,15,12,1]`, `n_Off = 0` --
re-audit TEMUAN-4); praktik cocok kanonik `_build_eda05.py` dan
diumumkan di komentar kode. Yang hilang hanya pengungkapan di
dokumen. Immaterial numerik; tutup. (Pengungkapan efek-batas
menjadi kewajiban dokumen sejak R-B2 Batch-1; tidak perlu rule
baru.)

**T5 (LOW) -- DIPUTUS: tutup sebagai catatan.** `sh4_run3.log` /
`sh5_run3.log` tak diumumkan di dokumen; determinisme terbukti 3x
(run1, run2, replikasi auditor -- R6 byte-identik, toolchain
identik). Murni higiene artefak; tutup dengan catatan: run
tambahan di direktori kerja WAJIB diumumkan atau dibersihkan
sebelum serah-terima.

**T6 (LOW) -- DIPUTUS: tutup sebagai catatan + rekomendasi ke
pemilik repo.** `src/features/build_labels.py` +
`tests/test_build_labels.py` untracked (di luar kendali versi;
C2-git buta terhadapnya) -- mtime sebelum batch, hash cocok
read-proof, `find -newermt` kosong, AFTER==BEFORE -- klaim "nol
tulis lindung" tetap sah. Rekomendasi (di luar wewenang arsitek):
`git add` kedua file agar gerbang C2 buta-proof. Tutup.

---

## P-5. Batas scope -- kunci anti-merambat (DIPUTUS)

1. **H1/H2/H3 tetap GUGUR FINAL** (putusan H1H2 P-1/P-2, putusan H3
   P-4) -- tak tersentuh putusan ini sejengkal pun.
2. **Tidak ada ambang/lock/vonis lain berubah** -- ambang H4
   (lock `:124-125`), ambang H5 (lock `:147-148`), alpha 0,01,
   seed/B/konstanta placebo, artefak beku, D4/M15/M1/M5 semuanya
   utuh tanpa addendum.
3. **Klausul anti-penyelamatan mengikat DUA ARAH** (lock `:48-51`,
   spec Q1, preseden H1H2 P-5 butir 4): kegagalan H5 DILARANG
   ditafsir-ulang via sub-sel/ambang/level/grid/window pasca-hoc
   (4 sel tertutup + agregat deskriptif = final); dan keberhasilan
   H4 (TAHAN) pun DILARANG diklaim kebal -- tanpa uji pra-registrasi
   segar di data segar -- terutama mengingat EKS-3 (tanda tahun
   berbalik).
4. Tie-break S27 tidak terpicu: coder dan auditor SEPAKAT pada
   seluruh angka penentu dan status gate (LULUS DENGAN TEMUAN);
   verifikasi saya (S-V) mengonfirmasi kesepakatan itu dari bahan
   mentah. Putusan ini mengesahkan keluaran formula menjadi vonis
   resmi + disposisi temuan/eskalasi + preseden. Severity temuan
   tertutup tidak berubah tanpa pasal (T1/T2 MEDIUM; T3--T6 LOW).

---

## Self-audit 3x adversarial (sebelum STOP)

**Putaran 1 -- Correctness.** (a) Hash S-2d (4 blob + HEAD) diukur
sesi ini, 5/5 cocok (S0; mismatch 0) -- putusan di atas dokumen yang
benar. (b) S-V(a)-(d) dikerjakan + dilaporkan: kode dibaca pada
baris penentu; angka diekstraksi dari JSON/sha sesi ini; tidak
run-ulang dengan rasional per butir di S-V(c); T1 diprobe dari
parquet mentah. (c) Tiap P berpasangan bukti mentah: P-1 -> JSON
`sh4_hasil_run1.json` + [O6] + R1/R3; P-2 -> JSON
`sh5_hasil_run1.json` + [O13]/[O14] + R2; P-3 -> EKS-1 (`sh4.py:329`
+ JSON `pool_identik_lock` + R3), EKS-2 (`sh5.py:419-433` + S-B.5),
EKS-3 (JSON per-tahun + [O8]), EKS-4 (`sh4.py:121-126`,
`sh5.py:366-367`); P-4 -> T1 (`hasil:1197/:1229` + S-V(d)),
T2 (`hasil:1299` + S-B.10), T3 (`hasil:1199`), T4 (`sh4.py:152`),
T5 (run3.log), T6 (git ls-files); P-5 -> putusan H3 P-4 + lock
`:48-51`. (d) Vonis H4/H5 masing-masing satu kalimat tunggal yang
dikutip (P-1(b), P-2(b)). (e) EKS-1--EKS-4 + T1--T6 masing-masing
diputus eksplisit; tidak satu pun digantung.

**Putaran 2 -- Bias & Asumsi.** (a) Ambang diterapkan verbatim:
kriteria-(a) `>= 2` dan kriteria-(b) `median <= 0` tidak dirapikan
agar H4 TAHAN -- justru P-1(c)/EKS-3 mencatat ketipisannya; Holm
0,01 tidak dilonggarkan agar H5 "hampir" (p 0,244 vs 0,0025 =
telak, bukan tipis). (b) T1 tidak menginfeksi penalaran vonis:
vonis H4 bersandar pada hitungan `n_Off`, bukan pada narasi sesi;
koreksi T1 dipakai untuk melarang sitiran, bukan untuk menggeser
ambang. (c) Tidak ada pintu penyelamatan diam-diam dua arah:
P-5 mengunci H5-gagal dari tafsir-ulang dan H4-TAHAN dari klaim
kebal; EKS-3 peringatan tercatat tanpa mengubah vonis.

**Putaran 3 -- Meta-check.** (a) Lock tak tersentuh tanpa addendum:
nol perubahan redaksi/ambang; satu-satunya aturan baru (pengganti
C8 eksternal) adalah aturan proses dokumen, bukan ambang uji.
(b) Ruang coder/auditor tidak diambil: tidak ada eksekusi, tidak
ada audit angka primer -- hanya vonis + disposisi + preseden di
atas rekaman yang dua pihaknya sepakati dan saya verifikasi.
(c) Severity lama tak berubah tanpa pasal (P-5 butir 4; P-4
masing-masing temuan). (d) Brief mandiri dipenuhi: S-V diputus
per huruf, P-1--P-5 tertutup, C8 terakhir, STOP menutup batch.

## C8 -- Blob putusan ini

Baris TERAKHIR berkas ini berisi blob dokumen TANPA baris tersebut --
direproduksi dengan (PowerShell, byte-exact):

```
$bytes = [System.IO.File]::ReadAllBytes("reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md")
$last = [Array]::LastIndexOf($bytes, [byte]10)
$prev = [Array]::LastIndexOf($bytes, [byte]10, $last - 1)
[System.IO.File]::WriteAllBytes("$env:TEMP/l3h4h5_putusan_noC8.tmp", $bytes[0..$prev])
git hash-object "$env:TEMP/l3h4h5_putusan_noC8.tmp"
```

CATATAN LUBANG (P-4/T2): kontrol ini VACUOUS sebagai anti-tamper
(dapat dihitung ulang dari dokumen yang sudah diubah); dipertahankan
di sini demi konsistensi rantai Batch-1, dengan lubang dinyatakan
terbuka. Batch berikutnya WAJIB memakai pengikatan eksternal.

STOP. Batch-2 TERTUTUP oleh putusan ini.

C8: 5bfa76a2d4e7ca9c44b184d8dd23e06ff5e38b10
