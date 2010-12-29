from lucidity.core.timing import MusicalClock

class Item:
    def __init__(self, id, track:"int", label:"str",
                 startPositionInBeats:"int", lengthInBeats:"int",
                 stackPosition:"int"):
        self.id = id
        self.track = track
        self.label = label
        self.startPositionInBeats = startPositionInBeats
        self.endPositionInBeats = self.startPositionInBeats + lengthInBeats
        self.lengthInBeats = lengthInBeats
        self.stackPosition = stackPosition

class Track:
    def __init__(self, id:int):
        self.items = []
        self.id = id

    def addItem(self, item:Item):
        self.items.append(item)

    def hasItemsAfterPosition(self, positionInBeats:int):
        for item in self.items:
            if item.endPositionInBeats > positionInBeats:
                return True
        return False

    def clear(self):
        self.items = []

class SequenceObserver:
    def onItemAdded(self, item:Item): pass

class Sequence:
    DEFAULT_TEMPO = 120.0
    MAX_TRACKS = 16
    MIN_TRACKS = 4

    def __init__(self, tempo:float=DEFAULT_TEMPO):
        self.clock = MusicalClock(tempo)
        self.observers = []
        self.tracks = []
        for i in range(0, self.MAX_TRACKS):
            self.tracks.append(Track(i))

    def addItem(self, item:Item):
        self.tracks[item.track].addItem(item)
        for observer in self.observers:
            observer.onItemAdded(item)

    def addObserver(self, observer:SequenceObserver):
        self.observers.append(observer)

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