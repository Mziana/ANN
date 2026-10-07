FIX NEWLINE BUILDERS (HULU B9-02) UNTUK CODER — `newline="\n"` ×5 + REGEN nb01–nb05 + SINKRON DOKUMEN

Konteks: B9-02 menemukan akar laten — kelima builder menulis notebook via `NB_PATH.open("w", encoding="utf-8")` tanpa `newline=`, sehingga `\n` jadi `\r\n` di Windows. Fakta disk: nb05 = CRLF penuh (1.663/1.663), nb00–nb04 = pure LF (mereka lolos via checkout/commit `eol=lf`, bukan via builder). Batch ini mematikan akar masalah: deterministik LF dari builder, di semua OS. Peranmu: CODER (baca `.ai/assistant/prompts/PERAN-coder.md` dulu). Kamu BUKAN auditor (DILARANG audit sendiri), BUKAN arsitek, BUKAN asisten (ABAIKAN `.ai/ASSISTANT_RULES.md`).

=== HASH TITIK-AWAL (verifikasi dulu, TIDAK cocok → STOP) ===
Builder (5, akan diubah — tepat 1 baris per file):
- `_build_eda01.py:677` → `94b2c70bc83c9163b904408641652f6f2b16b545`
- `_build_eda02.py:928` → `df38e3c4df5276b5ed1ba1cb80dd5107fa4d280f`
- `_build_eda03.py:835` → `7536fd221fcab0912795de98f93e7e593775d76c`
- `_build_eda04.py:1202` → `6da029c0d343a41689a1fc71b2ac981f9909f21c`
- `_build_eda05.py:1109` → `dd3d684a5a9513a379693b406ee329969d3bd541`
Notebook (5, hasil regen — JANGAN diedit manual):
- `eda_01_returns.ipynb` → `ec448a593c1b835fabe1aca363c97004481894df` (LF)
- `eda_02_volatility.ipynb` → `8ff4358d4175457ad9a823aefc3c7e5048e13015` (LF)
- `eda_03_autocorr.ipynb` → `0158ca994db9b335db9bc0c2eddba0ee939d1af0` (LF)
- `eda_04_swings_levels.ipynb` → `4ac4566f5f6cc63f07960f04c583602889e51f4b` (LF)
- `eda_05_regimes.ipynb` → `2cb57ad9ec1aef90a4dac65af41c8bd9d2b3cec0` (CRLF — satu-satunya yang berubah EOL)
Dokumen (hanya yang merujuk blob/EOL nb05 boleh berubah):
- `report.md` → `afeb1b1cb0dbe7a3782215692853ff815cbced69`
- `tahap_11` → `97cf27e111964b830e3e6dcb6d40e85af142f11e`
- `tahap_12` → `094d90d20e2598372bf4b40c6fe5703ef4dba18e`
- `tahap_14` → `bf20587df9f7918f577202e434faf182316acfdd`
- Audit (hanya dibaca, DILARANG diedit): `eda_nb05_audit_v1.md` (`4eafbdb2eb6e1e8a952db01cb0c5dcd425fd328e`, 238.097 byte / 3.851 baris)
- Workdir: `D:\ANN`. Interpreter: `venv/Scripts/python.exe`.

=== F-NL (WAJIB) — Satu baris per builder ===
Di tiap dari 5 baris di atas: `NB_PATH.open("w", encoding="utf-8")` → `NB_PATH.open("w", encoding="utf-8", newline="\n")`. Asumsi (terbuka untuk tantangan auditor): `newline="\n"` mematikan translasi EOL saat tulis sehingga output deterministik LF di semua OS; ini parameter stdlib, bukan perilaku baru. DILARANG mengubah apa pun selain parameter ini di builder. nb00 tidak punya builder → di luar scope (DILARANG sentuh `eda_00_setup.ipynb`).

=== REGEN (WAJIB) — Via builder, berurutan nb01→nb05 ===
Rerun `python scripts/_build_eda0N.py` + nbconvert exit=0 per notebook. DILARANG edit `.ipynb` manual. Hasil yang DIHARAPKAN (bila menyimpang → STOP + lapor, jangan paksa sinkron):
- nb01–nb04: **byte-identik** dengan titik-awal (sudah LF; regen LF deterministik tidak mengubah byte) — count tetap 23/30/31/30, 0 error, exec urut.
- nb05: **menyusut ±1.663 B, pure LF, CRLF=0** — angka/output selain EOL identik; count tetap 68/68, 0 error, exec 1..19 urut.
- FIG-01..07: hash IDENTIK semua (regen tidak menggambar ulang isi).
- Salin tiap notebook pra-rerun ke luar repo untuk diff determinisme (sumber + output gabungan per-sel, seperti protokol Batch C).

=== SINKRON DOKUMEN (WAJIB, minimal) ===
Hanya yang merujuk blob/EOL nb05 — masing-masing + label `KOREKSI NL` + tanggal:
1. Pin blob nb05 baru di: `report.md:15`, `tahap_11` header + catatan koreksi, `tahap_12:5`, `tahap_14:7-10`. Pin nb01–nb04 TAK BERUBAH (hash identik — JANGAN "sinkronkan" yang tidak berubah).
2. `tahap_14` catatan B9-02 (`:11-19`): perbarui status — EOL nb05 kini **LF deterministik dari builder** (`newline="\n"` di 5 builder, diverifikasi byte); akar masalah DITUTUP (bukan lagi "ditunda"); konvensi `git hash-object` tetap berlaku sebagai pengikat.
3. DILARANG menyentuh kesimpulan, angka, count, verdict apa pun.

=== ATURAN (mengikat) ===
1. Builder→notebook: edit builder, rerun, notebook ter-regenerate. DILARANG edit `.ipynb` manual. DILARANG buka/edit nb00 (tak ada builder) — nb01–nb04 sebagai objek regen BOLEH disentuh hanya via rerun. DILARANG sentuh file audit, FIG (kecuali regen menulisnya — laporkan), `.ai/*`, `requirements.txt`, `reports/go/`. DILARANG commit/push.
2. Diff minimal (§15.1): 5× satu baris builder + baris dokumen yang diminta. EOL file `.md` jangan diubah massal.
3. Gate tiap rerun: `ruff check` + `ruff format --check` bersih; `check_foreign_chars.py` OK; `pytest -q` hijau; nbconvert exit=0 ×5. `validate_data` bila terdampak (jujur laporkan bila tidak dijalankan + alasan).
4. Laporan format AGENTS §5: file diubah + tabel Klaim & Bukti (file:baris + output, termasuk bukti byte-identik nb01–04 dan delta byte nb05) + hash baru SEMUA file berubah (`git hash-object` setelah tulis final) + STOP.

=== SELF-AUDIT 3× ADVERSARIAL (sebelum STOP) ===
Putaran 1 — Correctness: tiap builder tepat 1 baris berubah (diff membuktikan); angka notebook identik kecuali EOL nb05; tidak ada pin/merujuk EOL basi tersisa; frasa riwayat tak terkorupsi.
Putaran 2 — Bias: apakah kamu "meningkatkan" builder, menilai metode, atau mengubah kesimpulan? Apakah asumsi `newline="\n"` dinyatakan terbuka untuk auditor?
Putaran 3 — Meta: notebook hasil regenerate? File audit tak tersentuh? Hash setelah tulis final? nb00/FIG-berlebih tak dikerjakan?

STOP. Re-audit/verifikasi HANYA atas perintah terpisah.
