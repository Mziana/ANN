# Broker Contract — FINEX

**Status:** tercatat 2026-10-14 · **Otoritas machine-readable:** [`configs/broker.yaml`](../configs/broker.yaml)

Dokumen ini adalah catatan manusiawi. Angka yang dipakai kode ada di
`configs/broker.yaml` — bukan di sini. Kalau ada selisih, **config yang menang**.

---

## ⚠️ Baca ini sebelum pakai

Setiap baris di bawah punya **provenance** yang berbeda. Jangan memperlakukan
semuanya sebagai fakta terverifikasi dengan bobot yang sama:

| Penanda | Arti |
|---|---|
| `[TERUKUR]` | Dihitung dari `data/processed/M1/*.parquet`. Bisa diaudit ulang kapan saja. |
| `[INPUT]` | Diberikan user. Belum dicek ke dokumen broker. |
| `[SPESIFIKASI]` | Dari spec/broker. **Belum ada sumber dokumen di repo ini.** |
| `[VERIFIKASI]` | **Wajib dikonfirmasi sebelum dipakai untuk keputusan dagang.** |

Hanya `[TERUKUR]` yang bisa dipertanggungjawabkan secara independen. Itu tidak
sedikit — spread adalah komponen terbesar dari biaya. Tapi sisanya belum.

---

## Isi kontrak

| Field | Nilai | Provenansi |
|---|---|---|
| Broker | FINEX | — |
| Tipe akun | Standard / Reguler (akun tunggal terpadu) | `[SPESIFIKASI]` |
| Komisi | **$1,00 / lot per sisi** (dibebankan saat buka + lagi saat tutup) | `[TERVERIFIKASI]` — konfirmasi user 2026-10-15 |
| Ukuran kontrak | 100.000 unit / lot (1 pip = $6,6935) | `[SPESIFIKASI]` — spec Finex USD/JPY dari user 2026-10-15, cocok silang anchor di bawah |
| Spread rata-rata | **0,65 pip** | `[TERUKUR]` |
| Spread p95 | **1,00 pip** | `[TERUKUR]` |
| Spread p99 / max | 1,60 / 55,60 pip | `[TERUKUR]` |
| Slippage | rendah — STP, mayoritas < 1 detik | `[SPESIFIKASI]` |
| Swap long/short | Free Swap (Akun Islami) → $0,00 | `[SPESIFIKASI]` `[VERIFIKASI]` |
| Leverage | s/d 1:500 (Forex & Logam, akun Standard) | `[SPESIFIKASI]` — spec Finex dari user 2026-10-15 |
| Minimum lot | 0,01 lot (mikro) = 1.000 unit | `[SPESIFIKASI]` — spec Finex dari user 2026-10-15 |
| Maksimum volume | 50 lot / order (= 5.000.000 USD eksposur) | `[SPESIFIKASI]` — spec Finex dari user 2026-10-15 |
| Pip size USDJPY | 0,01 | `[SPESIFIKASI]` — spec Finex dari user 2026-10-15 |
| Execution | Market Execution / STP, tanpa requote | `[SPESIFIKASI]` `[VERIFIKASI]` |
| Regulasi | BAPPEBTI · anggota JFX & KBI | `[SPESIFIKASI]` `[VERIFIKASI]` |

