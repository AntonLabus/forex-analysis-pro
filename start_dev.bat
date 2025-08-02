@echo off
echo ============================================================
echo          Forex Analysis Pro - Development Mode
echo ============================================================

echo Setting up development environment...

REM Set environment variables for development
set FLASK_ENV=development
set DEBUG=True

echo Development environment configured.

REM Check Python version
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Python version check passed.

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing Python dependencies...
    pip install -r requirements.txt > nul 2>&1
    if %errorlevel% neq 0 (
        echo WARNING: Some dependencies may have failed to install
    ) else (
        echo Dependencies installed successfully.
    )
) else (
    echo No requirements.txt found - skipping dependency installation.
)

REM Create database if it doesn't exist
if not exist forex_analysis.db (
    echo Creating database...
    python -c "import sqlite3; sqlite3.connect('forex_analysis.db').close()"
    echo Database created.
) else (
    echo Database already exists.
)

echo ============================================================
echo          Forex Analysis Pro - Starting Development Server
echo ============================================================
echo.
echo The application will be available at: http://localhost:5000
echo Emergency mode bypass is ENABLED for development
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================

REM Start the Flask development server
python app.py

pause
