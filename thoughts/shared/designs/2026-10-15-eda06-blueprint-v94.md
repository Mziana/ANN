# BLUEPRINT FINAL v9.4 — eda_06_candle_anatomy_regime.ipynb

> Dicatat: 2026-10-15. Status: FINAL, dokumen kanonik tunggal untuk LANGKAH 2.
> v9.4 = v9.3 + Amandemen-1 dilebur penuh (isi identik dengan pasangan
> v9.3 + `2026-10-15-eda06-amandemen-1.md`; pasangan itu arsip riwayat, tidak
> perlu dibaca terpisah). Riwayat: v8.1 → v8.8 → v8.9 → v9.0 → v9.1 → v9.2 →
> v9.3 → v9.4. Lampu hijau LANGKAH 2 diberikan 2026-10-15.
> Tidak ada iterasi blueprint lagi — masalah berikut = masalah kode.

## BAGIAN 0 — KONTRAK TERKUNCI

| Parameter | Nilai |
|---|---|
| Biaya eksekusi | 0.95 pip |
| Threshold Net TP minimum | 2.85 pip |
| Filter R:R minimum | 1.0 — hanya untuk momentum (reversal dikecualikan, R:R dilaporkan saja) |
| Spike threshold | Bar pertama sequence: range > 2.0 × ATR_M15(14, shift 1). Varian longgar: > 1.5 × ATR |
| Exhaustion RSI | ≥ 70 atau ≤ 30 dalam 6 bar setelah spike berakhir (RSI Wilder/ewm alpha=1/14, tanpa shift) |
| Momentum RSI | 40–55, dua titik: bar pertama sequence (primer: 4a1/4b1) dan bar terakhir s (varian: 4a2/4b2). Split rezim seragam: tiap sel momentum diuji di hari TRENDING (sufiks t) dan SIDEWAYS (sufiks s) → 4a1t/4a1s, 4a2t/4a2s, 4b1t/4b1s, 4b2t/4b2s |
| Nesting Sel (reversal) | Sel 1 = basis (spike + exhaustion + waktu + pre-filter biaya + konfirmasi + post-filter cost + side-check), TANPA filter rezim. Sel 2 = Sel 1 + SIDEWAYS_D1. Sel 3 = Sel 2 + mikro. Berlaku: Sel 3 ⊂ Sel 2 ⊂ Sel 1 |
| SIDEWAYS_D1 / TRENDING_D1 | SIDEWAYS_D1 := d1_range_5 < P25(d1_range_5/atr_d1 atas trigger) — dihitung di dry-run, angkanya dilaporkan. TRENDING_D1 := NOT SIDEWAYS_D1, dilabeli "non-sideways (trending/ekspansi)" — komplemen, BUKAN definisi tren independen |
| Mikro akumulasi | box_range_12 < P50(box/ATR atas trigger lolos makro) DAN dist < P50(yang sama) — dry-run, dilaporkan |
| Null regime-matched | Null tiap sel = mean placebo track yang sesuai, dihitung di atas trigger placebo (shared) yang memenuhi predikat rezim sel tersebut |
| OR | 4 bar M15 pertama setelah daily open. OR_top = max(high), OR_bottom = min(low). Tidak ada definisi sesi di dokumen ini |
| Trigger ≥ bar ke-5 | Mencegah spike memakai bar pembentuk OR |
| Window first-passage | K=16 primary, dihitung SETELAH entry (confirm+1..confirm+K). K=8/32 robustness, bukan kill |
| Partisi data | Hanya R (2023-07-01 s.d. 2024-12-31), stratum A, minus 19 hari anomali |
| Bootstrap real | Day-cluster 10.000 resample, seed 20261006 |
| Placebo | 1000 set per track × 2 track (reversal-track, momentum-track), seed dasar 20261007 (independen dari bootstrap). Trigger acak shared kedua track (NULL_SHARED_TRIGGERS = true) |
| Placebo direction | Reversal-track: pseudo-dir = sign(close_trigger − daily_open), verifikasi di entry. Momentum-track: coin flip 50/50 seeded |
| Placebo extremes | pseudo_spike_high/low = max/min 3 bar trailing (PSEUDO_N = 3). Rumus SL IDENTIK dengan real |
| Minimum hari ber-event / total event | 30 / 30 |
| FDR | BH q=0.10 global atas core {Sel 1, Sel 2, Sel 3, Sel 4a1t, Sel 4a1s}. Sensitivitas {4a2t, 4a2s, 4b1t, 4b1s, 4b2t, 4b2s}: p nominal saja. 4a1 pooled TIDAK diuji (diganti split — hindari double-count) |
| Daily open hours | [22, 23] |
| Power rule | n < 30 ATAU lebar CI95 mean net_pnl_pip > 5 pip (POWER_CI_PIP = 5; ~2× edge minimum 2,85) → UNDERPOWERED. CI win-rate (>25 pp) pendukung saja |
| Statistik primer | Mean net P&L per event dalam pip (termasuk timeout di-MTM, dikurangi biaya) |
| Aturan advance | Core LOLOS ≥ 1 → TV-01 (klaim yang dibawa = hipotesis yang LOLOS; bila hanya Sel 1 → hipotesis cadangan "reversal pasca-spike umum", AMD-full UNTESTED). Hanya-sensitivitas LOLOS → eksploratori, TIDAK advance. Semua core gagal → GUGUR |
| Label kejujuran | Sel 3 < 30 → "TIDAK TAHU" (hipotesis AMD-full BELUM TERUJI — bukan kegagalan). Sel 1 LOLOS → "edge lemah terdeteksi" |
| Venue & segel | TV-01 walk-forward di V (2025, 259 hari); FS-01 terkunci di V; ANN-01 train R, validasi V, test P. P PRISTINE — disentuh tepat sekali (test final ANN-01). Hierarki: R discovery-terkunci · V workhorse validasi · P segel |

