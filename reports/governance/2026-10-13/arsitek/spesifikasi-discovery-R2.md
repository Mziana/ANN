# Spec Discovery-R2 — Event-First + Barrier ATR, Bed 2026-Holdout (Arsitek, 2026-10-13)

Status: SPEC EKSEKUSI (R2-1..R2-6 diratifikasi user 2026-10-13 paket
penuh, tanpa veto). Berikutnya (§15 desain langkah 3): AUDITOR eksternal
audit spec, lalu coder discovery 2026-holdout. Spec ini TIDAK
mengotorisasi kode, eksperimen, config, staged file, commit, paper
order, atau live trade.

Dasar:
- `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R1.md`
  (R1; yang TIDAK berubah diwarisi verbatim, dirujuk per nomor D-).
- EDA-06 (`scripts/_build_eda06.py:59,74-75,166-167`;
  `reports/eda/2026-10-10/T-06-7_gerbang_tercile.csv`, 144 irisan).
- Alasan lahir (tercatat SESSION_LOG 2026-10-13): kunci barrier R1
  (TP/SL tetap 2,5 pip = 25 point = 0,91x ATR) menyimpang dari desain
  original ATR dan menempati lingkungan terburuk EDA-06 (FIX_30_45:
  0/12, delta 8,03). Vonis TOLAK R1 sah untuk barrier tetap; desain
  ATR belum diuji di jalur event-first.

Prinsip: tulis dulu baru lihat; biaya 3 lapis; satu ronde satu vonis;
tanpa double-dip (bed 2026 belum tersentuh EDA-06 maupun R1).

## R2-0. Titik keputusan (butuh ratifikasi paket)

| # | Titik | Usulan arsitek | Status |
|---|---|---|---|
| R2-1 | Event tetap E1/E2/E3 definisi R1 D-1? | YA, tanpa perubahan, tanpa keluarga ke-4 | MENGIKAT |
| R2-2 | SATU paket barrier ATR: SL = 1,5 x ATR M5(14), TP = 2,0 x SL? | YA, kausal-beku resep EDA-06 (D2-2) | MENGIKAT |
| R2-3 | Bed uji = 2026-holdout minus anomali 10–27 Mar 2026? | YA (D2-3; 250.727 bar usable terukur) | MENGIKAT |
| R2-4 | Biaya 3 lapis + kontrak eksekusi sama dengan R1? | YA (D2-4, D2-5) | MENGIKAT |
| R2-5 | Kriteria KANDIDAT 4-syarat sama (seed 1337, paruh 2026)? | YA (D2-6) | MENGIKAT |
| R2-6 | Lampiran D-8 dihitung-ulang di 2026 + segel baru; segel R1 tetap? | YA (D2-8) | MENGIKAT |

Ratifikasi 2026-10-13 (user): "setuju" = SETUJU R2 paket penuh, tanpa
veto. Tabel di atas MENGIKAT sejak ratifikasi, veto tetap terbuka (S1A).

Disetujui paket = "SETUJU R2". Veto baris-per-baris tetap terbuka (S1A).

## D2-1. Event (diwarisi R1 D-1 verbatim)

E1 grid 6 sel (N{4,5,6} x D{2,5;3,5} + body >= 50%), E2 satu sel,
E3 satu sel, falsifikasi dan larangan indikator sama. E1 bersarang
diakui (correction konservatif atas 6). Tidak ada threshold baru.

## D2-2. Barrier ATR — satu-satunya perubahan (resep EDA-06 verbatim)

- ATR = ATR M5(14) dalam pip dari bar M5 TERAKHIR YANG SELESAI pada
  atau sebelum t0 (kausal; def `_build_eda06.py:497-508`), DIBEKUKAN
  saat entri, tidak berubah setelah entri.
- SL = 1,5 x ATR; TP = 2,0 x SL (= 3,0 x ATR). SATU paket, tanpa
  ladder, tanpa pemilihan (aturan pemilihan = TIDAK ADA).
- Cakupan kata "verbatim" (Amandemen-R2-1 C1): definisi ATR,
  kausalitas, pembekuan saat entri, dan aturan-buang
  ketersediaan (tiga bullet ini). Semantik sentuhan barrier
  MENGIKUTI D2-5 di bawah — BUKAN kontrak EDA-06 (`:73`), yang
  menghitung bar-kembar sebagai SL.
- Entry DIBUANG bila ATR tak tersedia / jendela menyeberangi gap /
  anomali / sesi Off — nol imputasi, jumlah buang dilaporkan
  (resep `_build_eda06.py:74-75`).
- Skala terukur (2024, acuan kasar): ATR M5(14) mean 6,74 pip → SL
  ~101 point / TP ~202 point (~4x stop R1). Angka 2026 dihitung
  coder di ledger, bukan dipinjam dari 2024.

## D2-3. Bed uji 2026-holdout (anti-double-dip)

