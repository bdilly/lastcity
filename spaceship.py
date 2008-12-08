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
from game_entity import GameEntity
from world import World
from vector import Vector

class SpaceShip(GameEntity):
    def __init__(self, world, image, location, speed):
        GameEntity.__init__(self, world, "spaceship", image, location, speed)
        self.altitude = self.world.altitude_max
        self.set_destination()

    def set_destination(self):
        x, y = self.location
        w, h = self.image.get_size()
        ww, wh = self.world.size
        if x > 0:
            self.destination = Vector(0 - w/2, y)
        else:
            self.destination = Vector(ww + w/2, y)

    def act(self, time_passed):
        GameEntity.act(self, time_passed)
        if self.location == self.destination:
            self.lower_altitude()

    def lower_altitude(self):
        if self.altitude == 0:
            self.world.altitudes[self.altitude][1] = False
            self.destroy()
        elif not self.world.altitudes[self.altitude-1][1]:
            x, y = self.location
            self.world.altitudes[self.altitude][1] = False
            self.altitude -= 1
            self.world.altitudes[self.altitude][1] = True
            self.location = Vector(x, self.world.altitudes[self.altitude][0])
            self.set_destination()
            # flip the image
            self.image = pygame.transform.flip(self.image, 1, 0)

