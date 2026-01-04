@echo off
echo Starting Desktop Widget...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Check if Pillow is installed
python -c "import PIL" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing Pillow library...
    python -m pip install pillow
)

REM Run the desktop widget application
python main.py

REM If the application exits with an error, pause to see the error message
if %ERRORLEVEL% neq 0 (
    echo Application exited with an error.
    pause
)