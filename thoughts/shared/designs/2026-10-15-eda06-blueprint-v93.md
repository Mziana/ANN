# BLUEPRINT FINAL v9.3 — eda_06_candle_anatomy_regime.ipynb

> Dicatat: 2026-10-15. Status: FINAL, siap ke coder (Pre-Flight Checklist).
> Riwayat: v8.1 → v8.8 → v8.9 → v9.0 → v9.1 → v9.2 → v9.3.
> v9.3 = v9.2 + 3 patch terakhir (side-consistency real + placebo, shared triggers).
> Klaim "clip pseudo extreme 0,5 pip" DITOLAK dengan bukti (max() sudah meng-clip).

## BAGIAN 0 — KONTRAK TERKUNCI

| Parameter | Nilai |
|---|---|
| Biaya eksekusi | 0.95 pip |
| Threshold Net TP minimum | 2.85 pip |
| Filter R:R minimum | 1.0 — hanya untuk momentum (reversal dikecualikan, R:R dilaporkan saja) |
| Spike threshold | Bar pertama sequence: range > 2.0 × ATR_M15(14, shift 1). Varian longgar: > 1.5 × ATR |
| Exhaustion RSI | ≥ 70 atau ≤ 30 dalam 6 bar setelah spike berakhir (RSI Wilder/ewm alpha=1/14, tanpa shift) |
| Momentum RSI | 40–55, dua titik: bar pertama sequence (primer: 4a1/4b1) dan bar terakhir s (varian: 4a2/4b2) |
| OR | 4 bar M15 pertama setelah daily open. OR_top = max(high), OR_bottom = min(low). Tidak ada definisi sesi di dokumen ini |
| Trigger ≥ bar ke-5 | Mencegah spike memakai bar pembentuk OR |
| Window first-passage | K=16 primary, dihitung SETELAH entry (confirm+1..confirm+K). K=8/32 robustness, bukan kill |
| Partisi data | Hanya R (2023-07-01 s.d. 2024-12-31), stratum A, minus 19 hari anomali |
| Bootstrap real | Day-cluster 10.000 resample, seed 20261006 |
| Placebo | 1000 set per track × 2 track (reversal-track, momentum-track), seed dasar 20261007 (independen dari bootstrap). Trigger acak shared kedua track (NULL_SHARED_TRIGGERS = true) |
| Placebo direction | Reversal-track: pseudo-dir = sign(close_trigger − daily_open), verifikasi di entry. Momentum-track: coin flip 50/50 seeded |
| Placebo extremes | pseudo_spike_high/low = max/min 3 bar trailing (PSEUDO_N = 3). Rumus SL IDENTIK dengan real |
| Minimum hari ber-event / total event | 30 / 30 |
| FDR | BH q=0.10 global atas core {Sel 1, Sel 2, Sel 3, Sel 4a1}. Sensitivitas {4a2, 4b1, 4b2}: p nominal saja |
| Daily open hours | [21, 22] |
| Power rule | n < 30 ATAU lebar CI95 mean net_pnl_pip > 5 pip (POWER_CI_PIP = 5; ~2× edge minimum 2,85) → UNDERPOWERED. CI win-rate (>25 pp) pendukung saja |
| Statistik primer | Mean net P&L per event dalam pip (termasuk timeout di-MTM, dikurangi biaya) |
| Aturan advance | Core LOLOS ≥ 1 → TV-01. Hanya-sensitivitas LOLOS → eksploratori, TIDAK advance |

**Jangkar waktu:** s = bar terakhir spike sequence; r = bar touch RSI dalam s+1..s+6 (Sel exhaustion, tanpa r = bukan trigger); trigger = r (exhaustion) atau s (momentum); confirm = trigger+1; entry = close(confirm); window = confirm+1..confirm+K.

**LOLOS:** LOLOS = (real mean > persentil 97,5 null track yang sesuai) DAN (lolos FDR untuk core / p nominal < 0,10 untuk sensitivitas).

## BAGIAN 1 — PRE-FLIGHT CHECKLIST (gate keras, laporan sebelum coding)

