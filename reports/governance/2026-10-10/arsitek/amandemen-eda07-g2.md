# Amandemen Arsitek EDA-07: Perbaikan S8-G2 (cacat kriteria terbukti)

Peran: Arsitek (rangkap asisten atas perintah user 2026-10-10).
Tanggal: 2026-10-10. Status: MENGIKAT, menambal spec EDA-07 S8-G2 saja.
P-1 s/d P-6 putusan-eda06.md tetap utuh. S1-S7, S8-G1/G3/G4, S9 spec
EDA-07 tetap utuh kecuali yang diubah di sini.

## A-1 Cacat yang diterima sebagai fakta

Coder STOP tepat di gerbang kontrol sel 15 (alarm round_d 5/5, dst.),
tidak bypass, sesuai KONTRAK_07. Akar sebab TERBUKTI dengan kode MI asli
di data null murni: MI semester (n_sem) vs lantai pooled (n_tot ~= 5x)
lolos 5/5 pada semua n (300 s/d 30000/semester). Sebab: bias Miller-Madow
~= sel-terisi/(2n) membuat MI semester terinflasi ~5x relatif terhadap
lantai pooled; syarat arah-sama tidak menolong pada ratusan pasangan.
Satu akar, dua gejala: gerbang kontrol tak pernah berpeluang lolos, dan
G2 fitur longgar (mock: 21/62 LOLOS pada derau murni). Ini cacat kriteria
spec, bukan bug kode. Coder dipuji: gerbang pra-registrasi berfungsi
persis sebagaimana dirancang (menangkap metodologi yang salah, bukan sial).

## A-2 Putusan atas 4 opsi coder

- (a) Lantai per-semester: DITOLAK sebagai utama. Benar secara statistik
  tetapi mengalikan biaya lantai (bottleneck run =70 mnt) ~5x menjadi
  berjam-jam, tanpa menambah ketajaman melebihi opsi (c).
- (b) Koreksi bias Miller-Madow: DITOLAK sebagai utama. Koreksi orde-satu
  berderau pada sel jarang (20 kuantil x label, n kecil); menambah
  konstanta yang bisa diperdebatkan tanpa menghilangkan kebutuhan
  banding-se-n-sama.
- (c) Revisi kriteria G2: DITERIMA. Alasan: satu-satunya opsi yang
  menghilangkan bias secara struktural (banding selalu pada n yang sama)
  dengan nol biaya komputasi tambahan, sambil mempertahankan maksud
  G2 (informatif + stabil).
- (d) Pisahkan kontrol struktural: DITOLAK mandiri (tidak memperbaiki
  kriteria; hanya menafsir ulang alarm). Diadopsi sebagian di A-4.

## A-3 G2 revisi (menggantikan S8-G2 spec, mengikat)

- G2a (informatif, se-n-sama): MI pooled (semua semester digabung, n_tot)
  > lantai derau pooled p95 pada n_tot yang sama. Kedua sisi pada n
  yang sama sehingga bias-MM menempel di kedua sisi (lantai ADALAH
  distribusi null pada n itu) dan saling meniadakan dalam perbandingan.
- G2b (stabil, tanpa banding-MI): arah lift sama pada >= 4 dari 5 semester
  (tanda lift per semester, bukan perbandingan MI-vs-lantai).
- Fitur lolos G2 bila G2a DAN G2b. Aturan alarm kontrol TETAP: satu kontrol
  pun lolos G2-revisi = ALARM STOP (KONTRAK_07 tidak dilonggarkan).
- G1, G3, G4 tidak berubah. Ambang lain tidak berubah. DILARANG memakai
  amandemen ini untuk menggeser ambang apa pun.

## A-4 Klausul adjudikasi kontrol struktural

Bila di bawah G2-revisi suatu kontrol struktural (round_d, pdhl_d) tetap
lolos sementara noise murni tidak, itu BUKAN kegagalan otomatis melainkan
temuan yang wajib diadjudikasi: coder STOP, simpan bukti, arsitek memutus
apakah itu sinyal mikrostruktur asli (mis. clustering harga) atau artefak
residual. DILARANG mengabaikan maupun memisahkan diam-diam.

## A-5 Pengerasan eksekusi (pelajaran run C, mengikat)

- Log-then-assert: daftar alarm PENUH + tabel skrining (60 LA + 200 waktu)
  + laju kontrol pooled DICETAK KE DISK SEBELUM assert gerbang. STOP di
  masa depan tidak boleh lagi menghilangkan bukti (kerugian run C).
- Checkpoint per-irisan: tulis CSV per irisan selesai agar abort tidak
  menghapus progres; progres fraksi (irisan x/30, tahap) ke file log.
- 8 bugfix sepanjang jalan DITERIMA sebagai debugging (semua crash/fatal,
  nol perubahan ambang/logika penentu). Auditor wajib verifikasi: diff
  konstanta ambang vs spec + determinisme rerun bit-identik.
- Task Scheduler EDA07Build boleh didaftarkan ulang untuk rerun detached;
  hapus setelah selesai (schtasks /delete /tn EDA07Build /f).

## A-6 Otorisasi rerun + penugasan auditor

- Coder: terapkan A-3 + A-5 pada builder (mock smoke sel 15-18 ulang),
  lalu full-run ulang detached =70-90 mnt, verifikasi registry, tulis S5.
- Auditor (nanti): reaudit EDA-07 mencakup (i) G2-revisi sesuai A-3 tepat,
  (ii) nol drift ambang dari 8 bugfix, (iii) bukti log-then-assert ada di
  disk, (iv) rerun deterministik. Tanpa itu vonis auditor MOOT.
