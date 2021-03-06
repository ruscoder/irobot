"""
This module contains classes for main module
Wall for walls and Robot
"""

import pygame
import math
from constant import *


class Wall(pygame.sprite.Sprite):
    """
    Wall Class
    Static sprite, rendered to static background
    """

    def __init__(self, x, y):
        """
        Constructor initializes new rect in
        x and y coordinates.
        Also generates mask (square)
        """
        super(Wall, self).__init__()
        self.rect = pygame.Rect(
            OFFSET + x, OFFSET + y,
            SPRITE_WIDTH, SPRITE_HEIGHT
        )
        self.image = pygame.Surface(SPRITE_SIZE)

        # Mask is constantly - square
        self.mask = pygame.mask.Mask(SPRITE_SIZE)
        self.mask.fill()

    def render(self, background):
        """This method render sprite to static background"""
        pygame.draw.rect(background, COLOR_WALL, self.rect)


class Robot(pygame.sprite.Sprite):
    """Robot sprite class"""

    def __init__(self, screen, walls):
        """
        Constructor initializes new sprite, load image.
        Create mask from image, defines startup vars.
        """
        super(Robot, self).__init__()
        self.walls = walls
        self.image = pygame.image.load("irobot.png").convert_alpha()
        self.image_orig = self.image

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.to_deg = self.deg = 0

        self.speedx = 2
        self.speedy = 0

        # Move to center
        self.rect.move_ip(
            (screen.get_width() - self.image.get_width()) / 2,
            (screen.get_height() - self.image.get_height()) / 2
        )

    def move_forward(self):
        """This method changes coords by speed"""
        self.rect.move_ip(self.speedx, self.speedy)

    def render(self, screen):
        """"This method render sprite to screen"""
        screen.blit(self.image, self.rect)

    def compute_speed(self):
        """Compute speed X and Y for this degree"""
        self.speedx = math.trunc(math.cos(self.deg * math.pi / 180) * 5)
        self.speedy = -math.trunc(math.sin(self.deg * math.pi / 180) * 5)

    def rotate(self, deg):
        """Rotate image for this degree"""
        self.deg += deg
        # Save center
        old_center = self.rect.center
        # Rotate
        self.image = pygame.transform.rotate(self.image_orig, self.deg)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # Restore center
        self.rect.center = old_center

    def can_move_forward(self):
        """This method returns True if sprite can move forward"""
        old_rect = self.rect
        self.rect = self.rect.move(self.speedx, self.speedy)
        can = pygame.sprite.spritecollideany(
            self, self.walls,
            pygame.sprite.collide_mask) is None
        self.rect = old_rect
        return can
