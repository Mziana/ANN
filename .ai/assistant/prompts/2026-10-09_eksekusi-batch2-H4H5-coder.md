# PROMPT — Eksekusi Coder Batch-2 (H4+H5) — 2026-10-09 (tulis-ulang v2)

> Status: FINAL 2026-10-09 — substansi arsitek + 2 disiplin tambahan
> DISETUJUI user. Siap paste ke coder.
> File: `.ai/assistant/prompts/2026-10-09_eksekusi-batch2-H4H5-coder.md`

---

Anda adalah **Coder** (kontrak bersama `.ai/AGENTS.md` §26: implementasi +
self-audit + fix; DILARANG menentukan arsitektur; DILARANG mengaudit
sendiri; DILARANG menulis kode produksi untuk peran lain). Kerja di
`D:\ANN`. DILARANG commit/push tanpa perintah eksplisit.

Tugas SATU-SATUNYA sesi ini: eksekusi
`reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md`
kata-per-kata, lalu tulis hasilnya sebagai **file .md** di
`reports/governance/2026-10-07/coder/hasil-lapisan3-H4H5.md`.

## Gerbang masuk (ukur sesi ini, tempel output; mismatch = STOP)

1. `git hash-object reports/governance/2026-10-07/arsitek/spesifikasi-lapisan3-H4H5.md`
   → WAJIB `4a46b815211e6b0b050cbb6f3e98ce5e27904069`.
2. `git rev-parse HEAD` → WAJIB `e0b2b9f9e4b300fba5e4ccea3a97e29c4ad5b169`.
3. Bila brief ini vs spec berselisih, spec menang.

## Substansi eksekusi (verbatim arsitek, diringkas tanpa diubah maknanya;
detail penuh = spec)

**S-H4 — sesi-pintu (LONG-ONLY, tanpa tesis arah).** Universe: bar M15
processed 2024/2025 + join posisional ke features store beku (gate: n sama
+ sekuens date_broker/hour_utc identik + sha S0; mismatch = GAGAL-eksekusi).
(a) Bar sinyal = bar M15 yang buka tepat pada HH:00 UTC untuk HH dalam
[14,13,0,15,12,7] (6 bar/hari; tanpa filter close>open). (b) Entry long
pada close bar sinyal; 1x per jam-tetap per hari-broker; bar tak ada (gap)
= jam itu FLAT, dilaporkan. (c) ATR = `atr_14_d1` hari T-1; SL = entry −
1x ATR; TP = entry + 2x ATR (JPY); monitoring mulai bar berikutnya.
(d) Exit: (i) low ≤ SL → exit SL; (ii) else high ≥ TP → exit TP;
(iii) else close bar M15 terakhir hari T → time-stop. Prioritas intra-bar
SL > TP. TIDAK ada signal-exit. (e) Biaya =
`cost_basis.by_session[session_label(bar entry)]` (London 0.61 / NewYork
0.69 / Tokyo 0.62 / Sydney 0.8 pip; Off → default 0.65) × 0.01; EV (JPY) =
exit − entry − cost; fill exact, tanpa slippage di luar cost_basis.
(f) Overlap antar jam-tetap DIIZINKAN, per-trade independen, tanpa agregasi
portofolio. Tanpa pengecualian hari.
Kriteria-(a): resep M2 persis pada M1 2024–2025 pool
(`hourly.groupby("hour_utc")["abs_r_pips"].mean().sort_values(ascending=False).head(6)`);
**GUGUR bila n_Off ≥ 2.** Kriteria-(b): median EV-per-trade-after-cost pool;
**GUGUR bila median ≤ 0.** Hasil: GUGUR (salah satu terpenuhi) / TAHAN
(keduanya negatif). Uji EV HANYA 6 jam tetap; uji pola HANYA top-6
hitung-ulang — menukar = shopping-jam, GAGAL total.

