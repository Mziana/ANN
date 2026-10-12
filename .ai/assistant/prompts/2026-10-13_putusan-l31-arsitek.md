# Prompt vonis B-4 arsitek (vonis dagang biner atas TABEL M3 L3-1) -- FINAL, siap paste -- 2026-10-13

## Konteks (fakta, bukan instruksi)

Ronde coder L3-1 + re-audit independen SELESAI, keduanya gerbang
LOLOS sebagai dokumen sah. Keluaran mekanis lock (BUKAN vonis
resmi): **TABEL M3 103 pasangan = LOLOS 68 / GUGUR 35**
(diskret 56/11 via Brier margin 0,001 + menang H1&H2 + akurasi;
kontinu 12/24 via MSE 1% + menang per-semester + MAE).
Per-jenis: LB_bin 25/0, LC1 7/2, LC2 13/6, LD 11/3, LB_rng 12/24.
Margin ada headroom (Brier min 3,06x ambang; MSE min 11,2x
ambang). Konjungsi mengikat (29 GUGUR lolos (a) tapi gagal
(b)/(c)). Verdict audit: **LOLOS PROSEDURAL** -- 11 mandat
(a)-(k) nol selisih; 0 TINGGI/0 MENENGAH/4 RENDAH format-nol-dampak/
4 INFORMATIF; S6 jujur 6 butir. Tugasmu: VONIS BINER B-4
(keputusan dagang, S8A) + disposisi 4 RENDAH + kunci anti-merambat.
Verifikasi S-V WAJIB -- bukan vonis buta di atas ringkasan.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

- Kamu ARSITEK (kontrak bersama `.ai/AGENTS.md` S26-S27, S8A):
  merancang + memutus konflik + tie-break. DILARANG menulis/
  mengubah kode produksi, data, config.
- Kamu BUKAN coder, BUKAN auditor, BUKAN asisten. Namun verifikasi
  S-V di bawah WAJIB -- kamu memutus HANYA atas bahan yang kamu
  periksa sendiri.
- Workdir: `D:\ANN`. Interpreter verifikasi: `venv/Scripts/python.exe`
  (py3.12.8).

## S-2d. Gerbang hash (ukur sesi ini SEBELUM satu butir pun diputus)

Tempel output mentah perintah berikut SESUDAH pembacaan terakhir
(klaim tanpa output mentah = gagal):

```
git hash-object reports/governance/2026-10-12/arsitek/spesifikasi-lapisan3.md
git hash-object reports/governance/2026-10-12/arsitek/putusan-l30-audit.md
git hash-object reports/governance/2026-10-12/arsitek/amandemen-l31-metrik.md
git hash-object reports/eda/2026-10-12/laporan-coder-eda07-l31.md
git hash-object reports/governance/2026-10-12/Audit/reaudit-l31.md
git rev-parse HEAD
git status --porcelain=v1
```

Nilai rujukan (mismatch = STOP, bukan vonis):

```
d166d189aa0834c66b81ea89ac0bcfa8e7b1b3e7  spesifikasi-lapisan3.md
23c5fdf80e00619a0a06cd017b7cb978b71fa933  putusan-l30-audit.md (B-1..B-4 + T-1..T-6)
1921326dc4bb25b1277662c267edbc2916ed0e58  amandemen-l31-metrik.md (C-1..C-4)
b6a40abd4928720d0f78f1af65bd91680af08b65  laporan-coder-eda07-l31.md
36dbad57a7b1ddbdc6d7b296069df8e16b1c606d  reaudit-l31.md (452 baris / 24728 B)
b18992b5e57d45c125aacf3ca868c2f9e135d9d1  HEAD (tak bergerak)
staged NOL ronde ini
```

## S-V. Butir vonis (WAJIB verifikasi + putus satu per satu)

- **V-1 vonis biner B-4.** TABEL M3 LOLOS 68 -> cabang (a):
  (i) tetapkan status tabel (sah dipakai / tidak); (ii) putuskan
  GO (minta persetujuan user untuk spec pemodelan, S8A butir 3)
  atau NO-GO (pendekatan mati di sini + pivot/berhenti eksplisit).
  Marginal-rate BUKAN sinyal (koreksi B-4 mengikat): GO tidak
  berarti paper-trade. Vonis TEPAT SATU, tanpa cabang ganda.
- **V-2 daftar LOLOS-per-jenis.** Sahkan/ubah daftar S7 audit
  sebagai register beku pemodelan (atau tutup sebagian jenis).
  68 LOLOS bukan 68 tiket trade.
- **V-3 disposisi R1-R4.** Tetapkan nasib 4 RENDAH (aplikasi ronde
  berikut: T-6 encoding log, redaksi verbatim+display, hash ganda
  pra+pasca normalisasi, kolom `cocok` jujur) + 4 INFORMATIF
  (tanpa CI; tanpa re-eksekusi run 9; konjungsi mengikat; `arah`
  kembaran beda by-design) sebagai catatan putusan mengikat.
- **V-4 pagar T-5 + S8A.** Tegaskan kembali: lift besar rv60/atr_m5
  tetap BUKAN presumi lolos (2 London-GUGUR sebagai bukti); ronde
  investigasi tambahan DILARANG atas inisiatif AI.

## S3. Keluaran

Tulis `reports/governance/2026-10-12/arsitek/putusan-l31-final.md`:
V-1 (tepat satu) + V-2 + V-3 + V-4 + STOP. Tanpa P&L/backtest/edge.
Lapor S5 (file + hash + tabel Klaim & Bukti). STOP setelah
serah-terima (S8A). Tanpa vonis = ronde BELUM selesai.
