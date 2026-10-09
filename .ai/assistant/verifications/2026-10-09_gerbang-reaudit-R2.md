# Gerbang audit -- reaudit R-2-stratifikasi (ronde auditor independen)

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/Audit/reaudit-R2-stratifikasi.md`
**Status gerbang: LOLOS** (dokumen sah, terus ke putusan arsitek R-2)
**Putusan audit di dalam dokumen: GAGAL** atas T-1 HIGH (gate lock jam tak menggigit; angka penentu + verdict mekanis tetap benar)

## Fakta disk (cek saya sendiri, bukan salinan klaim)

| Item | Fakta | Status |
|---|---|---|
| sha256 `25E3C0E9AC559BA6FB10175507289FD386E47AA0348FB1EC881E7C9CCC7E1AAB` | `Get-FileHash` cocok (case-insensitive) | COCOK |
| blob `24a929c7f83474db0b8603f677db6213407cd44f` | `git hash-object` cocok | COCOK |
| 27235 byte / LF 599 / CR 0 / tail LF False (600 baris logis) | python baca byte mentah | COCOK ukuran; hitung baris lihat koreksi di bawah |
| TANPA self-hash (0x blob `24a929c7` / 0x sha `25E3C0E9` di isi) | hitung substring di teks = 0/0 | COCOK (pengikatan eksternal) |
| ASCII-only, LF-only | nonASCII 0, CR 0 | COCOK |
| S0 cocok: spec-R2 `c04199ce...`, hasil-R2 `c2f79913...`, B2 `4a46b815...`/`f06a8e27...`/`8a4d2109...`/`e02a203b...`, protokol-B `ed436fdd...`, hasil-B `0284f5f0...`, disposisi-B `7d125022...`, putusan-H4b `fe11383b...` | `git hash-object` ulang spec-R2 + hasil-R2 cocok; 8 hash lain dikutip verbatim dari rantai terkunci | COCOK |
| HEAD `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`, branch `codex/ANN` | `rev-parse` + `abbrev-ref` cocok | COCOK |
| staged tepat 2 T6, blob tak berubah: `2561efd5...` + `dc07a7e6...` | `diff --cached --name-only` + `ls-files -s` | COCOK |
| Laporan untracked, tak masuk index | `ls-files --others` memuat laporan | COCOK |
| Spec `:92-93` kewajiban gate terkonfirmasi | baca spec: `Assert: loop entry HANYA FIXED_HOURS lock (GAGAL bila tersentuh data)` + `utc.normalize() DILARANG` | COCOK (rujukan T-1 sah) |
| Harness + probe ada di `%TEMP%` | `r2\r2.py` True, `r2_audit\` True | COCOK keberadaan (isi = ranah auditor) |
| Verdict dokumen: GAGAL tunggal T-1 HIGH; A1 COCOK 26/26, A3 COCOK (2894 + n_Off 0/0 struktural), A4 COCOK + T-3 LOW, A5 COCOK + T-2 LOW, A6 COCOK byte-identik 3 JSON, A7 COCOK + T-4 LOW | baca isi `:12-18`, `:52-60`, `:520-534`, `:553-574` | COCOK struktur |

## Koreksi hitung baris (minor, tak pengaruhi verdict)

- Klaim kanal: 599 baris. Fakta disk: LF-count = 599, `splitlines()` = 600, tailLF = False.
- Selisih 1 = baris logis terakhir tanpa LF (`...lingkup auditor ini.` tanpa newline), bukan manipulasi. Isi/STOP/footer utuh (`STOP` `:598`, penutup `:598-600`).
- Byte 27235 tetap cocok; sha/blob tetap cocok.

## Penilaian substansi (ringkas, bukan audit ulang)

- T-1 HIGH TERCATAT BERISI: spec menuntut assert dependen-data; `r2.py:86` hanya banding konstanta-vs-literal; loop `r2.py:195` `for hh in sh4.FIXED_HOURS`; tabel sabotase S1b (top-6 data-uji, median berubah, rc 0) + S2 (`range(24)`, 3114 -> 11931 trade, artefak 3.8x, rc 0) membuktikan gate tak menggigit. Dampak angka aktual NOL (A1 26/26 + A6 byte-identik) dinyatakan terbuka di dokumen. Eskalasi ke arsitek SAH.
- T-2 LOW diteruskan: "tiga rekaman sepakat" = partisi aritmetik mesin yang sama; bukti independen sesungguhnya A1/A6.
- T-3 LOW diteruskan: 196 hari 2026 sebagai between-state, nol kontribusi bit-identik; frasa spec "dikecualikan PENUH" perlu klarifikasi arsitek.
- T-4 LOW diteruskan: label `:201` lemah, isi benar (nihil vonis H4/H5).
- Batas peran dipatuhi: rekomendasi perbaikan gate sebagai usulan, tak diterapkan; nol tulis selain laporan ini; nihil voris H4/H5/H6.

## Keputusan: LOLOS -> susun brief putusan arsitek R-2 (bawa T-1 HIGH verbatim + T-2/T-3/T-4 LOW; arsitek putus nasib gate + klarifikasi teks spec; vonis mekanis GUGUR(R-2) tak berubah oleh angka)
