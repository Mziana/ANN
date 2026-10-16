# Blueprint EDA-08 — ammo_round_R (FINAL 2026-10-15)

> Status: FINAL (dikunci 2026-10-15 atas persetujuan eksplisit user;
> klarifikasi warmup-volume §3 masuk sebagai syarat FINAL). BELUM BOLEH
> DIEKSEKUSI tanpa perintah eksekusi terpisah (§8A.3).
> Peran ronde: GENERASI di R (post-hoc diakui) — BUKAN konfirmasi.
> Konfirmasi = EDA-09 di partisi virgin. V/P DILARANG disentuh ronde ini
> (assert runtime).

## 1. Latar

EDA-07 (CLOSED c354d3b): Nunik=1632, band 515/415/240/462, full-room 1514
(460/391/231/432), L1 LOLOS 0.8223 [0.8029,0.8408], L2 GUGUR mean −4.23
[−5.10,−3.33]. Registry: #2 mag_cont (SMD −0.372), #3 has_exhaustion-terbalik
(exh 395 @0.5722 vs tanpa-exh 1119 @0.9106). Program: akumulasi 4–5 amunisi
terkonfirmasi-V; stopping rule §11.

## 2. Pertanyaan (terkunci)

- Q-joint (PRIMER, ESTIMASI — tanpa vonis): rate reversal-A per sel 4 band ×
  2 exh (8 sel) + CI95 cluster-per-day. Syarat: sel n<30 → point-only + tanpa
  simpulan (diharapkan tipis: band-2×exh).
- Q-wick (sekunder, klaim inkremental): apakah wick ratio menambah informasi
  SETELAH mag_cont diketahui? Statistik primer SATU: pooled within-band
  Δ = rate(tercil-wick-atas) − rate(tercil-wick-bawah), bobot-n per band,
  atas subset full-room. Null: permutasi NILAI wick dalam band (tercil dihitung
   ulang per permutasi, B=10000), p dua-arah. Robustness DI LUAR FDR (wajib
  lapor, dilarang klaim): Δ per band — pooled ≈ 0 dengan per-band heterogen
  = insight, bukan null (anti-penghapusan-Simpson). YEAR-GATE wick (koreksi
  ronde-7, temuan 1): Opsi A — hitung pooled Δ per tahun (2023H2, 2024),
  gate = tanda SAMA. Opsi B (Δ per band per tahun, 8 angka) DITOLAK tercatat:
  gate harus menguji statistik yang SAMA dengan yang lolos FDR; Opsi B
  meng-gate klaim yang tak pernah dibuat.
- Q-gap (sekunder, ekspektasi NOL): rate first-of-day vs non-first +
  gap ≤32 vs >32 bar (32 = 2× cooldown — KOREKSI audit ronde-6 atas cut 16:
  cooldown memaksa gap minimum 16, sehingga cut-16 memisahkan satu nilai
  tunggal vs rentang lebar = pisau tumpul)   sejak s-spike-sebelumnya se-hari.
  Famili uji: 2 (first-split, gap-split). FIRST-OF-DAY DI-EXCLUDE dari
  gap-split (koreksi ronde-7, temuan 3, Opsi B): event gap=INF hanya masuk
  first-split; gap-split = murni event NON-FIRST (n dilaporkan). Opsi A
  (INF → sisi >32) DITOLAK tercatat: mencampur efek first-vs-nonfirst
  (sudah diuji terpisah) ke dalam uji gap.
