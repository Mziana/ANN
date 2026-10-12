# Perintah Coder L3-0: Peta Arah 153 G3-Pass + 98 LOLOS (paste-manual)

Peran: Coder. Tugas: fase deskriptif L3-0 (mandat S3-1 spec Lapisan 3):
baca arah 153 baris G3-pass + peta 98 LOLOS ke arah + irisan.
TANPA model, TANPA latih, TANPA skor, TANPA null. BUKAN arsitek
(DILARANG ubah ambang/aturan), BUKAN auditor. Workdir: D:\ANN.
Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (S5 format laporan, S8A anti-looping),
   reports/governance/2026-10-12/arsitek/spesifikasi-lapisan3.md
   (S3-0 s/d S3-5 MENGIKAT), reports/governance/2026-10-12/arsitek/
   putusan-eda07-audit.md (A-1 s/d A-7), putusan-eda07-i2.md (C3-invers).
2. Patuh AGENTS.md penuh: reuse-first (pola _build_eda07*.py dipakai
   ulang, baca CSV beku, DILARANG hitung ulang strata/base),
   tanpa dependensi baru, tanpa tulis ke configs/src/data, tanpa
   commit/push, tanpa klaim tanpa bukti.
3. Setiap syarat berpasangan perintah mentah + output di laporan.
   Klaim tanpa output mentah = GAGAL (tulis eksplisit).
4. Bila bertentangan dengan spec/vonis terkunci, STOP dan laporkan;
   jangan improvisasi.

## S5 Tugas (batas L3-0, DILARANG melampaui)

1. Input BEKU saja (baca, jangan tulis ulang):
   reports/eda/2026-10-12/T-07-3_lift.csv (1315 baris, 153 G3=True),
   T-07-2 (verdict 98 LOLOS / 162 GUGUR), T-06-7 irisan,
   _gate_G2_alarm.csv. Hash input SEBELUM vs SESUDAH = sama.
2. Output di reports/eda/2026-10-12/:
   (a) T-L3-0_arah.csv = PERSIS 153 baris G3-pass (target, fitur,
   lift, CI, tanda +/-, irisan); (b) T-L3-0_peta98.csv = 98 pasangan
   LOLOS x arah dominan + irisan; (c) FIG-17 peta arah (pos/neg per
   sesi x horizon); (d) notebook eda_07_l30_arah.ipynb tereksekusi
   0 error + sel kesimpulan 1 paragraf; (e) builder
   scripts/_build_eda07_l30.py (ASCII/LF/tail-LF).
3. Assert mesin (log-then-assert, tulis bukti ke disk SEBELUM assert):
   153 baris tepat + split 120 positif / 33 negatif; 5 Tokyo kandidat
   hadir SEMUA bertanda negatif (nilai C3: -0,0473/-0,0549/-0,7446/
   -0,0279/-1,5868); 2 London kandidat ABSEN dari set G3-pass
   (GUGUR G3, CI memuat 0); 98 peta = 98 LOLOS tepat; 24/24 konstanta
   nol drift vs run 9; balance/registry bila menyentuh.
4. Runner-log (stdout/stderr + exit code) WAJIB disimpan sebagai
   artefak di folder tanggal run (S3-4, tutup T-2). Detached bila
   >30 menit (pola run 9/I-2, timeout >= 5400).
5. Serahkan laporan S5: file + tabel Klaim & Bukti + yang belum
   diverifikasi + potensi masalah. Tanpa vonis model, tanpa klaim
   edge, tanpa buka L3-1 (itu wewenang arsitek pasca-audit L3-0).

## Perintah mentah wajib

- Hash builder + notebook SESUDAH tulis terakhir + baris/byte.
- Hash input beku SEBELUM vs SESUDAH = sama (tempel kedua output).
- Isi T-L3-0_arah.csv (wc -l + head) + hitung split +/- independen.
- Bukti 5 Tokyo negatif + 2 London absen (grep + output).
- Bukti 98 peta vs 98 LOLOS (diff himpunan, harus KOSONG).
- Bukti runner-log tersimpan + exit code.
- git status --porcelain=v1 + git rev-parse HEAD (nol stage ronde ini).
- Cek ASCII/LF/tail-LF builder (perintah + output).
- DILARANG imbauan umum. Klaim tanpa output mentah = GAGAL.

## S8A diingatkan

Ronde ini berakhir dengan TABEL ARAH (go/no-go pasangan ke L3-1),
bukan dengan usulan investigasi baru. Selesai = peta arah terkunci.
