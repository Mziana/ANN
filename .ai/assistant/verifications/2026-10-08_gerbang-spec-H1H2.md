# Gerbang Pra-Audit — spesifikasi-lapisan3-H1H2 (2026-10-08)

## Klaim serah terima vs hasil ukur

| # | Klaim arsitek | Hasil ukur saya | Status |
|---|---|---|---|
| 1 | Hash spec `fc29f6fa…` | `git hash-object` → `fc29f6fa3595a89b918627dbdc71cfff82d8ebed` persis | COCOK |
| 2 | HEAD `e0b2b9f…` tak berubah | `git rev-parse HEAD` → `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` persis | COCOK |
| 3 | Status: dirt pra-ada + spec ??, staged 0, nol sentuh produksi/lindung | Kolom staged kosong di semua baris; `src/ tests/ data/ configs/` hanya entri pra-ada (`?? build_labels.py`, `?? test_build_labels.py` — D1/D2 pra-ada); spec di dalam `?? …/arsitek/` (dir untracked pra-ada) | COCOK |
| 4a | Q1 diputus: real-time jalan, M1 bukan vonis | Q1 ada (`:41-74`): real-time satu-satunya sumber vonis + aturan divergensi + anti-penyelamatan dua arah | ADA |
| 4b | Q2 diputus: ratifikasi + pin, teks final kata-per-kata | Q2 ada (`:76-134`): RATIFIKASI + teks final (a)–(f) + alasan satu paragraf | ADA |
| + | Cek asing OK (klaim) | python: 24143 byte / 369 baris / 0 non-ASCII / tanpa CR | COCOK (independen) |
| + | Blob S0: lock `97202803…`, putusan `e8eb03da…`, protokol `bc17e5de…` | `git hash-object` ketiganya → cocok penuh 40-hex | COCOK |

## Struktur spec (baca penuh 369 baris)

S0 tabel Klaim&Bukti → Q1 → Q2 → Uji S-H1 (S1 gate reproduksi [O8] exact-match → S2 verdict → S3 suplemen/divergence) → Uji S-H2 (S0 provenans → S1 EV → S2 VR) → S-C C1–C9 (C2 pola P-3 tracked-only + before/after; pola KOSONG dipensiunkan eksplisit) → S-B 12 larangan → S-R boleh/dilarang → self-audit 1× + adversarial.

## Catatan

- Arsitek undergraduate jujur soal 2 karakter asing pra-verifikasi (diperbaiki sebelum serah) — kredibilitas naik, pola sama seperti auditor H3.
- S-H1 S1 mensyaratkan reproduksi [O8] presisi penuh (n 330/324, median, CI95, chi2/p) — mismatch = GAGAL-eksekusi, STOP. Ini gate terkuat spec.
- Q2(b): konfirmasi H2 = day_label D4 beku T-1, dekopling dari S-H1 (larangan 10) — kopling hasil dilarang dua arah.
- Keputusan: LOLOS → susun prompt eksekusi coder Batch-1.
