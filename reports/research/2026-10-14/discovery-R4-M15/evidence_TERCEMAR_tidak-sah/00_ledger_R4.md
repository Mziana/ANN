# Ledger R4-M15 (hipotesis skala waktu) — 2026-10-14

Pra-registrasi: `reports/governance/2026-10-14/arsitek/spesifikasi-discovery-R4-M15.md`
(ditulis SEBELUM data 2024 dibuka). Bed: 2024-holdout. 2025/2026 tidak disentuh.

## Konstruksi M15

Resample bucket UTC-15min dari `data/processed/M1/usdjpy_m1_2024.parquet`
(358.331 bar). Syarat bucket penuh 15/15 (151 parsial dibuang = gap).
Hasil 23.758 bar M15, kontiguitas 98,61%. Gap >60 mnt = pola harian
broker (break 21:59→23:00) + weekend — normal, tanpa jendela anomali baru.
Spread per bar = max spread bucket (KONSERVATIF; +~0,2–0,4 pip vs metode R2,
dicatat jujur, tak mengubah orde vonis). Spread 2024: med 0,60 / p95 1,20.
Sesi: sidik `_eda_common` LOLOS (definisi sama dengan R2).

## Penyimpangan terdokumentasi dari resep R2 (disengaja, pra-registrasi)

- ATR barrier H1 (analog 5x TF, bukan M5). Ketersediaan 87,5%.
- Race TERMASUK bar entry t0+1 (koreksi audit 2026-10-14).
- Gerbang kapasitas: n_eval >= 30 (bukan 300; sampel M15 ~15x lebih kecil).
- Shadow pair kaki-B per event (matriks joint + ekskursi berpasangan).

## Hasil (detail: summary.json; event: events_eval.parquet)

8/8 sel TOLAK di syarat-(i): median net_obs negatif di semua sel,
kaki-A maupun kaki-B.

- E1 pooled (n=1.551): A WR 14,3% med ≈ −3,2 / B WR 16,2% med ≈ −1,2..−2,5.
- E2 (n=5.478): A WR 16,1% med −2,19 / B WR 13,7% med −1,82.
- E3 (n=108, lolos min-n): A WR 23,5% (8 TP) med −0,91 / B WR 10,3% med −5,04.

Shadow: joint TPTP = 0 di SEMUA sel (keduanya TP tak pernah ko-okur);
pasangan decisif terbelah nyaris rata sisi-sinyal vs cermin; selisih
berpasangan (A−B) median ≈ 0 dengan share positif 47–55% (koin);
mfe sisi-CERMIN ≥ sisi-sinyal di semua sel (0,20–0,25R vs 0,19–0,30R).
MFE≥1R hanya 3–8% event. Bar pertama med −1,9..−2,9 pip net.

## Vonis

H-R4 DITOLAK di bed 2024. Pola E1/E2/E3 gagal di dua skala waktu (M1 dan
M15); kebutaan-arah berlaku di keduanya. Forward 2025 BATAL (tak ada
kandidat untuk di-forward; 2025 tetap terkunci untuk ronde lain).
