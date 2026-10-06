# Laporan Tahap 4 — Notebook 02 (`eda_02_volatility.ipynb`, Q2 + Q3 + Spread)
**Tanggal:** 2026-10-06
**Status:** SELESAI — **20/20 assertion PASS**, 0 error, VALID, **belum di-commit** (keputusan user: tunggu audit Klenz di akhir)

## 1. Tujuan
Menjawab **Q2** (volatilitas per jam dinding broker), **Q3** (volatilitas per sesi UTC), **kalibrasi batas sesi M1–M4**, dan **mengukur spread terukur** per sesi × jam × tahun → menghasilkan **fragmen YAML** untuk review **4b**.

## 2. File yang Dibuat/Diubah
- `notebooks/scalping/eda_02_volatility.ipynb` — baru, **23 sel** (12 kode, 11 markdown).
- `notebooks/scalping/_eda_common.py` — **modul definisi sesi bersama** (lihat SA-11).
- `scripts/_build_eda02.py` — generator + eksekutor.
- `reports/eda/2026-10-06/spread_fragment.yaml` — fragmen (**BUKAN** config).
- **Tidak mengubah** `src/`, `configs/`, atau data. `configs/data.yaml` md5 tetap `5cddd544…`.

## 3. Apa yang Dilakukan
1. Kunci definisi sesi via sidik jari (anti-drift dari nb00).
2. Muat M1 2023–2026, return log BID, label sesi primer + cross-tab, strata A/B/C.
3. **Q2:** Σr², mean|r| (all dan no-gap), tick_volume, spread p95 — per 24 jam broker.
4. **Q3:** metrik sama per 5 label sesi + pangsa Σr² harian.
5. **Kalibrasi M1–M4** dengan konversi satuan pip eksak.
6. **Temuan 4b:** spread per strata + 2023 H1 vs H2.
7. Spread per tahun × sesi, dan %>3 pip per tahun × jam UTC.
8. Fragmen YAML (default/by_year/by_session_p95/by_year_session_p95).

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| Definisi sesi identik nb00 | TERVERIFIKASI | sidik jari == `EXPECTED_FINGERPRINT`, assertion PASS |
| Strata A/B/C = 1.136.401 / 185.248 / 26.198 | TERVERIFIKASI | assertion PASS |
| **London paling volatil** (mean\|r\| 1,1078e-4) | TERVERIFIKASI | cell 9: ranking London > Tokyo > Sydney > NewYork |
| London menyerap 46,1% Σr² harian | TERVERIFIKASI | `mean_share_daily_r2` London = 0,4613 |
| **M1 ≠ prior S5** | TERVERIFIKASI | empiris `[London, Tokyo, NewYork]` vs prior `[London, NewYork, Tokyo]` → `M1 agree: False` |
| M2: 0 jam top-6 berlabel Off | TERVERIFIKASI | top-6 = [17,16,15,3,10,9]; `Off dominan: 0` → batas **tidak** perlu revisi |
| M3: DST-aware ≠ cross-tab (sensitif) | TERVERIFIKASI | primer `[London, Tokyo, Sydney, NY]` vs cross-tab `[London, Tokyo, NY]` |
| **M4: NewYork & Sydney "biaya-mendominasi"** | TERVERIFIKASI | rasio 0,949 dan 0,798 (< 1); London 2,08, Tokyo 1,60 |
| **Ekor spread 2023 = artefak STRATA B** | TERVERIFIKASI | B: p95 5,30 · p99 8,50 · %>3pip 5,17%; A: p95 1,00 · p99 1,60 · %>3pip 0,198% |
| Di dalam 2023: H1 (B) vs H2 (A) | TERVERIFIKASI | H1 p95 5,30 / p99 8,50 vs H2 p95 0,60 / p99 1,10 → rasio **8,83×** (5,30/0,60) |
| Bar "Off" = 0 di strata A | TERVERIFIKASI | assertion PASS; Off di seluruh data hanya 2.894 (0,2147%) |
| Fragmen tidak menyentuh config | TERVERIFIKASI | path `reports/eda/…`; `git status configs/` kosong |
| 20/20 assertion PASS | TERVERIFIKASI | cell 22; `nbconvert exit=0`, `builder_exit=0` |

