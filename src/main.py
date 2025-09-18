
import pygame
import random
import sys
import json
from datetime import datetime
from pathlib import Path

# --------------------
# Config / constants
# --------------------
CELL = 20
SIDEBAR_WIDTH = 220
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Grid is placed to the right of the left sidebar:
GRID_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH
COLS = GRID_WIDTH // CELL
ROWS = SCREEN_HEIGHT // CELL
GRID_WIDTH = COLS * CELL  # snap
GRID_HEIGHT = ROWS * CELL

# Movement timer event
MOVE_EVENT = pygame.USEREVENT + 1

# Speed (ms per move): larger = slower
INITIAL_MOVE_INTERVAL_MS = 200
MIN_MOVE_INTERVAL_MS = 60
SPEED_MULTIPLIER = 0.94

# Highscore file (single score)
HIGH_SCORE_FILE = Path("high_score.json")

# Colors (dark theme)
BLACK = (12, 12, 12)
WHITE = (230, 230, 230)
GRID_COLOR = (40, 40, 40)
SNAKE_HEAD = (50, 202, 50)
SNAKE_BODY = (0, 160, 0)
FOOD_COLOR = (220, 60, 60)
PANEL_BG = (18, 18, 18)
BTN_BG = (60, 60, 60)
BTN_ACTIVE = (90, 140, 90)
TEXT_COLOR = WHITE
GAME_OVER_COLOR = (220, 80, 80)

# --------------------
# Exceptions
# --------------------
class CollisionException(Exception):
    pass

class WallCollision(CollisionException):
    pass

class SelfCollision(CollisionException):
    pass

# --------------------
# Snake class
# --------------------
class Snake:
    def __init__(self, init_length=3):
        mid_x, mid_y = COLS // 2, ROWS // 2
        self.body = [(mid_x - i, mid_y) for i in range(init_length)]
        self.direction = (1, 0)
        self.grow_pending = 0

    @property
    def head(self):
        return self.body[0]

    def set_direction(self, dx, dy):
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return
        self.direction = (dx, dy)

    def compute_next_head(self):
        hx, hy = self.head
        dx, dy = self.direction
        return (hx + dx, hy + dy)

    def will_collide_self(self, pos):
        return pos in self.body

    def move_head(self, new_head):
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def reset(self, init_length=3):
        mid_x, mid_y = COLS // 2, ROWS // 2
        self.body = [(mid_x - i, mid_y) for i in range(init_length)]
        self.direction = (1, 0)
        self.grow_pending = 0

# --------------------
# Food class (circle)
# --------------------
class Food:
    def __init__(self, snake_body):
        self.position = self._random_position(snake_body)

    def _random_position(self, snake_body):
        tries = 0
        while True:
            tries += 1
            p = (random.randrange(COLS), random.randrange(ROWS))
            if p not in snake_body:
                return p
            if tries > 1000:
                raise RuntimeError("Board full?")

    def respawn(self, snake_body):
        self.position = self._random_position(snake_body)

# --------------------
# Single high score manager
# --------------------
class HighScoreManager:
    def __init__(self, path=HIGH_SCORE_FILE):
        self.path = Path(path)
        self.high_score = self._load()

    def _load(self):
        if not self.path.exists():
            return 0
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # accept dict or plain int
            if isinstance(data, dict):
                return int(data.get("high_score", 0))
            return int(data)
        except Exception:
            return 0

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"high_score": int(self.high_score), "when": datetime.now().isoformat()}, f, indent=2)
        except Exception as e:
            print("Warning: could not save high score:", e)

    def update_if_beaten(self, score):
        if int(score) > int(self.high_score):
            self.high_score = int(score)
            self.save()

    def get(self):
        return int(self.high_score)

# --------------------
# Game class
# --------------------
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.collision = None
        self.move_interval = INITIAL_MOVE_INTERVAL_MS
        self.highscore = HighScoreManager()
        self.running = False  # started and not paused

    def start(self):
        if not self.running and not self.game_over:
            self.running = True
            pygame.time.set_timer(MOVE_EVENT, self.move_interval)

    def pause(self):
        if self.running:
            self.running = False
            pygame.time.set_timer(MOVE_EVENT, 0)

    def toggle_pause(self):
        if self.running:
            self.pause()
        else:
            if self.game_over:
                self.restart()
            else:
                self.start()

    def restart(self):
        self.snake.reset()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.collision = None
        self.move_interval = INITIAL_MOVE_INTERVAL_MS
        self.running = True
        pygame.time.set_timer(MOVE_EVENT, self.move_interval)

    def stop_timer(self):
        pygame.time.set_timer(MOVE_EVENT, 0)

    def update_move(self):
        if self.game_over or not self.running:
            return
        new_head = self.snake.compute_next_head()
        hx, hy = new_head
        if not (0 <= hx < COLS and 0 <= hy < ROWS):
            self.game_over = True
            self.collision = WallCollision("Hit wall")
            self.running = False
            self.stop_timer()
            self.highscore.update_if_beaten(self.score)
            return
        if self.snake.will_collide_self(new_head):
            self.game_over = True
            self.collision = SelfCollision("Hit self")
            self.running = False
            self.stop_timer()
            self.highscore.update_if_beaten(self.score)
            return
        self.snake.move_head(new_head)
        if new_head == self.food.position:
            self.score += 1
            self.snake.grow()
            self.food.respawn(self.snake.body)
            new_interval = max(MIN_MOVE_INTERVAL_MS, int(self.move_interval * SPEED_MULTIPLIER))
            if new_interval != self.move_interval:
                self.move_interval = new_interval
                pygame.time.set_timer(MOVE_EVENT, self.move_interval)

    def set_direction(self, dx, dy):
        self.snake.set_direction(dx, dy)

