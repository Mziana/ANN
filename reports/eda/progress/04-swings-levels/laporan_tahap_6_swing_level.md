# Laporan Tahap 6 — Notebook 04 (`eda_04_swings_levels.ipynb`, Q5 Swing + Q6 Level + Placebo)
**Tanggal:** 2026-10-06
**Status:** SELESAI — **20/20 assertion PASS**, 0 error, VALID, **belum di-commit** (menunggu keputusan user)

## 1. Tujuan
Menjawab **Q5** (struktur swing/fraktal M5) dan **Q6** (apakah level benar-benar "dihormati"
pasar), dengan **kontrol placebo yang dipreregistrasi di nb00**. Inti Q6: hit-rate reaksi
level **nyata** dibandingkan terhadap level **placebo**, bukan dinilai secara absolut.

## 2. File yang Dibuat/Diubah
- `notebooks/scalping/eda_04_swings_levels.ipynb` — baru, **19 sel** (**9 kode, 10 markdown**).
  (Komposisi dikoreksi dari klaim lama "10 kode, 9 markdown" yang terbalik — SA-46, lihat §9.)
  (Nama file dikoreksi dari `eda_04_swing_level.ipynb` sesuai D8 — lihat §9.)
- `scripts/_build_eda04.py` — generator + eksekutor.
- **Tidak mengubah** `src/`, `configs/`, atau data.

## 3. Apa yang Dilakukan
1. Kunci definisi sesi **dan** baca protokol placebo langsung dari `eda_00_setup.ipynb`.
2. Muat M5 + D1, hitung ATR(14), `theta = 0.5 x ATR(14)` dengan `.shift(1)` (anti look-ahead).
3. **Q5:** fraktal k=3 dan k=5 per sisi, ukuran dinormalisasi ATR, sebaran per sesi/tahun.
4. **Q6:** event touch round-number (xx.00 primer, xx.50 alternatif) + prior-day H/L
   (broker primer, UTC sekunder).
5. Mesin reaksi first passage: `away` / `through` / `tie` / `none` per window k ∈ {6,12,24}.
6. **Dua kontrol placebo** sesuai preregistrasi + bootstrap day-cluster 10.000 resample.

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Protokol placebo identik preregistrasi nb00 | TERVERIFIKASI | konstanta di-parse dari nb00 via `ast`, di-assert sama; assertion PASS |
| Seed = 20261006, timeframe = M5, theta = 0,5xATR(14) | TERVERIFIKASI | assertion PASS |
| Q5: 4 kombinasi swing (k=3/5 x high/low) | TERVERIFIKASI | 20.169 / 20.314 / 12.787 / 13.070 swing |
| Stratum A M5 = 227.568 (sama dengan nb03) | TERVERIFIKASI | assertion PASS — konsisten lintas notebook |
| Theta tanpa NaN di stratum A | TERVERIFIKASI | warmup ATR habis di stratum B |
| Event terdeteksi untuk semua jenis level | TERVERIFIKASI | xx.00 11.896 · xx.50 · H/L broker 10.477 · UTC |
| Tie dilaporkan terpisah, tidak dihitung reversal | TERVERIFIKASI | kolom `tie` ada; assertion PASS |
| Placebo tidak degeneratif | TERVERIFIKASI | hit-rate placebo < 0,95 (assertion PASS) |
| CI day-cluster tidak runtuh, semua ≥ 30 hari | TERVERIFIKASI | assertion PASS |
| nb04: 20/20 PASS, 0 error, urut | TERVERIFIKASI | `RINGKASAN: 20/20`, `GAGAL=0`, exec [1..10] |
| Gate hijau | TERVERIFIKASI | ruff 0 · format 29 file 0 · pytest 157 passed · validate 0 · chars OK |

### Temuan utama (k primer = 12 bar M5) — hasil NEGATIF

| Level | Nyata | Placebo acak | Placebo H/L |
|---|---|---|---|
| round_xx00 | **0,4694** | 0,4989 | — |
| round_xx50 | **0,4892** | — | — |
| hl_broker | **0,4799** | 0,5050 | 0,4922 |
| hl_utc | **0,4905** | — | 0,4890 |

**Level nyata TIDAK melampaui placebo.** Bahkan hit-rate level nyata (0,469-0,490) **lebih
rendah** dari placebo (0,499-0,505). Artinya: pada definisi touch & reaksi yang dipreregistrasi
ini, **tidak ada bukti** bahwa round-number atau prior-day H/L "dihormati" pasar lebih dari
level acak. Ini temuan negatif yang jujur — dan justru alasan kontrol placebo ada.

