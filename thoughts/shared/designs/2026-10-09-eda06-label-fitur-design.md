# Design EDA-06 Label-Fitur (tahap awal)

date: 2026-10-09
topic: EDA scalping event-to-outcome + target dua tahap menuju ANN
status: draft
peran: asisten + arsitek (rangkap atas perintah user, tahap awal saja)
workdir: D:\ANN

## Problem Statement

EDA Q1-Q7 menjawab seperti apa USDJPY itu (market profiling).
Belum menjawab setelah event X muncul, apa yang terjadi 1-20 candle
setelahnya, dan apakah cukup bayar biaya.

Akibatnya peneliti muter: label naik/turun mentah hampir 50/50 noisy,
fitur terlihat lemah, lalu ambang digeser pasca-hoc agar terlihat bagus.

## Constraints

- Vonis terkunci tidak tersentuh: H1/H2/H3/H5/H4b/R-2 GUGUR, H4 TAHAN tipis.
- H6+ DITOLAK sampai pra-registrasi segar. Ronde ini discovery, bukan vonis.
- Tipologi regime full-sample = ex-post, DILARANG jadi fitur.
- Satu otoritas biaya harus dipilih sebelum uji: cost_basis vs spread default.
- Format: ASCII-only, LF-only, tanpa self-hash. Tanpa commit/push oleh coder/auditor.
- Split waktu expanding, bukan acak. Fitur multi-timeframe hanya candle closed.
- Scaler fit hanya di train.

## Approach Pilihan

Satu notebook discovery: eda_06_label_fitur, memakai loader dan parquet
yang sudah ada. Tidak fetch baru, tidak ubah EDA lama.

Alasan pilih ini:

- Stuck sebenarnya di definisi label, bukan di cleaning atau pilihan indikator.
- Arah hampir acak, besaran gerak dan volatilitas yang terukur kuat.
- Target dua tahap memecah masalah: (a) apakah gerak N menit melebihi
  biaya + margin, lalu (b) arah hanya jika (a) terpenuhi.
- Gerbang baseline walk-forward: jika baseline sederhana tidak lewat biaya,
  ANN hampir pasti juga tidak. Ini penghenti muter yang jujur.

Yang ditolak:

- Menambah puluhan indikator dulu sebelum label dikunci.
- Optimasi threshold dengan memindai profit terbesar (optimasi noise).
- Memakai 2026 sebagai penentu (status dikecualikan penuh).
- Mengubah definisi sesi/Off (fingerprint mengikat).

## Architecture Alur

MARKET (sesi/regime/volatilitas/spread, sudah ada)
-> PRE-ENTRY CONTEXT (candle -20 s/d -1)
-> EVENT / TRIGGER (candle 0, identitas ber-ID mis EVENT-001)
-> LOCATION (posisi harga saat event)
-> EXECUTION CONDITION (spread/slippage/volatilitas saat event)
-> FORWARD OUTCOME (+1/+2/+3/+5/+10/+15/+20 candle)
-> MFE/MAE + TP-before-SL
-> CONDITIONAL ANALYSIS (sesi/volatilitas/spread/location/regime)
-> FAILURE ANALYSIS (kapan setup bagus justru gagal)
-> STABILITY (tahun/sesi/regime/strata A/B/C)
-> OUT-OF-SAMPLE expanding
-> BARU hipotesis trading (di luar ronde ini)

## Components

- Perbandingan 3 definisi label pada N 5, 15, 30 menit:
  return N menit, tiga kelas threshold spread/ATR, triple-barrier.
  Ukur class balance + ukuran gerak vs biaya.
- Mutual information / korelasi rank fitur terhadap label:
  realized-vol rolling real-time, jam sesi, jarak ke MA dalam satuan ATR,
  momentum M5/M15/H1 (closed saja).
- Pangkas multikolinearitas antarfitur yang redundan.
- Fitur regime dari selisih yield AS-Jepang hanya sebagai regime,
  bukan sinyal entry (opsional, bila data tersedia).
- Event fundamental (NFP/BoJ/CPI) ditandai sebagai fitur event,
  tidak langsung dibuang.

## Data Flow

Parquet M1/M5/M15/H1 yang sudah ada
-> loader beku yang sama dengan EDA lama
-> bangun label 3 definisi x 3 horizon (train-only threshold)
-> hitung fitur real-time only (t <= entry)
-> ukur outcome hanya dari t > entry (MFE/MAE/TP-before-SL)
-> MI/stabilitas per tahun + strata
-> baseline logistic/boosting walk-forward
-> STOP, lapor apa adanya

## Error Handling (pagar)

- Look-ahead: kondisi entry hanya dari t <= entry. Data t > entry
  hanya untuk ukur hasil. Pelanggaran = temuan HIGH.
- Threshold dikunci sebelum uji konfirmasi. Geser pasca-hoc = hipotesis
  baru wajib pra-registrasi segar + data segar.
- Jika pola hanya bagus di satu slice (mis satu tahun/sesi) dan buruk
  di sisanya, dilaporkan sebagai tidak umum, bukan edge.
- Spread saat event dicatat (nilai + percentile + vs median sesi).
  Event bagus saat spread normal bisa buruk saat spread melebar.

## Testing Strategy (gerbang sebelum ANN)

- Baseline sederhana walk-forward expanding (train masa lalu, test masa
  depan yang belum dipakai discovery).
- Kriteria gerbang: gerak rata-rata vs spread+komisi+slippage.
  Jika baseline tidak melewati biaya, ANN tidak dilanjutkan dengan
  dalih tuning.
- Stabilitas wajib: per tahun + per strata A/B/C + per sesi.
- Semua angka berpasangan output mentah. Tanpa bukti = BELUM DIVERIFIKASI.

## Open Questions

- Otoritas biaya final: cost_basis 0.65 vs spread default 1.5 — butuh satu putusan.
- Apakah data yield US10Y vs JGB tersedia dan sejalan timestamp broker.
- Apakah kalender libur NYSE/TSE dimasukkan sebagai missing-event atau tetap di luar scope.
- Setelah eda_06 discovery lolos gerbang, siapa menulis spec pra-registrasi konfirmasi.

## Next Steps

1. User setujui scope eda_06 di atas.
2. Asisten+arsitek susun brief spec eda_06 (substansi + perintah mentah + larangan bentuk-spesifik + SELF-AUDIT 3x).
3. Paste ke arsitek/coder lama sesuai pola paste-manual.
4. Kembali dengan laporan untuk gerbang pra-audit, lalu putuskan lanjut ANN atau tahan.
