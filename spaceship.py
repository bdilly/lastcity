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
        self.target = None
        self.set_destination()

    def set_destination(self):
        x, y = self.location
        w, h = self.image.get_size()
        ww, wh = self.world.size
        if x > 0:
            self.destination = Vector(0 - w/2, y)
        else:
            self.destination = Vector(ww + w/2, y)
        if self.altitude == 0:
            self.target = self.world.get_next_target()
            if self.target:
                # need to destroy the next target
                tx, ty = self.target.location
                self.future_destination = self.destination
                self.destination = Vector(tx, y)

    def act(self, time_passed):
        GameEntity.act(self, time_passed)
        if self.location == self.destination:
            self.change_destination()

    def change_destination(self):
        if self.altitude == 0:
            if self.target:
                # it reached the target
                self.fire(self.target)
                self.target = None
                self.destination = self.future_destination
            else:
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

    def fire(self, target):
        # FIXME
        print "FIRE!"
        self.world.remove_target(target)
