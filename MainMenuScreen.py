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
        self.statusLabel = KLabel("Choose a character", self.font, 300,400)
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
                if self.state.aangPlayerNumber == 0 and self.state.kataraPlayerNumber != self.gs.playerNumber:
                    self.state.aangPlayerNumber = self.gs.playerNumber
                    self.gs.connection.sendMenuState(self.state)
            if self.katara.rect.collidepoint(mx,my):
                #select katara
                print "Selected katara"
                if self.state.kataraPlayerNumber == 0 and self.state.aangPlayerNumber != self.gs.playerNumber:
                    self.state.kataraPlayerNumber = self.gs.playerNumber
                    self.gs.connection.sendMenuState(self.state)
            if self.statusLabel.rect.collidepoint(mx,my) and self.statusLabel.text == "Enter the Cave":
                print "clicked label"
                if self.state.aangPlayerNumber == self.gs.playerNumber:
                    self.state.aangPlayerReady = True
                else:
                    self.state.kataraPlayerReady = True

                self.gs.connection.sendMenuState(self.state)

    def tick(self):
        if self.state == None:
            return

        print "Tick"

        # The state object will be updated by the twisted client as appropriate
        pid = self.gs.playerNumber
        if pid == self.state.aangPlayerNumber:
            self.aangLabel.text = "You"
        elif self.state.aangPlayerNumber == 0:
            self.aangLabel.text = "Aang"
        else:
            self.aangLabel.text = "Lover"

        if pid == self.state.kataraPlayerNumber:
            self.kataraLabel.text = "You"
        elif self.state.kataraPlayerNumber == 0:
            self.kataraLabel.text = "Katara"
        else:
            self.kataraLabel.text = "Lover"

        if self.state.aangPlayerNumber > 0 and self.state.kataraPlayerNumber > 0:
            self.statusLabel.text = "Enter the Cave"
        elif self.state.aangPlayerNumber == pid or self.state.kataraPlayerNumber == pid:
            self.statusLabel.text = "Waiting for partner"
        else:
            self.statusLabel.text = "Choose a character"
            

        
