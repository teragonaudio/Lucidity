import os
import pygame
import time
import lucidity
from lucidity.app.delegate import MainDelegate
from lucidity.core.arrangement import Sequence
from lucidity.gui.grid import MainGrid
from lucidity.gui.layout import PanelSizer
from lucidity.gui.skinning import Skin
from lucidity.gui.toolbars import TopToolbar, BottomToolbar
from lucidity.media.library import MediaRequestLoop, MediaRequest, MediaRequestDelegate, MediaFileConverter
from lucidity.media.media import MediaFile
from lucidity.midi.midi import MidiEventLoop
from lucidity.system.log import logger
from lucidity.system.performance import SystemUsageLoop
from lucidity.system.settings import Settings
from lucidity.system.status import StatusLoop, ObtuseStatusProvider

class MainWindow(MediaRequestDelegate):
    def __init__(self, delegate:MainDelegate, sequence:Sequence, settings:Settings,
                 mediaRequestLoop:MediaRequestLoop, midiEventLoop:MidiEventLoop,
                 statusLoop:StatusLoop, systemUsageLoop:SystemUsageLoop):
        # Important variables for delegate, system sequence, settings
        self.mainDelegate = delegate
        self.mainDelegate.mainWindow = self
        self.sequence = sequence
        self.settings = settings

        # References to system threads
        self._mediaRequestLoop = mediaRequestLoop
        self._midiEventLoop = midiEventLoop
        self._systemUsageLoop = systemUsageLoop
        self._systemUsageLoop.fpsProvider = self
        self._statusLoop = statusLoop

        # Initialize display
        pygame.display.init()
        pygame.display.set_caption("Lucidity")
        pygame.display.set_icon(pygame.image.load(os.path.join(".", "icon.png")))

        # Variables related to display
        self.surface = None
        self.mainGrid = None
        self._ready = False
        self._shouldQuit = False
        self._resolution = (1440, 900)
        self._containers = []
        self._skin = Skin(self.settings.getString("gui.skin"), self.settings.getInt("gui.colorInterval"))
        self._setStatusTextFunction = None
        self._getCurrentItemProvider = self.getCurrentItem
        self._framesProcessed = 0

    def open(self):
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
        pygame.display.flip()

        self._statusLoop.statusProvider = self.getStatusProvider(self.settings)

    def run(self):
        maxFps = self.settings.getFloat("gui.maxFps")
        frameRenderTimeInSec = 1 / maxFps
        while not self._ready:
            startTime = time.time()
            pygame.event.pump()
            self._processFrame(startTime, frameRenderTimeInSec)

        while not self._shouldQuit:
            startTime = time.time()
            for event in pygame.event.get():
                self._processEvent(event)
            self._processFrame(startTime, frameRenderTimeInSec)

        pygame.display.quit()
        pygame.quit()

    def _processFrame(self, startTime, frameRenderTimeInSec):
        self.sequence.tick()
        for container in self._containers:
            container.draw()

        sleepTime = frameRenderTimeInSec - (time.time() - startTime)
        if sleepTime > 0:
            pygame.time.delay(int(sleepTime * 1000))
        self._framesProcessed += 1

    def _processEvent(self, event):
        eventType = pygame.event.event_name(event.type)
        try:
            processFunction = getattr(self.mainDelegate, "on" + eventType)
            processFunction(event.dict)
        except AttributeError as exception:
            logger.info("Error handling event '" + eventType + "': " + str(exception))
        except pygame.error as exception:
            logger.error("Error from pygame: " + str(exception))

    def _initializePanels(self, resolution, skin:"Skin"):
        panelSizer = PanelSizer()
        self.mainGrid = MainGrid(self.surface,
                                 panelSizer.getMainGridRect(resolution[0], resolution[1]),
                                 skin, self.sequence)
        self._containers.append(self.mainGrid)
        self.mainDelegate.mainGrid = self.mainGrid

        toolbarBackgroundColor = self._skin.guiColor("Toolbar")
        topToolbar = TopToolbar(self.surface,
                                panelSizer.getTopToolbarRect(resolution[0]),
                                skin, toolbarBackgroundColor, self.mainDelegate)
        self._containers.append(topToolbar)
        self._setStatusTextFunction = topToolbar.onStatusUpdate

        bottomToolbar = BottomToolbar(self.surface,
                                      panelSizer.getBottomToolbarRect(resolution[0], resolution[1]),
                                      skin, toolbarBackgroundColor, self.mainDelegate)
        self._containers.append(bottomToolbar)
        self._systemUsageLoop.delegate = bottomToolbar
        self._statusLoop.delegate = topToolbar

    def onReady(self):
        self._ready = True

    def quit(self):
        self._shouldQuit = True

    def minimize(self):
        logger.debug("Minimizing")
        pygame.display.iconify()

    # TODO: This should be replaced by a method in the bottom toolbar
    def getCurrentItem(self):
        file = MediaFile("/foo/bar")
        file.title = "Sample Block"
        file.timeInSeconds = 30.0
        return file

    def insert(self):
        mediaFile = self._getCurrentItemProvider()
        cursorPosition = self.mainGrid.getCursorPosition()
        item = MediaFileConverter.getItemForMediaFile(mediaFile, self.mainGrid.getCursorTrack(),
                                                      cursorPosition.beats,
                                                      self.sequence.getTempo())
        self.sequence.addItem(item)

    def onRequestComplete(self, request:MediaRequest, args):
        if request.type == MediaRequest.RESCAN:
            self.setStatusText(args[0])
        elif request.type == MediaRequest.SEARCH:
            pass

    def setStatusText(self, text):
        self._setStatusTextFunction(text)

    def onMouseButtonDown(self, eventDict):
        # logger.debug("Down at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for container in self._containers:
            if container.absRect.collidepoint(clickPosition[0], clickPosition[1]):
                container.onMouseDown(clickPosition)

    def onMouseButtonUp(self, eventDict):
        # logger.debug("Up at " + str(eventDict['pos']))
        clickPosition = eventDict['pos']
        for container in self._containers:
            if container.absRect.collidepoint(clickPosition[0], clickPosition[1]):
                container.onMouseUp(clickPosition)

    def onStartMidiMapping(self):
        for container in self._containers:
            container.onStartMidiMapping()

    def onStopMidiMapping(self):
        for container in self._containers:
            container.onStopMidiMapping()

    def getFramesPerSec(self):
        totalTime = self.sequence.getTime() - self.sequence.clock.startTime
        if totalTime > 0:
            return self._framesProcessed / totalTime
        else:
            return 0.0

    def getStatusProvider(self, settings):
        providerName = settings.getString("gui.statusProvider")
        if providerName == "system":
            return self._systemUsageLoop
        elif providerName == "obtuse":
            return ObtuseStatusProvider()
        elif providerName == "debug":
            return lucidity.system.log.statusHandler
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
