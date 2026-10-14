# Spec Discovery-R1 — Event-First Scalping USDJPY (Arsitek, 2026-10-13)

Status: SPEC EKSEKUSI (R-1..R-7 diratifikasi user 2026-10-13) +
AMANDEMEN-1 (paket A-A-Kunci, re-audit fokus LULUS ketiga butir
2026-10-13) + AMANDEMEN-2 minor (5 pengetatan C1–C5, disetujui user
2026-10-13). Spec ini TIDAK mengotorisasi kode, eksperimen, config,
staged file, commit, paper order, atau live trade.

Dasar: `.ai/backup/2026-10-09_DESAIN_FRESH_SCALPING_EVENT_FIRST.md` (613
baris, dibaca penuh). Semua nomor § di bawah merujuk dokumen itu kecuali
dinyatakan lain.

Prinsip: tulis dulu baru lihat (anti-obok-obok), biaya 3 lapis, satu
putaran satu vonis (S8A AGENTS.md).

## R-0. Titik keputusan (§18 desain + 3 tambahan) + Amandemen-1

| # | Titik | Nilai | Status |
|---|---|---|---|
| R-1 | E1/E2/E3 satu-satunya ruang R1? | YA, tanpa keluarga ke-4 | MENGIKAT |
| R-2 | Split 2024 cari / 2025 uji / 2023-H2 robustness / 2023-H1+2026 keluar? | YA, verbatim §5.2 | MENGIKAT |
| R-3 | Jalur P0->P1->P2, izin user tiap transisi? | YA, verbatim §11 | MENGIKAT |
| R-4 | Bukti (harness/JSON/stdout/hash) masuk repo sebelum auditor? | YA, verbatim §12 | MENGIKAT |
| R-5 | Otoritas spread: terukur per-sesi + stres p95/p99, buang default 1.5? | YA (lihat D-3.3) | MENGIKAT |
| R-6 | Komisi 1 USD/lot = 0,3 pip round-turn (asumsi per-side) sampai klarifikasi? | YA (lihat D-3.3) | MENGIKAT |
| R-7 | Lampiran deskriptif 8 pola + M15 (D-8)? | YA — murni deskriptif, TANPA konteks primer (Amandemen-1 A-H3 opsi a) | MENGIKAT |

Amandemen-1 (paket A-A-Kunci, disetujui user 2026-10-13):

| # | Temuan audit | Keputusan |
|---|---|---|
| A-H1 | H1: "bar M15 yang memuat t0 (selesai)" mustahil pada decision tepat setelah t0 close | Opsi (a): bias M15 = arah bar M15 TERAKHIR YANG SELESAI pada atau sebelum t0 (lihat D-8.2) |
| A-H2 | H2: family 6 sel vs 252 varian selectable (grid x 7 horizon x 6 ladder); "net-observed" tak terdefinisi vs horizon/ladder | Setting evaluasi DIKUNCI: horizon +10 M1 dari t0 close, barrier TP 2,5 / SL 2,5 pip. Q1 horizon lain + Q2 anak-tangga lain = pemetaan deskriptif, TIDAK boleh mengangkat kandidat. Kriteria KANDIDAT = pooled median net-observed > 0 + CI cluster-hari mengecualikan 0 + tanda sama di 2024-H1 dan 2024-H2 + failure map lengkap (lihat D-4.4) |
| A-H3 | H3: D-4.2 (M15 konteks primer) vs D-8 (lampiran dilarang memilih kandidat) saling meniadakan; kontradiksi diwarisi persetujuan log:1820 | Opsi (a): M15 STRICT deskriptif di R1. R1 TANPA pemisahan konteks primer (desain meminta batas, bukan obligasi memilih — desain:296-298). Larangan D-8 berlaku penuh tanpa pengecualian |

R-1 s/d R-7 + A-H1 s/d A-H3 mengikat sejak persetujuan paket user
2026-10-13, dengan hak veto baris-per-baris tetap terbuka (S1A).

