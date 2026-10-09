# Brief arsitek — Telaah fondasi opsi B (diagnostik, BUKAN vonis ulang) — 2026-10-09

## Konteks (fakta, bukan instruksi)

Batch-2 TERTUTUP 2026-10-09: vonis resmi **H4 TAHAN + H5 GUGUR** (telak),
H1/H2/H3 GUGUR. EKS-3 tercatat: median EV pool H4 +0,0144 tipis dengan
tanda tahun terbelah (2024 +0,048 / 2025 −0,005) — peringatan stabilitas
tanpa konsekuensi vonis. Tugas ini: uji §17 — apakah kegagalan &
ketipisan itu artefak fondasi (data/biaya/regime) atau vonis informatif.
**Keluaran = protokol diagnostik + rekomendasi. Vonis H1–H5 TETAP.**

Fakta ground (terverifikasi asisten dari disk sesi ini):
- F-1: karantina = 19 broker_day eksplisit (2024-10-28..11-01 +
  2026-03-10..03-27; yang overlap jendela 2024–2025 hanya 5 hari);
  H1-2023 (120 hari, strata B / regime SA-03) BUKAN anomali dan
  dikecualikan eksplisit (`coder/rencana-B2-fase0.md:75-90`,
  `arsitek/putusan-arsitek-F1.md:31-33,80`).
- Biaya: `cost_basis` pip per sesi London 0,61 / NewYork 0,69 / Tokyo 0,62 /
  Sydney 0,8 / Off 0,65; pip_size 0,01; EV = exit − entry − cost_JPY, tanpa
  slippage (`coder/hasil-lapisan3-H4H5.md:93,405-410`). Lock M4: rasio
  vol/spread London 2,08 / Tokyo 1,60 / NewYork 0,95 / Sydney 0,80 →
  flag "biaya-mendominasi" NY/Sydney (`arsitek/hipotesis_lock_v1.md:140-141`).
- Regime: H1-2023 (B) spread p95 5,30 vs H2-2023 (A) 0,60 → 5,3×
  (`reports/eda/2026-10-06/report.md:43`); filter regime H3 GUGUR dan
  DILARANG diaktifkan pada data mana pun
  (`arsitek/putusan-lapisan3-H3.md:141`).

## Peranmu (kontrak bersama `.ai/AGENTS.md` §26–§27)

- Kamu ARSITEK: merancang + memutus. DILARANG menulis/mengubah kode
  produksi, data, config. DILARANG commit/push.
- Workdir: `D:\ANN`. Kamu BUKAN coder (eksekusi = ronde coder terpisah),
  BUKAN auditor, BUKAN asisten.
- Format laporan: tabel Klaim & Bukti (AGENTS.md §5); tiap klaim angka
  WAJIB ditempel output mentahnya — klaim tanpa output mentah = gagal.

## S-2d. Gerbang hash (ukur sesi ini SEBELUM satu butir pun dirancang)

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  arsitek/spesifikasi-lapisan3-H4H5.md
f06a8e27b916172f5824438acd545614360d3b57  coder/hasil-lapisan3-H4H5.md
8a4d21090f27dd53555b3a12583ec337819efb2f  Audit/reaudit-lapisan3-H4H5.md
e02a203b96879d73e90339f2d78a37d15834a23a  arsitek/putusan-lapisan3-H4H5.md
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD
staged 2 (T6): src/features/build_labels.py + tests/test_build_labels.py (A)
```

## Butir rancangan (TERTUTUP — hanya ini)

**U-1. Sensitivitas H4 vs karantina F-1 (DIRANCANG).** (a) Tetapkan dari
kode: apakah eksekusi H4 memakai `quarantine_mask()` sisi konsumen, varian
apa (inklusi/eksklusi) — sitir baris kode, verifikasi ulang (path/baris
bisa bergeser). (b) Rancang hitungan kedua varian atas pool H4: median EV
pool + median per-tahun + n_Off, dilaporkan digit-per-digit + selisihnya.
(c) Aturan baca TERTUTUP: laporkan apakah tanda 2025 membalik atau tidak;
kedua hasil dicatat, vonis H4 TETAP. DILARANG eksklusi buta di luar 19
hari F-1. Perintah mentah wajib di protokol: `grep anomaly_windows`
pada config + `git hash-object` tiap artefak JSON yang diklaim.

**U-2. Dekomposisi biaya H4 + H5 (DIRANCANG).** Urai EV menjadi kaki
bruto vs kaki biaya, per sesi, untuk pool H4 dan tiap sel H5; porsi biaya
vs besaran efek dilaporkan angka. Sandingkan dengan rasio vol/spread M4
lock. Aturan baca TERTUTUP: ini KUANTIFIKASI, bukan jalur penyelamatan —
gap Holm H5 (0,244 vs 0,0025) berorde magnitude; P-5 putusan H4/H5
mengikat (kegagalan H5 DILARANG ditafsir-ulang pasca-hoc). Klaim porsi
biaya WAJIB ditempel tabel per-nilai + definisi EV yang dipakai.

**U-3. Cek regime deskriptif 2024 vs 2025 (DIRANCANG).** Deskriptif saja
dari data beku: spread p95/mean M1 per tahun, level RV, jumlah trade —
disandingkan dengan split tanda H4 (+/−). DILARANG mengaktifkan
`rv_regime_flag` sebagai filter (putusan H3 mengikat). DILARANG
kalibrasi-ulang ambang apa pun (TAU dkk). DILARANG gran hari-broker dari
rekonstruksi UTC (`utc.normalize()` DILARANG — grain tunggal `date_broker`
dari store). Keluaran = "bertepatan / tidak bertepatan", bukan vonis.

## Tugas tulis (satu-satunya tulis yang diizinkan)

Tulis protokol sebagai file .md:
`reports/governance/2026-10-07/arsitek/protokol-telaah-fondasi-B.md`
berisi: S0 (hash terukur sesi ini + tabel Klaim & Bukti) + U-1–U-3
(spesifikasi prosedur per butir: input beku + perintah mentah yang wajib
ditempel coder + aturan baca tertutup) + rekomendasi cabang ("jika X
maka Y", tanpa vonis) + self-audit 3x + STOP.
DILARANG commit/push. DILARANG merumuskan H6 (itu opsi A, ronde terpisah).
DILARANG mengubah vonis H1–H5 dalam bentuk apa pun.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: hash S-2d diukur sesi ini; tiap U berpasangan
sumber beku (file:baris terverifikasi-ulang); perintah mentah ada untuk
tiap klaim yang akan diminta dari coder; aturan baca tiap U tertutup
(dua sisi hasil).
Putaran 2 — Bias & Asumsi: tidak ada butir yang diam-diam membuka vonis
ulang; tidak ada filter/ambang baru yang diselundupkan via U-3; U-2
tidak menjadi pintu penyelamatan H5.
Putaran 3 — Meta-check: lock tak tersentuh; H6+ tetap DITOLAK (tidak
dirumuskan); ruang coder (eksekusi) tidak diambil; STOP menutup ronde
rancang ini.

STOP. Menunggu ronde coder terpisah untuk eksekusi protokol ini.
