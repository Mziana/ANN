# Laporan EDA Final — USDJPY 2023–2026 (Rantai nb00–nb05)

**Tanggal:** 2026-10-06 · **Rancangan:** EDA v3.1 (kanonik) · **Status:** draf untuk
review user + audit Klenz. **Metode BELUM dipilih** — output EDA berhenti di hipotesis.

## Sumber kebenaran (notebook tereksekusi, blob git)

| Notebook | Blob | Assertion | Menjawab |
|---|---|---|---|
| `eda_00_setup.ipynb` | (preregistrasi Kontrak 00) | 11/11 | definisi, strata, placebo |
| `eda_01_returns.ipynb` | `ec448a593c1b` | 23/23 | Q1 |
| `eda_02_volatility.ipynb` | `8ff4358d4175` | 30/30 | Q2, Q3, spread |
| `eda_03_autocorr.ipynb` | `0158ca994db9` | 31/31 | Q4 |
| `eda_04_swings_levels.ipynb` | `4ac4566f5f6c` | 30/30 | Q5, Q6 |
| `eda_05_regimes.ipynb` | `661c0aeb2357` | 68 | Q7, sintesis, T-01 (KOREKSI pasca-audit Batch A L3-01/L3-02/L3-03/L3-05 + L2-02; KOREKSI pasca-audit Batch B B4-01…B4-12 + B6-04 + L3-06; KOREKSI B9-01: 67 → 68 (+1 guard regresi `hour_utc`) + regen B8-04; blob & count dimutakhirkan; KOREKSI NL2 2026-10-07: regen LF deterministik pasca-proses Q2 → blob `661c0aeb2357`, KOREKSI M1 2026-10-07: pin lama `2cb57ad9ec1a` dipensiunkan karena merge chunking output pada regen NL2 — bukan karena era CRLF — provenance) |

Kalender: 1.347.847 bar M1 (2023–2026), 974 hari broker = strata A 825 hari
(1.136.401 bar) + B 130 (185.248) + C 19 (26.198); bucket D1 = kalender-broker
(R3, Lampiran A1); label hari-UTC membawa offset struktural −1 dan tidak pernah
digeser agar "sepakat" (R1–R2).

---

## Q1 — Distribusi return (nb01)

| Klaim | Status | Bukti |
|---|---|---|
| Ekor tebal di semua TF strata A | TERVERIFIKASI | kurtosis ekses M1 195,5 · M5 102,8 · M15 51,2 (σ: 1,61e-4 / 3,57e-4 / 6,12e-4); skew −0,74/−1,46/−1,22 (KOREKSI Q-TR-01 pasca-trace: M15 −1,22, bukan −1,23) |
| Kuantil ekstrem asimetris negatif | TERVERIFIKASI | q0,1% vs q99,9% M1: −9,67e-4 / +9,17e-4; M15: −4,04e-3 / +3,50e-3 |
| Skew strata B tidak kokoh tandanya | TERVERIFIKASI | bootstrap CI95 = [−3,0e-11, 5,6e-11] → pola, bukan temuan |
| "Massa nol" (T-01) | TERVERIFIKASI | 5,83% bar M1 |r|=0 persis; diratifikasi ulang nb05: 78.582 bar (A 66.817 = 5,88%; B 10.572 = 5,71%) |
| Atribusi kurtosis pada mikrostruktur | TIDAK DIDUKUNG (temuan negatif) | nb01: atribusi 'microstructure noise' untuk kurtosis TIDAK didukung Q1 — klaim yang sudah diuji dan ditolak, bukan "belum diverifikasi" (KOREKSI B6-04 pasca-audit Batch B) |

Figures: FIG-01/02/03 (QQ M1/M5/M15 vs normal).

## Q2/Q3 — Volatilitas per jam & sesi (nb02)

| Klaim | Status | Bukti |
|---|---|---|
| Profil per jam dinding broker & per sesi tersusun | TERVERIFIKASI | tabel Σr², mean\|r\| (dan no-gap), tick_volume, share r² harian per jam (output nb02) |
| Ekor spread per sesi × tahun, M1 vs M5-max (D10) | TERVERIFIKASI | maks M1 = maks M5-max di 16/16 bucket; contoh: London p99 1,20→1,40; NY 2,00→2,80; Tokyo 1,30→1,50; Sydney 2,70→3,40 (KOREKSI Q-TR-02 pasca-trace: 16/16, bukan 17/17) |
| Marker waktu terbukti DST-aware (D12) | TERVERIFIKASI | Tokyo fix 00:55 UTC ×825 hari; NYSE open jam 13 UTC ×560 (EDT) + jam 14 ×264 (EST) |
| Strata B = regime spread berbeda | TERVERIFIKASI | H1-2023 p95 5,30 / p99 8,50 / %>3pip 5,17% vs H2-2023(A) 0,60 / 1,10 / 0,23% → rasio p95 5,30× |

