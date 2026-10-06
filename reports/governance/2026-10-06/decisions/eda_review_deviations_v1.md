# Review Deviasi nb00–nb04

**Tanggal:** 2026-10-06
**Architect:** Spark 1.3
**Sumber rancangan:** eda_design_v3.1.md (kanonik; salinan bundle di `checkpoints/` adalah scratch prompt, bukan acuan)
**Sumber audit:** audit_kesesuaian_nb00_nb04.md (coder, 8 deviasi + D11/D12 + ronde-2 + 1 retraksi)

---

## Verdict per Deviasi
| # | Deviasi | Verdict | Alasan |
|---|---|---|---|
| D1 | ACF 1–20, rancangan 1–60 | INVALID | `LAGS = range(1,21)` (nb03:385) + assertion "20 lag" (:824). Lag 21–60 (= s/d 1 jam M1) belum diperiksa; relevan untuk holding M15. Fix: satu konstanta → 1–60 + update assertion. |
| D2 | Ljung-Box tidak dihitung | INVALID (tegakkan, dengan aturan interpretasi) | Item kontrak `[PS]` yang hilang. Keberatan coder sah (n>1jt → pasti reject) dan diadopsi sebagai ATURAN INTERPRETASI: laporkan Q/n + besaran, p tidak pernah menyimpulkan; paling informatif di slice M15/tahun/sesi. Implementasi manual via scipy chi2 (scipy sudah dipakai nb03) — tanpa dependensi baru. |
| D3 | VR semua-lag 1–20, rancangan k=5/15/60 | PARTIAL | Kurva 1–20 adalah superset yang memuat 5 dan 15 — dipertahankan; yang hilang hanya titik 60. Fix: ikut ekstensi D1 (satu konstanta, loop VR mengikuti otomatis) + pertahankan vr2. |
| D4 | Sign-autocorr lag-1 tidak ada | INVALID | Item kontrak hilang; murah (ACF dari sign(r) per TF × strata); melengkapi label arah momentum/MR yang sudah ada di SESSION_ACF. |
| D5 | Hanya strata A, tanpa B | INVALID | `STRATA_A` dipakai di semua loop nb03; `b_mask` didefinisikan tapi tak dipakai analisis. Perbandingan A-vs-B adalah inti pertanyaan regime SA-03. Fix: loop metrik headline (ACF, VR, sign) untuk B di M1/M5/M15. |
| D6 | Frekuensi swing per hari tidak ada | INVALID | groupby hanya `session_label` (:487) dan `year` (:493). `per_day` di :1100 adalah bootstrap CI hit-rate Q6, bukan frekuensi swing — D6 berdiri. Fix: satu groupby hari. |
| D7 | Waktu tahan median swing tidak ada | INVALID | `tahan/holding/durasi` nol hasil di kode nb04. Fix: jarak antar indeks fraktal, median. |
| D8 | Nama `eda_04_swing_level.ipynb` vs `eda_04_swings_levels.ipynb` | INVALID (trivial) | Terkonfirmasi via `ls`. Rename gratis (belum commit); nb05 kelak wajib merujuk nama benar. |
| D9 | 3 file berbagi FIG-01 | INVALID | `FIG-01_qq_{M1,M5,M15}.png` (nb01:999 + outputs + isi figures/). Putusan skema: urutan global FIG-01..NN dipertahankan (huruf rancangan); 3 file → FIG-01/02/03 (M1/M5/M15); nomor bebas berikutnya = FIG-04 ke atas, diklaim sekuensial oleh nb03, nb04, nb05 berurutan; nb05 memverifikasi registry. Setiap plot yang ditampilkan wajib disimpan. |
| D10 | `spread_pips_max` M5 tidak dipakai | INVALID | Hanya muncul di nb00 (matriks + cek kolom). Ekor M1 ada, tetapi ekor-per-bucket M5 adalah item kontrak. Fix: satu agregasi, dilaporkan berdampingan dengan tail M1. |
| D11 | Placebo "touch genuine" (coder pilih) | VALID | Aturan touch identik kedua sisi (`low<=L<=high`, nb04:510/603 = nb00:819); MAX_K=24 bar = max window reaksi (simetris, 2 jam M5); parameter preregistrasi di-assert identik (:136–149, :196–231); retensi non-degeneratif (0,557/0,468); hit placebo ~0,49–0,51 vs nyata 0,47. Tanpa syarat-touch, kontrol literal degeneratif (0,89–0,95) — perbandingan terkondisikan adalah yang sah secara statistik. Rancangan menyerap sebagai refinement tercatat (bukan tuning). |
| D12 | Event marker (fix/NYSE/BoJ) nol di semua notebook | PARTIAL | Terkonfirmasi (satu-satunya hit: nb00:976 justru menyatakan kalender di luar scope). Wajib MINIMAL: flag jam Tokyo-fix 00:55 UTC + jam buka NYSE di tabel/plot per-jam nb02; hitungan eksposur bar+touch di zona BoJ 150/155/160 di nb04. Studi event penuh KELUAR scope (itu analisis baru; kandidat hipotesis nb05 bila data menyarankan). |

