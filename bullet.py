#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# Author:
#   Bruno Dilly <bruno.dilly@brunodilly.org>
#
# Copyright (C) 2008 Bruno Dilly
#
# Released under GNU GPL, read the file 'COPYING' for more information
# ---------------------------------------------------------------------

import pygame
from game_entity import GameEntity
from vector import Vector

BULLET_SPEED = 0.3

class Bullet(GameEntity):
    def __init__(self, world, image, location, destination):
        GameEntity.__init__(self, world, "bullet", image, location, BULLET_SPEED)
        self.destination = destination

    def act(self, time_passed):
        GameEntity.act(self, time_passed)
        if self.location == self.destination:
            self.destroy()

