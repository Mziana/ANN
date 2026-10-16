# BRIEF CODER EDA-08 — ammo_round_R (FINAL, eksekusi 2026-10-15)

Blueprint kanonik (TERKUNCI, dibaca penuh dulu):
`thoughts/shared/plans/2026-10-15-eda08-ammo-R-draf.md` (§§1–15, status FINAL).

## Konteks kerja

- Worktree: `D:/eda-08-ammo-R`, branch `feature/eda-08-ammo-R` (satu-satunya cabang fitur).
- Venv kanonik: `venv/Scripts/python.exe`. DILARANG `.venv/`.
- KOREKSI pasca-STOP pra-FASE 0 (venv tak ada di worktree): pakai interpreter
  kanonik via path absolut `D:\ANN\venv\Scripts\python.exe` untuk SEMUA run.
  DILARANG `pip install` / ubah environment (dependensi kurang = STOP + lapor).
  Output tetap ditulis di worktree ini, bukan di `D:/ANN`.
- Target: `scripts/_build_eda08_ammo_R.py` + `notebooks/scalping/eda_08_ammo_R_explore.ipynb`.
- Paradigma EDA-06/07: notebook = artefak generator (string template), exit 0,
  deterministik, assertion mesin. Batas §15.1 generator berlaku.

## F0-DIPERLUAS (parquet EDA-07 hilang — recovery sah, bukan rescan)

`data/processed/events/eda07_spike_events.parquet` gitignored, tidak ikut merge
c354d3b, hilang bersama worktree lama. Recovery: regenerasi via generator BEKU
`scripts/_build_eda07_spike_anatomy.py` (seed 20261006/20261007, deterministik).
Verifikasi bit-identik vs vonis EDA-07: Nunik=1632, band 515/415/240/462,
exh 395/1119, full-room 1514 (460/391/231/432). COCOK = reuse sah, LANJUT.
GAGAL cocok = STOP + lapor (DILARANG improvisasi / rescan manual).

## Pre-flight F0–F4 + A-checks (blueprint §6)

Jalankan berurutan, STOP + lapor pada gagal pertama. F1: tick_volume M15
≥95% pada bar-s event (bar-s = bar analisis §3); gagal → volume "tertunda",
EDA-09 ditulis ulang di sekitar shortlist-uji (kontinjensi §6).

## Aturan mengikat (blueprint §§3–5,7,9)

- REUSE parquet (hasil F0), RESCAN = STOP. Whitelist-assert: hari yang diload
  ⊆ manifest 384 hari-R warisan EDA-07 (monkey-patch I/O DILARANG).
- V/P: BUKAN hanya "tak dibaca" — mustahil dibaca (whitelist di atas). Gagal = STOP.
- Famili FDR-BH q=0,10 TERTUTUP tepat 4 uji: wick-pooled (1) + gap-split (2:
  first-split SEMUA event; gap-split NON-FIRST saja, cut 32=2×cooldown) +
  dow-omnibus (1). Tambah uji = STOP + amandemen.
- Null SEMUA uji = permutasi terstratifikasi B=10000, STRATA=BAND
  (wick: nilai-dalam-band, tercil dihitung ulang; gap: label grup dalam band;
  dow: label-dow dalam band). Donor-path DILARANG di ronde ini.
- Seed BARU independen format YYYYMMDD-eksekusi, dicatat di notebook.
- Year-gate (§4 tabel-in-prosa): wick = tanda pooled-Δ-per-tahun sama;
  first/gap-split = tanda selisih-rate sama; dow = hari-max-dev sama + tanda
  sama; sel n<30 per tahun → gate tak dapat lolos.
- Shortlist EDA-09: FDR-pass + gate-tahun + |Δ|≥5pp (Opsi B: gate di bawah daya
  uji, V sebagai algojo). Joint table = ESTIMASI, bukan kandidat.
  Dow-entry = existence-only (lokalisasi hari = ronde baru).
  Shortlist BOLEH KOSONG (sukses-dengan-nol, alasan tertulis per kandidat).
- Volume: kunci SATU dari (a)/(b)/(c) §3 + laporkan SEMUA yang dicoba.
  Warmup: 20 hari pertama R di-drop dari evaluasi-volume (count dilaporkan).
- L2 resurrection DILARANG (tak ada simulasi trade; fade tetap GUGUR).
- Tiap kandidat wajib tag live-computability §9 (tanpa tag = tak masuk shortlist).
- Tiap angka klaim bertag generasi/konfirmasi (§8).

## Selesai = Done §8

Semua deliverable ada + F0–F4 hijau + shortlist eksplisit + label generasi.
Lapor kembali: tabel Klaim & Bukti (TERVERIFIKASI/BELUM/ASUMSI/GAGAL),
yang belum diverifikasi, potensi masalah. Commit di branch worktree
DIPERBOLEHKAN setelah self-review (§4 template, ruff bersih); DILARANG
push/merge (perlu otorisasi terpisah).
