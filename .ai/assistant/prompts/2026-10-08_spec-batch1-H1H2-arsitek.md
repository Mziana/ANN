# DRAF PROMPT ARSITEK — Spesifikasi Lapisan 3 Batch-1 (Vonis H1 + H2) — 2026-10-08

> Status draf: disusun Asisten, ditampilkan di chat, menunggu user paste ke arsitek.
> Substansi §3 verbatim dari lock/putusan/protokol. Asisten tidak menambah substansi.

# PROMPT ARSITEK — Spesifikasi Lapisan 3 Batch-1 (Vonis H1 + H2)

## 1. Peran dan mandat

Anda **Arsitek** menurut `.ai/AGENTS.md` §26: merancang + memutus konflik. **DILARANG menulis kode produksi/implementasi.** Kontrak bersama yang mengikat pekerjaan ini: `.ai/AGENTS.md` v3.0 — §5 (tabel Klaim & Bukti; dilarang "sepertinya OK"), §20 (setiap klaim wajib bukti; output asli ditempel), §21 (uji dulu, simpulkan kemudian; format Proposal Uji), §26 (peran terpisah), §27 (arbitrase).

## 2. Lingkup sempit

Tulis **spesifikasi eksekusi Batch-1**: uji vonis **H1** + backtest **H2**. **BUKAN eksekusi. BUKAN vonis H1/H2** (vonis = putusan terpisah sesudah re-audit). BUKAN H3 (sudah GUGUR via S4b — filter dilarang di data mana pun), BUKAN H4/H5 (batch-2 terpisah). DILARANG mengubah redaksi/ambang lock kecuali addendum berversi. DILARANG menyentuh file beku (§6).

## 3. Bahan mengikat (verbatim — spec wajib merujuk ini, bukan parafrasanya)

**3a. H1** (`arsitek/hipotesis_lock_v1.md` §H1): conditioning tipe hari dengan identifikasi H+1 pagi memakai data t-1 saja; drift berarah RELATIF M15 4 jam pertama London dinormalisasi ATR harian t-1, hari trending vs range, sign test + CI. Ambang klasifikasi: trending = ratio_path > 0,0268 AND range_atr > 88,79; range = keduanya ≤ median-A; sisanya normal. **Ambang gugur: selisih drift median CI95 memuat 0, ATAU share trending tak stabil antar tahun (chi-square antar-tahun p<0,01).** Catatan ex-post: ambang tipologi = median full-sample A → share deskriptif ex-post; uji memakai identifikasi real-time. Risiko reversal-day tercatat tiga lapis tanpa penanganan khusus. **Klausul anti-penyelamatan (mengikat):** *"Cemaran reversal-day yang tercatat di sini BUKAN dasar untuk menafsir ulang kegagalan H1. Conditioning usia-tren pasca-hoc setelah melihat hasil = hipotesis baru yang wajib pra-registrasi segar dan diuji di data segar."* Izin eksplorasi: split-usia tren boleh dilaporkan sebagai eksplorasi murni, tanpa pengaruh pada vonis.

**3b. S1** (`arsitek/putusan-arsitek-H1-H5.md:4-5`): *"H1 — KUATKAN. Redaksi + ambang + catatan risiko + klausul anti-penyelamatan + izin eksplorasi disahkan tanpa perubahan."*

**3c. H2** (`hipotesis_lock_v1.md` §H2): EV per trade strategi M5/M15 momentum sederhana − cost_basis mean sesi (fragmen 4b), walk-forward per tahun. **Ambang gugur: EV-after-cost median ≤ 0 di ≥2 dari 3 tahun utuh 2023–2025 OOS (2026 parsial dikecualikan; ambang 4-tahun MENUNGGU DATA), ATAU rata-rata VR OOS ≤ 1.**

**3d. S2** (`putusan-arsitek-H1-H5.md:6-8`): *"(a) median = median EV-per-trade-after-cost dalam-tahun (2023/2024/2025; gugur bila ≤0 pada ≥2 tahun); (b) strategi diagnostik wajib pra-registrasi di Lapisan 3 sebelum uji."*

**3e. Pra-registrasi H2 yang sudah ada** (`coder/protokol-H1-H2-H3.md` §1): strategi "H2 M15 momentum" — entry 1×/hari saat close > open jam 15 UTC dengan konfirmasi hari sebelumnya diawali tren (hari trending H1); exit saat close < open jam terakhir atau hari habis; SL = 1× ATR 14-hari satuan harga JPY (ATR mentah, bukan normalisasi); TP = 2× ATR; biaya = cost_basis mean sesi; DILARANG spread lain tanpa justifikasi. Status: dokumen saja, backtest BELUM dieksekusi.

**3f. Standing rule putusan H3** (`arsitek/putusan-lapisan3-H3.md` P-1/P-2/P-3, mengikat batch berikut): provenans wajib exact-comparison atau toleransi eksplisit (isclose-default dinyatakan tak memadai; pelanggaran = temuan); sampel bersarang wajib estimator paired yang valid + level CI selaras alpha penentu; pola "output KOSONG" DIPENSIUNKAN — buktikan via tracked-only atau before/after.

