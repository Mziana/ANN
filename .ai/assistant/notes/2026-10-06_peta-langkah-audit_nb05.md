# Peta Eksplisit Langkah Audit nb05 → Sumber — 2026-10-06

Penegasan: angka "10" dan urutannya adalah scaffolding asisten. Isi tiap
langkah berakar pada salah satu dari 4 sumber di bawah. Rancangan
(`eda_design_v3.1.md`) TIDAK memuat daftar "10 langkah audit".

## Legenda sumber
- [KLAIM] = klaim/laporan coder Freebuff (wajib diverifikasi per AGENTS §20)
- [ATURAN] = kewajiban dari AGENTS.md / RULES.md (berlaku umum)
- [RANCANGAN] = bagian eksplisit `eda_design_v3.1.md`
- [INSIDEN] = kejadian nyata dalam sejarah proyek

## Peta

| # | Langkah | Sumber | Status |
|---|---------|--------|--------|
| 1 | Replica fidelity (4 angka vs nb03/nb04) | [KLAIM] replica C1 | LULUS (re-audit `2db14c9e…`) |
| 2 | Insiden salah-baca ACF (resolusi dua metrik) | [INSIDEN] −0,022624 dibaca sebagai ACF besaran | Batch A (jalan) |
| 3 | Look-ahead / leakage (regime, bootstrap, hari-broker) | [ATURAN] AGENTS §19 (look-ahead bias, data leakage = dosa besar) | Batch A (jalan) |
| 4 | H1–H5 {klaim·metrik·uji·ambang} | [KLAIM] C2 + [RANCANGAN] §11 Kriteria Sukses (hipotesis falsifiable) | Batch B |
| 5 | report.md angka-per-angka | [KLAIM] C3 + [ATURAN] AGENTS §5 (tabel Klaim & Bukti) | Batch B |
| 6 | 8 item BELUM DIVERIFIKASI | [KLAIM] laporan coder C3 (coder sendiri menulisnya) + [ATURAN] §20 | Batch B |
| 7 | Registry FIG-01..07 + FIG-01..03 tak tersentuh | [KLAIM] C4 | Batch C |
| 8 | Temuan jujur (ranking sesi, proksi spread, Q6 negatif) | [KLAIM] laporan coder (bagian temuan jujur) | Batch C |
| 9 | 4 bug riwayat (bucket pembuka, fractal_mask, KeyError, ruff) + bug ke-5 pemetaan hari (rerun-1) | [KLAIM] laporan coder (riwayat iterasi) | Batch C |
| 10 | Konvensi RULES.md + §19 + Reuse-First §16 | [ATURAN] penuh | Batch C |

## Catatan
- Langkah 9 bertambah 1 item vs prompt awal: bug pemetaan hari dari rerun-1
  perbaikan Langkah 1 (laporan coder 2026-10-06). Basis: [KLAIM] riwayat coder.
- Peta ini WAJIB dilampirkan/diacu di prompt Batch B dan Batch C agar auditor
  tahu dasar tiap langkah.
