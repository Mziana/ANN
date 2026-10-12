# Putusan Arsitek Audit L3-0: LOLOS Diterima, L3-1 DIBUKA (2026-10-12)

Peran: Arsitek (rangkap asisten atas perintah user 2026-10-10).
Status: MENGIKAT. Spec S3-0..S3-5 + S8A tetap utuh.

## B-1 LOLOS PROSEDURAL DITERIMA, L3-0 TERTUTUP

8 mandat nol selisih, verdict independen 98/162 identik, 0 TINGGI/
0 MENENGAH. Ronde L3-0 selesai (eksekusi + reaudit).

## B-2 Disposisi temuan (mengikat untuk L3-1)

- T-1: manifest L3-1 WAJIB kolom path relatif-root.
- T-2: redaksi baku K24 = "transcription-guard, dikonfirmasi
  independen 24/24 vs source run 9; bukan bukti komputasi".
- T-3/T-4: hitungan baris/assert diverifikasi mesin, bukan manual.
- T-5 (watch-item -> PAGAR MENGIKAT): 4 target Tokyo berarah pos
  via rv60/atr_m5 (lift 0,4162/11,9112/0,2722/19,3823) + 2 London
  (13,8349/14,1417) = magnitudo-volatilitas. DILARANG memakai
  angka-angka itu sebagai bukti/presumsi prediktabilitas di L3-1.
  CSV L3-1 WAJIB kolom punya_round_d_invers (bool). M3 memutus
  untuk semua pasangan tanpa pengecualian; lift besar bukan
  tiket lolos.
- T-6: runner-log via redirect langsung, bukan Tee-Object.

## B-3 L3-1 DIBUKA dengan pra-registrasi M2 (ditutup di sini)

Pasangan terdaftar (M1 arah diketahui semua): 98 native peta98
+ 5 Tokyo round_d (neg) = MAKSIMAL 103. Tanpa tambahan.

- Model (baseline): prediktor laju-marginal per target-iris
  (P = proporsi train pada irisan target itu).
- Null: mayoritas-kelas train global per target.
- Metrik (SATU): Brier score; sekunder akurasi (syarat perlu).
- Split waktu: train 2023H2+2024H1+2024H2, test 2025H1+2025H2.
  Tanpa shuffle lintas batas. Deterministik; bootstrap CI saja
  boleh RNG dengan seed terkunci SEEDL31 = 31001/31002.
- M3 menang IFF: (a) Brier_model < Brier_null - 0,001 pada test
  pooled, DAN (b) Brier_model < Brier_null pada MASING-MASING
  2025H1 dan 2025H2, DAN (c) akurasi_model >= akurasi_null pada
  test pooled. Gagal satu = GUGUR permanen ronde ini.
- Label per-bar = konstruksi verbatim run 9 (reuse _eda_common +
  kode label run 9; DILARANG definisi label baru).
- DILARANG pindai ambang/fitur/split di luar yang didaftarkan di
  sini. DILARANG generalisasi sesi. DILARANG P&L/backtest/edge.

## B-4 Vonis pasca-L3-1 (diingatkan S8A, mengikat arsitek sendiri)

Setelah reaudit L3-1, vonis biner tanpa ronde lanjutan:
(a) ada yang lolos M3 -> minta persetujuan user untuk spec
pemodelan (BUKAN paper-trade; marginal-rate bukan sinyal);
(b) nol yang lolos -> pendekatan scalping-TF pada irisan ini
MATI, keputusan pivot/berhenti eksplisit bersama user.

Berikutnya: brief coder L3-1 (eksekusi B-3 persis).
