@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
title AI Pathfinder - Setup and Launch

echo ============================================
echo   AI Pathfinder Visualizer - Windows Setup
echo ============================================
echo.

echo [1/4] Checking for Python...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python was not found on your PATH.
    echo         Install Python 3.10+ from https://www.python.org/downloads/
    echo         Tick "Add Python to PATH" during installation.
    pause
    exit /b 1
)
FOR /F "tokens=*" %%v IN ('python --version 2^>^&1') DO SET PYVER=%%v
echo [OK] Found: %PYVER%
echo.

echo [2/4] Checking for Poetry...
poetry --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [INFO] Poetry not found. Installing via pip...
    pip install poetry --quiet
    poetry --version >nul 2>&1
    IF ERRORLEVEL 1 (
        echo [ERROR] Poetry installation failed.
        echo         Install manually: https://python-poetry.org/docs/#installation
        pause
        exit /b 1
    )
)
FOR /F "tokens=*" %%v IN ('poetry --version 2^>^&1') DO SET POETRYVER=%%v
echo [OK] Found: %POETRYVER%
echo.

echo [3/4] Installing project dependencies...
poetry install
IF ERRORLEVEL 1 (
    echo [ERROR] Dependency installation failed.
    echo         Check your pyproject.toml or network connection.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.
echo.

echo [4/4] Launching AI Pathfinder Visualizer...
echo.
poetry run python src/ai_path_finder/main.py

IF ERRORLEVEL 1 (
    echo.
    echo [ERROR] Application exited with an error.
    pause
    exit /b 1
)

ENDLOCAL
