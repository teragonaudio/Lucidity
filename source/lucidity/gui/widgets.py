import pygame
from pygame import Surface
from lucidity.gui.drawing import Border
from lucidity.gui.layout import Sizing, FontSizer, Positioning

class Widget:
    def __init__(self, parentSurface:Surface, rect:pygame.Rect):
        self.parentSurface = parentSurface
        self.rect = rect

    def onMouseDown(self): pass
    def onMouseUp(self): pass
    def draw(self): pass

class Button(Widget):
    def __init__(self, parentSurface:Surface, rect:pygame.Rect,
                 upImage:Surface, downImage:Surface,
                 onClickHandler):
        Widget.__init__(self, parentSurface, rect)
        self.upImage = upImage
        self.downImage = downImage
        self.activeImage = upImage
        self.rect.width = self.activeImage.get_width()
        self.rect.height = self.activeImage.get_height()
        self.onClickHandler = onClickHandler
        self.draw()

    def onMouseDown(self):
        self.activeImage = self.downImage
        self.draw()

    def onMouseUp(self):
        self.activeImage = self.upImage
        self.onClickHandler()
        self.draw()

    def draw(self):
        self.parentSurface.blit(self.activeImage, self.rect)
        pygame.display.update(self.rect)

class Label(Widget):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 fontName, fontColor, numLines,
                 borderColor, backgroundColor):
        Widget.__init__(self, parentSurface, rect)
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill(backgroundColor)
        Border.draw(self.background, borderColor)

        self.fontRect = Positioning.innerRect(self.rect, Sizing.fontPadding)
        fontSize = FontSizer.bestFitSizeInPoints(fontName, self.fontRect.height / numLines)
        self._font = pygame.font.Font(fontName, fontSize)
        self._color = fontColor
        self._text = ""

    def draw(self):
        fontSurface = self._font.render(self._text, True, self._color)
        self.parentSurface.blit(self.background, self.rect)
        self.parentSurface.blit(fontSurface, self.fontRect)
        pygame.display.update(self.rect)

    def setText(self, text:"str"):
        self._text = text
        self.draw()

class Filmstrip(Widget):
    def __init__(self, parentSurface:Surface, rect:pygame.Rect, filmstrip:Surface):
        Widget.__init__(self, parentSurface, rect)
        self.images = []
        self.numImages = int(filmstrip.get_rect().height / filmstrip.get_rect().width)
        self.currentImage = 0
        clipRect = pygame.Rect(0, 0, rect.width, rect.height)
        for x in range(0, self.numImages):
            self.images.append(filmstrip.subsurface(clipRect))
            clipRect.move_ip(0, rect.height)
        self.draw()

    def draw(self):
        self.parentSurface.blit(self.images[self.currentImage], self.rect)
        pygame.display.update(self.rect)

    def setImage(self, percent:float):
        self.currentImage = int((self.numImages - 1) * (percent / 100.0))
        self.draw()

class ItemPanel(Widget):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect"):
        Widget.__init__(self, parentSurface, rect)