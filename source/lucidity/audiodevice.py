import pygame
import pygame.mixer
from lucidity.log import logger
from threading import Thread
from multiprocessing.synchronize import Lock
from time import sleep, clock
import wave

class AudioOutputLoop(Thread):
    def __init__(self, sampleRate, bufferSize):
        Thread.__init__(self, name = "AudioOutputLoop")
        self._lock = Lock()
        self._isRunning = False
        self._bufferSize = bufferSize
        self._sampleRate = sampleRate
        self._maxTimePerBlockInSec = bufferSize / sampleRate

        pygame.mixer.init(frequency = sampleRate, buffer = bufferSize)
        self._channel = pygame.mixer.find_channel()

        self.testWave = wave.open("./tests/resources/test.wav", "r")
        self.totalFrames = self.testWave.getnframes()
        self.allsamples = self.testWave.readframes(self.totalFrames)

        self._byteArray = bytearray(self._bufferSize * 2)

        self.numFrames = 0
        logger.info("Mixer initialized")

    def terminate(self):
        pygame.mixer.quit()

    def run(self):
        logger.debug("AudioOutputLoop started")
        self._isRunning = True
        while self._isRunning:
            startTime = clock()
            self._lock.acquire(True)

            # do cool stuff here
            if self.numFrames + self._bufferSize > self.totalFrames:
                self._isRunning = False
            else:
                startFrame = self.numFrames
                endFrame = startFrame + self._bufferSize * 2
                bytesOut = bytes(self.allsamples[startFrame:endFrame])
                sound = pygame.mixer.Sound(self.allsamples[startFrame:endFrame])
                self._channel.play(sound)
                self.numFrames += self._bufferSize * 2

            stopTime = clock()
            timeInBlockInSec = (stopTime - startTime)
            sleepTime = self._maxTimePerBlockInSec - timeInBlockInSec
            if sleepTime < 0:
                logger.warn("Audio dropout!")
            else:
                logger.info("CPU: %f", 100 * timeInBlockInSec / self._maxTimePerBlockInSec)
                sleep(sleepTime)
            self._lock.release()
