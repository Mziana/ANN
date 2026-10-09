# Hasil Lapisan 3-H3 — Uji Prasyarat H3 (materialitas `gap_f2_flag` + sensitivitas TAU)

**Tanggal:** 2026-10-08
**Peran pelaksana:** Coder (§26 AGENTS.md: coder mengeksekusi; DILARANG audit sendiri).
**Spec yang dieksekusi (BUKAN ringkasan mana pun):**
`reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md`
**Cek hash spec SEBELUM eksekusi:** blob `dacd07087f4e1f66154dcc75a259ecfcdb769043`
— cocok prefix `dacd0708` yang disyaratkan brief [O1]. Eksekusi dilanjutkan.
**HEAD saat eksekusi:** `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` [O2].
**Sifat pekerjaan:** read-only terhadap repo; nol tulis produksi; D4 di disk tidak
ditimpa; seluruh skrip/harness HANYA di `%TEMP%\opencode\l3h3`
(`C:\Users\Fajar\AppData\Local\Temp\opencode\l3h3`).
**Berkas hasil ini:** `reports/governance/2026-10-07/coder/hasil-lapisan3-H3.md`.

## 0. Ringkasan hasil (setiap angka mentah di §3–§5)

| Uji | Hasil | Dasar (blok mentah) |
|---|---|---|
| Uji 1 — materialitas `gap_f2_flag` pada klasifikasi H1 | **IMMATERIAL** | M1: verdict gugur-H1 identik pada INK 974 & EKS 740 (keduanya GUGUR) [O8]; M2: χ²=0,9259, p=0,6294 ≥ α=0,01 [O9]; M3: tanda selisih sama dengan B1 (tidak ANOMALI) [O10]; robustness R1–R3: verdict tidak berubah [O8]; keputusan [O11] |
| Uji 2 — sensitivitas TAU (span/window) | **TIDAK STABIL** | K1 GAGAL (A1: AUC 0,1559 < 0,65), K2 GAGAL (agreement min 0,3154), K3 GAGAL (span 2024: median B < A) — identik pada kedua pembacaan agreement [O15] |

**Konsekuensi yang spec nyatakan sendiri** (§Uji-2 "Dampak ke vonis H3 (S4)"):
TIDAK STABIL → **H3 GUGUR via kriteria tambahan S4b**; filter DILARANG diaktifkan
pada data mana pun; S4b tidak mengubah ambang lock dan bukan izin kalibrasi ulang.
S4b adalah keputusan arsitek DI DALAM spec ini, **bukan lock** — coder hanya
melaporkan konsekuensi yang spec tetapkan, bukan memvonis H3 sendiri (§4.6 spec
+ §26 AGENTS.md). Tabel 5 baris (ref + A1–A4) ada di §4.4.

## 1. Klaim & Bukti (§5 AGENTS.md)

| Klaim | Status | Bukti |
|---|---|---|
| Blob spec = `dacd0708…` (cocok) | TERVERIFIKASI | [O1] |
| HEAD tidak berubah (C1) | TERVERIFIKASI | [O2]; status akhir [O20] |
| Nol tulis produksi + nol sentuh lindung (C2) | TERVERIFIKASI (dengan catatan pola, §5 DEV-1) | [O3] status+`find -newermt` kosong; [O4]; hash isi [O5] identik |
| D1/D2/D3/D5 + trio beku cocok hash (C3) | TERVERIFIKASI | [O5] |
| D4 tidak ditimpa | TERVERIFIKASI | [O5] (sha256 + mtime `2026-10-08 15:04`, sebelum tugas) |
| D1 dibaca ulang mereproduksi D4 persis (6/6 kolom, 0 mismatch) | TERVERIFIKASI | [O6] |
| Uji 1: baseline INK ditempel SEBELUM dibandingkan (§21 butir 7) | TERVERIFIKASI | [O7] lalu [O8] |
| Uji 1 M1: verdict gugur-H1 INK = GUGUR; EKS = GUGUR → tidak berbeda | TERVERIFIKASI | [O8] |
| Uji 1 M2: χ²=0,9258779541662121; p=0,629431041054359 (α=0,01) → tidak material | TERVERIFIKASI | [O9] |
| Uji 1 M2 efek: Δshare_trending = +0,019299, CI95 [+0,003008, +0,035234] | TERVERIFIKASI | [O9] |
| Uji 1 M2 tabel 2×3: INK [330,320,324]; EKS [265,243,232] | TERVERIFIKASI | [O9] |
| Uji 1 M3: median `ratio_path` gap 0,025134 vs non-gap 0,027810 → tanda sama dengan B1 (0,0251 vs 0,0280) | TERVERIFIKASI | [O10] |
| Uji 1 robustness R1 (drift tanpa norm), R2 (pembanding normal+range), R3 (kriteria-ii + 2026): verdict tidak berubah | TERVERIFIKASI | [O8] |
| Uji 1 keputusan = IMMATERIAL | TERVERIFIKASI | [O11] |
| Uji 1 determinisme (C5) | TERVERIFIKASI | [O12] |
| Uji 2 baseline: score20 = `rv_roll_20d`/20 (0 titik beda); TAU bit-identik `2.5951672079821496e-05` (runtime & store); n_B/n_A = 111/129 | TERVERIFIKASI | [O13] |
| Uji 2 baseline AUC: rank = 0,8173755150499337; trapesium = 0,8173755150499336 = konstanta lock bit-identik | TERVERIFIKASI | [O13] |
| Uji 2 flag referensi = kolom `rv_regime_flag` D4 (0 beda; 19 NaN; 619 flag-1) | TERVERIFIKASI | [O13] |
| Uji 2 A1–A4: TAU/AUC/n/agreement (dua pembacaan) | TERVERIFIKASI | [O14] |
| Uji 2 tanpa GAGAL-eksekusi (<200 hari evaluable): n evaluable min 230 (primer) / 945 (robust) | TERVERIFIKASI | [O14] |
| Uji 2 K1 GAGAL, K2 GAGAL, K3 GAGAL → TIDAK STABIL (kedua pembacaan sama) | TERVERIFIKASI | [O15] |
| Uji 2 determinisme (C5) | TERVERIFIKASI | [O16] |
| Gate hijau (C4): pytest 254 passed; ruff check rc=0; ruff format rc=0 (37) | TERVERIFIKASI | [O17], [O18] |
| Berkas hasil bebas karakter asing (C4d) | TERVERIFIKASI | [O19] |
| Staged = 0, tanpa commit (C9) | TERVERIFIKASI | [O20] |
| Kestabilan keputusan kriteria-i lintas 5 seed | TERVERIFIKASI (suplementer) | [O12b] |
| Robustness subset 223-counterfactual | BELUM DIVERIFIKASI | §7 butir 1 (tidak dihitung; spec menamai 234 sebagai penentu) |
| Vonis H1/H3/H4/H5 oleh coder | TIDAK DIKLAIM | §7 butir 4 (spec §4.1, §4.6) |

## 2. Pra-registrasi pelaksana, ASUMSI, dan koreksi harness

### 2.1 Pra-registrasi (ditetapkan SEBELUM run pertama, tidak diubah sesudah lihat hasil)

