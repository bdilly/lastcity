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

class World(object):

    def __init__(self, image, screen_size):
        self.entities = {}
        self.entity_id = 0
        self.targets = []
        self.targets_count = 0
        self.background = image
        self.size = screen_size
        # spaceships can fly in 4 different altitudes
        self.altitude_max = 3
        self.altitudes = []
        wh = self.size[1]
        distance = wh/6
        for alt in range(self.altitude_max+1):
            self.altitudes.append([wh - (distance * (alt+2) + distance / 2), False])

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

    def actions(self, time_passed):
        for entity in self.entities.values():
            entity.act(time_passed)

    def render(self, surface):
        surface.blit(self.background, (0,0))
        for entity in self.entities.values():
            entity.render(surface)

    def create_targets(self, target1_image, target2_image, city_image, shield_image):
        images = (target2_image, pygame.transform.flip(target2_image, 1, 0), target1_image,
                  pygame.transform.flip(target1_image, 1, 0), shield_image, city_image)
        locs_x = [int(x / 32. * self.size[0]) for x in [6, 26, 10, 22, 16, 16]]
        locs_y = [int(y / 24. * self.size[1]) for y in [19, 19, 19, 19, 20, 20]]
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
        return self.targets[self.targets_count-1]

    def remove_target(self, target):
        self.targets_count -= 1
        self.targets[targets_count].destroy
