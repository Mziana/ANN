# PROJECT_MAP.md — Peta Proyek USDJPY Bot

> Peta untuk AI agent dan manusia. Isi file ini **harus sesuai kenyataan**, bukan rencana.
> Kalau bedakan dengan kenyataan, blinks quickly update file ini.
>
> Update: 2026-10-05
> Detail aturan: `.ai/AGENTS.md`, `.ai/RULES.md`

---

## 1. Proyek dalam 3 Kalimat

Bot trading **USDJPY scalping M1–M15**, pendekatan hybrid **ANN + rule-based**.
Timeframe tersimpan: **7** (M1, M5, M15, M30, H1, H4, D1).
Data dari **MT5 broker Finex**, disimpan lokal, diproses sendiri.
Filosofi: *data dulu, tebakan nanti* — edge dibangun dari bukti, bukan opini.

---

## 2. Di Mana Harus Menulis

| Kalau mau bikin... | Taruh di | Aturan |
|---|---|---|
| Ambil / bersihkan data MT5 | `src/data/` | Raw immutable, CSV; processed Parquet |
| Hitung fitur & label | `src/features/` | Anti look-ahead: pakai `.shift(1)` |
| Model (baseline & ANN) | `src/models/` | Walk-forward, bukan random split |
| Backtest & audit | `src/backtest/` | Biaya transaksi WAJIB |
| Order & eksekusi | `src/execution/` | Bid/ask benar |
| SL/TP, sizing, kill switch | `src/risk/` | SL berbasis ATR |
| Indikator & sinyal | `src/signals/` | — |
| Strategy spesifik | `strategies/<nama>/` | — |
| Riset interaktif | `notebooks/<nama>/` | Eksplorasi, bukan logika produksi |
| Test | `tests/` | `test_<module>.py`, tanpa API live |
| Parameter | `configs/*.yaml` | **Tidak hardcode** |
| Config loader | `src/utils/config.py` | **Belum ada** — buat saat perlu |
| Jurnal trade | `journal/` | Rotasi bulanan |
| Hasil backtest | `reports/backtest/YYYY-MM-DD/NN_nama/` | Simpan semua, termasuk gagal |

---

## 3. Modul yang Sudah Ada

Hanya dua. Everything else belum ditulis.

| File | Fungsi |
|---|---|
| `scripts/verify_claims.py` | Cek file aturan ada, modul import, test lulus |
| `scripts/check_state.py` | Gate pre-commit: STATE.md hari ini |
| `main.py` | **Kosong** (placeholder) |
| `src/__init__.py` | **Kosong** (0 byte) |

### Modul yang DIBUTUHKAN `pipeline.ps1` tapi belum ada

```
src/data/fetch_data.py       src/features/build_features.py
src/data/clean_data.py       src/features/build_labels.py
src/data/validate_data.py    src/models/baseline.py
src/data/resample.py         src/models/train_ann.py
src/backtest/backtest.py     src/backtest/audit.py
```

> Subpackage `src/*/` sudah ada tapi **kosong dan tanpa `__init__.py`**.

---

## 4. Konvensi Kode

| Aturan | Nilai |
|---|---|
| Python | 3.11+ (venv sekarang 3.12.8) |
| Format | **Ruff saja** — Black sudah dihapus 2026-10-05 |
| Line length | 100 |
| Type hints | WAJIB di fungsi publik |
| Docstring | Google style, **bahasa Inggris** |
| Encoding | UTF-8 **tanpa BOM**, line ending **LF** |
| Windows script | `.ps1` / `.bat` pakai CRLF (lihat `.gitattributes`) |
| Logging | `logging`, bukan `print()` — kecuali script CLI yang outputnya memang laporan |
| Path | `pathlib`, bukan string |
| Waktu | UTC dengan `tzinfo` |
| Ukuran | file <400 baris, fungsi <50 baris |
| Konstan | Bernama atau di config, bukan magic number |

---

## 5. Jebakan yang Sudah Terverifikasi

