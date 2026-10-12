# Brief Eksekusi Coder EDA-06 (paste-manual, FINAL, siap paste ke coder)

Peran: Coder. Tugas: port + eksekusi EDA-06 gerbang biaya. BUKAN arsitek
(tidak merancang ulang), BUKAN auditor (tidak menilai vonis lama).
Workdir: D:\ANN. Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (kontrak kerja, S5 format laporan),
   thoughts/shared/designs/2026-10-10-eda06-eksekusi-design.md (scope beku),
   thoughts/shared/references/eda06/EDA_06_07_rancangan.md (bagian 0-2),
   thoughts/shared/references/eda06/eda_06_biaya_breakeven.ipynb (substansi
   VERBATIM, sumber tunggal logika).
2. Patuh AGENTS.md penuh: reuse-first (pola scripts/_build_eda05.py +
   notebooks/scalping/_eda_common.py), tanpa dependensi baru, tanpa tulis
   ke configs/src/data, tanpa commit/push, tanpa klaim tanpa bukti.
3. Setiap syarat di bawah berpasangan perintah mentah + output ditempel di
   laporan. Klaim tanpa output mentah = GAGAL (tulis eksplisit).
4. Bila instruksi bertentangan dengan vonis terkunci
   (H1/H2/H3/H5/H4b/R-2 GUGUR, H4 TAHAN) atau dengan kontrak notebook
   (sel KONTRAK_06), STOP dan laporkan konflik; jangan improvisasi.

## S5 Tugas (substansi VERBATIM dari referensi, tidak diringkas ulang)

1. Tulis scripts/_build_eda06.py (generator + executor nbconvert, pola
   _build_eda05.py): template notebook = sel referensi VERBATIM per sel
   (markdown + kode), tanpa mengubah angka/logika (YEARS 2023-2025,
   HOLDOUT 2026-01-01, STRIDE 5, HORIZON 120, FIXED_COMBOS 50/70-30/45-
   100/140, ATR_K 0,75/1,0/1,5, ATR_RR 1,0/1,4/2,0, N_DIRECTION 5/15/30/60,
   SLIPPAGE 0,0/0,1/0,3, K1 3,0/5,0pp, K2 >= 4/5 semester, K3 n >= 1000 dan
   hari >= 100, K4 p_none <= 50%, N_BOOT 1000, seed 20261010).
2. Generate + eksekusi notebooks/scalping/eda_06_biaya_breakeven.ipynb
   dari atas ke bawah sampai 0 error, urutan terbukti. Venv kanonik
   (pandas 2.x, tzdata 2026.5); fingerprint sesi = EXPECTED_FINGERPRINT
   (assert keras); PROJECT_ROOT via pyproject.toml + src/.
3. Keluarkan T-06-1a..1d, 2a, 2b, 3, 4 (A + B terpisah), 5a..5f, 6, 7a, 7b
   sebagai teks di output notebook + CSV di satu lokasi
   (reports/eda/2026-10-06/figures/ ATAU reports/eda/2026-10-10/,
   pilih satu, catat), dan FIG-08..12 sekuensial (DILARANG pakai ulang
   FIG-01..07). Registry figures diverifikasi tepat FIG-01..akhir.
4. Pertahankan uji bawaan referensi: ATR 12 timestamp hitung-ulang identik;
   simulator vektor vs naif 400 entri x 2 sisi identik; asersi B = 185.248,
   A+B+C utuh, tanpa Off di A, tanpa 2026, sidik jari cocok.
5. Hitung gerbang K1-K4 per irisan (144 tercile + 48 sesi), cetak jumlah
   irisan diuji + lolos tiap tahap (K1 saja, K1&K2, K1&K2&K3, semua+K4),
   dan verdict eksplisit GAGAL/LOLOS + rekomendasi irisan (LOLOS bukan
   bukti edge, hanya izin fokus EDA-07).
