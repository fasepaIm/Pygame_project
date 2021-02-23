#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import *
from os import path
from random import randint, choice

MOVE_SPEED = 1
PLAYER_HEALTH = 100

PLAYER_IMAGE_RIGHT = 'tank/r1.png'
PLAYER_IMAGE_LEFT = 'tank/l1.png'
PLAYER_IMAGE_UP = 'tank/u1.png'
PLAYER_IMAGE_DOWN = 'tank/d1.png'

BULLET_SPEED = 5
BULLET_LIFETIME = 1000

BULLET_X, BULLET_Y = 1, 0
KICKBACK = 3

BULLET_IMAGE_RIGHT = 'data/bullet/r.png'
BULLET_IMAGE_LEFT = 'data/bullet/l.png'
BULLET_IMAGE_UP = 'data/bullet/u.png'
BULLET_IMAGE_DOWN = 'data/bullet/d.png'

ENEMY_SPEED = 2
ENEMY_KICK = 30
ENEMY_DAMAGE = 20

ENEMY_IMAGE_RIGHT = 'tank/r3.png'
ENEMY_IMAGE_LEFT = 'tank/l3.png'
ENEMY_IMAGE_UP = 'tank/u3.png'
ENEMY_IMAGE_DOWN = 'tank/d3.png'

FLASH_DURATION = 40
KILL_FLASH_DURATION = 150
EFFECTS_LAYER = 4

BOOM_FLASHES = ['boom_flashes_1.png', 'boom_flashes_2.png',
                'boom_flashes_3.png', 'boom_flashes_4.png']
IMG_FOLDER = 'data'

kill_flashes = []


def collide_with_hero(self, xvel, yvel, walls, hero, all_sprites):
    if sprite.collide_rect(self, hero):
        MuzzleFlash(all_sprites, self.boom_flash, kill_flashes, self.rect.center, True)
        self.kill()
        hero.health -= ENEMY_DAMAGE
        if xvel > 0:                      # если движется вправо
            self.rect.right = hero.rect.left # то не движется вправо
            xvel = ENEMY_KICK
            hero.rect.x += xvel
            collide_with_walls(hero, xvel, 0, walls)
            self.xvel = 0

        if xvel < 0:                      # если движется влево
            self.rect.left = hero.rect.right # то не движется влево
            xvel = -ENEMY_KICK
            hero.rect.x += xvel
            collide_with_walls(hero, xvel, 0, walls)
            self.xvel = 0

        if yvel > 0:                      # если падает вниз
            self.rect.bottom = hero.rect.top # то не падает вниз
            yvel = ENEMY_KICK
            hero.rect.y += yvel
            collide_with_walls(hero, 0, yvel, walls)
            self.yvel = 0                 # и энергия падения пропадает

        if yvel < 0:                      # если движется вверх
            self.rect.top = hero.rect.bottom # то не движется вверх
            yvel = -ENEMY_KICK
            hero.rect.y += yvel
            collide_with_walls(hero, 0, yvel, walls)
            self.yvel = 0                 # и энергия прыжка пропадает


def collide_with_walls(self, xvel, yvel, walls, enemy=False, hero=False):
    for p in walls:
        if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
            if xvel > 0:                      # если движется вправо
                self.rect.right = p.rect.left # то не движется вправо

            if xvel < 0:                      # если движется влево
                self.rect.left = p.rect.right # то не движется влево

            if yvel > 0:                      # если падает вниз
                self.rect.bottom = p.rect.top # то не падает вниз 
                self.yvel = 0                 # и энергия падения пропадает

            if yvel < 0:                      # если движется вверх
                self.rect.top = p.rect.bottom # то не движется вверх
                self.yvel = 0                 # и энергия прыжка пропадает


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = image.load(PLAYER_IMAGE_RIGHT)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.pos = (x, y)
        self.health = PLAYER_HEALTH

        
    def update(self, left, right, up, down, walls):
        global BULLET_X, BULLET_Y, running
        self.pos = (self.rect.x, self.rect.y)
        self.xvel = 0
        self.yvel = 0

        if up:
            BULLET_X, BULLET_Y = 0, -1
            self.yvel = -MOVE_SPEED
            self.image = image.load(PLAYER_IMAGE_UP)

        elif down:
            BULLET_X, BULLET_Y = 0, 1
            self.yvel = MOVE_SPEED
            self.image = image.load(PLAYER_IMAGE_DOWN)
                       
        elif left:
            BULLET_X, BULLET_Y = -1, 0
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image = image.load(PLAYER_IMAGE_LEFT)
 
        elif right:
            BULLET_X, BULLET_Y = 1, 0
            self.xvel = MOVE_SPEED # Право = x + n
            self.image = image.load(PLAYER_IMAGE_RIGHT)

        self.rect.y += self.yvel
        collide_with_walls(self, 0, self.yvel, walls)
        self.rect.x += self.xvel # переносим свои положение на xvel
        collide_with_walls(self, self.xvel, 0, walls)

    def get_position(self):
        return (self.rect.x, self.rect.y)


