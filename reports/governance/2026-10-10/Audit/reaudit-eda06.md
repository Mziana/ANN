# Re-audit EDA-06 — Biaya, Microstructure, dan Break-even

Tanggal: 2026-10-10. Peran: **Auditor** (bukan arsitek, bukan coder).
Brief: `.ai/assistant/prompts/2026-10-10_reaudit-eda06-auditor.md` (blob `9c429eb0`).
Metode: hitung ulang dari nol dari parquet + config. **Tidak ada satu baris pun
kode notebook/builder yang diimpor** sebagai kebenaran — seluruh harness ditulis
ulang dari definisi di kontrak. Bahasa: Indonesia. STOP setelah serah-terima.

---

## 1. Vonis

**LOLOS — sah sebagai gerbang, dengan satu catatan terbuka (lihat §5, T-1).**

Gerbang dihitung ulang dari nol dan **identik** dengan artefak repo pada
seluruh penentu: 144 irisan tercile dengan 23 lolos, 48 irisan sesi dengan 7
lolos, funnel `K1 32 → K1&K2 23 → +K3 23 → +K4 23`, dan flag `K1/K2/K3/K4/LOLOS`
cocok **baris-per-baris** pada ke-192 irisan. Tidak ada satu pun klaim coder yang
tahan uji independen.

LolOS **bukan bukti edge**. Sesuai kontrak sel 2, ini hanya izin memfokuskan
EDA-07 pada 23+7 irisan tertentu.

---

## 2. S-0 — Gerbang masuk

| Objek | Hash (git hash-object) | Klaim brief | Status |
|---|---|---|---|
| `scripts/_build_eda06.py` | `fab369e674321867666356d031132a7f20ef854e` | `fab369e6` | COCOK |
| `notebooks/scalping/eda_06_biaya_breakeven.ipynb` | `dd0f229d6a18dbbdbe69d2f6022bba445cff64a7` | `dd0f229d` | COCOK |
| referensi `eda_06_biaya_breakeven.ipynb` | `6a6c6516bc96e7e9a7845a13b1909927cc718e75` | `6a6c6516` | COCOK |
| referensi `EDA_06_07_rancangan.md` | `6724c37ec5493b821d0179d0d00768fbd343a485` | `6724c37e` | COCOK |
| HEAD | `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` | `b18992b` | COCOK |
| staged | 0 berkas | nol stage | COCOK |

S-0 **LOLOS**.

---

## 3. Klaim & Bukti

### A1 — Replikasi tiga tabel penentu

| Klaim | Status | Bukti (perintah + output) |
|---|---|---|
| T-06-1a sebaran spread per sesi tereplikasi | TERVERIFIKASI | `a1a2a3_replika.py`; max abs diff vs `T-06-1a_spread_sesi.csv` = **4,939e-07** (bulat `%.6g`). London n=308.536 mean=0,6094; NewYork n=228.021 mean=0,7096; Tokyo n=285.448 mean=0,6183; Sydney n=63.849 mean=0,8076; SEMUA(A) n=885.854 mean=0,6523; B n=185.248 mean=1,3919 |
| T-06-4 grid p* tereplikasi (A+B terpisah) | TERVERIFIKASI | 32 baris replikasi = 32 baris artefak; strata artefak `['A','B']` (16+16). max diff `m_pip`=4,414e-05, `p*_normal`=4,921e-07, `p*_stres`=4,980e-07, `n`=0 |
| T-06-5a preset 50/70 tereplikasi | TERVERIFIKASI | max diff `n`=**0** (persis), `E`=3,994e-07, `delta_pp`=4,645e-06, `p_none`=3,644e-08, `amb`=1,000e-09. London delta=5,0645 pp; NewYork 5,2488; Tokyo 4,9190; Sydney 6,3399 |

### A2 — Anti look-ahead

