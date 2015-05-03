import sys
import os
from math import *
import pygame
from pygame.locals import *
from KSprite import KSprite
from KLabel import KLabel

class MazeView:
    def setupFromFile(self, desc):
        self.mazeViews = []
        y = 0
         f = open(ratings_file)
        for line in f:
            arr = []
            x = 0
            line = line.rstrip()
            components = line.split(",")
            for loc in components:
                if loc == 0:
                    #load an empty space
                    view = KSprite("images/emptySpace.gif")
                else:
                    view = KSPrite("images/wallSpace.png")
                view.rect.move_ip(48*x,48*y)
                arr.append(view)
            self.mazeViews.append(arr)
        f.close()   

    def __init__(self, parent):
        self.mazeViews = None
        self.parent = parent
        self.setupFromFile("maze1.txt")

    def drawAroundPoint(self, screen, (mx, my)):
        maxDist = 48*3
        mx = mx * 48
        my = my * 48
        for arr in self.mazeViews:
            for view in arr:
                dist = math.sqrt((view.rect.x-mx)**2 + (view.rect.y-my)**2))
                if dist <= maxDist:
                    view.draw(screen)