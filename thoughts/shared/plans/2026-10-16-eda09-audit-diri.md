# Audit Adversarial Diri — Draf Blueprint EDA-09 (2026-10-16)

> Auditor: Commander (peran-ganda terpaksa: penulis draf = auditor draf;
> bias dicatat, bukan disangkal — pembaca harap curiga ganda).
> Sasaran: `thoughts/shared/plans/2026-10-16-eda09-wick-confirm-draf.md` (223 baris).
> Metode: baca-ulang penuh + verifikasi tiap sitasi ke blueprint EDA-08
> (243 baris, dibaca penuh) + builder EDA-07-spike (`_build_eda07_spike_anatomy.py`)
> + builder EDA-08 + notebook EDA-08 di main.
> Hasil: 0 FATAL · 4 HIGH · 6 MEDIUM · 4 LOW. Desain inti (satu-arah,
> cut-lock, volume 0-uji) TAHAN; yang bocor = pagar pelaksanaan.

## FATAL — tidak ada

Desain inti benar: klaim directional terkunci → uji satu-arah; cut dari R;
famili tepat-1; volume pendamping 0-uji; P segel. Tidak ada cacat yang
memaksa rancang-ulang. (Dicatat eksplisit agar "nol FATAL" bisa digugat.)

## HIGH

### H1. Kill tanpa penjaga daya — GUGUR bisa dijatuhkan oleh bukti lemah
- Serangan: vonis GUGUR bersifat final ("tanpa banding", §2) dan membunuh
  satu-satunya kandidat program. Tapi draf tak mensyaratkan daya minimum
  V. Bila pipeline-V menghasilkan n jauh di bawah ekspektasi (≈1020 —
  mis. masalah data 2025, cleaning bergeser), p ≥ 0,05 berarti
  *absence of evidence*, namun aturan menjatuhkan *evidence of absence*.
  False-kill atas kandidat tunggal = kerusakan program permanen.
- Terkait: degenerasi cut-terkunci. Bila distribusi wick-2025 bergeser
  rezim, cut-R bisa menaruh <30 event di grup atas/bawah suatu band —
  Δ pooled jadi tak stabil, namun tetap diputus CONFIRM/GUGUR.
- Usul patch (preregistered, konservatif-searah-benar — hanya bisa
  MENCEGAH kill palsu, tak bisa memalsu CONFIRM):
  F2 ditambah tripwire daya: (a) total n-V < 500 (≈50% ekspektasi) →
  STOP + arsitek (BUKAN GUGUR); (b) grup tercil mana pun (atas/bawah ×
  4 band) n < 30 (standar POWER_MIN_N warisan program, bukan angka baru) →
  STOP + arsitek. Keduanya tripwire, bukan drop-diam.

### H2. P5 terlalu ketat — kebutaan rezim yang relevan-trading
- Serangan: larangan split-temporal TOTAL (bahkan deskriptif) mencegah
  narrative mining, tapi juga membutakan kematian-rezim: efek hidup di H1
  dan mati di H2 tetap lolos pooled-CONFIRM, lalu ANN mewarisi fitur mati.
  Untuk program trading, ini mode-kegagalan material — vonis "benar"
  statistik, salah dagang.
