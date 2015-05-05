
import sys
import os
import math
import pygame
from pygame.locals import *
from KSprite import KSprite
from KLabel import KLabel

## This class represents a view of the game maze. It can read in a maze description from a file, and can draw what is within sight of a certain position
class MazeView:
    # Loads a maze description from a file and creates the appropriate tiles
    def setupFromFile(self, desc):
        self.mazeViews = []
        self.mazeDesc = []
        y = 0 #Used to place newly created views
        f = open(desc)
        for line in f:
            arr = []
            x = 0 #Used to place newly created views
            line = line.rstrip()
            components = line.split(",")
            for loc in components:
                if loc == "0":
                    #load an empty space
                    view = KSprite("images/floor.png")
                else:
                    #load a wall space
                    view = KSprite("images/wall.png")
                view.rect.move_ip(48*x,48*y)
                x = x + 1
                arr.append(view)
            self.mazeViews.append(arr)
            self.mazeDesc.append(components)
            y = y + 1
        f.close()   

    def __init__(self, parent):
        self.mazeViews = None
        self.mazeDesc = None
        self.parent = parent
        self.setupFromFile("zachMaze.txt")

    # This method draws only the tiles of the maze that are within sight of a given position
    # The position is given in grid coordinates (0-9), not screen coordinates
    def drawAroundPoint(self, screen, (mx, my)):
        maxDist = 48*3
        mx = mx * 48
        my = my * 48
        for arr in self.mazeViews:
            for view in arr:
                dist = math.sqrt((view.rect.x-mx)**2 + (view.rect.y-my)**2)
                if dist <= maxDist:
                    view.draw(screen)
