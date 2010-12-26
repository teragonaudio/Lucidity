import pygame
from lucidity.arrangement import Sequence, Item
from lucidity.layout import Sizing
from lucidity.log import logger
from lucidity.containers import Container
from lucidity.skinning import Skin
from lucidity.spritegroups import GridSpriteGroup

class MainGrid(Container):
    def __init__(self, parentSurface:pygame.Surface, rect:pygame.Rect, skin:Skin, sequence:Sequence):
        Container.__init__(self, parentSurface, rect, skin)
        backgroundColor = skin.guiColor("Background")
        parentSurface.fill(backgroundColor, rect)
        self.sequence = sequence

        gridRect = pygame.Rect(0, rect.top + Sizing.gridPadding,
                               rect.width,
                               rect.height - (Sizing.gridPadding * 2))

        self.parentSurface = parentSurface.subsurface(gridRect)
        self.rect = self.parentSurface.get_rect()
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill(skin.guiColor("Grid"))
        self.parentSurface.blit(self.background, self.rect)

        self.gridSprites = GridSpriteGroup(sequence, (gridRect.left, gridRect.top),
                                           self.rect, skin)

    def draw(self):
        self.gridSprites.clear(self.parentSurface, self.background)
        self.gridSprites.update()
        updateRects = self.gridSprites.draw(self.parentSurface)
        pygame.display.update(updateRects)

    def onMouseDown(self, position): pass

    def onMouseUp(self, position):
        relativePosition = (position[0] - self.absRect.left, position[1] - self.absRect.top)
        trackNumber = self.gridSprites.getNearestTrackForPosition(relativePosition)
        barCount = self.gridSprites.getNearestBarForPosition(relativePosition)
        item = Item(1, trackNumber, "Block", barCount * 4, (barCount + 8) * 4, 0)
        self.sequence.tracks[trackNumber].addItem(item)
        self.gridSprites.addItem(item)

    def moveLeft(self):
        self.gridSprites.moveLeft()

    def moveRight(self):
        self.gridSprites.moveRight()

    def moveUp(self):
        self.gridSprites.moveUp()

    def moveDown(self):
        self.gridSprites.moveDown()

    def reset(self):
        self.sequence.clearAllTracks()
        self.gridSprites.refreshAllItems()
