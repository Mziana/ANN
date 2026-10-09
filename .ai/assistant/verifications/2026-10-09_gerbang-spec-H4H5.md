# Gerbang Pra-Audit — arsitek/spesifikasi-lapisan3-H4H5.md (2026-10-09)

## Klaim serah-terima vs hasil ukur saya

| # | Klaim arsitek | Hasil ukur saya | Status |
|---|---|---|---|
| 1 | Doc hash `4a46b815211e6b0b050cbb6f3e98ce5e27904069`, 461 baris | `git hash-object` → identik 40-hex; python: 29395 byte / 461 newline / 0 non-ASCII / tanpa CR | COCOK |
| 2 | HEAD `e0b2b9f…` tak berubah; staged 0; foreign-chars OK | `git rev-parse HEAD` persis; `git diff --cached` kosong; ASCII murni terukur | COCOK |
| 3 | Gerbang S-2d 6/6 cocok | Ukur ulang saya: `97202803…` / `e8eb03da…` / `15ecb37d…` / `ca4e0b70…` / `c643c1c9…` / `91d4c993…` — 6/6 cocok penuh 40-hex | COCOK |
| 4 | Struktur mirror Batch-1 | Baca penuh 461 baris: S0 + Q1–Q5 diputus + S-H4/S-H5 (Proposal S21 + metrik/ambang pra-reg) + S-C (C1–C9) + S-B (14 larangan) + S-R + self-audit 1x + adversarial | COCOK |
| 5 | Repo tak tersentuh | Porcelain 101 = pola pra-ada (M `.ai/*` saya; D `reports/eda/*` + governance lama; untracked `Audit/`/`arsitek/`/`coder/` + assistant; `requirements.txt` M pra-ada sejak `41b21d8`). Sesi ini nol sentuh produksi/lindung | TERJAWAB |
| 6 | Q1–Q5 + pin coder | Semua diputus eksplisit + alasan satu paragraf; pin join-posisional/fingerprint/utc.normalize/H1-H3-lockout/DAQ-2023-2026/deviasi-placebo tercatat di Q4/Q5/S-B/S-C | COCOK |

## Deviasi arsitek dari rekomendasi draf saya (hak arsitek, beralasan tertulis)

- Q1: pool TUNGGAL 2024–2025 penentu (tanpa uji per-tahun penentu, tanpa multiplicity antar-tahun); deskriptif per-tahun BOLEH non-penentu. 2023 = seed-kuartil SAJA; H4 DILARANG pakai 2023 untuk apa pun. **2026 dibuang PENUH bahkan deskriptif** (lebih ketat dari usulan saya; alasan anti-smuggling + preseden H2).
- Q2: grid TEPAT 4 sel + 1 agregat deskriptif; Holm α=0,01; **H4 OR-gugur TANPA koreksi** (rasional: dua syarat perlu yang arah-gugurnya sejalan → TAHAN lebih sulit, didokumentasikan bukan dari data).
- Q3: by_session SAJA (London 0.61/NY 0.69/Tokyo 0.62/Sydney 0.8, Off→default 0.65); by_year/stress-bands DILARANG.
- Q4: long-only 6 jam-tetap TANPA filter arah (filter H2 = cemaran); SL 1x/TP 2x, SL>TP, time-stop, TANPA signal-exit; overlap diizinkan; larangan tukar dua arah.
- Q5: placebo PERSIS nb04; kuartil expanding BLOK-TAHUNAN strict->; grain broker-day; `utc.normalize()` DILARANG.

## Keputusan: LOLOS → draf prompt eksekusi coder (output `coder/hasil-lapisan3-H4H5.md`, harness `%TEMP%\opencode\l3h4h5`).
