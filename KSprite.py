import pygame
from pygame.locals import *

# This class is a Sprite View that knows how to draw itself to a screen and tracks its current position
class KSprite(pygame.sprite.Sprite):
    	def __init__(self, file):
		pygame.sprite.Sprite.__init__(self)	
		self.image = pygame.image.load(file)
		self.rect = self.image.get_rect()

	# Draw to the given screen at the saved position
        def draw(self, screen):
            screen.blit(self.image, self.rect)
