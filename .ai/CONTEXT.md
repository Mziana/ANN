# CONTEXT.md â€” Konteks Proyek USDJPY Bot

> Memori jangka panjang AI agent.
> Update saat ada perubahan besar (bukan setiap sesi).
>
> Versi: 1.4
> Update: 2026-10-13
> Proyek: USDJPY Trading Bot

> **PENTING (2026-10-13).** Section §4 "Fase Proyek" dan §5 "Strategi" di
> bawah memakai bahasa fase LAMA (Training/Graduation/Live). Itu fase
> **Trading**, bukan fase **Riset** — keduanya beda. Posisi riset terkini
> yang otoritatif ada di `.ai/STATE.md` bagian atas + `.ai/PROGRESS.md`.
> Ringkas: EDA selesai 2026-10-12, vonis arsitek GO untuk lanjut ke spec
> pemodelan pra-registrasi (bukan paper-trade), dan spec itu **menunggu
> persetujuan user**. Fase Training (§4) belum dimulai sama sekali.

---

## TL;DR â€” Baca Ini Dulu

Kalau cuma ingat 12 hal:

### Proyek
1. Tujuan: bot USDJPY scalping (M1-M15) berbasis ANN + rule-based.
2. Stack: Python 3.11, PyTorch, MT5 Finex, pandas, YAML.
3. Fase: **Riset — Milestone 3 (Metode)**, blokir menunggu persetujuan user.
   Fase Trading (Training/Graduation/Live di §4) BELUM dimulai.

### Trading
4. Lot selalu minimum (0.01). Tidak ada risk %.
5. SL berbasis ATR (1,5-3 x ATR).
6. Limit HANYA live. Demo bebas.
7. Bid/ask wajib benar (RULES.md Â§18.16).
8. No martingale.

### Workflow
9. Multi-AI: Coder, Auditor, Architect.
10. Jurnal rotasi per bulan. Backtest folder per tanggal.

### Prinsip
11. Data dulu, tebakan nanti. Uji dulu, simpulkan kemudian.
12. Jangan andalkan memori AI. Andalkan file.

---

## 1. Tujuan Proyek

Bot USDJPY berbasis ANN + rule-based hybrid, scalping M1-M15.

Tujuan akhir:
- Profit konsisten, drawdown terkendali.
- Berbasis data, bukan tebakan.
- Bisa di-audit dan di-maintain.

Bukan tujuan:
- Get rich quick.
- Martingale.
- Bot tanpa pengawasan.
- Live sebelum edge terbukti.

---

## 2. Stack

| Komponen | Pilihan |
|---|---|
| Bahasa | Python 3.11+ |
| Data | pandas, numpy, pyarrow |
| ML | PyTorch |
| Backtest | Belum diputuskan (vectorbt / backtrader) |
| Broker | MT5 (Finex) |
| Config | YAML |
| Logging | standard logging |
| Test | pytest |
| Format | Ruff (Black dihapus 2026-10-05) |
| Editor | VS Code + AI coding |
| OS | Windows |
| Shell | PowerShell |
| Data | 4 tahun (2023-2026), 1.347.847 bar M1 |
| GitHub | **AKTIF** — `github.com/Mziana/ANN`, branch `main` (push pertama 2026-10-13) |

---

## 3. AI Tools & Workflow

### Tools
- Freebuff - AI coder utama (1 profil).
- Hermes Agent - multi-profile (2-5 AI), fitur grup AI.
- DeepSeek V4 - model backend.
- Bisa browse internet (harus dipaksa).
- Bisa baca link GitHub.

### Peran Multi-AI

Coder (Freebuff/Hermes):
- Implementasi, self-audit, fix, update state.

Auditor (model beda):
- Audit adversarial, cari bug/bias, laporan temuan.
- DILARANG nulis kode.

Architect (model terbaik):
- Rancang, putuskan konflik.
- DILARANG implementasi.

### Kapan Pakai Berapa AI

| Fase | AI |
|---|---|
| Fondasi | 1 (Coder) |
| Data | 1-2 |
| EDA | 1 |
| Metode | 2 |
| Model | 2-3 |
| Backtest | 3 |
| Paper | 1-2 |
| Graduation | 2 |
| Live review | 3 |

