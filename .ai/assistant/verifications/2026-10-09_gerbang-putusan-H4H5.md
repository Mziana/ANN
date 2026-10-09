# Gerbang pra-audit — putusan arsitek H4/H5 (Batch-2 TERTUTUP)

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md`
**Status gerbang: LOLOS** (Batch-2 TERTUTUP)

## Fakta disk (cek saya sendiri)

| Item | Fakta | Status |
|---|---|---|
| 410 baris / 21171 byte / LF-only / ASCII murni | python: CR=0, nonASCII=0 | COCOK |
| full-blob `e02a203b96879d73e90339f2d78a37d15834a23a` | dihitung dari disk | TERCATAT (pola auditor: di luar dokumen) |
| C8 `5bfa76a2d4e7ca9c44b184d8dd23e06ff5e38b10` | body-minus-last-line sha1, reproduksi persis | COCOK |
| HEAD `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` | tetap | COCOK |
| staged 0, nol commit | `diff --cached` kosong | COCOK |
| porcelain 108 | pola pra-ada + doc ini + berkas sesi | TERJAWAB sah |

## Isi (grep struktural + sitiran kunci)

- **Vonis resmi H4: TAHAN.** (`:179`, satu kalimat dikutip)
- **Vonis resmi H5: GUGUR.** (`:206`, satu kalimat dikutip; telak)
- **S-V dikerjakan per huruf:** (a) titik penentu sh4/sh5 + grep
  `TAU_alt|normalize` nihil; (b) trio-sha + 6 sha parquet + ekstraksi JSON
  sesi arsitek; (c) TIDAK run-ulang dengan rasional per butir, S27 tidak
  terpicu (tiga rekaman sepakat penuh); (d) T1 terkonfirmasi dari data
  (jam 0/1 = 100% Tokyo).
- **P-1–P-5 tertutup semua:** EKS-1 diputus sadar (klaim coder "tidak ada
  eskalasi wajib" DITOLAK); EKS-2 compliant; EKS-3 peringatan stabilitas
  tanpa konsekuensi vonis; EKS-4 aman. T1 sitir-angka-saja tanpa edit beku;
  T2 S-B.10 tetap + batch berikut WAJIB pengikatan eksternal; T3–T6 catatan
  (+rekomendasi git add ke pemilik repo). P-5 kunci dua arah; H1/H2/H3
  tak tersentuh.
- **Self-audit 3x + STOP `:408` + C8 baris terakhir `:410`.** Nol butir gantung.

## Batas gerbang ini

- Angka vonis TIDAK dihitung-ulang di sini — tiga rekaman independen sepakat
  (coder, auditor, S-V arsitek); wewenang vonis = arsitek, sudah dipakai.
- Rekomendasi T6 (`git add` dua file untracked) = keputusan user, belum
  dieksekusi siapa pun.

## Keputusan: LOLOS → Batch-2 TERTUTUP. H1/H2/H3/H5 GUGUR resmi; H4 TAHAN resmi.
