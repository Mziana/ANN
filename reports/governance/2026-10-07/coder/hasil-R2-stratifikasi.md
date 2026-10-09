# Hasil Coder -- R-2 Stratifikasi Tahun H4 (jam-tetap lock, 2024 vs 2025)

**Peran penulis:** Coder (AGENTS.md S26: implementasi + self-audit + fix;
DILARANG menentukan arsitektur; DILARANG audit formal; DILARANG vonis H4/H5).
**Spec:** `reports/governance/2026-10-07/arsitek/spesifikasi-R2-stratifikasi.md`
(blob `c04199cea2acfd692b731fcb7eacec16b0e4691d`).
**Tanggal eksekusi:** 2026-10-09.

## S-0. Konfirmasi pre-flight

AGENTS.md v3.0 dibaca penuh sebelum satu baris pun dieksekusi; HEAD terukur
`e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`; staged terukur tepat 2 file T6
(`src/features/build_labels.py` + `tests/test_build_labels.py`, milik
asisten-atas-perintah-user, tidak disentuh sesi ini). Tanpa konfirmasi ini
gerbang gagal; konfirmasi ini ada maka gerbang jalan.

## S-4. Gerbang (output mentah ditempel; klaim tanpa output mentah = GAGAL)

### G0 HEAD

```
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169
```

### G-S0 hash 9 file (diukur sesi ini via git hash-object, urutan brief)

```
c04199cea2acfd692b731fcb7eacec16b0e4691d  spesifikasi-R2-stratifikasi.md
4a46b815211e6b0b050cbb6f3e98ce5e27904069  spesifikasi-lapisan3-H4H5.md
f06a8e27b916172f5824438acd545614360d3b57  hasil-lapisan3-H4H5.md
8a4d21090f27dd53555b3a12583ec337819efb2f  reaudit-lapisan3-H4H5.md
e02a203b96879d73e90339f2d78a37d15834a23a  putusan-lapisan3-H4H5.md
ed436fddf607d3629fa226fd34d20ff60bf47232  protokol-telaah-fondasi-B.md
0284f5f022ce1c147cefef6dd7780aded6acf820  hasil-telaah-fondasi-B.md
7d125022cd14113325e5c5721da53a39be661f5c  disposisi-fondasi-B.md
fe11383b9bdd1e58819e32812eec75c52ab3aee9  putusan-H4b-stabilitas.md
```

8 hash S0 cocok awalan brief (`4a46b815...` s/d `fe11383b...`); spec R-2
cocok penuh. Mismatch = STOP; tidak ada mismatch maka lanjut.

### G-staged + worktree

```
git diff --cached --name-only:
src/features/build_labels.py
tests/test_build_labels.py
```

Staged tepat 2 T6. DILARANG stage/commit/push/stash/checkout oleh sesi ini;
tidak satu pun dilakukan (saksi: status SESUDAH identik SEBELUM kecuali
satu file laporan ini).

### G-nol-tulis

