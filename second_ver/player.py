#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim

MOVE_SPEED = 1
WIDTH = 30
HEIGHT = 30
COLOR =  "#888888"

IMAGE_RIGHT = 'tank/r1.png'
IMAGE_LEFT = 'tank/l1.png'
IMAGE_UP = 'tank/u1.png'
IMAGE_DOWN = 'tank/d1.png'


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = image.load(IMAGE_UP)
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        
    def update(self, left, right, up, down, platforms):
        self.xvel = 0
        self.yvel = 0
        if up:
            self.yvel = -MOVE_SPEED
            self.image = image.load(IMAGE_UP)

        elif down:
            self.yvel = MOVE_SPEED
            self.image = image.load(IMAGE_DOWN)
                       
        elif left:
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image = image.load(IMAGE_LEFT)
 
        elif right:
            self.xvel = MOVE_SPEED # Право = x + n
            self.image = image.load(IMAGE_RIGHT)

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

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
