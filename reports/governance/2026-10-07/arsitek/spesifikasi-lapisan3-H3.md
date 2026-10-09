# Spesifikasi Lapisan 3-H3 — Uji Prasyarat H3 — 2026-10-08

**Peran:** Arsitek (§26 AGENTS.md: merancang + memutus konflik; DILARANG
menulis kode produksi/implementasi). **BUKAN eksekusi.**
**Lingkup sempit:** hanya 2 prasyarat dari re-audit keempat §9 —
(a) materialitas `gap_f2_flag`, (b) sensitivitas TAU. Bukan vonis H1/H3/H4/H5.
**Kontrak yang mengikat dokumen ini:** `.ai/AGENTS.md` v3.0 —
§5 (tabel Klaim & Bukti; dilarang "sepertinya OK"),
§20 (setiap klaim wajib bukti; output asli ditempel),
§21 (uji dulu, simpulkan kemudian; format Proposal Uji),
§26 (Architect/Coder/Auditor beda peran).
**Dokumen audit menang atas ringkasan bila berselisih.**

---

## §0. Klaim & Bukti konteks (§5)

Cara baca status: TERVERIFIKASI = saya ukur sendiri di sesi ini;
TERVERIFIKASI (rujukan) = saya verifikasi keberadaan + isinya di dokumen
audit ter-hash (bukan saya yang menjalankan angkanya);
ASUMSI = keputusan arsitek dalam spec ini; BELUM DIVERIFIKASI = wajib
diisi pelaksana dengan output mentah (§3), klaim tanpanya = GAGAL.

| Klaim | Status | Bukti |
|---|---|---|
| Fase 1 LULUS (5/5 butir TERBUKTI, regresi 13/13, boleh naik Lapisan 3) | TERVERIFIKASI (rujukan) | `Audit/reaudit-keempat-batch4-D1-D5.md:11,650-667`, blob `23867354b0baebaeeb9cdef74afd803c902937aa` cocok `git hash-object` saya |
| HEAD = `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` | TERVERIFIKASI | output `git rev-parse HEAD` sesi ini |
| TAU_2023 = `2.5951672079821496e-05`, AUC in-sample `0.8173755150499336`, n 240 (B 111 / A 129), flag 162/240, warmup NaN 19/974 | TERVERIFIKASI (rujukan) | `coder/protokol-H1-H2-H3.md:140-147` + re-audit keempat §4/§7 (TAU bit-identik) |
| Recount gap single-grain = 234 hari / 597 bucket; 479 = artefak grain-campur; varian BATAS SESI = 578/230; nuansa 223/234 counterfactual | TERVERIFIKASI (rujukan) | `coder/protokol-H1-H2-H3.md:192-210`, re-audit keempat §9 (`:633-641`), adjudikasi A |
| Ambang gugur H1 = (i) selisih drift median CI95 memuat 0, ATAU (ii) share trending tak stabil antar-tahun (chi-square p<0.01) | TERVERIFIKASI (rujukan) | `coder/protokol-H1-H2-H3.md:94-96` |
| Ambang gugur H3 = AUC ≤ 0,7 ATAU filter potong >40% hari A tanpa kurangi drawdown; S4 = uji drawdown vs strategi diagnostik L3 pertama, filter DILARANG aktif sebelum S4 | TERVERIFIKASI (rujukan) | `coder/protokol-H1-H2-H3.md:162-164,249-264` |
| Larangan eksklusi buta: DILARANG pakai `gap_f2_flag` untuk eksklusi buta; eksklusi via dua varian + selisih | TERVERIFIKASI (rujukan) | `coder/protokol-H1-H2-H3.md:222-226` |
| D1/D2/D3/D5 + trio beku utuh (hash §12 re-audit keempat) | TERVERIFIKASI (rujukan) | re-audit keempat `:712-726`; pelaksana WAJIB ukur ulang (§3-C3) |
| Pointer `protokol:170-174` untuk status gap = STALE; yang benar §4 `:188-213` (gap `:192-211`) | TERVERIFIKASI (rujukan) | re-audit keempat T-5 (`:612-623`) — spec ini memakai rujukan benar |

---

## Uji 1 — Materialitas gap_f2_flag pada klasifikasi H1

### Proposal Uji (§21)

