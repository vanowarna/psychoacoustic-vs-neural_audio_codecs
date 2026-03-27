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
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3 -m venv .venv
    ) else (
        python -m venv .venv
    )
)
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Failed to create .venv. Ensure Python 3 is installed and that the venv module is available.
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
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip
    popd
    exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies from requirements.txt
    popd
    exit /b 1
)

echo === Running traditional coding sweep ===
python scripts\traditional-coding-sweep.py

echo === Running neural coding sweep ===
python scripts\neural-coding-sweep.py

echo === Running objective evaluation ===
python scripts\objective-evaluation.py

echo === All steps completed ===

popd
endlocal
