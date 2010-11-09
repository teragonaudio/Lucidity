import pygame
from pygame import midi
from lucidity.log import logger
from threading import Thread
from time import sleep
from multiprocessing.synchronize import Lock

class MidiEvent:
    def __init__(self, status, data1, data2, timestamp = 0):
        self.status = status
        self.data1 = data1
        self.data2 = data2
        self.timestamp = timestamp

    def __str__(self):
        return hex(self.status) + ", " + hex(self.data1) + ", " + hex(self.data2)

class MidiDevice:
    def __init__(self, id, name, type = None, isOpen = False):
        self._id = id
        self.name = name
        self.type = type
        self.isOpen = isOpen

    def __str__(self):
        result = "'" + self.name + "', type: " + self.type + ", status: "
        if self.isOpen:
            result += "Opened"
        else:
            result += "Not Open"
        return result

    def open(self): pass
    def close(self): pass
    def poll(self): pass

class MidiInput(MidiDevice):
    def __init__(self, id, name, opened):
        super().__init__(id, name, type = "Input", isOpen = opened)
        self._inputPort = None

    def open(self):
        self._inputPort = pygame.midi.Input(self._id)

    def poll(self):
        return self._inputPort.poll()

    def readEvents(self):
        return self._inputPort.read(1)

class MidiOutput(MidiDevice):
    def __init__(self, id, name, opened):
        super().__init__(id, name, type = "Output", isOpen = opened)

class MidiDeviceList:
    def __init__(self):
        self.devices = None
        self._openedInputs = {}
        logger.info("Initializing MIDI")
        pygame.midi.init()
        self.rescan()

    def rescan(self):
        self.devices = []
        numDevices = pygame.midi.get_count()
        logger.debug("Rescan started, found %d devices", (numDevices))
        for i in range(0, numDevices):
            (interface, name, input, output, opened) = pygame.midi.get_device_info(i)
            deviceName = name.decode("utf-8")

            if input:
                device = MidiInput(i, deviceName, opened)
            else:
                device = MidiOutput(i, deviceName, opened)

            logger.debug("Device %d: %s", i, device)
            self.devices.append(device)

    def openInput(self, name):
        device = None
        for d in self.devices:
            if d.name == name:
                device = d
                break

        if device is None:
            raise Exception("Device '" + name + "' not found")

        if device._id in self._openedInputs:
            raise Exception("Request to open device '%s', which is already open", name)

        if device.type == "Input":
            device.open()
            self._openedInputs[device._id] = device
        else:
            raise Exception("Device '%s' is not an input device", name)

    def openedInputs(self):
        return self._openedInputs.values()

class MidiEventLoop(Thread):
    def __init__(self, pollIntervalInMs = 25):
        Thread.__init__(self, name = "MidiEventLoop")
        self._lock = Lock()
        self._isRunning = False
        self._pollInterval = pollIntervalInMs / 1000
        self.devices = MidiDeviceList()

    def terminate(self):
        self._lock.acquire(True)
        self._isRunning = False
        for device in self.devices.openedInputs():
            device.close()
        pygame.midi.quit()
        self._lock.release()

    def run(self):
        logger.debug("MidiEventLoop started")
        self._isRunning = True
        while self._isRunning:
            self._lock.acquire(True)
            for device in self.devices.openedInputs():
                while device.poll():
                    self._parseEvent(device.readEvents())
            self._lock.release()
            sleep(self._pollInterval)

    def _parseEvent(self, eventList):
        eventData = eventList[0][0]
        midiEvent = MidiEvent(eventData[0], eventData[1], eventData[2], eventList[0][1])
        logger.debug("Incoming MIDI message: %s", midiEvent)
        pass
