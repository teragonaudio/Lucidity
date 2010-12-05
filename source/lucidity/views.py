import os
import pygame
from lucidity.log import logger
from lucidity.colors import ColorChooser
from lucidity.keyboard import KeyHandler
from lucidity.panels import MainGrid, Toolbar
from lucidity.layout import PanelSizer

# Avoid warnings about unused locals, which is necessary for the event handlers to work
# properly via reflection
#noinspection PyUnusedLocal
class MainWindow():
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption("Lucidity")
        pygame.display.set_icon(pygame.image.load(os.path.join(".", "icon.png")))
        self._shouldQuit = False
        self._surface = None
        self._colorChooser = ColorChooser()
        self._keyHandler = KeyHandler()
        self._resolution = (1440, 900)
        self._panelSizer = PanelSizer()
        self._surfaces = []

    def run(self):
        """
        Open up the window for the application.  This must, sadly, be done in the main
        thread, or else the window will not properly respond to events.
        """
        windowFlags = pygame.HWSURFACE | pygame.FULLSCREEN
        self._surface = pygame.display.set_mode(self._resolution, windowFlags, 32)
        self._printVideoInfo(pygame.display.Info())

        self._surface.fill(self._colorChooser.findColor("Black"))
        self._initializeSurfaces(self._resolution)
        pygame.display.flip()

        logger.debug("Initialized display with driver: " + pygame.display.get_driver())
        while not self._shouldQuit:
            event = pygame.event.wait()
            self._processEvent(event)

        pygame.display.quit()

    def _initializeSurfaces(self, resolution):
        topToolbar = Toolbar(self._surface, self._colorChooser,
                             self._panelSizer.getTopToolbarRect(resolution[0]))
        self._surfaces.append(topToolbar)
        bottomToolbar = Toolbar(self._surface, self._colorChooser,
                                self._panelSizer.getBottomToolbarRect(resolution[0], resolution[1]))
        mainGrid = MainGrid(self._surface, self._colorChooser,
                            self._panelSizer.getMainGridRect(resolution[0], resolution[1]))
        self._surfaces.append(mainGrid)

    def quit(self):
        logger.info("Lucidity is quitting. Bye-bye!")
        self._shouldQuit = True

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
        pass

    def _processMouseButtonUp(self, eventDict):
        logger.debug("Click at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        drawRect = pygame.Rect(clickPosition[0], clickPosition[1], 60, 60)
        pygame.draw.rect(self._surface, self._colorChooser.nextColor(3), drawRect)
        pygame.display.update(drawRect)

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