| Klaim | Status | Bukti |
|---|---|---|
| ATR M5(14) hanya bar M5 **selesai** | TERVERIFIKASI | Harness auditor mengimplementasikan ulang `merge_asof(direction="backward")` pada `T = utc + 1 menit` terhadap `avail = bucket + 5 menit`. ATR tersedia 1.024.509 / 1.078.001 bar — **identik** dengan output sel 15 |
| Anti look-ahead 12 timestamp identik | TERVERIFIKASI | Replikasi harness (seed 20261010): `semua identik? True`. Lolosan: London `mean=-0,607737` vs `-cost=-0,61`; Tokyo `-0,590277` vs `-0,62` — konsisten dengan biaya, bukan dengan advantage |
| Barrier hanya bar **sesudah** entri | TERVERIFIKASI | Harness memakai `sliding_window_view(HI, HORIZON+1)[ii][:, 1:]` → bar `idx+1 … idx+120`, tidak pernah bar entri. Semua angka `E`/`p_tp`/`p_none` cocok artefak pada presisi bulat |
| SL menang bila sebar (pesimis) | TERVERIFIKASI | `ambigu` tereplikasi: London 0,0037 / NewYork 0,0013 / Tokyo 0,0017 / Sydney 0,0019 — cocok artefak |
| Tidak ada input masa depan lain | TERVERIFIKASI | `no_c` memakai `C_CUM` kumulatif hanya Maju; `cont` hanya membandingkan `UTC_NS[idx+H] − UTC_NS[idx]`; tercile/desil dihitung dari ATR entri itu sendiri |

### A3 — Holdout dan universe

| Klaim | Status | Bukti |
|---|---|---|
| 2026 **nol bar** di pipeline | TERVERIFIKASI | Parquet `usdjpy_m1_2026.parquet` **ada** di disk (269.846 bar, UTC 2026-01-01 23:00 → 2026-10-02 20:57) tapi **tidak pernah dimuat** — `YEARS = (2023,2024,2025)`. Replikasi: `bar_2026_utc: 0`, `tahun_ada_setelah_filter: [2023, 2024, 2025]` |
| Batas hari broker dihormati | TERVERIFIKASI | Filter `broker_day >= 2026-01-01` aktif dan_remove 0 bar (karena 2026 memang tak dimuat). `max_utc_setelah_filter` < 2026-01-01. **Catatan:** proteksi berlapis — andai 2026 dimuat, bar tepi UTC 31 Des malam sudah tertangkap filter hari-broker |
| B = 185.248 | TERVERIFIKASI | Replikasi `b_mask` (broker_day 2023-01-01…06-30) = **185.248** persis |
| B terpisah, tidak masuk K2 | TERVERIFIKASI | `T-06-7_gerbang_tercile/sesi` **tidak punya kolom strata** — seluruh 192 irisan dari A. `T-06-6_barrier_semester` hanya berisi `['2023H2','2024H1','2024H2','2025H1','2025H2']` — **2023H1 (strata B) absen**. B tetap dilaporkan terpisah di `T-06-5_barrier_B.csv` (96 baris) dan `T-06-4` strata B |
| C dibuang | TERVERIFIKASI | C = 6.899 bar. Tidak ada tabel T-06-4/5/6/7 yang memuatnya. `B ∩ C = 0`, `A+B+C = 1.078.001` (partisi utuh) |
| Nol bar `Off` di A | TERVERIFIKASI | `Off_di_A: 0` |
| Fingerprint sesi | TERVERIFIKASI | Dihitung ulang dari nol: `Tokyo:Asia/Tokyo:9-18\|London:Europe/London:8-16\|New York:America/New_York:8-17\|Sydney:Australia/Sydney:8-16\|priority=London>NewYork>Tokyo>Sydney\|xtab=is_tokyo:0-9,is_london:8-16,is_ny:13-22,is_sydney:21-6` — identik `EXPECTED_FINGERPRINT` |

### A4 — Cakupan

| Klaim | Status | Bukti |
|---|---|---|
| 27/27 sel **VERBATIM** | TERVERIFIKASI | Perbandingan `(cell_type, source)` per sel repo↔referensi: `n_cells_repo: 27`, `n_cells_referensi: 27`, `n_sel_berbeda: 0`, `VERBATIM_27_SEL: true`. 16 sel kode |
| Notebook tereksekusi penuh | TERVERIFIKASI | `execution_count` = `[1..16]` berurutan, `n_output_error: 0` |
| FIG-08..12 ada dan sah | TERVERIFIKASI | 5 PNG, signature `\x89PNG\r\n\x1a\n` valid, ukuran 31.795–110.759 B, sha256 prefix `d9b55bc4 / 21ed6f0c / 17308d53 / 0c3514e3 / a6ddd283` |
| 14 CSV lengkap dan terbaca | TERVERIFIKASI | 14/14 terbaca, **NaN = 0** di semua kolom. Baris: 1a=6, 1b=24, 1c=5, 1d=5, 2a=10, 2b=6, 3=24, 4=32, 5B=96, 5desil=240, 5sesi=96, 6=480, 7sesi=48, 7tercile=144 |
| FIG-01..07 tak tersentuh | TERVERIFIKASI | Tetap di `reports/eda/2026-10-06/figures/`; tidak ada FIG-01..07 baru di `2026-10-10` |

