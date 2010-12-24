import pygame
from lucidity.arrangement import Sequence
from lucidity.layout import Sizing
from lucidity.containers import Container
from lucidity.sprites import Block, TrackLine, BarLine
from lucidity.timing import MusicTimeConverter

class GridSequence:
    MIN_WIDTH_IN_BARS = 32   # 1 minute @ 120 BPM
    MAX_WIDTH_IN_BARS = 1024 # 30 minutes @ 120 BPM
    DEF_WIDTH_IN_BARS = 120  # 4 minutes @ 120 BPM

    def __init__(self, sequence:"Sequence"):
        self._sequence = sequence
        self.widthInBars = self.DEF_WIDTH_IN_BARS
        self.activeTrackCount = Sequence.MIN_TRACKS

    def expandTracks(self):
        if self.activeTrackCount < Sequence.MAX_TRACKS:
            self.activeTrackCount += 1

    def collapseTracks(self):
        if self.activeTrackCount > Sequence.MIN_TRACKS:
            self.activeTrackCount -= 1

    def expandBars(self):
        if self.widthInBars < self.MAX_WIDTH_IN_BARS:
            self.widthInBars += 4

    def collapseBars(self):
        if self.widthInBars > self.MIN_WIDTH_IN_BARS:
            self.widthInBars -= 4

    def getTempo(self):
        return self._sequence.getTempo()

    def setTempo(self, tempo:"float"):
        self._sequence.setTempo(tempo)

    def moveLeft(self):
        self.collapseBars()

    def moveRight(self):
        self.expandBars()

    def moveUp(self):
        self.collapseTracks()

    def moveDown(self):
        self.expandTracks()

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
        parentSurface.fill(backgroundColor, rect)

        gridRect = pygame.Rect(0, rect.top + Sizing.gridPadding,
                               rect.width,
                               rect.height - (Sizing.gridPadding * 2))
        self.originalTop = gridRect.top

        self.parentSurface = parentSurface.subsurface(gridRect)
        self.rect = self.parentSurface.get_rect()
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill(skin.colorChooser.findColor("Banana Mania"))
        self.parentSurface.blit(self.background, self.rect)

        self.gridSequence = GridSequence(sequence)
        self.gridSizer = GridSizer(self.gridSequence, self.rect)
        self.gridTimer = GridTimer(self.gridSequence)

        self.gridItems = pygame.sprite.LayeredDirty()
        self.gridBarLines = pygame.sprite.LayeredDirty()
        barWidth = self.gridSizer.getBarWidthInPx()
        for i in range(0, self.gridSequence.widthInBars):
            self.gridBarLines.add(BarLine(i * 4, (i * barWidth, 0), self.rect.height, skin, self.getSpeed()))

        self.gridTrackLines = pygame.sprite.LayeredDirty()
        for i in range(0, Sequence.MAX_TRACKS):
            self.gridTrackLines.add(TrackLine(i, self.rect.width, skin))
        self.repositionTrackLines()

    def getPixelHeightPerTrack(self):
        return self.rect.height / self.gridSequence.activeTrackCount

    def repositionTrackLines(self):
        self.gridTrackLines.clear(self.parentSurface, self.background)
        pixelsPerTrack = self.getPixelHeightPerTrack()
        for sprite in self.gridTrackLines.sprites():
            sprite.visible = int(sprite.index < self.gridSequence.activeTrackCount)
            if sprite.visible:
                sprite.setPosition(self.rect.top + pixelsPerTrack * sprite.index)
            else:
                sprite.setPosition(-1)

        # TODO: All other sprites must be repositioned accordingly, uck

    def draw(self):
        self._drawGridItems()
        self._drawTrackLines()
        self._drawBarLines()

    def _drawBarLines(self):
        self.gridBarLines.clear(self.parentSurface, self.background)
        self.gridBarLines.update()
        updateRects = self.gridBarLines.draw(self.parentSurface)
        for rect in updateRects:
            rect.top += self.originalTop
        pygame.display.update(updateRects)
        numBarLines = len(self.gridBarLines.sprites())
        if numBarLines < self.gridSequence.widthInBars:
            lastSprite = self.gridBarLines.sprites()[numBarLines - 1]
            self.gridBarLines.add(BarLine(lastSprite.valueInBeats + 4, (lastSprite.rect.left + self.gridSizer.getBarWidthInPx(), 0),
                                          self.rect.height, self.skin, self.getSpeed()))

    def _drawGridItems(self):
        self.gridItems.clear(self.parentSurface, self.background)
        self.gridItems.update()
        updateRects = self.gridItems.draw(self.parentSurface)
        for rect in updateRects:
            rect.top += self.originalTop
        pygame.display.update(updateRects)

    def _drawTrackLines(self):
        self.gridTrackLines.clear(self.parentSurface, self.background)
        self.gridTrackLines.update()
        updateRects = self.gridTrackLines.draw(self.parentSurface)
        for rect in updateRects:
            rect.top += self.originalTop
        pygame.display.update(updateRects)

    def getSpeed(self):
        return self.rect.width / self.gridTimer.getWidthInSec()

    def onMouseDown(self, position):
        pass

    def onMouseUp(self, position):
        pixelsPerTrack = self.getPixelHeightPerTrack()
        nearestTrackLine = None
        positionY = position[1] - self.originalTop

        for trackLine in self.gridTrackLines.sprites():
            if trackLine.visible:
                if positionY > trackLine.rect.top and \
                   positionY - trackLine.rect.top < pixelsPerTrack:
                    nearestTrackLine = trackLine
                    break

        x = position[0] # TODO: Get nearest bar/beat line
        y = nearestTrackLine.rect.top + nearestTrackLine.rect.height
        block = Block(pygame.image.load("icon.png"), (x, y), self.getSpeed())
        self.gridItems.add(block)

    def recalculateAnimationSpeeds(self, gridBarWidthBefore):
        if self.gridSequence.widthInBars != gridBarWidthBefore:
            newSpeed = self.getSpeed()
            for sprite in self.gridItems.sprites():
                sprite.speedInPxPerSec = newSpeed
            for sprite in self.gridBarLines.sprites():
                sprite.speedInPxPerSec = newSpeed

    def moveLeft(self):
        gridBarWidthBefore = self.gridSequence.widthInBars
        self.gridSequence.moveLeft()
        self.recalculateAnimationSpeeds(gridBarWidthBefore)

    def moveRight(self):
        gridBarWidthBefore = self.gridSequence.widthInBars
        self.gridSequence.moveRight()
        self.recalculateAnimationSpeeds(gridBarWidthBefore)

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