## 5. Self-Audit 3× Adversarial

### Putaran 1 — Correctness
- **SA-42 (DITEMUKAN, diperbaiki) — placebo 1 degeneratif.** Implementasi literal
  (level digeser, bar sama) menghasilkan hit-rate placebo **0,893-0,915 vs nyata 0,47**.
  Sebabnya: level yang digeser sering jatuh **di luar rentang bar**, sehingga `away`
  terpicu seketika tanpa harga pernah menyentuh level placebo. Itu **artefak geometri**,
  bukan kontrol. Diperbaiki: level placebo **wajib genuinely disentuh** (cari bar terdekat
  sampai `MAX_K`). Sesudah perbaikan: 0,499-0,505 — **sebanding** dengan nyata.
- **SA-43 (DITEMUKAN, diperbaiki) — placebo 2 varian UTC kosong.** `daily_atr_broker`
  dipetakan ke event yang ber-`day` UTC, sehingga seluruh ATR NaN → 0 event → CI NaN.
  Diperbaiki dengan peta ATR per definisi hari (`atr_map`).
- **SA-44 (DITEMUKAN, diperbaiki) — assertion tautologis.** Saya menulis
  `int(A["theta"].isna().sum()) == A["theta"].isna().sum()` yang selalu True. Diganti
  menjadi `== 0` (fakta terukur: warmup ATR habis di stratum B). **Assertion tidak
  dilemahkan — justru diperketat.**
- **SA-45 (DITEMUKAN, diperbaiki) — B007 loop variable tak terpakai** di sel penambah kolom
  `day`; diganti `_nama` di builder lalu notebook di-regenerasi.

### Putaran 2 — Bias & Aturan
- **Parameter preregistrasi tidak diubah sama sekali**: offset 5-25 pip, tanda acak per
  event, ATR harian 0,25-1,00, seed 20261006, k primer 12. Yang saya ubah adalah
  **konstruksi event**, bukan parameter — dan itu dinyatakan terbuka di markdown notebook.
- **Tidak ada P&L / pemilihan metode / imputasi.**
- Anti look-ahead: `theta` hanya dari ATR sampai `t-1`; first passage hanya memindai
  bar `t+1..t+k` (tidak ada data `t+1` di fitur `t`).
- **Temuan negatif dilaporkan apa adanya** — tidak ada upaya mencari definisi yang membuat
  level "menang".
- Fraktal Q5 dinyatakan **deskriptif** (terkonfirmasi k bar setelahnya), bukan fitur real-time.

