import random
from threading import Thread
from time import sleep
from lucidity.system.paths import PathFinder

class StatusDelegate:
    def onStatusUpdate(self, status:"str"): pass

class StatusProvider:
    def getStatusString(self): pass

class StatusLoop(Thread):
    def __init__(self, intervalInSec=1.0):
        Thread.__init__(self, name="StatusProvider")
        self.intervalInSec = intervalInSec
        self.statusProvider = None
        self.delegate = None
        self._isRunning = False

    def run(self):
        self._isRunning = True
        lastStatus = None
        while self._isRunning:
            # Sleep first, then update.  This is done because we don't want to
            # write over the initial text right after starting up
            sleep(self.intervalInSec)
            if self.statusProvider is not None and self.delegate is not None:
                status = self.statusProvider.getStatusString()
                if lastStatus != status:
                    self.delegate.onStatusUpdate(status)
                    lastStatus = status

    def quit(self):
        self._isRunning = False

class ObtuseStatusProvider(StatusProvider):
    def __init__(self):
        self.lines = self._readLinesFromText()

    def getStatusString(self):
        randIndex = random.randint(0, len(self.lines) - 1)
        return self.lines[randIndex]

    def _readLinesFromText(self):
        result = []

        linesFile = open(PathFinder.findResource("text", "Obtuse.txt"), 'r')
        for line in linesFile:
            result.append(line.strip())
        linesFile.close()

        return result