- Usul patch (tanpa permukaan HARKing): SATU split preregistered H1/H2,
  deskriptif-saja + aturan-interpretasi preregistered ("tanda berlawanan
  antar-semester → regime-caveat di laporan, VONIS TAK BERUBAH; arsitek
  menilai implikasi ANN"). Vonis tetap satu-uji; yang ditambah = konteks
  yang tak bisa dipakai menggeser vonis.

### H3. Celah seed-shopping di perbatasan
- Serangan: p dilaporkan tanpa aturan pengulangan. Bila p = 0,051, coder
  (manusia, di bawah tekanan) tergoda re-run dengan seed "koreksi".
  Satu run draf ini = satu vonis final — insentif shopping maksimal,
  larangan nol. Draf melarang tuning konstruksi tapi lupa tuning acak.
- Usul patch: "satu seed, satu run; DILARANG re-seed untuk alasan apa pun
  kecuali bug terbukti (STOP + arsitek); p dilaporkan 4 desimal; kerapuhan
  perbatasan (0,04–0,06) dicatat apa adanya sebagai caveat, bukan alasan
  run-ulang." Tambahkan ke §5 + F4.

### H4. T_DAY/cls: lock-vs-recompute tak dispesifikasi → STOP palsu
- Serangan (TERVERIFIKASI kode): pipeline spike menghitung
  `T_DAY = P25(ctx)` dengan assert keras `round(T_DAY,4) == 1.7319`
  (`_build_eda07_spike_anatomy.py` L271–273). Klausa draf "reuse kode,
  bukan tulis ulang" + "tuning DILARANG" membuat coder-V mustahil patuh:
  recompute di 2025 hampir pasti ≠ 1,7319 → assert meledak → STOP palsu;
  mengunci manual = "tulis ulang" yang dilarang.
- Blast-radius TERBATAS (terverifikasi): drop/outcome/band tak memakai cls
  (drop = room-logic L461 `no_room_16`; cls hanya metadata + stratifikasi
  donor yang SUDAH MATI di EDA-08). Jadi ini pemblokir-eksekusi, bukan
  perusak-inferensi — tetap HIGH karena menghentikan ronde.
- Usul patch (§3): "T_DAY = 1,7319 DIKUNCI sebagai konstanta untuk V
  (warisan R, bukan recompute); assert-vs-EDA-06 dicabut TERTULIS untuk
  V; kolom cls/ctx tetap dihitung sebagai metadata (integrity), nol peran
  putusan." Satu baris mematikan seluruh ambiguitas.

## MEDIUM

### M1. Justifikasi "tanpa floor" salah alamat prosedur
- Serangan: §10 menolak floor-5pp dengan alasan "geser gawang
  pasca-registrasi". Tapi V masih virgin — draf INI registrasinya. Tak ada
  gawang yang digeser; argumen proseduralnya batal. Pertanyaan substantif
  tetap terbuka: bolehkah efek +0,5pp dengan p = 0,04 lolos CONFIRM?
- Rekomendasi (bukan perintah): PERTAHANKAN tanpa-floor tapi dengan alasan
  benar — (a) floor 5pp mewarisi arbitrariness R (Opsi-A-6pp DITOLAK
  tercatat justru karena angka-garis arbitrer); (b) materialitas diputus
  ANN + P-segel, bukan V; (c) Δ̂_V dilaporkan eksak sehingga tahap ANN
  melihat magnitudonya. ATAU preregistrasi floor-warisan-5pp sekarang
  (sah — V belum tersentuh). Pilih satu, tulis alasannya; jangan
  pertahankan argumen yang salah.
- Catatan penguat satu-arah (independen): ke-4 band-R bertanda positif
  (recompute: +0,1177/+0,0701/+0,1429/+0,3264) — arah unanimous, bukan
  artefak pooling. Layak dikutip di §10.

### M2. Penumpukan-V: konfirmasi dan validasi memakai dataset sama
- Serangan: desain program (Amandemen-1 EDA-06): ANN-01 train R, validasi V,
  test P. Bila V dipakai mengkonfirmasi wick LALU dipakai memvalidasi ANN
  yang memakai wick, validasi tak independen dari seleksi-fitur. Draf diam
  soal ini — padahal vonis EDA-08 ("joint = estimasi", "V hanya untuk
  pertanyaan baru") menunjukkan program peduli independensi.
- Usul patch (§9, satu kalimat jujur): "V dipakai dua kali (konfirmasi +
  validasi-ANN); independensi validasi TERBATAS; hakim final = P-segel
  yang pristine. CONFIRM-V = izin-masuk-ANN, BUKAN vonis-dagang."
  Ini tidak mengubah desain — hanya melarang pembacaan-berlebih.

### M3. F0 "= ronde batal" melebih-lebihkan STOP
- "STOP bila gagal (fondasi goyang = ronde batal)". STOP dalam konvensi
  program = arsitek menilai, BUKAN batal otomatis. Tanda "=" ini menutup
  diagnosis yang justru tugas STOP (mis. drift versi-numpy pada quantile
  → toleransi 1e-9 gagal padahal cut identik secara makna).
- Usul: hapus "= ronde batal"; tambah "...STOP + arsitek mendiagnosis
  (bedakan fondasi-goyang vs artefak-numerik)".

### M4. Kolom gugur di V: hitung-boleh, lapor/tanya-jangan
- Coder-V wajar mereuse pipeline yang menghitung first/gap/dow (EDA-08
  bahkan merecompute first sebagai integrity-check, builder L242–257).
  Draf melarang "tanya-ulang" tapi tak menyebut pelaporan deskriptif —
  celah narasi-kebangkitan ("rate first di V tampak...").
- Usul (§3, satu baris): "kolom first/gap/dow BOLEH ada sebagai artefak
  pipeline (integrity); DILARANG dilaporkan, diuji, atau dinarasikan."

### M5. F1 tanpa sanity bar-M15 (pola Cek-3 EDA-06 tak diwarisi)
- F1 punya STOP-band hari (<200/>320) tapi tak ada sanity volume data:
  259 hari × ~96 bar ≈ 20–28k bar M15. Korupsi parsial 2025 bisa lolos
  day-count namun meracuni deteksi.
- Usul (skala dari Cek-3 EDA-06: 384 hari → 30–42k, STOP <20k/>60k):
  "bar M15-V ekspektasi ≈20–28k; STOP-band <13k atau >40k."

### M6. Spesifikasi CI + direktori laporan menggantung
- CI cluster-per-day tanpa B; direktori reports tak dinamai. B = 10000
  (murah, konsisten null) + `reports/eda/2026-10-16-eda09/` + manifest.
  Kecil, tapi "prereg penuh" menuntutnya tertulis.

## LOW

- L1. A2 "sampling audit" → assert exhaustive (murah di kode: konvensi
  batas `lo_<=x<hi_` bisa diassert untuk SEMUA event-V, bukan sampel).
- L2. Jejak §12: "§1 = STATE + vonis" — angka vonis sebenarnya dari
  artefak (builder/notebook), bukan STATE. Presisi sitasi.
- L3. Volume deskriptif perlu didaftar eksplisit (med/IQR/P1/P99 +
  cakupan baseline + count-drop, cermin Sel-8 EDA-08) agar "tanpa klaim"
  tak menjadi narasi-bebas.
- L4. F1 tick_volume ≥ 0,95 mewarisi EDA-08 — catat bahwa ambang ini untuk
  bar-s-V (definisi bar-s = bar analisis, koreksi ronde-7 temuan 6),
  bukan agregat; draf sudah bilang "bar-s-V", tinggal tegaskan rujukan.

## Kompatibilitas ANN — verdict

KOMPATIBEL dengan satu caveat tercatat (M2). Wick = fitur per-event,
lagged-causal, dependensi end-detector sudah dicatat sekali (§9).
Volume-(c) = stateful (baseline 20-hari/slot); ronde ini justru
mendemonstrasikan jalur precompute R→V yang akan dipakai produksi
(update harian). Heterogenitas band3-dominan (0,3264 vs pooled 0,1682)
bukan masalah ANN (interaksi band dipelajari di training) — draf benar
membatasinya ke soal-klaim, bukan soal-fitur. Tidak ada yang diminta
draf ini yang tak bisa dipakai ANN; tidak ada yang dipakai ANN yang
tak dikunci draf ini — kecuali independensi-validasi (M2).

## Perilaku aturan — ringkas

- Terlalu KETAT: P5 (H2 — butakan rezim). Sisanya proporsional.
- Terlalu LONGAR: kill tanpa daya (H1), seed (H3), floor (M1),
  pelaporan kolom-gugur (M4).
- Tepat: famili-1, cut-lock, satu-arah, larangan resurrection,
  whitelist dua-arah, warmup-V-tanpa-drop (alasan eksplisit benar).

## Jejak verifikasi (klaim → bukti, §20)

| Klaim audit | Bukti |
|---|---|
| T_DAY assert 1,7319 | `_build_eda07_spike_anatomy.py` L271–273 |
| cls tak gate drop/outcome | drop = `no_room_16` (L461); cls → metadata + donor-mati (L798–804) |
| first direcompute sbg integrity di R | `_build_eda08_ammo_R.py` L242–257 |
| ANN-01 train R / validasi V / test P | Amandemen-1 EDA-06 (grep pra-compaction, v94 L39) |
| POWER_MIN_N / n<30 standar program | builder L801–804 (`_sc[k] >= POWER_MIN_N`) |
| Semua band-R positif | recompute independen pra-compaction |
| Cek-3 bar-band pola | blueprint v93/v94 §Cek-3 (30–42k, STOP <20k/>60k) |