**Jangkar waktu:** s = bar terakhir spike sequence; r = bar touch RSI dalam s+1..s+6 (Sel exhaustion, tanpa r = bukan trigger); trigger = r (exhaustion) atau s (momentum); confirm = trigger+1; entry = close(confirm); window = confirm+1..confirm+K.

**LOLOS:** LOLOS = (real mean > persentil 97,5 null track yang sesuai — null regime-matched per sel) DAN (lolos FDR untuk core / p nominal < 0,10 untuk sensitivitas).

## BAGIAN 1 — PRE-FLIGHT CHECKLIST (gate keras, laporan sebelum coding)

- **Cek 1 (trace positif):** 1 hari R — jam bar pertama (22/23 UTC) → daily open → OR_top/OR_bottom → spike ≤ 8 jam pertama (sequence, s = bar ke-berapa) → r (RSI touch s+berapa) → konfirmasi r+1 → entry/TP/SL → sentuhan pertama → label. Ambigu → STOP.
- **Cek 2 (trace negatif):** hari spike tanpa balasan, lacak penuh, pastikan tidak ada yang hilang.
- **Cek 3 (partisi):** max(utc) < 2025-01-01; nol broker_day anomali; hari ≈ 384 (drop open-abnormal ≈ 0 pasca-A1); bar M15 ekspektasi 30.000–42.000 (dari terukur 2024: 23.909/tahun). STOP hanya jika < 20.000 atau > 60.000.
- **Cek 4 (dry-run funnel, tanpa first-passage):** total bar → spike → exhaustion → sideways makro (SIDEWAYS_D1, ambang P25 dilaporkan) → akumulasi mikro (ambang P50 dilaporkan) → filter waktu → pre-filter biaya → side-check → Sel 1/2/3 + split rezim momentum (4a1t/4a1s, dst.). Gate: Sel 1 (basis) < 30 → STOP UNDERPOWERED. Sel 2/Sel 3 < 30 → drop + label ("TIDAK TAHU" untuk Sel 3), LANJUT Sel 1. Varian 0 event → drop dari uji.
- **Cek 5 (grep):** 0.95, 2.85, 16, 30, [22, 23], 20261006, 20261007, 5, 1000.
- **Cek 6 (runtime placeholder):** placebo 10 set dulu, ekstrapolasi ke 1000×2 track. > 10 menit → optimize (numba) dulu.
- **Diagnostik (dicatat, aturan tidak diubah):** atrisi pre-filter per posisi bar (bar 5–10 vs 11–32). Bukti pertama jika Sel 3 underpowered.

