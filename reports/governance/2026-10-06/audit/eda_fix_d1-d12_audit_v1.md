# Audit Kode Adversarial — Fix D1–D12 EDA (Langkah 1–5) — v1

**Tanggal:** 2026-10-06 · **Auditor:** Klenz · **Auditee:** coder (Freebuff)
**Objek:** `scripts/_build_eda01–04.py` + `notebooks/scalping/eda_01–04` (output cell = bukti eksekusi) + `figures/`
**Sumber kebenaran:** `eda_design_v3.1.md` (kanonik) + `eda_review_deviations_v1.md` (verdict Architect — tidak dire-litigasi). Laporan coder hanya peta.
**Baseline:** HEAD `e4efbfd`, semua perubahan uncommitted.

## Verdict
**LULUS** (kode) — dengan 1 MEDIUM dokumen yang **WAJIB** ditutup sebelum langkah 6 (dua commit), dan 3 LOW.

## Tabel D1–D12

| # | Status | Bukti (file:baris) | Catatan |
|---|---|---|---|
| D1 | OK | `_build_eda03.py:247` `LAGS=range(1,61)`; assert :710–711 | Klaim lama "\|ACF\|≤0,012" dibantah terbuka :781–784 (maks 0,0226 B M15 lag 50) — informasi baru yang diramalkan verdict |
| D2 | OK | LB manual `chi2.sf` :321–350; ATURAN BACA :302–313, dicetak :364; Q/n :756–758 | p tidak menyimpulkan; slice sesi/tahun terisi (:719–720) |
| D3 | OK | VR loop :455; `VR_HORIZONS=(5,15,60)` :448; vr2 :517; dua jendela 2–20 vs 2–60 :468–471 | Efek ekstensi dilaporkan terpisah |
| D4 | OK | `SIGN_ACF` :377–394; sign per sesi :507; arah ganda :529–533 | sign≠besaran didokumentasi (:785–788) |
| D5 | OK | `STRATA={A,B}` :218; semua loop `STRATA.items()` (:275,:354,:379,:451,:487); B asserted :224; `DELTA_AB` :736–737 | Catatan daya B M15 n=12.395 (:790–791) |
| D6 | OK | `SWING_FREQ` per hari :404–431 + sebaran :433–435; `HARI_BERBAR=825` dari `broker_day` | Jumlah swing identik pra-fix — tidak ada perubahan definisi |
| D7 | OK | `np.diff(flatnonzero(mask))` median/p90 :407–424; per sesi :441–452; "bukan durasi posisi/P&L" :454 | Sesuai verdict persis |
| D8 | OK | File `eda_04_swings_levels.ipynb`; `git ls-tree HEAD` tidak pernah memuat nama lama; STATE:52 mencatat rename | Gratis (belum commit) ✓ |
| D9 | OK | `_build_eda01.py:512,613` skema + assert daftar file; `git status` 3× `R` → FIG-01/02/03; figures/ hanya 3 file | nb02/03/04 tidak menampilkan plot (grep `plt.`=0) → tidak ada yang wajib disimpan; FIG-04+ bebas utk nb05 |
| D10 | OK | `_build_eda02.py:506–565` M5 `spread_pips_max` mask+label identik M1; assert :840 | "Agregasi M5 tidak menemukan ekor baru" dilaporkan berdampingan tail M1 |
| D11 | OK — nol perubahan kode | Parameter dibaca dari nb00 via **AST** + assert identik :130–192; seed 20261006 :158; MAX_K=24 :162/:705; touch `low<=L<=high` identik :487/:509 vs :466/:553; retensi 0,557/0,468 di output | **Konfirmasi Klenz** (menutup `audit_kesesuaian:119`): touch-genuine SAH — aturan identik dua sisi; kontrol literal terbukti degeneratif (0,89–0,95) dan dilaporkan, bukan disembunyikan |
| D12 | OK (minimal) | nb02 flag fix 00:55+NYSE tz-aware :614–625 (self-check JST assert); `MARKER_HOUR_TABLE` :650–667. nb04 BoJ 150/155/160 :475–541; guard "tanpa kolom pasca-event" :1113 | Event-study penuh tidak ada ✓ |

## Integritas rerun
- Cocok-silang 11 angka ringkasan markdown ↔ output cell (nb03: acf1 A/B, VR, Q/n, sign; nb04: 728/518/151; nb01: kurt 195.x, max|r| 164,7) — semua cocok.
- Assertion riil: **31/31 (nb03), 30/30 (nb04), 30/30 (nb02), 23/23 (nb01)** = persis klaim laporan tahap 7/8/9.
- Mtime notebook ≥ builder per pasang (14:23→14:24, 14:40, 14:46→14:46, 15:49→15:49).
- Assertion terbukti mencegah bug nyata (bukan tautologi): VR formula selisih-vs-jumlah tertangkap `VR(1)=1` (:439–441); KeyError tuple pandas (:458–459); label NaN Off → "n/a" (:522–527).