### A5 — Gerbang K1-K4 (hitung ulang penuh)

| Klaim | Status | Bukti |
|---|---|---|
| 144 + 48 irisan diuji | TERVERIFIKASI | Replikasi: `irisan diuji: tercile=144 \| sesi=48` |
| LOLOS 23 + 7 | TERVERIFIKASI | `LOLOS: tercile=23 dari 144 \| sesi=7 dari 48` |
| Funnel 32 → 23 → 23 → 23 | TERVERIFIKASI | `Funnel tercile: K1=32 \| K1&K2=23 \| K1&K2&K3=23 \| +K4=23` |
| Flag K1–K4 identik baris-per-baris | TERVERIFIKASI | `K1_cocok: true`, `K2_cocok: true`, `K3_cocok: true`, `K4_cocok: true`, `LOLOS_cocok: true` — pada ke-144 dan ke-48. `max_abs_diff_sem_ok = 0`, `max_abs_diff_n = 0`, `max_abs_diff_n_days = 0` |
| VERDICT | TERVERIFIKASI | `VERDICT replikasi = LOLOS` |
| T-06-5b drift buy vs sell | TERVERIFIKASI | Dihitung ulang; p_tp buy ≈ sell pada tiap sesi (selisih pada orde 1e-3), konsisten "tanpa sinyal keduanya harus mirip" |

**Funnel sesi** (tidak diklaim coder, dihitung auditor): `K1=10 → K1&K2=7 → +K3=7 → +K4=7`.

### A6 — Mutu dan determinisme

| Klaim | Status | Bukti |
|---|---|---|
| pytest hijau | TERVERIFIKASI | `254 passed in 18.91s` |
| builder ruff + format | TERVERIFIKASI | `All checks passed!` / `1 file already formatted` |
| builder ASCII / LF / tail-LF | TERVERIFIKASI | `non_ascii=0`, `CRLF=0`, `tail_ok=True` |
| Ruff notebook = 14 temuan | TERVERIFIKASI | Repo **dan** referensi: 14 temuan, **komposisi identik** — 9×E402, 3×SIM300, 1×B023, 1×B905. Klaim coder benar |
| Notebook deterministik | TERVERIFIKASI | **Replay persis** urutan konsumsi RNG notebook (32 draw bootstrap sel 13 → 1 draw sel 15 → 1 draw sel 17) menghasilkan CI **cocok sampai 4,41e-07** (= presisi tulis CSV `%.6g`). Lihat §5 T-2 |

### A7 — Integritas

| Klaim | Status | Bukti |
|---|---|---|
| HEAD tidak berubah | TERVERIFIKASI | `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` di awal **dan** akhir audit |
| Nol staged / commit / push | TERVERIFIKASI | `staged = 0 berkas` |
| Referensi tak tersentuh | TERVERIFIKASI | Hash kedua referensi identik S-0 (lihat §2) |
| Auditor menulis hanya laporan ini | TERVERIFIKASI | Seluruh harness di `%TEMP%\eda06_audit` (7 skrip). `git status` akhir: satu-satunya entri baru = `reports/governance/2026-10-10/` |
| Nol tulis ke configs/src/data | TERVERIFIKASI | `git status --porcelain` tidak memuat `configs/`, `src/`, `data/` |

---

## 4. Angka yang dihitung ulang dari nol

T-06-5a preset 50/70 point, skenario normal, strata A, delta dalam poin persen:

| sesi | n | n_hari | p_tp | p_none | amb | E (pip) | delta_pp |
|---|---|---|---|---|---|---|---|
| London | 122.826 | 643 | 0,3597 | 0,0131 | 0,0037 | −0,6077 | 5,0645 |
| NewYork | 59.308 | 641 | 0,3420 | 0,0458 | 0,0013 | −0,6299 | 5,2488 |
| Sydney | 8.566 | 424 | 0,3512 | 0,0047 | 0,0019 | −0,7608 | 6,3399 |
| Tokyo | 113.050 | 643 | 0,3569 | 0,0217 | 0,0017 | −0,5903 | 4,9190 |

