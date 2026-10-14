# Brief Audit Spec Discovery-R6-conditioning - Auditor Eksternal (2026-10-14)

## Otoritas + scope

Spec yang diaudit: `reports/governance/2026-10-14/arsitek/spesifikasi-discovery-R6-conditioning.md`
(status DRAF ARSITEK, belum pernah dieksekusi).

Fondasi yang boleh dipakai sebagai rujukan:
- `reports/governance/2026-10-14/arsitek/spesifikasi-discovery-R4-M15.md` (spec R4)
- `reports/governance/2026-10-14/Audit/addendum-R4-M15.md`
- `reports/research/2026-10-14/discovery-R4-M15/evidence/summary.json`
- `reports/research/2026-10-14/discovery-R4-M15/evidence/events.parquet`
- `.ai/AGENTS.md` (khususnya §8A anti-looping, §19 anti-pattern, §20 anti-halusinasi,
  §26 workflow multi-AI)

Audit ini **BUKAN** audit ulang warisan R4 (M15, ATR, E1/E2/E3, barrier, biaya,
cancel, shadow). Yang diaudit HANYA: **delta R6** = §0 justifikasi, §3 variabel
conditioning, §4 binning, §5 metrik bin, §6 gate, §7 vonis, §8 stop rule, §9
anti-drift tambahan. Temuan di luar delta = CATATAN kecuali cacat FATAL baru
(definisikan eksplisit di laporan).

Data 2023/2025/2026 **terkunci** untuk auditor juga. 2024 boleh dibaca hanya
untuk verifikasi angka di §0 dan §5, tidak untuk eksplorasi.

## Kerangka fakta yang WAJIB diverifikasi ulang (jangan percaya penulis spec)

Authors spec mengklaim angka-angka ini. Verifikasi dari evidence, bukan dari
spec. Bila salah, sebut koreksinya.

- **K1** - Pada TP:SL = 2:1, random walk tanpa drift: `P(+2R sebelum -1R) = 1/3`.
  Apakah ini benar secara matematis untuk random walk yang barrier-nya asimetris
  (SL 1R, TP 2R)? Perhatikan: untuk Brownian motion tanpa drift, peluang menyentuh
  +b sebelum -a adalah `a/(a+b)`. Dengan a=1, b=2 itu 1/3. Konfirmasi atau tolak.
- **K2** - Ambang impas setelah biaya: `WR > (SL + c)/(TP + SL) = 35,2%` dengan
  SL 17,6 pip dan c 1 pip. Turunkan sendiri dari(mean win = TP - c,
  mean loss = SL + c). Apakah 17,6 pip dan c = 1 pip itu angka yang benar dari
  `events.parquet` / `configs/data.yaml`?
- **K3** - `WR_decisive` gabungan R4 = 23,9%. Recompute dari `summary.json`
  (jumlahkan TP dan SL semua sel, bagi jumlah).
- **K4** - Edge R4 = 0,372-0,503. Recompute `median(mfe)/(median(mfe)+median(mae))`
  per sel.
- **K5** - Dekomposisi P&L kaki A: TP +56.654, SL -102.038, TIME +28.107 pip,
  total -17.277. Recompute dari `events.parquet`. Periksa juga klaim "bucket TIME
  profit +28.107" dan "45% event kena SL".
- **K6** - Baseline acak searah 13,50 pip (BUY) / 13,60 pip (SELL), median MFE
  horizon 10 bar M15 2024. Apakah spec R6 (§5) memakai baseline yang benar dan
  komparabel? Perhatikan: baseline dihitung dari entry ACAK tanpa conditioning,
  sedangkan MFE sinyal DIKONDISI. Apakah perbandingan Edge-vs-baseline ini
  menyesatkan karena base rate-nya berbeda?

## Butir audit delta

- **D1** - §0: apakah justifikasi ronde benar DAN lengkap? KHUSUS: apakah hipotesis
  "kondisional" benar-benar berbeda dari R1-R4, atau hanya pengulangan dengan
  nama lain? Bandingkan dengan §2 (yang diwarisi verbatim).
- **D2** - §3 causality: `EXT` pakai `c[t0]`; `VOLR` pakai ewm TR; `PREMOVE`
  pakai `c[t0-1], c[t0]`. Sinyal fires saat bar t0 TUTUP, entry di OPEN `t0+1`.
  Apakah keempat variabel 100% causal? Look-ahead tersembunyi?
  Periksa juga: apakah `sma20[i] = mean(c[i-19..i])` mendefinisikan ulang index
  dengan benar dan tidak off-by-one.
