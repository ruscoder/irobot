import pygame
from constant import *

class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Wall, self).__init__()
		self.rect = pygame.Rect(OFFSET + x, OFFSET + y, SPRITE_WIDTH, SPRITE_HEIGHT)
		self.image = pygame.Surface(SPRITE_SIZE)

		# Mask is constantly - square
		self.mask = pygame.mask.Mask(SPRITE_SIZE)
		self.mask.fill()


	def render(self, background):
		pygame.draw.rect(background, COLOR_WALL, self.rect)


