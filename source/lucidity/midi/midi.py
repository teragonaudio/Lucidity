import pygame
import pygame.midi
from multiprocessing.synchronize import Lock
from threading import Thread
from time import sleep
from lucidity.db.database import Sqlite3Database, Database
from lucidity.system.log import logger
from lucidity.system.paths import PathFinder

class MidiEvent:
    def __init__(self, status, data1, data2, timestamp = 0):
        self.status = status
        self.data1 = data1
        self.data2 = data2
        self.timestamp = timestamp

    def getMappingKey(self):
        return (self.status << 8) + self.data1

    def __str__(self):
        return str(self.getMappingKey()) + ", " + hex(self.data2)

class MidiDevice:
    def __init__(self, id, name, type = None, isOpen = False):
        self._id = id
        self.name = name
        self.type = type
        self.isOpen = isOpen
        self.port = None

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

    def open(self):
        logger.info("Opening MIDI input '" + self.name + "'")
        self.port = pygame.midi.Input(self._id)

    def close(self):
        logger.info("Closing MIDI input '" + self.name + "'")
        if self.port is not None:
            self.port.close()

    def poll(self):
        return self.port.poll()

    def readEvents(self):
        return self.port.read(1)

class MidiOutput(MidiDevice):
    def __init__(self, id, name, opened):
        super().__init__(id, name, type = "Output", isOpen = opened)

    def open(self):
        logger.info("Opening MIDI output '" + self.name + "'")
        self.port = pygame.midi.Output(self._id)

    def close(self):
        logger.info("Closing MIDI output '" + self.name + "'")
        if self.port is not None:
            self.port.close()

    def write(self, midiEvent:"MidiEvent"):
        self.port.write_short(midiEvent.status, midiEvent.data1, midiEvent.data2)

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

    def get(self, name:str, type:str):
        if type == "Input":
            deviceList = self._openedInputs
        elif type == "Output":
            deviceList = self._openedOutputs
        else:
            raise Exception("Invalid device type '" + type + "'")

        for device in deviceList.values():
            if device.name == name:
                return device
        return None

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

class MidiMapping:
    def __init__(self, key:int, value, type:str):
        self.key = key
        self.value = value
        self.type = type

    def isButton(self):
        return self.type == "button"

class MidiMappingTable:
    def __init__(self, absolutePath):
        self.absolutePath = absolutePath
        schemaLocation = PathFinder.findSchemaFile("midimappings.sql")
        self._database = Sqlite3Database(absolutePath, schemaLocation)
        self.mappingTable = self.loadMappings(self._database)

    def loadMappings(self, database:Database):
        mappings = {}
        cursor = database.query("SELECT `key`, `value`, `type` FROM `midimappings`")
        for (key, value, type) in cursor:
            mappings[key] = MidiMapping(key, value, type)
        return mappings

    def process(self, midiEvent:"MidiEvent", delegate):
        mappingKey = midiEvent.getMappingKey()
        try:
            if mappingKey in self.mappingTable:
                mapping = self.mappingTable[mappingKey]
                if mapping.isButton() and not midiEvent.data2:
                    return
                handlerFunction = getattr(delegate, "on" + mapping.value)
                handlerFunction()
            else:
                raise UnhandledMidiError(midiEvent)
        except AttributeError:
            logger.error("Delegate does not handle MIDI command")
        except UnhandledMidiError as error:
            logger.debug("Unhandled midi event: " + str(error.midiEvent))

class UnhandledMidiError(Exception):
    def __init__(self, midiEvent):
        self.midiEvent = midiEvent

class MidiEventLoop(Thread):
    def __init__(self, delegate, pollIntervalInMs = 25):
        Thread.__init__(self, name = "MidiEventLoop")
        self._lock = Lock()
        self._isRunning = False
        self.delegate = delegate
        self._pollInterval = pollIntervalInMs / 1000
        self.devices = None
        self.midiMappings = MidiMappingTable(PathFinder.findUserFile('midimappings.sql'))

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
        self.midiMappings.process(midiEvent, self.delegate)