`git status --porcelain` SESUDAH identik SEBELUM kecuali file laporan ini
(`reports/governance/2026-10-07/coder/hasil-R2-stratifikasi.md`, untracked
baru). File sementara HANYA di harness `%TEMP%\opencode\r2\`
(`r2.py`, `r2_hasil.json`, `r2_hasil_run1.json`, `r2_hasil_run2.json`,
`r2_run1.log`, `r2_run2.log`). NOL tulis ke `src/`/`configs/`/`data/`.

## S-2. Input beku (assert SEBELUM hitung di dalam harness; output mentah)

```
pip_size = 0.01
cost_basis.by_session[London] = 0.61
cost_basis.by_session[NewYork] = 0.69
cost_basis.by_session[Tokyo] = 0.62
cost_basis.by_session[Sydney] = 0.8
cost_basis.default (Off) = 0.65
FIXED_HOURS lock = [14, 13, 0, 15, 12, 7]
sha256 M1 2024 = 69b2c026d3ac52d47b2d29e6bb80a1747f32a46cc611ef7bebbdb3f74e213cac
sha256 M1 2025 = fce65a3a1fa715735b9ff58cfc3f1075172b2272a314d493bb2e3ff0762238af
sha256 M15 features = cd6a85e472dec353086cbd03064a74d355eee0dc977a340912ad6452c1e160fb
sha256 D4 day labels = 47d15c4142823b3a98aa1daceadddba7b486a92aaf5a899cc9742882168e7d6c
```

Awalan cocok spec (`69b2c026...`, `fce65a3a...`, `cd6a85e4...`,
`47d15c41...`); nilai penuh 64-hex di-assert dari provenans Batch-2
(konstanta diimpor dari `sh4.py`, bukan ketik-ulang). Varian default
INKLUSI. NOL konstanta diubah.

## S-3. Mesin + join-gate (satu mesin Batch-2; output mentah)

Harness: `%TEMP%\opencode\r2\r2.py` (tanpa `main()` di jalur eksekusi;
fungsi `run()` + guard `__main__`). Konstanta + helper (`FIXED_HOURS`,
`COST_*`, `SHA_*`, `plain`, `sha256_file`) diimpor dari
`%TEMP%\opencode\l3h4h5\sh4.py` via importlib (identitas, bukan salinan).
Loop entry HANYA `sh4.FIXED_HOURS` (di-assert `== [14,13,0,15,12,7]`);
grain hari-broker tunggal (`groupby("broker_day")`; `utc.normalize()`
tidak dipakai di mana pun). ATR = `daily["atr_14_d1"].shift(1)`,
cross-check exact vs kolom store beku.

```json
{
  "n_bar_pool_m15": 47721,
  "n_bar_store_pool": 47721,
  "n_sama": true,
  "sekuens_date_broker_identik": true,
  "sekuens_hour_utc_identik": true,
  "atr_daily_metrics_identik_store_exact": true,
  "n_hari_common_atr": 974,
  "n_hari_broker_pool": 519,
  "rentang_pool": ["2024-01-02T00:00:00", "2025-12-31T00:00:00"]
}
```

## R2-4. Stratifikasi tahun (output mentah run 1; penentu lock R-2)

```json
{
  "2024": {
    "n_trade": 1560,
    "median_ev_jpy": 0.04834999999999022,
    "mean_ev_jpy": 0.024799771062270975,
    "persen_positif": 0.5487179487179488,
    "n_exit_SL": 87,
    "n_exit_TP": 9,
    "n_exit_time_stop": 1464,
    "n_Off_deskriptif_sesi_Off": 0,
    "n_fallback_bukan_tabel_biaya": 0,
    "n_trade_hari_karantina_F1": 30
  },
  "2025": {
    "n_trade": 1554,
    "median_ev_jpy": -0.005049999999992838,
    "mean_ev_jpy": -0.0039283324140465484,
    "persen_positif": 0.49356499356499356,
    "n_exit_SL": 71,
    "n_exit_TP": 6,
    "n_exit_time_stop": 1477,
    "n_Off_deskriptif_sesi_Off": 0,
    "n_fallback_bukan_tabel_biaya": 0,
    "n_trade_hari_karantina_F1": 0
  }
}
```

Hari karantina F-1 di pool (deskriptif, bukan penentu):
`['2024-10-28', '2024-10-29', '2024-10-30', '2024-10-31', '2024-11-01']`
= tepat 5 hari F-1; 30 trade karantina = 5 hari x 6 jam (INKLUSI,
tanpa eksklusi lain, diputus fondasi-B D-1). n_Off 0/0 per tahun
(ESK-1: inoperatif struktural 2024-2025; non-penentu, dilaporkan
deskriptif).

## S-7. Aturan baca TERTUTUP (tepat satu vonis mekanis)

```json
{
  "aturan": "GUGUR bila median EV SATU PUN tahun-uji <= 0; TAHAN hanya bila KEDUA tahun > 0",
  "median_ev_2024": 0.04834999999999022,
  "median_ev_2025": -0.005049999999992838,
  "tahun_gugur": [2025],
  "verdict": "GUGUR(R-2)"
}
```

Median 2025 (`-0.005049999999992838`) <= 0 sedangkan median 2024
(`0.04834999999999022`) > 0: satu tahun gagal cukup maka lock
diterapkan mekanis tanpa tafsir-ulang: **GUGUR(R-2)** = tak stabil
antar-tahun pada split jam-tetap. DILARANG merembet ke TAHAN(H4
Batch-2) (P-5 dua arah mengikat; keterbatasan EKS-3 dicatat di spec).
Tanpa statistik tambahan; tanpa H5; tanpa kalibrasi; tanpa H6.

## G-det + toolchain (2x run; output mentah)

```
sha256 r2_hasil_run1.json = 4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4
sha256 r2_hasil_run2.json = 4664B4D89151485A29AC445192EFD08E81E22770B155A8F665A5F08F967E64A4
cmp run1 run2 -> LASTEXITCODE 0 (IDENTIK byte-per-byte)
python 3.12.8 | pandas 2.2.3 | numpy 1.26.4 | scipy 1.17.1 | pyarrow 17.0.0
interpreter: D:\ANN\venv\Scripts\python.exe
```

## Gate mutu (rc + cakupan ditempel)

```
pytest: venv\Scripts\python.exe -m pytest tests -q --no-header (FULL-SUITE)
  -> 254 passed in 24.32s, rc 0