> **SUMBER ANGKA 100.000 UNIT/LOT — spec Finex, cocok silang anchor kamu.**
> Spec resmi USD/JPY dari user (2026-10-15): 1,0 lot = 100.000 USD ·
> 0,1 lot = 10.000 USD · 0,01 lot = 1.000 USD · mata uang dasar USD ·
> pip size 0,01 · maksimum 50 lot/order · leverage s/d 1:500.
> Angka ini **cocok silang independen** dengan anchor pengguna di repo
> (bukan satu-satunya sumber lagi):
> `scripts/archive/eda-06-07/_build_eda06.py:411`
>
> ```python
> USD_PER_POINT_001 = 1.6 / 251   # patokan pengguna: 251 point = $1,6 pada lot 0,01
> ```
>
> Dibalik-balikkan (1 point = 0,001; kurs = 0,001 × unit / $ per point):
>
> | Ukuran kontrak | Kurs USDJPY implisit | Masuk akal? |
> |---|---|---|
> | **100.000** | **156,88** | **ya** — di dalam rentang data 127,26–163,97 |
> | 10.000 | 15,69 | tidak — USDJPY tidak pernah di sana |
> | 1.000.000 | 1.568,75 | tidak |
>
> 100.000 adalah satu-satunya pembacaan yang masuk akal — dan sekarang juga
> didukung spec langsung.
>
> **Keterbatasan yang tersisa:** kurs saat kamu mengamati angka `$1,6` itu
> belum tercatat (implisitnya 156,88). Komisi tetap `[INPUT]` user —
> bukan spec sheet Finex. Kalau terminalMU nanti menampilkan nilai
> berbeda, tabel biaya harus dihitung ulang.
>
> **Kesalahan yang sudah dikoreksi di dokumen ini:** versi sebelumnya menulis
> Mid pada 10.000 unit = `$1,70` dan `1,085×` komisi. Angka yang benar
> **$2,87** dan **1,44×** (komisi $2,00 flat + spread $0,87). Angka spread
> dalam pip tidak pernah berubah; hanya konversi ke dolar.

---

## Angka spread yang terukur

Dari 1.347.847 bar M1 2023–2026, kolom `spread_pips`.

| Stratum | n | mean | p50 | p95 | p99 | max |
|---|---|---|---|---|---|---|
| **A (utama)** | 1.136.401 | **0,6456** | 0,60 | **1,00** | 1,60 | 55,60 |
| B (H1-2023) | 185.248 | 1,392 | 1,00 | 5,30 | 8,50 | 34,30 |
| C (anomali) | 26.198 | 0,656 | 0,60 | 0,90 | 1,50 | 8,40 |

Per tahun (A): `2023: 0,51` · `2024: 0,70` · `2025: 0,67` · `2026: 0,62`

Per sesi (A):

| Sesi | n | mean | p95 | p99 | max |
|---|---|---|---|---|---|
| London | 395.884 | 0,608 | 0,80 | 1,20 | 4,60 |
| NewYork | 293.134 | 0,692 | 1,20 | 2,00 | **55,60** |
| Tokyo | 364.696 | 0,615 | 0,90 | 1,30 | 8,70 |
| **Sydney** | 82.687 | **0,796** | **1,50** | **2,70** | 24,10 |

> Sesi dihitung dari kolom `time` (UTC) → jam lokal DST-aware, dengan prioritas
> London > NewYork > Tokyo > Sydney. Jarang spike 55,60 pip terjadi di **NewYork,
> 24 Des 2024** (malam Natal) — bukan di Sydney.

Bar spread >3 pip di stratum A: **0,198%** (2.255 dari 1.136.401 bar).

> **Angka-angka ini cocok dengan `configs/data.yaml` → `spread.cost_basis`
> dan `spread.stress_bands`.** Verifikasi silang lolos: mean A 0,6456 vs 0,65
> · p95 1,00 vs 1,00 · p99 1,60 vs 1,60. Config dan data tidak berbeda.

---

## Skenario biaya (turunan, bukan input)

Rate pembagi: rata-rata close USDJPY 2023–2026 = **149,3987**
→ **1 pip = $6,6935** per lot (`0,01 × 100.000 unit / 149,3987`)
Formula: `spread × 2 sisi × $6,6935 + komisi $1,00 × 2 sisi`

| Skenario | Spread | Spread 2 sisi | Komisi 2 sisi | **Total** | Setara pip |
|---|---|---|---|---|---|
| **Cheap** — mean London/NY 2026 | 0,61 | $8,17 | $2,00 | **$10,17** | 1,52 |
| **Mid** — pooled A semua sesi/tahun | 0,65 | $8,70 | $2,00 | **$10,70** | 1,60 |
| **Expensive** — Sydney p95 | 1,50 | $20,08 | $2,00 | **$22,08** | 3,30 |
| **Krisis** — B H1-2023 p95 | 5,30 | $70,95 | $2,00 | **$72,95** | 10,90 |