- Q-dow (sekunder, KILL-role, SATU uji omnibus): "adakah perbedaan rate antar
  hari Senin–Jumat?" Statistik = max_d|rate_d − rate_agg|. Null: permutasi
  label-dow antar event full-room (B=10000). Rate per hari tetap dilaporkan
  deskriptif (bukan uji). YEAR-GATE omnibus (koreksi ronde-7, temuan 2):
  statistik max-dev TAK PUNYA arah — gate = hari max-dev SAMA di 2023H2 dan
  2024 DAN tanda deviasi (rate_d − rate_agg) SAMA. Tahun dengan n<30 untuk
  hari max-dev itu → gate TAK DAPAT lolos (klaim gugur, tanpa pengecualian).
  SHORTLIST-SEMANTIK
  (koreksi ronde-7, temuan 4): dow-entry = klaim EKSISTENSI ("efek-dow ada",
  statistik omnibus yang sama) untuk konfirmasi-V; lokalisasi hari = ronde
  baru, BUKAN EDA-09. Hasil nol = SUKSES (pertanyaan terbunuh murah).
  (Penolakan tercatat: subset Senin+Jumat "karena literatur" DITOLAK tanpa
  sitasi — prior pintu-belakang; pilihan netral hanya semua-5 atau omnibus-1.)
- Q-vol (DEFINISI-LOCK, tanpa uji outcome): kunci SATU normalisasi volume dari
  kandidat §3 + laporkan SEMUA kandidat yang dicoba (termasuk yang dibuang +
  alasannya). Outcome-correlation boleh menginformasikan pilihan di R
  (tak mencemari V) — wajib dilaporkan jujur.

## 3. Definisi terkunci

- Populasi: event unik EDA-07 (Nunik=1632) + subset full-room 1514 untuk rate.
  REUSE parquet EDA-07 deterministik (assert 1632 baris + cocok kunci +
  band 515/415/240/462 + exh 395/1119). RESCAN DILARANG (scope violation → STOP).
- Wick ratio = 1 − |net|/range (kolom EDA-07 ada). Tercil dihitung DALAM band.
- Gap = i_sekarang − s_spike-sebelumnya (bar M15, se-hari); spike pertama =
  INF + flag first_of_day (warisi).
- Dow dari broker_day. Volume: tick_volume M15 (PROXY aktivitas — asumsi
  eksplisit, bukan fakta; FX desentralisasi). Kandidat normalisasi:
  (a) vol_bar-s / median-vol-sesi-sama-20-hari; (b) / median rolling-20d
  bar-yang-sama; (c) / median rolling-20d bar-yang-sama TANPA hari-berjalan
   (live-computable; varian inklusif-hari-ini DITOLAK di definisi karena butuh
  masa depan hari itu). Kunci satu di ronde ini. WARMUP-RULE (kunci FINAL
  2026-10-15, atas pertanyaan user): event di 20 hari pertama R DI-DROP dari
  evaluasi-volume (count dilaporkan), BUKAN expanding-median, BUKAN
  minimum-history — definisi yang dikunci harus satu aturan (median-20-hari),
  bukan dua; biaya ≈5% event dan hanya menyentuh analisis-volume (wick/gap/
  dow tak memakai volume). Berlaku seragam untuk (a)/(b)/(c). Forward-note
  EDA-09: histori baseline V boleh memakai hari-R (past-only, live-sah);
  definisi rasio IDENTIK.
- R = 384 hari bersih (warisi EDA-07). V/P: WHITELIST-ASSERT (koreksi ronde-7,
  temuan 7) — himpunan hari yang diload HARUS ⊆ manifest 384 hari-R warisan
  EDA-07; V/P tertolak otomatis tanpa perlu tahu tanggal batasnya.
  Monkey-patch I/O DILARANG (fragile). Gagal assert = STOP.

## 4. Hierarki & famili uji

- Estimasi (di luar FDR, tanpa vonis): Q-joint 8 sel.
- Famili FDR-BH q=0,10 (TERKUNCI, tepat 4 uji — daftar tertutup):
  wick-pooled (1) + gap-split (2) + dow-omnibus (1). Tahun-split = gate, BUKAN uji.
  Volume = 0 uji ronde ini. Joint = 0 uji (estimasi).
