# Putusan Adjudikasi Re-audit Kedua — A/B/C — 2026-10-08

**Peran:** Arsitek. Tanpa kode. Tanpa vonis H4/H5. Hanya 3 butir.
**Dasar (audit menang atas ringkasan):**
`Audit/reaudit-kedua-fix-D1-D5.md` blob `1f99203711e92afa77166de9d6a0184a44463e19`
(TERVERIFIKASI via `git hash-object`),
`arsitek/putusan-arsitek-fix-D1-D5.md` blob `ca57e7647e955ee0dfe68579db5dbef6216a427b`
(TERVERIFIKASI — vonis saya sendiri),
`Audit/reaudit-adversarial-D1-D5.md` (#14–#19),
`arsitek/putusan-arsitek-H1-H5.md` (S1–S6),
`coder/protokol-H1-H2-H3.md`, `src/features/build_labels.py` (worktree, unstaged).
**Berdiri, jangan dibongkar:** ambang H1 `0.0268`/`88.79`, karantina 19 hari,
impor satu arah, 9/9 prohibisi, 3 hash artefak lama, fides jendela London
(#15-tertutup: `is_london` 100%, first-16 identik 974/974 —
reaudit-kedua `:44-53`).

---

## A. #23 — gap 479 vs 234: pilih (c) RUMUSKAN ULANG

**Fakta yang mengikat (semua dari dokumen audit):**

1. Asal 234: `audit/audit-fondasi-B1.md:122` — "1.281 bucket parsial;
597 di antaranya mid-day (**bukan boundary sesi**) — spread di **234 hari
broker**." Grain = broker-day, edge-rule = BATAS SESI.
2. Definisi Q3(a) saya (`putusan-arsitek-fix-D1-D5.md:83-89`): bucket parsial
= `m1_bars` < 15 DAN **bukan bucket pertama/terakhir hari-broker**
(edge-rule = BATAS HARI); "Target verifikasi: tepat 234 hari (angka reaudit
F-2) — selisih = gagal."
3. Hasil audit (`reaudit-kedua-fix-D1-D5.md:312`): "Implementasi **cocok
persis** dengan definisi arsitek (`m1_bars<15` ∧ bukan bucket tepi): hitung
ulang independen saya = 479 juga. Tetapi tidak ada varian yang mereproduksi
234: definisi-arsitek=479, tanpa-exclude-edge=607, broker-day+exclude-edge=0."
Eskalasi (`:336`): "Arsitek harus memutuskan: koreksi definisi, koreksi
target, atau rumuskan ulang. Auditor tidak memutus ini."
4. Grain implementasi salah (`:310`, #21): `compute_london_drift_4h`
mengelompokkan per UTC-midnight (`build_labels.py:200`) — 200 bar hantu,
1174 UTC-day vs 974 broker-day. Flag gap (1174 entri, `:50`) dihitung di
atas index grain-campur yang sama.

**Adjudikasi — mengapa bukan (a) dan bukan (b):**

- (b) "koreksi target ke 479" DITOLAK. 479 dihitung pada grain UTC + 200
hari hantu (`:310-312`); mengesahkannya berarti mengontrakkan bug grain
(#21) menjadi kebenaran. Angka di atas index yang salah bukan kandidat
target.
- (a) "definisi baru hasilkan 234" DITOLAK. Definisi Q3(a) tidak rusak —
yang rusak adalah grain pelaksanaannya. Tidak ada yang perlu diubah dari
rumus `m1_bars<15` ∧ bukan bucket tepi.
- Varian auditor "broker-day+exclude-edge=0" DIABAIKAN sebagai artefak
konstruksi varian: ia berkontradiksi langsung dengan pengukuran B1
(597 bucket mid-day pada grain broker) — varian yang menghasilkan NOL
padahal 597 bucket terukur ada, adalah varian yang salah rakit, bukan
refutasi terhadap 234.
- Koreksi terhadap klaim audit `":312 cocok persis dengan definisi"`:
cocok RUMUS, salah GRAIN. Kebenaran klausa ini dibatasi sampai di situ.
- Akar selisih yang sebenarnya: **234 lahir dari edge-rule BATAS SESI
(B1), sedangkan Q3(a) memerintahkan edge-rule BATAS HARI.** Denominator
berbeda sejak awal — maka aturan "tepat 234, selisih = gagal" (`fix:86-87`)
saya CABUT karena memadukan angka-rule-B1 dengan definisi-rule-Q3(a).

**Putusan (c) — syarat verifikasi dirumuskan ulang:**

1. Definisi Q3(a) DIPERTAHANKAN kata-per-kata (edge-rule BATAS HARI
otoritatif; edge-rule BATAS SESI milik B1 tidak berlaku untuk flag ini).
2. Grain DIPERTEGAS ke broker-day tunggal (butir C di bawah) SEBELUM
hitungan apa pun dibandingkan.
3. Target-uji = HITUNG-ULANG INDEPENDEN pada grain broker-day tunggal
dengan edge-rule Q3(a). Angka hasil recount ini — bukan 234, bukan 479 —
yang dikunci sebagai target final.
4. Rekonsiliasi WAJIB: selisih recount vs 234 (referensi B1) dan vs daftar
597 bucket B1 dijelaskan bucket-per-bucket (kontribusi edge-rule SESI→HARI
+ kontribusi grain UTC→broker). Tanpa rekonsiliasi = gagal.
5. Hasil 479 DITOLAK sebagai artefak grain-campur; dilarang dipakai sebagai
target, pembanding, maupun pembenar.
6. Angka 234 TETAP sebagai referensi orde + jangkar B1 (dan nuansa F-2
tetap berlaku: 234 hari ber-flag, 223 di antaranya ber-counterfactual —
`audit/reaudit-F2-F3-F4.md` F-2). Status BELUM DIUJI (`protokol:170-174`)
dipertahankan sampai uji sensitivitas klasifikasi H1 pada hari-hari itu ada;
eksklusi buta TETAP DILARANG.

---

## B. Lubang 1 / blocking 2 — guard paritas: BENTUK FINAL

**Fakta yang mengikat (`reaudit-kedua-fix-D1-D5.md` §4, `:253-291`):**

- Tiga klausa `build_labels.py:126-174` — `:153` hanya menangkap atr
NEGATIF; `:161` hanya menangkap `|norm| ≥ 1000`; `:169-172` membandingkan
`d/a` dengan `d/a` karena `:220` mendefinisikan `norm = d/a`
("Tautologi murni untuk setiap `a > 0`" — `:268`).
- Sabotase (`:272-283`): `1.0`, `2.0`, **`88.79`**, `100.0`, `12345.6`,
`1e6`, close-avg = NO RAISE. "Justru inilah yang seharusnya ditolak"
(`:287` — `88.79` median lock tak-berdimensi lolos).
- Klaim docstring `:138-141` ("harus MELEDAK…") FALSE (`:289`); klaim D5
`:147`/`:197` ("diuji via bukti mutasi", "Benar") salah dan dikontradiksi
pengakuan coder `:237`/`:270` (`:179`).

**Putusan — bentuk guard yang mengikat (rasional: NILAI tak bisa bersaksi
tentang SATUANNYA; yang bisa diuji adalah PROVENANS pembagi):**

1. Klausus `:169-172` (loop `r` vs `d/a`) DIHAPUS. Pernyataan yang
membandingkan nilai dengan dirinya sendiri BUKAN guard — dilarang kembali
dalam bentuk apa pun, termasuk yang dibungkus komentar/docstring.
2. Klausus `:153` (non-negatif) dan `:161` (`|norm|<1e3`) BOLEH tinggal
SEBAGAI smoke-bounds dengan label jujur di kode ("batas kewajaran, BUKAN
bukti satuan"). Dilarang mengklaim keduanya — sendiri maupun bersama —
sebagai paritas satuan.
3. Guard PENGGANTI (wajib): pemeriksaan provenans — assert pembagi yang
dipakai SAMA DENGAN kolom `atr_14_d1` store yang di-reindex ke grain label
(`allclose` dengan toleransi eksplisit tertulis di kode). Deret referensi
ATR store dilewatkan eksplisit ke fungsi guard. Rasional mengikat: harga
vs konstanta tak-berdimensi tidak dapat dibedakan dari nilainya; yang
dapat dibedakan adalah IDENTITAS terhadap kolom harga store.
4. Konsekuensi yang wajib terpenuhi (kriteria terima, bukan saran):
sabotase `atr → 1.0` konstanta HARUS meledak; sabotase `atr → 88.79`
konstanta HARUS meledak; sabotase `atr → close-avg` HARUS meledak
(harga dengan kuantitas salah ≠ kolom ATR store); baseline (ATR store
asli) lolos. Minimal DUA test sabotase (1.0 dan 88.79) terkunci di suite.
5. Docstring `:138-141` wajib ditulis ulang sesuai perilaku TERBUKTI
(janji MELEDAK hanya untuk kasus yang benar-benar meledak). Klaim D5
`:147`/`:197` DICABUT sampai guard + test butir 3–4 ada dan hijau.
6. Syarat blocking 2 ("assert NYATA") dinyatakan TERTUTUP jika dan hanya
jika butir 1–5 terpenuhi dan terbukti via eksekusi sabotase independen.
Sampai itu: Lubang 1 = TERBUKA (menguatkan `:291`).

---

## C. #21/#22 — grain: YA, TUNGGAL BROKER-DAY

**Fakta yang mengikat (`:310-311`, `:31`):** 200 bar hantu dari
`utc.dt.normalize()` (`build_labels.py:200`, juga `:103`, `:245`);
`day_label=None` 200; `quarantine_mask=None` dtype object; reindex ATR
buta-grain (`:219`) dengan NaN 214 (200 grain + 14 warmup); 12 hari hantu
membawa `gap_f2_flag=1`.

**Putusan:**

1. Seluruh rantai label WAJIB satu grain: **broker-day kanonik =
`date_broker` dari `daily_metrics`/store** (F-1/B1). Setiap
variabel/kolom bernama `broker_day`/`date_broker` di `build_labels.py`
wajib berisi broker-day sungguhan — REUSE pemetaan store; DILARANG
merekonstruksi hari dari `utc.normalize()`.
2. `_daily_from_m15` (`:85`, kode mati per #29 `:318`) WAJIB dihapus —
ia adalah sumber grain kedua (UTC-normalize) yang menyesatkan docstring
`:193`. Penghapusan ini sekaligus menutup #29; pagu 400/50 tetap berlaku.
3. Kriteria terima (mengikat): D4 = **974 baris broker-day**; `day_label`
tanpa None; `quarantine_mask` bool murni (tanpa None/object);
`london_drift_norm` NaN HANYA warmup ATR (±14, terdokumentasi) — bukan 214.
4. Fides jendela London DIPERTAHANKAN: yang diperbaiki hanya KUNCI
grouping hari, bukan definisi sesi (`is_london` local-hour 8–16 + 16 bar
pertama, sudah 100% terbukti `:44-53`).
5. BATAS ADJUDIKASI: mekanisme row-key D4 (#20, `index=False`) TIDAK
diputus di sini — butir C hanya mengunci grain + kriteria hitung butir 3.
#20, #24/Lubang 2, #25–#36 bukan bagian putusan ini dan tetap terbuka
untuk ronde berikutnya.

---

## Yang TIDAK diputus (batas mandat)

Tidak ada vonis H4/H5. Tidak ada perubahan lock/ambang/EDA/fondasi B1.
Tidak ada koreksi target 234 menjadi angka lain. Tidak ada putusan atas
Lubang 2 (prasyarat prosedur Lapisan 3-H3 — reaudit-kedua `:295-301`,
dibenarkan), #20, #24–#36. Butir A menggantikan aturan `fix:86-87`;
seluruh sisa Q1–Q4 tetap berlaku.

---

## Self-audit 1×

1. Tiap butir menunjuk baris sumber audit: A → `:310-312`, `:336`,
`audit-fondasi-B1.md:122`, `fix:83-89`; B → `:253-291` (`:268`, `:287`,
`:289`), `:179`; C → `:310-311`, `:31`, `:44-53`. Tidak ada putusan
tanpa kutip sumber.
2. Tidak menulis/mengubah kode produksi; tidak menyentuh H4/H5/H6+/EDA/lock;
tidak melebarkan ke `hipotesis_lock_v1.md` (meta-check ala reaudit-kedua
`:363` dipatuhi).
3. File ini satu-satunya artefak yang ditulis, di `arsitek/`; tanpa
commit/stage (menunggu verifikasi hash di bawah).
