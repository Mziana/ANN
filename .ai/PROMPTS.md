# PROMPTS.md - Prompt Siap Pakai

> Kumpulan prompt untuk user paste ke AI coder.
> Versi: 2.0
> Update: 2026-10-05
> Proyek: USDJPY Trading Bot

## Cara Pakai

1. Cari prompt sesuai situasi (lihat tabel).
2. Copy seluruh blok di antara tanda kutip tiga.
3. Ganti bagian `<...>` dengan info Anda.
4. Paste ke AI coder.

## Daftar Prompt

### Kategori A - Sesi & Dasar
| # | Prompt | Kapan |
|---|---|---|
| 0 | Onboarding AI Baru | AI baru / ganti model |
| 1 | Session Start | Buka sesi |
| 2 | Session End | Tutup sesi |
| 8 | Force Re-Read | AI lupa |
| 15 | Minta Penjelasan | Tidak paham |

### Kategori B - Tugas
| # | Prompt | Kapan |
|---|---|---|
| 3 | New Coding Task | Tugas kode |
| 4 | New Trading Task | Tugas trading |
| 11 | Reuse Check | AI mau bikin baru |
| 12 | Pre-Commit Check | Sebelum commit |
| 13 | Update Context | Perubahan besar |
| 14 | Update State | Checkpoint |

### Kategori C - Audit & Verifikasi
| # | Prompt | Kapan |
|---|---|---|
| 5 | Code Review | Review kode (self) |
| 6 | Failure Analysis | Strategi gagal |
| 7 | Strategy Audit | Audit internal |
| 9 | Anti-Halusinasi | Klaim tanpa bukti |
| 10 | Force Test | AI malas uji |

### Kategori D - Discovery
| # | Prompt | Kapan |
|---|---|---|
| 16 | Strategi Discovery | Fase 4 |
| 17 | Bandingkan Kandidat | Setelah uji |
| 18 | Cek Overfit | Sebelum live |

### Kategori E - Referensi
| # | Prompt | Kapan |
|---|---|---|
| 19 | Wajib Verifikasi | API/library baru |
| 20 | Cek Versi | Mulai kode baru |
| 21 | Paste Referensi | Setelah PERLU VERIFIKASI |
| 22 | Paksa Browse | AI bilang tidak bisa |

### Kategori F - GitHub
| # | Prompt | Kapan |
|---|---|---|
| 23 | Baca Link GitHub | Kirim link repo |
| 24 | Update GitHub | Push ke repo |

### Kategori G - Auditor (AI Terpisah)
| # | Prompt | Kapan |
|---|---|---|
| A1 | Audit Kode | Setelah coder selesai |
| A2 | Audit Strategi | Setelah backtest |
| A3 | Verifikasi Spesifik | Cek 1 aspek |
| A4 | Red Team | Sebelum live |
| A5 | Bandingkan Versi | Cek kode lama vs baru |

### Kategori H - Architect (AI Terpisah)
| # | Prompt | Kapan |
|---|---|---|
| B1 | Arsitek: Rancang | Sebelum fitur besar |
| B2 | Auditor: Re-Audit | Setelah coder self-audit |
| B3 | Arsitek: Tie-Breaker | Coder vs Auditor konflik |

---

## PROMPT 0 - Onboarding AI Baru

Kapan: AI baru pertama kali, ganti model, atau setelah jeda lama.
ONBOARDING AI BARU.

Kamu adalah AI BARU di proyek ini. Kamu belum tahu apa-apa.
JANGAN langsung koding. Ikuti protokol onboarding (section 24 AGENTS.md):

FASE 1 - BACA ATURAN:

.ai/AGENTS.md

.ai/RULES.md

.ai/CONTEXT.md

.ai/PROMPTS.md

docs/PROJECT_MAP.md (kalau ada)

FASE 2 - BACA STATE:

.ai/STATE.md

.ai/PROGRESS.md

.ai/TASKS.md

.ai/CHECKPOINT_LOG.md

.ai/SESSION_LOG.md

FASE 3 - INVENTARISASI:
Jelajahi src/, strategies/, notebooks/, configs/, tests/, journal/.
List semua file + docstring. JANGAN baca detail isi.
Cukup: nama file, docstring, tujuan.

