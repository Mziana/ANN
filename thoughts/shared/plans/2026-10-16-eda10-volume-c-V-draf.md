# Blueprint EDA-10 — volume-(c) lock-produksi di V (FINAL 2026-10-16)

> Status: FINAL (dikunci 2026-10-16 atas putusan eksplisit user: R1/R2/R3 =
> A/A/A, §13; Amandemen-Audit §14 (perintah "terapkan patch gabungan");
> eksekusi MENUNGGU perintah terpisah, §8A.3). Peran ronde:
> MENGUNCI spesifikasi-produksi volume-(c) di V — BUKAN konfirmasi baru,
> BUKAN generasi. Vonis wick CONFIRM (EDA-09) IMMUTABLE — ronde ini tak
> bisa mengubahnya ke arah mana pun. P (2026) DILARANG disentuh
> (assert runtime).

## 1. Latar (beku)

- EDA-08 CLOSED (bc4dac7): Volume LOCK FINAL = (c): vol_bar-s /
  median-rolling-20d-slot-HH:MM-sama TANPA-hari-berjalan (R1 HH:MM;
  R2 pooled bobot-n); warmup-R: drop 20 hari pertama + count (87 event,
  n-vol-R = 1427).
- EDA-09 CLOSED (641a25f): Q-vol-V lock-in TERKARAKTERISASI di V, 0 uji:
  med-V 1.179 (R 1.151), baseline-penuh 1018/1018, drop 0; V-hari-1 =
  20 hari-R terakhir; fungsi IDENTIK R (reuse, bukan tulis-ulang).
  Vonis lock-in TERPENUHI — TETAPI dua hal belum ada: (a) bukti reproduksi
  mandiri dari resep-beku (sel-7 hidup di dalam notebook konfirmasi-wick,
  bukan pipeline volume mandiri); (b) spesifikasi rolling-live untuk
  produksi/ANN (aturan update baseline harian — forward-note EDA-08/09
  "baseline mesti diupdate harian" belum diformalkan).
- EDA-10 menjawab (a) + (b). Tidak menjawab apa-apa lagi.

## 2. Pertanyaan (terkunci — tepat 2 butir, 0 uji)

- Q-repro-V (REPRODUKSI, 0 UJI): apakah resep-beku volume-(c) +
  deteksi-event-V mereproduksi angka-beku EDA-09 sel-7 bit-identik
  (n-V = 1018; band-V unik 367/286/168/289; full-room 325/269/156/268;
  med 1.179; drop 0)? LOCKED-parsial = semua sama persis.
- Q-spec-live (SPESIFIKASI, 0 UJI): resep rolling-live yang dibekukan =
  baseline tiap hari-T memakai 20 hari-bersih sebelum-T (slot-HH:MM-sama,
  tanpa hari-berjalan); hari tanpa 20-hari histori = event hari itu DROP
  + count (aturan umum — V-hari-1 = kasus khusus 20-hari-R-terakhir,
  konsisten, bukan pengecualian). Spesifikasi ditulis sebagai teks
  terkunci + diuji-prosedural pada 20 hari-V pertama vs baseline-R
  (kesamaan prosedur, bukan angka — angkanya sudah Q-repro).
- DILARANG: uji statistik apa pun atas volume (deskriptif tetap
  deskriptif); klaim R-vs-V ("distribusi bergeser" tanpa uji = narasi);
  sentuh wick/null/CI (milik EDA-09, beku); L2/simulasi-trade.

## 3. Definisi terkunci

- Konstruksi event-V = IDENTIK EDA-07/08/09: `scan_spikes` verbatim +
  ambang + dedup/overlap + BAND_EDGES [1.5,2.0,2.5,3.0] + outcome machine
  + full-room (drop_flag==0). Re-detect di 2025 dari kode-beku (bukan
  load artefak EDA-09 — EDA-09 tak menyimpan parquet-V; re-detect =
  uji-reproduksi, bukan konstruksi-baru).