# --------------------
# Drawing helpers and main loop
# --------------------
def draw_grid(surface, grid_x, grid_y):
    for x in range(grid_x, grid_x + GRID_WIDTH, CELL):
        pygame.draw.line(surface, GRID_COLOR, (x, grid_y), (x, grid_y + GRID_HEIGHT))
    for y in range(grid_y, grid_y + GRID_HEIGHT, CELL):
        pygame.draw.line(surface, GRID_COLOR, (grid_x, y), (grid_x + GRID_WIDTH, y))

def draw_buttons(surface, font, start_rect, pause_rect, running):
    pygame.draw.rect(surface, BTN_ACTIVE if running else BTN_BG, start_rect, border_radius=6)
    txt = font.render("Start" if not running else "Running", True, TEXT_COLOR)
    surface.blit(txt, (start_rect.x + 10, start_rect.y + 6))

    pygame.draw.rect(surface, BTN_BG if running else (80, 80, 80), pause_rect, border_radius=6)
    ptxt = font.render("Pause" if running else "Paused", True, TEXT_COLOR)
    surface.blit(ptxt, (pause_rect.x + 10, pause_rect.y + 6))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake — Group 18 (Merged)")
    clock = pygame.time.Clock()
    small_font = pygame.font.SysFont(None, 20)
    mid_font = pygame.font.SysFont(None, 26)
    big_font = pygame.font.SysFont(None, 36)

    # Sidebar on the left
    panel_x = 0
    grid_x = SIDEBAR_WIDTH
    start_btn = pygame.Rect(panel_x + 20, 20, SIDEBAR_WIDTH - 40, 36)
    pause_btn = pygame.Rect(panel_x + 20, 70, SIDEBAR_WIDTH - 40, 36)
    hs_y = 140

    game = Game()
    # start paused so UI is visible and user presses Start
    game.pause()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == MOVE_EVENT:
                game.update_move()

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                if start_btn.collidepoint(mx, my):
                    if game.game_over:
                        game.restart()
                    else:
                        game.start()
                elif pause_btn.collidepoint(mx, my):
                    game.toggle_pause()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if ev.key in (pygame.K_LEFT, pygame.K_a):
                    game.set_direction(-1, 0)
                elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                    game.set_direction(1, 0)
                elif ev.key in (pygame.K_UP, pygame.K_w):
                    game.set_direction(0, -1)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    game.set_direction(0, 1)
                elif ev.key == pygame.K_SPACE:
                    game.toggle_pause()
                elif ev.key == pygame.K_r:
                    game.restart()

        # draw background & sidebar
        screen.fill(BLACK)
        pygame.draw.rect(screen, PANEL_BG, (panel_x, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))

        # draw grid
        draw_grid(screen, grid_x, 0)

        # draw food as rounded ball (Yusuf style)
        fx, fy = game.food.position
        food_px = grid_x + fx * CELL + CELL // 2
        food_py = fy * CELL + CELL // 2
        radius = CELL // 3
        pygame.draw.circle(screen, FOOD_COLOR, (food_px, food_py), radius)

        # draw snake (rectangles)
        for i, (sx, sy) in enumerate(game.snake.body):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            rect = pygame.Rect(grid_x + sx*CELL, sy*CELL, CELL, CELL)
            pygame.draw.rect(screen, color, rect, border_radius=4)

        # HUD: score in top-left of grid area (but keep dark theme)
        score_surf = mid_font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_surf, (grid_x + 8, 8))

        # Sidebar content: buttons and high score (single)
        draw_buttons(screen, small_font, start_btn, pause_btn, game.running)

        hs_title = mid_font.render("High Score", True, TEXT_COLOR)
        screen.blit(hs_title, (panel_x + 16, hs_y))
        hs_val = small_font.render(str(game.highscore.get()), True, TEXT_COLOR)
        screen.blit(hs_val, (panel_x + 20, hs_y + 36))

        # Game over overlay
        if game.game_over:
            over_surf = big_font.render("GAME OVER", True, GAME_OVER_COLOR)
            screen.blit(over_surf, (grid_x + GRID_WIDTH//2 - over_surf.get_width()//2, GRID_HEIGHT//2 - 30))
            sub = small_font.render("Press R to restart or Start to restart", True, TEXT_COLOR)
            screen.blit(sub, (grid_x + GRID_WIDTH//2 - sub.get_width()//2, GRID_HEIGHT//2 + 8))

        # paused hint
        if not game.running and not game.game_over:
            pmsg = small_font.render("Paused — press Start or Space to run", True, (180,180,180))
            screen.blit(pmsg, (grid_x + GRID_WIDTH//2 - pmsg.get_width()//2, GRID_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)  # render fps

if __name__ == "__main__":
    main()
