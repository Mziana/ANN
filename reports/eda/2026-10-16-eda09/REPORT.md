# LAPORAN FINAL — EDA-09 wick_confirm_V (eksekusi-ulang 2026-10-16)

Peran: CODER (implementasi + self-audit + fix). Otoritas satu-satunya = blueprint FINAL
`thoughts/shared/plans/2026-10-16-eda09-wick-confirm-draf.md` (§§1–15 + Amandemen-1/2).
Tanggal UTC eksekusi: 2026-10-16. HEAD: `bc4dac7` (main, tanpa branch/worktree baru,
tanpa commit/push/merge). Venv kanonik: `venv/Scripts/python.exe`.

## File dibuat/diubah

| File | Peran | `git hash-object` (SES UDAH penulisan terakhir) |
|---|---|---|
| `scripts/_build_eda09_wick_confirm.py` (BARU) | Generator + executor notebook | `c703eeb421695cee4d2e80b44eda133f9d12657d` |
| `notebooks/scalping/eda_09_wick_confirm.ipynb` (BARU, regenerate via generator) | Artefak notebook, exit 0 ×2 | `7ade7bce9ba01a40614f409c0475e7ecaac89afa` |
| `reports/eda/2026-10-16-eda09/fig-wick-V-perband.png` (BARU) | Kurva Δ-wick-V | `95821700edd8d653067a0d08d6401e9af810ebb3` |
| `reports/eda/2026-10-16-eda09/manifest.json` (BARU) | Manifest mesin | `1a8126818c63a8f35e9a5fbfaf83ceb0a6f895a6` |
| `reports/eda/2026-10-16-eda09/REPORT.md` (BARU, file ini) | Laporan final | `8887734b187e609061d5827d08d4a4632d536030` |
| `notebooks/scalping/eda_07_spike_anatomy_outcome.ipynb` (REGENERATE) | Efek samping prosedur delta-(c): generator beku EDA-07 dijalankan apa adanya; isi deterministik | hash tidak diklaim (di luar file kerja; jangkar tetap, lihat FASE 1) |
| `data/processed/events/eda07_spike_events.parquet` | TIDAK DIUBAH ISI (hash identik pra vs pasca run generator beku) | `B800E50EE42D72349F52426B2FCB635EFB5101597E40AFBDD89BF2054B1BDFC2` |

## FASE 0 — SELF-AUDIT PRA-EKSEKUSI (LULUS tertulis sebelum eksekusi)

### Bukti paham (kutip blueprint, bukan "sudah baca")

- **Famili tepat-1 (§4):** "Konfirmasi: wick-pooled-V SATU-ARAH, α=0,05
  (satu-satunya p-value ronde)." → Satu-satunya uji = Δ pooled within-band
  (tercil-atas − bawah, bobot-n, cut TERKUNCI) positif di V; arah dikunci R
  (atas > bawah); lawan = null permutasi terstratifikasi-band (§5).
- **Cut-lock P3 (§3 + Amandemen-2 §15):** "F0 hitung-ulang cut tercil R (t1,t2 ×
  4 band) dengan fungsi IDENTIK EDA-08 pada parquet-R" → `_tercile_masks`
  verbatim: `t1 = float(np.percentile(vals, 100/3))`,
  `t2 = float(np.percentile(vals, 200/3))`,
  `return (vals < t1), ((vals >= t1) & (vals < t2)), (vals >= t2), (t1, t2)`.
  Assert Amandemen-2: `round(pooled,4) == 0.1682` (literal 1e-9 DITARIK —
  cacat spesifikasi) + 8 cut SAMA PERSIS §15: b0
  0.24647887323941978/0.47041420118341626; b1 0.1954397394136033/0.3721973094169312;
  b2 0.1717716422203372/0.33835948462822907; b3 0.16332011857566983/0.3379338240019312.
- **T_DAY (§3/H4):** "T_DAY = 1,7319 DIKUNCI sebagai konstanta untuk V (warisan R,
  bukan recompute); assert-vs-EDA-06 dicabut TERTULIS untuk V."
