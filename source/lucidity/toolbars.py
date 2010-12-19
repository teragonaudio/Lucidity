import pygame
from lucidity.layout import Sizing, Positioning
from lucidity.containers import Toolbar
from lucidity.widgets import Button, Label

class TopToolbar(Toolbar):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 skin:"Skin", backgroundColor, delegate):
        Toolbar.__init__(self, parentSurface, rect, skin, backgroundColor)
        firstButtonRect = pygame.Rect(rect.left + Sizing.toolbarPadding,
                                      rect.top + Sizing.toolbarPadding, 0, 0)
        leftButton = Button(parentSurface, firstButtonRect,
                            skin.images["Left-Arrow-Up"],
                            skin.images["Left-Arrow-Down"],
                            delegate.processMoveLeft)
        self.addWidget(leftButton)
        rightButton = Button(parentSurface, Positioning.rectToRight(leftButton.rect, Sizing.toolbarPadding),
                             skin.images["Right-Arrow-Up"],
                             skin.images["Right-Arrow-Down"],
                             delegate.processMoveRight)
        self.addWidget(rightButton)
        upButton = Button(parentSurface, Positioning.rectToRight(rightButton.rect, Sizing.toolbarPadding),
                          skin.images["Up-Arrow-Up"],
                          skin.images["Up-Arrow-Down"],
                          delegate.processMoveUp)
        self.addWidget(upButton)
        downButton = Button(parentSurface, Positioning.rectToRight(upButton.rect, Sizing.toolbarPadding),
                            skin.images["Down-Arrow-Up"],
                            skin.images["Down-Arrow-Down"],
                            delegate.processMoveDown)
        self.addWidget(downButton)

        placeholderUp = skin.images["Placeholder-Up"]
        placeholderDown = skin.images["Placeholder-Down"]
        cueButton = Button(parentSurface, Positioning.rectToRight(downButton.rect, Sizing.toolbarEmptySpace),
                           placeholderUp, placeholderDown, delegate.processCue)
        self.addWidget(cueButton)
        undoButton = Button(parentSurface, Positioning.rectToRight(cueButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.processUndo)
        self.addWidget(undoButton)
        redoButton = Button(parentSurface, Positioning.rectToRight(undoButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.processRedo)
        self.addWidget(redoButton)

        selectButton = Button(parentSurface, Positioning.rectToRight(redoButton.rect, Sizing.toolbarEmptySpace),
                              placeholderUp, placeholderDown, delegate.processSelect)
        self.addWidget(selectButton)
        deleteButton = Button(parentSurface, Positioning.rectToRight(selectButton.rect, Sizing.toolbarPadding),
                              placeholderUp, placeholderDown, delegate.processDelete)
        self.addWidget(deleteButton)
        cloneButton = Button(parentSurface, Positioning.rectToRight(deleteButton.rect, Sizing.toolbarPadding),
                             placeholderUp, placeholderDown, delegate.processClone)
        self.addWidget(cloneButton)
        saveButton = Button(parentSurface, Positioning.rectToRight(cloneButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.processSave)
        self.addWidget(saveButton)

        lastButtonRect = pygame.Rect(rect.right - Sizing.toolbarPadding - Sizing.toolbarButtonSize,
                                     rect.top + Sizing.toolbarPadding, 0, 0)
        settingsButton = Button(parentSurface, lastButtonRect, placeholderUp, placeholderDown, delegate.processSettings)
        self.addWidget(settingsButton)

        statusLabelLeft = saveButton.rect.right + Sizing.toolbarEmptySpace
        statusLabelRect = pygame.Rect(statusLabelLeft, rect.top + Sizing.toolbarPadding,
                                      lastButtonRect.left - Sizing.toolbarEmptySpace - statusLabelLeft,
                                      Sizing.toolbarButtonSize)
        self.statusLabel = Label(parentSurface, statusLabelRect,
                                 "resources/graphics/fonts/AtomicClockRadio.ttf",
                                 skin.colorChooser.findColor("White"), 22,
                                 True, skin.colorChooser.findColor("Black"),
                                 backgroundColor)
        self.addWidget(self.statusLabel)

    def setStatusText(self, text):
        self.statusLabel.setText(text)
        
class BottomToolbar(Toolbar):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect", skin:"Skin", backgroundColor, delegate):
        Toolbar.__init__(self, parentSurface, rect, skin, backgroundColor)