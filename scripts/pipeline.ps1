# scripts/pipeline.ps1
# Menu interaktif pipeline proyek USDJPY Bot.

$ErrorActionPreference = "Stop"

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  USDJPY Bot - Pipeline" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [DATA]" -ForegroundColor Yellow
    Write-Host "   1. Fetch data MT5 (raw)"
    Write-Host "   2. Clean data"
    Write-Host "   3. Validate data"
    Write-Host "   4. Resample ke TF lain"
    Write-Host ""
    Write-Host "  [FITUR & LABEL]" -ForegroundColor Yellow
    Write-Host "   5. Build features"
    Write-Host "   6. Build labels"
    Write-Host ""
    Write-Host "  [MODEL]" -ForegroundColor Yellow
    Write-Host "   7. Train baseline"
    Write-Host "   8. Train ANN"
    Write-Host ""
    Write-Host "  [BACKTEST]" -ForegroundColor Yellow
    Write-Host "   9. Backtest"
    Write-Host "  10. Audit strategi"
    Write-Host ""
    Write-Host "  [UTILITAS]" -ForegroundColor Yellow
    Write-Host "  11. Run tests"
    Write-Host "  12. Verify claims"
    Write-Host "  13. Check state"
    Write-Host "  14. Lihat log"
    Write-Host ""
    Write-Host "   0. Keluar" -ForegroundColor Red
    Write-Host ""
}

function Run-Python {
    param([string]$Script)
    if (-not (Test-Path $Script)) {
        Write-Host "  GAGAL: $Script belum ada." -ForegroundColor Red
        Read-Host "  Tekan Enter untuk lanjut"
        return
    }
    Write-Host "  Menjalankan: python $Script" -ForegroundColor Green
    python $Script
    Read-Host "  Selesai. Tekan Enter untuk lanjut"
}

while ($true) {
    Show-Menu
    $choice = Read-Host "  Pilih"

    switch ($choice) {
        "1"  { Run-Python "src/data/fetch_data.py" }
        "2"  { Run-Python "src/data/clean_data.py" }
        "3"  { Run-Python "src/data/validate_data.py" }
        "4"  { Run-Python "src/data/resample.py" }
        "5"  { Run-Python "src/features/build_features.py" }
        "6"  { Run-Python "src/features/build_labels.py" }
        "7"  { Run-Python "src/models/baseline.py" }
        "8"  { Run-Python "src/models/train_ann.py" }
        "9"  { Run-Python "src/backtest/backtest.py" }
        "10" { Run-Python "src/backtest/audit.py" }
        "11" { python -m pytest tests/ -v; Read-Host "  Enter untuk lanjut" }
        "12" { Run-Python "scripts/verify_claims.py" }
        "13" { Run-Python "scripts/check_state.py" }
        "14" {
            if (Test-Path "logs") {
                Get-ChildItem logs -Recurse -File | Select-Object -Last 10
            } else {
                Write-Host "  Belum ada log." -ForegroundColor Yellow
            }
            Read-Host "  Enter untuk lanjut"
        }
        "0"  { Write-Host "  Keluar." -ForegroundColor Cyan; break }
        default { Write-Host "  Pilihan tidak valid." -ForegroundColor Red; Start-Sleep 1 }
    }

    if ($choice -eq "0") { break }
}
