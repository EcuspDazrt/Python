import pygame
import random
import sys

# --- INIT ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧱 Block Breaker - Slower Ball Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PWR_COLORS = {
    "expand": (255, 165, 0),
    "sticky": (0, 255, 255),
    "multiball": (255, 255, 0),
    "magnet": (200, 0, 255),
    "explode": (255, 100, 100)
}

# --- SETTINGS ---
BASE_BALL_SPEED = 3
LEVEL = 1

# --- INIT GAME OBJECTS ---
def reset_game(level):
    global paddle, balls, bricks, powerups, active_powerups, BALL_SPEED

    paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 120, 15)
    powerups = []
    BALL_SPEED = BASE_BALL_SPEED + (level // 3)

    balls = [{
        "rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, 12, 12),
        "vel": [random.choice([-BALL_SPEED, BALL_SPEED]), -BALL_SPEED],
        "sticky": False,
        "magnet": False
    }]
    active_powerups = {"expand": False, "sticky": False, "magnet": False}

    # Create Bricks
    global bricks, brick_colors
    bricks = []
    brick_colors = []
    rows, cols = 5 + level, 10
    brick_w = WIDTH // cols
    brick_h = 30
    for r in range(rows):
        for c in range(cols):
            brick = pygame.Rect(c * brick_w, r * brick_h + 40, brick_w - 4, brick_h - 4)
            color = [random.randint(50, 255) for _ in range(3)]
            bricks.append(brick)
            brick_colors.append(color)

# --- POWERUPS ---
def spawn_powerup(x, y):
    kinds = ["expand", "sticky", "multiball", "magnet", "explode"]
    kind = random.choice(kinds)
    powerups.append({"rect": pygame.Rect(x, y, 20, 20), "type": kind})

def draw_powerup(pwr):
    color = PWR_COLORS[pwr["type"]]
    pygame.draw.rect(screen, color, pwr["rect"])
    text = font.render(pwr["type"][0].upper(), True, BLACK)
    screen.blit(text, (pwr["rect"].x + 4, pwr["rect"].y + 2))

def explode_bricks(center_rect):
    removed = 0
    for i in range(len(bricks)-1, -1, -1):
        if bricks[i].colliderect(center_rect.inflate(100, 100)):
            del bricks[i]
            del brick_colors[i]
            removed += 1
    return removed

# --- MAIN GAME LOOP ---
reset_game(LEVEL)
running = True
while running:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 10
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 10

    if active_powerups["expand"]:
        paddle.width = 180
    else:
        paddle.width = 120

    # Ball logic
    for ball in balls:
        if ball["sticky"]:
            ball["rect"].centerx = paddle.centerx
            ball["rect"].bottom = paddle.top
            if keys[pygame.K_SPACE]:
                ball["sticky"] = False
        else:
            if ball.get("magnet"):
                dx = paddle.centerx - ball["rect"].centerx
                ball["vel"][0] += dx * 0.002
                ball["vel"][0] = max(min(ball["vel"][0], BALL_SPEED), -BALL_SPEED)

            ball["rect"].x += int(ball["vel"][0])
            ball["rect"].y += int(ball["vel"][1])

            if ball["rect"].left <= 0 or ball["rect"].right >= WIDTH:
                ball["vel"][0] *= -1
            if ball["rect"].top <= 0:
                ball["vel"][1] *= -1

            if ball["rect"].colliderect(paddle) and ball["vel"][1] > 0:
                ball["vel"][1] *= -1
                if active_powerups["sticky"]:
                    ball["sticky"] = True

            for i in range(len(bricks)-1, -1, -1):
                if ball["rect"].colliderect(bricks[i]):
                    if abs(ball["rect"].bottom - bricks[i].top) < 10 and ball["vel"][1] > 0:
                        ball["vel"][1] *= -1
                    elif abs(ball["rect"].top - bricks[i].bottom) < 10 and ball["vel"][1] < 0:
                        ball["vel"][1] *= -1
                    else:
                        ball["vel"][0] *= -1

                    if random.random() < 0.5:  # 50% drop rate
                        spawn_powerup(bricks[i].x, bricks[i].y)

                    del bricks[i]
                    del brick_colors[i]
                    break

    # Remove lost balls
    balls = [b for b in balls if b["rect"].top < HEIGHT]
    if not balls:
        LEVEL = 1
        reset_game(LEVEL)

    # Powerup logic
    for pwr in powerups[:]:
        pwr["rect"].y += 4
        if pwr["rect"].colliderect(paddle):
            kind = pwr["type"]
            if kind == "expand":
                active_powerups["expand"] = True
            elif kind == "sticky":
                active_powerups["sticky"] = True
            elif kind == "magnet":
                active_powerups["magnet"] = True
                for b in balls:
                    b["magnet"] = True
            elif kind == "multiball":
                new_balls = []
                for b in balls:
                    new_balls.append({
                        "rect": b["rect"].copy(),
                        "vel": [random.choice([-BALL_SPEED, BALL_SPEED]), -BALL_SPEED],
                        "sticky": False,
                        "magnet": b.get("magnet", False)
                    })
                balls.extend(new_balls)
            elif kind == "explode":
                for b in balls:
                    explode_bricks(b["rect"])
            powerups.remove(pwr)
        elif pwr["rect"].top > HEIGHT:
            powerups.remove(pwr)

    # Draw bricks
    for i, brick in enumerate(bricks):
        pygame.draw.rect(screen, brick_colors[i], brick)

    # Draw paddle and balls
    pygame.draw.rect(screen, WHITE, paddle)
    for ball in balls:
        pygame.draw.ellipse(screen, (0, 255, 0), ball["rect"])

    # Draw powerups
    for pwr in powerups:
        draw_powerup(pwr)

    # Display level
    level_text = font.render(f"Level {LEVEL}", True, WHITE)
    screen.blit(level_text, (10, 10))

    # Next level
    if not bricks:
        LEVEL += 1
        reset_game(LEVEL)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
