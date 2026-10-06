# Laporan Tahap 5 — Notebook 03 (`eda_03_autocorr.ipynb`, Q4 Autokorelasi)
**Tanggal:** 2026-10-06
**Status:** SELESAI — **17/17 assertion PASS**, 0 error, VALID, **belum di-commit** (menunggu keputusan user)

## 1. Tujuan
Menjawab **Q4** dari Rancangan EDA v3: apakah return M1/M5/M15 menunjukkan autokorelasi,
seberapa besar efeknya, dan apakah arahnya (mean-reversion atau momentum) berbeda menurut
time-frame, sesi UTC, dan tahun. Semua angka dihitung pada **stratum A** (semesta yang
diperdagangkan), dengan versi **no-gap** sebagai pembanding.

## 2. File yang Dibuat/Diubah
- `notebooks/scalping/eda_03_autocorr.ipynb` — baru, **17 sel** (8 kode, 9 markdown).
- `scripts/_build_eda03.py` — generator + eksekutor.
- `scripts/_build_eda01.py`, `scripts/_build_eda02.py` — perbaikan akar masalah (lihat §7).
- `notebooks/scalping/eda_01_returns.ipynb`, `eda_02_volatility.ipynb` — **di-regenerasi**
  ulang setelah akar masalah diperbaiki.
- **Tidak mengubah** `src/`, `configs/data.yaml` (nilai), atau data mentah.

## 3. Apa yang Dilakukan
1. Kunci definisi sesi via sidik jari (anti-drift dari nb00) — sama seperti nb01–nb02.
2. Muat M1/M5/M15 2023–2026, return log BID, label sesi primer, stratifikasi A/B/C.
3. **ACF lag 1–20** per time-frame, versi `all` dan `no-gap`, plus p-value dua-sisi.
4. **Variance ratio** `VR(l) = Var(r_lag)/(l·Var(r_1))` per lag (formulasi Lo-MacKinlay).
5. **Pemisahan arah per sesi** (ACF lag-1 + VR(2)) dan **stabilitas per tahun**.
6. Assertion penutup + ringkasan hasil dan batasnya.

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Definisi sesi identik nb00 | TERVERIFIKASI | sidik jari == `EXPECTED_FINGERPRINT`, assertion PASS |
| Tiga time-frame termuat & urut naik | TERVERIFIKASI | assertion PASS; M1 1.136.401 bar |
| ACF dihitung 20 lag × 3 TF | TERVERIFIKASI | assertion PASS |
| Tidak ada assertion `True` hardcode | TERVERIFIKASI | regex `\("[^"]+",\s*True\)` → 0 hasil di seluruh sel kode |
| `VR(1) = 1,0000` di ketiga TF | TERVERIFIKASI | tabel VR kolom lag=1 = 1,0000; assertion definisional PASS |
| ACF lag-1 no-gap M1 = −0,004372 | TERVERIFIKASI | output nb03 strata A |
| ACF lag-1 no-gap M5 = −0,011582 · M15 = +0,003496 | TERVERIFIKASI | output nb03 strata A |
| Rata-rata VR(lag≥2): M1 0,9771 · M5 0,9978 · M15 1,0127 | TERVERIFIKASI | output nb03 |
| Tanda ACF1 M1 tidak stabil antar tahun | TERVERIFIKASI | 2023 −, 2024 +, 2025 −, 2026 −; assertion PASS |
| Baris `Off` berlabel `n/a` (bukan "mean-reversion") | TERVERIFIKASI | `n=0`, acf NaN → `n/a`; assertion PASS |
| nb03: 17/17 assertion PASS, 0 error, urut | TERVERIFIKASI | `RINGKASAN: 17/17`, `GAGAL=0`, exec [1..8] |
| nb01/nb02 tidak rusak setelah regenerasi | TERVERIFIKASI | nb01 22/22, nb02 20/20, keduanya 0 error |
| Fragmen spread tetap cocok dengan config | TERVERIFIKASI | `cost_basis` & `stress_bands` dict-identik |
| Nilai config lama tidak tersentuh | TERVERIFIKASI | `by_year {2023:3.0, 2024:1.5, 2025:1.5, 2026:1.5}`, `default 1.5`, `pip_size` utuh |
| Gate hijau | TERVERIFIKASI | ruff check 0 · format 27 file 0 · pytest 157 passed · validate_data 0 · chars OK |

