import os
import pygame
from lucidity.log import logger
from lucidity.colors import Colors

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

    def run(self):
        """
        Open up the window for the application.  This must, sadly, be done in the main
        thread, or else the window will not properly respond to events.
        """
        windowFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self._surface = pygame.display.set_mode((1024, 768), windowFlags, 24)
        print(pygame.display.Info())

        self._surface.fill(Colors.darkBackgroundColor)
        pygame.display.flip()

        logger.debug("Initialized display with driver: " + pygame.display.get_driver())
        while not self._shouldQuit:
            event = pygame.event.wait()
            self._processEvent(event)

        pygame.display.quit()

    def quit(self):
        self._shouldQuit = True

    def _processEvent(self, event):
        eventType = pygame.event.event_name(event.type)
        try:
            processFunction = getattr(self, "_process" + eventType)
            processFunction(event.dict)
        except AttributeError:
            logger.info("Event type '" + eventType + "' cannot be handled")

    #noinspection PyUnusedLocal
    def _processQuit(self, eventDict = None):
        self.quit()