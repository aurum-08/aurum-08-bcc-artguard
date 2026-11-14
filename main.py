import pygame
import sys
import math
import os

# ==================== НАСТРОЙКИ ====================
WIDTH, HEIGHT = 1000, 900
FPS = 60

# Цвета BCC
BG_COLOR = (11, 18, 32)
SAFE_COLOR = (0, 171, 117)       # #00AB75
DANGER_COLOR = (220, 38, 38)     # красный
GOLD = (201, 162, 39)
WHITE = (240, 240, 240)
GRAY = (148, 163, 184)

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BCC ArtGuard — Индикатор безопасности")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont("Arial", 32, bold=True)
font_medium = pygame.font.SysFont("Arial", 22)
font_small = pygame.font.SysFont("Arial", 18)

# ==================== ЗАГРУЗКА КАРТИНОК ====================
def load_image(name):
    if not os.path.exists(name):
        print(f"Ошибка: файл {name} не найден!")
        print("Положи safe.png и danger.png в ту же папку, где лежит этот скрипт.")
        pygame.quit()
        sys.exit()
    img = pygame.image.load(name).convert_alpha()
    return img

safe_img_original = load_image("safe.png")
danger_img_original = load_image("danger.png")

# Масштабируем под окно (оставь место для текста)
IMG_SIZE = 620
safe_img = pygame.transform.smoothscale(safe_img_original, (IMG_SIZE, IMG_SIZE))
danger_img = pygame.transform.smoothscale(danger_img_original, (IMG_SIZE, IMG_SIZE))

# ==================== СОСТОЯНИЕ ====================
status = "safe"          # "safe" или "danger"
transition = 0.0         # 0.0 = полностью safe, 1.0 = полностью danger
transition_speed = 0.025
pulse = 0.0

# ==================== ГЛАВНЫЙ ЦИКЛ ====================
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    # ----- События -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                status = "danger" if status == "safe" else "safe"
            if event.key == pygame.K_ESCAPE:
                running = False

    # ----- Логика перехода -----
    target = 1.0 if status == "danger" else 0.0
    if transition < target:
        transition = min(1.0, transition + transition_speed)
    elif transition > target:
        transition = max(0.0, transition - transition_speed)

    # Пульсация
    pulse += dt * (2.5 if status == "safe" else 5.0)

    # ----- Отрисовка -----
    screen.fill(BG_COLOR)

    # Центр для картинки
    center_x = WIDTH // 2
    center_y = HEIGHT // 2 - 30

    # Эффект пульсации (лёгкое изменение размера)
    pulse_scale = 1.0 + math.sin(pulse) * (0.012 if status == "safe" else 0.025)
    current_size = int(IMG_SIZE * pulse_scale)

    # Масштабируем текущие кадры
    safe_scaled = pygame.transform.smoothscale(safe_img, (current_size, current_size))
    danger_scaled = pygame.transform.smoothscale(danger_img, (current_size, current_size))

    # Позиция
    img_rect = safe_scaled.get_rect(center=(center_x, center_y))

    # Рисуем safe
    screen.blit(safe_scaled, img_rect)

    # Рисуем danger поверх с прозрачностью
    if transition > 0:
        danger_scaled.set_alpha(int(transition * 255))
        screen.blit(danger_scaled, img_rect)

    # ----- Текст -----
    # Заголовок
    title = font_large.render("BCC ArtGuard", True, GOLD)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 55)))

    # Статус
    if status == "safe":
        status_text = "СТАТУС: БЕЗОПАСНО"
        status_color = SAFE_COLOR
    else:
        status_text = "⚠ ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ"
        status_color = DANGER_COLOR

    status_surf = font_medium.render(status_text, True, status_color)
    screen.blit(status_surf, status_surf.get_rect(center=(WIDTH // 2, HEIGHT - 95)))

    # Подсказка
    hint = font_small.render("Пробел — сменить статус    |    Esc — выход", True, GRAY)
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 50)))

    # Небольшая линия под заголовком
    pygame.draw.line(screen, GOLD, (WIDTH//2 - 120, 85), (WIDTH//2 + 120, 85), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()