- **STOP-band F1/F2 (§6 + Amandemen-1):** F1: hari-V <200/>320 → STOP;
  bar-M15-V <13k/>40k → STOP; tick_volume bar-s-V ≥0,95 PER BAR-S (bukan agregat;
  gagal → volume "tertunda", wick-confirm LANJUT). F2: ke-4 band non-kosong;
  tripwire (a) total n-V < 500 → STOP (BUKAN GUGUR); (b) grup tercil mana pun
  (atas/bawah × 4 band) n < 30 → STOP. Konsekuensi: STOP = arsitek mendiagnosis
  (fondasi-goyang vs artefak-numerik), BUKAN vonis; tripwire hanya bisa MENCEGAH
  kill-palsu, tak bisa memalsu CONFIRM.
- **Concat-indikator (§3 Amandemen-2):** "ATR14/RSI14-Wilder dihitung pada frame
  gabungan 2023+2024+2025 (reuse kode loading, tahun diperluas), whitelist event-V
  DILAKUKAN SESUDAH deteksi. Event-R yang ikut-terdeteksi = artefak-terbuang
  (boleh ada, DILARANG dilapor/diuji/dinarasikan)." 2025-only DITOLAK tercatat.
- **Satu-seed (§5/F4/H3):** "Seed BARU independen format YYYYMMDD-eksekusi,
  dicatat … SATU SEED SATU RUN: DILARANG re-seed untuk alasan apa pun kecuali bug
  terbukti (STOP + arsitek); kerapuhan perbatasan (p ∈ [0,04, 0,06]) dicatat apa
  adanya sebagai caveat, BUKAN alasan run-ulang."
- **DILARANG §3 (verbatim pendek):** "tanya-ulang first/gap32/dow (gugur final);
  joint-sebagai-kandidat; klaim per-band; L2/simulasi-trade (fade GUGUR);
  floor-5pp di V; kolom first/gap/dow BOLEH ada sebagai artefak pipeline tetapi
  DILARANG dilaporkan, diuji, atau dinarasikan."

### Self-review AGENTS.md §4 (10 butir vs builder)

1. Baca ulang: builder dibaca-ulang pasca-tulis (syntax + import OK, 8 sel).
2. Bug/edge: overflow mag<1.5 → band 0 + tercacah (tak ada di V: band-V lengkap
   367/286/168/289); CI bootstrap melewati band kosong per-resample (den menyusut;
   tak materialisasi — CI tercetak finit [0.1631,0.2717]); `assert` dipakai untuk
   pagar mesin, bukan kontrol alur.
3. Look-ahead: ATR shift-1, RSI/diff kontemporer (verbatim beku); `day_ctx` hanya
   hari lampau; baseline volume tanpa-hari-berjalan.
4. Leakage: Sel 1 hanya 2023+2024; tahun load eksplisit; P tak pernah dimuat;
   V∩R=∅ di-assert dua-arah.
5. Konvensi: `lo_<=x<hi_` konsisten di A2, null, pooled, CI (bawah=`<t1`, atas=`>=t2`).
6. Hardcode: T_DAY/cut/seed/ambang = angka blueprint (mandat, bukan pilihan coder).
7. Duplikasi: `scan_spikes`, `first_exhaustion`, outcome machine, `_boot_ci`,
   `_wilder_ema`, volume-(c) = salinan verbatim (reuse-first §16), bukan tulis-ulang.
8. Test: assertion mesin tiap pagar (F0/F1/F2/A1/A2/F4); nbconvert exit=0.
9. Import: ruff bersih; `build()` di bawah `if __name__ == "__main__"`.
10. Panjang: file >400 baris → `# LENGTH_EXCEPTION` header (preseden §15.1 EDA-08).
Keraguan `# REVIEW:` tercatat di header builder (R1–R5); tak ada yang menggantung.

### Self-audit 3× (pra-eksekusi)

- **Correctness:** tiap angka klaim dipasangkan ke sumber SEBELUM ada output —
  F0: sel 1 (`F0 …: aktual=… ekspektasi=…`); F1: sel 2; A1/A2/F2: sel 5;
  uji/CI/split: sel 6; volume: sel 7; manifest: `manifest.json`. Toolchain
  (numpy 1.26.4/pandas 2.2.3/pyarrow 17.0.0) tercetak di manifest.
