import pygame
from lucidity.layout import Sizing
from lucidity.sprites import Block

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

class MainGrid(Panel):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 colorChooser:"ColorChooser", skin:"Skin"):
        Panel.__init__(self, parentSurface, rect, colorChooser, skin)
        backgroundColor = colorChooser.findColor("Black")
        self.parentSurface.fill(backgroundColor, self.rect)
        self.sprites = pygame.sprite.RenderUpdates()

        gridRect = pygame.Rect(0, self.rect.top + Sizing.gridPadding,
                               self.rect.width,
                               self.rect.height - (Sizing.gridPadding * 2))
        self.rect = gridRect
        self.background = pygame.Surface((gridRect.width, gridRect.height))
        self.background = self.background.convert()
        self.background.fill(colorChooser.findColor("Banana Mania"))
        self.parentSurface.blit(self.background, self.rect)
        pygame.display.flip()

    def draw(self):
        self.sprites.clear(self.parentSurface, self.background)
        self.sprites.update()
        updateRects = self.sprites.draw(self.parentSurface)
        pygame.display.update(updateRects)
        for sprite in self.sprites.sprites():
            if not self.rect.colliderect(sprite.rect):
                sprite.kill()

    def onMouseDown(self, position):
        pass

    def onMouseUp(self, position):
        block = Block(pygame.image.load("icon.png"), position)
        self.sprites.add(block)

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def moveUp(self):
        pass

    def moveDown(self):
        pass

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
