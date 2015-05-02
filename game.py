import sys
import os
from math import *
import pygame
from pygame.locals import *

class GameSpace:
	def main(self):
		# 1) basic init
		pygame.init()

		self.size = self.width, self.height = 640, 480

		self.black = 0, 0, 0

		self.screen = pygame.display.set_mode(self.size)
	
		# 2) set up game objects
		self.clock = pygame.time.Clock()

		# 3) start game loop
		while 1:
			# 4) regulate tick speed
			self.clock.tick(60)

			# 5) handle user input events
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					#self.player.moveForKey(event.key)
					#self.ball.move(event.key)
                                if event.type == pygame.QUIT:
                                    sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					#self.projectile = self.player.fire(self.enemy)


			# 6) ongoing behavior

			# 7) animation
			self.screen.fill(self.black)
			#if self.enemy:
			#	self.screen.blit(self.enemy.image, self.enemy.rect)
				
                        pygame.display.flip()


gs = GameSpace()
gs.main()

