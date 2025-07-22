@echo off
echo Starting Kalashnikoff Site...
echo.

REM Check if Python is installed
py -3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

echo Installing dependencies...
py -3 -m pip install Django channels daphne

echo Running migrations...
py -3 manage.py migrate

echo Starting server...
echo.
echo 🌐 Landing page: http://127.0.0.1:8080/
echo 💬 IRC Client: http://127.0.0.1:8080/irc/
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Run the development server
py -3 manage.py runserver 127.0.0.1:8080

pause