- **Cek 1 (trace positif):** 1 hari R — jam bar pertama (21/22 UTC) → daily open → OR_top/OR_bottom → spike ≤ 8 jam pertama (sequence, s = bar ke-berapa) → r (RSI touch s+berapa) → konfirmasi r+1 → entry/TP/SL → sentuhan pertama → label. Ambigu → STOP.
- **Cek 2 (trace negatif):** hari spike tanpa balasan, lacak penuh, pastikan tidak ada yang hilang.
- **Cek 3 (partisi):** max(utc) < 2025-01-01; nol broker_day anomali; hari ≈ 384 (minus drop open-abnormal); bar M15 ekspektasi 30.000–42.000 (dari terukur 2024: 23.909/tahun). STOP hanya jika < 20.000 atau > 60.000.
- **Cek 4 (dry-run funnel, tanpa first-passage):** total bar → spike → exhaustion → sideways makro → akumulasi mikro → filter waktu → pre-filter biaya → side-check → Sel 4a1/4a2/4b1/4b2. Sel 3 < 30 → STOP UNDERPOWERED. Varian 0 event → drop dari uji.
- **Cek 5 (grep):** 0.95, 2.85, 16, 30, [21, 22], 20261006, 20261007, 5, 1000.
- **Cek 6 (runtime placeholder):** placebo 10 set dulu, ekstrapolasi ke 1000×2 track. > 10 menit → optimize (numba) dulu.
- **Diagnostik (dicatat, aturan tidak diubah):** atrisi pre-filter per posisi bar (bar 5–10 vs 11–32). Bukti pertama jika Sel 3 underpowered.

## BAGIAN 2 — ALUR SEL

### Sel 1: Setup, Kontrak, Assertion
Load R + stratum A. Assert max(utc) < '2025-01-01'. Assert nol broker_day anomali.

### Sel 2: Daily Open & Indikator
Daily open = open bar pertama broker_day, broadcast. Assertion open-abnormal: anomaly_rate (first-bar hour ∉ [21,22]) > 5% → RuntimeError; else drop hari abnormal, lanjut. Indikator: ATR_M15(14).shift(1); ATR_D1(14) dari D1 closed (nilai hari sebelumnya); RSI(14) Wilder/ewm tanpa shift. Komentar seed: 20261007 ≠ 20261006 = dua proses acak independen.

### Sel 3: Fitur Kontinu & Anatomi
body_ratio, wick_up, wick_down; rolling percentile window 500 (~5 hari, regime lokal). pre_i_size (range pip bar trigger−i) + pre_i_dir (+1/−1/0), i=1..10. dist_to_daily_open (pip).

### Sel 4: Operasionalisasi Hipotesis
- **OR:** 4 bar M15 pertama setelah daily open. Trigger ≥ bar ke-5.
- **Makro sideways (D1-based):** d1_range_5 (max high − min low 5 D1 closed) < 1,5 × atr_d1.
- **Mikro akumulasi (basis OR/ATR):** 12 bar pre-spike: box_range_12 < 0,5×atr_m15 DAN jarak maks 12 close ke batas OR terdekat < 0,25×atr_m15.
- **Spike sequence (dua arah eksplisit):** threshold di Bar1 (>2,0×ATR; varian longgar >1,5×ATR). Bar 2–3 opsional jika close lebih ekstrem searah spike_dir. spike_high = max(high) SELURUH sequence; spike_low = min(low) SELURUH sequence. s = bar terakhir.
- **Exhaustion (Sel 1,2,3):** r = bar pertama s+1..s+6 dengan RSI ≥70/≤30. Tanpa r = bukan trigger.
- **Momentum:** 4a1: Bar1 >2,0×ATR + RSI(bar pertama) 40–55 (primer). 4a2: sama + RSI(s). 4b1/4b2: threshold 1,5×ATR. Varian 0-event = insight; <30 event = drop dari uji, lapor terpisah.
- **Filter waktu:** trigger dalam 32 bar pertama sejak daily open.
- **Pre-filter biaya:** |close_trigger − daily_open_price| > 2,85 pip.

### Sel 5: Konfirmasi & Labeling
1. Konfirmasi di confirm = trigger+1. Reversal: warna confirm berlawanan spike_dir. Momentum: close_confirm melampaui close_trigger searah spike. Gagal → label −1 ('confirmation_failed'). Stop.
2. Entry = close_confirm. Reversal: TP = daily_open_price; SL sell = max(entry+1,0×ATR, spike_high+0,5); SL buy = min(entry−1,0×ATR, spike_low−0,5). Momentum: TP = entry±1,5×ATR; SL = entry∓1,0×ATR.
3. Post-filter: Net TP = |entry−TP| − 0,95 < 2,85 → skip 'cost_too_low' (semua sel). R:R = Net TP/|entry−SL| < 1,0 → skip 'rr_too_low' (MOMENTUM SAJA; reversal catat rr_value tanpa gugur).
4. **Side-consistency REVERSAL (Patch A):** SELL wajib entry > daily_open; BUY wajib entry < daily_open. Langgar → label −1 ('wrong_side').
5. First-passage K=16: confirm+1..confirm+16, high/low intra-bar. Label 1 (TP dulu) / 0 (SL dulu) / 2 (timeout).
6. net_pnl_pip: win/loss dari TP/SL minus 0,95; timeout = P&L bertanda di close confirm+K minus 0,95. Win-rate = L1/(L1+L0); timeout_share terpisah.
7. skip_reason: None / 'confirmation_failed' / 'rr_too_low' / 'cost_too_low' / 'pre_filter_cost' / 'wrong_side'. Non-None → label −1 (audit filter, keluar inferensi).
8. Dedup per-spike: cooldown 16 bar dari s. Satu spike → satu baris per sel lolos (kolom sel_name) + overlap_with + is_first_spike_of_day.

