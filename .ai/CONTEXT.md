# CONTEXT.md â€” Konteks Proyek USDJPY Bot

> Memori jangka panjang AI agent.
> Update saat ada perubahan besar (bukan setiap sesi).
>
> Versi: 1.2
> Update: 2026-10-05
> Proyek: USDJPY Trading Bot

---

## TL;DR â€” Baca Ini Dulu

Kalau cuma ingat 12 hal:

### Proyek
1. Tujuan: bot USDJPY scalping (M1-M15) berbasis ANN + rule-based.
2. Stack: Python 3.11, PyTorch, MT5 Finex, pandas, YAML.
3. Fase: Training (Demo Bebas) - kumpulkan 500+ trade.

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
| Format | Black, Ruff |
| Editor | VS Code + AI coding |
| OS | Windows |
| Shell | PowerShell |
| Data | 3 tahun (2023-sekarang) |
| GitHub | Belum dipakai |

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

Fase saat ini: Fase 1 (Training).

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

Status metode: BELUM DITENTUKAN.
Dipilih SETELAH EDA. Bukan opini.

Belum diputuskan:
- Library backtest.
- Arsitektur ANN.
- TF utama.
- Sesi prioritas.
- Metode sinyal (EMA, SMC, Fibo, dll).

---

## 6. Risk Framework

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
| 2026-10-05 | Risk: no %, daily limit $ |
| 2026-10-05 | 3 fase: Training, Graduation, Live |
| 2026-10-05 | Metode dipilih setelah EDA |
| 2026-10-05 | Bid/ask wajib benar (Â§18.16) |
| 2026-10-05 | Jurnal rotasi per bulan |
| 2026-10-05 | Backtest folder per tanggal |
| 2026-10-05 | Workflow multi-AI (1-3 AI) |
| 2026-10-05 | Onboarding AI baru (Prompt 0) |

---

## 8. Asumsi (Belum Diverifikasi)

- Simbol MT5 Finex: USDJPY (mungkin USDJPYm).
- Timezone broker: GMT+2 atau GMT+3.
- Finex punya cent account: BELUM DIKONFIRMASI.
- Spread USDJPY: 1,5-3 pip (perlu dicek).
- Data MT5: 3 tahun.
- Freebuff + Hermes bisa browse (harus dipaksa).

Aksi: verifikasi saat fetch data pertama.

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

## 12. Yang Belum Ada

- Data fetch MT5 (belum dijalankan)
- docs/architecture.md
- Metode strategi
- Model & backtest
- 500+ trade data
- GitHub repo (belum)

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

Akhir CONTEXT.md v1.2