## Gate (dijalankan auditor sendiri)
pytest **157 passed** · ruff check bersih · format 24 files · validate exit 0 (**2/2/1/1**) · check_foreign_chars 68 files OK · nbformat 4/4 valid, exec_count urut, 0 error cell · HEAD `e4efbfd` (tidak ada commit; amend dilarang ✓).

## Temuan
- **[MEDIUM-18]** Putaran dokumen pasca-fix belum dijalankan. (a) `STATE.md:41–44` masih "17/17" dan **"\|ACF\| ≤ 0,012 di semua TF"** — klaim yang **dibantah nb03 hasil fix sendiri** (0,0226); STATE masih "nb04 20/20" (aktual 30/30). (b) `audit_kesesuaian` §F masih "BELUM dijalankan" (mtime 13:20 < fix pertama 14:23). (c) **Tidak ada laporan mini langkah 2** (rework nb03) — melanggar rancangan §4 butir 8. (d) SESSION_LOG tanpa entri ronde fix. Dampak: propagasi klaim terbukti salah ke nb05/keputusan user. **Satu-satunya blocker sebelum dua commit langkah 6.**
- **[LOW-34]** Dead code `_build_eda02.py:691–694`: `mean_by_session_full["Off"]=None` tidak pernah dipakai (fragmen ditulis dari `mean_by_session`, :743); komentar mengklaim Off "dicatat eksplisit sebagai null" padahal output hanya menghilangkan key. Pilih satu: hapus, atau pakai `_full`.
- **[LOW-35]** Aturan R1/R2 (Lampiran A1: offset struktural −1; hanya divergensi melebihi geseran = temuan) tidak tercatat di nb04 — hanya R3 (:549–550). Output "agreement primer vs sekunder" (:681) bisa dibaca literal tanpa penjelas. A1-R4 mengikat "R1–R3 dicatat di nb04/nb05 dan laporan final" — pastikan tidak hilang.
- **[LOW-36]** Putusan D11 hidup hanya di dokumen governance; "PERTANYAAN TERBUKA untuk Klenz" (STATE:59–63) kini **DIJAWAB/DIKONFIRMASI** oleh audit ini — catat penutupnya saat MEDIUM-18.

## Tambahan-di-luar-desain
| # | Item | Klasifikasi |
|---|---|---|
| T-01 | Metrik "massa nol" (`_build_eda01.py:362` §3b) | **(b) butuh ratifikasi ringan** — tidak ada di daftar metrik Q1 rancangan; deskriptif, 0 risiko; ratifikasi via laporan EDA final |
| T-02 | Kolom `p_value_no_gap` per lag (nb03:239–240) | (a) dibingkai aturan baca |
| T-03 | Band BoJ 10/25/50 pip + tabel tahun/sesi (nb04:477–498) | (a) bentuk eksplisit "eksposur" D12 |
| T-04 | `swing_per_1000_bar` (nb04:414) | (a) normalisasi netral |
| T-05 | Assertion kunci-tanda-tahun SIGN_STABLE (nb03:733–734) | (a) drift-lock fakta terukur, data beku |

## Kepatuhan
0 look-ahead/leakage (semua `shift(1)`; window reaksi murni pasca-event); 0 imputasi harga (fillna nb02:284 = reindex agregat harian, terdokumentasi); 0 P&L/equity (satu-satunya hit = assertion negatif nb01:614); hardcode terkendali (konstanta prereg + fingerprint sesi asserted di nb02/03/04; nb01 tidak pakai sesi → tanpa fingerprint, sah); duplikasi definisi = trade-off disetujui (T2 verdict).

## Pertanyaan untuk coder
1. Kapan paket dokumen langkah 6 dijalankan? (satu-satunya blocker)
2. LOW-34: hapus atau pakai `mean_by_session_full`?
3. LOW-35: catatan R1/R2 masuk nb04 sekarang, atau didelegasi eksplisit ke nb05/report?

## Belum diverifikasi
- Kecocokan seluruh angka output (11 cocok-silang + 4 ringkasan assertion; sisanya diasumsikan hasil eksekusi yang sama).
- Isi piksel FIG-01/02/03 (scope: eksistensi + skema).
- Teori statistik di balik metrik (wilayah desain — tidak dire-litigasi).

## Self-audit auditor 3 putaran
- **P1 correctness:** semua temuan teruji file:baris; MEDIUM-18 berbasis teks live STATE vs kode fix; tidak ada temuan yang ternyata hanya markdown.
- **P2 bias:** 2 tuntutan ditarik — (i) "nb01 tanpa fingerprint" (nb01 tidak memakai sesi → sah); (ii) kecurigaan rerun menimpa header DITERAPKAN fragmen (builder meng-embed header identik :697–731 → byte-identical by construction). Klasifikasi (a)/(b)/(c) konsisten.
- **P3 meta:** LULUS proporsional — objek audit (Langkah 1–5) terverifikasi selesai di kode; MEDIUM-18 adalah prasyarat langkah 6 yang belum diklaim selesai.