**S-H5 — level pada Q4-ATR × sesi vs placebo.** Grid TERTUTUP tepat 4 sel:
{hari Q4-ATR} × {London/Tokyo/NewYork/Sydney}, event round_xx00 SAJA,
window primer k=12 SAJA, komparator placebo_acak round_xx00 SAJA; +1 agregat
Q4-ALL deskriptif non-penentu. Placebo PERSIS nb04: seed 20261006; M5;
ATR(14) `.shift(1)`; theta 0.5×ATR; grid 0.5 xx.00; touch `low ≤ L ≤ high`;
direction `sign(close_{t-1}−L)`, lewati == 0; through/away `L −/+ d*theta`;
pindai t+1..t+24; tie/away-dulu/through-dulu/none; denom away+through;
hit = away/denom. Placebo_acak: `L' = L + U(5,25) pip`, tanda acak per
event, stream RNG sendiri seed 20261006, cari-maju penyentuh-genuine s/d 24,
buang direction==0, retensi dilaporkan. Dua stream RNG terpisah, keduanya
seed 20261006. **Penyimpangan satu konstanta pun = GAGAL-eksekusi.**
Spread dari `spread_pips` M1 langsung (audit deskriptif per sel, non-penentu).
Kuartil: cutoff_2024 = kuantil-0,75 `atr_14_d1` harian 2023; cutoff_2025 =
kuantil-0,75 atas 2023–2024; hari T Q4 bila `atr_14_d1(T−1) > cutoff`
(strict; tie → Q3). Metrik sel: `diff = HR_real − HR_plac`, CI95 + p
satu-sisi bootstrap paired-day (B=10.000, seed 20261006).
**Sel positif bila lolos Holm α=0,01 atas 4 p-value. TAHAN bila ≥ 1 sel
positif-Holm; GUGUR bila keempatnya gagal.**

**DAQ (mengikat):** evaluasi = date_broker 2024-01-01..2025-12-31 pool
tunggal; 2023 = seed-kuartil SAJA (H4: nol pemakaian); **2026 TIDAK MUNCUL
di tabel penentu maupun deskriptif mana pun.** H1/H2/H3 DILARANG
dibangkitkan dalam bentuk apa pun. Grain tunggal hari-broker;
`utc.normalize()` DILARANG. Sesi beku: Tokyo 9–18 Asia/Tokyo; London 8–16
Europe/London; NewYork 8–17 America/New_York; Sydney 8–16
Australia/Sydney; prioritas London>NewYork>Tokyo>Sydney (label M15 =
kolom beku store; M1/M5 = derivasi runtime resep beku + assert fingerprint,
mismatch = GAGAL-eksekusi). Satuan: pip untuk biaya; JPY untuk EV/ATR/SL/TP.

**S-B — 14 larangan (verbatim makna, lengkap):** (1) Vonis H1/H2/H3
DILARANG. (2) Cell-carving DILARANG (tepat 4 sel + 1 agregat).
(3) Hour-shopping DILARANG dua arah. (4) 2026-smuggling DILARANG.
(5) Threshold-peeking DILARANG (cutoff dihitung sekali sebelum evaluasi).
(6) FDR/unadjusted-multiple-looks DILARANG (satu-satunya koreksi sah =
Holm Q2). (7) Eksklusi buta DILARANG (jam-FLAT lapor-eksplisit;
direction==0 lewati + laporkan n-nya; burn-in = min_periods verbatim nb04,
dilaporkan). (8) Cabang biaya selain by_session DILARANG; satuan selain
pip→JPY-0.01 DILARANG. (9) Kalibrasi ulang apa pun DILARANG. (10) Guard
nilai-vs-diri DILARANG (klaim reproduksi/identik/join-gate WAJIB instrumen
exact atau toleransi eksplisit). (11) Output parsial berlabel proses-penuh
DILARANG. (12) Grain selain hari-broker DILARANG. (13) Menyentuh
file beku/lindung DILARANG (daftar C2 spec) = gagal total. (14) Mengubah
redaksi/ambang lock DILARANG kecuali addendum berversi arsitek.

