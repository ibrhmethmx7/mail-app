@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi.
    echo Lutfen https://www.python.org/downloads/ adresinden Python yukleyin (kurulumda "Add Python to PATH" isaretli olsun).
    pause
    exit /b 1
)
python gui_app.py
if errorlevel 1 pause
