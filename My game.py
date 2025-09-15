

import pygame
import random
import time
import mysql.connector

dbconfig = {
    'host': 'localhost',
    'user': 'root',
    'password': '',    #your password from Sql
    'database': ''                   #name of your database
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor(buffered=True)


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

#Шрифты
font1 = pygame.font.SysFont("arial",36)
font2 = pygame.font.Font(None,30)
font3 = pygame.font.Font(None, 50)


# Размеры дисплея и ФПС
WIDTH = 600
HEIGHT = 600
FPS = 60

# Цвета
PINK = (255,20,147)
YELLOW = (255,255,0)


# Настройки фона и дисплейя
pygame.display.set_icon(pygame.image.load("Patick_main.jpg"))
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Patriks' dream")
clock = pygame.time.Clock()

 # Загрузка картинок
player = pygame.image.load('Patrick.png')
bg = pygame.image.load('Krusty Krab.png')
Jellyfish = pygame.image.load('Jellyfish.png')
Patty = pygame.image.load('KrabbyPatty.png')

# Размеры персонажа и объектов
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
player = pygame.transform.scale(player, (100, 100))
Jellyfish = pygame.transform.scale(Jellyfish, (50, 50))
Patty = pygame.transform.scale(Patty, (50, 50))

# Глобальные переменные
run = True
lives = 3
game_score = 0
player_speed = 100
x_change = 0

# Функции
def score():
    cursor.execute('''SELECT MAX(best_score) FROM games_best''')
    best_score = cursor.fetchone()[0]
    # print(best_score)
    if game_score > best_score:
        best_score = game_score
        cursor.execute(f'''update games_best set best_score = {best_score}''')
        _SQL = f'''insert into games_best (score, best_score) values ({game_score}, {best_score}) '''
    else:
        _SQL = f'''insert into games_best (score, best_score) values ({game_score}, {best_score}) '''
    cursor.execute(_SQL)
    conn.commit()


def best_score_text(x, y):
    cursor.execute('''SELECT MAX(best_score) FROM games_best''')
    best_score = cursor.fetchone()[0]
    best_surface = font2.render(f"Best score: {best_score}", True, (YELLOW))
    window.blit(best_surface, (x, y))


def menu_text():
    name_surface = font3.render("Patriks' dream", True, (PINK))
    window.blit(name_surface, (WIDTH / 2 - 140, HEIGHT / 2 - 100))

    game_surface = font2.render("Click left mouse button to start!", True, (YELLOW))
    window.blit(game_surface, (WIDTH / 2 - 150, HEIGHT / 2))


def lives_and_score_text():
    lives_surface = font1.render(f'Lives left: {lives}', True, (YELLOW))
    window.blit(lives_surface, (0, 0))

    score_surface = font1.render(f'Score: {game_score}', True, (YELLOW))
    window.blit(score_surface, (400, 0))


def game_over_text():
    game_surface = font1.render('Game Over', True, (YELLOW))
    window.blit(game_surface, (200, 150))

    score_surface = font1.render(f'You score: {game_score}', True, (YELLOW))
    window.blit(score_surface, (WIDTH / 2 - 125, HEIGHT / 2 - 70))

    restart_surface = font2.render("Press R to restart game", True, (YELLOW))
    window.blit(restart_surface, (WIDTH / 2 - 125, HEIGHT / 2))


def add_player(x, y):
    window.blit(player, (x, y))


# Скорость и расположение персонажа и объектов
x = 0
y = (HEIGHT * 0.86)

jellyfish_x = random.randrange(0, WIDTH + 1, 100)
jellyfish_y = 0
jellyfish_speed = 10

patty_x = random.randrange(0, WIDTH + 1, 100)
patty_y = 0
patty_speed = 10


def jellyfish_spawn(x, y):
    window.blit(Jellyfish, (x, y))


def patty_spawn(x, y):
    window.blit(Patty, (x, y))


# Звки
GameMode = "menu"
pygame.mixer.music.load('Patrikstheme.mp3')
pygame.mixer.music.set_volume(0.04)
pygame.mixer.music.play(-1)

jellyfish_sound = pygame.mixer.Sound("electricity.mp3")
jellyfish_sound.set_volume(0.1)
patty_sound = pygame.mixer.Sound("Patrikslove.mp3")
patty_sound.set_volume(0.1)


# Главное тело игры
while run:
    if GameMode == "play":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT or i.key == pygame.K_a:
                    x_change = -player_speed
                elif i.key == pygame.K_RIGHT or i.key == pygame.K_d:
                    x_change = +player_speed
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT or i.key == pygame.K_d or i.key == pygame.K_a:
                    x_change = 0

            if x + x_change < 0 or x + x_change >= WIDTH:
                x_change = 0

            x += x_change

        jellyfish_y += jellyfish_speed
        if jellyfish_y >= HEIGHT:
            jellyfish_y = 0
            jellyfish_x = random.randrange(0, WIDTH + 1, 100)

        patty_y += patty_speed
        if patty_y >= HEIGHT:
            patty_y = 0
            patty_x = random.randrange(0, WIDTH + 1, 100)

        window.blit(bg, (0, 0))
        add_player(x, y)
        jellyfish_spawn(jellyfish_x, jellyfish_y)
        patty_spawn(patty_x, patty_y)

        player_rect = player.get_rect(midbottom=(x, y))
        jellyfish_rect = Jellyfish.get_rect(midbottom=(jellyfish_x, jellyfish_y))
        patty_rect = Patty.get_rect(midbottom=(patty_x, patty_y))

        if player_rect.colliderect(jellyfish_rect):
            jellyfish_sound.play()
            lives -= 1
            jellyfish_y = 0
            jellyfish_x = random.randrange(0, WIDTH + 1, 100)
        elif player_rect.colliderect(patty_rect):
            patty_sound.play()
            game_score += 10
            patty_y = 0
            patty_x = random.randrange(0, WIDTH + 1, 100)

        lives_and_score_text()

        if lives <= 0:
            time.sleep(2)
            score()
            GameMode = "game over"

    elif GameMode == "menu":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    GameMode = "play"

        window.blit(bg, (0, 0))
        menu_text()
        best_score_text(250, 400)

    elif GameMode == "game over":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_r:
                    lives = 3
                    game_score = 0
                    GameMode = "play"

        window.blit(bg, (0, 0))
        best_score_text(100, 20)
        game_over_text()

    pygame.display.update()
    clock.tick(FPS)

cursor.close()
conn.close()
pygame.quit()