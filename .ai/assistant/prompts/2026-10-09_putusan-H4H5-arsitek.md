# Prompt putusan arsitek H4/H5 (Batch-2 TERTUTUP) — 2026-10-09

## Konteks (fakta, bukan instruksi)

Eksekusi coder Batch-2 + re-audit auditor SELESAI, keduanya gerbang LOLOS.
Keluaran formula (BUKAN vonis): **S-H4 = TAHAN, S-H5 = GUGUR**.
Verdict audit: **LULUS DENGAN TEMUAN** — seluruh angka penentu bit-exact
dari nol, harness byte-identik 3x; 2 MEDIUM non-penentu + 4 LOW; 4 eskalasi.
Tugasmu: VERIFIKASI DETAIL + VONIS RESMI H4/H5 + disposisi temuan/eskalasi +
preseden. Verifikasi di sini WAJIB (lihat S-V) — bukan vonis buta di atas
ringkasan.

## Peranmu (dibaca sebagai bagian brief ini, mandiri)

- Kamu ARSITEK (kontrak bersama `.ai/AGENTS.md` §26–§27): merancang + memutus
  konflik + tie-break. DILARANG menulis/mengubah kode produksi, data, config.
- Kamu BUKAN coder, BUKAN auditor. Namun verifikasi S-V di bawah WAJIB —
  kamu memutus HANYA atas bahan yang kamu periksa sendiri.
- Kamu BUKAN asisten.
- Workdir: `D:\ANN`. Interpreter verifikasi: `venv/Scripts/python.exe`.

## S-2d. Gerbang hash (ukur sesi ini SEBELUM satu butir pun diputus)

```
4a46b815211e6b0b050cbb6f3e98ce5e27904069  arsitek/spesifikasi-lapisan3-H4H5.md (461 baris)
f06a8e27b916172f5824438acd545614360d3b57  coder/hasil-lapisan3-H4H5.md (1299 baris)
8a4d21090f27dd53555b3a12583ec337819efb2f  Audit/reaudit-lapisan3-H4H5.md (707 baris)
ca4e0b70...                                arsitek/putusan-lapisan3-H1H2.md (preseden pola)
e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169  HEAD
```

## S-V. Verifikasi arsitek (WAJIB, sebelum P-1 — dari kode hingga hasil)

Vonis tanpa pemeriksaan sendiri = GAGAL. Kerjakan berurutan, laporkan
ringkas per huruf (COCOK / TIDAK COCOK + bukti file:baris/output):

