import pygame
from pygame.sprite import DirtySprite
from lucidity.arrangement import Item
from lucidity.layout import Sizing

class GridSprite(DirtySprite):
    def __init__(self, id, rect:"pygame.Rect", speedInPxPerSec:"float"):
        DirtySprite.__init__(self)
        self.id = id
        self.rect = rect
        self.speedInPxPerSec = float(speedInPxPerSec)
        self.movePixels = 0

    def moveLeft(self, numPixels:"int"):
        self.rect.move_ip(0 - numPixels, 0)
        self.dirty = 1

    def update(self, *args):
        elapsedTime = args[0]
        self.movePixels += self.speedInPxPerSec * elapsedTime
        if self.movePixels > 1.0:
            self.moveLeft(int(self.movePixels))
            self.movePixels = 0.0

        if self.rect.left + self.rect.width < 0:
            self.kill()

class Block(GridSprite):
    def __init__(self, id, position:"tuple", width:"int", height:"int",
                 color:tuple, fontName:str, speedInPxPerSec:"float"):
        GridSprite.__init__(self, id, pygame.Rect(position[0], position[1], width, height), speedInPxPerSec)
        self.backgroundColor = color
        self.fontName = fontName
        self.image = self.createBlock(self.rect, color, fontName, id)

    def resize(self, newRect:pygame.Rect):
        self.rect = newRect
        self.image = self.createBlock(newRect, self.backgroundColor, self.fontName, self.id)
        self.dirty = True

    def createBlock(self, rect:pygame.Rect, color:tuple, fontName:str, item:Item):
        surface = pygame.Surface((rect.width, rect.height))
        colorRect = surface.get_rect()
        colorRect.top += 2
        colorRect.left += 2
        colorRect.width -= 4
        colorRect.height -= 4
        surface.fill(color, colorRect)

        font = pygame.font.Font(fontName, int(rect.height / 4))
        fontSurface = font.render(item.label, True, (0,0,0))
        colorRect.left += Sizing.fontPadding
        surface.blit(fontSurface, colorRect)

        return surface

class BarLine(GridSprite):
    def __init__(self, barCount:"int", position:"tuple", height:"int", color:tuple, speedInPxPerSec:"float"):
        GridSprite.__init__(self, barCount, pygame.Rect(position[0], position[1], 1, height), speedInPxPerSec)
        self.backgroundColor = color
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.backgroundColor)

class TrackLine(DirtySprite):
    def __init__(self, trackNumber:"int", width:"int", color:tuple):
        DirtySprite.__init__(self)
        self.id = trackNumber
        self.visible = False
        self.backgroundColor = color
        self.rect = pygame.Rect(0, -1, width, 1)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.backgroundColor)

    def setTop(self, top:"int"):
        self.rect.top = top

    def update(self, *args):
        pass
