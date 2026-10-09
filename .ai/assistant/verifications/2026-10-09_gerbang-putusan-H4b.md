# Gerbang putusan — putusan arsitek H4b-stabilitas (vonis resmi)

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/arsitek/putusan-H4b-stabilitas.md`
**Status gerbang: LOLOS → H4b TERTUTUP**

## Fakta disk (cek saya sendiri)

| Item | Fakta | Status |
|---|---|---|
| blob `fe11383b9bdd1e58819e32812eec75c52ab3aee9` | `git hash-object` cocok klaim kanal | COCOK |
| 5326 byte / 119 baris (< pagu 150) / CR 0 / tail LF | `Get-Item` + `Get-Content` + baca byte | COCOK |
| ASCII murni (non-ASCII 0) | hitung byte >127 | COCOK |
| TANPA self-hash (0× `fe11383b` di isi) | `Select-String` Count 0 | COCOK (pengikatan eksternal) |
| S0 8/8: spec-H4b `0437b563…` / hasil-H4b `6410b180…` / reaudit-H4b `e3530477…` / spec-B2 `4a46b815…` / hasil-B2 `f06a8e27…` / reaudit-B2 `8a4d2109…` / putusan-B2 `e02a203b…` / HEAD `e0b2b9f9…` | cocok rujukan | COCOK |
| HEAD `e0b2b9f9…` tak bergeser, branch `codex/ANN`; staged tepat 2 T6 blob tak berubah | `rev-parse` + `diff --cached` + `ls-files -s` | COCOK |
| Tanpa commit (file putusan + brief = untracked di `--others`, tak masuk index) | `ls-files --others` | COCOK |
| Vonis tepat satu: `## V-1…GUGUR (DIPUTUS)` `:65` + `> **Vonis resmi H4b: GUGUR.**` `:71` (sama, bukan dua vonis) | grep | COCOK |
| V-2 ESK-1 BEKUKAN+CATAT (tolak revisi berpasal pra-registrasi+P-5); V-3 LOW-1/LOW-2 tetap LOW; V-4 H4/H1/H2/H3/H5 untouched, H6+ DITOLAK, P-5 mengikat | baca `:77-100` | DIPUTUS semua, tak digantung |
| S-V(a)–(d) dikerjakan: (a) lock+sha `1bbaf427…`, sabotase menggigit; (b) JSON langsung digit-per-digit + blob `7975db73`/`138d9025`; (c) tidak run-ulang berasional, S27 tak terpicu; (d) Off 2894 bar 2023 provare | baca `:40-61` | LENGKAP |
| Self-audit 3x + STOP `:119` (H4b TERTUTUP) | baca `:104-119` | LENGKAP |

## Keputusan: LOLOS → H4b TERTUTUP. Vonis resmi H4b: GUGUR. H4 TAHAN Batch-2 berdiri; yang gugur stabilitasnya.
