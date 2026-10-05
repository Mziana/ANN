# scripts/setup.ps1
# Setup environment proyek USDJPY Bot. Jalankan SEKALI.
# Cara: powershell -ExecutionPolicy Bypass -File scripts/setup.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Environment - USDJPY Bot" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Cek Python
Write-Host "[1/6] Cek Python..." -ForegroundColor Yellow
try {
    $pyVersion = py -3.12 --version 2>&1
    Write-Host "      OK - $pyVersion" -ForegroundColor Green
    $versionNum = ($pyVersion -split " ")[1]
    $major = [int]($versionNum -split "\.")[0]
    $minor = [int]($versionNum -split "\.")[1]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
        Write-Host "      GAGAL - Python 3.11+ dibutuhkan." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "      GAGAL - Python tidak ditemukan di PATH." -ForegroundColor Red
    Write-Host "      Install Python 3.11+ dari https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 2. Buat venv
Write-Host "[2/6] Buat virtual environment..." -ForegroundColor Yellow
$venvPath = Join-Path $root "venv"
if (Test-Path $venvPath) {
    Write-Host "      INFO - venv/ sudah ada, skip" -ForegroundColor DarkYellow
} else {
    py -3.12 -m venv $venvPath
    Write-Host "      OK - venv/ dibuat" -ForegroundColor Green
}

# 3. Aktifkan venv & upgrade pip
Write-Host "[3/6] Aktifkan venv & upgrade pip..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "      GAGAL - Activate.ps1 tidak ditemukan" -ForegroundColor Red
    exit 1
}
& $activateScript
py -3.12 -m pip install --upgrade pip --quiet
Write-Host "      OK - pip upgraded" -ForegroundColor Green

# 4. Install dependencies
Write-Host "[4/6] Install dependencies..." -ForegroundColor Yellow
$reqPath = Join-Path $root "requirements.txt"
if (-not (Test-Path $reqPath)) {
    Write-Host "      GAGAL - requirements.txt tidak ada" -ForegroundColor Red
    exit 1
}
Write-Host "      (ini bisa 3-10 menit pertama kali)" -ForegroundColor DarkGray
pip install -r $reqPath
Write-Host "      OK - dependencies installed" -ForegroundColor Green

# 5. Pre-commit
Write-Host "[5/6] Install pre-commit hooks..." -ForegroundColor Yellow
$gitDir = Join-Path $root ".git"
if (-not (Test-Path $gitDir)) {
    Write-Host "      INFO - Git belum di-init. Jalankan:" -ForegroundColor DarkYellow
    Write-Host "             git init" -ForegroundColor Cyan
    Write-Host "             pre-commit install" -ForegroundColor Cyan
} else {
    pre-commit install
    Write-Host "      OK - pre-commit hooks installed" -ForegroundColor Green
}

# 6. Verifikasi
Write-Host "[6/6] Verifikasi instalasi..." -ForegroundColor Yellow
Write-Host ""
python -c "import pandas; print(f'  pandas: {pandas.__version__}')"
python -c "import numpy; print(f'  numpy: {numpy.__version__}')"
python -c "import pyarrow; print(f'  pyarrow: {pyarrow.__version__}')"
python -c "import torch; print(f'  torch: {torch.__version__}')"
python -c "import yaml; print(f'  pyyaml: {yaml.__version__}')"
python -c "import pytest; print(f'  pytest: {pytest.__version__}')"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup SELESAI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Langkah berikutnya:" -ForegroundColor Yellow
Write-Host "  1. Aktifkan venv: .\venv\Scripts\Activate.ps1"
Write-Host "  2. git init"
Write-Host "  3. pre-commit install"
Write-Host "  4. .\scripts\run.ps1"
Write-Host ""
