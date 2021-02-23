# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
import pygame
import os
import random
import pytmx
from os import path
from menu import *
from pygame import *
from player import *
from tiled_map import *
from particles import *


#Объявляем переменные
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

TOTAL_LEVEL_WIDTH = 0
TOTAL_LEVEL_HEIGHT = 0
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
IMG_FOLDER = 'data'
LIGHT_MASK = "light_350_med.png"

MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png',
                  'whitePuff17.png', 'whitePuff18.png']

FPS = 60

PARTICLE_EVENT = pygame.USEREVENT + 1
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
    def __init__(self, screen, camera, hero):
        self.screen = screen
        self.camera = camera
        self.player = hero
        self.fog = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = load_image(LIGHT_MASK).convert_alpha()
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


def menu_show():
    menu_background = pygame.image.load('data/menu.jpg')
    font_type = pygame.font.Font('fonts/20219.ttf', 50)
    show = True
    start_btn = Button(220, 70)
    quit_btn = Button(120, 70)
    screen = pygame.display.set_mode(DISPLAY)
    while show: # Основной цикл программы
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT:
                show = False
            screen.blit(menu_background, (0, 0))
            start_btn.draw(screen, 300, 300, 'Play game', font_type, game)
            quit_btn.draw(screen, 350, 380, 'Quit', font_type, quit)
            pygame.display.update()


def game():
    left = right = up = down = False    # по умолчанию — стоим
    night = False
    timer = pygame.time.Clock()
    
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Tanks") # Пишем в шапку
    running = True

    map_folder = 'maps'
    Map = TiledMap('maps/level1.tmx')
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
            hero = Player(tile_object.x, tile_object.y)
        if tile_object.name == 'enemy':
            Enemy(all_sprites, hero, enemies, tile_object.x, tile_object.y)
        if tile_object.name == 'wall':
            Obstacle(walls, tile_object.x, tile_object.y, 
                     tile_object.width, tile_object.height)

    all_sprites.add(hero)
      
    camera = Camera(camera_configure, TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT)
    key_state = pygame.key.get_pressed()

    fog = Fog(screen, camera, hero)
    pygame.time.set_timer(PARTICLE_EVENT,70)
    particle1 = ParticlePrinciple(screen)
    draw_particle = False

    gun_flashes = []
    for img in MUZZLE_FLASHES:
        gun_flashes.append(pygame.image.load(path.join(IMG_FOLDER, img)).convert_alpha())

    clock = pygame.time.Clock()

    while running: # Основной цикл программы
        dt = clock.tick(FPS) / 1000.0
        pygame.display.set_caption("{:.2f}".format(clock.get_fps()))

        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT:
                running = False

            elif event.type == KEYDOWN:
                key_state = pygame.key.get_pressed()

                if event.key == K_SPACE:
                    Bullet(all_sprites, bullets, walls, hero.rect.center, hero, boom_flash)
                    MuzzleFlash(all_sprites, muzzle_flash, gun_flashes, hero.rect.center)

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
                center_coords = camera.apply(hero).center
                particle1.add_particles(left, right, up, down, center_coords)
                
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
                
        screen.blit(map_img, camera.apply_rect(map_rect)) # Каждую итерацию необходимо всё перерисовывать 

        camera.update(hero) # центризируем камеру относительно персонажа        

        hero.update(left, right, up, down, walls) 
        bullets.update()
        muzzle_flash.update()
        boom_flash.update()
        enemies.update(walls, bullets, all_sprites, boom_flash, hero)
        draw_player_health(screen, 10, 10, hero.health / PLAYER_HEALTH)


        if hero.health <= 0:
            running = False
        if night:
            fog.render_fog()
        if draw_particle:
            particle1.emit()
        for e in all_sprites:
            screen.blit(e.image, camera.apply(e)) # отображение всего
        pygame.display.update()     # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    menu_show()
