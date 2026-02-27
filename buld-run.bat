@echo off
REM ========================
REM Build and Run Script
REM ========================

REM Go to your project folder
cd /d "C:\Users\muthukumaran\New folder"

echo 🔨 Building EXE...
python -m PyInstaller --onefile --windowed --icon=app.ico mk.py

echo.
echo ✅ Build complete! Launching app...

REM Go to dist folder and run the exe
cd dist
start mk.exe

echo.
echo App is running! Press any key to close this window.
pause >nul
