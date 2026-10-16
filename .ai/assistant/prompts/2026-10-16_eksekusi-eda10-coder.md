# Brief Eksekusi EDA-10 volume_lock_V — Coder (2026-10-16)

## Otoritas + PRASYARAT

Satu-satunya otoritas = blueprint FINAL
`thoughts/shared/plans/2026-10-16-eda10-volume-c-V-draf.md` (§§1–14: status
FINAL + §14 Amandemen-Audit + 2 klarifikasi audit-final — T_DAY dikeluarkan
dari warisan, F0' whitelist tegas — dibaca PENUH sebelum menyentuh apa pun;
bila brief ini bertentangan dengan blueprint, blueprint menang — laporkan
konflik, jangan improvisasi).
**PRASYARAT: blueprint sudah FINAL + perintah eksekusi user sudah turun
(2026-10-16: "susun prompt coder + eksekusi (terpisah, §8A.3)").**
Keduanya terpenuhi. Klaim tanpa output mentah = gagal.

## Workdir + disiplin peran (AGENTS.md §26 + §23)

- Workdir = `D:/ANN` (main). DILARANG buat branch/worktree baru — §23:
  tanpa perintah eksplisit user (tidak ada dalam order ini). DILARANG
  commit/push/merge tanpa perintah eksplisit.
- Kamu CODER: implementasi + self-audit + fix. DILARANG memutuskan
  metode/kriteria/ambang (eskalasi lewat user bila ragu). DILARANG audit
  independen pengganti Auditor; yang WAJIB = self-review §4 + self-audit
  klaim (§20-butir-7) sebagai section laporan — FASE 0 (pra-eksekusi) dan
  FASE PASCA (pasca-run), keduanya gerbang (blokir + kelulusan).
- Venv kanonik: `venv/Scripts/python.exe`. DILARANG `.venv/`.
- Builder→notebook: tulis `scripts/_build_eda10_volume_lock.py`, rerun,
  notebook `notebooks/scalping/eda_10_volume_lock.ipynb` ter-regenerate.
  DILARANG edit notebook manual. DILARANG mulai dari 0 / rewrite artefak
  beku (reuse-first §16: `scan_spikes`, `_wilder_ema`, `_vol_c`, MANIFEST
  disalin verbatim dari `scripts/_build_eda09_wick_confirm.py`, bukan
  ditulis ulang — verifikasi ulang nomor baris via NAMA FUNGSI sebelum
  menyalin; nomor baris bisa bergeser).
- Baris vonis mekanis ("LOCKED"/"GAGAL", §11) dicetak generator; tepat
  satu kata; DILARANG menarasikan/mengkualifikasi vonis di luar baris itu.
  GAGAL = SELESAI SUKSES (bukan gagal eksekusi).

## FASE 0 — SELF-AUDIT PRA-EKSEKUSI (gerbang blokir)

