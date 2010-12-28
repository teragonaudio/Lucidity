from lucidity.timing import MusicalClock

class Item:
    def __init__(self, id, track:"int", label:"str", startPositionInBeats:"int",
                 endPositionInBeats:"int", stackPosition:"int"):
        self.id = id
        self.track = track
        self.label = label
        self.startPositionInBeats = startPositionInBeats
        self.endPositionInBeats = endPositionInBeats
        self.stackPosition = stackPosition

class Track:
    def __init__(self, id:int):
        self.items = []
        self.id = id

    def addItem(self, item:"Item"):
        self.items.append(item)

    def hasItemsAfterBeat(self, beats:"int"):
        for item in self.items:
            if item.endPositionInBeats > beats:
                return True
        return False

    def contains(self, item:"Item"):
        return item in self.items

    def clear(self):
        self.items = []

class Sequence:
    DEFAULT_TEMPO = 120.0
    MAX_TRACKS = 16
    MIN_TRACKS = 4

    def __init__(self, tempo:float=DEFAULT_TEMPO):
        self.clock = MusicalClock(tempo)
        self.tracks = []
        for i in range(0, self.MAX_TRACKS):
            self.tracks.append(Track(i))

    def getTempo(self):
        return self.clock.tempo

    def setTempo(self, tempo:"float"):
        self.clock.tempo = tempo

    def getTime(self):
        return self.clock.currentTime

    def getCurrentBar(self):
        return self.clock.getBars()

    def getCurrentBeat(self):
        return self.clock.getBeats()

    def tick(self):
        self.clock.tick()

    def clearAllTracks(self):
        for track in self.tracks:
            track.clear()