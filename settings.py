# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
from os import path

#Объявляем переменные цветов
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (20, 20, 20)

# пути к папкам игры
game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')
music_folder = path.join(game_folder, 'assets/music')
sounds_folder = path.join(game_folder, 'assets/sounds')
images_folder = path.join(game_folder, 'assets/images')
fonts_folder = path.join(game_folder, 'assets/fonts')

# основные параметры игры
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
TOTAL_LEVEL_WIDTH = 0 # полная ширина уровня
TOTAL_LEVEL_HEIGHT = 0 # полная высота уровня
FPS = 60 # количество кадров в секунду
NAME = '' # имя игрока по умолчанию
ENEMIES_SPAWN_COORDINATES = [] # координаты возрождения врагов
NIGHT = False # ночь
SELECTED_MODE = 'mode: NORMAL' # выбранный режим игры
BACKGROUND_MUSIC = 'third.ogg' # фоновая музыка
MUSIC_VOLUME = 0.05 # громкось музыки

# параметры ночного режима
NIGHT_COLOR = (0, 0, 0) # ночная заливка
LIGHT_RADIUS = (500, 500) # радиус света
LIGHT_MASK = "light_350_med.png" # маска света

# параметры игрока
MOVE_SPEED = 1 # скорость игрока
PLAYER_HEALTH = 100 # здоровье игрока
ENEMIES_KILLED = 0 # убито врагов
POINT_PRICE = 10 # цена очка
DAMAGE_ALPHA = [i for i in range(0, 255, 55)] # эффект урона
PLAYERS_TANK_IMAGE = path.join(images_folder, 'players_tank.png') # изобрадение игрока
PLAYER_SHOT_SOUND = 'player_shot.wav' # звук выстрела
PLAYER_RIDE_SOUND = 'player_ride.wav' # звук передвижения
LEVEL_START_SOUND = 'level_start.wav' # звук начала уровня

# параметры врагов
ENEMY_SPEED = 2 # скорость врагов
ENEMY_KICK = 15 # отдача врагов
ENEMY_DAMAGE = 20 # урон врагов
ENEMY_TANK_IMAGE = path.join(images_folder, 'enemies_tank.png') # изображение врагов
ENEMY_HIT_SOUND = 'enemy_hit.wav' # звук ударв врагов

# параметры снарядов
AMMUNITION = 5 # боезапас
BULLET_SPEED = 6 # скорость снаряда
BULLET_LIFETIME = 1000 # время жизни снаряда
BULLET_X, BULLET_Y = 1, 0 # направление полёта
KICKBACK = 3 # отдача от выстрела
BULLET_IMAGE = path.join(images_folder, 'bullet.png') # изображение снаряда

# эффекты
# изображения облаков стрельбы
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png',
                  'whitePuff17.png', 'whitePuff18.png']

# изображения взрывов
BOOM_FLASHES = ['boom_flashes_1.png', 'boom_flashes_2.png',
                'boom_flashes_3.png', 'boom_flashes_4.png']
EXPLOSION_SOUND = 'explosion.wav' # звук взрыва
FLASH_DURATION = 40 # длительность облака выстрела
KILL_FLASH_DURATION = 150 # длительность взрыва
EFFECTS_LAYER = 4
kill_flashes = []

# просто Рикардо
RICARDO_IMAGE = path.join(images_folder, 'ricardo.png')
RICARDO_SOUND = 'ricardo.wav'

