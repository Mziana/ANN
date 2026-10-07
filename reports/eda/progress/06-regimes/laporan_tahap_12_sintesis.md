# Laporan Tahap 12 — C2: Sintesis Rantai EDA → Draf Hipotesis H1–H5

**Tanggal:** 2026-10-06 · **Sumber angka:** output notebook `eda_05_regimes.ipynb`
(blob `661c0aeb2357…`) sel #13–#18, diambil dari disk via nbformat (bukan draf).
(KOREKSI NL2, 2026-10-07: regen nb05 LF deterministik (pasca-proses Q2) → blob `661c0aeb2357…`; KOREKSI M1 2026-10-07: pin lama `2cb57ad9ec1a…` dipensiunkan karena merge chunking output pada regen NL2 — bukan karena era CRLF (provenance); sel, sumber & output-gabungan identik. KOREKSI pasca-audit Batch B: blob & sel dimutakhirkan — sebelumnya `8158d5b57b20e…`
sel #13–#17; angka H1–H5 kini memuat 13 temuan B4-01…B4-12. KOREKSI Batch C B8-04/B9-01:
blob dimutakhirkan — sebelumnya `2d8f600acade…`; regen mengubah hanya string Q6 pada
sel #18 + 1 guard `hour_utc` pada sel #16 — sel & angka H1–H5 lain identik.)
Format wajib §11 v3.1: {klaim · metrik EDA pendukung · rencana uji Lapisan 3 ·
ambang falsifikasi}. **Metode BELUM dipilih** — ini kandidat.

## H1 — Regime tipe-hari (basis Q7)

- **Klaim:** hari terbagi dalam tipe terukur (trending/normal/range dari ratio_path &
  range/ATR vs median A); kelanjutan arah pada hari trending layak diuji.
  Definisi KOREKSI B4-01: bucket "range" = hari TENANG (kedua metrik ≤ median-A:
  volatilitas & range terendah — bukan "choppy lebar").
- **Pendukung (stratum A):** trending 33,7% · range 33,8% · normal 32,5%; chi-square
  tipe-hari A-vs-B p=0,325 (n-A=825, n-B=116).
- **Uji Lapisan 3:** conditioning tipe hari (identifikasi H+1 pagi, data t-1 saja):
  drift berarah RELATIF M15 4 jam pertama London (dinormalisasi ATR harian t-1 —
  normalisasi memisahkan "kelanjutan arah" dari "pergerakan lebih besar", koreksi
  confound level-volatilitas B4-01) pada hari trending vs range, sign test + CI.
- **Ambang gugur:** selisih drift median CI95 memuat 0, ATAU share trending tak stabil
  antar tahun (chi-square antar-tahun p<0,01).
- **Catatan ex-post (L3-01 opsi b):** ambang tipologi = median full-sample A → share di
  atas deskriptif ex-post, bukan hasil klasifikasi real-time; uji Lapisan 3 memakai
  identifikasi H+1 pagi real-time (data t-1 saja), bukan ambang ini.

## H2 — Mikro-momentum M15 (basis Q4)

- **Klaim (KOREKSI B4-07 — kata "terukur" DITURUNKAN):** pola horizon-pendek
  M15-A lemah dan SECARA STATISTIK TAK TERBEDAKAN dari iid (dihitung ulang di
  nb05, bukan disalin audit) → trend-following M15 layak diuji dengan biaya penuh
  SEBAGAI HIPOTESIS EKSPLORATORI; EDA tidak mengklaim sinyal terdeteksi.
- **Pendukung (KOREKSI pasca-audit Langkah 1 — metode eksak nb03: ddof=1 + no-gap
  kolom `gap_return`; angka lama memakai metode berbeda yang tak disclosed):**
  ACF1 M15-A = +0,001793 (nb03 acf_all 0,001793); sign-ACF(1) no-gap = −0,022624
  (identik nb03, n_no_gap 75.038); VR(5)=1,0160, VR(15)=1,0119, VR(60)=1,0657;
  rata-rata VR = 1,0312 (referensi nb03 1,0312 ✓). Angka 1,0337 pada nb03 =
  rata-rata VR lag 2–60, bukan pembanding horizon. ACF M1 negatif = mikrostruktur
  (bid-bounce), bukan sinyal. **Signifikansi (KOREKSI B4-07):** ACF1 z = 0,494,
  CI95 [−0,00532, +0,00891] memuat 0; VR z ≈ 0,90/0,20/0,26 (audit independen) —
  seluruhnya tak signifikan vs iid.
- **Uji Lapisan 3:** EV per trade strategi M5/M15 momentum sederhana − cost_basis mean
  sesi (fragmen 4b), walk-forward per tahun.
- **Ambang gugur (KOREKSI B4-06 — ambang lama "≥3 dari 4 tahun OOS" TIDAK DAPAT
  DIEKSEKUSI: span 2023-01-02→2026-10-02 = 3,75 tahun, 2026 hanya 196 hari):**
  EV-after-cost median ≤ 0 di ≥2 dari 3 tahun utuh 2023–2025 OOS (2026 parsial
  dikecualikan sebagai tahun berjalan; ambang 4-tahun penuh MENUNGGU DATA), ATAU
  rata-rata VR OOS ≤ 1.

## H3 — Filter regime volatilitas (basis Q4/Q7, A vs B)

- **Klaim:** H1-2023 (B) berbeda **intensitas**, bukan bentuk: median RV harian B =
  3,648e-5 vs A = 2,292e-5 (1,59×), Cliff δ=−0,384 (KOREKSI B4-08 — konvensi tanda:
  δ = P(A>B) − P(B>A); δ<0 berarti B cenderung LEBIH BESAR), KS p=1,2e-11;
  komposisi tipe-hari tidak terdeteksi beda (p=0,325). Bila beda ini terdeteksi
  real-time dari RV rolling, filter regime menaikkan ketahanan tanpa mengganti aturan.
- **Pendukung:** tabel uji level-hari lengkap + block bootstrap (RV tak marginal);
  range/ATR & ratio_path = "tidak terdeteksi pada n ini" (n-B=116/130).
- **Uji Lapisan 3:** detektor RV rolling 20 hari > ambang → AUC klasifikasi hari-B
  tanpa label strata.
- **Ambang gugur:** AUC ≤ 0,7, ATAU filter memotong >40% hari A tanpa mengurangi
  drawdown (klarifikasi B4-11: drawdown = max peak-to-trough pada kurva ekuitas
  strategi diagnostik Lapisan 3; strategi BELUM dipilih — ambang dievaluasi saat
  strategi ada).

## H4 — Sesi sebagai alpha (basis Q2/Q3 + M2)

- **Klaim (KOREKSI B4-02):** volatilitas terkonsentrasi di jam sesi berlabel
  (M2: 6 jam teratas harus di dalam sesi berlabel) dengan massa |r| London+NY
  78,3% dari massa 6 jam teratas (definisi: Σ|r| pip per sesi pada 6 jam teratas)
  → strategi sesi-pintu layak diuji sebagai alpha kapasitas-rendah. Caveat:
  konsentrasi London/NY parsial, bukan eksklusif (jam 00 UTC peringkat 3 = 100%
  Tokyo; ranking sesi Tokyo>NY menyalahi prior S5 — deviasi dilaporkan jujur).
- **Pendukung:** 6 jam UTC teratas = [14, 13, 0, 15, 12, 7], **semua di dalam sesi
  berlabel (share Off = 0,0; n Off = 0)** → M2 LOLOS dengan guard mesin yang kini
  menegakkan kanon (KOREKSI B4-03: assertion lama `share<0,5` meloloskan 2 jam Off;
  kini `n_Off < 2`); massa London+NY = 0,7827; mean |r| per sesi: London 1,666 ·
  Tokyo 1,439 · Sydney 1,196 · NewYork 1,139 pip/bar (urutan London>Tokyo>Sydney>NY).
- **Temuan deviasi (M1, dicatat sebagai temuan bukan kegagalan):** ranking empiris
  **Tokyo > NewYork** pada label eksklusif — berbeda dari prior sekunder S5
  (London 66 > NY 59 > Tokyo 51 pip). Konsisten dengan keputusan v3.1 bahwa prior S5
  adalah kalibrasi, bukan temuan; prior TIDAK dipakai memaksa kesimpulan.
- **Uji Lapisan 3:** EV-after-cost per jam masuk + stabilitas antar-tahun jam teratas.
- **Ambang gugur:** ≥2 dari 6 jam teratas jatuh di Off pada data OOS baru (kanon M2),
  ATAU EV-after-cost 6 jam masuk H4 ≤ 0 (klarifikasi B4-11: "semua jam" = 6 jam
  masuk H4, bukan 24 jam).

## H5 — Reaksi level syarat biaya rendah (basis Q6 + T-01 + M4)

- **Klaim (KOREKSI B4-04/B4-05):** Q6 menemukan hit-rate level TIDAK melampaui
  placebo secara agregat — temuan negatif. Hipotesis ini mempersempit: pada
  sub-populasi volatilitas tinggi reaksi level mungkin melampaui placebo. Syarat
  biaya kini terukur per sesi (bukan proksi): London 2,08 & Tokyo 1,60 di atas
  biaya; NewYork 0,95 & Sydney 0,80 ter-flag biaya-mendominasi.
- **Pendukung:** Q6 nb04 (real 0,469–0,490; KOREKSI B4-09 — placebo DITAMPILKAN
  DUA VARIAN TERPISAH, bukan rentang rakitan: placebo_acak 0,4989 [0,4831–0,5144];
  placebo_hl 0,4890–0,4922 (KOREKSI B8-04: sebelumnya 0,4890–0,5050 — 0,5050 milik
  placebo_acak; 0,4890 = titik estimasi hl_utc, bukan batas bawah CI [0,4748/0,4798];
  titik estimasi hl 0,4890 tumpang tindih batas atas real 0,490);
  rasio vol/spread kanon M4 (mean|r| terhadap spread p95 per-bar — KOREKSI B4-04,
  proksi mean-D1 yang hampir datar DIGANTI): London 2,0823 · Tokyo 1,5992 ·
  NewYork 0,9488 · Sydney 0,7975 → flag "biaya-mendominasi" (rasio < 1) =
  [NewYork, Sydney] (KOREKSI B4-10: contoh sesi ber-rasio tinggi = London,
  tertinggi — bukan Tokyo). T-01 massa nol = 5,83% (66.817 A / 10.572 B).
- **Uji Lapisan 3:** ulangi protokol placebo nb04 PERSIS, kondisioning kuartil-atas
  ATR hari & sesi; CI bootstrap day-cluster seed 20261006.
- **Ambang gugur:** pada setiap sub-populasi hit-rate real ≤ placebo (CI95 memuat 0)
  → level dinyatakan tak dieksploitasi; disimpan sebagai temuan negatif.

## Integritas sintesis

- Nol hipotesis tanpa metrik pendukung (§11): H1←Q7, H2←Q4, H3←Q4+Q7, H4←Q2/Q3+M2,
  H5←Q6+T-01+M4.
- Dua temuan jujur dicatat: (a) deviasi ranking Tokyo>NY (prior sekunder tak dipakai
  memaksa); (b) KOREKSI B4-04: M4 kini memakai spread p95 per-bar M1 (kanon
  `eda_design_v3.1.md:64`) — proksi mean-D1 dipertahankan TERCETAK sebagai pembanding
  lama→baru, bukan dipakai klaim.
- Item preregistrasi M3 (KOREKSI B4-12): sensitivitas DST-aware vs cross-tab UTC-tetap
  DIJALANKAN di nb05 sel #17 — urutan sesi & top-6 jam identik pada keduanya,
  share Off xtab = 0,0000 → SETUJU, pelabelan DST-aware tetap primer.
- Ambang falsifikasi semuanya **angka Lapisan 3**, dideklarasikan sebelum uji.

## Self-audit 3×

1. **Correctness** — semua angka cocok output nb05 di disk (sel #7/#9/#10/#13–#18);
   tidak ada angka baru yang dikarang di luar notebook. KOREKSI Batch B: M4 p95
   (2,0823/1,5992/0,9488/0,7975, flag NY+Sydney), z ACF1 0,494 CI memuat 0,
   massa London+NY 0,7827, M3 SETUJU — semuanya dibaca dari output sel, bukan draf.
2. **Bias & asumsi** — H4 tidak disembunyikan walau menyalahi prior sekunder; H5
   tidak mengklaim level "bekerja" — mempertahankan temuan negatif Q6 sebagai basis;
   H2 tidak mengklaim "terukur" — signifikansi dilaporkan apa adanya (B4-07).
3. **Meta-check** — 5 hipotesis (dalam rentang 3–5 §3 v3.1); setiap satunya punya
   ambang yang bisa menggugurkan; tidak ada pemilihan metode.

## Yang belum diverifikasi

- Seluruh hipotesis **belum diuji** — uji milik Lapisan 3.
- report.md konsolidasi (tahap 13) menyusul; audit Klenz di akhir rantai.
