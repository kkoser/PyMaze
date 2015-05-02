import sys
import os
from math import *
import pygame
from pygame.locals import *
from KSprite import KSprite
from KLabel import KLabel

class MainMenuScreen:
    def setup(self):
        #Add in the logos and buttons here
        self.aang = KSprite("images/aang.gif")
        self.aang.rect.move(200,200)
        self.katara = KSprite("images/katara.jpg")
        self.katara.rect.move(400,200)

        self.font = pygame.font.Font(None,30)
        self.statusLabel = KLabel("Choose a character", self.font, 500,400)

    def __init__(self, gs):
        self.gs = gs
        self.setup()

    def draw(self, screen):
        screen.fill(self.gs.black)
        self.aang.draw(screen)
        self.katara.draw(screen)
        self.statusLabel.draw(screen)

    def handleEvent(self, event):
        print event
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if self.aang.rect.collidepoint(mx,my):
                #select aang
                print "Selected aang"
                self.statusLabel.text = "Waiting for partner"
            if self.katara.rect.collidepoint(mx,my):
                #select katara
                print "Selected katara"
                self.statusLabel.text = "Waiting for partner"

    def tick(self):
        print "tick"

            

        
