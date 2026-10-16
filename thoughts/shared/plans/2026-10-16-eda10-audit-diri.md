# Audit-diri adversarial EDA-10 (3 ronde, 2026-10-16)

> Target: `thoughts/shared/plans/2026-10-16-eda10-volume-c-V-draf.md` (FINAL,
> 180 baris). Metode: serang berulang — Ronde 1 angka-vs-disk, Ronde 2
> konsistensi + eksekutabilitas, Ronde 3 adversarial penuh. Status tiap
> klaim: TERVERIFIKASI / GAGAL / BELUM. Temuan: H (gagal-eksekusi /
> vonis-salah bila dibiarkan), M (lubang spesifikasi), L (presisi).
> NOL patch diterapkan — FINAL terkunci, temuan menunggu putusan user.

## Ronde 1 — angka-oracle vs disk (sumber: REPORT EDA-09 + builder + manifest)

| Oracle di draf EDA-10 | Sumber disk | Hasil |
|---|---|---|
| Nunik-V = 1110 | REPORT L169 "UNIQ-V=1110 di 259 hari" | TERVERIFIKASI |
| Band unik 367/286/168/289 | REPORT L155 | TERVERIFIKASI |
| Full-room 325/269/156/268 | REPORT L155 + manifest `band_V` | TERVERIFIKASI |
| n-V = 1018 | REPORT L213 + manifest `n_V` | TERVERIFIKASI |
| med 1.179, IQR [0.914,1.607], P1/P99 0.503/4.396 | REPORT L213 | TERVERIFIKASI |
| Baseline 1018/1018, drop 0 | REPORT L213 | TERVERIFIKASI |
| 259 hari / 23812 bar / fill 1.0000 | REPORT L152–153 | TERVERIFIKASI |
| Warmup-R 87 event, n-vol-R 1427 | REPORT L214 (warisan EDA-08, rantai-sitasi) | TERVERIFIKASI (rantai, bukan ukur-ulang) |
| Toolchain 1.26.4/2.2.3/17.0.0 | manifest `toolchain` (terbaca 66 baris) | TERVERIFIKASI |
| Parquet hash B800E50E…BDFC2 | REPORT L130–134 + verifikasi Commander | TERVERIFIKASI |
| "20 hari-bersih" (bukan kalender) | builder L670 `MANIFEST_ALL = MANIFEST_R + MANIFEST_V` (keduanya daftar hari-bersih) + L684 `past20` atasnya | TERVERIFIKASI — wording draf BENAR |

Kesimpulan Ronde 1: oracle solid. Tak ada angka-beku yang salah.

## Ronde 2 — konsistensi internal + eksekutabilitas (baca kode-beku)

- **H1 — §3 memerintahkan hal yang mematahkan F0'.** Draf L56:
  "volume-(c) tak butuh ATR/RSI; JANGAN hitung yang tak dipakai." Fakta
  kode: `scan_spikes` MEMBACA `g["atr"]` (builder L352–356, syarat
  `H−L > thresh*atr`) dan `g["rsi"]` (L377+); kolom itu dihitung pada
  frame concat 2023+2024+2025 (L260–261, L306–309). Re-detect verbatim
  (F0') TANPA indikator = KeyError/crash; coder yang improvisasi =
  deviasi-tak-teregistrasi. Premis "tak dipakai" SALAH — yang tak
  memakai indikator adalah fungsi volume, BUKAN deteksi. Perbaikan:
  §3 wajibkan hitung concat-indikator verbatim (reuse sel-3 EDA-09)
  sebagai prasyarat scan, sama seperti EDA-09. Butuh amandemen
  sebelum eksekusi — F0' tak bisa hijau apa adanya.
- **M2 — teks spesifikasi belum mandiri (3 lubang).** (a) F3'(b) L89
  mengklaim perlakuan bar-tanpa-tick "DITETAPKAN di sini" — tetapi §2/§3
  tak menetapkan aturan apa pun (dangling). Rekomendasi konservatif:
  bila fill < 1.0 pada bar mana pun → catat + STOP + arsitek (tak ada
  preseden → jangan karang aturan). (b) Agregasi med/IQR tak
  didefinisikan di teks (median atas rasio SEMUA event-V — ada di kode
  L700, tak ada di spesifikasi; teks keluaran §8 harus mandiri).
  (c) Semantik MANIFEST/clean-day tak disitir di teks (benar di kode,
  L670 — tulis eksplisit agar resep-tekkunci dapat dibaca tanpa kode).
- **L1 — langkah whitelist-V tak disebut di F0'.** EDA-09: whitelist
  sesudah deteksi (REPORT L169). Coder reuse-verbatim tetap benar, tapi
  spesifikasi haru
...[truncated 2700 chars]
