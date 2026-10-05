@echo off
REM Wrapper for pre-commit local hooks.
REM
REM Alasan file ini ada (2026-10-05):
REM - `language: system` + `python` memakai Python 3.14 dari PATH (pandas 3.0.3)
REM   yang tidak punya pyarrow, sehingga 2 tes parquet selalu gagal.
REM - Path relatif `venv/Scripts/python.exe` sebagai entry TIDAK bisa: Windows
REM   CreateProcess tidak meresolve program relatif (WinError 2).
REM - Path absolut tidak boleh: tidak portabel antar mesin.
REM - `language: python_system` baru ada di pre-commit 4.0; project ini 3.8.0.
REM
REM cmd.exe me-resolve path relatif terhadap direktori kerja, dan pre-commit
REM selalu menjalankan hook dari root repo. Jadi bentuk di bawah portabel.
REM
REM Pemakaian: scripts\run_hook.bat scripts\nama_script.py [args...]
setlocal
venv\Scripts\python.exe %*
exit /b %ERRORLEVEL%