**Apa yang diuji:** apakah 234 hari ber-flag mengubah kesimpulan
klasifikasi H1 (bukan apakah gap "nyata" — keberadaan 597 bucket sudah
terbukti B1; bukan vonis H1 — uji hipotesis ≠ uji sensitivitas data).
**Hipotesis:** H0 = gap immaterial (verdict gugur-H1 sama pada kedua
varian + distribusi label homogen); H1 = material.
**Populasi terkunci:** 234 hari-broker ber-flag hasil recount
single-grain (jangkar B1; rekonsiliasi `597 = 578 + 19`). Analisis
primer pada 234 penuh; subset 223-counterfactual hanya sebagai cek
robustness (bukan penentu) — nuansa F-2 dihormati tanpa memecah uji.
**Varian (analog F-1, bukan eksklusi):** INK = klasifikasi H1 pada 974
hari; EKS = klasifikasi H1 pada 974−234 = 740 hari. Klasifikasi memakai
`classify_day_label` TERKUNCI (ambang `0.0268`/`88.79`, D1 hash §0 —
reuse read-only, DILARANG ubah kode).
**Baseline:** verdict gugur-H1 varian INK + distribusi label INK
(dihitung dulu, ditempel, baru dibandingkan — §21 butir 7).
**Estimasi biaya:** komputasi read-only menit; nol perubahan repo
(§3-C2 menegakkan).
**Rencana:** hitung M1→M2→M3 berurutan; tempel semua output mentah;
simpulkan MATERIAL/IMMATERIAL/ANOMALI hanya sesudahnya.
**Status:** BELUM DIUJI (protokol `:211`).

### Metrik + ambang (pra-registrasi; dilarang menambah pasca-hoc)

- **M1 (primer, penentu).** Verdict gugur-H1 lock (`protokol:94-96`)
dihitung per varian (GUGUR bila salah satu kriteria terpenuhi, else
TAHAN). **MATERIAL bila verdict EKS ≠ verdict INK** (ke arah mana pun —
membaik maupun memburuk; keduanya = kesimpulan tergantung pada data
yang statusnya belum teruji).
- **M2 (sekunder, penentu).** Homogenitas distribusi label
(trending/normal/range) INK vs EKS, chi-square, α = 0,01 (satu keluarga
uji dengan kriteria stabilitas lock `:96` — bukan angka dari data).
**MATERIAL bila p < 0,01.** Δshare_trending + CI95 bootstrap WAJIB
dilaporkan sebagai efek (bukan penentu).
- **M3 (konsistensi, BUKAN penentu).** Median `ratio_path` hari-gap vs
non-gap vs baseline B1 (gap lebih tenang: 0,0251 vs 0,0280; kausal
+0,019%). **Bila tanda selisih BERBALIK vs B1 → status ANOMALI:**
uji dinyatakan SELESAI-TAPI-ANOMALI, wajib eskalasi ke Arsitek,
DILARANG menyimpulkan MATERIAL/IMMATERIAL darinya.
- **Hasil uji:** MATERIAL (M1 atau M2 positif) / IMMATERIAL (keduanya
negatif + M3 konsisten) / ANOMALI. Selesainya uji (lulus-eksekusi) ≠
hasilnya — §3-C6 menegakkan keduanya terpisah.

### Boleh vs dilarang pakai hasil (§4 menguatkan)

| Hasil dipakai untuk | Status |
|---|---|
| Anotasi sensitivitas pada vonis H1 (bila MATERIAL, vonis H1 wajib lapor kedua varian) | BOLEH |
| Keputusan Arsitek apakah gap-days butuh mekanisme dua-varian ala F-1 (bukan eksklusi) | BOLEH |
| Bila IMMATERIAL: konsumen H1 boleh memakai varian INK tunggal dengan merujuk hasil ini; kolom flag TETAP di store | BOLEH |
| Membuang 234 hari / menonaktifkan flag / menghapus kolom dengan alasan hasil apa pun | DILARANG (protokol `:224`) |
| Memakai uji ini SEBAGAI vonis H1 (lulus/gagal hipotesis) | DILARANG (sensitivitas data ≠ uji hipotesis) |
| Memakai hasil untuk vonis H5 (placebo/kuartil-ATR butuh desain independen; status uji ini hanya konteks) | DILARANG |
| Mengubah ambang/threshold apa pun berdasarkan hasil (optimasi-dari-data) | DILARANG |

---

## Uji 2 — Sensitivitas TAU terhadap span/window alternatif

### Terkunci (referensi; DILARANG diubah)

`TAU_2023 = 2.5951672079821496e-05` (Youden, `>` strict),
span `2023-01-01..2023-12-31`, B = Jan–Jun / A = Jul–Des 2023,
`rv_score = rv_roll_20d / 20`, `RV_WINDOW = 20`, warmup NaN dikecualikan,
AUC in-sample `0.8173755150499336`, sens/spec `1.0 / 0.6047`,
n 240 (B 111 / A 129), flag 162/240 (B 111/111; A 51/129),
urutan lock B > A (3,648e-5 vs 2,292e-5 — basis, bukan ambang).

