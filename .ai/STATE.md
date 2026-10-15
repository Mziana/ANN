# STATE.md — Status Saat Ini

**Update terakhir:** 2026-10-15 (EDA-06 CLOSED: Sel 1 UNDERPOWERED, Sel 2/3/4x TIDAK TAHU; TIDAK LANJUT TV-01; commit 3 artefak menunggu user. R6 tetap DITARIK)
**Fase:** Milestone 1 (Data) + 2 (EDA) SELESAI. Milestone 3 (Metode) BERJALAN
dan TERBLOKIR di persetujuan user.
**Status ronde terakhir:** EDA-07 L3-1 selesai + re-audit LULUS PROSEDURAL +
vonis arsitek L3-1 MASUK 2026-10-13 (`arsitek/putusan-l31-final.md`).
Register beku 68 LOLOS / 35 GUGUR. Ronde L3 DITUTUP.
**Vonis B-4 = GO cabang (a):** lanjut ke **spec pemodelan pra-registrasi**
(BUKAN paper-trade, BUKAN live). Ronde berikutnya Discovery-R1, berbasis
`.ai/backup/2026-10-09_DESAIN_FRESH_SCALPING_EVENT_FIRST.md`.
**Draf `spesifikasi-fingerprint.md` DIPENSIUNKAN** (arsip, jangan dijalankan).
**Yang menunggu user (satu jalur tersisa):** paste brief replikasi
R1 ke AUDITOR (vonis final R1 menunggu ini).
**R2 TERTUTUP 2026-10-13: VONIS FINAL TOLAK E1/E2/E3** (replikasi
auditor LULUS tanpa arbitrase; 8/8 sel gagal 4-syarat; segel D-8 R2
tetap TERTUTUP — tak ada KANDIDAT).
**P2-flipmurni SELESAI 2026-10-14: KALAH 8/8** (side->-side, barrier R2
beku, bed 2026; med stacked -1,52..-1,89; replay 1-posisi negatif semua
sel; anti-drift LOLOS n=90.525). **Jalur flip DITUTUP** (kill-signal
kedua setelah R3-KALAH 7/7).

**R4-M15-native SELESAI 2026-10-14: TOLAK 9/9 sel.** M15 jadi basis,
ambang ATR-based (bukan pip) — desain ulang setelah run tercemar
dikarantina. Bed 2024, 2025/2026 tetap terkunci. 23.758 bar M15.
Median net_obs_A: E1 −10,4..−15,5; E2 −6,61/−7,40; E3 −10,06. **Ujung
atas CI pun negatif semua sel** (−0,41..−3,51). P(profit) dengan timeout
ikut dihitung 27,96–42,98%, tapi **impas nominal 33,3% itu salah**: RR
terealisasi hanya 1,09–1,67 karena exit TIME, jadi impas nyata 37,5–47,8%
dan **9/9 sel tetap gagal**. Shadow: **E1 arah-buta TERBALIK**
(Edge A 0,37–0,46 < 0,5 di 6/6 sel, kaki B di atas 0,5); E2 simetris;
E3 kaki A sedikit di atas 0,5 (koreksi atas "netral"). Nol bug material
(auditor independen). Lihat SESSION_LOG.
**Audit addendum 2026-10-14:** `reports/governance/2026-10-14/Audit/
addendum-R4-M15.md` — 3 temuan: (1) label `winrate` sebenarnya
`TP/(TP+SL)` dengan TIME dibuang; (2) exit TIME SELL di BID vs BUY di ASK
(baris 326 `r4_m15.py`) sehingga 19% event dua kaki rugi, invarian PnL
tidak berlaku untuk barrier; (3) ambang impas nominal keliru. Vonis tidak
berubah. Batasan: bed 2024 tidak boleh di-run ulang dengan aturan exit
berbeda.
Audit R2 = CATATAN; Amandemen-R2-1 SUDAH diterapkan 2026-10-13
(disetujui user paket).

**R6-conditioning DITARIK 2026-10-14 — TIDAK PERNAH DIJALANKAN.** Spec R6
ditolak eksekusi oleh audit independen: 4 cacat FATAL + 2 blocking, semua
diverifikasi ulang dari evidence beku. Spec tetap DRAF di `arsitek/`.
 disposition: `reports/governance/2026-10-14/Audit/addendum-R6-conditioning.md`.

Empat cacat fatal: (D4) 39 dari 52 bin mati struktural oleh n — E1 1.313/tercil
438 dan E3 136/tercil 45 tidak pernah bisa lewat G1, E2 hanya punya 2 sel
sehingga G5 mustahil; hanya 13 bin pooled yang hidup dan 86%-nya E2;
(D1) argumen §0 salah karena exit TIME 40,89% membuat "impas tepat di 1/3"
tidak berlaku dan ambang 35,2% melanggar A7.5; (D1/K5) angka P&L spec salah
skala (count x median, bukan sum); (D7) G6 inert, P(>3 bin lolos | null) ~ 0.

**Cacat tambahan yang tidak ada di laporan auditor (B3):** ambang G2
`Edge >= 0,56` **sudah terbukti tidak cukup**. Kaki B (E1 dicerminkan)
sudah punya Edge 0,560 / 0,602 / 0,567 / 0,575 dan keempatnya tetap rugi
(gap -2,2..-9,0 pp, median net -0,76..-6,99 pip). Korelasi `Edge_B` vs
`gap_pp` = **-0,189**: makin tinggi Edge, makin buruk P&L terealisasi.
Edge memprediksi URUTAN median net (r = +0,773) tapi median net negatif di
seluruh 9 sel — jadi Edge adalah skor peringkat, bukan ambang kelayakan.
Akar masalahnya Edge berbasis median, sedangkan impas ditentukan mean.

**Posisi evidence untuk penutupan kelas (B5):** realized breakeven kaki A
dengan CI 95% cluster-per-hari (10.000 boot, seed 1337) —
**0 / 9 sel significantly positif, 5 / 9 significantly negatif**, seluruh
9 sel `median_net_A` negatif (-6,61..-15,45 pip). Empat sel yang "belum
terbukti" semuanya E1 dengan n 104-315, Edge_A < 0,5, dan median net
-10,4..-11,6 pip. Sel terdekat impas (`E1_N6_k1.0`, gap -0,39 pp) adalah
artefak mean-vs-median: WR-nya kebetulan impas tapi median per trade -10,42 pip.

