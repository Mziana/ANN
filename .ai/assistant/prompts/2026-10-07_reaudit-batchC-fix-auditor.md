RE-AUDIT SEMPIT FIX BATCH C UNTUK AUDITOR — VERIFIKASI F-B804 + F-B802 + F-B901 + TUTUP B8-03

Konteks: Batch C (Langkah 7-10) verdict LULUS DENGAN CATATAN — 2 MEDIUM, 4 LOW, tanpa HIGH. Coder mengeksekusi prompt fix `2026-10-07_fix-nb05-batchC.md` (F-B804 + F-B802 + F-B901; B8-01/B10-01/B8-03/ekstrak-common dikecualikan) dan melapor 6 file diubah + semua gate hijau + STOP tanpa commit. Tugasmu: RE-AUDIT SEMPIT atas hasil fix ini — verifikasi klaim coder dari artefak (bukan dari kata coder), tutup B8-03, beri verdict fix. Peranmu: AUDITOR (baca `.ai/assistant/prompts/PERAN-auditor.md` dulu). Kamu BUKAN coder (DILARANG menulis/mengubah kode — SATU-SATUNYA tulis yang diizinkan adalah APPEND ke file audit), BUKAN arsitek, BUKAN asisten (ABAIKAN `.ai/ASSISTANT_RULES.md`).

=== HASH TITIK-AWAL (verifikasi dulu, TIDAK cocok → STOP) ===
Hash di bawah = hash PASCA-FIX yang diklaim coder (asisten memverifikasi 7/7 cocok ke disk sebelum prompt ini dibuat):
- `scripts/_build_eda05.py`: `dd3d684a5a9513a379693b406ee329969d3bd541` (52.203 byte / 1140 baris)
- `notebooks/scalping/eda_05_regimes.ipynb`: `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` (83.611 byte, LF)
- `reports/eda/2026-10-06/report.md`: `afeb1b1cb0dbe7a3782215692853ff815cbced69` (12.335 byte)
- `reports/eda/progress/06-regimes/laporan_tahap_11_regime.md`: `118baf140130980378ef9eaae254c48f5acd3264` (8.621 byte)
- `reports/eda/progress/06-regimes/laporan_tahap_12_sintesis.md`: `094d90d20e2598372bf4b40c6fe5703ef4dba18e` (9.227 byte)
- `reports/eda/progress/06-regimes/laporan_tahap_14_figures.md`: `b4269a97361d3a7414cb6cc60c95852ef29dbc22` (4.184 byte)
- Audit pra-append (boleh dibaca, hanya di-append): `reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md` (`f7a5a9f8b894575b37b68eeab370725e8d631081`, 2964 baris / 183892 byte)
- Workdir: `D:\ANN`. Interpreter: `venv/Scripts/python.exe` (yang punya scipy).

=== LINGKUP RE-AUDIT (hanya ini — bukan audit ulang Batch A/B/C penuh) ===
Verifikasi INDEPENDEN tiap klaim coder berikut dari artefak (replikasi angka dari parquet/kode/notebook, bukan dari dokumen). Setiap butir: COCOK / TIDAK COCOK + bukti file:baris/output. Tanpa bukti = bukan temuan; ragu → BELUM DIVERIFIKASI + Pertanyaan untuk Coder.

