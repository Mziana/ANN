# Arsip Brief Coder EDA-07 (disalin dari worktree root saat merge 2026-10-15)

> Salinan `D:\eda-07-spike-anatomy\BRIEF_CODER_EDA07.md` (worktree sudah dihapus
> pasca-merge c354d3b). Disimpan sebagai jejak audit perintah eksekusi.

## 1. Referensi kode (baca sebelum nulis)

- `scripts/_build_eda06_candle.py` — `scan_spikes`, `first_exhaustion`,
  first-passage, null machine. Warisi verbatim.
- `configs/data.yaml` + `configs/broker.yaml` — otoritas angka (biaya 0,95 flat).
- `.ai/AGENTS.md` §15.1 — syarat file generator.

## 2. Deliverables

1. `scripts/_build_eda07_spike_anatomy.py`
2. `notebooks/scalping/eda_07_spike_anatomy_outcome.ipynb` (14± sel, exit 0)
3. Parquet event (`mag_cont`, `band`, `has_exhaustion`, `r_bar`,
   `first_of_day`, flag drop + alasan)
4. Tabel rate per band/stratum + tabel Q1-sub/Q3-sub
5. Laporan coder (Klaim & Bukti; spek null F6 + live-applicability +
   kurva magnitudo-vs-rate + CI)
6. Vonis tertulis per lapis + klausul scoping §6 blueprint

## 3. Pre-flight (urutan terkunci)

F1 (2116+270) → F0a (split + rekonsiliasi) → F0b (dedup) → F2 (contoh/status)
→ F4 (seed) → F6 (spek null 6-butir SEBELUM eksekusi). Gagal = STOP + lapor.
F3/F5 lapor-saja. A-checks: A1 `|rasio| ≤ 1+1e-6`, A2 taksonomi exhaustive.

## 4. Spesifikasi terkunci

Entry lapis-2 = close(s+1); SL = ekstrem + 0,5×`atr_s`; prefilter 2,85;
kill hanya @0,95 (stres 2× tanpa daya bunuh); R 384 hari M15; larangan
cross-day; B=10000; FDR q=0,10. GUGUR hanya matikan fade-standalone.

## 5. Larangan

Angka 856 sebagai fakta output; sentuh arsip/P; improvisasi (STOP + lapor);
Python selain venv worktree. JANGAN commit, JANGAN push.