DILARANG menulis/menjalankan generator/notebook SEBELUM fase ini lulus
tertulis. Bukti paham (tulis di laporan, BUKAN sekadar "sudah baca"):
kutip dari blueprint — 0 uji (Q-repro-V + Q-spec-live; famili kosong
§§4–5; menambah uji = STOP + amandemen) + oracle F0' (Nunik-V = 1110,
band unik 367/286/168/289, full-room 325/269/156/268; 0 whitelist-drop
vs 1110, bila > 0 → STOP + arsitek) + oracle F2' (baseline penuh
1018/1018 drop 0; med/IQR/P1/P99 = 1.179/[0.914,1.607]/0.503/4.396
bit-eksak) + T_DAY/cls TIDAK dihitung (metadata-only, NOL peran putusan)
+ concat-indikator prasyarat (§3: frame 2023+2024+2025 verbatim,
whitelist-V SESUDAH deteksi) + hash parquet-R pra=pasca tanpa syarat +
DILARANG RNG (tanpa seed; determinisme via rerun-diff A2') + daftar
DILARANG §2 verbatim pendek (uji statistik; klaim R-vs-V; sentuh
wick/null/CI; L2/simulasi-trade).

1. Self-review AGENTS.md §4 (10 butir: baca ulang, bug/edge/None,
   look-ahead, leakage, konvensi, hardcode, duplikasi, test, import;
   tandai keraguan `# REVIEW:`).
2. Self-audit 3×: Correctness (tiap angka yang akan diklaim bersumber
   file:baris/output — tulis sumbernya SEBELUM ada output) · Bias (di mana
   letak godaan HARKing ronde ini? tulis 3 + penangkalnya; ingat volume
   deskriptif sejak EDA-08, dan "mendekati" = GAGAL) · Meta (semua syarat
   §§2–8 blueprint terpetakan ke sel kode apa? file luar scope apa yang
   berisiko tersentuh? — jawab eksplisit: P-segel, parquet-R (read-only),
   notebook EDA-09, artefak beku).
3. Pasangan perintah mentah (tempel SEMUA output di laporan):
   `ruff check <builder>` (wajib rc=0, sebut rc) +
   `ruff format --check <builder>` (wajib rc=0) +
   `git status --porcelain` (klaim tanpa-stage di luar file kerja) +
   `venv/Scripts/python.exe scripts/check_foreign_chars.py <builder>`
   (wajib OK).
4. Larangan bentuk-spesifik: DILARANG guard yang membandingkan nilai dengan
   dirinya sendiri (termasuk via kolom turunan frame yang sama) · DILARANG
   merekonstruksi hari dari UTC (grain tunggal hari-broker) · DILARANG
   referensi dibaca dari objek yang sama diperiksa (hash parquet-R dihitung
   dari file di disk pra-run vs pasca-run sebagai dua pembacaan terpisah;
   sebut versi pyarrow/pandas bila klaim byte-identik) · DILARANG klaim
   "sudah diuji" di satu bagian sambil "belum ada test" di bagian lain ·
   DILARANG fixture seragam untuk test yang mengklaim sensitif-parameter ·
   DILARANG menempel output parsial dengan label proses penuh · DILARANG
   kutip baris/path tanpa verifikasi ulang (jangkar = nama fungsi, bukan
   nomor baris).
5. Hasil FASE 0 = section laporan tersendiri. Gagal = fix + ulangi FASE 0.
   Lolos = baru boleh FASE 1.

## FASE 1 — F0' reproduksi-event-V (fondasi; gagal = STOP)

Re-detect 2025 dari kode-beku (BUKAN load artefak EDA-09 — EDA-09 tak
menyimpan parquet-V; re-detect = uji-reproduksi, bukan konstruksi-baru):
`scan_spikes` verbatim (jangkar: fungsi `scan_spikes` di builder EDA-09) +
ambang + dedup/overlap + BAND_EDGES [1.5,2.0,2.5,3.0] + outcome machine +
full-room (drop_flag==0) + concat-indikator ATR14/RSI14-Wilder pada frame
2023+2024+2025 (jangkar: fungsi `_wilder_ema`; builder EDA-09 membaca
`g["atr"]`/`g["rsi"]` di dalam scan — itulah alasan indikator dihitung;
fungsi volume sendiri tak memakainya) + whitelist-V SESUDAH deteksi.
T_DAY/cls TIDAK dihitung sama sekali (jangan port konstanta T_DAY maupun
klasifikasi hari; metadata-only, NOL peran putusan).
Assert bit-eksak vs oracle BEKU-EDA-09: Nunik-V = 1110; band unik
367/286/168/289; full-room 325/269/156/268; 0 whitelist-drop (vs 1110) —
bila > 0 → STOP + arsitek (DILARANG drop-diam; DILARANG karang aturan
penutup). Gagal assert mana pun → STOP + lapor (DILARANG improvisasi /
"perbaikan" kode-beku; bedakan TEGAS fondasi-goyang vs artefak-numerik —
EDA-09 hijau di data sama). Tempel aktual vs ekspektasi baris-per-baris.
F0' hijau = prasyarat MENYENTUH V (P3: sentuh = load hari-2025; resep
dikunci SEBELUM sentuh V).

## FASE 2 — F1'/F2'/F3' + A-checks (blueprint §6)

Berurutan, STOP + lapor pada gagal pertama (tempel output tiap cek).
F1': hari-V ⊆ 2025, V∩R = ∅ (whitelist dua-arah), max(day-V) <
2026-01-01; tick_volume bar-s-V terisi ≥ 0,95 — ambang dihitung PER BAR-s
(= bar analisis), BUKAN agregat; hari-V 259; bar-M15-V 23812 —
assert-vs-beku, bukan eksplorasi.
F2': TIAP event-V punya baseline penuh 20 hari (target 1018/1018, drop
0 — assert-vs-beku); agregasi med/IQR/P1/P99 atas rasio SEMUA event-V
pooled = 1.179/[0.914,1.607]/0.503/4.396 (assert-vs-beku, bit-eksak
float-repr; gagal → STOP, bukan "mendekati").
F3': (a) V-hari-1 baseline = 20 hari-R terakhir; V-hari-2..20 = campuran
(19R+1V, …, 1R+19V); yang diaudit = prosedur satu-jalur (tak ada cabang
khusus V-hari-1); (b) bar-s tanpa tick_volume: ekspektasi 0 (fill-V
1.0000 di EDA-09) — bila > 0 → catat + STOP + arsitek, DILARANG karang
aturan; (c) slot-HH:MM tanpa histori-20-penuh di tengah-V: aturan umum
DROP + count, ekspektasi 0 — bila > 0 → STOP + arsitek. DILARANG
drop-diam di semua cabang.
A-checks: A1' diff fungsi volume vs `_vol_c` EDA-09 = kosong (salin
verbatim; jangkar: `MANIFEST_ALL = MANIFEST_R + MANIFEST_V` terurut,
`past20 = MANIFEST_ALL[max(0,j-20):j]`, `np.nanmedian`; "20 hari penuh"
= 20 hari di MANIFEST, slot NaN diabaikan — laporkan diff sebagai bukti);
A2' determinisme — rerun penuh → diff kosong pada seluruh file-ipynb +
artefak-data (bila gagal HANYA pada metadata-volatil notebook → STOP +
arsitek, bukan GAGAL) + parquet-R: read-only bila dibaca; hash SHA256
pra-run vs pasca-run WAJIB identik tanpa syarat (pembanding:
`reports/eda/2026-10-16-eda09/manifest.json`; berubah = bug = STOP).

