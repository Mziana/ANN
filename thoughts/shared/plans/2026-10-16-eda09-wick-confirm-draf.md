# Blueprint EDA-09 — wick_confirm_V (FINAL 2026-10-16)

> Status: FINAL (dikunci 2026-10-16 atas persetujuan eksplisit user, §13;
> Amandemen-1 (§14) + Amandemen-2 (§15, dikunci 2026-10-16 atas perintah
> eksplisit "kunci + revert + jalan"). EKSEKUSI DIPERINTAHKAN 2026-10-16
> (satu seed, satu run; butir 5 putusan arsitek).
> Peran ronde: KONFIRMASI di V (virgin) — BUKAN generasi. Satu-satunya
> pertanyaan konfirmasi = efek-wick pooled (shortlist-final EDA-08) +
> lock-in definisi volume-(c) (0 uji). P (2026) DILARANG disentuh
> (assert runtime). R dipakai HANYA untuk tiga keperluan past-only yang
> preregistered: F0 reproduksi-cut + histori baseline volume + warmup
> indikator concat (§3, Amandemen-2); selain itu DILARANG.

## 1. Latar (beku)

- EDA-07 CLOSED (c354d3b): Nunik=1632, band 515/415/240/462, full-room 1514.
- EDA-08 CLOSED (bc4dac7): famili FDR-BH q=0,10 tepat 4 uji → lolos 1
  (wick pooled Δ=0.1682, p=0.0001 dua-arah, gate-tanda +0.1714/+0.1651);
  first/gap32/dow GUGUR-komputasi; joint = estimasi. Shortlist-final=[wick].
  Volume LOCK FINAL=(c): vol_bar-s / median-rolling-20d-slot-HH:MM-sama
  TANPA-hari-berjalan (R1 HH:MM; R2 pooled bobot-n); warmup-R: drop 20 hari
  pertama + count (87 event, n-vol-R=1427).
- Partisi (beku EDA-06 Amandemen-1): R = 2023H2+2024 (384 hari, terkunci);
  V = 2025 (259 hari, workhorse validasi); P = 2026 segel (ujian final,
  sentuh tepat sekali). EDA-07 assert: max(day) < 2025-01-01 (R tak bocor
  ke V). Ekspektasi daya: R 1514/384 ≈ 3,94 event/hari → V ≈ 1020 event
  (ekspektasi, BUKAN gate).
- Registry #4 = wick-ratio, KANDIDAT V-confirm (GENERASI-R).

## 2. Pertanyaan (terkunci — tepat 2 butir, 1 uji)

- Q-wick-V (SATU-SATUNYA UJI, KONFIRMASI): apakah Δ pooled within-band
  (tercil-wick-atas − bawah, bobot-n, cut TERKUNCI dari R §3) positif di V?
  Uji SATU-ARAH (arah dikunci R: atas > bawah), α=0,05, lawan null
  permutasi terstratifikasi-band (§5). CONFIRM = p_satu-arah < 0,05 DAN
  tanda Δ̂_V sama dengan R. GUGUR = selain itu (p ≥ 0,05 ATAU tanda
  berbalik — keduanya final, tanpa banding ke konstruksi lain).
- Q-vol-V (LOCK-IN, 0 UJI): terapkan definisi-(c) terkunci ke event V
  dengan baseline precomputed (§3); laporkan distribusi vs R berdampingan
  (tanpa uji, tanpa klaim). Split H1/H2 deskriptif (§3) BUKAN butir
  pertanyaan dan BUKAN uji — vonis imun terhadapnya. Volume GUGUR-sebagai-pendamping BUKAN vonis
  ronde (vonis = Q-wick-V saja); bila tick_volume-V tak memenuhi F1 maka
  volume turun ke "tertunda" dan ronde tetap diputus oleh Q-wick-V.

## 3. Definisi terkunci

- Konstruksi event-V = IDENTIK EDA-07/08, parameter beku: `scan_spikes`
  verbatim + ambang + dedup/overlap (F0a/F0b) + BAND_EDGES [1.5,2.0,2.5,3.0]
  + outcome machine + full-room (drop_flag==0) + wick_ratio = 1−|q3_ratio|
  + is_rev = (outcome==reversal). Tuning DILARANG (STOP + amandemen).
- CUT-LOCK (P3, SEBELUM sentuh V): F0 hitung-ulang cut tercil R
  (t1,t2 × 4 band) dengan fungsi IDENTIK EDA-08 pada parquet-R, assert
  pooled-Δ reproduksi 0.1682 (toleransi 1e-9 — deterministik, mesti eksak)
  → 8 angka cut DIBEKUKAN sebagai konstanta untuk V. Cut V = cut R,
  DILARANG hitung-ulang tercil di V (itu konstruksi baru = HARKing).
- V-partisi: hari-bersih 2025 per RESEP EDA-07 (anomaly windows +
  session fingerprint + drop open-abnormal, reuse kode, bukan tulis ulang).
  Assert: semua hari-V tahun==2025; V ∩ R = ∅ (whitelist dua-arah);
  max(day-V) < 2026-01-01 (P tak tersentuh). Estimasi jumlah ≈259 hari
  (STOP-band §6 bila meleset jauh = drift pipeline, bukan variasi wajar).
- Konstanta cleaning TERKUNCI untuk V (diputus user 2026-10-16, audit H4):
  T_DAY = 1,7319 (warisan R; DILARANG recompute-P25 di V; assert-vs-EDA-06
  dicabut TERTULIS untuk V — recompute di 2025 pasti memicu STOP palsu).
  Kolom cls/ctx tetap dihitung sebagai metadata (integrity), nol peran
  putusan (terverifikasi: drop = room-logic `no_room_16`, bukan cls;
  cls → stratifikasi donor-mati EDA-08).
- Indikator-V di atas CONCAT 2023+2024+2025 (Amandemen-2, putusan arsitek
  2026-10-16): ATR14/RSI14-Wilder dihitung pada frame gabungan (reuse kode
  loading, tahun diperluas), whitelist event-V DILAKUKAN SESUDAH deteksi.
  Event-R yang ikut-terdeteksi = artefak-terbuang (sekelas kolom-M4: boleh
  ada, DILARANG dilapor/diuji/dinarasikan). Alasan tercatat: pipeline
  warisan TAK PERNAH menghitung indikator di atas frame tersayat (R memakai
  buffer H1-2023 6 bulan; builder L131/L175–213); 2025-only = konstruksi
  BARU + butuh parameter-K warmup-drop yang arbitrer (= tuning, dilarang);
  transien-ewm nyata di awal-Jan (~0,1% skala pasca-1-hari — cukup membalik
  event batas); live-sah past-only (justifikasi sama dengan forward-note
  baseline). 2025-only DITOLAK tercatat.
- Volume-(c)-V: baseline median-rolling-20d per slot-HH:MM boleh memakai
  hari-R (past-only, live-sah — forward-note EDA-08). V-hari-1 baseline =
  20 hari-R terakhir. Assert TIAP event-V punya baseline penuh 20 hari
  (bila tidak → DROP + count, dilaporkan). TIDAK ADA warmup-drop di V
  (alasan eksplisit: baseline pre-exists; drop-R dulu karena baseline
  dibangun dari nol di dalam R). Definisi rasio IDENTIK R (fungsi sama,
  slot=HH:MM, tanpa hari-berjalan — assert kesamaan kode via reuse).
- Per-band di V: deskriptif-saja (Δ + n per band, tanpa p, tanpa klaim) —
  MENGIKAT dari vonis EDA-08. Split H1/H2-2025: SATU split preregistered,
  DESKRIPTIF-SAJA (Δ + n per semester, tanpa p, tanpa klaim) — diputus user
  2026-10-16 (audit H2: vonis pooled buta terhadap kematian-rezim).
  Aturan-interpretasi preregistered: tanda berlawanan antar-semester →
  regime-caveat di laporan, VONIS TAK BERUBAH (vonis tetap pooled §2);
  arsitek menilai implikasi ANN. Split lain (kuartal/bulan/custom) TETAP
  DILARANG total — eksekusi bukan eksplorasi, cegah narrative mining.
- DILARANG di ronde ini: tanya-ulang first/gap32/dow (gugur final);
  kolom first/gap/dow BOLEH ada sebagai artefak pipeline (integrity —
  preseden EDA-08 merecompute first, builder L242–257) tetapi DILARANG
  dilaporkan, diuji, atau dinarasikan (cegah narasi-kebangkitan; diputus
  user 2026-10-16, audit M4); joint-sebagai-kandidat; klaim per-band; L2/simulasi-trade (fade GUGUR);
  floor-5pp di V (lihat §10 — floor adalah filter-generasi, bukan aturan
  konfirmasi; menambahnya = geser gawang pasca-registrasi).

## 4. Famili uji (TERKUNCI, tepat 1)

- Konfirmasi: wick-pooled-V SATU-ARAH, α=0,05 (satu-satunya p-value ronde).
- Volume = 0 uji. Joint = tidak dihitung di V dan tidak dipakai
  sama sekali (estimasi-R tinggal di R; pengecualian eksplisit §4 EDA-08 —
  V hanya untuk pertanyaan baru + volume). Per-band = 0 uji.
- Menambah uji/split/gate di tengah = STOP + amandemen (pagar HARKing).

## 5. Null machine V (terstratifikasi-band, B=10000)

- Statistik: Δ̂_V = pooled bobot-n (rate_atas − rate_bawah) atas cut TERKUNCI,
  subset full-room-V. Bobot = n band-V (R2 warisan).
- Null: permutasi NILAI wick DALAM band pada event-V, cut TERKUNCI
  diterapkan ulang per permutasi (coherent dengan statistik), B=10000,
  p_satu-arah = fraksi(null Δ ≥ obs Δ). STRATA = BAND (band confounder
  terbukti; konsisten R). Seed BARU independen format YYYYMMDD-eksekusi,
  dicatat (independen dari SEED_EXEC EDA-08). p dilaporkan 4 desimal.
  SATU SEED SATU RUN (diputus user 2026-10-16, audit H3): DILARANG re-seed
  untuk alasan apa pun kecuali bug terbukti (STOP + arsitek); kerapuhan
  perbatasan (p ∈ [0,04, 0,06]) dicatat apa adanya sebagai caveat, BUKAN
  alasan run-ulang.
- Catatan P2 (tanpa kontradiksi): R-null final untuk klaim-R; V-null (§5)
  adalah null primer klaim-KONFIRMASI. Tak ada V-kedua untuk wick.

## 6. Pre-flight coder (F-style)

- F0: reproduksi-R + cut-lock — load parquet-R EDA-07/08, assert Nunik/band/
  full-room/exh, hitung-ulang cut + assert reproduksi pooled-Δ:
  `round(pooled,4) == 0.1682` (Amandemen-2 — literal 1e-9 atas presisi-penuh
  DITARIK sebagai cacat spesifikasi: publikasi 0.1682 = pembulatan 4dp,
  banding-di-4dp = perbandingan jujur) + assert 8 cut SAMA PERSIS dengan
  §15 (repr-penuh) → bekukan (dicatat ke laporan sebagai konstanta
  presisi-penuh). STOP bila gagal → arsitek mendiagnosis (bedakan
  fondasi-goyang vs artefak-numerik, mis. drift versi-numpy pada quantile
  vs cut beda makna; diputus user 2026-10-16, audit M3 — "= ronde batal"
  DITARIK: STOP = arsitek menilai, bukan batal otomatis).
- F1: V-whitelist + availabilitas — hari-V ⊆ 2025, V∩R=∅, max<2026-01-01;
  tick_volume bar-s-V terisi ≥0,95 (ambang dihitung per bar-s = bar analisis,
  koreksi ronde-7 temuan 6 — BUKAN agregat; diputus user 2026-10-16, audit L4)
  (bila gagal → volume "tertunda", wick-confirm LANJUT; BUKAN improvisasi
  proxy). STOP-band jumlah hari-V: <200 atau >320 → STOP (drift pipeline,
  arsitek menilai). Sanity volume-data (warisan Cek-3 EDA-06, skala
  proporsional 384-hari→30–42k: 259 hari × ~96 bar ≈ 20–28k bar M15-V;
  diputus user 2026-10-16, audit M5): STOP-band <13k atau >40k → STOP
  (korupsi parsial 2025 bisa lolos day-count namun meracuni deteksi).
- F2: deteksi-V struktural — ke-4 band non-kosong (band kosong = STOP +
  arsitek, bukan drop-diam). TRIPWIRE DAYA (preregistered, anti-false-kill,
  diputus user 2026-10-16): (a) total n-V < 500 (≈50% ekspektasi 1020) →
  STOP + arsitek, BUKAN GUGUR (p ≥ 0,05 pada n kecil = absence of evidence,
  bukan evidence of absence); (b) grup tercil mana pun (atas/bawah × 4 band)
  n < 30 (standar POWER_MIN_N warisan program, bukan angka baru) → STOP +
  arsitek (cut-terkunci degenerat bila distribusi-2025 bergeser rezim).
  Keduanya tripwire validitas-keputusan — hanya bisa MENCEGAH kill-palsu,
  tak bisa memalsu CONFIRM; total-n-V dilaporkan vs ekspektasi.
- F4: seed baru tercatat (YYYYMMDD-eksekusi + streams; satu-seed-satu-run,
  larangan re-seed §5). STOP bila tak tercatat.
- A-checks: A1 taksonomi V exhaustive (band×outcome); A2 cut-lock teraplikasi
  (assert EXHAUSTIVE untuk SEMUA event-V — konvensi batas `lo_<=x<hi_`
  murah di kode, bukan sampling; diputus user 2026-10-16, audit L1).

## 7. Gate & disiplin (warisi EDA-06/07/08 + pagar baru)

- Prereg penuh; ambigu → STOP; assertion crash = bug; deterministik;
  notebook = artefak generator (exit 0); venv kanonik; §8A.3.
  (§8A.3 = AGENTS.md §8A butir 3, anti-looping: ronde investigasi tambahan
  setelah vonis DILARANG atas inisiatif AI — butuh persetujuan eksplisit
  user. Berlaku mengikat: draf ini tidak mengeksekusi diri sendiri.)
- P1 label: tiap angka-V bertag KONFIRMASI-V; angka-R yang dikutip bertag
  GENERASI-R (warisan) — headline tanpa label = cacat laporan.
- P2 dan null-V (tanpa kontradiksi, baca persis): null-R FINAL untuk
  klaim-R — tak diulang, tak butuh V (warisan harfiah). Null-V di sini
  adalah null PRIMER untuk klaim-KONFIRMASI (dataset virgin, konstruksi
  terkunci, §5) — bukan pengulangan R-null, bukan banding atas R-null.
- P3 lock-sebelum-V: cut + konstruksi dikunci di F0 SEBELUM sentuh V
  (sentuh = load hari-2025 mana pun; F0 mesti hijau dulu).
- P4 larangan resurrection-L2: TAK ADA simulasi trade di ronde ini.
- PAGAR BARU (dari vonis EDA-08 + audit-diri EDA-09): (P5) Split-temporal
  dalam-V: HANYA H1/H2 preregistered-deskriptif (§3; vonis imun, diputus
  user 2026-10-16); split lain (kuartal/bulan/custom) DILARANG total —
  eksekusi bukan eksplorasi;
  (P6) DILARANG floor-efek di V (signifikansi + tanda = vonis; materialitas
  untuk ANN diputus di tahap ANN dengan P-segel, bukan di sini).

## 8. Deliverables & Done

- Generator `scripts/_build_eda09_wick_confirm.py` + notebook
  `eda_09_wick_confirm.ipynb` + tabel wick-V (pooled Δ̂ + p + CI cluster-per-day
  B=10000 bootstrap — murah, konsisten null — sebagai karakterisasi TANPA
  peran putusan + per-band deskriptif + split-H1/H2 deskriptif) + laporan
  lock-in volume-(c)-V (distribusi vs R: med/IQR/P1/P99 + cakupan baseline +
  count-drop, cermin Sel-8 EDA-08 — daftar eksplisit agar "tanpa klaim" tak
  jadi narasi-bebas; diputus user 2026-10-16, audit L3/M6) + direktori
  `reports/eda/2026-10-16-eda09/` + manifest + baris vonis eksplisit
  "CONFIRM" / "GUGUR" (tepat satu kata, tanpa kualifikasi).
- Done = semua ada + F0/F1/F2/F4 hijau + vonis satu-kata + label
  KONFIRMASI-V di tiap klaim-V. GUGUR = SELESAI SUKSES (bukan gagal).

## 9. Kompatibilitas ANN (tag warisan)

- wick = lagged-causal (butuh end-detector + live scan — dependensi bersama,
  dicatat sekali). volume-(c) = live-jika-baseline-precomputed (ronde ini
  MEMPRAKTIKKAN jalan precompute-nya: baseline R→V; catatan untuk produksi:
  baseline mesti diupdate harian).
- Penumpukan-V (caveat tercatat, diputus user 2026-10-16, audit M2): V
  dipakai dua kali — konfirmasi ronde ini + validasi ANN-01 (desain program:
  train R, validasi V, test P). Independensi validasi TERBATAS (validasi tak
  independen dari seleksi-fitur); hakim final = P-segel yang pristine.
  CONFIRM-V = izin-masuk-ANN, BUKAN vonis-dagang. Tidak mengubah desain —
  melarang pembacaan-berlebih.

## 10. Kalibrasi (jawaban eksplisit per pilihan)

- Satu-arah α=0,05: TEPAT untuk satu klaim directional terkunci (dua-arah
  sudah dibayar di R; mengulang dua-arah di V = bayar dua kali untuk
  pertanyaan yang sama). Penguat independen (diputus user 2026-10-16,
  sub-item M1; DIKOREKSI Amandemen-2): ke-4 band-R bertanda positif
  (+0,1169/+0,0687/+0,1429/+0,3264 — triple-verifikasi: coder → user →
  Commander, cocok notebook EDA-08 sel 7) — arah unanimous, bukan artefak
  pooling. Sitasi lama (+0,1177/+0,0701 band0-1, recompute pra-compaction)
  DITARIK TERTULIS: tidak muncul di notebook tereksekusi, diganti angka
  terverifikasi.
- Tanpa floor-5pp (Opsi A, diputus user 2026-10-16): floor adalah FILTER
  GENERASI, bukan aturan konfirmasi — V menguji realitas efek ("apakah efek
  ini nyata?"), materialitas diputus ANN + P-segel (P pristine yang
  menghakimi, bukan V). Floor-5pp mewarisi arbitrariness R (penolakan
  Opsi-A-6pp tercatat justru menolak angka-garis arbitrer — menambah
  floor-di-V = arbitrariness baru, bukan disiplin). Δ̂_V dilaporkan eksak
  (4 desimal) agar tahap ANN melihat magnitudo. Argumen prosedural lama
  ("geser gawang pasca-registrasi") DITARIK TERTULIS: V masih virgin,
  draf ini registrasinya — tak ada gawang yang digeser.
- Tanpa gate-tahun-dalam-V: gate konsistensi sudah dibayar di R (tanda sama
  2023H2/2024). V = satu pool 2025; memecahnya = uji tambahan tak-teregistrasi.
- n<30 warisan: tak relevan di pool-V (≈1020 ekspektasi); bila band-V ada
  yang <30 → tetap masuk pool (bobot-n menanganinya), dilaporkan.

## 11. Konsekuensi stopping-rule (§11 EDA-08, terkunci)

- CONFIRM → Registry #4 naik pangkat TERKONFIRMASI-V (amunisi-V pertama;
  himpunan terkonfirmasi-V = {wick}); program LANJUT (butuh 4–5).
