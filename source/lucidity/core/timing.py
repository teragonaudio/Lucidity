import time

class TimeSignature:
    def __init__(self, beatUnit, beatsPerMeasure):
        self.beatUnit = beatUnit
        self.beatsPerMeasure = beatsPerMeasure

    def getBarsForBeats(self, beats:int):
        return int(beats / self.beatUnit)

    def getBeatsForBars(self, bars:int):
        return bars * self.beatUnit

DEFAULT_TIME_SIGNATURE = TimeSignature(4, 4)

class Position:
    def __init__(self, beats:int=0, sixteenths:int=0):
        self.beats = beats
        self.sixteenths = sixteenths

    def getBars(self, timeSignature:TimeSignature=DEFAULT_TIME_SIGNATURE):
        return int(self.beats / timeSignature.beatsPerMeasure)

    def getTime(self, tempo:"float"):
        return MusicTimeConverter.beatsToSeconds(tempo, self.beats)

class MusicalClock:
    def __init__(self, tempo:"float", timeSignature:TimeSignature=DEFAULT_TIME_SIGNATURE):
        self.tempo = tempo
        self.position = Position()
        self.currentTime = time.time()
        self.startTime = self.currentTime
        self.elapsedTime = 0
        # Note: For the moment, this is hardcoded to be 4/4, but it is possible
        # that this will be changed in the future to allow the user to set the
        # time signature of the arrangement.
        self.timeSignature = timeSignature

    def getBeats(self):
        return self.position.beats

    def getBars(self):
        return self.position.getBars(self.timeSignature)

    def tick(self):
        self.currentTime = time.time()
        self.elapsedTime = self.currentTime - self.startTime
        self.position.beats = MusicTimeConverter.secondsToBeats(self.tempo, self.elapsedTime)

class MusicTimeConverter:
    @staticmethod
    def beatsToSeconds(tempo:float, beats:int):
        return float(beats) * 60.0 / tempo

    @staticmethod
    def secondsToBeats(tempo:float, seconds:float):
        return tempo * seconds / 60.0