#!/usr/bin/python2.7
import sys
import pygame

pygame.init()

size = (width, height) = (640, 480)
offset = 10

sprite_size = (sprite_width, sprite_height) = (31, 23)

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
irobot_rect = irobot.get_rect().move(width / 2, height / 2)

wall = pygame.Rect(offset, offset, sprite_width, sprite_height)
walls = []

# Make walls around
for i in range(0, width - sprite_width,  sprite_width):
	new_wall = wall.move(i, 0)
	walls.append(new_wall)
	pygame.draw.rect(background, grey, new_wall)

	new_wall = wall.move(i, height - sprite_height - offset * 2)
	walls.append(new_wall)
	pygame.draw.rect(background, grey, new_wall)
for i in range(sprite_height, height - sprite_height * 2,  sprite_height):
	new_wall = wall.move(0, i)
	walls.append(new_wall)
	pygame.draw.rect(background, grey, new_wall)

	new_wall = wall.move(width - sprite_width - offset * 2, i)
	walls.append(new_wall)
	pygame.draw.rect(background, grey, new_wall)

started = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Draw walls
			if event.button == 1 and not started:
				mouse_pos = pygame.mouse.get_pos()
				new_wall = wall.move(
					mouse_pos[0] - (mouse_pos[0] % sprite_width),
					mouse_pos[1] - (mouse_pos[1] % sprite_height)
				)
				if not irobot_rect.colliderect(new_wall):
					# Add walll to list
					walls.append(new_wall)
					# Draw wall
					pygame.draw.rect(background, grey, new_wall)
				else:
					print("Error while adding new wall")

			# Move irobot
			if event.button == 3 and not started:
				mouse_pos = pygame.mouse.get_pos()
				posx = mouse_pos[0] - irobot_rect[0] - irobot_rect[2] / 2
				posy = mouse_pos[1] - irobot_rect[1] - irobot_rect[3] / 2
				new_irobot_rect = irobot_rect.move(
					posx,
					posy
				)
				if new_irobot_rect.collidelist(walls) == -1:
					irobot_rect = new_irobot_rect
				else:
					print("error")

	screen.blit(background, (0, 0))
	screen.blit(irobot, irobot_rect)
	pygame.display.flip()