FASE 4 - LAPORKAN (format section 24 AGENTS.md):

Identitas proyek

Posisi proyek (fase, progress)

Struktur file yang sudah ada

File konkret + fungsi

Apa yang sudah selesai

Apa yang belum

Aturan kunci (Reuse-First, no start from 0)

Pertanyaan (kalau ada)

FASE 5 - TUNGGU KONFIRMASI.
JANGAN mulai kerja sebelum user bilang "lanjut".

DILARANG:

Langsung koding.

Bikin file baru sebelum inventarisasi.

Mulai dari 0.

Rewrite file lama

---

## PROMPT 1 - Session Start

Kapan: Setiap buka sesi chat.
SESSION START.

Baca berurutan:

.ai/STATE.md

.ai/TASKS.md

.ai/PROGRESS.md

.ai/AGENTS.md

.ai/RULES.md

.ai/CONTEXT.md

Entry terakhir .ai/SESSION_LOG.md

Tulis konfirmasi Session Start (section 0.1 AGENTS.md).
Tunggu konfirmasi saya sebelum lanjut.

---

## PROMPT 2 - Session End
SESSION END.

Update:

.ai/STATE.md

.ai/TASKS.md

.ai/PROGRESS.md

.ai/SESSION_LOG.md

journal/daily/YYYY-MM-DD.md

journal/INDEX.md

.ai/CONTEXT.md (kalau perlu)

Tulis konfirmasi Session End (section 0.2 AGENTS.md).

---

## PROMPT 3 - New Coding Task
TUGAS KODE BARU.

Tugas: <deskripsi>

Ikuti:

Pre-Flight Check (section 0.1 AGENTS.md).

Laporan Reuse (section 16 AGENTS.md).

Tunggu konfirmasi saya.

Tulis kode.

Self-Review (section 4 AGENTS.md).

Laporan dengan tabel Klaim & Bukti (section 5, 20).

DILARANG:

Bikin file baru kalau ada yang bisa dipatch.

Klaim "sudah selesai" tanpa bukti.

Skip test tanpa alasan.

---

## PROMPT 4 - New Trading Task
TUGAS TRADING.

Tugas: <deskripsi>

Ikuti:

Baca ulang RULES.md section 18 (Aturan Trading).

Cek fase di CONTEXT.md section 3.

Cek asumsi di CONTEXT.md section 7.

Tulis Proposal Uji (section 21.3 AGENTS.md) kalau eksperimen.

Tunggu konfirmasi.

DILARANG:

Tolak uji dengan opini (section 21).

Kesimpulan sebelum uji.

Sembunyikan hasil negatif.
CODE REVIEW.

Review file: <path>

Cek:

Bug (edge case, off-by-one, None handling).

Look-ahead bias.

Data leakage.

Bid/ask handling (section 18.16 RULES.md).

Konvensi RULES.md.

Hardcode.

Duplikasi.

Test coverage.

Anti-pattern (section 19 AGENTS.md).

Laporkan dengan tabel Klaim & Bukti.
Jangan ubah kode dulu.
---

## PROMPT 6 - Failure Analysis
ANALISIS KEGAGALAN.

Strategi <nama> gagal:

Sharpe: <...>

Drawdown: <...>

Win rate: <...>

Ikuti Protokol Persistence (section 17 AGENTS.md):

Analisis (data, fitur, label, model, eksekusi, regime).

Ajukan minimal 3 hipotesis perbaikan.

Ekspektasi perbaikan per hipotesis.

Rekomendasi urutan uji.

Tunggu konfirmasi.

DILARANG:

Menyerah setelah 1 kegagalan.

Saran ganti instrumen tanpa diminta.

Saran ganti timeframe tanpa analisis.

---

## PROMPT 7 - Strategy Audit
AUDIT STRATEGI.

Strategi: <nama>

Ikuti Template Audit (section 18 AGENTS.md). Semua section WAJIB:
A. Performa Dasar
B. Analisis Trade
C. Analisis Regime
D. Robustness
E. Bias
F. Biaya
G. Kegagalan
H. Kesimpulan

Kalau data belum ada, tulis "BELUM ADA DATA".
Jangan simpulkan sebelum semua selesai.


