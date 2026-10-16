# ARSIP — EDA-06 & EDA-07 (dipensiunkan)

> **Status: `SUPERSEDED` — tidak boleh dijalankan ulang untuk menghasilkan hasil baru.**
> Diarsipkan pada 2026-10-14. Isi folder ini dibekukan sebagai rekam jejak.

## Konvensi penomoran (2026-10-15)

Nomor EDA dipakai ulang berurutan — seri lama di folder ini dianggap **tidak ada**.
Ronde baru memakai nama deskriptif agar tidak tertukar dengan file arsip
(contoh: `eda_06_candle_anatomy_regime`, `eda_07_spike_anatomy_outcome`).
Auditor: acuan aktif = file di `notebooks/scalping/` + generator
`scripts/_build_eda*.py`, bukan folder arsip ini.

---

## Isi folder

| File | Asal |
|---|---|
| `eda_06_biaya_breakeven.ipynb` | EDA-06 — gerbang biaya + breakeven |
| `eda_07_label_fitur.ipynb` | EDA-07 — label & fitur (run 9) |
| `eda_07_i1_adendum.ipynb` | EDA-07 I-1 adendum |
| `eda_07_i2.ipynb` | EDA-07 I-2 penyelesaian |
| `eda_07_l30_arah.ipynb` | L3-0 — peta arah |
| `eda_07_l31_baseline.ipynb` | L3-1 — baseline vs null |

Generator notebook ada di `scripts/archive/eda-06-07/`.
Output dan laporan ada di `reports/eda/2026-10-10/`, `2026-10-12/`,
dan `reports/governance/2026-10-09/`, `2026-10-10/`, `2026-10-12/`.

Semua file tetap ada. **Tidak ada yang dihapus** — supaya jejaknya bisa diaudit.

---

## Kenapa dipensiunkan

Empat cacat. Satu di antaranya bug kode yang tidak pernah terdeteksi.

### 1. EDA-06 memasang pertanyaan yang salah

> §1: "apakah ada kombinasi sesi × horizon/barrier di mana **ruang gerak cukup besar
> dibanding biaya**"

Itu **go/no-go gate untuk melanjutkan pencarian strategi**, bukan deskripsi. Rancangan
sendiri sudah mengatakannya (§Metode barrier):

> "Entri tanpa sinyal setiap 5 bar M1, buy dan sell digabung (arah acak).
> Ini laju dasar, **bukan strategi**."

Hasilnya `23/144` irisan tercile + `7/48` irisan sesi **LOLOS** — dan itu jadi corong
untuk semua tahap berikutnya. Padahal yang terukur cuma *tinggi hurdle*, bukan
*keberadaan sinyal*. `E_normal` negatif di **seluruh** sel (−0,55 s/d −1,46): tanpa
sinyal, semuanya rugi.

### 2. EDA-07 menemukan fitur yang **tautologis**

Dari 98 target yang LOLOS (`T-L3-0_peta98.csv`):

| Jenis fitur | Jumlah |
|---|---|
| **Volatilitas** (`rv60` 48, `rv15` 15, `atr_m5` 11) | **74** |
| Aksi-harga (`ema*_d_atr`, `ret_5`, `ret_15`, `m15_pos`) | 15 |
| Jam / kalender | 6 |
| Jarak ke open | 3 |

Label-nya `LA` / `LB_bin` = **barrier-hit**, dan barrier didefinisikan dalam **satuan ATR**.
Jadi `atr_m5` memprediksi "barrier kena" hampir otomatis: volatilitas tinggi = barrier
ATR-unit lebih mudah disentuh. Itu aritmetika, bukan prediksi.

Rancangan EDA-06/07 sendiri sudah menyiratkannya di baris 99:

> "Target ini sesuai temuan EDA bahwa **besaran gerak lebih terprediksi daripada arah**."

R1–R6 lalu mencoba menarik **arah** dari prediktor **besaran** — dan hasilnya 0/9 sel
positif di R4.

### 3. 🐛 Gate G4 mustahil lolos (bug satuan)

Di `eda_07_label_fitur.ipynb` sel 14 baris 174:

```python
ev["g4"] = bool(ev.get("liftN", -9) >= d_n and ev["liftS"] >= G4_STRESS_MIN_PP)
```

| Nilai | Sumber | Satuan |
|---|---|---|
| `liftN` = `w["top"] − r["base"]` | selisih dua probabilitas | **fraksi** (−0,065 … +0,084) |
| `d_n` = `delta_pp_normal` | EDA-06 | **persen poin** (0,97 … 20,62) |

`0,084 ≥ 0,974` → **selalu False**. G4 tidak pernah bisa lolos, apa pun datanya.

Hasil: **G4 = False untuk seluruh 153 baris yang lolos G3.**

Dua konsekuensi:

- Rancangan baris 129: *"Gagal G2 atau G4: **berhenti dan rumuskan ulang target;
  jangan lanjut ke baseline**"* — sinyal stop dipancarkan, lalu **diabaikan**.
- Gate-nya sendiri salah. Kalau satuannya dibetulkan (`liftN × 100`),
  **103 dari 307** baris LA akan LOLOS — arah kesalahannya **terbalik**.

### 4. L3-1 memakai null yang terlalu lemah

`T-L3-1_baseline.csv`:

| | nilai |
|---|---|
| null model | `mayoritas-global` (67), `mean-global` (36) |
| baseline | `marginal-per-iris` (67), `mean-per-iris` (36) |
| vonis | **68 LOLOS** / 35 GUGUR |

Model yang **tahu bucket** dibandingkan dengan null yang **buta bucket** → LOLOS
hampir dijamin oleh konstruksi. Baris GUGUR menunjukkan pola klasik:
`lolos_a=True`, `menang_h1=True`, `menang_h2=False` — in-sample lolos, out-of-sample gagal.

---

## Yang sebenarnya bisa diselamatkan

- **EDA-01…05 tidak salah.** Lihat `../EDA/`.
- Temuan negatifnya **tidak** perlu diulang.
- EDA-06 mengukur `delta` dengan benar; masalahnya hanya **cara memakainya** sebagai
  gerbang, bukan angkanya. Angka `delta_pp_normal` masih valid sebagai referensi.

---

## Pelajaran

1. **`LOLOS` selalu berarti "layak dicek", tidak pernah berarti "ada edge".** Tapi di
   rantai ini, `LOLOS` diperlakukan sebagai izin melanjutkan. Itu akar masalahnya.
2. **Arah ≠ besaran.** "Volatilitas bisa diprediksi" tidak mengizinkan
   "harga bisa diprediksi arahnya".
3. **Gate yang selalu gagal sama dengan tidak adanya dengan gate yang tidak ada.** Kalau sebuah
   gate menolak 100% kandidat, itu bug — bukan bukti.
4. **Cek satuan saat membandingkan dua angka dari sumber berbeda.** Satu baris kode
   sudah mengembalikan seluruh tahap.
5. **Uji dengan fitur kontrol.** Kalau fitur derau acak juga "lolos", lantainya salah.
6. **Hasil negatif EDA adalah untuk dihormati, bukan dilewati.** Tiga temuan negatif
   (ACF ≈ 0, level ≈ placebo, komposisi hari ≈ sama) sudah mengarah ke jawaban yang
   sama. R1–R6 menghabiskan banyak waktu untuk sampai ke sana.

---

## Kalau nanti perlu menghidupkan ulang

Jangan. Rancang ulang dari EDA-05 dengan pertanyaan yang benar — lihat
`../EDA/README.md` bagian "Nasihat untuk EDA-06 ke depan" di setiap halaman.