### Proposal Uji (§21)

**Apa yang diuji:** apakah identitas filter regime stabil di luar span
kalibrasi (bukan mencari TAU "lebih baik" — shopping DILARANG).
**Hipotesis:** H0 = stabil (K1∧K2∧K3); H1 = tidak stabil.
**Alternatif pra-registrasi (TERTUTUP — 4 saja; dilarang tambah
pasca-lihat-hasil):** A1 = span 2024 tahun penuh, split tengah-tahun
sama, W=20, Youden; A2 = span 2025, sama; A3 = span terkunci 2023,
W=10; A4 = span terkunci 2023, W=30. DILARANG: rule selain Youden,
split selain tengah-tahun, span lain, memakai TAU_alt sebagai pengganti.
**Per alternatif, hitung + tempel:** TAU_alt, AUC_alt, n_B/n_A/NaN,
agreement flag vs flag-terkunci pada hari overlapping yang evaluable di
kedua sisi (kappa dilaporkan, bukan penentu).
**Aturan eksekusi gagal:** alternatif dengan <200 hari evaluable =
GAGAL-eksekusi yang dilaporkan (bukan skip senyap).
**Status:** BELUM DIUJI (protokol `:214-217`).

### Kriteria STABIL vs TIDAK (ambang = keputusan arsitek, ASUMSI)

- **K1:** AUC_alt ≥ 0,70 pada SEMUA alternatif (jangkar = ambang gugur
H3 lock; filter yang jatuh di bawah ambang lock pada span wajar =
tidak robust).
- **K2:** agreement ≥ 90% (flip ≤ 10%) pada hari overlapping evaluable.
- **K3:** urutan strata kekal (median `rv_score` B > A, konsisten basis
lock) pada semua alternatif.
- **STABIL** = K1∧K2∧K3. **MARJINAL** = tepat satu gagal tipis
(AUC_alt ∈ [0,65–0,70) ATAU agreement ∈ [80–90%)) — margin ini ASUMSI
arsitek: ketat karena filter menggerakkan keputusan, longgar karena
sampling; didokumentasikan di sini agar bisa diaudit, bukan dari data.
**TIDAK STABIL** = selain itu (≥2 gagal, atau AUC_alt < 0,65, atau
agreement < 80%).

### Dampak ke vonis H3 (S4)

S4 = uji drawdown vs strategi diagnostik L3 pertama; filter DILARANG
aktif sebelum S4 dievaluasi (protokol `:249-264`).

- **STABIL →** S4 berjalan normal dengan TAU terkunci; tabel
sensitivitas dilampirkan sebagai bukti robustness.
- **MARJINAL →** S4 boleh berjalan (TAU terkunci) tetapi vonis H3 final
DITUNDA sampai evaluasi drawdown selesai; dokumen S4 wajib lapor varian
terkunci + varian gagal-tipis.
- **TIDAK STABIL → H3 GUGUR via kriteria tambahan S4b.** S4b adalah
keputusan arsitek DALAM SPEC INI, BUKAN lock: filter tanpa identitas
stabil tidak dapat dipegang; dilarang mengaktifkan filter pada data mana
pun. S4b tidak mengubah ambang lock, tidak memvonis H1/H2/H4/H5, dan
tidak memberi izin kalibrasi ulang (Q1(a) tetap: DILARANG kalibrasi
ulang di luar span 2023).

---

## §3. Kriteria selesai Lapisan 3-H3 (mesin + output mentah)

**Aturan besi (tulis eksplisit): Klaim tanpa output mentah = GAGAL.**
Setiap angka di dokumen hasil wajib tertaut ke blok output bernomor
[O1]…[On]; auditor memverifikasi dengan mencocokkan ulang, bukan dengan
membaca narasi. Dokumen hasil kontrak: `coder/hasil-lapisan3-H3.md`
(memuat tabel Klaim & Bukti §5 + semua [On]).

