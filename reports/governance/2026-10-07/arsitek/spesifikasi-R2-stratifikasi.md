# Spesifikasi Pra-Registrasi -- R-2 Stratifikasi Tahun H4

**Peran penulis:** Arsitek (AGENTS.md S26: merancang; DILARANG tulis
kode produksi/data/config; DILARANG commit/push). **Status:**
PRA-REGISTRASI -- dikunci SEBELUM eksekusi coder; penyimpangan = STOP.
**Tanggal lock:** 2026-10-09. **Dasar:** disposisi fondasi-B D-2
(R-2 DIBUKA); putusan Batch-2 P-5; putusan H4b V-4 (anti-merambat).
**Bukan vonis:** DILARANG memvonis H4/H5 di sini; vonis = putusan
terpisah sesudah re-audit. H5 tak tersentuh; H1/H2/H3 FINAL; H6 nihil.
**Aturan besi:** tiap klaim angka WAJIB output mentah (S5/S20); tanpa itu = GAGAL.

---

## S0. Gerbang sesi arsitek (8/8 COCOK + HEAD + staged 2 T6)

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spec-B2
f06a8e27b916172f5824438acd545614360d3b57  hasil-B2
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit-B2
e02a203b96879d73e90339f2d78a37d15834a23a  putusan-B2 (H4 TAHAN FINAL)
ed436fddf607d3629fa226fd34d20ff60bf47232  protokol-B (218 baris)
0284f5f022ce1c147cefef6dd7780aded6acf820  hasil-B (416 baris)
7d125022cd14113325e5c5721da53a39be661f5c  disposisi-B (D-1--D-4)
fe11383b9bdd1e58819e32812eec75c52ab3aee9  putusan-H4b (GUGUR)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD (staged: build_labels.py + test_build_labels.py)
```
Tanpa commit/push/stash/checkout oleh sesi ini. Mismatch = STOP.

---

## S-V. Verifikasi arsitek (sebelum R-2)

(a) Empat bahan S2 dibaca UTUH: putusan-B2 410/410 (termasuk celah
:121-157), hasil-B2 penuh ([O6]/[O8]/[O13]/[O14]), disposisi-B (D-1--D-4),
putusan-H4b (V-1--V-4 + ESK-1). Bukan ringkasan.
(b) Angka diekstraksi sesi ini dari JSON mentah: INKLUSI pool
`0.014399999999998407`/3114; 2024 `0.04834999999999022`/1560; 2025
`-0.005049999999992838`/1554 (`membalik_tanda: False`); n_Off 0/0;
top6 pool `[14,13,0,15,12,1]`; H4b Maju `-0.005049999999992838`/1554
vs Mundur `0.05439999999999045`/1560; trio-sha `b1b69d33`/`7a7f5ee7`;
porsi biaya `0.014621990418018331`; 6/6 sha parquet cocok. Digit-per-digit cocok.
(c) Tidak run-ulang -- diputus per butir: tiga rekaman sepakat penuh
(JSON coder, replikasi auditor, bacaan langsung saya); S27 tak terpicu;
direktori arsitek `%TEMP%` baru TIDAK dibuat (nol klaim baru di spec ini).
(d) Tanpa probe baru: NOL klaim empiris baru; ESK-1 dikutip dari putusan-H4b
ter-hash (2024/2025 n_Off=0; 2023 2894 bar jam 21 UTC).

---

## R2. Pertanyaan + lock verbatim (DIPUTUS, mengikat)

**Pertanyaan tunggal:** "Apakah efek H4 stabil antar-tahun bila pool
2024-2025 dipecah stratifikasi tahun pada jam tetap lock?"

**Lock R-2 verbatim -- GUGUR bila pada SATU PUN tahun-uji (2024, 2025):
median EV-after-cost tahun <= 0. TAHAN hanya bila KEDUA tahun:
median EV > 0. Tanpa TAK-MENENTUKAN.**

**Alasan OR-gugur (U-3, opsi default):** sejajar lock H4b ("satu pun"
cukup); mencegah tahun-negatif disembunyikan pool; tanpa angka/ambang baru
selain pemecahan strata yang D-2 izinkan. Kriteria (a) n_Off DIBEKUKAN
non-penentu (alasan tertulis): ESK-1 sah (inoperatif struktural 2024-2025,
n_Off 0/0); dilaporkan deskriptif per tahun; DILARANG menentukan vonis.

**Jendela + anti-intip:** evaluasi = date_broker 2024-01-01..2025-12-31
dipecah 2024 vs 2025 (pool tunggal DILARANG sebagai penentu). 2023 =
seed/history SAJA (H4 tanpa pemakaian). 2026 dikecualikan PENUH (offset
belum terverifikasi). Jam uji = jam tetap lock `[14,13,0,15,12,7]`;
DILARANG top-6 per tahun sebagai penentu (hour-shopping); DILARANG shopping-jendela.

**Keterbatasan jujur:** R-2 termotivasi EKS-3; bobot konfirmatori terbatas;
GUGUR(R-2) BUKAN retak H4 Batch-2; TAHAN(R-2) BUKAN klaim kebal (P-5 dua arah mengikat).

---

## Input beku (sha di-assert SEBELUM hitung, mismatch = STOP)

- M1 2024/2025 sha `69b2c026...`/`fce65a3a...`; M15 store `cd6a85e4...`;
  D4 labels `47d15c41...`. Mesin S-H4 Batch-2: ATR T-1, SL 1xATR, TP 2xATR,
  biaya by_session (Off->0.65 x pip 0.01), fill exact, join-gate posisional.
  NOL konstanta diubah. Varian default INKLUSI; karantina F-1 5 hari counter
  deskriptif per tahun (DILARANG eksklusi lain, diputus fondasi-B D-1).

---

## Prosedur (stratifikasi, satu mesin, tanpa intip)

1. Pool EV HANYA pada 6 jam tetap lock, pecah 2024 vs 2025 (ATR T-1 beku,
   biaya by_session, fill exact, time-stop close terakhir hari-T).
2. Per tahun: n trade, median + mean EV, fraksi positif, exit-cause
   (SL/TP/time_stop), n_Off deskriptif (definisi Off beku).
3. Assert: loop entry HANYA `FIXED_HOURS` lock (GAGAL bila tersentuh data);
   grain hari-broker tunggal (`utc.normalize()` DILARANG).
4. Determinisme: coder 2x (sha256 identik) + auditor replikasi dari nol;
   seed/toolchain/venv diumumkan.

---

## Gate coder + deliverable (C1-C9 ringkas, mengikat)

- C1 HEAD tetap; C2 nol tulis lindung (AFTER==BEFORE + find kosong);
  C3 hash beku + 4 sha + cost by_session nilai-per-nilai; C4 pytest + ruff
  (rc + cakupan) + foreign-chars (rc=0, LF-only, ASCII); C5 2x (sha + cmp
  IDENTIK + toolchain); C6/C7 R-2 selesai + diputus mekanis; C8 pengikatan
  eksternal (TANPA self-hash; hash di kanal luar); C9 staged/nol commit/HEAD tetap.
- Harness HANYA `%TEMP%\opencode\r2\` (`r2.py` -> `r2_hasil.json` + log);
  venv kanonik `D:\ANN\venv\Scripts\python.exe` (py3.12.8).
  DILARANG tulis `src/`/`configs/`/`data/`; DILARANG `main()` di jalur eksekusi.
- Laporan `coder/hasil-R2-stratifikasi.md`: Klaim & Bukti, output mentah per
  tahun, hash artefak, self-audit 3x, STOP. Tanpa vonis arsitek.

---

## Larangan S-B eksplisit (mengikat coder + auditor)

B1 tanpa vonis di dokumen hasil; B2 tanpa filter regime/sub-sel/ambang/window
pasca-hoc penentu; B3 tanpa ubah lock/ambang/vonis Batch-2/fondasi-B/H4b tanpa
addendum BARU; B4 tanpa H6; B5 tanpa `utc.normalize()`/rekonstruksi UTC; B6 tanpa
guard nilai-vs-diri; B7 tanpa fixture seragam klaim sensitif / test tanpa assertion;
B8 tanpa output parsial berlabel penuh / klaim "diuji via X" + "belum ada test X";
B9 tanpa kutip tanpa verifikasi / naik severity tertutup; B10 provenans terpisah +
sabotase ke jalur produksi; B11 gate format sebut rc+cakupan, byte-identik sebut
toolchain; B12 konstanta kalibrasi dikunci test (mutasi tanpa hitung-ulang = merah).

---

## Aturan baca TERTUTUP

1. Terapkan lock R-2 verbatim; tepat satu vonis: **GUGUR(R-2)** / **TAHAN(R-2)**.
2. GUGUR = tak stabil antar-tahun (satu tahun gagal cukup); DILARANG merembet
   ke TAHAN(H4 Batch-2); DILARANG tafsir-ulang via sub-sel/ambang.
3. TAHAN = stabil pada split 2024/2025 jam-tetap; DILARANG dibaca kebal umum.
4. Tanpa statistik tambahan; tanpa H5; tanpa kalibrasi; tanpa H6.

## Self-audit 3x (sebelum STOP)

P1 Correctness: S0 8/8 + S-V(a)-(d) + lock verbatim pada angka bacaan-sendiri.
P2 Bias: ambang tak disetel agar vonis bagus; EKS-3 dicatat bukan disembunyikan.
P3 Meta: lock Batch-2/fondasi-B/H4b utuh; ruang coder/auditor tak diambil; STOP menutup.

STOP. Spec terkunci; menunggu ronde coder.
