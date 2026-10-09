# Brief Arsitek — Desain R-2 Stratifikasi Tahun H4 (FINAL, disetujui user 2026-10-09, siap paste)

**Peran:** Arsitek (AGENTS.md §26-§27: merancang + memutus; DILARANG tulis/ubah kode produksi, data, config; DILARANG commit/push dalam bentuk apa pun).
**Tanggal:** 2026-10-09. **Lingkup TERTUTUP:** desain spec R-2 saja. BUKAN eksekusi, BUKAN vonis H4, BUKAN vonis ulang Batch-2, BUKAN H6.
**Kontrak bersama (wajib dirujuk):** `.ai/AGENTS.md` v3.0 §5 (Klaim & Bukti), §20 (klaim wajib bukti; output mentah ditempel), §21 (uji dulu), §26 (pemisahan peran), §27 (arbitrase).
**Aturan besi (berlaku untuk dokumen desain ini juga): klaim angka WAJIB output mentah; klaim tanpa output mentah = GAGAL.**

---

## S1. Substansi verbatim pengikat (disalin eksplisit, bukan pointer)

1. Disposisi fondasi-B D-2: "Ronde desain berikut BOLEH mempertimbangkan stratifikasi tahun pra-registrasi. BUKAN filter regime — filter tetap DILARANG tanpa spec baru + uji stabilitas LULUS (putusan H3 mengikat)."
2. Disposisi D-1: "Vonis H4 TETAP TAHAN." D-2 membuka opsi, bukan memerintahkan hasil; D-1/D-3/D-4 tidak diputus-ulang.
3. Putusan Batch-2 P-5 (kunci dua arah): H5-gagal DILARANG tafsir-ulang via sub-sel/ambang/window pasca-hoc; H4-TAHAN DILARANG diklaim kebal tanpa uji pra-registrasi segar di data segar.
4. Putusan H4b V-4: GUGUR(H4b) BUKAN retak pada H4; H4 TAHAN Batch-2 + H1/H2/H3/H5 FINAL tak tersentuh; H6+ DITOLAK.
5. EKS-3 tercatat: median 2024 positif vs 2025 negatif; konsumen hilir DILARANG membaca TAHAN sebagai bukti stabil.

## S2. Bahan yang WAJIB dibaca utuh langsung (bukan ringkasan)

1. `reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md` (putusan H4 TAHAN FINAL + EKS-1–EKS-4 + T1–T6 + P-5).
2. `reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md` (angka penentu: n_Off, median pool, per-tahun, JSON trio-sha).
3. `reports/governance/2026-10-07/arsitek/disposisi-fondasi-B.md` (D-1–D-4 + warisan R-2).
4. `reports/governance/2026-10-07/arsitek/putusan-H4b-stabilitas.md` (GUGUR stabilitas + ESK-1 BEKUKAN+CATAT + V-4 anti-merambat).

## S0. Gerbang hash sesi arsitek (wajib SEBELUM satu butir pun diputus)

Ukur sesi ini: `git hash-object` atas spec-B2 + hasil-B2 + reaudit-B2 + putusan-B2 + protokol-B + hasil-B + disposisi-B + putusan-H4b, plus `git rev-parse HEAD`. Cocokkan digit-per-digit dengan S2; mismatch = STOP. Tempel output mentah. Staged wajib tepat 2 T6 (`git diff --cached --name-only`); tanpa commit/push/stash/checkout oleh sesi ini.

## S-V. Verifikasi arsitek (wajib sebelum desain)

(a) Empat bahan S2 dibaca UTUH langsung, bukan ringkasan. (b) Angka penentu H4 diekstraksi dari JSON/bahan mentah sesi ini (n_Off, median pool, per-tahun, trio-sha). (c) Run/tidak-run diputus eksplisit per butir; S27 tak terpicu bila rekaman sepakat. (d) Probe independen bila klaim baru diajukan.

## S3. Tugas desain (diminta dari arsitek)

