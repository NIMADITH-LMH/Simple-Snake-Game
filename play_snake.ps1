# Snake Game Launcher for PowerShell
# Sets up optimal terminal settings and runs the game

# Set window title
$host.UI.RawUI.WindowTitle = "Snake Game"

# Try to set optimal window size
try {
    $window = $host.UI.RawUI
    $newSize = $window.BufferSize
    $newSize.Width = 120
    $newSize.Height = 50
    $window.BufferSize = $newSize
    
    $newSize = $window.WindowSize
    $newSize.Width = 120
    $newSize.Height = 40
    $window.WindowSize = $newSize
} catch {
    Write-Host "Note: Could not resize window. Using current size." -ForegroundColor Yellow
}

# Set UTF-8 encoding for proper character display
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Clear-Host

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        TERMINAL SNAKE GAME 🐍          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Checking requirements..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python from python.org" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Check windows-curses
Write-Host "Checking for windows-curses..." -NoNewline
$cursesCheck = python -c "import curses; print('OK')" 2>&1
if ($cursesCheck -ne "OK") {
    Write-Host " Not found!" -ForegroundColor Yellow
    Write-Host "Installing windows-curses..."
    pip install windows-curses
    Write-Host "✓ Installation complete!" -ForegroundColor Green
} else {
    Write-Host " ✓ Found!" -ForegroundColor Green
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "CONTROLS:" -ForegroundColor Cyan
Write-Host "  Arrow Keys  → Move snake" -ForegroundColor White
Write-Host "  Space Bar   → Pause/Resume" -ForegroundColor White
Write-Host "  [+/-]       → Speed up/down" -ForegroundColor White
Write-Host "  [c]         → Change color" -ForegroundColor White
Write-Host "  [w/s]       → Canvas height" -ForegroundColor White
Write-Host "  [j/l]       → Canvas width" -ForegroundColor White
Write-Host "  [q]         → Quit game" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Press any key to start the game..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Clear and run game
Clear-Host
python snake_game.py

# Game ended
Write-Host ""
Write-Host "Thanks for playing! 🎮" -ForegroundColor Cyan
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
