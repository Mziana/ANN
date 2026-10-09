# Laporan Tahap 1 — Pin Dependensi (`tzdata` + `MetaTrader5`)
**Tanggal:** 2026-10-06 (verifikasi ulang 2026-10-06 10:11)
**Status:** SELESAI — sudah **ter-commit** (`9a60995`); gate hijau

> Catatan metodologi: semua angka di laporan ini **diverifikasi ulang** pada sesi penulisan
> (pytest, ruff, validate_data, requirements.txt, isi commit). Laporan_step_1 sebelumnya hanya
> ada di `SESSION_LOG.md`; file ini adalah deliverable `.md` per tahap sesuai kontrak.

## 1. Tujuan
Tambahkan dependensi baru yang disetujui user untuk menjalankan EDA v3 di Windows: `tzdata==2026.5` (agar `zoneinfo` punya database zona waktu di OS tanpa DB sistem), plus pin `MetaTrader5` ke versi terpasang. Semua sesuai RULES §13 (izin user + pin versi + update CHANGELOG).

## 2. File yang Dibuat/Diubah
Commit tunggal `9a60995` — 5 file, +120 / −7 baris:
- `requirements.txt` — tambah `tzdata==2026.5`, pin `MetaTrader5==5.0.6231`.
- `CHANGELOG.md` — catat penambahan (RULES §13).
- `.ai/STATE.md`, `.ai/TASKS.md`, `.ai/SESSION_LOG.md` — dokumentasi + aturan baru "upgrade venv wajib update requirements di commit yang sama".

Tidak ada kode produksi (`src/`) yang disentuh.

## 3. Apa yang Dilakukan
1. Verifikasi versi terpasang: `tzdata==2026.5`, `MetaTrader5==5.0.6231`.
2. Tambah pin eksplisit + komentar alasan di `requirements.txt`.
3. Update `CHANGELOG.md` sesuai RULES §13.
4. Jalankan gate penuh di venv kanonik (`venv/`): pytest, ruff check, ruff format, `validate_data`.
5. Commit tunggal `chore(deps): ...`.

## 4. Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| `tzdata==2026.5` terpasang di venv kanonik | TERVERIFIKASI | `importlib.metadata.version('tzdata')` = `2026.5` |
| `requirements.txt` pin `tzdata==2026.5` | TERVERIFIKASI | baris 9 (dengan komentar pin eksplisit, RULES §13) |
| `requirements.txt` pin `MetaTrader5==5.0.6231` | TERVERIFIKASI | baris 17 |
| `MetaTrader5` terpasang = 5.0.6231 | TERVERIFIKASI | `importlib.metadata.version('MetaTrader5')` = `5.0.6231` |
| `pyarrow==17.0.0` sinkron antara requirements dan venv | TERVERIFIKASI | requirements baris 8 = `17.0.0`; `version('pyarrow')` = `17.0.0` |
| `pip install -r requirements.txt` = no-op | TERVERIFIKASI (dari catatan sesi; **tidak diulang** hari ini) | semua "already satisfied", exit 0 |
| Gate: pytest **157 passed**, exit 0 | TERVERIFIKASI | `python -m pytest tests/ -q` → `157 passed in 1.38s`, `pytest_exit=0` |
| Gate: ruff check bersih | TERVERIFIKASI | `ruff check src/ tests/` → `All checks passed!`, exit 0 |
| Gate: ruff format --check bersih | TERVERIFIKASI (dari catatan sesi; **tidak diulang** hari ini) | "14 files already formatted"; tidak diulang karena tidak ada `.py` berubah |
| Gate: `validate_data` exit 0, 0 error | TERVERIFIKASI | `python -m src.data.validate_data` → `validate_data_exit=0` |
| Peringatan `validate_data` per tahun = 2 / 2 / 1 / 1 | TERVERIFIKASI | 2023: 2, 2024: 2, 2025: 1, 2026: 1 (semua "LOLOS", 0 error) |
| Commit tunggal, pesan `type(scope):` | TERVERIFIKASI | `git show 9a60995` → `chore(deps): pin tzdata==2026.5 + MetaTrader5==5.0.6231` |
| Tidak ada file `.py` produksi berubah → pytest tidak perlu diulang setelah commit | TERVERIFIKASI | `git show --stat` hanya requirements/CHANGELOG/`.ai/*.md` |

## 5. Self-Audit Adversarial

### Checklist
- [x] Dependency ditambah **dengan izin** (disetujui user), **di-pin** versi, **CHANGELOG** diupdate (RULES §13).
- [x] Gate dijalankan di venv kanonik yang benar (`venv/`, bukan `.venv/`).
- [x] Exit status tiap gate di-preserve (bukan hanya output yang difilter).
- [x] Tidak ada kode produksi berubah; tidak ada dependensi lain yang di-drag.

### Temuan

- **[SA-01] "pip install -r requirements.txt = no-op" tidak diulang hari ini.** Dikuatkan secara
  tidak langsung: seluruh versi requirements yang dicek (tzdata, pyarrow, MetaTrader5) cocok dengan
  versi terpasang. Status: **tidak diulang** (lihat §6).

- **[SA-02] Klaim "pandas 3.0.6 di `.venv`" dihitung sebagai env bantu, bukan regresi.** `.venv/`
  sengaja **dibiarkan** di disk (keputusan user) dan **tidak dipakai** untuk gate. Konsekuensi yang
  harus diingat: menjalankan notebook dengan interpreter salah akan memakai pandas 3.x dan
  mengulang kelas bug `.asi8`/`as_unit("ns")` yang dulu menangkap pipeline (lihat SESSION_LOG
  2026-10-05). **Mitigasi wajib:** seluruh notebook EDA harus dijalankan dengan
  `venv/Scripts/python.exe`, bukan `.venv`. Notebook 00 memang dijalankan di venv kanonik
  (terbukti dari versi pandas 2.2.3 di sysinfo notebook).

- **[SA-03] Angka peringatan gate sebelumnya pernah jadi sumber salah ketik historik.**
  Sudah diverifikasi ulang di sini dan **benar** (2 / 2 / 1 / 1).

## 6. Yang Belum Diverifikasi
- `pip install -r requirements.txt` no-op exit 0 — **tidak diulang** hari ini (didukung kuat oleh
  pencocokan versi).
- `jupyter` / `ipykernel` masih terpasang & versi cocok — **tidak diulang** hari ini.
- Test `pre-commit run --all-files` 12/12 — **tidak diulang** hari ini (gate commit sudah hijau saat
  commit; tidak ada file `.py`/hook yang berubah sejak itu).

## 7. Potensi Masalah
- Dua venv berdampingan (SA-02) adalah sumber kesalahan lingkungan paling mungkin untuk sesi
  berikutnya. Rekomendasi: runbook eksplisit "pakai venv kanonik" sudah ada di STATE.md; tidak ada
  perubahan kode yang saya lakukan di sini (di luar scope Langkah 1).
- Tidak ada blocking issue.

## 8. Langkah Berikutnya
- Langkah 1 selesai & ter-commit. Lanjut ke Langkah 2 (notebook 00) — **sudah selesai**, lihat
  `laporan_tahap_2_nb00_setup.md`.
- Berikutnya yang menunggu persetujuan: **Langkah 3** (`eda_01_returns.ipynb`, Q1 return).

## 9. STOP — Tunggu Review User
