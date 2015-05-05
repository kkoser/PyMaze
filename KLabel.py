import pygame
from pygame.locals import *

## This class is a Label View that knows how to draw itself on the screen and tracks its position
class KLabel():
    	def __init__(self, text, font, x, y):
		self.text = text
                self.font = font
                self.x = x
                self.y = y
                self.color = (255,255,255)
		self.rect = Rect(x,y,0,0)

	# Draws itself to the given screen at saved position
        def draw(self, screen):
            drawText = self.font.render(self.text, 1,self.color)
	    self.rect = drawText.get_rect().move(self.x,self.y)
            screen.blit(drawText, (self.x,self.y))
