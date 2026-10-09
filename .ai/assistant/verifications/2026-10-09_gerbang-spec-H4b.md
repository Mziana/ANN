# Gerbang pra-audit — spec pra-registrasi H4b-stabilitas

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/arsitek/spesifikasi-H4b-stabilitas.md`
**Status gerbang: LOLOS** (siap ronde coder atas perintah user)

## Fakta disk (cek saya sendiri)

| Item | Fakta | Status |
|---|---|---|
| 108 baris / 4600 byte / LF-only / ASCII murni | python: CR=0, nonASCII=0 | COCOK |
| blob `0437b563c85e578567eb58b8cfe6b0dd3ef02b47` | dihitung dari disk, cocok yang dilaporkan | COCOK |
| pola pengikatan eksternal (tanpa self-hash di dalam) | konsisten P-4/T2 | COCOK |
| HEAD `e0b2b9f9…` tetap; staged tetap 2 T6; nol commit | `diff --cached` = hanya 2 file T6 | COCOK |
| Struktur: lock H4b verbatim + input beku + prosedur dua-arah anti-intip + gate/deliverable coder + aturan baca tertutup + STOP `:108` | grep struktural | LENGKAP |
| Guard scope: GUGUR(H4b) ≠ runtuhnya TAHAN(H4); TAHAN(H4b) ≠ klaim kebal | `:32-34,99-101` | COCOK (P-5 dua arah dihormati) |

## Penilaian scope (asisten, bukan vonis)

- H4b = tindak lanjut R-2 yang diizinkan protokol fondasi-B (stratifikasi
  tahun pra-registrasi, BUKAN filter regime). Bukan H6 baru; tidak
  melanggar "H6+ DITOLAK". Vonis Batch-2 tak tersentuh oleh desain ini.

## Keputusan: LOLOS → menunggu perintah user "jalankan ronde coder H4b".
