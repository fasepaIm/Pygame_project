# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
import pygame
import os
import random
from random import choice
import pytmx
from os import path
from pygame import *
# импортируем из файлов
from settings import *
from records import *
from input_box import *
from sprites import *
from tiled_map import *
from particles import *


PARTICLE_EVENT = pygame.USEREVENT + 1 # событие для частиц
ENEMIES_EVENT = pygame.USEREVENT      # событие для возрождения врагов
AMMUNITION_EVENT = pygame.USEREVENT   # событие для перезарядки
pygame.init() # Инициация PyGame

# класс объектов (создаём спрайты и присваиваем им параметры)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, walls, x, y, w, h):
        self.groups = walls
        pygame.sprite.Sprite.__init__(self, self.groups) # добавляем спрайт в группу walls
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

# пасхалка
class Woo(pygame.sprite.Sprite):
    def __init__(self, all_sprites, camera):
        super().__init__(all_sprites)
        self.image = image.load(RICARDO_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = camera[0], camera[1]
        self.go = True
        self.camera = camera

    def update(self, player):
        if self.rect.right > self.camera[0] - 10 and self.go:
            self.rect.x -= 10
        else:
            self.kill()

# класс для создания тумана/ночного освещения
class Fog:
    def __init__(self, screen, camera, player):
        self.screen = screen
        self.camera = camera
        self.player = player
        self.fog = pygame.Surface((WIN_WIDTH, WIN_HEIGHT)) # создаём слой
        self.fog.fill(NIGHT_COLOR) # заливаем слой цветом
        self.light_mask = pygame.image.load(path.join(images_folder, LIGHT_MASK)).convert_alpha() # загружем маску
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS) # изменяем размеры маски
        self.light_rect = self.light_mask.get_rect() # получаем размеры маски

    # функция отрисовки тумана
    def render_fog(self):
        self.fog.fill(NIGHT_COLOR) # заливаем слой цветом
        self.light_rect.center = self.camera.apply(self.player).center # центруем маску
        self.fog.blit(self.light_mask, self.light_rect) # накадываем маску на слой
        self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT) # отображем слой на экране

# класс камеры
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
	
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def apply_rect(self, rect):
        return rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы
    return Rect(l, t, w, h)

# функция основного меню
def menu_show():
    global SELECTED_MODE
    menu_background = pygame.image.load(path.join(images_folder, 'menu.jpg')) # загружаем изображение фона
    input_box = InputBox(WIN_WIDTH / 9, WIN_HEIGHT / 2 - 10, 265, 40) # добавляем поле ввода
    show = True # переменная показа окна
    screen = pygame.display.set_mode(DISPLAY) # создаём окно
    icon = pygame.image.load(path.join(images_folder, ICON))
    pygame.display.set_icon(icon) # меняем иконку программы
    pygame.display.set_caption('Pytanks 2D') # Пишем в шапку
    clock = pygame.time.Clock() # добавляем часы
    while show: # Основной цикл программы
        clock.tick(FPS) # ограничиваем частоту отрисовки кадров
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT: # если выйти
                show = False # цикл останавливается
            if event.type == MOUSEBUTTONDOWN: # если нажали на кнопку мыши
                draw_main_menu_button(screen, event) # вызываем метод для отрисовки кнопок
            input_box.handle_event(event)
        screen.blit(menu_background, (0, 0)) # добавляем фон
        text_print(screen, WIN_WIDTH / 9, WIN_HEIGHT / 2 - 40, 'Enter a name and press ENTER:',
                   path.join(fonts_folder, '20219.ttf'), WHITE, 20, False)
        draw_main_menu_button(screen) # отрисовываем кнопки
        input_box.draw(screen) # отрисовываем поле ввода
        drawing_of_records(screen) # отрисовываем таблицу рекордов
        pygame.display.update() # обновление и вывод всех изменений на экран

