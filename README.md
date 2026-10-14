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

- **Milestone 1 (Data) + 2 (EDA) selesai.** Data 4 tahun (1.347.847 bar M1),
  resample sampai D1, fitur + label selesai dan ter-audit.
- **Milestone 3 (Metode) berjalan, terblokir** di persetujuan user.
- EDA-07 L3-1 selesai + re-audit + vonis arsitek: register 68 pola LOLOS /
  35 GUGUR. Ronde L3 ditutup.
- Vonis B-4 = **GO**: lanjut ke *spec pemodelan pra-registrasi* — **belum**
  paper-trade, **belum** live, dan belum ada satu pun run backtest.
- Metode dipusatkan pada dokumen desain event-first
  (`.ai/backup/2026-10-09_DESAIN_FRESH_SCALPING_EVENT_FIRST.md`): tiga
  keluarga event E1/E2/E3, 7 gerbang G1–G7, jalur P0→P1→P2.
- Draf `spesifikasi-fingerprint.md` **dipensiunkan** (arsip, jangan dijalankan).

**Yang menunggu user:** 4 keputusan §18 dokumen desain, dan damakan spread di
`configs/data.yaml` (terukur ~0,65 pip vs config 1,5 pip).

## Cara membaca status tanpa tersesat

| Mau tahu | Buka |
|---|---|
| Posisi proyek SEKARANG | `.ai/STATE.md` bagian atas |
| Yang harus dikerjakan berikutnya | `.ai/STATE.md` → "Langkah Berikutnya" (paling bawah) |
| Peta pekerjaan | `.ai/TASKS.md` |
| Kemajuan per tahap | `.ai/PROGRESS.md` |
| Kronologi +vonis tiap ronde | `reports/governance/<tanggal>/` |
