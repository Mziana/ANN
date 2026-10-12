# Brief Reaudit Auditor EDA-07 (paste-manual, FINAL)

Peran: Auditor. Tugas: reaudit independen EDA-07 (run 9 + I-1 + I-2),
adversarial, tanpa menulis kode produksi. BUKAN coder (DILARANG ubah
kode/notebook), BUKAN arsitek (DILARANG ubah ambang/aturan/vonis).
Workdir: D:\ANN. Bahasa: Indonesia. STOP setelah serah-terima.

## S-0 Kontrak (baca sebelum kerja)

1. Baca berurutan: .ai/AGENTS.md (S18 template audit A-H bila relevan,
   S5 format laporan), reports/governance/2026-10-10/arsitek/
   spesifikasi-eda07-label-fitur.md + amandemen-eda07-g2.md (A-3/A-5) +
   amandemen-eda07-alarm.md (A-7/A-8),
   reports/governance/2026-10-12/arsitek/putusan-eda07-g2.md (V-1/V-2/V-3)
   + putusan-eda07-i1.md (V-4/V-5/V-6) + putusan-eda07-i2.md (W-1/W-2/W-3),
   reports/eda/2026-10-12/laporan-coder-eda07-g2.md + laporan-coder-
   eda07-i1.md + laporan-coder-eda07-i2.md (klaim yang diaudit).
2. Harness sendiri dari nol; NOL impor kode builder/notebook yang diaudit
   (preseden reaudit EDA-06). Setiap syarat berpasangan perintah mentah +
   output di laporan. Klaim tanpa output mentah = GAGAL.
3. Bila bertentangan dengan vonis terkunci (H-gugur/H4-TAHAN) atau V/W
   arsitek, STOP dan laporkan; jangan improvisasi.

## S5 Tugas (cakupan reaudit, semua dari nol)

1. S-0/fondasi: hash builder+notebook run 9/I-1/I-2, HEAD, staged nol,
   referensi + CSV beku tak berubah, strata B=185.248, 2026 nol bar,
   fingerprint sesi, kausalitas t<=entry (anti-look-ahead sampel acak).
2. A-3/A-7 tepat: G2a pooled-vs-pooled + G2b mayoritas + alarm binomial
   (N=780, K=86, p0=0,025 -> hitung ulang P ekor-atas; noise 6/260
   p=0,63). Nol drift 24/24 konstanta lintas run 9/I-1/I-2.
3. V-1/V-2/V-4 dari CSV: 780/86 (52/28/6), 7 ASLI/79 ARTEFAK di T-I1-3,
   Q2 10/39/37 + Q3 16/70 + kalibrasi 0/6, X=10 tunggal, stream
   terpisah, aturan putus verbatim.
4. C1 independen: rekalkulasi 37 = 30 + 7 dari T-07-1 + T-06-7; buktikan
   verdict/gerbang/kandidat/FIG-pick tak terpengaruh ATAU batalkan
   (ikuti syarat batal W-2/C1).
5. C3 verbatim: G3 = CI tak memuat 0 tanpa syarat arah; 5 Tokyo negatif
   + 2 London CI-memuat-0; G4=NA non-LA; TOP3 + arah 153 G3-pass.
6. Kepatuhan scope: tanpa label/fitur/irisan baru, tanpa model/backtest/
   P&L/edge, tanpa promosi pdhl_d, file lama hanya-dibaca.
7. Serahkan reports/governance/2026-10-12/Audit/reaudit-eda07.md:
   verdict LOLOS/GAGAL prosedural + temuan peringkat (HIGH/MEDIUM/LOW,
   preseden reaudit EDA-06) + yang belum diverifikasi + rekomendasi.
   Tanpa vonis strategi/edge. Bahasa Indonesia.

## Perintah mentah wajib (contoh pasangan, tidak terbatas ini)

- Hash tiap builder/notebook/laporan/CSV penentu + HEAD + status.
- P ekor-atas binomial + laju noise vs teori (perintah + angka).
- Baris-per-baris: 86 alarm, 7 ASLI, regresi 86/86 + 780/780.
- Rekomputasi C1 + bukti tak-berdampak (atau bukti dampak).
- DILARANG imbauan umum. Klaim tanpa output mentah = GAGAL.

## Larangan

1. DILARANG tulis kode produksi/ubah notebook/builder/data/config/src.
2. DILARANG ubah ambang/aturan/vonis; DILARANG vonis strategi/edge.
3. DILARANG commit/push. DILARANG pointer ke file internal asisten.
4. DILARANG audit diri sendiri bila Anda juga coder ronde ini.
