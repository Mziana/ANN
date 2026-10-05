# reports/backtest/ - Struktur Backtest

## Struktur

backtest/
- YYYY-MM-DD/
  - INDEX.md
  - 01_<nama>/
    - config.yaml
    - result.json
    - trades.csv
    - equity_curve.png
    - report.md
  - 02_<nama>/

## Aturan (section 17.3 RULES.md)

1. Setiap backtest di folder YYYY-MM-DD/NN_<nama>/.
2. Nomor urut 01, 02, dst.
3. WAJIB ada INDEX.md di folder tanggal.
4. Simpan semua, termasuk yang gagal.
5. JANGAN campur file backtest.
6. JANGAN timpa hasil lama.

Akhir README
