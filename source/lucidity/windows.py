import os
import pygame
from time import time
from lucidity.log import logger
from lucidity.colors import ColorChooser
from lucidity.keyboard import KeyHandler
from lucidity.grid import MainGrid
from lucidity.panels import Toolbar
from lucidity.layout import PanelSizer, Sizing, Positioning
from lucidity.widgets import Button
from lucidity.skinning import Skin

# Avoid warnings about unused locals, which is necessary for the event handlers to work
# properly via reflection
#noinspection PyUnusedLocal
class MainWindow():
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption("Lucidity")
        pygame.display.set_icon(pygame.image.load(os.path.join(".", "icon.png")))
        self._shouldQuit = False
        self.surface = None
        self._colorChooser = ColorChooser()
        self._keyHandler = KeyHandler()
        self._resolution = (1440, 900)
        self._panelSizer = PanelSizer()
        self._panels = []
        self._skin = Skin("default")
        self._maxFps = 30

    def run(self):
        """
        Open up the window for the application.  This must, sadly, be done in the main
        thread, or else the window will not properly respond to events.
        """
        windowFlags = pygame.FULLSCREEN
        self.surface = pygame.display.set_mode(self._resolution, windowFlags)
        self._printVideoInfo(pygame.display.Info())

        self.surface.fill(self._colorChooser.findColor("Black"))
        self._initializeSurfaces(self._resolution, self._skin)
        pygame.display.flip()

        logger.info("Initialized display with driver: " + pygame.display.get_driver())
        frames = 0
        initTime = time()
        frameRenderTimeInSec = 1 / self._maxFps

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
        pygame.display.quit()

    def _initializeSurfaces(self, resolution, skin:"Skin"):
        mainGrid = MainGrid(self.surface, self._panelSizer.getMainGridRect(resolution[0], resolution[1]),
                            self._colorChooser, self._skin)
        self._panels.append(mainGrid)

        topToolbar = Toolbar(self.surface, self._panelSizer.getTopToolbarRect(resolution[0]),
                             self._colorChooser, self._skin)
        firstButtonRect = pygame.Rect(topToolbar.rect.left + Sizing.toolbarPadding,
                                      topToolbar.rect.top + Sizing.toolbarPadding, 0, 0)
        leftButton = Button(self.surface, firstButtonRect,
                            skin.images["Left-Arrow-Up"],
                            skin.images["Left-Arrow-Down"],
                            mainGrid.moveLeft)
        topToolbar.addButton(leftButton)
        rightButton = Button(self.surface, Positioning.rectToRight(leftButton.rect, Sizing.toolbarPadding),
                             skin.images["Right-Arrow-Up"],
                             skin.images["Right-Arrow-Down"],
                             mainGrid.moveRight)
        upButton = Button(self.surface, Positioning.rectToRight(rightButton.rect, Sizing.toolbarPadding),
                          skin.images["Up-Arrow-Up"],
                          skin.images["Up-Arrow-Down"],
                          mainGrid.moveUp)
        topToolbar.addButton(upButton)
        downButton = Button(self.surface, Positioning.rectToRight(upButton.rect, Sizing.toolbarPadding),
                            skin.images["Down-Arrow-Up"],
                            skin.images["Down-Arrow-Down"],
                            mainGrid.moveDown)
        topToolbar.addButton(downButton)
        topToolbar.addButton(rightButton)
        self._panels.append(topToolbar)

        bottomToolbar = Toolbar(self.surface, self._panelSizer.getBottomToolbarRect(resolution[0], resolution[1]),
                                self._colorChooser, self._skin)
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
            processFunction = getattr(self, "_process" + eventType)
            processFunction(event.dict)
        except AttributeError:
            logger.info("Event type '" + eventType + "' is not handled")

    def _processActiveEvent(self, eventDict):
        gain = eventDict['gain']
        state = eventDict['state']
        logger.info("Application activated, gain: " + str(gain) + ", state: " + str(state))

    def _processKeyDown(self, eventDict):
        pass

    def _processKeyUp(self, eventDict):
        self._keyHandler.processKey(self, eventDict['key'], eventDict['mod'])
        pass

    def _processMouseButtonDown(self, eventDict):
        logger.debug("Down at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for panel in self._panels:
            if panel.rect.collidepoint(clickPosition[0], clickPosition[1]):
                panel.onMouseDown(clickPosition)

    def _processMouseButtonUp(self, eventDict):
        logger.debug("Up at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for panel in self._panels:
            if panel.rect.collidepoint(clickPosition[0], clickPosition[1]):
                panel.onMouseUp(clickPosition)

    def _processMouseMotion(self, eventDict):
        pass

    def _processQuit(self, eventDict = None):
        self.quit()

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
