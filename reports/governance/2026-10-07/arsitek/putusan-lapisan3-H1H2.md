# Putusan Arsitek -- Lapisan 3 Batch-1 (Vonis Resmi H1/H2)

**Peran:** Arsitek (AGENTS.md S26-S27: merancang + memutus konflik +
tie-break; DILARANG menulis kode produksi). **BUKAN eksekusi, BUKAN audit
ulang.** Fakta menang atas opini (S27 langkah 1) -- di sini coder dan
auditor SEPAKAT byte-per-byte pada semua angka penentu, sehingga tugas
putusan ini bukan arbitrase fakta melainkan **vonis + preseden**.
**Tanggal:** 2026-10-09. **HEAD sesi ini:**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
**Lingkup TERTUTUP -- 5 butir saja:** P-1 (vonis H1), P-2 (vonis H2),
P-3 (ambang burn-in), P-4 (standing rule Batch-2), P-5 (batas scope).
Bukan ubah lock/ambang, bukan kalibrasi ulang, bukan varian/ambang baru,
bukan vonis H3/H4/H5, bukan eksekusi ulang harness.
**Dokumen yang diputus (satu-satunya bahan; dibaca UTUH langsung, bukan
ringkasan):** `arsitek/spesifikasi-lapisan3-H1H2.md` (369 baris),
`coder/hasil-lapisan3-H1H2.md` (1175 baris),
`Audit/reaudit-lapisan3-H1H2.md` (511 baris),
`arsitek/putusan-lapisan3-H3.md` (204 baris, preseden pola).
Rujukan konsistensi (tidak wajib baca-ulang penuh, putusan konsisten
dengannya): lock S-H1/S-H2, `putusan-arsitek-H1-H5.md` (S1/S2),
`coder/protokol-H1-H2-H3.md:37-77`.
**Kontrak:** AGENTS.md v3.0 S5 (Klaim & Bukti), S20 (klaim wajib bukti;
output asli ditempel), S21 (uji dulu, simpulkan kemudian), S26 (pemisahan
peran), S27 (arbitrase). **Aturan besi (berlaku untuk putusan ini juga):
klaim tanpa output mentah = GAGAL.**

---

## S0. Bukti baca + Klaim & Bukti sesi ini (S5)

Gerbang S-2d brief: kelima hash diukur sesi ini dengan `git hash-object`
+ `git rev-parse HEAD` SEBELUM satu butir pun diputus. Hasil ukur:

```
fc29f6fa3595a89b918627dbdc71cfff82d8ebed  arsitek/spesifikasi-lapisan3-H1H2.md
1550209f40fde7998036c51c47a3f991b898f91c  coder/hasil-lapisan3-H1H2.md
e41431326825f121991d9d5284a8935de833abf4  Audit/reaudit-lapisan3-H1H2.md
c643c1c934055d1b85d972f4e2e2f65d8d57a69f  arsitek/putusan-lapisan3-H3.md
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD
```

Kelima nilai COCOK dengan S-2d brief (mismatch = 0). Gerbang LULUS;
putusan dilanjutkan. (Catatan jujur hitungan baris: `wc -l` reaudit =
510 newline; alat baca = 511 baris -- berkas tanpa newline akhir. Isi
identik terbukti oleh hash yang cocok; selisih ini non-material.)

Cara baca status: TERVERIFIKASI = saya ukur/baca sendiri sesi ini;
TERVERIFIKASI (rujukan) = saya verifikasi hash + isinya di dokumen
ter-hash yang saya baca utuh; KEPUTUSAN = penilaian arsitek di putusan ini.

| Klaim | Status | Bukti |
|---|---|---|
| HEAD = `e0b2b9f9...` | TERVERIFIKASI | `git rev-parse HEAD` sesi ini |
| Blob spec = `fc29f6fa...` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob hasil = `1550209f...` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob re-audit = `e4143132...` | TERVERIFIKASI | `git hash-object` sesi ini |
| Blob putusan H3 = `c643c1c9...` | TERVERIFIKASI | `git hash-object` sesi ini |
| Hasil (1175) + re-audit (511) + putusan H3 (204) + AGENTS S26-S27 dibaca utuh sesi ini | TERVERIFIKASI | 1175 + 511 + 204 baris + AGENTS `:619-684` dibaca sesi ini |
| Spec (369) dibaca utuh; isi byte-identik sesi ini | TERVERIFIKASI (rujukan) | dibaca utuh sesi sebelumnya; hash cocok sesi ini |
| Angka sitiran P-1/P-2 ([O6]/[O8]/[O11]/[O12], G.2/G.4/G.5) | TERVERIFIKASI (rujukan) | `hasil` + re-audit Section G, keduanya ter-hash dan dibaca utuh |
| Tidak ada hitung-ulang ketiga oleh arsitek | KEPUTUSAN | rasional di S0.1 |
| Staged = 0, tanpa commit/stash/checkout oleh sesi ini | TERVERIFIKASI | `git diff --cached --name-only` kosong, sesi ini (S5) |

