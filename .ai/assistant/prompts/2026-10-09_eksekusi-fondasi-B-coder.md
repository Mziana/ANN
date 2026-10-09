# Brief coder — Eksekusi protokol telaah fondasi B (U-1–U-3) — 2026-10-09

[SUBSTANSI VERBATIM DARI ARSITEK — `arsitek/protokol-telaah-fondasi-B.md`]

## S0 (konteks hash sesi arsitek — ukur ulang sesimu sendiri sebelum mulai)

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  arsitek/spesifikasi-lapisan3-H4H5.md
f06a8e27b916172f5824438acd545614360d3b57  coder/hasil-lapisan3-H4H5.md
8a4d21090f27dd53555b3a12583ec337819efb2f  Audit/reaudit-lapisan3-H4H5.md
e02a203b96879d73e90339f2d78a37d15834a23a  arsitek/putusan-lapisan3-H4H5.md
ed436fddf607d3629fa226fd34d20ff60bf47232  arsitek/protokol-telaah-fondasi-B.md
```

## U-1(b). Prosedur hitungan varian EKSKLUSI

Input beku: parquet M1 2024-2025 (`69b2c026`/`fce65a3a`), M15 store
(`cd6a85e4`), D4 (`47d15c41`), `ANOMALY_WINDOWS`
(`build_labels.py:53-56`), `quarantine_mask()`
(`build_labels.py:228-242`), konstanta Q3/Q4 spec Batch-2
(identik S-H4: jam tetap, ATR T-1, SL 1x/TP 2x, biaya by_session).
Langkah: (1) bangun ulang pool H4 PERSIS S-H4 (resep `sh4.py`);
(2) varian INKLUSI direplikasi (cek kesamaan median pool
`0.014399999999998407` digit-per-digit — gate kewarasan);
(3) varian EKSKLUSI: buang 5 broker_day karantina dalam-jendela
(`2024-10-28..2024-11-01`) dari pool M1 P1 DAN pool M15 E1,
hitung-ulang top-6 M2 + `n_Off`/any_off/maj_off + median EV pool
+ median per-tahun + n trade; (4) tulis JSON artefak kedua varian
+ tabel selisih digit-per-digit (inklusi vs eksklusi).
DILARANG eksklusi buta di luar 19 hari F-1. DILARANG menukar daftar jam
(larangan Q4 dua arah tetap berlaku pada kedua varian).
Perintah mentah WAJIB ditempel: (i) `grep anomaly_windows`
pada `configs/data.yaml` (blok `:184-198`); (ii) `git hash-object`
tiap artefak JSON yang diklaim; (iii) sha256 tiap parquet yang
dipakai; (iv) cetak 5 tanggal karantina dalam-jendela yang
dibuang + cacah trade terbuang (harus 30).
Aturan baca TERTUTUP: Dilaporkan apakah median 2025 membalik tanda
(negatif → non-negatif) atau tidak; selisih median pool
inklusi-vs-eksklusi angka; `n_Off` kedua varian. **Vonis H4 TETAP
TAHAN apa pun hasilnya.**

## U-2. Dekomposisi biaya H4 + H5

Definisi tunggal: EV JPY = exit − entry − cost_jpy; cost_jpy =
cost_basis.by_session (Off → default 0.65) × pip 0.01; fill exact tanpa
slippage; biaya per sesi London 0,61 / NewYork 0,69 / Tokyo 0,62 /
Sydney 0,8. Kaki bruto per trade = exit − entry; kaki biaya = cost_jpy.
H4: dari 3114 trade pool (`sh4_hasil.json` trio-sha `b1b69d33`), urai
per sesi (London/NewYork/Tokyo/Sydney/Off): n trade, mean/median kaki
bruto, mean/median kaki biaya, mean/median EV, porsi biaya =
mean(kaki biaya) / mean(|kaki bruto|) + porsi terhadap median pool
+0,0144. H5: per sel laporkan cost_basis pip sel +
`mean_spread_pips_m1_bar_event` sel (sudah di JSON `7a7f5ee7`) + rasio
vol/spread M4 lock (London 2,08 / Tokyo 1,60 / NewYork 0,95 /
Sydney 0,80; flag biaya-mendominasi = [NewYork, Sydney]) disandingkan
dengan diff/CI95/p sel (`hasil [O13]`). Tanpa statistik keputusan baru —
tanpa ambang, tanpa uji, tanpa peringkat sel.
Aturan baca TERTUTUP: KUANTIFIKASI headwind biaya, BUKAN jalur
penyelamatan. Keluaran = tabel per-nilai + kalimat "biaya menjelaskan
X dari Y", bukan rekomendasi ubah biaya (by_session beku; S-B.8).

## U-3. Cek regime deskriptif 2024 vs 2025

Deskriptif saja dari data beku (M1 2024-2025, M15 store): per tahun
2024 vs 2025 — spread p95 + mean M1 (kolom `spread_pips` beku), level
RV (kolom store beku), jumlah bar/trade — disandingkan dengan split
tanda H4 (median EV 2024 +0,04835 vs 2025 −0,00505, [O8]). Grain =
`date_broker` store; DILARANG rekonstruksi grain dari UTC
(`utc.normalize()` DILARANG, S-B.12).
Larangan eksplisit (mengikat, putusan H3): DILARANG mengaktifkan
`rv_regime_flag`/`rv_score`/TAU sebagai filter pada data mana pun.
DILARANG kalibrasi-ulang ambang apa pun. DILARANG menambah
kolom/menulis store.
Aturan baca TERTUTUP: SATU dari dua kalimat — "bertepatan" atau
"tidak bertepatan" — deskriptif, tanpa konsekuensi pada H4 TAHAN.

## R-4 (umum)

Semua artefak JSON ronde ini WAJIB ter-hash (`git hash-object`
ditempel) sebelum dibaca arsitek; klaim tanpa output mentah = GAGAL.

## Tugas tulis

Tulis laporan sebagai file .md: `coder/hasil-telaah-fondasi-B.md`
berisi S0 (hash terukur sesimu + tabel Klaim & Bukti) + hasil U-1–U-3
(tabel per-nilai + output mentah ditempel) + kalimat aturan-baca per
butir + self-audit 3× + STOP. DILARANG commit/push. DILARANG
merumuskan H6. DILARANG mengubah vonis H1–H5.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness
Putaran 2 — Bias & Asumsi
Putaran 3 — Meta-check

=== USULAN TAMBAHAN DARI ASISTEN ===

Butuh konfirmasi user (dengan paste brief ini, usulan dianggap disetujui):

1. Lokasi resep S-H4: `sh4.py`/`sh5.py` + JSON trio-sha hidup di
`%TEMP%\opencode\l3h4h5\` (harness Batch-2, luar repo — terverifikasi
asisten 2026-10-09) — BUKAN di repo. Jangan klaim "file tidak ada".
Alasan: coder Batch-2 mengeksekusi dari temp; repo tidak menyimpan
skripnya (risiko rantai-bukti bila temp terhapus — sudah dicatat).

2. Interpreter + goresan: `venv/Scripts/python.exe`; file sementara
hanya di `%TEMP%\opencode\fondasiB\`. Dilarang tulis repo kecuali
satu file laporan di atas.
Alasan: menjaga worktree + pola Batch-2 (S-V arsitek).

3. Gate kewarasan U-1 bersifat BLOKIR: bila replikasi INKLUSI ≠
`0.014399999999998407` digit-per-digit → STOP, laporkan, jangan
lanjut ke EKSKLUSI.
Alasan: tanpa replikasi persis, selisih varian tak bermakna
(pelajaran re-audit: klaim mendahului pengukuran).

4. U-2 H4 memakai `sh4_hasil.json` beku trio-sha `b1b69d33` (verifikasi
sha dulu); DILARANG baca EV dari prosa dokumen (`:1197`/`:1229`
terbukti salah, T1) — hanya dari JSON.
Alasan: mengulang kesalahan sitir-prosa yang sudah divonis T1.

Tunggu konfirmasi sebelum kirim ke AI tujuan.