### Putaran 3 — Yang Terlewat
- **Retensi event placebo 1 hanya 46,8-55,7%** (placebo/nyata setelah syarat "genuinely
  disentuh"). Placebo punya sampel lebih kecil dari nyata; ini **keterbatasan**, dilaporkan
  di notebook, bukan disembunyikan. Arahnya tetap aman untuk kesimpulan negatif (placebo
  yang lebih kecil tetap tidak kalah).
- **Interpretasi placebo masih perlu konfirmasi Klenz.** nb00 menulis pergeseran level
  tanpa menyatakan syarat "harus  disentuh". Saya memilih konstruksi yang membuat placebo valid sebagai kontrol touch, dan menandainya
  eksplisit. **Ini titik yang paling perlu direview.** → **RESOLVED 2026-10-06: D11 VALID** (§9).
- Kalender berita di luar scope → reaksi di sekitar rilis berita ikut terhitung.
- `tie` (satu bar memuat dua ambang) dikecualikan dari hit-rate; jumlahnya dilaporkan.
- Fibonacci tidak diuji (hanya boleh dengan protokol identik; tidak diuji di nb04).

### Verdict
- **Siap lapor? Ya, dengan satu pertanyaan protokol.** 20/20 assertion PASS (semuanya fakta
  terukur), 0 error, urutan terbukti, gate hijau.
- **4 temuan diperbaiki** (SA-42, SA-43, SA-44, SA-45); SA-42 adalah yang paling penting
  karena tanpa perbaikan itu, placebo akan melaporkan hasil yang salah arah.
- **1 pertanyaan terbuka untuk Klenz/user:** apakah interpretasi "level placebo wajib
  disentuh" sesuai maksud preregistrasi nb00?
  → **TERJAWAB 2026-10-06**: Architect (Spark) memutuskan **D11 VALID** — interpretasi
  coder sah, kode **tidak diubah** (§9).

## 6. Yang Belum Diverifikasi
- Interpretasi konstruksi placebo (lihat §5 Putaran 3) — **SUDAH dikonfirmasi** sebagai
  D11 VALID pada 2026-10-06 (§9); tidak lagi terbuka.
- Robustness window k=6 dan k=24 (dihitung di notebook, dibahas di laporan nb05).
- Uji Fibonacci — belum, sesuai batas.
- Efek biaya spread terhadap reaksi level — di luar scope EDA.
- nb04 belum di-commit.

## 7. Potensi Masalah
- **Retensi placebo 1 ~50%** → daya banding placebo lebih lemah dari ideal.
- `cost_basis.default` 0,65 vs `spread.default` 1,5 masih dua otoritas.
- Blok `_sesi` fragmen belum diterapkan ke config.
- Kunci tahun berbeda tipe (`spread.by_year` int vs `cost_basis.by_year` str).

## 8. Langkah Berikutnya
- **Langkah 7 — nb05** (Q7 regime) + `report.md` EDA, termasuk pembenahan penomoran figure
  (SA-09 dari nb01).
- **Keputusan user yang terbuka:** (a) commit nb04; ~~(b) konfirmasi interpretasi placebo~~
  → **TERJAWAB** D11 VALID (§9); (c) commit nb03 dan tahap 5 **sudah** dilakukan (commit `e4efbfd`).

## 9. Addendum 2026-10-06 — D8 (nama file) + D11 (placebo)

Ditambahkan saat eksekusi perbaikan 12 deviasi (langkah 1 dari urutan perbaikan).

### D8 — rename file (trivial, nol komputasi)

- `notebooks/scalping/eda_04_swing_level.ipynb` → `notebooks/scalping/eda_04_swings_levels.ipynb`
  (nama di Rancangan v3.1 §3/§12 langkah 7).
- `scripts/_build_eda04.py`: `NB_PATH` + module docstring disesuaikan → regenerasi kelak
  menulis ke nama yang benar (builder = sumber kebenaran).
- Isi notebook **tidak berubah**: `grep -c "eda_04" <nb>` = **0** (tidak ada rujukan
  nama-diri di sel/output) dan `git mv` memindahkan entri indeks apa adanya —
  `git hash-object <nb>` = `git ls-files -s <nb>` = `1ad2ad1e8482ee8f07c3aff7c1bbe06a38434e98`,
  status tetap `A ` (tanpa `M`) → worktree == indeks, tidak ada modifikasi tersembunyi.
- Notebook tetap notebook *tereksekusi* (bukan hasil regenerate kosong): 9/9 sel kode punya
  output, `execution_count` = 1..9 berurutan, output terakhir
  `RINGKASAN: 20/20 assertion PASS untuk Q5/Q6/placebo.` → **tidak perlu eksekusi ulang**.

### D11 — putusan Architect: **VALID**, kode tidak diubah

Verdict (`eda_review_deviations_v1.md`, D11): aturan touch identik di kedua sisi
(`low <= L <= high`; nb04:510/603 == nb00:819), `MAX_K = 24` simetris, parameter
preregistrasi di-assert identik, retensi non-degeneratif (0,557/0,468), hit placebo
≈ 0,49–0,51 vs nyata 0,47. Tanpa syarat-touch, kontrol literal degeneratif (0,89–0,95) —
maka perbandingan terkondisikan adalah yang sah secara statistik.

- **Status: DICATAT, tidak diubah.** Nol perubahan kode/notebook untuk D11.
- Formalisasi ke adendum rancangan v3.2 bersifat opsional (wewenang user/Architect,
  bukan coder).

### SA-46 (BARU, ditemukan saat self-audit langkah 1) — klaim komposisi sel terbalik

- **Klaim lama (§2):** nb04 = 19 sel ("10 kode, 9 markdown").
- **Fakta (`nbformat`, dihitung ulang):** 19 sel = **9 kode + 10 markdown**.
  Pembanding metode: nb03 = 17 sel = 8 kode + 9 markdown (klaim tahap 5 **cocok**),
  jadi ini kesalahan spesifik nb04, bukan cara hitung yang berbeda.
- **Status: DIKOREKSI** (satu baris, nol komputasi) + dilaporkan terbuka di sini.
  Ini deviasi **baru** di luar 12 deviasi D1–D12 → butuh ratifikasi user.

## 10. STOP — Tunggu Review User
