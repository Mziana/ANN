# Design EDA-06 Eksekusi (gerbang biaya dulu)

date: 2026-10-10
topic: EDA-06 biaya breakeven execution
status: validated
peran: asisten (penerjemah + penjaga alur; bukan komandan)
workdir: D:\ANN
pola: paste-manual ke coder (spawn internal gagal, pin model host tak terjangkau)

## Problem Statement

EDA Q1-Q7 memprofilkan pasar tetapi tidak menjawab apakah ruang gerak
cukup besar dibanding biaya. Notebook referensi user
(eda_06_biaya_breakeven.ipynb) menjawab itu sebagai gerbang: bila tidak
ada irisan sesi x horizon/barrier yang lolos, EDA-07 dan baseline tidak
dijalankan dengan rumusan ini.

Yang dieksekusi adalah notebook user apa adanya (C1-C4, K1-K4),
di-port ke pola kanonis repo agar hasilnya sah sebagai gerbang.

## Constraints

- Vonis terkunci tak tersentuh: H1/H2/H3/H5/H4b/R-2 GUGUR, H4 TAHAN.
- H6+ DITOLAK. Ronde ini deskriptif + gerbang, BUKAN vonis, BUKAN backtest P&L.
- Holdout 2026 dikunci: tidak dimuat sama sekali, asersi max(utc) < 2026-01-01.
- Universe: strata A + B 2023-2025 minus C; B dilaporkan terpisah, tidak dihitung di K2.
- Otoritas biaya: cost_basis.by_session (normal) + stress_bands.p95.by_session
  (stres); spread.default 1.5 BUKAN otoritas. Slippage hanya skenario +0/+0,1/+0,3.
- Kausal: keputusan di akhir bar M1; bar M5 hanya yang sudah selesai.
- Nol tulis ke configs/src/data oleh coder; DILARANG commit/push oleh coder.
- Tanpa dependensi baru (pandas, numpy, scipy, matplotlib yang sudah ada).
- Referensi beku (jangan diubah, hanya dibaca):
  thoughts/shared/references/eda06/eda_06_biaya_breakeven.ipynb
  thoughts/shared/references/eda06/EDA_06_07_rancangan.md

## Approach

Port notebook referensi ke pola rantai EDA repo: satu builder
scripts/_build_eda06.py yang men-generate + mengeksekusi
notebooks/scalping/eda_06_biaya_breakeven.ipynb secara deterministik.

Alasan pilih ini:

- Notebook referensi sudah benar secara substansi dan sudah lolos uji
  sintetis; yang kurang hanya bungkus provenance repo.
- Menjalankan file Downloads langsung menghasilkan angka tanpa gate,
  tidak sah sebagai gerbang keputusan.
- Uji sintetis ulang hanya bila port mengubah logika (tidak direncanakan).

Yang ditolak:

- Rewrite logika barrier/ATR/simulator (verbatim dari referensi).
- Menambah label, fitur, model, atau baseline ke ronde ini (itu EDA-07/Lapisan 3).
- Memakai 2026, mengubah definisi sesi/Off, atau menambah dependensi.

## Architecture

```
parquet M1 2023-2025 (tanpa 2026)
  -> builder _build_eda06.py (template + executor nbconvert, pola _build_eda05.py)
  -> notebook eda_06_biaya_breakeven.ipynb (kontrak verbatim sel pertama)
  -> C1 spread -> C2 spread vs vol/jam -> C3 biaya -> C4a grid p*
  -> ATR M5(14) kausal -> entri stride -> simulasi barrier
  -> stabilitas semester -> gerbang K1-K4 -> FIG-08..12 + CSV
  -> verdict GAGAL/LOLOS -> STOP (LOLOS = izin fokus EDA-07 pada irisan lolos)
```

## Components

- Builder: generator + executor, RUF-format idempoten, referensi baris stabil.
- Kontrak notebook: holdout, universe, biaya, stride, barrier pesimis
  (SL-menang-bila-sebar), ATR dibekukan saat entry, delta = -E/(TP+SL).
