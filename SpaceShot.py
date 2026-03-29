import pygame
import random
import os
import sys

# --- Function to get correct path for .py or EXE ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Pygame init ---
pygame.init()
pygame.mixer.init()

# --- Window setup ---
WIDTH, HEIGHT = 600, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceShot")

# --- Load & scale images ---
player_img = pygame.image.load(resource_path("spaceship.png"))
player_img = pygame.transform.scale(player_img, (80, 80))

enemy_img = pygame.image.load(resource_path("alien.png"))
enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# --- Colors ---
WHITE = (255, 255, 255)
bg_color = (0, 0, 0)

# --- Load sounds ---
laser_sound = pygame.mixer.Sound(resource_path("laser.wav"))
explosion_sound = pygame.mixer.Sound(resource_path("explosion.wav"))

# --- Player setup ---
player_x = WIDTH // 2 - player_img.get_width() // 2
player_y = HEIGHT - player_img.get_height() - 10
player_vel = 5
bullets = []

# --- Enemy setup ---
enemies = []
enemy_width, enemy_height = enemy_img.get_width(), enemy_img.get_height()

# --- Screen shake ---
shake_offset = [0, 0]
shake_timer = 0

# --- Score ---
score = 0
font = pygame.font.SysFont("comicsans", 30)

# --- Shooting control ---
shoot_cooldown = 0  # frames until next shot

# --- Clock ---
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(60)
    win.fill(bg_color)

    # --- Spawn enemies ---
    if random.randint(0, 50) == 1:
        enemies.append([random.randint(0, WIDTH - enemy_width), 0])

    # --- Draw player with shake ---
    win.blit(player_img, (player_x + shake_offset[0], player_y + shake_offset[1]))

    # --- Draw enemies ---
    for enemy in enemies[:]:
        enemy[1] += 2
        win.blit(enemy_img, (enemy[0] + shake_offset[0], enemy[1] + shake_offset[1]))
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # --- Draw and handle bullets ---
    for bullet in bullets[:]:
        bullet[1] -= 7
        if bullet[1] < 0:
            bullets.remove(bullet)
            continue

        pygame.draw.rect(win, WHITE, (*bullet, 5, 10))

        for enemy in enemies[:]:
            if (bullet[0] < enemy[0] + enemy_width and
                bullet[0] + 5 > enemy[0] and
                bullet[1] < enemy[1] + enemy_height and
                bullet[1] + 10 > enemy[1]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                shake_timer = 5
                score += 10
                explosion_sound.play()
                break

    # --- Screen shake ---
    if shake_timer > 0:
        shake_offset = [random.randint(-5, 5), random.randint(-5, 5)]
        shake_timer -= 1
    else:
        shake_offset = [0, 0]

    # --- Draw score ---
    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

    pygame.display.update()

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # --- Player movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_vel > 0:
        player_x -= player_vel
    if keys[pygame.K_RIGHT] and player_x + player_vel + player_img.get_width() < WIDTH:
        player_x += player_vel

    # --- Shooting bullets with cooldown ---
    if keys[pygame.K_SPACE] and shoot_cooldown == 0:
        bullets.append([player_x + player_img.get_width() // 2 - 2, player_y])
        laser_sound.play()
        shoot_cooldown = 15  # frames until next shot

    if shoot_cooldown > 0:
        shoot_cooldown -= 1

pygame.quit()
