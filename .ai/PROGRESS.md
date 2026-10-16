# PROGRESS.md — Milestone

**Update terakhir:** 2026-10-14 (R6 ditarik; kelas fixed-barrier M15 MATI-KELAS)

## Milestone 0: Setup Fondasi — SELESAI (100%)

- [x] Struktur folder
- [x] State files
- [x] Scripts (verify_claims.py, check_state.py, pipeline.ps1)
- [x] Configs (data.yaml, paths.yaml, logging.yaml, pyproject, requirements)
- [x] Setup.ps1 + run.ps1
- [x] Pre-commit hooks terpasang
- [x] AGENTS.md v3.0
- [x] RULES.md v2.0
- [x] PROMPTS.md v2.0
- [x] CONTEXT.md v1.3
- [x] Struktur jurnal + backtest
- [x] Environment (venv Python 3.12.8, 134 paket)
- [x] Git init + commit

## Milestone 0.5: Perbaikan Rumah (Phase A) — SELESAI

- [x] Fix `broker_timezone` -> UTC+3 di `configs/data.yaml`
- [x] Hapus BOM UTF-8 dari 27 file (0 tersisa)
- [x] Docstring Google Style untuk fungsi publik `verify_claims.py` + `check_state.py`
- [x] `.gitattributes` (text=auto eol=lf, ps1/bat crlf, biner)
- [x] Black dihapus, hanya ruff + ruff-format
- [x] Buat `docs/PROJECT_MAP.md`

## Milestone 1: Data Pipeline — SELESAI

- [x] Fetch data MT5 M1 per tahun -> `data/raw/M1/usdjpy_m1_<year>.csv`
- [x] Validasi data (gap, jumlah baris, duplikat, OHLC, spread) — **LOLOS 4 tahun**
- [x] Clean data -> `data/processed/M1/` (Parquet) — tanpa interpolasi
- [x] Simpan Parquet ke `data/processed/M1/` (1.347.847 bar, folder di-gitignore)
- [x] Resample M1 -> M5/M15/M30/H1/H4/D1
- [x] `src/features/build_features.py` (B1 TERTUTUP 2026-10-07) + `build_labels.py`
      (B2 TERTUTUP 2026-10-08)
- [ ] **Akhir Milestone 1**: pecah `validate_data.py` (431 baris terukur) jadi check
vs render — batas keras dari user. Batas ">600 baris" belum tersentuh, tapi
      batas "akhir Milestone 1" SUDAH lewat. Perluiputuskan: masih relevan atau
      resmi dicoret. MEMBUKA FILE NYATA.

## Milestone 2: Eksplorasi (EDA) — SELESAI

- [x] Distribusi return (nb01, 23/23 assertion)
- [x] Volatilitas per sesi (nb02, 30/30) + fragmen spread -> `configs/data.yaml`
- [x] Autokorelasi (nb03, 31/31) — klaim lama "|ACF| ≤ 0,012" DIBATALKAN (maks
      0,022639); sign-ACF lag-1 negatif di semua sel
- [x] Swing/level + placebo (nb04, 30/30) — TEMUAN NEGATIF: hit-rate reversal
      level (0,469-0,490) TIDAK melampaui placebo (0,499-0,505)
- [x] Regime + laporan EDA (nb05, audit LULUS DENGAN SISA 1 LOW)
- [x] Biaya & breakeven (nb06) + label-fitur + I-1 + I-2 (EDA-07)
- [x] EDA-07 spike_anatomy_outcome CLOSED+MERGED 2026-10-15 (c354d3b): Nunik=1632, L1 LOLOS (rev 0.8223, bawah-CI 0.8029), L2 GUGUR decisif (mean -4.23 CI [-5.10,-3.33]); jalur fade-spike DITUTUP; amunisi #2 (mag_cont) + #3 (has_exhaustion-terbalik) masuk registry sebagai KANDIDAT
- [x] Pengukuran spread aktual per sesi -> `spread.cost_basis` / `spread.stress_bands`

## Milestone 3: Metode — IN PROGRESS (blokir persetujuan user)

- [x] Hipotesis H1-H5 dipra-registrasi + vonis (lihat "Update 2026-10-13" bawah)
- [x] Uji kandidat H1-H5 + H3 + H4b (semua divonis; lihat ringkasan)
- [x] Register 68 LOLOS / 35 GUGUR (TABEL M3, EDA-07 L3-1)
- [x] Vonis B-4 = **GO cabang (a)**: lanjut ke spec pemodelan pra-registrasi
      (BUKAN paper-trade)