## BAGIAN 2 — ALUR SEL

### Sel 1: Setup, Kontrak, Assertion
Load R + stratum A. Assert max(utc) < '2025-01-01'. Assert nol broker_day anomali.

### Sel 2: Daily Open & Indikator
Daily open = open bar pertama broker_day, broadcast. Assertion open-abnormal: anomaly_rate (first-bar hour ∉ [22,23]) > 5% → RuntimeError; else drop hari abnormal, lanjut. Indikator: ATR_M15(14).shift(1); ATR_D1(14) dari D1 closed (nilai hari sebelumnya); RSI(14) Wilder/ewm tanpa shift. Komentar seed: 20261007 ≠ 20261006 = dua proses acak independen.

### Sel 3: Fitur Kontinu & Anatomi
body_ratio, wick_up, wick_down; rolling percentile window 500 (~5 hari, regime lokal). pre_i_size (range pip bar trigger−i) + pre_i_dir (+1/−1/0), i=1..10. dist_to_daily_open (pip).

### Sel 4: Operasionalisasi Hipotesis
- **OR:** 4 bar M15 pertama setelah daily open. Trigger ≥ bar ke-5.
- **Makro sideways (D1-based):** SIDEWAYS_D1 := d1_range_5 (max high − min low 5 D1 closed) < P25(d1_range_5/atr_d1 atas trigger). Ambang dihitung di dry-run Cek 4, dilaporkan. TRENDING_D1 := komplemen (label "non-sideways (trending/ekspansi)").
- **Mikro akumulasi (basis OR/ATR):** 12 bar pre-spike: box_range_12 < P50(box/ATR atas trigger lolos makro) DAN jarak maks 12 close ke batas OR terdekat < P50(dist/ATR yang sama). Ambang dry-run, dilaporkan.
- **Spike sequence (dua arah eksplisit):** threshold di Bar1 (>2,0×ATR; varian longgar >1,5×ATR). Bar 2–3 opsional jika close lebih ekstrem searah spike_dir. spike_high = max(high) SELURUH sequence; spike_low = min(low) SELURUH sequence. s = bar terakhir.
- **Exhaustion (Sel 1,2,3 — nested: Sel 1 basis; Sel 2 = Sel 1 + SIDEWAYS_D1; Sel 3 = Sel 2 + mikro):** r = bar pertama s+1..s+6 dengan RSI ≥70/≤30. Tanpa r = bukan trigger.
- **Momentum:** 4a1: Bar1 >2,0×ATR + RSI(bar pertama) 40–55 (primer). 4a2: sama + RSI(s). 4b1/4b2: threshold 1,5×ATR. Tiap sel diuji ganda rezim: sufiks t (hari TRENDING_D1), sufiks s (hari SIDEWAYS_D1) → 4a1t/4a1s, 4a2t/4a2s, 4b1t/4b1s, 4b2t/4b2s. Varian 0-event = insight; <30 event = drop dari uji, lapor terpisah.
- **Filter waktu:** trigger dalam 32 bar pertama sejak daily open.
- **Pre-filter biaya:** |close_trigger − daily_open_price| > 2,85 pip.

