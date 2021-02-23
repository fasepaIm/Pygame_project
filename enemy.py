#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pygame
vec = pygame.math.Vector2

MOVE_SPEED = 1
WIDTH = 30
HEIGHT = 30
COLOR =  "#888888"

IMAGE_RIGHT = 'tank/r3.png'
IMAGE_LEFT = 'tank/l3.png'
IMAGE_UP = 'tank/u3.png'
IMAGE_DOWN = 'tank/d3.png'

ENEMY_SPEED = 5


class Enemy(sprite.Sprite):
    def __init__(self, all_sprites, hero, enemies, x, y):
        self.groups = all_sprites, enemies
        sprite.Sprite.__init__(self, self.groups)
        self.x = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.y = y
        self.hero = hero
        self.image = image.load(IMAGE_UP)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self, dt):
        if self.hero.pos[0] > self.rect.x:
            self.rect.x += ENEMY_SPEED
        if self.hero.pos[0] < self.rect.x:
            self.rect.x -= ENEMY_SPEED
        if self.hero.pos[1] > self.rect.y:
            self.rect.y += ENEMY_SPEED
        if self.hero.pos[1] < self.rect.y:
            self.rect.y -= ENEMY_SPEED        
        #self.rect = self.image.get_rect()
        #self.rect.center = self.pos 
        

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
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
