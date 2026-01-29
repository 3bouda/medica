@echo off
echo ==========================================
echo       Starting Medica Application
echo ==========================================
echo.

if not exist "venv" (
    echo [ERROR] Virtual environment (venv) not found.
    echo Please run setup.bat first!
    pause
    exit /b
)

echo [INFO] Activating environment and starting server...
call venv\Scripts\activate
python manage.py runserver

pause
