# Brief Audit Spec Discovery-R1 — untuk AUDITOR eksternal (Arsitek, 2026-10-13)

## S-0. Objek (baca penuh sebelum menilai)

1. `reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R1.md`
   (SPEC EKSEKUSI — diratifikasi user 2026-10-13: SETUJU R-1..R-6 + R-7).
2. `.ai/backup/2026-10-09_DESAIN_FRESH_SCALPING_EVENT_FIRST.md` (desain
   induk, 613 baris — spec wajib verbatim/turunannya, bukan karangan).
3. `.ai/SESSION_LOG.md` (entri RATIFIKASI 2026-10-13 — konfirmasi status
   spec; R-7 lampiran TERKUNCI atas persetujuan user).

Konteks proyek: USDJPY scalping M1 (entry+outcome) / M5-M15 konteks;
1.347.847 bar M1 2023-2026; broker Finex MT5; komisi 1 USD/lot (asumsi
per-side sampai klarifikasi); `trade_allowed=False` (riset saja).

## S-1. Mandat (desain §15 langkah 3: audit spec SEBELUM coder bekerja)

Periksa apakah spec dapat dieksekusi coder TANPA membuka lubang yang
diserang red-team desain (§3). Sembilan titik audit:

- A1 Traceability: tiap butir D-1..D-11 menunjuk § desain induk yang
  tepat; tidak ada gerbang/istilah karangan; tidak ada kontradiksi
  dengan desain.
- A2 Look-ahead: definisi operasional E1/E2/E3 (D-1) + Q3 (D-4.3)
  hanya memakai informasi sampai t0 close; tidak ada swing/range/
  ATR/volatilitas yang memakai bar sesudah t0.
- A3 Multiple-testing budget: 3 keluarga x 1 kandidat; sel grid
  dihitung dan dinilai satu family; aturan kapasitas min 300 event
  efektif melawan sel-tipis-menang; tidak ada derajat kebebasan
  tersembunyi (grid, horizon, ladder, konteks).
- A4 Barrier ambiguity: ladder TP/SL hanya pemetaan; satu paket beku
  sebelum confirmation; AMBIGUOUS_SEQUENCE dibuang-terhitung
  (dikunci, bukan opsi pasca-hasil).
- A5 Bid/ask + biaya: sisi harga verbatim (§8.2); 3 lapis konsisten
  (observed/conservative/stress); angka R-5/R-6 (spread terukur,
  komisi 0,3 pip asumsi per-side, slippage 0,2/0,3) eksplisit dan
  ditandai asumsi; tidak ada kandidat lulus dari gross.
- A6 Split temporal: 2024/2025 verbatim §5.2; 2023-H1 + 2026 keluar
  denominator; eksklusi tambahan proyek (2 jendela anomali + SA-03)
  beralasan dan tercatat.
- A7 Kontainment lampiran D-8: 8 definisi pola operasional dan
  pra-registrasi; M15 satu-satunya konteks primer; tidak ada jalur
  dari lampiran ke pemilihan/menyetel kandidat R1; jendela
  SEBELUM/SAAT/SESUDAH deskriptif saja.
- A8 Anti-rescue H4: lima butir §2 desain hadir penuh dan efektif
  (tidak ada filter/jam/ambang H4 yang memilih event).
- A9 Integritas ratifikasi: nilai R-1..R-6 di spec = usulan yang
  diratifikasi user; R-7 = persetujuan lampiran yang benar-benar ada
  di log; tidak ada R yang diisi nilai lain diam-diam.

## S-2. Larangan auditor

DILARANG menulis kode, mengedit file apa pun, mengubah spec, atau
memvonis dagang. Output HANYA teks laporan. Klaim tanpa sitiran
baris file = kalah (AGENTS §27 langkah 1).

## S-3. Format laporan (kembalikan teks ini ke user)

Untuk tiap A1-A9: COCOK / TEMUAN (dengan sitiran `file:baris` kedua
sisi). Derajat temuan: HIGH (lubang dieksploitasi diam-diam) /
MEDIUM (ambiguitas dapat di-game) / LOW (redaksi). Diakhiri SATU
verdict: LULUS (coder boleh jalan) / LULUS DENGAN CATATAN (sebut
syarat) / GAGAL (spec wajib amandemen — sebut butirnya).

=== SELF-AUDIT 3x ADVERSARIAL (brief ini) ===
Putaran 1 — Correctness: S-0 tiga objek lengkap + status ratifikasi
benar (log 2026-10-13); S-1 sembilan titik = §15 langkah 3
(leakage, future swing, budget, ambiguity, bid/ask, split) + 3
tambahan (traceability, kontainment, ratifikasi); S-2 larangan
tegas; S-3 format verdict tunggal.
Putaran 2 — Bias & Asumsi: brief tidak mengarahkan verdict (tiga
opsi simetris); tidak meminta auditor menulis kode; asumsi konteks
proyek (simbol, bar, komisi) dinyatakan eksplisit bukan diselipkan.
Putaran 3 — Meta-check: brief ini otorisasi NOL eksekusi — hanya
audit teks; keputusan material (amandemen vs jalan) tetap di
arsitek/user setelah laporan masuk; tidak ada staged/commit yang
diminta.