### S0.1 Mengapa tanpa hitung-ulang ketiga

Dua implementasi independen -- harness coder (2x run, sha256 identik
`41b3630c...` / `c818aad3...`) dan rekomputasi auditor dari nol tanpa
impor skrip coder (4 run, `cmp` IDENTIK coder-vs-auditor) -- cocok
bit-exact pada SEMUA angka penentu: gate S1 9/9 presisi penuh, CI95 S-H1,
chi2/p kriteria-ii, 140 trade H2 per-trade (0 selisih > 1e-9), VR5/15/60
bit-per-bit, seluruh suplemen S3 (re-audit G.1-G.5; hasil [O5]-[O13]).
Hitung-ulang ketiga tidak menambah informasi; arsitek memutus di atas
rekaman terverifikasi, bukan mengulanginya. Preseden H3 (putusan H3
S0.1) ditegakkan: bila dua implementasi independen BERBEDA, hitung-ulang
ketiga menjadi wajib.

---

## P-1. Vonis resmi H1 -- GUGUR (DIPUTUS)

**(a) Konfirmasi, bukan beda-pendapat.** Keluaran formula S-H1 = GUGUR
via kriteria (i) lock: CI95 selisih median drift (trending real-time vs
range real-time) `[-0.02668182694022586, +0.05242264543726398]` MEMUAT 0
(`hasil` [O6], `hasil:403-404`); kriteria (ii) tidak terpenuhi
(chi2 = 3.333835311042838, p = 0.18882820311496487 >= alpha 0,01).
Penerapan ambang lock benar: kriteria (i) memakai estimator unpaired
(disjoint) day-level B=10000 seed 20261006 sesuai standing rule P-2/F-3;
kriteria (ii) chi2 tahun x trending/bukan 2023-2025 tanpa Yates sesuai
pin spec. Auditor merekonstruksi dari nol dan cocok digit terakhir
(re-audit G.5 `:344-359`), termasuk R1/R2/R3 yang ketiganya GUGUR dan
agreement 98,03% (18/914 pindah keranjang). Tidak ada pasal lock yang
mendukung pembacaan berbeda; tidak ada angka yang menopang TAHAN.

**(b) Vonis resmi H1, kalimat tunggal yang dikutip:**

> **Vonis resmi H1: GUGUR.**

**(c) Status Q1: TIDAK ADA DIVERGENSI.** Uji real-time GUGUR searah
verdict-lock M1 GUGUR (`hasil` [O8]: `searah_dengan_M1 = true`,
`divergence_annotation = false`,
`eskalasi_sebelum_dipakai_ke_mana_pun = false`). Maka sesuai relasi Q1
yang saya putus di spec: M1 disitir sebagai anotasi sensitivitas
(Uji-1 IMMATERIAL -- gap-flag bukan penggerak klasifikasi), dan
**eskalasi Q1 = false; tidak ada tindak lanjut Q1.**

---

## P-2. Vonis resmi H2 -- GUGUR, FINAL tanpa menunggu 2026 (DIPUTUS)

