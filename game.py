import pygame
from pygame.locals import *
from MainMenuScreen import MainMenuScreen
from GameScreen import GameScreen

## This class controls the game window, and tells the current screen to draw
## It should be instantiated by player.py, so that Twisted can handle the game loop
class GameSpace:
	# The playerNumber of this game instance
	playerNumber = -1
	# The connection so that screens may send new game states back
	connection = None
	
	# Basic Intialization
	def main(self):
		pygame.init()

		self.size = self.width, self.height = 480, 520

		self.black = 0, 0, 0

		self.screen = pygame.display.set_mode(self.size)
		self.mainMenuScreen = MainMenuScreen(self)
		self.gameScreen = GameScreen(self)
		self.activeScreen = self.mainMenuScreen

	def tick(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			self.activeScreen.handleEvent(event)


		#Ongoing behavior
		self.activeScreen.tick()

		#Drawing
		self.screen.fill(self.black)
		self.activeScreen.draw(self.screen)
		pygame.display.flip()
