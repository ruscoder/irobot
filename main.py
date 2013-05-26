#!/usr/bin/python2.7
import sys
import pygame
from pygame import sprite
from random import randint
from sprites import Robot, Wall
from constant import *


# Main
pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("iRobot visual. Author: Laletin Vadim KI10-01")

background = pygame.image.load("laminat.png").convert()

walls = sprite.Group()
irobot = Robot(screen, walls)

# Make walls around
for i in range(0, WIDTH - SPRITE_WIDTH, SPRITE_WIDTH):
    up_wall = Wall(i, 0)
    up_wall.render(background)

    down_wall = Wall(i, HEIGHT - SPRITE_HEIGHT - OFFSET * 2)
    down_wall.render(background)

    walls.add(up_wall, down_wall)

for i in range(SPRITE_HEIGHT, HEIGHT - SPRITE_HEIGHT * 2, SPRITE_HEIGHT):
    left_wall = Wall(0, i)
    left_wall.render(background)

    right_wall = Wall(WIDTH - SPRITE_WIDTH - OFFSET * 2, i)
    right_wall.render(background)

    walls.add(left_wall, right_wall)

started = False
fps = 60
clock = pygame.time.Clock()
state = STATE_MOVE

font = pygame.font.Font(None, 20)
text = font.render(
    "Mouse: left - Wall. Right - God mode." +
    "KB: 1-5 - Speed, space - Start/Stop",
    1,
    COLOR_BLACK
)
textpos = text.get_rect(centerx=background.get_width() / 2,
                        centery=HEIGHT - 26)
background.blit(text, textpos)

while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Start the work
            if event.unicode == " ":
                started = not started
            if event.unicode in ["1", "2", "3", "4", "5"]:
                fps = int(event.unicode) * 60

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Draw walls
            if event.button == 1 and not started:
                mouse_pos = pygame.mouse.get_pos()
                new_wall = Wall(
                    mouse_pos[0] - (mouse_pos[0] % SPRITE_WIDTH),
                    mouse_pos[1] - (mouse_pos[1] % SPRITE_HEIGHT)
                )

                if sprite.collide_mask(new_wall, irobot) is None:
                    new_wall.render(background)
                    walls.add(new_wall)
                else:
                    print("Error while adding new wall")

            # Move irobot
            if event.button == 3 and not started:
                    mouse_pos = pygame.mouse.get_pos()
                    posx = mouse_pos[0] - irobot.rect[0] - irobot.rect[2] / 2
                    posy = mouse_pos[1] - irobot.rect[1] - irobot.rect[3] / 2
                    old_rect = irobot.rect
                    irobot.rect = irobot.rect.move(posx, posy)
                    if sprite.spritecollideany(irobot, walls,
                                               sprite.collide_mask):
                        irobot.rect = old_rect
                        print("Error while move irobot")

    if started:
        if state == STATE_ROTATE:
            if irobot.deg <= irobot.to_deg:
                irobot.rotate(2)
            else:
                irobot.compute_speed()
                state = STATE_MOVE

        if state == STATE_MOVE:
            if irobot.can_move_forward():
                start_pos = irobot.rect.center
                irobot.move_forward()
                pygame.draw.line(
                    background,
                    COLOR_LINE,
                    start_pos,
                    irobot.rect.center,
                    1
                )
            else:
                irobot.to_deg = (irobot.deg + randint(10, 125))
                state = STATE_ROTATE

    screen.blit(background, (0, 0))
    irobot.render(screen)

    text = font.render("FPS: %d" % clock.get_fps(), 1, COLOR_BLACK)
    textpos = text.get_rect(centerx=background.get_width() / 2, centery=26)
    screen.blit(text, textpos)

    pygame.display.flip()
