FIX NEWLINE LANJUTAN (PUTUSAN ARSITEK Q1–Q4) UNTUK CODER — PASCA-PROSES EOL ×5 BUILDER + REGEN nb05 SAJA + SINKRON DOKUMEN

Konteks: Putusan arsitek `2026-10-07_tanya-arsitek-determinisme-full.md` (Q1–Q4, mengikat): Q1 — "byte-identik" TURUN menjadi "deterministik ternormalisasi" (normalisasi tepat 3 kategori: EOL, cell.id, stempel waktu run; DILARANG normalisasi source/outputs/urutan/jumlah sel/asserts/FIG/angka); Q2 — normalisasi EOL tinggal (a) PASCA-PROSES DI BUILDER sesudah `nbconvert --inplace` (DILARANG script terpisah, DILARANG patch nbconvert); Q3 — checklist audit 8 item; Q4 — regen nb05 SAJA, nb00–nb04 DILARANG disentuh. F-NL (`newline="\n"` ×5) sudah mendarat dan terverifikasi. Peranmu: CODER (baca `.ai/assistant/prompts/PERAN-coder.md` dulu). Kamu BUKAN auditor, BUKAN arsitek, BUKAN asisten (ABAIKAN `.ai/ASSISTANT_RULES.md`).

=== HASH TITIK-AWAL (verifikasi dulu, TIDAK cocok → STOP) ===
Builder (pasca F-NL, akan +1 langkah pasca-proses):
- `_build_eda01.py` → `c3a3880926ba4953dedc4dca96144149f688c02f`
- `_build_eda02.py` → `f9bf6c3f65eb0c1200991d93e72e93dad1c3defd`
- `_build_eda03.py` → `bca5b896b533c0d6d108f162f6f2256d5477c96d`
- `_build_eda04.py` → `c07cab160b3b53561b54dcde051403d510b96ce3`
- `_build_eda05.py` → `3b07e3a8a7de3d46fb433983a1f85e1c978e7aec`
Notebook: nb01 `ec448a59…` · nb02 `8ff4358d…` · nb03 `0158ca99…` · nb04 `4ac4566f…` (KEEMPATNYA DILARANG DIEKSEKUSI/DISENTUH) · nb05 `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` (CRLF 1.663/1.663 — baseline pembanding regen, akan dipensiunkan).
Dokumen (hanya merujuk nb05 boleh berubah): `report.md` `afeb1b1c…` · `tahap_11` `97cf27e1…` · `tahap_12` `094d90d2…` · `tahap_14` `bf20587d…`.
Audit (hanya dibaca, DILARANG diedit): `eda_nb05_audit_v1.md` (`4eafbdb2eb6e1e8a952db01cb0c5dcd425fd328e`, 238.097 byte / 3.851 baris).
Workdir: `D:\ANN`. Interpreter: `venv/Scripts/python.exe`.

=== F-NL2 (WAJIB) — Langkah pasca-proses di 5 builder ===
1. Tambahkan langkah normalisasi EOL DI DALAM tiap builder, berjalan sesudah `nbconvert --inplace` dalam satu eksekusi: baca byte notebook → CRLF→LF → tulis kembali dengan `newline="\n"`. Seragam ×5, idempoten (run ulang pada file LF = no-op byte). DILARANG script terpisah; DILARANG edit `.ipynb` manual; DILARANG sentuh/mengonfigurasi/patch nbconvert dalam bentuk apa pun; DILARANG ubah selain langkah ini.
2. 4 builder non-nb05 (eda01–04) TIDAK DIEKSEKUSI — perubahannya diverifikasi hanya sebagai diff langkah + gate statis (ruff check + format). Catat hash final keempatnya tanpa regen.