- 2026: 269.846 bar M1 (01 Jan–02 Okt, terukur). EDA-06 memakai
  2023–2025 (`_build_eda06.py:69,147`) dan tak pernah memuat 2026
  (`:147` "2026 = holdout, TIDAK dimuat"); R1 memakai 2024. Maka
  2026 segar untuk DUA-DUANYA: pilihan k/RR dan pemetaan event.
- Eksklusi: 2026-03-10..03-27 (19.119 bar, BELUM TERVERIFIKASI) KELUAR
  denominator — tanpa batas waktu, tanpa re-entry ronde ini.
  Usable ~250.727 bar (92,9% dari 269.846 bar 2026 yang dimuat;
  ~70% terhadap tahun kalender penuh dengan cakupan sesi yang sama;
  basis ditulis eksplisit — Amandemen-R2-1 C5).
- Paruh stabilitas (MENGIKAT, Amandemen-R2-1 B4): tengah rentang
  usable — Paruh-1 = 2026-01-01 s.d. 2026-05-18; Paruh-2 =
  2026-05-19 s.d. 2026-10-02 (anomali 10–27 Mar sudah keluar dari
  keduanya). Coder menyalin batas ini ke ledger pra-run (bukan
  menghitung-ulang).
- Estimasi kasar E3 (densitas 2024): ~500–600 event — di atas gerbang
  300 tapi pas-pasan. Bila E3 < 300: GUGUR-dilaporkan (temuan, bukan
  tuning). Tanpa kompensasi ambang.
- DILARANG: 2024 / 2025 / 2023 untuk evaluasi; 2026 untuk ronde lain
  sebelum R2 selesai (satu bed satu ronde).

## D2-4. Biaya 3 lapis (sama dengan R1 D-3.3)

Observed / conservative (+0,2 ASUMSI) / stress (p95 + 0,3 ASUMSI) +
komisi 0,3 pip round-turn asumsi per-side. Literal config
`spread.cost_basis.by_session` + `spread.stress_bands.p95.by_session`;
`spread.default` / `by_year` / `stress_multiplier` DILARANG. Coder
melaporkan cakupan sesi-2026 di ledger (bila sesi tak terpetakan:
fallback `cost_basis.default` + laporkan — bukan diam-diam).

## D2-5. Kontrak eksekusi (sama dengan R1 D-3.1/D-3.2)

Entry OPEN bar t0+1; horizon dari t0 close; BUY ASK→BID / SELL
BID→ASK; spread nol dan mid dilarang; AMBIGUOUS_SEQUENCE = buang +
hitung eksplisit. First-passage dihitung pada bar SESUDAH bar entry
t0+1 (bar entry dikecualikan, mengikuti loop-dari-k=1 EDA-06); bar
yang menyentuh SL dan TP sekaligus = AMBIGUOUS_SEQUENCE (beda sadar
dari EDA-06 yang menghitungnya SL — Amandemen-R2-1 C1). Output
minimum per event = D-3.4.

## D2-6. Discovery (Q0–Q5 adaptasi, kriteria sama)

- Q0 coverage + GERBANG KAPASITAS 300 (sel < 300 tidak dinilai).
- Q1 horizon +1/+2/+3/+5/+10/+15/+20 dipetakan; evaluasi H+10.
  Horizon selain H+10 = pemetaan deskriptif saja, TIDAK boleh
  mengangkat kandidat (Amandemen-R2-1 B2).
- Q2 = SATU paket ATR (tanpa ladder; deviasi sadar dari Q2 R1 —
  aturan satu paket melarang permukaan seleksi).
- Q3 konteks pra-t0 (tanpa RV/TAU, tanpa M15); Q4 failure map wajib;
  Q5 paruh-2026.
- Kriteria KANDIDAT 4-syarat pada setting beku (MENGIKAT; setting
  beku = horizon +10 M1 dari t0 close, paket ATR tunggal, observed
  net — Amandemen-R2-1 B2): (i) pooled median
  net-observed > 0; (ii) CI 95% bootstrap cluster-hari 10.000
  resample seed 1337 mengecualikan 0 positif; (iii) tanda sama di
  paruh-1/paruh-2 2026; (iv) failure map lengkap. Seed 1337
  dipertahankan (kontinuitas determinisme; bed baru, pra-registrasi).
- Keluaran: TOLAK / KANDIDAT / BELUM JELAS per keluarga (tepat satu).
  KANDIDAT → confirmation spec terpisah (bed uji confirmation
  diputuskan saat itu; 2023+2024+2025 membawa caveat kontaminasi
  pemilihan k/RR EDA-06 — 2024 additionally terkontaminasi tes
  barrier R1 — dicatat jujur sejak kini, tidak diputuskan kini;
  ketiganya tidak bersih untuk bed confirmation tanpa ronde baru;
  Amandemen-R2-1 B7).

## D2-7. Jalur paper + bukti (sama dengan R1 D-6/D-7)

