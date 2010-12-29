import pygame
from lucidity.gui.containers import Toolbar
from lucidity.gui.layout import Padding, Positioning, Spacing, Sizing
from lucidity.gui.widgets import Button, Filmstrip, Label
from lucidity.system.status import StatusDelegate

class TopToolbar(Toolbar, StatusDelegate):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 skin:"Skin", backgroundColor, delegate):
        Toolbar.__init__(self, parentSurface, rect, skin, backgroundColor)
        firstButtonRect = pygame.Rect(rect.left + Padding.TOOLBAR,
                                      rect.top + Padding.TOOLBAR, 0, 0)
        leftButton = Button(parentSurface, firstButtonRect,
                            skin.images["Left-Arrow-Up"],
                            skin.images["Left-Arrow-Down"],
                            delegate.onMoveLeft)
        self.addWidget(leftButton)
        rightButton = Button(parentSurface, Positioning.rectToRight(leftButton.rect, Padding.TOOLBAR),
                             skin.images["Right-Arrow-Up"],
                             skin.images["Right-Arrow-Down"],
                             delegate.onMoveRight)
        self.addWidget(rightButton)
        upButton = Button(parentSurface, Positioning.rectToRight(rightButton.rect, Padding.TOOLBAR),
                          skin.images["Up-Arrow-Up"],
                          skin.images["Up-Arrow-Down"],
                          delegate.onMoveUp)
        self.addWidget(upButton)
        downButton = Button(parentSurface, Positioning.rectToRight(upButton.rect, Padding.TOOLBAR),
                            skin.images["Down-Arrow-Up"],
                            skin.images["Down-Arrow-Down"],
                            delegate.onMoveDown)
        self.addWidget(downButton)

        placeholderUp = skin.images["Placeholder-Up"]
        placeholderDown = skin.images["Placeholder-Down"]
        cueButton = Button(parentSurface, Positioning.rectToRight(downButton.rect, Spacing.TOOLBAR_BUTTON_GAP),
                           placeholderUp, placeholderDown, delegate.onCue)
        self.addWidget(cueButton)
        undoButton = Button(parentSurface, Positioning.rectToRight(cueButton.rect, Padding.TOOLBAR),
                            placeholderUp, placeholderDown, delegate.onUndo)
        self.addWidget(undoButton)
        redoButton = Button(parentSurface, Positioning.rectToRight(undoButton.rect, Padding.TOOLBAR),
                            placeholderUp, placeholderDown, delegate.onRedo)
        self.addWidget(redoButton)

        selectButton = Button(parentSurface, Positioning.rectToRight(redoButton.rect, Spacing.TOOLBAR_BUTTON_GAP),
                              placeholderUp, placeholderDown, delegate.onSelect)
        self.addWidget(selectButton)
        deleteButton = Button(parentSurface, Positioning.rectToRight(selectButton.rect, Padding.TOOLBAR),
                              placeholderUp, placeholderDown, delegate.onDelete)
        self.addWidget(deleteButton)
        cloneButton = Button(parentSurface, Positioning.rectToRight(deleteButton.rect, Padding.TOOLBAR),
                             placeholderUp, placeholderDown, delegate.onClone)
        self.addWidget(cloneButton)
        bounceButton = Button(parentSurface, Positioning.rectToRight(cloneButton.rect, Padding.TOOLBAR),
                              placeholderUp, placeholderDown, delegate.onBounce)
        self.addWidget(bounceButton)

        lastButtonRect = pygame.Rect(rect.right - Padding.TOOLBAR - Sizing.TOOLBAR_BUTTON,
                                     rect.top + Padding.TOOLBAR, 0, 0)
        settingsButton = Button(parentSurface, lastButtonRect, placeholderUp, placeholderDown, delegate.onSettings)
        self.addWidget(settingsButton)

        statusLabelLeft = bounceButton.rect.right + Spacing.TOOLBAR_BUTTON_GAP
        statusLabelRect = pygame.Rect(statusLabelLeft, rect.top + Padding.TOOLBAR,
                                      lastButtonRect.left - Spacing.TOOLBAR_BUTTON_GAP - statusLabelLeft,
                                      Sizing.TOOLBAR_BUTTON)
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

        lastButtonRect = pygame.Rect(rect.right - Sizing.TOOLBAR_BUTTON - Padding.TOOLBAR,
                                     rect.bottom - Sizing.TOOLBAR_BUTTON - Padding.TOOLBAR,
                                     Sizing.TOOLBAR_BUTTON, Sizing.TOOLBAR_BUTTON)
        self.cpuUsageButton = Filmstrip(parentSurface, lastButtonRect, skin.images["CPU-Usage"])
        self.addWidget(self.cpuUsageButton)

    def processCpuUsage(self, percent):
        self.cpuUsageButton.setImage(percent)

    def processMemUsage(self, memUsage):
        # logger.debug("Memory usage: " + str(memUsage / 1048576) + "Mb")
        pass
