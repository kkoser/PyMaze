import sys
import os
import math
import pygame
from pygame.locals import *
from KSprite import KSprite
from KLabel import KLabel
from MazeView import MazeView

## This class contains all of the views and logic needed for the actual gameplay screen.
class GameScreen:
    #Handles UI Setup
    def setup(self):
        #Add in the avatars and maze here
        self.mazeView = MazeView(self)
        self.aang = KSprite("images/aang.gif")
        self.aang.rect.move_ip(200,200)
        self.katara = KSprite("images/katara.png")
        self.katara.rect.move_ip(400,200)

        self.font = pygame.font.Font(None,30)
        self.turnLabel = KLabel("Your Turn", self.font, 20,490)

        self.bigFont = pygame.font.Font(None, 45)
        self.gameOverLabel = KLabel("You win!", self.bigFont, 150,300)

        self.state = None

    def __init__(self, gs):
        self.gs = gs
        self.setup()

    # Draws all of the screens views to the given screen
    def draw(self, screen):
        screen.fill(self.gs.black)

        #Ensure that we draw the maze around the opposite of our player
        if self.gs.playerNumber == self.state.aangPlayerNumber:
            self.mazeView.drawAroundPoint(screen, self.state.kataraPosition)
        else:
            self.mazeView.drawAroundPoint(screen, self.state.aangPosition)

        self.aang.draw(screen)
        self.katara.draw(screen)
        self.turnLabel.draw(screen)

        if self.checkGameOver():
            self.gameOverLabel.draw(screen)

    # Returns true if the players are in a winning position (same location)
    def checkGameOver(self):
        if self.state.aangPosition == self.state.kataraPosition:
            return True
        return False

    # Returns true if a given position is valid on this maze
    def isValidPosition(self, (x,y)):
        # Check for out of bounds positions
        if x < 0 or y < 0:
            return False
        if x > 9 or y > 9:
            return False

        # Check board to see if there is a wall there
        if self.mazeView.mazeDesc[y][x] == "0":
            return True

        return False

    # Moves a player in the direction indicated by the key, if valid
    def move(self, key):
        if self.gs.playerNumber == self.state.aangPlayerNumber:
            pos = self.state.aangPosition
        else:
            pos = self.state.kataraPosition

        #Create new pos
        if key == pygame.K_UP:
            pos = (pos[0], pos[1]-1)
        elif key == pygame.K_DOWN:
            pos = (pos[0], pos[1]+1)
        elif key == pygame.K_LEFT:
            pos = (pos[0]-1, pos[1])
        elif key == pygame.K_RIGHT:
            pos = (pos[0]+1, pos[1])

        #Complete move if it is valid
        if self.isValidPosition(pos):
            if self.gs.playerNumber == self.state.aangPlayerNumber:
                self.state.aangPosition = pos
            else:
                self.state.kataraPosition = pos

            #Send new state to partner over server
            self.gs.connection.sendGameState(self.state)
        

    # Handles keyboard events for moving
    def handleEvent(self, event):
        if self.state.playerTurnNumber != self.gs.playerNumber:
            return

        if event.type == pygame.KEYUP:
            self.move(event.key)
            

    # Updates positions of sprites to match the current game state
    def tick(self):
        if self.state == None:
            return

        self.aang.rect.x = 48*self.state.aangPosition[0]
        self.aang.rect.y = 48*self.state.aangPosition[1]
        
        self.katara.rect.x = 48*self.state.kataraPosition[0]
        self.katara.rect.y = 48*self.state.kataraPosition[1]

        if self.state.playerTurnNumber == self.gs.playerNumber:
            self.turnLabel.text = "Your Turn"
        else:
            self.turnLabel.text = "Their Turn"
        
