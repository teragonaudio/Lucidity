import pygame
from lucidity.layout import PanelSizer

class Panel:
    def __init__(self, surface, colorChooser, backgroundRect):
        self._surface = surface
        self._colorChooser = colorChooser
        self._backgroundRect = backgroundRect
        self._backgroundColor = None

    def height(self):
        return self._backgroundRect.height

    def width(self):
        return self._backgroundRect.width

    def update(self):
        pygame.display.update(self._backgroundRect)

class MainGrid(Panel):
    def __init__(self, surface, colorChooser, backgroundRect):
        Panel.__init__(self, surface, colorChooser, backgroundRect)
        self._backgroundColor = colorChooser.findColor("Black")
        pygame.draw.rect(self._surface, self._backgroundColor, self._backgroundRect)

        self._gridRect = pygame.Rect(0, self._backgroundRect.top + PanelSizer.gridPadding,
                                     self._backgroundRect.width,
                                     self._backgroundRect.height - (PanelSizer.gridPadding * 2))
        self._gridColor = self._colorChooser.findColor("Banana Mania") # Heh, yes!
        pygame.draw.rect(self._surface, self._gridColor, self._gridRect)

        self.update()

class Toolbar(Panel):
    def __init__(self, surface, colorChooser, backgroundRect):
        Panel.__init__(self, surface, colorChooser, backgroundRect)
        self._backgroundColor = colorChooser.findColor("Gray")
        pygame.draw.rect(self._surface, self._backgroundColor, self._backgroundRect)
        self.update()