Amandemen-2 minor (5 pengetatan atas catatan re-audit C1–C5, disetujui
user 2026-10-13; semuanya menghapus derajat bebas, tanpa angka
alternatif):

| # | Catatan | Pengetatan (lihat butir terkait) |
|---|---|---|
| A-C1 | C1: seed bootstrap tak ditetapkan | Seed = 1337, beku pra-run; tercatat di ledger sebelum run; ganti seed = ronde baru (D-4.4) |
| A-C2 | C2: batas family correction tak eksplisit | E1 = 1 family isi 6 sel; E2 = 1 family isi 1 sel; E3 = 1 family isi 1 sel (D-4.2) |
| A-C3 | C3: metode correction tak dinamai | Keputusan tanpa p-value; butir (ii) memakai CI; kontrol multiplicity lewat penguncian + pra-registrasi (D-4.4) |
| A-C4 | C4: tabel M15-bias permukaan baca | Tabel lampiran DISEGEL; dibuka hanya setelah vonis KANDIDAT beku (D-8.3) |
| A-C5 | C5: konvensi resample tak eksplisit | Resample via `src/data/resample.py`, diverifikasi coder di ledger (D-8.2) |

## D-1. Ruang Discovery-R1 (satu-satunya)

Maksimal tiga keluarga, satu kandidat per keluarga keluar dari 2024
(§9.2). Ronde ini tidak boleh menambah keluarga ke-4.

### E1 — Exhaustion-to-reversal (diusulkan operasional)

Mekanisme: setelah dorongan satu arah yang meluas, apakah reversal yang
selesai pada t0 close menghasilkan gerak berlawanan cukup besar sebelum
adverse move dan biaya?

Grid pra-registrasi (kecil, satu family untuk correction):
- N = {4, 5, 6} bar M1 tutup searah berturut-turut sebelum t0.
- D = {2,5; 3,5} pip signed displacement atas N bar.
- t0 = bar berlawanan arah, body >= 50% range bar itu.

Aturan kapasitas: sel grid dengan < 300 event di 2024 GUGUR dari
evaluasi (dilaporkan sebagai dropped, bukan di-tuning).

Bersarang diakui (M4): 6 sel E1 bersarang (N bertingkat, D bertingkat)
— uji efektif < 6; correction atas 6 = konservatif, diterima.

Falsifikasi (§7): reversal baru diketahui sesudah future swing
terbentuk, atau MFE tidak melewati biaya/MAE horizon pendek.

### E2 — Pullback-then-continuation (diusulkan operasional)

Mekanisme: setelah expansion masa lalu, apakah pullback kecil yang
selesai pada t0 lebih sering kembali searah dorongan sebelum invalidasi?

Parameter pra-registrasi (SATU sel, tanpa grid — koreksi label M5;
aturan threshold tunggal selama ini salah disebut "grid"):
- Expansion: displacement 20 bar >= 1,0 x ATR(14) M1 yang selesai.
- Pullback: retrace <= 40% range expansion, <= 5 bar.
- t0 = tutup searah dorongan awal.

Keterbatasan yang diterima (M5): tanpa variasi threshold, kegagalan
E2 tidak bisa membedakan "mekanisme mati" vs "ambang salah".
Diagnosisnya = failure map (Q4). Tidak ada penambahan threshold
pasca-hasil.

Aturan kapasitas: sama (min 300 event/sel).

Falsifikasi (§7): arah awal memakai future high/low, atau net outcome
tidak mengalahkan biaya stres.

### E3 — Compression-to-expansion (diusulkan operasional)

Mekanisme: setelah kompresi selesai, apakah break pada t0 punya
continuation netto sebelum false break/adverse barrier?

Parameter pra-registrasi (SATU sel, tanpa grid — koreksi label M5):
- Kompresi: range 30 bar <= 0,5 x median 20 window sebelumnya yg selesai.
- Break: tutup di luar edge >= 1,0 pip pada t0.