| # | Syarat | Perintah mentah (jalankan, tempel output) | Pola lolos |
|---|---|---|---|
| C1 | HEAD tak berubah | `git rev-parse HEAD` | `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` |
| C2 | Nol tulis produksi + nol sentuh lindung | `git status --porcelain -- src/ tests/ data/ configs/` ; `git diff HEAD --name-only -- src/features/build_features.py tests/test_build_features.py data/features/M15/ reports/governance/2026-10-07/arsitek/hipotesis_lock_v1.md reports/governance/2026-10-07/arsitek/putusan-arsitek-B1.md reports/eda/` | kedua output KOSONG |
| C3 | Hash D1/D2/D3/D5 + trio beku cocok | `git hash-object src/features/build_labels.py tests/test_build_labels.py coder/protokol-H1-H2-H3.md coder/laporan-final-fase1.md src/features/build_features.py tests/test_build_features.py data/features/M15/usdjpy_m15_features.parquet` | `2561efd5…` / `dc07a7e6…` / `bc17e5de…` / `34530854…` / `399e64b3…` / `ed7ac435…` / `07402f40…` (prefix; §0/§12 re-audit keempat) |
| C4 | Gate hijau | `pytest` penuh ; `ruff check .` ; `ruff format --check .` ; `venv/Scripts/python.exe scripts/check_foreign_chars.py coder/hasil-lapisan3-H3.md` | 0 fail/skip (N passed dicatat), All checks passed, 37 formatted, OK asing |
| C5 | Determinisme uji | skrip uji-1 + uji-2 di `%TEMP%\opencode\l3h3` dijalankan 2×, `sha256` berkas angka-hasil ditempel keduanya | kedua hash IDENTIK per uji |
| C6 | Uji-1 selesai + hasil diputus | angka M1 (verdict INK, verdict EKS), M2 (χ², p), Δshare+CI95, M3 (2 median) ditempel [On] | M1+M2 terhitung → LULUS-eksekusi; MATERIAL/IMMATERIAL/ANOMALI per §Uji-1 |
| C7 | Uji-2 selesai + hasil diputus | tabel 5 baris (ref+A1…A4: TAU/AUC/n/agreement) + keputusan K1–K3 ditempel [On] | STABIL/MARJINAL/TIDAK STABIL per §Uji-2 |
| C8 | Dokumen hasil final | `git hash-object coder/hasil-lapisan3-H3.md` SESUDAH penulisan terakhir (contoh benar) ditempel | hash tercatat; contoh SALAH: "pastikan hash benar" tanpa output |
| C9 | Staged = 0, tanpa commit | `git status --porcelain` (amati staged) ; `git log --oneline -1` | nol entri staged, HEAD tetap C1 |

Skrip analisis HANYA di `%TEMP%\opencode\l3h3` (tidak di-commit;
C2 menegakkan). D4 di disk tidak ditimpa (`out_dir` temporer bila
`main()` dipakai — preseden re-audit keempat §0.4).

---

## §4. Batasan eksplisit

1. **H4/H5 DILARANG vonis final** sebelum KEDUA uji tercatat
(C6+C7 lulus + C8 ter-hash). H4/H5 hanya berjalan dengan protokol
karantina yang sudah terimplementasi (protokol `:266-279`).
2. **Eksklusi buta TETAP DILARANG** (protokol `:222-226`) — hasil
MATERIAL bukan izin eksklusi; hasilnya memicu dua-varian, bukan
pembuangan.
3. **Tidak menyentuh file lock/EDA/fondasi B1** — daftar lindung di
C2; pelanggaran = gagal total (preseden putusan fix DILARANG-1).
4. **Tidak mengubah kode produksi** — D1/D2/D3/D5 beku pada hash §0;
perubahan apa pun = prasyarat re-audit baru, bukan bagian Lapisan 3-H3.
5. **Tidak ada backtest, tidak ada H6+, tidak ada ambang baru.**
S1–S6 mengikat kata-per-kata; dokumen audit menang atas ringkasan.
6. **Peran (§26):** Coder mengeksekusi read-only + menulis dokumen
hasil; Auditor memverifikasi adversarial; Arsitek tie-break bila
konflik (Arbitrase §27). Coder DILARANG audit sendiri.

---

## Self-audit 1×

1. Lingkup = 2 prasyarat H3 saja: tidak ada instruksi H4/H5 selain
larangan, tidak ada langkah eksekusi selain perintah verifikasi C1–C9,
tidak ada perubahan kode/data/ambang.
2. Setiap ambang penentu tertaut ke lock (M1→`:94-96`, M2→α lock,
K1→ambang H3, K3→basis lock) atau dilabel ASUMSI dengan rasional
(margin MARJINAL, S4b) — tidak ada angka dari data evaluasi.
3. Semua rujukan baris mengikuti T-5 yang diperbaiki (`:192-211`,
`:214-217`, `:222-226`), bukan pointer stale `:170-174`.
