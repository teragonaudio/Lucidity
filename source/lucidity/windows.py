import os
import pygame
import time
import lucidity
from lucidity.arrangement import Sequence
from lucidity.log import logger
from lucidity.keyboard import KeyHandler
from lucidity.grid import MainGrid
from lucidity.layout import PanelSizer
from lucidity.midi import MidiEventLoop
from lucidity.paths import PathFinder
from lucidity.performance import SystemUsage
from lucidity.settings import Settings
from lucidity.status import StatusLoop, ObtuseStatusProvider
from lucidity.toolbars import TopToolbar, BottomToolbar
from lucidity.skinning import Skin

class MainWindow():
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption("Lucidity")
        pygame.display.set_icon(pygame.image.load(os.path.join(".", "icon.png")))
        self.mainDelegate = MainDelegate(self)
        self.surface = None
        self.sequence = Sequence()
        self.settings = Settings(PathFinder.findUserFile('settings.db'))
        self._shouldQuit = False
        self._resolution = (1440, 900)
        self._containers = []
        self._skin = Skin(self.settings.getString("gui.skin"), self.settings.getInt("gui.colorInterval"))
        self._maxFps = self.settings.getFloat("gui.maxFps")
        self._setStatusTextCallback = None
        self._midiEventLoop = MidiEventLoop(self.mainDelegate)
        self._framesProcessed = 0
        self._systemUsage = SystemUsage(self)
        self._statusLoop = StatusLoop()

    def _initializePanels(self, resolution, skin:"Skin"):
        panelSizer = PanelSizer()
        mainGrid = MainGrid(self.surface,
                            panelSizer.getMainGridRect(resolution[0], resolution[1]),
                            skin, self.sequence)
        self._containers.append(mainGrid)
        self.mainDelegate.mainGrid = mainGrid

        toolbarBackgroundColor = self._skin.guiColor("Toolbar")
        topToolbar = TopToolbar(self.surface,
                                panelSizer.getTopToolbarRect(resolution[0]),
                                skin, toolbarBackgroundColor, self.mainDelegate,
                                self._systemUsage)
        self._containers.append(topToolbar)
        self._setStatusTextCallback = topToolbar.onStatusUpdate

        bottomToolbar = BottomToolbar(self.surface,
                                      panelSizer.getBottomToolbarRect(resolution[0], resolution[1]),
                                      skin, toolbarBackgroundColor, self.mainDelegate)
        self._containers.append(bottomToolbar)
        self._systemUsage.delegate = bottomToolbar
        self._statusLoop.delegate = topToolbar

    def run(self):
        """
        Open up the window for the application.  This must, sadly, be done in the main
        thread, or else the window will not properly respond to events.
        """
        windowFlags = self.getWindowFlags(self.settings)
        self.surface = pygame.display.set_mode(self._resolution, windowFlags)
        self._printVideoInfo(pygame.display.Info())
        logger.info("Initialized display with driver: " + pygame.display.get_driver())

        self.surface.fill(self._skin.guiColor("Background"))
        self._initializePanels(self._resolution, self._skin)
        self.setStatusText("Starting Up...")
        pygame.display.flip()

        frameRenderTimeInSec = 1 / self._maxFps

        midiStarted = False
        if self.settings.getInt("midi.enable"):
            self._midiEventLoop.start()
            midiStarted = True

        self._systemUsage.start()
        self._statusLoop.statusProvider = self.getStatusProvider(self.settings)
        self._statusLoop.start()
        self.setStatusText("Ready")

        while not self._shouldQuit:
            startTime = time.time()
            for event in pygame.event.get():
                self._processEvent(event)

            self.sequence.tick()
            for container in self._containers:
                container.draw()

            sleepTime = frameRenderTimeInSec - (time.time() - startTime)
            if sleepTime > 0:
                pygame.time.delay(int(sleepTime * 1000))
            self._framesProcessed += 1

        self._statusLoop.quit()
        self._statusLoop.join()
        self._systemUsage.quit()
        self._systemUsage.join()

        if midiStarted:
            self._midiEventLoop.quit()
            self._midiEventLoop.join()

        pygame.display.quit()
        pygame.quit()

    def quit(self):
        logger.info("Lucidity is quitting. Bye-bye!")
        self.setStatusText("Shutting down...")
        self._shouldQuit = True

    def minimize(self):
        logger.debug("Minimizing")
        pygame.display.iconify()

    def setStatusText(self, text):
        self._setStatusTextCallback(text)

    def _processEvent(self, event):
        eventType = pygame.event.event_name(event.type)
        try:
            processFunction = getattr(self.mainDelegate, "process" + eventType)
            processFunction(event.dict)
        except AttributeError as exception:
            logger.info("Error handling event '" + eventType + "': " + str(exception))
        except pygame.error as exception:
            logger.error("Error from pygame: " + str(exception))

    def processMouseButtonDown(self, eventDict):
        # logger.debug("Down at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for container in self._containers:
            if container.absRect.collidepoint(clickPosition[0], clickPosition[1]):
                container.onMouseDown(clickPosition)

    def processMouseButtonUp(self, eventDict):
        # logger.debug("Up at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for container in self._containers:
            if container.absRect.collidepoint(clickPosition[0], clickPosition[1]):
                container.onMouseUp(clickPosition)

    def getFramesPerSec(self):
        totalTime = self.sequence.getTime() - self.sequence.clock.startTime
        if totalTime > 0:
            return self._framesProcessed / totalTime
        else:
            return 0.0

    def getStatusProvider(self, settings):
        providerName = settings.getString("gui.statusProvider")
        if providerName == "usage":
            return self._systemUsage
        elif providerName == "obtuse":
            return ObtuseStatusProvider()
        elif providerName == "debug":
            return lucidity.log.statusHandler
        else:
            return None

    def getWindowFlags(self, settings):
        windowFlags = 0

        for setting in ["fullscreen", "doublebuf", "hwsurface", "opengl"]:
            fullSettingName = "gui" + "." + setting
            if settings.getInt(fullSettingName) > 0:
                pygameWindowFlagAttr = getattr(pygame, setting.upper())
                windowFlags |= pygameWindowFlagAttr

        return windowFlags

    def _printVideoInfo(self, videoInfo):
        resolutionWidth = str(videoInfo.current_w)
        resolutionHeight = str(videoInfo.current_h)
        logger.debug("Current resolution: " + resolutionWidth + "x" + resolutionHeight)
        videoInfoAttributes = {'hw': 'Hardware acceleration',
                               'wm': 'Windowed display',
                               'bitsize': 'Display depth',
        }

        for key in videoInfoAttributes.keys():
            logger.debug(videoInfoAttributes[key] + ": " + str(getattr(videoInfo, key)))

