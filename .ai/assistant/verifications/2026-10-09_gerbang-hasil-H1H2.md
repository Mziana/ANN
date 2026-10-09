# Gerbang Pra-Audit — coder/hasil-lapisan3-H1H2.md (2026-10-09)

## Klaim serah-terima vs hasil ukur saya

| # | Klaim coder | Hasil ukur saya | Status |
|---|---|---|---|
| 1 | Doc hash `1550209f40fde7998036c51c47a3f991b898f91c` (1175 baris) | `git hash-object` → identik 40-hex; baca file = 1175 baris | COCOK |
| 2 | Baris C8 `522c221c9d9f4ee3ad480282f13d0bf97a8942be` | Rekonstruksi git-style (`blob LEN\0` + body tanpa baris akhir) → identik | COCOK |
| 3 | HEAD `e0b2b9f…` tak berubah | `git rev-parse HEAD` → `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` persis; `git log --oneline -1` sama | COCOK |
| 4 | Porcelain 97 baris, staged 0, pra-ada | `git status --porcelain` saya = 97 baris, entri-per-entri identik dengan [O18]; `git diff --cached` kosong | COCOK |
| 5 | 59016 B, LF-only | python: 59016 byte / 1175 newline / tanpa CR | COCOK |
| 6 | Cek asing bersih | `check_foreign_chars.py` → OK rc=0 (601 byte non-ASCII = UTF-8 legal: em-dash dkk) | COCOK |
| 7 | Spec gate `fc29f6fa…` | `git hash-object` spec → `fc29f6fa3595a89b918627dbdc71cfff82d8ebed` persis | COCOK |
| 8 | D4/config/protokol beku | sha256 `47d15c41…` + `32eaf6b2…` dari disk identik; `configs/data.yaml` → `e277d67e…`; protokol → `bc17e5de…` | COCOK |

## Silang isi (baca penuh 1175 baris)

- S1 gate: 9/9 `true`, `gate_pass=true`; angka referensi [O8] di doc persis nilai spec (:166-170) yang saya kenal — n 330/324, median, CI95, chi2, p, verdict GUGUR.
- S-H1: CI95 `[-0.02668182694022586, +0.05242264543726398]` memuat 0 → kriteria (i) terpenuhi; chi2 `3.333835311042838`, p `0.18882820311496487` → (ii) tidak; burn-in 60 (2023-01-02..03-24), evaluable 914; divergence: searah M1 → tanpa eskalasi. Angka chat == angka [O6]/[O8] di doc.
- S-H2: EV median 2023/2024/2025 semuanya ≤ 0 (3/3 tahun) → kriteria EV terpenuhi; VR 1.0172/1.0236/1.0388, mean `1.0265420777270247` > 1 → VR tidak; 778 hari / 140 trade / exit sinyal 140. Angka chat == [O11]/[O12].
- [O1]–[O19] semua hadir; C1–C9 diklaim LULUS dengan pasangan bukti; self-audit 3 putaran tertulis; DEV-B1…B7 dilaporkan eksplisit (bukan disembunyikan).
- Manifest §3a = 45 baris parameter bersumber — protokol anti-salah-ketik prompt terpenuhi di permukaan.

## Anomali / titik fokus untuk re-audit (bukan vonis saya)

- **DEV-B1 (burn-in):** "60 hari riwayat" dibaca 60 posisi + median skipna (46 nilai non-NaN pada ambang pertama karena warmup ATR 14 hari). Bila maksud spec = 60 nilai non-NaN, batas evaluable bergeser +14 hari. Satu-satunya titik interpretasi yang bisa menggeser hasil → auditor WAJIB menilai, arsitek memutuskan perlu/tidaknya rerun.
- **DEV-B3 (exit 140/140 sinyal, 0 SL/TP/time-stop):** konsekuensi mekanis Q2(d)(iii) — exit dicek tiap bar sehingga SL/TP (≥1× ATR) praktis tak tersentuh. Spec-compliant, tapi auditor wajib smell-check: strategi ini secara efektif hold ~1 bar; pastikan bukan salah implementasi monitoring (mis. mulai bar entry vs bar berikut).
- **DEV-B2:** bucket akunting tambahan 369 hari (`close<=open`) — rekonsiliasi 778 = 0+369+269+140 benar per tahun (259/260/259). Wajar, bukan varian.
- C2: BEFORE ([O2], 42 baris lingkup) vs AFTER ([O16]) diklaim identik + `find -newermt` kosong — pola P-3 terpenuhi di permukaan; auditor memverifikasi ulang.

## Keputusan: LOLOS → susun prompt auditor re-audit sempit Batch-1.
