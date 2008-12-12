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

class GameEntity(object):

    def __init__(self, world, kind, image, location, speed = 0):
        self.world = world
        self.kind = kind
        self.image = image
        self.location = location
        self.speed = speed
        self.destination = location

    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))

    def act(self, time_passed):
        if self.speed > 0 and self.location != self.destination:
            path_to_destination = self.destination - self.location
            distance_to_destination = path_to_destination.get_magnitude()
            path_to_destination.normalize()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += path_to_destination * travel_distance

    def destroy(self):
        self.world.remove_entity(self)