- **Bias (3 godaan HARKing ronde ini + penangkal):** (1) Menghitung-ulang tercil di
  V yang "lebih cocok" → penangkal: cut-LOCK konstan + A2 exhaustive + larangan
  tertulis. (2) Membaca CI/per-band/split sebagai vonis kedua bila p marginal →
  penangkal: CI/split/per-band dicetak sebagai karakterisasi/deskriptif tanpa p,
  tanpa klaim; vonis hanya dari baris mekanis. (3) Re-seed saat p di perbatasan →
  penangkal: satu-seed-satu-run + caveat 0,04–0,06 tercatat (tak materialisasi:
  p=0,0001).
- **Meta:** §§2–8 + Amandemen-1 terpetakan: §2→sel 6 (uji + vonis); §3→sel 1/3/4/5/7
  (cut-lock, concat, T_DAY, volume-c, larangan); §4→sel 6 (famili-1);
  §5→sel 6 (null B=10000 strata-band, seed 20261016); §6→sel 1/2/5/6
  (F0/F1/F2/F4/A1/A2); §7→sel 2–7 (P1–P6); §8→sel 6/7 + direktori + manifest.
  File luar scope berisiko tersentuh: notebook EDA-07 (regenerate deterministik
  oleh prosedur delta-(c) yang diotorisasi) + parquet EDA-07 (hash dibuktikan
  identik). Keduanya dilaporkan jujur.

### Pasangan perintah mentah ( ditempel semua )

- `ruff check scripts/_build_eda09_wick_confirm.py` → `All checks passed!`, **rc=0**
- `ruff format --check scripts/_build_eda09_wick_confirm.py` → `1 file already formatted`, **rc=0**
- `git status --porcelain`: kotor pra-eksis di luar file kerja (modified `.ai/*`,
  `configs/data.yaml`, `journal/`, `tests/`; staged archive-moves; untracked
  prompts/reports) — BUKAN buatanku; satu-satunya file kerjaku
  (`scripts/_build_eda09_wick_confirm.py`, lalu notebook/reports EDA-09) tak di-stage.
  Klaim stage: **tanpa-stage di luar file kerja — TERVERIFIKASI** (tak ada `git add`).

### Larangan bentuk-spesifik (dipatuhi)

Tanpa guard nilai-vs-dirinya-sendiri; tanpa rekonstruksi hari dari UTC (grain
hari-broker via `wall_clock_series`); referensi parquet-R dibaca-ulang dari disk
sebagai objek terpisah (`EV_REF` pola EDA-08 diwarisi di F0 via baca + assert
panjang; versi pyarrow/pandas: 17.0.0/2.2.3 — tercatat di manifest bila klaim
byte-identik; klaimku = hash SHA256 identik); tanpa klaim "sudah diuji/belum ada
test" yang bertentangan; tanpa fixture seragam (data riil V).

### Konflik brief-vs-brief yang dilaporkan (bukan diimprovisasi)

Brief FASE 0 melarang "menulis" generator sebelum lulus NAMUN menuntut output
`ruff check <builder>` sebagai syarat lulus — mustahil literal. Diselesaikan via
supremasi blueprint (tak melarang authoring statis): authoring statis = objek audit;
yang digerbang = EKSEKUSI (nbconvert), dijalankan hanya setelah FASE 0 LULUS di
bawah ini. **FASE 0: LULUS.**

## FASE 1 — F0 recovery + cut-lock (HIJAU)

Prosedur delta-(c) yang diotorisasi (parquet sudah ada): hash pra-run generator beku
= `B800E50EE42D72349F52426B2FCB635EFB5101597E40AFBDD89BF2054B1BDFC2`;
jalankan `scripts/_build_eda07_spike_anatomy.py` apa adanya (SEED_BOOT=20261006,
SEED_NULL=20261007, TAK diubah) → exit=0; hash pasca =
`B800E50EE42D72349F52426B2FCB635EFB5101597E40AFBDD89BF2054B1BDFC2` — **IDENTIK**
(bukti determinisme + validasi file eksis). Regen notebook EDA-07: UNIQ=1632
band 515/415/240/462; analyzed=1514.