### Sel 5: Konfirmasi & Labeling
1. Konfirmasi di confirm = trigger+1. Reversal: warna confirm berlawanan spike_dir. Momentum: close_confirm melampaui close_trigger searah spike. Gagal → label −1 ('confirmation_failed'). Stop.
2. Entry = close_confirm. Reversal: TP = daily_open_price; SL sell = max(entry+1,0×ATR, spike_high+0,5); SL buy = min(entry−1,0×ATR, spike_low−0,5). Momentum: TP = entry±1,5×ATR; SL = entry∓1,0×ATR.
3. Post-filter: Net TP = |entry−TP| − 0,95 < 2,85 → skip 'cost_too_low' (semua sel). R:R = Net TP/|entry−SL| < 1,0 → skip 'rr_too_low' (MOMENTUM SAJA; reversal catat rr_value tanpa gugur).
4. **Side-consistency REVERSAL:** SELL wajib entry > daily_open; BUY wajib entry < daily_open. Langgar → label −1 ('wrong_side').
5. First-passage K=16: confirm+1..confirm+16, high/low intra-bar. Label 1 (TP dulu) / 0 (SL dulu) / 2 (timeout).
6. net_pnl_pip: win/loss dari TP/SL minus 0,95; timeout = P&L bertanda di close confirm+K minus 0,95. Win-rate = L1/(L1+L0); timeout_share terpisah.
7. skip_reason: None / 'confirmation_failed' / 'rr_too_low' / 'cost_too_low' / 'pre_filter_cost' / 'wrong_side'. Non-None → label −1 (audit filter, keluar inferensi).
8. Dedup per-spike: cooldown 16 bar dari s. Satu spike → satu baris per sel lolos (kolom sel_name, termasuk sufiks t/s) + overlap_with + is_first_spike_of_day.