**Uji 1** — populasi terkunci 234 hari-flag (jangkar B1; rekonsiliasi `597 = 578 + 19`);
varian INK = 974 hari, EKS = 974 − 234 = 740 hari; klasifikasi memakai
`classify_day_label` D1 apa adanya (ambang 0,0268 / 88,79) — kode produksi tidak diubah.
- M1 = verdict gugur-H1 lock (`protokol:94-96`): (i) selisih drift median CI95 memuat 0,
  ATAU (ii) share trending tak stabil antar-tahun (χ², p<0,01). MATERIAL bila verdict EKS ≠ verdict INK.
- M2 = homogenitas distribusi label INK vs EKS (χ² 2×3, α=0,01). MATERIAL bila p<0,01.
  Δshare_trending + CI95 bootstrap dilaporkan sebagai efek (bukan penentu).
- M3 = konsistensi (BUKAN penentu): median `ratio_path` hari-gap vs non-gap vs B1
  (0,0251 vs 0,0280); tanda berbalik → ANOMALI.
**Uji 2** — 4 alternatif TERTUTUP (tidak ada tambahan pasca-lihat-hasil):
A1 = span 2024 W=20; A2 = span 2025 W=20; A3 = span 2023 W=10; A4 = span 2023 W=30.
K1 = AUC_alt ≥ 0,70 semua; K2 = agreement ≥ 90% semua; K3 = median rv_score B > A semua.
MARJINAL = tepat satu gagal tipis (AUC ∈ [0,65;0,70) ATAU agreement ∈ [80%;90%)).

### 2.2 ASUMSI pelaksana pada titik yang spec/lock tidak menetapkan bentuk operasionalnya

| # | ASUMSI | Alasan | Uji kepekaan yang dijalankan |
|---|---|---|---|
| A-1 | Drift M1 = kolom `london_drift_norm`; pasangan = trending vs range | lock H1: "drift berarah RELATIF M15 4 jam pertama London (dinormalisasi ATR harian t-1) pada hari trending vs range" | R1 (kolom `london_drift_4h`) & R2 (pembanding normal+range) → verdict tidak berubah [O8] |
| A-2 | CI95 = percentile bootstrap hari-level, B=10.000, seed 20261006 | spec tidak memfix metode/seed; 20261006 = konvensi seed bootstrap proyek (lock H5) | 5 seed berbeda → keputusan kriteria-i tidak berubah [O12b] |
| A-3 | Kriteria (ii): tahun utuh 2023–2025 (2026 parsial dikecualikan); tabel 2×k (tahun × trending/bukan), tanpa koreksi Yates | analog konvensi H2 lock "3 tahun utuh 2023–2025 OOS (2026 parsial dikecualikan)"; lock menulis "antar tahun" tanpa daftar | R3 (memuat 2026 parsial) → verdict tidak berubah; tabel 3 kolom juga dilaporkan [O8] |
| A-4 | Uji 2 skor untuk W≠20: `rv_score_W = rv_roll_Wd / W` (semantik mean, protokol §2) | protokol §2 mendefinisikan `rv_score = rv_roll_20d/20` sebagai "mean, turunan label" | AUC & K3 invarian skala (rank/urutan); TAU & agreement memang skala-relatif — dicatat, bukan disembunyikan |
| A-5 | Uji 2 agreement dibaca dua cara: (a) primer = flag_alt dibatasi span alternatif (pembacaan harfiah "hari overlapping"); (b) robust = flag_alt diterapkan ke seluruh indeks | spec tidak eksplisit domain penerapan flag_alt | kedua pembacaan dilaporkan penuh dan memberi verdict SAMA (TIDAK STABIL) [O14][O15] |
| A-6 | Kegagalan K3-tunggal (tanpa pita tipis di spec) diperlakukan TIDAK STABIL | spec hanya mendefinisikan pita tipis untuk AUC/agreement | tidak terpicu (K1 & K2 juga gagal) |

### 2.3 Koreksi harness (dicatat untuk auditor; TIDAK mengubah metrik/pra-registrasi/ambang)

1. **FIX-1 (uji-1):** perbandingan provenans S0 mula-mula membandingkan kolom teks
   `day_label` sebagai float → run pertama gagal `ValueError: could not convert string
   to float: 'normal'`. Diperbaiki dengan cabang dtype object (bandingkan sebagai string).
   Tidak ada angka metrik yang berubah; run sukses 2× [O6], [O12].
2. **FIX-2 (uji-2):** cek baseline `score20 == rv_roll_20d/20` memakai `np.max` sehingga
   NaN warmup merambat (hasil `NaN`, bukan 0). Diganti `np.nanmax` + hitungan titik beda,
   dan ditambahkan cek silang AUC trapesium (metode pembanding) di blok baseline.
   Alternatif, ambang K1–K3, dan keputusan tidak diubah [O13].

## 3. Uji 1 — materialitas `gap_f2_flag` pada klasifikasi H1

**Urutan eksekusi dipatuhi: baseline INK dulu (ditempel), baru M1 → M2 → M3 → keputusan.**
Skrip: `%TEMP%\opencode\l3h3\uji1_materialitas_gap.py` (read-only; hasil angka: `uji1_hasil.json`).

### 3.1 Provenans — D1 dibaca ulang vs artefak D4 beku [O6]

D1 (`build_labels`) dipanggil ulang apa adanya (`_build_daily_labels`) atas M15/M1 sumber
+ referensi ATR store; seluruh 6 kolom D4 dibandingkan:

```
$ venv/Scripts/python.exe %TEMP%\opencode\l3h3\uji1_materialitas_gap.py /d/ANN
```
```
=== S0. PROVENANS: D1 dibaca ulang vs artefak D4 beku ===
{
  "baris_daily_runtime": 974,
  "baris_labels_build": 974,
  "baris_d4_disk": 974,
  "index_identik": true,
  "kolom_sama": true,
  "mismatch_per_kolom_build_vs_d4": {
    "day_label": 0,
    "london_drift_4h": 0,
    "london_drift_norm": 0,
    "gap_f2_flag": 0,
    "rv_regime_flag": 0,
    "quarantine_mask": 0
  },
  "gap_hari": 234,
  "nongap_hari": 740,
  "distribution_day_label_ink": {
    "trending": 330,
    "normal": 320,
    "range": 324
  },
  "quarantine_true": 19,
  "rv_nan": 19
}
```


Catatan: `mismatch_per_kolom_build_vs_d4` = 0 untuk keenam kolom → label, drift, flag gap,
flag rv, dan mask karantina direproduksi tanpa satu pun sel berbeda; `gap_hari` = 234,
`nongap_hari` = 740, distribusi INK trending/normal/range = 330/320/324, karantina 19,
rv NaN 19. Jadi varian INK/EKS di bawah berjalan atas artefak D4 yang identik dengan
hasil pembacaan ulang D1 — bukan atas salinan yang diubah.

### 3.1b Baseline INK — dihitung & ditempel SEBELUM perbandingan (§21 butir 7) [O7]

