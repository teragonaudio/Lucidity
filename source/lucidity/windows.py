import os
import pygame
from time import time
from lucidity.log import logger
from lucidity.colors import ColorChooser
from lucidity.keyboard import KeyHandler
from lucidity.grid import MainGrid
from lucidity.layout import PanelSizer
from lucidity.midi import MidiEventLoop
from lucidity.toolbars import TopToolbar, BottomToolbar
from lucidity.skinning import Skin

class MainWindow():
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption("Lucidity")
        pygame.display.set_icon(pygame.image.load(os.path.join(".", "icon.png")))
        self.mainDelegate = MainDelegate(self)
        self.surface = None
        self._shouldQuit = False
        self._colorChooser = ColorChooser()
        self._resolution = (1440, 900)
        self._panels = []
        self._skin = Skin("default")
        self._maxFps = 30
        self._midiEventLoop = MidiEventLoop(self.mainDelegate)

    def run(self):
        """
        Open up the window for the application.  This must, sadly, be done in the main
        thread, or else the window will not properly respond to events.
        """
        windowFlags = pygame.FULLSCREEN
        self.surface = pygame.display.set_mode(self._resolution, windowFlags)
        self._printVideoInfo(pygame.display.Info())

        self.surface.fill(self._colorChooser.findColor("Black"))
        self._initializePanels(self._resolution, self._colorChooser, self._skin)
        pygame.display.flip()

        logger.info("Initialized display with driver: " + pygame.display.get_driver())
        frames = 0
        initTime = time()
        frameRenderTimeInSec = 1 / self._maxFps

        self._midiEventLoop.start()

        while not self._shouldQuit:
            startTime = time()
            for event in pygame.event.get():
                self._processEvent(event)

            for panel in self._panels:
                panel.draw()

            sleepTime = frameRenderTimeInSec - (time() - startTime)
            if sleepTime > 0:
                pygame.time.delay(int(sleepTime * 1000))
            frames += 1

        totalTime = time() - initTime
        logger.info("Average FPS: " + str(frames / totalTime))
        self._midiEventLoop.quit()
        pygame.display.quit()

    def _initializePanels(self, resolution, colorChooser:"ColorChooser", skin:"Skin"):
        panelSizer = PanelSizer()
        mainGrid = MainGrid(self.surface,
                            panelSizer.getMainGridRect(resolution[0], resolution[1]),
                            colorChooser, skin)
        self._panels.append(mainGrid)
        self.mainDelegate.mainGrid = mainGrid

        topToolbar = TopToolbar(self.surface,
                                panelSizer.getTopToolbarRect(resolution[0]),
                                colorChooser, skin, self.mainDelegate)
        self._panels.append(topToolbar)

        bottomToolbar = BottomToolbar(self.surface,
                                      panelSizer.getBottomToolbarRect(resolution[0], resolution[1]),
                                      colorChooser, skin, self.mainDelegate)
        self._panels.append(bottomToolbar)

    def quit(self):
        logger.info("Lucidity is quitting. Bye-bye!")
        self._shouldQuit = True

    def minimize(self):
        logger.debug("Minimizing")
        pygame.display.iconify()

    def _processEvent(self, event):
        eventType = pygame.event.event_name(event.type)
        try:
            processFunction = getattr(self.mainDelegate, "process" + eventType)
            processFunction(event.dict)
        except AttributeError:
            logger.info("Event type '" + eventType + "' is not handled")

    def processMouseButtonDown(self, eventDict):
        logger.debug("Down at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for panel in self._panels:
            if panel.rect.collidepoint(clickPosition[0], clickPosition[1]):
                panel.onMouseDown(clickPosition)

    def processMouseButtonUp(self, eventDict):
        logger.debug("Up at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for panel in self._panels:
            if panel.rect.collidepoint(clickPosition[0], clickPosition[1]):
                panel.onMouseUp(clickPosition)

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