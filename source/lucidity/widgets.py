import pygame

class Widget:
    def __init__(self, rect:"Rect"):
        self.rect = rect

    def onMouseDown(self): pass
    def onMouseUp(self): pass
    def update(self): pass

class Button(Widget):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 upImage:"Surface", downImage:"Surface",
                 onClickHandler:"callable"):
        Widget.__init__(self, rect)
        self.upImage = upImage
        self.downImage = downImage
        self.activeImage = upImage
        self.rect.width = self.activeImage.get_width()
        self.rect.height = self.activeImage.get_height()
        self._surface = parentSurface
        self.onClickHandler = onClickHandler

    def onMouseDown(self):
        self.activeImage = self.downImage
        self.update()

    def onMouseUp(self):
        self.activeImage = self.upImage
        self.update()
        self.onClickHandler()

    def update(self):
        self._surface.blit(self.activeImage, self.rect)
        pygame.display.update(self.rect)
