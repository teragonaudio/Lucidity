import pygame

class Panel:
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 colorChooser:"ColorChooser", skin:"Skin"):
        self.parentSurface = parentSurface
        self._colorChooser = colorChooser
        self.rect = rect
        self.background = None
        self.skin = skin
        self._widgets = []

    def addWidget(self, widget:"Widget"):
        self._widgets.append(widget)

    def width(self): return self.rect.width
    def height(self): return self.rect.height

    def draw(self): pass
    def onMouseDown(self, position): pass
    def onMouseUp(self, position): pass

class Toolbar(Panel):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 colorChooser:"ColorChooser", skin:"Skin", backgroundColor):
        Panel.__init__(self, parentSurface, rect, colorChooser, skin)
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill(backgroundColor)
        self.parentSurface.blit(self.background, self.rect)
        pygame.display.flip()

    def onMouseDown(self, position):
        for widget in self._widgets:
            if widget.rect.collidepoint(position):
                widget.onMouseDown()

    def onMouseUp(self, position):
        for widget in self._widgets:
            if widget.rect.collidepoint(position):
                widget.onMouseUp()
