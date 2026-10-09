# Gerbang hasil -- coder/hasil-R2-stratifikasi.md (2026-10-09)

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/coder/hasil-R2-stratifikasi.md`
**Status gerbang: LOLOS -> ronde re-audit R-2**

## Fakta disk (cek saya sendiri, bukan salinan klaim)

| # | Klaim kanal | Hasil ukur saya | Status |
|---|---|---|---|
| 1 | Laporan hash `c2f79913...`, 9811 B | `git hash-object` -> identik 40-hex; python: 9811 byte / 226 baris / 0 non-ASCII / CR 0 / tail LF True | COCOK |
| 2 | C8 pengikatan eksternal (TANPA self-hash) | `c2f79913` di isi = 0x; hash artefak `4664B4D8` di isi = 2x (wajib S-5, bukan self-hash) | COCOK |
| 3 | G0/G-S0/G-staged (HEAD `e0b2b9f9`, 9 hash, staged 2 T6) | `rev-parse` persis; 9 hash di laporan cocok brief+S0; `diff --cached` tepat 2 T6 (`build_labels.py` + `test_build_labels.py`) | COCOK |
| 4 | Laporan untracked, tak masuk index | `ls-files --others` memuat laporan; `ls-files -s` atas laporan kosong | COCOK |
| 5 | Artefak `4664B4D8...E64A4` | `Get-FileHash` atas `r2_hasil.json` + run1 + run2 -> ketiganya identik 64-hex dengan klaim kanal; harness berisi `r2.py` 14211 B + 3 JSON @1356769 B + 2 log @5126 B | COCOK |
| 6 | Isi JSON vs JSON-di-laporan vs S-V(b) spec | Python banding digit-per-digit: 2024 (1560, 0.04834999999999022, 87/9/1464, Off 0, F1 30) + 2025 (1554, -0.005049999999992838, 71/6/1477, Off 0, F1 0) + join (47721=47721, sekuens true/true, ATR exact 974 hari, pool 519) + lock (`GUGUR(R-2)`, tahun_gugur [2025]) + meta (py3.12.8, pandas 2.2.3, numpy 1.26.4, scipy 1.17.1, pyarrow 17.0.0, jam lock, biaya 0.61/0.69/0.62/0.80/0.65) -- tiga rekaman sepakat | COCOK semua |
| 7 | Tepat satu vonis mekanis; tanpa vonis H4/H5 | `verdict: GUGUR(R-2)` satu-satunya; H4/H5 eksplisit DILARANG + berlabel BELUM DIVERIFIKASI; self-audit 3x + STOP menutup | COCOK |
| 8 | Mutu (pytest 254 passed rc 0; ruff rc 0; foreign rc 0) | Output mentah ditempel di laporan (rc + cakupan + toolchain); eksekusi-ulang penuh = tugas auditor (replikasi dari nol per spec) | DITERIMA dgn catatan |

## Catatan (non-penentu, diteruskan ke re-audit)

- N.1: klaim mutu G8 (pytest/ruff/foreign) ber-output-mentah di laporan;
  asisten tidak run-ulang; auditor WAJIB replikasi + verifikasi independen.
- N.2: `r2_hasil.json` (induk) byte-identik dengan run1/run2 (satu artefak,
  tiga salinan) -- sah pola determinisme, bukan tiga artefak berbeda.

## Keputusan: LOLOS -> susun brief re-audit R-2 (replikasi nol + anti-intip +
## Off/lock + scope + karantina + determinisme + integritas, tanpa vonis).
