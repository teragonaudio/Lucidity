import pygame
from pygame.sprite import LayeredDirty
from lucidity.arrangement import Sequence, Item
from lucidity.timing import MusicTimeConverter
from lucidity.gui.skinning import Skin
from lucidity.gui.sprites import Block, BarLine, TrackLine, CursorLine

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

        self.cursor = CursorLine(0, (0, 0), self.getTrackHeightInPx() + 1, 4,
                                 skin.guiColor("Cursor"), self.getSpeed())
        self.cursor.moveToBar(self.barLines[0])
        self.cursor.moveToTrack(self.trackLines[0])
        self.add(self.cursor, layer="cursor")
        self.move_to_front(self.cursor)

        self._updateTrackLines()

    def add(self, *sprites, **kwargs):
        for sprite in sprites:
            layerName = "grid"
            if isinstance(sprite, Block):
                self.blocks.append(sprite)
                layerName = "items"
            elif isinstance(sprite, BarLine):
                self.barLines.append(sprite)
                layerName = "barLines"
            elif isinstance(sprite, TrackLine):
                self.trackLines.append(sprite)
                layerName = "trackLines"
            super().add(sprite, layer=layerName)


    def addItem(self, item:Item, barLine:BarLine):
        beatsPerBar = self.sequence.clock.timeSignature.beatsPerMeasure
        positionX = barLine.rect.left
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
        now = self.sequence.getTime()
        elapsedTime = float(now - self.lastTime)
        super().update(elapsedTime)
        self.lastTime = now

        self._updateBarLines()
        self._updateCursor()

    def _updateCursor(self):
        if self.cursor.isOffscreen:
            self.cursor.moveToBar(self.barLines[1])
            self.cursor.isOffscreen = False

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
        self.cursor.updateHeight(trackHeightInPx + 1)

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

    def _findBarFromId(self, id):
        for barLine in self.barLines:
            if barLine.id == id:
                return barLine
        return None

    def moveLeft(self):
        nextBarId = self.cursor.bar.id - 1
        nextBar = self._findBarFromId(nextBarId)
        if nextBar is not None:
            self.cursor.moveToBar(nextBar)
        #self.collapseBars()

    def moveRight(self):
        nextBarId = self.cursor.bar.id + 1
        nextBar = self._findBarFromId(nextBarId)
        if nextBar is not None:
            self.cursor.moveToBar(nextBar)
        #self.expandBars()

    def moveUp(self):
        nextTrack = self.cursor.track.id - 1
        if nextTrack >= 0:
            if nextTrack < self.activeTrackCount:
                currentBeat = self.sequence.getCurrentBeat()
                if not self.sequence.tracks[self.activeTrackCount - 1].hasItemsAfterBeat(currentBeat):
                    self.collapseTracks()
            self.cursor.moveToTrack(self.trackLines[nextTrack])

    def moveDown(self):
        nextTrack = self.cursor.track.id + 1
        if nextTrack < Sequence.MAX_TRACKS:
            if nextTrack >= self.activeTrackCount:
                self.expandTracks()
            self.cursor.moveToTrack(self.trackLines[nextTrack])

    def expandTracks(self):
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
                    return barLine
        return None