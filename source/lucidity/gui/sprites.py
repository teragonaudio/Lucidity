import pygame
from pygame.sprite import DirtySprite
from lucidity.core.arrangement import Item
from lucidity.core.timing import Position
from lucidity.gui.colors import ColorChooser
from lucidity.gui.layout import Padding, FontSizer, Positioning

class GridSprite(DirtySprite):
    def __init__(self, id, rect:pygame.Rect, speedInPxPerSec:float):
        DirtySprite.__init__(self)
        self.id = id
        self.rect = rect
        self.speedInPxPerSec = float(speedInPxPerSec)
        self.movePixels = 0

    def moveLeft(self, numPixels:"int"):
        self.rect.move_ip(0 - numPixels, 0)
        self.dirty = True

    def update(self, *args):
        elapsedTime = args[0]
        self.movePixels += self.speedInPxPerSec * elapsedTime
        if self.movePixels > 1.0:
            self.moveLeft(int(self.movePixels))
            self.movePixels = 0.0
        if self.rect.right < 0:
            self.onOffscreen()

    def onOffscreen(self):
        self.kill()

class Block(GridSprite):
    BORDER_SIZE = 2

    def __init__(self, id, position:tuple, width:int, height:int,
                 color:tuple, fontName:str, speedInPxPerSec:float):
        GridSprite.__init__(self, id, pygame.Rect(position[0], position[1], width, height), speedInPxPerSec)
        self.backgroundColor = color
        self.fontName = fontName
        self.fontColor = (0, 0, 0)
        if ColorChooser.isDarkColor(self.backgroundColor):
            self.fontColor = (255, 255, 255)
        self.image = self.createBlock(self.rect, color, fontName, id)

    def resize(self, newRect:pygame.Rect):
        self.rect = newRect
        self.image = self.createBlock(newRect, self.backgroundColor, self.fontName, self.id)
        self.dirty = True

    def createBlock(self, rect:pygame.Rect, color:tuple, fontName:str, item:Item):
        surface = pygame.Surface((rect.width, rect.height))
        colorRect = Positioning.innerRect(surface.get_rect(), Block.BORDER_SIZE)
        surface.fill(color, colorRect)

        fontRect = Positioning.innerRect(colorRect, Padding.LABEL)
        fontRect.left += Padding.BLOCK
        fontSize = FontSizer.bestFitSizeInPoints(fontName, rect.height / 4)
        font = pygame.font.Font(fontName, fontSize)
        fontSurface = font.render(item.label, True, self.fontColor)
        colorRect.left += Padding.LABEL
        colorRect.top += Padding.LABEL
        surface.blit(fontSurface, fontRect)

        return surface

class BarLine(GridSprite):
    def __init__(self, sequencePosition:Position, gridPosition:tuple,
                 height:int, width:int, color:tuple, speedInPxPerSec:float):
        GridSprite.__init__(self, sequencePosition,
                            pygame.Rect(gridPosition[0], gridPosition[1],
                                        width, height), speedInPxPerSec)
        self.backgroundColor = color
        self.image = self.createBar()

    def createBar(self):
        surface = pygame.Surface((self.rect.width, self.rect.height))
        surface.fill(self.backgroundColor)
        return surface

class CursorLine(BarLine):
    def __init__(self, sequencePosition:Position, gridPosition:tuple,
                 height:int, width:int, color:tuple, speedInPxPerSec:float):
        super().__init__(sequencePosition, gridPosition, height, width,
                         color, speedInPxPerSec)
        self.track = 0
        self.isOffscreen = False

    def onOffscreen(self):
        self.isOffscreen = True

    def moveToBeat(self, beat:int, positionX:int):
        self.id.beats = beat
        self.rect.left = positionX
        self.dirty = True

    def moveToTrack(self, track:int, positionY:int):
        self.track = track
        self.rect.top = positionY
        self.dirty = True

    def updateHeight(self, trackHeightInPx:"int"):
        self.rect.height = trackHeightInPx
        self.image = self.createBar()
        self.dirty = True

class TrackLine(DirtySprite):
    def __init__(self, trackNumber:int, width:int, color:tuple):
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
