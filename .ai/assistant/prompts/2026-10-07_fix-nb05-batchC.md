FIX BATCH C UNTUK CODER — F-B804 + F-B802 + F-B901 (B8-01, B10-01, B8-03 SENGAJA DIKECUALIKAN)

Konteks: Batch C (Langkah 7-10) verdict LULUS DENGAN CATATAN — 2 MEDIUM, 4 LOW, tanpa HIGH. Tidak ada hitungan yang salah dan tidak ada kesimpulan yang terbalik. Yang diperbaiki di sini hanya ketidakkonsistenan artefak + 1 guard regresi yang hilang. Peranmu: CODER (baca `.ai/assistant/prompts/PERAN-coder.md` dulu). Kamu BUKAN auditor (DILARANG audit sendiri), BUKAN arsitek, BUKAN asisten (ABAIKAN `.ai/ASSISTANT_RULES.md`).

=== HASH TITIK-AWAL (verifikasi dulu, TIDAK cocok → STOP) ===
- `scripts/_build_eda05.py`: `ba11f079282367b0885732dbf41116cfdf8f2434` (51783 byte / 1132 baris)
- `notebooks/scalping/eda_05_regimes.ipynb`: `2d8f600acade43cd97b67d7d376f0eaa693d19bb` (81193 byte, LF)
- `reports/eda/2026-10-06/report.md`: `918f2afa48c5873c08ac6aeccd696bcbb238e84c` (12265 byte / 157 baris, sudah memuat Q-TR-01/02/03)
- `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md`: `f012df4f7ec60650e95ae3be7f737a1bdcf5c4fd` (8287 byte)
- `reports/eda/progress/06-regimes/laporan_tahap_12_sintesis.md`: `2dfd7bb7dae8feac069d5d926a907741833aaa43` (8872 byte)
- Audit (hanya dibaca, DILARANG diedit): `reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md` (`f7a5a9f8b894575b37b68eeab370725e8d631081`, 2964 baris / 183892 byte)
- Workdir: `D:\ANN`. Interpreter: `venv/Scripts/python.exe`.

=== F-B804 (MEDIUM, WAJIB) — Endpoint placebo_hl basi di hulu ===
Sumber: audit B8-04 (`:2565-2616`, ringkasan `:2810`). Fakta yang sudah diverifikasi asisten ke disk: `report.md:73` sudah `0,4890–0,4922` ✅, tetapi `_build_eda05.py:909-911`, `ipynb:1312` (output), `ipynb:1340` (source), `tahap_12:98` masih `0,4890-0,5050` ❌. Nilai `0,5050` memang sah sebagai batas atas `placebo_acak` (ada di nb04 sel 19) — yang keliru hanya labelnya.
1. Edit `_build_eda05.py:910`: `placebo_hl 0,4890-0,5050` → `placebo_hl 0,4890-0,4922`, dengan anotasi koreksi memuat 2 fakta: `0,5050 milik placebo_acak`; `0,4890 = titik estimasi hl_utc, bukan batas bawah CI [0,4748/0,4798]`. Sebut `KOREKSI Q-TR-03/B8-04`.
2. Regenerate notebook dari builder (DILARANG edit `.ipynb` manual — akan hilang saat regenerasi). Pastikan output teregenerasi memuat string baru.
3. Sinkron `tahap_12:98`: `placebo_hl 0,4890–0,5050` → `0,4890–0,4922` + label `KOREKSI B8-04`, cermin `report.md:73`.
4. Verifikasi: tidak ada lagi `0,4890-0,5050` berlabel `placebo_hl` di builder/notebook (source+output)/tahap_12; `0,5050` yang tersisa hanya berlabel `placebo_acak`. Kesimpulan Q6 tetap negatif (tumpang tindih tetap ada di kedua versi) — JANGAN ubah kesimpulan.

