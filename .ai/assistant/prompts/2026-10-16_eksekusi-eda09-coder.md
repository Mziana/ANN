# Brief Eksekusi EDA-09 wick_confirm_V — Coder (2026-10-16)

## Otoritas + PRASYARAT

Satu-satunya otoritas = blueprint FINAL
`thoughts/shared/plans/2026-10-16-eda09-wick-confirm-draf.md` (§§1–15, status
FINAL + Amandemen-1 + Amandemen-2 — dibaca PENUH sebelum menyentuh apa pun; bila brief ini
bertentangan dengan blueprint, blueprint menang — laporkan konflik, jangan
improvisasi). Detail audit-diri arsitek (konteks, BUKAN otoritas):
`thoughts/shared/plans/2026-10-16-eda09-audit-diri.md`.
**PRASYARAT: blueprint sudah FINAL (termasuk Amandemen-2) + perintah
eksekusi-ulang user sudah turun (2026-10-16: "kunci + revert + jalan" —
satu seed, satu run).** Keduanya terpenuhi. Klaim tanpa output mentah = gagal.

## Workdir + disiplin peran (AGENTS.md §26 + §23)

- Workdir = `D:/ANN` (main). DILARANG buat branch/worktree baru — §23:
  tanpa perintah eksplisit user (tidak ada dalam order ini). DILARANG
  commit/push/merge tanpa perintah eksplisit.
- Kamu CODER: implementasi + self-audit + fix. DILARANG memutuskan
  metode/kriteria/ambang (eskalasi lewat user bila ragu). DILARANG audit
  independen pengganti Auditor; yang WAJIB = self-review §4 + self-audit
  klaim (§20-butir-7) sebagai section laporan — FASE 0 (pra-eksekusi) dan
  FASE PASCA (pasca-run/pasca-test), keduanya gerbang (blokir + kelulusan).
- Venv kanonik: `venv/Scripts/python.exe`. DILARANG `.venv/`.
- Builder→notebook: tulis `scripts/_build_eda09_wick_confirm.py`, rerun,
  notebook `notebooks/scalping/eda_09_wick_confirm.ipynb` ter-regenerate.
  DILARANG edit notebook manual. DILARANG mulai dari 0 / rewrite artefak beku
  (reuse-first §16: `scan_spikes`, outcome machine, resep cleaning, fungsi
  tercil disalin verbatim, bukan ditulis ulang).
- Baris vonis mekanis ("CONFIRM"/"GUGUR", §2) dicetak generator; DILARANG
  menarasikan/mengkualifikasi vonis di luar baris itu.

## FASE 0 — SELF-AUDIT PRA-EKSEKUSI (gerbang blokir)

DILARANG menulis/menjalankan generator/notebook SEBELUM fase ini lulus
tertulis. Bukti paham (tulis di laporan, BUKAN sekadar "sudah baca"):
kutip dari blueprint — famili tepat-1 (apa satu-satunya uji + α + arah) +
prosedur cut-lock P3 (fungsi `_tercile_masks` verbatim; assert Amandemen-2:
`round(pooled,4) == 0.1682` + 8 cut SAMA PERSIS §15) + T_DAY + STOP-band
F1/F2 (angka + konsekuensi) + aturan concat-indikator (§3: frame
2023+2024+2025, whitelist sesudah deteksi) + aturan satu-seed + daftar
DILARANG §3 (verbatim pendek).

1. Self-review AGENTS.md §4 (10 butir: baca ulang, bug/edge/None,
   look-ahead, leakage, konvensi, hardcode, duplikasi, test, import;
   tandai keraguan `# REVIEW:`).
2. Self-audit 3×: Correctness (tiap angka yang akan diklaim bersumber
   file:baris/output — tulis sumbernya SEBELUM ada output) · Bias (di mana
   letak godaan HARKing ronde ini? tulis 3 + penangkalnya) · Meta (semua
   syarat §§2–8 blueprint terpetakan ke sel kode apa? file luar scope apa
   yang berisiko tersentuh?).
3. Pasangan perintah mentah (tempel SEMUA output di laporan):
   `ruff check <builder>` (wajib rc=0, sebut rc) +
   `ruff format --check <builder>` (wajib rc=0) +
   `git status --porcelain` (klaim tanpa-stage di luar file kerja).
