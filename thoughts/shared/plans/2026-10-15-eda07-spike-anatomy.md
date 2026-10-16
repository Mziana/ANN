# Blueprint EDA-07 — spike_anatomy_outcome (FINAL — menunggu approval eksekusi)

> Status: FINAL 2026-10-15. Audit adversarial mandiri selesai (1 FATAL + 4 HIGH + 7 MED + 4 LOW) — SEMUA diterapkan di bawah. Eksekusi (worktree + coder) HANYA setelah approval eksplisit user.
> Planner subagent gagal spawn (model tidak tersedia) — draf disusun Commander dari artefak run. Jejak audit: §12.

## 1. Latar

EDA-06 (CLOSED, commit `061602c`) membuktikan eksistensi spike+exhaustion → kembali ke open (51 event, 12 win) tapi UNDERPOWERED. Yang belum dijawab: **base rate "terbalas" atas seluruh pool spike mentah**, karakteristik pra/pasca, dan hubungan magnitudo → outcome. EDA-07 = deskriptif murni (anatomi + base rate). Entry test = EDA-08/09, hanya bila base rate lolos kill.

Fakta terverifikasi dari run EDA-06 (output sel 5, bukan ringkasan):
`spike terdeteksi: 2116 | kandidat exhaustion (r ada): 270`. Angka 856 TIDAK ada di output — dilarang dipakai sebagai fakta.

## 2. Pertanyaan (terkunci)

1. Dari pool spike R, berapa % **terbalas** (agregat + per band magnitudo)?
2. Bagaimana distribusi **jarak spike** (pip dan ×ATR: median/p25/p75/p95)?
3. Bagaimana **anatomi 10 bar pra + 16 bar pasca** tiap spike?
4. Apakah karakteristik pra **memprediksi** reversal vs continuation? (deskriptif: tabel stratifikasi median/IQR per outcome + standardized mean difference — TANPA classifier, TANPA uji di luar daftar FDR)
5. **Q1-sub**: berapa bar dari akhir spike sampai reversal pertama (definisi A primer), per band? Dihitung DARI bar-s: `bar_ke = idx_reversal − s` (reversal di bar berikut = 1; TERKUNCI audit R4 B-3). Output: median + IQR + CI95 cluster-per-day untuk median per band, metode = **percentile bootstrap atas median hasil resample-per-hari** (B=10000, seed §7-F4; TERKUNCI audit R4 B-2); bila n_rev terlalu kecil untuk bootstrap reliabel → labeli eksplisit "point-only". Dihitung atas event YANG TERBALAS SAJA + wajib lapor `n_rev/n_band` di sampingnya (timeout/continuation excluded, dinyatakan eksplisit).
6. **Q3-sub**: range (hi−lo) vs net movement per band. Net = `sdir×(close(s)−open(i))` (bertanda arah agar antar-arah komparabel). Sifat: `|net| ≤ range` selalu → **assertion generator** `|rasio| ≤ 1+eps` dengan `eps = 1e-6` (`np.isclose`, atol standar numerik; TERKUNCI audit R4 B-4). Negatif dalam eps → clamp 0 + counter (debu floating-point); negatif melebihi eps → crash (sinyal bug, sesuai disiplin assertion — usulan skip-diam audit R4 C-1 DITOLAK dengan alasan ini). Output per band: rasio net/range (unitless) + selisih absolut "wick" (range−|net|) dalam pip DAN ×atr_s. Median + IQR + CI95 cluster-per-day (atau label "point-only").
7. Q1-sub & Q3-sub dihitung HANYA agregat + per band (bukan cross-cut baru).

## 3. Definisi terkunci (preregistrasi)

