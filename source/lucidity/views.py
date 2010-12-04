from threading import Thread
import pygame
from time import sleep

class MainWindow(Thread):
    def __init__(self):
        pygame.display.init()

    def run(self):
        windowFlags = pygame.DOUBLEBUF | pygame.OPENGL
        pygame.display.set_mode(resolution = (1024, 768), flags = windowFlags, depth = 24)
        sleep(10)
