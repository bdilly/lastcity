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
BULLET_FILENAME = os.path.join(IMAGE_DIR, "bullet.png")
SPACESHIP_FILENAMES = []
SPACESHIP_FILENAMES.append(os.path.join(IMAGE_DIR, "spaceship1.png"))
SPACESHIP_FILENAMES.append(os.path.join(IMAGE_DIR, "spaceship2.png"))
SPACESHIP_FILENAMES.append(os.path.join(IMAGE_DIR, "spaceship3.png"))
CANNON_FILENAME = os.path.join(IMAGE_DIR, "cannon.png")



def show_menu(screen, font, font_size):
    dark = screen.convert()
    before_dark = dark.copy()
    dark.fill([0,0,0])
    dark.set_alpha(90)
    #make current screen darker
    screen.blit(dark,[0,0])
    pygame.display.update()

    menu = 0
    active_option = 0

    messages = [["RESUME", "CONTROLS", "HELP", "CREDITS", "QUIT"],
                ["SELECT LEFT CANNON", "SELECT RIGHT CANNON", "FIRE", "USE BOMB"]]

    while True:
        max_option = len(messages[menu])
        # handle input
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if menu == 0:
                        # resume
                        screen.blit(before_dark,[0,0])
                        pygame.display.update()
                        return
                    else:
                        menu = 0
                        active_option = 0
                elif event.key == K_UP:
                    active_option -= 1
                elif event.key == K_DOWN:
                    active_option += 1
                elif event.key == K_RETURN:
                    if menu == 0 and active_option == 0:
                        # resume
                        screen.blit(before_dark,[0,0])
                        pygame.display.update()
                        return
                    elif menu == 0 and active_option == 4:
                        # quit
                        sys.exit()
                    elif menu == 0:
                        menu = active_option
                        active_option = 0

        if active_option < 0:
            active_option = max_option - 1
        elif active_option == max_option:
            active_option = 0

        # create messages to be displayed
        disp_messages = messages[menu][:]
        disp_messages[active_option] = "> " + disp_messages[active_option] + " <"

        # show the menu
        screen.blit(before_dark,[0,0])
        screen.blit(dark,[0,0])
        w, h = screen.get_size()
        gap = h/(len(disp_messages)+2)
        y = 0
        for message in disp_messages:
            y = y + gap
            text_surface = font.render(message, True, (255,255,255))
            tw, th = text_surface.get_size()
            screen.blit(text_surface, (w/2 - tw/2, y))
        pygame.display.update()


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_p or event.key == K_PAUSE:
                    return


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
    l_cannon_image = pygame.image.load(CANNON_FILENAME).convert_alpha()
    r_cannon_image = pygame.transform.flip(l_cannon_image, 1, 0)
    bullet_image = pygame.image.load(BULLET_FILENAME).convert_alpha()
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

    # initialize some variables
    message = "LAST CITY"
    hi_score = 0

    while True:
        # create world
        world = World(background_image, bullet_image, SCREEN_SIZE,
                      font_size, game_font, score_font, hi_score)
        # create spaceship targets
        world.create_targets(target1_image, target2_image, city_image, shield_image)
        world.create_cannons(l_cannon_image, r_cannon_image)
        world.render(screen)
        # display message in the screen
        x = world.size[0]/2
        y = world.size[1]/3
        world.display_text(message, screen, game_font, font_size, [x, y], (255, 0, 0))
        y = world.size[1]/2
        message = "Press 'fire' to start"
        world.display_text(message, screen, score_font, font_size, [x, y], (255, 0, 0))
        # update the display
        pygame.display.update()

        start = False
        while not start:
            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        show_menu(screen, game_font, font_size)
                    elif event.key == K_SPACE:
                        start = True

        # start clock
        clock = pygame.time.Clock()

        # initialize variables:
        game_over = False
        spaceship_time = 0
        level = 0
        spaceships = 0
        waiting_new_level = False
        # cannon 0 is left and 1 is right
        active_cannon = 0
        enabled_bomb = True
        use_bomb = False
        shoot = False

        # main game loop
        while not game_over:

            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        show_menu(screen, game_font, font_size)
                        clock.tick()
                    if event.key == K_p or event.key == K_PAUSE:
                        pause()
                        clock.tick()
                    elif event.key == K_LEFT:
                        active_cannon = 0
                    elif event.key == K_RIGHT:
                        active_cannon = 1
                    elif event.key == K_UP:
                        if enabled_bomb:
                            use_bomb = True
                            enabled_bomb = False
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
                    enabled_bomb = True
                    world.render(screen)
                    message = "Level %02d" % level
                    x = world.size[0]/2
                    y = world.size[1]/2
                    world.display_text(message, screen, game_font, font_size, [x, y], (0, 255, 0))
                    # update the display
                    pygame.display.update()
                    #FIXME
                    pygame.time.wait(1500)
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
            game_over = world.actions(time_passed, use_bomb, active_cannon, shoot)
            use_bomb = False
            shoot = False
            world.render(screen)
            pygame.display.update()

        message =  "Game Over"
        if world.score > hi_score:
            hi_score = world.score


if __name__ == "__main__":
    run()
