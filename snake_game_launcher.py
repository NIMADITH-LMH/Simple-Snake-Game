#!/usr/bin/env python3
"""
Snake Game Launcher
Automatically opens the game in a new terminal window
"""

import os
import sys
import subprocess
import platform

def launch_in_new_terminal():
    """Launch the snake game in a new terminal window"""
    
    # Get the path to the snake game
    game_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snake_game.py")
    
    if not os.path.exists(game_path):
        print("Error: snake_game.py not found in the same directory!")
        input("Press Enter to exit...")
        return
    
    system = platform.system()
    
    if system == "Windows":
        # Check if running in a terminal already
        try:
            # Try to get terminal size - if this fails, we're not in a proper terminal
            os.get_terminal_size()
            # We're in a terminal, just run the game directly
            subprocess.run([sys.executable, game_path])
        except:
            # Not in a proper terminal, open a new one
            
            # Try Windows Terminal first (best experience)
            try:
                subprocess.run([
                    "wt.exe",
                    "-d", os.path.dirname(game_path),
                    "python", game_path
                ])
                return
            except:
                pass
            
            # Try PowerShell
            try:
                subprocess.run([
                    "powershell",
                    "-NoExit",
                    "-Command",
                    f"cd '{os.path.dirname(game_path)}'; python snake_game.py; Write-Host 'Press any key to exit...'; $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')"
                ])
                return
            except:
                pass
            
            # Fallback to cmd
            try:
                cmd_command = f'cd /d "{os.path.dirname(game_path)}" && python snake_game.py && pause'
                subprocess.run([
                    "cmd",
                    "/c",
                    f"start cmd /k {cmd_command}"
                ])
            except Exception as e:
                print(f"Error launching terminal: {e}")
                input("Press Enter to exit...")
                
    elif system == "Darwin":  # macOS
        # Open in Terminal app
        apple_script = f'''
        tell application "Terminal"
            do script "cd '{os.path.dirname(game_path)}' && python3 '{game_path}'"
            activate
        end tell
        '''
        subprocess.run(["osascript", "-e", apple_script])
        
    elif system == "Linux":
        # Try various terminal emulators
        terminals = [
            ["gnome-terminal", "--", "python3", game_path],
            ["konsole", "-e", "python3", game_path],
            ["xterm", "-e", "python3", game_path],
            ["xfce4-terminal", "-e", f"python3 {game_path}"]
        ]
        
        for terminal_cmd in terminals:
            try:
                subprocess.run(terminal_cmd)
                break
            except:
                continue
        else:
            print("No suitable terminal found. Running in current terminal...")
            subprocess.run(["python3", game_path])

if __name__ == "__main__":
    launch_in_new_terminal()