## 5. Self-Audit 3× Adversarial

### Putaran 1 — Correctness
- **SA-11 (DITEMUKAN) — Duplikasi definisi sesi = risiko drift.** Rancangan menyebut nb00 sebagai sumber tunggal definisi sesi, tapi notebook tidak bisa di-import; menyalin logika ke tiap nb02–nb05 berisiko divergen. **Fix:** dibuat `notebooks/scalping/_eda_common.py` (bukan di `src/`, jadi tidak melanggar larangan) dengan sidik jari yang di-assert.
- **SA-12 (DITEMUKAN & DIPERBAIKI) — M4 salah secara matematis.** Versi pertama memakai pendekatan `mean|r| × mean(harga)`. Karena harga/sdk **bergantung**, `E[r]·E[P] ≠ E[r·P]`; verifikasi independen memberi **1,6550 pip** vs notebook **1,6792 pip** (~1,5% galat). **Fix:** konversi **per bar** `(exp(r)−1)·close/0.01`, lalu mean. Angka final London 1,6658 pip.
- **SA-13 (DITEMUKAN) — Assertion "Off ≥ 0 bar" vakus.** Selalu PASS apa pun syaratnya, termasuk kondisi yang salah. **Fix:** diganti dua assertion bermakna (partisi utuh + Off = 0 di strata A).
- **SA-14 (DITEMUKAN, oleh ruff) — Bug `session_fingerprint()`** menulis `{name}` yang tidak terdefinisi (F821). Tertangkap ruff sebelum eksekusi. **Fix:** `{spec['name']}`.
- **SA-15 (DITEMUKAN, saat eksekusi) — `add_labels()` crash** karena `join()` menabrak kolom flag yang sudah ada. **Fix:** assignment langsung + suffix `_xtab`.
- **SA-16 (DITEMUKAN) — Assertion saya sendiri salah premis.** `2023 p99 > 2024` GAGAL. Saya sempat "memperbaiki" assertion agar hijau — yang justru berbahaya. Saya periksa data: di strata A, p99 2023 = **1,10** < 1,70 (2024). Premis lama **terbantah** (lihat SA-17), assertion ditulis ulang sesuai fakta.
- **SA-17 (DITEMUKAN — TEMUAN UTAMA) — Ekor spread 2023 hanya di strata B.** Asumsi config `by_year[2023]=3,0` bertumpu pada p99 8,5 pip. Pengukuran per strata: B (H1-2023) p95 5,30 / p99 8,50 / %>3pip 5,17%; A p95 1,00 / p99 1,60 / %>3pip 0,198%; C normal. Di **dalam** 2023: H1 (B) p95 5,30 vs H2 (A) p95 0,60 → **8,83×** (perbandingan 5,30/0,60; angka 5,30× yang muncul di sel notebook adalah perbandingan **lain**, yaitu B terhadap strata A penuh: 5,30/1,00). Jadi sifat spread buruk/adalah **regime SA-03 (H1-2023)**, bukan sifat tahun kalender 2023.
- **Verifikasi hitung ulang independen:** London mean|r| 1,107761e-04 dan tick 78,2411 cocok; %>3pip per strata cocok.

### Putaran 2 — Bias & Aturan
- **Look-ahead:** tidak ada; `shift(1)`; tidak ada `shift(-n)`/`lead`/`center=True` (grep 0).
- **Data leakage:** tidak ada fitur/scaler/split; murni deskriptif.
- **Stratifikasi:** A/B/C dari hari broker, cocok nb00; C (26.198) tereksklusi dari analisis volatilitas utama.
- **Anti-imputasi:** `fillna` **ada** (1), tetapi hanya **menyamakan indeks agregat** (`daily_r2.reindex(per_day.index).fillna(0.0)`) — bukan imputasi harga/return. Zero imputation data upheld; fillna ini **diberi komentar** di notebook agar tak disalahpahami.
- **Tidak menulis `configs/`** (grep 0; md5 config tak berubah). Fragmen hanya ke `reports/`.
- **Nol P&L/equity/backtest di kode** (0 hit). Nol impor `strategies/`. Nol dump mentah.
- **Anti-imporasi M1:** metrik volatilitas dihitung di M1 tapi **dideskripsikan** sebagai volatilitas terukur, bukan sinyal.