---

## PROMPT 8 - Force Re-Read
STOP.

Kamu lupa konteks. Lakukan:

Baca ulang .ai/AGENTS.md dan .ai/RULES.md.

Baca ulang .ai/STATE.md dan .ai/TASKS.md.

Baca ulang .ai/CONTEXT.md.

Konfirmasi:

Sedang kerjakan apa.

Fase proyek.

3 aturan WAJIB paling relevan.

Jangan lanjut sebelum konfirmasi.


---

## PROMPT 9 - Anti-Halusinasi
ULANGI LAPORAN.

Melanggar section 20 AGENTS.md (Anti-Halusinasi).

Wajib:

Tabel "Klaim & Bukti".

Status: TERVERIFIKASI / BELUM DIVERIFIKASI / ASUMSI / GAGAL.

Paste output asli.

Kalau tidak bisa verifikasi, tulis BELUM DIVERIFIKASI.

DILARANG:

"Sepertinya OK"

"Mungkin benar"

"Harusnya jalan"

Klaim "sudah" tanpa bukti.

Mengarang output test.


---

## PROMPT 10 - Force Test
ULANGI.

Kamu menolak uji dengan opini. Melanggar section 21 AGENTS.md.

Lakukan:

Tulis Proposal Uji (section 21.3):

Apa yang diuji

Hipotesis

Metrik

Baseline

Threshold sukses

Estimasi biaya

Rencana

Tunggu konfirmasi.

Baru uji.

DILARANG:

"Menurut saya..."

"Biasanya..."

"Sepertinya..."

"Saya yakin..."


---

## PROMPT 11 - Reuse Check
SEBELUM BIKIN FILE BARU.

Ikuti Protokol Reuse-First (section 16 AGENTS.md):

List file src/ relevan.

List fitur lama (config, filter, jurnal, sinyal).

List modul utils.

Tulis Laporan Reuse.

Tunggu konfirmasi.

DILARANG:

Bikin file baru kalau ada yang bisa dipatch.

Abaikan fitur lama.

Bikin "v2" tanpa alasan.


---

## PROMPT 12 - Pre-Commit Check
PRE-COMMIT CHECK.

Cek section 21 RULES.md:

Black, Ruff, test passed.

Type hints, docstring lengkap.

No hardcode, print(), except: pass.

No look-ahead bias, data leakage.

Bid/ask handling benar (section 18.16).

Import rapi.

Tidak commit .env / secrets.

Laporkan dengan tabel Klaim & Bukti.
Kalau ada yang belum, jangan bilang siap commit.


---

## PROMPT 13 - Update Context
UPDATE CONTEXT.md.

Perubahan: <deskripsi>

Update section relevan:

section 3 Fase

section 6 Keputusan Penting

section 7 Asumsi

section 5 Strategi

Bump versi (v1.2 -> v1.3). Changelog di header.


---

## PROMPT 14 - Update State
CHECKPOINT.

Update:

.ai/STATE.md

.ai/TASKS.md

.ai/SESSION_LOG.md

Format mini-log:

Checkpoint HH:MM
Selesai: <ringkas>

Lanjut: <ringkas>

Blocker: <->


---

## PROMPT 15 - Minta Penjelasan
JELASKAN.

Jelaskan <topik/kode/keputusan>:

Analogi sederhana.

Kenapa penting.

Risiko kalau salah.

Contoh konkret.

Asumsi: saya bukan programmer. Hindari jargon.
Kalau ada istilah teknis, jelaskan dalam 1 baris.

---

(Part 2 akan ditambahkan di file yang sama)

## PROMPT 16 - Strategi Discovery
TUGAS DISCOVERY STRATEGI.

Fase proyek: <CONTEXT.md section 3>
Data: USDJPY, TF <M1/M5/M15>

Alur discovery (bukan rekomendasi):

LANGKAH 1 - EDA
Analisis data:

Distribusi return

Volatilitas per jam & sesi

Autokorelasi (trending/mean-reverting)

Swing high/low

Level yang di-hormati

Karakter per regime

LANGKAH 2 - Hipotesis
Dari EDA, ajukan 3-5 hipotesis.
Setiap hipotesis: berbasis data, testable, metrik jelas.