**Gates S-C (tiap syarat + perintah mentah yang outputnya ditempel):**
C1 `git rev-parse HEAD` → `e0b2b9f…`. C2 SEBELUM/SESUDAH:
`git status --porcelain -uall -- src/ tests/ data/ configs/ reports/eda/ <daftar-C2>`
+ `find src tests data configs -type f -newermt "<timestamp-mulai>"` →
AFTER identik BEFORE dan find kosong (pola "output KOSONG" PENSIUN,
DILARANG dipakai). C3 `git hash-object` trio+D1/D2+Batch-1+builder +
`sha256sum` D4 (`47d15c41…`) + M15 (`cd6a85e4…`) + M1/M5 2024–2025
(`69b2c026/fce65a3a/da5e8944/a999a4bb`) + mtime tak berubah +
`git hash-object configs/data.yaml` + cost_basis cocok nilai-per-nilai +
fingerprint sesi cocok. C4 `pytest` penuh + `ruff check .` +
`ruff format --check .` + `python scripts/check_foreign_chars.py coder/hasil-lapisan3-H4H5.md`
→ N passed 0 fail/skip + All checks passed + formatted + OK asing,
masing-masing rc + cakupan ditempel (venv kanonik `venv/`).
C5 harness S-H4 + S-H5 masing-masing 2× → sha256 IDENTIK + `cmp` IDENTIK.
C6 P0+P1+E0+E1 ditempel [On] → GUGUR/TAHAN. C7 B0+B1+suplemen ditempel [On]
→ GUGUR/TAHAN. C8 `git hash-object coder/hasil-lapisan3-H4H5.md` SESUDAH
penulisan terakhir ditempel (contoh SALAH yang DILARANG: "pastikan hash
benar" tanpa output). C9 `git diff --cached --name-only` kosong +
`git log --oneline -1` tetap C1.
Skrip HANYA di `%TEMP%\opencode\l3h4h5` (tidak di-commit).
Provenans WAJIB exact-comparison atau toleransi eksplisit; sampel bersarang
WAJIB estimator paired + CI selaras alpha. Klaim tanpa output mentah = GAGAL.

Dokumen hasil WAJIB memuat tabel Klaim & Bukti (`.ai/AGENTS.md` §5) + semua
[On] bernomor bertaut angka; LF-only, ASCII murni. Selesai = serah-terima
6 item (hash hasil, HEAD, status, kriteria-a/b + sel/Holm, temuan DEV bila
ada, berkas). Nol commit.

## Disiplin tambahan (DISETUJUI user 2026-10-09, mengikat)

1. Manifest per nilai harness: tiap nilai operasional di harness
   berpasangan sumber (spec S/baris, lock, config); nilai tanpa sumber =
   GAGAL-eksekusi bila dipakai.
2. Kutip-balik presisi-penuh untuk konstanta pin; `git hash-object` tiap
   berkas sumber SEBELUM dipakai (tempel output).

=== SELF-AUDIT 3× ADVERSARIAL ===

**Putaran 1 — Correctness.** (a) Hash spec `4a46b815…` + HEAD `e0b2b9f…`
diukur asisten sesi ini via `git hash-object`/`git rev-parse` (bukti di
`verifications/2026-10-09_gerbang-spec-H4H5.md`). (b) Setiap angka di brief
disalin dari spec yang dibaca penuh 461 baris sesi ini (biaya Q3 `:124-127`;
strategi Q4 `:152-176`; placebo Q5 `:197-207`; kuartil `:212-216`; sesi
S0 `:36`; M2 S0 `:37`; kriteria S-H4 `:262-271`; S-H5 `:305-312`; C1–C9
`:329-337`; S-B `:349-384`). (c) Perintah .md + lokasi file eksplisit ada
(output `coder/hasil-lapisan3-H4H5.md`). (d) Tiap syarat C1–C9 punya pasangan
perintah mentah (Aturan 1 PROMPT_DISIPLIN). (e) Tidak ada pointer ke file
internal asisten; satu-satunya rujukan = `.ai/AGENTS.md` (kontrak bersama,
diizinkan).

**Putaran 2 — Bias & Asumsi.** (a) Brief tidak memuat vonis H4/H5 —
hanya GUGUR/TAHAN sebagai keluaran formula + putusan terpisah. (b) Tidak ada
rekomendasi metode dari asisten di substansi (Q1–Q5 milik arsitek,
disalin). (c) Penyederhanaan ("diringkas tanpa diubah maknanya") = risiko
parafrasa — dimitigasi: tiap butir menunjuk baris spec + angka kritis
disalin presisi-penuh; coder diwajibkan spec-menang bila berselisih.
(d) Frasa "pola Batch-1" / "preseden" tidak dipakai sebagai instruksi
(mandiri penuh).

**Putaran 3 — Meta-check.** (a) Brief mandiri: seluruh konstanta verbatim di
dalam, tanpa ketergantungan pada ingatan sesi. (b) Ruang coder tidak
diambil (tidak ada ambang baru; tidak ada pilihan desain tersisa —
semuanya diputus Q1–Q5). (c) Ruang auditor/arsitek tidak diambil (tidak ada
vonis; tidak ada audit angka primer). (d) Checklist §10: substansi dari
arsitek ✓; self-audit ada ✓; tambahan disetujui user 2026-10-09 dan
digabung eksplisit ✓; tanpa "menurut saya" ✓; angka persis dari spec
✓ (bukti baca: gerbang-spec-H4H5).

=== USULAN TAMBAHAN DARI ASISTEN — DISETUJUI user 2026-10-09, sudah digabung ke brief di atas ===

<item 1 — Manifest R-B1 per nilai harness> DISETUJUI, tergabung.
<item 2 — Kutip-balik presisi-penuh + bukti hash baca per berkas sumber> DISETUJUI, tergabung.
