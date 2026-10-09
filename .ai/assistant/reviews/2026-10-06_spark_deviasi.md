# Review Spark — Ringkasan Sederhana (2026-10-06)

Sumber: `reports/governance/2026-10-06/decisions/eda_review_deviations_v1.md`.
Diterjemahkan Asisten (chat) untuk user.

## Verdict
- INVALID 9 (D1, D2, D4, D5, D6, D7, D8, D9, D10): temuan coder sah, wajib fix.
- VALID 1 (D11): kekhawatiran coder sah, desain menyerap, catat saja, tanpa ubah kode.
- PARTIAL 2 (D3, D12): separuh benar.

## Keputusan khusus
- D2: Ljung-Box tetap ditegakkan, dengan aturan baca khusus (p tak menyimpulkan; Q/n + besaran).
- D11: interpretasi coder sah; preregistrasi utuh, tidak diubah.
- D12: marker wajib minimal (fix Tokyo, NYSE, zona BoJ); event-study = scope creep, skip.

## Urutan perbaikan
1. D8 rename + catat D11
2. Batch nb03: D2/D4 + D1/D3 + D5 → rerun
3. nb04: D6/D7 + BoJ → rerun
4. nb02: D10 + flag fix/NYSE → rerun sel
5. D9 rename figure
6. Update audit → DUA commit (A: nb04; B: koreksi). DILARANG amend e4efbfd.
7. nb05 baru setelah commit koreksi.

## Dampak nb03
Hasil provisional; kualifikasi hampir pasti berubah; A-vs-B + lag 21–60 = info baru.
Besaran perubahan tidak diklaim (butuh komputasi ulang).
