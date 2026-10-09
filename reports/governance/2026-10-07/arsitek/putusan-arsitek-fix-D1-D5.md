# Putusan Arsitek Fix D1–D5 — Q1–Q4 atas Re-audit Adversarial — 2026-10-07

**Peran:** Arsitek. Tanpa kode. Tanpa vonis H4/H5.
**Dasar:** `Audit/reaudit-adversarial-D1-D5.md` (vonis GAGAL, temuan #14–#19,
syarat blocking 1–9 — dokumen ini menang atas ringkasan bila berselisih),
`rencana-B2-fase0.md` (kontrak), `hipotesis_lock_v1.md` (ambang),
`putusan-arsitek-H1-H5.md` (S1–S8), putusan B1 (D0 + 4 butir), putusan F-1.
**Berdiri, jangan dibongkar:** ambang H1 0,0268/88,79; karantina 19 hari
(1748/90041 terverifikasi); impor satu arah; anggaran baris; hash file lama;
9/9 prohibisi.

---

## Q1 — Ambang RV H3: pilih (a)

**Putusan: opsi (a).** `NotImplementedError` dicabut dan diganti flag hidup
hasil prosedur kalibrasi terkunci di bawah. Opsi (b) ditolak: menunda flag
berarti D4 gagal lagi dengan pola yang sama (parquet tanpa kolom RV =
deliverable tak-kontrak), dan audit sudah menyatakan penentuan ambang RV
sebagai prasyarat arsitek ("Pasca pemblokiran 1-7").