1. Tetapkan pertanyaan R-2 tunggal yang pra-registrasi: apakah efek H4 stabil antar-tahun bila pool dipecah stratifikasi tahun — dengan ambang stabilitas yang terkunci SEBELUM eksekusi (mis. arah yang dipakai, bukan angka yang diintip).
2. Tetapkan jendela evaluasi, pemisah seed-vs-evaluasi, dan aturan anti-intip (2023/2026 diperlakukan eksplisit; DILARANG shopping-jendela).
3. Tetapkan kriteria keputusan R-2 yang verbatim dan mekanis (TAHAN/GUGUR/TAK-MENENTUKAN bila perlu), tanpa mengubah lock/vonis Batch-2 dan tanpa menyentuh H5. Usulan terkunci yang disetujui sebagai opsi default: OR-gugur gaya-H4b (satu tahun gagal = GUGUR) — arsitek boleh mendefinisikan sendiri dengan alasan tertulis, bukan diam-diam.
4. Tetapkan mesin C1–C9 (HEAD, status kosong, hash tiap bahan + trio beku, gate determinisme, output JSON-bukan-prosa, artefak harness di `%TEMP%` luar repo dengan interpreter venv kanonik dinyatakan eksplisit) + daftar larangan S-B eksplisit (termasuk 12 larangan bentuk-spesifik di bawah). DILARANG tulis ke `src/`/`configs/`/`data/`.
5. Perintah tulis: dokumen desain ke `reports/governance/2026-10-07/arsitek/spesifikasi-R2-stratifikasi.md`, target <150 baris, diakhiri STOP. Tempel output mentah tiap klaim: `git hash-object` tiap bahan SEBELUM satu butir pun diputus; `git rev-parse HEAD`; `git status --porcelain`; `git diff --cached --name-only`.

## S4. Larangan eksplisit (disalin ke brief, berlaku untuk desain ini)

1. DILARANG vonis H4/H5 di dokumen desain (desain ≠ vonis; vonis = putusan terpisah sesudah re-audit).
2. DILARANG filter regime / sub-sel / ambang / window pasca-hoc sebagai penentu.
3. DILARANG mengubah lock/ambang/vonis Batch-2 dan fondasi-B tanpa addendum pra-registrasi BARU.
4. DILARANG merumuskan H6 dalam bentuk apa pun.
5. DILARANG `utc.normalize()` / rekontruksi hari dari UTC; grain tunggal hari-broker dari store.
6. DILARANG guard nilai-vs-diri (termasuk terbungkus komentar/docstring).
7. DILARANG fixture seragam untuk klaim sensitif-parameter; DILARANG test tanpa assertion dihitung dalam total.
8. DILARANG output parsial berlabel proses penuh; DILARANG klaim "diuji via X" sambil mengaku "belum ada test X" di dokumen sama.
9. DILARANG kutip baris/path tanpa verifikasi ulang; DILARANG naikkan severity temuan tertutup.
10. Guard provenans WAJIB dari sumber terpisah; sabotase WAJIB ke jalur produksi persis `main()`.
11. Klaim gate format/lint WAJIB sebut rc + cakupan; klaim byte-identik WAJIB sebut toolchain.
12. Konstanta pengikat kalibrasi WAJIB dikunci test (mutasi tanpa hitung-ulang HARUS merah).
13. Self-audit 3x adversarial WAJIB sebelum STOP (correctness, bias & asumsi, meta-check).

---

## Disiplin tambahan (DISETUJUI user 2026-10-09 — bagian mengikat brief ini)

- S0 8-hash + staged tepat 2 T6 + tanpa commit/push oleh sesi arsitek (U-1).
- S-V(a)–(d) wajib pola putusan (U-2).
- Kriteria stabilitas default OR-gugur gaya-H4b atau definisi arsitek beralasan (U-3).
- Harness `%TEMP%` luar repo + venv kanonik eksplisit; larangan tulis `src/configs/data` (U-4).
- Pagu tulis <150 baris + STOP menutup desain (U-5).

**Status:** FINAL. Siap paste ke arsitek → desain MASUK → gerbang → ronde coder.
