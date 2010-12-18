import pygame
import pygame.midi
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
        logger.info("Opening MIDI input '%s'", self.name)
        self._inputPort = pygame.midi.Input(self._id)

    def close(self):
        logger.info("Closing MIDI input '%s'", self.name)
        if self._inputPort is not None:
            self._inputPort.close()

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
        self._openedOutputs = {}
        logger.info("Initializing MIDI")
        pygame.midi.init()
        self.rescan()

    def rescan(self):
        self.devices = []
        numDevices = pygame.midi.get_count()
        logger.debug("MIDI device rescan started, found %d devices", numDevices)
        for i in range(0, numDevices):
            (interface, name, input, output, opened) = pygame.midi.get_device_info(i)
            deviceName = name.decode("utf-8")

            if input:
                device = MidiInput(i, deviceName, opened)
            else:
                device = MidiOutput(i, deviceName, opened)

            logger.debug("Device %d: %s", i, device)
            self.devices.append(device)

    def openAll(self):
        for device in self.devices:
            self.open(device)

    def open(self, device):
        if device is None:
            raise Exception("Device cannot be None")

        if device._id in self._openedInputs:
            raise Exception("Request to open device '%s', which is already open", device.name)

        if device.type == "Input":
            device.open()
            self._openedInputs[device._id] = device
        elif device.type == "Output":
            device.open()
            self._openedOutputs[device._id] = device
        else:
            raise Exception("Device '%s' has unknown type '%s'", device.name, device.type)

    def openedInputs(self):
        return self._openedInputs.values()

    def openedOutputs(self):
        return self._openedOutputs.values()

    def closeAll(self):
        for device in self.devices:
            self.close(device)

    def close(self, device):
        device.close()
        if device.type == "Input":
            self._openedInputs.pop(device._id)
        elif device.type == "Output":
            self._openedOutputs.pop(device._id)

class MidiMappings:
    def __init__(self, delegate):
        self.delegate = delegate
        self.mappingTable = {}
        self.reloadMappings()

    def reloadMappings(self):
        pass

    def process(self, midiEvent:"MidiEvent"):
        if not midiEvent.data2:
            return

        mappingKey = (midiEvent.status << 8) + midiEvent.data1
        if mappingKey in self.mappingTable:
            if self.mappingTable[mappingKey]:
                self.mappingTable[mappingKey]()

class MidiEventLoop(Thread):
    def __init__(self, delegate, pollIntervalInMs = 25):
        Thread.__init__(self, name = "MidiEventLoop")
        self._lock = Lock()
        self._isRunning = False
        self._pollInterval = pollIntervalInMs / 1000
        self.devices = None
        self.midiMappings = MidiMappings(delegate)

    def quit(self):
        self._lock.acquire(True)
        if self.devices is not None:
            self.devices.closeAll()
        self._isRunning = False
        self._lock.release()
        logger.info("Closed all MIDI devices")

    def run(self):
        # Initialize is done here so as not to block the main thread
        self.devices = MidiDeviceList()
        self.devices.openAll()

        logger.debug("MidiEventLoop started")
        self._isRunning = True
        while self._isRunning:
            self._lock.acquire(True)
            for device in self.devices.openedInputs():
                while device.poll():
                    self._parseEvent(device.readEvents())
            self._lock.release()
            sleep(self._pollInterval)

        pygame.midi.quit()

    def _parseEvent(self, eventList):
        eventData = eventList[0][0]
        midiEvent = MidiEvent(eventData[0], eventData[1], eventData[2], eventList[0][1])
        logger.debug("Incoming MIDI message: %s", midiEvent)
        self.midiMappings.process(midiEvent)
