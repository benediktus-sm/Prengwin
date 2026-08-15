Write-Host "===================================================" -ForegroundColor Green
Write-Host "  AgriTwin AI - Digital Twin Pertanian Padi" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""

if (-not (Test-Path ".venv")) {
    Write-Host "[!] Virtual environment (.venv) belum ditemukan." -ForegroundColor Yellow
    Write-Host "[+] Membuat virtual environment baru..." -ForegroundColor Cyan
    python -m venv .venv
    Write-Host "[+] Menginstal dependensi..." -ForegroundColor Cyan
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        & .\.venv\Scripts\Activate.ps1
    }
    python -m pip install -r requirements.txt
} else {
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        & .\.venv\Scripts\Activate.ps1
    }
}

Write-Host ""
Write-Host "[+] Menjalankan AgriTwin AI Server di http://localhost:5000" -ForegroundColor Green
Write-Host "[+] Tekan Ctrl+C untuk menghentikan server." -ForegroundColor Yellow
Write-Host ""
python app.py
