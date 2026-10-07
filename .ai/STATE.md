# STATE.md — Status Saat Ini

**Update terakhir:** 2026-10-07
**Fase:** Lapisan 2 (EDA) — dimulai; Lapisan 0–1 selesai dan ter-commit
**Progress keseluruhan:** ~60%

## Ringkasan Eksekutif

Semua checkpoint (01, 05-09d) **SUDAH SELESAI**. State file lama menandai
sebagian besar sebagai belum — itu sudah usang dan sudah dikoreksi di sini.
Environment siap, MT5 terhubung, data historis terbukti tersedia.
**`src/` berisi 1.775 baris** (`validate_data.py` 540, `fetch_data.py` 363,
`resample.py` 351, `clean_data.py` 258, `broker_time.py` 196,
`utils/config.py` 65, ditambah dua `__init__.py` satu baris).

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

- [x] Phase B: `src/data/fetch_data.py` + `src/utils/config.py` + `__init__.py` + 22 test
- [x] Test 1 bulan (2026-10-01 s/d 10-06) → 3.134 bar, **7/7 verifikasi LOLOS**
- [x] Fetch full 2023-01-01 s/d 2026-10-05 -> 1.347.847 bar M1
- [x] `src/data/validate_data.py` (cek gap, baris, offset historis)
- [x] `src/data/clean_data.py` (raw -> Parquet, tanpa interpolasi)
- [x] `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1, bucket jam broker)
- [ ] `src/data/resample.py` (M1 -> M5/M15/M30/H1/H4/D1) — berikutnya
- [ ] **Akhir Milestone 1**: pecah `validate_data.py` (543 baris) jadi check vs
      render — batas keras dari user, bukan opsional lagi
- [ ] Modul `src/features/`: build_features.py, build_labels.py
- [ ] Modul `src/models/`, `src/backtest/`
- [ ] EDA (distribusi return, volatilitas per sesi, regime)
- [ ] Pemilihan metode strategi (menunggu EDA)
- [ ] Backtest + audit
- [ ] 500+ trade data (kriteria Fase 1)

## Blocker

- Tidak ada blocker eksternal.
- MT5 terminal terhubung (`connected=True`), simbol dan history data terbukti tersedia.
- `trade_allowed=False` — akun belum login untuk trading (tidak menghalangi fetch data).

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

1. **Lapisan 2 EDA — Langkah 4:** tulis `notebooks/scalping/eda_02_volatility.ipynb`
   (Q2 volatilitas per jam dinding broker + Q3 per sesi UTC + pengukuran spread
   p50/p95/p99/maks dan %>3 pip per sesi × jam × tahun) → **fragmen YAML yang BELUM
   diterapkan** ke `configs/data.yaml` → laporan mini → STOP untuk review user.
2. **Langkah 4b (terpisah):** review fragmen spread (fragmen + diff vs config +
   dampak hilir) → putusan user: terapkan / tunda / tolak.
3. Notebook 03–05 sesuai Rancangan EDA v3 Final, lalu audit adversarial Klenz dan
   penguncian hipotesis.
4. Pemilihan metode strategi — setelah EDA lulus audit (tugas terpisah).

**Status terperinci tiap tahap:** `reports/eda/progress/laporan_tahap_*.md`
(tahap 0 reuse-check, 1 pin deps, 2 nb00, 3 nb01).

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
