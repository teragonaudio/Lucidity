import pygame
import time
from pygame.sprite import DirtySprite
from lucidity.log import logger

class GridSprite(DirtySprite):
    def __init__(self, rect:"pygame.Rect", speedInPxPerSec:"float"):
        DirtySprite.__init__(self)
        self.rect = rect
        self.lastTime = time.time()
        self.speedInPxPerSec = speedInPxPerSec
        self.absolutePosition = float(rect.left)

    def moveLeft(self, numPixels:"int"):
        self.rect.move_ip(0 - numPixels, 0)
        self.dirty = 1

    def update(self, *args):
        now = time.time()
        elapsedTime = now - self.lastTime
        newPosition = self.absolutePosition - (self.speedInPxPerSec * elapsedTime)
        differenceInPx = self.rect.left - newPosition
        if differenceInPx > 1.0:
            self.moveLeft(int(differenceInPx))
        self.absolutePosition = newPosition
        self.lastTime = now

class Block(GridSprite):
    def __init__(self, image:"Surface", position:"tuple", speedInPxPerSec:"float"):
        GridSprite.__init__(self, image.get_rect().move(position[0], position[1]), speedInPxPerSec)
        self.image = image.convert_alpha()

class VerticalLine(GridSprite):
    def __init__(self, valueInBeats:"int", height:"int", skin:"Skin", speedInPxPerSec:"float"):
        GridSprite.__init__(self, pygame.Rect(-1, 0, 1, height), speedInPxPerSec)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.backgroundColor = skin.colorChooser.findColor("Black")

class TrackLine(DirtySprite):
    def __init__(self, index:"int", width:"int", skin:"Skin"):
        DirtySprite.__init__(self)
        self.index = index
        self.visible = False
        self.backgroundColor = skin.colorChooser.findColor("Black")
        self.rect = pygame.Rect(0, -1, width, 1)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.backgroundColor, self.rect)

    def setPosition(self, top:"int"):
        self.rect.top = top

    def update(self, *args):
        self.dirty = 1
