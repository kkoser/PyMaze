import sys
import os
from math import *
import pygame
from pygame.locals import *
from MainMenuScreen import MainMenuScreen

class GameSpace:
	
	def main(self):
		# 1) basic init
		pygame.init()

		self.size = self.width, self.height = 640, 480

		self.black = 0, 0, 0

		self.screen = pygame.display.set_mode(self.size)
		self.mainMenu = MainMenuScreen(self)
		#self.gameScreen = GameScreen(self)
		self.activeScreen = self.mainMenu

	def tick(self):
		# 5) handle user input events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			self.activeScreen.handleEvent(event)


		# 6) ongoing behavior
		self.activeScreen.tick()

		# 7) drawing
		self.screen.fill(self.black)
		self.activeScreen.draw(self.screen)
		pygame.display.flip()