- C1: sebaran spread per sesi/jam/semester (T-06-1a..1d).
- C2: spread vs desil rv15 + jam tetap rollover/open/fix (T-06-2a, 2b).
- C3: biaya per sesi x skenario x slippage dalam pip/point/USD (T-06-3).
- C4a: grid p* = 0,5 + c/(2m) N = 5/15/30/60, sampel tanpa tumpang tindih (T-06-4).
- C4b: laju dasar barrier tetap (50/70, 30/45, 100/140 point) + ATR
  (k 0,75/1,0/1,5 x RR 1,0/1,4/2,0), horizon 120 mnt, stride 5 (T-06-5a..5f).
- Stabilitas: delta per semester x sesi (T-06-6); gerbang per irisan (T-06-7).
- Uji bawaan: ATR 12 timestamp hitung-ulang identik; simulator vs naif
  400 entri x 2 sisi identik; asersi strata/fingerprint/holdout.

## Data Flow

Parquet M1 2023-2025 kolom time, broker_time_raw, high, low, close,
spread_pips -> wall_clock_series hari-broker -> add_labels sesi ->
partisi A (825 hari pola) / B (185.248 bar H1-2023) / C (anomali, dibuang) ->
numpy array CL/HI/LO/UTC -> T-06-1..4 -> ATR M5 kausal -> IDX entri stride
(dengan laporan buang per alasan) -> simulate buy+sell digabung ->
agregasi per sesi/semester/tercile/desil/sisi -> delta + CI day-cluster ->
gerbang -> gambar + CSV -> ringkasan verdict.

## Error Handling

- Look-ahead: ATR hanya bar M5 selesai; uji 12 timestamp acak wajib identik.
- Simulator: vektor vs naif wajib identik; bila beda, STOP dan laporkan.
- Strata: B tepat 185.248, A tanpa Off, A+B+C utuh, tanpa 2026, fingerprint
  cocok; bila gagal, STOP (asersi cost_basis +-0,15 yang gagal = informasi
  untuk investigasi sebelum pelonggaran, bukan bug yang disembunyikan).
- Timeout/ambigu: timeout keluar di close; bar kembar dihitung SL (pesimis);
  pangsa ambigu dilaporkan; K4 mencegah barrier raksasa lolos semu.
- Klaim tanpa output mentah = GAGAL.

## Testing Strategy

- Gerbang pra-registrasi pada irisan (combo x sesi x tercile ATR = 144)
  + (combo x sesi = 48): K1 delta_normal <= 3pp DAN delta_stres <= 5pp;
  K2 delta_normal <= 3pp pada >= 4/5 semester A; K3 n >= 1000 entri-sisi
  DAN >= 100 hari; K4 p_none <= 50%.
- CI95 bootstrap klaster-hari (N_BOOT=1000, seed 20261010); effect-size dari
  besaran delta/p*, bukan p-value.
- Verdict eksplisit: GAGAL = jangan jalankan EDA-07 rumusan ini (opsi horizon
  lebih panjang / sesi tertentu / tinjau kelayakan scalping); LOLOS = fokuskan
  EDA-07 hanya pada irisan lolos (bukan bukti edge).
- Laporan tugas pola AGENTS.md S5: file dibuat/diubah + tabel Klaim & Bukti
  (TERVERIFIKASI/BELUM DIVERIFIKASI/ASUMSI) + yang belum diverifikasi +
  potensi masalah + rekomendasi irisan. Bahasa Indonesia. STOP setelah serah-terima.

## Open Questions

- Ambang K1-K4 (3/5pp, 100 hari, 1000 entri, 50% timeout) dipertahankan atau
  diubah sebelum run (keputusan user, tercatat di sel parameter).
- Horizon 120 mnt + stride 5 dipertahankan (keputusan user).
- Lokasi output: reports/eda/2026-10-06/figures/ (lama) vs
  reports/eda/2026-10-10/ (baru) - satu lokasi, dicatat coder.
- Setelah LOLOS: siapa menulis spec EDA-07 (irisan lolos sebagai scope).
- Pekerjaan terpisah: perpanjang jadwal DST broker_time.py sebelum 1 Nov 2026
  (tidak menghalangi ronde ini; EDA-06 tidak memanggil utc_series).
