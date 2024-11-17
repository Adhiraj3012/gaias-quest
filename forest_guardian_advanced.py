import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gaia's Quest")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Load assets
player_img = pygame.image.load("aria.png")
player_img = pygame.transform.scale(player_img, (50, 50))

boss_sprites = [
    pygame.image.load("trashtitan.png"),
    pygame.image.load("oilbeast.png"),
    pygame.image.load("smogzilla.png")
]
boss_sprites = [pygame.transform.scale(sprite, (100, 100)) for sprite in boss_sprites]

backgrounds = [
    pygame.image.load("level1bg.png"),
    pygame.image.load("lvl2bg.png"),
    pygame.image.load("lvl3bg.png")
]
backgrounds = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in backgrounds]

boss_attack_sprites = [
    pygame.image.load("trashcan.png"),
    pygame.image.load("oilb.png"),
    pygame.image.load("emission.png")
]
boss_attack_sprites = [pygame.transform.scale(attack, (15, 15)) for attack in boss_attack_sprites]

# Player setup
player_x, player_y = WIDTH // 2, HEIGHT - 100
player_speed = 5
player_health = 250
player_max_health = 250

# Bullets
bullet_img = pygame.Surface((10, 10))
bullet_img.fill(WHITE)
bullets = []
bullet_speed = -10
can_shoot = False
shoot_timer = 0
shoot_interval = random.randint(300, 660)  # Randomize interval (5-11 seconds)
shoot_duration = random.randint(300, 420)  # Shooting period duration (5-7 seconds)

# Boss setup
bosses = [
    {"health": 3000, "speed": 3, "fire_rate": 0.01},  # Level 1
    {"health": 6000, "speed": 4, "fire_rate": 0.02},  # Level 2
    {"health": 10000, "speed": 5, "fire_rate": 0.03},  # Level 3
]
current_boss_level = 0
boss_health = bosses[current_boss_level]["health"]
boss_x, boss_y = WIDTH // 2 - 50, 50
boss_bullets = []

# Game state
running = True
game_over = False
victory = False


def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def reset_level():
    """Resets the level for the current boss."""
    global player_x, player_y, player_health, bullets, boss_bullets, game_over, victory, can_shoot, shoot_timer, shoot_interval, shoot_duration
    global boss_x, boss_y, boss_health
    player_x, player_y = WIDTH // 2, HEIGHT - 100
    player_health = player_max_health
    bullets = []
    boss_bullets = []
    game_over = False
    victory = False
    can_shoot = False
    shoot_timer = 0
    boss_x, boss_y = WIDTH // 2 - 50, 50
    boss_health = bosses[current_boss_level]["health"]
    shoot_interval = random.randint(300, 660)  # Reset shooting interval
    shoot_duration = random.randint(300, 420)  # Reset shooting period


def next_level():
    """Moves to the next boss level or ends the game if all bosses are defeated."""
    global current_boss_level, boss_health, player_health
    current_boss_level += 1
    if current_boss_level < len(bosses):
        boss_health = bosses[current_boss_level]["health"]
        player_health = player_max_health
        reset_level()
    else:
        global victory
        victory = True


