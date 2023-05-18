import pygame
import sys
import subprocess
import random
import math


def fire_bullet(x, y, bullet_state):
    bullet_state = "fire"
    bullet_pos = (x + 16, y + 10)
    return bullet_state, bullet_pos


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        math.pow(enemyX - bulletX, 2) +
        math.pow(enemyY - bulletY, 2)
    )
    if distance < 27.0:
        return True
    else:
        return False


# Инициализация библиотеки pygame и mixer
pygame.init()
pygame.mixer.init()

# Задаем параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Заголовок и иконка
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('Image/space-invaders.png')
pygame.display.set_icon(icon)

# Игрок
player_img = pygame.image.load('Image/space-invaders-ship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Враг
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('Image/alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(64, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40.0)

# Пуля
bullet_img = pygame.image.load('Image/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Фон
background = pygame.image.load('Image/Background.jpg')

# Музыка
pygame.mixer.music.load("Music/SpaceInvadersTheme.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
stop_main_music = False

shoot_sound = pygame.mixer.Sound("Music/SpaceInvadersShoot.wav")
shoot_sound.set_volume(0.35)

hit_sound = pygame.mixer.Sound("Music/SpaceInvadersHit.wav")
hit_sound.set_volume(0.4)

lose_sound = pygame.mixer.Sound("Music/SpaceInvadersLose.wav")
lose_sound.set_volume(0.2)

# Очки текст
score_value = 0
score_font = pygame.font.Font('Font/VT323-Regular.ttf', 32)
textX = 10
textY = 10

# Конец игры текст
over_font = pygame.font.Font('Font/VT323-Regular.ttf', 128)


def show_score(x, y, score_value):
    score_text = "Score: " + str(score_value)
    score = score_font.render(score_text, True, (255, 255, 255))

    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (180, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# Бесконечный цикл работы программы
while True:
    # Цвет экрана
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            subprocess.Popen(['python', 'Code/main.py'])
            print("Запуск меню игры")
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    shoot_sound.play()
                    bullet_state, bullet_pos = fire_bullet(
                        playerX, bulletY, bullet_state
                    )

                    bulletX, bulletY = bullet_pos

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Проверка выхода игрока за границы карты
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Движение врага
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            pygame.mixer.music.stop()
            stop_main_music = True
            game_over_text()
            show_score(350, 400, score_value)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Колизия
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            hit_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(64, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Звук проигрыша
    if stop_main_music:
        lose_sound.play(1)
        stop_main_music = False

    # Движение пули
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        screen.blit(bullet_img, (bulletX + 16, bulletY + 10))
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY, score_value)
    pygame.display.update()