- [x] **Spec Discovery-R1 ditulis + DIRATIFIKASI user (R-1..R-7)**
      2026-10-13 — `reports/governance/2026-10-13/arsitek/`
- [x] **Audit auditor atas spec = GAGAL** 2026-10-13 (3 HIGH H1/H2/H3 +
      6 MEDIUM + 5 LOW; ketiganya benar terverifikasi arsitek ke teks spec)
- [x] **Amandemen-1 diterapkan** (paket A-A-Kunci disetujui user):
      D-4.2 tanpa konteks primer, setting beku H+10/TP2,5/SL2,5 + kriteria
      KANDIDAT 4-syarat, D-8.2 bar M15 terakhir selesai, D-8 otoritas R-7,
      entry open t0+1, literal config + slippage ASUMSI, denominator beku,
      E1 bersarang / E2-E3 satu-sel diakui, D-13 re-audit fokus
- [x] **Re-audit fokus = LULUS ketiga butir (H1/H2/H3)** 2026-10-13
      (sitasi diverifikasi arsitek; tanpa cacat fatal baru; 5 catatan
      C1–C5 non-blocking) — spec + Amandemen-1 SAH sebagai basis eksekusi
- [x] **Amandemen-2 diterapkan** (disetujui user paket 2026-10-13):
      seed 1337 beku, family E1=6/E2=1/E3=1, tanpa p-value, segel
      lampiran, resample.py — spec 421 baris SAH penuh
- [x] **Coder discovery 2024 PULANG: TOLAK-sementara E1/E2/E3**
      2026-10-13 (evidence 13 file, urutan pra-run benar, koheren internal)
- [ ] **Replikasi auditor dari nol** (brief disusun, menunggu user paste)
- [ ] Vonis final arsitek TOLAK/KANDIDAT/BELUM JELAS (setelah replikasi)
- [x] **Spec Discovery-R2 ditulis + DIRATIFIKASI paket (R2-1..R2-6)**
      2026-10-13 — event E1/E2/E3 + barrier ATR k1,5/RR2,0 + bed
      2026-holdout (269.846 bar minus anomali 19.119)
- [ ] **Audit auditor atas spec R2** — PULANG 2026-10-13: CATATAN
      (B1/B3/B5/B6/B8 LULUS; B2/B4/B7 GAGAL wording; C1–C5 catatan)
- [x] **Amandemen-R2-1 diterapkan** 2026-10-13 (disetujui user paket):
      3 perbaikan + 5 pengetatan, tanpa perubahan angka
- [x] **Re-audit fokus auditor atas Amandemen-R2-1 — LULUS 8/8**
      2026-10-13 (hash spec C05D5E4F…654C5 cocok; tanpa cacat FATAL;
      2 catatan kosmetik tanpa amandemen; prasyarat coder TERPENUHI)
- [x] **Coder discovery 2026-holdout PULANG: TOLAK-sementara 8/8**
      2026-10-13 (median −1,32..−1,72; TIME-share 0,71–0,84; E3
      n_eval=507; 2 run identik; evidence 12 file + urutan pra-run
      + koherensi exact terverifikasi; J1–J5 TERIMA SEMUA)
- [x] **Replikasi auditor R2: LULUS tanpa arbitrase** 2026-10-13
      (7/7 butir COCOK; median/CI/paruh identik ~1e-12; satu-satunya
      selisih 5 event E2 = FP < 1 ULP, terbukti; C-R2-1..C-R2-7
      non-blocking dicatat)
- [x] **VONIS FINAL R2: TOLAK E1/E2/E3** 2026-10-13 (0/8 sel lolos
      4-syarat; segel D-8 tetap tertutup; pertanyaan barrier-ATR
      jalur event-first DITUTUP)
- [ ] Draf `spesifikasi-fingerprint.md` DIPENSIUNKAN (arsip)
- [x] **P2-flipmurni SELESAI 2026-10-14: KALAH 8/8** (jalur flip ditutup;
      med stacked -1,52..-1,89; replay 1-posisi negatif semua sel)
- [x] **R4-M15-native SELESAI 2026-10-14: TOLAK 9/9 sel** (M15 sebagai basis,
      ambang ATR bukan pip, bed 2024; audit independen nol bug material;
      E1 proven berarah terbalik, E2/E3 netral-arah)
- [x] **R4 audit addendum 2026-10-14**: definisi WR direvisi (TIME dihitung
      sebagai posisi untung/rugi saat timeout); impas nominal keliru, impas
      observatif nyata 37,5–47,8%; cacat quote TIME SELL di BID
