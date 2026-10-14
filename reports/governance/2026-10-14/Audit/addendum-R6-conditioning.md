# AUDIT ADDENDUM - R6-conditioning (2026-10-14)

Status: TAMBAHAN terhadap audit independen spec R6.
Vonis atas spec: **TOLAK EKSEKUSI** - 4 cacat FATAL + 2 blocking, diverifikasi ulang.
Spec `spesifikasi-discovery-R6-conditioning.md` **TIDAK diubah** (masih DRAF, tidak pernah dieksekusi).
Ronde R6 **DITARIK**, bukandi-refute: desainnya tidak mampu menghasilkan verdict yang
memiliki hubungan evidential dengan hipotesisnya.

Alasan addendum: arsitek memverifikasi ulang setiap klaim K1-K6 dan D1-D13 dari
evidence beku. Auditor benar pada semua poin. arsitek menemukan satu cacat tambahan
yang tidak tercatat di laporan auditor: **ambang G2 = Edge >= 0,56 sudah
terbukti tidak cukup**, karena data beku R4 sendiri memuat sel pada Edge 0,602
yang tetap rugi.

---

## B0. Ringkasan disposition

| Temuan | Klaim auditor | Hasil verifikasi arsitek | Disposisi |
|---|---|---|---|
| K1 | rumus 1/3 benar | **BENAR** (gambler's ruin a=1,b=2) | diterima, tapisee B2 |
| K2 | rumus impas benar | **BENAR** secara matematis | diterima |
| K2 | SL 17,464; c ~0,92-1,0 | **BENAR** | diterima |
| K3 | pooled 23,94%; median sejati 19,29% | **BENAR** | diterima |
| K4 | Edge 0,3725-0,5027 | **BENAR** | diterima |
| K5 | TP +66.797 / SL -121.519 / TIME +28.107 | **BENAR** - klaim spec salah | diterima |
| K5 | "bucket SL 44,96%" | **BENAR** | diterima |
| K6 | baseline acak 13,50 pip tidak bersumber | **BENAR** | diterima |
| D1 | §0 salah argumen | **BENAR** | diterima |
| D4 | 39/52 bin mati struktural | **BENAR** | diterima |
| D5 | G2 tanpa justifikasi | **BENAR** | diterima + diperkuat (B3) |
| D6 | G5 bersandar noise E3 | **BENAR** | diterima |
| D7 | G6 inert | **BENAR** | diterima |
| D8-D13 | LULUS / CATATAN | tidak ada klaim yang ditolak | diterima |

Tidak ada temuan auditor yang ditolak. Tidak ada temuan auditor yang diperbaiki.

---

## B1. Kesalahan numerik penulis spec (§0) - dikonfirmasi

### B1.1 Dekomposisi P&L salah skala

Spec §0 menyebut `TP +56.654 / SL -102.038 / TIME +28.107`.

Ternilai dua-duanya adalah `jumlah_event x median_per_event`, bukan `sum`:

```
TP  1487 x  38,10 =  56.655   vs  sum(grossA | TP)   =  +66.797
SL  4724 x -21,60 = -102.038  vs  sum(grossA | SL)   = -121.519
TIME 4297 x   4,40 =  18.907   vs  sum(grossA | TIME) =  +28.107
```

Yang benar (A-leg, post-cancel, excl-B-AMBIGUOUS, n = 10.508):

| Outcome | n | sum(grossA) | median(grossA) |
|---|---|---|---|
| TP | 1.487 | **+66.797,0 pip** | +38,10 |
| SL | 4.724 | **-121.519,4 pip** | -21,60 |
| TIME | 4.297 | **+28.107,1 pip** | +4,40 |
| **TOTAL** | 10.508 | **-26.615,3 pip** | - |

Net setelah biaya (`netA_obs`) = **-36.510,6 pip**.

Kesalahan arahnya **tidak konservatif**: selisih terbesar justru pada bucket
pembunuh (SL dikecilkan ~16%), sehingga spec tampak lebih optimistis dari kenyataan.

### B1.2 "median 23,9%" adalah pooled, bukan median

`23,9%` = 1.487 / 6.211 = **23,94% pooled**. Median sebenarnya dari 9 sel =
**19,29%** (sorted: 13,7 / 15,3 / 17,3 / 18,6 / 19,3 / 21,0 / 24,8 / 24,9 / 26,8).

Kesalahan redaksi. Tidak mengubah arah kesimpulan.

### B1.3 Baseline acak 13,50 pip tidak bersumber dari R4

Angka ini dihitung arsitek pada sesi terpisah, **tidak ada** di `qc.json`,
`summary.json`, `events.parquet`, atau `r4_m15.py` (yang `rng` dipakai untuk
bootstrap multinomial, bukan random entry). Spec B2 mengaitkannya ke R4 sebagai
baseline in-run; tidak dapat direproduksi. Diterima.

---

## B2. Argumen §0 tidak berlaku untuk struktur exit sebenarnya

Tiga lapis, semua benar menurut auditor dan dikonfirmasi:

1. **`P(+2R sebelum -1R) = 1/3` benar** untuk Brownian motion tanpa drift dengan
   barrier asimetris (gambler's ruin, `a/(a+b)`, a=1, b=2). Rumus tidak salah.

2. **Tapi argumen "tepat impas" salah**, karena exit TIME memotong ekor. **40,89%
   exit adalah TIME**, dan RR terealisasi hanya **1,09-1,67**, bukan 2,00. Pada
   payoff yang benar-benar ±2R tanpa TIME, 1/3 memang impas; pada payoff yang
   ebenar ada, tidak.

3. **Ambang 35,2% melanggar A7.5.** Angka itu berasal dari rasio nominal
   TP/SL. A3 sudah mengukur impas observatif dari `mean_win` dan `mean_loss`
   nyata, yaitu **37,5% - 47,8%**. A7.5 melarang penggunaan rasio nominal.

Konsekuensi: argumen pembuka R6 bertumpu pada baseline teoritis yang tidak berlaku.
Baseline yang benar untuk R6 adalah `gap_pp` dari A3, yaitu **-0,39 sampai -12,47 pp**.

---

## B3. CACAT TAMBAHAN (tidak tercatat di laporan auditor): G2 sudah refuted oleh data beku

Auditor (D5) menolak G2 `Edge >= 0,56` karena **tidak ada justifikasi
preregistrasi**. Itu benar, tapi belumvagyu. Masalahnya lebih dalam:

**Nilai Edge itu sendiri sudah tercermin di evidence R4, dan di situ tetap rugi.**

Kaki B (E1 dicerminkan) adalah cermin sah yang sudah dihitung di R4. Nilainya:

| Sel | Edge_A | Edge_B | RR_real_B | BE_WR_B | WR_akt_B | gap_pp | median_net_B |
|---|---|---|---|---|---|---|---|
| E1_N3_k1.0 | 0,410 | **0,560** | 0,992 | 50,2% | 45,5% | **-4,7** | - |
| E1_N4_k1.5 | 0,372 | **0,602** | 0,896 | 52,8% | 50,5% | **-2,2** | -0,76 |
| E1_N6_k1.0 | 0,408 | **0,567** | 0,926 | 51,9% | 43,0% | **-9,0** | -6,99 |
| E1_N6_k1.5 | 0,403 | **0,575** | 0,911 | 52,3% | 44,2% | **-8,1** | -6,79 |

Tiga sel **sudah memenuhi G2 = 0,56** (sampai 0,602) dan **ketiganya tetap
negatif**: gap -2,2 sampai -9,0 pp, median net -0,76 sampai -6,99 pip.

### B3.1 Edge bukan ambang kelayakan - Edge adalah skor peringkat

Korelasi di 9 sel:

```
corr(Edge_B, gap_pp)      = -0,189     <-- makin tinggi Edge, makin BURUK P&L nyata
corr(Edge_B, median_net_B) = +0,773     <-- Edge memprediksi URUTAN median net
```

Dua hal ini tidak bertentangan, dan bersama-sama menunjukkan hal yang fatal:

- Edge **valid sebagai metrik peringkat** (ia memprediksi urutan median net).
- Edge **tidak valid sebagai ambang kelayakan**, karena **median net negatif di
  seluruh 9 sel**. Menggate-kan pada 0,56 berarti meminta puncak peringkat dari
  kumpulan yang seluruh anggotanya rugi.

Akar masalahnya: `Edge = median(mfe)/(median(mfe)+median(mae))` memakai **median**,
sedangkan impas tunbledetermined oleh **mean** win dan loss.Selisih median-vs-mean
inilah yang membuat sel ber-Edge tinggi tetap merugi.

### B3.2 Akibat untuk R6

G2 tidak sekadar "tanpa justifikasi" - G2 **sudah terbukti tidak cukup** dengan
data yang ada. R6 akan mencari bin yang mencapai 0,56; kita sudah punya bin di 0,602
yang kalah. Bila R6 tidak menghasilkan bin yang lebih baik, itu **bukan informasi**;
bila menghasilkan, itu selection bias pada 13 bin (masalah yang menurut D7 memang
tidak tertangani G6).

**G2 harus diganti dengan ambang berbasis `gap_pp` yang diukur dari
`mean_win`/`mean_loss` observatif, sesuai A7.5 - bukan Edge.**

---

## B4. Gate R6 yang tidak akan pernah menyala (D4, dikonfirmasi)

Dihitung ulang dari `events.parquet` (A-leg, post-cancel):

| Keluarga | n total | per-tercil | G1 (>=500) | jumlah sel | G5 ("3 dari 9 sel" / "1 keluarga 3 sel") |
|---|---|---|---|---|---|
| E1 | 1.313 | 437,7 | **GAGAL** | 6 | tidak dapat diuji |
| E2 | 9.059 | 3.019,7 | LOLOS | 2 | **MUSTAHIL** |
| E3 | 136 | 45,3 | **GAGAL** | 1 | **MUSTAHIL** |
| POOLED | 10.508 | 3.502,7 | LOLOS | 9 | mungkin |

**39 dari 52 bin (75%) mati sebelum data dilihat.** Yang tersisa hanya 13 bin
pooled, yang 86,2%-nya E2 (9.059 / 10.508).

R6 tidak menguji E1 (G1), tidak menguji E3 (G1 + G5), tidak menguji E2
per-keluarga (G5). Vonis `MATI-KELAS` yang Feministanya dirancang untuk
menutup kelas secara permanen akan menjatuhkan vonis pada kelas yang **tidak
pernah diuji**. Inilah cacat paling fundamental.

---

## B5. Posisi evidence terhadap hipotesis saat spec ditarik

Diragram di bawah bukan ganti R6; ini yang **sudah terukur** pada evidence beku,
supaya vonis penutupan punya dasar numerik dan bukan sekadar ketidakmampuan
mengeksekusi R6.

### B5.1 Realized breakeven kaki A per sel + CI 95% cluster-per-hari

Bootstrap 10.000, seed 1337, resampling **hari** (bukan event).

| Sel | n | BE_WR | WR_akt | gap_pp | CI95 gap_pp | median_net | Edge_A |
|---|---|---|---|---|---|---|---|
| E1_N3_k1.0 | 398 | 44,3% | 35,2% | -9,09 | [-16,02, **-2,24**] | -11,96 | 0,408 |
| E1_N3_k1.5 | 189 | 38,4% | 33,3% | -5,04 | [-16,01, +4,66] | -10,80 | 0,452 |
| E1_N4_k1.0 | 315 | 43,2% | 36,2% | -6,96 | [-15,80, +1,02] | -10,71 | 0,462 |
| E1_N4_k1.5 | 186 | 37,5% | 28,0% | -9,57 | [-21,06, **-0,27**] | -15,45 | 0,372 |
| E1_N6_k1.0 | 121 | 43,4% | 43,0% | **-0,39** | [-15,23, +12,58] | -10,42 | 0,408 |
| E1_N6_k1.5 | 104 | 45,3% | 41,3% | -3,92 | [-21,05, +10,95] | -11,61 | 0,403 |
| E2_W12_k1.5 | 5.422 | 47,5% | 42,5% | -4,99 | [-8,30, **-1,79**] | -6,61 | 0,493 |
| E2_W12_k2.5 | 3.637 | 47,3% | 41,8% | -5,54 | [-9,68, **-1,62**] | -7,40 | 0,492 |
| E3_W16 | 136 | 47,8% | 35,3% | -12,47 | [-23,24, **-1,86**] | -10,06 | 0,503 |

```
Sel significantly positif (CI bawah > 0) : 0 / 9
Sel significantly negatif (CI atas < 0) : 5 / 9
Sel belum terbukti (CI memuat 0)         : 4 / 9
median_net_A < 0 di seluruh 9 sel        : ya
```

### B5.2 Empat sel yang "belum terbukti" bukan kandidat

Keempatnya (E1_N3_k1.5, E1_N4_k1.0, E1_N6_k1.0, E1_N6_k1.5) punya:

- n kecil (104-315), CI lebar ~24-30 pp - tidak informatif
- `Edge_A` **< 0,5 di keempatnya** (0,403-0,452): distribusi ekskursi lebih suka rugi
- `median_net_A` **-10,4 sampai -11,6 pip**: tiap tradenya rugsinga hefty

Sel terdekat impas, `E1_N6_k1.0` (gap -0,39 pp), adalah **artefak mean-vs-median**:
`mean_win`/`mean_loss`-nya kebetulan menya impas pada WR, sementara `median_net`
per trade -10,42 pip dan `Edge_A` 0,408. Bukan sinyal; kebetulan momen.

---

## B6. Batas yang HARUS dicatat dalam vonis penutupan

Agar record jujur, dua hal berikut **tidak boleh** diklaim:

1. **Bukan berarti "conditioning sudah dibuktikan tidak berguna."** Spec R6 ditarik
   karena defective. Tidak ada probe yang valid terhadap hipotesis conditioning yang
   pernah dijalankan. Yang terbukti: **spec yang ada tidak mampu mengujinya**.

2. **Bukan berarti kelas hipotesis ini mustahil secara teoretis.** Yang terbukti
   adalah: **pada bed 2024, pada barrier/entry/exit/biaya yang sama, tidak ada
   sel pun yang menunjukkan P&L positifsignifikan** - 0 dari 9, dengan 5 dari 9
   secara signifikan negatif.

---

## B7. Rekomendasi arsitek

R6 ditarik sebagai **NON-EXECUTABLE** (bukan `INKONSISTEN`, bukan `MATI-KELAS`
dari R6 - R6 tidak pernah jalan).

Untuk kelas hipotesis "fixed-barrier M15 on JPY-pair M1 bars", posisi evidence
yang didukung data adalah:

**MATI-KELAS** dengan dasar:
- 0 / 9 sel significantly positif pada realized breakeven
- 5 / 9 significantly negatif
- seluruh `median_net_A` negatif (-6,61 sampai -15,45 pip)
- ambang kelayakan (`Edge >= 0,56`) terbukti tidak cukup pada data beku sendiri (B3)

Dengan catatan eksplisit B6.1: conditioning belum diuji dengan probe yang valid.

Ronde berikutnya - bila ada - **butuh persetujuan eksplisit owner** dan harus
mengubah struktur kelas (bukan filter di atas barrier yang sama): misalnya
horizon/window berbeda, rezolusi berbeda, atau instrumen berbeda. Itu hipotesis baru,
di luar R6.

---

## Catatan prosedural

- Tidak ada file yang ditulis di repo oleh auditor.
- Spec R6 **tidak diubah**; masih DRAF di `arsitek/`.
- Tidak ada run backtest baru. Semua angka di addendum ini dihitung ulang dari
  `events.parquet` dan `summary.json` yang beku.
- 2023 / 2025 / 2026 tidak dibuka.
- Skrip verifikasi di luar repo: `C:\Users\Fajar\AppData\Local\Temp\opencode\`.
- Angka di B5.1 memakai `day` sebagai unit cluster (cluster-per-hari), sesuai A4.
