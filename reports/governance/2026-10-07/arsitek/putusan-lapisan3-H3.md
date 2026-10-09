# Putusan Arsitek -- Tindak Lanjut Lapisan 3-H3

**Peran:** Arsitek (AGENTS.md S26: merancang + memutus konflik; DILARANG
menulis kode produksi/implementasi). **BUKAN eksekusi, BUKAN audit ulang.**
**Tanggal:** 2026-10-08. **HEAD sesi ini:** `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
**Lingkup TERTUTUP -- 4 butir saja:** F-1, F-2, DEV-1/C2, S4b.
Bukan vonis H1/H4/H5, bukan ubah lock/ambang, bukan kalibrasi ulang,
bukan tambah alternatif/span, bukan eksekusi ulang harness.
**Dokumen yang diputus (dibaca UTUH langsung, bukan ringkasan):**
`Audit/reaudit-lapisan3-H3.md` (527 baris, blob `1c233a8d...`),
`arsitek/spesifikasi-lapisan3-H3.md` (215 baris, blob `dacd0708...`),
`coder/hasil-lapisan3-H3.md` (1051 baris, blob `fd52d722...`).
**Kontrak:** AGENTS.md v3.0 S5 (Klaim & Bukti), S20 (klaim wajib bukti),
S21 (uji dulu, simpulkan kemudian), S26 (pemisahan peran).

---

## S0. Klaim & Bukti sesi ini (S5)

Cara baca: TERVERIFIKASI = saya ukur/baca sendiri sesi ini;
TERVERIFIKASI (rujukan) = saya verifikasi keberadaannya di dokumen
ter-hash yang saya baca utuh; KEPUTUSAN = penilaian arsitek di putusan ini.

| Klaim | Status | Bukti |
|---|---|---|
| HEAD = `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` | TERVERIFIKASI | `git rev-parse HEAD` sesi ini |
| Blob reaudit = `1c233a8d327c13213673641ba1c329da370a3ef5` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob spec = `dacd07087f4e1f66154dcc75a259ecfcdb769043` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob hasil penuh = `fd52d72242109a74bbb9a9d5425033604b04145a` | TERVERIFIKASI | `git hash-object` sesi ini |
| Ketiga dokumen dibaca utuh sebelum memutus | TERVERIFIKASI | 527 + 215 + 1051 baris dibaca sesi ini |
| Staged = 0, tanpa commit/stash/checkout oleh sesi ini | TERVERIFIKASI | `git diff --cached --name-only` kosong, sesi ini |
| Angka sitiran (M1/M2/TAU/AUC/agreement/CI/hash) | TERVERIFIKASI (rujukan) | `hasil` [O6]-[O21] + reaudit Section C/E/F, keduanya ter-hash dan dibaca utuh |
| Tidak ada hitung-ulang ketiga oleh arsitek | KEPUTUSAN | rasional di S0.1 |

### S0.1 Mengapa tanpa hitung-ulang ketiga

Dua implementasi independen (coder harness + auditor rekomputasi dari nol
tanpa impor skrip coder) cocok sampai digit terakhir pada SEMUA statistik
penentu: chi2 M2 manual == scipy bit-cocok, `ratio_path` bit-exact dari
rekonstruksi independen, Youden/AUC pasangan-per-pasangan identik,
TAU bit-identik runtime & store, K1/K2/K3 identik pada dua pembacaan
(reaudit Section E + Lampiran B sha256 `23c29b0f...` / `d7927fb9...`).
Hitung-ulang ketiga tidak menambah informasi; arsitek memutus di atas
rekaman terverifikasi, bukan mengulanginya. Bila di masa depan dua
implementasi independen BERBEDA, hitung-ulang ketiga menjadi wajib --
aturan ini dicatat agar presedennya eksplisit.

---

## P-1. F-1 -- Instrumen S0 lebih lemah dari klaimnya (MEDIUM)

**Masalah (rujukan):** reaudit F-1 (`reaudit-lapisan3-H3.md:357-371`):
pembanding S0 memakai `np.isclose` toleransi default (`rtol=1e-5`),
sehingga "0 mismatch" (`hasil` [O6]) tidak menyiratkan reproduksi
bit-exact yang dituntut konsep artefak beku.
**Fakta penutup (rujukan):** auditor membuktikan dengan instrumen tepat --
`np.array_equal` bit_exact untuk keempat kolom float,
`max_abs_diff = 0.0`, pola NaN identik. Klaim S0 BENAR, instrumennya LEMAH.

**PUTUSAN P-1:**
1. Klaim S0 DITERIMA: D1 dibaca ulang mereproduksi D4 bit-exact
   (6/6 kolom, gap 234 / nongap 740, INK [330,320,324]).
   Provenans Uji-1 SAH; tidak ada eksekusi ulang.
2. Instrumen `isclose`-toleransi-default DINYATAKAN TIDAK MEMADAI untuk
   klaim ketiadaan-sel ("tanpa satu pun sel berbeda", "beku", "bit-exact").
   Standing rule ke depan: cek provenans WAJIB memakai perbandingan exact
   (`np.array_equal` / `pd.testing.assert_series_equal(..., check_exact=True)`)
   ATAU mencantumkan toleransi eksplisit di dokumen. Pelanggaran = temuan.
3. Tidak ada dampak ke vonis Uji-1 (IMMATERIAL) maupun Uji-2.

## P-2. F-2 -- chi2 M2 + kontras CI vs p pada alpha spec (MEDIUM)

**Masalah (rujukan):** reaudit F-2 (`:373-389`): spec menetapkan penentu
pada 1% (`p < 0,01`) tetapi efek pada 95% (CI95); chi2 2x3 memperlakukan
EKS (subset INK, nested 740 dari 974) sebagai sampel independen; CI95
paired `[+0,003008; +0,035234]` tidak memuat 0 sehingga tampak
berkontradiksi dengan `p = 0,629431041054359` (`hasil` [O9]).
**Fakta penutup (rujukan):** pada alpha spec 0,01 kontradiksi MENGHILANG --
CI99 paired memuat 0 pada 5/5 nilai B dan 7/7 seed; CI95 unpaired memuat 0
pada 7/7 seed; two-proportion z `p = 0,406` (reaudit E.2 `:227-249`).
`IMMATERIAL` invarian terhadap estimator, B, dan seed. Uji chi2 pada desain
bersarang bersifat konservatif (rujukan auditor), bukan pro-MATERIAL.

**PUTUSAN P-2:**
1. Vonis M2 (tidak material) dan hasil Uji-1 IMMATERIAL DITERIMA dan DIKUNCI.
   Tidak ada eksekusi ulang, tidak ada ambang baru.
2. Remedi disclosure WAJIB dicatat (tanpa hitung ulang -- angka auditor
   sudah ada): rekaman M2 dilengkapi CI99 berdampingan CI95, yaitu CI99
   paired MEMUAT 0 (5/5 B; 7/7 seed), sehingga kontradiksi semu tertutup
   pada alpha spec. Sitiran ini SAH sebagai TERVERIFIKASI (rujukan E.2).
3. Standing rule ke depan: uji homogenitas pada sampel bersarang WAJIB
   memakai estimator paired yang valid ATAU menyatakan eksplisit bahwa
   homogenitas diuji pada sampel bersarang; level-CI laporan efek WAJIB
   selaras dengan alpha penentu (atau keduanya dilaporkan dengan label).
4. Tidak ada dampak ke vonis; 234 tetap populasi penentu (DEV-2 tetap
   BELUM DIVERIFIKASI dan non-penentu -- lihat P-4 butir 5).

## P-3. DEV-1 / C2 -- Pola literal vs substansi + perbaikan pola

**Masalah (rujukan):** pola lolos C2 spec ("kedua output KOSONG") tidak
terpenuhi pada state repo pra-ada: `?? src/features/build_labels.py`,
`?? tests/test_build_labels.py`, dan 14 `reports/eda/progress/*.md`
berstatus ` D` sebelum tugas (`hasil:808-817`; reaudit F.1 `:295-321`).
**Fakta penutup (rujukan):** substansi terbukti lewat 4 jalur independen --
mtime (`find -newermt` kosong; mtime terakhir 18:30:12 persis `hasil:903`),
hash isi 9/9 identik (Section C.3), kolom index bersih (27 baris semuanya
worktree pra-ada, reaudit C.2), jejak `OUT` harness hanya di direktori
harness. Coder pertama kali melaporkan sendiri + eskalasi (jujur, tidak
menutupi). Keadaan worktree kotor pra-ada juga tercatat di re-audit
keempat S12 -- konsisten, bukan ulah sesi Lapisan 3-H3.

**PUTUSAN P-3:**
1. Mengadopsi putusan auditor: **C2 = LULUS (substansi) / GAGAL (pola
   literal).** Lapisan 3-H3 memenuhi C2 secara substansi.
2. Kegagalan pola adalah TANGGUNG JAWAB DESAIN spec, bukan coder.
   Tidak ada sanksi, tidak ada pengulangan tugas.
3. Amendemen pola C2 (wewenang arsitek, berlaku UNTUK SPEC BERIKUTNYA
   termasuk lapisan H4/H5 -- tidak retroaktif): pola lolos C2 WAJIB salah
   satu: (a) dibatasi pada berkas tracked, atau (b) didefinisikan sebagai
   perbandingan before/after (snapshot sebelum tugas vs sesudah).
   Pola "kedua output KOSONG" tanpa kualifikasi DINYATAKAN PENSIUN.
4. Fakta state pra-ada dicatat sebagai TERVERIFIKASI (rujukan): 2 berkas
   untracked tak pernah di-commit (sejalan larangan commit/stage);
   14 penghapusan eda pra-ada dari reorganisasi sebelumnya.

## P-4. S4b -- Kriteria tambahan: H3 GUGUR

**Prasyarat firing (rujukan):** Uji-2 = TIDAK STABIL, terverifikasi dua
implementasi independen -- coder [O13]-[O15] (`hasil:500-770`): K1 GAGAL
(AUC min 0,1559 < 0,65, bukan tipis), K2 GAGAL (agreement min 0,3154
primer / 0,3518 robust, bukan tipis), K3 GAGAL (A1 median B < A);
auditor E.4 (`:271-289`) cocok digit terakhir + `kedua_pembacaan_sama =
true`; tanpa GAGAL-eksekusi (n evaluable min 230 primer / 945 robust,
batas 200 terpenuhi). Baseline terkunci utuh: TAU bit-identik
`2.5951672079821496e-05`, n_B=111/n_A=129/NaN=19, flag_ref 0 beda vs D4.
Aturan S4b adalah keputusan arsitek DI DALAM spec (`spesifikasi:141-156`):
"TIDAK STABIL -> H3 GUGUR via kriteria tambahan S4b".

**PUTUSAN P-4 (inti putusan ini):**
1. S4b AKTIF. **H3 GUGUR via kriteria tambahan S4b.**
2. Filter regime (`rv_score`/TAU) DILARANG diaktifkan pada data mana pun.
3. Batas S4b (mengikat, dari spec): tidak mengubah ambang lock; tidak
   memvonis H1/H2/H4/H5; bukan izin kalibrasi ulang (Q1(a) tetap:
   DILARANG kalibrasi ulang di luar span 2023); S4b BUKAN lock
   (tidak mengamendemen berkas lock apa pun).
4. S4 (uji drawdown vs strategi diagnostik) sebagai gate aktivasi DINYATAKAN
   MOOT: aktivasi filter sudah dilarang sehingga gate tidak berfungsi.
   S4 tidak perlu dieksekusi. Spec diagnostik masa depan boleh
   mengkomisikan S4 murni-informatif, tetapi hasilnya tidak dapat
   mengaktifkan filter tanpa spec baru + uji stabilitas baru yang LULUS.
5. A-5 (pembacaan agreement) DITUTUP: pembacaan PRIMER (harfiah spec,
   "hari overlapping") ditetapkan sebagai pembacaan RESMI; ROBUST sebagai
   pendukung. Keduanya TIDAK STABIL sehingga pilihan non-material --
   dicatat agar tidak dibuka ulang.
   DEV-2 (subset 223) tetap BELUM DIVERIFIKASI, NON-BLOKIR untuk penutupan
   H3 (spec menamai 234 sebagai penentu); pemakaian masa depan wajib
   menerima identitas 11 hari sebagai input terlebih dulu (mengarang
   definisi = temuan).

---

## Batasan putusan (yang TIDAK diputus)

1. F-3, F-4, F-5 (LOW/redaksi) DICATAT sebagaimana adanya; saran auditor
   diteruskan sebagai higiene spec berikutnya; tidak ada aksi wajib,
   tidak ada perubahan vonis.
2. Tidak ada vonis H1/H2/H4/H5 di putusan ini. Angka "GUGUR" pada M1
   adalah formula verdict lock sebagai penilai materialitas, bukan hasil
   uji H1 Lapisan 3 (rujukan `hasil` S7 butir 6).
3. Tidak ada perubahan ambang/threshold (M1/M2/K1-K3/alpha), lock, kode,
   data, atau artefak beku. Cakupan data tetap 2023-01-02..2026-10-02.
4. Tie-break S27 tidak terpicu: coder dan auditor SEPAKAT pada vonis
   (IMMATERIAL / TIDAK STABIL / C2 substansi-lulus); putusan ini
   mengesahkan + menutup 4 butir eskalasi.

---

## Self-audit 1x

1. Lingkup = 4 butir eskalasi saja: tidak ada instruksi H4/H5 selain
   larangan yang sudah ada, tidak ada langkah eksekusi selain perintah
   verifikasi S0, tidak ada perubahan kode/data/ambang.
2. Setiap ambang penentu tertaut ke lock/spec pra-ada (M1->protokol:94-96,
   M2 alpha lock, K1->ambang H3, K3->basis lock, S4b->spec:141-156) --
   tidak ada angka dari data evaluasi; satu-satunya angka "baru" (CI99)
   adalah sitiran komputasi auditor yang sudah ada, bukan hitungan saya.
3. Peran S26 dipatuhi: arsitek tidak mengeksekusi harness, tidak
   mengaudit angka primer, hanya memutus di atas rekaman terverifikasi;
   staged = 0 dan HEAD tak berubah diukur sesi ini.

## C8 -- Blob putusan ini

Baris TERAKHIR berkas ini berisi blob dokumen TANPA baris tersebut --
direproduksi dengan (PowerShell, byte-exact):

```
$bytes = [System.IO.File]::ReadAllBytes("reports/governance/2026-10-07/arsitek/putusan-lapisan3-H3.md")
$last = [Array]::LastIndexOf($bytes, [byte]10)
$prev = [Array]::LastIndexOf($bytes, [byte]10, $last - 1)
[System.IO.File]::WriteAllBytes("$env:TEMP/l3h3_putusan_noC8.tmp", $bytes[0..$prev])
git hash-object "$env:TEMP/l3h3_putusan_noC8.tmp"
```

C8: 478fc831c82b703c1f632dc0dc1e0a0cf9acf174
