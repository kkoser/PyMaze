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
        self.aang.rect.move_ip(200,200)
        self.katara = KSprite("images/katara.jpg")
        self.katara.rect.move_ip(400,200)

        self.font = pygame.font.Font(None,30)
        self.statusLabel = KLabel("Choose a character", self.font, 500,400)
        self.aangLabel = KLabel("Aang", self.font, 200,250)
        self.kataraLabel = KLabel("Katara", self.font, 400,250)

        self.state = None

    def __init__(self, gs):
        self.gs = gs
        self.setup()

    def draw(self, screen):
        screen.fill(self.gs.black)
        self.aang.draw(screen)
        self.katara.draw(screen)
        self.statusLabel.draw(screen)
        self.aangLabel.draw(screen)
        self.kataraLabel.draw(screen)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if self.aang.rect.collidepoint(mx,my):
                #select aang
                print "Selected aang"
                if self.state.aangPlayer == 0 and self.state.kataraPlayer != self.state.playerNum:
                    self.state.aangPlayer = self.state.playerNumer
            if self.katara.rect.collidepoint(mx,my):
                #select katara
                print "Selected katara"
                if self.state.kataraPlayer == 0 and self.state.aangPlayer != self.state.playerNum:
                    self.state.kataraPlayer = self.state.playerNum

    def tick(self):
        if self.state == None:
            return

        # The state object will be updated by the twisted client as appropriate
        pid = self.state.playerNumber
        if pid == self.state.aangPlayer:
            self.aangLabel.text = "You"
        elif self.state.aangPlayer == 0:
            self.aangLabel.text = "You"
        else:
            self.aangLabel.text = "Them"

        if pid == self.state.kataraPlayer:
            self.kataraLabel.text = "You"
        elif self.state.kataraPlayer == 0:
            self.kataraLabel.text = "You"
        else:
            self.kataraLabel.text = "Them"

        if self.state.aangPlayer > 0 and self.state.kataraPlayer > 0:
            self.statusLabel.text = "Ready to Play!"
        elif self.state.aangPlayer == self.state.playerNum or self.state.kataraPlayer == pid:
            self.statusLabel.text = "Waiting for partner"
        else:
            self.statusLabel.text = "Choose a character"
            

        
