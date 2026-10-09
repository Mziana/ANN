# Gerbang pra-audit — hasil coder Batch-2 H4/H5

**Tanggal:** 2026-10-09
**File:** `reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md`
**Status gerbang: LOLOS** (diteruskan ke re-audit auditor)

## Klaim vs fakta disk (cek saya sendiri, python + git)

| Klaim coder | Fakta disk | Status |
|---|---|---|
| 1299 baris / 50219 B | 1299 baris / 50219 byte (python) | COCOK |
| LF-only, pure-ASCII, foreign-chars rc=0 | CR=0, nonASCII=0 | COCOK |
| full-blob `f06a8e27…` | `f06a8e27b916172f5824438acd545614360d3b57` | COCOK |
| C8 `9cef2998…` | body-minus-last-line sha1 = `9cef2998867fc10c295a4ac53825aa9ad39e4cab` | COCOK |
| HEAD `e0b2b9f9…` tetap | `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169` | COCOK |
| staged 0, nol commit | `diff --cached` kosong | COCOK |
| sh4 trio sha `b1b69d33` | `sh4_hasil*.json` 3/3 `b1b69d33`, size 1399453 identik | COCOK |
| sh5 trio sha `7a7f5ee7` | `sh5_hasil*.json` 3/3 `7a7f5ee7`, size 13442 identik | COCOK |
| porcelain pola pra-ada | 103 baris; `M .ai/*` + `requirements.txt` + `D reports/…` pra-ada; `?? coder/` = doc baru ini | TERJAWAB sah |

## Anomali yang muncul + resolusi

- **Dua nilai C8 di chat coder** (`bf587d31…` di pesan tengah vs `9cef2998…` di final
  check). Resolusi: file berubah di tengah (tabel ringkas §8b ditambah SETELAH C8
  pertama direproduksi). Nilai FINAL (`9cef2998…` + full `f06a8e27…`) konsisten
  dengan disk saat ini. Bukan manipulasi — tapi preseden: C8 hanya bermakna
  terhadap file-beku-terakhir.
- **Verdict formula S-H4 = TAHAN, S-H5 = GUGUR** — dicatat sebagai keluaran formula,
  BUKAN vonis. Vonis resmi H4/H5 menunggu re-audit + putusan arsitek terpisah.
- **Top-6 hitung-ulang `[14,13,0,15,12,1]` vs lock P0 `[14,13,0,15,12,7]`** — coder
  mengklaim spec mengatur ini sebagai temuan sah kriteria-(a). Validitas penanganan
  = fokus re-audit (DEV-B2 + C2-AS), bukan diputus di gerbang.
- **DEV-B2-1..4 terbuka** — diteruskan sebagai batasan untuk arsitek via auditor.

## Batas gerbang ini

- Run-ulang harness (byte-repro eksekusi) TIDAK dilakukan di sini — wewenang
  re-audit auditor (C5). Klaim determinisme berbasis trio-sha + `cmp IDENTIK`
  di [O5], yang keberadaan + hash-nya saya verifikasi di disk.
- Isi analitik (angka EV, p-value Holm, MFE/MAE) TIDAK dihitung-ulang di sini —
  wewenang auditor.

## Keputusan: LOLOS → susun prompt re-audit sempit Batch-2