```
=== S1. BASELINE (dihitung DULU, baru dibandingkan): INK 974 hari ===
{
  "n_hari": 974,
  "distribution_day_label": {
    "trending": 330,
    "normal": 320,
    "range": 324
  },
  "verdict_h1": {
    "drift_col": "london_drift_norm",
    "pembanding": "trending vs range",
    "tahun_kriteria_ii": [
      2023,
      2024,
      2025
    ],
    "n_trending": 330,
    "n_pembanding": 324,
    "median_trending": 0.02948996641114935,
    "median_pembanding": 0.015065793016650224,
    "selisih_median": 0.014424173394499126,
    "ci95_lo": -0.02729045556350576,
    "ci95_hi": 0.052787080233690914,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 0.7666041417663041,
    "p_2xk": 0.6816069745648556,
    "kriteria_ii_p_lt_alpha": false,
    "share_per_tahun": {
      "2023": {
        "n": 259,
        "trending": 94,
        "share_trending": 0.36293436293436293
      },
      "2024": {
        "n": 260,
        "trending": 85,
        "share_trending": 0.3269230769230769
      },
      "2025": {
        "n": 259,
        "trending": 88,
        "share_trending": 0.33976833976833976
      }
    },
    "chi2_3_kolom": 1.712804294616369,
    "p_3_kolom": 0.7883904142851688,
    "verdict": "GUGUR"
  }
}
```


### 3.2 M1 (primer, penentu) — verdict gugur-H1 INK vs EKS [O8]

```
=== S2. M1 (primer, penentu): verdict gugur-H1 INK vs EKS ===
{
  "varian_ink": {
    "drift_col": "london_drift_norm",
    "pembanding": "trending vs range",
    "tahun_kriteria_ii": [
      2023,
      2024,
      2025
    ],
    "n_trending": 330,
    "n_pembanding": 324,
    "median_trending": 0.02948996641114935,
    "median_pembanding": 0.015065793016650224,
    "selisih_median": 0.014424173394499126,
    "ci95_lo": -0.02729045556350576,
    "ci95_hi": 0.052787080233690914,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 0.7666041417663041,
    "p_2xk": 0.6816069745648556,
    "kriteria_ii_p_lt_alpha": false,
    "share_per_tahun": {
      "2023": {
        "n": 259,
        "trending": 94,
        "share_trending": 0.36293436293436293
      },
      "2024": {
        "n": 260,
        "trending": 85,
        "share_trending": 0.3269230769230769
      },
      "2025": {
        "n": 259,
        "trending": 88,
        "share_trending": 0.33976833976833976
      }
    },
    "chi2_3_kolom": 1.712804294616369,
    "p_3_kolom": 0.7883904142851688,
    "verdict": "GUGUR"
  },
  "varian_eks": {
    "drift_col": "london_drift_norm",
    "pembanding": "trending vs range",
    "tahun_kriteria_ii": [
      2023,
      2024,
      2025
    ],
    "n_trending": 265,
    "n_pembanding": 232,
    "median_trending": 0.028947089386057737,
    "median_pembanding": 0.015407976369708167,
    "selisih_median": 0.01353911301634957,
    "ci95_lo": -0.0342357583305254,
    "ci95_hi": 0.04550979106155891,
    "kriteria_i_ci_memuat_0": true,
    "chi2_2xk": 0.17826537825676758,
    "p_2xk": 0.9147241915659032,
    "kriteria_ii_p_lt_alpha": false,
    "share_per_tahun": {
      "2023": {
        "n": 156,
        "trending": 58,
        "share_trending": 0.3717948717948718
      },
      "2024": {
        "n": 208,
        "trending": 76,
        "share_trending": 0.36538461538461536
      },
      "2025": {
        "n": 205,
        "trending": 72,
        "share_trending": 0.35121951219512193
      }
    },
    "chi2_3_kolom": 0.6059686958438115,
    "p_3_kolom": 0.962398125372731,
    "verdict": "GUGUR"
  },
  "n_ink": 974,
  "n_eks": 740,
  "verdict_berbeda": false,
  "material_m1": false,
  "robustness": {
    "R1_drift_4h_tanpa_norm": {
      "verdict_ink": "GUGUR",
      "verdict_eks": "GUGUR",
      "verdict_berbeda": false,
      "detail_ink_ringkas": {
        "kriteria_i_ci_memuat_0": true,
        "p_2xk": 0.6816069745648556,
        "median_trending": 0.041499999999999204,
        "median_pembanding": 0.01849999999998886
      },
      "detail_eks_ringkas": {
        "kriteria_i_ci_memuat_0": true,
        "p_2xk": 0.9147241915659032,
        "median_trending": 0.036000000000001364,
        "median_pembanding": 0.01849999999998886
      }
    },
    "R2_pembanding_normal_range": {
      "verdict_ink": "GUGUR",
      "verdict_eks": "GUGUR",
      "verdict_berbeda": false,
      "detail_ink_ringkas": {
        "kriteria_i_ci_memuat_0": true,
        "p_2xk": 0.6816069745648556,
        "median_trending": 0.02948996641114935,
        "median_pembanding": 0.027507253935215772
      },
      "detail_eks_ringkas": {
        "kriteria_i_ci_memuat_0": true,
        "p_2xk": 0.9147241915659032,
        "median_trending": 0.028947089386057737,
        "median_pembanding": 0.02597990404634548
      }
    },
    "R3_kriteria_ii_muat_2026": {
      "verdict_ink": "GUGUR",
      "verdict_eks": "GUGUR",
      "verdict_berbeda": false,
      "detail_ink_ringkas": {
        "kriteria_i_ci_memuat_0": true,
        "p_2xk": 0.776530117500301,
        "median_trending": 0.02948996641114935,
        "median_pembanding": 0.015065793016650224
      },
      "detail_eks_ringkas": {
        "kriteria_i_ci_memuat_0": true,
        "p_2xk": 0.9514310311116166,
        "median_trending": 0.028947089386057737,
        "median_pembanding": 0.015407976369708167
      }
    }
  }
}
```


**Bacaan [O8]:** INK verdict = **GUGUR** (kriteria-i: CI95 [−0,027290; +0,052787] memuat 0;
kriteria-ii: χ²=0,7666, p=0,6816 → tidak tak-stabil). EKS verdict = **GUGUR**
(kriteria-i: CI95 [−0,034236; +0,045510] memuat 0; kriteria-ii: χ²=0,1783, p=0,9147).
**Verdict identik → M1 tidak material.** Robustness R1 (drift 4h mentah), R2 (pembanding
normal+range), R3 (kriteria-ii memuat 2026) juga GUGUR/GUGUR → tidak ada satu pun pembacaan
yang membuat verdict berpindah. n_trending/n_pembanding: INK 330/324 → EKS 265/232.

**Batas klaim:** angka ini adalah *formula verdict lock* yang dipakai sebagai penilai
materialitas — **bukan vonis H1** (spec §"Boleh vs dilarang pakai hasil": memakai uji ini
sebagai vonis H1 DILARANG). Drift di sini dihitung pada label terkunci, bukan pada
identifikasi real-time H+1 pagi milik uji H1 Lapisan 3.

### 3.3 M2 (sekunder, penentu) — homogenitas distribusi label INK vs EKS [O9]

```
=== S3. M2 (sekunder, penentu): homogenitas label INK vs EKS ===
{
  "tabel_2x3": {
    "INK": [
      330,
      320,
      324
    ],
    "EKS": [
      265,
      243,
      232
    ],
    "kolom": [
      "trending",
      "normal",
      "range"
    ]
  },
  "chi2": 0.9258779541662121,
  "dof": 2,
  "p": 0.629431041054359,
  "alpha": 0.01,
  "material_m2": false,
  "share_trending_ink": 0.33880903490759756,
  "share_trending_eks": 0.3581081081081081,
  "delta_share_trending": 0.019299073200510553,
  "delta_ci95_lo": 0.0030084639086084292,
  "delta_ci95_hi": 0.03523449994702561,
  "delta_memuat_0": false
}
```