- **D3** - §4 binning: tercile dihitung atas event yang lolos cancel, **pooled
  seluruh 9 sel**. Apakah ambang tercile yang dihitung dari sampel yang sedang
  dianalisis menimbulkan kebocoran? (Argumen: bin hanya bergantung variabel
  pre-trade, jadi tidak boleh bocor. Setuju atau tolak, dengan bukti.)
  Apakah "3 bin per variabel x 3 keluarga + 13 pooled = 52 bin" konsisten dengan
  teks spec?
- **D4** - **Gate G1 `n_eval >= 500` terhadap ukuran sampel sebenarnya.**
  Hitung dari `summary.json`: `n_eval` per sel, jumlah per keluarga (E1/E2/E3),
  jumlah pooled. Lalu jawab: bin mana yang secara struktur **tidak mungkin**
  mencapai n=500? Apakah ada keluarga yang otomatis gugur tanpa diuji? Jika ya,
  apakah itu cacat spec (pembeda perlakuan tidak adil antar keluarga) atau
  keputusan desain yang sah? Berikan angka.
- **D5** - §6 G2 `Edge >= 0,56`: dari mana angka ini? Apakah konsisten dengan
  G3/G4 dan dengan K1-K4? Mengapa 0,56 dan bukan 0,55 atau 0,58? Apakah ada
  pembenaran Beyond "sebmodakfeel"? Kalau tidak, sebut sebagai angka arbitrer.
- **D6** - §6 G5 (Edge >= 0,53 di >= 3 dari 9 sel): apakah ini bisa dihitung
  dari artefak yang akan dihasilkan? Apakah bin pooled punya "sel"? Spec
  TIDAK JELAS di sini - auditor wajib menilai dan menyebut.
- **D7** - **§6 G6 (jumlah bin yang lolos <= 3) sebagai kontrol overfit.**
  Ini pagar anti-overfit yang diklaim penulis spec. Uji skeptis: dengan 52 bin,
  n>=500, dan gate median-net + CI-batas-bawah, berapa bin akan lolos **secara
  kebetulan di bawah null** (Edge ~ 0,5, tanpa edge)? Apakah angka 3 punya dasar
  kuantitatif atau hanyaZdravood? Apakah G6 cukup, atau G6 justru melokalisasi
  overfitting (menambah lookup tanpa menambah kebenaran)?
- **D8** - §7: tiga vonis, tanpa `BELUM JELAS`. Apakah ada kondisi nyata yang
  tidak terpetakan ke salah satu dari tiga? Miscoded: misalnya semua bin gugur
  karena n<500 (lihat D4) - itu `MATI-KELAS` atau `INKONSISTEN`?
- **D9** - §8 stop rule: "R6 ronde terakhir kelas E1/E2/E3 fixed-barrier".
  Apakah ini enforceable? Apakah ada celah untukuttar R7 dengan menyebut "hipotesis
  baru" padahal masih E1/E2/E3 + filter?
- **D10** - §5 memaksa WR koreksi (P_profit/P_loss/P_time/TIME%/P_flat)
  **bersamaan** dengan `winrate_decisive`. Apakah ini cukup untuk mencegah
  addendum-R4 terulang? Apakah ada metrik R4 lain yang WAJIB dipertahankan?
- **D11** - §9 anti-drift tambahan: whitelist path, baseline acak in-run, larangan
  variabel kelima. Cukup? Apakah "tidak boleh menambah variabel kelima"
  dapat ditegakkan (bagaimana kalau coder butuh kolom helper)?
- **D12** - §10 artefak: `tabel_gate.csv` 52 bar. Apakah 52 benar? Apakah
  `events.parquet` R6 akan menimpa / membingungkan `events.parquet` R4?
- **D13** - §8A compliance: apakah spec R6 boleh ada sama sekali (§8A ayat 3:
  ronde tambahan butuh persetujuan eksplisit user)? Apakah spec ini mencatat
  bahwa persetujuan itu sudah diberikan, dan oleh siapa/tanggal?

## Format jawaban

- Per butir (K1-K6, D1-D13): `LULUS` / `GAGAL` / `CATATAN` + bukti
  (`file:baris` atau angka yang dihitung ulang).
- **Verdict**: `LULUS` / `CATATAN` (lulus bersyarat - sebut syaratnya) /
  `GAGAL` (sebut butir + alasan + **perbaikan minimal** yang konkret).
- SAYA BUTA / GANGGUAN KHUSUS: sebutkan urutan cacat berdasarkan-ahead-of-time.

## Larangan keras

- Tidak menulis kode produksi. Auditor TIDAK mengimplementasikan (§26).
- Tidak merancang ulang spec; hanya melaporkan cacat + perbaikan minimal.
- Tidak mengusulkan variabel conditioning kelima, threshold alternatif, atau
  barrier/RR alternatif.
- Tidak membuka 2023/2025/2026.
- Tidak menjalankan run backtest apa pun.
- Semua angka yang dipakai harus dihitung ulang dari evidence, bukan dikutip
  dari spec tanpa verifikasi.