Preset 50/70 **tidak lolos** di sesi mana pun pada irisan sesi (delta ≥ 4,92 pp, jauh di atas K1 = 3,0 pp). Yang lolos seluruhnya berasal dari barrier ATR lebar dan `FIX_100_140`.

Empat irisan terkuat (delta_pp normal | stres):

| combo | sesi | tercile | n | delta_normal | delta_stres |
|---|---|---|---|---|---|
| ATR_k1.5_rr2 | Tokyo | 3 | 37.684 | 1,344 | 1,888 |
| ATR_k1.5_rr2 | London | 3 | 40.946 | 1,379 | 1,663 |
| ATR_k1.5_rr1.4 | Tokyo | 3 | 37.684 | 1,494 | 2,120 |
| ATR_k1.5_rr1.4 | London | 3 | 40.946 | 1,617 | 1,981 |

Pola yang terlihat: **`ATR_k1.5` mendominasi, dan Tokyo/London tercile 3 mendominasi.** Tercile 3 = ATR M5(14) tinggi di tengah rentang sesi — bukan ekor. Sydney nyaris tak muncul (hanya `FIX_100_140` tercile 1).

---

## 5. Temuan

### T-1 (MENENGAH — terbuka, bukan cacat) — Sel 27 masih kosong

Notebook menutup dengan sel markdown **"Kesimpulan (isi manual setelah membaca tabel)"**
yang **tidak diisi**. Isi sel 27 adalah lima pertanyaan teliti (sesi/jam mana
ekornya terburuk, adakah p\* ≤ 0,53, dsb.) — bukan boilerplate.

Dampak: artefak EDA-06 yang sedang di-*hand-off* **tidak memuat jawaban atas C1–C3**.
Gerbang K1–K4 berdiri sendiri dan tidak bergantung sel 27, sehingga vonis
**tidak terganggu**. Tapi tabel deskriptif C1–C3 (T-06-1a/b/c/d, 2a/2b, 3) belum
disimpulkan di mana pun.

Fakta yang sudah dihitung ulang dan siap dipakai arsitek: minimum p\*_
normal strata A = **0,5212** (di bawah 0,53 — jadi ambang sel 27 **terpenuhi**, bukan
tidak tercapai);Sydney punya ekor spread paling buruk (39,10% bar > 2× default,
mean 0,8076 pip); T-06-1b menunjukkan pola per jam.

### T-2 (RENDAH) — CI bootstrap rapuh terhadap urutan draw

Pada replikasi penuh, `E_lo`/`E_hi` menyimpang sampai **4,7e-02** pip. Ini **bukan**
ketidakdeterminan notebook. Bukti: dengan mereplay urutan konsumsi RNG notebook
(32 draw bootstrap sel 13 → 1 draw choice sel 15 → 1 draw sel 17), CI cocok sampai
**4,41e-07** — tepat presisi bulat `%.6g`.

Artinya: angka CI hanya dapat direproduksi bila urutan sel tidak berubah. Menyisipkan
satu sel yang memakai `RNG` di sel 5 akan menggeser seluruh CI. Tidak berpengaruh ke
vonis — **K1–K4 tidak memakai `E_lo`/`E_hi` sama sekali**, hanya `delta_pp_normal`,
`delta_pp_stres`, `sem_ok`, `n`, `n_days`, `p_none`, yang semuanya cocok persis.
Saran: allocate RNG terpisah per analisis bila EDA-07 butuh CI yang stabil.

### T-3 (RENDAH — sesuai klaim coder) — 14 temuan ruff pada notebook

E402×9, SIM300×3, B023×1, B905×1. **Komposisi identik dengan referensi** → bawaan
referensi, bukan regresi eksekusi. Setiap perbaikan = pelanggaran kunci VERBATIM.
Tidak diperbaiki; tercatat sebagai keputusan arsitek.

### T-4 (INFORMATIF) — Biaya=config memuat 2026

`cost_basis` dan `stress_bands` di config disusun termasuk 2026, sedangkan analisis
2023–2025. Sel 7 mengasersi selisih < 0,15 pip dan lolos. Tidak ada bias terhadap
2026 karena 2026 tak pernah dimuat — hanya catatan bahwa config adalah angka global,
bukan statistik 2023–2025.

### T-5 (INFORMATIF) — B INITIALLY BUKAN " Regime vol tinggi" yang diasumsikan

