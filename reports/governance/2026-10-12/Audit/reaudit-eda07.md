# Re-audit EDA-07 — Label, Fitur, dan Gerbang G1–G4

**Tanggal**: 2026-10-12
**Status**: LOLOS PROSEDURAL — 7 temuan (0 TINGGI, 2 MENENGAH, 4 RENDAH, 1 INFORMATIF)
**Sifat**: Deskriptif. Tanpa model, tanpa backtest, tanpa P&L, tanpa vonis edge.

---

## 1. Vonis

**LOLOS PROSEDURAL.** Seluruh angka penentu (gerbang A-2/A-3/A-7, selektor G1–G4, adjudicasi I-1, item C1 dan C3) terhitung ulang dari nol dan **cocok**. Kontrak tidak dilanggar: tidak ada fitur, label, atau irisan baru di luar wewenang; `pdhl_d` tidak pernah dipromosikan; tidak ada model/backtest/P&L; tidak ada perubahan ambang batas.

Dua temuan MENENGAH bersifat **provenance/evidence**, bukan cacat komputasi, dan tidak mengubah satu pun angka atau verdict:

1. Kode beku run 9 menulis ke `2026-10-10`, sedangkan seluruh artefak run 9 berada di `2026-10-12`.
2. `run9.log` dan `run8.log` yang dikutip sebagai bukti mentah tidak ada di repo.

Empat temuan RENDAH (semantik kolom `n_arah`, label "TOP3", satu token hash salah ketik, verdict tidak dipersistensi) dan satu INFORMATIF (byte non-ASCII di notebook).

> **Laporan ini tidak mengatakan apa pun tentang edge.** 98 LOLOS adalah status *deskriptif* — target berfrekuensi tinggi dan fitur asosiasinya, bukan profitabilitas. Lapisan 3 (W-1..W-4) tetap terpisah dan belum diputuskan.

---

## 2. S-0 — Gerbang masuk

| Item | Nilai | Status |
|---|---|---|
| HEAD | `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` | TERVERIFIKASI |
| Branch | `main` | TERVERIFIKASI |
| Staged | `0` | TERVERIFIKASI |
| SHA256 builder run 9 | `BD40E1A35E6A85D9DAA04523B922CA8E4C351C9B2D4B812E2A32F293980BD95F` | TERVERIFIKASI |
| SHA256 builder I-1 | `8775C8A2892F67636BBA5F81B965457F6FA359B5CED83CEBC2F501F14C0E08B0` | TERVERIFIKASI |
| SHA256 builder I-2 | `A388472581CA7C9032FF2A3E07EBD3A739AD9C63FF75D8BF85BE02F6E34FBAE9` | TERVERIFIKASI |
| SHA256 NB run 9 | `4F1F98E6A3E5D0EFA37EA6D8E9D4623AE56CDC7223C08724450654C0C70F7766` | TERVERIFIKASI |
| SHA256 NB I-1 | `F1488991593A4D1F8BE175D2196E819052C3454F4FA33C171CBA328F716E6A91` | TERVERIFIKASI |
| SHA256 NB I-2 | `442720BA70BD1333C6B77D1921FF84A002858FCB7808C9996B809DD8E173085E` | TERVERIFIKASI |
| Referensi `eda_06_biaya_breakeven.ipynb` | `6a6c6516bc96e7e9a7845a13b1909927cc718e75` | TERVERIFIKASI |
| Referensi `EDA_06_07_rancangan.md` | `6724c37ec5493b821d0179d0d00768fbd343a485` | TERVERIFIKASI |
| Hash beku klaim coder I-2 | 13 token | **12 COCOK, 1 salah ketik (T-5)** |