> Angka sebelum pembulatan: Cheap mean London+NewYork 2026 = `0,6146` (n=152.461) · Mid
> pooled A = `0,6456` (n=1.136.401) · Expensive Sydney p95 = `1,50` · Krisis B p95 = `5,30`.

---

## Tiga temuan yang mengubah cara kita menghitung

### 1. Komisi cuma 19% dari biaya — spread 81%

```
Mid:  spread $8,70 (81%)  +  komisi $2,00 (19%)  =  $10,70
```

Kalau spread diabaikan, model hanya menghitung $2,00 padahal biaya sebenarnya
$10,70 — **unterstatement 81%**, atau biaya sebenarnya **5,35×** model tanpa spread.
Ini masuk akal secara struktural — komisi $1/lot itu murah, sedangkan menyeberangi
spread tidak.

> **Kenapa tabel ini tetap dipakai** meski 100.000 sudah spec resmi:
> komisi $1/lot itu nominal **flat dalam dolar** — tidak ikut diskalakan.
> Spread dalam pip justru ikut skala. Jadi proporsi spread:komisi
> **sensitif terhadap contract size**, dan ini pembuktian bahwa angka itu
> tidak bisa diasumsikan:
>
> | contract size | 1 pip | spread $ | komisi $ | total $ | x komisi | share spread |
> |---|---|---|---|---|---|---|
> | 1.000 | $0,0669 | $0,09 | $2,00 | $2,09 | 1,044x | 4,3% |
> | 10.000 | $0,6693 | $0,87 | $2,00 | $2,87 | 1,435x | 30,3% |
> | **100.000** *(spec Finex)* | **$6,6935** | **$8,70** | **$2,00** | **$10,70** | **5,351x** | **81,3%** |
> | 1.000.000 | $66,94 | $87,02 | $2,00 | $89,02 | 44,508x | 97,8% |
>
> Kalau ternyata bukan 100.000, Finding #1 ("komisi cuma 19%") bisa **berbalik
> jadi komisi 70%**, dan conclusions "spread cuma tambahan kecil" runtuh.
> Angka spread dalam pip tetap berdiri; yang runtuh hanya konversi ke dolar.
> `x komisi` dan `share spread` dihitung dari nominal yang sudah dibulatkan
> seperti yang ditampilkan di tabel, bukan dari nilai tak-bulat.

### 2. Spread bukan konstan — harus per-sesi

0,608 pip di London sampai 0,796 di Sydney, dan 5,30 di p95 saat stratum B.
Angka spread global akan salah di setiap sesi kecuali kebetulan.

### 3. Slippage sebaiknya **0**, bukan konstanta positif

Aturan OHLC repo ini berbasis **bid** (`src/data/resample.py:21`), dan
`spread_pips` sudah mengukur jarak bid-ask **per bar** — termasuk saat spread
melebar karena berita atau pembukaan sesi.

Artinya spread-widening **sudah ada di dalam angka yang kitaukur**. Menambah
konstanta slippage di atasnya = **hitung dua kali**.

Bukti pendukung: temuan D10 EDA-02 — `spread_pips_max` M5 **identik** dengan
maksimum `spread_pips` M1 di setiap bucket. M1 sudah menangkap titik ekstrem,
jadi tidak ada yang hilang dari agregasi.

> **Model yang dipakai:** biaya = `spread` (dari distribusi terukur) + `komisi`.
> Tekanan stress diskenario Krisis — bukan dengan slippage buatan.

---

## Yang WAJIB diverifikasi sebelum dipakai

Empat hal. Semuanya impacting, tidak ada yang bisa diasumsikan.

### Swap "Free" / Akun Islami