**Redaksi S3 verbatim** (wajib dikutip coder kata-per-kata,
sumber `putusan-arsitek-H1-H5.md:15-16):

> S3: AUC = kalibrasi in-sample span terkunci, bukan klaim OOS.

**Formula dan span mengikat coder kata-per-kata:**

> `rv_score` = `rv_roll_20d` / 20 (mean harian; store tetap sum per B1-4).
> `rv_regime_flag` = 1[`rv_score` > TAU_2023]. TAU_2023 = ambang Youden
> (maksimum sensitivitas + spesifisitas − 1) dari ROC `rv_score` versus
> label-periode pada span kalibrasi terkunci 2023-01-01..2023-12-31, dengan
> label B = broker-day dalam 2023-01-01..2023-06-30 dan label A = broker-day
> dalam 2023-07-01..2023-12-31. Hari tanpa `rv_roll_20d` penuh (warmup NaN)
> dikecualikan dari kalibrasi dan berflag NaN — DILARANG default False.
> AUC yang dilaporkan = AUC in-sample span tersebut; DILARANG klaim OOS.
> DILARANG mengkalibrasi ulang pada span lain. DILARANG memilih ambang dari
> performa OOS. Nilai TAU_2023 + AUC + n per kelas wajib tertulis di protokol
> sebagai hasil kalibrasi, bukan sebagai ambang lock.

Dasar: lock memberi basis orde (`rv_day` B 3,648e-5 vs A 2,292e-5) tetapi
tidak memberi angka ambang — prosedur di atas melengkapi S3 menurut
istilahnya sendiri (kalibrasi in-sample), bukan menggeser lock. Titik-tengah
dari median data DITOLAK sebagai ambang (surga-dari-data; protokol L89-92
yang memuat 3,648e-5/20 sebagai calon ambang DIBUANG dan diganti prosedur
ini). Tahun 2023 adalah satu-satunya tahun kalender yang memuat kedua
strata, dan batasnya adalah definisi kalender H1 (bukan dari data).

## Q2 — Kolom close hilang: pilih (b)

**Putusan: opsi (b).** Drift dihitung dari parquet M15 sumber langsung per
doktrin D0, tanpa menyentuh store B1. Opsi (a) ditolak: menambah OHLC ke
store berarti hash parquet baru + re-audit B1 parsial + pemecahan file
400/400 — biaya arsitektur tanpa pembenar, karena kebutuhan drift adalah
kebutuhan bar-grain yang menurut D0 (preseden B1-1/B1-2: spread M1 untuk H5,
M5 untuk H2) DILAYANI via baca-langsung parquet sumber. Opsi (c) ditolak:
store tidak memuat satu pun level harga (baca `FEATURE_COLUMNS` audit
D1-#14) — setiap "formula pengganti" dari kolom yang ada = menggeser lock
§H1 ("drift berarah RELATIF M15 4 jam pertama London").

**Instruksi eksplisit ke coder (konsekuensi hash/anggaran/audit):**
hash `399e64b3`, `ed7ac435`, `07402f40` TETAP (nol sentuh file lama);
anggaran tak bergerak; tanpa re-audit B1. Alur data kontrak:
`compute_london_drift_4h` menerima frame M15 sumber (via `load_processed`
reuse) + `daily`; jendela = 16 bar `is_london` paling awal per broker-day
(BLOKIR jendela `hour_utc` 8–12 — temuan #15: 60,6% hari berbeda);
formula = close bar-terakhir − open bar-pertama dari 16 bar kontrak
(satuan harga) + kolom kedua `london_drift_norm` = drift / `atr_14_d1`(t−1)
dengan pernyataan `assert` paritas satuan yang NYATA di kode (bukan komentar
— syarat blocking 2, temuan #14). Kedua kolom hidup di frame label grain-hari
(lihat Q4), BUKAN di store.

## Q3 — m1_bars hilang: pilih (a)

**Putusan: opsi (a).** `compute_gap_f2_flag` membaca M15 sumber langsung per
D0 (kolom `m1_bars` ada di parquet M15 terproses — fakta skema, bukan
inferensi). Opsi diam-all-False SUDAH DIVETO auditor (false negative
senyap, HIGH #15) dan tidak tersedia. Opsi (b) ditolak: gagal-keras
meninggalkan D4 tak-kontrak untuk kedua kalinya padahal datanya tersedia di
sumber. Opsi (c) ditolak: mengeluarkan kolom berarti mengamandemen kontrak
Fase 0 §2 + membiarkan residual F-2 #2 terbuka permanen — ditolak.

**Instruksi eksplisit ke coder:** bucket parsial = `m1_bars` < 15 DAN bukan
bucket pertama/terakhir hari-broker (mid-day; bucket batas parsial oleh
konstruksi); `gap_f2_flag` hari = 1 bila ≥1 bucket mid-day parsial, else 0,
NaN DILARANG, default-senyap DILARANG. Target verifikasi: tepat 234 hari
(angka reaudit F-2) — selisih = gagal. Status BELUM DIUJI di protokol
dipertahankan sampai uji sensitivitas klasifikasi H1 pada 234 hari itu ada;
eksklusi buta TETAP DILARANG (24% sampel).

## Q4 — Redaksi kutipan + /20 + atribusi

**(i) Redaksi S3–S6 verbatim** (sumber `putusan-arsitek-H1-H5.md:15-21,
wajib dikutip coder kata-per-kata, masing-masing dengan tag sumbernya):

> S3 (H1-H5:15-16): AUC = kalibrasi in-sample span terkunci, bukan klaim OOS.
> S4 (H1-H5:16-17): uji drawdown vs strategi diagnostik L3 pertama; filter
> DILARANG aktif sebelum S4 dievaluasi.
> S5 (H1-H5:18-19): EV memakai 6 jam tetap [14,13,0,15,12,7] + `cost_basis`
> fragmen 4b; uji pola OOS memakai 6 jam teratas hitung-ulang; dicatat
> terpisah.
> S6 (H1-H5:20-21): wajib lapor jumlah sel; klaim sel mana pun wajib koreksi
> multiplicity bernama (atau replikasi independen); tanpa itu = eksplorasi.

