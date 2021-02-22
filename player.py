#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import *
from random import randint, choice

MOVE_SPEED = 1
WIDTH = 30
HEIGHT = 30
COLOR =  "#888888"

PLAYER_IMAGE_RIGHT = 'tank/r1.png'
PLAYER_IMAGE_LEFT = 'tank/l1.png'
PLAYER_IMAGE_UP = 'tank/u1.png'
PLAYER_IMAGE_DOWN = 'tank/d1.png'

BULLET_IMAGE_RIGHT = 'data/bullet/r.png'
BULLET_IMAGE_LEFT = 'data/bullet/l.png'
BULLET_IMAGE_UP = 'data/bullet/u.png'
BULLET_IMAGE_DOWN = 'data/bullet/d.png'

BULLET_SPEED = 10
BULLET_LIFETIME = 1000

BULLET_X, BULLET_Y = 1, 0
KICKBACK = 3

FLASH_DURATION = 40
EFFECTS_LAYER = 4


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = image.load(PLAYER_IMAGE_RIGHT)
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        
    def update(self, left, right, up, down, walls):
        global BULLET_X, BULLET_Y
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
        self.collide(0, self.yvel, walls)
        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, walls)

    def collide(self, xvel, yvel, walls):
        for p in walls:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                    self.yvel = 0                 # и энергия прыжка пропадает

    def get_position(self):
        return (self.rect.x, self.rect.y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, walls, pos, player):
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
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, all_sprites, muzzle_flash, gun_flashes, pos):
        self._layer = EFFECTS_LAYER
        self.groups = all_sprites, muzzle_flash
        pygame.sprite.Sprite.__init__(self, self.groups)
        size = randint(20, 50)
        self.image = pygame.transform.scale(choice(gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.rect.x += 15 * BULLET_X
        self.rect.y += 15 * BULLET_Y
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()
