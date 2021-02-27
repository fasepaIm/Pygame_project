#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import *
from settings import *
from os import path
from itertools import chain
from random import randint, choice


def collide_with_hero(self, xvel, yvel, walls, player, all_sprites):
    if sprite.collide_rect(self, player):
        MuzzleFlash(all_sprites, self.boom_flash, kill_flashes, self.rect.center, True)
        pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()
        pygame.mixer.Sound(path.join(sounds_folder, ENEMY_HIT_SOUND)).play()
        self.kill()
        player.hit()
        player.health -= ENEMY_DAMAGE
        if self.xvel > 0:                      # если движется вправо
            xvel = ENEMY_KICK
            player.rect.x += xvel
            collide_with_objects(player, xvel, 0, walls)
            player.xvel = 0

        elif self.xvel < 0:                      # если движется влево
            xvel = -ENEMY_KICK
            player.rect.x += xvel
            collide_with_objects(player, xvel, 0, walls)
            player.xvel = 0

        elif self.yvel > 0:                      # если падает вниз
            yvel = ENEMY_KICK
            player.rect.y += yvel
            collide_with_objects(player, 0, yvel, walls)
            player.yvel = 0                 # и энергия падения пропадает

        elif self.yvel < 0:                      # если движется вверх
            yvel = -ENEMY_KICK
            player.rect.y += yvel
            collide_with_objects(player, 0, yvel, walls)
            player.yvel = 0                 # и энергия прыжка пропадает


def collide_with_objects(self, xvel, yvel, objects):
    for p in objects:
        if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
            if self.rect.center != p.rect.center:
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
        self.image = image.load(PLAYERS_TANK_IMAGE)
        self.last_image_rotation = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.pos = (x, y)
        self.health = PLAYER_HEALTH
        self.score = 0
        self.damaged = False
        self.xvel = 0
        self.yvel = 0

        
    def update(self, left, right, up, down, walls):
        global BULLET_X, BULLET_Y, running
        self.pos = (self.rect.x, self.rect.y)
        self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE), self.last_image_rotation)

        if up:
            BULLET_X, BULLET_Y = 0, -1
            self.yvel = -MOVE_SPEED
            self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE), 90)
            self.last_image_rotation = 90

        elif down:
            BULLET_X, BULLET_Y = 0, 1
            self.yvel = MOVE_SPEED
            self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE), 270)
            self.last_image_rotation = 270

        elif left:
            BULLET_X, BULLET_Y = -1, 0
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE), 180)
            self.last_image_rotation = 180

        elif right:
            BULLET_X, BULLET_Y = 1, 0
            self.xvel = MOVE_SPEED # Право = x + n
            self.image = image.load(PLAYERS_TANK_IMAGE)
            self.last_image_rotation = 0

        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        self.rect.y += self.yvel # переносим свои положение на yvel
        collide_with_objects(self, 0, self.yvel, walls)
        self.rect.x += self.xvel # переносим свои положение на xvel
        collide_with_objects(self, self.xvel, 0, walls)
        self.xvel = 0
        self.yvel = 0

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 3)

    def get_position(self):
        return (self.rect.x, self.rect.y)


class Enemy(sprite.Sprite):
    def __init__(self, all_sprites, player, enemies, coords):
        self.groups = all_sprites, enemies
        sprite.Sprite.__init__(self, self.groups)
        x, y = coords
        self.x = x
        self.y = y
        self.player = player
        self.image = image.load(ENEMY_TANK_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self, walls, bullets, all_sprites, boom_flash, player, enemies):
        self.all_sprites = all_sprites
        self.boom_flash = boom_flash
        self.xvel = 0
        self.yvel = 0
        if self.player.pos[0] > self.rect.x:
            self.xvel += ENEMY_SPEED
            self.image = image.load(ENEMY_TANK_IMAGE)

        elif self.player.pos[0] < self.rect.x:
            self.xvel -= ENEMY_SPEED
            self.image = pygame.transform.rotate(image.load(ENEMY_TANK_IMAGE), 180)

        if self.player.pos[1] > self.rect.y:
            self.yvel += ENEMY_SPEED
            self.image = pygame.transform.rotate(image.load(ENEMY_TANK_IMAGE), 270)

        elif self.player.pos[1] < self.rect.y:
            self.yvel -= ENEMY_SPEED
            self.image = pygame.transform.rotate(image.load(ENEMY_TANK_IMAGE), 90)

        self.collide_with_bullets(bullets)
        self.rect.y += self.yvel
        collide_with_hero(self, 0, self.yvel, walls, player, all_sprites)
        collide_with_objects(self, 0, self.yvel, enemies)
        collide_with_objects(self, 0, self.yvel, walls)
        self.rect.x += self.xvel # переносим свои положение на xvel
        collide_with_hero(self, 0, self.yvel, walls, player, all_sprites)
        collide_with_objects(self, self.xvel, 0, enemies)
        collide_with_objects(self, self.xvel, 0, walls)

    def collide_with_bullets(self, bullets):
        for p in bullets:
            if sprite.collide_rect(self, p): # если есть пули с врагом
                MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, p.rect.center, True)
                self.player.score += POINT_PRICE
                pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()
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

        xvel = -(KICKBACK * self.bul_x)
        player.rect.x += xvel
        collide_with_objects(player, xvel, 0, walls)
        yvel = -(KICKBACK * self.bul_y)
        player.rect.y += yvel
        collide_with_objects(player, 0, yvel, walls)

        self.spawn_time = pygame.time.get_ticks()

    def check_image(self):
        if self.bul_x > 0:
            self.image = image.load(BULLET_IMAGE)
        elif self.bul_x < 0:
            self.image = pygame.transform.rotate(image.load(BULLET_IMAGE), 180)
        elif self.bul_y < 0:
            self.image = pygame.transform.rotate(image.load(BULLET_IMAGE), 90)
        elif self.bul_y > 0:
            self.image = pygame.transform.rotate(image.load(BULLET_IMAGE), 270)
        self.rect = self.image.get_rect()


    def update(self):
        self.check_image()
        self.pos[0] += self.vel * self.bul_x
        self.pos[1] += self.vel * self.bul_y
        self.rect.center = self.pos
        if sprite.spritecollideany(self, self.walls):
            MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center)
            pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, all_sprites, muzzle_flash, gun_flashes, pos, kill=False):
        for img in BOOM_FLASHES:
            kill_flashes.append(pygame.image.load(path.join(game_folder, f'data/images/{img}')).convert_alpha())
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
