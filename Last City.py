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

# imports
try:
    import pygame
    from pygame.locals import *
    import random, os, sys
except ImportError:
    print "One or more of the following modules couldn't be imported:"
    print "pygame, random, os, sys"
    exit()
# other game classes
from vector import Vector
from game_entity import GameEntity
from world import World
from spaceship import SpaceShip

# constants
SCREEN_SIZE = (800, 600)
IMAGE_DIR = "images"
SOUND_DIR = "sounds"
BACKGROUND_FILENAME = os.path.join(IMAGE_DIR, "background.png")
TARGET1_FILENAME = os.path.join(IMAGE_DIR, "target1.png")
TARGET2_FILENAME = os.path.join(IMAGE_DIR, "target2.png")
CITY_FILENAME = os.path.join(IMAGE_DIR, "city.png")
SHIELD_FILENAME = os.path.join(IMAGE_DIR, "shield.png")
SPACESHIP_FILENAMES = []
SPACESHIP_FILENAMES.append(os.path.join(IMAGE_DIR, "spaceship1.png"))
SPACESHIP_FILENAMES.append(os.path.join(IMAGE_DIR, "spaceship2.png"))
SPACESHIP_FILENAMES.append(os.path.join(IMAGE_DIR, "spaceship3.png"))



def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return


def display_text(message, screen, font, font_size, location, color):
    text_surface = font.render(message, True, (0,0,0))
    x = location[0] + font_size/2 - text_surface.get_width()/2
    y = location[1] + font_size/2 - text_surface.get_height()/2
    screen.blit(text_surface, (x, y))
    text_surface = font.render(message, True, color)
    x = location[0] - text_surface.get_width()/2
    y = location[1] - text_surface.get_height()/2
    screen.blit(text_surface, (x, y))
    pygame.display.update()

def run():
    # initializes pygame and set display
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE, 32)
    pygame.display.set_caption("Last City")

    #loads all images
    background_image = pygame.image.load(BACKGROUND_FILENAME).convert()
    target1_image = pygame.image.load(TARGET1_FILENAME).convert_alpha()
    target2_image = pygame.image.load(TARGET2_FILENAME).convert_alpha()
    city_image = pygame.image.load(CITY_FILENAME).convert_alpha()
    shield_image = pygame.image.load(SHIELD_FILENAME).convert_alpha()
    spaceship_images = []
    for i in range(3):
        spaceship_images.append(pygame.image.load(SPACESHIP_FILENAMES[i]).convert_alpha())

    # load font
    # FIXME change by a font distributed with the game
    # game_font = pygame.font.Font("game_font.ttf", 32)
    # score_font = pygame.font.Font("game_font.ttf", 16)
    font_size = 16
    game_font = pygame.font.SysFont("arial", 5*font_size)
    score_font = pygame.font.SysFont("arial", 2*font_size)

    message = "LAST CITY"

    while True:
        # create world
        world = World(background_image, SCREEN_SIZE)
        # create spaceship targets
        world.create_targets(target1_image, target2_image, city_image, shield_image)
        world.render(screen)
        #FIXME
        # display message in the screen
        x = world.size[0]/2
        y = world.size[1]/3
        display_text(message, screen, game_font, font_size, [x, y], (255, 0, 0))
        y = world.size[1]/2
        message = "Press 'fire' to start"
        display_text(message, screen, score_font, font_size, [x, y], (255, 0, 0))

        start = False
        while not start:
            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        show_menu()
                    elif event.key == K_SPACE:
                        start = True

        # start clock
        clock = pygame.time.Clock()

        # initialize variables:
        game_over = False
        spaceship_time = 0
        level = 0
        spaceships = 0
        score = 0
        waiting_new_level = False
        # cannon 0 is left and 1 is right
        active_cannon = 0
        use_bomb = False
        shoot = False

        # main game loop
        while not game_over:

            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        show_menu()
                    elif event.key == K_LEFT:
                        active_cannon = 0
                    elif event.key == K_RIGHT:
                        active_cannon = 1
                    elif event.key == K_UP:
                        use_bomb = True
                    elif event.key == K_SPACE:
                        shoot = True

            # verify if it's a new level
            if level == 0 or spaceships % (10 + level*5) == 0:
                # verify if all spaceships were destroyed
                busy = False
                for alt, state in world.altitudes:
                    busy += state
                if not busy:
                    spaceships = 0
                    waiting_new_level = False
                    world.add_target()
                    level += 1
                    #FIXME
                    print "level ", level
                else:
                    waiting_new_level = True

            # verify if a new spaceship can be created
            if spaceship_time == 0 and not world.altitudes[world.altitude_max][1] and not waiting_new_level:
                # select a spaceship image
                image = random.choice(spaceship_images)
                # select a speed
                speed = level/10. + random.random() * level/15.
                # select a location
                w, h = image.get_size()
                x = random.randint(0,1)
                if x == 0:
                    x = -w/2 - random.randint(0, 2 *w)
                    image = pygame.transform.flip(image, 1, 0)
                else:
                    x = w/2 + world.size[0] + random.randint(0, 2 *w)
                location = Vector(x, world.altitudes[world.altitude_max][0])
                # create spaceship
                ship = SpaceShip(world, image, location, speed)
                world.add_entity(ship)
                world.altitudes[world.altitude_max][1] = True
                spaceships += 1

            # objects move and the screen is update
            time_passed = clock.tick()
            game_over = world.actions(time_passed)
            world.render(screen)
            pygame.display.update()

        message =  "Game Over"

if __name__ == "__main__":
    run()
