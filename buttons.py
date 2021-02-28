import pygame
from pygame import *
from main import *
from settings import *

def draw_main_menu_button(screen, mouse_click=False):
    global GAME_OFF, SELECTED_MODE, NIGHT, LIGHT_MASK, ENEMY_SPEED, BACKGROUND_MUSIC
    play_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 - 20, WIN_WIDTH / 3, 50)
    draw_button(screen, play_button, 'Play game')

    tutorial_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 40, WIN_WIDTH / 3, 50)
    draw_button(screen, tutorial_button, 'Tutorial')

    mode_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 100, WIN_WIDTH / 3, 50)
    draw_button(screen, mode_button, SELECTED_MODE)

    records_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 160, WIN_WIDTH / 3, 50)
    draw_button(screen, records_button, 'Records')

    quit_button = pygame.Rect(WIN_WIDTH / 9, WIN_HEIGHT / 2 + 220, WIN_WIDTH / 3, 50)
    draw_button(screen, quit_button, 'Quit')

    if mouse_click:
        if mouse_click.button == 1:
            if button_intersection(play_button):
                game()

            if button_intersection(tutorial_button):
                pass

            if button_intersection(mode_button):
                if 'NORMAL' in SELECTED_MODE:
                    SELECTED_MODE = 'mode: NIGHT'
                    NIGHT = True
                elif 'NIGHT' in SELECTED_MODE:
                    SELECTED_MODE = 'mode: HARD'
                    NIGHT = True
                    LIGHT_MASK = "light_350_soft.png"
                    BACKGROUND_MUSIC = 'first.ogg'
                    ENEMY_SPEED = 4
                elif 'HARD' in SELECTED_MODE:
                    SELECTED_MODE = 'mode: NORMAL'
                    NIGHT = False
                    LIGHT_MASK = "light_350_med.png"
                    BACKGROUND_MUSIC = 'second.ogg'
                    ENEMY_SPEED = 2

            if button_intersection(quit_button):
                exit()
