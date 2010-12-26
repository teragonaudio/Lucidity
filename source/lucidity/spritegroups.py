import pygame
from pygame.sprite import LayeredDirty
from lucidity.arrangement import Sequence, Item
from lucidity.skinning import Skin
from lucidity.sprites import Block, BarLine, TrackLine, CursorLine
from lucidity.timing import MusicTimeConverter

class GridSpriteGroup(LayeredDirty):
    MIN_WIDTH_IN_BARS = 32   # 1 minute @ 120 BPM
    MAX_WIDTH_IN_BARS = 1024 # 30 minutes @ 120 BPM
    #DEF_WIDTH_IN_BARS = 120  # 4 minutes @ 120 BPM
    DEF_WIDTH_IN_BARS = MIN_WIDTH_IN_BARS

    def __init__(self, sequence:Sequence, offset:tuple, rect:pygame.Rect, skin:Skin):
        LayeredDirty.__init__(self)
        self.sequence = sequence
        self.offset = offset
        self.rect = rect
        self.skin = skin
        self.blocks = []
        self.trackLines = []
        self.barLines = []
        self.lastTime = sequence.getTime()
        self.widthInBars = self.DEF_WIDTH_IN_BARS
        self.activeTrackCount = Sequence.MIN_TRACKS

        self.add(BarLine(0, (0, 0), self.rect.height, 1, skin.guiColor("Bar Line"), self.getSpeed()))
        for i in range(0, Sequence.MAX_TRACKS):
            self.add(TrackLine(i, self.rect.width, skin.guiColor("Track Line")))

        self.cursor = CursorLine(0, (0, 0), self.getTrackHeightInPx(), 4,
                                 skin.guiColor("Cursor"), self.getSpeed())
        self.cursor.moveToBar(self.barLines[0])
        self.cursor.moveToTrack(self.trackLines[0])
        self.add(self.cursor)

        self._updateTrackLines()

    def add(self, *sprites, **kwargs):
        super().add(*sprites, **kwargs)
        for sprite in sprites:
            if isinstance(sprite, Block):
                self.blocks.append(sprite)
            elif isinstance(sprite, BarLine):
                self.barLines.append(sprite)
            elif isinstance(sprite, TrackLine):
                self.trackLines.append(sprite)

    def addItem(self, item:Item):
        firstBar = self.barLines[0]
        beatsPerBar = self.sequence.clock.timeSignature.beatsPerMeasure
        positionX = firstBar.rect.left + (((item.startPositionInBeats / beatsPerBar) -
                                           firstBar.id) * self.getBarWidthInPx())
        positionY = self.trackLines[item.track].rect.top
        width = ((item.endPositionInBeats - item.startPositionInBeats) / beatsPerBar) * self.getBarWidthInPx()
        self.add(Block(item, (positionX, positionY), width, self.getTrackHeightInPx(),
                       self.skin.nextPaletteColor(), self.skin.font("Block"), self.getSpeed()))

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
        self._updateBarLines()

        now = self.sequence.getTime()
        elapsedTime = float(now - self.lastTime)
        super().update(elapsedTime)
        self.lastTime = now

    def _updateBarLines(self):
        lastBarLine = self.barLines[len(self.barLines) - 1]
        while lastBarLine.rect.left < self.rect.right:
            nextRect = lastBarLine.rect.move(self.getBarWidthInPx(), 0)
            barLine = BarLine(lastBarLine.id + 1, (nextRect.left, nextRect.top), self.rect.height, 1,
                              self.skin.guiColor("Bar Line"), self.getSpeed())
            self.add(barLine)
            lastBarLine = barLine

    def _updateGridItemSpeeds(self):
        speed = self.getSpeed()
        for sprite in self.barLines:
            sprite.speedInPxPerSec = speed
        for sprite in self.blocks:
            sprite.speedInPxPerSec = speed

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
        self.cursor.updateHeight(trackHeightInPx)

    def _updateBlockHeights(self, trackHeightInPx:"int"):
        for block in self.blocks:
            newRect = block.rect
            newRect.top = self.trackLines[block.id.track].rect.top
            newRect.height = trackHeightInPx
            block.resize(newRect)

    def refreshAllItems(self):
        for sprite in self.sprites():
            if isinstance(sprite, Block):
                track = self.sequence.tracks[sprite.id.track]
                if not track.contains(sprite.id):
                    sprite.kill()

    def getSpeed(self):
        return self.rect.width / self.getWidthInSec()

    def getTrackHeightInPx(self):
        return self.rect.height / self.activeTrackCount

    def getBarWidthInPx(self):
        return self.rect.width / self.widthInBars

    def getWidthInSec(self):
        return MusicTimeConverter.beatsToSeconds(self.getTempo(), self.widthInBars * 4)

    def getTempo(self):
        return self.sequence.getTempo()

    def setTempo(self, tempo:float):
        self.sequence.setTempo(tempo)

    def moveLeft(self):
        self.collapseBars()

    def moveRight(self):
        self.expandBars()

    def moveUp(self):
        self.collapseTracks()

    def moveDown(self):
        self.expandTracks()

    def expandTracks(self):
        if self.activeTrackCount < Sequence.MAX_TRACKS:
            self.activeTrackCount += 1
            self._updateTrackLines()

    def collapseTracks(self):
        if self.activeTrackCount > Sequence.MIN_TRACKS:
            self.activeTrackCount -= 1
            self._updateTrackLines()

    def expandBars(self):
        if self.widthInBars < self.MAX_WIDTH_IN_BARS:
            self.widthInBars += 4
            self._updateGridItemSpeeds()

    def collapseBars(self):
        if self.widthInBars > self.MIN_WIDTH_IN_BARS:
            self.widthInBars -= 4
            self._updateGridItemSpeeds()

    def getNearestTrackForPosition(self, position:"tuple"):
        trackHeightInPx = self.getTrackHeightInPx()
        for trackLine in self.trackLines:
            if trackLine.visible:
                if position[1] > trackLine.rect.top and \
                    position[1] - trackLine.rect.top < trackHeightInPx:
                    return trackLine.id
        return -1

    def getNearestBarForPosition(self, position:"tuple"):
        barWidthInPx = self.getBarWidthInPx()
        for barLine in self.barLines:
            if barLine.visible:
                if position[0] > barLine.rect.left and \
                    position[0] - barLine.rect.left < barWidthInPx:
                    return barLine.id
        return -1
