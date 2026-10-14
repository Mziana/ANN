# Brief Pemanasan-2 / P2-flipmurni — Eksekusi langsung (2026-10-13)

## Status: PEMANASAN DIAGNOSTIK — BUKAN RONDE VONIS

Tafsir asimetri (ditetapkan arsitek + user, ditempel di laporan):
- KALAH = varian flip-murni gugur kuat → hemat bed 2025, tutup jalur flip.
- MENANG = tanpa makna (bed 2026 sudah dipakai R2+R3) → tetap wajib bed
  baru untuk arti apa pun. Tidak membuka segel, tidak mengubah status R1/R2.

## Keputusan user yang dikunci (2026-10-13)

1. JANGAN geser pagar: barrier = R2 persis (SL 1,5xATR, TP 3,0xATR).
2. Metode 1-posisi: tidak ada entry baru sebelum posisi terbuka close.
3. Bed = 2026 yang sama (pemanasan, murah, non-vonis).

## Satu-satunya perubahan vs R2

`side -> -side` (SATU operasi sesudah scan, sebelum evaluate).
Selain itu NOL perubahan: scan, ATR, barrier, biaya, horizon, cancel.

## Anti-drift (pelajaran R3)

DILARANG menafsir ulang prose spec. Scan WAJIB reuse kode R2
(`d1_events.py`: scan_e1/scan_e2/scan_e3/apply_exclusions/compute_atr_m5,
via import dari folder evidence R2 — folder R2 read-only, tidak ditulis).
Kewajiban: jumlah event per sel IDENTIK dengan R2 (E1 6 sel + E2 + E3);
selisih >0 = run gagal. (R3 melar E2 2,34x karena tafsir prose — dilarang
terulang.)

## Kontrak eksekusi (warisan R2, D2-4/D2-5)

- Entry OPEN bar t0+1; BUY ASK->BID / SELL BID->ASK (mengikuti side HASIL
  FLIP); spread nol dan mid dilarang.
- First-passage 10 bar sesudah bar entry (t0+2..t0+11); bar-kembar SL+TP =
  AMBIGUOUS (buang + hitung eksplisit, sama seperti R2).
- TIME exit = close t0+11. Biaya 3 lapis literal R2. Q0 gerbang 300
  dilaporkan (bukan gerbang vonis — pemanasan tidak memvonis).
- Kolom JSON = skema R2 (D-3.4 warisan) + 3 kolom tambahan: `side_scan`
  (sisi asli pra-flip), `pos1_seq` (-1 = tidak dibuka di replay 1-posisi),
  `pos1_busy_until` (bar-index).

## Definisi beku replay 1-posisi (SATU-SATUNYA hal baru, dibekukan di sini)

- Urutan kronologis: entry bar e = t0_pos+1, tie-break = urutan file.
- Hanya event evaluable (cancel=='' dan BATR_res != AMBIGUOUS) ikut replay;
  cancel/AMBIGUOUS tidak membuka posisi dan tidak memblokir.
- Event dibuka HANYA bila e >= busy_until ( sedentary awal = -inf).
- busy_until sesudah membuka event dengan kbar=k:
  SL/TP -> t0_pos + k + 1; TIME (k=10) -> t0_pos + 12 (exit di close t0+11).
- Catat: n_dibuka, n_dilewat (terblokir sibuk), net stacked vs net 1-posisi.

## Verifikasi byte-level (run gagal bila satu pun meleset)

1. Scan: count per sel == R2 events.jsonl (8 sel, toleransi 0).
2. Flip: side == -side_scan untuk SEMUA baris; side_scan == side R2 pada
   pasangan (t0_utc, family, cell).
3. Pagar: sl_pips == 1,5*atr dan tp_pips == 3,0*atr untuk semua evaluable.
4. Determinisme: 2 run -> events.jsonl hash identik.

## Keluaran

Folder BARU `reports/research/2026-10-13/discovery-P2-flipmurni/evidence/`:
ledger pra-run + manifest hash + `run_flipmurni.py` + `events.jsonl` +
`summary.json` (stacked per-sel + 1-posisi + tabulasi cermin vs R2) +
run_stdout.log. Tanpa D-8, tanpa segel. Folder R2/R1 tidak disentuh.

## Larangan

Baca folder R2 (import kode OK); tulis ke folder R2/R1 = gagal. Tanpa
2023/2024/2025. Tanpa varian tambahan. Tanpa indikator. Tanpa p-value
seleksi. Tanpa `except: pass`. Tanpa `print()` produksi (logging).
Fungsi <50 baris, file <400 baris.