**Bacaan [O9]:** tabel 2×3 INK [330, 320, 324] vs EKS [265, 243, 232]; χ² = 0,9258779541662121,
dof = 2, p = 0,629431041054359 ≥ α = 0,01 → **M2 tidak material.** Efek yang dilaporkan
(bukan penentu): share_trending INK 0,338809 → EKS 0,358108; Δ = +0,019299 dengan
CI95 [+0,003008; +0,035234] (tidak memuat 0 — dilaporkan apa adanya sebagai efek, sesuai
spec, tetapi TIDAK dipakai untuk memutus materialitas).

### 3.4 M3 (konsistensi, BUKAN penentu) — median `ratio_path` [O10]

```
=== S4. M3 (konsistensi, BUKAN penentu): median ratio_path ===
{
  "n_gap": 234,
  "n_nongap": 740,
  "median_ratio_path_gap": 0.025133520587895034,
  "median_ratio_path_nongap": 0.027809705068563857,
  "selisih_gap_minus_nongap": -0.0026761844806688223,
  "b1_median_gap": 0.0251,
  "b1_median_nongap": 0.028,
  "b1_selisih": -0.0029,
  "tanda_sama_dengan_b1": true,
  "anomali": false,
  "ratio_path_nan": 0
}
```


**Bacaan [O10]:** median `ratio_path` hari-gap = 0,025133520587895034 (n=234) vs non-gap
= 0,027809705068563857 (n=740); selisih = −0,0026761844806688223 — **tanda SAMA dengan
baseline B1** (−0,0029; gap lebih tenang), jadi **tidak ANOMALI**. `ratio_path` NaN = 0.
M3 hanya konsistensi: ia tidak pernah menjadi penentu materialitas.

### 3.5 Keputusan Uji 1 [O11]

```
=== S5. HASIL UJI 1 ===
{
  "material_m1": false,
  "material_m2": false,
  "m3_anomali": false,
  "hasil": "IMMATERIAL",
  "robustness_semua_verdict_sama": true
}

[hasil angka ditulis] C:\Users\Fajar\AppData\Local\Temp\opencode\l3h3\uji1_hasil.json
```


**Keputusan: IMMATERIAL** — M1 negatif (verdict identik), M2 negatif (p=0,6294 ≫ 0,01),
M3 konsisten dengan B1 (tidak ANOMALI). `robustness_semua_verdict_sama` = true.

### 3.6 Robustness R1–R3 (dilaporkan di dalam [O8], BUKAN penentu)

| Varian | INK | EKS | Verdict berbeda? |
|---|---|---|---|
| R1 drift `london_drift_4h` tanpa normalisasi | GUGUR (kriteria-i) | GUGUR (kriteria-i) | tidak |
| R2 pembanding normal∪range | GUGUR (kriteria-i) | GUGUR (kriteria-i) | tidak |
| R3 kriteria-ii memuat 2026 parsial | GUGUR (kriteria-i) | GUGUR (kriteria-i) | tidak |

Ketiganya mengubah bentuk operasional (kolom drift, kelompok pembanding, daftar tahun)
dan tidak satu pun memindahkan verdict INK/EKS. Pilihan A-1/A-3 (§2.2) karena itu tidak
menopang kesimpulan.

### 3.7 Determinisme uji-1 (C5) [O12]

```
$ cp uji1_hasil.json run1.json && venv/Scripts/python.exe uji1_materialitas_gap.py /d/ANN && sha256sum run1.json uji1_hasil.json && cmp run1.json uji1_hasil.json && echo IDENTIK
23c29b0f2927d28d940a3ec21339ac80a0ecca160198f34f6bbe13dd42cc26ef *run1.json
23c29b0f2927d28d940a3ec21339ac80a0ecca160198f34f6bbe13dd42cc26ef *uji1_hasil.json
IDENTIK
```


Dua eksekusi skrip yang sama menghasilkan `uji1_hasil.json` dengan sha256 identik
(`23c29b0f2927d28d940a3ec21339ac80a0ecca160198f34f6bbe13dd42cc26ef`); `cmp` = identik.
Keputusan kriteria-i juga stabil lintas 5 seed berbeda [O12b]:

```
$ venv/Scripts/python.exe _seed_probe.py
INK seed= 20261006 ci95=[-0.027290,+0.052787] memuat_0=True
INK seed=        1 ci95=[-0.028294,+0.052689] memuat_0=True
INK seed=        2 ci95=[-0.028939,+0.052075] memuat_0=True
INK seed=       42 ci95=[-0.027502,+0.051912] memuat_0=True
INK seed=      777 ci95=[-0.027145,+0.052425] memuat_0=True
EKS seed= 20261006 ci95=[-0.034236,+0.045510] memuat_0=True
EKS seed=        1 ci95=[-0.034600,+0.045529] memuat_0=True
EKS seed=        2 ci95=[-0.035137,+0.046298] memuat_0=True
EKS seed=       42 ci95=[-0.033968,+0.045737] memuat_0=True
EKS seed=      777 ci95=[-0.034664,+0.045208] memuat_0=True
```


## 4. Uji 2 — sensitivitas TAU terhadap span/window alternatif

Skrip: `%TEMP%\opencode\l3h3\uji2_sensitivitas_tau.py` (read-only; hasil angka: `uji2_hasil.json`).
Aturan terkunci yang dipakai apa adanya: `rv_score = rv_roll_20d / 20`, span
2023-01-01..2023-12-31, B = Jan–Jun (positif) / A = Jul–Des, Youden J = sens + spec − 1,
perbandingan strict `>`. Alternatif TERTUTUP: A1 span 2024 W=20; A2 span 2025 W=20;
A3 span 2023 W=10; A4 span 2023 W=30 (tidak ada alternatif tambahan pasca-lihat-hasil;
`TAU_alt` tidak pernah dipakai sebagai pengganti TAU terkunci).

### 4.1 Baseline terkunci dihitung ULANG sebelum alternatif [O13]

```
=== S0. BASELINE TERKUNCI (hitung ulang sebelum alternatif) ===
{
  "score20_sama_dengan_rv_roll_20d_per_20": true,
  "selisih_maks_nanmax": 0.0,
  "jumlah_titik_beda_score20_vs_raw": 0,
  "auc_trapz_runtime_2023_W20": 0.8173755150499336,
  "auc_trapz_sama_konstanta": true,
  "auc_rank_minus_konstanta": 1.1102230246251565e-16,
  "kalibrasi_runtime_2023_W20": {
    "tau": 2.5951672079821496e-05,
    "J": 0.6046511627906976,
    "auc": 0.8173755150499337,
    "n_b": 111,
    "n_a": 129,
    "nan_span": 19,
    "median_b": 4.145214537383251e-05,
    "median_a": 2.2750316674777358e-05,
    "auc_trapz": 0.8173755150499336
  },
  "kalibrasi_store_shift_minus1_2023_W20": {
    "tau": 2.5951672079821496e-05,
    "J": 0.6046511627906976,
    "auc": 0.8173755150499337,
    "n_b": 111,
    "n_a": 129,
    "nan_span": 19,
    "median_b": 4.145214537383251e-05,
    "median_a": 2.2750316674777358e-05
  },
  "tau_konstanta": 2.5951672079821496e-05,
  "auc_konstanta": 0.8173755150499336,
  "n_b_konstanta": 111,
  "n_a_konstanta": 129,
  "tau_runtime_sama_konstanta": true,
  "auc_runtime_sama_konstanta": false,
  "tau_store_sama_konstanta": true,
  "n_b_runtime_sama": true,
  "n_a_runtime_sama": true,
  "n_span_2023": 259,
  "flag_ref_beda_vs_D4": 0,
  "flag_ref_nan": 19,
  "flag_ref_1": 619
}
```