## Keputusan Khusus
- D2: **Tegakkan sesuai rancangan** (tambah LB manual via scipy, laporkan Q/n + besaran + p; p tidak menyimpulkan; fokus informatif di slice). Keberatan statistik coder benar dan diabadikan sebagai aturan interpretasi — bukan sebagai penghapusan.
- D11: **Interpretasi coder VALID.** Touch-conditioning adalah syarat kontrol yang adil; preregistrasi parameter utuh; dideklarasikan terbuka di notebook. Tidak ada perubahan kode diminta; putusan ini dicatat (calon adendum v3.2 bila user menghendaki formalisasi).
- D12: **Wajib minimal, studi menyusul-tidak.** Marker deskriptif murah dan terkontrak (khususnya fix 00:55 untuk USDJPY); event-study adalah scope creep yang tepat dilewatkan.

## Urutan Perbaikan
1. D8 rename + catat putusan D11 (nol komputasi; membuka kunci finalisasi nb04).
2. D2/D4 (tambahan termurah nb03) + D1/D3 (satu konstanta + assertion) + D5 (loop strata B) — satu batch rework nb03 → rerun nb03.
3. D6/D7 nb04 (+ hitungan eksposur BoJ D12) → rerun nb04.
4. D10 agregasi M5-max + flag fix/NYSE di nb02 (D12) → rerun sel terkait.
5. D9: rename 3 file → FIG-01/02/03 + kunci skema global (bebas = FIG-04+).
6. Update audit kesesuaian → review arsitek → DUA commit: (A) nb04 baru (D8+D6+D7+D12-BoJ); (B) koreksi nb03+nb01+nb02 ter-commit. DILARANG amend `e4efbfd` (riwayat review dipertahankan).
7. Baru kemudian nb05. nb05 DILARANG mengonsumsi output nb03 sebelum commit koreksi mendarat.

## Dampak ke nb03
Kesimpulan Q4 saat ini **provisional**. Arah headline (momentum/MR per TF) kemungkinan stabil, tetapi kualifikasi hampir pasti berubah dan perbandingan A-vs-B adalah informasi genuinely baru (B tanpa daily break → struktur gap/ACF dapat berbeda; lag 21–60 = struktur s/d 1 jam yang relevan untuk M15 belum dijelajahi). Besaran perubahan tidak dapat dinyatakan tanpa komputasi ulang — klaim sebaliknya akan melanggar §20.

## Temuan Tambahan (di luar 12, mengikat ringan)
- **T1 — Dokumen kanonik**: `governance/eda_design_v3.1.md` adalah SATU-SATUNYA acuan; bundle `checkpoints/RANCANGAN EDA V.3.MD` adalah scratch prompt (isinya se-era, tak diverifikasi baris-per-baris). Audit berikutnya wajib menyitir file governance.
- **T2 — `_eda_common.py` DITERIMA**: modul notebook-lokal (bukan `src/`), terdokumentasi, dijaga fingerprint assert yang lolos di 5 notebook. Pola ini disetujui; assert fingerprint tetap mandatori. Duplikasi definisi (nb00 + modul) adalah trade-off sadar demi anti-drift.
- **T3 — Kredit proses**: audit coder memenuhi §20 (mengaku improvisasi sadar di seksi D, mencabut temuan palsunya sendiri dengan bukti). Insentif kejujuran ini dipertahankan: temuan jujur tidak menghukum.
- **T4 — figures/**: hanya berisi 3 file nb01 → tidak ada tabrakan lain; aturan D9 mencegah pertumbuhan tabrakan.

## Self-Audit Architect 3 Putaran
- **Putaran 1 (correctness)**: setiap verdict berjangkar file:baris disk (nb03:385/824, :286–288, :508–541; nb04:487/493/510/603/848–870/1100; nb01:999; figures/ isi). Satu koreksi presisi: `per_day` nb04:1100 adalah CI bootstrap Q6, bukan frekuensi swing — D6 dinilai terhadap bukti yang benar.
- **Putaran 2 (bias & asumsi)**: melawan rancangan sendiri 1× (D11 VALID untuk coder) dan melawan coder 9× berbasis item-kontrak-hilang (bukan opini) — seimbang dan terdokumentasi. Asumsi tercatat: biaya komputasi ekstensi "murah" (ACF-60/VR-60/loop-B; fallback fft bila lambat); kebenaran numerik output notebook TIDAK diverifikasi (tugas coder self-audit + Klenz — dinyatakan terbuka, bukan diklaim).
- **Putaran 3 (meta)**: semantik VALID/INVALID/PARTIAL dipakai konsisten (VALID = deviasi benar→desain menyerap, 1 kasus; INVALID = deliverable hilang→kode berubah, 9 kasus; PARTIAL = pertahankan+tambah, 2 kasus; TIDAK JELAS = nol — semua 12 decidable). Trade-off dinyatakan (higiene commit, biaya komputasi, scope studi). Setiap fix menunjuk file:baris/konstanta/nama-pasti sehingga coder langsung eksekusi.

---

**Akhir Review Deviasi v1**