**Kelas hipotesis "fixed-barrier M15 pada bar M1 pair JPY": MATI-KELAS.**
Dasar: 0/9 positif signifikan, 5/9 negatif signifikan, median net seragam
negatif, dan ambang kelayakan sudah terbukti gagal pada data beku sendiri.
**Batasan wajib:** ini BUKAN berarti "conditioning terbukti tidak berguna".
R6 ditarik karena defective, bukan karena refute. Tidak ada probe valid
terhadap hipotesis conditioning yang pernah dijalankan — yang terbukti
adalah spec yang ada tidak mampu mengujinya. Ronde berikutnya butuh
persetujuan eksplisit owner dan harus mengubah struktur kelas (horizon,
window, rezolusi, atau instrumen), bukan filter di atas barrier yang sama.

**Progress keseluruhan:** ~60% (data+EDA selesai, metode belum)

> **Cara baca file ini (per 2026-10-13).** Bagian atas = status terkini (wajib
> dibaca). Section "Yang Sedang Dikerjakan", "Yang Sudah Selesai",
> "Keputusan Terverifikasi", dan "Peringatan Waktu Broker" di bawah =
> **ARSIP PROVENANSI** — isinya benar sebagai catatan kapan terjadi, tapi
> beberapa bullet masih memakai bahasa tahap lama. Tidak boleh dipakai untuk
> memutuskan langkah berikutnya. Yang otoritatif untuk langkah berikutnya:
> bagian "Langkah Berikutnya" paling bawah file ini + `.ai/TASKS.md`.

## Ringkasan Eksekutif

Semua checkpoint (01, 05-09d) **SUDAH SELESAI**. State file lama menandai
sebagian besar sebagai belum — itu sudah usang dan sudah dikoreksi di sini.
Environment siap, MT5 terhubung, data historis terbukti tersedia (4 tahun,
1.347.847 bar M1), dan repo GitHub sudah aktif (`main` `2112f94`).

**`src/` berisi 2.035 baris di 8 modul** (terukur ulang 2026-10-13):
`data/validate_data.py` 431 · `features/build_labels.py` 327 ·
`data/fetch_data.py` 283 · `data/resample.py` 280 · `features/build_features.py`
321 · `data/clean_data.py` 198 · `data/broker_time.py` 150 · `utils/config.py`
45, plus tiga `__init__.py` satu baris.
**Catatan metodologi:** angka lama di versi file ini ("1.775 baris", dan
nama `build_features.py` "400/400") **tidak cocok** dengan hitungan fisik
baris di atas. Penyebabnya belum saya periksa — mungkin metode hitung berbeda
(baris logis vs fisik) atau file berubah. Perlakukan kedua angka sebagai
**belum terverifikasi** dan jangan kutip keduanya tanpa menyebut sumber.

## Blueprint EDA-06 v9.3 — FINAL (2026-10-15)

Blueprint `candle_anatomy_regime` FINAL setelah 10 iterasi (v8.1->v9.3), tiap
putaran diaudit adversarial + counter-audit. File:
`thoughts/shared/designs/2026-10-15-eda06-blueprint-v93.md`.
Terkunci: biaya 0,95 flat (rumus lama spread x2 = hitung ganda, dicabut) ·
Net TP 2,85 · R:R momentum-only · OR = 4 bar M15 setelah daily open ·
trigger >= bar ke-5 · K=16 setelah entry · partisi R minus 19 hari anomali ·
placebo 1000x2 track · FDR core {1,2,3,4a1} q=0,10 · power CI mean > 5 pip ·
side-consistency 'wrong_side' (real + placebo). Discovery-R1 BATAL (satu rantai).
Brief coder diterbitkan; menunggu Pre-Flight Checklist (Cek 1-6).
PENDING: penyelarasan biaya repo ke 0,95 (broker.yaml/docs/CONTEXT §15).
Tidak ada iterasi blueprint lagi — masalah berikut = masalah kode.
Pre-Flight 2026-10-15: F1 [21,22] gugurkan winter (bukti ganda: DST audit
`data.yaml:271-281` + 255@22/129@23/0@21 → [22,23]) · F2 ambang mikro mustahil ·
F3 Sel 1/2/3 undefined (lubang nyata). Amandemen-1 (A1/A2/A3) MENUNGGU
ratifikasi. Anggaran: R 384 (pertama); sisa V 259 + P 182 = 441 utk
walk-forward (V) + OOS kunci (P).
Amandemen-1 TERBIT (`thoughts/shared/designs/2026-10-15-eda06-amandemen-1.md`):
A1 [22,23] YA · A2 DIMODIFIKASI user → split momentum rezim (4a1t/4a1s;
core {1,2,3,4a1t,4a1s}; trending = komplemen sideways, label jujur;
null regime-matched; gate Cek 4 direvisi: STOP hanya jika Sel 1 <30) ·
A3 framing jujur (Sel 3<30 = "TIDAK TAHU"; Sel 1 LOLOS = "edge lemah" +
hipotesis cadangan "reversal pasca-spike umum"; AMD-full UNTESTED).
A4 (TV-01→V, FS-01→P) + lampu hijau LANGKAH 2 MENUNGGU user.
A4 DIPUTUS (modifikasi user, benar): TV-01 walk-forward di V, FS-01 terkunci
di V, P SEGEL pristine — disentuh tepat sekali (test final ANN-01).
Hierarki: R discovery-terkunci · V workhorse validasi · P ujian final.
LAMPU HIJAU LANGKAH 2 DIBERIKAN 2026-10-15.

## Vonis EDA-06 — CLOSED 2026-10-15: TIDAK LANJUT (tak terbukti, bukan gagal-terbukti)

Eksekusi penuh selesai (notebook 14 sel, nbconvert exit=0; parquet 51×57).
Sel 1: n=51, mean +4.33, CI95 [−5.50,+15.51] lebar 21 > 5 → UNDERPOWERED
(menurut power rule; CI lewati 0 → bukan LOLOS, tanpa klaim maju).
Sel 2 n=12, Sel 3 n=0, momentum 3/7/2/20 → TIDAK TAHU (drop+label).
Nol core LOLOS → TIDAK ADVANCE TV-01. AMD-full DAN versi longgar sama-sama
belum teruji/terbukti di R. Output sah §8A: modal tidak dipertaruhkan.
Profil jujur: win 0.27, win rata +45.0 vs loss −13.8, satu ekor −99.75
penggerak varians; Sel 3 nol karena spike hari-sideways menumpuk bar 4–11
(jendela mikro 12-bar tak pernah ada) — insight struktural, tercatat.
Verifikasi independen arsitek: mean 4.33 ✓, winrate ✓, vonis tercetak
verbatim di notebook ✓. Caveat: parquet hanya event Sel-1 (subset Sel 2/3
di notebook; regenerasi via generator). P/2026 tak tersentuh. Commit 3
artefak aditif MENUNGGU user (coder tidak commit; tree muat perubahan lain).