- **Scan spike: warisi EDA-06 verbatim** (`scan_spikes`: range bar > thresh×ATR14, ekstensi ≤2 bar searah, cooldown 16 bar, mulai bar ke-4). Ekstensi DILARANG cross-day (TERKUNCI audit R4 A-3, sesuai perilaku EDA-06 yang scan per-day-frame: `j >= n: break`). Spike di ujung hari berhenti di bar terakhir frame (`s` = bar terakhir); event demikian hampir pasti gugur di aturan ruang-16-bar — tercatat sebagai drop, bukan dianalisis. Dijalankan untuk KEDUA ambang (2,0× dan 1,5×) + dikumpulkan anatomi untuk keduanya (EDA-06 hanya menyimpan 2,0× — inilah "kode baru" yang dibutuhkan).
- **Dedup ke spike fisik unik (TERKUNCI)**: gabung kedua scan → kelompokkan deteksi se-hari + searah yang jendela `[i..s]`-nya bertumpuk → wakil = magnitudo terbesar → laporkan susut `2116→Nunik`. Seluruh analisis (band, tercil, rate) di atas populasi unik. Alasan: kedua scan tidak saling mencakup (rantai cooldown berbeda) sehingga "2116" mengandung duplikat parsial.
- **Magnitudo terukur**: `(hi − lo) / atr_s`, dengan hi/lo terakumulasi aturan ekstensi, `atr_s` = ATR bar ujung-s. **Parquet WAJIB simpan magnitudo kontinu** (`mag_cont`); band hanya untuk pelaporan — ANN dilarang memakai band sebagai fitur kategorikal tanpa uji (anti-cliff 2,49 vs 2,51).
- **4 band DISJOINT by magnitudo terukur**: `[1.5–2.0)`, `[2.0–2.5)`, `[2.5–3.0)`, `[3.0+)`. Tepi TERKUNCI. Overflow: mag terukur <1,5 (mungkin karena atr_s ≠ atr_i) → masuk band-1 + counter dilaporkan. **Fallback pra-registrasi berjenjang (TERKUNCI audit R4 A-4)**: bila band-4 <30 event, laporkan pool `[2.5+)` sebagai sekunder; bila pool itu juga <30 → naik ke `[2.0+)`; bila tetap <30 → tulis eksplisit "pool besar tidak teruji pada n ini". Tiap jenjang dilaporkan (dilarang melompat diam-diam). Bukan kill, bukan ganti primer — ronde tidak boleh bisu di titik terpanas.
- **Reversal primer (A)**: harga menyentuh level `(hi+lo)/2` (retracement ≥50% range) dalam 16 bar M15 setelah bar-s. Rasional jendela 16: komparabilitas EDA-06 (K=16) + kontainment se-hari. Sentuhan = overlap range bar dengan level (wick dihitung, konvensi EDA-06 — coder verifikasi). Arah: spike naik = sentuh via low ≤ level; spike turun = via high ≥ level. Sentuh-dulu-menang antar-bar; tie se-bar (sentuh level-A sekaligus cetak ekstrem baru searah) = **continuation menang** (TERKUNCI).
- **Reversal robustness (B)**: kembali ke harga pre-spike (close bar i−1) dalam 16 bar. **Opsi C**: retracement ≥1×ATR dari ekstrem dalam 16 bar — robustness DI LUAR FDR.
- **Continuation**: close melewati ≥1×ATR (pakai `atr_s`) searah spike dari ekstrem dalam 16 bar. **Timeout**: tak ada keduanya dalam 16 bar.
- **First reversal**: bar pertama sentuh level-A; catat: berapa bar sampai sentuh (1–16), adverse excursion sebelum sentuh (×ATR), jangkauan balasan sesudahnya (16 bar penuh).
- **Flag exhaustion (TERKUNCI, jembatan EDA-06)**: tiap event simpan `has_exhaustion` + bar-r (hitung dengan `first_exhaustion` EDA-06 verbatim) + cross-tab reversal-rate × exhaustion sebagai eksploratori. Tanpa ini pertanyaan "apakah filter RSI EDA-06 ada gunanya?" tak terjawab.
- **First-spike-of-day**: event unik dengan bar-i terkecil hari itu (untuk sensitivitas). Arah seleksi TERKUNCI (audit R4 C-2): spike pertama cenderung Tokyo/Sydney (jam awal) → sensitivitas ini bias ke sesi Asia → bandingkan dengan agregat untuk membaca apakah pola lebih kuat/lemah di Asia.
- **Anatomi pra** (warisi + tambah): pre_1..10 size/dir, micro_box/dist 12 bar, jarak close(i−1)→open harian, persentil rolling-500, RSI bar-i & bar-s, **kelas hari A/B/C (warisi EDA-06)**, jam UTC + sesi (Tokyo/London/NY via broker_time).
- **Ruang 16 bar (TERKUNCI)**: butuh bar s+1..s+16 dalam hari yang sama (tanpa cross-day, karena level terikat open hari itu). Spike tanpa ruang = drop + LAPORKAN jumlah per band DAN per jam (bias sore hari harus terlihat) + catatan live-applicability. Bukan assert-stop (deskriptif; kehilangan beberapa spike tidak fatal).
- **Gap M15: DIBUANG.**