**3g. Konteks hasil kemarin** (rujukan, bukan untuk diubah): Uji-1 IMMATERIAL (M1 GUGUR=GUGUR INK 974 vs EKS 740; M2 p=0,6294; M3 tanda sama B1) → konsumen H1 boleh memakai varian INK tunggal, kolom flag TETAP di store. Q1 di bawah lahir dari fakta M1 ini.

## 4. Dua pertanyaan yang WAJIB diputus di dalam spec

- **Q1:** Verdict-lock M1 berbunyi GUGUR pada INK maupun EKS. Apakah itu sudah = **vonis H1 GUGUR**, atau uji real-time H+1 tetap berjalan? Bila tetap berjalan, tulis eksplisit relasi kedua vonis itu (apa yang terjadi bila hasilnya berbeda arah).
- **Q2:** Pra-registrasi H2 (§3e) diratifikasi **apa adanya** atau **direvisi**? Bila direvisi, tulis versi finalnya kata-per-kata di spec (jam entry, syarat konfirmasi, SL:TP, biaya) — revisi di sini = bagian spec, bukan optimasi-dari-data (backtest belum pernah jalan).

## 5. Isi spec yang diminta

1. **§0 tabel Klaim & Bukti** (§5): tiap rujukan §3 diukur/dikonfirmasi ulang (c-status: TERVERIFIKASI / rujukan / ASUMSI / BELUM DIVERIFIKASI). Kutipan baris/path wajib verifikasi ulang (path bisa pindah, baris bisa bergeser).
2. **Proposal Uji §21 per hipotesis** (apa diuji, hipotesis H0/H1, populasi terkunci, baseline dihitung-dulu-ditempel, estimasi biaya, rencana, status). Populasi/alternatif TERTUTUP — dilarang tambah pasca-lihat-hasil.
3. **Metrik + ambang pra-registrasi**, masing-masing tertaut ke lock (§3a/§3c) atau dilabel **ASUMSI** dengan rasional terdokumentasi. Tidak ada angka dari data evaluasi.
4. **Kriteria selesai mesin** (meniru pola C1–C9 spec H3): **tiap syarat WAJIB dipasangkan dengan perintah mentah yang outputnya wajib ditempel coder** (contoh benar: "tempel output `git hash-object <file>` SESUDAH penulisan terakhir"; contoh SALAH yang dilarang: "pastikan hash benar"). **Tulis eksplisit: klaim tanpa output mentah = GAGAL.** Mencakup minimal: HEAD tak berubah, nol tulis produksi + daftar lindung, hash beku cocok, gate hijau (full-suite + ruff + cek karakter asing, sebut rc + cakupan), determinisme 2×, angka uji ditempel bernomor, dokumen hasil + hash, staged 0 tanpa commit. Skrip analisis HANYA di `%TEMP%`, D4 tidak ditimpa.
5. **Larangan eksplisit**: vonis H3/H4/H5 di batch ini; eksklusi buta (dua-varian + selisih bila relevan); shopping ambang/rule/alternatif dari data; kalibrasi ulang apa pun; guard yang membandingkan nilai dengan dirinya sendiri; fixture seragam untuk klaim sensitivitas; output parsial berlabel proses penuh; klaim "diuji via X" sambil mengaku belum ada test X; menaikkan severity temuan tertutup; grain selain hari-broker tunggal (`utc.normalize()` dilarang).
6. **Relasi ke konsumen hilir** (gaya "boleh vs dilarang pakai hasil"): untuk apa hasil H1/H2 boleh dipakai (vonis masing-masing; anotasi sensitivitas INK bila MATERIAL — preseden Uji-1) dan untuk apa DILARANG (vonis silang H4/H5, ubah ambang, buang data/flag).

## 6. Output yang diperintahkan

Tulis spec sebagai file **`reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H1H2.md`**, lalu di chat tempel: `git hash-object` file tersebut + HEAD + `git status --porcelain` + status Q1/Q2 (diputus yang mana + satu paragraf alasan). Tanpa keempatnya, spec dianggap belum diserahkan.

## 7. Self-audit 1× (tulis di akhir spec)

1. Tidak ada instruksi eksekusi selain perintah verifikasi; tidak ada vonis; tidak ada perubahan kode/data/ambang.
2. Setiap ambang tertaut ke lock atau ASUMSI berlabel — tidak ada angka dari data evaluasi.
3. Q1 dan Q2 keduanya diputus eksplisit dengan alasan.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness (substansi §3 verbatim dari lock/putusan/protokol? Q1/Q2 eksplisit? perintah .md + path ada? angka persis — 0,0268/88,79/2,5951…e-05/0,8174/p=0,6294/974/740?)
Putaran 2 — Bias & Asumsi (adakah ambang baru yang diselipkan? adakah arahan hasil tersembunyi? apakah revisi H2 bebas konflik — backtest belum jalan sehingga revisi = desain, bukan fitting?)
Putaran 3 — Meta-check (brief mandiri tanpa pointer internal? ruang putusan nyata arsitek di Q1/Q2 terjaga? larangan bentuk-spesifik mencakup pelajaran H3: P-1/P-2/P-3, C2, ANOMALI?)

Akhir draf 2026-10-08.
