@echo off
title AgriTwin AI Local Server
echo ===================================================
echo   AgriTwin AI - Digital Twin Pertanian Padi
echo ===================================================
echo.

if not exist .venv (
    echo [!] Virtual environment (.venv) belum ditemukan.
    echo [+] Membuat virtual environment baru...
    python -m venv .venv
    echo [+] Menginstal dependensi dari requirements.txt...
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo [+] Menjalankan AgriTwin AI Server di http://localhost:5000
echo [+] Tekan Ctrl+C di terminal ini untuk menghentikan server.
echo.
python app.py
pause
