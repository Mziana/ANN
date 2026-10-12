# Brief Re-audit Auditor EDA-06 (paste-manual, FINAL, siap paste ke auditor)

Peran: Auditor. Tugas: verifikasi independen hasil coder EDA-06.
DILARANG menulis kode produksi; DILARANG mengubah builder/notebook/data.
Workdir: D:\ANN. Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (S18 template audit, S5 format laporan),
   thoughts/shared/designs/2026-10-10-eda06-eksekusi-design.md,
   reports/eda/2026-10-10/laporan-coder-eda06.md,
   .ai/assistant/verifications/2026-10-10_gerbang-hasil-eda06.md.
2. Kerja dari NOL: hitung ulang dari parquet + config, jangan impor kode
   coder sebagai kebenaran. Harness bila perlu di %TEMP%\eda06_audit
   (di luar repo), interpreter venv kanonik.
3. Setiap syarat berpasangan perintah mentah + output ditempel. Klaim tanpa
   output mentah = GAGAL (tulis eksplisit).
4. Vonis terkunci (H1/H2/H3/H5/H4b/R-2 GUGUR, H4 TAHAN) tidak dinilai ulang;
   temukan bila laporan menyelamatkan hipotesis gugur.

## A1-A7 (cakupan audit, semua wajib)

- A1 Replikasi: pilih minimal 3 tabel penentu (T-06-1a spread sesi,
  T-06-4 grid p* satu sel, T-06-5a preset 50/70 satu sesi) dan hitung ulang
  dari parquet 2023-2025; nyatakan COCOK/bit-exact atau selisih digit.
- A2 Anti look-ahead: verifikasi ATR M5(14) hanya dari bar selesai
  (merge backward utc+1mnt) + uji hitung-ulang parsial; verifikasi barrier
  hanya memakai bar SESUDAH entry; laporkan pelanggaran bila ada.
- A3 Holdout + universe: buktikan 2026 nol bar (termasuk bar tepi hari
  broker), B = 185.248 terpisah dari K2, C dibuang, tanpa Off di A.
- A4 Scope: notebook 27 sel VERBATIM vs referensi (terima perbedaan bungkus
  builder; tolak perubahan logika/angka); FIG-08..12 + 14 CSV lengkap dan
  konsisten dengan output notebook.
- A5 Gerbang: hitung ulang K1-K4 per irisan dari CSV + definisi kontrak;
  verifikasi funnel 32 -> 23 -> 23 -> 23 dan LOLOS 23+7; nilai apakah K4
  benar mencegah barrier raksasa lolos semu.
- A6 Determinisme + mutu: jalankan ulang pytest yang diklaim (254) +
  ruff/format/foreign_chars builder; putuskan status 14 temuan ruff
  notebook (terima GAGAL-dengan-sebab hanya bila memang pra-ada referensi).
- A7 Integritas: S0 hash (builder fab369e6, notebook dd0f229d, 2 referensi),
  HEAD b18992b, staged/nol-commit; satu-satunya tulis = laporan ini.

## Larangan

1. DILARANG menulis kode ke repo; DILARANG commit/push/stage.
2. DILARANG memakai 2026, mengubah ambang K1-K4, atau menambah irisan.
3. DILARANG mengklaim edge tradable; verdict audit = LULUS / LULUS DENGAN
   CATATAN / GAGAL atas temuan, bukan vonis strategi.
4. DILARANG mengutip file internal asisten di luar repo sebagai bukti utama;
   bukti = artefak repo + output mentah.

## Output

- reports/governance/2026-10-10/Audit/reaudit-eda06.md (tanpa self-hash;
  ASCII/LF/tail-LF): verdict + A1-A7 + temuan (HIGH/MEDIUM/LOW) + eskalasi
  bila ada + laporan pola AGENTS.md S5 (Klaim & Bukti + output mentah).
- STOP; berikut putusan arsitek EDA-07 (di luar ronde ini).