P0→P1→P2 izin per transisi; evidence di
`reports/research/2026-10-13/discovery-R2/evidence/` (ledger +
manifest hash SEBELUM run; script+harness+JSON+stdout sebelum
auditor). Logging gagal = run gagal.

## D2-8. Lampiran D-8 R2 (segel baru; segel R1 utuh)

8 pola + bias M15 dihitung-ulang di 2026 (definisi R1 D-8.1/D-8.2 +
A-C5), keluaran tabel hitungan, DISEGEL sampai vonis KANDIDAT R2
beku. Segel R1 (`5bc324aa…67df963`) TETAP TERTUTUP sampai vonis
final R1 beku — R2 tidak membukanya, tidak membacanya.

## D2-9. Justifikasi paket (ringkas, dari vonis EDA-06)

144 irisan unconditional: E_normal>0 = 0/144 (tak ada yang profit;
LOLOS = izin lanjut). Rantai median delta lengkap, naik = makin
buruk (Amandemen-R2-1 C4): ATR_k1.5_rr2 2,49 (5/12) < FIX_100_140
2,74 (6/12) < ATR_k1.5_rr1.4 3,35 < ATR_k1_rr2 3,65 < ATR_k1.5_rr1
3,92 < ATR_k1_rr1.4 4,39 < ATR_k0.75_rr2 4,59 < FIX_50_70 5,13 <
ATR_k1_rr1 5,55 < ATR_k0.75_rr1.4 5,86 < ATR_k0.75_rr1 7,19 <
FIX_30_45 8,03 (0/12, terburuk).
FIX_100_140 menang hitung 6 vs 5 tetapi fixed tak-adaptif dan bukan
desain original — satu paket ATR dikunci. LOLOS menumpuk
Tokyo/London tercile-3 (konsentrasi tercile-3 — FIX non-adaptif pun
menang di sana, jadi BUKAN bukti keunggulan adaptivitas ATR;
Amandemen-R2-1 C3). Dipilih pra-pembukaan 2026; bed 2026 tak
terlibat dalam ranking ini.
Keterbatasan diketahui (Amandemen-R2-1 C2): k/RR dipilih pada
horizon 120-menit EDA-06 tetapi dievaluasi pada H+10 dengan barrier
~4x R1 — porsi TIME-out diharapkan besar; failure map + proporsi
TIME yang bersaksi. Tanpa perubahan desain atas dasar ini.

## D2-10. Larangan ronde

Tanpa tuning; tanpa subset pasca-hasil; tanpa 2024/2025/2023 untuk
evaluasi; tanpa H4 rescue; tanpa RV/TAU; tanpa statistik penentu
tambahan; tanpa p-value untuk seleksi; tanpa ronde lanjutan atas
inisiatif AI (S8A); tanpa lompat ke live; tanpa buka segel R1.

## D2-11. Self-audit 3x (ringkas)

Correctness: event = R1; satu-satunya delta = barrier ATR resep
verbatim + bed segar; biaya/eksekusi/kriteria = R1; evidence
terpisah R2. Bias: k/RR dipilih dari EDA-06 + pengalaman user SEBELUM
2026 dibuka (pra-registrasi sah); bed 2026 segar ganda; Q2 tanpa
ladder (anti-seleksi); E3-tipis = temuan bukan alasan tuning.
Meta: NOL otorisasi eksekusi; keputusan material di user (R2-1..R2-6
menunggu ratifikasi); satu ronde satu vonis.

## D2-12. Ratifikasi yang diminta

Ratifikasi 2026-10-13 (user): "setuju" = SETUJU R2 paket penuh, tanpa
veto. Spec DRAF naik menjadi SPEC EKSEKUSI. Berikutnya (§15 desain
langkah 3): auditor audit spec, lalu coder discovery 2026-holdout.
R1 berjalan independen (replikasi → vonis final); R2 tidak menunggu
R1 kecuali user memerintahkan.

## Amandemen-R2-1 (2026-10-13, disetujui user paket "setuju")

Audit auditor atas spec R2 = CATATAN: B1/B3/B5/B6/B8 LULUS;
B2/B4/B7 GAGAL wording; C1–C5 catatan. Amandemen ini menutup
ketiganya + mengetatkan kelimanya, tanpa mengubah angka (k=1,5 /
RR=2,0 / H+10 / 2026-holdout / seed 1337 tetap):
- B2 → setting beku di kepala kriteria + larangan horizon lain (D2-6).
- B4 → tanggal exact paruh (D2-3).
- B7 → kontaminasi 2023+2024+2025 (D2-6).
- C1 → cakupan "verbatim" + semantik sentuhan barrier (D2-2, D2-5).
- C2 → limitasi horizon-mismatch (D2-9). C3 → redaksi tercile-3
  (D2-9). C4 → rantai median lengkap (D2-9). C5 → basis persen (D2-3).
Berikutnya (§15 desain langkah 3): re-audit fokus auditor atas
B2/B4/B7 + C1–C5, lalu coder discovery 2026-holdout.
