# Quick Setup Script for Python 3.12
# Run this after installing Python 3.12

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Insurance Agent - Python 3.12 Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Python 3.12 is available
Write-Host "Checking for Python 3.12..." -ForegroundColor Yellow
$python312 = py -3.12 --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Python 3.12 not found!" -ForegroundColor Red
    Write-Host "`nPlease install Python 3.12 from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/release/python-3120/`n" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ Found: $python312`n" -ForegroundColor Green

# Remove old venv
Write-Host "Removing old virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv
    Write-Host "✅ Old venv removed`n" -ForegroundColor Green
}

# Create new venv with Python 3.12
Write-Host "Creating new virtual environment with Python 3.12..." -ForegroundColor Yellow
py -3.12 -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Failed to create virtual environment!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created`n" -ForegroundColor Green

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "`nInstalling requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Failed to install requirements!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ All packages installed successfully!`n" -ForegroundColor Green

# Test the installation
Write-Host "Testing Google Generative AI..." -ForegroundColor Yellow
python -c "import google.generativeai as genai; print('✅ google-generativeai works!')"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Make sure GEMINI_API_KEY is set in .env" -ForegroundColor White
Write-Host "2. Run: python main.py" -ForegroundColor White
Write-Host "3. Open: http://localhost:5173`n" -ForegroundColor White
