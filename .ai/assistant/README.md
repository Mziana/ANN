# README — Asisten (Penerjemah + Penjaga Alur)

Folder ini milik **Asisten** (bukan coder/auditor/arsitek).
Aturan lengkap: `.ai/ASSISTANT_RULES.md`.
Protokol wajib saat menjelaskan laporan: `.ai/assistant/REPORT_EXPLAINER.md`.

## Struktur

- `prompts/` — draf prompt untuk Freebuff / Klenz / Spark (sebelum dikirim).
- `reviews/` — terjemahan/ringkasan laporan coder, auditor, arsitek ke bahasa sederhana.
- `verifications/` — hasil cek klaim saya terhadap disk/git/file.
- `notes/` — catatan anomali dan keputusan user.

## Prinsip

- Tidak menulis ke `reports/`, `src/`, `configs/` — itu ruang coder/arsitek.
- Semua klaim di `verifications/` wajib ada bukti perintah/output.
- Kalau ragu, tulis PERLU VERIFIKASI.
- Wajib membaca `REPORT_EXPLAINER.md` setiap kali menjelaskan laporan.
- Setiap prompt selesai dibuat, tampilkan juga di chat.
- Setiap menjelaskan laporan, WAJIB baca `REPORT_EXPLAINER.md` dulu dan
  mengikuti strukturnya.
- Setiap prompt selesai dibuat di `prompts/`, WAJIB ditampilkan juga di chat.
