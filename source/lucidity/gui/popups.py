import pygame
from pygame.sprite import DirtySprite
from lucidity.gui.colors import ColorChooser
from lucidity.gui.drawing import Border
from lucidity.gui.skinning import Skin

class Popup(DirtySprite):
    def __init__(self, parentSurface:pygame.Surface, rect:pygame.Rect, skin:Skin):
        DirtySprite.__init__(self)
        self.parentSurface = parentSurface
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(skin.guiColor("Popup Background"))
        self.rect = rect
        self.skin = skin
        self.visible = False

    def show(self):
        Border.draw(self.image, ColorChooser.DEFAULT_COLOR)
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, *args):
        pass

class SearchPopup(Popup):
    def __init__(self, parentSurface:pygame.Surface, rect:pygame.Rect, skin:Skin):
        super().__init__(parentSurface, rect, skin)

