# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
import pygame
import os
import random
import pytmx
from os import path
from pygame import *
from player import *
from settings import *
from tiled_map import *
from particles import *


PARTICLE_EVENT = pygame.USEREVENT + 1
ENEMIES_EVENT = pygame.USEREVENT
AMMUNITION_EVENT = pygame.USEREVENT
pygame.init() # Инициация PyGame, обязательная строчка


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, walls, x, y, w, h):
        self.groups = walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


# класс для создания тумана/ночного освещения
class Fog:
    def __init__(self, screen, camera, player):
        self.screen = screen
        self.camera = camera
        self.player = player
        self.fog = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pygame.image.load(path.join(images_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()


    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)


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

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 190, 58)

    def draw(self, screen, x, y, message, action=None):
        global GAME_OFF, SELECTED_MODE, NIGHT, LIGHT_MASK, ENEMY_SPEED, BACKGROUND_MUSIC
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if click[0]:
                if action == quit:
                    GAME_OFF = True
                    return
                elif 'mode' in message:
                    if 'NORMAL' in message:
                        SELECTED_MODE = 'mode: NIGHT'
                        NIGHT = True
                    elif 'NIGHT' in message:
                        SELECTED_MODE = 'mode: HARD'
                        NIGHT = True
                        LIGHT_MASK = "light_350_soft.png"
                        BACKGROUND_MUSIC = 'first.ogg'
                        ENEMY_SPEED = 4
                    elif 'HARD' in message:
                        SELECTED_MODE = 'mode: NORMAL'
                        NIGHT = False
                        LIGHT_MASK = "light_350_med.png"
                        BACKGROUND_MUSIC = 'second.ogg'
                        ENEMY_SPEED = 2
                else:
                    pygame.mixer.Sound(path.join(sounds_folder, LEVEL_START_SOUND)).play()
                    pygame.time.delay(300)
                    action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        text_print(screen, WIN_WIDTH / 2, y + 35, message, path.join(fonts_folder, '20219.ttf'), WHITE, 50, True)


def text_print(screen, x, y, message, font_type, fonts_color, font_size, center_align=False):
    font = pygame.font.Font(font_type, font_size)
    text_surface = font.render(message, True, fonts_color)
    text_rect = text_surface.get_rect()
    if center_align:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def menu_show():
    global GAME_OFF, SELECTED_MODE
    menu_background = pygame.image.load(path.join(images_folder, 'menu.jpg'))
    show = True
    start_btn = Button(300, 70)
    mode_btn = Button(300, 70)
    quit_btn = Button(300, 70)
    screen = pygame.display.set_mode(DISPLAY)
    while show: # Основной цикл программы
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT:
                show = False
            screen.blit(menu_background, (0, 0))
            start_btn.draw(screen, 250, 300, 'Play game', game)
            mode_btn.draw(screen, 250, 380, SELECTED_MODE)
            quit_btn.draw(screen, 250, 460, 'Quit', quit)
            if GAME_OFF:
                show = False
                break
            pygame.display.update()
            
def game_over(screen):
    dim_screen = pygame.Surface(screen.get_size()).convert_alpha()
    dim_screen.fill((0, 0, 0, 180))
    screen.blit(dim_screen, (0, 0))
    text_print(screen, WIN_WIDTH / 2, WIN_HEIGHT / 2, 'GAME OVER', path.join(fonts_folder, '20219.ttf'), RED, 105, True)


