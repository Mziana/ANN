# Spec Pendalaman Fingerprint Naik-vs-Turun (Arsitek, 2026-10-13)

Status: DRAF, menunggu persetujuan user sebelum dikerjakan.
Prinsip: tulis dulu baru lihat (anti-obok-obok), biaya dihitung,
satu putaran satu vonis (S8A).

## F-0. Scope terkunci

- Pasangan: 31 LOLOS berarah (LC1 7 + LC2 13 + LD 11). LB_bin
  (tanpa arah) dan LB_rng (kontinu) DIKECUALIKAN dari bagian arah;
  LB_bin dipakai hanya untuk satu sidik "sebelum gerakan besar".
- Fitur: 29 kolom kausal run 9, VERBATIM, tanpa tambah/kurang.
  Himpunan fitur beku = tidak ada cherry-picking.
- Label/irisan/split: warisan L3-1 (train 2023H2-2024H2, test
  2025H1+H2, 2026 terkunci). Biaya: spread stres sesi (COST_STRESS).

## F-1. Sidik "sebelum" (kondisi sebelum kejadian)

Untuk tiap pasangan, untuk tiap dari 29 fitur (metode sama
semua, tanpa pilih-pilih):
1. Bagi nilai fitur jadi 10 keranjang (desil) di data train.
2. Hitung peluang "naik" di tiap keranjang vs peluang dasar,
   dengan rentang keyakinan klaster-hari (preseden run 9).
3. Sidik = 3 keranjang pembeda terbesar (naik-vs-turun) yang
   arahnya SAMA di 2025H1 dan 2025H2.

## F-2. Sidik "sesudah" (jalur harga setelah kejadian)

Untuk tiap pasangan, pra-registrasi 3 statistik jalur:
1. Lanjutan vs balik: tanda gerakan N-menit BERIKUTNYA (sama
   dengan label atau berbalik).
2. Gerak maksimum searah vs berlawanan dalam N menit (pip).
3. Bersih-biaya: (gerak searah - spread stres sesi) > 0?

## F-3. Aturan vonis (biner, dikunci sebelum run)

- Kandidat aturan trade = pasangan yang punya (a) sidik-sebelum
  stabil dua semester + (b) lanjutan dominan + (c) bersih-biaya
  positif di KEDUA semester test.
- GO iff >= 3 pasangan menghasilkan kandidat aturan trade.
  Jika tidak: NO-GO (pendalaman berhenti, pendekatan tidak naik
  ke aturan trade).
- Ambang 3 adalah judgment arsitek, terbuka untuk veto user
  sebelum run (tulis penggantinya di persetujuan).

## F-4. Larangan

- Tanpa menambah fitur/label/irisan; tanpa mengintip test
  sebelum kunci F-1/F-2; tanpa klaim P&L (bersih-biaya adalah
  filter, bukan bukti profit); tanpa ronde lanjutan atas
  inisiatif AI.

## F-5. Keluaran

CSV sidik per pasangan + FIG + laporan coder + reaudit + vonis
GO/NO-GO. STOP setelah serah-terima.
