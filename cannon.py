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
from vector import Vector
from bullet import Bullet

MAX_COOLDOWN = 800

class Cannon(GameEntity):
    def __init__(self, world, image, location):
        GameEntity.__init__(self, world, "cannon", image, location, 0)
        self.cooldown = MAX_COOLDOWN

    def act(self, time_passed):
        self.cooldown += time_passed
        if self.cooldown >= MAX_COOLDOWN:
            self.cooldown = MAX_COOLDOWN

    def fire(self):
        if self.cooldown > 0:
            self.cooldown -= MAX_COOLDOWN * 1.2
            x, y = self.location
            w, h = self.image.get_size()
            bullet_image = self.world.bullet_image
            bw, bh = bullet_image.get_size()
            if x < self.world.size[0]/2:
                # left cannon fire
                bullet_location = Vector(x+w/2, y-h/2)
            else:
                # right cannon fire
                bullet_location = Vector(x-w/2, y-h/2)
            bullet_destination = Vector(self.world.size[0] - x -w/2 + bh/2, 0)
            bullet = Bullet(self.world, bullet_image,
                            bullet_location, bullet_destination)
            self.world.add_entity(bullet)