class Enemy(sprite.Sprite):
    def __init__(self, all_sprites, hero, enemies, x, y):
        self.groups = all_sprites, enemies
        sprite.Sprite.__init__(self, self.groups)
        self.x = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.y = y
        self.hero = hero
        self.image = image.load(ENEMY_IMAGE_UP)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self, walls, bullets, all_sprites, boom_flash, hero):
        self.all_sprites = all_sprites
        self.boom_flash = boom_flash
        self.xvel = 0
        self.yvel = 0
        if self.hero.pos[0] > self.rect.x:
            self.xvel += ENEMY_SPEED
            self.image = image.load(ENEMY_IMAGE_RIGHT)

        if self.hero.pos[0] < self.rect.x:
            self.xvel -= ENEMY_SPEED
            self.image = image.load(ENEMY_IMAGE_LEFT)

        if self.hero.pos[1] > self.rect.y:
            self.yvel += ENEMY_SPEED
            self.image = image.load(ENEMY_IMAGE_DOWN)

        if self.hero.pos[1] < self.rect.y:
            self.yvel -= ENEMY_SPEED
            self.image = image.load(ENEMY_IMAGE_UP)

        self.collide_with_bullets(bullets)
        self.rect.y += self.yvel
        collide_with_hero(self, 0, self.yvel, walls, hero, all_sprites)
        collide_with_walls(self, 0, self.yvel, walls)
        self.rect.x += self.xvel # переносим свои положение на xvel
        collide_with_hero(self, 0, self.yvel, walls, hero, all_sprites)
        collide_with_walls(self, self.xvel, 0, walls)

    def collide_with_bullets(self, bullets):
        for p in bullets:
            if sprite.collide_rect(self, p): # если есть пули с врагом
                MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, p.rect.center, True)
                p.kill()
                self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, walls, pos, player, boom_flash):
        global kill_flashes
        self.boom_flash = boom_flash
        self.all_sprites = all_sprites
        self.player = player
        self.groups = all_sprites, bullets
        self.walls = walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.bul_x = BULLET_X
        self.bul_y = BULLET_Y
        self.check_image()
        self.rect.center = pos
        self.pos = list(pos)
        self.vel = BULLET_SPEED
        player.rect.x -= KICKBACK * self.bul_x
        player.rect.y -= KICKBACK * self.bul_y
        self.spawn_time = pygame.time.get_ticks()

    def check_image(self):
        if self.bul_x > 0:
            self.image = image.load(BULLET_IMAGE_RIGHT)
        elif self.bul_x < 0:
            self.image = image.load(BULLET_IMAGE_LEFT)
        elif self.bul_y < 0:
            self.image = image.load(BULLET_IMAGE_UP)
        elif self.bul_y > 0:
            self.image = image.load(BULLET_IMAGE_DOWN)
        self.rect = self.image.get_rect()


    def update(self):
        self.check_image()
        self.pos[0] += self.vel * self.bul_x
        self.pos[1] += self.vel * self.bul_y
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.walls):
            MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center)
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, all_sprites, muzzle_flash, gun_flashes, pos, kill=False):
        for img in BOOM_FLASHES:
            kill_flashes.append(pygame.image.load(path.join(IMG_FOLDER, img)).convert_alpha())
        self._layer = EFFECTS_LAYER
        self.groups = all_sprites, muzzle_flash
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.killed = kill
        if kill:
            size = randint(60, 90)
        else:
            size = randint(20, 50)
        self.image = pygame.transform.scale(choice(gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.rect.x += 15 * BULLET_X
        self.rect.y += 15 * BULLET_Y
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if self.killed:
            if pygame.time.get_ticks() - self.spawn_time > KILL_FLASH_DURATION:
                self.kill()
        else:
            if pygame.time.get_ticks() - self.spawn_time > FLASH_DURATION:
                self.kill()