**Bacaan [O13]:** `score20` identik dengan `rv_roll_20d/20` (0 titik beda; selisih maks nanmax 0,0);
kalibrasi ulang dari data memberi **TAU bit-identik** dengan konstanta lock
(`2.5951672079821496e-05`) baik dari frame runtime maupun dari store (`shift(-1)`), dengan
n_B=111 / n_A=129 / warmup NaN=19 persis seperti protokol §2. Flag referensi sama persis
dengan kolom `rv_regime_flag` D4 (0 beda; 19 NaN; 619 hari flag-1 dari 955 evaluable).
AUC: metode rank (dipakai untuk semua alternatif) = `0.8173755150499337`, yaitu **1 ULP
(1,11e-16) di atas** konstanta lock `0.8173755150499336`; metode trapesium ROC atas data
yang sama = `0.8173755150499336` **bit-identik** dengan konstanta → selisih 1 ULP adalah
artefak metode penjumlahan floating point, bukan perbedaan data. Selisih itu ~1e-16
terhadap ambang K1 0,70 → tidak material (dicatat sebagai INFO di §5 DEV-3).

### 4.2 Hasil per alternatif [O14]

```
=== S1. ALTERNATIF PRA-REGISTRASI (A1..A4) ===
{
  "A1_span2024_W20": {
    "span": [
      "2024-01-01",
      "2024-12-31"
    ],
    "W": 20,
    "tau_alt": 0.00013548874602906333,
    "auc_alt": 0.15586721107757856,
    "J_alt": 0.0,
    "n_b": 129,
    "n_a": 131,
    "nan_span": 0,
    "median_b": 2.094437714340629e-05,
    "median_a": 4.903155897552072e-05,
    "k3_median_b_gt_a": false,
    "rasio_tau_alt_per_locked": 5.2208098812411965,
    "agreement_primer_span": {
      "n": 260,
      "agreement": 0.3153846153846154,
      "kappa": 0.0,
      "flip": 178
    },
    "agreement_robust_semua_hari": {
      "n": 955,
      "agreement": 0.3518324607329843,
      "kappa": 0.0,
      "flip": 619
    },
    "gagal_eksekusi_lt_200": false
  },
  "A2_span2025_W20": {
    "span": [
      "2025-01-01",
      "2025-12-31"
    ],
    "W": 20,
    "tau_alt": 3.584422282311362e-05,
    "auc_alt": 0.957418893129771,
    "J_alt": 0.8361164122137406,
    "n_b": 128,
    "n_a": 131,
    "nan_span": 0,
    "median_b": 4.334909705257482e-05,
    "median_a": 2.6210696891220676e-05,
    "k3_median_b_gt_a": true,
    "rasio_tau_alt_per_locked": 1.3811912663224502,
    "agreement_primer_span": {
      "n": 259,
      "agreement": 0.6718146718146718,
      "kappa": 0.39159872875500906,
      "flip": 85
    },
    "agreement_robust_semua_hari": {
      "n": 955,
      "agreement": 0.7602094240837697,
      "kappa": 0.5451198585616973,
      "flip": 229
    },
    "gagal_eksekusi_lt_200": false
  },
  "A3_span2023_W10": {
    "span": [
      "2023-01-01",
      "2023-12-31"
    ],
    "W": 10,
    "tau_alt": 2.5041018330339243e-05,
    "auc_alt": 0.7886475751169197,
    "J_alt": 0.5963866999807803,
    "n_b": 121,
    "n_a": 129,
    "nan_span": 9,
    "median_b": 4.08234664505282e-05,
    "median_a": 2.2297351067067476e-05,
    "k3_median_b_gt_a": true,
    "rasio_tau_alt_per_locked": 0.9649096309986775,
    "agreement_primer_span": {
      "n": 240,
      "agreement": 0.9125,
      "kappa": 0.8012304779933743,
      "flip": 21
    },
    "agreement_robust_semua_hari": {
      "n": 955,
      "agreement": 0.8931937172774869,
      "kappa": 0.7695855804711892,
      "flip": 102
    },
    "gagal_eksekusi_lt_200": false
  },
  "A4_span2023_W30": {
    "span": [
      "2023-01-01",
      "2023-12-31"
    ],
    "W": 30,
    "tau_alt": 2.8106701591701573e-05,
    "auc_alt": 0.8393583544400952,
    "J_alt": 0.5736434108527133,
    "n_b": 101,
    "n_a": 129,
    "nan_span": 29,
    "median_b": 4.905570315544095e-05,
    "median_a": 2.666791487086194e-05,
    "k3_median_b_gt_a": true,
    "rasio_tau_alt_per_locked": 1.0830401025896017,
    "agreement_primer_span": {
      "n": 230,
      "agreement": 0.9304347826086956,
      "kappa": 0.8428425008541168,
      "flip": 16
    },
    "agreement_robust_semua_hari": {
      "n": 945,
      "agreement": 0.8920634920634921,
      "kappa": 0.7654093836246552,
      "flip": 102
    },
    "gagal_eksekusi_lt_200": false
  }
}
```


**Bacaan [O14] (ringkas; angka mentah di atas):**

| Alt | span | W | TAU_alt | AUC_alt | n_B | n_A | NaN | agreement (primer) | n | agreement (robust) | n | K3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref | 2023 | 20 | 2,5951672079821496e-05 | 0,8173755150499337 * | 111 | 129 | 19 | 1,000000 (trivial) | 240 | — | — | ya |
| A1 | 2024 | 20 | 1,3548874602906333e-04 | **0,15586721107757856** | 129 | 131 | 0 | **0,315385** (κ=0,000; flip 178) | 260 | **0,351832** (κ=0,000; flip 619) | 955 | **tidak** |
| A2 | 2025 | 20 | 3,584422282311362e-05 | 0,9574188931297710 | 128 | 131 | 0 | **0,671815** (κ=0,392; flip 85) | 259 | **0,760209** (κ=0,545; flip 229) | 955 | ya |
| A3 | 2023 | 10 | 2,5041018330339243e-05 | 0,7886475751169197 | 121 | 129 | 9 | 0,912500 (κ=0,801; flip 21) | 240 | 0,893194 (κ=0,770; flip 102) | 955 | ya |
| A4 | 2023 | 30 | 2,8106701591701573e-05 | 0,8393583544400952 | 101 | 129 | 29 | 0,930435 (κ=0,843; flip 16) | 230 | 0,892063 (κ=0,765; flip 102) | 945 | ya |

\* konstanta lock = 0,8173755150499336; metode trapesium = bit-identik (§4.1).
Tidak ada GAGAL-eksekusi: n hari evaluable minimum = 230 (primer) dan 945 (robust), dua-duanya ≥ 200.