# Avoid warnings about unused locals, which is necessary for the event handlers to work
# properly via reflection
#noinspection PyUnusedLocal
class MainDelegate:
    def __init__(self, mainWindow:"MainWindow"):
        self.mainWindow = mainWindow
        self.mainGrid = None
        self.keyHandler = KeyHandler()

    def processCue(self):
        pass

    def processMoveLeft(self):
        self.mainGrid.moveLeft()

    def processMoveRight(self):
        self.mainGrid.moveRight()

    def processMoveUp(self):
        self.mainGrid.moveUp()

    def processMoveDown(self):
        self.mainGrid.moveDown()

    def processActiveEvent(self, eventDict):
        gain = eventDict['gain']
        state = eventDict['state']
        logger.info("Application activated, gain: " + str(gain) + ", state: " + str(state))

    def processKeyDown(self, eventDict):
        pass

    def processKeyUp(self, eventDict):
        self.keyHandler.processKey(self, eventDict['key'], eventDict['mod'])
        pass

    def processMouseButtonDown(self, eventDict):
        self.mainWindow.processMouseButtonDown(eventDict)

    def processMouseButtonUp(self, eventDict):
        self.mainWindow.processMouseButtonUp(eventDict)

    def processMouseMotion(self, eventDict):
        pass

    def processMinimize(self, eventDict = None):
        self.mainWindow.minimize()

    def processQuit(self, eventDict = None):
        self.mainWindow.quit()

    def processUndo(self):
        pass

    def processRedo(self):
        pass

    def processSelect(self):
        pass

    def processDelete(self):
        pass

    def processClone(self):
        pass

    def processSave(self):
        pass

    def processSettings(self):
        pass

    def processReset(self):
        logger.info("Reset called")
        self.mainGrid.reset()