### Sel 6: Inferensi Statistik
1. Bootstrap real day-cluster 10.000x → CI95 mean net_pnl_pip (lapor + power rule).
2. Placebo per track (1000 set): trigger uniform 32 bar pertama tiap hari ber-event (jumlah = trigger nyata, min 1; SHARED kedua track). Reversal-track: pseudo-dir = sign(close_trigger−O), verifikasi sign(entry−O), beda → drop 'wrong_side'; TP = open; SL rumus identik via pseudo extremes. Momentum-track: pseudo-dir coin flip; TP = entry±1,5ATR. Mean per set → null per track; null tiap sel dibatasi pada trigger placebo yang memenuhi predikat rezim sel tersebut (regime-matched).
3. p_sel = (1+#{null ≥ real})/1001 → FDR BH q=0,10 atas {1,2,3,4a1t,4a1s}. Sensitivitas {4a2t,4a2s,4b1t,4b1s,4b2t,4b2s} p nominal. <30 event → drop, "statistik tidak viable" ("TIDAK TAHU" untuk Sel 3).
4. LOLOS core = null-beat DAN FDR-pass. Sensitivitas = null-beat DAN p<0,10 (eksploratori). K=8/32 robustness. Catatan nested-test wajib. Kill: semua core gagal → gugur; ≥1 core LOLOS → TV-01 di V (klaim yang dibawa = hipotesis yang LOLOS — bila hanya Sel 1: "reversal pasca-spike umum", AMD-full UNTESTED).

### Sel 7: Handoff
Kolom: utc, daily_open_price, or_top, or_bottom, atr14, rsi14, rsi_bar1, rsi_at_s, spike_dir, spike_high, spike_low, trigger_bar, confirm_bar, entry_price, tp_price, sl_price, rr_value, net_pnl_pip, label_final, skip_reason, sel_name, overlap_with, is_first_spike_of_day, pre_1_size..10_size/dir, is_confirmed_color (reversal: warna lawan; momentum: searah), is_confirmed_breakout (momentum: confirm lewati extreme; reversal: False/tidak berlaku). Kolom placebo: null_track, pseudo_dir. Disclaimer: OR = 4 bar setelah open; window setelah entry; timeout MTM; placebo 1000 set×2 track; split momentum t/s; null regime-matched; R:R tak gugurkan reversal; biaya flat 0,95. Venue: EDA-06 di R; TV-01 walk-forward di V; FS-01 terkunci di V; ANN-01 train R, validasi V, test P (P pristine, satu sentuh).

## BAGIAN 3 — INSTRUKSI CODER
Pre-Flight + laporan dulu. Jangan ubah: 0.95, 2.85, 16, 30, [22, 23], seed 20261006/20261007, power 5 pip, placebo 1000×2 track, FDR core {1,2,3,4a1t,4a1s}, PSEUDO_N=3, NULL_SHARED_TRIGGERS, aturan persentil P25 (makro) / P50 (mikro), venue TV-01:V / FS-01:V / P SEGEL. Anti look-ahead: trigger ≤ close trigger_bar; konfirmasi/entry bar berikut; outcome setelah entry. spike_high/low = SELURUH sequence. Assertion crash disengaja, biarkan crash. NaN drop + lapor, nol imputasi. Stream + parquet sebelum TV-01. Cek 6 runtime dulu. Error/ambigu → STOP, jangan improvisasi. 2026/P JANGAN disentuh.

## BAGIAN 4 — CONSISTENCY CHECK (wajib di akhir)
Cetak + assert: COST_DRAG_PIP==0.95, MIN_NET_TP_PIP==2.85, MIN_RR_RATIO==1.0 (RR_SCOPE=="momentum"), K_PRIMARY==16, PARTISI 2023-07-01..2024-12-31, MIN_DAYS==30, MIN_EVENTS==30, DAILY_OPEN_HOURS==[22,23], POWER_CI_PIP==5, N_PLACEBO==1000, NULL_TRACKS==2, NULL_SHARED_TRIGGERS==true, FDR_CORE=={1,2,3,4a1t,4a1s}, SIDEWAYS_DEF=="P25(d1_range_5/atr_d1)", MICRO_DEF=="P50(box,dist)", VENUE=="TV-01:V,FS-01:V,P:SEALED", PSEUDO_N==3, OR_DEF=="4 bar setelah daily open".

## RIWAYAT PERUBAHAN (v9.3 → v9.4 = Amandemen-1 dilebur)
1. A1: jam open [21,22] → [22,23] di 6 titik (kontrak, Cek 1, Cek 5, Sel 2, BAGIAN 3, consistency). Bukti ganda: audit DST `data.yaml:271-281` + ukuran coder 255@22/129@23/0@21.
2. A2a: nesting Sel 1/2/3 didefinisikan (tutup lubang F3): Sel 3 ⊂ Sel 2 ⊂ Sel 1.
3. A2b: makro 1,5× mati → SIDEWAYS_D1 P25 (dry-run, dilaporkan); TRENDING_D1 = komplemen (label jujur).
4. A2c: mikro 0,5/0,25 mustahil → P50 ganda (dry-run, dilaporkan).
5. A2d: split momentum seragam (t/s); core {1,2,3,4a1t,4a1s}; 4a1 pooled dihapus dari core.
6. A2e: null regime-matched per sel (klarifikasi "null track yang sesuai").
7. Gate Cek 4 direvisi: STOP hanya jika Sel 1 < 30; Sel 2/3 < 30 → drop + label, lanjut.
8. A3: label "TIDAK TAHU" (Sel 3), "edge lemah" (Sel 1), hipotesis cadangan "reversal pasca-spike umum", AMD-full UNTESTED.
9. A4 (modifikasi user): TV-01 walk-forward V; FS-01 terkunci V; P SEGEL pristine satu-sentuh; hierarki R/V/P.

STATUS: FINAL v9.4 — dokumen kanonik tunggal. Koder: pakai file ini; v9.3 + Amandemen-1 arsip riwayat. Jalankan Pre-Flight ulang terhadap angka v9.4, lalu LANGKAH 2. Tidak ada iterasi blueprint lagi.