- Volume-(c) = fungsi IDENTIK EDA-09 sel-7 (salin verbatim, reuse-first
  §16): rasio vol_bar-s / median-rolling-20d-slot-HH:MM-sama,
  tanpa-hari-berjalan. Assert kesamaan-kode (diff fungsi = kosong,
  dilaporkan sebagai bukti). Tiga presisi-teks (Amandemen-Audit):
  agregasi med/IQR/P1/P99 = atas rasio SEMUA event-V pooled (bukan
  per-hari); MANIFEST = daftar hari-bersih (`MANIFEST_ALL` =
  `MANIFEST_R` + `MANIFEST_V` terurut, builder L670); "20 hari penuh"
  = 20 hari di MANIFEST (bukan 20 slot valid) — slot NaN diabaikan
  `np.nanmedian` (konsisten EDA-09, builder L684–688).
- V-partisi + whitelist + concat-indikator = warisan EDA-09
  (reuse): ATR14/RSI14-Wilder dihitung pada frame 2023+2024+2025
  verbatim sel-3 EDA-09 sebagai PRASYARAT `scan_spikes` (builder
  L346–356 membaca `g["atr"]`, L377+ `g["rsi"]`); premis lama
  ("volume tak butuh indikator → JANGAN hitung") DITARIK TERTULIS —
  yang tak memakai indikator adalah fungsi volume, BUKAN deteksi
  (temuan H1 audit-diri, perintah "terapkan patch gabungan").
  T_DAY/cls TIDAK dihitung di EDA-10 (cls tak dipakai — metadata-only,
  NOL peran putusan; dikeluarkan dari daftar warisan).
- Baseline histori boleh memakai hari-R (past-only, live-sah —
  forward-note EDA-08). V-hari-1..20 vs 20-hari-R-terakhir = jangkar
  Q-spec (prosedur sama, sumber histori beda — tercatat eksplisit).
- DILARANG RNG di pipeline (tak ada langkah stokastik) → tak ada seed;
  determinisme dibuktikan via rerun byte-identik (diff output kosong),
  preseden klaim-coder EDA-09.

## 4. Famili uji (TERKUNCI: 0)

- Tepat NOL p-value ronde ini. Menambah uji di tengah = STOP + amandemen
  (pagar HARKing — volume didaftarkan deskriptif sejak EDA-08).
- Vonis LOCKED/GAGAL (§11 draf ini) berasal dari gate reproduksi +
  kelengkapan spesifikasi, BUKAN dari ambang statistik.

## 5. Null machine: TIDAK ADA (tercatat eksplisit — bukan kelalaian)

## 6. Pre-flight coder (F-style)

- F0': reproduksi-event-V — re-detect 2025 (termasuk concat-indikator
  prasyarat + whitelist-V sesudah deteksi, reuse EDA-09; assert
  0 whitelist-drop (vs 1110). Bila > 0 → STOP + arsitek — DILARANG
  drop-diam) + assert Nunik-V = 1110, band unik 367/286/168/289,
  full-room 325/269/156/268 (angka-beku EDA-09 REPORT FASE 2).
  Gagal → STOP + arsitek (fondasi-goyang vs artefak-numerik; bedakan
  TEGAS karena EDA-09 hijau di data sama).
- F1': V-whitelist + availabilitas (warisan EDA-09 F1: hari ⊆ 2025,
  V∩R = ∅, max < 2026-01-01; tick_volume bar-s ≥ 0,95 per bar-s;
  hari-V 259; bar-M15-V 23812 — assert-vs-beku, bukan eksplorasi).
- F2': volume-gate — assert TIAP event-V punya baseline penuh 20 hari
  (target: 1018/1018, drop 0 — assert-vs-beku); med/IQR/P1/P99 =
  1.179/[0.914,1.607]/0.503/4.396 (assert-vs-beku, toleransi bit-eksak
  float-repr; gagal → STOP, bukan "mendekati").
- F3': audit-tepi — (a) V-hari-1 baseline = 20 hari-R terakhir;
  V-hari-2..20 = campuran (19R+1V, …, 1R+19V); yang diaudit = prosedur
  satu-jalur (tak ada cabang khusus V-hari-1), BUKAN klaim "semua
  dari R" (koreksi-U1: kalimat lama tak-akurat);
  (b) bar-s tanpa tick_volume: ekspektasi 0 kejadian (fill-V 1.0000
  di EDA-09); bila > 0 → catat + STOP + arsitek (tak ada preseden →
  jangan karang aturan; klaim lama "DITETAPKAN di sini" DITARIK —
  menutup lubang M2(a));
  (c) slot-HH:MM tanpa histori-20-penuh di tengah-V: aturan umum DROP
  + count; ekspektasi 0 kejadian — bila > 0 → STOP + arsitek.
  DILARANG drop-diam.
