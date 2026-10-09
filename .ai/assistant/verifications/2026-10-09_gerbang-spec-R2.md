# Gerbang spec -- arsitek/spesifikasi-R2-stratifikasi.md (2026-10-09)

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/arsitek/spesifikasi-R2-stratifikasi.md`
**Status gerbang: LOLOS -> ronde coder R-2**

## Fakta disk (cek saya sendiri)

| # | Klaim / syarat | Hasil ukur saya | Status |
|---|---|---|---|
| 1 | Doc hash `c04199cea2acfd692b731fcb7eacec16b0e4691d`, 141 baris | `git hash-object` -> identik 40-hex; python: 6849 byte / 141 newline / 0 non-ASCII / CR 0 / tail LF True | COCOK |
| 2 | TANPA self-hash (pengikatan eksternal) | `0x c04199ce` di isi | COCOK |
| 3 | Pagu <150 baris, ASCII murni, LF-only | 141 baris / nonASCII 0 / CRLF 0 | COCOK |
| 4 | S0 8/8 + HEAD + staged 2 T6 | `4a46b815...` spec-B2 / `f06a8e27...` hasil-B2 / `8a4d2109...` reaudit-B2 / `e02a203b...` putusan-B2 / `ed436fdd...` protokol-B / `0284f5f0...` hasil-B / `7d125022...` disposisi-B / `fe11383b...` putusan-H4b -- 8/8 cocok penuh 40-hex; `rev-parse HEAD` = `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` persis; `diff --cached --name-only` tepat 2 T6 (`src/features/build_labels.py` + `tests/test_build_labels.py`) | COCOK |
| 5 | S-V(a)-(d) lengkap | (a) 4 bahan S2 dibaca UTUH + celah :121-157; (b) angka sesi ini digit-per-digit (INKLUSI `0.014399999999998407`/3114, 2024 `0.04834999999999022`/1560, 2025 `-0.005049999999992838`/1554, n_Off 0/0, top6 pool, H4b Maju/Mundur, trio-sha `b1b69d33`/`7a7f5ee7`, porsi biaya `0.014621990418018331`, 6/6 sha parquet); (c) tidak run-ulang beralasan, S27 tak terpicu, nol klaim baru; (d) NOL probe baru, ESK-1 dikutip | LENGKAP |
| 6 | Lock R-2 verbatim OR-gugur + anti-intip | GUGUR bila SATU PUN tahun-uji (2024, 2025) median EV-after-cost <= 0; TAHAN hanya bila KEDUA tahun > 0; tanpa TAK-MENENTUKAN; kriteria (a) n_Off DIBEKUKAN non-penentu; 2023 seed-saja; 2026 dikecualikan PENUH; jam lock `[14,13,0,15,12,7]`; top-6 per tahun + shopping-jendela DILARANG | DIPUTUS, mengikat |
| 7 | Mesin C1-C9 + harness + larangan S-B | C1-C9 ringkas mengikat; harness HANYA `%TEMP%\opencode\r2\` (`r2.py` -> `r2_hasil.json` + log); venv kanonik `D:\ANN\venv\Scripts\python.exe` py3.12.8; DILARANG tulis `src/`/`configs/`/`data/`; B1-B12 eksplisit; laporan `coder/hasil-R2-stratifikasi.md` tanpa vonis | COCOK |
| 8 | Tanpa vonis di spec; H5/H1/H2/H3 untouched; H6 nihil; STOP menutup | Baca penuh 141 baris: desain saja + aturan baca TERTUTUP + self-audit 3x + STOP akhir | COCOK |
| 9 | Tanpa commit/push/stash/checkout oleh sesi arsitek | HEAD tak bergeser; staged tetap 2 T6; file spec + brief = untracked di `ls-files --others`, tak masuk index | COCOK |

## Keputusan: LOLOS -> susun brief eksekusi coder (output `coder/hasil-R2-stratifikasi.md` + `r2_hasil.json`, 2x identik kata-per-kata blob `c04199ce`).
