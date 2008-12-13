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

MAX_COOLDOWN = 400

class Cannon(GameEntity):
    def __init__(self, world, image, location):
        GameEntity.__init__(self, world, "cannon", image, location, 0)
        self.cooldown = MAX_COOLDOWN

    def act(self, time_passed):
        self.cooldown += time_passed
        if self.cooldown >= MAX_COOLDOWN:
            self.cooldown = MAX_COOLDOWN

    def fire(self, target):
        if MAX_COOLDOWN > 0:
            #FIXME
            print "FIRE!"
            self.cooldown -= MAX_COOLDOWN/4