**HEAD tetap** `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` dengan staged `0`. Semua file beku dibaca-saja; tidak ada file production yang disentuh. Harness audit berada di `C:\Users\Fajar\AppData\Local\Temp\opencode\audit-eda07\`.

### 2.1 Ringkasan format

| File | Bytes | non-ASCII | CRLF | tail-LF |
|---|---|---|---|---|
| `_build_eda07.py` | 69.252 | 0 | 0 | ya |
| `_build_eda07_i1.py` | 63.137 | 0 | 0 | ya |
| `_build_eda07_i2.py` | 81.200 | 0 | 0 | ya |
| `eda_07_label_fitur.ipynb` | 78.604 | 15 | 0 | ya |
| `eda_07_i1_adendum.ipynb` | 94.783 | 0 | 0 | ya |
| `eda_07_i2.ipynb` | 162.728 | 15 | 0 | ya |

Ketiga builder **ASCII/LF/tail-LF** sesuai klaim. Dua notebook memiliki 15 byte non-ASCII (karakter elipsis `…` di teks kontrak) — klaim coder hanya mencakup builder, jadi **bukan** temuan; dicatat sebagai T-7.

---

## 3. Klaim & Bukti

### A1 — Fondasi

| Klaim | Bukti independen | Sumber | Status |
|---|---|---|---|
| Holdout 2026 dikecualikan | `bar tepi holdout dikeluarkan: 0`; `max(utc) < 2026-01-01` | sel07 | TERVERIFIKASI |
| Partisi strata utuh | `A=885.854 + B=185.248 + C=6.899 = 1.078.001` | sel07 | TERVERIFIKASI |
| B = 185.248 (jumlah baris strata B) | `PASS: strata konsisten EDA-06 (B=185.248, partisi utuh, tanpa Off di A, tanpa 2026)` | sel07 | TERVERIFIKASI |
| 5 semester A | `['2023H2','2024H1','2024H2','2025H1','2025H2']` | sel07 | TERVERIFIKASI |
| Sidik jari definisi sesi | `PASS: definisi sesi identik Notebook 00 (sidik jari cocok)` | sel04 | TERVERIFIKASI |
| Anti-lookahead acak | `PASS: anti-leakage 200/200 identik (rtol=1e-9, lookback 20.000 bar)` | sel16 | TERVERIFIKASI |
| Rekap ATR tanpa look-ahead | `PASS: ATR 12 timestamp hitung-ulang identik` | sel09 | TERVERIFIKASI |
| 23 irisan tercile + 7 sesi | T-06-7 = 144 dan 48 baris data | T-06-7 | TERVERIFIKASI |

> **Jangkar silang EDA-06**: `1.078.001 bar, N_ENT 184.731` (sel02). `N_ENT` adalah hitungan entitas dari EDA-06, sedangkan `B = 185.248` adalah hitungan **baris** strata B — dua besaran berbeda, jadi **tidak ada pertentangan numerik**.

### A2 — Gerbang A-2/A-3/A-7 (hitung ulang penuh dari CSV beku)

Tabel `_gate_G2_skrining.csv` (780 baris = 260 target × 3 kontrol) dan `_gate_G2_alarm.csv` (86 baris) dihitung ulang secara independen.

**Kalibrasi noise terhadap teori** — noise harus Idle:

| Metrik | Teori | Noise | pdhl_d | round_d |
|---|---|---|---|---|
| G2a (pooled, `p0=0.025`) | 0.025 | 0.0577 (15/260) | 0.2731 (71/260) | 0.2269 (59/260) |
| G2b (majority ≥4/5, dua arah) | 0.3750 | 0.3538 (92/260) | 0.5577 (145/260) | 0.4000 (104/260) |
| Joint G2 | — | 0.0231 (6/260) | 0.2000 (52/260) | 0.1077 (28/260) |
| **Teori joint** (0.025 × 0.375) | | **0.009375** | — | — |
| **p-tail joint** (binom. eksak) | | 0.6337 | 8.83e-04 | 2.72e-04 |
| **Rasio thd. floor 0.025** | | 0.92× | **8.00×** | **4.31×** |

Teori G2b dua-arah dihitung dari nol dengan enumerasi `k=0..5` untuk kedua tanda: `2 × (C(5,4)+C(5,5))/32 = 12/32 = 0.3750`. Noise teramati 0.3538 berada tepat di bawahnya, sedangkan `pdhl_d` 21,3× dan `round_d` 11,5× di atas teori joint — keduanya melompati ambang G2a secara struktural, bukan acak.

Semuanya **cocok** dengan putusan arsitek `putusan-eda07-g2.md` (V-1: 0.0577/0.3538/0.0231 dan 0.2731/0.5577/0.2000 dan 0.2269/0.4000/0.1077).

**Alarm 86 bukan kebetulan:**

```
P(X >= 86 | n=780, p=0.025) = 8.186827e-30  <  0.01   → ALARM sah
P(X >=  6 | n=260, p=0.025) = 0.6337            → noise kompatibel Idle
```

Ditambah struktur: `pdhl_d` 8,00× langka dari floor dan `round_d` 4,31×, keduanya signifikan, sementara noise tidak. Gate A-2/A-7 **terverifikasi penuh**.

**Himpunan alarm = himpunan `G2a ∧ G2b`**, selisih ∅. Alarm hanya berisi kontrol `pdhl_d` (52) dan `round_d` (28) plus 6 noise — **nol kontrol non-alarm lolos, nol alarm lolos gate tanpa G2a**. Sumber `maj = max(nz.count(1), nz.count(-1))` di builder cocok dengan perilaku yang teramati (lihat T-3).

### A3 — V-2/V-4 Adjudikasi I-1

`T-I1-1/2/3.csv` masing-masing 86 baris, himpunan `(target,kontrol)` identik dengan 86 alarm.

| Metrik | Nilai | Klaim arsitek | Status |
|---|---|---|---|
| Q2 DEKAT-mendominasi | 10 (semua round_d) | 10 | TERVERIFIKASI |
| Q2 JAUH-mendominasi | 39 (semua pdhl_d) | 39 | TERVERIFIKASI |
| Q2 tak-beda | 37 | 37 | TERVERIFIKASI |
| Q2 noise | 0/6 signifikan (6 tak-beda) | 0 | TERVERIFIKASI |
| Q3 Bertahan | 16 (9 pdhl_d + 7 round_d) | 16 | TERVERIFIKASI |
| Q3 Lenyap | 70 | 70 | TERVERIFIKASI |
| Vonis V-2 ASLI | 7 | 7 | TERVERIFIKASI |
| Vonis V-2 ARTEFAK | 79 | 79 | TERVERIFIKASI |

Hitungan ulang aturan V-2 dari nol (`ASLI ⟺ Q2 DEKAT ∧ Q3 Bertahan`) menghasilkan **7/86 identik** dengan `T-I1-3.csv` — nol ketidakcocokan. Tujuh ASLI = himpunan V-5 tepat:

```
LB_rng London t3 N5    LB_rng London tALL N5
LB_bin Tokyo t2 N15    LB_bin Tokyo tALL N5   LB_rng Tokyo tALL N5
LB_bin Tokyo tALL N15  LB_rng Tokyo tALL N15
```

Seluruhnya kontrol `round_d`; **nol** `pdhl_d`. Putusan struktural-noise diterapkan dengan benar: `pdhl_d` 52 pasangan seluruhnya artefak, tidak satu pun lolos ke kandidat.

**Klausa preregistrasi X_PIN:**

| Aspek | Nilai | Status |
|---|---|---|
| `X_PIN` | 10 pip, ditetapkan di sel04 NB I-1 | TERVERIFIKASI |
| Seed Q2 / Q3 | `80701` / `80702` (terpisah) | TERVERIFIKASI |
| Stream bootstrap | `rng_q2` dan `rng_q3` terpisah | TERVERIFIKASI |
| Target ganda | 0 (tiap pasangan menghasilkan satu Putusan V-2) | TERVERIFIKASI |

### A4 — C1 Ulang Hitung (irisan)

Tabel `T-06-7_gerbang_tercile.csv` (144 baris data = 12 kombinasi × 4 sesi × 3 tercile) dan `_sesi.csv` (48 baris = 12 × 4). Diverifikasi terhadap run 9/I-1: semua tercile ∈ {1,2,3}, sesi ∈ 4 sesi.

Output NB I-2 `sel20` (tabel `PERINGKAT-IRISAN`) berisi **37 baris**:

| Komponen | Jumlah | Sumber |
|---|---|---|
| Irisan tercile LOLOS | 23 | T-06-7 tercile |
| Irisan sesi LOLOS | 7 | T-06-7 sesi |
| **Irisan real** | **30** | cocok dengan `iris_ter_nol`/`iris_ses_nol` di builder |
| Pseudo-irisan (t=0) | 7 | tidak ada di T-06-7 |
| **Total baris tabel** | **37** | **30 + 7 ✓** |

Tujuh pseudo-irisan seluruhnya `t=0` — **nol** dari ketujuhanya ada di T-06-7 (`atr_ter_s ∈ {1,2,3}`). Semua `n_lolos=0` dan `delta=NaN`.

**Dampak verdict: tidak ada.** Target yang dinilai dihitung sebelum agregasi per-irisan, sehingga baris `t=0` tidak pernah masuk hitungan. **FIG-pick = rank-1 = `("ses", "ATR_k1.5_rr1.4", "Tokyo", 0)` — irisan real**, bukan pseudo. Tidak ada kandidat yang terpengaruh.

### A5 — C3 Ulang Hitung (selektor G1–G4)

`T-07-3_lift.csv` = 1.315 baris / 260 target unik. Hitungan ulang:

| Metrik | Nilai | Status |
|---|---|---|
| Baris G3=True | 153 | TERVERIFIKASI |
| Lift negatif | 33 | TERVERIFIKASI |
| Baris G3 bertentangan dengan aturan CI | **0** | TERVERIFIKASI |
| G4 terisi | 307 baris (60 target LA), seluruhnya `False` | TERVERIFIKASI |
| G4 kosong = `NA` (non-LA) | 1.008 baris / 200 target | TERVERIFIKASI |

Aturan G3 = "CI 95% tidak memuat 0", **tanpa syarat arah**. 33 baris lift negatif tetap sah (CI seluruhnya di bawah 0). Nol baris melanggar aturan — implementasi konsisten dengan kontrak.

**Tujuh kandidat V-5, diperiksa satu per satu:**

| Target | G2a | G2b | G2 | G3 | lift | G4 | Vonis |
|---|---|---|---|---|---|---|---|
| `LB_rng London t3 N5` | T | T | T | **F** | −0.5562 | NA | GUGUR (CI memuat 0) |
| `LB_rng London tALL N5` | T | T | T | **F** | −0.4129 | NA | GUGUR (CI memuat 0) |
| `LB_bin Tokyo t2 N15` | T | T | T | T | −0.0473 | NA | LOLOS |
| `LB_bin Tokyo tALL N5` | T | T | T | T | −0.0549 | NA | LOLOS |
| `LB_rng Tokyo tALL N5` | T | T | T | T | −0.7446 | NA | LOLOS |
| `LB_bin Tokyo tALL N15` | T | T | T | T | −0.0279 | NA | LOLOS |
| `LB_rng Tokyo tALL N15` | T | T | T | T | −1.5868 | NA | LOLOS |

Dua London gagal **karena CI-nya memuat 0** — inilah pembeda antara "lift negatif besar" dan "signifikan". Lima Tokyo lolos dengan CI seluruhnya negatif. Semua G4 `NA` karena bukan target LA. Verdict: **5 LOLOS, 2 GUGUR** ✓ sesuai klaim.

**Regresi dan determinisme:**

| Perbandingan | Baris | Status |
|---|---|---|
| `_gate_G2_alarm.csv` vs `_i2` | 86 × 3 | **BIT-IDENTIK** |
| `_gate_G2_skrining.csv` vs `_i2` | 780 × 5 | **BIT-IDENTIK** |
| `_ckpt_LA.csv` vs `_i2` | 60 × 5 | **BIT-IDENTIK** |
| `_ckpt_T.csv` vs `_i2` | 200 × 5 | **BIT-IDENTIK** |
| Kontrol baru di luar 86 | 0 | TERVERIFIKASI |

Klaim regresi **86/86 + 780/780 terbukti penuh** — nilai tak satu pun bergeser.

### A6 — Scope compliance

| Pemeriksaan | Hasil | Status |
|---|---|---|
| Fitur non-kontrol di T-07-2 | 26 = **tepat** daftar S4, nol tambahan | TERVERIFIKASI |
| `round_d` di T-07-2/3 | hanya pada **tepat 7 target V-5** | TERVERIFIKASI |
| `pdhl_d` di T-07-2/3 | **0 baris** — tidak pernah dipromosikan | TERVERIFIKASI |
| `noise` di T-07-2/3 | **0 baris** | TERVERIFIKASI |
| Baris wakil di T-07-2 | 267 = 260 native + 7 kandidat | TERVERIFIKASI |
| T-07-1 balance | 260 baris, deviasi maks **1e-4** (rounding 4 desimal) | TERVERIFIKASI |
| T-07-4 stabilitas | 1.335 baris, 5 semester A per target | TERVERIFIKASI |
| Larangan model/backtest/P&L | hanya muncul di teks **larangan** | TERVERIFIKASI |
| Drift konstanta penentu | **24/24 identik** di ketiga notebook, diverifikasi independen | TERVERIFIKASI |
| Sel kesimpulan terisi | I-1 sel18 ✓, I-2 sel22 ✓ | TERVERIFIKASI |

Nol temuan cakupan.

**Verifikasi drift K24 secara independen.** Sel06 NB I-2 menyertakan daftar literal `K24` berisi 24 konstanta dan meng-*assert* satu per satu — tetapi *self-check* itu hanya membandingkan nilai terhadap literal yang ditulis ulang di dalam notebook yang sama, bukan terhadap source NB run 9. Auditor karena itu mengekstrak 24 literal itu, lalu membandingkannya dengan definisi aktual di ketiga notebook:

- 18 konstanta non-seed identik secara literal di run 9, I-1, dan I-2 (termasuk tuple-assign `G1_BIN_LO, G1_BIN_HI = 0.10, 0.90` dan `G1_CONT_MIN_N, G1_CONT_MIN_DAYS = 1000, 100`).
- 6 seed `SEED07` identik byte-per-byte di ketiga notebook: `70701 / 70702 / 70703 / 70704 / 70705 / 70800`.
- `N_LEAK = 200` identik di run 9 dan I-2; di I-1 nama itu tidak ada karena diganti `N_LEAK_I1 = 60` (preregistrasi I-1 untuk 86 pasangan) — **bukan drift**.
- `X_PIN = 10` hanya ada di I-1, sesuai preregistrasi adjudicasi I-1.

**Kesimpulan: nol drift ambang/metode.** Verifikasi ini lebih kuat daripada klaim `PASS: 24/24` di sel06, karena membandingkan ke source run 9 dan bukan ke literal turunan.

Byte non-ASCII di dua notebook berada pada teks kontrak (elipsis), bukan kode — di luar klaim format yang hanya mencakup builder (lihat T-7).

---

## 4. Angka yang dihitung ulang dari nol

| Besaran | Klaim | Hitung ulang | Δ |
|---|---|---|---|
| Baris skrining | 780 | 780 | 0 |
| Baris alarm | 86 | 86 | 0 |
| Komposisi alarm | 52 / 28 / 6 | 52 / 28 / 6 | 0 |
| `P(X≥86\|780,0.025)` | < 0.01 | 8.186827e-30 | ✓ |
| Teori G2b majority (dua arah) | 0.375 | 0.3750 (enumerasi k=0..5 × 2 tanda) | 0 |
| Q2 DEKAT / JAUH / sama | 10 / 39 / 37 | 10 / 39 / 37 | 0 |
| Q3 Bertahan / Lenyap | 16 / 70 | 16 / 70 | 0 |
| Vonis V-2 ASLI / ARTEFAK | 7 / 79 | 7 / 79 | 0 |
| Target ganda | 0 | 0 | 0 |
| Baris tabel C1 | 37 = 30 + 7 | 30 + 7 | 0 |
| Baris G3=True | 153 | 153 | 0 |
| Baris G3 bertentangan CI | 0 | 0 | 0 |
| Kandidat LOLOS / GUGUR | 5 / 2 | 5 / 2 | 0 |
| Konstanta penentu (K24) | 24/24 | 24/24 (independen) | 0 |
| Sel kesimpulan I-1 | 86 pasangan | 86 pasangan | 0 |
| Balance sum-to-1 | 220 target diskret | 220 (40 target 1-kelas) | 0 |
| Anti-leakage | 200/200 | 200/200 | 0 |
| Partisi strata | 1.078.001 | 885.854+185.248+6.899 = 1.078.001 | 0 |

---

## 5. Temuan

### T-1 (MENENGAH) — Kode beku run 9 menunjuk ke direktori output yang salah

`scripts/_build_eda07.py` dan NB run 9 menetapkan `REPORT_DIR = 2026-10-10`. Namun seluruh artefak run 9 (`_gate_G2_*`, `_ckpt_*`, `eda07_progress.log`) berada di `reports/eda/2026-10-12`. Direktori `2026-10-10` tidak memuat satu pun `_gate_*`/`_ckpt_*`.

Timeline: builder ditulis 08:59 → gate CSV 10:52:37 → progress log 10:52:15 → notebook ditulis ulang 10:52:40 (oleh builder, bukan `nbconvert`, yang tidak menulis saat assert gagal) → laporan coder 11:01:44.

**Dampak**: nol angka. Tidak ada jalur penulisan yang menghasilkan lokasi tersebut dari kode yang sekarang ada, dan artefaknya sendiri koheren serta tidak saling bertentangan — ini murni isu provenance.

**Rekomendasi**: sebelum mengarsipkan run 9 sebagai "frozen", rekonsiliasi `REPORT_DIR` di builder + notebook dengan lokasi artefak, atau tambahkan README yang menyatakan pemindahan artefak bersifat manual.

### T-2 (MENENGAH) — `run9.log` dan `run8.log` tidak ditemukan

Laporan coder G2 mengutip keduanya sebagai bukti mentah (AssertionError + CellTimeoutError). Pencarian rekursif di `D:\ANN` tidak menemukan keduanya.

**Dampak terbatas, klaim inti tetap terkonfirmasi lewat `mtime`**:

| Artefak | mtime | Run penghasil |
|---|---|---|
| `_ckpt_LA.csv`, `_ckpt_T.csv` | 09:36:43 | run 9 |
| `eda07_progress.log` | 10:52:15 | run 9 |
| `_gate_G2_alarm.csv`, `_gate_G2_skrining.csv` | 10:52:37 | run 9 |
| `T-07-1..4*.csv` | **16:29:18** | **I-2, bukan run 9** |

Pola ini justru **menguatkan** klaim stop: run 9 menghasilkan checkpoint → progress log → gate CSV, lalu berhenti. Tidak ada satu pun `T-07-*` bercap waktu run 9 — sesuai prinsip A-5 (tulis bukti ke disk **sebelum** assert, lalu STOP). `eda07_progress_run8.log` yang berakhir di T183/200 juga konsisten dengan klaim timeout 3.600 s.

**Bukti yang benar-benar hilang**: teks persis `AssertionError` (pesan stop run 9) dan `CellTimeoutError` (run 8). Keduanya tidak dapat direkonstruksi dari artefak yang tersisa — urutan tahap dapat dibuktikan, tetapi **isi pesannya tidak**.

**Rekomendasi**: lampirkan log, atau nyatakan eksplisit sebagai belum terverifikasi.

### T-3 (RENDAH) — `n_arah` punya dua makna berbeda

`_gate_G2_alarm.csv` → `n_arah` = `maj` (jumlah tanda dominant). `_gate_G2_skrining.csv` → `n_arah` = `len(nz)` (jumlah arah nonnol). Pada 44 dari 86 baris, keduanya berbeda.

**Dampak**: nol. Gate `G2b` sendiri memakai `maj`, bukan kolom `n_arah`, sehingga himpunan alarm tetap identik dengan `G2a∧G2b` (terverifikasi). Hanya kolomnya yang menyesatkan pembaca.

**Rekomendasi**: ganti nama menjadi `n_maj` (alarm) dan `n_nonzero` (skrining).

### T-4 (RENDAH) — "TOP3" adalah tiga baris pertama, bukan tiga lift tertinggi

Kolom TOP3 pada output NB I-2 berisi `LB_bin London t1 N5`, `LB_rng London t1 N5`, `LC1 London t1 N5` — tiga baris **pertama** pada tabel. Tiga lift G3-pass tertinggi sebenarnya:

| Target | Fitur | lift | CI |
|---|---|---|---|
| `LB_rng Tokyo t3 N60` | rv15 | 39.5192 | (29.5278, 50.0379) |
| `LB_rng London tALL N60` | rv60 | 36.6588 | (33.7614, 39.7958) |
| `LB_rng Tokyo tALL N60` | rv60 | 34.8501 | (29.7454, 40.4887) |

**Dampak**: hanya katalog presentasi, bukan komputasi. Tidak ada verdict yang bergantung padanya. Namun label "TOP3" menyiratkan "teratas" dan dapat menyesatkan pembaca.

### T-5 (RENDAH) — Satu token hash salah ketik

Laporan coder I-2 mencantumkan 13 hash beku. Dua belas cocok. `T-I1-1.csv` diklaim `DCDFF41882CB…`, aktual `DCDFF41882C1…` — berbeda **satu karakter terakhir**. `T-I1-2.csv` (`83046E121F6D…`) dan `T-I1-3.csv` (`A1BC480AEF3F…`) cocok.

**Bukan manipulasi**: `mtime` `T-I1-1.csv` = 13:47:19, sama dengan T-I1-2/3, yakni **sebelum** build I-2 (14:21) dan run I-2 (16:29). Isi file konsisten dengan gate run 9 (`(target,kontrol)` identik 86). Ini transkripsi, bukan perubahan file.

**Rekomendasi**: koreksi satu karakter di laporan coder.

### T-6 (RENDAH) — Verdict final tidak dipersistensi di CSV

`98 LOLOS / 162 GUGUR` dan tabel `TARGET-LOLOS` hanya ada di output sel notebook, bukan di CSV terpisah. CSV T-07-* berisi metrik G1–G4 per fitur, bukan verdict akhir. Auditor harus mengekstrak dari output notebook.

**Dampak**: tidak membatalkan apa pun, tetapi menambah gesekan. Output notebook terisi penuh, jadi verdict dapat diverifikasi.

### T-7 (INFORMATIF) — 15 byte non-ASCII pada dua notebook

`eda_07_label_fitur.ipynb` dan `eda_07_i2.ipynb` masing-masing memuat 15 byte non-ASCII (karakter elipsis pada teks kontrak), sedangkan ketiga builder 100% ASCII. Klaim format coder hanya mencakup builder sehingga **bukan pelanggaran**. Dicatat agar ekspektasi "semua file ASCII" tidak diasumsikan diam-diam.

---

## 6. Yang belum diverifikasi

1. **Provenance penuh artefak run 9** — T-1 dan T-2 saling menutupi sebagian: lokasi output dan log eksekusi yang hilang membuat rantai resmi sulit direkonstruksi. Yang **dapat** diverifikasi (hash, isi CSV, kemutuan, partisi, gate) sudah diverifikasi; yang **tidak dapat** adalah urutan eksekusi menit-per-menit.
2. **Teks persis exception run 8/run 9** — `AssertionError` (stop run 9) dan `CellTimeoutError` (run 8) tidak direkonstruksi dari artefak mana pun yang tersisa (lihat T-2).
3. **Replikasi penuh run 9 dalam lingkungan audit** — tidak dilakukan. Menjalankan builder/notebook beku berada di luar cakupan audit read-only dan berisiko, sehingga verifikasi dibatasi pada reading sumber + hitung ulang dari CSV beku. Konsekuensinya, temuan T-1 **tidak bisa** ditutup hanya dengan pemeriksaan file: butuh penjelasan dari pihak yang menjalankan.

---

## 7. Rekomendasi

1. **T-1**: rekonsiliasi `REPORT_DIR` builder + NB run 9 dengan lokasi artefak sebelum arsip beku.
2. **T-2**: lampirkan `run9.log`/`run8.log`, atau nyatakan eksplisit sebagai belum terverifikasi.
3. **T-3**: ganti nama kolom `n_arah` → `n_maj` (alarm) dan `n_nonzero` (skrining) di builder berikutnya.
4. **T-4**: ganti label "TOP3" → "3 baris pertama tabel", atau urutkan benar-benar.
5. **T-5**: koreksi satu karakter di laporan coder I-2.
6. **T-6**: pertimbangkan CSV verdict terpisah untuk run berikutnya.
7. **T-7**: tidak ada tindakan; cukup dicatat.
8. **Tidak ada rekomendasi substantif** untuk Gate A-2/A-7, V-2/V-4, C1, maupun C3 — semuanya lolos tanpa catatan.

---

## 8. Output mentah (kunci)

Semua harness di `C:\Users\Fajar\AppData\Local\Temp\opencode\audit-eda07\`:

| Skrip | Isi | Fungsi |
|---|---|---|
| `a2_alarm.py` | A2 binomial + komposisi | A2/A-7 |
| `a3_g2b.py` | Teori G2b majority | A3 |
| `a5_narah.py` | Dual semantics `n_arah` | T-3 |
| `a7_fix.py` | Aturan V-2 + set ASLI | A3 |
| `a8_nb.py` | Struktur notebook, X_PIN, seeds | A3 |
| `a10_drift_nb.py` | Drift konstanta | A6 |
| `a11_log.py` | Log dan REPORT_DIR | T-1/T-2 |
| `a14_c1b.py` | C1 hitung ulang | A4 |
| `a15_rank.py` | Tabel PERINGKAT-IRISAN | A4 |
| `a16_c3.py` | G3/G4 | A5 |
| `a17_final.py` | Ringkasan angka | §4 |
| `a18_scope.py` | Scope, sel kesimpulan, format | A6 |
| `a19_kand.py` | 7 kandidat V-5 | A5 |
| `a20_close.py` | Balance, 13 hash, regresi | A5/A6 |
| `a21_scope2.py` | Hash I-2, larangan, verdict | A6 |
| `a22_fix.py` | Konfirmasi hash, konteks, ASCII | T-5/T-7 |
| `a23_claimcheck.py` | Verifikasi klaim sel02/04/06/07 | A1 |
| `a24_k24.py` | Penelusuran daftar K24 + bukti sel | A6 |
| `a25_k24verify.py` | K24 vs source run 9/I-1/I-2 | A6 |
| `a26_k24numeric.py` | K24 bandingan numerik final | A6 |

Output teks mentah setiap skrip tersimpan sebagai `*_out.txt` di direktori yang sama.

Tidak ada file production yang dimodifikasi.

---

*Laporan ini bersifat prosedural. Tidak memuat vonis edge, profitabilitas, atau rekomendasi strategi.*