LANGKAH 3 - Proposal Uji
Untuk setiap hipotesis.

LANGKAH 4 - Tunggu Konfirmasi.
Jangan uji dulu.

DILARANG:

Langsung kasih "strategi terbaik" tanpa EDA.

Pilih karena "populer".

Skip EDA.

---

## PROMPT 17 - Bandingkan Kandidat
BANDINGKAN KANDIDAT.

Kandidat:

<A> - <metrik>

<B> - <metrik>

<C> - <metrik>

Tabel:

Metrik	A	B	C	Baseline
Sharpe				
Max DD				
WR				
PF				
Expectancy				
Robust				
Analisis:

Mana paling robust (bukan tertinggi)?

Mana tahan biaya?

Mana sesuai EDA?

Ada overfit?

Rekomendasi?

Laporkan dengan Klaim & Bukti.


---

## PROMPT 18 - Cek Overfit
CEK OVERFIT.

Strategi: <nama>
In-sample: <metrik>
Out-of-sample: <metrik>

Cek 6 poin:

Gap in-sample vs out-of-sample?

Berapa parameter dioptimasi?

Walk-forward?

Stabil di berbagai periode?

Sensitif ke perubahan parameter kecil?

Monte Carlo shuffle?

Verdict: OVERFIT / OK / PERLU UJI.

DILARANG bilang "bagus" tanpa cek 6 poin.


---

## PROMPT 19 - Wajib Verifikasi
VERIFIKASI API/LIBRARY.

Sebelum pakai <nama>, verifikasi:

Library ada? Versi?

Fungsi <nama> ada?

Signature (parameter)?

Return?

Contoh minimal?

WAJIB coba browse dulu (section 22 AGENTS.md).
Berhasil: laporkan URL + isi.
Gagal: tulis "PERLU VERIFIKASI: <topik>".

| Item | Nilai | Sumber | Status |

DILARANG:

Bilang "tidak bisa cek" tanpa coba.

Mengarang URL/API.


---

## PROMPT 20 - Cek Versi
CEK VERSI.

Sebelum kode baru, konfirmasi:

Python: <3.11>

pandas: <...>

numpy: <...>

torch: <...>

MetaTrader5: <...>

Cek: API ada di versi itu? Deprecation? Breaking change?

Kalau ragu, browse. Gagal browse, tulis "PERLU VERIFIKASI".
DILARANG mengarang versi.


---

## PROMPT 21 - Paste Referensi
REFERENSI DARI USER.

Ini referensinya:
<paste dokumentasi/URL>

Tugas:

Baca referensi.

Konfirmasi apa yang kamu ambil.

Lanjutkan tugas dengan info ini.

Tandai: sumber = user-provided.

Jangan mengarang di luar referensi.
Kalau kurang, bilang "PERLU VERIFIKASI" lagi.


---

## PROMPT 22 - Paksa Browse
PAKSA BROWSE.

Kamu bilang tidak bisa cek. Melanggar section 22.4 AGENTS.md.
WAJIB coba browse dulu sebelum menyerah.

Lakukan:

Coba browse ke <sumber relevan>.

Berhasil: laporkan URL + isi.

Gagal: tulis "PERLU VERIFIKASI" + alasan.

Jangan mengarang.

DILARANG bilang "tidak bisa" tanpa coba.


---

## PROMPT 23 - Baca Link GitHub
BACA REPO GITHUB.

URL: <link>

Ikuti section 23 AGENTS.md:

Browse link.

Baca README, struktur, file relevan.

Laporan Baca Repo (section 23.2).

Tandai yang bisa di-reuse.

Tandai yang berbeda dengan lokal.

Rekomendasi: patch / merge / skip.

DILARANG:

Abaikan link.

Mengarang isi repo.

Lanjut tanpa laporan.


---

## PROMPT 24 - Update GitHub
UPDATE GITHUB.

Perubahan: <deskripsi>

Ikuti section 23.4 AGENTS.md:

Konfirmasi branch.

Konfirmasi commit message.

Konfirmasi file.

Tanya saya dulu sebelum push.

Format: type(scope): pesan singkat.


---

## PROMPT A1 - Audit Kode (Auditor)