**Angka kunci (stratum A, no-gap):**

| Metrik | M1 | M5 | M15 |
|---|---|---|---|
| ACF lag-1 | −0,004372 | −0,011582 | +0,003496 |
| rata-rata VR(lag≥2) | 0,9771 | 0,9978 | 1,0127 |
| arah dominan | mean-reversion | mean-reversion lemah | momentum lemah |

Per sesi (M1): London p=0,000084 dan NewYork p=0,0271 → mean-reversion signifikan.
Sydney bertanda momentum tetapi **p=0,4439 → tidak signifikan**, jadi tidak dibaca sebagai
temuan. Tokyo p=0,054 (batas).

## 5. Self-Audit 3× Adversarial

### Putaran 1 — Correctness
- **SA-35 (DITEMUKAN, diperbaiki) — ambang gap tidak mengikuti skala time-frame.** Saya
  menyalin `utc.diff() > 1 menit` dari nb01/nb02. Untuk M1 itu benar, tetapi pada M5/M15
  **setiap** bar selisihnya ≥5/15 menit, sehingga **seluruh** bar ditandai gap: kolom
  no-gap jadi kosong dan `variance_ratio` membagi nol (`ZeroDivisionError`). Diperbaiki
  dengan `TF_MINUTES = {M1:1, M5:5, M15:15}`. Tanpa temuan ini notebook akan melaporkan
  "tidak ada return no-gap" sebagai fakta.
- **SA-36 (DITEMUKAN, diperbaiki) — `variance_ratio` memakai selisih, bukan jumlah.** Versi
  pertama memakai `values[lag:] - values[:-lag]`, sehingga `VR(1) ≈ 2` dan `VR(20) ≈ 0,10`
  pada data iid. Assertion definisional "`VR(lag=1)` mendekati 1" **menggagalkan** build,
  lalu saya verifikasi ulang di luar notebook: formulasi jumlah memberi `VR=1,0000` pada
  data iid dan `VR(2)=0,799` pada AR1 dengan acf1=−0,20 (teori: 1+acf1=0,8). **Assertion
  tidak dilemahkan** — implementasinya yang diperbaiki agar cocok dengan formula yang
  didokumentasikan.
- **SA-37 (DITEMUKAN, diperbaiki) — `VR[TIMEFRAMES]` dibaca pandas sebagai satu kunci tuple**
  (`KeyError: ('M1','M5','M15')`). Diganti `VR.loc[:, list(TIMEFRAMES)]`.
- **SA-38 (DITEMUKAN, diperbaiki) — baris `Off` dilabeli "mean-reversion".** Karena
  `np.where(NaN > 0)` bernilai False, baris dengan `n=0` dan acf NaN mendapat label yang
  salah. Ditambah cabang `isna() → "n/a"` plus assertion penjaganya.
- **SA-39 (DITEMUKAN, diperbaiki) — nama assertion tidak cocok dengan isinya.** Assertion
  berlabel "ACF1 per tahun bertanda konsisten" ternyata menguji **magnitudo** (`abs < 0,05`).
  Label diganti menjadi "Semua |ACF1| per tahun < 0,05", dan temuan yang sebenarnya
  (tanda M1 **tidak** stabil antar tahun) diangkat menjadi assertion tersendiri + masuk
  ringkasan notebook.

### Putaran 2 — Bias & Aturan
- **Tidak ada P&L / equity / backtest**, tidak ada pemilihan metode, tidak ada imputasi.
- **Tidak menulis `configs/`** dari notebook; hanya membaca.
- **M1 tidak dipakai untuk inferensi sinyal** — batas yang sama seperti nb01 tetap dijaga.
- Efek kecil dinyatakan sebagai efek kecil (|ACF| ≤ 0,012), dan dibandingkan dengan biaya
  `cost_basis.default` 0,65 pip, bukan dibesar-besarkan menjadi "temuan strategi".
- Sydney yang tidak signifikan **dinyatakan tidak signifikan**, tidak diangkat jadi temuan.