4. Larangan bentuk-spesifik: DILARANG guard yang membandingkan nilai dengan
   dirinya sendiri (termasuk via kolom turunan frame yang sama) · DILARANG
   merekonstruksi hari dari UTC (grain tunggal hari-broker) · DILARANG
   referensi dibaca dari objek yang sama diperiksa (parquet-R dibaca ulang
   dari disk sebagai referensi terpisah; sebut versi pyarrow/pandas bila
   klaim byte-identik) · DILARANG klaim "sudah diuji" di satu bagian sambil
   "belum ada test" di bagian lain · DILARANG fixture seragam untuk test
   yang mengklaim sensitif-parameter.
5. Hasil FASE 0 = section laporan tersendiri. Gagal = fix + ulangi FASE 0.
   Lolos = baru boleh FASE 1.

## FASE 1 — F0 recovery + cut-lock (fondasi; gagal = STOP)

Parquet EDA-07/08 TAK ADA di disk (`data/processed/events/` hanya berisi
`eda06_candle_events.parquet` — terverifikasi 2026-10-16; gitignored, tak
ikut merge — preseden EDA-08). Recovery BUKAN rescan: jalankan generator
BEKU `scripts/_build_eda07_spike_anatomy.py` apa adanya (SEED_BOOT=20261006,
SEED_NULL=20261007 — JANGAN ubah), verifikasi jangkar bit-identik vs vonis
EDA-07: Nunik=1632, band 515/415/240/462, full-room 1514. Tempel aktual vs
ekspektasi baris-per-baris. Satu pun GAGAL = STOP + lapor (DILARANG
improvisasi/scan manual/"perbaikan" generator beku).
Lanjut: hitung-ulang cut tercil R (t1,t2 × 4 band) dengan fungsi IDENTIK
EDA-08 (`_tercile_masks`: `np.percentile` 100/3, 200/3 — salin verbatim),
assert Amandemen-2: `round(pooled,4) == 0.1682` (literal 1e-9 DITARIK —
cacat spesifikasi, bukan ambangmu untuk ditafsir) + assert 8 cut SAMA
PERSIS dengan §15 (b0 0.24647887323941978/0.47041420118341626; b1
0.1954397394136033/0.3721973094169312; b2 0.1717716422203372/
0.33835948462822907; b3 0.16332011857566983/0.3379338240019312) → bekukan
sebagai konstanta presisi-penuh (catat ke laporan). STOP + arsitek
mendiagnosis bila gagal (bedakan fondasi-goyang vs artefak-numerik —
Amandemen-1 M3).

## FASE 2 — Pre-flight F1/F2/F4 + A-checks (blueprint §6 + Amandemen-1)

Berurutan, STOP + lapor pada gagal pertama (tempel output tiap cek).
F1: hari-V ⊆ 2025, V∩R=∅ (whitelist dua-arah), max(day-V)<2026-01-01;
tick_volume bar-s-V terisi ≥0,95 — ambang dihitung PER BAR-s (= bar
analisis), BUKAN agregat (gagal → volume "tertunda", wick-confirm LANJUT,
DILARANG improvisasi proxy); STOP-band hari <200/>320; sanity bar-M15-V
≈20–28k, STOP-band <13k/>40k. F2: ke-4 band non-kosong + TRIPWIRE DAYA:
total n-V < 500 → STOP (BUKAN GUGUR); grup tercil mana pun (atas/bawah ×
4 band) n < 30 → STOP. F4: seed BARU independen format YYYYMMDD-eksekusi
TERCATAT (tempel nilainya; satu-seed-satu-run — DILARANG re-seed kecuali
bug terbukti + STOP). A1 taksonomi exhaustive; A2 assert EXHAUSTIVE semua
event-V (konvensi `lo_<=x<hi_`), bukan sampling.

## FASE 3 — Build + run

