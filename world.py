#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# Author:
#   Bruno Dilly <bruno.dilly@brunodilly.org>
#
# Copyright (C) 2008 Bruno Dilly
#
# Released under GNU GPL, read the file 'COPYING' for more information
# ----------------------------------------------------------------------

import pygame
from vector import Vector
from game_entity import GameEntity
from cannon import Cannon

class World(object):

    def __init__(self, image, bullet_image, screen_size, font_size, game_font, score_font, hi_score):
        self.entities = {}
        self.entity_id = 0
        self.targets = []
        self.targets_count = 0
        self.background = image
        self.bullet_image = bullet_image
        self.size = screen_size
        # spaceships can fly in 4 different altitudes
        self.altitude_max = 3
        self.altitudes = []
        wh = self.size[1]
        distance = wh/6
        for alt in range(self.altitude_max+1):
            self.altitudes.append([wh - (distance * (alt+2) + distance / 2), False])
        self.hi_score = hi_score
        self.score = 0
        self.font_size = font_size
        self.game_font = game_font
        self.score_font = score_font

    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def actions(self, time_passed, use_bomb, active_cannon, shoot):
        for entity in self.entities.values():
            entity.act(time_passed)
        if shoot:
            if active_cannon == 0:
                self.left_cannon.fire()
            else:
                self.right_cannon.fire()
        if self.targets_count == 0:
            return True
        return False

    def render(self, surface):
        surface.blit(self.background, (0,0))
        for entity in self.entities.values():
            entity.render(surface)
        self.display_score(surface)

    def create_targets(self, target1_image, target2_image, city_image, shield_image):
        images = (city_image, shield_image, pygame.transform.flip(target1_image, 1, 0),
                  target1_image, pygame.transform.flip(target2_image, 1, 0), target2_image)
        locs_x = [int(x / 32. * self.size[0]) for x in [16, 16, 22, 10, 26, 6]]
        locs_y = [int(y / 24. * self.size[1]) for y in [20, 20, 20, 20, 19, 19]]
        for target_i in range(6):
            location = Vector(locs_x[target_i], locs_y[target_i])
            target = GameEntity(self, "target", images[target_i], location, 0)
            self.add_entity(target)
            self.targets.append(target)
            self.targets_count += 1

    def add_target(self):
        if self.targets_count < len(self.targets):
            t = self.targets[self.targets_count]
            target = GameEntity(self, "target", t.image, t.location, 0)
            self.add_entity(target)
            self.targets[self.targets_count] = target
            self.targets_count += 1

    def get_next_target(self):
        if self.targets_count > 0:
            return self.targets[self.targets_count-1]
        else:
            return None

    def remove_target(self, target):
        self.targets_count -= 1
        target.destroy()

    def display_text(self, message, screen, font, font_size, location, color):
        text_surface = font.render(message, True, (0,0,0))
        x = location[0] + font_size/2 - text_surface.get_width()/2
        y = location[1] + font_size/2 - text_surface.get_height()/2
        screen.blit(text_surface, (x, y))
        text_surface = font.render(message, True, color)
        x = location[0] - text_surface.get_width()/2
        y = location[1] - text_surface.get_height()/2
        screen.blit(text_surface, (x, y))

    def display_score(self, screen):
        y = self.size[1] - 1.5 * self.font_size
        x = 10 * self.font_size
        message = "HI-SCORE   %08d" % self.hi_score
        self.display_text(message, screen, self.score_font, self.font_size/2, [x, y], (0, 255, 0))
        x = self.size[0] - 10 * self.font_size
        message = "SCORE      %08d" % self.score
        self.display_text(message, screen, self.score_font, self.font_size/2, [x, y], (0, 255, 0))

    def create_cannons(self, l_cannon_image, r_cannon_image):
        l_location = Vector( 1 / 16. * self.size[0], 19 / 24. * self.size[1])
        r_location = Vector( 15 / 16. * self.size[0], 19 / 24. * self.size[1])
        self.left_cannon = Cannon(self, l_cannon_image, l_location)
        self.add_entity(self.left_cannon)
        self.right_cannon = Cannon(self, r_cannon_image, r_location)
        self.add_entity(self.right_cannon)

