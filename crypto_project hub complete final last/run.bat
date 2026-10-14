@echo off
TITLE CryptoHub Server
echo ======================================================
echo    CRYPTOHUB - SECURE LEARNING PLATFORM
echo ======================================================
echo.

:: Navigate to the Django project directory
cd /d "%~dp0crypto_project"

:: Attempt to install requirements if Django is missing
echo [0/3] Checking dependencies...
python -c "import django" 2>nul
if %errorlevel% neq 0 (
    echo Django not found. Installing requirements...
    pip install -r requirements.txt
)

:: Check for database migrations
echo [1/3] Syncing database...
python manage.py migrate

:: Launch the browser automatically
echo [2/3] Launching local server at http://127.0.0.1:8000
start "" "http://127.0.0.1:8000"

:: Start the Django development server
echo [3/3] Starting Django server...
echo.
python manage.py runserver

pause
