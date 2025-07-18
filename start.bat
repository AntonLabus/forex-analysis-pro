@echo off
echo.
echo ================================================================
echo              Forex Analysis Pro - Startup Script
echo ================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    echo Please install pip or reinstall Python
    pause
    exit /b 1
)

echo Python installation detected...
echo.

:: Install requirements if they don't exist
echo Checking Python dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
    echo.
) else (
    echo Dependencies already installed.
    echo.
)

:: Create database if it doesn't exist
if not exist "forex_data.db" (
    echo Creating database...
    python -c "from backend.database import create_tables; create_tables()"
    echo Database created successfully!
    echo.
)

:: Start the application
echo Starting Forex Analysis Pro...
echo.
echo The application will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================================
echo.

python app.py

pause
