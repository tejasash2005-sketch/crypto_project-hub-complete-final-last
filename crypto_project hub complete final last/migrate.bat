@echo off
TITLE CryptoHub Migrations
echo ======================================================
echo    CRYPTOHUB - DATABASE MIGRATIONS
echo ======================================================
echo.

:: Navigate to the Django project directory
cd /d "%~dp0crypto_project"

echo [1/2] Creating migrations...
python manage.py makemigrations

echo [2/2] Applying migrations...
python manage.py migrate

echo.
echo ======================================================
echo    Migrations completed successfully!
echo ======================================================
pause