- GUGUR → wick MATI (dilarang dihidupkan ronde lain tanpa spek baru +
  perintah eksplisit); himpunan terkonfirmasi-V = {}; STALL COUNT = 1
  (interpretasi TERCATAT, bukan perubahan aturan: ronde-konfirmasi tanpa
  CONFIRM dihitung sebagai ronde-tanpa-positif untuk §11-butir-(ii);
  program LANJUT — berhenti butuh 2 berturut).
- Volume-(c) lock-in TERPENUHI di kedua cabang (definisi terkarakterisasi
  di V; status "tertunda" hanya bila F1-volume gagal — dilaporkan).

## 12. Jejak (vonis EDA-08 → draf ini + bantai-draf)

- Sumber tiap §: §1 = STATE + vonis EDA-08 2026-10-16; §2 = shortlist-final
  + Q-vol (§2-Qvol EDA-08); §3 = R1/R2 + warmup-rule + forward-note (§3 EDA-08)
  + Cek-3 EDA-06 (partisi); §4 = famili-1 (baru — R menutup 4, V membuka 1);
  §5 = null warisan (§5 EDA-08) + P2; §6 = pola F-style EDA-07/08;
  §7 = P1–P4 warisan + P5/P6 baru; §9 = tag warisan (§9 EDA-08);
  §11 = stopping-rule §11 EDA-08.
