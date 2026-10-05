# RULES.md — Panduan Kode & Trading Proyek USDJPY Bot

> Ini panduan, bukan kitab suci.
> Aturan dibagi 3 tingkat:
>   - WAJIB       : tidak boleh dilanggar
>   - DIANJURKAN  : ikuti default ini, kecuali ada alasan kuat
>   - BOLEH       : boleh dilanggar dengan `# EXCEPTION: <alasan>`
>
> Untuk aturan perilaku AI, lihat `.ai/AGENTS.md`.
>
> Versi: 2.0
> Update: 2026-10-05
> Proyek: USDJPY Trading Bot

---

## TL;DR — Baca Ini Dulu

Kalau cuma ingat 25 hal:

### Kode (WAJIB)
1. Type hints di semua fungsi publik.
2. Docstring gaya Google di fungsi/class publik.
3. Config di `configs/`, jangan hardcode.
4. `logging`, bukan `print()`.
5. `except: pass` DILARANG.
6. `pathlib` untuk path, bukan string.
7. UTC untuk waktu, bukan local.

### Kode (DIANJURKAN)
8. File <400 baris, fungsi <50 baris, CC <10 (soft).
9. Format: Black line-length 100, Ruff.
10. Naming: snake_case, PascalCase, UPPER_SNAKE.

### Test & Git
11. Test tidak boleh hit API live. Deterministik, cepat.
12. Commit format: `type(scope): pesan`. Jangan commit `.env`.

### Trading (PALING PENTING)
13. Anti look-ahead bias dan anti data leakage — dosa besar.
14. SL berbasis ATR (1,5-3 × ATR), bukan angka tetap.
15. Lot minimum selalu (0.01). Tidak ada risk % per trade.
16. BID/ASK WAJIB BENAR (§18.16):
    - BUY: entry ask, exit bid.
    - SELL: entry bid, exit ask.
    - Spread dari config, per sesi.

### Trading (Framework)
17. Limit HANYA di live. Demo/training BEBAS.
18. Daily limit = Lot × 500. Guard akun <$50: 25% cap.
19. No martingale. No grid tanpa SL. No averaging down.
20. 3 SL beruntun → pause 1 jam, review, lanjut.
21. Backtest WAJIB pakai spread + slippage + komisi.
22. Walk-forward, bukan random split.

### Jurnal & Backtest
23. Jurnal rotasi per bulan (`journal/trades/YYYY-MM.csv`).
24. Backtest folder per tanggal (`reports/backtest/YYYY-MM-DD/NN_nama/`).
25. Baca jurnal: INDEX dulu, bukan CSV mentah.

### Filosofi
> Tegas di yang penting. Longgar di yang tidak.
> Edge > Limit. Tapi kill switch tetap ada.

---

## DAFTAR ISI

- §1  Bahasa & Versi
- §2  Format Kode
- §3  Penamaan
- §4  Struktur File
- §5  Type Hints
- §6  Docstring
- §7  Import
- §8  Error Handling
- §9  Logging
- §10 Config
- §11 Testing
- §12 Git & Commit
- §13 Dependency
- §14 Angka & Konstanta
- §15 Timezone & Waktu
- §16 Path & File
- §17 Data, Format, Jurnal & Backtest
- §18 Aturan Trading (PENTING)
- §19 Ringkasan WAJIB vs DIANJURKAN
- §20 Filosofi
- §21 Checklist Sebelum Commit
- §22 Referensi

---

## §1. BAHASA & VERSI

**WAJIB:**
- Python 3.11+.
- Encoding UTF-8.
- Line ending LF.

**DIANJURKAN:**
- Fitur modern Python 3.11.
- `from __future__ import annotations` di file baru.

---

## §2. FORMAT KODE

**DIANJURKAN:**
- Black `line-length = 100`.
- Ruff.
- Indentasi 4 spasi.
- Double quote.
- Trailing comma di multi-line.
- 2 blank line antar fungsi top-level.

**BOLEH DILANGGAR:**
- Line >100 kalau tidak bisa dipecah (URL, string). `# EXCEPTION:` kalau >120.
- Format manual kalau Black bikin jelek.

---

## §3. PENAMAAN

| Elemen | Gaya |
|---|---|
| Variabel | snake_case |
| Fungsi | snake_case |
| Konstanta | UPPER_SNAKE |
| Class | PascalCase |
| Private | _prefix |
| File | snake_case |
| Test file | test_<module>.py |
| Test function | test_<fungsi>_<skenario> |