- A-checks: A1' diff-fungsi-volume vs EDA-09 sel-7 = kosong (reuse
  verbatim terbukti); A2' determinisme — rerun penuh → diff kosong
  pada seluruh file-ipynb + artefak-data (bila gagal HANYA pada
  metadata-volatil notebook → STOP + arsitek, bukan GAGAL) +
  parquet-R: read-only bila dibaca; hash SHA256 pra-run vs pasca-run
  WAJIB identik B800E50E…BDFC2 tanpa-syarat (berubah = bug = STOP).

## 7. Gate & disiplin (warisi EDA-09)

- Prereg penuh; ambigu → STOP; assertion crash = bug; deterministik
  (DILARANG RNG); notebook = artefak generator (exit 0); venv kanonik;
  §8A.3 (draf ini tidak mengeksekusi diri sendiri).
- P1 label: tiap angka-V bertag REPRODUKSI-V; angka-beku EDA-09 bertag
  BEKU-EDA-09. P3: resep dikunci SEBELUM sentuh V (F0' hijau dulu —
  sentuh = load hari-2025). P4: TAK ADA simulasi trade.
- Penumpukan-V diperluas (caveat §9 EDA-09): V dipakai KETIGA kali
  (konfirmasi + validasi-ANN + lock-spesifikasi ini). Independensi
  TERBATAS — hakim final tetap P-segel pristine. LOCKED = izin-pakai-ANN,
  BUKAN vonis-dagang.

## 8. Deliverables & Done

- Generator `scripts/_build_eda10_volume_lock.py` + notebook
  `eda_10_volume_lock.ipynb` + `reports/eda/<tgl>-eda10/` (laporan +
  manifest [skema: tabel oracle-vs-aktual + bukti-diff +
  teks-spesifikasi-rolling-live + toolchain + vonis] + §
  spesifikasi-rolling-live terkunci sebagai teks) +
  baris vonis "LOCKED" / "GAGAL" (tepat satu kata).
- Done = semua ada + F0'/F1'/F2'/F3'/A' hijau + vonis satu-kata +
  label REPRODUKSI-V. GAGAL = SELESAI SUKSES (bukan gagal eksekusi).

## 9. Kompatibilitas ANN (tag warisan)

- Output ronde = resep-tekkunci siap-pakai ANN-01: fungsi + aturan
  update-harian + aturan-drop. ANN memakai, tak memodifikasi
  (modifikasi = ronde baru + perintah eksplisit).
- Volume-(c) dikunci sebagai fitur TAPI belum diuji prediktif-arah
  (0 uji sejak EDA-08). FS-01 WAJIB uji MI/FDR sebelum masuk ANN;
  tak-lolos = jangan dipaksa masuk (peringatan-U6: LOCKED ≠ berguna).

## 10. Kalibrasi (jawaban eksplisit per pilihan)

- 0 uji: volume didaftarkan deskriptif sejak EDA-08 §2-Qvol; memberi uji
  di EDA-10 = pertanyaan-tak-teregistrasi (HARKing prosedural walau
  prereg-sekarang — registrasinya tak punya hipotesis arah).
- Re-detect vs load-artefak: EDA-09 tak menyimpan parquet-V; re-detect
  dari kode-beku = reproduksi SESUNGGUHNYA (load-artefak = sirkular).
  F0' menjaga dengan angka-beku sebagai oracle.
- Bit-eksak (bukan toleransi): float deterministik + toolchain beku
  (numpy 1.26.4/pandas 2.2.3/pyarrow 17.0.0); "mendekati" = GAGAL.
- Tanpa CI/bootstrap: karakterisasi cukup di EDA-09; mengulang =
  komputasi tanpa pertanyaan.

## 11. Konsekuensi (terkunci)

- LOCKED → spesifikasi-produksi volume-(c) TERKUNCI untuk ANN-01;
  Registry tak berubah (volume bukan amunisi arah); stopping-rule
  tak tersentuh (bukan ronde-konfirmasi: stall-count N/A).
  LOCKED (EDA-10) MELAMPAUI "lock-in terpenuhi" EDA-09 (karakterisasi
  awal): bukti reproduksi mandiri + spesifikasi rolling-live lengkap.
