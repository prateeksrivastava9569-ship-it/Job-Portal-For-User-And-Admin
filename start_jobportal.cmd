@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE=%~dp0..\.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

netstat -ano | findstr ":8000" >nul
if not errorlevel 1 (
    echo Site already running on http://127.0.0.1:8000
    exit /b 0
)

start "Job Portal" "%PYTHON_EXE%" manage.py runserver 0.0.0.0:8000

echo Starting Job Portal on http://127.0.0.1:8000
