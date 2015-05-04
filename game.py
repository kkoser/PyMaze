import sys
import os
from math import *
import pygame
from pygame.locals import *
from MainMenuScreen import MainMenuScreen
from GameScreen import GameScreen

class GameSpace:
	playerNumber = -1
	connection = None
	
	def main(self):
		# 1) basic init
		pygame.init()

		self.size = self.width, self.height = 480, 480

		self.black = 0, 0, 0

		self.screen = pygame.display.set_mode(self.size)
		self.mainMenuScreen = MainMenuScreen(self)
		self.gameScreen = GameScreen(self)
		self.activeScreen = self.mainMenuScreen

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
