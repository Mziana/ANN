# ANN — Riset Metode Scalping USDJPY

Riset kuantitatif untuk menemukan metode scalping USDJPY.
**Bukan bot trading** — belum ada strategi live maupun paper trade.

## Mulai dari sini (AI lain / manusia)

| Mau apa | Buka |
|---|---|
| Posisi proyek sekarang | `.ai/STATE.md` |
| Tugas + progres | `.ai/TASKS.md`, `.ai/PROGRESS.md` |
| Aturan kerja AI | `.ai/AGENTS.md`, `.ai/RULES.md` |
| Log sesi terakhir | `.ai/SESSION_LOG.md` (entri paling bawah) |
| Jurnal harian | `journal/daily/` (file tanggal terbaru) |
| Hasil EDA | `reports/eda/<tanggal>/` + `notebooks/scalping/` |
| Putusan arsitek | `reports/governance/<tanggal>/arsitek/` |

## Struktur

- `scripts/_build_eda*.py` — generator notebook EDA (deterministik, seed tetap)
- `notebooks/scalping/` — notebook EDA (sumber: generator di atas)
- `reports/eda/` — CSV + gambar + laporan coder per ronde
- `reports/backtest/` — KOSONG (belum ada satu pun run backtest)
- `reports/governance/` — prompt, verifikasi gerbang, putusan arsitek
- `configs/data.yaml` — spread terukur, biaya, sesi (otoritas angka)
- `journal/` — jurnal harian + decision/experiment log

## Data (tidak ikut push)

`data/raw/`, `data/processed/`, `data/features/`, `data/labels/`
di-ignore git. Untuk reproduksi: taruh feed M1 USDJPY 2023–2026
di `data/raw/`, lalu jalankan generator `scripts/_build_eda*.py`.

## Status singkat (2026-10-13)

- EDA-07 L3-1 selesai + reaudit + vonis arsitek: 68 pola LOLOS / 35 GUGUR.
- Simulasi biaya: biaya mendominasi (G4=False semua target LA).
- Berikutnya (menunggu izin user): spec pendalaman fingerprint +
  Spesifikasi Metode Target.