**(a) Konfirmasi, bukan beda-pendapat.** Keluaran formula S-H2 = GUGUR
via kriteria EV lock ("median <= 0 pada >= 2 tahun"): median EV-per-trade
2023 `-0.016099999999990906` (n=47), 2024 `-0.06060000000000443` (n=42),
2025 `-0.044099999999982493` (n=51) -- **3/3 tahun <= 0**
(`hasil` [O11], `hasil:740-766`). Kriteria VR tidak terpenuhi
(rata-rata VR = `1.0265420777270247` > 1, `hasil` [O12]), tetapi aturan
lock adalah "salah satu terpenuhi" sehingga hasil EV saja cukup.
Auditor membangun ulang loop strategi dari nol (termasuk hitung-ulang
ATR sendiri): 140 trade cocok 0-selisih, EV/cost/SL/TP benar untuk
semuanya, VR bit-per-bit (re-audit G.2 `:271-292`, G.4 `:323-340`).
Seluruh 140 trade berbiaya London 0.61, fallback Off 0 kejadian --
asumsi biaya spec terpenuhi tanpa sisa. Tidak ada pasal lock yang
mendukung pembacaan berbeda.

**(b) Vonis resmi H2, kalimat tunggal yang dikutip:**

> **Vonis resmi H2: GUGUR.**

**(c) Implikasi B4-06 / tahun ke-4: VONIS INI FINAL, TIDAK MENUNGGU 2026
penuh.** Diputus eksplisit, tidak digantung. Alasan: ambang lock
didefinisikan atas "3 tahun utuh 2023-2025 OOS" dan sudah terpenuhi
3/3 -- kriteria terlampaui pada jendela OOS terkunci yang lengkap.
Lock tidak menyediakan mekanisme pembalikan via tahun tambahan apa pun,
dan spec mengecualikan 2026 PENUH dari populasi H2 (bukan parsial yang
menunggu lengkap). Data 2026 kelak tidak dapat mengubah vonis ini;
ambang 4-tahun ("MENUNGGU DATA" di lock) bila kelak diuji adalah
hipotesis/spec BARU dengan addendum berversi, bukan kelanjutan putusan
ini.

---

## P-3. Ambang burn-in eksplisit -- kanonik 60 POSISI, tanpa re-run (DIPUTUS)

**(a) Ditetapkan sebagai kanonik ke depan:** "60 hari riwayat" =
**60 POSISI hari-broker** dengan median expanding skipna (min_periods
default) -- tepat pembacaan yang dieksekusi coder (`hasil` S-4.3:
n_non_evaluable 60, 2023-01-02..2023-03-24, evaluable 914, 46 nilai
`range_atr` pada ambang pertama dilaporkan apa adanya). Ini BUKAN
pilihan pasca-lihat-hasil: ditetapkan sebelum run dan dilaporkan
terbuka termasuk konsekuensinya.

**(b) Re-run Batch-1 TIDAK diperlukan -- posisi auditor DISETUJUI.**
Auditor menghitung ulang kedua pembacaan dari nol: 60 posisi -> GUGUR
(CI95 memuat 0; p = 0,1888), 60 nilai non-NaN (n_non_eval 74,
n_evaluable 900) -> GUGUR (CI95 memuat 0; p = 0,2265) (re-audit H.1
`:370-408`). p pada kedua pembacaan (0,19-0,23) jauh di atas alpha
0,01; tidak satu pun angka penentu bergerak. Mengulang batch demi
ambang yang terbukti non-penentu adalah biaya tanpa informasi.

**(c) Standing rule (mengikat spec Batch-2 dan seterusnya):** setiap
spec yang memakai ambang riwayat/window WAJIB menyatakan eksplisit
"posisi" vs "nilai non-NaN" + `min_periods`/aturan-NaN; kebisuan spec
atas hal ini = cacat spec (MEDIUM), bukan hak pilih pelaksana. Tanpa
butir ini putusan belum lengkap -- butir ini memenuhinya.

---

## P-4. Standing rule untuk Batch-2 -- panen preseden (DIPUTUS)

**R-B1 -- Manifest parameter / anti-salah-ketik (wajib di setiap spec
Batch-2).** Setiap spec WAJIB memuat tabel manifest ala `hasil` S-1:
tiap nilai operasional berpasangan dengan sumbernya (spec S/baris,
lock, config); nilai tanpa sumber = GAGAL-eksekusi bila dipakai.
*Alasan satu paragraf:* Batch-1 selamat dari empat jebakan salah-ketik
(14:45-vs-15:00, sesi/biaya London-vs-NewYork, satuan pip/JPY, tahun
date_broker-vs-UTC) BUKAN karena keberuntungan melainkan karena
manifest memaksa tiap nilai menunjuk sumbernya sebelum run; tanpa
manifest, jebakan semacam itu hanya tertangkap bila auditor beruntung
melihatnya. Manifest mengubah ketelitian dari kebajikan personal
menjadi syarat mesin.