## FASE 3 — Build + run

Notebook exit 0 via nbconvert (tempel exit code + jumlah sel/asersi).
DILARANG RNG di pipeline (tak ada langkah stokastik → tak ada seed;
determinisme dibuktikan via rerun-diff A2', bukan seed). Tiap angka-V
bertag REPRODUKSI-V; tiap angka-beku yang dikutip bertag BEKU-EDA-09.
Spesifikasi rolling-live ditulis sebagai TEKS TERKUNCI di laporan:
baseline tiap hari-T memakai 20 hari-bersih sebelum-T (slot-HH:MM-sama,
tanpa hari-berjalan); hari tanpa 20-hari histori = event hari itu DROP +
count (aturan umum; V-hari-1 = kasus khusus 20-hari-R-terakhir, konsisten
bukan pengecualian) + diuji-prosedural pada 20 hari-V pertama vs
baseline-R (kesamaan prosedur, bukan angka — angkanya sudah Q-repro).
Laporan + manifest ke `reports/eda/2026-10-16-eda10/` — manifest skema
5-elemen: tabel oracle-vs-aktual + bukti-diff + teks-spesifikasi-
rolling-live + toolchain (numpy 1.26.4/pandas 2.2.3/pyarrow 17.0.0 —
bit-eksak rapuh lintas-versi, DILARANG upgrade) + vonis. Baris vonis
mekanis tepat satu kata ("LOCKED"/"GAGAL") dicetak generator.

## FASE PASCA — SELF-AUDIT PASCA-RUN (gerbang kelulusan)

DILARANG menulis laporan final SEBELUM fase ini lulus tertulis. Setelah
SEMUA assert hijau (tempel output full-suite, BUKAN satu file):

1. Correctness ulang: tiap klaim laporan tunjuk ke output mentah (sel
   notebook / baris log / file:baris). Klaim tanpa pasangan output =
   klaim GAGAL — tulis sebagai BELUM DIVERIFIKASI, jangan dipoles.
2. Bias ulang: label REPRODUKSI-V di tiap angka-V? ada klaim R-vs-V tanpa
   uji terselip? ada "mendekati" yang dibaca sebagai lolos? ada kolom
   pipeline yang dinarasikan? Tulis hasil periksa per butir (lolos/gagal
   + bukti).
3. Meta ulang: semua syarat §§2–8 + §14 terjawab di sel mana? file luar
   scope tersentuh? (`git status --porcelain` ditempel.) determinisme
   rerun dibuktikan? (angka rerun ditempel, bukan "sama".) hash parquet-R
   pra=pasca ditempel?
4. Gagal = fix + ulangi FASE PASCA (DILARANG re-seed untuk memperbaiki apa
   pun — tak ada seed di ronde ini). Lolos = tulis laporan.

## Larangan (pelanggaran = run gagal)

Re-detect di luar kode-beku (= konstruksi baru); sentuh R selain histori
baseline; baca/hitung V sebelum F0' hijau (P3); hitung T_DAY/cls dalam
bentuk apa pun; uji statistik apa pun atas volume (0 uji — menambah =
STOP + amandemen); klaim R-vs-V; sentuh P (2026) dalam bentuk apa pun
(assert runtime); sentuh wick/null/CI (milik EDA-09, beku); L2/simulasi
trade; kolom pipeline dinarasikan; `except: pass`; `print()` produksi;
fungsi >50 baris / file >400 baris tanpa `# LENGTH_EXCEPTION`
(pengecualian generator §15.1: referensi stabil + diff kecil +
deterministik + assertion); edit notebook manual; mulai dari 0 / rewrite
artefak beku.

## Format pulang

Laporan AGENTS.md §5: file dibuat/diubah (+ `git hash-object` tiap file
klaim SESUDAH penulisan terakhir) · tabel Klaim & Bukti (TERVERIFIKASI /
BELUM DIVERIFIKASI / ASUMSI / GAGAL — DILARANG "sepertinya OK") · section
FASE 0 tersendiri · section FASE PASCA tersendiri · yang belum
diverifikasi · potensi masalah · saran. Satu ronde satu vonis: DILARANG
"sekalian coba varian". Vonis wick CONFIRM (EDA-09) IMMUTABLE — ronde ini
tak bisa mengubahnya ke arah mana pun.