**(ii) Transformasi /20 DIPERTAHANKAN sebagai transformasi label.**
Dasar eksplisit: store memegang sum (B1-4 verbatim,
`build_features.py:261` `.rolling(20,min_periods=20).sum()` — tanpa /20,
TETAP); lock §H3 memberi basis dalam orde `rv_day` (mean harian); /20
mengubah sum→mean agar komparabel dengan basis lock. /20 hidup di LABEL
(`rv_score`, lihat Q1), BUKAN di store. Redaksi wajib di protokol dan
docstring: "`rv_score` = `rv_roll_20d` / 20 (mean, turunan label; store
tetap sum per B1-4)" — menyebut hasil-bagi sebagai "sum" = gagal
(temuan #18). Kontradiksi L85/L86 ditutup dengan redaksi ini.

**(iii) Atribusi yang dibenarkan:** S4 ← `putusan-arsitek-H1-H5.md:16-17`
(L144 protokol yang menunjuk lock §H3 SALAH — lock tidak memuat label S4);
larangan vonis H4/H5 ← `putusan-arsitek-H1-H5.md:18-21` (L156 protokol yang
menunjuk F-1 butir 2 SALAH — F-1 hanya mengatur mekanisme karantina + garis
B2). Kutipan S1–S6 tanpa merujuk `putusan-arsitek-H1-H5.md` = gagal
(temuan #17: dokumen itu dikutip 0 kali).

**Perbaikan D3 turunan (wajib dalam batch fix yang sama):** pindahkan D3 ke
`reports/governance/2026-10-07/` (blocking 6); perbaiki typo L35
"menggunakanspread"; `register_h2_strategy` wajib membawa "jam 15 UTC",
"1x", dan "satuan harga JPY" dari protokol L18/L26 ke kode (temuan #19);
pisahkan SL (1× `atr_14_d1`, tanpa normalisasi) dari normalisasi drift
harga/harga B1-3 (L27 protokol kontradiktif — B1-3 adalah paritas drift,
bukan ATR); angka 3,648e-5/20 DIBUANG dari protokol kecuali disebut dengan
tag "basis lock §H3, bukan ambang pakai".

---

## Coder BOLEH (batch fix)

1. Menutup syarat blocking auditor 1–9: drift dari M15 sumber + norm + assert
   nyata (1–3); D4 grain-hari dari store produksi bernama kontrak
   `usdjpy_day_labels.parquet` + `usdjpy_h2_trades.parquet`, dua varian
   benar-benar berbeda + tabel selisih (4); S3 + kutipan H1-H5 di protokol
   (5); D3 pindah folder (6); `TestBuktiMutasi` ditulis ulang agar GAGAL pada
   kode rusak + test jendela London + test varian-eksklusi di `main()` + satu
   end-to-end `main()` (7); D5 diisi hash sebenarnya + 213/19 + atribusi ke
   `test_build_labels.py` + hapus konstanta fiktif + koreksi .gitignore (8);
   severity #9→HIGH, #10→BLOCKER (9).
2. Mengimplementasikan Q1(a), Q2(b), Q3(a), Q4 di atas kata-per-kata.
3. `usdjpy_h2_trades.parquet` berisi SPESIFIKASI strategi terdaftar per
   setup (parameter entry/SL/TP/biaya) — kolom hasil (pnl/EV) DILARANG diisi
   di batch ini (pengisian = backtest = butuh persetujuan protokol).

## Coder DILARANG (batch fix)

1. Menyentuh `build_features.py`, `test_build_features.py`, parquet
   `07402f40` (hash TETAP; pelanggaran = gagal total).
2. Menambah kolom ke store; menggeser ambang lock 0,0268/88,79/AUC 0,7;
   menilai ulang angka EDA; membuka H6+; memvonis H4/H5 final.
3. Nilai default senyap dalam bentuk apa pun (all-False/all-True/0/NaN
   yang dibungkam) — setiap yang belum diketahui = gagal keras atau NaN
   eksplisit yang diuji.
4. Ambang dari data evaluasi; kalibrasi ulang TAU di luar span 2023;
   menyebut nilai-data sebagai ambang pakai; klaim tanpa tempelan output;
   commit/stage.
5. Menulis ulang D4 dari data sintetis; dua file byte-identik; nama file di
   luar kontrak; menaruh angka-data ke dokumen terkunci sebagai vonis.