Saat ini: Fase Fondasi -> Data, cukup 1 AI (Freebuff).

---

## 4. Fase Proyek

Fase Trading saat ini: **BELUM DIMULAI**. §4 ini hanya rencana, bukan status
aktif. Untuk status riset yang sebenarnya, baca `.ai/PROGRESS.md`.

Status Riset (per 2026-10-13): Milestone 1 (Data) dan 2 (EDA) selesai.
Milestone 3 (Metode) sedang berjalan dan **terblokir** di persetujuan user
untuk spec Discovery-R1. Milestone 4-9 belum mulai.

### Fase 1 - Training (Demo Bebas)
- 500+ trade data.
- Lot 0.01.
- No daily/weekly/kill switch/limit trade.
- Semua sesi & TF.
- Anti-martingale WAJIB.

### Fase 2 - Graduation
- Daily limit simulasi $5.
- 100 trade.
- Lulus kalau <30% hari kena limit.

### Fase 3 - Live
- Daily limit hard stop.
- Kill switch aktif.

---

## 5. Strategi

Fokus: Scalping M1-M15, USDJPY saja.
Pendekatan: Hybrid (ANN + rule-based).

Status metode: **MASIH BELUM DITENTUKAN** — dan ini disengaja.
Dasar pilihan sudah pindah dari EDA ke dokumen desain event-first
(`.ai/backup/2026-10-09_DESAIN_FRESH_SCALPING_EVENT_FIRST.md`): tiga keluarga
event E1 (balik)/E2 (pullback)/E3 (kompresi), 7 gerbang G1-G7, jalur
P0 (putar ulang data lama) -> P1 (bayangan real-time) -> P2 (paper 0,01 lot).
Empat keputusan §18 dokumen itu masih menunggu persetujuan user.

Belum diputuskan:
- Library backtest.
- Arsitektur ANN.
- TF utama.
- Sesi prioritas.
- Metode sinyal (EMA, SMC, Fibo, dll).
- Spread: angka mana yang otoritatif (§8.3) — 2,3x selisih belum|datumai.

---

## 6. Risk Framework

- Broker: Finex (MT5). Komisi 1 USD per 1,0 lot (info user 2026-10-13;
  per-side vs round-turn BELUM dikonfirmasi — asumsikan per-side sampai
  ada klarifikasi). Lot minimum 0,01.
- Risk per trade: TIDAK ADA (lot min).
- SL: 1,5-3 x ATR(14).
- TP: 1:1,5 (Asia) / 1:2 (London/NY).
- Daily limit (live): Lot x 500.
- Guard akun kecil: 25% cap.
- Anti-martingale: WAJIB.
- Bid/ask handling: WAJIB.

Detail: RULES.md Â§18.

---

## 7. Keputusan Penting

| Tanggal | Keputusan |
|---|---|
| 2026-10-04 | Struktur folder strategies/ |
| 2026-10-04 | Fokus scalping dulu |
| 2026-10-05 | AGENTS.md v3.0 |
| 2026-10-05 | RULES.md v2.0 |
| 2026-10-05 | PROMPTS.md v2.0 |
| 2026-10-05 | CONTEXT.md v1.2 |
| 2026-10-05 | Broker timezone = UTC+3 (terverifikasi empiris) |
| 2026-10-05 | Simbol MT5 = USDJPY, bukan USDJPYm (terverifikasi) |
| 2026-10-05 | Risk: no %, daily limit $ |
| 2026-10-05 | 3 fase: Training, Graduation, Live |
| 2026-10-05 | Metode dipilih setelah EDA |
| 2026-10-05 | Bid/ask wajib benar (Â§18.16) |
| 2026-10-05 | Jurnal rotasi per bulan |
| 2026-10-05 | Backtest folder per tanggal |
| 2026-10-05 | Workflow multi-AI (1-3 AI) |
| 2026-10-05 | Onboarding AI baru (Prompt 0) |
| 2026-10-07 | H1-H5 dikunci (H1 KUATKAN, H2-H5 bersyarat S1-S8, H6+ DITOLAK) |
| 2026-10-08/09 | Vonis: H1 GUGUR, H2 GUGUR FINAL, H3 GUGUR (S4b), H4 TAHAN, H5 GUGUR FINAL, H4b GUGUR, R-2 GUGUR |
| 2026-10-09 | Fondasi-B TERTUTUP (D-1/D-2/D-3 DISAHKAN, D-4 SELESAI) |
| 2026-10-12 | EDA-07 L3-1: register 68 LOLOS / 35 GUGUR; simulasi LA = biaya mendominasi (G4=False semua) |
| 2026-10-13 | Asisten merangkap arsitek (formal, S1A ASSISTANT_RULES; preseden Amandemen C) |
| 2026-10-13 | Repo GitHub aktif `github.com/Mziana/ANN` branch `main`, commit `2112f94` (bukan "belum dipakai") |
| 2026-10-13 | Vonis B-4 = GO: spec pemodelan pra-registrasi, BUKAN paper-trade |
| 2026-10-13 | Draf `spesifikasi-fingerprint.md` DIPENSIUNKAN -> diganti Discovery-R1 |
| 2026-10-13 | Metode dipusatkan pada dokumen desain event-first (E1/E2/E3, gerbang G1-G7, jalur P0-P2) |
| 2026-10-13 | Broker Finex: komisi 1 USD/lot, lot min 0,01 (per-side vs round-turn belum jelas) |

