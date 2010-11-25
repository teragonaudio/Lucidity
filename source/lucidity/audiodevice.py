import pygame
import pygame.mixer
from lucidity.log import logger
from threading import Thread
from multiprocessing.synchronize import Lock
from time import sleep, clock
import wave

class AudioDevice:
    def __init__(self, name, numInputs, numOutputs):
        self.name = name
        self.numInputs = numInputs
        self.numOutputs = numOutputs

    def __str__(self):
        return "Device name: '" + self.name + "', " + \
               "Inputs: " + str(self.numInputs) + ", " + \
               "Outputs: " + str(self.numOutputs)

class AudioDeviceList:
    def __init__(self):
        self.devices = {}
        self.rescan()

    def rescan(self):
        self.devices = {}
        logger.info("Audio device rescan started")
        devices = pygame.mixer.get_devices()
        logger.debug("Found %d devices", len(devices))
        for device in devices:
            (name, numInputs, numOutputs) = device
            scannedDevice = AudioDevice(name, numInputs, numOutputs)
            self.devices[name] = scannedDevice
            logger.debug("%s", scannedDevice)

    def get(self, deviceName):
        if deviceName in self.devices.keys():
            return self.devices[deviceName]
        else:
            raise Exception("Device '" + deviceName + "' not found")

class AudioOutputLoop(Thread):
    def __init__(self, audioDevice, sampleRate = 44100.0, bufferSize = 512):
        Thread.__init__(self, name = "AudioOutputLoop")
        self._lock = Lock()
        self._isRunning = False

        self._audioDevice = audioDevice
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