Notebook exit 0 via nbconvert (tempel exit code + jumlah sel/asersi).
Deterministik (rerun = angka sama). T_DAY = 1,7319 KONSTANTA (DILARANG
recompute-P25; assert-vs-EDA-06 dicabut untuk V); cls/ctx = metadata, nol
peran putusan. CONCAT-INDIKATOR (Amandemen-2, §3): ATR14/RSI14 dihitung pada
frame gabungan 2023+2024+2025 (reuse kode loading, tahun diperluas);
whitelist event-V SESUDAH deteksi; event-R yang ikut-terdeteksi =
artefak-terbuang (DILARANG dilapor/diuji/dinarasikan). 2025-only DITOLAK
( = konstruksi baru + butuh-K arbitrer). Assertion mesin tiap pagar: whitelist, V∩R, P-tak-tersentuh,
cut-terkunci teraplikasi, baseline-20-hari penuh per event-V (tidak →
DROP + count). Null = permutasi NILAI wick DALAM band, cut TERKUNCI
diterapkan ulang per permutasi, B=10000, STRATA=BAND, p SATU-ARAH 4
desimal; kerapuhan perbatasan (0,04–0,06) = caveat, BUKAN alasan run-ulang.
CI cluster-per-day B=10000 (karakterisasi, TANPA peran putusan). Per-band +
split-H1/H2 = deskriptif-saja (Δ + n, tanpa p, tanpa klaim; tanda
berlawanan → regime-caveat, VONIS TAK BERUBAH). Volume-(c): baseline
median-rolling-20d/slot-HH:MM TANPA-hari-berjalan (fungsi IDENTIK R;
V-hari-1 = 20 hari-R terakhir); laporkan med/IQR/P1/P99 + cakupan baseline
+ count-drop vs R berdampingan (0 uji, 0 klaim). Kolom first/gap/dow BOLEH
ada sebagai artefak pipeline; DILARANG dilaporkan/diuji/dinarasikan.
Laporan ke `reports/eda/2026-10-16-eda09/` + manifest. Tiap angka bertag
KONFIRMASI-V (angka-R yang dikutip bertag GENERASI-R).

## FASE PASCA — SELF-AUDIT PASCA-RUN/PASCA-TEST (gerbang kelulusan)

DILARANG menulis laporan final SEBELUM fase ini lulus tertulis. Setelah
SEMUA test/assert hijau (tempel output full-suite, BUKAN satu file):

1. Correctness ulang: tiap klaim laporan tunjuk ke output mentah (sel
   notebook / baris log / file:baris). Klaim tanpa pasangan output =
   klaim GAGAL — tulis sebagai BELUM DIVERIFIKASI, jangan dipoles.
2. Bias ulang: label KONFIRMASI-V di tiap angka-V? ada kalimat yang
   membangkitkan first/gap/dow/joint/floor/split-liar? ada p yang
   dibaca sebagai vonis kedua? Tulis hasil periksa per butir (lolos/gagal
   + bukti).
3. Meta ulang: semua syarat §§2–8 + Amandemen-1 terjawab di sel mana?
   file luar scope tersentuh? (`git status --porcelain` ditempel.)
   determinisme rerun dibuktikan? (angka rerun ditempel, bukan "sama").
4. Gagal = fix + ulangi FASE PASCA (DILARANG re-seed untuk memperbaiki p —
   §5/H3). Lolos = tulis laporan §5.

## Larangan (pelanggaran = run gagal)

Rescan; sentuh R selain F0 + histori baseline (§3); baca/hitung V sebelum
F0 hijau (P3); hitung-ulang tercil di V; sentuh P (2026) dalam bentuk apa
pun; uji ke-2; split selain H1/H2-preregistered; floor-efek; klaim
per-band; L2/simulasi trade; kolom-gugur dinarasikan; re-seed;
`except: pass`; `print()` produksi; fungsi >50 baris / file >400 baris
tanpa `# LENGTH_EXCEPTION` (pengecualian generator §15.1: referensi stabil
+ diff kecil + deterministik + assertion).

## Format pulang

Laporan AGENTS.md §5: file dibuat/diubah (+ `git hash-object` tiap file
klaim SESUDAH penulisan terakhir) · tabel Klaim & Bukti (TERVERIFIKASI /
BELUM DIVERIFIKASI / ASUMSI / GAGAL — DILARANG "sepertinya OK") · section
FASE 0 tersendiri · section FASE PASCA tersendiri · yang belum diverifikasi
· potensi masalah · saran. Satu ronde satu vonis: DILARANG "sekalian coba
varian".
