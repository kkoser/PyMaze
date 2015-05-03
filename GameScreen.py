import sys
import os
import math
import pygame
from pygame.locals import *
from KSprite import KSprite
from KLabel import KLabel
from MazeView import MazeView

class GameScreen:
    def setup(self):
        #Add in the logos and buttons here
        self.mazeView = MazeView(self)
        self.aang = KSprite("images/aang.gif")
        self.aang.rect.move_ip(200,200)
        self.katara = KSprite("images/katara.jpg")
        self.katara.rect.move_ip(400,200)

        self.state = None

    def __init__(self, gs):
        self.gs = gs
        self.setup()

    def draw(self, screen):
        screen.fill(self.gs.black)
        if self.gs.playerNumber == self.state.aangPlayerNumber:
            self.mazeView.drawAroundPoint(screen, self.state.aangPosition)
        else:
            self.mazeView.drawAroundPoint(screen, self.state.kataraPosition)

        self.aang.draw(screen)
        self.katara.draw(screen)
        

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

    def tick(self):
        if self.state == None:
            return

        self.aang.rect.x = 48*self.state.aangPosition[0]
        self.aang.rect.y = 48*self.state.aangPosition[1]
        
        self.katara.rect.x = 48*self.state.kataraPosition[0]
        self.katara.rect.y = 48*self.state.kataraPosition[1]
        