## Registry Amunisi ANN (program user 2026-10-15: pancing multi-rod)

EDA menjawab hipotesis (ada/tidak + karakter), BUKAN mesin pencetak uang.
Setiap hipotesis teruji = satu amunisi (fitur/setup) untuk ANN; ANN
menggabungkan banyak amunisi. Dua jalur kelulusan: (a) standalone edge
(LOLOS ketat → advance strategi); (b) amunisi fitur (eksistensi
terkonfirmasi + karakter terdokumentasi → registry, tanpa klaim edge).

| # | Amunisi | Status | Bukti |
|---|---|---|---|
| 1 | Spike-reversal (spike + exhaustion → kembali ke open) | TERKONFIRMASI-eksistensi, edge BELUM terukur → jalur (b) | Sel 1 n=51, 12 win rata +45.0, win 0.27, CI lewati 0; parquet 51×57 |
| 2 | (terbuka — EDA berikut) | — | — |
| 3 | (terbuka — EDA berikut) | — | — |
| 4 | (terbuka — EDA berikut) | — | — |

Catatan: AMD-full (Sel 3) = NOL kemunculan → TIDAK masuk registry
(yang tak pernah terjadi bukan amunisi). Ronde EDA baru atas inisiatif AI
tetap DILARANG (§8A.3) — slot 2-4 diisi atas perintah user.
Blueprint v9.4 diterbitkan (`thoughts/shared/designs/2026-10-15-eda06-blueprint-v94.md`):
konsolidasi IDENTIK v9.3 + Amandemen-1, dokumen kanonik tunggal untuk coder
(verifikasi: nol sisa angka lama di aturan aktif; satu-satunya "[21,22]" =
baris riwayat perubahan). v9.3 + Amandemen-1 = arsip riwayat.

## Yang Sedang Dikerjakan

- **Lapisan 2 (EDA) berjalan (2026-10-06).** Langkah 0 (reuse-check), Langkah 1
  (pin `tzdata==2026.5` + `MetaTrader5==5.0.6231`, commit `9a60995`), Langkah 2
  (nb00 setup + audit strata 11/11 PASS), dan **Langkah 3 (nb01, Q1 distribusi return,
  23/23 assertion PASS pasca rework D9 — improvisasi mikro **diratifikasi Klenz + user**)** selesai.
  Venv kanonik = `venv/`; `.venv/` = env bantu uv
  (JANGAN dipakai gate/notebook).
  **Putusan Architect atas SA-03 (R1–R4) dicatat di nb01 dan SESSION_LOG**: kerja
  level-hari (Q6/Q7) dikunci pada tanggal-broker; hari-UTC hanya sekunder.
  Berikutnya: **Langkah 4 — nb02** (Q2 volatilitas per jam broker + Q3 per sesi UTC +
  pengukuran spread → fragmen YAML) **SELESAI** (**30/30** assertion PASS pasca rework D10) dan
  **Langkah 4b SELESAI**: fragmen revisi spread sudah diaudit Klenz
  (LULUS DENGAN CATATAN), 5 fix terpasang, LOW-27.1 ditutup sebagai no-op,
  lalu **fragmen sudah DITERAPKAN ke `configs/data.yaml`** sebagai sub-kunci baru
  `spread.cost_basis` (MEAN) dan `spread.stress_bands` (p95/p99). Blok spread
  lama (`default`, `by_year`, `by_session`, `by_news`, `pip_size`,
  `stress_multiplier`) **tidak diganti**; `by_year[2023]=3.0` tetap.
  **MASIH TERBUKA:** `cost_basis.default=0.65` vs `spread.default=1.5`
  (selisih 2,3x) — backtest wajib menyebut kode mana yang otoritas.
  **Juga terbuka:** blok `_sesi` dari fragmen **belum** diterapkan ke config;
  definisi sesi masih hanya hidup di `notebooks/scalping/_eda_common.py`.
  **Catatan tipe kunci:** `spread.by_year` = int, `cost_basis.by_year` = str
  (consumer harus pakai `str(year)`).
  **nb03 sudah di-commit** (`e4efbfd`, bersama fix builder import).
  **nb04 sudah di-commit** (`4c914b0`, Langkah 6 Commit A — notebook + builder +
  laporan tahap 6–7; 4 file, 3.205 baris). **Commit B (Langkah 6)** = koreksi
  nb01/nb02/nb03 + builder (D1–D5, D9, D10, LOW-34/35/37), rename FIG-01/02/03
  (blob PNG identik), laporan tahap 5 (addendum)/9/10, audit §F/§F.1,
  governance INDEX ×2 (putusan user), dan STATE/SESSION_LOG ini — entri ini
  ikut ter-commit dalam Commit B.
  **Langkah 5 SELESAI — nb03 `eda_03_autocorr.ipynb`** (Q4 autokorelasi, **31/31** assertion
  PASS pasca rework D1–D5, 0 error, VALID, urutan eksekusi terbukti). **Klaim lama
  "|ACF| ≤ 0,012 di semua TF" DICABUT (terbantahkan):** maks |ACF| lintas strata/TF/lag 1–60
  = **0,022639** (strata B, M15, lag 50; no-gap) — ~2× lipat klaim lama. Temuan baru:
  **sign-ACF lag-1 negatif di SEMUA sel** (A & B × M1/M5/M15; A: M1 −0,017702 · M5 −0,009805
  · M15 −0,022624; B: M1 −0,013226 · M5 −0,012994 · M15 −0,017336) dan **lebih besar
  magnitudonya daripada ACF mentah** → mean-reversion jangka sangat pendek lebih terbaca di
  tanda daripada di besaran. **Struktur ikut muncul di lag 21–60** (mis. M1-A lag 23 =
  +0,005862, lag 30 = −0,004757), di luar cakupan lama 1–20. VR(1)=1,0000; rata-rata VR
  (lag 2–60) A: M1 0,9796 (mean-reversion), M5 0,9942, M15 1,0337 (momentum lemah).
  **Ljung-Box** kini dihitung manual (scipy `chi2.sf`) untuk h=5/15/60; **p-value BUKAN
  kesimpulan** — baca Q/n + besaran rho_k. **Tabel A-vs-B** ditambahkan; untuk strata B
  (n kecil, M15 n=12.430) hasil negatif dibaca "tidak terdeteksi pada n ini" (daya unbalanced),
  bukan bukti kesamaan. **Tanda ACF1 M1 masih tidak stabil antar tahun**
  (2023 −, 2024 +, 2025 −, 2026 −). **Koreksi penting:** klaim laporan 4b bahwa
  "7 isu ruff diperbaiki di builder" **tidak benar** — perbaikan hanya di `.ipynb`,
  sehingga regenerasi memunculkan kembali I001 (nb02) dan F401 `utc_series` (nb01).
  Akar masalah kini diperbaiki di ketiga builder, dan setiap `build()` menjalankan
  `ruff format` pada notebook hasil generator (idempoten).
  **Langkah 6 SELESAI — nb04 `eda_04_swings_levels.ipynb`** (Q5 struktur swing + Q6 level
  + placebo, **30/30** assertion PASS pasca rework D6/D7, 0 error, VALID, urutan terbukti).
  (Nama file dikoreksi dari `eda_04_swing_level.ipynb` pada 2026-10-06 sesuai D8:
  `git mv` + `NB_PATH`/docstring `scripts/_build_eda04.py`; isi notebook tidak berubah.)
  Protokol placebo **dibaca langsung dari `eda_00_setup.ipynb`** dan di-assert sama persis
  (seed 20261006, M5, theta 0,5×ATR(14), window 6/12/24, bootstrap 10.000 day-cluster).
  **Temuan NEGATIF (penting):** hit-rate reversal level nyata (0,469–0,490) **TIDAK
  melampaui placebo** (0,499–0,505); jadi belum ada bukti round-number atau prior-day H/L
  "dihormati" pasar lebih dari level acak.
  **PERTANYAAN TERBUKA untuk Klenz:** nb00 menulis pergeseran level tanpa menyatakan
  syarat "level placebo harus benar-benar disentuh". Implementasi literal menghasilkan
  placebo degeneratif (0,89 vs 0,47) karena level jatuh di luar rentang bar. Saya memakai
  interpretasi placebo = touch genuine (semua parameter preregistrasi dipertahankan).
  Retensi event placebo 1 = 46,8–55,7% (keterbatasan, dilaporkan).
  Berikutnya: **Langkah 7 — nb05** (Q7 regime + `report.md` EDA + penomoran figure SA-09).
  **Backlog tercatat (Klenz):** (a) **T-01 "massa nol"** (5,83% bar M1 ber-return persis 0, nb01)
  menunggu **ratifikasi via laporan EDA final** `report.md` (tugas nb05); (b) **ratifikasi user atas
  improvisasi mikro nb01** (`16/16`→`23/23`) dicatat resmi di STATE + SESSION_LOG.