=== REGEN nb05 SAJA (WAJIB) — Dengan kriteria Q3 arsitek ===
1. Eksekusi `python scripts/_build_eda05.py` + nbconvert exit=0. Snapshot nb05 pra-rerun ke luar repo. DILARANG menjalankan builder 01–04. DILARANG menulis dokumen/audit selama regen.
2. Buktikan lulus 8 checklist Q3 (lampirkan bukti tiap item, bukan klaim): (1) EOL byte-count = 0 CR + catat ukuran; (2) diff ternormalisasi KOSONG vs baseline `2cb57ad9…` (normalisasi TEPAT 3 kategori Q1.1 — tiap baris diff non-kosong didaftar + didisposisikan satu per satu; normalisasi menyentuh source/outputs = GAGAL); (3) invarian struktural (jumlah + urutan sel sama, top-to-bottom 0 error; chunking flush = observasi); (4) assertion **68/68** (baseline pin terakhir `report.md:15` — BUKAN 67; contoh "67/67" di putusan arsitek adalah angka riwayat, pin mengikat = 68 hasil AST); (5) FIG-04..07 hash identik pin (`3420bca3…/fedd896f…/124867c6…/a90a16b0e40d`); (6) spot-check pin angka otoritatif nb05 tak berubah (temuan analitik baru dari regen = anomali proses → STOP); (7) catat blob builder + versi nbconvert + log regen + baseline `2cb57ad9…`; (8) Regen GAGAL bila menyentuh objek di luar nb05 + FIG-04..07.
3. Bila item mana pun gagal → STOP + lapor + restore nb05 ke `2cb57ad9…` (seperti preseden restore nb01 `ec448a59…`).

=== SINKRON DOKUMEN (WAJIB, minimal, setelah regen lulus) ===
Masing-masing + label `KOREKSI NL2` + tanggal 2026-10-07:
1. Pin blob nb05 BARU (LF ternormalisasi) di: `report.md:15`, `tahap_11` header + catatan koreksi, `tahap_12:5`, `tahap_14:7-10`. Pin CRLF lama `2cb57ad9…` DIPENSIUNKAN dengan catatan provenance (diganti pin baru), BUKAN dihapus dari riwayat (Q4.2).
2. `tahap_14` catatan B9-02: status → EOL nb05 kini **LF deterministik dari builder** (pasca-proses Q2, diverifikasi 0 CR); akar masalah DITUTUP.
3. Koreksi bahasa "byte-identik" untuk regen notebook di dokumen bila ada (Q1.4) → merujuk putusan arsitek; byte-identik tetap berlaku hanya untuk artefak byte-stabil (FIG/fragmen).
4. DILARANG menyentuh kesimpulan, angka, count, verdict, pin nb01–nb04, frasa riwayat.

=== ATURAN (mengikat) ===
1. DILARANG eksekusi/menyentuh nb00–nb04, file audit, `.ai/*`, `requirements.txt`, `reports/go/`. DILARANG commit/push.
2. Diff minimal (§15.1): 1 langkah ×5 builder + baris dokumen yang diminta. EOL `.md` jangan diubah massal.
3. Gate: `ruff check` + `ruff format --check` bersih; `check_foreign_chars.py` OK (ulang setelah tulis final); `pytest -q` hijau; nbconvert exit=0 ×1 (nb05). `validate_data` bila terdampak, jujur laporkan bila tidak.
4. Laporan format AGENTS §5: file diubah + tabel Klaim & Bukti per 8 checklist Q3 + hash baru SEMUA file berubah (setelah tulis final) + STOP.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap builder tepat 1 langkah baru; checklist Q3 8/8 berbukti; tidak ada pin/EOL basi; count 68 via AST.
Putaran 2 — Bias: apakah kamu menambah normalisasi kategori ke-4, menilai metode, atau mengubah kesimpulan? Apakah pin lama dipensiunkan (bukan dihapus)?
Putaran 3 — Meta: hanya nb05 + FIG-04..07 yang tereksekusi? Audit tak tersentuh? Hash setelah tulis final? nb00–nb04 tak dikerjakan?

STOP. Re-audit/verifikasi HANYA atas perintah terpisah.