## 4. Populasi, partisi, efek ganda

- R 384 hari, M15 saja. V hanya konfirmasi shortlist nanti. P segel.
- **Split waktu vs non-waktu (KOREKSI 2026-10-15 atas STOP coder — versi lama menulis 379 = 384−5, derivasi ganda)**: kode EDA-06 SUDAH mengeluarkan 5 hari anomali dari R (`_build_eda06_candle.py:157-158`, assert anti-bocor), sehingga "R 384 hari" = hari bersih PASCA-eksklusi. Split sesi + jam dihitung atas **384 hari bersih yang sama** (intent TASKS-245 — nol fitur sesi dari jendela anomali — terpenuhi by construction). Dilarang menjatuhkan 5 hari tambahan demi angka literal. Laporan wajib satu baris caveat menjelaskan koreksi ini.
- **Cek-0a pre-flight**: split 2116 per ambang scan (exact count 2,0× vs 1,5×) + reproduksi `2116` dan `270` dengan kode EDA-06 sebelum ekstensi (sanity reproduksibilitas — gagal = STOP).
- **Cek-0b**: matriks overlap antar-scan + verifikasi dedup (tiap event unik tepat satu band; susut 2116→Nunik dilaporkan).
- **Klastering**: jendela 16-bar antar-spike se-hari bertumpuk → outcome berkorelasi. Primer memakai **CI cluster-per-day** (bootstrap by day, B=10000, seed §7). Sensitivitas: ulangi primer pada **first-spike-of-day only**. Searah = kokoh; divergen = laporkan, jangan pilih yang bagus.

## 5. Hierarki estimasi (terkunci)

- **Primer**: agregat + 4 band, masing-masing reversal-rate + continuation-rate + timeout-rate + CI95 cluster-per-day. (Tercil BUKAN primer.)
- **Robustness** (di luar FDR, di atas populasi unik): tercil magnitudo, definisi B, definisi C.
- **Eksploratori berlabel + FDR-BH** (q=0,10, TERKUNCI): sesi × kelas-hari × jam-dalam-hari (bar 5–10/11–20/21–32/33+, atas 384 hari bersih §4) + cross-tab exhaustion (§3) + split per-tahun untuk distribusi jarak (rezim volatilitas 2023 vs 2024). Bukan kill.
- **Null machine warisi EDA-06 — DENGAN SPESIFIKASI WAJIB (§7-F6)**: "warisi" tanpa adaptasi tertulis = cek kosong. Coder menulis konstruksi null (apa yang dipermutasi, atas populasi apa, seed) di laporan pre-flight; reviewer menolak bila hand-wavy. Dilarang placebo shift ±U(2,6) (kontaminasi cooldown-16, terbukti).
- **Sel <30 → drop+label (warisi EDA-06), BUKAN kill** (+ fallback band §3). Ronde deskriptif: sel kecil dilaporkan tanpa simpulan.
- **Agnostik bentuk kurva**: gradasi monotonik vs U-terbalik — baca pola estimasi per band + CI, dilarang menyimpulkan bentuk tanpa dukungan CI.

## 6. Kill criteria dua lapis (terpisah level)