- Shortlist EDA-09 = klaim UJI (wick/gap/dow) yang lolos SEMUA: FDR-pass + arah konsisten
  2023H2 vs 2024 + |Δ|≥5pp (Δ = selisih rate relevan; ambang preregistrasi —
  lihat kalibrasi §10). EKSPLISIT (Opsi B audit ronde-6): gate 5pp SENGAJA di
  bawah daya uji; shortlist = KANDIDAT untuk eksekusi-V, BUKAN hasil final —
  V yang membunuh false positive. Opsi A (naikkan ke 6pp) DITOLAK tercatat:
  menggeser garis arbitrer tak menghilangkan arbitrariness; konjungsi + V
  yang bekerja, bukan angka garisnya. GATE-TAHUN PER UJI (koreksi ronde-7):
  wick = tanda pooled-Δ-per-tahun sama; first-split = tanda
  (rate_first−rate_nonfirst) sama; gap-split = tanda (rate_≤32−rate_>32,
  non-first saja) sama; dow = hari max-dev sama + tanda deviasi sama (§2).
  PENGECUALIAN EKSPLISIT: sel joint table BUKAN kandidat
  EDA-09 (estimasi, bukan klaim — V hanya untuk pertanyaan baru + volume).
  Shortlist BOLEH KOSONG (sukses-dengan-nol). Sensitivitas daya: Δ≈5pp di
  bawah daya tipikal uji tercil (~6–7pp) — null wick berbunyi "tak ada efek
  inkremental BESAR", BUKAN "wick terbukti sia-sia".

## 5. Null machine (permutasi terstratifikasi — donor-path DICABUT)

KOREKSI audit ronde-6 (temuan 5): donor-path permutation menguji hipotesis
  EDA-07 ("rate vs jalur acak"), BUKAN hipotesis EDA-08 ("fitur vs outcome").
  Donor-path keluar dari ronde ini sepenuhnya. Null untuk SEMUA uji =
  permutasi terstratifikasi (B=10000): nilai-wick dalam band (tercil dihitung
  ulang); label grup-gap; label-dow (statistik omnibus). STRATA = BAND untuk
  SEMUA uji (koreksi ronde-7, temuan 5): label grup-gap (first/non-first;
  ≤32/>32 dalam non-first) dan label-dow dipermutasi DALAM band — band
  adalah confounder terbukti (gradien 93→70); tahun BUKAN confounder
  terbukti dan ditangani via gate §4, bukan via null. Alternatif strata
  band×tahun dipertimbangkan dan DITOLAK tercatat (sel mengecil, menguji
  pertanyaan lebih tajam dari statistiknya). Seed BARU independen format YYYYMMDD-eksekusi, dicatat (alasan:
  resampling independen dari EDA-07; warisi disiplin F4, bukan angkanya).

## 6. Pre-flight coder (F-style)

- F0: reproduksi Nunik=1632 + band + exh-split + full-room 1514 dari parquet
  EDA-07 (reuse, bukan rescan). STOP bila gagal.
- F1: ketersediaan data — tick_volume ada di M15 parquet + terisi ≥95% pada
  bar-s event (bar-s = bar ANALISIS: kandidat volume §3 didefinisikan di
  vol_bar-s — cek di bar yang dipakai, bukan bar-i/agregat; koreksi ronde-7,
  temuan 6); dow derivabel. STOP bila gagal (volume turun ke "tertunda",
  BUKAN improvisasi proxy lain; KONTINJENSI: EDA-09 ditulis ulang di sekitar
  shortlist-uji saja — bila shortlist kosong DAN volume mati → program PAUSE
  untuk putusan user (pause, bukan akhir permanen — user memilih: pivot
  hipotesis lain / amunisi sumber berbeda / tutup program; ronde baru perlu
  perintah eksplisit §8A.3), dilarang auto-advance).
- F2: Q-joint exhaustive — jumlah 8 sel = 1514; margin band vs primer EDA-07
  rekonsiliasi. STOP bila gagal.
- F3: demo metode within-band pada 1 band (tercil + permutasi jalan). STOP.
- F4: seed baru tercatat. STOP bila tak tercatat.
- A-checks: A1 taksonomi per sel exhaustive; A2 tercil within-band exhaustive.