- GAGAL → volume-(c) kembali "tertunda" (spesifikasi belum layak-ANN);
  wick CONFIRM TAK TERSENTUH; arsitek mendiagnosis (bedakan
  resep-salah vs data-bergeser); ronde-perbaikan butuh perintah.

## 12. Jejak + bantai-draf (self-audit Commander 2026-10-16)

- Sumber tiap §: §§1–2 = vonis EDA-09 + forward-note EDA-08/09;
  §3 = reuse-first §16 + angka-beku REPORT EDA-09; §6 = pola F-style;
  §11 = adaptasi stopping-rule (bukan ronde-konfirmasi).
- B1 "Kenapa ronde baru — sel-7 EDA-09 belum cukup?" → sel-7 =
  karakterisasi-di-dalam-notebook-konfirmasi, tanpa reproduksi-mandiri
  dan tanpa spesifikasi-rolling-live. Keduanya syarat-pakai-ANN.
  DITOLAK (tetap ronde baru).
- B2 "Re-detect = sentuh-V dengan 'konstruksi baru'?" → BUKAN:
  kode-beku + oracle-angka-beku + 0 derajat-bebas. F0' sebagai pagar.
  DITOLAK beralasan.
- B3 "GAGAL bisa berarti data-2025 bergeser — vonis wick ikut goyang?" →
  TIDAK: wick CONFIRM final EDA-09 (data + metode sama-hijaunya);
  GAGAL-volume = masalah-spesifikasi-volume, dipisah TEGAS §11.
- B4 "Tanpa seed — determinisme tak terjamin?" → DILARANG RNG =
  determinisme struktural; gerbangnya rerun-diff (A2'), bukan seed.
- B5 "§7-penumpukan: tiga-kali-pakai-V melemahkan CONFIRM?" → CONFIRM
  diputus SEBELUM ronde ini atas data-virgin; EDA-10 tak menyentuh
  wick/null. Caveat untuk ANN, bukan revisi vonis. Dicatat §7.

## 13. Putusan review (DIPUTUS user 2026-10-16 — ronde DIKUNCI FINAL)

- R1 SCOPE = (a) reproduksi + spesifikasi-live seperti draf.
  (b)/(c) DITOLAK.
- R2 RESPONS-GAGAL = "tertunda" seperti draf (§11). Amandemen-otomatis
  DITOLAK (amandemen butuh perintah eksplisit).
- R3 TOOLCHAIN = kunci numpy 1.26.4/pandas 2.2.3/pyarrow 17.0.0
  (bit-eksak rapuh lintas-versi). Terbaru + toleransi DITOLAK.
- Self-pass terakhir Commander sebelum kunci: 0 uji tertutup (famili
  kosong §§4–5), oracle angka-beku eksplisit (F0'/F2'), DILARANG-RNG +
  rerun-diff (A2'), P-segel tersentuh nol, vonis wick immutable,
  stall-count N/A tercatat — NOL cacat fundamental tersisa.
  Blueprint TERKUNCI. Eksekusi MENUNGGU perintah terpisah (§8A.3).

## 14. Amandemen-Audit (2026-10-16, perintah eksplisit "terapkan patch gabungan")

Masuk: H1 (§3: concat-indikator verbatim prasyarat `scan_spikes`;
premis "JANGAN hitung" ditarik); M2 (teks-spesifikasi mandiri:
agregasi pooled, semantik MANIFEST, "20 hari" opsi-A; lubang F3'(b)
ditutup U7); L1 (whitelist di F0'); L2 (diff-scope + metadata-STOP);
L3 (skema manifest); U1 (F3'(a): campuran R+V); U2 (GAGAL tunggal —
L68 GUGUR diperbaiki); U3 (LOCKED melampaui lock-in-terpenuhi);
U4 (opsi-A); U5 (hash pra=pasca tanpa-syarat); U6 (§9 peringatan
FS-01); U7 (>0 → STOP, anti-drop-diam). Sifat: koreksi-spesifikasi
+ presisi-teks; NOL perubahan desain (0 uji, oracle, vonis-imun,
R1/R2/R3 tak tersentuh). Blueprint TETAP FINAL. Eksekusi MENUNGGU
perintah terpisah (§8A.3).
