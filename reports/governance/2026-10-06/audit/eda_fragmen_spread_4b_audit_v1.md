# Audit Fragmen Spread (Revisi 4b) — v1

**Tanggal:** 2026-10-06 · **Auditor:** Klenz (adversarial) · **Objek:** `reports/eda/2026-10-06/spread_fragment.yaml` + laporan 4b + `configs/data.yaml` + `eda_02_volatility.ipynb`
**Dasar aturan:** AGENTS §20 (anti-halusinasi), §21 (empiris), RULES §13 (dependency + CHANGELOG)

## Ringkasan
- **Jumlah temuan:** 8 (0 CRITICAL, 0 HIGH, 3 MEDIUM, 5 LOW)
- **Verdict:** **LULUS DENGAN CATATAN** — angka fragmen 100% valid (verifikasi independen dari parquet); laporan & proses butuh perbaikan sebelum commit.

## Verifikasi angka (fragment vs hitungan auditor dari `broker_time_raw`/parquet, strata A, label primer DST-aware)

| Angka | Fragmen | Verifikasi | Cocok |
|---|---|---|---|
| Strata A/B/C | 1.136.401 / 185.248 / 26.198 | persis | ✓ |
| cost_basis.default | 0,65 | 0,6456→0,65 | ✓ |
| cost_basis.by_year | 0,51 / 0,70 / 0,67 / 0,62 | 0,5095 / 0,7029 / 0,6735 / 0,6218 | ✓ |
| cost_basis.by_session | 0,61 / 0,69 / 0,62 / 0,80 | 0,6076 / 0,6924 / 0,6151 / 0,7959 | ✓ |
| stress p95 default/by_year | 1,0 · 0,6/1,2/1,0/0,7 | persis | ✓ |
| stress p95 by_session | 0,8/1,2/0,9/1,5 | persis | ✓ |
| p99 default/by_year | 1,6 · 1,1/1,7/1,7/1,1 | persis | ✓ |
| Off strata A | 0 bar | 0 ✓ ("MEAN tak terdefinisi" valid) | ✓ |
| Off semua data | 2.894 = 0,2147% | persis | ✓ |
| by_year[2023] config | tetap 3,0 | diff = 0 baris nilai (hanya komentar) | ✓ |
| pip_size config | dict utuh | {USDJPY: 0.01, default: 0.0001} | ✓ |

**Dua penyimpangan yang diklaim coder — keduanya terverifikasi valid:** Off di-exclude dari by_session (0 bar di A — memasang nilai = mengarang); kunci `NewYork` (konsisten `SESSION_ORDER` nb00/`_eda_common.py:38`).

## Temuan
- **[MEDIUM-26]** Klaim SA-24 coder SALAH: `check_foreign_chars` justru memindai YAML (`SCANNED_SUFFIXES` ∋ `.yaml/.yml`; hook `files:` ∋ `ya?ml`; diskonfirmasi dengan eksekusi langsung). Yang lolos adalah token **ASCII** — di luar cakupan blok skrip asing oleh desain. Diagnosis "cacat proses YAML" = asumsi tanpa verifikasi (§20); koreksi narasi sebelum memblokir keputusan user.
- **[MEDIUM-27]** SA-25 TERBUKTI: `scipy==1.17.1`, `matplotlib==3.10.9`, `nbformat==5.11.1` ditambahkan ke requirements (uncommitted) TANPA entri CHANGELOG → RULES §13. Isi benar, versinya cocok venv; fix dokumen.
- **[MEDIUM-28]** Semantik penerapan fragmen tidak didefinisikan (merge vs replace; kunci `cost_basis`/`stress_bands` bukan bagian blok `spread` config) + `pip_size` fragmen tanpa `default: 0.0001`. Safety net ada (pytest), tapi jalur penerapan harus ditulis eksplisit.
- **[LOW-26]** Laporan menyebut "16/16 assertion" — aktual notebook tersimpan: **20/20** (pasca +5 assertion SA-23).
- **[LOW-27]** Typo/fragmen kalimat: fragment:1 "DITERAPKAN" (= LOW-27.1), laporan "baru,menjelaskan" (27.2), laporan tahap-4:65 kalimat menggantung (27.3).
- **[LOW-28]** HEAD sudah bergeser (1e42bd1→a63d117→9a60995) sebelum ronde 4b; klaim "tanpa commit" hanya valid relatif baseline ronde ini.
- **[LOW-29]** Line ending: working copy LF; warning CRLF git = artefak normalisasi checkout, bukan pelanggaran.
- **[LOW-30]** Rasio 8,83× (5,30/0,60) benar; dua rasio terlapor (8,83× vs 5,30×) tidak kontradiktif.

## Gate (dijalankan auditor)
pytest **157 passed** · ruff check/format bersih · validate_data exit 0 (2/2/1/1) · nb02 20/20 PASS + 0 error output · check_foreign_chars exit 0 · HEAD 9a60995, 4b uncommitted.

## Verdict & kesiapan terapkan
Fragmen (angka): **VALID**. Siap terapkan ke config: **Belum** — prosedural: (1) jalur merge eksplisit (MEDIUM-28), (2) CHANGELOG dep EDA (MEDIUM-27), (3) koreksi SA-24 (MEDIUM-26). Keputusan otoritas `cost_basis.default 0,65` vs `spread.default 1,5` tetap milik user; sampai diterapkan, config lama yang dibaca `check_spread`.

*Catatan pascaterbit: LOW-27.1 direvisi (MODIFIKASI) — lihat `eda_fragmen_spread_audit_revisi_LOW-27.1.md`. MEDIUM-26/27/28 + LOW-26/27.2/27.3 dieksekusi coder dan terverifikasi di ronde berikutnya; fragmen kini berstatus DITERAPKAN (sub-kunci baru, blok lama utuh) sesuai Lampiran A2.*
