# Kunci Hipotesis v1 — EDA USDJPY 2023–2026 → Lapisan 3

**Tanggal lock:** 2026-10-07
**Status:** BEKU — redaksi di bawah tidak boleh diubah kecuali addendum berversi
**Sumber redaksi:** `reports/eda/progress/06-regimes/laporan_tahap_12_sintesis.md`
**Sumber angka:** output notebook `eda_05_regimes.ipynb` (blob `661c0aeb2357…`),
  sel #13–#18, via nbformat
**Konsolidasi:** `reports/eda/2026-10-06/report.md`
**Putusan arsitek H1 vs cemaran reversal-day:** 2026-10-07 (opsi iii)

---

## H1 — Regime tipe-hari (basis Q7) — TERKUNCI

**Redaksi (verbatim tahap_12:12–28):**

> Hari terbagi dalam tipe terukur (trending/normal/range dari ratio_path &
> range/ATR vs median A); kelanjutan arah pada hari trending layak diuji.
> Bucket "range" = hari TENANG (kedua metrik ≤ median-A: volatilitas & range
> terendah — bukan "choppy lebar").

**Basis EDA:** trending 33,7% · range 33,8% · normal 32,5% (stratum A);
chi-square tipe-hari A-vs-B p=0,325 (n-A=825, n-B=116).

**Uji Lapisan 3:** conditioning tipe hari (identifikasi H+1 pagi, data t-1 saja):
drift berarah RELATIF M15 4 jam pertama London (dinormalisasi ATR harian t-1)
pada hari trending vs range, sign test + CI.

**Ambang gugur:** selisih drift median CI95 memuat 0, ATAU share trending tak
stabil antar tahun (chi-square antar-tahun p<0,01).

**Catatan ex-post (L3-01 opsi b):** ambang tipologi = median full-sample A
(ratio_path 0,0268; range/ATR 88,79) → share deskriptif ex-post, bukan hasil
klasifikasi real-time; uji Lapisan 3 memakai identifikasi H+1 pagi real-time.

### Catatan risiko reversal-day (putusan arsitek 2026-10-07, opsi iii)

(a) Mekanisme cemaran: hari pembalikan tak terbedakan oleh klasifikasi t-1 dan
masuk keranjang trending. (b) Arah bias: melemahkan efek ke arah gagal, BUKAN
ke arah lulus palsu — reversal-day menarik median keranjang trending ke arah
median keranjang range; uji median + sign test kebal terhadap minoritas ekstrem
(spike terminal tidak menggerakkan median kecuali menjadi mayoritas); metrik
hanya 4 jam pertama London sehingga reversal siang/sore bukan cemaran.
(c) Status intervensi: terkurung tiga lapis (intervensi BoJ jarang; median/sign
kebal minoritas ekstrem; zona 150/155/160 tereksklusi ke strata C) — tanpa
penanganan khusus untuk H1.

**Klausul anti-penyelamatan (mengikat):** "Cemaran reversal-day yang tercatat di
sini BUKAN dasar untuk menafsir ulang kegagalan H1. Conditioning usia-tren
pasca-hoc setelah melihat hasil = hipotesis baru yang wajib pra-registrasi
segar dan diuji di data segar."

**Izin eksplorasi:** Lapisan 3 BOLEH melaporkan split-usia tren sebagai analisis
eksplorasi murni — berlabel eksplorasi, tanpa pengaruh apa pun pada vonis
LULUS/GAGAL H1.

---

## H2 — Mikro-momentum M15 (basis Q4) — TERKUNCI

**Redaksi (verbatim tahap_12:30–51):**

> Pola horizon-pendek M15-A lemah dan SECARA STATISTIK TAK TERBEDAKAN dari iid
> → trend-following M15 layak diuji dengan biaya penuh SEBAGAI HIPOTESIS
> EKSPLORATORI; EDA tidak mengklaim sinyal terdeteksi.

**Basis EDA:** ACF1 M15-A = +0,001793; sign-ACF(1) no-gap = −0,022624 (identik
nb03, n_no_gap 75.038); VR(5)=1,0160, VR(15)=1,0119, VR(60)=1,0657; rata-rata
VR = 1,0312. Signifikansi: ACF1 z = 0,494, CI95 [−0,00532, +0,00891] memuat 0;
VR z ≈ 0,90/0,20/0,26 — seluruhnya tak signifikan vs iid. ACF M1 negatif =
mikrostruktur (bid-bounce), bukan sinyal.

**Uji Lapisan 3:** EV per trade strategi M5/M15 momentum sederhana − cost_basis
mean sesi (fragmen 4b), walk-forward per tahun.

**Ambang gugur:** EV-after-cost median ≤ 0 di ≥2 dari 3 tahun utuh 2023–2025
OOS (2026 parsial dikecualikan sebagai tahun berjalan; ambang 4-tahun penuh
MENUNGGU DATA), ATAU rata-rata VR OOS ≤ 1.

---