# функция отрисовки кнопок в меню
def draw_main_menu_button(screen, mouse_click=False):
    global SELECTED_MODE, NIGHT, LIGHT_MASK, ENEMY_SPEED, BACKGROUND_MUSIC, MUSIC_VOLUME
    play_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 40, WIN_WIDTH / 3, 50) # создаём прямоугольник
    draw_button(screen, play_button, 'Play game') # рисуем кнопку

    tutorial_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 100, WIN_WIDTH / 3, 50) # создаём прямоугольник
    draw_button(screen, tutorial_button, 'Tutorial') # рисуем кнопку

    mode_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 160, WIN_WIDTH / 3, 50) # создаём прямоугольник
    draw_button(screen, mode_button, SELECTED_MODE) # рисуем кнопку

    quit_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 220, WIN_WIDTH / 3, 50) # создаём прямоугольник
    draw_button(screen, quit_button, 'Quit') # рисуем кнопку

    if mouse_click: # если нажали кнопку мыши
        if mouse_click.button == 1: # если левая кнопка мыши
            if button_intersection(play_button): # если нажали на кнопку play_button
                game() # запускаем игру

            if button_intersection(tutorial_button): # если нажали на кнопку tutorial_button
                tutorial_show(screen)

            if button_intersection(mode_button): # если нажали на кнопку mode_button
                # меняем значения выбранного мода и настроек игры
                if 'NORMAL' in SELECTED_MODE:
                    SELECTED_MODE = 'mode: NIGHT'
                    NIGHT = True
                elif 'NIGHT' in SELECTED_MODE:
                    SELECTED_MODE = 'mode: HARD'
                    NIGHT = True
                    LIGHT_MASK = "light_350_soft.png"
                    BACKGROUND_MUSIC = 'first.ogg'
                    MUSIC_VOLUME = 0.2
                    ENEMY_SPEED = 4
                elif 'HARD' in SELECTED_MODE:
                    SELECTED_MODE = 'mode: NORMAL'
                    NIGHT = False
                    LIGHT_MASK = "light_350_med.png"
                    MUSIC_VOLUME = 0.05
                    BACKGROUND_MUSIC = 'second.ogg'
                    ENEMY_SPEED = 2

            if button_intersection(quit_button): # если нажали на кнопку quit_button
                exit() # закрываем игру

# функция меню обучения
def tutorial_show(screen):
    loaded_images = []
    for img in TUTORIAL_IMAGES:
        loaded_images.append(pygame.image.load(path.join(images_folder, img)))
    loaded_images = chain(loaded_images)
    current_image = next(loaded_images)
    show = True # переменная показа окна
    pygame.display.set_caption('Tutorial Pytanks 2D') # Пишем в шапку
    clock = pygame.time.Clock() # добавляем часы
    while show: # Основной цикл программы
        clock.tick(FPS) # ограничиваем частоту отрисовки кадров
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT: # если выйти
                show = False # цикл останавливается
            elif event.type == KEYDOWN: # если нажали любую клавишу
                try:
                    current_image = next(loaded_images) # изображение меняется на следующее
                except:
                    show = False # цикл останавливается
            elif event.type == MOUSEBUTTONDOWN: # если нажали на кнопку мыши
                try:
                    current_image = next(loaded_images) # изображение меняется на следующее
                except:
                    show = False # цикл останавливается
        screen.blit(current_image, (0, 0)) # рисуем изображение
        pygame.display.update() # обновление и вывод всех изменений на экран

# функция отрисовки полоски здоровья игрока
def draw_player_health(surf, x, y, pct):
    if pct < 0: # если здоровье станет меньшн нуля
        pct = 0 # то равно нулю
    BAR_LENGTH = 100 # ширина полоски
    BAR_HEIGHT = 20 # высота полоски
    fill = pct * BAR_LENGTH # длина заливки
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) # создаём контур
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT) # создаём площадь для заливки
    if pct > 0.6: # если здоровье больше 60%
        col = GREEN # заливаем зелёным
    elif pct > 0.3: # если здоровье больше 30%
        col = YELLOW # заливаем жёлтым
    else: # если меньше
        col = RED # заливаем красным
    pygame.draw.rect(surf, col, fill_rect) # отрисовываем полоску
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # отрисовываем контур

