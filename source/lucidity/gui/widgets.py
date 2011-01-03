import pygame
from pygame import Surface
from lucidity.gui.drawing import Border
from lucidity.gui.layout import Padding, FontSizer, Positioning

class Widget:
    def __init__(self, parentSurface:Surface, rect:pygame.Rect, borderColor:tuple,
                 onClickHandler):
        self.parentSurface = parentSurface
        self.rect = rect
        self.borderColor = borderColor
        self.onClickHandler = onClickHandler

    def onStartMidiMapping(self):
        self.draw()
        if self.onClickHandler is not None:
            overlay = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 100))
            self.parentSurface.blit(overlay, self.rect)
            pygame.display.update(self.rect)

    def onStopMidiMapping(self):
        self.draw()

    def getSurface(self): pass
    def onMouseDown(self): pass
    def onMouseUp(self): pass

    def draw(self):
        surface = self.getSurface()
        self.parentSurface.blit(surface, self.rect)
        if self.borderColor is not None:
            Border.draw(surface, self.borderColor)
        pygame.display.update(self.rect)

class Button(Widget):
    def __init__(self, parentSurface:Surface, rect:pygame.Rect,
                 upImage:Surface, downImage:Surface, borderColor:tuple,
                 onClickHandler):
        Widget.__init__(self, parentSurface, rect, borderColor, onClickHandler)
        self.upImage = upImage
        self.downImage = downImage
        self.activeImage = upImage
        self.rect.width = self.activeImage.get_width()
        self.rect.height = self.activeImage.get_height()
        self.draw()

    def onMouseDown(self):
        self.activeImage = self.downImage
        self.draw()

    def onMouseUp(self):
        self.activeImage = self.upImage
        self.onClickHandler()
        self.draw()

    def getSurface(self):
        return self.activeImage

class Label(Widget):
    def __init__(self, parentSurface:Surface, rect:pygame.Rect,
                 fontName:str, fontColor:tuple, numLines:int,
                 borderColor:tuple, backgroundColor:tuple):
        Widget.__init__(self, parentSurface, rect, borderColor, None)
        self.backgroundColor = backgroundColor
        self.surface = self.getBackgroundSurface()

        self.fontRect = Positioning.innerRect(self.surface.get_rect(), Padding.LABEL)
        fontSize = FontSizer.bestFitSizeInPoints(fontName, self.fontRect.height / numLines)
        self._font = pygame.font.Font(fontName, fontSize)
        self._color = fontColor
        self._text = ""
        self.draw()

    def getBackgroundSurface(self):
        surface = pygame.Surface((self.rect.width, self.rect.height))
        if self.backgroundColor:
            surface.fill(self.backgroundColor)
        return surface

    def getSurface(self):
        fontSurface = self._font.render(self._text, True, self._color)
        self.surface = self.getBackgroundSurface()
        self.surface.blit(fontSurface, self.fontRect)
        return self.surface

    def setText(self, text:"str"):
        self._text = text
        self.draw()

class Filmstrip(Widget):
    def __init__(self, parentSurface:Surface, rect:pygame.Rect, filmstrip:Surface, borderColor:tuple):
        Widget.__init__(self, parentSurface, rect, borderColor, None)
        self.images = []
        self.numImages = int(filmstrip.get_rect().height / filmstrip.get_rect().width)
        self.currentImage = 0
        clipRect = pygame.Rect(0, 0, rect.width, rect.height)
        for x in range(0, self.numImages):
            self.images.append(filmstrip.subsurface(clipRect))
            clipRect.move_ip(0, rect.height)
        self.draw()

    def getSurface(self):
        return self.images[self.currentImage]

    def setImage(self, percent:float):
        self.currentImage = int((self.numImages - 1) * (percent / 100.0))
        self.draw()

class ItemPanel(Widget):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect"):
        Widget.__init__(self, parentSurface, rect, None, None)