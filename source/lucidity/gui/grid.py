import pygame
from lucidity.core.arrangement import Sequence
from lucidity.gui.layout import Padding, Positioning
from lucidity.gui.containers import Container
from lucidity.gui.popups import SearchPopup
from lucidity.gui.skinning import Skin
from lucidity.gui.spritegroups import GridSpriteGroup

class MainGrid(Container):
    def __init__(self, parentSurface:pygame.Surface, rect:pygame.Rect, skin:Skin, sequence:Sequence):
        Container.__init__(self, parentSurface, rect, skin)
        backgroundColor = skin.guiColor("Background")
        parentSurface.fill(backgroundColor, rect)
        self.sequence = sequence

        gridRect = pygame.Rect(0, rect.top + Padding.GRID,
                               rect.width,
                               rect.height - (Padding.GRID * 2))

        self.parentSurface = parentSurface.subsurface(gridRect)
        self.rect = self.parentSurface.get_rect()
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill(skin.guiColor("Grid"))
        self.parentSurface.blit(self.background, self.rect)

        self.gridSprites = GridSpriteGroup(sequence, (gridRect.left, gridRect.top),
                                           self.rect, skin)
        self.activePopup = None

    def draw(self):
        self.gridSprites.clear(self.parentSurface, self.background)
        self.gridSprites.update()
        updateRects = self.gridSprites.draw(self.parentSurface)
        pygame.display.update(updateRects)

    def onMouseDown(self, position): pass

    def onMouseUp(self, position):
        relativePosition = (position[0] - self.absRect.left, position[1] - self.absRect.top)
        nearestTrack = self.gridSprites.getNearestTrackLineAt(relativePosition)
        nearestBar = self.gridSprites.getNearestBarLineAt(relativePosition)
        if nearestBar and nearestTrack:
            self.gridSprites.cursor.moveToBeat(nearestBar.id.beats, nearestBar.rect.right)
            self.gridSprites.cursor.moveToTrack(nearestTrack.id, nearestTrack.rect.bottom)

    def moveLeft(self):
        self.gridSprites.moveCursorLeft(4)

    def moveRight(self):
        self.gridSprites.moveCursorRight(4)

    def moveUp(self):
        self.gridSprites.moveUp()

    def moveDown(self):
        self.gridSprites.moveDown()

    def reset(self):
        self.sequence.clearAllTracks()
        self.gridSprites.reset()

    def getCursorPosition(self):
        return self.gridSprites.cursor.position

    def getCursorTrack(self):
        return self.gridSprites.cursor.track

    def showSearchPopup(self):
        rect = Positioning.innerRect(self.gridSprites.rect, Padding.SEARCH_POPUP)
        searchPopup = SearchPopup(self.parentSurface, rect, self.skin)
        self.gridSprites.add(searchPopup)
        searchPopup.show()
        self.activePopup = searchPopup

    def hidePopup(self):
        if self.activePopup is not None:
            self.activePopup.hide()
            self.activePopup = None