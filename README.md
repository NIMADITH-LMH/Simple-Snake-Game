# Terminal Snake Game 🐍

A feature-rich snake game for the terminal with customizable controls, dynamic obstacles, and bonus rewards!

## 📋 Requirements

- Python 3.6 or higher
- Windows: `windows-curses` package (auto-installed by launchers)
- Linux/Mac: Built-in curses support

## 🚀 Quick Start

### Method 1: Double-Click Launch (Easiest)
- **Windows**: Double-click `play_snake.bat`
- **PowerShell**: Right-click `play_snake.ps1` → "Run with PowerShell"
- **Cross-platform**: Double-click `snake_game_launcher.py`

### Method 2: Command Line
```bash
python snake_game.py
```

### Method 3: VS Code
1. Open folder in VS Code
2. Press `F5` and choose:
   - "Play Snake Game (External Terminal)" - Opens in new window
   - "Play Snake Game (Integrated Terminal)" - Runs in VS Code
   - "Play Snake Game (New Window)" - Uses launcher

### Method 4: Desktop Shortcut
1. Double-click `create_desktop_shortcut.vbs`
2. Find "Snake Game" on your desktop

## 🎮 Game Controls

### Movement
- **Arrow Keys**: Move the snake (Up, Down, Left, Right)

### Game Control
- **Space Bar**: Pause/Unpause the game
- **q**: Quit the game  
- **r**: Restart (after game over)

### Speed Control (0.1x - 5.0x)
- **`-`**: Decrease speed (make snake slower)
- **`+` or `=`**: Increase speed (make snake faster)
- **`a`**: Toggle automatic speed increase on/off

### Customization
- **`c`**: Change snake color (6 color options)
- **`w`/`s`**: Decrease/Increase canvas height
- **`j`/`l`**: Decrease/Increase canvas width

**Note**: All settings changes auto-pause the game. Press Space to continue!

## 🎯 Game Features

### Scoring System
- **🌟 Regular Food**: 10 points
- **💎 Bonus Food**: 50 points (5x value!)
- **💣 Bombs**: Instant death - avoid them!

### Dynamic Obstacles & Rewards

#### 💣 Bombs
- Spawn with cooldown timer (30 moves minimum between spawns)
- Random lifetime: 30-100 moves
- Visual warnings:
  - **Solid**: Safe for now
  - **Flickering**: About to disappear (last 10 moves)
- Maximum 3 bombs at once
- Can disappear randomly for surprises

#### 💎 Bonus Food  
- Spawn with cooldown timer (50 moves minimum between spawns)
- Random lifetime: 40-80 moves
- Visual warnings:
  - **Slow flash**: Plenty of time
  - **Rapid flash**: Hurry! (last 15 moves)
- Worth 5x regular food
- Can vanish early randomly

### Visual Panels

#### Control Panel (Right Side)
- Speed controls and current multiplier
- Color selector with preview
- Canvas size controls
- Auto-speed toggle status

#### Stats Panel
- Current snake length
- Speed multiplier
- Canvas dimensions  
- Active bomb count

#### Cooldown Display
- Shows countdown to next possible bomb/bonus
- "Ready" when items can spawn

#### Legend
- Quick reference for all game elements

## 📁 File List

| File | Description |
|------|-------------|
| `snake_game.py` | Main game file |
| `play_snake.bat` | Windows batch launcher |
| `play_snake.ps1` | PowerShell launcher (best for Windows) |
| `snake_game_launcher.py` | Python launcher (opens new terminal) |
| `create_desktop_shortcut.vbs` | Creates desktop shortcut |
| `README.md` | This documentation |
| `.vscode/settings.json` | VS Code terminal settings |
| `.vscode/launch.json` | VS Code debug configurations |
| `snake_game_complete.zip` | All files in one archive |

## 💡 Pro Tips

### Strategy
1. **Speed Management**: Start at 0.5x speed to learn
2. **Bomb Timing**: Watch for flickering - they're about to vanish
3. **Bonus Priority**: Rapidly flashing = grab NOW!
4. **Canvas Size**: Bigger = easier, Smaller = harder
5. **Color Choice**: White/Yellow most visible on dark terminals

### Advanced Techniques
1. **Cooldown Tracking**: Plan moves based on spawn timers
2. **Risk Assessment**: Sometimes wait for bombs to disappear
3. **Speed Bursts**: Increase speed for bonus food, decrease for navigation
4. **Pause Strategy**: Use space bar to plan complex routes

## 🛠️ Troubleshooting

### Windows Issues

#### "Module not found" error:
```bash
pip install windows-curses
```

#### PowerShell script blocked:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Characters look wrong:
```cmd
chcp 65001
```

### Terminal Issues

#### Game looks corrupted:
- Resize terminal to at least 80x40 characters
- Try different terminal (Windows Terminal recommended)
- Ensure UTF-8 encoding

#### Can't see colors:
- Use PowerShell instead of CMD
- Try Windows Terminal from Microsoft Store
- Check terminal color settings

#### Controls not responding:
- Make sure terminal window is focused
- Try running outside VS Code
- Disable terminal mouse mode if enabled

### VS Code Issues

#### External terminal not opening:
1. Go to File → Preferences → Settings
2. Search "terminal external"
3. Set path to your preferred terminal

## 🎨 Customization

### Terminal Recommendations
- **Best**: Windows Terminal (from Microsoft Store)
- **Good**: PowerShell 7+
- **Basic**: PowerShell 5.1 (built-in)
- **Minimal**: Command Prompt

### Optimal Settings
- **Font**: Consolas, Cascadia Code, or Fira Code
- **Size**: 14-16pt
- **Window**: 120x40 characters or larger
- **Theme**: Dark background for best contrast

## 📊 Game Mechanics

### Spawn Rates
- **Bombs**: 0.5% chance per move (after cooldown)
- **Bonus Food**: 0.3% chance per move (after cooldown)
- **Cooldowns**: Prevent overwhelming spawns

### Speed Formula
- Base speed: 0.1 seconds per move
- With multiplier: `0.1 / multiplier` seconds
- Auto-increase: -0.005 seconds per food (when enabled)

### Scoring
- Regular food: 10 points
- Bonus food: 50 points
- No points for survival time
- High score persists until game closed

## 🏆 Challenge Modes

Try these self-imposed challenges:

1. **Speed Demon**: Play at 3.0x+ speed
2. **Tiny Box**: Minimum canvas size (10x20)
3. **No Pause**: Never use space bar
4. **Bomb Dodger**: Survive with 3 bombs active
5. **Bonus Hunter**: Only eat bonus food

## 📝 Version History

- **v1.0**: Basic snake game
- **v2.0**: Added colors and speed control
- **v3.0**: Added bombs and bonus food
- **v4.0**: Added auto-pause and canvas resize
- **v5.0**: Added cooldowns and visual warnings
- **Current**: Multiple launch methods and full documentation

## 🎮 Enjoy the Game!

Challenge yourself and friends to beat high scores while mastering the dynamic obstacles!

---
*Created with Python and curses library*
