# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
import pygame
from settings import *


pygame.init()
FONT = pygame.font.Font(path.join(fonts_folder, '20219.ttf'), 40)  # загружаем шрифт


# класс поля ввода
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global NAME
        if event.type == pygame.MOUSEBUTTONDOWN:
            # если пользователь нажал на прямоугольник поля ввода
            if self.rect.collidepoint(event.pos):
                # статус активности меняется на пративоположную
                self.active = not self.active
            else:
                self.active = False
            # изменяем выбранный цвет рамки
            self.color = DARK_GRAY if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 14:  # если количество введённых символов не превышает 14
                        self.text += event.unicode
                NAME = self.text
                # добавляем текст
                self.txt_surface = FONT.render(self.text, True, WHITE)

    def draw(self, screen):
        # отрисовываем текст
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        # отрисовываем рамку
        pygame.draw.rect(screen, self.color, self.rect, 7)


# функция для вывода имени игрока
def score_name():
    return NAME