def game():
    global AMMUNITION
    left = right = up = down = False    # по умолчанию — стоим
    timer = pygame.time.Clock()
    
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Tanks") # Пишем в шапку
    running = True
    game_over = False
    paused = False

    Map = TiledMap(path.join(map_folder, 'level2.tmx'))
    map_img = Map.make_map()
    map_rect = map_img.get_rect()
    TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT = Map.get_sizes()

    all_sprites = pygame.sprite.Group() # Все объекты
    enemies = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    muzzle_flash = pygame.sprite.Group()
    boom_flash = pygame.sprite.Group()
    
    for tile_object in Map.tmxdata.objects:
        if tile_object.name == 'player':
            player = Player(tile_object.x, tile_object.y)
        if tile_object.name == 'enemy':
            ENEMIES_SPAWN_COORDINATES.append((tile_object.x, tile_object.y))
            Enemy(all_sprites, player, enemies, (tile_object.x, tile_object.y))
        if tile_object.name == 'wall':
            Obstacle(walls, tile_object.x, tile_object.y, 
                     tile_object.width, tile_object.height)

    pygame.time.set_timer(ENEMIES_EVENT,3000)
    pygame.time.set_timer(AMMUNITION_EVENT,2000)

    all_sprites.add(player)
      
    camera = Camera(camera_configure, TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT)
    key_state = pygame.key.get_pressed()

    fog = Fog(screen, camera, player)
    pygame.time.set_timer(PARTICLE_EVENT,70)
    particle1 = ParticlePrinciple(screen)
    draw_particle = False

    gun_flashes = []
    for img in MUZZLE_FLASHES:
        gun_flashes.append(pygame.image.load(path.join(images_folder, img)).convert_alpha())

    dim_screen = pygame.Surface(screen.get_size()).convert_alpha()
    dim_screen.fill((0, 0, 0, 180))

    clock = pygame.time.Clock()

    pygame.mixer.music.load(path.join(music_folder, BACKGROUND_MUSIC))
    player_shot_sound = pygame.mixer.Sound(path.join(sounds_folder, PLAYER_SHOT_SOUND))
    player_ride_sound = pygame.mixer.Sound(path.join(sounds_folder, PLAYER_RIDE_SOUND))
    player_ride_sound.set_volume(0.5)

    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)


    while running: # Основной цикл программы
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                    if not paused and not game_over:
                        player_ride_sound.stop()
                        player_ride_sound.play(loops=-1)

                key_state = pygame.key.get_pressed()

                if event.key == K_ESCAPE:
                    paused = not paused

                if event.key == K_SPACE:
                    if AMMUNITION > 0:
                        Bullet(all_sprites, bullets, walls, player.rect.center, player, boom_flash)
                        MuzzleFlash(all_sprites, muzzle_flash, gun_flashes, player.rect.center)
                        AMMUNITION -= 1
                        if not paused and not game_over:
                            player_shot_sound.play()

            elif event.type == KEYUP:
                key_state = pygame.key.get_pressed()
                draw_particle = False
                if event.key == K_RIGHT:
                    right = False
                elif event.key == K_LEFT:
                    left = False
                elif event.key == K_UP:
                    up = False
                elif event.key == K_DOWN:
                    down = False

            if event.type == PARTICLE_EVENT:
                center_coords = camera.apply(player).center
                particle1.add_particles(left, right, up, down, center_coords)

            if event.type == ENEMIES_EVENT and len(enemies) <= 5:
                Enemy(all_sprites, player, enemies, random.choice(ENEMIES_SPAWN_COORDINATES))

            if event.type == AMMUNITION_EVENT and AMMUNITION < 5:
                AMMUNITION += 1
                
        if key_state[K_LEFT]:
            left = True
            draw_particle = True

        elif key_state[K_RIGHT]:
            right = True
            draw_particle = True

        elif key_state[K_UP]:
            up = True
            draw_particle = True

        elif key_state[K_DOWN]:
            down = True
            draw_particle = True

        else:
            player_ride_sound.stop()
            
        screen.blit(map_img, camera.apply_rect(map_rect)) # Каждую итерацию необходимо всё перерисовывать 

        if not paused and not game_over:
            camera.update(player) # центризируем камеру относительно персонажа
            player.update(left, right, up, down, walls)
            bullets.update()
            muzzle_flash.update()
            boom_flash.update()
            enemies.update(ENEMY_SPEED, walls, bullets, all_sprites, boom_flash, player, enemies)

            if player.health <= 0:
                game_over = True
            if draw_particle:
                particle1.emit()
            for e in all_sprites:
                screen.blit(e.image, camera.apply(e)) # отображение всего
            if NIGHT:
                fog.render_fog()
            draw_player_health(screen, 10, 10, player.health / PLAYER_HEALTH)
            text_print(screen, 10, 30, f'Bullets: {AMMUNITION}', path.join(fonts_folder, '20219.ttf'), WHITE, 20)
            text_print(screen, WIN_WIDTH - 50, 20, 'Score:', path.join(fonts_folder, '20219.ttf'), WHITE, 40, True)
            text_print(screen, WIN_WIDTH - len(str(player.score)) * 20, 60, str(player.score), path.join(fonts_folder, '20219.ttf'), WHITE, 70, True)
            text_print(screen, WIN_WIDTH - 10, WIN_HEIGHT - 10, str(int(clock.get_fps())), path.join(fonts_folder, '20219.ttf'), WHITE, 15, True)
            
        elif not game_over:
            player_ride_sound.stop()
            for e in all_sprites:
                screen.blit(e.image, camera.apply(e)) # отображение всего
            if NIGHT:
                fog.render_fog()
            screen.blit(dim_screen, (0, 0))
            text_print(screen, WIN_WIDTH / 2, WIN_HEIGHT / 2, 'Pause', path.join(fonts_folder, '20219.ttf'), RED, 105, True)
            
        else:
            if NIGHT:
                fog.render_fog()
            screen.blit(dim_screen, (0, 0))
            text_print(screen, WIN_WIDTH / 2, WIN_HEIGHT / 2, 'GAME OVER', path.join(fonts_folder, '20219.ttf'), RED, 105, True)
            
        pygame.display.update()     # обновление и вывод всех изменений на экран
    pygame.mixer.music.stop()

if __name__ == "__main__":
    menu_show()
    # game()
