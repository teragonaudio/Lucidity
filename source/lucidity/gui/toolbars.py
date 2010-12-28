import pygame
from lucidity.gui.containers import Toolbar
from lucidity.gui.layout import Sizing, Positioning
from lucidity.gui.widgets import Button, Filmstrip, Label
from lucidity.system.status import StatusDelegate

class TopToolbar(Toolbar, StatusDelegate):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 skin:"Skin", backgroundColor, delegate):
        Toolbar.__init__(self, parentSurface, rect, skin, backgroundColor)
        firstButtonRect = pygame.Rect(rect.left + Sizing.toolbarPadding,
                                      rect.top + Sizing.toolbarPadding, 0, 0)
        leftButton = Button(parentSurface, firstButtonRect,
                            skin.images["Left-Arrow-Up"],
                            skin.images["Left-Arrow-Down"],
                            delegate.onMoveLeft)
        self.addWidget(leftButton)
        rightButton = Button(parentSurface, Positioning.rectToRight(leftButton.rect, Sizing.toolbarPadding),
                             skin.images["Right-Arrow-Up"],
                             skin.images["Right-Arrow-Down"],
                             delegate.onMoveRight)
        self.addWidget(rightButton)
        upButton = Button(parentSurface, Positioning.rectToRight(rightButton.rect, Sizing.toolbarPadding),
                          skin.images["Up-Arrow-Up"],
                          skin.images["Up-Arrow-Down"],
                          delegate.onMoveUp)
        self.addWidget(upButton)
        downButton = Button(parentSurface, Positioning.rectToRight(upButton.rect, Sizing.toolbarPadding),
                            skin.images["Down-Arrow-Up"],
                            skin.images["Down-Arrow-Down"],
                            delegate.onMoveDown)
        self.addWidget(downButton)

        placeholderUp = skin.images["Placeholder-Up"]
        placeholderDown = skin.images["Placeholder-Down"]
        cueButton = Button(parentSurface, Positioning.rectToRight(downButton.rect, Sizing.toolbarEmptySpace),
                           placeholderUp, placeholderDown, delegate.onCue)
        self.addWidget(cueButton)
        undoButton = Button(parentSurface, Positioning.rectToRight(cueButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.onUndo)
        self.addWidget(undoButton)
        redoButton = Button(parentSurface, Positioning.rectToRight(undoButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.onRedo)
        self.addWidget(redoButton)

        selectButton = Button(parentSurface, Positioning.rectToRight(redoButton.rect, Sizing.toolbarEmptySpace),
                              placeholderUp, placeholderDown, delegate.onSelect)
        self.addWidget(selectButton)
        deleteButton = Button(parentSurface, Positioning.rectToRight(selectButton.rect, Sizing.toolbarPadding),
                              placeholderUp, placeholderDown, delegate.onDelete)
        self.addWidget(deleteButton)
        cloneButton = Button(parentSurface, Positioning.rectToRight(deleteButton.rect, Sizing.toolbarPadding),
                             placeholderUp, placeholderDown, delegate.onClone)
        self.addWidget(cloneButton)
        saveButton = Button(parentSurface, Positioning.rectToRight(cloneButton.rect, Sizing.toolbarPadding),
                            placeholderUp, placeholderDown, delegate.onSave)
        self.addWidget(saveButton)

        lastButtonRect = pygame.Rect(rect.right - Sizing.toolbarPadding - Sizing.toolbarButtonSize,
                                     rect.top + Sizing.toolbarPadding, 0, 0)
        settingsButton = Button(parentSurface, lastButtonRect, placeholderUp, placeholderDown, delegate.onSettings)
        self.addWidget(settingsButton)

        statusLabelLeft = saveButton.rect.right + Sizing.toolbarEmptySpace
        statusLabelRect = pygame.Rect(statusLabelLeft, rect.top + Sizing.toolbarPadding,
                                      lastButtonRect.left - Sizing.toolbarEmptySpace - statusLabelLeft,
                                      Sizing.toolbarButtonSize)
        self.statusLabel = Label(parentSurface, statusLabelRect,
                                 skin.font("Status"),
                                 skin.guiColor("Toolbar Text"), 1,
                                 skin.guiColor("Toolbar Outline"),
                                 skin.guiColor("Toolbar Status Background"))
        self.addWidget(self.statusLabel)

    def onStatusUpdate(self, status:"str"):
        self.statusLabel.setText(status)

class BottomToolbar(Toolbar):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect", skin:"Skin", backgroundColor, delegate):
        Toolbar.__init__(self, parentSurface, rect, skin, backgroundColor)

        lastButtonRect = pygame.Rect(rect.right - Sizing.toolbarButtonSize - Sizing.toolbarPadding,
                                     rect.bottom - Sizing.toolbarButtonSize - Sizing.toolbarPadding,
                                     Sizing.toolbarButtonSize, Sizing.toolbarButtonSize)
        self.cpuUsageButton = Filmstrip(parentSurface, lastButtonRect, skin.images["CPU-Usage"])
        self.addWidget(self.cpuUsageButton)

    def processCpuUsage(self, percent):
        self.cpuUsageButton.setImage(percent)

    def processMemUsage(self, memUsage):
        # logger.debug("Memory usage: " + str(memUsage / 1048576) + "Mb")
        pass