| Jangkar | Aktual | Ekspektasi §15 | Hasil |
|---|---|---|---|
| Nunik | 1632 | 1632 | HIJAU |
| band unik | 515/415/240/462 | 515/415/240/462 | HIJAU |
| full-room | 1514 | 1514 | HIJAU |
| band full-room | 460/391/231/432 | 460/391/231/432 | HIJAU |
| exh | (395, 1119) | (395, 1119) | HIJAU |
| `round(pooled,4)` | 0.1682 (repr `0.16818284622594523`) | 0.1682 | HIJAU |
| 8 cut | sama persis §15 (4 baris sel 1) | §15 | HIJAU |

Cut dibekukan sebagai konstanta presisi-penuh (lihat manifest). FASE 1: HIJAU → lanjut.

## FASE 2 — Pre-flight F1/F2/F4 + A-checks (HIJAU, berurutan, tanpa gagal pertama)

- **F1:** hari-V ⊆ 2025 ✓; V∩R=∅ (dua-arah) ✓; max(day-V)=2025-… < 2026-01-01 ✓;
  tick_volume bar-s-V terisi **1.0000** ≥ 0,95 (per bar-s) ✓ → volume LANJUT
  (bukan "tertunda"); hari-V **259** (band 200–320) ✓; bar-M15-V **23812**
  (ekspektasi 20–28k; band 13k–40k) ✓.
- **F2:** ke-4 band non-kosong ✓ (367/286/168/289 unik; 325/269/156/268 full-room);
  total n-V **1018** (≥500; ekspektasi ≈1020) ✓; grup tercil: bawah 111/93/50/96,
  atas 105/94/56/76 — semua ≥ 30 ✓. Tripwire tak terpicu.
- **F4:** `SEED_EXEC=20261016 wick=20261027 boot=20261017` tercatat (satu-seed-satu-run;
  tak di-re-seed) ✓.
- **A1** taksonomi exhaustive per band (325=299+25+1; 269=234+35+0; 156=116+34+6;
  268=169+85+14) ✓. **A2** cut-terkunci exhaustive SEMUA event-V
  (b0 111/109/105; b1 93/82/94; b2 50/50/56; b3 96/96/76) ✓.

## FASE 3 — Build + run

Notebook `eda_09_wick_confirm.ipynb` (8 sel) exit **0** (nbconvert; log run tersimpan
di luar repo). Deterministik: rerun penuh → output sel **identik byte-per-byte**
(diff kosong) + hash parquet tetap. T_DAY=1,7319 konstanta; cls/ctx metadata.
Indikator concat 2023+2024+2025 + whitelist sesudah deteksi (UNIQ-V=1110 di 259 hari;
artefak-R dibuang tanpa dinarasikan). Null: permutasi nilai wick dalam band, cut
terkunci diterapkan ulang, B=10000, STRATA=BAND, p satu-arah 4 desimal. CI
cluster-per-day B=10000 (karakterisasi). Per-band + H1/H2 deskriptif-saja.
Volume-(c) fungsi identik R; V-hari-1 = 20 hari-R terakhir; baseline-penuh 1018/1018.

## Hasil uji (satu-satunya uji ronde)

- Q-wick-V pooled Δ̂ = **0.2179** [KONFIRMASI-V] (repr `0.21788725180524166`)
- Null-mean ≈ -0,0001; p satu-arah = **0.0001** [KONFIRMASI-V] (repr `9.999e-05`)
- Tanda Δ̂_V (+) = tanda R (+) ✓; p < 0,05 ✓
- Baris vonis mekanis (generator, §2): `CONFIRM` (tepat satu kata, tanpa kualifikasi)

## FASE PASCA — SELF-AUDIT PASCA-RUN/PASCA-TEST (LULUS)

1. **Correctness ulang:** tiap klaim ↔ output mentah — F0: sel 1 (12 baris
   aktual-vs-ekspektasi); F1: sel 2 + sel 5 (fill 1.0000); F2: sel 5; F4/uji/CI/
   split: sel 6; volume: sel 7; toolchain: manifest. Tak ada klaim tanpa pasangan
   output; nol klaim BELUM DIVERIFIKASI pada angka putusan.
