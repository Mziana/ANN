# DRAF PROMPT — Spec Arsitek Batch-2 (H4+H5) — 2026-10-09

> Status draf: disusun asisten 2026-10-09, MENUNGGU user paste ke arsitek.
> Simpan sebagai: `.ai/assistant/prompts/2026-10-09_spec-batch2-H4H5-arsitek.md`

---

Anda adalah **Arsitek** (AGENTS.md §26–§27: merancang + memutus konflik +
tie-break; DILARANG menulis kode produksi). Tugas SATU-SATUNYA sesi ini:
**tulis spec eksekusi Batch-2** untuk H4 + H5 di:

`reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md`

**Bukan** eksekusi, **bukan** audit angka, **bukan** vonis H4/H5 (vonis milik
putusan terpisah sesudah re-audit, pola Batch-1). H1/H2/H3 tetap GUGUR —
putusan ini tidak membukanya sejengkal pun.

## S-2d. Brief mandiri (angka di bawah = seluruh yang Anda butuhkan)

**Hash terukur asisten 2026-10-09, HEAD
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`** (ukur ulang sesi ini sebelum
satu baris pun ditulis; mismatch = STOP):

```
9720280320dcc813d422d6f540e37847b70571ff  arsitek/hipotesis_lock_v1.md
e8eb03daf994051600258cf412ec9e9af65d800c  arsitek/putusan-arsitek-H1-H5.md
15ecb37dcfc62df64196714eed3ceabdc6a31ced  ../../eda/2026-10-06/report.md
ca4e0b70d9dc4272347b74b1ea78d7a5f94593ee  arsitek/putusan-lapisan3-H1H2.md
c643c1c934055d1b85d972f4e2e2f65d8d57a69f  arsitek/putusan-lapisan3-H3.md
91d4c99307e3750e78802b5b424af579e2113249  arsitek/putusan-arsitek-B1.md
```

**H4 (lock §H4 + S5):** 6 jam UTC teratas `[14, 13, 0, 15, 12, 7]`, semua di
dalam sesi berlabel (share Off = 0,0; n Off = 0; guard `n_Off < 2`); massa
London+NY = 0,7827; mean |r| per sesi (pip/bar, label eksklusif): London
1,666 · Tokyo 1,439 · Sydney 1,196 · NewYork 1,139; M3 DST-aware vs
cross-tab UTC-tetap SETUJU. Ambang gugur lock: ≥2 dari 6 jam teratas jatuh
Off pada data OOS baru (kanon M2), ATAU EV-after-cost 6 jam masuk H4 ≤ 0.
S5: EV memakai 6 jam TETAP di atas + `cost_basis` fragmen 4b; uji pola OOS
memakai 6 jam teratas HITUNG-ULANG; keduanya dicatat TERPISAH.

**H5 (lock §H5 + S6 + B1-butir-1):** Q6 real 0,469–0,490; placebo_acak 0,4989
[0,4831–0,5144]; placebo_hl 0,4890–0,4922 (0,4890 = titik estimasi hl_utc,
bukan batas bawah CI [0,4748/0,4798]); rasio vol/spread kanon M4 (mean|r|
thd spread p95 per-bar M1): London 2,0823 · Tokyo 1,5992 · NewYork 0,9488 ·
Sydney 0,7975 → flag biaya-mendominasi (rasio < 1) = [NewYork, Sydney];
T-01 massa nol 5,83% (78.582 bar; A 66.817 = 5,88%, B 10.572 = 5,71%).
Protokol placebo nb04: seed 20261006, M5, theta 0,5×ATR(14), window 6/12/24,
bootstrap 10.000 day-cluster, touch-genuine, retensi event placebo
46,8–55,7% dilaporkan. H5 baca `spread_pips` M1 LANGSUNG (putusan B1
butir 1). Ambang gugur lock: pada SETIAP sub-populasi hit-rate real ≤
placebo (CI95 memuat 0). S6: wajib lapor JUMLAH SEL; klaim sel mana pun
wajib koreksi multiplicity BERNAMA atau replikasi independen; tanpa itu =
eksplorasi.

**Infra/aturan warisan (berlaku, bukan diputus ulang):** D4 974 hari-broker
(`47d15c41…`, grain TUNGGAL broker-day); burn-in kanonik 60 POSISI +
rule posisi-vs-nilai + min_periods eksplisit (P-3); R-B1 manifest parameter
(nilai tanpa sumber = GAGAL); R-B2 bucket akunting genap (hilang senyap =
GAGAL); R-B3 pagar exit (strategi ber-SL/TP wajib distribusi jenis-exit +
justifikasi jarak; SL/TP tak tersentuh = fakta desain); R-B4 venv kanonik
satu-satunya lingkungan gate; pola P-1/P-2/P-3 (exact-comparison,
paired/CI, pola C2 pensiun); anti-penyelamatan DUA ARAH; alpha 0,01;
TERBUKA tercatat: `cost_basis.default=0,65` vs `spread.default=1,5`
(otoritas biaya wajib Anda pin di Q3).

## Q1. PUTUSAN: desain OOS + status 2026 (DIPUTUS — tanpa ini spec tak bisa ditulis)

Fakta desain: EDA menghitung seluruh angka H4/H5 atas full-sample 2023–2026,
sehingga "OOS baru" tidak bisa berupa potongan 2023–2026 yang diklaim buta.
Rekomendasi asisten (boleh Anda tolak dengan alasan tertulis): **walk-forward
expanding-window tahunan sebagai kanonik** — 2023 = tahun seed/pemanasan,
evaluasi penentu = 2024 dan 2025, tiap tahun-Y hanya memakai informasi ≤ Y−1
(top-6 hitung-ulang H4 dan cutoff kuartil-ATR H5 dari histori s/d Y−1; grid
sel TETAP); **2026 parsial DIKECUALIKAN dari penentu** (konsisten preseden
H2/B4-06), boleh deskriptif. Opsi single-block (2026-parsial sebagai OOS +
threshold EDA beku) tercatat DITOLAK karena daya kecil + kontaminasi penuh.
Putuskan: (a) kanonik OOS, (b) status 2026, (c) stance seed-threshold
(expanding-history vs EDA-beku-transparan).

## Q2. PUTUSAN: grid sel H5 + koreksi multiplicity (DIPUTUS)

Ambang lock asimetris (GUGUR butuh SEMUA sel gagal) = tanpa koreksi, makin
banyak sel makin mudah "lolos". Rekomendasi asisten: **grid TETAP 4 sel
(sesi ∩ hari-kuartil-atas-ATR) + 1 agregat Q4-ATR deskriptif (bukan
penentu); koreksi Holm atas 4 sel; TAHAN bila ≥1 sel lolos PASCA-koreksi,
GUGUR bila semua gagal pasca-koreksi**; FDR DITOLAK untuk vonis (butuh
FWER). Putuskan: grid final, metode koreksi BERNAMA, aturan keputusan
eksplisit. Tanpa koreksi = eksplorasi (S6 verbatim, bukan negosiasi).

## Q3. PUTUSAN: pin biaya H4 (DIPUTUS)

Pasangan tiap jam-tetap → sesi label-eksklusif, otoritas biaya
(rekomendasi: `cost_basis` fragmen 4b — tutup selisih 0,65-vs-1,5 di sini),
satuan, dan perlakuan tahun 2023. Nilai tanpa sumber = GAGAL (R-B1).

## Q4. PUTUSAN: mekanik strategi pintu H4 (DIPUTUS)

Entry/exit mekanis pra-registrasi + stance SL/TP: bila pakai SL/TP maka
R-B3 mengikat penuh (distribusi jenis-exit wajib + justifikasi jarak vs
frekuensi cek exit); bila tanpa SL/TP, nyatakan eksplisit. DILARANG
mengganti jam-tetap dengan top-6 OOS untuk klaim EV (shopping varian).

## Q5. PUTUSAN: pin placebo H5 (DIPUTUS)

Konfirmasi PERSIS nb04 (seed/window/theta/tie/touch-genuine/retensi sebagai
bucket bernama R-B2) + spread M1 langsung + definisi kuartil-atas-ATR
(expanding, konsisten Q1) + grain broker-day. Satu penyimpangan pun wajib
dinamai + dibenarkan, atau = cacat spec.

## Isi spec (wajib)

S0 bukti-baca (hash ukur-ulang + pernyataan baca utuh lock/putusan/report);
Uji S-H4 (EV jam-tetap + pola OOS, Proposal Uji S21, metrik + ambang
pra-registrasi, S-C mesin + output mentah, S-B larangan bentuk-spesifik:
no-cell-carving, no-hour-shopping, no-2026-smuggling, no-threshold-peeking,
no-FDR, no-eksklusi-buta; S-R relasi hilir); Uji S-H5 (idem + grid sel +
Holm + aturan keputusan Q2); manifest R-B1; S-B memuat R-B2/R-B3/R-B4;
C8 blob; self-audit 1×. Ambang lock VERBATIM — nol ambang baru, nol
perubahan tanpa addendum.

## Disiplin tulis (mengikat)

Baca-ulang AGENTS.md §26–§27 + bukti hash bacanya; anti-salah-ketik 5 lapis
(manifest + kutip-balik presisi-penuh + bukti hash); klaim tanpa output
mentah = GAGAL; ASCII murni, LF-only; staged 0, tanpa commit.
