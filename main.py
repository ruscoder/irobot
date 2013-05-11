#!/usr/bin/python2.7
import sys
import pygame

pygame.init()

size = (width, height) = (640, 480)
offset = 10

sprite_size = (sprite_width, sprite_height) = (20, 20)
sprite_obj = pygame.Rect(0, 0, sprite_width, sprite_height)

black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("iRobot visual")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

main_rect = pygame.Rect(offset, offset, width - 2 * offset, height - 2 * offset)
pygame.draw.rect(background, white, main_rect)

# Load images
irobot = pygame.image.load("irobot.bmp")
irobot_rect = irobot.get_rect()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			mouse_pos = pygame.mouse.get_pos()
			sprite_offsetted = sprite_obj.move(
				mouse_pos[0] - (mouse_pos[0] % sprite_width),
				mouse_pos[1] - (mouse_pos[1] % sprite_height)
			)
		 	pygame.draw.rect(background, grey, sprite_offsetted)


	screen.blit(background, (0, 0))
	pygame.display.flip()