(a) **Baca kode pada titik penentu** (bukan narasi): `sh4.py` —
`FIXED_HOURS`, loop entry, `gugur_a`/`gugur_b`, konstruksi top6 hitung-ulang;
`sh5.py` — `cutoff_2024`/`cutoff_2025` (posisi relatif terhadap pembentukan
event Q4), loop bootstrap paired-day, Holm step-down. Verifikasi dari kode
bahwa: EV hanya jam tetap, pola hanya top-6 hitung-ulang, cutoff dihitung
sekali pre-eval, tanpa `TAU_alt`/cutoff full-sample/in-eval.
(b) **Spot-check angka penentu vs artefak** (bukan vs prosa dokumen):
median EV pool + per-tahun, n_Off kedua bacaan, 4 diff + 4 p + keputusan
Holm — cocokkan melawan JSON harness di `%TEMP%\opencode\l3h4h5`
(trio-sha `b1b69d33` / `7a7f5ee7`, verifikasi sha dulu) dan sha parquet beku.
(c) **Run-ulang bila perlu.** Bila (a)/(b) menimbulkan KERAGUAN atas satu
angka/klaim: jalankan ulang skrip/probe SEMENTARA hanya di
`%TEMP%\opencode\l3h4h5_arsitek\` (dilarang tulis repo/commit), laporkan
path + hash hasilnya. Bila (a)/(b) meyakinkan tanpa run-ulang: tulis eksplisit
per butir MENGAPA tidak run-ulang (bukan default malas). Preseden S0.1
putusan H3/H1H2 tetap: bila verifikasimu MENEMUKAN selisih terhadap dua
rekaman sepakat → hitung-ulang penuh menjadi WAJIB + catat sebagai temuan
baru (tie-break S27 terpicu).
(d) **Verifikasi T1 dari data**: distribusi sesi jam 0/1/7 (re-audit D/R3
mengklaim 0/1 = 100% Tokyo) — konfirmasi sendiri sebelum memakai argumen
sesi apa pun di P-1/P-3.

## Bahan (dibaca UTUH langsung, bukan ringkasan)

1. `arsitek/spesifikasi-lapisan3-H4H5.md` — kriteria: H4 GUGUR bila
   (a) ≥2 dari 6 jam-teratas-hitung-ulang jatuh Off, ATAU (b) median EV pool
   ≤ 0; TAHAN = keduanya negatif (`:100-103`, `:266`, `:270`). H5 GUGUR bila
   keempat sel gagal; sel positif bila lolos Holm α=0,01 atas 4 p (`:100`, `:310`).
2. `coder/hasil-lapisan3-H4H5.md` — angka penentu: kriteria-(a) n_Off=0;
   median EV pool `0.014399999999998407` (2024 `+0.04834999999999022`,
   2025 `-0.005049999999992838`); Holm p Sydney 0.244 / Tokyo 0.291 /
   London 0.5176 / NewYork 0.7658 → nol reject.
3. `Audit/reaudit-lapisan3-H4H5.md` — R1/R2 bit-exact, R3 tak-ada-tukar
   (kedua bacaan n_Off=0), T1–T6, EKS-1–EKS-4.
4. `arsitek/putusan-lapisan3-H1H2.md` — preseden pola putusan (S0, P-1–P-5,
   self-audit 3x, C8).
   Rujukan konsistensi: lock H4/H5 + `putusan-arsitek-H1-H5.md`.

## Butir putusan (TERTUTUP — hanya ini)

**P-1. Vonis resmi H4 (DIPUTUS).** Terapkan kriteria lock verbatim pada angka
yang dua pihaknya sepakati: (a) n_Off=0 pada KEDUA bacaan (lock
`[14,13,0,15,12,7]` maupun hitung-ulang `[14,13,0,15,12,1]` — re-audit R3);
(b) median EV pool +0,0144 > 0. Keluaran formula TAHAN → sahkan atau tolak
dengan pasal. PERINGATAN T1: prosa coder "semua 6 bar London/NewYork"
terbukti SALAH (jam 0/1 = 100% Tokyo) — vonis WAJIB menyitir angka `[O6]`
(share 0,6833 + n_Off hitungan), DILARANG menyitir prosa `:1197`/`:1229`.
Vonis satu kalimat tunggal yang dikutip.

**P-2. Vonis resmi H5 (DIPUTUS).** Holm α=0,01: p terkecil 0,244 (Sydney) >
ambang pertama 0,0025 → berhenti di posisi 1 → nol reject → 4/4 sel gagal.
Sahkan GUGUR dengan pasal lock `:147-148`. Vonis satu kalimat tunggal.
Nyatakan eksplisit: GUGUR-nya H5 telak (bukan tipis) atau secukupnya.

**P-3. Disposisi EKS-1–EKS-4 (DIPUTUS).** EKS-1: selisih lock-vs-hitung-ulang
(7→1, komposisi sesi berubah) — putuskan sadar: "lock tetap dipakai" dicatat
sebagai keputusan, atau sebaliknya; tolak klaim coder "tidak ada eskalasi
wajib" secara eksplisit (auditor tidak setuju tanpa bukti lanjutan).
EKS-2: cutoff_2025 dari ATR 2024 — sahkan compliant/bukan-peeking (atau
putuskan sebaliknya). EKS-3: tanda 2024 + vs 2025 − — putuskan: apakah ini
menggoyang makna TAHAN H4 (peringatan stabilitas tercatat), atau murni
deskriptif tanpa konsekuensi vonis. EKS-4: definisi Off beku + fingerprint —
sahkan aman.

**P-4. Disposisi T1–T6 + standing rule C8 (DIPUTUS).** T1: mekanisme koreksi
prosa salah pada dokumen beku (adendum/erratum vs aturan sitir-angka-saja
mengikat konsumen hilir — pilih satu, jangan gantung). T2/S-B.10: C8
self-hash VACUOUS — putuskan status S-B.10 + pola pengganti C8 untuk batch
berikutnya (pengikatan eksternal; preseden: auditor Batch-2 sengaja tanpa
self-hash). T3–T6 LOW: tutup sebagai catatan atau naikkan — putuskan
satu-per-satu, tidak boleh diam. Severity temuan tertutup tidak berubah
tanpa pasal.

**P-5. Batas scope — kunci anti-merambat (DIPUTUS).** H1/H2/H3 tetap
GUGUR FINAL, tak tersentuh putusan ini. Tidak ada ambang/lock/vonis lain
berubah. Klausul anti-penyelamatan dua arah mengikat (kegagalan H5
DILARANG ditafsir-ulang via sub-sel/ambang pasca-hoc; dan bila H4 TAHAN —
keberhasilan itu pun DILARANG diklaim kebal tanpa uji pra-registrasi segar).
Tie-break S27 tidak terpicu bila coder-auditor sepakat fakta (sahkan
+ vonis + preseden).

## Tugas tulis (satu-satunya tulis yang diizinkan)

Tulis putusan sebagai file .md:
`reports/governance/2026-10-07/arsitek/putusan-lapisan3-H4H5.md`
berisi: S0 (hash terukur sesi ini + tabel Klaim & Bukti) + P-1–P-5 +
self-audit 3x adversarial + baris C8 TERAKHIR (blob dokumen tanpa baris itu;
bila menolak pola self-hash per P-4, tulis hash di luar dokumen TIDAK
diizinkan — putuskan konsisten: C8 ada dengan lubangnya dinyatakan, atau
pengganti yang P-4 tetapkan) + STOP. DILARANG commit/push. DILARANG vonis
di luar P-1–P-5. DILARANG memulai batch berikutnya.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: hash S-2d diukur sesi ini; S-V(a)–(d) dikerjakan +
dilaporkan (run/tidak-run diputus eksplisit per butir); tiap P berpasangan bukti
mentah ([O]/R/T/EKS + baris); vonis H4/H5 masing-masing satu kalimat dikutip;
EKS-1–EKS-4 + T1–T6 masing-masing diputus eksplisit, tidak digantung.
Putaran 2 — Bias & Asumsi: ambang diterapkan verbatim (tidak dirapikan agar
H4 TAHAN/GUGUR tertentu); T1 tidak menginfeksi penalaran vonis; tidak ada
pintu penyelamatan diam-diam dua arah.
Putaran 3 — Meta-check: lock tak tersentuh tanpa addendum; ruang coder/auditor
tidak diambil; severity lama tak berubah tanpa pasal.

STOP. Batch-2 TERTUTUP oleh putusan ini.