Fragmen spread (`spread_fragment.yaml`, sha256 `6596adf2…`) **sudah direview langkah 4b
dan diterapkan** ke `configs/data.yaml` sebagai `cost_basis` (MEAN) + `stress_bands`
(p95/p99) — keputusan Lampiran A2; `by_year[2023]=3,0` dipertahankan dengan komentar
ulang (sifat file utuh, bukan semesta trading).

## Q4 — Autokorelasi (nb03)

| Klaim | Status | Bukti |
|---|---|---|
| ACF dihitung lag 1–60, all & no-gap, A dan B (D1) | TERVERIFIKASI | tabel ACF 3 TF × 2 strata; maks \|ACF\| = 0,022639 (B M15 lag 50; no-gap) — klaim lama "≤0,012" DICABUT |
| Ljung-Box manual (scipy chi2.sf), h=5/15/60 | TERVERIFIKASI | Q>0, Q/n>0, p∈[0,1] di A & B; p-value BUKAN kesimpulan — baca Q/n + besaran ρ |
| Sign-ACF lag-1 negatif semua sel (D4) | TERVERIFIKASI | A: M1 −0,017702 · M5 −0,009805 · M15 −0,022624; B: −0,013226/−0,012994/−0,017336 → mean-reversion jangka sangat pendek terbaca di TANDA, bukan besaran |
| VR: M1 mean-reversion, M15 momentum lemah | TERVERIFIKASI | rata-rata VR(2–60): A M1 0,9796 · M5 0,9942 · M15 1,0337; B: 0,9848/1,0332/1,0236 |
| Tabel delta A-vs-B lengkap | TERVERIFIKASI | PASS "Tabel delta A vs B lengkap (3 TF)"; daya B kecil → "tidak terdeteksi pada n ini" |

## Q5 — Struktur swing (nb04)

| Klaim | Status | Bukti |
|---|---|---|
| Fraktal k=3 & k=5 di M5, keduanya dilaporkan | TERVERIFIKASI | k=3 high 20.169 / low 20.314; k=5 12.787/13.070; replika nb05 k=3 = 40.483 = 49,07/hari (COCOK) |
| Frekuensi swing per hari (D6) | TERVERIFIKASI | gabungan 48,74 swing/hari (median harian 49; p10 43; p90 54) |
| Waktu tahan median antar swing (D7) | TERVERIFIKASI | k=3: 10 bar (50 mnt); k=5: 15 bar (75 mnt); gabungan 5 bar (25 mnt) — jarak antar fraktal, BUKAN durasi posisi |

## Q6 — Level & placebo (nb04)

| Klaim | Status | Bukti |
|---|---|---|
| Zona BoJ 150/155/160 deskriptif (D12) | TERVERIFIKASI | touch eksak 150: 728 bar/53 hari · 155: 518/51 · 160: 151/20; band 10/25/50 pip (150): 3.532/8.474/16.376; tanpa return pasca-event |
| Hit-rate level vs placebo (preregistrasi nb00) | TERVERIFIKASI | real 0,469–0,490 vs placebo_acak 0,4989 [0,4831–0,5144] & placebo_hl 0,4890–0,4922 (KOREKSI B4-09: dua varian ditampilkan terpisah; batas bawah hl 0,4890 tumpang tindih batas atas real 0,490; KOREKSI Q-TR-03 pasca-trace: hl 0,4890–0,4922, bukan 0,4890–0,5050 — 0,5050 milik placebo_acak; 0,4890 = titik estimasi hl_utc, bukan batas bawah CI [0,4748/0,4798]) → level TIDAK terbukti "dihormati" |
| Protokol placebo identik preregistrasi | TERVERIFIKASI | PASS seed 20261006; retensi event placebo dilaporkan (keterbatasan); tie dilaporkan terpisah |

**Temuan negatif penting:** tanpa bukti = tanpa klaim; Fibonacci tidak diuji.

## Q7 — Regime (nb05, hari-broker R3)