- Bantai-draf (self-audit Commander 2026-10-16):
  - B1 "Kenapa satu-arah, bukan dua-arah konservatif?" → arah = klaim
    terkunci R; dua-arah di V = bayar-ganda. Ditolak beralasan (§10).
  - B2 "Kenapa tanpa floor efek?" → floor = filter generasi; V menguji
    realitas, ANN+P menghakimi materialitas. Ditolak beralasan (§10).
  - B3 "Tercil dihitung-ulang di V lebih natural" → itu konstruksi BARU
    (distribusi-V ≠ R); cut-lock = inti P3. Ditolak (§3).
  - B4 "Split H1/H2 deskriptif tak ada salahnya" → salah: narasi pasca-hoc
    tanpa gate = HARKing lunak. Dilarang total (§3/§7-P5).
  - B5 "V ≈ 1020 asumsi rate-R konstan" → ditulis sebagai ekspektasi bukan
    gate; drift ditangkap STOP-band hari (§6-F1). Resolusi di teks.
  - B6 "Manifest-V eksplisit tak ditemukan di artefak" → JUJUR: V
    didefinisikan ekstensional via resep-beku + whitelist dua-arah (§3/§6-F1),
    bukan klaim file yang tak ada. Resolusi di teks.
  - B7 "Volume gagal = ronde gagal?" → TIDAK: volume 0-uji pendamping;
    vonis = Q-wick-V; status "tertunda" dilaporkan (§2/§11). Resolusi di teks.
