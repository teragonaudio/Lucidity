import pygame
from pygame.sprite import LayeredDirty
from lucidity.core.arrangement import Sequence, SequenceObserver, Item
from lucidity.core.timing import MusicTimeConverter, Position
from lucidity.gui.popups import Popup
from lucidity.gui.skinning import Skin
from lucidity.gui.sprites import Block, BarLine, TrackLine, CursorLine
from lucidity.system.log import logger

class GridSpriteGroup(LayeredDirty, SequenceObserver):
    MIN_WIDTH_IN_BARS = 32   # 1 minute @ 120 BPM
    MAX_WIDTH_IN_BARS = 1024 # 30 minutes @ 120 BPM
    #DEF_WIDTH_IN_BARS = 120  # 4 minutes @ 120 BPM
    DEF_WIDTH_IN_BARS = MIN_WIDTH_IN_BARS

    def __init__(self, sequence:Sequence, offset:tuple, rect:pygame.Rect, skin:Skin):
        LayeredDirty.__init__(self)
        self.sequence = sequence
        self.sequence.addObserver(self)
        self.offset = offset
        self.rect = rect
        self.skin = skin
        self.blocks = []
        self.trackLines = []
        self.barLines = []
        self.lastTime = sequence.getTime()
        self.widthInBeats = sequence.timeSignature.getBeatsForBars(self.DEF_WIDTH_IN_BARS)
        self.activeTrackCount = Sequence.MIN_TRACKS

        self._initializeGridSprites()

    def _initializeGridSprites(self):
        # We already know the maximum number of track lines, so go ahead and add them all now
        for i in range(0, Sequence.MAX_TRACKS):
            self.add(TrackLine(i, self.rect.width, self.skin.guiColor("Track Line")))

        # Add a few empty sprites for these groups
        # This is necessary so that the layers are properly sorted for this sprite
        # group, and also so that grid can be efficiently created by there being at
        # least one item to compare the current time with.
        self.add(BarLine(Position(0), (0, 0), self.rect.height, 1, self.skin.guiColor("Bar Line"), self.getSpeed()))

        # Finally, add the cursor object, which should always be on the very top
        self.cursor = CursorLine(Position(0), (0, 1), self.getTrackHeightInPx() + 1, 4,
                                 self.skin.guiColor("Cursor"), self.getSpeed())
        self.add(self.cursor, layer=3)

        self._updateBarLines()
        self._updateTrackLines()

    def add(self, *sprites, **kwargs):
        for sprite in sprites:
            layer = 0
            if isinstance(sprite, Block):
                self.blocks.append(sprite)
                layer = 1
            elif isinstance(sprite, CursorLine):
                layer = 2
            elif isinstance(sprite, BarLine):
                self.barLines.append(sprite)
                layer = 0
            elif isinstance(sprite, TrackLine):
                self.trackLines.append(sprite)
                layer = 0
            elif isinstance(sprite, Popup):
                layer = 3
            super().add(sprite, layer=layer)

    def onItemAdded(self, item:Item):
        self.addItem(item)

    def addItem(self, item:Item):
        positionX = self.getOffsetFromFirstBarLine(item.startPosition.beats)
        positionY = self.trackLines[item.track].rect.top
        width = item.getLengthInBeats() * self.getBeatWidthInPx()

        self.add(Block(item, (positionX, positionY),
                       width, self.getTrackHeightInPx(),
                       self.skin.nextPaletteColor(), self.skin.font("Block"),
                       self.getSpeed()))

        # TODO: This really shouldn't be necessary...
        self.change_layer(self.cursor, 2)

    def remove_internal(self, sprite):
        super().remove_internal(sprite)
        if isinstance(sprite, Block):
            self.blocks.remove(sprite)
        elif isinstance(sprite, BarLine):
            self.barLines.remove(sprite)
        elif isinstance(sprite, TrackLine):
            self.trackLines.remove(sprite)

    def draw(self, surface, bgd=None):
        updateRects = super().draw(surface, bgd)
        # TODO: It's probably more efficient to pass the offset into draw()
        for rect in updateRects:
            rect.left += self.offset[0]
            rect.top += self.offset[1]
        return updateRects

    def update(self, *args):
        now = self.sequence.getTime()
        elapsedTime = float(now - self.lastTime)
        super().update(elapsedTime)
        self.lastTime = now

        self._updateBarLines()
        self._updateCursor()

    def _updateCursor(self):
        if self.cursor.isOffscreen:
            nextBar = self.barLines[0]
            self.cursor.moveToBeat(nextBar.id.beats, nextBar.rect.right)
            self.cursor.isOffscreen = False

    def _updateBarLines(self):
        numBarLines = len(self.barLines)
        lastBarLine = self.barLines[numBarLines - 1]
        while lastBarLine.rect.left < self.rect.right:
            nextRect = lastBarLine.rect.move(self.getBarWidthInPx(), 0)
            barLine = BarLine(Position(lastBarLine.id.beats + 4), (nextRect.left, nextRect.top), self.rect.height, 1,
                              self.skin.guiColor("Bar Line"), self.getSpeed())
            self.add(barLine)
            lastBarLine = barLine

    def _updateBarLineWidths(self):
        barWidth = self.getBarWidthInPx()
        startingBarX = self.barLines[0].rect.left
        for i in range(1, len(self.barLines)):
            barLine = self.barLines[i]
            barLine.rect.left = startingBarX + (barWidth * i)
            barLine.dirty = True

    def _updateGridItemSpeeds(self):
        speed = self.getSpeed()
        for sprite in self.barLines:
            sprite.speedInPxPerSec = speed
        for sprite in self.blocks:
            sprite.speedInPxPerSec = speed
        self.cursor.speedInPxPerSec = speed

    def _updateTrackLines(self):
        trackHeightInPx = self.getTrackHeightInPx()
        for trackLine in self.trackLines:
            trackLine.visible = trackLine.id < self.activeTrackCount
            if trackLine.visible:
                trackLine.setTop(self.rect.top + trackHeightInPx * trackLine.id)
            else:
                trackLine.setTop(-1)
            trackLine.dirty = 1
        self._updateBlockHeights(trackHeightInPx + 1)
        # TODO: 1 is used here for the track line height, but this should not be hardcoded
        self.cursor.updateHeight(trackHeightInPx - 1)

    def _updateBlockHeights(self, trackHeightInPx:int):
        for block in self.blocks:
            newRect = block.rect
            newRect.top = self.trackLines[block.id.track].rect.top
            newRect.height = trackHeightInPx
            block.resize(newRect)

    def reset(self):
        for sprite in self.blocks:
            sprite.kill()

    def getSpeed(self):
        return self.rect.width / self.getWidthInSec()

    def getTrackHeightInPx(self):
        return self.rect.height / self.activeTrackCount

    def getBeatWidthInPx(self):
        return self.rect.width / self.widthInBeats

    def getBarWidthInPx(self):
        return self.rect.width / self.getWidthInBars()

    def getWidthInBars(self):
        return self.sequence.timeSignature.getBarsForBeats(self.widthInBeats)

    def getWidthInSec(self):
        return MusicTimeConverter.beatsToSeconds(self.getTempo(), self.widthInBeats)

    def getTempo(self):
        return self.sequence.getTempo()

    def setTempo(self, tempo:float):
        self.sequence.setTempo(tempo)

    def findSpriteFromId(self, id, gridSpriteList):
        for gridSprite in gridSpriteList:
            if gridSprite.id == id:
                return gridSprite
        return None

    def moveCursorLeft(self, beats:int):
        nextBeat = self.cursor.id.beats - beats
        if nextBeat >= self.barLines[0].id.beats:
            self.cursor.moveToBeat(nextBeat, self.getOffsetFromFirstBarLine(nextBeat))

    def moveCursorRight(self, beats:int):
        nextBeat = self.cursor.id.beats + beats
        if nextBeat < self.sequence.timeSignature.getBeatsForBars(self.MAX_WIDTH_IN_BARS):
            if nextBeat - self.barLines[0].id.beats >= self.widthInBeats:
                self.expandBars(beats)
            self.cursor.moveToBeat(nextBeat, self.getOffsetFromFirstBarLine(nextBeat))

    def getOffsetFromFirstBarLine(self, beats:int):
        return self.barLines[0].rect.left + \
               ((beats - self.barLines[0].id.beats) * self.getBeatWidthInPx())

    def moveUp(self):
        nextTrack = self.cursor.track - 1
        if nextTrack >= 0:
            if nextTrack < self.activeTrackCount:
                currentBeat = self.sequence.getCurrentBeat()
                if not self.sequence.hasItemsAfterBeat(currentBeat, self.activeTrackCount - 1):
                    self.collapseTracks()
            self.cursor.moveToTrack(nextTrack, self.trackLines[nextTrack].rect.bottom)

    def moveDown(self):
        nextTrack = self.cursor.track + 1
        if nextTrack < Sequence.MAX_TRACKS:
            if nextTrack >= self.activeTrackCount:
                self.expandTracks()
            self.cursor.moveToTrack(nextTrack, self.trackLines[nextTrack].rect.bottom)

    def expandTracks(self):
        self.activeTrackCount += 1
        self._updateTrackLines()

    def collapseTracks(self):
        if self.activeTrackCount > Sequence.MIN_TRACKS:
            self.activeTrackCount -= 1
            self._updateTrackLines()

    def expandBars(self, widthInBeats:int):
        self.widthInBeats += widthInBeats
        self._updateBarLineWidths()
        self._updateBarLines()
        self._updateBlockSizes()
        self._updateGridItemSpeeds()

    def _updateBlockSizes(self):
        beatWidth = self.getBeatWidthInPx()
        for block in self.blocks:
            block.rect.left = self.getOffsetFromFirstBarLine(block.id.startPosition.beats)
            newRect = pygame.Rect(block.rect.left, block.rect.top,
                                  block.id.getLengthInBeats() * beatWidth, block.rect.height)
            block.resize(newRect)

    def collapseBars(self):
        if self.getWidthInBars() > self.MIN_WIDTH_IN_BARS:
            self.widthInBeats -= self.sequence.timeSignature.beatsPerMeasure
            self._updateGridItemSpeeds()

    def getNearestTrackLineAt(self, position:tuple):
        trackHeightInPx = self.getTrackHeightInPx()
        for trackLine in self.trackLines:
            if trackLine.visible:
                if position[1] > trackLine.rect.top and \
                    position[1] - trackLine.rect.top < trackHeightInPx:
                    return trackLine
        return None

    def getNearestBarLineAt(self, position:tuple):
        barWidthInPx = self.getBarWidthInPx()
        for barLine in self.barLines:
            if barLine.visible:
                if position[0] > barLine.rect.left and \
                    position[0] - barLine.rect.left < barWidthInPx:
                    return barLine
        return None
