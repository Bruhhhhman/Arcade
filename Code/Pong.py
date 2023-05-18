import pygame
import sys
import random
import subprocess


def ball_animation(
    ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
):
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(hit_sound)
        ball_speed_y *= -1

    # Счет игрока
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1

    # Счет противника
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    # Колайдеры
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(hit_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(hit_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    return ball_speed_x, ball_speed_y, player_score, opponent_score, score_time


def player_animation(player_speed):
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

    return player_speed


def opponent_ai(opponent_speed):
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

    return opponent_speed


def opponent_animation(opponent_speed):
    opponent.y += opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

    return opponent_speed


def ball_start(ball_speed_x, ball_speed_y, score_time):
    ball.center = (screen_width/2, screen_height/2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = basic_font.render("3", False, white)
        screen.blit(number_three, (screen_width/2 - 5, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = basic_font.render("2", False, white)
        screen.blit(number_two, (screen_width/2 - 6, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = basic_font.render("1", False, white)
        screen.blit(number_one, (screen_width/2 - 5, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_y = 0
        ball_speed_x = 0
    else:
        ball_speed_x = 6 * random.choice((1, -1))
        ball_speed_y = 6 * random.choice((1, -1))
        score_time = None

    return ball_speed_x, ball_speed_y, score_time


# Инициализация библиотеки pygame
pygame.init()
clock = pygame.time.Clock()

# Задаем параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')
icon = pygame.image.load('Image/pong-icon.png')
pygame.display.set_icon(icon)

# Цвета
light_blue = (65, 180, 247)
light_red = (229, 89, 117)
white = (255, 255, 255)
light_grey = (200, 200, 200)
bg_color = pygame.Color(70, 79, 84)

# Игровые объекты
ball = pygame.Rect(screen_width / 2 - 13, screen_height / 2 - 13, 26, 26)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 60, 10, 120)
opponent = pygame.Rect(10, screen_height / 2 - 60, 10, 120)

# Переменная отвечающая за реализацию мультиплейерой
multiplayer = True

# Переменные скорости
ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = 6 * random.choice((1, -1))
player_speed = 0
if multiplayer:
    opponent_speed = 0
else:
    opponent_speed = 6
ball_moving = False
score_time = True

# Переменные подсчета очков
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('Font/VT323-Regular.ttf', 32)

# Музыка
pygame.mixer.music.load("Music/PongTheme.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

score_sound = pygame.mixer.Sound("Music/PongScore.wav")
score_sound.set_volume(0.5)

hit_sound = pygame.mixer.Sound("Music/PongHit.wav")
hit_sound.set_volume(0.4)


# Бесконечный цикл работы программы
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            subprocess.Popen(['python', 'Code/main.py'])
            print("Запуск меню игры")
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 6
            if event.key == pygame.K_DOWN:
                player_speed += 6
            if multiplayer:
                if event.key == pygame.K_w:
                    opponent_speed -= 6
                    print("Зажата w")
                if event.key == pygame.K_s:
                    opponent_speed += 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 6
            if event.key == pygame.K_DOWN:
                player_speed -= 6
            if multiplayer:
                if event.key == pygame.K_w:
                    opponent_speed += 6
                if event.key == pygame.K_s:
                    opponent_speed -= 6

    # Анимация
    (ball_speed_x, ball_speed_y, player_score, opponent_score,
        score_time) = ball_animation(
        ball_speed_x, ball_speed_y, player_score, opponent_score, score_time)

    player_speed = player_animation(player_speed)

    if multiplayer:
        opponent_speed = opponent_animation(opponent_speed)
    else:
        opponent_speed = opponent_ai(opponent_speed)

    # Визуализация объектов
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_blue, player)
    pygame.draw.rect(screen, light_red, opponent)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),
                       (screen_width / 2, screen_height))
    pygame.draw.ellipse(screen, white, ball)

    if score_time:
        ball_speed_x, ball_speed_y, score_time = ball_start(
            ball_speed_x, ball_speed_y, score_time)

    player_text = basic_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (410, 290))

    opponent_text = basic_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (375, 290))

    pygame.display.flip()
    clock.tick(60)
