import sys
import os
from math import *
import pygame
from pygame.locals import *

class KLabel():
    	def __init__(self, text, font, x, y):
		self.text = text
                self.font = font
                self.x = x
                self.y = y
                self.color = (255,255,255)

        def draw(self, screen):
            drawText = self.font.render(self.text, self.color)
            screen.blit(drawText, (self.x,self.y))
