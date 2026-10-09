# Gerbang pra-audit — laporan coder H4b-stabilitas (ronde eksekusi)

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/coder/hasil-H4b-stabilitas.md`
**Status gerbang: LOLOS** (terus ke ronde auditor independen)

## Fakta disk (cek saya sendiri)

| Item | Fakta | Status |
|---|---|---|
| 14015 byte / 259 baris / LF-only / ASCII murni | python: CR=0, nonASCII=0 | COCOK |
| blob `6410b1800f6dc46ec511949e1311fcda853b0807` | dihitung dari disk, cocok yang dilaporkan | COCOK |
| Branch `codex/ANN` (pindah workspace terkonfirmasi); HEAD `e0b2b9f9…` tak berubah; staged tetap 2 T6; nol commit | branch + rev-parse + diff-cached | COCOK, tanpa divergensi |
| Struktur: S0 + SHA + mesin/anti-intip + output 2 arah + top-6 + karantina + aturan baca + R-4 + ringkasan + self-audit 3× + STOP `:256` + footer `:258` | grep struktural | LENGKAP |
| R-4: maju `7975db73…`, mundur `138d9025…` | `git hash-object` ULANG saya atas `%TEMP%\h4b` → cocok 2/2 | TERVERIFIKASI independen |
| Tepat satu vonis: GUGUR(H4b) (vonis + footer); TAHAN(H4b) 0×; "H6" hanya sitir larangan | grep | COCOK |
| Aritmetika exit-cause: 71+6+1477=1554; 94+12+1454=1560 | hitung ulang | COCOK |
| Median Maju −0,005049999999992838 = median 2025 Batch-2 persis (klaim cross-validasi) | cocok digit-per-digit vs hasil beku | KONSISTEN |

## Catatan (bukan temuan)

- Pindah branch ke `codex/ANN` tidak diperintah brief, tapi tanpa
  divergensi (HEAD sama) + nol commit → netral, dicatat saja. Gerbang
  saya berikutnya berjalan di branch ini.
- Atribusi staged=2: milik T6 asisten-atas-perintah-user (BUKAN pihak
  tak dikenal); coder benar tak menyentuh. Koreksi kedua kali dicatat.

## Porcelain

- 117 (+3 = file laporan + brief H4b + gerbang spec-H4b). Pola pra-ada
  selebihnya tidak berubah.

## Keputusan: LOLOS → bahan auditor independen (replikasi dari nol).