**1. Timestamp MT5 = waktu broker, BUKAN UTC.**
Offset terukur **+3 jam** (`Etc/GMT-3`). Timestamp `copy_rates*` harus
dikonversi. Offset **historis belum terverifikasi** — simpan timestamp mentah,
jangan buang.

**2. Data OHLC MT5 = BID, bukan ask.**
BUY: entry di ask (`close + spread`), exit di bid.
SELL: entry di bid, exit di ask (`close + spread`).
Harga tengah (mid) dilarang untuk entry maupun exit.

**3. Backtest tanpa spread/slippage/komisi = TIDAK VALID.**

**4. Simbol bukan `USDJPYm`.** Sudah dicek: hanya ada `USDJPY`.

---

## 6. Gate Sebelum Commit

```bash
venv/Scripts/ruff.exe check scripts/ src/ main.py
venv/Scripts/ruff.exe format --check scripts/ src/ main.py
venv/Scripts/python.exe scripts/check_state.py
venv/Scripts/python.exe scripts/verify_claims.py
```

Hook yang sama sudah terpasang di `.pre-commit-config.yaml`.

---

## 7. Folder Referensi

| Folder | Isi | Status |
|---|---|---|
| `.ai/` | Aturan AI + state file | Lengkap |
| `configs/` | Parameter YAML | Lengkap |
| `checkpoints/` | Script generator setup | **gitignored**, arsip |
| `src/` | Kode utama | **Kosong** |
| `tests/` | Test | **Kosong** |
| `docs/` | Dokumentasi | File ini saja |
| `data/` | `raw`/`processed`/`features`/`labels` × 7 TF (M1-M30, H1-H4, D1) | Hanya `.gitkeep` |
| `journal/` | Jurnal trading | Struktur siap, kosong |
| `reports/` | Hasil backtest | Struktur siap, kosong |
| `models/` | Model tersimpan | Kosong |
| `scripts/` | CLI & setup | 2 script Python + 3 PowerShell |
| `strategies/` | Per strategi | Kosong |
| `notebooks/` | Riset | Kosong |
| `bot/`, `dashboard/`, `archive/`, `secrets/` | Cadangan | `.gitkeep` |
| `venv/` | Environment | 134 paket, siap |

---

## 8. Alur Kerja

```
Pipeline PowerShell (scripts/run.ps1)
   -> src/data/fetch_data.py    MT5 -> data/raw/M1/usdjpy_m1_<year>.csv
   -> src/data/validate_data.py cek gap, baris, timezone
   -> src/data/clean_data.py    raw -> data/processed/ (Parquet)
   -> src/features/             fitur & label
   -> src/models/               baseline lalu ANN
   -> src/backtest/             backtest + audit 8 section
   -> src/execution/ + src/risk/  (fase paper/live)
```

Semua modul di atas **belum ada**. Yang pertama adalah `fetch_data.py`.

---

## 9. Urutan Prioritas

1. `fetch_data.py` — tanpa data, tidak ada yang bisa diuji
2. `validate_data.py` — data kotor lebih buruk daripada tidak ada
3. EDA — **pilih metode setelah EDA, jangan lebih dulu**
4. Baseline rule-based
5. ANN
6. Backtest + audit

---

## 10. Referensi

| File | Isi |
|---|---|
| `.ai/AGENTS.md` | Kontrak kerja AI agent (§24 = onboarding) |
| `.ai/RULES.md` | Aturan kode + trading (§18.16 = bid/ask) |
| `.ai/CONTEXT.md` | Memori jangka panjang proyek |
| `.ai/STATE.md` | Status saat ini |
| `.ai/TASKS.md` | Task board |
| `.ai/SESSION_LOG.md` | Log setiap sesi |
| `configs/data.yaml` | Parameter data, spread, timezone broker |
| `configs/logging.yaml` | Setup logging |
| `configs/paths.yaml` | Lokasi folder |

---

**Akhir PROJECT_MAP.md**
