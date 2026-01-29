@echo off
echo ==========================================
echo       Medica Project Setup Script
echo ==========================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

:: Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
) else (
    echo [INFO] Virtual environment already exists.
)

:: Activate Venv and Install Requirements
echo [INFO] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Run Migrations
echo [INFO] Running database migrations...
python manage.py migrate

:: Final message
echo.
echo ==========================================
echo SETUP COMPLETE! You can now run the app.
echo Use start.bat to launch the server.
echo ==========================================
echo.
pause