- **Lapis-1 (jalur harga)**: batas bawah CI95 reversal-rate agregat primer-A < 50% → GUGUR sebagai pola reversal. (Pembanding = koin, bukan biaya.)
- **Lapis-2 (trade implisit)** — spesifikasi TETAP (TERKUNCI): entry = **close(s+1)** (BUKAN close(s) — `s` baru diketahui setelah bar s+1 close; entry di close(s) = look-ahead, temuan audit F-A1), arah fade (`rd = −sdir`), TP = level 50% range, SL = ekstrem spike + **0,5×`atr_s` buffer (ATR EKSPLISIT `atr_s`)**, biaya 0,95 flat, first-passage K=16 (MTM net-pip setelah biaya saat timeout, warisi EDA-06). **Prefilter**: |entry−TP| − biaya < 2,85 pip → trade degenerate → drop+label, jumlah dilaporkan (rasional: logika gross−biaya identik dengan `MIN_NET_TP_PIP` EDA-06; nilai diwarisi, makna ditulis eksplisit). **Sensitivitas biaya**: ulangi expectancy pada biaya stres 2× (0,95→1,90) sebagai robustness — spread melebar saat spike; biaya flat = asumsi termurah. **Tafsir TERKUNCI (audit R4 A-1)**: kill HANYA di biaya 0,95; hasil stres 2× dilaporkan sebagai batas ketahanan, TIDAK punya daya bunuh. Mean net (0,95) ≤ 0 atau CI95 lewati 0 → GUGUR sebagai kandidat trade.
- Lolos lapis-1 saja = pola ada, belum tradeable. Lolos keduanya = layak masuk EDA-08 (entry).
- **SCOPING VONIS (TERKUNCI, temuan H-A2)**: GUGUR di ronde ini HANYA mematikan hipotesis fade-standalone. Status fitur spike di registry amunisi ANN diputus TERPISAH (pola univariat-mati bisa hidup kondisional dalam model multivariat). Vonis dilarang mengklaim "spike tidak berguna untuk ANN".

## 7. Pre-flight coder (F-style, verifikasi benar — bukan asal lolos)

- F1: reproduksi `2116` + `270` dengan kode scan EDA-06 verbatim sebelum ekstensi — Dikerjakan DULU (fondasi semua check). **STOP bila gagal.**
- F0a: laporkan split exact per ambang + verifikasi DUA persamaan rekonsiliasi: (i) `n(2,0)+n(1,5) = 2116` (sum check vs total F1); (ii) `n(2,0)+n(1,5)−overlap = Nunik` (dedup check, overlap = jumlah pasangan window-overlap). (KOREKSI 2026-10-15 atas STOP coder: versi lama menulis RHS=2116 untuk persamaan (ii) — salah aritmetika untuk overlap>0, bertentangan dengan §3. Putusan: opsi (a) SAH, RHS→Nunik. Data pre-flight terukur: n(2,0)=856, n(1,5)=1260, overlap=484, Nunik=1632; 856+1260=2116 ✓, 856+1260−484=1632 ✓.) **STOP bila gagal.**
- F0b: dedup terverifikasi (tiap event unik tepat satu band; matriks overlap + susut 2116→Nunik dilaporkan + distribusi ukuran grup union-find dilaporkan eksplisit: jumlah grup ukuran-1 vs ukuran-2 vs >2 — klaim "semua berukuran 2" atas total grup DILARANG tanpa rincian ini). **STOP bila gagal.**
- F2: SATU contoh tiap status akhir (reversal-A / continuation / timeout) dengan alasan benar. **STOP bila gagal.**
- F3: bandingkan CI cluster-per-day vs CI naive pada sampel klaster, LAPORKAN keduanya + arah selisih (sanity anti-iid — **lapor-saja, BUKAN stop**: korelasi negatif intra-hari yang legitimasi menghasilkan CI lebih sempit).
- F4 (seed): coder melaporkan seed EDA-06; cocok dengan 20261006 → pakai **20261006** (konsistensi); tidak cocok → seed tanggal baru + tulis "seed baru independen" sebagai alasan. Salah satu cabang tercatat di blueprint final. (B=10000, TERKUNCI.) **STOP bila seed tak tercatat.**
- F5 (drop): jumlah spike tanpa ruang-16-bar dilaporkan per band + per jam. **Lapor-saja.**
- F6 (null): konstruksi null tertulis di laporan pre-flight SEBELUM eksekusi, wajib memuat 6 butir checklist — hilang satu = STOP (TERKUNCI audit R4 A-2, menggantikan penilaian subjektif "hand-wavy"): (1) apa yang dipermutasi (label outcome / posisi trigger / arah); (2) populasi apa (semua spike unik / per band / per sesi); (3) jumlah permutasi; (4) seed; (5) statistik yang diukur (reversal rate / mean net); (6) cara p-value dihitung (proporsi null ≥ real, satu-arah).
- A-checks (assertion runtime generator; crash = sinyal bug, BUKAN stop prosedural): A1 `|rasio| ≤ 1+eps` (§2); A2 rekonsiliasi taksonomi per band: `n_rev + n_cont + n_timeout == n_band` (TERKUNCI audit R4 C-3 — taksonomi harus exhaustive & mutually exclusive, crash bila tidak).
- Prinsip: gagal check STOP = STOP + lapor, bukan improvisasi. Check lapor-saja tidak menghentikan ronde.

