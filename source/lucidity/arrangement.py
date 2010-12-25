from lucidity.timing import MusicalClock

class Item:
    def __init__(self, label:"str", offset:"int", stackPosition:"int"):
        self.label = label
        self.offset = offset
        self.stackPosition = stackPosition

class Track:
    def __init__(self):
        self.items = []

    def addItem(self, item:"Item"):
        self.items.append(item)

class Sequence:
    DEFAULT_TEMPO = 120.0
    MAX_TRACKS = 16
    MIN_TRACKS = 4

    def __init__(self, tempo:"float" = DEFAULT_TEMPO):
        self.clock = MusicalClock(tempo)
        self.tracks = []
        for i in range(0, self.MAX_TRACKS):
            self.tracks.append(Track())

    def getTempo(self):
        return self.clock.tempo

    def setTempo(self, tempo:"float"):
        self.clock.tempo = tempo

    def getTime(self):
        return self.clock.currentTime

    def getCurrentBar(self):
        return self.clock.getBars()

    def tick(self):
        self.clock.tick()