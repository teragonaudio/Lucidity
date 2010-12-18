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

    def width(self): return self.rect.width
    def height(self): return self.rect.height

    def draw(self): pass
    def onMouseDown(self, position): pass
    def onMouseUp(self, position): pass

class Toolbar(Panel):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 colorChooser:"ColorChooser", skin:"Skin"):
        Panel.__init__(self, parentSurface, rect, colorChooser, skin)
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill(colorChooser.findColor("Gray"))
        self.parentSurface.blit(self.background, self.rect)
        pygame.display.flip()

    def addButton(self, button:"Button"):
        self._widgets.append(button)

    def draw(self):
        for widget in self._widgets:
            if False: #widget.isDirty:
                self.parentSurface.blit(self.background, widget.rect, widget.rect)
                widget.draw()

    def onMouseDown(self, position):
        for widget in self._widgets:
            if widget.rect.collidepoint(position):
                widget.onMouseDown()

    def onMouseUp(self, position):
        for widget in self._widgets:
            if widget.rect.collidepoint(position):
                widget.onMouseUp()
