import os
import pygame
import time
from lucidity.arrangement import Sequence
from lucidity.log import logger
from lucidity.keyboard import KeyHandler
from lucidity.grid import MainGrid
from lucidity.layout import PanelSizer
from lucidity.midi import MidiEventLoop
from lucidity.paths import PathFinder
from lucidity.performance import SystemUsage
from lucidity.settings import Settings
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
        self._systemUsage = SystemUsage(self.mainDelegate)

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

        frames = 0
        initTime = time.time()
        frameRenderTimeInSec = 1 / self._maxFps

        if self.settings.getInt("midi.enable"):
            self._midiEventLoop.start()
        self._systemUsage.start()

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
            frames += 1

        logger.info("Lucidity is quitting. Bye-bye!")
        totalTime = time.time() - initTime
        logger.info("Average FPS: " + str(frames / totalTime))
        self._systemUsage.quit()
        self._midiEventLoop.quit()
        pygame.display.quit()
        pygame.quit()

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
                                skin, toolbarBackgroundColor, self.mainDelegate)
        self._containers.append(topToolbar)
        self._setStatusTextCallback = topToolbar.setStatusText

        bottomToolbar = BottomToolbar(self.surface,
                                      panelSizer.getBottomToolbarRect(resolution[0], resolution[1]),
                                      skin, toolbarBackgroundColor, self.mainDelegate)
        self._containers.append(bottomToolbar)

    def quit(self):
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

    def processMouseButtonDown(self, eventDict):
        # logger.debug("Down at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for container in self._containers:
            if container.rect.collidepoint(clickPosition[0], clickPosition[1]):
                container.onMouseDown(clickPosition)

    def processMouseButtonUp(self, eventDict):
        # logger.debug("Up at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for container in self._containers:
            if container.rect.collidepoint(clickPosition[0], clickPosition[1]):
                container.onMouseUp(clickPosition)

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

    def processCpuUsage(self, cpuUsage):
        # logger.debug("CPU usage: " + str(cpuUsage))
        pass

    def processMemUsage(self, memUsage):
        # logger.debug("Memory usage: " + str(memUsage / 1048576) + "Mb")
        pass

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