Keterbatasan yang diterima (M5): tanpa variasi threshold, kegagalan
E3 tidak bisa membedakan "mekanisme mati" vs "ambang salah".
Diagnosisnya = failure map (Q4). Tidak ada penambahan threshold
pasca-hasil.

Aturan kapasitas: sama (min 300 event/sel).

Falsifikasi (§7): break memakai range sesudah t0, atau barrier race net
tidak lebih baik dari baseline unconditional.

### Larangan bersama E1-E3 (§7, verbatim)

RSI, MACD, EMA, candle-name, atau pola vendor tidak ditambahkan hanya
karena populer. Pengecualian sah: representasi sekunder bila mekanisme
telah menemukan effect DAN menambah informasi pada holdout tanpa
kebebasan tersembunyi. Lampiran D-8 adalah deskripsi, bukan pengecualian
ini.

## D-2. Split temporal (§5.2, verbatim + tambahan proyek)

| Blok | Peran | Boleh | Dilarang |
|---|---|---|---|
| 2024 | Discovery utama | Ledger, outcome mapping, maks 1 kandidat/keluarga | Klaim edge; pakai 2025 untuk menyetel |
| 2025 | Confirmation | Uji kandidat + kontrak beku | Pilih event/threshold/jam/horizon/barrier baru |
| 2023-H2 | Replikasi mundur | Uji transportabilitas setelah 2024->2025 selesai | Menyelamatkan kegagalan 2025 |
| 2023-H1 | Keluar denominator | Analisis regime terpisah | Menjadi penentu kelulusan |
| 2026 | Tidak digunakan | Tidak ada | Semua discovery/confirmation/paper |

Tambahan proyek (spesifik repo ini, MENGIKAT): jendela anomali
2024-10-28..11-01 + regime SA-03 KELUAR dari denominator Discovery-R1 —
tanpa batas waktu, tanpa syarat re-entry di ronde ini. Re-entry hanya
lewat ronde baru + ledger baru (anti-rescue, koreksi M9). Alasan:
status keduanya BELUM TERVERIFIKASI (STATE.md). (Koreksi L3: jendela
2026 dihapus dari daftar ini — 2026 sudah keluar penuh per tabel di
atas; penyebutan ganda SA-03 dihapus.)

Sumber: USDJPY M1 (event + outcome mikro); M5/M15 hanya konteks pada
atau sebelum t0; harga+spread tervalidasi proyek; raw immutable; tiap
turunan manifest SHA-256.

## D-3. Kontrak outcome dan eksekusi (§8)

### D-3.1 Timestamp

