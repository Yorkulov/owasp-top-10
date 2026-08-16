@echo off
REM One-command setup + run for the Vega Market OWASP Top 10:2025 Black-Box Lab (Windows).
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
  echo Python topilmadi. Avval Python 3.11+ ni python.org dan o'rnating.
  exit /b 1
)

if not exist venv (
  echo ==^> Virtual muhit ^(venv^) yaratilmoqda...
  python -m venv venv
)

call venv\Scripts\activate.bat

echo ==^> Kutubxonalar o'rnatilmoqda...
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ==^> Ma'lumotlar bazasi tayyorlanmoqda...
python manage.py migrate --noinput

echo ==^> Namunaviy do'kon va lab flaglari yaratilmoqda...
python manage.py seed_lab

if "%PORT%"=="" set PORT=8000

echo.
echo ==================================================================
echo  Vega Market tayyor!  Brauzeringizda oching:  http://localhost:%PORT%
echo  Progress paneli:                              http://localhost:%PORT%/lab/progress/
echo ==================================================================
echo.

python manage.py runserver 0.0.0.0:%PORT%
