# Revisi Audit — LOW-27.1 (Klarifikasi) — v1

**Tanggal:** 2026-10-06 · **Auditor:** Klenz · **Rujukan:** `eda_fragmen_spread_4b_audit_v1.md` (LOW-27)
**Pemicu:** penolakan coder atas LOW-27.1 dengan 4 alasan (laporan_fix_audit_fragmen.md §B).

## Pertanyaan yang dijawab
1. **Apakah memang typo/salah tulis?** Terpisah menjadi dua hal yang tercampur di temuan awal:
   - Status "BELUM DITERAPKAN" → **faktual** (config belum memuat `cost_basis`/`stress_bands` saat itu; hanya baris komentar yang menyebutnya). Argumen safety coder (poin 2–4) tidak terbantahkan.
   - Ejaan kata terakhir `DITERAPKAN` → **typo nyata**; kata baku **DITERAPKAN** (dari *menerapkan*).
2. **Apakah mengorbankan kebenaran?** Tidak. Yang dikorbankan justru ejaan; status benar. **Miskomunikasi lahir dari notasi temuan saya sendiri** — `→ "DITERAPKAN"` terbaca sebagai penggantian status seluruhnya.
3. **Bukti byte-exact:** baris 1 file terverifikasi via `sed -n '1p'`; typo hidup juga di `eda_02_volatility.ipynb` (cell 1931/2010) — **notebook = generator**, mengoreksi .yaml saja akan hilang saat regenerasi.

## Keputusan
**MODIFIKASI** — bukan VALID seperti ditulis, bukan DICABUT.
- Penggantian status → **DICABUT** (coder benar; interpretasi itu lahir dari notasi ambigu auditor).
- Koreksi ejaan `DITERAPKAN → DITERAPKAN` dengan "BELUM" tetap → **TETAP VALID** (LOW, kosmetik).

## Tindak lanjut yang disepakati
1. Perubahan minimal: hanya huruf N pada kata terakhir; makna/status tidak berubah.
2. Perbaikan di **sumber generator** (cell notebook), bukan hanya file hasil.
3. **Perbaikan proses sisi auditor:** temuan teks ditulis dengan notasi tak-ambigu (kutip kalimat utuh pasca-perbaikan).
4. Tidak ada gate yang terpengaruh; verdict ronde 4b tidak berubah.

*Status akhir ronde fix (laporan_fix_audit_fragmen.md, terverifikasi auditor): LOW-27.1 **no-op** — byte tersimpan sudah ejaan benar (`sed` → "DITERAPKAN"); LOW-27.2 dan 27.3 terverifikasi FIX; MEDIUM-26/27/28 + LOW-26 terverifikasi FIX dengan bukti angka independen oleh auditor.*
