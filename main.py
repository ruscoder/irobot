#!/usr/bin/python2.7
import sys
import pygame

pygame.init()

size = (width, height) = 640, 480
speed = [2, 2]
black = (0, 0, 0)

screen = pygame.display.set_mode(size)

# Load images
irobot = pygame.image.load("irobot.bmp")
irobot_rect = irobot.get_rect()
`

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.fill(black)
	pygame.display.flip()
