import pygame
from lucidity.arrangement import Sequence
from lucidity.layout import Sizing
from lucidity.containers import Container
from lucidity.sprites import Block, TrackLine
from lucidity.timing import MusicTimeConverter

MIN_WIDTH_IN_BARS = 32   # 1 minute @ 120 BPM
MAX_WIDTH_IN_BARS = 1024 # 30 minutes @ 120 BPM
DEF_WIDTH_IN_BARS = 120  # 4 minutes @ 120 BPM

class GridSequence:
    def __init__(self, sequence:"Sequence"):
        self._sequence = sequence
        self.widthInBars = DEF_WIDTH_IN_BARS
        self.activeTrackCount = Sequence.MIN_TRACKS

    def expandTracks(self):
        if self.activeTrackCount < 16:
            self.activeTrackCount += 1

    def collapseTracks(self):
        if self.activeTrackCount > 4:
            self.activeTrackCount -= 1

    def getTempo(self):
        return self._sequence.getTempo()

    def setTempo(self, tempo:"float"):
        self._sequence.setTempo(tempo)

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def moveUp(self):
        pass

    def moveDown(self):
        pass

class GridSizer:
    def __init__(self, gridSequence:"GridSequence", rect:"pygame.Rect"):
        self.gridSequence = gridSequence
        self.rect = rect

    def getTrackHeightInPx(self):
        return self.rect.height / self.gridSequence.activeTrackCount

    def getBarWidthInPx(self):
        return self.rect.width / self.gridSequence.widthInBars

class GridTimer:
    def __init__(self, gridSequence:"GridSequence"):
        self.gridSequence = gridSequence

    def getWidthInSec(self):
        return MusicTimeConverter.beatsToSeconds(self.gridSequence.getTempo(), self.gridSequence.widthInBars)

class MainGrid(Container):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect", skin:"Skin", sequence:"Sequence"):
        Container.__init__(self, parentSurface, rect, skin)
        backgroundColor = skin.colorChooser.findColor("Black")
        self.parentSurface.fill(backgroundColor, self.rect)

        self.gridSequence = GridSequence(sequence)
        self.gridSizer = GridSizer(self.gridSequence, rect)
        self.gridTimer = GridTimer(self.gridSequence)

        self.gridItems = pygame.sprite.RenderUpdates()
        self.gridBarLines = pygame.sprite.RenderUpdates()
        self.gridTrackLines = pygame.sprite.RenderUpdates()
        for i in range(0, Sequence.MAX_TRACKS):
            self.gridTrackLines.add(TrackLine(i, self.rect.width, skin))

        gridRect = pygame.Rect(0, self.rect.top + Sizing.gridPadding,
                               self.rect.width,
                               self.rect.height - (Sizing.gridPadding * 2))
        self.rect = gridRect

        self.background = pygame.Surface((gridRect.width, gridRect.height))
        self.background = self.background.convert()
        self.background.fill(skin.colorChooser.findColor("Banana Mania"))
        self.parentSurface.blit(self.background, self.rect)
        self.repositionTrackLines()

        pygame.display.flip()

    def repositionTrackLines(self):
        pixelsPerTrack = self.rect.height / self.gridSequence.activeTrackCount
        for sprite in self.gridTrackLines.sprites():
            sprite.visible = int(sprite.index < self.gridSequence.activeTrackCount)
            if sprite.visible:
                sprite.setPosition(self.rect.top + pixelsPerTrack * sprite.index)

        updateRects = self.gridTrackLines.draw(self.parentSurface)
        pygame.display.update(updateRects)

    def draw(self):
        self.gridItems.clear(self.parentSurface, self.background)
        self.gridItems.update()
        updateRects = self.gridItems.draw(self.parentSurface)
        pygame.display.update(updateRects)
        for sprite in self.gridItems.sprites():
            if not self.rect.colliderect(sprite.rect):
                sprite.kill()

        self.gridBarLines.clear(self.parentSurface, self.background)
        self.gridItems.update()
        updateRects = self.gridBarLines.draw(self.parentSurface)
        pygame.display.update(updateRects)
        for sprite in self.gridBarLines.sprites():
            if sprite.rect.left <= 0:
                sprite.kill()

    def getSpeed(self):
        return self.rect.width / self.gridTimer.getWidthInSec()

    def onMouseDown(self, position):
        pass

    def onMouseUp(self, position):
        block = Block(pygame.image.load("icon.png"), position, self.getSpeed())
        self.gridItems.add(block)

    def moveLeft(self):
        self.gridSequence.moveLeft()

    def moveRight(self):
        self.gridSequence.moveRight()

    def redrawTrackLines(self, activeTrackCountBefore):
        if self.gridSequence.activeTrackCount != activeTrackCountBefore:
            self.repositionTrackLines()

    def moveUp(self):
        activeTrackCountBefore = self.gridSequence.activeTrackCount
        self.gridSequence.moveUp()
        self.redrawTrackLines(activeTrackCountBefore)

    def moveDown(self):
        activeTrackCountBefore = self.gridSequence.activeTrackCount
        self.gridSequence.moveDown()
        self.redrawTrackLines(activeTrackCountBefore)