Nilai untuk scalp intraday sebenarnya **nol secara struktural** — selama semua
posisi ditutup sebelum rollover. Jadi swap tidak mengubah expectancy apa pun
untuk strategi ini.

**Yang perlu dicek:**
- Apakah Free Swap berlaku di akun **Standard**, bukan hanya Islamic/Pro?
- Berlaku untuk **USDJPY** spesifik, atau hanya metal?
- Bagaimana aturan **triple Wednesday**? (1x / 3x / 5x di hari Wednesday)
- **Peringatan:** jangan pernah pakai default "free swap" di backtest yang
  menahan posisi melewati batas hari. Itu cara paling mudah menghasilkan
  expectancy palsu.

### Leverage 1:500

Spec Finex dari user (2026-10-15): leverage s/d 1:500 berlaku untuk
Forex & Logam pada akun **Standard**. Contoh margin: lot 0,01 =
$1.000 eksposur → margin $2,00 pada 1:500.

### Regulasi BAPPEBTI / JFX / KBI

Ini bukan detail administratif — seluruh sejarah pemilihan broker bergantung
pada ini.

- **Nama entitas resmi** di daftar BAPPEBTI. Nama dagang ≠ nama entitas
  teregulasi.
- **Perlindungan deposito.** Kalau masuk KBI (Kliring Berjangka Indonesia),
  apakah dana dijamin negara? Kalau tidak, jangan tulis `$0 swap` di mana pun
  sebagai alasan "aman".
- Kalau ada perbedaan antara yang tertulis di sini dan yang ada di website
  resmi, **yang menang adalah website resmi**.

### "Tanpa requote"

Ini bukan keuntungan — ini **risiko yang tidak bisa dinegosiasi**.

Tanpa requote berarti tidak ada jaminan fill di harga yang diminta. Order bisa
**partial atau kosong** saat likuiditas tipis. Untuk scalping di session open
atau sekitar berita, itu perbedaan antara fill dan tidak fill.

Klaim "99,57% di bawah 1 detik" adalah angka marketing. Tidak bisa kita uji
ulang — kita tidak menyimpan log fill broker.

---

## Status config spread — SUDAH SELESAI

Konflik lama antara `spread.default` (1,5) dan `cost_basis.default` (0,65) di
`configs/data.yaml` **sudah diselesaikan**. Kondisi sekarang:

```yaml
spread.default = 0.65                    # mean stratum A terukur
spread.by_year = {2023: 0.51, 2024: 0.70, 2025: 0.67, 2026: 0.62}
spread.warn_multiplier  = 3.0             # 0.51 x 3 = 1.53 -> p99 2023 = 8.50 -> ERROR
spread.error_multiplier = 8.0
```

Konsekuensi yang disengaja: validator menandai **2023 sebagai ERROR**, karena
`spread.default` dipakai sebagai baseline pembanding untuk data **seluruh** tahun —
termasuk stratum B yang p99-nya memang 8,50. Ini bukan regresi data.

> **Sisa pekerjaan yang masih terbuka:** `configs/broker.yaml` menyimpan angka
> spread terukur, tapi **belum ada kode yang membacanya** — `check_spread` masih
> memakai `configs/data.yaml`. Klaim "satu-satunya sumber otoritas" di
> `broker.yaml` belum benar secara teknis sampai kedua file itu disatukan.
> Angka keduanya sekarang sudah identik, jadi tidak ada risiko disagreement
> sementara — tapi duplikasi ini masih rapuh.

---

## Relasi

- Kontrak ini dipakai EDA-02 sebagai sumber angka spread, dan akan dipakai
  skenario biaya di EDA-06 ke depan.
- Angka spread di sini **sama** dengan `configs/data.yaml` →
  `spread.cost_basis` / `spread.stress_bands`. Kalau suatu saat berbeda,
  jalankan ulang audit dan perbarui **dua** file sekaligus.
- Semua baris `[TERUKUR]` bisa direproduksi ulang dari parquet — kalau data
  berubah, hitung ulang, jangan diedit manual.
