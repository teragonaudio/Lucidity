import pygame
from pygame.sprite import DirtySprite
from lucidity.gui.colors import ColorChooser
from lucidity.gui.drawing import Border
from lucidity.gui.layout import Positioning, Padding, Sizing
from lucidity.gui.skinning import Skin
from lucidity.gui.widgets import Button

class Popup(DirtySprite):
    def __init__(self, parentSurface:pygame.Surface, rect:pygame.Rect, skin:Skin):
        DirtySprite.__init__(self)
        self.parentSurface = parentSurface
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(skin.guiColor("Popup Background"))
        self.rect = rect
        self.contentRect = Positioning.innerRect(self.image.get_rect(), Padding.POPUP_WINDOW_FRAME)
        toolbarHeight = (Padding.POPUP_WINDOW_FRAME * 2) + Sizing.POPUP_WINDOW_FRAME_BUTTON
        self.contentRect = pygame.Rect(Padding.POPUP_WINDOW_FRAME,
                                       toolbarHeight,
                                       rect.width - (Padding.POPUP_WINDOW_FRAME * 2),
                                       rect.height - toolbarHeight - Padding.POPUP_WINDOW_FRAME)
        self.skin = skin
        self.visible = False

    def drawWindowDecorations(self):
        closeButtonRect = pygame.Rect(self.rect.right - Padding.POPUP_WINDOW_FRAME - Sizing.TOOLBAR_BUTTON,
                                      self.rect.top + Padding.POPUP_WINDOW_FRAME,
                                      Sizing.POPUP_WINDOW_FRAME_BUTTON,
                                      Sizing.POPUP_WINDOW_FRAME_BUTTON)
        self.closeButton = Button(self.parentSurface, closeButtonRect,
                                  self.skin.images["Close-Up"],
                                  self.skin.images["Close-Down"],
                                  ColorChooser.BLACK, self.hide)
        self.image.blit(self.closeButton.activeImage, closeButtonRect)

    def show(self):
        Border.draw(self.image, ColorChooser.BLACK, width=1)
        self.drawWindowDecorations()
        popupSurface = self.getPopupSurface(self.contentRect)
        self.image.blit(popupSurface, self.contentRect)
        self.visible = True

    def hide(self):
        self.visible = False

    def getPopupSurface(self, rect:pygame.Rect): pass
    def onMouseDown(self, position): pass
    def onMouseUp(self, position): pass

class SearchPopup(Popup):
    def __init__(self, parentSurface:pygame.Surface, rect:pygame.Rect, skin:Skin):
        Popup.__init__(self, parentSurface, rect, skin)

    def getPopupSurface(self, rect:pygame.Rect):
        surface = pygame.Surface((rect.width, rect.height))
        surface.fill(self.skin.guiColor("Popup Foreground"))
        return surface

    def onMouseDown(self, position): pass
    def onMouseUp(self, position): pass