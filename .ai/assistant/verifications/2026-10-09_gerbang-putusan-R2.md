# Gerbang putusan -- arsitek/putusan-R2-stratifikasi.md (2026-10-09)

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/arsitek/putusan-R2-stratifikasi.md`
**Status gerbang: LOLOS -- R-2 TERTUTUP dengan catatan V-2**

## Fakta disk (cek saya sendiri, bukan salinan klaim)

| # | Klaim kanal | Hasil ukur saya | Status |
|---|---|---|---|
| 1 | Blob `c92733fd7957fc71fc42bec1769356d746d86dc8` | `git hash-object` -> identik 40-hex | COCOK |
| 2 | 143 baris (<150), foreign rc=0, LF-only, ASCII murni | python: 7697 B / LF 143 / CR 0 / nonASCII 0 / tailLF True / 143 baris logis; self-hash `c92733fd` di isi = 0x | COCOK semua |
| 3 | S0 9/9 + HEAD `e0b2b9f9` + staged 2 T6 | `rev-parse` persis; S0 di berkas `:14-25` (trio R-2 + B2 + disposisi-B + H4b); `ls-files -s` 2 blob tak berubah (`2561efd5...`, `dc07a7e6...`) | COCOK |
| 4 | Satu-satunya tulis arsitek, untracked, nol commit | `status --porcelain -- <path>` = `??`; HEAD tak bergeser | COCOK |
| 5 | S-V(a)-(e) dikerjakan sendiri | baca isi `:39-67`: (a) lock+loop aktual, (b) angka ukur-sendiri JSON `4664B4D8...` + 4 sha parquet, (c) tidak run-ulang per butir + S27, (d) T-1 kata-sendiri + S1b/S2 kinetik, (e) T-2/T-3/T-4 dari bahan | COCOK struktur |
| 6 | V-1 vonis resmi GUGUR | `:71-81`: lock `:55-57` verbatim atas median sepakati (2024 `> 0`, 2025 `<= 0`, `tahun_gugur=[2025]`); satu kalimat dikutip; R-2 saja, bukan H4/H5 | COCOK |
| 7 | V-2 opsi (ii) TERIMA DENGAN CATATAN | `:85-100`: pilih (ii) berpasal (angka independen + loop aktual benar + preseden P-4/T2; (i) ditolak sebagai teater proses); pola konstanta PENSIUN; pengganti mengikat (`set(jam_utc trades) == set(LOCK_HOURS)` + S1b/S2 wajib `rc != 0`) | COCOK, TERTUTUP tanpa syarat gantung |
| 8 | V-3 T-2/T-3/T-4 satu-per-satu | `:104-116`: ketiganya TUTUP catatan tanpa erratum + klarifikasi mengikat T-3 ("PENUH" = nol kontribusi, uji kausal wajib); T-4 dibaca `TERVERIFIKASI`; severity tetap LOW | COCOK |
| 9 | V-4 anti-merambat + self-audit 3x + STOP | `:120-126` + `:130-143`: H4 Batch-2/H1-H3/H5/H4b/fondasi-B utuh, H6 ditolak, P-5 mengikat; STOP menutup | COCOK |

## Keputusan: LOLOS -- R-2 TERTUTUP dengan catatan V-2 (vonis resmi GUGUR(R-2); pola assert-konstanta pensiun; tidak ada ronde lanjutan R-2 tanpa spec baru)
