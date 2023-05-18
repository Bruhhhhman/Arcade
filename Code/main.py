import pygame
import sys
import subprocess
from pygame import mixer

# Инициализация Pygame
pygame.init()

# Фон
background = pygame.image.load('Image/MenuBackground.jpg')

# Создание окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Arcade")
icon = pygame.image.load('Image/arcade.png')
pygame.display.set_icon(icon)

# Загрузка изображений для кнопок
button1_image = pygame.image.load("Image/MenuSpaceInvadersBtn.png")
button2_image = pygame.image.load("Image/MenuPongBtn.png")
button3_image = pygame.image.load("Image/MenuExitBtn.png")

# Размещение кнопок на экране
button1_rect = button1_image.get_rect(center=(400, 350 - 50))
button2_rect = button2_image.get_rect(center=(400, 350 + 50))
button3_rect = button3_image.get_rect(center=(400, 350 + 150))

# Заголовок меню
arcade_font = pygame.font.Font('Font/VT323-Regular.ttf', 180)


def arcade_text():
    arcade_text = arcade_font.render("ARCADE", True, (255, 255, 255))
    screen.blit(arcade_text, (190, 80))


# Музыка
mixer.music.load("Music/MenuTheme.wav")
mixer.music.set_volume(0.4)
mixer.music.play(-1)

click_sound = mixer.Sound("Music/MenuChoise.wav")
click_sound.set_volume(0.3)

# Основной цикл программы
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button1_rect.collidepoint(event.pos):
                click_sound.play()
                subprocess.Popen(['python', 'Code/SpaceInvaders.py'])
                print("Запуск первой игры")
                pygame.time.delay(500)
                pygame.quit()
                sys.exit()
            elif button2_rect.collidepoint(event.pos):
                click_sound.play()
                subprocess.Popen(['python', 'Code/Pong.py'])
                print("Запуск второй игры")
                pygame.time.delay(500)
                pygame.quit()
                sys.exit()
            elif button3_rect.collidepoint(event.pos):
                click_sound.play()
                print("Выход из игры")
                pygame.time.delay(500)
                pygame.quit()
                sys.exit()

    screen.blit(background, (0, 0))
    arcade_text()

    # Отрисовка кнопок
    screen.blit(button1_image, button1_rect)
    screen.blit(button2_image, button2_rect)
    screen.blit(button3_image, button3_rect)

    # Обновление экрана
    pygame.display.flip()
