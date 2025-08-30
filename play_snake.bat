@echo off
title Snake Game
echo Starting Snake Game...
echo.

:: Check if python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python from python.org
    pause
    exit /b 1
)

:: Check if windows-curses is installed
python -c "import curses" >nul 2>&1
if errorlevel 1 (
    echo Installing required package: windows-curses
    pip install windows-curses
    echo.
)

:: Clear screen and run the game
cls
echo ========================================
echo         TERMINAL SNAKE GAME
echo ========================================
echo.
echo Controls:
echo   Arrow Keys - Move snake
echo   Space Bar  - Pause/Resume
echo   + / -      - Adjust speed
echo   c          - Change color
echo   q          - Quit game
echo.
echo Press any key to start...
pause >nul

:: Run the game
cls
python snake_game.py

:: Keep window open after game ends
echo.
echo Game Over! Press any key to exit...
pause >nul
