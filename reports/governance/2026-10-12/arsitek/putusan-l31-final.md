# Putusan Final L3-1 -- Vonis Biner B-4 (Arsitek, 2026-10-13)

Peran: arsitek dirangkap asisten (S1A ASSISTANT_RULES, keputusan
user 2026-10-13). Verifikasi S-V di bawah dikerjakan sendiri atas
bahan yang diperiksa sendiri, bukan vonis buta atas ringkasan.

## S-2d. Gerbang hash (diukur sesi ini, sebelum memutus)

```
d166d189aa0834c66b81ea89ac0bcfa8e7b1b3e7  spesifikasi-lapisan3.md
23c5fdf80e00619a0a06cd017b7cb978b71fa933  putusan-l30-audit.md
1921326dc4bb25b1277662c267edbc2916ed0e58  amandemen-l31-metrik.md
b6a40abd4928720d0f78f1af65bd91680af08b65  laporan-coder-eda07-l31.md
36dbad57a7b1ddbdc6d7b296069df8e16b1c606d  reaudit-l31.md
b18992b5e57d45c125aacf3ca868c2f9e135d9d1  HEAD (tak bergerak)
staged NOL
```
Semua COCOK nilai rujukan. Brief eksternal
`2026-10-13_putusan-l31-arsitek.md` DINYATAKAN MOOT (diganti
putusan langsung ini per peran gabungan).

## S-V. Verifikasi bahan (ringkas, semua diperiksa sendiri)

- TABEL M3 103 = LOLOS 68 / GUGUR 35; rekonstruksi aturan =
  vonis 103/103 oleh dua pihak independen (asisten + auditor).
- Margin headroom dua sisi (Brier min 3,06x; MSE min 11,2x);
  konjungsi mengikat (29+8+12 pola gagal per-kaki).
- Audit LOLOS PROSEDURAL (452 baris dibaca penuh): 11 mandat nol
  selisih, 0 TINGGI/0 MENENGAH, S6 jujur, S18 jujur.
- Split aman (max-train < min-test, test tak sentuh 2026);
  verbatim run 9 identik (sel10/sel11 byte-per-byte, K24 24/24).
- R1-R4 nol dampak angka; I1-I4 catatan sah.

## V-1. VONIS: GO (cabang (a)) -- TEPAT SATU

GO didefinisikan ketat: **meminta persetujuan user untuk menyusun
spec pemodelan pra-registrasi atas register V-2.** BUKAN
paper-trade, BUKAN live, BUKAN sinyal. Marginal-rate bukan sinyal.

Alasan: 68 pasangan mengalahkan null di KEDUA semester test
dengan headroom, angka terverifikasi tiga lapis, audit bersih
temuan material. Hasil negatif pun akan sah (S8A butir 2), tapi
hasil ini positif -- mematikan pendekatan di sini akan membuang
informasi yang sudah dibayar mahal verifikasinya.

Syarat mengikat spec pemodelan (pelanggaran = STOP + lapor):
1. Pra-registrasi sebelum run model apa pun (disiplin yang sama
   seperti L3: M1/M2/M3 + split + ambang dikunci dulu).
2. Metrik per-jenis dipertahankan (Brier diskret, MSE/MAE
   kontinu); DILARANG mencampur atau memindai ulang ambang M3.
3. Pagar T-5 tetap: lift besar bukan presumi lolos.
4. Skrutini khusus: LB_bin 25/25 sempurna WAJIB memuat uji
   leakage ulang di spec (bukan diskualifikasi -- split waktu
   sah -- tapi skor sempurna menuntut pemeriksaan, bukan
   perayaan).
5. Tanpa model yang lolos gate pra-registrasinya sendiri, TIDAK
   ADA paper-trade.

## V-2. Register beku pemodelan

68 LOLOS per S7 audit DISAHKAN sebagai register (LB_bin 25,
LC1 7, LC2 13, LD 11, LB_rng 12). 35 GUGUR DITUTUP: tanpa
pemodelan atasnya tanpa persetujuan arsitek baru. 68 LOLOS
bukan 68 tiket trade.

## V-3. Disposisi R1-R4 + I1-I4

R1-R4 DITERAPKAN di ronde berikut (T-6 encoding log; redaksi
verbatim + pengecualian display; hash ganda pra+pasca
normalisasi; kolom `cocok` jujur). I1-I4 catatan mengikat
(tanpa CI; tanpa re-eksekusi run 9; konjungsi mengikat; `arah`
kembaran beda by-design).

## V-4. Pagar T-5 + S8A

T-5 ditegaskan kembali (2 London-GUGUR sebagai bukti pagar
bekerja). Ronde investigasi tambahan DILARANG atas inisiatif AI.

**Ronde L3 DITUTUP dengan vonis ini.** Ronde berikut (spec
pemodelan) HANYA atas persetujuan eksplisit user (diminta di
V-1). STOP setelah serah-terima.