- [x] **R6-conditioning DITARIK 2026-10-14: NON-EXECUTABLE** — 4 cacat FATAL
      + 2 blocking dari audit independen; spec tidak pernah dijalankan.
      39/52 bin mati struktural oleh n; ambang `Edge >= 0,56` terbukti tidak
      cukup (sel Edge_B 0,602 tetap rugi)
- [x] **Kelas hipotesis fixed-barrier M15: MATI-KELAS** — 0/9 sel significantly
      positif, 5/9 significantly negatif pada realized breakeven dengan CI
      cluster-per-hari. Conditioning belum diuji dengan probe valid.
- [ ] Spesifikasi Metode Target v1 (definisi sukses trading) — setelah Discovery-R1

## Milestone 4: Baseline Model — BELUM DIMULAI

- [ ] Rule-based
- [ ] Logistic regression
- [ ] Modul `src/models/`, `src/backtest/` belum ada (terverifikasi 2026-10-13)

## Milestone 5: ANN

- [ ] MLP
- [ ] Walk-forward validation

## Milestone 6: Backtest

- [ ] Spread + slippage + komisi (WAJIB, tanpa itu tidak valid)
- [ ] Bid/ask handling benar (RULES.md §18.16)
- [ ] Stress test

## Milestone 7: Paper Trading (Fase 1)

- [ ] 500+ trade data

## Milestone 8: Graduation (Fase 2)

- [ ] 100 trade simulasi limit

## Milestone 9: Live (Fase 3)

- [ ] Modal kecil

## Kemajuan Fase B — Data (per 2026-10-05; angka dikoreksi 2026-10-13)

- [x] Fetch MT5 M1 2023-2026 -> 1.347.847 bar CSV (raw, immutable)
- [x] `fetch_data.py` — timezone UTC+3, spread POINT vs PIP, epoch mentah
- [x] `validate_data.py` — 0 error, 5 peringatan, 4 tahun
- [x] `clean_data.py` — Parquet **1.347.847 bar, 0 gap diisi** (angka lama
      "1.349.857 bar, 2.010 gap terisi" dari SEBELUM keputusan D1 2026-10-05
      yang menghapus interpolasi — sudah usang, lihat "Catatan clean_data" TASKS)
- [x] `resample.py` — M1 -> M5/M15/M30/H1/H4/D1

Jumlah test: **angka terakhir yang tercatat = 147 hijau (per 2026-10-05)**, lalu
bertambah di ronde berikutnya. TIDAK di-run ulang pada 2026-10-13 (rekonsiliasi
ini read-only) — jadi "147" bukan angka terkini, jangan dikutip sebagai gospel.

### Update 2026-10-05 (audit Phase B)

- [x] 8 temuan diperbaiki, 5 dibatalkan atas bukti data
- [x] Validasi data nyata: exit 0, 2023 kini WARN karena spread p99 8,50 pip
- [x] 120 test hijau, pre-commit 12/12

### Update 2026-10-07 (batch newline + M1 + commit)

- [x] F-NL + F-NL2 ×5 builder, regen nb05 (81.851 B, 0 CR, 68/68 assertion),
      FIG-04..07 hash identik pin, diff ternormalisasi kosong + 9 baris chunking
      terdisposisi
- [x] Re-audit F-NL/F-NL2 TERVERIFIKASI TUTUP; temuan baru M1 (MEDIUM,
      provenance "era CRLF" salah kausal) diperbaiki ×4 dokumen + re-audit
      TERVERIFIKASI TUTUP
- [x] Commit `43e2a07` (37 file, semua hook hijau); Batch C: 0 MEDIUM + 4 LOW
      terbuka (B8-01/B10-01 dikecualikan, L2-01/L2-02 catatan)

### Update 2026-10-07 (penguncian hipotesis H1–H5)

- [x] Review redaksi H1→H5 oleh user (H1 ditahan untuk tanya arsitek
      reversal-day → putusan opsi iii: kunci + catat risiko + klausul
      anti-penyelamatan)
- [x] Putusan arsitek: H1 KUATKAN, H2–H5 TERIMA bersyarat S1–S8
      (H3 vonis TERBUKA sampai S4; H2 pra-registrasi strategi; H4 dua "6 jam"
      terpisah; H5 koreksi multiplicity), H6+ DITOLAK
- [x] Dokumen `hipotesis_lock_v1.md` + `putusan-arsitek-H1-H5.md`;
      commit `0107a56` (2 file, semua hook hijau)

