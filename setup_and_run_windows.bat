@echo off
setlocal enabledelayedexpansion

pushd "%~dp0"

echo === Checking ffmpeg ===
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ffmpeg is required but not found in PATH.
    echo Install from https://ffmpeg.org/download.html or via:
    echo   choco install ffmpeg   ^(Chocolatey^)
    echo   winget install --id Gyan.FFmpeg
    popd
    exit /b 1
)

echo === Creating virtual environment (if needed) ===
if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv || python -m venv .venv
)
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Failed to create .venv
    popd
    exit /b 1
)

echo === Activating virtual environment ===
call ".venv\Scripts\activate.bat" || (
    echo [ERROR] Failed to activate .venv
    popd
    exit /b 1
)

echo === Installing Python dependencies ===
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo === Running traditional coding sweep ===
python scripts\traditional-coding-sweep.py

echo === Running neural coding sweep ===
python scripts\neural-coding-sweep.py

echo === Running objective evaluation ===
python scripts\objective-evaluation.py

echo === All steps completed ===

popd
endlocal
