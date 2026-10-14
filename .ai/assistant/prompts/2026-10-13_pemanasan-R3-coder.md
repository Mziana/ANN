# Brief Pemanasan R3 (flip + resize) — Coder Eksternal (2026-10-13)

## Status: PEMANASAN DIAGNOSTIK — BUKAN RONDE VONIS

Run ini **tidak menghasilkan vonis apa pun** (bukan TOLAK/KANDIDAT/BELUM
JELAS). Aturan tafsirnya asimetris, ditetapkan arsitek + user:
- Hasil KALAH = ide paket gugur kuat (bahkan dengan setting dipilih
  sesudah melihat data pun gagal) → hemat bed 2025.
- Hasil MENANG = tanpa makna (artefak seleksi sirkuler) → tidak membuka
  segel apa pun, tidak mengubah status ronde mana pun, tetap wajib uji
  bed baru untuk arti apa pun.
Dua kalimat di atas ditempel di laporan pulang. Coder dilarang
menyimpulkan lebih dari itu.

## Otoritas teknis

Satu-satunya resep teknis = spec
`reports/governance/2026-10-13/arsitek/spesifikasi-discovery-R2.md`
(status SPEC EKSEKUSI + Amandemen-R2-1) + brief eksekusi R2
(`.ai/assistant/prompts/2026-10-13_eksekusi-discovery-R2-coder.md`).
Semua prosedur (ledger pra-run, manifest hash, kontrak eksekusi, biaya
3 lapis, Q0–Q5, paruh, seed, determinisme 2 run) DIIKUTI PERSIS R2,
KECUALI dua perubahan di bawah. Bila bertentangan dengan spec R2, spec
R2 menang — laporkan konflik, jangan improvisasi.

## Tugas: SATU — ulangi R2 di bed 2026 yang sama, dengan DUA perubahan

1. Tulis LEDGER pra-run + manifest hash (SHA-256) di folder evidence
   BARU `reports/research/2026-10-13/discovery-R3-pemanasan/evidence/`
   SEBELUM run pertama. Isi ledger = salinan R2 (paruh-1
   2026-01-01..05-18 / paruh-2 2026-05-19..10-02, seed `1337`, config
   spread literal, anomali 2026-03-10..03-27 KELUAR dari denominator)
   + dua perubahan di bawah dinyatakan eksplisit + label PEMANASAN
   NON-VONIS. Tanpa ini = run gagal.
2. Petakan event E1 (6 sel) + E2 (1 sel) + E3 (1 sel, definisi R1 D-1
   verbatim — TITIK-KOMA pun sama) di 2026, lalu **NEGASIKAN side**
   (`side → -side`, satu operasi sesudah scan, tanpa ubah logika
   scan E1/E2/E3 apa pun).
3. Barrier ATR diresize (D2-2, SATU paket, tanpa ladder): ATR = ATR
   M5(14) pip dari bar M5 terakhir selesai ≤ t0, DIBEKUKAN saat entri;
   **SL = 1,0×ATR, TP = 1,5×ATR** (RR 1,5:1). Entry DIBUANG bila ATR
   tak tersedia / jendela menyeberangi gap / anomali / sesi Off — nol
   imputasi, jumlah buang dilaporkan.
4. Kontrak eksekusi = R2 persis (D2-5): entry OPEN bar t0+1; horizon
   dari t0 close; BUY ASK→BID / SELL BID→ASK (mengikuti side HASIL
   NEGASI — pagar SL/TP otomatis tercermin); spread nol dan mid
   dilarang; first-passage pada bar SESUDAH bar entry; bar-kembar
   SL+TP = AMBIGUOUS_SEQUENCE buang + hitung eksplisit.
5. Biaya 3 lapis per event = R2 persis (D2-4). `spread.default`,
   `by_year`, `stress_multiplier` DILARANG. Fallback default +
   laporkan bila sesi tak terpetakan.
6. Hitung Q0 (gerbang 300, dilaporkan), Q1 (evaluasi HANYA H+10),
   Q2 (satu paket, tanpa ladder), Q4 failure map (wajib), Q5
   paruh-2026. Tanpa RV/TAU; tanpa M15 di evaluasi. **Tanpa lampiran
   D-8, tanpa segel** (pemanasan tidak menyegel apa pun).
7. Kriteria 4-syarat D2-6 DIHITUNG sebagai angka diagnostik per sel
   (median pooled, CI bootstrap cluster-hari 10.000 resample seed
   1337, tanda paruh, failure map) — TANPA vonis per keluarga.
   Coder MELAPORKAN angka + kalimat tafsir sesuai Status di atas.

## Keluaran

Ledger + manifest hash + script/harness + JSON event-level (kolom
minimum D-3.4 warisan) + stdout, semua di folder evidence pemanasan
di atas. Determinisme: 2 run identik (disiplin R2).

## Larangan (pelanggaran = run gagal)

Folder `discovery-R2/evidence/` + segel R2 (`2575473c…b7331a`) + segel
R1 (`5bc324aa…67df963`) TIDAK DISENTUH (baca pun jangan); tanpa
2023/2024/2025 untuk evaluasi; tanpa ubah apa pun selain dua
perubahan di atas (tidak ada "sekalian coba varian"); tanpa
indikator; tanpa uji p-value untuk seleksi; tanpa `except: pass`;
tanpa `print()` produksi (pakai logging); fungsi < 50 baris, file <
400 baris.

## Format pulang

Laporan §5 AGENTS.md (file dibuat/diubah, tabel Klaim & Bukti, yang
belum diverifikasi, potensi masalah, saran). Ekspektasi jujur dari
meja hitung: impas butuh ~49% menang vs langit-langit sentuh ~17% —
kemungkinan besar KALAH; laporkan angkanya apa adanya, jangan
"perbaiki" dengan mengubah apa pun.