**Catatan penting A1 (bukan penyesalan pasca-hoc, melainkan sebab kegagalan K1):**
pada span 2024 urutan strata lock **terbalik** — median `rv_score` B (Jan–Jun) = 2,094e-05
**<** A (Jul–Des) = 4,903e-05, sehingga AUC arah-lock = 0,1559 (≈ 1 − 0,844) dan Youden
degenerat: J maksimum = 0,0 dengan `TAU_alt` = nilai skor maksimum observasi
(1,3549e-04) → filter praktis berhenti menandai apa pun. Ini konsisten dengan kejadian
pasar nyata 2024 (ledakan volatilitas JPY pada semester kedua 2024) — dicatat sebagai
penjelasan, **bukan** sebagai justifikasi untuk mengganti alternatif atau menambah span.

### 4.3 Keputusan K1–K3 [O15]

```
=== S2. KEPUTUSAN K1-K3 (dua pembacaan agreement) ===
{
  "auc_alt_semua": [
    0.15586721107757856,
    0.957418893129771,
    0.7886475751169197,
    0.8393583544400952
  ],
  "auc_min": 0.15586721107757856,
  "K1_ambang": 0.7,
  "K1_status": "GAGAL",
  "K1_gagal_tipis": false,
  "agreement_primer_semua": [
    0.3153846153846154,
    0.6718146718146718,
    0.9125,
    0.9304347826086956
  ],
  "agreement_robust_semua": [
    0.3518324607329843,
    0.7602094240837697,
    0.8931937172774869,
    0.8920634920634921
  ],
  "K2_ambang": 0.9,
  "K2_status_primer": "GAGAL",
  "K2_status_robust": "GAGAL",
  "K2_gagal_tipis_primer": false,
  "K2_gagal_tipis_robust": false,
  "K3_status": "GAGAL",
  "verdict_primer": "TIDAK STABIL",
  "verdict_robust": "TIDAK STABIL",
  "fails_primer": [
    "K1",
    "K2",
    "K3"
  ],
  "fails_robust": [
    "K1",
    "K2",
    "K3"
  ],
  "kedua_pembacaan_sama": true,
  "ada_gagal_eksekusi": false
}

[hasil angka ditulis] C:\Users\Fajar\AppData\Local\Temp\opencode\l3h3\uji2_hasil.json
```


**Bacaan [O15]:** AUC_alt semua = [0,15586721107757856; 0,957418893129771; 0,7886475751169197;
0,8393583544400952] → K1 **GAGAL** (min 0,1559; bukan gagal tipis karena < 0,65).
Agreement primer semua = [0,315385; 0,671815; 0,912500; 0,930435] → K2 **GAGAL** (min 0,3154;
bukan gagal tipis karena < 80%). Agreement robust semua = [0,351832; 0,760209; 0,893194;
0,892063] → K2 tetap **GAGAL** (min 0,3518). K3 **GAGAL** (A1: median B < A).
Ketiga kriteria gagal → **TIDAK STABIL**; dan pembacaan primer vs robust memberi verdict
yang **sama** (`kedua_pembacaan_sama = true`), sehingga pilihan A-5 tidak menopang hasil.
`ada_gagal_eksekusi` = false (tidak ada alternatif dengan < 200 hari evaluable).

### 4.4 Konsekuensi yang spec tetapkan (S4/S4b)

Spec §Uji-2 "Dampak ke vonis H3 (S4)" menyatakan: **TIDAK STABIL → H3 GUGUR via kriteria
tambahan S4b**; filter tanpa identitas stabil "tidak dapat dipegang; dilarang mengaktifkan
filter pada data mana pun"; S4b tidak mengubah ambang lock, tidak memvonis H1/H2/H4/H5, dan
tidak memberi izin kalibrasi ulang (Q1(a) tetap). **S4b adalah keputusan arsitek di dalam
spec ini, bukan lock** — coder melaporkan konsekuensinya, bukan memvonis H3 sendiri
(spec §4.6 + §26 AGENTS.md). S4 (uji drawdown vs strategi diagnostik L3 pertama) tetap
wajib sebelum filter aktif; dengan TIDAK STABIL, spec menyatakan filter justru dilarang.

### 4.5 Determinisme uji-2 (C5) [O16]

```
$ cp uji2_hasil.json run1.json && venv/Scripts/python.exe uji2_sensitivitas_tau.py /d/ANN && sha256sum run1.json uji2_hasil.json && cmp run1.json uji2_hasil.json && echo IDENTIK
d7927fb92edb836a4173c1fc5077ba885e451632faa6313392f7c2600fea1c62 *run1.json
d7927fb92edb836a4173c1fc5077ba885e451632faa6313392f7c2600fea1c62 *uji2_hasil.json
IDENTIK
```


## 5. Kriteria selesai Lapisan 3-H3 (C1–C9)

| # | Syarat | Status | Bukti |
|---|---|---|---|
| C1 | HEAD tak berubah | **LULUS** | [O2] (`git rev-parse HEAD` = `e0b2b9f9…`), diulang di [O20] |
| C2 | Nol tulis produksi + nol sentuh lindung | **LULUS (substansi)** — pola literal "KOSONG" tidak dapat tercapai pada state repo pra-ada; lihat DEV-1 | [O3] (status + `find -newermt` kosong), [O4], [O5] (hash isi identik) |
| C3 | Hash D1/D2/D3/D5 + trio beku cocok | **LULUS** — 7/7 cocok prefix spec | [O5] |
| C4 | Gate hijau | **LULUS** | [O17] pytest `254 passed` rc=0; [O18] ruff 0.6.9 check rc=0 + format rc=0 (`37 files already formatted`); C4d [O19] |
| C5 | Determinisme uji-1 & uji-2 dijalankan 2× | **LULUS** — sha256 kedua berkas angka identik per uji | [O12] (uji-1), [O16] (uji-2) |
| C6 | Uji-1 selesai + hasil diputus | **LULUS** (eksekusi: M1 & M2 terhitung) **dan** hasil **IMMATERIAL** — dua hal ini dilaporkan terpisah, bukan digabung | [O7]–[O11] |
| C7 | Uji-2 selesai + hasil diputus | **LULUS** (tabel 5 baris ref+A1–A4: TAU/AUC/n/agreement + keputusan K1–K3) **dan** hasil **TIDAK STABIL** | [O13]–[O15] |
| C8 | Dokumen hasil final + hash sesudah penulisan terakhir | **LULUS** | §C8 + [O21] |
| C9 | Staged = 0, tanpa commit | **LULUS** | [O20] |

### 5.1 Catatan deviasi/interpretasi (untuk Auditor)

- **DEV-1 (C2, pola literal).** Perintah C2 diminta menghasilkan output KOSONG. Pada state repo
  pra-ada, output **tidak** kosong: (i) `src/features/build_labels.py` & `tests/test_build_labels.py`
  berstatus `??` (untracked — memang tidak pernah di-commit, sejalan larangan commit/stage);
  (ii) `reports/eda/progress/*.md` (14 berkas) sudah terhapus di worktree sebelum tugas ini
  (status ` D`, tercatat pula di re-audit keempat §12). Karena itu C2 dinilai pada **substansi**,
  dengan bukti yang lebih ketat: output perintah C2 sebelum vs sesudah tugas **identik**, `git diff
  HEAD` untuk berkas lindung = hanya penghapusan pra-ada itu, `find src tests data configs
  -newermt "2026-10-08 22:00"` **kosong** (nol berkas tersentuh selama tugas), dan hash isi D1/D2
  + trio beku tidak berubah [O5]. **Eskalasi ke Arsitek:** pola lolos "kedua output KOSONG" perlu
  diperbaiki (mis. dibatasi pada berkas tracked, atau dibandingkan before/after).