=== F-B802 (LOW, WAJIB) — Rujukan sel tahap_14 tanpa patokan blob ===
Sumber: audit B8-02 (ringkasan `:2813`). Fakta terverifikasi: `laporan_tahap_14_figures.md:11-12` menulis `sel #21`/`sel #22` tanpa menyebut hash notebook; `tahap_12:5` mencatat blob berubah (`8158d5b57b20e` → `2d8f600acade`, sel #13–#17 → #13–#18); figures & registry kini di json idx 22/23.
1. Tambahkan cite blob notebook aktif ke `tahap_14` (hash penuh + tanggal).
2. Betulkan rujukan `sel #21`/`#22` ke nomor yang benar terhadap blob tersebut.
3. Jawab eksplisit di `tahap_14` pertanyaan auditor Q1: konvensi penomoran yang dipakai (0-indexed sel-kode / 1-indexed sel-kode / json idx) — tulis konvensinya agar rujukan berikutnya tertelusur tanpa tebakan.

=== F-B901 (LOW, WAJIB) — Assertion regresi hour_utc + ripple count ===
Sumber: audit B9-01 (ringkasan `:2814`). Fakta terverifikasi: `tahap_11:60` mencatat fix KeyError `hour_utc`; `_build_eda05.py:807` memang `hourly["hour_utc"] = ...` dipakai di 808/810/813; grep tidak menemukan satu pun `assert` yang mengunci kolom itu (4 bug lain punya guard).
1. Tambahkan TEPAT SATU assertion regresi yang gagal bila kolom `hour_utc` hilang/rusak (lokasi logis: sesudah `:807`).
2. Ripple count WAJIB ikut (pelajaran B7-01): total assertion builder 67 → 68. Perbarui SEMUA penyebut count: `report.md:15` (`67` → `68` + label `KOREKSI B9-01`), `tahap_11` (baris count + rincian item), dan komentar count di builder bila ada. JANGAN ulangi B7-01 (klaim 68 isi 67 atau sebaliknya) — hitung via AST, bukan regex.
3. Rerun penuh: 68/68 PASS, 0 error, `execution_count` 1..19 berurutan. Semua angka selain string Q6 dan count WAJIB identik (deterministik).

=== SENGAJA DIKECUALIKAN (jangan kerjakan, jangan "tingkatkan") ===
- B8-01 (mtime 15:49:27): bukti netral oleh bulk EOL sync `10:42:00` — tak dapat diperbaiki; jalur hash sudah membuktikan substansi. DILARANG "memulihkan" mtime (menyentuh file = pelanggaran append-only).
- B10-01 (docstring `md()`/`code()`): prevalen di `_build_eda02/03/04` (terverifikasi grep) — gaya proyek, bukan regresi. DILARANG refactor docstring massal.
- B8-03 (tabel identitas `:1819-1825`): isi dokumen AUDIT milik auditor — coder DILARANG menyentuh file audit. Pembaruan tabel + konvensi `git hash-object` menjadi tugas append auditor berikutnya; coder hanya menyerahkan hash baru yang akurat.
- Ekstrak `fractal_mask`/`variance_ratio` ke `_eda_common.py` (pertanyaan auditor Q3): refactor, DITUNDA ke batch terpisah. Duplikasi sadar sudah di-disclose (`:466-469`/`:602-604`).

=== ATURAN FIX (mengikat) ===
1. Builder→notebook: edit builder, rerun, notebook ter-regenerate. DILARANG edit `.ipynb` manual. DILARANG buka/edit nb01–nb04. DILARANG sentuh file audit. DILARANG commit/push.
2. Diff kecil per file (syarat §15.1): hanya baris yang diminta di atas. EOL konsisten LF; integritas diuji via `git hash-object`, BUKAN ukuran byte.
3. Gate tiap rerun: `ruff check` + `ruff format --check` bersih; `scripts/check_foreign_chars.py` OK pada semua file tersentuh; `nbconvert` exit 0.
4. Laporan format AGENTS §5: file diubah + tabel Klaim & Bukti (file:baris + output) + hash baru 5 blob + STOP. Sebutkan jawaban Q1 (konvensi sel) dan konfirmasi kesimpulan Q6 tetap negatif.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap angka/string bersumber file:baris/output; count 68 via AST; tidak ada `placebo_hl 0,4890-0,5050` tersisa; tidak ada file di luar scope tersentuh.
Putaran 2 — Bias: apakah kamu mengubah kesimpulan Q6, menilai metode, atau refactor di luar perintah? Apakah label koreksi jujur (titik estimasi vs CI)?
Putaran 3 — Meta: notebook hasil regenerate (bukan edit manual)? File audit tak tersentuh? Hash dihitung SETELAH semua tulis final? B8-01/B10-01/B8-03/ekstrak-common benar-benar tak dikerjakan?

STOP. Re-audit/verifikasi HANYA atas perintah terpisah.