- Bantai-draf lanjutan (self-audit pasca-compaction, verifikasi ulang
  terhadap blueprint EDA-08 + artefak main, 2026-10-16):
  - B8 "Joint sebagai stratifikasi di V?" → SALAH TULIS di draf: joint
    tak dihitung/dipakai sama sekali (§4 EDA-08: pengecualian eksplisit).
    DIPERBAIKI (§4).
  - B9 "P2 (null-R final) vs null-V?" → tegangan semu: P2 harfiah = R-null
    final untuk klaim-R; null-V = null primer klaim-KONFIRMASI. Ditegaskan
    tanpa kontradiksi (§5/§7-P2). DIPERBAIKI.
  - B10 "Header 'R DILARANG selain F0' vs baseline-R untuk V?" →
    KONTRADIKSI nyata: forward-note §3 EDA-08 eksplisit membolehkan histori
    baseline-V dari hari-R. Header DIPERBAIKI (dua keperluan past-only).
  - B11 "§8A.3 dirujuk terus, didefinisikan di mana?" → KOREKSI ATAS
    TEMUAN SENDIRI (pasca-compaction, baca-ulang AGENTS.md): §8A.3 BUKAN
    dangling — §8A = ANTI-LOOPING PENELITIAN, butir 3 = ronde tambahan
    DILARANG atas inisiatif AI, butuh persetujuan eksplisit user. Temuan
    awal SALAH (ditarik); definisi benar ditulis di §7. Pelajaran: verifikasi
    referensi ke file sumber SEBELUM tulis temuan.
  - B12 "Stall-count GUGUR = 1, dasarnya?" → §11-butir-(ii) menghitung
    ronde-tanpa-shortlist-positif; ronde-konfirmasi bukan ronde-shortlist.
    Ditulis sebagai INTERPRETASI TERCATAT (§11), bukan perubahan aturan.
  - Angka sitasi TERVERIFIKASI dari main (bukan dari ingatan): BAND_EDGES
    [1.5,2.0,2.5,3.0] (builder L117+assert L123); gate +0.1714/+0.1651
    n=522/992 (notebook L574); warmup-drop 87 event, n-vol 1427
    (notebook L1184); R1 (a)/(b)/(c) + forward-note (builder L70/notebook
    L1157-1158, L1229-1241); "arbitrer-jujur > tune-sembunyi" (§10 EDA-08).
  - B13 (pasca-audit, putusan user 2026-10-16 → kunci FINAL): H1–H4 +
    M1(opsi-A) + M2 DITERIMA dan masuk teks (§§2,3,5,6-F2/F4,7-P5,9,10).
    M3–M6/L1–L4 (audit-diri) DIAJUKAN-BELUM-DIPUTUS — tetap di file audit,
    BUKAN bagian kunci ini; butuh perintah amandemen bila ingin masuk.

