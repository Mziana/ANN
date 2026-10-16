# Brief Eksekusi EDA-08 ammo_round_R — Coder Eksternal (2026-10-15)

## Otoritas + PRASYARAT

Satu-satunya otoritas = blueprint FINAL
`thoughts/shared/plans/2026-10-15-eda08-ammo-R-draf.md` (§§1–15, status FINAL —
dibaca PENUH sebelum menyentuh apa pun; bila brief ini bertentangan dengan
blueprint, blueprint menang — laporkan konflik, jangan improvisasi).
Detail operasional: `BRIEF_CODER_EDA08.md` (root worktree).
**PRASYARAT: blueprint sudah FINAL + perintah eksekusi user sudah turun.**
Keduanya terpenuhi. Klaim tanpa output mentah = gagal.

## Workdir + disiplin peran (AGENTS.md §26)

- Workdir = worktree `D:/eda-08-ammo-R`, branch `feature/eda-08-ammo-R`
  (satu-satunya cabang fitur; DILARANG branch baru). BUKAN `D:/ANN`.
- Kamu CODER: implementasi + self-audit + fix. DILARANG memutuskan
  metode/kriteria/ambang (eskalasi lewat user bila ragu), DILARANG vonis
  (LOLOS/GUGUR/shortlist-final = arsitek), DILARANG audit independen atas
  pekerjaan sendiri di luar self-audit §4.
- Venv kanonik: `venv/Scripts/python.exe` di worktree. DILARANG `.venv/`.
- Builder→notebook: tulis `scripts/_build_eda08_ammo_R.py`, rerun,
  notebook `notebooks/scalping/eda_08_ammo_R_explore.ipynb` ter-regenerate.
  DILARANG edit notebook manual. DILARANG mulai dari 0 / rewrite artefak beku.
- DILARANG commit/push tanpa perintah eksplisit. DILARANG merge.

## FASE 0 — SELF-AUDIT KODE SEBELUM EKSEKUSI (gerbang blokir)

DILARANG menjalankan notebook/generator SEBELUM fase ini lulus tertulis.
Setelah builder ditulis, SEBELUM run pertama:

1. Self-review AGENTS.md §4 (10 butir: baca ulang, bug/edge/None,
   look-ahead, leakage, konvensi, hardcode, duplikasi, test, import;
   tandai keraguan `# REVIEW:`).
2. Self-audit 3×: Correctness (tiap angka klaim bersumber file:baris/output) ·
   Bias (label generasi/konfirmasi jujur?) · Meta (semua syarat blueprint
   terjawab? file luar scope tersentuh?).
3. Pasangan perintah mentah (tempel SEMUA output di laporan):
   `ruff check scripts/_build_eda08_ammo_R.py` (wajib rc=0, sebut rc) +
   `ruff format --check scripts/_build_eda08_ammo_R.py` (wajib rc=0) +
   `git status --porcelain` (klaim tanpa-stage di luar file kerja).
4. Larangan bentuk-spesifik: DILARANG guard yang membandingkan nilai dengan
   dirinya sendiri (termasuk via kolom turunan frame yang sama) · DILARANG
   merekonstruksi hari dari UTC (grain tunggal hari-broker) · DILARANG
   referensi dibaca dari objek yang sama diperiksa (parquet reuse dibaca
   ulang dari disk sebagai referensi terpisah) · DILARANG klaim
   "sudah diuji" di satu bagian sambil "belum ada test" di bagian lain.
5. Hasil FASE 0 ditulis sebagai section laporan tersendiri. Gagal = fix +
   ulangi FASE 0. Lolos = baru boleh FASE 1.

## FASE 1 — F0-DIPERLUAS (recovery parquet, bukan rescan)

`data/processed/events/eda07_spike_events.parquet` hilang (gitignored, tak
ikut merge). Regenerasi via generator BEKU
`scripts/_build_eda07_spike_anatomy.py` (seed 20261006/20261007 — JANGAN ubah),
lalu verifikasi bit-identik vs vonis EDA-07: Nunik=1632, band 515/415/240/462,
exh 395/1119, full-room 1514 (460/391/231/432). Tempel angka aktual vs ekspektasi
baris-per-baris. COCOK semua = reuse sah, LANJUT. Satu pun GAGAL = STOP + lapor
(DILARANG improvisasi / scan manual / "perbaikan" generator beku).

## FASE 2 — Pre-flight F0–F4 + A-checks (blueprint §6)

Berurutan, STOP + lapor pada gagal pertama (tempel output tiap cek).
F1: tick_volume M15 ada + terisi ≥95% pada bar-s event (bar-s = bar analisis
§3). Gagal → volume "tertunda", EDA-09 ditulis ulang di sekitar shortlist-uji
(kontinjensi blueprint §6 — DILARANG improvisasi proxy lain). F2: joint 8 sel
= 1514 + rekonsiliasi margin vs primer EDA-07. F3: demo within-band 1 band.
F4: seed BARU independen format YYYYMMDD-eksekusi TERCATAT (tempel nilainya).

## FASE 3 — Build + run

Notebook exit 0 via nbconvert (tempel exit code + jumlah sel/asersi).
Deterministik (rerun = angka sama). Assertion mesin untuk tiap angka pagar:
whitelist hari ⊆ manifest 384 hari-R (gagal = STOP; monkey-patch I/O DILARANG);
V/P mustahil dibaca. Famili FDR-BH q=0,10 TERTUTUP tepat 4 uji
(wick-pooled 1 + gap-split 2 + dow-omnibus 1); tambah uji = STOP + amandemen.
Null SEMUA uji = permutasi terstratifikasi B=10000 STRATA=BAND
(wick: nilai-dalam-band + tercil dihitung ulang; gap: label grup dalam band,
gap-split HANYA event non-first, cut 32; dow: label-dow dalam band).
Donor-path DILARANG. L2 resurrection DILARANG (nol simulasi trade).
Year-gate per uji (blueprint §4): wick = tanda pooled-Δ-per-tahun sama;
first/gap-split = tanda selisih sama; dow = hari-max-dev sama + tanda sama;
n<30 → gate tak lolos. Shortlist = FDR-pass + gate-tahun + |Δ|≥5pp
(dow-entry = existence-only); joint = estimasi BUKAN kandidat; BOLEH KOSONG
+ alasan per kandidat. Volume: kunci SATU dari (a)/(b)/(c), laporkan SEMUA
yang dicoba; warmup 20-hari-pertama-R di-drop (count dilaporkan).
Tiap kandidat wajib tag live-computability §9. Tiap angka bertag
generasi/konfirmasi §8.

## Larangan (pelanggaran = run gagal)

Rescan; baca V/P; uji ke-5; donor-path; L2/simulasi trade; tuning cut (32
beku — principled 2×cooldown); expanding-median/minimum-history untuk warmup;
klaim atas sel joint; lokalisasi hari-dow; `except: pass`; `print()` produksi;
fungsi >50 baris / file >400 baris tanpa `# LENGTH_EXCEPTION` (pengecualian
generator §15.1: referensi stabil + diff kecil + deterministik + assertion).

## Format pulang

Laporan AGENTS.md §5: file dibuat/diubah (+ `git hash-object` tiap file klaim
SESUDAH penulisan terakhir) · tabel Klaim & Bukti (TERVERIFIKASI / BELUM
DIVERIFIKASI / ASUMSI / GAGAL — DILARANG "sepertinya OK") · section FASE 0
tersendiri · yang belum diverifikasi · potensi masalah · saran. Satu ronde
satu vonis: DILARANG "sekalian coba varian".