- **Audit adversarial nb05 berjalan (2026-10-06 s/d 2026-10-07).** Dokumen:
  `reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md`. Objek dikunci ke
  `_build_eda05.py`, `eda_05_regimes.ipynb`, `report.md`, `laporan_tahap_11_regime.md`,
  `laporan_tahap_12_sintesis.md` (materi audit lama tidak dibuka sebagai bukti).
  **Batch A (Langkah 1-3: replica, insiden ACF, look-ahead) — selesai.**
  **Batch B (Langkah 4-6: H1-H5, trace `report.md`, 8 item BELUM DIVERIFIKASI)
  — selesai 2026-10-07, verdict GAGAL: 13 temuan baru (12 B4 + B6-04), 1 HIGH.**
  **RE-AUDIT perbaikan (putaran 2026-10-07) — selesai, verdict LULUS DENGAN SISA
  1 LOW:** 13 temuan lama **tertutup semua** (B4-01…B4-12, B6-04) plus L3-06 ditutup
  juga; notebook dijalankan penuh (19 sel kode, 67/67 assertion lulus, tanpa error).
  - **Verdict per langkah:** LANGKAH 4 **LULUS** · LANGKAH 5 **LULUS DENGAN CATATAN** ·
    LANGKAH 6 **LULUS DENGAN CATATAN**. Hash audit final `b802ee1959eb…`
    (`git hash-object`, 128.118 byte / 2.105 baris).
  - **B7-01 (LOW, temuan baru) — jumlah assertion diklaim 68, aktual 67.** Builder dan
    notebook identik 67 `ast.Assert` (hitung AST, bukan regex); `report.md:15` dan
    `tahap_11:4,106` menyebut 68, dan `tahap_11:5` merinci 10 item meski menulis "+9".
    Dampak nol pada hasil analitik; hanya provenance yang meleset satu.
  - **Angka 78,27% vs 77,17% diputuskan BUKAN temuan:** 78,2745 = massa |r| London+NY
    berbobot Σ|r|; 77,1700 = rata-rata 6 jam tanpa bobot. Selisih 1,1045 pp murni
    efek pembobotan; angka baru lebih tepat untuk klaim konsentrasi volatilitas.
  - **Koreksi metadata dokumen audit:** judul kolom hash lama `sha256 (12)` sebenarnya
    `git hash-object` (SHA-1) — sudah dibetulkan, ini koreksi label bukan temuan.
  - **B4-04 (HIGH)** — H5 memakai proksi spread mean-D1 harian yang hampir datar
    (rentang 0,0086 pip antar sesi vs 0,1883 pip spread per-bar sebenarnya);
    kanon `eda_design_v3.1.md:64` M4 menetapkan `spread_p95`. Akibatnya
    `flag_biaya_mendominasi = []` palsu — dengan p95, NewYork (0,9488) dan
    Sydney (0,7975) ter-flag. Pembela di `_build_eda05.py:543` ("spread per bar
    tidak ada di skema") **tidak berlaku**: M1 sudah punya `spread_pips` per bar.
  - **B4-03 (MEDIUM)** — assertion `share_off_top6 < 0.5` (`:776`) meloloskan 2 jam
    Off, sedangkan M2 kanon memicu revisi batas pada >=2 jam Off.
  - **B4-01, B4-02, B4-05** — metrik tidak mengukur klaimnya (bucket "range"
    sebenarnya bucket volatilitas TERENDAH; `share_Off_di_top6` tidak menguji
    London/NY; tidak ada sesi pun yang punya biaya rendah relatif pergerakan).
  - **B4-06, B4-07** — ambang H2 ">=3 dari 4 tahun OOS" tidak dapat dieksekusi pada
    span 3,75 tahun; kata "terukur" tidak didukung uji signifikansi.
  - **B4-12 (MEDIUM)** — M3 (DST-aware vs cross-tab) tidak dijalankan/dilaporkan;
    hitung ulang menunjukkan SETUJU, jadi dampak angka nol.
  - **B6-04 (MEDIUM)** — `report.md:32` salah label: kurtosis mikrostruktur sudah
    diuji dan **ditolak**, jadi statusnya `TIDAK DIDUKUNG`, bukan BELUM DIVERIFIKASI.
  - **Angka H1-H5 sendiri seluruhnya benar** (~20 baris `report.md` bersumber
    nb05 diverifikasi ulang tanpa selisih); angka Q1-Q6 bersumber nb00-nb04
    **di luar objek** -> tetap BELUM DIVERIFIKASI.
  - ~~**2 pertanyaan terbuka untuk Coder/Architect**~~ — **SUDAH dijawab initiator
    (2026-10-07): Q1-Q6 + kalender libur TETAP DI LUAR OBJEK sampai user putuskan.**
    Jadi nb01-nb04 tidak dibuka untuk trace pasif dan kalender libur eksternal tidak
    dipakai; item kalender libur statusnya tidak berubah (tetap partly BELUM). Jangan
    dipertanyakan ulang tanpa perintah baru dari user.
  - **Langkah 7-10 audit (Batch C: registry FIG-01..07, temuan jujur coder, 4-5 bug
    riwayat, konvensi RULES.md) BELUM dijalankan** — hanya atas perintah eksplisit.
  - Catatan tooling: audit wajib pakai `venv/Scripts/python.exe` (scipy 1,17,1);
    `.venv/` tidak punya scipy.
  - **Batch newline + M1 SELESAI (2026-10-07, ikut commit batch ini):** F-NL
    (`newline="\n"` ×5 builder) + F-NL2 (pasca-proses CRLF→LF sesudah nbconvert,
    putusan arsitek Q1–Q4) + regen nb05 saja (81.851 byte, 0 CR, 68 assertion,
    FIG-04..07 identik) + koreksi frasa provenance M1 ×4 dokumen. Re-audit:
    F-NL/F-NL2/M1 TERVERIFIKASI TUTUP, tanpa temuan baru. Batch C mutakhir:
    **0 MEDIUM terbuka, 4 LOW terbuka** (B8-01/B10-01 dikecualikan, L2-01/L2-02
     catatan).
- **Penguncian hipotesis H1–H5 SELESAI (2026-10-07, commit `0107a56`):**
  review redaksi per hipotesis oleh user (H1 sempat ditahan untuk pertanyaan
  reversal-day ke arsitek — putusan opsi iii: kunci + catat risiko, klausul
  anti-penyelamatan); arsitek putuskan nasib H1–H5 (H1 KUATKAN, H2–H5 TERIMA
  bersyarat S1–S8, H6+ DITOLAK, vonis H3 TERBUKA sampai S4). Dokumen:
  `reports/governance/2026-10-07/hipotesis_lock_v1.md` (redaksi beku) +
  `putusan-arsitek-H1-H5.md` (lampiran putusan).
- **Fondasi fitur B1 SELESAI + rantai audit TERTUTUP (2026-10-07):**
  `src/features/build_features.py` 400/400 baris + 37 test, parquet
  `07402f40…` (90.041×11) identik objek audit; audit fondasi 0 HIGH/1 MEDIUM/3 LOW
  → putusan arsitek B1 (D0 + 4 butir, tersimpan) → F-1 diputus arsitek
  (karantina-presisi sisi konsumen B2, larangan dipertahankan) → LOW F-2/F-3/F-4
  diperbaiki → re-audit (F-3 bersih; F-2/F-4 TERTUTUP-bersyarat) → micro-batch
  R1/R2/R3 → konfirmasi auditor 3×YA. Residual berdiri: #4 (nol test `main()`),
  #5 (`return 0` hardcoded),   #7 (headroom nol → split B2 wajib), materialitas
  H1/H5 F-2 berlabel BELUM DIUJI. **B2 SELESAI 2026-10-08** (`build_labels.py`
  399 baris + 60 test, D4 974 hari-broker `47d15c41…`, re-audit keempat LULUS
  5/5 + regresi 13/13 — Fase 1 TERTUTUP). Berikutnya: **Lapisan 3-H3**
  (materialitas gap 234 hari + sensitivitas TAU).
- **Data 2023-2026 ter-fetch**: 1.347.847 bar M1 total (4 file di `data/raw/M1/`).
- **R1 DIPERBAIKI (2026-10-05): kolom `time` sekarang UTC sejati.** MT5
  mengodekan jam dinding broker seolah-olah epoch UTC. Fungsi
  `broker_epoch_to_utc` yang lama adalah no-op, jadi seluruh `data/raw`
  tersimpan 3 jam **maju**. Sudah diperbaiki dan data di-fetch ulang.
- **DST CONFIRMED (2026-10-05): server Finexseasonal, bukan statis.** GMT+2
  (EET) musim dingin, GMT+3 (EEST) musim panas, mengikuti DST **Amerika**.
  Jadwal 2023-2026 di `configs/data.yaml`; konversi di `src/data/broker_time.py`.
  Data di-fetch ulang; ~35% bar (musim dingin) sebelumnya salah 1 jam.
- **Validasi data LOLOS**: 0 error, 6 peringatan di 4 tahun.
- **Pembersihan data SELESAI**: `data/processed/M1/*.parquet`, 1.347.847 bar
  (tanpa interpolasi — D1 2026-10-05).
- **Resample SELESAI**: M5/M15/M30/H1/H4/D1 di `data/processed/<TF>/`.
- Berikutnya (Lapisan 2): `src/features/build_features.py` setelah EDA lulus audit.

## Yang Sudah Selesai

- [x] Checkpoint 01: Struktur folder
- [x] Checkpoint 05: State files
- [x] Checkpoint 06: scripts (verify_claims.py, check_state.py, pipeline.ps1)
- [x] Checkpoint 07: configs (requirements, pyproject, pre-commit, configs/*.yaml)
- [x] Checkpoint 08: setup.ps1 + run.ps1
- [x] Checkpoint 09a-09d: AGENTS v3.0, RULES v2.0, PROMPTS v2.0, CONTEXT, configs+jurnal+backtest
- [x] Setup environment: venv Python 3.12.8, 134 paket (MetaTrader5 5.0.6231, torch 2.4.0, pandas 2.2.3)
- [x] Git init + 2 commit + pre-commit hook terpasang
- [x] Struktur jurnal lengkap (header CSV 29 kolom)
- [x] Struktur backtest per tanggal + template audit 8 section
- [x] **Onboarding AI baru (Prompt 0 / AGENTS.md §24)** — inventarisasi + verifikasi
- [x] Verifikasi broker: simbol `USDJPY`, timezone UTC+3, data 3,75 tahun (1.348.135 bar M1)
- [x] **Phase A (task 1-5) SELESAI**: state files, `broker_timezone` UTC+3, hapus BOM 27 file,
      `.gitattributes`, ruff-only, docstring Google Style, `docs/PROJECT_MAP.md`
- [x] Gate pre-commit dibetulkan: hook `mixed-line-ending` dihapus (tabrak `.gitattributes`),
      `pytest-quick` -> `scripts/run_tests.py` (toleran exit 5). `pre-commit run --all-files` 11/11 hijau
- [x] **Phase B (task 6): `src/data/clean_data.py`** — raw CSV -> Parquet.
      Awalnya mengisi 2.010 gap kecil dengan kolom penanda `is_filled`; sejak
      D1 (2026-10-05) interpolasi **dihapus**: 1.347.847 bar masuk == keluar,
      0 gap diisi, tidak ada bar sintetis sama sekali.
- [x] **Bug `.asi8` pandas 3.x ditemukan & diperbaiki** — `datetime64[s].asi8`
      menghitung detik, bukan nanosekon, sehingga kolom epoch jadi `1` semua.
      Fix `as_unit("ns")` + tes regresi `test_epoch_values_are_real_seconds`.
- [x] Hook pre-commit lokal sekarang jalan dengan interpreter venv lewat
      `cmd /c "scripts\run_hook.bat" ...`. Sebelumnya pakai Python 3.14 sistem
      (tanpa pyarrow) sehingga 2 tes parquet selalu gagal.
- [x] **Perbaikan 8 temuan audit Phase B** (fetch_data + validate_data):
      import MT5 jadi lazy (`import_mt5()`, `timeframe_constant()`) — kedua modul
      kini import-able tanpa MetaTrader5 terpasang; `check_spread` benar-benar
      membandingkan p99 vs `spread.by_year` (2023 jadi WARN, sebelumnya selalu
      LOLOS); `KNOWN_ANOMALY_WINDOWS` pindah ke config; `print` + stderr +
      `logger`; `trading_days` pakai logika sesi. 120 test hijau.
- [x] **5 temuan audit DIBATALKAN** atas bukti data: C-02, H-02, H-03, H-04,
      L-02. Detail pembatalan ada di `SESSION_LOG.md`.
- [x] **Keputusan user atas Q1/Q2/Q3 diimplementasikan** (2026-10-05):
      `validate_data.py` tetap 543 baris dengan `# EXCEPTION` yang diperbaiki
      (jujur soal komposisi baris) + 3 batas keras (>600 baris / fungsi publik
      baru / akhir Milestone 1); `check_bar_count` tetap `dt.date` dengan
      docstring yang menjelaskan kenapa berbeda dari `trading_days`; `black==24.10.0`
      dihapus dari `requirements.txt`; pyproject TIDAK disentuh; `CHANGELOG.md`
      diisi; catatan usang `check_foreign_chars.py` di TASKS.md dibersihkan.

## Yang Belum

> Direkonsiliasi 2026-10-13. Yang masih [ ] di bagian "Yang Sudah Selesai"
> ATAU di bawah ini sudah usang bila bertanda ~~coret~~.

- [x] Phase B: `src/data/fetch_data.py` + `src/utils/config.py` + `__init__.py` + 22 test
- [x] Test 1 bulan (2026-10-01 s/d 10-06) → 3.134 bar, **7/7 verifikasi LOLOS**
- [x] Fetch full 2023-01-01 s/d 2026-10-05 -> 1.347.847 bar M1
- [x] `src/data/validate_data.py` (cek gap, baris, offset historis)
- [x] `src/data/clean_data.py` (raw -> Parquet, tanpa interpolasi)
- [x] `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1, bucket jam broker)
- [x] ~~`src/data/resample.py` — berikutnya~~ (USANG: sudah selesai 2026-10-05)
- [ ] **Akhir Milestone 1**: pecah `validate_data.py` (431 baris terukur) jadi check
      vs render — batas keras dari user. Batas ">600 baris" belum tersentuh,
      tapi batas "akhir Milestone 1" sudah lewat. MEMBUKA FILE NYATA.
- [x] Modul `src/features/`: build_features.py SELESAI (B1 TERTUTUP 2026-10-07)
- [x] Modul `src/features/`: build_labels.py SELESAI (B2 TERTUTUP 2026-10-08)
- [ ] Modul `src/models/`, `src/backtest/` — **folder belum ada sama sekali**
      (terverifikasi 2026-10-13)
- [x] ~~EDA (distribusi return, volatilitas per sesi, regime)~~ (USANG: EDA-00..07
      selesai + audit + vonis, 2026-10-12/13)
- [ ] **Pemilihan metode** — TIDAK "menunggu EDA" lagi (EDA sudah selesai).
      Sekarang menunggu **persetujuan user atas 4 keputusan §18 dokumen desain
      9 Okt** untuk menulis spec Discovery-R1
- [ ] Backtest + audit — belum dimulai; `reports/backtest/` masih kosong (nol run)
- [ ] 500+ trade data (kriteria Fase 1) — belum tercapai
- [ ] Isi `.env.example` (masih 0 byte)
- [x] Damakan spread di `configs/data.yaml` — SELESAI 2026-10-15, sudah
      memakai terukur per-sesi + stres p95/p99
- [x] Tutup komisi — SELESAI 2026-10-15, user konfirmasi $1,00/lot per sisi
      ($2,00 round-turn); kontrak 100.000 + leverage/min/maks/pip spec Finex

## Blocker

- **Blocker aktif = menunggu AUDIT AUDITOR atas spec** (sejak
  ratifikasi 2026-10-13).
  Brief audit sudah disusun; user paste ke auditor eksternal, bawa
  pulang laporan; arsitek putuskan LULUS/GAGAL lalu coder discovery
  2024. Tanpa laporan audit, coder tidak jalan (§15 desain langkah 3).
- Tidak ada blocker eksternal/teknis. MT5 terhubung (`connected=True`), data
  4 tahun tersedia, test suite hijau per catatan terakhir.
- `trade_allowed=False` — akun belum login untuk trading (tidak menghalangi
  riset; juga tidak relevan karena belum ada strategi live).

## Keputusan Terverifikasi (2026-10-05)

| Keputusan | Nilai | Bukti |
|---|---|---|
| Simbol MT5 | `USDJPY` (bukan `USDJPYm`) | `symbols_get()` 82 simbol, `USDJPYm` absen |
| Timezone broker | **UTC+3** (`Etc/GMT-3`) | diukur 2026-10-05 vs jam internet independen (timeapi.io + HTTP `Date:`): tick dan bar M1 tepat +10800 dtk, 5/5 sampel; setelah fix selisih <=2 dtk |
| Offset historis broker | **CONFIRMED seasonal** GMT+2/GMT+3 | finex.co.id/trading/instruments + jawaban Support 2026-10-05 dengan 8 tanggal, diverifikasi ulang terhadap aturan DST AS (8/8 cocok) |
| 1 pip USDJPY | 0.01 | `digits=3`, `point=0.001` |
| Spread live | 0,8 pip | tick 157.851 / 157.859 |
| Pipeline order | M1 dulu, 1 TF, verifikasi, baru expand | diputuskan user 2026-10-05 |
| Format simpan | CSV per tahun: `usdjpy_m1_<year>.csv` | diputuskan user 2026-10-05 |
| Spread per tahun | `by_year`: 2023=3,0 · 2024-2026=1,5 | p99 2023 = 8,5 pip vs 1,2-1,7 tahun lain |
| Total data | **1.347.847 bar M1** (2023-2026) | jumlah file = jumlah `copy_rates_range` awal |

## Langkah Berikutnya

> Ditulis ulang 2026-10-13. Versi lama (yang masih diarsipkan di bawah daftar ini
> sebelumnya) menunjuk "Langkah 4 = tulis nb02" — itu **sudah selesai
> 2026-10-06**. Kalau kamu membaca langkah lama itu, abaikan.

1. **Tunggu 4 keputusan user atas §18 dokumen desain 9 Oktober:**
   (1) E1/E2/E3 sebagai satu-satunya ruang ronde pertama — tanpa menambah pola ke-4;
   (2) 2024 untuk mencari, 2025 untuk menguji, 2026 terkunci, 2023-H2 uji tambahan;
   (3) jalur P0 (putar ulang data lama) -> P1 (bayangan real-time, tanpa order)
   -> P2 (paper 0,01 lot), tiap pindah butuh izin user;
   (4) semua bukti (perintah, output, hash) masuk repo sebelum auditor mulai.
2. **Tulis `spec Discovery-R1`** di `reports/governance/2026-10-13/arsitek/` —
   cara kerja bernomor: unit = KEJADIAN-XXX, jendela SEBELUM/SAAT/SESUDAH,
   MFE/MAE pip, pasangan barrier TP/SL, biaya event-time, analisis
   kapan-jangan-masuk, uji stabilitas, lalu vonis biner. Ronde pertama maksimal
   3 keluarga event, 1 kandidat per keluarga. Ledger discovery ditulis
   SEBELUM run.
3. ~~**Damaikan spread di `configs/data.yaml`**~~ — **SELESAI 2026-10-15**
   (sudah memakai terukur per-sesi + stres p95/p99).
4. ~~**Tutup komisi** di rumus biaya 3 lapis~~ — **SELESAI 2026-10-15**
   (user konfirmasi $1,00/lot per sisi = $2,00 round-turn; kontrak +
   leverage/min/maks/pip spec Finex).
5. **Baru setelah itu**: `Spesifikasi Metode Target v1` (definisi sukses trading
   yang bisa diuji), lalu eksekusi Discovery-R1, re-audit, vonis GO/NO-GO.
6. **STOP setelah serah-terima.** Satu putaran = satu vonis (S8A). Tidak
   boleh mengusulkan ronde investigasi berikutnya tanpa persetujuan user.

**Status terperinci tiap tahap:** `reports/eda/progress/laporan_tahap_*.md`
(tahap 0 reuse-check, 1 pin deps, 2 nb00, 3 nb01) dan
`reports/governance/<tanggal>/`.

## Venv — satu kanonik (2026-10-06)

- **`venv/` = kanonik.** Dibuat setup.ps1 (Python 3.12.8, pip 24.3.1); dipakai
  `setup.ps1`, `run.ps1`, `pipeline.ps1`, dan `run_hook.bat` (hook pre-commit).
  Semua gate dijalankan dengan `venv/Scripts/python.exe`.
- **`.venv/` = env bantu, JANGAN dipakai gate/notebook.** Dibuat uv 0.12.13
  pada 2026-10-05 22:13 oleh sesi AI (Python 3.12.13; pandas 3.0.6 dkk, tanpa
  pip, tanpa torch/sklearn/MT5/jupyter). Dibiarkan di disk; penghapusan
  menunggu perintah eksplisit user.
- `requirements.txt` mengikuti `venv/`: `tzdata==2026.5` dan
  `MetaTrader5==5.0.6231` dipin 2026-10-06; `pip install -r requirements.txt`
  no-op (semua requirement sudah terpenuhi).

## Aturan Pipeline (2026-10-05)

- **Raw immutable.** `data/raw/` tidak pernah ditulis ulang.
- Processed = Parquet di `data/processed/M1/`.
- Kalau `validate_data.py` jadi panjang, pecah jadi logika check vs render.

## Format Kode (KEGIATAN 2026-10-05)

- **Ruff saja.** Black dihapus dari `.pre-commit-config.yaml` dan
  `[tool.black]` dari `pyproject.toml`. Dua formatter bisa saling menimpa.
- `.gitattributes`: `* text=auto eol=lf`, `*.ps1`/`*.bat` `eol=crlf`,
  biner (`png`/`jpg`/`parquet`) `binary`.
- Gate: `ruff check` + `ruff format --check` keduanya hijau.
- Line ending: 38 file teks LF, 3 file `.ps1` CRLF.

## Peringatan Waktu Broker (WAJIB)

Timestamp dari `mt5.copy_rates*` = **jam dinding broker UTC+3** yang
dikodekan seolah-olah epoch UTC, BUKAN instants Unix.

Aturan: `UTC = broker_epoch_raw - offset` (`Etc/GMT-3` = 10800 detik).
`datetime.fromtimestamp(epoch, tz=broker_tz).astimezone(UTC)` **bukan**
konversi, melainkan no-op, dan itulah bug R1 yang bertahan sampai
2026-10-05. Peringatan di bagian ini sejak awal **benar**; kodenya yang
melanggarnya.

Status: **sudah diperbaiki** di `fetch_data.py`, data di-fetch ulang
(1.347.847 bar, `time` = `broker_time_raw` dikurangi offset seasonale,
0 bar salah konversi).

### DST — CONFIRMED, dengan satu risiko residu

Server Finex **seasonal**: GMT+2 (EET) musim dingin, GMT+3 (EEST) musim panas,
mengikuti DST Amerika (Minggu ke-2 Maret / Minggu ke-1 November).

Sumber, dua-duanya independen satu sama lain:
1. `finex.co.id/trading/instruments` — "GMT+2 ... selama Waktu Musim Panas,
   waktu akan beralih ke GMT+3".
2. Jawaban Finex Support 2026-10-05 dengan tanggal persis per tahun. Delapan
   tanggal diverifikasi ulang terhadap aturan DST AS, **8 dari 8 cocok**.

Bukti bahwa seasonalnya benar-benar dipakai:
- Tick live 5 Okt 2026 meleset **0 detik** setelah konversi seasonale
  (sebelumnya +10.799 detik).
- Bucket M5/H1/D1 kita **identik dengan bar native MT5**, diuji pada jendela
  musim dingin (Jan 2024) dan musim panas (Jul 2024), dibandingkan pada
  `broker_time_raw` sehingga bebas dari asumsi offset. 6 dari 6 COCOK.
- Sesi broker terbukti berjalan **01:00-00:00 server**, persis seperti sesi
  yang Finex terbitkan.

#### Risiko residu yang BELUM terjawab (diperbarui 2026-10-05, self-audit)

Self-audit adversarial menemukan bahwa gambaran lama salah. Yang sebenarnya
terjadi: **digit jam broker mundur 1 jam**, sesi buka di jam dinding **00:00**
dan bukan 01:00. Ini terlihat langsung di `broker_time_raw`, tanpa perlu
mengebak offset.

Terdapat **dua** jendela (2023-03-17..24 telah dihapus 2026-10-05; dikategorikan
sebagai regime SA-03, bukan anomali — lihat Keputusan Architect):

| Jendela | Hari perdagangan | Bar | % dari 1.347.847 |
|---|---|---|---|
| 2024-10-28..11-01 | 5 | 6.899 | 0,51% |
| 2026-03-10..03-27 | 14 | 19.299 | 1,43% |
| **Total** | **19** | **26.198** | **1,94%** |

Bukti lokal yang discriminating (hanya `broker_time_raw`, tidak pernah menyentuh
kolom `time` yang kita karunia sendiri):

- Di luar jendela, buka sesi = 01:00 -> **22:00 UTC** di musim panas (offset +3)
  dan **23:00 UTC** di musim dingin (offset +2). Stabil di 4 tahun.
- Di dalam jendela, digit 00:00. Dengan offset **+3** hasilnya **21:00 UTC** -
  nilai yang **tidak pernah muncul** di 4 tahun selain 19 hari tersebut.
  Dengan offset **+2** hasilnya **22:00 UTC**, identik dengan tetangganya.
- Kedua jendela berdekatan dengan transisi DST, dan langkahnya tepat 1 jam -
  sama dengan besar langkah DST itu sendiri.

Dua penjelasan masih mungkin dan keduanya cocok dengan data: (a) server benar
saja menyala dengan GMT+2 selama jendela itu, atau (b) sesinya yang bergeser.
Bukti lokal cenderung ke (a), tapi itu **inferensi, bukan konfirmasi broker**.
Status offset di kedua jendela: **BELUM TERVERIFIKASI**.

- Keduanya terdaftar di `configs/data.yaml` -> `validation.anomaly_windows`,
  jadi `validate_data` menandainya WARN otomatis dan tidak bisa terlewat diam-diam.
- **Jangan dipakai sebagai input fitur sesi Tokyo/London/NY** sebelum penyebabnya
  dikonfirmasi ke Finex.
- Pertanyaan ke Finex sudah disiapkan (non-blocking), dan sekarang bisa lebih
  spesifik karena kita tahu gejalanya presisi 1 jam, bukan "break di jam 23".

**Temuan SA-03 (terpisah):** Januari-Juni 2023 punya **185.248 bar = 13,74%**
dengan digit buka ~00:07 dan **1.431 bar/hari** - bukan 1.380 seperti
2023-H2 dan semua tahun berikutnya. Artinya sesi berjalan ~23,9 jam/hari tanpa
break 60 menit seperti tahun-tahun lain. Regime data 2023-H1 **berbeda** dari
seluruh periode lain dan belum pernah dijelaskan. Ini bukan anomali offset,
tetapi harus dicatat sebelum dipakai sebagai input fitur apa pun.

---

## Kontrak Broker FINEX - M1-M5 TERTUTUP (2026-10-15)

Semua temuan M1-M5 diperbaiki dan diverifikasi ulang dari
`data/processed/M1/*.parquet` secara **independen** (tanpa mengimpor
`add_labels`/`session_flags`/`wall_clock_series` dari notebook).

**Angka otoritatif (stratum A, n = 1.136.401):**

| Sesi | n | mean | p50 | p95 | p99 | max |
|---|---|---|---|---|---|---|
| London | 395.884 | 0,608 | 0,60 | 0,80 | 1,20 | 4,60 |
| NewYork | 293.134 | 0,692 | 0,60 | 1,20 | 2,00 | **55,60** |
| Tokyo | 364.696 | 0,615 | 0,60 | 0,90 | 1,30 | 8,70 |
| Sydney | 82.687 | 0,796 | 0,60 | 1,50 | 2,70 | 24,10 |

Spike `55,60` pip = **NewYork 2024-12-24**, bukan Sydney.
Stratum: A n=1.136.401 mean 0,6456 · B n=185.248 mean 1,392 · C n=26.198 mean 0,656.

**Biaya per lot:** `1 pip = $6,6935` (`0,01 x 100.000 / 149,3987`).
Mid = $10,70 -> spread **5,35x** lebih besar dari komponen komisi (understatement 81,3%).

**KONTRAK DITUTUP 2026-10-15:** komisi `$1/lot per sisi` (= $2,00
round-turn) dikonfirmasi user; spec Finex USD/JPY dari user (kontrak
100.000, base USD, pip 0,01, min 0,01, maks 50 lot/order, leverage 1:500)
+ cocok silang anchor EDA-06. Tidak ada blocker biaya tersisa.

**MASALAH ARSITEKTUR:** `configs/broker.yaml` TIDAK dibaca kode mana pun
(`git grep broker.yaml -- '*.py'` = nihil). `check_spread`
(`src/data/validate_data.py:256`) masih `load_config()` -> `configs/data.yaml`.
Header broker.yaml sudah dikoreksi agar tidak mengklaim otoritas tunggal.

Laporan: `reports/governance/2026-10-15/Audit/fix-M1-M5-broker-contract.md`
