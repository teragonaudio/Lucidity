import pygame
from lucidity.layout import Sizing

class Widget:
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect"):
        self.parentSurface = parentSurface
        self.rect = rect

    def onMouseDown(self): pass
    def onMouseUp(self): pass
    def draw(self): pass

class Button(Widget):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 upImage:"Surface", downImage:"Surface",
                 onClickHandler:"callable"):
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
                 fontName, fontColor, fontSize,
                 drawBorder, borderColor, backgroundColor):
        Widget.__init__(self, parentSurface, rect)
        if drawBorder:
            pygame.draw.rect(self.parentSurface, borderColor, self.rect, 1)

        self.rect = pygame.Rect(rect.left + Sizing.widgetPadding, rect.top + Sizing.widgetPadding,
                                rect.width - (Sizing.widgetPadding * 2),
                                rect.height - (Sizing.widgetPadding * 2))
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill(backgroundColor)
        self.backgroundColor = backgroundColor

        pygame.font.init()
        self._font = pygame.font.Font(fontName, fontSize)
        self._color = fontColor
        self._text = ""

    def draw(self):
        fontSurface = self._font.render(self._text, True, self._color)
        self.parentSurface.blit(self.background, self.rect)
        self.parentSurface.blit(fontSurface, self.rect)
        pygame.display.update(self.rect)

    def setText(self, text:"str"):
        self._text = text
        self.draw()

class ItemPanel(Widget):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 upImage:"Surface", downImage:"Surface"):
        Widget.__init__(self, parentSurface, rect)
        
        #self.itemImageButton = Button()