ruff check: r2.py -> All checks passed!, rc 0
ruff format --check: r2.py -> 1 file already formatted, rc 0
  (cakupan = tiap file harness yang ditulis: r2.py satu-satunya)
foreign: scripts\check_foreign_chars.py (laporan ini + r2.py) -> rc 0
C8: hitung hash-artefak berprefix 0x di isi dokumen ini = 0
```

## Klaim & Bukti (S5)

| Klaim | Status | Bukti |
|---|---|---|
| S-0 dibaca + HEAD/staged terukur sesi ini | TERVERIFIKASI | AGENTS.md v3.0 dibaca penuh; HEAD + 9 hash + staged 2 T6 ditempel di atas |
| Input beku cocok sebelum hitung | TERVERIFIKASI | 4 sha256 + biaya nilai-per-nilai + FIXED_HOURS ditempel; assert mesin lolos (rc run 0) |
| Join-gate + ATR exact lolos | TERVERIFIKASI | n_sama true; sekuens identik true/true; ATR exact true (974 hari); pool 519 hari-broker |
| 2024: n 1560, median EV 0.04835 > 0 | TERVERIFIKASI | JSON mentah R2-4 di atas; exit SL/TP/time_stop 87/9/1464 |
| 2025: n 1554, median EV -0.00505 <= 0 | TERVERIFIKASI | JSON mentah R2-4 di atas; exit SL/TP/time_stop 71/6/1477 |
| n_Off deskriptif 0/0 per tahun | TERVERIFIKASI | `n_Off_deskriptif_sesi_Off` 0 dan 0; fallback 0 dan 0 (non-penentu) |
| Karantina F-1 INKLUSI, 5 hari tepat | TERVERIFIKASI | 5 tanggal 2024-10-28..11-01; 30 trade 2024 / 0 trade 2025; tanpa eksklusi lain |
| Verdict mekanis GUGUR(R-2) | TERVERIFIKASI | 2025 <= 0 memicu OR-gugur; diterapkan verbatim, tanpa tafsir-ulang |
| Determinisme byte-identik 2x | TERVERIFIKASI | sha256 sama + cmp LASTEXITCODE 0 + toolchain ditempel |
| Nol tulis repo + staged utuh + tanpa main() | TERVERIFIKASI | status SESUDAH == SEBELUM + 1 laporan; staged tetap 2 T6; `run()` + guard |
| Vonis H4/H5 di dokumen ini | BELUM DIVERIFIKASI | - (DILARANG oleh spec; vonis = putusan terpisah sesudah re-audit) |

## Self-audit 3x

1. **Correctness.** Angka R2-4 cocok digit-per-digit dengan bacaan arsitek
   di spec S-V(b) (0.04834999999999022/1560; -0.005049999999992838/1554;
   n_Off 0/0) -- tiga rekaman sepakat (JSON run ini + JSON Batch-2 +
   bacaan spec); loop entry hanya `sh4.FIXED_HOURS` yang di-assert sama
   dengan lock; tidak ada `utc.normalize()` di `r2.py` (grain
   `broker_day` semata); `r2_hasil.json` ditulis deterministik
   (`plain` + indent + newline, tanpa timestamp).
2. **Bias & asumsi.** Ambang tidak disetel (lock verbatim OR-gugur dari
   spec; hasil GUGUR dilaporkan apa adanya padahal 2024 positif --
   tahun-negatif tidak disembunyikan pool karena pool dilarang sebagai
   penentu); EKS-3/bobot konfirmatori terbatas adalah keterbatasan spec,
   dikutip bukan disembunyikan; karantina F-1 dihitung INKLUSI (30 trade
   tetap di dalam angka penentu) sesuai D-1; tanpa sub-sel/ambang/window
   pasca-hoc (B2); tanpa H6 (B4); tanpa guard nilai-vs-diri (B6 --
   assert hanya vs konstanta Batch-2/spec).
3. **Meta-check.** Lock Batch-2/fondasi-B/H4b utuh (NOL konstanta diubah;
   mesin diimpor bukan disalin); ruang auditor tidak diambil (replikasi
   dari nol tetap dimungkinkan dari `r2.py` + JSON mentah); ruang arsitek
   tidak diambil (tanpa vonis H4/H5 di sini); STOP menutup.

STOP. Eksekusi R-2 selesai; ronde re-audit menunggu perintah terpisah.
Hash dokumen ini TIDAK ditempel di isi (C8); dilaporkan di kanal luar.