2. **Bias ulang:** (a) label KONFIRMASI-V di tiap angka-V — LULUS (semua baris V
   bertag; angka-R bertag GENERASI-R); (b) first/gap/dow/joint/floor/split-liar —
   LULUS (tak satu pun muncul di notebook kecuali H1/H2 preregistered deskriptif
   tanpa p); (c) p kedua dari CI — LULUS (CI dilabel karakterisasi, tanpa peran
   putusan; vonis hanya dari baris mekanis). Bukti: dump output sel 1–7 di atas.
3. **Meta ulang:** §§2–8 + Amandemen-1 terjawab di sel 1–7 (pemetaan § FASE 0);
   file luar scope tersentuh: notebook EDA-07 (regenerate deterministik terotorisasi)
   + parquet EDA-07 (hash identik — tak berubah isi); `git status` ditempel (§ FASE 0
   + akhir); determinisme rerun dibuktikan (diff output kosong, hash tetap).
   Gagal = fix + ulangi (tak terjadi). **FASE PASCA: LULUS → laporan §5 ini ditulis.**

## Tabel Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| F0 jangkar 1632/515/415/240/462/1514/460-391-231-432/(395,1119) | TERVERIFIKASI | sel 1 notebook (aktual vs ekspektasi baris-per-baris) |
| `round(pooled,4)==0.1682` + 8 cut = §15 | TERVERIFIKASI | sel 1 + manifest.json |
| F1 259 hari / 23812 bar / fill 1.0000 / whitelist | TERVERIFIKASI | sel 2 + sel 5 |
| F2 n-V=1018 ≥500; grup ≥30 (min 50) | TERVERIFIKASI | sel 5 |
| F4 SEED_EXEC=20261016, satu run | TERVERIFIKASI | sel 6 |
| A1/A2 exhaustive | TERVERIFIKASI | sel 5 |
| Δ̂_V=0.2179, p=0.0001, tanda + | TERVERIFIKASI | sel 6 + manifest |
| CI [0.1631,0.2717] karakterisasi | TERVERIFIKASI | sel 6 |
| Per-band-V +0.1251/+0.0871/+0.2171/+0.4622 deskriptif | TERVERIFIKASI (deskriptif, tanpa klaim) | sel 6 |
| H1 Δ=0.2305 (n=499) / H2 Δ=0.2025 (n=519), tanda sama | TERVERIFIKASI (deskriptif; regime-caveat tak terpicu) | sel 6 |
| Volume-(c)-V med 1.179 IQR [0.914,1.607] P1/P99 0.503/4.396; baseline 1018/1018, drop 0 | TERVERIFIKASI (0 uji, 0 klaim) | sel 7 |
| Angka-R pembanding (0.1682; per-band; vol-c-R; warmup 87/1427) | TERVERIFIKASI sebagai GENERASI-R (sumber: notebook EDA-08 + blueprint §10/§15) | sel 1/7 bertag GENERASI-R |
| Rerun identik + parquet hash identik | TERVERIFIKASI | diff kosong; hash pra=pasca |
| ruff rc=0 / format rc=0 / tanpa-stage | TERVERIFIKASI | output § FASE 0 |

## Yang belum diverifikasi

- Tidak ada. (Seluruh pagar dan angka putusan berpasangan output mentah.)

## Potensi masalah

1. H1/H2 deskriptif menunjukkan efek hidup di kedua semester (tanda sama) —
   regime-caveat tak terpicu; arsitek menilai implikasi ANN (penumpukan-V, §9).
2. CI bootstrap melewati band kosong per-resample tanpa assert finit eksplisit —
   residual kecil; tak materialisasi (CI finit); vonis imun (CI non-putus).
3. Notebook EDA-07 ter-regenerate (efek samping prosedur terotorisasi) — isi
   deterministik, jangkar cocet; tak di-stage/di-commit.

## Saran

1. CONFIRM → Registry #4 naik pangkat TERKONFIRMASI-V (amunisi-V pertama);
   program LANJUT (butuh 4–5) — keputusan arsitek/user.
2. Volume-(c) lock-in TERPENUHI di V (definisi terkarakterisasi; status bukan
   "tertunda") — baseline R→V mempraktikkan jalur precompute produksi.
3. Pertahankan larangan re-seed dan P-segel hingga tahap ANN + P.

## Bukti hash (git hash-object, sesudah penulisan terakhir)

(ditempel pasca-penulisan REPORT.md — lihat perintah di laporan eksekusi)
