import pygame
import time
from pygame.sprite import DirtySprite

class GridSprite(DirtySprite):
    def __init__(self, rect:"pygame.Rect", speedInPxPerSec:"float"):
        DirtySprite.__init__(self)
        self.rect = rect
        self.speedInPxPerSec = float(speedInPxPerSec)
        self.movePixels = 0

    def moveLeft(self, numPixels:"int"):
        self.rect.move_ip(0 - numPixels, 0)
        self.dirty = 1

    def update(self, *args):
        elapsedTime = float(args[0])
        self.movePixels += self.speedInPxPerSec * elapsedTime
        if self.movePixels > 1.0:
            self.moveLeft(int(self.movePixels))
            self.movePixels = 0.0

        if self.rect.left + self.rect.width < 0:
            self.kill()

class Block(GridSprite):
    def __init__(self, position:"tuple", width:"int", height:"int", color:tuple, speedInPxPerSec:"float"):
        GridSprite.__init__(self, pygame.Rect(position[0], position[1], width, height), speedInPxPerSec)
        self.backgroundColor = color
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.backgroundColor)

class BarLine(GridSprite):
    def __init__(self, valueInBeats:"int", position:"tuple", height:"int", color:tuple, speedInPxPerSec:"float"):
        GridSprite.__init__(self, pygame.Rect(position[0], position[1], 1, height), speedInPxPerSec)
        self.valueInBeats = valueInBeats
        self.backgroundColor = color
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.backgroundColor)

class TrackLine(DirtySprite):
    def __init__(self, index:"int", width:"int", color:tuple):
        DirtySprite.__init__(self)
        self.index = index
        self.visible = False
        self.backgroundColor = color
        self.rect = pygame.Rect(0, -1, width, 1)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.backgroundColor)

    def setPosition(self, top:"int"):
        self.rect.top = top

    def update(self, *args):
        self.dirty = 1