**R-B2 -- Bucket akunting: partisi populasi WAJIB genap (pola DEV-B2,
bukan ad-hoc).** Setiap pembagian populasi (hari/bar/trade) WAJIB
dijumlahkan kembali ke universe dengan bucket bernama eksplisit
(pola: 0 hari-tanpa-bar + 369 bar-ada-tanpa-sinyal + 269
sinyal-tanpa-konfirmasi + 140 trade = 778; `hasil` [O10], re-audit
G.3). Hari/bar yang hilang senyap = GAGAL. Bucket tambahan deskriptif
diizinkan dan justru diwajibkan bila kategorinya ada; yang dilarang
adalah kategori tanpa nama.
*Alasan satu paragraf:* tanpaInvariant penjumlahan, eksklusi buta dapat
bersembunyi sebagai "pembersihan data" yang tak tercatat; DEV-B2
membuktikan pola sebaliknya -- 369 hari `close<=open` yang nyaris
menjadi lubang akunting justru menjadi bukti kelengkapan karena
diberi nama dan dijumlahkan. Aturan ini membuat S-B.2 (larangan
eksklusi buta) dapat diverifikasi mesin, bukan sekadar dideklarasikan.

**R-B3 -- Catatan realitas strategi DEV-B3 untuk desain spec H4/H5
(implikasi desain, bukan temuan).** Bila aturan exit per-bar
(`close<open` tiap bar) berkompetisi dengan SL/TP berjarak >= 1x ATR,
exit-sinyal mendominasi secara mekanis (140/140; 47,1% keluar di bar
monitoring pertama; jarak terdekat ke SL/TP saat exit min 0,26 JPY --
re-audit H.2 `:410-434`). Spec H4/H5 yang memakai SL/TP WAJIB
melaporkan distribusi jenis-exit sebagai deskriptif wajib dan
menjustifikasi jarak SL/TP relatif terhadap frekuensi cek exit;
strategi yang exit risikonya tidak pernah tersentuh adalah fakta
desain yang harus dikonfrontasi, bukan anomali untuk disembunyikan.
*Alasan satu paragraf:* SL/TP yang tak tersentuh berarti profil risiko
tercatat (1:2) bukan profil risiko aktual; tanpa aturan ini Batch-2
dapat mengklaim karakteristik risiko dari parameter yang tidak pernah
aktif. R-B3 bukan temuan melawan S-H2 (yang sah apa adanya) melainkan
pagar agar desain berikutnya jujur tentang mekanikanya sendiri.

**R-B4 -- Lingkungan kanonik untuk verifikasi gate (tambahan).**
Gate C4/C5 WAJIB dijalankan dengan venv kanonik (python + ruff versi
terkunci repo); `.venv` BUKAN kanonik -- laporannya dicatat sebagai
catatan, tidak pernah sebagai vonis (re-audit C `:138-154`; DEV-B5
`hasil` S-8.5).
*Alasan satu paragraf:* dua ruff (0.6.9 vs 0.16.10) memformat `.md`
secara berbeda; tanpa kanonik, gate yang sama memberi jawaban berbeda
di dua mesin dan sengketa versi menjadi tak terputus. Satu gate, satu
lingkungan, tercatat versinya.

---

## P-5. Batas scope -- kunci anti-merambat (DIPUTUS)

1. **H3 tetap GUGUR** via S4b (putusan H3 P-4); larangan filter
   (`rv_score`/TAU) pada data mana pun tetap berlaku penuh -- putusan
   ini tidak membukanya sejengkal pun.
2. **H4/H5 BELUM divonis dan tak tersentuh putusan ini** -- tidak ada
   kalimat di dokumen ini yang boleh disitir sebagai vonis, ambang,
   atau izin untuk H4/H5. R-B3 adalah pagar desain, bukan vonis awal.
3. **Tidak ada ambang/lock/vonis lain yang berubah** -- ambang H1
   (`:29-30` lock), ambang H2 (`:76-78` lock + S2), alpha 0,01,
   seed/B, artefak beku, dan D4 semuanya utuh tanpa addendum.
