# Disposisi Arsitek -- Penutup Telaah Fondasi B (Diagnostik Selesai)

**Peran:** Arsitek (S26-S27; DILARANG ubah kode/data/config,
DILARANG commit/push). S-V dikerjakan sendiri -- tanpa itu vonis
buta. **Tanggal:** 2026-10-09. **HEAD:**
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` (staged tepat 2 T6).
**Lingkup TERTUTUP:** D-1--D-4. BUKAN vonis ulang, BUKAN H6.
**Aturan besi:** angka WAJIB output mentah (S5).

---

## S0. Gerbang sesi ini (7/7 COCOK + HEAD + staged 2 T6)

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec-B2
f06a8e27b916172f5824438acd545614360d3b57  hasil-B2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit-B2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan-B2 (H4 TAHAN FINAL)
ed436fddf607d3629fa226fd34d20ff60bf47232  protokol-B (218 baris)
0284f5f022ce1c147cefef6dd7780aded6acf820  hasil-B (416 baris)
fe11383b9bdd1e58819e32812eec75c52ab3aee9  putusan-H4b (119 baris)
```

S-V: (a) hasil-B dibaca UTUH 416/416 sesi ini. (b) R-4 cocok
3/3 (`2c76e2d0`, `ac9eed29`, `2ced2c88`); bacaan langsung JSON
sesi ini: INKLUSI `0.014399999999998407`/3114, EKSKLUSI
`0.01390000000001023`/3084, 2025 identik
`-0.005049999999992838` (`membalik_tanda: False`), n_Off 0/0,
porsi biaya `0.014621990418018331`, selisih RV/spread U-3 cocok.
(c) Tidak run-ulang: 3 run sha-identik + bacaan langsung cocok
digit-per-digit; nol keraguan angka; S27 tak terpicu.

---

## D-1. R-1 DISAHKAN -- EKS-3 DITUTUP sebagai noise tahunan

Eksklusi 5 hari/30 trade tidak membalik tanda 2025 (identik
digit terakhir); selisih pool `-0.0005`. Karantina BUKAN
penjelas ketipisan H4. **Vonis H4 TETAP TAHAN.**

## D-2. R-2 DISAHKAN -- "Bertepatan" dicatat, R-2 DIBUKA

RV 2025 lebih rendah + spread lebih rendah searah pembalikan
tanda (deskriptif, tanpa konsekuensi vonis). Ronde desain
berikut BOLEH mempertimbangkan stratifikasi tahun
pra-registrasi. BUKAN filter regime -- filter tetap DILARANG
tanpa spec baru + uji stabilitas LULUS (putusan H3 mengikat).

## D-3. R-3 DISAHKAN -- TANPA flag biaya-sensitif

Porsi biaya 1,46% << 50%; gap Holm H5 orde magnitude di luar
jangkauan biaya. H4 tanpa flag; H5 tanpa cabang aksi (GUGUR
telak final).

## D-4. Fondasi-B SELESAI (DIPUTUS)

Ronde diagnostik TERTUTUP: vonis H1-H5 tetap seluruhnya; H6
nihil (tidak dirumuskan); warisan = (a) opsi R-2 yang kini
dibuka D-2, (b) risiko rantai-bukti `%TEMP%` yang tercatat.
DILARANG butir baru.

---

## Self-audit 3x

**P1 Correctness:** 7/7 hash + bacaan langsung JSON cocok
prosa coder; tiap D berpasangan angka mentah.
**P2 Bias:** tidak ada D yang mengubah atau menggeser vonis (H4 TETAP
di D-1 ditegaskan, bukan diputus-ulang); D-2 membuka opsi,
bukan memerintahkan desain; D-3 tanpa pintu penyelamatan H5.
**P3 Meta-check:** lock/ambang/vonis utuh; H6 nihil; ruang
coder tak diambil; worktree selain file ini tak tersentuh;
STOP menutup fondasi-B.

STOP. Fondasi-B TERTUTUP oleh disposisi ini.
