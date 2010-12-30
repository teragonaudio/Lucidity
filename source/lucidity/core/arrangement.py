from lucidity.core.timing import *

class Item:
    def __init__(self, id, track:int, label:str,
                 startPosition:Position, lengthInSec:int, tempo:float):
        self.id = id
        self.track = track
        self.label = label
        self.startPosition = startPosition
        self.lengthInSec = lengthInSec
        self.endPosition = Position()
        self.setTempo(tempo)

    def getLengthInBeats(self):
        return self.endPosition.beats - self.startPosition.beats

    def setTempo(self, tempo:float):
        self.endPosition.beats = self.startPosition.beats + \
                                 MusicTimeConverter.secondsToBeats(tempo, self.lengthInSec)

class Track:
    def __init__(self, id:int):
        self.items = []
        self.id = id

    def addItem(self, item:Item):
        self.items.append(item)

    def hasItemsAfterBeat(self, beat:int):
        for item in self.items:
            if item.endPosition.beats > beat:
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

    def __init__(self, tempo:float=DEFAULT_TEMPO, timeSignature:TimeSignature=DEFAULT_TIME_SIGNATURE):
        self.timeSignature = timeSignature
        self.clock = MusicalClock(tempo, self.timeSignature)
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

    def setTempo(self, tempo:float):
        self.clock.tempo = tempo
        for track in self.tracks:
            for item in track.items:
                item.setTempo(tempo)

    def getTime(self):
        return self.clock.currentTime

    def getCurrentBar(self):
        return self.clock.getBars()

    def getCurrentBeat(self):
        return self.clock.getBeats()

    def hasItemsAfterBeat(self, beat:int, trackNumber:int=None):
        if trackNumber is not None:
            return self.tracks[trackNumber].hasItemsAfterBeat(beat)
        else:
            for i in range(0, len(self.tracks)):
                if self.hasItemsAfterBeat(trackNumber):
                    return True
            return False

    def tick(self):
        self.clock.tick()

    def clearAllTracks(self):
        for track in self.tracks:
            track.clear()