- **DEV-2 (Uji-1, subset 223).** Spec menamai 234 hari sebagai populasi terkunci/penentu dan
  223-subset hanya sebagai "cek robustness (bukan penentu)". Cek robustness 223 **tidak
  dihitung** di sini karena spec tidak menyediakan identitas 11 hari pembedanya dan saya
  DILARANG mengarang definisi (larangan "menambah alternatif pasca-lihat-hasil"). Status: BELUM
  DIVERIFIKASI (§7 butir 1). Yang ditegaskan: 234 dipakai sebagai penentu — bukan 223.
- **DEV-3 (Uji-2, AUC 1 ULP).** Baseline AUC dengan metode rank = `0.8173755150499337`, konstanta
  lock = `0.8173755150499336` (selisih 1 ULP = 1,11e-16). Metode trapesium ROC atas data yang sama
  mereproduksi konstanta **bit-identik** → perbedaan murni artefak penjumlahan float, bukan data.
  INFO, bukan temuan; tidak memengaruhi K1 (ambang 0,70).
- **DEV-4 (jalur mentah C3/C4).** Perintah C3 spec mencampur jalur repo-root (`src/…`, `tests/…`,
  `data/…`) dengan jalur relatif governance (`coder/…`); perintah C4 menulis
  `coder/hasil-lapisan3-H3.md`. Keduanya dijalankan dari root repo dengan jalur `coder/…`
  diekspansi menjadi `reports/governance/2026-10-07/coder/…` — berkas yang sama, tidak ada
  perbedaan objek yang diperiksa. (Pola dokumentasi, bukan temuan substansi.)

### 5.2 Output mentah C1–C9

Seluruh blok mentah di bawah disalin apa adanya dari keluaran terminal; hanya akhir baris
`
` (artefak terminal Windows) dinormalkan menjadi `
` saat penyisipan, tanpa mengubah
satu pun karakter isi. Berkas ini seluruhnya berakhir-baris `
`.

**Cek hash spec sebelum eksekusi [O1]**

```
$ git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H3.md
dacd07087f4e1f66154dcc75a259ecfcdb769043
```


**C1 — HEAD tak berubah [O2]**

```
$ git rev-parse HEAD
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
```


**C2 — nol tulis produksi + nol sentuh lindung [O3][O4][O5]**

```
$ git status --porcelain -- src/ tests/ data/ configs/
?? src/features/build_labels.py
?? tests/test_build_labels.py
$ find src tests data configs -type f -newermt "2026-10-08 22:00"
[kosong = nol berkas tersentuh sesudah 22:00]
```


```
$ git diff HEAD --name-only -- src/features/build_features.py tests/test_build_features.py data/features/M15/ reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md reports/governance/2026-10-07/arsitek/putusan-arsitek-B1.md reports/eda/
reports/eda/progress/audit_kesesuaian_nb00_nb04.md
reports/eda/progress/laporan_fix_audit_fragmen.md
reports/eda/progress/laporan_revisi_fragmen_4b.md
reports/eda/progress/laporan_tahap_0_reuse_check.md
reports/eda/progress/laporan_tahap_10_autocorr_fix.md
reports/eda/progress/laporan_tahap_1_pin_deps.md
reports/eda/progress/laporan_tahap_2_nb00_setup.md
reports/eda/progress/laporan_tahap_3_returns.md
reports/eda/progress/laporan_tahap_4_volatility.md
reports/eda/progress/laporan_tahap_5_autokorelasi.md
reports/eda/progress/laporan_tahap_6_swing_level.md
reports/eda/progress/laporan_tahap_7_swing_level_fix.md
reports/eda/progress/laporan_tahap_8_volatility_fix.md
reports/eda/progress/laporan_tahap_9_figures_fix.md
```


```
$ git hash-object src/features/build_labels.py tests/test_build_labels.py reports/governance/2026-10-07/coder/protokol-H1-H2-H3.md reports/governance/2026-10-07/coder/laporan-final-fase1.md src/features/build_features.py tests/test_build_features.py data/features/M15/usdjpy_m15_features.parquet
2561efd552544feeb9af0b6733711015b83f43dd
dc07a7e651d38f07a5cabbe4e693b10681312d25
bc17e5de6cfefb355fe7418acd2a3a0d8b461212
345308540d27c38534b77cdcd278e32eb15735ec
399e64b372e430b6def79b4fa8324a4e8e629918
ed7ac43520c4431519d4d7065504866ae9b3ad95
07402f40478aaed9391203f5db3237d636f5a959
$ sha256sum data/labels/*.parquet ; stat mtime
47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c *data/labels/usdjpy_day_labels.parquet
32eaf6b206c5107bfca95dee4bbeda6128f17065129b17a816820146bebda93f *data/labels/usdjpy_h2_trades.parquet
2026-10-08 15:04:01.255371600 +0700 data/labels/usdjpy_day_labels.parquet
2026-10-08 15:04:01.255371600 +0700 data/labels/usdjpy_h2_trades.parquet
2026-10-08 18:26:01.025453000 +0700 src/features/build_labels.py
2026-10-08 18:30:12.706189600 +0700 tests/test_build_labels.py
```


**C4 — gate hijau: pytest [O17], ruff [O18], karakter asing [O19]**

```
$ venv/Scripts/python.exe -m pytest -q | tail -3
$ echo rc=${PIPESTATUS[0]}
..                                                                       [100%]

============================ 254 passed in 18.96s =============================
rc=0
$ venv/Scripts/python.exe -m pytest --collect-only -q | tail -2

======================== 254 tests collected in 0.48s =========================
```


```
$ venv/Scripts/python.exe -m ruff --version ; .venv/Scripts/python.exe -m ruff --version
ruff 0.6.9
ruff 0.16.10
$ venv/Scripts/python.exe -m ruff check .
All checks passed!
rc=0
$ venv/Scripts/python.exe -m ruff format --check .
37 files already formatted
rc=0
$ .venv/Scripts/python.exe -m ruff format --check reports/governance/2026-10-07/coder/hasil-lapisan3-H3.md
io: D:\ANN\reports\governance\2026-10-07\coder\hasil-lapisan3-H3.md: The system cannot find the file specified. (os error 2)
--> reports\governance\2026-10-07\coder\hasil-lapisan3-H3.md:1:1

rc=2
```


**C4d — cek karakter asing pada berkas hasil ini [O19]** (dijalankan setelah seluruh isi di atas ditulis;
blok ini ber-ASCII sehingga tidak mengubah hasil cek — dijalankan ulang setelah penulisan terakhir, output identik)

```
$ venv/Scripts/python.exe scripts/check_foreign_chars.py reports/governance/2026-10-07/coder/hasil-lapisan3-H3.md
OK: 1 file discan, tidak ada karakter asing.
rc=0
```

**C4e — ruff 0.16.10 format --check pada berkas hasil ini (DISIPLIN 11: rc + cakupan)**

```
$ .venv/Scripts/python.exe -m ruff format --check reports/governance/2026-10-07/coder/hasil-lapisan3-H3.md
1 file already formatted
rc=0
[cakupan: 1 berkas .md; ruff 0.6.9 per-berkas .md = parse error, jadi per-berkas hanya bermakna di 0.16.10]
```

