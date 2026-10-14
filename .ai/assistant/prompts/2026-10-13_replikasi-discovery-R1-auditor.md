# Brief Replikasi Discovery-R1 — Auditor Eksternal (2026-10-13)

## Otoritas
Spec `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R1.md`
(SPEC EKSEKUSI + AMANDEMEN-1 + AMANDEMEN-2). Laporan coder sudah masuk:
TOLAK-sementara E1/E2/E3 (median pooled ≈ −3,6 pip, CI negatif, tanda
H1/H2 negatif konsisten). Tugas Anda: REPLIKASI DARI NOL (D-5) —
**dilarang mengimpor artefak coder** (`d1-d4`, `run_discovery.py`,
`events.jsonl`, `summary.json`, segel). Fondasi bersama yang boleh
dipakai: raw/processed M1 2024, `configs/data.yaml`, `src/data/resample.py`,
teks spec, preseden nb04 (bootstrap day-cluster 10.000).

## Yang harus direplikasi / diverifikasi
1. **Urutan governance:** manifest hash + ledger pra-run bertimestamp
   SEBELUM output run (klaim: manifest 14:52:01, ledger 14:52:18,
   output 15:25–15:26 2026-10-13). Cocokkan dengan filesystem +
   isi `00_manifest.json` (5 artefak, termasuk spec 21.307 byte).
2. **Independen:** implementasikan ulang scan event E1 (6 sel) + E2 +
   E3 dan outcome mapping (entry OPEN t0+1, horizon H+10, TP2,5/SL2,5,
   3 lapis biaya literal, AMBIGUOUS dibuang-terhitung, eksklusi anomali
   2024-10-28..11-01). Bandingkan: hitungan event per sel (klaim Q0
   1.142–104.339), pooled median + CI 95% cluster-hari seed 1337 per
   sel (klaim ≈ −3,6, CI negatif), tanda H1/H2 per sel (klaim semua
   negatif), cancel/GAP/AMBIGUOUS (klaim 2.097 cancel semua GAP;
   AMBIGUOUS 3.617/131.415), rasio SL:TP (klaim ≈ 1,7:1).
3. **Biaya:** literal config yang dipakai = `cost_basis.by_session` +
   `stress_bands.p95.by_session`; `spread.default`/`by_year`/
   `stress_multiplier` tidak tersentuh; komisi 0,3 pip; slippage
   0,2/0,3 sebagai ASUMSI berlabel.
4. **Segel:** `appendix_D8.sealed.json` utuh (cocokkan SHA
   `5bc324aa…67df963`), tidak pernah dibuka untuk keputusan; M15
   tidak masuk evaluasi mana pun.
5. **Scope:** tanpa 2025/2023/2026, tanpa indikator, tanpa threshold
   baru, tanpa p-value untuk seleksi. Catat `__pycache__` di folder
   evidence sebagai catatan higiene (bukan verdict).
6. **Determinisme:** seed 1337 tercatat pra-run; ulangi run atau
   verifikasi klaim "dua run identik".

## Format jawaban
- Per butir: COCOK / TIDAK COCOK + bukti (angka Anda vs angka coder).
- Verdict: LULUS REPLIKASI (semua cocok dalam toleransi numerik yang
  Anda nyatakan eksplisit) / GAGAL (sebut butir + selisih).
- Bila GAGAL: arbitrase §27 — arsitek putuskan atas bukti.
- Larangan: tidak merancang ulang, tidak mengusulkan varian, tidak
  membuka segel D-8, tidak menyentuh 2025.
