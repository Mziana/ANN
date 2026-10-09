# Verifikasi Langkah 1 audit nb05 — 2026-10-06

## 1. File tersimpan
`reports/governance/2026-10-06/audit/eda_nb05_audit_v1.md` ADA (2.138 byte,
mtime 21:57). Isi = draf Langkah 1, cocok dengan klaim chat (4 metrik + verdict).

## 2. SHA256 TIDAK COCOK
- Klaim auditor: `9dd935bfc532…`
- Hitung ulang asisten: `f800819ff645a1efb013cc26a2277fa178fe061edcabd13bdc98b8a91787d218`
- Status: MISMATCH. Kemungkinan: hash dihitung sebelum tulis final / beda
  encoding. BUKAN bukti fabrikasi isi (isi file cocok dengan chat), tetapi
  klaim hash SALAH dan wajib dikoreksi — STOP auditor ("sebut hash") belum sah.

## 3. Referensi silang ke nb03 (spot-check asisten)
- `-0.022624` ADA di output nb03 (×3). ✓
- VR `1.03xx` ADA (1.0330/1.0346/1.0359…). ✓ (klaim ref 1.0337 plausibel)
- `0.0035` dan `0.0018` KEDUANYA ADA di output nb03. ✓
- Kesimpulan: auditor benar-benar membaca output nb03, bukan mengarang.

## 4. Catatan kualitas (bukan temuan, untuk langkah berikut)
- "Bukti File" menulis "baris ~t15" — samar, melanggar aturan bukti
  file:baris yang ia sebut sendiri (§20). Minta nomor baris pasti mulai Langkah 2.
- Assert VR "implisit via toleransi wajar" = tidak ada assert; jujur dinyatakan,
  tetapi labelnya jangan disamakan dengan assert eksplisit.
- "EXACT MATCH" untuk selisih 0,7% = pilihan kata berlebihan; maksudnya
  "dalam toleransi".