# функция для отрисовки текста
def text_print(screen, x, y, message, font_type, fonts_color, font_size, center_align=False):
    font = pygame.font.Font(font_type, font_size) # загружаем шрифт
    text_surface = font.render(message, True, fonts_color) # применяем параметры к тексту
    text_rect = text_surface.get_rect() # получаем размер занимаемого текста
    if center_align: # если в аргументах передана центровка
        text_rect.center = (x, y) # выравниваем по центру
    else: # если нет
        text_rect.topleft = (x, y) # выравниваем по верхней левой точке
    screen.blit(text_surface, text_rect) # отрисовываем текст

# функция для отрисовки таблицы рекордов
def drawing_of_records(screen):
    text_print(screen, 500, 320, 'Table of records:', 
               path.join(fonts_folder, '20219.ttf'), WHITE, 30, False) # отрисовываем имя таблицы
    # отрисовываем топ-5 рекордов
    text_print(screen, 500, 360, f'{score_table(SELECTED_MODE)[0][0]}: {score_table(SELECTED_MODE)[0][1]}', path.join(fonts_folder, '20219.ttf'),
               WHITE, 25, False)
    text_print(screen, 500, 400, f'{score_table(SELECTED_MODE)[1][0]}: {score_table(SELECTED_MODE)[1][1]}',
               path.join(fonts_folder, '20219.ttf'), WHITE, 25, False)
    text_print(screen, 500, 440, f'{score_table(SELECTED_MODE)[2][0]}: {score_table(SELECTED_MODE)[2][1]}',
               path.join(fonts_folder, '20219.ttf'), WHITE, 25, False)
    text_print(screen, 500, 480, f'{score_table(SELECTED_MODE)[3][0]}: {score_table(SELECTED_MODE)[3][1]}',
               path.join(fonts_folder, '20219.ttf'), WHITE, 25, False)
    text_print(screen, 500, 520, f'{score_table(SELECTED_MODE)[4][0]}: {score_table(SELECTED_MODE)[4][1]}',
               path.join(fonts_folder, '20219.ttf'), WHITE, 25, False)

# функция проверки пересечения мышки с кнопкой
def button_intersection(button):
    return abs(button.center[0] - mouse.get_pos()[0]) <= button.width / 2 and \
               abs(button.center[1] - mouse.get_pos()[1]) <= button.height / 2

# функция создания кнопок
def draw_button(screen, button, text):
    button_color = BLACK # цвет кнопки
    if button_intersection(button): # если мышь пересекается с кнопкой
        button_color = DARK_GRAY # то меняем цвет
    pygame.draw.rect(screen, button_color, button) # отрисовываем прямоугольник
    text_print(screen, button.center[0], button.center[1], text,
               path.join(fonts_folder, '20219.ttf'), WHITE, 40, True) # печатаем текст кнопки

# функция для отрисовки экрана проигрыша
def game_over(screen):
    dim_screen = pygame.Surface(screen.get_size()).convert_alpha() # создаём слой
    dim_screen.fill((0, 0, 0, 180)) # заливаем слой
    screen.blit(dim_screen, (0, 0)) # отрисовывам слой
    text_print(screen, WIN_WIDTH / 2, WIN_HEIGHT / 2, 'GAME OVER',
               path.join(fonts_folder, '20219.ttf'), RED, 105, True) # печатаем текст

