# AMANDEMEN-1 atas BLUEPRINT EDA-06 v9.3

> Diterbitkan: 2026-10-15 (arsitek). Status: A1+A2+A3 DIRATIFIKASI;
> A4 DIPUTUS (modifikasi user: FS-01→V, P SEGEL pristine). BERLAKU —
> lampu hijau LANGKAH 2 diberikan. Dasar: Pre-Flight coder F1–F3
> (ketiganya BENAR, terverifikasi).
> Blueprint induk: `2026-10-15-eda06-blueprint-v93.md` (tetap FINAL, dibaca
> bersama dokumen ini; yang bertentangan = dokumen ini menang).

## A1. Jam open [21,22] → [22,23] (ratifikasi: YA)

Bukti ganda yang saling mengunci:
(i) Audit DST 2026-10-05 (`configs/data.yaml:271-281` + STATE) — open normal
01:00 server = 22:00 UTC summer (+3) / 23:00 UTC winter (+2); 21:00 UTC justru
tanda-tangan anomali. (ii) Ukuran independen coder: 255 hari @22, 129 hari @23,
0 hari @21. Blueprint [21,22] salah melawan data repo sendiri.

Penggantian exact (6 titik): tabel kontrak (`Daily open hours | [22, 23]`),
Cek 1 (`jam bar pertama (22/23 UTC)`), Cek 5 grep
(`0.95, 2.85, 16, 30, [22, 23], 20261006, 20261007, 5, 1000`),
Sel 2 assertion (`first-bar hour ∉ [22,23]`), BAGIAN 3 daftar jangan-ubah
(`[22, 23]`), consistency check (`DAILY_OPEN_HOURS==[22,23]`).
Cek 3: ekspektasi hari bersih ≈ 384 (drop open-abnormal ≈ 0); assertion
toleransi 5% dipertahankan.

## A2. Nesting Sel + split momentum rezim (ratifikasi: YA, bentuk modifikasi user)

- **A2a — Nesting (tutup lubang F3).** Sel 1 = basis: spike + exhaustion +
  waktu(32) + pre-filter biaya + konfirmasi + post-filter cost + side-check,
  TANPA filter rezim. Sel 2 = Sel 1 + makro-sideways. Sel 3 = Sel 2 + mikro.
  Berlaku: Sel 3 ⊂ Sel 2 ⊂ Sel 1. Cabang reversal saja; momentum di A2d.
- **A2b — Satu predikat rezim, nol angka baru (ganti ambang mati 1,5× yang
  lolos hanya 22/179).** `SIDEWAYS_D1 := d1_range_5 < P25(d1_range_5/atr_d1
  atas trigger)` — dihitung di dry-run, angkanya dilaporkan.
  `TRENDING_D1 := NOT SIDEWAYS_D1`, dilabeli jujur "non-sideways
  (trending/ekspansi)" — komplemen, BUKAN definisi tren independen.
- **A2c — Mikro persentil (ganti 0,5/0,25 yang mustahil; min terukur
  1,37/0,59).** `box_range_12 < P50(box/ATR atas trigger lolos makro) DAN
  dist < P50(dist/ATR yang sama)` — dry-run, dilaporkan.
- **A2d — Split momentum seragam.** Berlaku ke SEMUA sel momentum dengan
  predikat yang sama: 4a1t/4a1s, 4a2t/4a2s, 4b1t/4b1s, 4b2t/4b2s
  (t = trending-day, s = sideways-day). FDR core: **{1, 2, 3, 4a1t, 4a1s}**
  (5 tes, q=0,10); 4a1 pooled DIHAPUS dari core (diganti split — hindari
  double-count data sama dalam satu famili). Sensitivitas:
  {4a2t, 4a2s, 4b1t, 4b1s, 4b2t, 4b2s}, p nominal, tanpa advance.
  Uji yang dijawab: apakah momentum hanya bekerja di trending (4a1t LOLOS +
  4a1s gagal = bukti; keduanya sama = insight lain).
- **A2e — Null regime-matched (klarifikasi, nol angka baru).** Null tiap sel =
  mean placebo track yang sesuai, dihitung di atas trigger placebo (shared)
  yang memenuhi predikat rezim sel tersebut. Berlaku reversal dan momentum.
- **Ekspektasi jujur.** Basis momentum pasca-fix [22,23] belum diketahui
  (dulu 0/0/0/0 di bawah jam yang salah). Jika basis < 30 → split MOOT ronde
  ini: drop, catat, BUKAN vonis. Drop rule < 30 per sel berlaku semua sel baru.
- **Revisi gate Cek 4 (wajib oleh A3).** STOP UNDERPOWERED hanya jika
  **Sel 1 (basis) < 30**. Sel 2/Sel 3 < 30 → drop + label, LANJUT Sel 1.
  Funnel Cek 4 ditambah tahap split rezim momentum.

## A3. Aturan kejujuran + hipotesis cadangan (ratifikasi: YA, framing user)

- Sel 3 < 30 → label **"TIDAK TAHU"**: hipotesis AMD-full (sideways +
  akumulasi + exhaustion) BELUM TERUJI. Bukan kegagalan, bukan vonis.
- Sel 1 LOLOS (null-beat + FDR-pass) → **"edge lemah terdeteksi"** → advance
  TV-01 dengan HIPOTESIS DIREVISI: "reversal pasca-spike umum".
  AMD-full tetap UNTESTED di semua laporan, STATE, dan CONTEXT.
- Semua core gagal (termasuk Sel 1) → GUGUR (kill rule tegak).
- Advance rule "≥1 core LOLOS → TV-01" tetap; yang dibawa = klaim longgar.

## A4. Venue TV-01/FS-01 (DIPUTUS user: modifikasi — P PRISTINE, SEGEL)

TV-01 = konfirmasi walk-forward di **V (2025, 259 hari, expanding/rolling)**;
FS-01 = konfirmasi terkunci di **V** — BUKAN P, BUKAN R (R = in-sample
discovery). ANN-01 tetap (train R, validasi V, test P).
Alasan (user, benar secara metodologis): P adalah ujian final satu-kali;
FS-01 di P akan "melihat" P sebelum test ANN-01 dan menghancurkan nilai
pristine-nya. Hierarki sentuh: R = discovery (sekali, terkunci);
V = workhorse validasi (boleh dipakai TV-01 + FS-01 + validasi ANN-01 —
V bukan ujian final); **P = PRISTINE — disentuh tepat sekali, hanya untuk
test final ANN-01. SEGEL sampai saat itu.**
Anggaran: R 384 (terkunci); V 259; P 182 (segel). H1-2023 stratum B =
stress saja. Overlap R dengan bed discovery-R1 lama = moot (R1 BATAL);
validasi tidak pernah di R.

## Penutup

Tidak ada Amandemen-2 untuk blueprint EDA-06. A4 diputus + lampu hijau
LANGKAH 2 diberikan 2026-10-15; coder jalan dengan blueprint v9.3 +
Amandemen-1 ini; masalah berikut = masalah kode. Biaya repo (0,95) yang
belum selaras tetap PENDING di luar amandemen ini.