4. **Klausul anti-penyelamatan mengikat DUA ARAH** (lock `:48-51`,
   spec Q1): kegagalan H1/H2 DILARANG ditafsir-ulang via reversal-day,
   usia-tren pasca-hoc, atau eksklusi hari/flag apa pun; dan -- bila
   kelak ada keberhasilan di hipotesis lain -- keberhasilan itu pun
   DILARANG diklaim kebal terhadap reversal-day tanpa uji pra-registrasi
   segar di data segar.
5. Tie-break S27 tidak terpicu: coder dan auditor SEPAKAT pada seluruh
   angka penentu dan status C1-C9 (LULUS); putusan ini mengesahkan
   keluaran formula menjadi vonis resmi + menutup ambang burn-in +
   memanen preseden. Severity temuan tertutup tidak berubah (F-3/F-4/F-5
   H3 tetap LOW; Uji-1 IMMATERIAL tetap; DEV-B1/B3 tetap MEDIUM
   non-penentu).

---

## Self-audit 3x adversarial (sebelum serah)

**Putaran 1 -- Correctness.** (a) Kelima hash S-2d + HEAD diukur sesi
ini dan cocok semua (S0; mismatch 0) -- putusan di atas dokumen yang
benar. (b) Tiap P-1..P-5 berpasangan bukti mentah: P-1 -> [O6]/[O8] +
G.5; P-2 -> [O11]/[O12] + G.2/G.4; P-3 -> [O6] + H.1; P-4 -> S-1/`hasil`
S-1 + [O10]/G.3 + H.2 + re-audit C; P-5 -> putusan H3 P-4 + lock
`:48-51`. (c) Vonis H1/H2 masing-masing satu kalimat tunggal yang
dikutip (P-1(b), P-2(b)). (d) Ambang burn-in diputus eksplisit
(60 posisi + min_periods default + rule ke depan), tidak digantung.
(e) B4-06 diputus eksplisit (FINAL), tidak digantung.

**Putaran 2 -- Bias & Asumsi.** (a) Tidak ada ambang yang "dirapikan":
kriteria (i)/(ii) H1 dan EV/VR H2 diterapkan verbatim; R-B1..R-B4
mengetatkan disiplin, tidak menggeser satu pun ambang penentu.
(b) Tidak ada pintu penyelamatan diam-diam: P-5 mengunci dua arah;
2026 dikecualikan PENUH dari H2 sehingga tidak ada jalan "tunggu data
lalu balikkan"; reversal-day/usia-tren dilarang eksplisit.
(c) Q1 tidak dibuka ulang: searah dikonfirmasi, eskalasi=false,
anotasi M1 tetap sitiran konteks bukan penentu.
(d) DEV-B1/B3 tetap MEDIUM non-penentu -- tidak dinaikkan untuk
menjustifikasi apa pun, tidak diturunkan menjadi catatan kaki.

**Putaran 3 -- Meta-check.** (a) Brief mandiri dipenuhi: seluruh bahan
(S-2d, angka [O6]/[O8]/[O11]/[O12], p, VR, n) tertuang di brief atau
terukur sesi ini; tidak ada pointer internal yang tak terverifikasi.
(b) Lock tak tersentuh tanpa addendum: nol perubahan redaksi/ambang;
satu-satunya "aturan baru" (S4b-style) tidak ada -- R-B1..R-B4 adalah
aturan proses spec, bukan ambang uji. (c) Ruang coder/auditor tidak
diambil: tidak ada eksekusi, tidak ada audit angka primer, hanya vonis
+ preseden di atas rekaman yang dua pihaknya sepakati. (d) Severity
temuan lama tak berubah (P-5 butir 5).

## C8 -- Blob putusan ini

Baris TERAKHIR berkas ini berisi blob dokumen TANPA baris tersebut --
direproduksi dengan (PowerShell, byte-exact):

```
$bytes = [System.IO.File]::ReadAllBytes("reports/governance/2026-10-07/arsitek/putusan-lapisan3-H1H2.md")
$last = [Array]::LastIndexOf($bytes, [byte]10)
$prev = [Array]::LastIndexOf($bytes, [byte]10, $last - 1)
[System.IO.File]::WriteAllBytes("$env:TEMP/l3h1h2_putusan_noC8.tmp", $bytes[0..$prev])
git hash-object "$env:TEMP/l3h1h2_putusan_noC8.tmp"
```

C8: 9ad9f80588ed66697056e4be8fd7a1f02a72c2aa