## 7. Gate & disiplin (warisi EDA-06/07 + pagar baru)

Prereg penuh; ambigu → STOP; assertion crash = bug; deterministik; notebook =
  artefak generator (exit 0); venv kanonik; arsip frozen; §8A.3. PAGAR BARU
  (temuan audit-diri §12): (P1) label generasi vs konfirmasi di tiap klaim;
  (P2) null-asimetri — null di R final, tak butuh V; (P3) lock-sebelum-V —
  EDA-09 mengunci konstruksi dari R SEBELUM sentuh V; (P4) larangan
  resurrection-L2 — ronde ini TAK ADA simulasi trade; fade tetap GUGUR.

## 8. Deliverables & Done

Generator `scripts/_build_eda08_ammo_R.py` + notebook
  `eda_08_ammo_R_explore.ipynb` + tabel joint (8 sel + CI) + tabel
  wick/gap/dow (termasuk Δ-wick per band sebagai robustness) + dokumen definisi volume terkunci + SHORTLIST EDA-09 tertulis
  (boleh kosong + alasan per kandidat) + section laporan "Label generasi" per
  tabel (tiap angka bertag generasi/konfirmasi — headline tanpa label = cacat
  laporan). Done = semua ada + F0–F4 hijau +
  shortlist eksplisit + label generasi di tiap klaim. Shortlist kosong =
  SELESAI SUKSES (bukan gagal).

## 9. Kompatibilitas ANN (tag live-computability, warisi EDA-07 §9)

Tiap kandidat wajib tag: mag/wick/exh/gap-time/first/volume = lagged-causal (butuh
  end-detector + live scan — SATU dependensi bersama, dicatat sekali, bukan per fitur);
  dow = exactly-live; volume-norm = live-jika-baseline-precomputed (syarat
  eksplisit). Joint rule = lookup stratifikasi, bukan fitur. TANPA tag =
  kandidat tak masuk shortlist (disiplin, bukan opsional).

## 10. Kalibrasi ketat-vs-longgar (jawaban eksplisit per gate)

- FDR q=0,10: longgar untuk vonis, TEPAT untuk filter-generasi (vonisnya di V).
  q=0,05 akan membunuh eksplorasi yang memang tugas ronde ini.
- |Δ|≥5pp: arbitrer TAPI preregistrasi (arbitrer-jujur > tune-sembunyi);
  sensitivitas dilaporkan (3pp/7pp) tanpa mengubah shortlist.
- Gate konsistensi-tahunan: KETAT — sadar membunuh efek rezim-spesifik.
  Tradeoff diterima: efek rezim = ronde rezim, bukan amunisi umum. Dicatat
  sebagai limitasi, bukan disesali.
- n<30 point-only: warisi EDA-07, konsisten.
- 4 uji tertutup: menambah uji di tengah = STOP + amandemen (pagar HARKing).

## 11. Stopping rule program (TERKUNCI, tulis sekarang)

Berhenti tambah amunisi bila: (i) himpunan terkonfirmasi-V = 4–5; ATAU
  (ii) dua ronde EDA berturut-turut tak menambah shortlist-positif.
  Null/kill murah = output sah, tak dihitung "gagal" untuk (ii).
  Continuation-mirror (spike-besar-lanjut) = PARKIR bernama (butuh spek
  sendiri; framing fade dilarang jadi asumsi permanen).

## 12. Jejak audit-diri Commander (bantai-draf 2026-10-15)

A1 "Joint = konfirmasi ganda" → resolusi: label estimasi + tanpa vonis (§2/§7-P1).
A2 "5pp arbitrer" → preregistrasi + sensitivitas lapor (§10).
A3 "Year-gate bunuh efek rezim" → tradeoff diterima + limitasi (§10).
A4 "q=0,10 longgar untuk ANN" → filter≠vonis; vonis di V (§10).
A5 "4 pertanyaan × 1632 event sama = overfit berlapis" → label generasi +
  regularisasi+segel-P di tahap ANN; tak ada klaim independensi (§7-P1).