Nama "B" berasal dari stratifikasi Lapisan 1 (H1-2023). Rata-rata spread B = 1,3919
pip vs 0,6523 di A — memang jauh lebih mahal, konsisten dengan deskripsi. Tidak
menjadi temuan; hanya memastikan stratifikasi tidak berubah makna.

---

## 6. Yang belum diverifikasi

- **Isi sel 27** (Kesimpulan) — kosong, bukan wewenang auditor (§5 T-1).
- **Rerun notebook end-to-end** — tidak dilakukan auditor karena__
  `REPORT_DIR = reports/eda/<tanggal>` memakai `date.today()` sehingga eksekusi ulang
  akan menimpa artefak repo. Determinisme dibuktikan lewat replay RNG (§5 T-2)
  dan replikasi penuh A1–A5 yang identik.
- **Makna economis 23+7 irisan** — di luar wewenang auditor (bukan backtest, bukan
  vonis). LOLOS ≠ edge.

---

## 7. Rekomendasi

1. **Terima gerbang LOLOS.** Angka konsisten di tiga sumber (notebook, CSV, replikasi
   auditor). Lanjut ke spec EDA-07 dengan scope = 23 irisan tercile + 7 irisan sesi.
2. **Isi sel 27** (pembaca/arsitek) sebelum EDA-07 — lima pertanyaannya sudah
   menjadi bahan jawab dari data yang ada.
3. **Pisahkan RNG per analisis** bila EDA-07 memerlukan CI bootstrap yang stabil
   lintas perubahan urutan sel.
4. **Rombak nol-titik session bucket**: preset 50/70 gagal di semua sesi
   (delta ≥ 4,92 pp). Jika EDA-07 memakai barrier, mulai dari `ATR_k1.5_rr{1,1.4,2}`
   pada Tokyo/London tercile ATR 3, dan `FIX_100_140` sebagai pembanding.

**Catatan tambahan**: 39,10% bar Sydney punya spread > 2× default — bila nanti ada
strategi pada sesi Sydney, model biayanya perlu disesuaikan lebih dulu.

---

## 8. Output mentah (kunci)

```
fab369e674321867666356d031132a7f20ef854e   <- scripts/_build_eda06.py
dd0f229d6a18dbbdbe69d2f6022bba445cff64a7   <- notebook (post-exec)
6a6c6516bc96e7e9a7845a13b1909927cc718e75   <- referensi ipynb
6724c37ec5493b821d0179d0d00768fbd343a485   <- referensi md
b18992b5e57d45c125aacf3ca868c2f9e135d9d1   <- HEAD (tak berubah)

A1 T-06-1a : max abs diff vs artefak        = 4.939e-07
A1 T-06-4  : 32 baris = 32 baris | strata A,B | max|diff m_pip| = 4.414e-05
A1 T-06-5a : max|diff n| = 0 | E = 3.994e-07 | delta_pp = 4.645e-06
A2 ATR     : 1.024.509 / 1.078.001 | anti look-ahead 12/12 identik = True
A2 entri   : kandidat 215.576 -> valid 184.731 (A=151.875, B=32.856)
A3         : A=885.854 B=185.248 C=6.899 | Off_di_A=0 | 2026 nol bar
A4         : 27 sel | n_sel_berbeda=0 | 14 CSV NaN=0 | 5 PNG valid
A5         : 144+48 | LOLOS 23+7 | funnel 32->23->23->23 | semua flag cocok
A6         : 254 passed | 14 temuan ruff (E402x9,SIM300x3,B023,B905)
A6 replay  : max |diff CI| pada urutan RNG persis = 4.409e-07
A7         : HEAD tetap b18992b | staged 0 | nol tulis configs/src/data
```

**Harness auditor** (di luar repo, `%TEMP%\eda06_audit`): `a1a2a3_replika.py`,
`a5_gerbang.py`, `a3a7_bukti.py`, `a6_bukti_rng.py`, `a6_bukti_replay.py`,
`a4a_cells.py`, `dump_cells.py`.

---

**PUTUSAN AUDITOR: LOLOS — sah sebagai gerbang biaya EDA-06.**
Syarat terpenuhi: replikasi independen cocok, anti look-ahead terbukti, holdout utuh,
strata terpisah, determinisme terbukti. Catatan T-1 terbuka untuk peran pembaca.

STOP.