t0 close = penutupan bar event (semua feature keputusan tersedia).
Decision = tepat setelah t0 close (catat UTC + broker time). Entry =
OPEN bar t0+1 — penguncian operasional (koreksi M3; frasa lama "bar/tick
pertama realistis" GUGUR karena tak teraudit). Semua horizon Q1 diukur
dari t0 close. Exit = SL/TP/time-stop/cancel yang didefinisikan
sebelumnya.

Urutan ambigu (dua barrier satu bar tanpa urutan bid/ask) = label
AMBIGUOUS_SEQUENCE. Perlakuan (diusulkan, dikunci sebelum confirmation):
BUANG dari evaluasi dengan hitungan eksplisit. Tidak dihitung win/loss
diam-diam.

### D-3.2 Sisi harga (verbatim)

BUY entry ASK exit BID. SELL entry BID exit ASK. Spread nol dilarang.
Close mid untuk entry/exit dilarang.

### D-3.3 Biaya 3 lapis (angka diusulkan — R-5/R-6)

1. Observed: spread event-time per event + komisi (R-6).
2. Conservative: observed + slippage 0,2 pip (ASUMSI skenario — tidak
   terukur dari OHLC; sumber: keluarga +0/+0,1/+0,3 _build_eda06.py:70;
   skenario tengah dipakai sebagai konservatif).
3. Stress: spread p95 sesi + slippage 0,3 pip (ASUMSI, skenario atas) +
   komisi.

R-5: spread observasi = mean terukur per sesi, literal config
`spread.cost_basis.by_session` (fallback `cost_basis.default` bila sesi
tak terpetakan) — koreksi M7: kunci literal ini yang dipakai coder,
bukan `spread.default`. Stres = `spread.stress_bands.p95.by_session`.
`spread.default: 1.5` dan `by_year[2023]: 3.0` TIDAK dipakai ronde ini.
`stress_multiplier: 2.0` TIDAK dipakai di R1 — p95 bands sudah
merupakan skenario stres; penggandaan ganda dilarang (M8).

R-6: komisi = 0,3 pip round-turn (1 USD/lot, asumsi per-side, kurs
~150). Rumus dicatat; angka final menunggu klarifikasi user.

Kandidat tidak pernah lulus dari gross saja. Observed net positif tapi
stress net negatif = tertinggi TAHAN, bukan edge.

### D-3.4 Output minimum per event (§8.3 verbatim)

Arah+identitas event; semua feature pra-t0; bid/ask entry-exit (atau
transformasi rekonstruksibel); gross/net; MFE, MAE, time-to-MFE/MAE;
outcome horizon tetap; barrier pertama atau AMBIGUOUS_SEQUENCE; label
sesi, spread, skenario biaya, tahun, broker-day; cluster/day id + alasan
cancel/reject.

## D-4. Discovery 2024

### D-4.1 Ledger (ditulis SEBELUM run, §9.1)

Kolom wajib: event_id, mekanisme, definisi informasi-sampai-t0, arah,
feature diizinkan, outcome, biaya, horizon, unit bootstrap, eksklusi,
alasan ilmiah, status. Event tidak boleh lahir dari contoh chart
setelah outcome terlihat.

### D-4.2 Batas eksplorasi (§9.2 + Amandemen-1 A-H3 opsi a)

R1 TANPA pemisahan konteks primer. Larangan perkalian bebas tetap
berlaku: bukan event x cost x session x day x volatility x location
sekaligus. Parameter hanya grid kecil D-1: E1 = satu family isi 6
sel; E2 = satu family isi 1 sel; E3 = satu family isi 1 sel (A-C2),
SATU setting evaluasi beku (D-4.4), dan SATU paket barrier
beku (Q2). Desain meminta batas eksplorasi, bukan obligasi memilih satu
konteks (desain:296-298) — maka opsi (a): tidak ada yang dipilih,
larangan D-8 berlaku tanpa pengecualian. (Kalimat lama "Satu konteks
primer per kandidat: M15-bias" GUGUR bersama H3.)

### D-4.3 Kamus pertanyaan (Q0-Q5, §6)

Q0 coverage (observability per tahun/hari/sesi/spread; zero-return, gap,
overlap) + GERBANG KAPASITAS: hitungan event per sel/hari DULU; sel <
300 event di 2024 GUGUR dari evaluasi (dilaporkan dropped, bukan
di-tuning). Q1 displacement gross+net horizon +1/+2/+3/+5/+10/+15/+20
M1, MFE/MAE, proporsi MFE>biaya, median+quantile — evaluasi KANDIDAT
memakai SATU setting beku: horizon +10 M1 dari t0 close (A-H2, alasan:
tengah antara mikro dan drift; dikunci sebelum data dibuka, bukan
dipilih pasca-hasil); horizon lain deskriptif saja, TIDAK boleh
mengangkat kandidat. Q2 barrier race (ladder dipetakan: TP {1,5; 2,5;
4,0} pip x SL {1,5; 2,5} pip — pemetaan deskriptif saja); paket evaluasi
BEKU: TP 2,5 / SL 2,5 pip (A-H2; alasan: simetris-netral, di atas biaya
~1,2 pip). Aturan pemilihan = TIDAK ADA pemilihan: paket beku, bukan
dipilih pasca-hasil (koreksi M6; frasa lama "SATU paket dikunci sebelum
confirmation" GUGUR karena membuka jendela seleksi). Q3 konteks pra-t0
(path return, expansion/compression vs baseline selesai, lokasi vs
high/low rolling selesai, spread+percentile masa lalu, bucket waktu,
satu kategori volatilitas; rv_regime_flag/TAU TERLARANG). Q4 failure
map (wajib; tidak memberi hak membuang sel buruk lalu klaim subset).
Q5 stabilitas (arah 2024 vs 2025, unit hari, stres, kontribusi
satu-hari/sesi; negatif = tolak/tahan, bukan tuning).

### D-4.4 Keluaran discovery (tepat satu, §9.3)

TOLAK (tidak ada displacement netto tereksekusi) / KANDIDAT (mekanisme
+ effect layak pra-registrasi) / BELUM JELAS (data/urutan/barrier tak
cukup; bukan alasan tuning). Hanya KANDIDAT masuk confirmation spec.
Kandidat bukan strategi sebelum lulus confirmation.

Kriteria KANDIDAT operasional (Amandemen-1 A-H2, MENGIKAT; kriteria
lama "mayoritas day-block" GUGUR bersama H2/M1): pada setting beku
(horizon +10 M1 dari t0 close, barrier TP 2,5/SL 2,5, observed net),
SATU sel grid DINYATAKAN KANDIDAT bila SEMUA terpenuhi: (i) pooled
median net-observed > 0; (ii) interval kepercayaan 95% bootstrap
cluster-hari (preseden nb04: 10.000 resample jaga-cluster) mengecualikan
0 di sisi positif — menggantikan "mayoritas day-block" yang tak
bermakna pada ~1,2 event/hari/sel; (iii) tanda pooled median SAMA di
2024-H1 dan 2024-H2 (uji stabilitas internal atas belahan kalender,
bukan subset pasca-hasil — bukan tuning); (iv) failure map lengkap
(Q4). Gerbang kapasitas Q0 berlaku DULU: sel < 300 event tidak dinilai
sama sekali. Seed bootstrap 10.000 resample = 1337: beku, tercatat di
ledger SEBELUM run; perubahan seed = ronde baru (A-C1). Metode
multiplicity (A-C3): tidak ada uji p-value dalam keputusan KANDIDAT;
butir (ii) memakai CI bootstrap; kontrol multiplicity lewat penguncian
setting + pra-registrasi + kriteria 4-syarat. Tidak ada koreksi p-value
karena tidak ada p-value. Ambang tetap judgment arsitek, terbuka veto
(S1A).

## D-5. Confirmation 2025 (per kandidat, spec terpisah)

Spec confirmation wajib 10 butir §10 (hash/manifest/HEAD; definisi+arah
+timestamp; entry/cancel/stop/target/time-stop/AMBIGUOUS; bid-ask+3
lapis+rumus P&L; horizon penentu + SATU metrik primer; unit
cluster-day/embargo+interval; tahun beku; syarat lulus/gugur — stres,
min hari, sign, stabilitas; baseline pra-2025: unconditional
direction-neutral atau event-time shuffle jaga-cluster; larangan:
tuning, subset baru, 2026, H4 rescue, RV/TAU, statistik penentu
tambahan).

Gate G1-G7 (§10.1 verbatim): Causal, Executable, Sequence,
Dependence, Temporal, Robustness, Operational. Gagal satu = GUGUR.
Tanpa voting.

Coder eksekusi; auditor replikasi dari nol tanpa impor artefak coder;
arsitek vonis setelah sepakat atau arbitrase berbukti.

## D-6. Jalur paper P0->P1->P2 (§11, R-3)

P0 replay offline (deterministik 2x byte-identik; mutasi 1 bar pasca-t0
tidak mengubah sinyal t0; tanpa order). P1 shadow real-time (tanpa
order; rekonsiliasi harian log-vs-replay; tanpa adaptasi parameter;
angka minimum dikunci sebelum P1). P2 paper/demo 0,01 lot (hanya atas
izin eksplisit; tanpa martingale/grid/averaging; stop bila mismatch,
log hilang, biaya > guard, fill tak terekonsiliasi). Transisi tiap
tahap butuh keputusan user. Lolos P2 BUKAN izin live (§11.5).

Strategy contract mengikuti §11.1 bila kandidat lulus; tanpa diskresi
tak terdefinisi.

## D-7. Rantai bukti (§12, R-4)

Telemetri minimum §12 per keputusan. Raw log append-only rotasi
bulanan. Manifest hash keluar SEBELUM run. Script+harness+JSON+stdout
di repo evidence (`reports/research/2026-10-13/discovery-R1/evidence/`)
sebelum auditor mulai — bukan folder temp. Laporan pisahkan fakta log,
turunan, interpretasi. Logging gagal = run gagal.

Artefak mengikuti §14 (folder discovery/confirmation/paper terpisah;
tidak campur bukti).

## D-8. Lampiran deskriptif: 8 pola + M15 (MENGIKAT, R-7)

Otoritas: persetujuan user 2026-10-13 (log:1820) atas usulan arsitek
R-7 — BUKAN derivasi §7 desain (koreksi L1: §7 hanya melarang
indikator; lampiran ini berdiri di atas R-7).

Kedudukan: deskripsi SAJA. Tanpa vonis, tanpa ambang, tanpa pemenang.
Keluaran = tabel hitungan mentah. Hasilnya boleh melahirkan hipotesis
ronde-2 (yang bila diuji lewat 7 gerbang penuh sebagai kandidat baru).
Tidak boleh dipakai memilih/menyetel kandidat R1.

### D-8.1 Delapan pola (definisi operasional M1, pra-registrasi)

| # | Pola | Definisi (bar t0 vs t-1) |
|---|---|---|
| P1 | Engulfing | Body(t0) menelan body(t-1) + range(t0) >= 1,5 x median range 20 bar; arah dicatat |
| P2 | Hammer | Lower wick >= 2 x body, upper wick <= 0,5 x body, tutup setengah atas range |
| P3 | Shooting star | Cermin P2 (upper wick dominan, tutup setengah bawah) |
| P4 | Three white soldiers | 3 tutup naik beruntun, tiap body > 0, tiap tutup > tutup lalu |
| P5 | Three black crows | Cermin P4 |
| P6 | Doji | Body <= 10% range |
| P7 | Harami | Body(t0) dalam body(t-1) + range(t0) <= 0,6 x range(t-1) |
| P8 | Marubozu | Total wick <= 10% range, body searah |

Definisi di atas adalah usulan arsitek yang ikut terkunci saat
ratifikasi (R-7 sudah setuju prinsipnya; angka boleh diveto).

### D-8.2 Satu variabel latar M15 (deskriptif SAJA — A-H3 opsi a)

Bias M15 = arah bar M15 TERAKHIR YANG SELESAI pada atau sebelum t0
(A-H1 opsi a; definisi lama "bar yang memuat t0 (selesai)" GUGUR karena
mustahil fisik pada decision tepat setelah t0 close): SEARAH /
BERLAWANAN / DATAR (|return| < 0,5 pip — ambang diusulkan, terbuka
veto). Return = close-to-close bar M15 selesai tersebut. Resample
M1→M15 memakai `src/data/resample.py` (konvensi proyek: boundary sesi
+ offset broker); coder verifikasi di ledger (A-C5). Variabel ini
MURNI inventarisasi: dihitung, DILARANG dipakai memilih/menyetel
kandidat R1 (A-H3). Bukan konteks primer — R1 tidak punya (D-4.2).

### D-8.3 Jendela inventarisasi + keluaran

SEBELUM = 5 bar M1 pra-t0; SAAT = bar t0; SESUDAH = 5 bar pasca-t0
(deskriptif; tidak dipakai vonis). Keluaran: tabel hitungan pola x
jendela x keluarga-E + tabel M15-bias x keluarga-E. Tanpa uji
signifikansi sebagai alat keputusan. Tabel lampiran DIHITUNG dan
DISEGEL; dibuka hanya setelah vonis KANDIDAT R1 dibekukan (A-C4) —
anti-pembacaan-dini yang dulu memicu H3.

Catatan jujur (§17 desain putaran 2): sebagian pola bernama kemungkinan
reduksi dari ukuran E1-E3 (body/range/run-length). Bila terbukti, itu
temuan sah — memetakan dongeng ke ukuran.

## D-9. Sukses dan berhenti (§16)

Sukses sah: (a) kandidat net terkonfirmasi temporal + tereksekusi via
P0/P1; (b) bukti kuat ketiga mekanisme tak membayar biaya; (c)
diagnosis integritas data/eksekusi. Berhenti/reset: E1-E3 gagal G1/G2
di 2024; evidence/reproduksibilitas rusak; barrier tak tertentukan
proporsi material; biaya hapus semua displacement; 2025 tak mendukung;
discovery butuh fitur melewati budget demi satu positif. "Tambah
indikator" bukan respons default.

## D-10. Kontrak anti-rescue H4 (§2 verbatim)

Lima butir §2 berlaku penuh: H4 tak memilih event baru; H4 hanya kolom
deskriptif pasif; spread/volatilitas/pullback/lokasi = hipotesis baru
bukan subset H4; tanpa tukar median/mean, pool/sel, tahun/sesi,
gross/net pasca-hasil; gagal kandidat tak membuka varian segera.

## D-11. Larangan ronde

Tanpa tuning; tanpa subset baru pasca-hasil; tanpa 2026; tanpa H4
rescue; tanpa filter RV/TAU; tanpa statistik penentu tambahan; tanpa
ronde lanjutan atas inisiatif AI (S8A); tanpa lompat ke live.

## D-12. Self-audit desain spec ini (3x, ringkas)

Putaran 1 — Correctness: scope E1-E3 terkunci; split verbatim §5.2 +
anomaly/SA-03 keluar; bid/ask kontrak; ambigu dibuang-terhitung;
ledger sebelum run; satu metrik primer per kandidat (di confirmation
spec); evidence repo sebelum auditor.

Putaran 2 — Bias/asumsi (pasca-Amandemen-1): grid kecil + correction
per family; kapasitas min 300 + gerbang Q0 + CI cluster-hari (anti
sel-tipis-menang, M1); setting evaluasi beku H+10/TP2,5/SL2,5 tanpa
pemilihan (A-H2, M6); failure map wajib; E1 bersarang diakui,
correction konservatif (M4); E2/E3 satu-sel, keterbatasan diterima
(M5); entry open t0+1, horizon dari t0 close (M3); slippage = ASUMSI
berlabel, multiplier 2,0 tidak dipakai (M8); literal config dikunci
(M7); denominator beku tanpa re-entry ronde ini (M9); lampiran tanpa
vonis atas otoritas R-7 (L1); komisi konservatif (per-side) sampai
klarifikasi.

Putaran 3 — Meta-check: spec ini otorisasi NOL eksekusi; R-1..R-7 +
A-H1..A-H3 mengikat dengan veto terbuka; folder evidence
`reports/research/2026-10-13/discovery-R1/evidence/` — deviasi dari
§14 dicatat sadar: §14 mencontohkan folder `discovery/` generik tanpa
tanggal, repo ini memakai tanggal-per-ronde agar artefak ronde tak
bercampur (L5); kriteria berhenti eksplisit; satu ronde satu vonis.

## D-13. Yang diminta sekarang (pasca-Amandemen-2)

Spec + Amandemen-1 + Amandemen-2 = SAH sebagai basis eksekusi
(re-audit fokus LULUS ketiga butir 2026-10-13; veto user atas
Amandemen-2: tidak ada — disetujui paket).

Langkah berikutnya (§15 desain langkah 3): CODER eksternal eksekusi
discovery 2024 berbekal brief
`.ai/assistant/prompts/2026-10-13_eksekusi-discovery-R1-coder.md`.
Urutan tetap: coder pulang membawa hasil + bukti → auditor replikasi
dari nol → arsitek vonis TOLAK/KANDIDAT/BELUM JELAS. Bila eksekusi
menemukan cacat spec: Amandemen-3, bukan jalan terus.
