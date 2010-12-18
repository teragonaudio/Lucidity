import pygame
from lucidity.layout import Sizing, Positioning
from lucidity.panels import Toolbar
from lucidity.widgets import Button

class TopToolbar(Toolbar):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 colorChooser:"ColorChooser", skin:"Skin", delegate):
        Toolbar.__init__(self, parentSurface, rect, colorChooser, skin)
        firstButtonRect = pygame.Rect(rect.left + Sizing.toolbarPadding,
                                      rect.top + Sizing.toolbarPadding, 0, 0)
        leftButton = Button(parentSurface, firstButtonRect,
                            skin.images["Left-Arrow-Up"],
                            skin.images["Left-Arrow-Down"],
                            delegate.moveLeft)
        self.addButton(leftButton)
        rightButton = Button(parentSurface, Positioning.rectToRight(leftButton.rect, Sizing.toolbarPadding),
                             skin.images["Right-Arrow-Up"],
                             skin.images["Right-Arrow-Down"],
                             delegate.moveRight)
        self.addButton(rightButton)
        upButton = Button(parentSurface, Positioning.rectToRight(rightButton.rect, Sizing.toolbarPadding),
                          skin.images["Up-Arrow-Up"],
                          skin.images["Up-Arrow-Down"],
                          delegate.moveUp)
        self.addButton(upButton)
        downButton = Button(parentSurface, Positioning.rectToRight(upButton.rect, Sizing.toolbarPadding),
                            skin.images["Down-Arrow-Up"],
                            skin.images["Down-Arrow-Down"],
                            delegate.moveDown)
        self.addButton(downButton)

class BottomToolbar(Toolbar):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 colorChooser:"ColorChooser", skin:"Skin", delegate):
        Toolbar.__init__(self, parentSurface, rect, colorChooser, skin)