| Klaim | Status | Bukti |
|---|---|---|
| Tipologi hari (ambang median A: ratio_path 0,0268; range/ATR 88,79) | TERVERIFIKASI | A: trending 33,7% / normal 32,5% / range 33,8%; warmup ATR 14 hari B dikeluarkan (n-B tipologi 116, drop dilaporkan); ambang = median full-sample 825 hari A → label ex-post/deskriptif, BUKAN ambang real-time (KOREKSI label pasca-audit L3-01; angka tak berubah) |
| Komposisi tipe-hari A vs B tidak terdeteksi beda | TERVERIFIKASI | chi2=2,248, dof=2, p=0,325 (n-A=825, n-B=116); catatan daya & clustering wajib |
| **Intensitas** hari B > A | TERVERIFIKASI | RV median 3,648e-5 vs 2,292e-5 (1,59×), Cliff δ=−0,384 (konvensi: δ=P(A>B)−P(B>A); δ<0 = B cenderung lebih besar — KOREKSI B4-08), KS p=1,2e-11; Σ\|r\| beda 0,0284 CI95-iid [0,0192, 0,0392] |
| Bentuk hari (range/ATR, ratio_path) A≈B | TERVERIFIKASI | CI95-iid memuat 0 (range/ATR [−7,02, 12,59]; ratio_path [−0,0052, 0,0034]); block bootstrap 20-hari ×10.000 kedua-sisi memuat 0 (range/ATR [−7,63, 13,72]; ratio_path [−0,0038, 0,0028]). KOREKSI pasca-audit L3-02: CI-block lama satu-sisi-A ([−1,72, 6,81]/[−0,0028, 0,0010]) cacat karena B tak di-resample; kolom CI utama kini `ci95_beda_iid` (L3-03; sufiks -iid = KOREKSI L3-06 Batch B) |

Figures: FIG-04 (range/ATR A vs B), FIG-05 (RV harian log10), FIG-06 (tipologi per
strata), FIG-07 (mean \|r\| per jam UTC). Registry figures = tepat FIG-01..07
(terverifikasi di dalam nb05).

**Koreksi pasca-audit Langkah 1 (replika nb03 di nb05):** metode VR kini eksak nb03
(ddof=1, no-gap via kolom `gap_return`) → rata-rata VR(5,15,60) M15-A = **1,0312**
(= referensi nb03 1.0160/1.0119/1.0657); sign-ACF no-gap = **−0,022624** (identik
nb03; n_no_gap 75.038). Angka lama 1,0277 / −0,0220 = metode berbeda yang kini
diganti; referensi lama 1,0337 = rata-rata VR **lag 2–60** nb03, statistik berbeda.

---

## Tabel spread terukur (ringkas; detail = nb02 + fragmen 4b)

| Sesu | p99 M1 | p99 M5-max | maks | Catatan |
|---|---|---|---|---|
| London | 1,20 | 1,40 | 4,60 | strata A, seluruh tahun |
| NewYork | 2,00 | 2,80 | 55,60 | ekor ekstrem, tetap sama di M5-max |
| Tokyo | 1,30 | 1,50 | 8,70 | — |
| Sydney | 2,70 | 3,40 | 24,10 | — |
| H1-2023 (B) | p95 5,30 · p99 8,50 · %>3pip 5,17% | — | — | dilaporkan terpisah (ekor 2023 = artefak strata B) |

Ambang ">3 pip" = deskriptif warisan fetch 2026, BUKAN ambang keputusan trading.

## Sintesis — Hipotesis kandidat H1–H5 (detail ambang = laporan tahap 12)

