#!/usr/bin/env bash
# One-command setup + run for the Vega Market OWASP Top 10:2025 Black-Box Lab.
# Works on Linux and macOS. On Windows, use run.bat or run this via WSL.
set -e

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

if [ ! -d "venv" ]; then
  echo "==> Virtual muhit (venv) yaratilmoqda..."
  "$PYTHON_BIN" -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "==> Kutubxonalar o'rnatilmoqda..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "==> Ma'lumotlar bazasi tayyorlanmoqda..."
python manage.py migrate --noinput

echo "==> Namunaviy do'kon va lab flaglari yaratilmoqda (agar mavjud bo'lmasa)..."
python manage.py seed_lab

PORT="${PORT:-8000}"
echo ""
echo "=================================================================="
echo " Vega Market tayyor!  Brauzeringizda oching:  http://localhost:${PORT}"
echo " Progress paneli:                              http://localhost:${PORT}/lab/progress/"
echo "=================================================================="
echo ""

python manage.py runserver "0.0.0.0:${PORT}"
