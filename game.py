import pygame
import random

# ── Setup ───────────────────────────────────────────
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font      = pygame.font.SysFont(None, 36)
big_font  = pygame.font.SysFont(None, 72)

# ── Colors ──────────────────────────────────────────
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
CYAN   = (0,   200, 255)
RED    = (255, 60,  60)
YELLOW = (255, 220, 0)
GRAY   = (150, 150, 150)
ORANGE = (255, 140, 0)

# ── Player ──────────────────────────────────────────
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 40)
player_speed = 6

#Now add the draw function ABOVE  running = True  as well:

# ── Draw helpers ─────────────────────────────────────
def draw_ship(rect, color=CYAN):
    pygame.draw.polygon(screen, color, [
        (rect.centerx, rect.top),
        (rect.left,    rect.bottom),
        (rect.right,   rect.bottom),
    ])
    pygame.draw.rect(screen, ORANGE,
        (rect.centerx - 5, rect.bottom - 6, 10, 8))

def draw_stars():
    random.seed(42)       # same seed = same stars every frame
    for _ in range(80):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(1, 2)
        pygame.draw.circle(screen, WHITE, (x, y), r)
    random.seed()          # restore normal randomness

# ── Bullets ─────────────────────────────────────────
bullets       = []
bullet_speed  = 10
shoot_cooldown = 0

# ── Asteroids ───────────────────────────────────────
asteroids      = []
asteroid_speed = 3
spawn_timer    = 0
spawn_interval = 40    # frames between spawns
score = 0

def draw_asteroid(rect):
    pygame.draw.circle(screen, GRAY, rect.center,
                       rect.width // 2)
    pygame.draw.circle(screen, (100, 100, 100),
                       rect.center, rect.width // 2, 2)

# ── Score & lives ───────────────────────────────────
score     = 0
lives     = 3
game_over = False

def draw_hud():
    score_surf = font.render(f"Score: {score}", True, WHITE)
    lives_surf = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_surf, (10, 10))
    screen.blit(lives_surf, (WIDTH - 130, 10))

# ── Main loop ───────────────────────────────────────
running = True
while running:
    clock.tick(60)          # cap at 60 frames/second

    for event in pygame.event.get():
        # Quit handler
        if event.type == pygame.QUIT:
            running = False
        # Restart handler
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                player.centerx = WIDTH // 2
                bullets.clear()
                asteroids.clear()
                score     = 0
                lives     = 3
                shoot_cooldown = 0
                spawn_timer    = 0
                game_over = False

    if not game_over:
        # ── Input ─────────────────────────────────────────
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and player.left  > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            bullet = pygame.Rect(player.centerx - 3,
                             player.top - 10, 6, 14)
            bullets.append(bullet)
            shoot_cooldown = 15     # wait 15 frames before next shot

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        # ── Move bullets ─────────────────────────────────
        for b in bullets[:]:
            b.y -= bullet_speed
            if b.bottom < 0:    # off the top of the screen
                bullets.remove(b)

        # ── Spawn asteroids ──────────────────────────────
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            size = random.randint(24, 48)
            x    = random.randint(size, WIDTH - size)
            asteroids.append(
                pygame.Rect(x - size, -size * 2,
                        size * 2,  size * 2))
            asteroid_speed = 3 + score // 5  # gets faster!

        # ── Move asteroids ───────────────────────────────
        for a in asteroids[:]:
            a.y += asteroid_speed
            if a.top > HEIGHT:
                asteroids.remove(a)

        # ── Collision: bullet hits asteroid ──────────────
        for b in bullets[:]:
            for a in asteroids[:]:
                if b.colliderect(a):
                    bullets.remove(b)
                    asteroids.remove(a)
                    score += 1
                    break

        # ── Collision: asteroid hits player ─────────────
        for a in asteroids[:]:
            if a.colliderect(player):
                asteroids.remove(a)
                lives -= 1
                if lives <= 0:
                    game_over = True

    screen.fill(BLACK)
    draw_stars()
    if not game_over:
        # ── Draw ship ────────────────────────────────────
        draw_ship(player)
        # ── Draw bullets ─────────────────────────────────
        for b in bullets:
            pygame.draw.rect(screen, YELLOW, b)
        # ── Draw asteroids ───────────────────────────────
        for a in asteroids:
            draw_asteroid(a)
        draw_hud()
    else:
        over_surf  = big_font.render("GAME OVER", True, RED)
        score_surf = font.render(f"Final Score: {score}", True, WHITE)
        restart    = font.render("Press R to play again", True, GRAY)
        screen.blit(over_surf,  (WIDTH//2 - over_surf.get_width()//2,  HEIGHT//2 - 80))
        screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, HEIGHT//2))
        screen.blit(restart,    (WIDTH//2 - restart.get_width()//2,    HEIGHT//2 + 50))

    pygame.display.flip()

pygame.quit()
