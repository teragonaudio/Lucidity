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
                            delegate.processMoveLeft)
        self.addButton(leftButton)
        rightButton = Button(parentSurface, Positioning.rectToRight(leftButton.rect, Sizing.toolbarPadding),
                             skin.images["Right-Arrow-Up"],
                             skin.images["Right-Arrow-Down"],
                             delegate.processMoveRight)
        self.addButton(rightButton)
        upButton = Button(parentSurface, Positioning.rectToRight(rightButton.rect, Sizing.toolbarPadding),
                          skin.images["Up-Arrow-Up"],
                          skin.images["Up-Arrow-Down"],
                          delegate.processMoveUp)
        self.addButton(upButton)
        downButton = Button(parentSurface, Positioning.rectToRight(upButton.rect, Sizing.toolbarPadding),
                            skin.images["Down-Arrow-Up"],
                            skin.images["Down-Arrow-Down"],
                            delegate.processMoveDown)
        self.addButton(downButton)

        placeholderUp = skin.images["Placeholder-Up"]
        placeholderDown = skin.images["Placeholder-Down"]
        cueButton = Button(parentSurface, Positioning.rectToRight(downButton.rect, Sizing.toolbarEmptySpace),
                           placeholderUp, placeholderDown, delegate.processCue)
        self.addButton(cueButton)
        undoButton = Button(parentSurface, Positioning.rectToRight(cueButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.processUndo)
        self.addButton(undoButton)
        redoButton = Button(parentSurface, Positioning.rectToRight(undoButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.processRedo)
        self.addButton(redoButton)

        selectButton = Button(parentSurface, Positioning.rectToRight(redoButton.rect, Sizing.toolbarEmptySpace),
                              placeholderUp, placeholderDown, delegate.processSelect)
        self.addButton(selectButton)
        deleteButton = Button(parentSurface, Positioning.rectToRight(selectButton.rect, Sizing.toolbarPadding),
                              placeholderUp, placeholderDown, delegate.processDelete)
        self.addButton(deleteButton)
        cloneButton = Button(parentSurface, Positioning.rectToRight(deleteButton.rect, Sizing.toolbarPadding),
                             placeholderUp, placeholderDown, delegate.processClone)
        self.addButton(cloneButton)
        saveButton = Button(parentSurface, Positioning.rectToRight(cloneButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.processSave)
        self.addButton(saveButton)

        lastButtonRect = pygame.Rect(rect.right - Sizing.toolbarPadding - Sizing.toolbarButtonSize,
                                     rect.top + Sizing.toolbarPadding, 0, 0)
        settingsButton = Button(parentSurface, lastButtonRect, placeholderUp, placeholderDown, delegate.processSettings)
        self.addButton(settingsButton)
        
class BottomToolbar(Toolbar):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 colorChooser:"ColorChooser", skin:"Skin", delegate):
        Toolbar.__init__(self, parentSurface, rect, colorChooser, skin)