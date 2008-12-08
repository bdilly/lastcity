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

class World(object):

    def __init__(self, image, screen_size):
        self.entities = {}
        self.entity_id = 0
        # start the game with 6 targets
        self.targets_count = 6
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