6. Serahkan laporan pola AGENTS.md S5: file dibuat/diubah + apa dilakukan +
   tabel Klaim & Bukti (TERVERIFIKASI/BELUM DIVERIFIKASI/ASUMSI) +
   yang belum diverifikasi + potensi masalah + rekomendasi.

## Perintah mentah wajib (tiap syarat berpasangan output ditempel)

- Klaim file ada + ukuran: tempel output
  git hash-object scripts/_build_eda06.py +
  notebooks/scalping/eda_06_biaya_breakeven.ipynb SESUDAH tulis terakhir
  + baris/byte tiap file.
- Klaim referensi tak diubah: tempel output
  git hash-object thoughts/shared/references/eda06/eda_06_biaya_breakeven.ipynb
  (harus 6a6c6516bc96e7e9a7845a13b1909927cc718e75) +
  git hash-object thoughts/shared/references/eda06/EDA_06_07_rancangan.md
  (harus 6724c37ec5493b821d0179d0d00768fbd343a485).
- Klaim tanpa commit/stage oleh ronde ini: tempel output
  git status --porcelain=v1 + git rev-parse HEAD.
- Klaim ASCII/LF-only/tail-LF untuk builder: tempel output cek non-ASCII +
  CRLF + byte terakhir (perintah + output, bukan ringkasan).
- Klaim notebook tereksekusi penuh: tempel output eksekusi (urutan sel +
  0 error) + daftar FIG + daftar CSV tersimpan.
- Klaim angka: tiap angka penentu (B = 185.248, semester A = 5, verdict,
  irisan lolos) menyebut sel notebook + artefak CSV + sha bila ada.
- DILARANG imbauan umum ("pastikan hash benar"). Klaim tanpa output
  mentah = GAGAL (tulis eksplisit).

## Larangan bentuk-spesifik ronde ini

1. DILARANG mengubah logika/angka referensi (ambang, stride, horizon,
   kombinasi, seed) setelah melihat hasil; ubah HANYA sebelum run pertama
   atas perintah user, tercatat di sel parameter.
2. DILARANG memuat data 2026 dalam bentuk apa pun (termasuk bar tepi hari
   broker >= 2026-01-01); DILARANG memakai 2026 sebagai penentu.
3. DILARANG menghitung B (H1-2023) pada kriteria K2; B hanya pembanding
   terpisah (T-06-4b, T-06-5f).
4. DILARANG menambah label, fitur, model, baseline, backtest, atau P&L/equity
   sebagai klaim pada ronde ini.
5. DILARANG menambah dependensi (sklearn/numba DILARANG); hanya pandas,
   numpy, scipy, matplotlib yang sudah ada.
6. DILARANG menulis ke configs/src/data; DILARANG commit/push; DILARANG tulis
   governance selain laporan tugas.
7. DILARANG mengubah/menafsir-ulang vonis H1-H5/H4b/R-2 atau definisi sesi/Off.
8. DILARANG pointer ke file internal asisten di luar repo; brief ini mandiri.

## SELF-AUDIT 3x ADVERSARIAL (wajib di laporan)

Putaran 1 Correctness: tiap sel sama dengan referensi (diff hanya bungkus
builder)? holdout 2026 nol bar? B = 185.248? fingerprint cocok? ATR 12/12
identik? simulator 400x2 identik? FIG-08..12 sekuensial? CSV 14 tabel ada?
Putaran 2 Bias: ada ambang yang digeser pasca-hoc? ada B yang bocor ke K2?
ada 2026 yang dipakai memilih? ada delta kecil yang diklaim sebagai edge?
ada irisan sekunder yang dipromosikan diam-diam?
Putaran 3 Meta-check: file hanya builder + notebook di lokasi kanonis?
referensi tak tersentuh (2 hash cocok)? format ASCII/LF builder? nol
commit/push? nol vonis baru? nol tulis governance selain laporan?