### Update 2026-10-07 (fondasi fitur B1 + rantai audit TERTUTUP)

- [x] `build_features.py` 400/400 + 37 test, parquet `07402f40…` identik objek
      audit; audit fondasi 0 HIGH/1 MEDIUM/3 LOW → putusan arsitek B1 + F-1
      tersimpan → F-2/F-3/F-4 → re-audit → R1/R2/R3 → konfirmasi 3×YA
- [x] Residual berdiri: #4/#5/#7 + materialitas H1/H5 (BELUM DIUJI);
      headroom nol → B2 wajib buka dengan rencana split

### Update 2026-10-12 (EDA-07 I-2 selesai, coder)

- [x] Full-run I-2 (mandat V-6): 260 pasangan (60 LA + 200 waktu), verdict
      G1-G4 penuh fitur asli = 98 LOLOS / 162 GUGUR; irisan 29/37;
      regresi kontrol 86/86 + 780/780 identik beku; 7 kandidat round_d V-5
      dinilai (5 LOLOS Tokyo efek INVERS + 2 GUGUR London, G4=NA);
      T-07-1..4 + FIG-13..16 + KESIMPULAN_I2 terkunci (ASSERT_LOG 569);
      13/13 file beku hash sama; HEAD `b18992b`, nol stage/commit.
      Laporan `reports/eda/2026-10-12/laporan-coder-eda07-i2.md`.
      Berikutnya: AUDITOR independen, arsitek putusan Lapisan 3.

### Update 2026-10-12 (EDA-07 L3-0 selesai, coder)

- [x] Peta arah L3-0 (S3-1 deskriptif, tanpa model): 153 baris G3-pass
      (120 pos/33 neg) -> T-L3-0_arah.csv + FIG-17 per sesi x horizon;
      98 LOLOS native (verdict verbatim) -> T-L3-0_peta98.csv
      (arah pos 78/neg 20, diff himpunan kosong); 5 Tokyo INVERS menempel;
      2 kandidat London gugur sbg round_d (target LOLOS via wakil asli);
      manifest hash 6/6 + runner-log EXITCODE=0; KESIMPULAN_L30 terkunci
      (ASSERT_LOG 343); beku untouched. Laporan
eports/eda/2026-10-12/laporan-coder-eda07-l30.md.
      Berikutnya: AUDITOR independen L3-0, arsitek putusan buka L3-1.

### Update 2026-10-12 (EDA-07 L3-1 STOP pra-eksekusi, coder)

- [x] S-0 read-only -> konflik B-3: M3 Brier+akurasi+mayoritas tak terdefinisi
      untuk 36/103 pasangan kontinu LB_rng (YPOS/YCODE=None verbatim run 9).
      STOP + lapor per S-0.4; nol artefak M3. Laporan
      `laporan-coder-eda07-l31-konflik-B3.md`. Berikutnya: AMANDEMEN ARSITEK B-3.

### Update 2026-10-12 (EDA-07 L3-1 SELESAI, coder)

- [x] Eksekusi L3-1 pasca-Amandemen C via `scripts/_build_eda07_l31.py` ->
      `notebooks/scalping/eda_07_l31_baseline.ipynb` (8 sel, 0 error, EXIT=0).
      TABEL M3 103 pasangan terkunci: LOLOS 68 / GUGUR 35 (diskret 56/11 via
      Brier; kontinu 12/24 via MSE). Jangkar T-07-1 200/200; register 98+5;
      C-3 twin 5 round_d identik native; split max-train<min-test; hash 5/5
      input sama; S8B 11/11 utuh; ASSERT_LOG 1268; KESIMPULAN_L31 terkunci.
      3 perbaikan builder terdokumentasi (FIG-18 kolom, `)` berlebih, C-3 twin
      posisi-register). T-5 menandai 12 baris / 7 target. FIG-18 dua panel.
      Laporan `reports/eda/2026-10-12/laporan-coder-eda07-l31.md`.
      HEAD `b18992b`, staged nol ronde ini.
      Berikutnya: AUDITOR independen L3-1, arsitek putusan + vonis dagang.

### Update 2026-10-13 (reaudit L3-1 LOLOS PROSEDURAL + brief vonis B-4)

- [x] Reaudit L3-1 LOLOS (B091A4FC, 452 baris dibaca penuh):
      11 mandat (a)-(k) nol selisih; 0 TINGGI/0 MENENGAH/4 RENDAH
      (format, nol dampak)/4 INFORMATIF; R1 TERIMA catatan log;
      R3 asumsi EOL-manifest jadi FAKTA reproducible; S6 jujur.
      Gerbang LOLOS (`2026-10-13_gerbang-reaudit-l31.md`).