---

## 8. Asumsi

### 8.1 Sudah Terverifikasi (2026-10-05)

| Asumsi lama | Hasil verifikasi | Bukti |
|---|---|---|
| Simbol MT5 Finex: USDJPY (mungkin USDJPYm) | **TERVERIFIKASI: `USDJPY`** | `mt5.symbols_get()` mengembalikan 82 simbol; `USDJPYm` TIDAK ada |
| Timezone broker: GMT+2 atau GMT+3 | **TERVERIFIKASI: UTC+3** (`Etc/GMT-3`) | `now UTC` 02:48:49 vs last M1 bar 05:48 -> offset +3 jam |
| Data MT5: 3 tahun | **TERVERIFIKASI: 3,75 tahun = 1.348.135 bar M1** | `copy_rates_range('USDJPY', M1, 2023-01-01, 2026-10-06)` |

Tambahan terverifikasi (2026-10-05):
- Terminal: **Finex Bisnis Solusi MT5 Terminal**, build 6230, `connected=True`.
- USDJPY: `digits=3`, `point=0.001` -> 1 pip = 0.01 (cocok `configs/data.yaml`).
- Spread live terukur: **0,8 pip** (8 point; tick bid 157.851 / ask 157.859).
- `configs/data.yaml` `spread.default: 1.5` **konservatif** vs live 0,8 -> aman untuk backtest.
- `trade_allowed=False` -> akun belum login untuk trading.
- First bar M1: 2023-01-02 00:07 (waktu broker UTC+3).

### 8.2 Belum Diverifikasi

- Finex punya cent account: **BELUM DIKONFIRMASI**. `trade_allowed=False` adalah indikasi belum login trading, bukan bukti adanya akun cent. Perlu cek manual di terminal.
- Spread multiplier berita (FOMC/CPI/NFP/BoJ): **ANGKA ASUMSI**.
- Spread `sunday_open: 5.0`: **ANGKA ASUMSI**, belum diukur.
- Freebuff + Hermes bisa browse: belum diuji di sesi ini.

### 8.3 Terukur 2026-10-06/12 — tapi OTAORITAS TERPUTUS