BOLEH: variabel loop `i`, `x` kalau jelas konteksnya.
Yang penting: nama **jelas**, bukan singkatan misterius.

---

## §4. STRUKTUR FILE

Urutan:
1. Module docstring.
2. `from __future__ import annotations`.
3. Standard library.
4. Third-party.
5. Local.
6. Konstanta.
7. Logger.
8. Class.
9. Fungsi.
10. `if __name__ == "__main__":` (kalau perlu).

File: **DIANJURKAN** <400 baris.
**BOLEH** lebih dengan `# EXCEPTION:`.

---

## §5. TYPE HINTS

**WAJIB:** fungsi publik, method publik, parameter, return.

**Tidak wajib:** variabel lokal, lambda, helper pendek.

```python
def process(prices: pd.Series, window: int = 20) -> pd.Series:
    ...
§6. DOCSTRING
WAJIB: fungsi publik, class publik, module.

DIANJURKAN: Google Style, Bahasa Inggris.
def calculate_sharpe(returns: pd.Series, risk_free: float = 0.0) -> float:
    """Hitung Sharpe ratio.

    Args:
        returns: Series return harian.
        risk_free: Risk-free rate tahunan.

    Returns:
        Sharpe ratio tahunan.

    Raises:
        ValueError: Kalau returns kosong.
    """
Hindari docstring yang cuma ulang nama fungsi.

§7. IMPORT
Urutan: stdlib → third-party → local. Dipisah blank line.

DILARANG: from x import *, import tidak dipakai, relative import.

BOLEH: import di dalam fungsi kalau circular dependency.

§8. ERROR HANDLING
WAJIB: tangkap error spesifik, log, raise ulang.
DILARANG: except: pass, bare except.
try:
    df = fetch_rates(...)
except ConnectionError as e:
    logger.error("Gagal connect: %s", e)
    raise
return None hanya untuk flow normal, bukan menutupi error.

§9. LOGGING
WAJIB: logging, bukan print(). DILARANG log password/token.
DIANJURKAN: lazy formatting logger.info("x=%d", x).

Level: DEBUG, INFO, WARNING, ERROR, CRITICAL.

Setup di configs/logging.yaml.

§10. CONFIG
WAJIB: semua parameter di configs/ (YAML). Tidak hardcode.
from src.utils.config import load_config
config = load_config("data")
symbol = config["mt5"]["symbol"]
Pengecualian: konstanta universal (PI), default value.

§11. TESTING
DIANJURKAN: minimal 3 test per fungsi publik (happy, edge, error).

WAJIB:

Test tidak hit API live.

Deterministik.

Cepat (<5 detik).

Coverage target: >70%.

§12. GIT & COMMIT
Format: type(scope): pesan singkat.
Type: feat, fix, docs, test, chore, refactor, perf, style.

Jangan commit: .env, secrets/, data/raw/, models/, logs/.

§13. DEPENDENCY
WAJIB: tambah dengan izin, pin versi, update CHANGELOG.

Rekomendasi:

Data: pandas, numpy, pyarrow

ML: torch, scikit-learn

Config: pyyaml, python-dotenv

Test: pytest, pytest-cov

Format: black, ruff

MT5: MetaTrader5

Backtest: belum diputuskan

§14. ANGKA & KONSTANTA
Angka penting → konstanta bernama atau config.

BOLEH langsung: loop counter, matematika jelas, indeks array.

§15. TIMEZONE & WAKTU
WAJIB: internal UTC, simpan dengan tzinfo.
DILARANG: datetime.now() tanpa timezone.

Khusus MT5: timezone broker (GMT+2/GMT+3). Konversi ke UTC.
Config: configs/data.yaml → broker_timezone.

§16. PATH & FILE
WAJIB: pathlib, bukan string. Tidak hardcode absolute path.
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
§17. DATA, FORMAT, JURNAL & BACKTEST
§17.1 Format Data
Tahap	Format
Raw	CSV
Processed	Parquet
Features	Parquet
Labels	Parquet
Model	PyTorch
Log	JSON Lines
WAJIB:

Data mentah immutable.

Data besar jangan di Git.

Backup sebelum hapus.

Nama file: <symbol>_<tf>_<tahun>.parquet.
Contoh: usdjpy_m1_2026.parquet.

§17.2 Struktur Jurnal

journal/
├── INDEX.md              # peta + ringkasan
├── trades/
│   ├── 2026-10.csv       # trade per bulan
│   └── 2026-11.csv
├── daily/
│   ├── 2026-10-05.md     # ringkasan harian
│   └── 2026-10-06.md
├── monthly/
│   ├── 2026-10.md        # ringkasan bulanan
│   └── 2026-11.md
├── decision_log.md       # keputusan besar
└── experiment_log.md     # eksperimen model
WAJIB:

CSV rotate per bulan (otomatis oleh bot).

Daily dibuat setiap hari kerja.

Monthly dibuat di awal bulan.

INDEX.md selalu diupdate.

Baca jurnal: INDEX → monthly → daily (3 hari). JANGAN CSV mentah.

Kolom wajib di journal/trades/*.csv:

trade_id, open_time, close_time, pair, direction

entry_price, exit_price, sl, tp, lot

bid_entry, ask_entry, bid_exit, ask_exit

spread_at_entry, spread_at_exit

pips_result, pnl_usd

fingerprint_entry, fingerprint_exit

condition_entry, condition_exit (JSON)

signal_source, confidence

strategy, mode (learning/discovery/live)

emotion, lesson

§17.3 Struktur Backtest
Setiap backtest WAJIB di folder:
reports/backtest/YYYY-MM-DD/NN_<nama>/

Isi:

config.yaml — parameter backtest

result.json — metrik (Sharpe, DD, WR, PF)

trades.csv — detail trade

equity_curve.png — grafik

report.md — laporan (Template Audit §18 AGENTS.md)

WAJIB:

INDEX.md di setiap folder tanggal.

Nomor urut 01, 02, dst.

Simpan semua, termasuk yang gagal.

DILARANG:

Campur file backtest di satu folder.

Timpa hasil lama.

Nama folder tanpa nomor urut.

§18. ATURAN TRADING (PENTING)
§18.1 Prinsip Umum
Risk per trade: TIDAK ADA (lot minimum).

SL: berbasis ATR.

Kontrol risiko: daily loss limit $.

Limit HANYA live. Demo bebas.

Limit trade: TIDAK ADA.

Anti-martingale: WAJIB.

§18.2 Tiga Fase
Fase 1 — Training (Demo Bebas) — SEDANG DIJALANI

Tujuan: 500+ trade data.

Lot 0.01.

No daily/weekly/kill switch/limit trade.

Semua sesi & TF.

Kriteria pindah: 500+ trade.

Fase 2 — Graduation (Demo Limit Simulasi)

Daily limit simulasi $5 (lot 0.01).

100 trade.

Lulus kalau <30% hari kena limit.

Fase 3 — Live

Daily limit hard stop.

Kill switch aktif.

§18.3 Daily Loss Limit (LIVE)
Lot	Daily	Weekly
0.01	$5	$15
0.02	$10	$30
0.03	$15	$45
0.05	$25	$75
0.10	$50	$150
Rumus: Daily = Lot × 500.

Guard akun <$50: daily = min(Lot × 500, 25% akun).

§18.4 SL (SEMUA MODE)
ATR(14) di TF entry.

SL = 1,5 × ATR (default).

Min 1,5 × ATR. Max 3 × ATR.

Buffer di swing high/low.

DILARANG SL < 1,5 × ATR (rawan SL hunt).

§18.5 TP
Min 1:1,5 (Asia).

Min 1:2 (London/NY).

Boleh trailing stop.

§18.6 Trigger Evaluasi (SEMUA MODE)
3 SL beruntun → pause 1 jam, review, lanjut.

5 SL beruntun → kurangi lot 50%, review total.

3 SL beruntun dengan total >50% daily limit → pause.

Yang dicek: noise vs struktur, regime, sinyal, news.

§18.7 Kill Switch (LIVE)
Daily loss → limit: STOP.

Weekly loss → limit: STOP.

DD peak >25% → lot 50%.

DD peak >40% → STOP review.

§18.8 Limit Trade
TIDAK ADA limit trade. Yang dibatasi: total $ loss/hari (live).

§18.9 Sesi
Semua sesi valid. USDJPY aktif Tokyo, London, NY.
Spread lebar Tokyo awal (tunggu 08:00 JST).
Tokyo fix 09:55 JST = volatilitas.

§18.10 Look-Ahead Bias (WAJIB)
DILARANG fitur di t pakai data t+1. Pakai .shift(1).

§18.11 Data Leakage (WAJIB)
Scaling hanya di train. Split temporal, bukan random.

§18.12 Walk-Forward (WAJIB)
Wajib untuk validasi time series.

§18.13 Biaya Transaksi (WAJIB)
Semua backtest WAJIB: spread + komisi + slippage.
Backtest tanpa biaya = TIDAK VALID.

§18.14 Intervensi BoJ
Hati-hati di zona 150/155/160.
Flag intervention_zone di fitur.
Pause saat spread melebar ekstrem.

§18.15 Yang DILARANG (SEMUA MODE)
Martingale.

Grid tanpa SL.

Averaging down tanpa rencana.

Trading saat spread ekstrem (>3× normal).

Trading saat news high impact tanpa proteksi.

Melanjutkan setelah kill switch aktif.

§18.16 BID/ASK HANDLING (WAJIB)
Aturan Emas
BUY: entry di ASK, exit di BID.

SELL: entry di BID, exit di ASK.

DILARANG pakai harga yang sama untuk entry & exit.

Di Backtest
Data OHLC MT5 = BID.

BUY entry: ask = close + spread.

BUY exit: bid = close.

SELL entry: bid = close.

SELL exit: ask = close + spread.

Spread
TIDAK konstan.

Lebar di: news, Tokyo awal, Jumat malam.

Config: configs/data.yaml → spread.

Di Live
Ambil bid & ask real-time dari MT5.

Log spread setiap trade di jurnal.

Yang DILARANG
Pakai harga tengah (mid) untuk entry/exit.

Asumsi spread = 0.

Pakai spread konstan di semua sesi.

Backtest tanpa spread.

Lupa konversi bid→ask untuk BUY entry.

Checklist Backtest
□ BUY entry pakai ask.
□ BUY exit pakai bid.
□ SELL entry pakai bid.
□ SELL exit pakai ask.
□ Spread dari config (per sesi/TF).
□ Spread naik di news (stress test).
□ Jurnal mencatat spread setiap trade.
§19. RINGKASAN WAJIB vs DIANJURKAN
WAJIB
Kode:

Python 3.11+.

Type hints di fungsi publik.

Docstring di fungsi/class publik.

logging, bukan print().

Tangkap error spesifik.

Config di configs/.

Tidak hardcode API key/path.

pathlib untuk path.

UTC untuk waktu.

Test tidak hit API live.

Tidak commit .env.

Trading:

Anti look-ahead bias.

Anti data leakage.

Walk-forward.

Biaya transaksi di backtest.

Anti-martingale.

SL berbasis ATR.

Bid/ask handling benar (§18.16).

Kill switch ada (live).

Limit hanya di live.

Jurnal & Backtest:

Rotasi CSV per bulan.

Backtest folder per tanggal + nomor urut.

Update INDEX.md.

DIANJURKAN
Black + Ruff, line 100.

File <400, fungsi <50, CC <10.

Naming conventions.

Docstring Inggris.

Min 3 test per fungsi.

Commit type(scope):.

Parquet untuk processed.

BOLEH (dengan # EXCEPTION:)
Line >100.

File >400.

Fungsi >50 (linear).

Naming singkat kalau jelas.

§20. FILOSOFI
Aturan ini untuk membantu, bukan mengikat.
Kalau menghambat cara wajar, boleh dilanggar dengan alasan.
Yang penting: jangan langgar WAJIB.

Tegas di yang penting. Longgar di yang tidak.

Untuk trading:

Edge > Limit. Evaluasi > Stop.
Kill switch hanya untuk bencana.

§21. CHECKLIST SEBELUM COMMIT
□ Black dijalankan.
□ Ruff bersih.
□ Test passed.
□ Type hints lengkap.
□ Docstring lengkap.
□ Tidak ada hardcode.
□ Tidak ada print().
□ Tidak ada except: pass.
□ Tidak ada look-ahead bias.
□ Tidak ada data leakage.
□ Bid/ask handling benar (§18.16).
□ Import rapi.
□ Tidak commit .env / secrets.
Kalau ada yang tidak bisa dicentang, jelaskan alasannya.

§22. REFERENSI
.ai/AGENTS.md — aturan perilaku AI

.ai/CONTEXT.md — konteks proyek

.ai/PROMPTS.md — prompt siap pakai

.ai/STATE.md, TASKS.md, PROGRESS.md, SESSION_LOG.md

docs/PROJECT_MAP.md

pyproject.toml, requirements.txt

Akhir RULES.md v2.0