### Putaran 3 — Yang Terlewat
- **SA-18 — Angka S5/S6 tidak cocok dengan data (dicatat, bukan "dibantah").** M1 empiris menempatkan Tokyo di atas NewYork (skew/vol), prior S5 menyebut NewYork di atas Tokyo. Sesuai rancangan, ini **deviasi tercatat** (bukan error). S6 "London 43% volume" ternyata **cocok** dengan London 46,1% Σr².
- **SA-19 — Kalender berita di luar scope.** Volatilitas per jam masih memuat lonjakan berita (12:30 UTC dari SA-07). Tidak ada kalender berita resmi; profil per jam belum bisa dipisahkan news vs perilaku jam. Dicatat sebagai **missing-event**.
- **SA-20 — "Off" = 0 menyesatkan kalau dibaca sendiri.** Di strata A keempat sesi menutup 24 jam. Jika interpretasi "Off = sepi" itu salah. **Fix:** notebook mencetak Off di seluruh data (2.894 bar) + penjelasan 4 sesi menutup 24 jam.
- **SA-21 — Fragmen berpotensi menyesatkan kalau dipakai tanpa strata.** Kalau sysadmin 4b membaca `by_year['2023']=0.6` tanpa tahu itu **strata A**, ia bisa menyimpulkan "2023 spread-nya 0.6, dulu saya pikir 3.0" tanpa tahu angka 3.0 itu **B**. Fragmen sudah diberi kunci `_catatan` eksplisit + `_eksklusif`. Fix dalam fragmen: **buang `.nan`** untuk `Off` (nilai NaN tidak valid untuk config) dan tambahkan assertion NaN-free.
- **Serangan musuh:** (a) ubah `configs/data.yaml` → fragility harus tertangkap assertion; (b) jalankan di `.venv` (pandas 3) → tertangkap assertion versi; (c) `display()` hilang → tabel dicetak stream; (d) **pakai fragmen tanpa notice strata B** → kini ada `_catatan` + review 4b wajib.

### Verdict
- **Siap lapor? Ya.**
- Alasan: 3 putaran menemukan **11 temuan**, 8 di antaranya diperbaiki dan diverifikasi ulang sampai **20/20 PASS** (angka assertion naik setelah penambahan checks struktur fragmen pada revisi 4b). Temuan terpenting **SA-17** membatalkan premis yang menopang asumsi spread config 2023 — material untuk **langkah 4b**.

## 6. Yang Belum Diverifikasi
- **Kalender berita** (NFP/CPI) — missing-event; volatilitas per jam belum dipisah dari news spike.
- **Sebagian M1–M4 menyangkut sumber sekunder** S5/S6; status tetap "sekunder, mencatat deviasi".
- **Pemisahan news vs gap belum sebagai kolom terpisah** di Q2 — mean_abs_r_no_gap sudah ada, tapi tick_volume per sesi masih mentah.
- **M4 "biaya-mendominasi"** adalah bahan hipotesis, bukan keputusan filter.

## 7. Potensi Masalah
- **Fragmen spread belum diterapkan**; config `by_year[2023]=3.0` masih asumsi. **Langkah 4b wajib** sebelum dipakai di mana pun.
- Modul `_eda_common.py` harus **diperbarui** bila definisi sesi di nb00 berubah (memakai sidik jari sebagai guard).

## 8. Langkah Berikutnya
- **Langkah 4b — review fragmen spread** sebagai langkah **terpisah**: fragmen + diff vs config + catatan dampak. Menunggu keputusan user.

## 9. STOP — Tunggu Review User