- Spread per sesi **SUDAH DIUKUR dari data M1 4 tahun** (item lama "belum
  diukur" di §8.2 sudah usang). Mean ~0,65 pip: London ~0,6 · NewYork ~0,7 ·
  Tokyo ~0,6 · Sydney ~0,8. Stres p95 0,8-1,5. Tidak ada ekor tersembunyi
  (sudah dicek M1 vs M5 max). Tercatat di `configs/data.yaml` sebagai
  `spread.cost_basis` + `spread.stress_bands`.
- **KONFLIK TERSISA (per 2026-10-13, belum diputuskan):** config punya dua
  sumber angka yang berbeda 2,3x —
  `spread.default: 1.5` & `by_year[2023]: 3.0` (konservatif, dari p99)
  vs `cost_basis.default: 0.65` (mean terukur).
  Blok yang lebih lama **TIDAK diganti** saat fragmen baru diterapkan 2026-10-06.
  Sampai user memutuskan, **backtest WAJIB menyebut kode mana yang dipakai.**
- Spread live 0,8 pip (tik 2026-10-05) berada di antara keduanya.
- Offset dua jendela anomali + SA-03: lihat `.ai/STATE.md` bagian "Peringatan
  Waktu Broker" — BELUM TERVERIFIKASI, dilarang jadi input fitur sesi.

---

## 9. Struktur Folder

usdjpy-bot/
- .ai/                # Aturan AI + state
- configs/            # Config global
- strategies/         # Per strategi
- data/               # M1-D1
- src/                # Kode shared
- notebooks/          # Riset
- journal/            # Jurnal (INDEX, trades/, daily/, monthly/)
- models/             # Model tersimpan
- logs/               # Log runtime
- reports/            # backtest/YYYY-MM-DD/NN_nama/
- tests/              # Test
- scripts/            # Script bantu
- docs/               # Dokumentasi

---

## 10. File Penting

| File | Isi |
|---|---|
| .ai/AGENTS.md | Kontrak AI (v3.0) |
| .ai/RULES.md | Kode + trading (v2.0) |
| .ai/CONTEXT.md | File ini |
| .ai/PROMPTS.md | 33 prompt (v2.0) |
| .ai/STATE.md | Status saat ini |
| .ai/TASKS.md | Task board |
| .ai/PROGRESS.md | Milestone |
| .ai/SESSION_LOG.md | Log per sesi |
| .ai/CHECKPOINT_LOG.md | Log checkpoint |
| docs/PROJECT_MAP.md | Peta proyek |

---

## 11. Jurnal & Backtest

### Jurnal (rotasi per bulan)
journal/
- INDEX.md              # peta
- trades/YYYY-MM.csv    # per bulan
- daily/YYYY-MM-DD.md   # harian
- monthly/YYYY-MM.md    # bulanan
- decision_log.md
- experiment_log.md

Cara baca: INDEX -> monthly -> daily (3 hari). JANGAN CSV mentah.

### Backtest (folder per tanggal)
reports/backtest/
- 2026-10-05/
  - INDEX.md
  - 01_ema_cross/
    - config.yaml
    - result.json
    - trades.csv
    - equity_curve.png
    - report.md
  - 02_rsi_meanrev/
- 2026-10-06/

---

## 12. Yang Belum Ada (per 2026-10-13)

DAFTAR LAMA SUDAH USANG — data fetch sudah dijalankan (1.347.847 bar),
GitHub repo sudah aktif (`main` `2112f94`). Yang benar-benar belum ada:

- `docs/architecture.md`
- **Metode strategi** — masih kosong; dasar riset (dokumen desain
  event-first) sudah dibaca, spec Discovery-R1 belum ditulis
- **Modul model & backtest** — `src/models/` dan `src/backtest/` belum ada
  sama sekali (terverifikasi 2026-10-13). `reports/backtest/` masih kosong:
  nol run backtest sampai sekarang
- **Hasil backtest** — nol. Belum ada satu pun angka P&L
- **Isi `.env.example`** — masih 0 byte (terverifikasi)
- 500+ trade data (kriteria Fase 1)
- Spec pemodelan Discovery-R1 + Spesifikasi Metode Target (menunggu izin user)

Status `trade_allowed=False` (akun belum login trading) tetap sama sejak
2026-10-05 dan tidak menghalangi riset.

---

## 13. Aturan Emas Proyek

1. Data dulu, tebakan nanti.
2. Uji dulu, simpulkan kemudian.
3. Jujur soal yang belum dicek.
4. Jangan andalkan memori AI. Andalkan file.
5. Patch, jangan rewrite.
6. Satu strategi, satu fokus.
7. Akun kecil = testing.
8. Edge > Limit. Kill switch tetap ada.
9. Bid/ask wajib benar.
10. Onboarding AI baru wajib.

---

## 14. Referensi

- .ai/AGENTS.md - aturan perilaku AI
- .ai/RULES.md - kode + trading
- .ai/PROMPTS.md - 33 prompt
- docs/PROJECT_MAP.md - peta proyek

---

Akhir CONTEXT.md v1.3