## 13. Penguncian FINAL (2026-10-16)

User SETUJU FINAL dengan 6 temuan audit masuk: H1 tripwire-daya F2
(n-V < 500 + grup < 30 → STOP, bukan GUGUR); H2 split-H1/H2-deskriptif
(vonis imun pooled); H3 satu-seed-satu-run + p-4-desimal + caveat
0,04–0,06; H4 T_DAY = 1,7319 konstanta-V; M1 tanpa-floor-opsi-A
(argumen "geser gawang" ditarik); M2 caveat-penumpukan-V di §9.
Self-pass terakhir Commander sebelum kunci: famili-1 tertutup, cut-lock P3
koheren (F0 → 8 cut → V), null satu-arah terstratifikasi-band, vonis
satu-kata, label KONFIRMASI-V, P-segel tersentuh nol, stall-count sebagai
interpretasi tercatat — NOL cacat fundamental tersisa (maka tanpa audit
ronde-4, sesuai preseden EDA-08 §15). Blueprint TERKUNCI. Eksekusi
MENUNGGU perintah terpisah (§8A.3).

## 14. Amandemen-1 (2026-10-16, perintah eksplisit user)

Masuk: M3 (F0: STOP + diagnosis, "= ronde batal" ditarik — §6);
M4 (kolom first/gap/dow: hitung-boleh, lapor/tanya/narasi-jangan — §3);
M5 (sanity bar-M15-V, STOP-band <13k/>40k — §6-F1);
M6 (CI B=10000 + `reports/eda/2026-10-16-eda09/` + manifest — §8);
L1 (A2 exhaustive, bukan sampling — §6); L3 (deskriptif volume eksplisit
med/IQR/P1/P99 + cakupan + count-drop — §8); L4 (ambang 0,95 per bar-s —
§6-F1); sub-item M1 (unanimous-positive 4 band-R dikutip — §10).
DITOLAK/SKIP: L2 (presisi sitasi §12 — kosmetik, tak layak amandemen
sendirian; ikut bila ada amandemen lain).
Konsistensi-tercatat: B4 (§12, "split H1/H2 dilarang total") dibaca bersama
H2 + Amandemen-1 ini — larangan-total B4 DIGANTI split-H1/H2-preregistered-
deskriptif vonis-imun (§3/§7-P5). B4 tidak ditulis-ulang (rekam jejak
penalaran dipertahankan); yang mengikat = teks §3 + §7 + amandemen ini.
Sifat amandemen: klarifikasi + tripwire + kelengkapan spesifikasi; NOL
perubahan desain (famili-1, cut-lock, satu-arah, vonis-imun tak tersentuh).
Blueprint TETAP FINAL. Eksekusi MENUNGGU perintah terpisah (§8A.3).