| ID | Klaim inti | Basis EDA | Ambang falsifikasi (Lapisan 3) |
|---|---|---|---|
| H1 | Kelanjutan arah pada hari trending vs range = hari tenang (KOREKSI B4-01: kedua metrik ≤ median-A = volatilitas & range terendah) | Q7: share 33,7/32,5/33,8% | drift RELATIF (normalisasi ATR, koreksi confound volatilitas) median CI95 memuat 0 ATAU share tak stabil antar tahun |
| H2 | Momentum M15 lemah, tak terbedakan dari iid — hipotesis eksploratori (KOREKSI B4-07: ACF1 z=0,494, CI95 memuat 0; kata "terukur" diturunkan) | Q4: VR 1,0312; sign-ACF −0,022624 (metode eksak nb03) | EV-after-cost ≤0 di ≥2/3 tahun utuh 2023–2025 OOS (2026 parsial dikecualikan; 4-tahun menunggu data — KOREKSI B4-06) ATAU VR OOS ≤1 |
| H3 | Regime B = volatilitas tinggi, terdeteksi real-time | Q7: RV 1,59×, δ=−0,384 (δ<0 = B lebih besar — KOREKSI B4-08) | AUC detektor ≤0,7 ATAU filter >40% hari tanpa mengurangi drawdown (= max peak-to-trough ekuitas strategi Lapisan 3 — KOREKSI B4-11) |
| H4 | Sesi-pintu sebagai alpha kapasitas-rendah; konsentrasi London/NY parsial 78,3% massa 6 jam teratas, bukan eksklusif (KOREKSI B4-02) | Q2/Q3+M2+M3: 6 jam teratas semua dalam sesi (Off=0,0%; guard `n_Off<2` — KOREKSI B4-03); M3 DST-vs-xtab SETUJU (KOREKSI B4-12) | ≥2 jam teratas jatuh Off OOS ATAU EV 6 jam masuk ≤0 (KOREKSI B4-11) |
| H5 | Reaksi level hanya pada sub-populasi vol/spread tinggi | Q6 negatif + M4 kanon p95 (KOREKSI B4-04: London 2,08 · Tokyo 1,60 · NY 0,95 · Sydney 0,80; flag=[NY, Sydney]; contoh rasio = London — KOREKSI B4-10) | hit-rate real ≤ placebo di SEMUA sub-populasi |

Catatan jujur: (a) ranking empiris mean\|r\| sesi = **London 1,666 > Tokyo 1,439 >
Sydney 1,196 > NewYork 1,139** pada label eksklusif — berbeda dari prior sekunder
S5; prior tak dipakai memaksa kesimpulan; (b) KOREKSI B4-04: M4 di nb05 kini memakai
**spread p95 per-bar M1** (kanon v3.1 §5; cross-check cost_basis fragmen 4b cocok
<0,02) — proksi mean-D1 lama hanya tercetak sebagai pembanding, bukan dipakai klaim.

## Ratifikasi T-01 (backlog Klenz)

Temuan nb01 "5,83% bar M1 ber-return persis 0" **diratifikasi** via hitung-ulang nb05
dari parquet: 78.582/1.347.847 = 5,83% (A 5,88%, B 5,71%). Massa nol = sifat microstructure
bar M1 (bid-ask stagnan), dilaporkan sebagai karakteristik data — implikasi biaya
ditangani fragmen `cost_basis`.

## BELUM DIVERIFIKASI (daftar wajib §3 v3.1)

1. Angka sumber-sekunder S5/S6 (jam sesi literatur, pangsa volume, pergerakan pip per sesi) — berlabel sekunder, tak diverifikasi independen.
2. Kalender libur NYSE/TSE — di luar scope EDA; hari bervolume rendah terlihat tapi tak teratribusi ("missing event").
3. Offset jendela anomali 2024-10-28 & 2026-03-10 — BELUM TERVERIFIKASI ke Finex (warisan Lapisan 1); strata C deskriptif saja.
4. Atribusi kurtosis M1 pada mikrostruktur — TIDAK DIDUKUNG (temuan negatif nb01; KOREKSI B6-04 — bukan "belum diverifikasi").
5. Granularitas level .50 & tutup London 16:00 vs 17:00 lokal — dicover cross-tab/sensitivitas, bukan klaim final.
6. Seluruh H1–H5 — belum diuji; uji milik Lapisan 3 (walk-forward, biaya penuh).
7. Daya uji strata B (n=130 hari; 116 untuk metrik berbasis ATR) — hasil negatif ≠ bukti kesamaan.
8. Spread sesi di nb05 — TERUKUR per-bar (KOREKSI B4-04: M4 = spread p95 per sesi
   dari kolom `spread_pips` M1; bukan lagi proksi mean-D1). Pengukuran final biaya
   eksekusi tetap milik Lapisan 3.

## Catatan Lampiran A1 (R1–R4) — tercatat

Seluruh pekerjaan level-hari (Q7, prior-day Q6) terkunci **tanggal-broker** (R3);
hari-UTC = label dengan offset struktural −1 (R1); hanya divergensi melebihi geseran
yang menjadi temuan (R2); aturan R1–R3 tercatat di nb04 §3 dan nb05 §5 (R4). Dalam Q7,
kalender tunggal D1 == hari-broker M1 di-assert (974/974, paritas `m1_bars` penuh).

---

**STOP** — laporan ini bukan akhir proyek: metode BELUM dipilih. Langkah berikutnya =
review user + audit adversarial Klenz → penguncian hipotesis → Lapisan 3.
