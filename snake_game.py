#!/usr/bin/env python3
"""
Terminal Snake Game
Use arrow keys to control the snake
Press 'q' to quit, 'space' to pause/unpause
"""

import curses
import random
import time
from collections import deque

class SnakeGame:
    def __init__(self, height=20, width=40, max_height=25, max_width=60):
        self.height = height
        self.width = width
        self.max_height = max_height
        self.max_width = max_width
        self.snake = deque([(height//2, width//2)])
        self.direction = (0, 1)  # (y, x) - start moving right
        self.food = None
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = 0.1  # seconds between moves
        self.base_speed = 0.1  # base speed for manual adjustment
        self.speed_multiplier = 1.0  # for manual speed control
        self.auto_speed_increase = True  # toggle for automatic speed increase
        self.snake_color = 1  # Default green
        self.current_color_index = 0
        
        # Bombs and bonus food
        self.bombs = []  # List of (position, timer) tuples
        self.max_bombs = 3  # Maximum number of bombs on screen
        self.bomb_spawn_chance = 0.005  # Reduced chance to spawn a bomb each move
        self.bomb_min_duration = 30  # Minimum time bomb stays
        self.bomb_max_duration = 100  # Maximum time bomb stays
        self.bomb_cooldown = 0  # Cooldown before spawning next bomb
        self.bomb_cooldown_time = 30  # Minimum moves between bomb spawns
        self.bonus_food = None  # Position of bonus food
        self.bonus_food_timer = 0  # Timer for bonus food expiration
        self.bonus_food_min_duration = 40  # Minimum time bonus stays
        self.bonus_food_max_duration = 80  # Maximum time bonus stays
        self.bonus_spawn_chance = 0.003  # Reduced chance to spawn bonus food
        self.bonus_cooldown = 0  # Cooldown before spawning next bonus
        self.bonus_cooldown_time = 50  # Minimum moves between bonus spawns
        
        # Available snake colors
        self.color_names = ['Green', 'Blue', 'Cyan', 'Magenta', 'Yellow', 'White']
        self.color_pairs = [1, 4, 5, 6, 3, 7]  # Corresponding color pair indices
        
        # Direction mappings
        self.directions = {
            curses.KEY_UP: (-1, 0),
            curses.KEY_DOWN: (1, 0),
            curses.KEY_LEFT: (0, -1),
            curses.KEY_RIGHT: (0, 1)
        }
        
    def generate_food(self):
        """Generate food at a random position not occupied by the snake"""
        while True:
            y = random.randint(1, self.height - 2)
            x = random.randint(1, self.width - 2)
            # Check bomb positions
            bomb_positions = [bomb[0] for bomb in self.bombs]
            if ((y, x) not in self.snake and 
                (y, x) not in bomb_positions and
                (y, x) != self.bonus_food):
                self.food = (y, x)
                break
    
    def generate_bomb(self):
        """Generate a bomb at a random position with random duration"""
        if len(self.bombs) >= self.max_bombs:
            return
            
        attempts = 0
        while attempts < 50:  # Prevent infinite loop
            y = random.randint(1, self.height - 2)
            x = random.randint(1, self.width - 2)
            # Check if position is free
            bomb_positions = [bomb[0] for bomb in self.bombs]
            if ((y, x) not in self.snake and 
                (y, x) != self.food and
                (y, x) != self.bonus_food and
                (y, x) not in bomb_positions):
                # Random duration for this bomb
                duration = random.randint(self.bomb_min_duration, self.bomb_max_duration)
                self.bombs.append(((y, x), duration))
                break
            attempts += 1
    
    def generate_bonus_food(self):
        """Generate bonus food worth extra points with random duration"""
        if self.bonus_food is not None:
            return
            
        attempts = 0
        while attempts < 50:  # Prevent infinite loop
            y = random.randint(1, self.height - 2)
            x = random.randint(1, self.width - 2)
            # Check if position is free
            bomb_positions = [bomb[0] for bomb in self.bombs]
            if ((y, x) not in self.snake and 
                (y, x) != self.food and
                (y, x) not in bomb_positions):
                self.bonus_food = (y, x)
                # Random duration for bonus food
                self.bonus_food_timer = random.randint(self.bonus_food_min_duration, 
                                                      self.bonus_food_max_duration)
                break
            attempts += 1
    
    def move_snake(self):
        """Move the snake in the current direction"""
        if self.paused or self.game_over:
            return
            
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.height - 1 or
            new_head[1] <= 0 or new_head[1] >= self.width - 1):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
            
        # Check bomb collision
        bomb_positions = [bomb[0] for bomb in self.bombs]
        if new_head in bomb_positions:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.generate_food()
            # Increase speed slightly if auto speed is enabled
            if self.auto_speed_increase:
                self.base_speed = max(0.05, self.base_speed - 0.005)
                self.update_speed()
        # Check if bonus food is eaten
        elif new_head == self.bonus_food:
            self.score += 50  # Bonus food worth 5x normal food
            self.bonus_food = None
            self.bonus_food_timer = 0
            # Bonus food also grows the snake
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
        # Update cooldowns
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1
        if self.bonus_cooldown > 0:
            self.bonus_cooldown -= 1
            
        # Randomly spawn bombs (with cooldown check)
        if (self.bomb_cooldown == 0 and 
            len(self.bombs) < self.max_bombs and 
            random.random() < self.bomb_spawn_chance):
            self.generate_bomb()
            self.bomb_cooldown = self.bomb_cooldown_time
            
        # Randomly spawn bonus food (with cooldown check)
        if (self.bonus_food is None and 
            self.bonus_cooldown == 0 and 
            random.random() < self.bonus_spawn_chance):
            self.generate_bonus_food()
            self.bonus_cooldown = self.bonus_cooldown_time
            
        # Update bonus food timer
        if self.bonus_food is not None:
            self.bonus_food_timer -= 1
            if self.bonus_food_timer <= 0:
                self.bonus_food = None
                
        # Update bomb timers and remove expired bombs
        self.bombs = [(pos, timer - 1) for pos, timer in self.bombs if timer > 1]
        
        # Add some randomness to disappearance
        # Small chance for bombs to disappear early
        if self.bombs and random.random() < 0.005:
            # Remove a random bomb
            self.bombs.pop(random.randint(0, len(self.bombs) - 1))
            
        # Small chance for bonus food to disappear early
        if self.bonus_food and random.random() < 0.005:
            self.bonus_food = None
            self.bonus_food_timer = 0
    
    def change_direction(self, key):
        """Change snake direction based on key press"""
        if key in self.directions:
            new_direction = self.directions[key]
            # Prevent snake from going back into itself
            if (new_direction[0] + self.direction[0] != 0 or
                new_direction[1] + self.direction[1] != 0):
                self.direction = new_direction
    
    def draw(self, stdscr):
        """Draw the game state"""
        stdscr.clear()
        
        # Draw border
        for y in range(self.height):
            stdscr.addch(y, 0, '│')
            stdscr.addch(y, self.width - 1, '│')
        for x in range(self.width):
            stdscr.addch(0, x, '─')
            stdscr.addch(self.height - 1, x, '─')
        # Corners
        stdscr.addch(0, 0, '┌')
        stdscr.addch(0, self.width - 1, '┐')
        stdscr.addch(self.height - 1, 0, '└')
        stdscr.addch(self.height - 1, self.width - 1, '┘')
        
        # Draw snake
        for i, (y, x) in enumerate(self.snake):
            if i == 0:
                stdscr.addch(y, x, '●', curses.color_pair(self.snake_color))  # Head
            else:
                stdscr.addch(y, x, '○', curses.color_pair(self.snake_color))  # Body
        
        # Draw food
        if self.food:
            stdscr.addch(self.food[0], self.food[1], '★', curses.color_pair(2))
            
        # Draw bombs
        for bomb_data in self.bombs:
            pos, timer = bomb_data
            # Flicker effect when bomb is about to disappear
            if timer < 10 and timer % 2 == 0:
                continue  # Skip drawing for flicker effect
            try:
                stdscr.addch(pos[0], pos[1], '💣', curses.color_pair(2))
            except:
                # Fallback if emoji doesn't work
                stdscr.addch(pos[0], pos[1], 'X', curses.color_pair(2) | curses.A_BOLD)
                
        # Draw bonus food
        if self.bonus_food:
            # More intense flash effect when about to disappear
            if self.bonus_food_timer < 15:
                # Rapid flashing when time is running out
                if self.bonus_food_timer % 2 == 0:
                    try:
                        stdscr.addch(self.bonus_food[0], self.bonus_food[1], '◆', curses.color_pair(3) | curses.A_BOLD)
                    except:
                        stdscr.addch(self.bonus_food[0], self.bonus_food[1], '$', curses.color_pair(3) | curses.A_BOLD)
            else:
                # Normal flash effect
                if self.bonus_food_timer % 4 < 2:
                    try:
                        stdscr.addch(self.bonus_food[0], self.bonus_food[1], '◆', curses.color_pair(3) | curses.A_BOLD)
                    except:
                        stdscr.addch(self.bonus_food[0], self.bonus_food[1], '$', curses.color_pair(3) | curses.A_BOLD)
        
        # Draw score and status
        status_y = self.height
        stdscr.addstr(status_y, 2, f"Score: {self.score}")
        speed_display = f"Speed: {self.speed_multiplier:.1f}x"
        stdscr.addstr(status_y, self.width // 2 - len(speed_display) // 2, speed_display)
        
        if self.paused:
            pause_msg = "PAUSED - Press 'space' to continue"
            settings_msg = "(Settings changed)"
            stdscr.addstr(self.height // 2 - 1, self.width // 2 - len(pause_msg) // 2, 
                         pause_msg, curses.color_pair(3))
            if not self.game_over:
                stdscr.addstr(self.height // 2, self.width // 2 - len(settings_msg) // 2,
                             settings_msg, curses.color_pair(3))
        
        if self.game_over:
            game_over_msg = "GAME OVER!"
            final_score_msg = f"Final Score: {self.score}"
            restart_msg = "Press 'r' to restart or 'q' to quit"
            
            stdscr.addstr(self.height // 2 - 1, self.width // 2 - len(game_over_msg) // 2,
                         game_over_msg, curses.color_pair(2))
            stdscr.addstr(self.height // 2, self.width // 2 - len(final_score_msg) // 2,
                         final_score_msg, curses.color_pair(2))
            stdscr.addstr(self.height // 2 + 1, self.width // 2 - len(restart_msg) // 2,
                         restart_msg, curses.color_pair(3))
        
        # Instructions
        stdscr.addstr(status_y + 1, 2, "Arrow keys: move | space: pause | q: quit | r: restart")
        
        # Draw control panel on the right side
        control_x = self.width + 2
        control_y = 1
        
        stdscr.addstr(control_y, control_x, "╔═══ CONTROLS ═══╗", curses.color_pair(3))
        stdscr.addstr(control_y + 1, control_x, "║                ║", curses.color_pair(3))
        stdscr.addstr(control_y + 2, control_x, "║ Speed Control: ║", curses.color_pair(3))
        stdscr.addstr(control_y + 3, control_x, "║ [-/+] Adjust   ║", curses.color_pair(3))
        stdscr.addstr(control_y + 4, control_x, "║ [a] Auto: ", curses.color_pair(3))
        auto_status = "ON " if self.auto_speed_increase else "OFF"
        stdscr.addstr(control_y + 4, control_x + 11, auto_status, 
                     curses.color_pair(1) if self.auto_speed_increase else curses.color_pair(2))
        stdscr.addstr(control_y + 4, control_x + 14, " ║", curses.color_pair(3))
        
        stdscr.addstr(control_y + 5, control_x, "║                ║", curses.color_pair(3))
        stdscr.addstr(control_y + 6, control_x, "║ Color:         ║", curses.color_pair(3))
        stdscr.addstr(control_y + 7, control_x, "║ [c] ", curses.color_pair(3))
        color_name = self.color_names[self.current_color_index]
        stdscr.addstr(control_y + 7, control_x + 5, f"{color_name:10}", curses.color_pair(self.snake_color))
        stdscr.addstr(control_y + 7, control_x + 15, " ║", curses.color_pair(3))
        
        stdscr.addstr(control_y + 8, control_x, "║                ║", curses.color_pair(3))
        stdscr.addstr(control_y + 9, control_x, "║ Canvas Size:   ║", curses.color_pair(3))
        stdscr.addstr(control_y + 10, control_x, "║ [w/s] Height   ║", curses.color_pair(3))
        stdscr.addstr(control_y + 11, control_x, "║ [j/l] Width    ║", curses.color_pair(3))
        stdscr.addstr(control_y + 12, control_x, "║                ║", curses.color_pair(3))
        stdscr.addstr(control_y + 13, control_x, "╚════════════════╝", curses.color_pair(3))
        
        # Current stats
        stdscr.addstr(control_y + 15, control_x, "╔═══ STATS ══════╗", curses.color_pair(3))
        stdscr.addstr(control_y + 16, control_x, "║                ║", curses.color_pair(3))
        stdscr.addstr(control_y + 17, control_x, f"║ Length: {len(self.snake):6} ║", curses.color_pair(3))
        stdscr.addstr(control_y + 18, control_x, f"║ Speed: {self.speed_multiplier:5.1f}x  ║", curses.color_pair(3))
        stdscr.addstr(control_y + 19, control_x, f"║ Size: {self.height}x{self.width:<5} ║", curses.color_pair(3))
        stdscr.addstr(control_y + 20, control_x, f"║ Bombs: {len(self.bombs):<7} ║", curses.color_pair(3))
        stdscr.addstr(control_y + 21, control_x, "║                ║", curses.color_pair(3))
        stdscr.addstr(control_y + 22, control_x, "╚════════════════╝", curses.color_pair(3))
        
        # Legend
        stdscr.addstr(control_y + 24, control_x, "╔═══ LEGEND ═════╗", curses.color_pair(3))
        stdscr.addstr(control_y + 25, control_x, "║ ★ Food = 10pts ║", curses.color_pair(3))
        stdscr.addstr(control_y + 26, control_x, "║ ◆ Bonus = 50pts║", curses.color_pair(3))
        stdscr.addstr(control_y + 27, control_x, "║ X Bomb = Death ║", curses.color_pair(3))
        stdscr.addstr(control_y + 28, control_x, "╚════════════════╝", curses.color_pair(3))
        
        # Show cooldowns if active
        if self.bomb_cooldown > 0 or self.bonus_cooldown > 0:
            stdscr.addstr(control_y + 30, control_x, "╔══ COOLDOWNS ═══╗", curses.color_pair(3))
            if self.bomb_cooldown > 0:
                stdscr.addstr(control_y + 31, control_x, f"║ Bomb in: {self.bomb_cooldown:3}   ║", curses.color_pair(3))
            else:
                stdscr.addstr(control_y + 31, control_x, "║ Bomb: Ready    ║", curses.color_pair(3))
            if self.bonus_cooldown > 0:
                stdscr.addstr(control_y + 32, control_x, f"║ Bonus in: {self.bonus_cooldown:3}  ║", curses.color_pair(3))
            else:
                stdscr.addstr(control_y + 32, control_x, "║ Bonus: Ready   ║", curses.color_pair(3))
            stdscr.addstr(control_y + 33, control_x, "╚════════════════╝", curses.color_pair(3))
        
        stdscr.refresh()
    
    def reset(self):
        """Reset the game to initial state"""
        # Save current preferences
        saved_color_index = self.current_color_index
        saved_speed_multiplier = self.speed_multiplier
        saved_auto_speed = self.auto_speed_increase
        saved_max_height = self.max_height
        saved_max_width = self.max_width
        
        self.__init__(self.height, self.width, saved_max_height, saved_max_width)
        
        # Restore preferences
        self.current_color_index = saved_color_index
        self.snake_color = self.color_pairs[self.current_color_index]
        self.speed_multiplier = saved_speed_multiplier
        self.auto_speed_increase = saved_auto_speed
        self.update_speed()
        
        # Clear bombs and bonus food on reset
        self.bombs = []
        self.bonus_food = None
        self.bonus_food_timer = 0
        self.bomb_cooldown = 0
        self.bonus_cooldown = 0
    
    def update_speed(self):
        """Update the actual game speed based on base speed and multiplier"""
        self.speed = self.base_speed / self.speed_multiplier
    
    def change_speed(self, delta):
        """Change game speed by delta"""
        self.speed_multiplier = max(0.1, min(5.0, self.speed_multiplier + delta))
        self.update_speed()
        self.paused = True  # Auto-pause when changing speed
    
    def next_color(self):
        """Cycle to the next snake color"""
        self.current_color_index = (self.current_color_index + 1) % len(self.color_pairs)
        self.snake_color = self.color_pairs[self.current_color_index]
        self.paused = True  # Auto-pause when changing color
    
    def toggle_auto_speed(self):
        """Toggle automatic speed increase"""
        self.auto_speed_increase = not self.auto_speed_increase
        self.paused = True  # Auto-pause when toggling auto speed
    
    def resize_canvas(self, height_delta=0, width_delta=0):
        """Resize the game canvas"""
        new_height = self.height + height_delta
        new_width = self.width + width_delta
        
        # Ensure minimum size
        new_height = max(10, min(new_height, self.max_height))
        new_width = max(20, min(new_width, self.max_width))
        
        if new_height != self.height or new_width != self.width:
            # Save game state
            saved_score = self.score
            saved_color_index = self.current_color_index
            saved_speed_multiplier = self.speed_multiplier
            saved_auto_speed = self.auto_speed_increase
            
            # Reinitialize with new size
            self.__init__(new_height, new_width, self.max_height, self.max_width)
            
            # Restore saved state
            self.score = saved_score
            self.current_color_index = saved_color_index
            self.snake_color = self.color_pairs[self.current_color_index]
            self.speed_multiplier = saved_speed_multiplier
            self.auto_speed_increase = saved_auto_speed
            self.update_speed()
            self.generate_food()
            self.paused = True  # Auto-pause after resizing
            
            # Clear bombs and regenerate to fit new size
            self.bombs = []
            self.bonus_food = None
            self.bonus_food_timer = 0
            self.bomb_cooldown = 0
            self.bonus_cooldown = 0

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Refresh rate in milliseconds
    
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Messages
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)   # Blue Snake
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Cyan Snake
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Magenta Snake
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)  # White Snake
    
    # Get terminal size and create game
    height, width = stdscr.getmaxyx()
    max_game_height = min(height - 3, 30)
    max_game_width = min(width - 25, 80)
    game_height = min(20, max_game_height)  # Start with reasonable size
    game_width = min(40, max_game_width)
    
    game = SnakeGame(game_height, game_width, max_game_height, max_game_width)
    game.generate_food()
    
    last_move_time = time.time()
    
    while True:
        # Handle input
        key = stdscr.getch()
        
        if key == ord('q'):
            break
        elif key == ord(' '):  # Space bar for pause
            game.paused = not game.paused
        elif key == ord('r') and game.game_over:
            game.reset()
            game.generate_food()
        elif key == ord('-') or key == ord('_'):
            game.change_speed(-0.1)
        elif key == ord('+') or key == ord('='):
            game.change_speed(0.1)
        elif key == ord('a') and not game.game_over:
            game.toggle_auto_speed()
        elif key == ord('c') and not game.game_over:
            game.next_color()
        elif key == ord('w') and not game.game_over:
            game.resize_canvas(height_delta=-1)
        elif key == ord('s') and not game.game_over:
            game.resize_canvas(height_delta=1)
        elif key == ord('j') and not game.game_over:
            game.resize_canvas(width_delta=-2)
        elif key == ord('l') and not game.game_over:
            game.resize_canvas(width_delta=2)
        elif key in game.directions and not game.game_over:
            game.change_direction(key)
        
        # Move snake at specified speed
        current_time = time.time()
        if current_time - last_move_time >= game.speed:
            game.move_snake()
            last_move_time = current_time
        
        # Draw everything
        game.draw(stdscr)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame interrupted!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Make sure your terminal window is large enough for the game.")