## 8. Gate & disiplin (warisi EDA-06)

Preregistrasi penuh; ambigu → STOP; assertion crash dibiarkan crash; deterministik (seed §7-F4); notebook = artefak generator (`nbconvert --execute` exit 0); reuse `broker_time`/resample; `venv/Scripts/python.exe`; arsip 06-07 frozen; P tidak tersentuh; §8A.3 (ronde baru hanya atas perintah user).

## 9. Deliverables & Done

- `scripts/_build_eda07_spike_anatomy.py` (nama deskriptif — JANGAN pakai `_build_eda07*.py` polos, tertukar arsip) + `notebooks/scalping/eda_07_spike_anatomy_outcome.ipynb` (14± sel, exit 0) + parquet event (kolom wajib: `mag_cont`, `band`, `has_exhaustion`, `r_bar`, `first_of_day`, flag drop + alasan) + tabel rate per band/stratum + tabel Q1-sub/Q3-sub + laporan coder (termasuk §7-F6 + catatan live-applicability tiap aturan drop; KONSEKUENSI TERKUNCI audit R4 B-5: aturan yang tak bisa direplikasi live ⇒ hasil hanya sah untuk subset yang bisa direplikasi — subset untuk validasi ANN berikutnya DITANDAI eksplisit) + kurva magnitudo-vs-rate + CI.
- Done = semua deliverable ada + F0–F2/F4/F6 hijau + F3/F5 dilaporkan + vonis tertulis (LOLOS/GUGUR per lapis + sel eksploratori + klausul scoping §6) + commit selektif setelah review.

## 10. Risiko / jebakan terdaftar

1. Double-count antar-scan (→ dedup §3 + Cek-0b). 2. Korelasi intra-hari (→ cluster-CI). 3. Multiple testing (→ hierarki + FDR, eksploratori ≠ vonis). 4. Campur level rate-vs-biaya (→ kill dua lapis). 5. Creep scope: TF lain / partisi lain / entry test (→ DITOLAK di ronde ini, catat sebagai EDA-08/09/robustness). 6. Threshold 1,5× = grey zone (→ agnostik, uji bukan asumsi). 7. Tie intra-bar (→ §3, TERKUNCI). 8. Bias drop sore-hari (→ lapor per jam, §3). 9. Label sesi/jam 5 hari anomali (→ eksklusi §4, patuh TASKS-245). 10. Look-ahead ujung-spike (→ entry s+1 §6; fitur turunan-s = lagged-causal, ANN live butuh end-detector). 11. Vonis meracuni registry (→ scoping §6). 12. Null tak terdefinisi (→ F6). 13. Band bisu di titik panas (→ fallback §3). 14. Train-serve skew (→ live-applicability §9). 15. Cliff band untuk ANN (→ mag kontinu §3). 16. Tafsir kill-vs-stres (→ TERKUNCI: kill hanya 0,95, §6). 17. Ekstensi cross-day (→ dilarang §3). 18. Split tanpa referensi run (→ rekonsiliasi internal F0a §7). 19. Median tanpa metode CI (→ percentile bootstrap §2).

