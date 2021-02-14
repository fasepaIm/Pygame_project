# !/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import pygame


class ParticlePrinciple:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.particles_2 = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(self.screen, pygame.Color('Gray'), particle[0], int(particle[1]))

            for particle in self.particles_2:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(self.screen, pygame.Color(rgb(148, 154, 93)), particle[0], int(particle[1]))


    def add_particles(self, left, right, up, down, center_coords):
        #pos_x = pygame.mouse.get_pos()[0]
        #pos_y = pygame.mouse.get_pos()[1]
        pos_x_1, pos_y_1 = center_coords
        pos_x_2, pos_y_2 = center_coords
        if left:
            pos_x_1 += 12
            pos_x_2 += 12
            pos_y_1 += 12
            pos_y_2 -= 12
        elif right:
            pos_x_1 -= 12
            pos_x_2 -= 12
            pos_y_1 += 12
            pos_y_2 -= 12
        elif up:
            pos_x_1 -= 12
            pos_x_2 += 12
            pos_y_1 += 12
            pos_y_2 += 12
        elif down:
            pos_x_1 -= 12
            pos_x_2 += 12
            pos_y_1 -= 12
            pos_y_2 -= 12
        radius = 4
        direction_x_1 = random.randint(-3, 3)
        direction_y_1 = random.randint(-3, 3)

        direction_x_2 = random.randint(-2, 4)
        direction_y_2 = random.randint(-2, 4)

        particle_circle = [[pos_x_1, pos_y_1], radius, [direction_x_1, direction_y_1]]
        particle_circle_1 = [[pos_x_2, pos_y_2], radius, [direction_x_2, direction_y_2]]
        self.particles.append(particle_circle)
        self.particles.append(particle_circle_1)


    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy
        particle_copy = [particle for particle in self.particles_2 if particle[1] > 0]
        self.particles_2 = particle_copy