## 15. Amandemen-2 (2026-10-16, perintah eksplisit "kunci + revert + jalan")

Latar: STOP-coder F0 2026-10-16 — assert `|recompute − 0.1682| < 1e-9`
gagal pada recompute yang BENAR. Verifikasi tiga lapis (coder → user →
Commander recompute independen): pooled repr `0.16818284622594523`
karakter-identik; `|pooled − 0.1682| = 1.7154e-05`; jangkar
1632/1514/460-391-231-432; per-band 0.1169/0.0687/0.1429/0.3264 (cocok
notebook EDA-08 sel 7); toolchain numpy 1.26.4/pandas 2.2.3/pyarrow 17.0.0.
Vonis: CACAT SPESIFIKASI (literal toleransi membandingkan presisi-penuh vs
publikasi-4dp — mustahil lolos), BUKAN fondasi goyang. Coder tepat STOP +
tepat tidak menafsir-ulang ambang sendiri.

Isi (mengikat, merujuk patch di §§header/3/6-F0/10):
(a) F0-assert = `round(pooled,4) == 0.1682` (+ ekuivalensi tercatat:
`|selisih| = 1.7154e-05 < 5e-5 setengah-ULP-4dp — konsisten, bukan assert
kedua); (b) 8 cut BEKU repr-penuh — b0 0.24647887323941978 /
0.47041420118341626; b1 0.1954397394136033 / 0.3721973094169312; b2
0.1717716422203372 / 0.33835948462822907; b3 0.16332011857566983 /
0.3379338240019312 (`_tercile_masks` verbatim EDA-08); F0 juga assert
kesamaan-persis 8 cut ini; (c) §10 dikoreksi 0.1169/0.0687/0.1429/0.3264 +
retraksi 1177/0701; (d) indikator concat + header tiga-keperluan (§3).
Sifat: koreksi-spesifikasi + pembekuan-angka; NOL perubahan desain.
Blueprint TETAP FINAL. EKSEKUSI DIPERINTAHKAN 2026-10-16 (satu seed,
satu run).
