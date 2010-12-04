import pygame
from threading import Thread
from time import sleep
import os

class MainWindow(Thread):
    def __init__(self):
        Thread.__init__(self, name = "MainWindow")
        pygame.display.init()
        pygame.display.set_caption("Lucidity")
        pygame.display.set_icon(self._getIcon())
        self.shouldQuit = False

    def run(self):
        windowFlags = pygame.DOUBLEBUF | pygame.OPENGL | pygame.HWSURFACE
        pygame.display.set_mode((1024, 768), windowFlags, 24)
        print(pygame.display.Info())
        print(pygame.display.get_driver())
        while not self.shouldQuit:
            event = pygame.event.wait()
            self._processEvent(event)

        pygame.display.quit()

    def _processEvent(self, event):
        print("Got event ", event)

    def quit(self):
        # TODO: Should we use a mutex here?
        self.shouldQuit = True

    def _getIcon(self):
        return pygame.image.load(os.path.join(".", "icon.png"))