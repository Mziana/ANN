# scripts/run.ps1
# Shortcut: aktifkan venv + jalankan pipeline menu.
# Cara: .\scripts\run.ps1

$root = Split-Path -Parent $PSScriptRoot
$activate = Join-Path $root "venv\Scripts\Activate.ps1"

if (-not (Test-Path $activate)) {
    Write-Host "GAGAL - venv belum ada. Jalankan setup dulu:" -ForegroundColor Red
    Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\setup.ps1" -ForegroundColor Cyan
    exit 1
}

& $activate
& (Join-Path $PSScriptRoot "pipeline.ps1")