Kapan: Setelah coder selesai. Audit adversarial.
AUDIT KODE (ADVERSARIAL).

Kamu AUDITOR. Tugas: MENCARI YANG SALAH.
Kamu DILARANG menulis kode.

=== FILE ===
<path>

=== LAPORAN CODER ===
<paste>

=== PROTOKOL ===

Cek SEMUA:

Bug (edge case, off-by-one, None handling)

Look-ahead bias

Data leakage

Bid/ask handling (section 18.16 RULES.md)

Spread di backtest

Hardcode

Duplikasi dengan file lama

Anti-pattern (section 19 AGENTS.md)

Konvensi RULES.md

Test coverage

Reuse-First (section 16 AGENTS.md)

Format laporan:

Laporan Audit
Ringkasan
File: <list>

Jumlah temuan: <N>

Verdict: LULUS / PERLU PERBAIKAN / TOLAK

Temuan
[CRITICAL-01] <judul>
Lokasi: <file>:<baris>

Masalah: <deskripsi>

Bukti: <bukti>

Dampak: <akibat>

Saran: <perbaikan>

[HIGH-01] ...
[MEDIUM-01] ...
[LOW-01] ...
Yang Sudah Benar
<singkat>
Pertanyaan untuk Coder
<kalau ada>
DILARANG:

Menulis kode.

Bilang "sepertinya OK" tanpa cek.

Memuji tanpa alasan.

Skip item di atas.

Tanpa bukti.


---

## PROMPT A2 - Audit Strategi (Auditor)
AUDIT STRATEGI (ADVERSARIAL).

Kamu AUDITOR STRATEGI. Cari KELEMAHAN.
DILARANG menulis kode.

=== STRATEGI ===
<nama + deskripsi>

=== HASIL BACKTEST ===
<paste>

=== FILE ===
<config, signal.py, dll>

=== PROTOKOL ===

Cek 8 kategori (section 18 AGENTS.md):
A. Performa Dasar
B. Analisis Trade
C. Analisis Regime
D. Robustness (walk-forward, Monte Carlo, stress test)
E. Bias (look-ahead, leakage, survivorship, overfit)
F. Biaya (spread, slippage, bid/ask)
G. Kegagalan
H. Kesimpulan

KHUSUS ADVERSARIAL - cari:

Hasil "terlalu bagus"?

Berapa parameter dioptimasi?

Gap in-sample vs out-of-sample?

Hanya jalan di 1 periode?

Hanya jalan di 1 sesi?

Bid/ask benar?

Spread realistis?

Asumsi tidak diverifikasi?

Format:

Laporan Audit Strategi
Verdict: LULUS / PERLU PERBAIKAN / TOLAK
Temuan Kritis
Temuan Lain
Rekomendasi
Pertanyaan untuk Coder
DILARANG:

Menulis kode.

Memuji tanpa data.

Bilang "bagus" tanpa cek 8 kategori.


---

## PROMPT A3 - Verifikasi Spesifik
VERIFIKASI SPESIFIK.

Kamu auditor. Cek HANYA aspek: <aspek>.

=== FILE ===
<path>

=== ASPEK ===
<misal: bid/ask, look-ahead, data leakage>

Format:

Verifikasi <aspek>
Temuan
| # | Lokasi | Masalah | Severity | Saran |

Verdict: LULUS / PERLU PERBAIKAN
DILARANG cek aspek lain, menulis kode.


---

## PROMPT A4 - Red Team
RED TEAM STRATEGI.

Kamu RED TEAM. Tugas: BANTAI strategi ini.
Cari SEGALA cara strategi GAGAL.

=== STRATEGI ===
<nama + deskripsi + hasil>

=== MISI ===

Bayangkan kamu market maker yang ingin mengalahkan strategi ini.

Cari:

Kapan paling rentan?

Kondisi pasar apa yang menghancurkan?

Event apa yang bikin rugi besar?

Bagaimana broker bisa mengalahkan?

Bagaimana slippage merusak?

Bagaimana spread widening merusak?

Bagaimana intervensi BoJ merusak?

Bagaimana black swan merusak?

Asumsi rapuh?

Tail risk yang diabaikan?

Format:

Red Team Report
Skenario Serangan
<skenario> - Trigger, Dampak, Severity, Mitigasi
Asumsi Rapuh
Tail Risk
Verdict: Siap Live? Ya/Tidak
DILARANG:

Memuji.

Bilang "sudah bagus".

Kalau tidak ketemu kelemahan, audit kurang dalam.


---

## PROMPT A5 - Bandingkan Versi
BANDINGKAN 2 VERSI.

=== LAMA ===
<path>

=== BARU ===
<path>

Cek:

Apa berubah?

Kenapa? (baca commit/komentar)

Memperbaiki?

Ada regresi (fitur hilang)?

Duplikasi?

Konvensi tetap?

Test masih pass?

Format:

Perbandingan Versi
Perubahan
| Aspek | Lama | Baru | Verdict |

Regresi
Perbaikan
Verdict: LEBIH BAIK / SAMA / LEBIH BURUK
DILARANG menulis kode, bilang "lebih baik" tanpa bukti.


---

## PROMPT B1 - Arsitek: Rancang
TUGAS ARSITEK.

Kamu ARCHITECT. Tugas: rancang, bukan implementasi.

Tugas: <deskripsi>

Ikuti:

Baca .ai/AGENTS.md, RULES.md, CONTEXT.md.

Baca STATE.md, TASKS.md.

Baca file terkait di src/ (jangan duplikasi).

Output:

Rancangan
Tujuan
Pendekatan
Struktur File
<file baru/diubah>: <tanggung jawab>

Dependency (reuse)
Risiko
Alternatif + trade-off
Kriteria Sukses
Rencana Implementasi (langkah kecil)
DILARANG:

Menulis kode produksi.

Implementasi.

Skip baca file lama.


---

## PROMPT B2 - Auditor: Re-Audit
AUDIT ULANG.

Kamu Auditor. Coder sudah self-audit. Audit ulang.

=== KODE ===
<path>

=== SELF-AUDIT CODER ===
<paste>

Tugas:

Baca kode.

Baca self-audit coder.

Cari yang coder LEWATKAN.

Cari yang coder SALAH audit.

Cari yang coder TIDAK cek.

Fokus: apa yang self-audit tidak tangkap?

Format:

Audit Ulang
Yang Coder Sudah Cek (Benar)
Yang Coder Lewatkan
[CRITICAL/HIGH/MEDIUM]

Yang Coder Salah Cek
Coder bilang: <X>

Sebenarnya: <Y>

Bukti: <bukti>

Verdict: LULUS / PERLU PERBAIKAN / TOLAK
DILARANG:

Menulis kode.

Mengulang temuan coder tanpa tambahan.

Bilang "sama dengan coder" tanpa cek ulang.


---

## PROMPT B3 - Arsitek: Tie-Breaker
TIE-BREAKER.

Kamu ARCHITECT. Ada konflik Coder vs Auditor.

=== KONFLIK ===
<isu>

=== ARGUMEN CODER ===
<paste>
Bukti Coder: <output test / benchmark / data>

=== ARGUMEN AUDITOR ===
<paste>
Bukti Auditor: <bukti bug / data / logika>

Tugas:

Baca dua argumen.

Cek bukti masing-masing.

Nilai berdasarkan: fakta, dampak, tujuan proyek.

Putuskan:

CODER BENAR

AUDITOR BENAR

DUA-DUANYA SALAH

BUTUH UJI TAMBAHAN

Format:

Keputusan Tie-Breaker
Analisis
Keputusan
Alasan
Tindak Lanjut
DILARANG:

Menulis kode.

Menghindari keputusan.

Bilang "dua-duanya benar" (kecuali benar-benar).


---

## Catatan Penggunaan

1. Prompt 0 wajib untuk AI baru / ganti model.
2. Prompt 1 wajib setiap sesi baru.
3. Prompt 2 wajib setiap tutup sesi.
4. Prompt 8-10 untuk menegur AI.
5. Prompt A1-A5 untuk auditor (AI terpisah).
6. Prompt B1-B3 untuk architect (AI terpisah).
7. Prompt 19+22 = pasangan browse.
8. Prompt 21 = kasih referensi manual.

---

Akhir PROMPTS.md v2.0
