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

import math

class Vector(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        magnitude = self.get_magnitude()
        self.x /= magnitude
        self.y /= magnitude

    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)

    def __iter__(self):   
        return iter([self.x, self.y])

    def __eq__(self, rhs):
        return self.x == rhs.x and self.y == rhs.y

    def __ne__(self, rhs):
        return self.x != rhs.x or self.y != rhs.y

