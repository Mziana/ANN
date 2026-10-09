# Konfirmasi R1/R2/R3 - adendum atas re-audit F-2/F-3/F-4

Tanggal 2026-10-07. Sifat: konfirmasi residual MEDIUM, bukan audit baru; tidak ada
probe berat, dan F-1, B1, EDA, angka lama, serta vonis lama tidak dibuka.

Artefak: `src/features/build_features.py` `399e64b372e430b6def79b4fa8324a4e8e629918`
(400 baris); `tests/test_build_features.py` `ed7ac43520c4431519d4d7065504866ae9b3ad95`
(357 baris); parquet M15 `07402f40478aaed9391203f5db3237d636f5a959` (tak berubah).
Klaim coder cocok: test 35 -> 37 (+2 di `TestDailyMetrics`, keduanya test F-4).

## Konfirmasi

**R1 - YA.** Benar secara konstruksi: `intraday` dari `bars_m1` =
`prepare_bars(m1, "M1", ...)` dicetak sebagai M1, `daily_bars` dari `bars_m15` =
`prepare_bars(m15, "M15", ...)` dicetak sebagai M15. Spot-check independen saya,
dua hari broker tidak bersebelahan (2023-02-01, 2025-06-12) dihapus dari M1:
ground truth M1=972/M15=974, pesan keluar `M1 972, M15 974` - cocok.

**R2 - YA.** `grep` + baca baris 321-334: `BELUM DIUJI` (1 hit) ada tepat pada
kalimat materialitas H1/H5 dan menyebutnya "hanya catatan audit, bukan bukti uji";
p95 `+0.28%` dan maks `+1.06%` verbatim berdampingan dengan median `+0.019%`.

**R3 - YA.** Uji mutasi saya sendiri: guard 249-253 dicabut dari salinan temp
(400 -> 395 baris), `pytest` di pohon temp, `conftest` membuktikan yang diimpor
adalah salinan itu (`PROBE_HAS_GUARD=False`). Hasil `1 failed, 36 passed`; gagalnya
tepat `test_imbalance_m1_m15_raises` dengan `DID NOT RAISE`. Kontrol: `37 passed`.

## Residual tetap berdiri

Dicatat, bukan diadili ulang: #4 nol test memanggil `main()` (F-3); #5 `return 0`
hardcoded tanpa branch gagal; #7 budget 400/400 dan 50/50, headroom nol, pemecahan
B2 wajib. Ketiganya tidak terkait R1/R2/R3. Koreksi "R4/R5/R7 tidak ada" dari
coder saya catat sah: residual tidak gugur karena tidak disebut.

## Self-audit

Ketiga YA tertaut eksekusi/grep sendiri: R1 ke `c1_r1_spot.py` plus rantai
`prepare_bars` -> `groupby` -> f-string; R2 ke `grep` dan baca baris 321-334 tanpa
eksekusi karena tekstual; R3 ke `c3_r3_mutasi_kuat.py` dengan bukti import. Hash
diambil ulang setelah probe, sumber tetap `399e64b3`, tidak ada file produksi berubah.