## 11. Keputusan reviewer (TERKUNCI 2026-10-15)

(a) Tepi band tetap 1.5/2.0/2.5/3.0. (b) Tie → continuation menang. (c) Spek lapis-2 + SL buffer 0,5×`atr_s` eksplisit + prefilter 2,85. (d) B=10000, seed 20261006 bila cocok / seed baru independen + F4. (e) FDR q=0,10. + Drop-16-bar lapor (bukan stop). + Q1-sub & Q3-sub agregat+band saja. + 10 butir kunci. + 16 temuan audit adversarial (§12): 1 FATAL + 4 HIGH wajib, 7 MED + 4 LOW diterima semua ("Terapkan semua"). + Audit ronde-4 (§13): 4 material + 5 medium diterapkan; 3 low: C-2/C-3 diterapkan, C-1 DITOLAK-dengan-modifikasi (two-tier clamp-dalam-eps/crash-melebihi-eps — skip-diam dilarang karena melanggar disiplin assertion); +1 perbaikan di luar teks audit (rekonsiliasi internal F0a: split per ambang tak punya referensi run EDA-06).

## 12. Jejak audit adversarial mandiri (2026-10-15)

Commander menyerang draf dari sudut metode, kesesuaian EDA-06, dampak ANN, dan keketatan aturan. Temuan → perbaikan (semua masuk di atas): F-A1 entry close(s)→close(s+1) (§6); H-A2 klausul scoping vonis + tag lagged-causal (§3/§6/§9); H-A3 F3 stop→lapor, STOP keras = F0a/F0b/F1/F2/F4/F6 (§7); H-A4 F6 spesifikasi null (§5/§7/§9); H-A5 flag `has_exhaustion` + cross-tab (§3/§5/§9); M-A6 sensitivitas biaya 2× (§6); M-A7 fallback pool [2.5+) (§3); M-A8 rasional prefilter 2,85 (§6); M-A9 live-applicability (§3/§9); M-A10 CI median Q-sub (§2); M-A11 mag kontinu, band pelaporan (§3); M-A12 caveat 379-vs-384 (§4 — SELESAI via koreksi 2026-10-15: 384 bersih dipakai seragam); L-A13 assert |rasio|≤1+eps (§2); L-A14 split per-tahun (§5); L-A15 rasional jendela-16 (§3); L-A16 arah seleksi first-of-day (§3).

## 13. Jejak audit ronde-4 (2026-10-15)

Audit eksternal, verifikasi Commander per butir ke blueprint/kode: A-1 (ambiguitas kill-vs-stres → tafsir A: kill hanya 0,95 §6); A-2 (F6 subjektif → checklist 6 butir §7); A-3 (ekstensi cross-day → dilarang, sesuai `j >= n: break` EDA-06 §3); A-4 (fallback berjenjang §3); B-1 (urutan F1→F0a §7); B-2 (metode percentile bootstrap median §2); B-3 (`bar_ke = idx−s` §2); B-4 (`eps = 1e-6` §2); B-5 (konsekuensi live-applicability §9); C-2 (bias Asia eksplisit §3); C-3 (assert rekonsiliasi taksonomi §7). C-1 DITOLAK-dengan-modifikasi (alasan §2). Perbaikan sendiri di luar teks: F0a rekonsiliasi internal (split tak punya referensi run). Audit menyatakan 0 FATAL — Commander konkuren. Nasihat audit ("blueprint 95% dieksekusi > 100% tak jalan", tanpa ronde-5) dicatat dan disetujui sebagai prinsip penutup.