### Putaran 3 — Yang Terlewat
- **SA-40 (DITEMUKAN, akar masalah diperbaiki) — klaim laporan sebelumnya keliru.** Audit
  fix 4b menyatakan "7 isu ruff diperbaiki **di builder**". Kenyataannya perbaikan itu
  diterapkan ke `.ipynb` saja. Buktinya: begitu `scripts/_build_eda02.py` dijalankan ulang
  (untuk memperbaiki `_status` fragmen), ruff kembali menandai **I001 di nb02** dan **F401
  `utc_series` di nb01** — persis regresi kelas SA-34. Semua perbaikan sekarang dilakukan
  di builder: urutan import dibetulkan di ketiga builder, `utc_series` dihapus dari nb01.
- **SA-41 (DITEMUKAN, diperbaiki) — format notebook drift setiap regenerasi.** `ruff format
  --check` menolak ketiga notebook setelah regenerasi, karena formatnya pernah diperbaiki
  langsung di `.ipynb`. Alih-alih memperbaiki ulang secara manual (yang akan hilang lagi),
  **setiap `build()` sekarang menjalankan `ruff format` pada notebook hasil generator**
  sebelum eksekusi. Builder tetap satu-satunya sumber kebenaran, dan properti "regenerasi
  → bersih" menjadi idempoten.
- **Kalender berita tetap di luar scope** → autokorelasi masih memuat efek berita & gap.
- **Tidak ada koreksi multiple-comparison** pada 20 lag × 3 TF × 4 tahun; p-value dilaporkan
  apa adanya dan **tidak** dijadikan dasar klaim.

### Verdict
- **Siap lapor? Ya.** 17/17 assertion PASS (semuanya fakta terukur), 0 error, urutan
  eksekusi terbukti, tidak ada assertion `True` hardcode, seluruh gate hijau.
- **4 bug nyata ditemukan & diperbaiki** (SA-35, SA-36, SA-37, SA-38) — dua di antaranya
  akan menghasilkan angka yang salah bila lolos (VR tidak bermakna, no-gap kosong).
- **1 koreksi laporan** (SA-40): klaim "fixed in builder" pada laporan 4b **tidak benar**
  dan sudah dikoreksi di sini; akar masalahnya kini benar-benar diperbaiki.

## 6. Yang Belum Diverifikasi
- Uji autokorelasi multivariat / formal (mis. Ljung-Box sebagai keputusan) — sengaja tidak
  dijadikan kesimpulan karena n > 1 juta bar membuat hampir semua uji menolak.
- Kalender berita resmi (NFP/CPI/FOMC) — tidak dipakai; pemisahan news spike di luar scope.
- Efek biaya transaksi pada "profitabilitas" autokorelasi — di luar scope EDA; hanya
  dibandingkan secara kualitatif terhadap `cost_basis`.
- nb03 belum di-commit (menunggu keputusan user).

## 7. Potensi Masalah
- **`_sesi` di fragmen belum diterapkan ke config.** Fragmen memuat blok `_sesi`
  (syarat backtest wajib memakai pelabelan DST-aware). Config kini punya `cost_basis` dan
  `stress_bands`, tetapi **belum** punya `_sesi`; definisi sesi masih hidup di
  `notebooks/scalping/_eda_common.py`. Ini keputusan user (dua sumber kebenaran?).
- **Dua otoritas biaya masih hidup bersama:** `cost_basis.default` 0,65 vs `spread.default`
  1,5 (selisih 2,3×). Backtest wajib menyebut mana yang dipakai.
- **Kunci tahun berbeda tipe** antara `spread.by_year` (int) dan `cost_basis.by_year` (str).
  Consumer baru harus memakai `str(year)`; sudah dicatat di komentar config.
- **M5 bukan parquet asli** bila belum diverifikasi; kalibrasi M1–M4 nb02 tetap acuan.

## 8. Langkah Berikutnya
- **Langkah 6 — nb04** (Q6 prior-day high/low + Q7 regime), dengan putusan Architect R1–R4:
  kerja level-hari dikunci pada **tanggal-broker**, hari-UTC hanya sekunder.
- **Langkah 7 — nb05** + `report.md` EDA, termasuk pembenahan penomoran figure (SA-09).
- **Keputusan user yang masih terbuka:** (a) commit nb03; (b) penerapan blok `_sesi`;
  (c) kode otoritas biaya spread.

## 9. STOP — Tunggu Review User
