# Perintah Coder EDA-07: Terapkan Amandemen G2 + Rerun (paste-manual, FINAL)

Peran: Coder. Tugas: terapkan amandemen G2 revisi + pengerasan eksekusi,
mock smoke, full-run ulang detached, serah-terima S5. BUKAN arsitek
(DILARANG ubah ambang/kriteria selain A-3), BUKAN auditor. Workdir:
D:\ANN. Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (S5 format laporan),
   reports/governance/2026-10-10/arsitek/amandemen-eda07-g2.md
   (MENGIKAT, A-1 s/d A-6),
   reports/governance/2026-10-10/arsitek/spesifikasi-eda07-label-fitur.md
   (S1-S9, kecuali S8-G2 yang diganti A-3),
   reports/eda/2026-10-10/laporan-coder-eda07.md (konteks run C + 8 bugfix).
2. Patuh AGENTS.md penuh: reuse-first, tanpa dependensi baru, tanpa tulis
   ke configs/src/data, tanpa commit/push, tanpa klaim tanpa bukti.
3. Setiap syarat berpasangan perintah mentah + output di laporan.
   Klaim tanpa output mentah = GAGAL (tulis eksplisit).
4. Bila bertentangan dengan vonis terkunci atau KONTRAK_07 (ALARM STOP),
   STOP dan laporkan; jangan improvisasi.

## S5 Tugas

1. Terapkan A-3 pada builder: G2 = G2a (MI pooled vs lantai pooled, n sama)
   DAN G2b (arah lift sama >= 4/5 semester). Evaluator kontrol memakai
   kriteria IDENTIK (baris-per-baris sama). Ambang lain DILARANG berubah;
   buktikan nol drift dengan diff konstanta (tugas 4).
2. Terapkan A-5: log-then-assert (alarm PENUH + tabel skrining + laju
   kontrol pooled ke disk SEBELUM assert), checkpoint CSV per irisan
   selesai, progres fraksi (irisan x/30, tahap) ke file log.
3. Mock smoke sel 15-18 ulang (kode ASLI + data sintetis incl. null murni):
   PASS + rerun bit-identik PASS + pada null murni alarm terkendali
   (tidak boleh 21/62 LOLOS lagi; catat angka barunya).
4. Buktikan nol drift 8 bugfix: diff nilai SEMUA konstanta ambang
   (theta, bin, N_PERM, seed, K-gate, delta) vs run C = identik.
   Satu drift = STOP, laporkan.
5. Full-run ulang detached (Task Scheduler, rantai tunggal, =70-90 mnt):
   sel 01-19 sampai 0 error ATAU STOP pra-registrasi (bila STOP lagi,
   simpan bukti lengkap per A-5 + laporkan, DILARANG bypass).
   Verifikasi registry FIG-01..16 + T-07 bila sampai sel 16-18.
   Hapus task Scheduler setelah selesai.
6. Serahkan laporan S5: file + tabel Klaim & Bukti + yang belum
   diverifikasi + potensi masalah + rekomendasi irisan x label x fitur
   (tanpa vonis, tanpa klaim edge).

## Perintah mentah wajib

- Hash builder + notebook SESUDAH tulis terakhir + baris/byte.
- Diff konstanta ambang vs run C (perintah + output, harus identik).
- Bukti mock: PASS + angka null-murni baru + rerun bit-identik.
- Bukti log-then-assert: path file bukti di disk + cuplikan isi.
- Bukti eksekusi: urutan sel + exit code + daftar FIG/CSV (atau bukti
   STOP + file bukti lengkap bila berhenti di gerbang).
- git status --porcelain=v1 + git rev-parse HEAD (nol stage oleh ronde ini).
- Cek ASCII/LF/tail-LF builder (perintah + output).
- DILARANG imbauan umum. Klaim tanpa output mentah = GAGAL.

## Larangan

1. DILARANG ubah ambang/kriteria selain A-3; DILARANG bypass gerbang.
2. DILARANG model/backtest/P&L/vonis/edge sebagai klaim.
3. DILARANG tulis configs/src/data/governance selain laporan tugas.
4. DILARANG commit/push. DILARANG pointer ke file internal asisten.