R1. F-B804 hulu: `_build_eda05.py:916-920` memuat `placebo_hl 0,4890-0,4922` + label `KOREKSI Q-TR-03/B8-04` + 2 fakta (`0,5050 milik placebo_acak`; `0,4890 = titik estimasi hl_utc, bukan batas bawah CI [0,4748/0,4798]`). Output sel H5 notebook hasil regen memuat string baru. Grep independen: sisa `placebo_hl 0,4890-0,5050` di builder/notebook/tahap_12 = NOL (sisa yang sah hanya di file audit historis + ledger `thoughts/` di luar scope).
R2. Regenerasi via builder: notebook = hasil `python scripts/_build_eda05.py` + nbconvert (DILARANG rerun ulang oleh auditor — verifikasi dari artefak: struktur sel, `execution_count`, konsistensi builder↔notebook; JANGAN rerun builder/nbconvert karena akan menyentuh mtime).
R3. `tahap_12:100-102` sinkron (`0,4890–0,4922` + `KOREKSI B8-04`, cermin `report.md:73`); kesimpulan Q6 tetap negatif (`report.md:73` verdict tak berubah — JANGAN nilai metodenya, hanya pastikan kesimpulan tidak bergeser diam-diam).
R4. F-B802: `tahap_14:7-10` patok blob penuh + tanggal; `:16-17` rujuk json idx 22/23 disandingkan kode_sel #17/#18 + `execution_count` — cocokkan terhadap notebook aktual (parse JSON, bukan percaya dokumen); `:39-52` jawab Q1 (konvensi = json idx) + klaim blob lama tak terekonstruksi (`git cat-file -e 8158d5b57b20e` / `2d8f600acade`).
R5. F-B901: TEPAT SATU assert regresi `hour_utc` di `_build_eda05.py:808-813` (sesudah `:807`); uji logikanya benar-benar gagal bila kolom hilang/kosong/NaN/di luar 0–23 (baca predikatnya, jangan percaya labelnya).
R6. Count via AST independen (bukan regex, bukan percaya coder): total `ast.Assert` atas 19 sel kode = 68; 0 output error; `execution_count` 1..19 urut. Penyebut diperbarui di `report.md:15` (68 + `KOREKSI B9-01`), `tahap_11:4-5/:106-107` (68 + riwayat B7-01→B9-01); pastikan tidak ada penyebut 67 tersisa dan tidak ada komentar count basi di builder.
R7. Determinisme: FIG-01..07 hash (`709db8ae…/e55fc1f5…/73d65368…/3420bca3…/fedd896f…/124867c6…/a90a16b0…`) cocok klaim; diff per-sel vs pra-rerun — coder disclose beda sumber hanya json idx [16, 18] (assert baru + string Q6) dan beda output hanya sel Q6 + chunking stream sel idx 9 (teks gabungan identik). Verifikasi byte-level Independen atas disclose ini; bila ada beda angka di luar itu → temuan.
R8. Gate DIJALANKAN ULANG oleh auditor (asisten DILARANG run test, jadi angka gate coder belum terverifikasi independen): `ruff check` + `ruff format --check` + `scripts/check_foreign_chars.py` + `pytest -q` — laporkan rc/output asli. `validate_data` tidak dijalankan coder (alasan: src/data/config tak tersentuh) — nilai apakah alasan itu sah atau gate wajib tetap jalan.
R9. Eksklusi dihormati: B8-01/B10-01/ekstrak-common tak dikerjakan; nb01–nb04, `.ai/*`, rename, `requirements.txt`, `reports/go/` tak tersentuh.
R10. Tiga anomali terdeteksi asisten (disetujui user masuk lingkup 2026-10-07): (A1) `tahap_11:3` header masih tulis Builder blob lama `ba11f0792823…` padahal builder aktif `dd3d684a…` (Notebook blob di baris yang sama sudah baru) — putuskan: temuan LOW baru, atau catatan + perintah betulkan satu baris; (A2) konfirmasi byte-level independen atas disclose chunking stream sel idx 9 (teks gabungan diklaim identik) — putuskan: bukan temuan dengan bukti hitung ulang, atau temuan bila ada beda; (A3) coder menyentuh `tahap_14:28-34` (mtime FIG-04..07) di luar scope F-B802 ketat meski berlabel ripple-rerun — putuskan: diterima sebagai ripple wajar (preseden "ripple berlabel diizinkan"), dicatat, atau temuan LOW proses.

=== TUGAS APPEND (bagian dari lingkup — satu-satunya tulis yang diizinkan) ===
Tutup B8-03 sesuai rekomendasi audit sendiri (`:2865-2871`): tulis ulang tabel identitas `:1819-1825` sebagai RIWAYAT v0/v1/v2 (hash lama + hash pra-fix + hash pasca-fix fix ini) dan tetapkan konvensi byte: integritas via `git hash-object`, BUKAN ukuran file. Append ke file audit (JANGAN timpa isi lama); hash audit dihitung SETELAH tulis final. Beri verdict fix (LULUS / LULUS DENGAN CATATAN / GAGAL) + verdict batch C mutakhir.

=== ATURAN (mengikat) ===
1. Read-only kecuali append audit. DILARANG rerun builder/nbconvert/validate_data yang menulis artefak. DILARANG buka nb01–nb04 sebagai bukti (tetap di luar objek). DILARANG commit/push.
2. Setiap temuan WAJIB file:baris + angka/output. Bedakan tidak-sama ≠ tidak-sesuai-rancangan ≠ salah-hitung ≠ kesimpulan-salah.
3. False positive yang dibatalkan sendiri DICATAT terbuka.
4. Laporan: tabel Klaim & Bukti per R1–R10 + hash pasca-append + verdict + STOP.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap angka bersumber file:baris/output; AST dihitung sendiri; hash setelah tulis final.
Putaran 2 — Bias: apakah kamu menilai metode (arsitek) atau kejujuran klaim (auditor)? Apakah butir di luar R1–R9 ikut divonis tanpa bukti?
Putaran 3 — Meta: objek benar (6 blob pasca-fix)? Hanya file audit yang ditulis? Batch berikutnya tidak dimulai?

STOP. Commit / fix lanjutan HANYA atas perintah terpisah.

=== PERSETUJUAN USER (2026-10-07) ===
Item A (A1–A3) DISETUJUI masuk lingkup sebagai R10 di atas. Bukan lagi usulan — auditor WAJIB mengerjakannya.
