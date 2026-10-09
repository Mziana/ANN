# Gerbang Pra-Audit — arsitek/putusan-lapisan3-H1H2.md (2026-10-09)

## Klaim serah-terima vs hasil ukur saya

| # | Klaim arsitek | Hasil ukur saya | Status |
|---|---|---|---|
| 1 | Doc hash `ca4e0b70d9dc4272347b74b1ea78d7a5f94593ee` | `git hash-object` → identik 40-hex | COCOK |
| 2 | C8 `9ad9f80588ed66697056e4be8fd7a1f02a72c2aa` | Rekonstruksi git-style → identik (catatan: metode arsitek PowerShell byte-exact, metode saya git-style — keduanya bertemu; konsisten) | COCOK |
| 3 | HEAD `e0b2b9f…` tak berubah; staged 0 | `git rev-parse HEAD` persis; `git diff --cached` kosong | COCOK |
| 4 | Porcelain pola pra-ada | Ukur saya = 99 baris = 98 + doc putusan ini sendiri (untracked). Rantai: 97 (coder) + 1 berkas gerbang saya + 1 doc putusan. Sah, BUKAN temuan | TERJAWAB |
| 5 | ASCII murni, cek asing OK | python: 15615 byte / 296 newline / 0 non-ASCII / tanpa CR | COCOK |
| 6 | Bukti baca S0 (5 hash) | `fc29f6fa` / `1550209f` / `e4143132` / `c643c1c9` / HEAD — semua nilai yang saya pegang cocok; plus catatan jujur 510-vs-511 (tanpa newline akhir, non-material, terbukti oleh hash) | COCOK |

## Silang isi (baca penuh 296 baris)

- P-1: **Vonis resmi H1: GUGUR** (konfirmasi; kriteria i memuat 0, ii p=0.1888; Q1 searah M1, eskalasi=false). Kalimat tunggal dikutip. Benar-pattern.
- P-2: **Vonis resmi H2: GUGUR**, FINAL tanpa menunggu 2026 (3/3 tahun pada jendela OOS terkunci; lock tanpa mekanisme pembalikan; 2026 dikecualikan penuh; ambang 4-tahun kelak = hipotesis BARU). B4-06 diputus eksplisit, tidak digantung.
- P-3: burn-in kanonik = 60 POSISI + skipna default; re-run tidak diperlukan (posisi auditor disetujui); rule ke depan (posisi-vs-nilai + min_periods wajib di spec). Lengkap — butir yang saya minta ada.
- P-4: R-B1 (manifest) / R-B2 (bucket genap) / R-B3 (realitas exit untuk desain H4/H5) / R-B4 (venv kanonik) — masing-masing kalimat + alasan satu paragraf. Panen preseden benar-bentuk.
- P-5: H3 tetap GUGUR; H4/H5 untouched (R-B3 pagar desain, bukan vonis awal — kalimat ini penting dan ada); nol ambang berubah; anti-penyelamatan dua arah; severity lama tetap; S27 tak terpicu.
- Self-audit 3 putaran tertulis; S0.1 (tanpa hitung-ulang ketiga) beralasan + preseden H3 + syarat kapan menjadi wajib. Tanpa celah gantung yang saya temukan.

## Keputusan: LOLOS → Batch-1 TERTUTUP (H1 GUGUR, H2 GUGUR resmi). Berikutnya: desain Batch-2 (H4/H5).