## H3 — Filter regime volatilitas (basis Q4/Q7, A vs B) — TERKUNCI

**Redaksi (verbatim tahap_12:53–67):**

> H1-2023 (B) berbeda intensitas, bukan bentuk. Bila beda ini terdeteksi
> real-time dari RV rolling, filter regime menaikkan ketahanan tanpa mengganti
> aturan.

**Basis EDA:** median RV harian B = 3,648e-5 vs A = 2,292e-5 (1,59×),
Cliff δ=−0,384 (δ = P(A>B) − P(B>A); δ<0 berarti B cenderung LEBIH BESAR),
KS p=1,2e-11; komposisi tipe-hari tidak terdeteksi beda (p=0,325).
Range/ATR & ratio_path = "tidak terdeteksi pada n ini" (n-B=116/130).

**Uji Lapisan 3:** detektor RV rolling 20 hari > ambang → AUC klasifikasi hari-B
tanpa label strata.

**Ambang gugur:** AUC ≤ 0,7, ATAU filter memotong >40% hari A tanpa mengurangi
drawdown (drawdown = max peak-to-trough pada kurva ekuitas strategi diagnostik
Lapisan 3; strategi BELUM dipilih — ambang dievaluasi saat strategi ada).

---

## H4 — Sesi sebagai alpha (basis Q2/Q3 + M2) — TERKUNCI

**Redaksi (verbatim tahap_12:69–89):**

> Volatilitas terkonsentrasi di jam sesi berlabel (M2: 6 jam teratas harus di
> dalam sesi berlabel) dengan massa |r| London+NY 78,3% dari massa 6 jam
> teratas → strategi sesi-pintu layak diuji sebagai alpha kapasitas-rendah.
> Konsentrasi London/NY parsial, bukan eksklusif.

**Basis EDA:** 6 jam UTC teratas = [14, 13, 0, 15, 12, 7], semua di dalam sesi
berlabel (share Off = 0,0; n Off = 0; guard `n_Off < 2`); massa London+NY =
0,7827; mean |r| per sesi: London 1,666 · Tokyo 1,439 · Sydney 1,196 ·
NewYork 1,139 pip/bar. Deviasi tercatat: ranking empiris Tokyo > NewYork
menyalahi prior sekunder S5 — prior tak dipakai memaksa kesimpulan. M3:
sensitivitas DST-aware vs cross-tab UTC-tetap SETUJU (urutan sesi & top-6 jam
identik; share Off xtab = 0,0000).

**Uji Lapisan 3:** EV-after-cost per jam masuk + stabilitas antar-tahun jam
teratas.

**Ambang gugur:** ≥2 dari 6 jam teratas jatuh di Off pada data OOS baru (kanon
M2), ATAU EV-after-cost 6 jam masuk H4 ≤ 0.

---

## H5 — Reaksi level syarat biaya rendah (basis Q6 + T-01 + M4) — TERKUNCI

**Redaksi (verbatim tahap_12:91–111):**

> Q6 menemukan hit-rate level TIDAK melampaui placebo secara agregat — temuan
> negatif. Hipotesis ini mempersempit: pada sub-populasi volatilitas tinggi
> reaksi level mungkin melampaui placebo.

**Basis EDA:** Q6 nb04 — real 0,469–0,490; placebo_acak 0,4989 [0,4831–0,5144];
placebo_hl 0,4890–0,4922 (0,4890 = titik estimasi hl_utc, bukan batas bawah CI
[0,4748/0,4798]; titik estimasi hl tumpang tindih batas atas real 0,490).
Rasio vol/spread kanon M4 (mean|r| terhadap spread p95 per-bar): London 2,0823
· Tokyo 1,5992 · NewYork 0,9488 · Sydney 0,7975 → flag "biaya-mendominasi"
(rasio < 1) = [NewYork, Sydney]. T-01 massa nol = 5,83% (66.817 A / 10.572 B).

**Uji Lapisan 3:** ulangi protokol placebo nb04 PERSIS, kondisioning
kuartil-atas ATR hari & sesi; CI bootstrap day-cluster seed 20261006.

**Ambang gugur:** pada setiap sub-populasi hit-rate real ≤ placebo (CI95 memuat
0) → level dinyatakan tak dieksploitasi; disimpan sebagai temuan negatif.

---

## Verifikasi penulisan (asisten)

Redaksi H1–H5 dan seluruh angka di atas dibaca ulang terhadap
`tahap_12_sintesis.md` baris 12–111 sebelum tulis — cocok. Klausul
anti-penyelamatan dan catatan risiko H1 disalin dari putusan arsitek
2026-10-07 (opsi iii) tanpa diubah.

## Yang belum diverifikasi

- Frekuensi persis hari intervensi BoJ (dinyatakan PERLU VERIFIKASI oleh
  arsitek; putusan H1 tidak bergantung padanya).
- Seluruh H1–H5 belum diuji — uji milik Lapisan 3 (walk-forward, biaya penuh).