# основной класс игры
def game():
    global AMMUNITION, TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT
    left = right = up = down = False # по умолчанию — стоим
    clock = pygame.time.Clock() # создаём часы
    pygame.time.set_timer(ENEMIES_EVENT,3000) # добавляем таймер на событие возрождения врагов
    pygame.time.set_timer(AMMUNITION_EVENT,2000) # добавляем таймер на событие перезарядки
    pygame.time.set_timer(PARTICLE_EVENT,70) # добавляем таймер на частицы
    
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Pytanks 2D") # Пишем в шапку
    pygame.mouse.set_visible(False) # скрываем курсор мыши
    running = True # работает ли игра
    game_over = False # значение экрана проигрыша
    paused = False # значение паузы

    Map = TiledMap(path.join(map_folder, 'level_1.tmx')) # загружем карту
    map_img = Map.make_map() # создаём карту
    map_rect = map_img.get_rect() # получаем размеры прямоугольника карты
    TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT = Map.get_sizes() # меняем значение размера уровня

    all_sprites = pygame.sprite.Group() # Все объекты
    enemies = pygame.sprite.Group() # Враги
    walls = pygame.sprite.Group() # Стены
    bullets = pygame.sprite.Group() # Снаряды
    muzzle_flash = pygame.sprite.Group() # Вспышки от выстрелов
    boom_flash = pygame.sprite.Group() # Взрывы
    
    for tile_object in Map.tmxdata.objects: # проходим по всем объектам карты
        if tile_object.name == 'player': # если имя объекта - "player"
            player = Player(tile_object.x, tile_object.y) # то создаём игрока в полученных координатах
        if tile_object.name == 'enemy': # если имя объекта - "enemy"
            ENEMIES_SPAWN_COORDINATES.append((tile_object.x, tile_object.y)) # то добавляем координату в список точек возрождения
            Enemy(all_sprites, player, enemies, (tile_object.x, tile_object.y)) # и создаём врага в полученных координатах
        if tile_object.name == 'wall': # если имя объекта - "wall"
            Obstacle(walls, tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height) # то добавляем стену

    all_sprites.add(player) # добавлем игрока во все объекты
      
    camera = Camera(camera_configure, TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT) # создаём камеру
    key_state = pygame.key.get_pressed() # получаем значения нажатия клавиш

    if NIGHT: # если ночь
        fog = Fog(screen, camera, player) # создаём туман

    particle1 = ParticlePrinciple(screen) # создаём объект частиц
    draw_particle = False # рисовать ли частицы

    gun_flashes = [] # изображения облака выстрела
    for img in MUZZLE_FLASHES:
        gun_flashes.append(pygame.image.load(path.join(images_folder, img)).convert_alpha()) # добавляем изображения

    dim_screen = pygame.Surface(screen.get_size()).convert_alpha() # подложка для меню паузы
    dim_screen.fill((0, 0, 0, 180)) # заливаем чёрным с небольшой прозрачностью

    pygame.mixer.music.load(path.join(music_folder, BACKGROUND_MUSIC)) # загружем фоновую музыку
    pygame.mixer.music.play(loops=-1) # запсукаем музыку и зацикливаем воспроизведение
    pygame.mixer.music.set_volume(MUSIC_VOLUME) # выставляем громкость музыки
    player_shot_sound = pygame.mixer.Sound(path.join(sounds_folder, PLAYER_SHOT_SOUND)) # загружаем звук выстрела
    player_ride_sound = pygame.mixer.Sound(path.join(sounds_folder, PLAYER_RIDE_SOUND)) # загружаем звук передвижения
    player_ride_sound.set_volume(0.5) # выставляем громкость 
    
    while running: # Основной цикл программы
        dt = clock.tick(FPS) / 1000.0 # значение FPS
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT: # если выйти
                running = False # то выходим
                pygame.mouse.set_visible(False)
                
            elif event.type == KEYDOWN: # если нажимаем клавиши
                if event.key == K_ESCAPE: # если нажали Escape
                    paused = not paused # значение паузы меняется на противоположное

                if not paused and not game_over: # если не поузы и не проигрыш
                    key_state = pygame.key.get_pressed() # получаем значения нажатых клавиш
                    if event.key in [K_w, K_a, K_s, K_d]: # если нажата одна из клавиш WASD
                        player_ride_sound.stop() # звук передвижения останавливается
                        player_ride_sound.play(loops=-1) # звук передвижения запускается зацикленно

                    if event.key == K_SPACE: # если нажали пробел
                        if AMMUNITION > 0: # если боезапас больше нуля
                            Bullet(all_sprites, bullets, walls, player.rect.center, player, boom_flash) # создаём снаряд
                            MuzzleFlash(all_sprites, muzzle_flash, gun_flashes, player.rect.center) # создаём вспышку выстрела
                            AMMUNITION -= 1 # уменьшаем боезапас
                            player_shot_sound.play() # проигрываем звук выстрела

            elif event.type == KEYUP: # если отпустили клавишу
                key_state = pygame.key.get_pressed() # получаем значение нажатых клавиш
                draw_particle = False # частицы не рисуем
                if event.key == K_d: # если отпустили клавишу D
                    right = False # не вправо
                elif event.key == K_a: # если отпустили клавишу A
                    left = False # не влево
                elif event.key == K_w: # если отпустили клавишу W
                    up = False # не вверх
                elif event.key == K_s: # если отпустили клавишу S
                    down = False # не вниз

            if event.type == MOUSEBUTTONDOWN and paused: # если нажали кнопку мыши на паузе
                if event.button == 1: # если правая кнопка
                    if button_intersection(continue_button): # если мышь пересекается с кнопкой continue_button
                        paused = False # снимаем с паузы
                        pygame.mouse.set_visible(False)
                    if button_intersection(menu_button): # если мышь пересекается с кнопкой menu_button
                        running = False # выходим в меню

            if event.type == MOUSEBUTTONDOWN and game_over: # если нажали кнопку мыши на экране проигрыша
                if event.button == 1: # если правая кнопка
                    if button_intersection(menu_button): # если мышь пересекается с кнопкой menu_button
                        running = False # выходим в меню

            if event.type == PARTICLE_EVENT: # если событие частиц
                center_coords = camera.apply(player).center # получаем координаты игрока
                particle1.add_particles(left, right, up, down, center_coords) # создаём частицы

            if event.type == ENEMIES_EVENT and len(enemies) <= 5: # если событие возрождения врагов и врагов на поле меньше пяти
                # создаём врага в одной из точек возрождения
                Enemy(all_sprites, player, enemies, random.choice(ENEMIES_SPAWN_COORDINATES))

            if event.type == AMMUNITION_EVENT and AMMUNITION < 5: # если событие перезарядки и боезапас меньше пяти
                AMMUNITION += 1 # боезапас + 1
                
        if key_state[K_a]: # если зажата клавиша A
            left = True # налево
            draw_particle = True # рисуем частицы

        elif key_state[K_d]: # если зажата клавиша D
            right = True # направо
            draw_particle = True # рисуем частицы

        elif key_state[K_w]: # если зажата клавиша W
            up = True # наверх
            draw_particle = True # рисуем частицы

        elif key_state[K_s]: # если зажата клавиша S
            down = True # вниз
            draw_particle = True # рисуем частицы

        else: # иначе
            player_ride_sound.stop() # останавливаем воспроизведение звука передвижения
            
        screen.blit(map_img, camera.apply_rect(map_rect)) # Каждую итерацию необходимо всё перерисовывать

        if not paused and not game_over:
            camera.update(player) # центризируем камеру относительно персонажа
            player.update(left, right, up, down, walls) # обновляем позицию игрока
            bullets.update() # обновляем позицию снаряды
            muzzle_flash.update() # обновляем облака выстрелов
            boom_flash.update() # обновляем вызрывы
            enemies.update(ENEMY_SPEED, walls, bullets, all_sprites, boom_flash, player, enemies) # обновляем позиции врагов

            # пасхалка
            if player.special_score == 300 and player.ricardo_go[0]:
                woo = Woo(all_sprites, center_coords)
                pygame.mixer.Sound(path.join(sounds_folder, RICARDO_SOUND)).play()
                player.ricardo_go = [False, True]
            if player.ricardo_go[1]:
                woo.update(player)

            if player.health <= 0: # если здоровье закончилось
                game_over = True # то игра окончена
            if draw_particle: # если отрисовываем чатицы
                particle1.emit() # то обновляем частицы
            for e in all_sprites:
                screen.blit(e.image, camera.apply(e)) # отображение всего
            if NIGHT: # если ночь
                fog.render_fog() # то отрисовываем туман
            draw_player_health(screen, 10, 10, player.health / PLAYER_HEALTH) # рисуем здоровье игрока
            # отрисовываем кол-во снарядов
            text_print(screen, 10, 30, f'Bullets: {AMMUNITION}', path.join(fonts_folder, '20219.ttf'), WHITE, 20)
            # отрисовываем счёт
            text_print(screen, WIN_WIDTH - 50, 20, 'Score:', path.join(fonts_folder, '20219.ttf'), WHITE, 40, True)
            text_print(screen, WIN_WIDTH - len(str(player.score)) * 20, 60, str(player.score), 
                       path.join(fonts_folder, '20219.ttf'), WHITE, 70, True)
            # отрисовываем кол-во кадров в секунду(fps)
            text_print(screen, WIN_WIDTH - 10, WIN_HEIGHT - 10, str(int(clock.get_fps())), 
                       path.join(fonts_folder, '20219.ttf'), WHITE, 15, True)

        elif not game_over: # если пауза
            player_ride_sound.stop() # останавливаем воспроизведение звука передвижения
            for e in all_sprites:
                screen.blit(e.image, camera.apply(e)) # отображение всего
            if NIGHT: # если ночь
                fog.render_fog() # то отрисовываем туман
            # отрисовываем меню паузы
            screen.blit(dim_screen, (0, 0)) # рисуем подложку
            text_print(screen, WIN_WIDTH / 2, WIN_HEIGHT / 5, 'Pause', path.join(fonts_folder, '20219.ttf'), RED, 105, True)
            continue_button = pygame.Rect(WIN_WIDTH / 3, WIN_HEIGHT / 3, WIN_WIDTH / 3, 50)
            draw_button(screen, continue_button, 'Continue') # добавляем кнопку продолжения игры
            menu_button = pygame.Rect(WIN_WIDTH / 3, WIN_HEIGHT / 2 - 25, WIN_WIDTH / 3, 50)
            draw_button(screen, menu_button, 'Main menu') # добавляем кнопку выхода в меню
            pygame.mouse.set_visible(True)

        else:
            if NIGHT: # если ночь
                fog.render_fog() # то отрисовывам туман
            # отрисовываем меню проигрыша
            screen.blit(dim_screen, (0, 0)) # рисуем подложку
            text_print(screen, WIN_WIDTH / 2, WIN_HEIGHT / 3, 'GAME OVER',
                       path.join(fonts_folder, '20219.ttf'), RED, 105, True)
            text_print(screen, WIN_WIDTH / 2, WIN_HEIGHT / 2 - 25, f'Your score: {player.score}',
                       path.join(fonts_folder, '20219.ttf'), WHITE, 50, True)
            menu_button = pygame.Rect(WIN_WIDTH / 3, WIN_HEIGHT / 2 + 25, WIN_WIDTH / 3, 50)
            draw_button(screen, menu_button, 'Main menu') # добавляем кнопку выхода в меню
            pygame.mouse.set_visible(True) # делаем курсор мыши видимым
        pygame.display.update() # обновление и вывод всех изменений на экран
    pygame.mixer.music.stop() # отсанавливаем воспроизведение фоновой музыки
    add_record(score_name(), player.score, SELECTED_MODE) # добавляем рекорд в таблицу


if __name__ == "__main__":
    menu_show()
    #game()
