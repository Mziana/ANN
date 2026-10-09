PERBAIKAN nb05 ATAS TEMUAN AUDIT LANGKAH 1 — verdict: PERLU PERBAIKAN
(2 HIGH · 2 MEDIUM · 3 LOW; LOW tidak butuh perbaikan kode)

Catatan posisi: angka hitunganmu TIDAK salah aritmetika (auditor: "bukan
perhitungannya salah", melainkan "tidak sesuai rancangan" pada label dan
desain assertion). Yang diminta: betulkan label, disclose metode, ketatkan
kunci, jawab 6 pertanyaan. Audit Langkah 2–10 DITAHAN sampai verdict LULUS.

=== SUBSTANSI TEMUAN (verbatim dari auditor, Space Bunny) ===

[HIGH-01] `_build_eda05.py:444` mencetak
`f"rata-rata VR(5,15,60) = {mean_vr:.4f} (referensi nb03: 1,0337)"`.
Angka `1,0337` di nb03 adalah rata-rata VR pada lag 2-60 (59 titik), bukan
rata-rata VR pada tiga horizon kontrak (5, 15, 60). Pembanding
apples-to-apples: `(1.0160 + 1.0119 + 1.0657) / 3 = 1,0312`.
Saran auditor: ganti string referensi menjadi `1,0312` dan tambahkan baris
kedua yang menyebut `1.0337` sebagai rata-rata lag 2-60, supaya tidak tertukar
lagi. Assertion harus diarahkan ke `1.0312`.

[HIGH-02] nb05: `rolling(k).sum().dropna().var(ddof=0) / (k * r15.var(ddof=0))`
atas seri `r15` penuh (`_build_eda05.py:435, 439-440`). nb03:
`np.var(values, ddof=1)` / `np.var(lag_sum, ddof=1)` atas
`subset.loc[~subset["gap_return"], "r"]`. Dua perbedaan independen:
(a) `ddof=0` vs `ddof=1`; (b) menyertakan bar gap vs no-gap. Tidak disclosed
di docstring maupun output, padahal label `"replica nb03"` ada di
`_build_eda05.py:422, 443, 444`.
Saran auditor (rekomendasi konservatif): samakan `variance_ratio` nb05 dengan
nb03 (fungsi yang sama, `ddof=1`, no-gap), lalu assertion
`1.025 < mean_vr < 1.038` dengan referensi `1.0312`. Jika tetap memakai versi
`ddof=0` penuh, ubah label output dari `"replica nb03"` menjadi
`"indikator VR (metode nb05, bukan nb03)"`.

[MEDIUM-01] nb05 menentukan pasangan no-gap lewat
`np.diff(t15) == np.timedelta64(900, "s")` (`_build_eda05.py:450-451`) di atas
pemetaan `broker_day` yang dibangun ulang sendiri; nb03 memakai kolom
`gap_return` milik stratifikasi nb00. Hasil: `-0.022005` vs `-0.022624`
(selisih 0,000619 = 2,74%). `n_no_gap` nb03 M15-A lag 1 = `75038`; nb05 tidak
mencetak n sehingga selisih tak bisa diatribusi.
Saran auditor: cetak `n_no_gap` di output + satu kalimat sumber definisi
no-gap (adjacency timestamp, bukan kolom `gap_return`).

[MEDIUM-02] Keempat assertion replika terlalu lebar:
`_build_eda05.py:445` `abs(acf1_m15_a) < 0.05` vs acuan `0.001793` (~2.800%);
`:446` `0.9 < mean_vr < 1.2` vs `1.0312` (tak menyebut acuan sama sekali);
`:453` `-0.030 < sign_acf1 < -0.015` vs `-0.022624`; `:543`
`45.0 < SWING_PER_DAY_K3 < 52.0` vs `49.070`.
Saran auditor: kunci ketat eksplisit, mis. `abs(acf1_m15_a - 0.001793) < 0.0005`,
`abs(mean_vr - 1.0312) < 0.005`, `abs(sign_acf1 + 0.022624) < 0.001`,
`abs(SWING_PER_DAY_K3 - 49.070) < 0.05`. Band lebar boleh tetap sebagai
assertion kedua dengan nama berbeda.

[LOW-01/02/03] Koreksi draf audit lama, TIDAK butuh perbaikan kode. Satu yang
menyangkutmu: LOW-02 meminta konfirmasi — referensi swing yang benar adalah
`high_k3 24.447 + low_k3 24.623 = 49,070` (k=3 saja), bukan `48,74`
(gabungan k=3+k=5). Catatanmu di `_build_eda05.py:542` sudah benar memisahkan
keduanya; pertahankan.

=== 6 PERTANYAAN (jawab satu per satu, dengan bukti) ===
1. VR: pertahankan versi nb05 (`ddof=0`, penuh) atau samakan nb03 (`ddof=1`,
   no-gap)? Jika pertahankan, apakah label `"replica nb03"` (`:422,443,444`)
   diubah ke label non-replika?
2. VR: angka `1,0337` di `:444` dan sel 9 diganti `1,0312`, atau keduanya
   dicetak berdampingan dengan keterangan masing-masing?
3. Swing: concurring bahwa referensi benar `24.447 + 24.623 = 49,070`?
4. Sign-ACF: mengapa `n_no_gap` tidak dicetak? Bisakah selisih 2,74%
   direduksi dengan menyamakan definisi no-gap ke kolom `gap_return`?
5. Assertion: pasang kunci ketat seperti usulan, atau pertahankan band lebar
   dengan alasan tertulis?
6. Apakah ada salinan lain draf audit berisi klaim
   `assert abs(mean_vr - 1.0337) < 0.05` (klaim karangan draf lama) agar tidak
   tersalin ke laporan lain? (Catatan: ini artefak draf auditor lama, bukan
   file-mu — jawab "tidak ada di ruang coder" bila benar demikian.)

=== BATAS KERJA ===
- Ubah HANYA yang diminta di atas. DILARANG merombak di luar temuan.
- Setelah ubah builder: rerun notebook penuh + gate (ruff, nbconvert exit=0;
  pytest/validate bila terdampak). Lapor tabel Klaim & Bukti (§5 AGENTS.md)
  + hash blob baru tiap file yang berubah.
- DILARANG commit. Commit menunggu verdict LULUS auditor.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness: tiap angka/acuan di laporanmu ada sumber
  (file:baris/output). Tak bersumber → BELUM DIVERIFIKASI.
Putaran 2 — Bias & Asumsi: apakah ada pilihan metode yang kamu sembunyikan?
  Apakah label output jujur soal metode?
Putaran 3 — Meta-check: apakah semua 4 temuan + 6 pertanyaan terjawab? Apakah
  ada file di luar scope yang tersentuh?

STOP — tunggu audit ulang Langkah 1 oleh auditor.
