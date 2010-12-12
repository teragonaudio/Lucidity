import pygame

class Widget:
    def __init__(self, parentSurface:"Surface", rect:"Rect"):
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
