# Putusan Arsitek EDA-06 TERTUTUP + Mandat EDA-07 (2026-10-10)

Peran: Arsitek (rangkap asisten atas perintah user 2026-10-10).
Status: EDA-06 TERTUTUP dengan vonis prosedural LOLOS (izin lanjut,
bukan bukti edge). Vonis hipotesis H1-H5/H4b/R-2 tak tersentuh.

## P-1 Vonis prosedural EDA-06: LOLOS (sah, mengikat)

Coder (23+7, funnel 32-23-23-23) dan auditor independen (replikasi dari
nol, flag baris-per-baris cocok) sepakat tanpa divergensi material.
Gerbang K1-K4 berfungsi: menggugurkan 50/70 dan 30/45 di semua irisan,
meloloskan hanya barrier lebar di kondisi volatil. Ronde ini tidak
menghasilkan vonis strategi apa pun.

## P-2 Disposisi temuan re-audit

- T-MEDIUM sel 27 kosong: DITERIMA sebagai catatan, DITOLAK sebagai
  penghalang. Notebook tetap beku VERBATIM (dilarang edit pasca-run).
  Jawaban C1-C3 dikunci DI SINI (P-4), bukan di sel notebook.
- T-LOW CI bootstrap urutan-draw: DITERIMA + aturan mengikat untuk EDA-07
  (P-5): satu RNG stream per analisis, seed berbeda per blok, urutan draw
  didokumentasikan; K-gate EDA-07 dilarang bergantung pada CI.
- Observasi pola (lolos = ATR k1.5 Tokyo/London tercile-3; 50/70 gagal
  total): DICATAT sebagai konteks scope, bukan temuan. Skeptisisme auditor
  (konsentrasi Tokyo/London) sah dan diteruskan sebagai peringatan di
  spec EDA-07: dilarang mengklaim generalisasi sesi.

## P-3 Klarifikasi auditor yang diadopsi

- p* minimum 0,5212 memenuhi ambang informatif 0,53 (terpenuhi = di bawah
  atau sama; arah benar: semakin kecil semakin ramah biaya).
- Sydney ekor spread terburuk (39,10% bar > 2x default) + n kecil:
  Sydney KELUAR dari fokus EDA-07 kecuali sebagai pembanding deskriptif.
- NewYork p_none 4,58% tertinggi: dicatat sebagai bahan failure analysis
  EDA-07, bukan alasan menambah irisan.

## P-4 Jawaban C1-C3 (pengganti sel 27, mengikat sebagai bacaan resmi)

- C1 Spread: ekor menentukan, bukan mean. Sydney terburuk di semua
  kuantil atas; London/Tokyo paling ramah; pelebaran terkait volatilitas
  (Spearman dibaca dari rho) dan jam tetap rollover/open/fix.
- C2 Kapan melebar: desil rv15 atas + jendela rollover 23:30-00:30 wall +
  open Sydney/London/NY + fix Tokyo. Rilis berita tak terpisahkan di sini
  (tanpa kalender historis di repo) - DILARANG mengklaim efek berita.
- C3 Biaya: skenario normal vs stres vs slippage +0/+0,1/+0,3 per sesi
  (T-06-3); otoritas tetap cost_basis/p95, spread.default 1,5 bukan otoritas.
- C4a Arah N-menit: p* minimum 0,5212 (ambang 0,53 terpenuhi); bandingkan
  dengan prediktabilitas arah EDA-03 ~0,50 +/- 0,02 - arah murni saja
  tidak cukup, barrier + kondisi yang menentukan.
- C4b Barrier: laju dasar negatif sesuai harapan (tanpa edge hanya bayar
  biaya); delta terkecil pada ATR lebar tercile-3 London/Tokyo; 50/70
  gagal total (delta >= 4,92 semua sesi).
- Keputusan: LANJUT ke EDA-07 hanya pada 23 irisan tercile + 7 irisan sesi
  lolos (daftar T-06-7). Di luar itu: DILARANG dibawa.

## P-5 Kunci mengikat untuk spec EDA-07

1. Scope = 23 + 7 irisan lolos; 50/70, 30/45, NewYork/Sydney-nonlolos hanya
   pembanding deskriptif, tidak menentukan gerbang.
2. Notebook tetap deskriptif: tanpa P&L, backtest, atau pelatihan model.
   Baseline dan ANN tetap di Lapisan 3.
3. Holdout 2026 tetap tidak dimuat. Universe, semester, strata, kausalitas,
   dan otoritas biaya sama dengan EDA-06.
4. RNG terpisah per analisis (seed berbeda per blok bootstrap); gerbang
   tidak boleh bergantung pada CI bootstrap.
5. MI memakai lantai derau permutasi blok-hari; fitur kontrol wajib
   (derau acak + level bulat + prior-day H/L); redundansi |rho| > 0,8
   diringkas satu wakil.
6. Gerbang G1-G4 per rancangan user bagian 3.6, dengan G4 menaut ke delta
   EDA-06 irisan yang sama; gagal G2 atau G4 = berhenti, rumuskan ulang.

## P-6 Anti-merambat

H1/H2/H3/H5/H4b/R-2 GUGUR dan H4 TAHAN tak tersentuh putusan ini. H6+
tetap DITOLAK. P-5 hanya mengikat EDA-07; Lapisan 3 butuh spec baru.

Berikutnya: spec arsitek EDA-07 (label + fitur, scope P-5), lalu paket
coder paste-manual.