### Sel 6: Inferensi Statistik
1. Bootstrap real day-cluster 10.000x → CI95 mean net_pnl_pip (lapor + power rule).
2. Placebo per track (1000 set): trigger uniform 32 bar pertama tiap hari ber-event (jumlah = trigger nyata, min 1; SHARED kedua track). Reversal-track: pseudo-dir = sign(close_trigger−O), verifikasi sign(entry−O), beda → drop 'wrong_side'; TP = open; SL rumus identik via pseudo extremes. Momentum-track: pseudo-dir coin flip; TP = entry±1,5ATR. Mean per set → null per track.
3. p_sel = (1+#{null ≥ real})/1001 → FDR BH q=0,10 atas {1,2,3,4a1}. Sensitivitas p nominal. <30 event → drop, "statistik tidak viable".
4. LOLOS core = null-beat DAN FDR-pass. Sensitivitas = null-beat DAN p<0,10 (eksploratori). K=8/32 robustness. Catatan nested-test wajib. Kill: semua core gagal → gugur; ≥1 core LOLOS → TV-01.

### Sel 7: Handoff
Kolom: utc, daily_open_price, or_top, or_bottom, atr14, rsi14, rsi_bar1, rsi_at_s, spike_dir, spike_high, spike_low, trigger_bar, confirm_bar, entry_price, tp_price, sl_price, rr_value, net_pnl_pip, label_final, skip_reason, sel_name, overlap_with, is_first_spike_of_day, pre_1_size..10_size/dir, is_confirmed_color (reversal: warna lawan; momentum: searah), is_confirmed_breakout (momentum: confirm lewati extreme; reversal: False/tidak berlaku). Kolom placebo: null_track, pseudo_dir. Disclaimer: OR = 4 bar setelah open; window setelah entry; timeout MTM; placebo 1000 set×2 track; R:R tak gugurkan reversal; biaya flat 0,95. Partisi: EDA-06/TV-01/FS-01 di R; ANN-01 train R, validasi V, test P.

## BAGIAN 3 — INSTRUKSI CODER
Pre-Flight + laporan dulu. Jangan ubah: 0.95, 2.85, 16, 30, [21, 22], seed 20261006/20261007, power 5 pip, placebo 1000×2 track, FDR core {1,2,3,4a1}, PSEUDO_N=3, NULL_SHARED_TRIGGERS. Anti look-ahead: trigger ≤ close trigger_bar; konfirmasi/entry bar berikut; outcome setelah entry. spike_high/low = SELURUH sequence. Assertion crash disengaja, biarkan crash. NaN drop + lapor, nol imputasi. Stream + parquet sebelum TV-01. Cek 6 runtime dulu. Error/ambigu → STOP, jangan improvisasi.

## BAGIAN 4 — CONSISTENCY CHECK (wajib di akhir)
Cetak + assert: COST_DRAG_PIP==0.95, MIN_NET_TP_PIP==2.85, MIN_RR_RATIO==1.0 (RR_SCOPE=="momentum"), K_PRIMARY==16, PARTISI 2023-07-01..2024-12-31, MIN_DAYS==30, MIN_EVENTS==30, DAILY_OPEN_HOURS==[21,22], POWER_CI_PIP==5, N_PLACEBO==1000, NULL_TRACKS==2, NULL_SHARED_TRIGGERS==true, FDR_CORE=={1,2,3,4a1}, PSEUDO_N==3, OR_DEF=="4 bar setelah daily open".

## RIWAYAT PERUBAHAN (v9.2 → v9.3)
1. Side-consistency real: 'wrong_side' (lubang yang sama di pipeline real, ditemukan saat verifikasi klaim kritis).
2. Placebo reversal dir = sign(close_trigger−O) + verifikasi entry; momentum tetap coin flip.
3. Trigger acak shared dua track.
4. Clip 0,5 pip DITOLAK (max() sudah meng-clip; SL ≥ entry+1 ATR selalu).

STATUS: FINAL. Koder: jalankan Pre-Flight. Tidak ada iterasi blueprint lagi — masalah berikut = masalah kode.