while running:
    # Draw background
    screen.blit(backgrounds[current_boss_level], (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > boss_y + 150:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < boss_y + 400:
        player_y += player_speed

    # Handle shooting
    shoot_timer += 1

    if not can_shoot and shoot_timer >= shoot_interval:
        can_shoot = True
        shoot_timer = 0
        shoot_duration = random.randint(300, 420)  # Randomize the shooting period (5-7 seconds)

    if can_shoot and shoot_timer >= shoot_duration:
        can_shoot = False
        shoot_timer = 0
        shoot_interval = random.randint(300, 660)  # Randomize the next interval (5-11 seconds)

    if keys[pygame.K_SPACE] and can_shoot and len(bullets) < 5:
        bullets.append([player_x + 20, player_y])

    # Update bullets
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        elif boss_x < bullet[0] < boss_x + 100 and boss_y < bullet[1] < boss_y + 100:
            boss_health -= 10
            bullets.remove(bullet)

    # Boss attacks
    boss_speed = bosses[current_boss_level]["speed"]
    fire_rate = bosses[current_boss_level]["fire_rate"]

    if not game_over and random.random() < fire_rate:
        dx = player_x + 25 - (boss_x + 50)
        dy = player_y + 25 - (boss_y + 50)
        distance = math.hypot(dx, dy)
        if distance != 0:
            vx = boss_speed * (dx / distance)
            vy = boss_speed * (dy / distance)
            boss_bullets.append([boss_x + 50, boss_y + 50, vx, vy])

    for boss_bullet in boss_bullets[:]:
        boss_bullet[0] += boss_bullet[2]
        boss_bullet[1] += boss_bullet[3]
        if boss_bullet[1] > HEIGHT or boss_bullet[0] < 0 or boss_bullet[0] > WIDTH:
            boss_bullets.remove(boss_bullet)
        elif player_x < boss_bullet[0] < player_x + 50 and player_y < boss_bullet[1] < player_y + 50:
            player_health -= 10
            boss_bullets.remove(boss_bullet)

    # Check game state
    if player_health <= 0:
        game_over = True
    if boss_health <= 0:
        next_level()

    # Draw entities
    screen.blit(player_img, (player_x, player_y))
    screen.blit(boss_sprites[current_boss_level], (boss_x, boss_y))

    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    for boss_bullet in boss_bullets:
        screen.blit(boss_attack_sprites[current_boss_level], (boss_bullet[0], boss_bullet[1]))

    import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gaia's Quest")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Load assets
player_img = pygame.image.load("aria.png")
player_img = pygame.transform.scale(player_img, (50, 50))

boss_sprites = [
    pygame.image.load("trashtitan.png"),
    pygame.image.load("oilbeast.png"),
    pygame.image.load("smogzilla.png")
]
boss_sprites = [pygame.transform.scale(sprite, (100, 100)) for sprite in boss_sprites]

backgrounds = [
    pygame.image.load("level1bg.png"),
    pygame.image.load("lvl2bg.png"),
    pygame.image.load("lvl3bg.png")
]
backgrounds = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in backgrounds]

boss_attack_sprites = [
    pygame.image.load("trashcan.png"),
    pygame.image.load("oilb.png"),
    pygame.image.load("emission.png")
]
boss_attack_sprites = [pygame.transform.scale(attack, (15, 15)) for attack in boss_attack_sprites]

# Player setup
player_x, player_y = WIDTH // 2, HEIGHT - 100
player_speed = 5
player_health = 250
player_max_health = 250

# Bullets
bullet_img = pygame.Surface((10, 10))
bullet_img.fill(WHITE)
bullets = []
bullet_speed = -10
can_shoot = False
shoot_timer = 0
shoot_interval = random.randint(300, 660)  # Randomize interval (5-11 seconds)
shoot_duration = random.randint(300, 420)  # Shooting period duration (5-7 seconds)

# Boss setup
bosses = [
    {"health": 3000, "speed": 3, "fire_rate": 0.01},  # Level 1
    {"health": 6000, "speed": 4, "fire_rate": 0.02},  # Level 2
    {"health": 10000, "speed": 5, "fire_rate": 0.03},  # Level 3
]
current_boss_level = 0
boss_health = bosses[current_boss_level]["health"]
boss_x, boss_y = WIDTH // 2 - 50, 50
boss_bullets = []

# Game state
running = True
game_over = False
victory = False


def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def reset_level():
    """Resets the level for the current boss."""
    global player_x, player_y, player_health, bullets, boss_bullets, game_over, victory, can_shoot, shoot_timer, shoot_interval, shoot_duration
    global boss_x, boss_y, boss_health
    player_x, player_y = WIDTH // 2, HEIGHT - 100
    player_health = player_max_health
    bullets = []
    boss_bullets = []
    game_over = False
    victory = False
    can_shoot = False
    shoot_timer = 0
    boss_x, boss_y = WIDTH // 2 - 50, 50
    boss_health = bosses[current_boss_level]["health"]
    shoot_interval = random.randint(300, 660)  # Reset shooting interval
    shoot_duration = random.randint(300, 420)  # Reset shooting period


def next_level():
    """Moves to the next boss level or ends the game if all bosses are defeated."""
    global current_boss_level, boss_health, player_health
    current_boss_level += 1
    if current_boss_level < len(bosses):
        boss_health = bosses[current_boss_level]["health"]
        player_health = player_max_health
        reset_level()
    else:
        global victory
        victory = True


while running:
    # Draw background
    screen.blit(backgrounds[current_boss_level], (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > boss_y + 150:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < boss_y + 400:
        player_y += player_speed

    # Handle shooting
    shoot_timer += 1

    if not can_shoot and shoot_timer >= shoot_interval:
        can_shoot = True
        shoot_timer = 0
        shoot_duration = random.randint(300, 420)  # Randomize the shooting period (5-7 seconds)

    if can_shoot and shoot_timer >= shoot_duration:
        can_shoot = False
        shoot_timer = 0
        shoot_interval = random.randint(300, 660)  # Randomize the next interval (5-11 seconds)

    if keys[pygame.K_SPACE] and can_shoot and len(bullets) < 5:
        bullets.append([player_x + 20, player_y])

    # Update bullets
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        elif boss_x < bullet[0] < boss_x + 100 and boss_y < bullet[1] < boss_y + 100:
            boss_health -= 10
            bullets.remove(bullet)

    # Boss attacks
    boss_speed = bosses[current_boss_level]["speed"]
    fire_rate = bosses[current_boss_level]["fire_rate"]

    if not game_over and random.random() < fire_rate:
        dx = player_x + 25 - (boss_x + 50)
        dy = player_y + 25 - (boss_y + 50)
        distance = math.hypot(dx, dy)
        if distance != 0:
            vx = boss_speed * (dx / distance)
            vy = boss_speed * (dy / distance)
            boss_bullets.append([boss_x + 50, boss_y + 50, vx, vy])

    for boss_bullet in boss_bullets[:]:
        boss_bullet[0] += boss_bullet[2]
        boss_bullet[1] += boss_bullet[3]
        if boss_bullet[1] > HEIGHT or boss_bullet[0] < 0 or boss_bullet[0] > WIDTH:
            boss_bullets.remove(boss_bullet)
        elif player_x < boss_bullet[0] < player_x + 50 and player_y < boss_bullet[1] < player_y + 50:
            player_health -= 10
            boss_bullets.remove(boss_bullet)

    # Check game state
    if player_health <= 0:
        game_over = True
    if boss_health <= 0:
        next_level()

    # Draw entities
    screen.blit(player_img, (player_x, player_y))
    screen.blit(boss_sprites[current_boss_level], (boss_x, boss_y))

    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    for boss_bullet in boss_bullets:
        screen.blit(boss_attack_sprites[current_boss_level], (boss_bullet[0], boss_bullet[1]))

    # Draw health bars
    pygame.draw.rect(screen, RED, (50, HEIGHT - 50, 200, 20))
    pygame.draw.rect(screen, GREEN, (50, HEIGHT - 50, 200 * (player_health / player_max_health), 20))
    pygame.draw.rect(screen, RED, (WIDTH - 250, 50, 200, 20))
    pygame.draw.rect(screen, GREEN, (WIDTH - 250, 50, 200 * (boss_health / bosses[current_boss_level]["health"]), 20))

    # Text
    draw_text("Player Health", 50, HEIGHT - 80)
    draw_text("Boss Health", WIDTH - 250, 20)
    draw_text(f"Level: {current_boss_level + 1}", WIDTH // 2 - 50, 20)

    if can_shoot:
        draw_text("Shoot Now!", WIDTH // 2 - 50, HEIGHT - 80, GREEN)

    if game_over:
        draw_text("GAME OVER", WIDTH // 2 - 100, HEIGHT // 2, RED)
        draw_text("Press R to Restart", WIDTH // 2 - 120, HEIGHT // 2 + 40)
        if keys[pygame.K_r]:
            current_boss_level = 0
            reset_level()

    if victory:
        draw_text("VICTORY!", WIDTH // 2 - 100, HEIGHT // 2, GREEN)
        draw_text("Press R to Restart", WIDTH // 2 - 120, HEIGHT // 2 + 40)
        if keys[pygame.K_r]:
            current_boss_level = 0
            reset_level()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
    