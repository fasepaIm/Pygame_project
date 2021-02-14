#            #self.rect = rect(x, y, WIDTH, WIDTH)!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import os
import random
from pygame import *
from player import Player
from blocks import Platform

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = pygame.Color('brown')
TITLE_SIZE = 32
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_med.png"

PARTICLE_EVENT = pygame.USEREVENT + 1


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

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


class ParticlePrinciple:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(self.screen, pygame.Color('Gray'), particle[0], int(particle[1]))

    def add_particles(self, left, right, up, down, center_coords):
        #pos_x = pygame.mouse.get_pos()[0]
        #pos_y = pygame.mouse.get_pos()[1]
        pos_x, pos_y = center_coords
        if left:
            pos_x += 12
            pos_y += 12
        elif right:
            pos_x -= 12
        elif up:
            pos_y += 12
        elif down:
            pos_y -= 12
        radius = 5
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
	
    def apply(self, target):
        return target.rect.move(self.state.topleft)

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


def main():
    level = [
       "----------------------------------",
       "-                                -",
       "-                       --       -",
       "-                                -",
       "-            --                  -",
       "-                                -",
       "--                               -",
       "-                                -",
       "-                   ----     --- -",
       "-                                -",
       "--                               -",
       "-                                -",
       "-                            --- -",
       "-                                -",
       "-                                -",
       "-      ---                       -",
       "-                                -",
       "-   -------         ----         -",
       "-                                -",
       "-                         -      -",
       "-                            --  -",
       "-                                -",
       "-                                -",
       "----------------------------------"]

    hero = Player(55,55) # создаем героя по (x,y) координатам
    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    entities.add(hero)

    x = y = 0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    # то же самое и с высотой
        x = 0                   # на каждой новой строчке начинаем с нуля


    left = right = up = down = False    # по умолчанию — стоим
    night = True
    timer = pygame.time.Clock()
    
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Tanks") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    running = True

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту
   
    camera = Camera(camera_configure, total_level_width, total_level_height)
    key_state = pygame.key.get_pressed()

    fog = Fog(screen, camera, hero)
    pygame.time.set_timer(PARTICLE_EVENT,70)
    particle1 = ParticlePrinciple(screen)
    draw_particle = False


    while running: # Основной цикл программы
        timer.tick(60)
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == pygame.QUIT:
                running = False

            elif event.type == KEYDOWN:
                key_state = pygame.key.get_pressed()

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
            hero.update(left, right, up, down, platforms) # передвижение

        elif key_state[K_RIGHT]:
            right = True
            draw_particle = True
            hero.update(left, right, up, down, platforms) # передвижение

        elif key_state[K_UP]:
            up = True
            draw_particle = True
            hero.update(left, right, up, down, platforms) # передвижение

        elif key_state[K_DOWN]:
            down = True
            draw_particle = True
            hero.update(left, right, up, down, platforms) # передвижение
                
        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 
         
        camera.update(hero) # центризируем камеру относительно персонажа

        if night:
            fog.render_fog()
        if draw_particle:
            particle1.emit()
        for e in entities:
            screen.blit(e.image, camera.apply(e)) # отображение всего
        pygame.display.update()     # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    main()
