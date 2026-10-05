# checkpoint_05_state_files.ps1
# Tulis state files: STATE, TASKS, PROGRESS, SESSION_LOG, CHECKPOINT_LOG
# Jalankan: powershell -ExecutionPolicy Bypass -File checkpoint_05_state_files.ps1

$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$aiDir = Join-Path $root ".ai"

if (-not (Test-Path $aiDir)) { New-Item -ItemType Directory -Path $aiDir -Force | Out-Null }

Write-Host "Menulis state files di: $aiDir" -ForegroundColor Cyan

# 1. STATE.md
$stateMd = @'
# STATE.md — Status Saat Ini

**Update terakhir:** 2026-10-05
**Fase:** Setup Fondasi (Fase 0)
**Progress keseluruhan:** ~40%

## Yang Sedang Dikerjakan
- Setup struktur proyek & aturan AI agent.

## Yang Sudah Selesai
- [x] Checkpoint 01: Struktur folder
- [x] Checkpoint 05: State files

## Yang Belum
- [ ] Checkpoint 06: scripts
- [ ] Checkpoint 07: configs
- [ ] Checkpoint 08: setup.ps1
- [ ] Checkpoint 09a-09d: final files
- [ ] Fetch data MT5
- [ ] EDA
- [ ] Pilih metode

## Blocker
- Belum jalankan checkpoint 06-09d.

## Langkah Berikutnya
1. Jalankan Checkpoint 06.
2. Lanjut 07, 08, 09a-09d.
3. Setup environment.
4. git init.
5. Fetch data MT5.
'@
$stateMd | Out-File -FilePath (Join-Path $aiDir "STATE.md") -Encoding UTF8
Write-Host "  [+] STATE.md" -ForegroundColor Green

# 2. TASKS.md
$tasksMd = @'
# TASKS.md — Task Board

**Update terakhir:** 2026-10-05

## In Progress
- [ ] Checkpoint 05-09d

## Todo (Prioritas Tinggi)
- [ ] Checkpoint 06: scripts
- [ ] Checkpoint 07: configs
- [ ] Checkpoint 08: setup
- [ ] Checkpoint 09a-09d: final files
- [ ] Setup environment (scripts/setup.ps1)
- [ ] git init + pre-commit install

## Todo (Prioritas Sedang)
- [ ] Verifikasi nama simbol MT5 Finex
- [ ] Verifikasi timezone broker

## Done (7 hari terakhir)
- [x] Checkpoint 01: Struktur folder (2026-10-05)
- [x] Checkpoint 05: State files (2026-10-05)

## Blocked
- [ ] Fetch data MT5 - nunggu setup selesai
'@
$tasksMd | Out-File -FilePath (Join-Path $aiDir "TASKS.md") -Encoding UTF8
Write-Host "  [+] TASKS.md" -ForegroundColor Green

# 3. PROGRESS.md
$progressMd = @'
# PROGRESS.md — Milestone

**Update terakhir:** 2026-10-05

## Milestone 0: Setup Fondasi (40%)
- [x] Struktur folder
- [x] State files
- [ ] Scripts
- [ ] Configs
- [ ] Setup.ps1
- [ ] AGENTS.md v3.0
- [ ] RULES.md v2.0
- [ ] PROMPTS.md v2.0
- [ ] CONTEXT.md v1.2
- [ ] Configs final + jurnal + backtest

## Milestone 1: Data Pipeline
- [ ] Fetch data MT5 (M1-M15)
- [ ] Clean data
- [ ] Validate data
- [ ] Simpan Parquet

## Milestone 2: Eksplorasi (EDA)
- [ ] Distribusi return
- [ ] Volatilitas per sesi
- [ ] Karakter per regime

## Milestone 3: Metode
- [ ] Hipotesis dari EDA
- [ ] Uji kandidat
- [ ] Pilih metode

## Milestone 4: Baseline Model
- [ ] Rule-based
- [ ] Logistic regression

## Milestone 5: ANN
- [ ] MLP
- [ ] Walk-forward

## Milestone 6: Backtest
- [ ] Spread + slippage + komisi
- [ ] Stress test

## Milestone 7: Paper Trading (Fase 1)
- [ ] 500+ trade data

## Milestone 8: Graduation (Fase 2)
- [ ] 100 trade simulasi limit

## Milestone 9: Live (Fase 3)
- [ ] Modal kecil
'@
$progressMd | Out-File -FilePath (Join-Path $aiDir "PROGRESS.md") -Encoding UTF8
Write-Host "  [+] PROGRESS.md" -ForegroundColor Green

# 4. SESSION_LOG.md
$sessionLogMd = @'
# SESSION_LOG.md — Log Sesi

## Sesi 2026-10-05 — Setup Fondasi

**Fokus:** Struktur folder + state files.

**Selesai:**
- Checkpoint 01: Struktur folder
- Checkpoint 05: State files

**Belum:**
- Checkpoint 06-09d
- Setup environment
- Git init

**Catatan:**
- User pakai Freebuff + Hermes + DeepSeek V4.
- Proyek di D:\ANN.
- Metode strategi belum dipilih (tunggu EDA).

**Langkah berikutnya:**
- Jalankan Checkpoint 06.
'@
$sessionLogMd | Out-File -FilePath (Join-Path $aiDir "SESSION_LOG.md") -Encoding UTF8
Write-Host "  [+] SESSION_LOG.md" -ForegroundColor Green

# 5. CHECKPOINT_LOG.md
$checkpointLogMd = @'
# CHECKPOINT_LOG.md — Log Checkpoint

## Checkpoint 05 — 2026-10-05
- Tulis STATE.md, TASKS.md, PROGRESS.md, SESSION_LOG.md.
- Tulis file ini.

## Checkpoint 01 — 2026-10-05
- Buat struktur folder lengkap (~50 folder).
- File placeholder + .gitkeep.
- .gitignore.
'@
$checkpointLogMd | Out-File -FilePath (Join-Path $aiDir "CHECKPOINT_LOG.md") -Encoding UTF8
Write-Host "  [+] CHECKPOINT_LOG.md" -ForegroundColor Green

Write-Host ""
Write-Host "Checkpoint 05 SELESAI." -ForegroundColor Cyan
Write-Host "File di .ai\ :" -ForegroundColor Yellow
Get-ChildItem $aiDir | Select-Object Name