- [x] Brief vonis B-4 arsitek terbit
      (`2026-10-13_putusan-l31-arsitek.md`, V-1 biner + V-2 + V-3 + V-4).
      Menunggu user paste -> `putusan-l31-final.md` -> GO/NO-GO (S8A).

### Update 2026-10-13 (VONIS B-4: GO cabang (a), ronde L3 DITUTUP)

- [x] Vonis arsitek (dirangkap asisten, S1A; brief eksternal MOOT):
      `arsitek/putusan-l31-final.md` (81 baris, SHA256 `EA1BC4FD...`).
- [x] V-1 GO = minta persetujuan user utk spec pemodelan
      pra-registrasi (BUKAN paper-trade; 5 syarat incl. skrutini
      LB_bin 25/25). V-2 register 68 beku / 35 tutup.
- [ ] Menunggu persetujuan eksplisit user (S8A butir 3) sebelum
      ronde spec pemodelan.

### Update 2026-10-13 (rekonsiliasi dokumentasi, read-only)

- [x] Baca penuh: README, STATE, CONTEXT, TASKS, PROGRESS, SESSION_LOG,
      `putusan-l31-final.md`, `spesifikasi-fingerprint.md`, dokumen desain
      9 Okt (613 baris)
- [x] Empat file state dikoreksi agar tidak saling bertentangan:
      TASKS (metadata + checkbox usang + Blocked), PROGRESS (metadata +
      Milestone 1-4 + angka Fase B), CONTEXT (versi/tanggal + fase +
      spread + keputusan + §12), STATE (arsip + Yang Belum + Langkah)
- [x] Temuan dokumentasi konkret (semua sudah dikoreksi di file):
      README masih sebut "fingerprint masih draf" -> jadi **DIPENSIUNKAN**;
      STATE bagian lama punya "Langkah Berikutnya" yang menunjuk EDA-04 (sudah
      selesai 2026-10-06); CONTEXT masih "Fase 1 Training" + "metode menunggu
      EDA" (keduanya sudah lewat); TASKS/PROGRESS metadata tertinggal 2026-10-07
- [x] Konfirmasi empiris saat rekonsiliasi: `src/` = 8 modul/2.035 baris
      (bukan 0 byte); `models/`+`backtest/` memang belum ada;
      `.env.example` masih 0 byte; HEAD `2112f94` == `origin/main`

### Update 2026-10-15 (fix M1-M5 kontrak broker + self-audit 3x, TERTUTUP)

- [x] M1 angka spread di `configs/broker.yaml` + `docs/broker-contract-finex.md`
      ditulis ulang dari hitung independen; spike 55,60 dipindah dari Sydney
      ke NewYork (ternyata 2024-12-24)
- [x] M2 `EDA/README.md` - 5 nilai dolar terinterpolasi PowerShell dipulihkan
- [x] M3 `EDA/02-volatility.md` - status keputusan lama ditandai sudah diterapkan
- [x] M4 section konflik spread basi ditulis ulang sebagai tertutup
- [x] M5 provenance angka "68 assertion PASS" ditambahkan
- [x] X1 3 kata tergarbling (`hariWednesday`, `bisabisa`, `terHopital`)
- [x] X2 7 karakter Mandarin bocor ke teks tulisan sendiri (U+5E74, U+7528/U+6237,
      U+6839/U+6E90, U+5C5E/U+6027) - semua dibetulkan
- [x] Gate baru: 80 pemeriksaan dokumen-vs-data, 0 gagal
- [x] Negative control gate: 3 angka dikorup -> 3/3 tertangkap (gate terbukti berguna)
- [x] Regresi 254/254 passed · `git diff --check` bersih · YAML valid
- [x] Self-audit 3x adversarial selesai; 6 cacat di kerja sendiri terdokumentasi
- [x] Komisi per side vs round-turn - SELESAI 2026-10-15, user konfirmasi
      **$1,00/lot per sisi** (= $2,00 round-turn); blocker biaya dihapus
- [x] Spec kontrak Finex - SELESAI 2026-10-15: kontrak 100.000, base USD,
      pip 0,01, min 0,01, maks 50 lot/order, leverage 1:500 (user) +
      cocok silang anchor EDA-06
- [ ] Keputusan arsitek: samakan konsumen `broker.yaml` vs turunkan jadi dokumentasi