**C9 — staged = 0, tanpa commit [O20]**

```
$ git diff --cached --name-only
[kosong = nol staged]
$ git log --oneline -1
e0b2b9f feat(features): fondasi B1 TERTUTUP + governance audit (konfirmasi 3xYA)
$ git status --porcelain | grep -c "^[MADRC]"
0
```


## 6. Self-audit 3× adversarial (dijalankan pelaksana; verifikasi tetap milik Auditor)

### Putaran 1 — Correctness

1. **Urutan eksekusi M1→M2→M3 berurutan**, dan **baseline INK dihitung + ditempel dulu
   baru dibandingkan** (§21 butir 7): blok baseline [O7] mendahului blok M1 [O8] di skrip
   (fungsi `h1_verdict(ink)` dipanggil sebelum `h1_verdict(eks)`) dan di dokumen ini.
2. **Setiap angka tertaut** ke blok output bernomor [O1]…[O21]; angka di tabel §4.2/§4.4
   disalin dari [O13]/[O14]/[O15], bukan dari ingatan.
3. **Skrip hanya di `%TEMP%\opencode\l3h3`**: `uji1_materialitas_gap.py`,
   `uji2_sensitivitas_tau.py`, `_auc_probe.py`, `_auc_probe2.py`, `_seed_probe.py`,
   plus berkas angka `uji1_hasil.json`/`uji2_hasil.json`. Tidak ada berkas `.py` baru di repo
   (`git status` [O3] hanya memuat entri pra-ada).
4. **D4 tidak ditimpa**: sha256 + mtime `2026-10-08 15:04` (sebelum tugas) di [O5];
   `main()` tidak pernah dipanggil (hanya fungsi baca/`_build_daily_labels`), tidak ada
   `write_labels` di jalur eksekusi; `find -newermt` kosong [O3].
5. Dua cacat harness ditemukan dan diperbaiki, dicatat terbuka di §2.3 (FIX-1, FIX-2);
   run pertama uji-1 yang gagal `ValueError` dilaporkan, bukan disembunyikan.

### Putaran 2 — Bias & Asumsi (tiga godaan yang dilarang spec)

1. **Menambah alternatif TAU pasca-lihat-hasil — TIDAK dilakukan.** Daftar alternatif
   (A1–A4) tertulis di header skrip dan di pra-registrasi §2.1 sebelum eksekusi pertama;
   tidak ada span/rule/window kelima; `TAU_alt` tidak pernah dipakai sebagai ambang pakai
   ([O13] `tau_konstanta` tetap dipakai untuk flag referensi; [O15] keputusan memakai
   TAU_alt hanya sebagai bahan kriteria, sesuai spec).
2. **Memakai subset 223 sebagai penentu — TIDAK dilakukan.** Penentu = 234 penuh
   (INK 974 vs EKS 740) [O6]/[O8]; 223 tidak dihitung dan tidak diklaim; statusnya BELUM
   DIVERIFIKASI (DEV-2, §7 butir 1). Angka 479 artefak grain-campur juga tidak dipakai.
3. **Membaca MATERIAL sebagai izin eksklusi — tidak terjadi** (hasilnya IMMATERIAL); dan
   seandainya MATERIAL pun, spec hanya mengizinkan mekanisme dua-varian. Bukti bahwa tidak
   ada eksklusi/pembuangan yang dilakukan: D4 tetap 974 baris dengan keenam kolom utuh
   ([O6] `gap_hari` = 234 dan `nongap_hari` = 740 masih utuh; tidak ada berkas label baru/
   terhapus di [O3]).
4. **Arah bias diuji ke arah yang bisa menyalahkan pelaksana**: R1–R3 (§3.6), 5 seed
   ([O12b]), dan dua pembacaan agreement (A-5) semuanya dilaporkan — termasuk yang bisa
   mengubah kesimpulan. Hasil TIDAK STABIL justru **menggugurkan** filter (bukan hasil yang
   menguntungkan coder); hasil IMMATERIAL juga tidak dipakai untuk mengklaim apa pun di luar
   izin spec §"Boleh vs dilarang pakai hasil".

### Putaran 3 — Meta-check: C1–C9 sebelum klaim + lulus-eksekusi ≠ hasil

1. C1 ✓ [O2] diulang [O20]; C2 ✓ substansi [O3][O4][O5] (+DEV-1); C3 ✓ 7/7 prefix cocok [O5];
   C4 ✓ [O17][O18][O19]; C5 ✓ [O12] & [O16]; C6 ✓; C7 ✓; C8 ✓ §C8; C9 ✓ [O20] (`staged` kosong,
   HEAD tetap `e0b2b9f9…`).
2. **"Lulus-eksekusi" dipisahkan dari "hasil" (C6/C7):** Uji-1 = LULUS-eksekusi (M1 & M2
   terhitung, tidak ada alternatif gagal) **dan** hasil IMMATERIAL ([O11]); Uji-2 =
   LULUS-eksekusi (4/4 alternatif punya ≥ 200 hari evaluable, `ada_gagal_eksekusi=false`)
   **dan** hasil TIDAK STABIL ([O15]). Dokumen ini tidak menyatakan "berhasil" untuk
   menggantikan "hasil".
3. **Coder tidak mengaudit sendiri**: §1–§7 adalah laporan bukti + pembacaan angka; vonis
   H3/H1/H4/H5 dan penilaian adversarial atas dokumen ini adalah wewenang Auditor/Arsitek
   (§26 AGENTS.md, §27 arbitrase).

## 7. Yang belum diverifikasi / batasan

1. **Cek robustness subset 223-counterfactual TIDAK dihitung** (DEV-2). Spec menyebutnya
   non-penentu dan tidak menyediakan identitas 11 hari pembeda; saya tidak mengarang definisi.
   Bila Arsitek ingin cek ini, daftar 11 hari itu diperlukan sebagai input.
2. **Tidak ada vonis H1/H2/H3/H4/H5 oleh coder.** Konsekuensi "H3 GUGUR via S4b" pada §4.4
   adalah kutipan aturan spec; validasi/pemutusan akhir tetap milik Arsitek.
3. **Cakupan data** = store/label 2023-01-02..2026-10-02; tidak ada verifikasi untuk data
   setelah 2026-10-02.
4. **Pembacaan agreement** (A-5) memberi verdict sama, tetapi pemilihan pembacaan "resmi"
   tetap keputusan Arsitek.
5. **Celah spec A-6** (K3 gagal tunggal tanpa pita tipis) tidak terpicu, jadi tidak
   memengaruhi hasil — tetapi tetap dilaporkan sebagai celah.
6. **Angka "GUGUR" pada M1 bukan hasil uji H1 Lapisan 3** (uji itu memakai identifikasi
   real-time H+1 pagi); ia hanya formula verdict lock yang dipakai sebagai penilai materialitas.
7. Harness tidak di-commit (memang dilarang spec); reproduksi = jalankan ulang skrip di
   `%TEMP%\opencode\l3h3` atas HEAD yang sama.

## 8. C8 — Blob dokumen ini

Blok ini ditulis **setelah** seluruh isi di atas final. Baris **terakhir** berkas ini berisi
blob dokumen **tanpa** baris tersebut — direproduksi dengan:

```
head -n -1 reports/governance/2026-10-07/coder/hasil-lapisan3-H3.md | git hash-object --stdin
```

C8: c5cb5177eba1b084177e7560953c34875fceee9c
