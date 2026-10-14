# Ledger pra-run — Pemanasan-2 flip-murni (NON-VONIS)

Tanggal: 2026-10-13. Eksekutor: Commander (langsung, brief
`.ai/assistant/prompts/2026-10-13_pemanasan-P2-flipmurni.md`).

## Bed + prosedur (warisan R2, tanpa ubah)

- M1: `data/processed/M1/usdjpy_m1_2026.parquet` (paruh-1 2026-01-01..05-18,
  paruh-2 2026-05-19..10-02), seed `1337`, biaya 3 lapis literal R2,
  anomali 2026-03-10..03-27 KELUAR dari denominator.
- Scan: REUSE KODE R2 (`d1_events.py` via import, folder R2 read-only).
- Race: REUSE KODE R2 (`d2_outcomes.evaluate`, SL=1,5xATR TP=3,0xATR beku).

## Perubahan vs R2 (SATU + SATU overlay)

1. `side_scan` = side asli pasca-scan; `side` = `-side_scan` sebelum
   `evaluate` (flip-murni; pagar TIDAK digeser).
2. Replay 1-posisi (beku, §Definisi brief): kronologis entry bar
   e=t0_pos+1 (tie-break urutan file); hanya evaluable
   (cancel=='' dan BATR_res IN TP/SL/TIME); buka bila e>=busy_until;
   busy_until baru = t0_pos+kbar+1 (SL/TP) atau t0_pos+12 (TIME);
   AMBIGUOUS/cancel tidak membuka dan tidak memblokir.

## Tafsir (asimetri, ditempel di laporan)

KALAH = varian gugur kuat (tutup jalur flip). MENANG = tanpa makna
(bed 2026 terpakai) — tetap wajib bed baru. Tanpa D-8, tanpa segel.