Catatan metodologi: verifikasi pertama sempat memakai `add_labels()` - fungsi
yang SAMA dengan notebook, jadi hanya membuktikan determinisme. Ditulis ulang
independen dengan `zoneinfo` + `numpy.quantile` + kolom `spread_pips` mentah.

### Update 2026-10-15 (blueprint EDA-06 v9.3 FINAL + brief coder, menunggu Pre-Flight)

- [x] Blueprint EDA-06 `candle_anatomy_regime` FINAL v9.3 (10 iterasi v8.1->v9.3,
      tiap putaran diaudit adversarial + counter-audit; semua klaim counter
      terakhir diverifikasi hitungan: 2 benar+1 temuan tambahan, 1 salah, 1 setuju).
      File: `thoughts/shared/designs/2026-10-15-eda06-blueprint-v93.md`
- [x] Keputusan terkunci: biaya 0,95 pip flat (spread x1 + komisi x2; rumus lama
      spread x2 = hitung ganda, DICABUT) · Net TP min 2,85 · R:R >=1,0 momentum
      saja · OR = 4 bar M15 setelah daily open (referensi sesi DIHAPUS) ·
      trigger >= bar ke-5 · K=16 setelah entry · partisi R + minus 19 hari anomali ·
      placebo 1000 set x 2 track (reversal dir dari sisi open, momentum coin flip;
      SL identik via pseudo extremes N=3) · FDR core {1,2,3,4a1} q=0,10 ·
      power rule CI mean > 5 pip · side-consistency 'wrong_side' (real + placebo)
- [x] Brief coder diterbitkan (Pre-Flight Cek 1-6 sebagai gate; reuse
      `broker_time`/`resample`; venv kanonik; arsip 06-07 frozen)
- [ ] Pre-Flight Checklist coder — MENUNGGU coder (belum ada laporan masuk)
- [ ] Penyelarasan biaya repo ke 0,95 (broker.yaml skenario mid 1,60 + docs +
      CONTEXT §15 masih rumus lama) — PENDING, belum dieksekusi
- [x] Pre-Flight coder MASUK (3 blocking, semua BENAR): F1 jam [21,22] vs data —
      DST audit 2026-10-05 (`data.yaml:271-281`) + ukuran coder 255@22/129@23/0@21
      → open normal = [22,23], 21 = tanda anomali · F2 ambang mikro mustahil
      (min terukur 1,37/0,59) · F3 Sel 1/2/3 memang tak pernah didefinisikan
- [x] Putusan arsitek + Amandemen-1 diterbitkan (A1/A2/A3 + Sel 1 tetap diuji,
      Sel 3 diprediksi UNDERPOWERED) — MENUNGGU ratifikasi user 3 butir
- [x] Anggaran data: R pakai 384 (pertama); sisa 441 bersih (V 2025 = 259,
      P 2026 = 182) utk walk-forward (V) + OOS kunci (P); H1-2023 stratum B
      dikecualikan (stress saja)
- [x] Amandemen-1 TERBIT (`thoughts/shared/designs/2026-10-15-eda06-amandemen-1.md`):
      A1 YA · A2 modif-user (split 4a1t/4a1s, core 5 sel, trending=komplemen,
      null regime-matched, Cek 4 direvisi) · A3 YA (hipotesis cadangan)
- [ ] Nod A4 + lampu hijau LANGKAH 2 — MENUNGGU user
- [x] A4 DIPUTUS (modifikasi user, benar): FS-01→V (bukan P — P pristine,
      satu sentuh test ANN-01); hierarki R-terkunci / V-workhorse / P-segel
- [x] LAMPU HIJAU LANGKAH 2 (2026-10-15): coder jalan, blueprint v9.3 + Amandemen-1
- [x] Blueprint v9.4 = konsolidasi IDENTIK (kanonik tunggal; grep: nol angka lama di aturan aktif)
- [ ] LANGKAH 2 coder BERJALAN: notebook Sel 1–7 + event parquet + vonis §8A per sel
- [x] LANGKAH 2 SELESAI + vonis CLOSED: Sel 1 UNDERPOWERED (n=51, +4.33,
      CI [−5.50,+15.51] lebar 21; win 0.27, +45.0/−13.8, ekor −99.75) ·
      Sel 2/3/4x TIDAK TAHU (12/0/3/7/2/20) · nol core LOLOS → TIDAK LANJUT TV-01
- [ ] Commit 3 artefak aditif — MENUNGGU user
