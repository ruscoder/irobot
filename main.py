#!/usr/bin/python2.7
import sys
import pygame
import math
from random import randint

pygame.init()

STATE_MOVE = 0
STATE_ROTATE = 1

size = (width, height) = (640, 640)
offset = 10

sprite_size = (sprite_width, sprite_height) = (31, 31)

black = (0, 0, 0)
line_color = (255, 255, 255)
white = (255, 255, 255)
wall_color = (138, 0, 90)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("iRobot visual. Author: Laletin Vadim KI10-01")

background = pygame.image.load("laminat.png").convert()

main_rect = pygame.Rect(offset, offset, width - 2 * offset, height - 2 * offset)
#pygame.draw.rect(background, white, main_rect)

# Load images
deg = 0
to_deg = deg
speedx = 2
speedy = 0
state = STATE_MOVE
irobot = pygame.image.load("irobot.png").convert_alpha()
irobot_orig = irobot
irobot_rect = irobot.get_rect()
irobot_rect.move_ip((width - irobot_rect[2]) / 2, (height - irobot_rect[3]) / 2)

wall = pygame.Rect(offset, offset, sprite_width, sprite_height)
walls = []

# Make walls around
for i in range(0, width - sprite_width,  sprite_width):
	new_wall = wall.move(i, 0)
	walls.append(new_wall)
	pygame.draw.rect(background, wall_color, new_wall)

	new_wall = wall.move(i, height - sprite_height - offset * 2)
	walls.append(new_wall)
	pygame.draw.rect(background, wall_color, new_wall)
for i in range(sprite_height, height - sprite_height * 2,  sprite_height):
	new_wall = wall.move(0, i)
	walls.append(new_wall)
	pygame.draw.rect(background, wall_color, new_wall)

	new_wall = wall.move(width - sprite_width - offset * 2, i)
	walls.append(new_wall)
	pygame.draw.rect(background, wall_color, new_wall)

started = False
fps = 60
clock = pygame.time.Clock()


def irobot_rotate(deg):
	global irobot, irobot_rect
	# Save center
	old_center = irobot_rect.center
	# Rotate
	irobot = pygame.transform.rotate(irobot_orig, deg)
	irobot_rect = irobot.get_rect()
	# Restore center
	irobot_rect.center = old_center


def can_move_forward():
	global irobot_rect, walls, deg, speedx, speedy
	irobot_rect_new = irobot_rect.move(speedx * 2.5, speedy * 2.5)
	if irobot_rect_new.collidelist(walls) == -1:
		return True
	return False


font = pygame.font.Font(None, 20)
text = font.render("Mouse: left - Wall, right - God mode. KB: 1-5 - Speed, space - Start/Stop", 1, white)
textpos = text.get_rect(centerx=background.get_width() / 2, centery = height - 26)
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
				new_wall = wall.move(
					mouse_pos[0] - (mouse_pos[0] % sprite_width),
					mouse_pos[1] - (mouse_pos[1] % sprite_height)
				)
				if not irobot_rect.colliderect(new_wall):
					# Add walll to list
					walls.append(new_wall)
					# Draw wall
					pygame.draw.rect(background, wall_color, new_wall)
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
					print("Error while move irobot")

	if started:
		if state == STATE_ROTATE:
			if deg <= to_deg:
				deg += 2
				irobot_rotate(deg)
			else:
				speedx = math.trunc(math.cos(deg * math.pi / 180) * 5)
				speedy = -math.trunc(math.sin(deg * math.pi / 180) * 5)
				state = STATE_MOVE

		if state == STATE_MOVE:
			if can_move_forward():
				start_pos = irobot_rect.center
				irobot_rect.move_ip(speedx, speedy)
				pygame.draw.line(background, line_color, start_pos, irobot_rect.center, 1)
			else:
				deg_offset = randint(10, 125)
				to_deg = (deg + deg_offset)
				state = STATE_ROTATE

	screen.blit(background, (0, 0))
	screen.blit(irobot, irobot_rect)

	text = font.render("FPS: %d" % fps, 1, white)
	textpos = text.get_rect(centerx=background.get_width() / 2, centery = 26)
	screen.blit(text, textpos)
	pygame.display.flip()



