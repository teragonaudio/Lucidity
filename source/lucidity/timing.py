import time

class TimeSignature:
    def __init__(self, beatUnit, beatsPerMeasure):
        self.beatUnit = beatUnit
        self.beatsPerMeasure = beatsPerMeasure

class MusicalClock:
    def __init__(self, tempo:"float"):
        self.tempo = tempo
        self._beatCount = 0
        self._currentTime = time.time()
        self._startTime = self._currentTime
        self._elapsedTime = 0
        # Note: For the moment, this is hardcoded to be 4/4, but it is possible
        # that this will be changed in the future to allow the user to set the
        # time signature of the arrangement.
        self.timeSignature = TimeSignature(4, 4)

    def getBeats(self):
        return self._beatCount

    def getBars(self):
        return self._beatCount / self.timeSignature.beatsPerMeasure

    def tick(self):
        self._currentTime = time.time()
        self._elapsedTime = self._currentTime - self._startTime
        self._beatCount = MusicTimeConverter.secondsToBeats(self.tempo, self._elapsedTime)

class MusicTimeConverter:
    @staticmethod
    def beatsToSeconds(tempo:"float", beats:"int"):
        return beats * 60.0 / tempo

    @staticmethod
    def secondsToBeats(tempo:"float", seconds:"float"):
        return tempo * seconds / 60.0