A6 "Seleksi normalisasi-volume di R mencemari V" → TIDAK (seleksi tak sentuh
  V; uji-V tetap valid; syarat: semua kandidat dilaporkan) (§2-Qvol).
A7 "Ronde tanpa kill = sukses otomatis" → Done mensyaratkan shortlist
  eksplisit + alasan; kosong = sukses TERTULIS, bukan default (§8).
A8 "Rescan godaan" → reuse-assert + rescan=STOP (§3/§6-F0).
A9 "L2 resurrection via joint" → larangan eksplisit §7-P4.
A10 "Dow 5 uji + tahun-split = 15 uji sembunyi" → tahun = gate bukan uji;
  famili TERTUTUP 4 (wick 1 + gap 2 + dow-omnibus 1) — KOREKSI ronde-6:
  subset Senin+Jumat DITOLAK (prior tanpa sitasi); omnibus untuk peran-kill. A11 "tick_volume mungkin tak ada" → F1
  availability-gate, turun-tertib bukan improvisasi (§6).
A12 "ANN-compat klaim belakangan" → tag wajib pra-shortlist (§9).
A13 "dow-null campur donor-path" → null = permutasi label-dow; klaim lama
  dicabut (§5). A14 "joint diselundupkan ke EDA-09" → pengecualian eksplisit
  (§4). A15 "volume-(c) butuh masa depan" → varian inklusif-hari DITOLAK di
  definisi (§3). A16 "F1-gagal lalu apa" → kontinjensi berhenti-untuk-putusan
  (§6). A17 "gap-time tanpa tag live" → masuk lagged-causal (§9).
A18 "null wick dibaca sebagai vonis" → bunyi-null presisi (§4).

## 13. Jejak audit ronde-6 eksternal (2026-10-15)

Verifikasi klaim-vs-output EDA-07: 7/7 cocok, nol karangan (konkuren).
  DITERIMA: gap-cut 16→32 (floor cooldown); Δ-wick per-band robustness;
  Opsi B 5pp-eksplisit; pause-bukan-berhenti; null-stratifikasi + donor-path
  dicabut. DITOLAK TERCATAT: subset dow Senin+Jumat (alasan §2); Opsi A 6pp
  (alasan §4). Net: famili 8→4, §5 ditulis ulang, §6-kontinjensi presisi.

## 14. Jejak audit ronde-7 eksternal (2026-10-15)

Verifikasi 7/7 konkuren; penerimaan ronde-6 + kedua penolakan DIAKUI VALID
  oleh auditor. 7/7 temuan baru DITERIMA (nol penolakan): year-gate wick =
  Opsi A (§2/§4); year-gate omnibus = hari-max-dev-sama + tanda-sama (§2);
  gap-split = non-first saja (§2); dow-shortlist = existence-only (§2/§4);
  strata = band-untuk-semua, band×tahun ditolak tercatat (§5); justifikasi
  bar-s F1 (§6); whitelist-assert manifest-R (§3). Net: gate-tahun per-uji
  eksplisit (§4 tabel-in-prosa), §5 strata terkunci, §3/§6 presisi.

## 15. Penguncian FINAL (2026-10-15)

User SETUJU FINAL dengan satu syarat (warmup-rule volume §3: drop +
  count, expanding/minimum-history ditolak beralasan) — syarat MASUK di atas.
  Self-pass terakhir Commander sebelum kunci: joint-berlabel, famili-4
  tertutup, null-stratifikasi koheren, gate-tahun per-uji, dow-existence-only,
  whitelist-V/P, kontinjensi-pause, warmup seragam — NOL cacat fundamental
  ditemukan (maka tanpa audit ronde-4, sesuai instruksi user). Blueprint
  TERKUNCI. Eksekusi MENUNGGU perintah terpisah (§8A.3).
