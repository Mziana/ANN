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

## Pengingat Operasional (keputusan user 2026-10-08, WAJIB)

- Membaca README ini = WAJIB membaca `PROMPT_DISIPLIN.md` sampai habis dan
  menerapkan ketiga aturannya (perintah mentah per syarat, larangan
  bentuk-spesifik, gerbang pra-audit) pada setiap prompt berikutnya.
- Setiap prompt untuk coder/arsitek/auditor WAJIB memuat perintah eksplisit:
  tulis laporan/putusan/audit sebagai **file .md** (sebutkan nama file + folder
  tujuannya di dalam prompt). Tanpa perintah ini, prompt belum selesai.
- Jika mereka lupa / laporannya hanya ada di chat: **Asisten yang menuliskannya**
  menjadi file .md di lokasi kanonis — verbatim, tanpa dikurangi dan tanpa
  ditambah — lalu catat path + hash-nya sebagai sumber resmi.
- Asisten WAJIB update penjurnalan **setiap ada perubahan dan keputusan baru**,
  sebelum lanjut ke langkah berikut: `.ai/SESSION_LOG.md` (mini-log),
  `journal/daily/YYYY-MM-DD.md`, dan `.ai/STATE.md` / `.ai/TASKS.md` bila ada
  keputusan baru. DILARANG menunda penjurnalan sampai akhir sesi.
