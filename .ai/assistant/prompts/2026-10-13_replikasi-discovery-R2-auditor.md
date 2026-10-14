# Brief Replikasi Discovery-R2 — Auditor Eksternal (2026-10-13)

## Otoritas
Spec `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R2.md`
(SPEC EKSEKUSI + Amandemen-R2-1, hash `C05D5E4F…80654C5`,
re-audit fokus = LULUS 8/8). Laporan coder sudah masuk:
TOLAK-sementara E1/E2/E3 (8 sel: median −1,32..−1,72, CI negatif,
paruh-1/paruh-2 negatif semua, TIME-share 0,71–0,84). Tugas Anda:
REPLIKASI DARI NOL — **dilarang mengimpor artefak coder** (`d1-d4`,
`run_discovery.py`, `events.jsonl`, `summary.json`, segel R2).
Fondasi bersama yang boleh dipakai: processed M1 2026,
`configs/data.yaml`, `src/data/resample.py`, teks spec,
`scripts/_build_eda06.py` (resep ATR), preseden nb04 (bootstrap
day-cluster 10.000 seed 1337).

## Putusan arsitek atas J1–J5 (MENGIKAT untuk replikasi)
J1 TERIMA: race = 10 bar SESUDAH bar entry (t0+2..t0+11), TIME exit
= close t0+11; label "H+10" = 10 bar race. J2 TERIMA: MFE/MAE atas
jendela race (deskriptif). J3 TERIMA: Q0 = n_eval (preseden R1).
J4 TERIMA: cluster bootstrap = hari-UTC t0. J5 TERIMA: cek gap
epoch broker mentah, liputan t0+1..t0+20 (pre-outcome, dilaporkan).
Replikasi memakai interpretasi ini; bukan varian baru.

## Yang harus direplikasi / diverifikasi
1. **Urutan governance:** ledger (file 19:51:03) + manifest
   (`created_utc 2026-10-13T12:52:46Z` = 19:52:46 lokal) SEBELUM
   output run (run1 19:52:55–19:53:32, run2 19:53:52–19:54:26).
   Cocokkan dengan filesystem + isi `00_manifest.json` (11 artefak,
   termasuk spec 10.307 byte `C05D5E4F…`, config `1127514518AA…`,
   parquet M1-2026 `7F267BB94005…`).
2. **Independen:** implementasikan ulang scan event E1 (6 sel) + E2 +
   E3 dan outcome mapping (entry OPEN t0+1; race t0+2..t0+11;
   SL=1,5×ATR M5(14) beku / TP=2×SL; biaya 3 lapis literal;
   bar-kembar = AMBIGUOUS buang-terhitung; eksklusi anomali
   2026-03-10..03-27; paruh exact 01-01..05-18 / 05-19..10-02;
   seed 1337). Bandingkan: Q0 n_raw/n_eval per sel (klaim E1
   4906/4674, 3788/3625, 2530/2427, 2112/2034, 1160/1108, 1021/977;
   E2 74344/69538; E3 664/507), median per sel (klaim −1,32..−1,72),
   ci_lo negatif semua, med_h1/med_h2 negatif semua, cancel
   (klaim ATR_NA 4265 / GAP 1360 / ANOMALY_CROSS 10 / OFF 0),
   AMBIGUOUS per sel (klaim 2,1,1,1,0,0,13,0), TIME-share
   (klaim 0,71–0,84), TP 1,7–4,3% / SL 12–24%.
3. **Biaya:** literal config = `cost_basis.by_session` +
   `stress_bands.p95.by_session` (+ fallback default bila sesi tak
   terpetakan — klaim: 0 kejadian, Off 0 bar di 2026);
   `spread.default`/`by_year`/`stress_multiplier` tidak tersentuh;
   komisi 0,3 pip; slippage 0,2/0,3 sebagai ASUMSI berlabel.
4. **Barrier (wajib):** konfirmasi dari KODE + `sl_pips`/`tp_pips` di
   JSON (ground truth: sl = 1,5×atr, tp = 3×atr — contoh terverifikasi
   arsitek: atr 5,82 → sl 8,73/tp 17,46), BUKAN dari string log
   "~766 point" yang berskala display ×10 (artefak kosmetik, tidak
   memengaruhi hasil — catat bila Anda mengonfirmasi).
5. **Segel:** `appendix_D8.sealed.json` utuh (cocokkan SHA
   `2575473C…B7331A`), tidak pernah dibuka untuk keputusan; segel R1
   (`5bc324aa…67df963`) tidak dibuka, tidak dibaca; M15 tidak masuk
   evaluasi mana pun.
6. **Scope:** tanpa 2023/2024/2025 untuk evaluasi, tanpa indikator,
   tanpa threshold/horizon/barrier baru, tanpa p-value untuk seleksi.
7. **Determinisme:** seed 1337 tercatat pra-run; verifikasi klaim
   "dua run identik" (stdout run1 vs run2 + hash artefak).

## Format jawaban
- Per butir: COCOK / TIDAK COCOK + bukti (angka Anda vs angka coder).
- Verdict: LULUS REPLIKASI (semua cocok dalam toleransi numerik yang
  Anda nyatakan eksplisit) / GAGAL (sebut butir + selisih).
- Bila GAGAL: arbitrase §27 — arsitek putuskan atas bukti.
- Larangan: tidak merancang ulang, tidak mengusulkan varian, tidak
  membuka segel (R1 maupun R2), tidak menyentuh 2026 di luar bed
  replikasi, tidak memakai 2023/2024/2025 untuk evaluasi.
