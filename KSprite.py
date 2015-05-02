import sys
import os
from math import *
import pygame
from pygame.locals import *

class KSprite(pygame.sprite.Sprite):
    	def __init__(self, file):
		pygame.sprite.Sprite.__init__(self)	
		self.image = pygame.image.load(file)
		self.rect = self.image.get_rect()

        def draw(self, screen):
            screen.blit(self.image, self.rect)
