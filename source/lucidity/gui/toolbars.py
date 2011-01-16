import pygame
from lucidity.gui.containers import Toolbar
from lucidity.gui.layout import Padding, Positioning, Spacing, Sizing
from lucidity.gui.widgets import Button, Filmstrip, Label
from lucidity.system.status import StatusDelegate

class TopToolbar(Toolbar, StatusDelegate):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect",
                 skin:"Skin", backgroundColor, delegate):
        Toolbar.__init__(self, parentSurface, rect, skin, backgroundColor)

        placeholderUp = skin.images["Placeholder-Up"]
        placeholderDown = skin.images["Placeholder-Down"]
        borderColor = None #skin.guiColor("Toolbar Widget Border Color")

        firstButtonRect = pygame.Rect(rect.left + Padding.TOOLBAR,
                                      rect.top + Padding.TOOLBAR, 0, 0)
        leftButton = Button(parentSurface, firstButtonRect,
                            skin.images["Left-Button-Up"],
                            skin.images["Left-Button-Down"],
                            borderColor,
                            delegate.onMoveLeft)
        self.addWidget(leftButton)
        rightButton = Button(parentSurface, Positioning.rectToRight(leftButton.rect, Padding.TOOLBAR),
                             skin.images["Right-Button-Up"],
                             skin.images["Right-Button-Down"],
                             borderColor,
                             delegate.onMoveRight)
        self.addWidget(rightButton)
        upButton = Button(parentSurface, Positioning.rectToRight(rightButton.rect, Padding.TOOLBAR),
                          skin.images["Up-Button-Up"],
                          skin.images["Up-Button-Down"],
                          borderColor,
                          delegate.onMoveUp)
        self.addWidget(upButton)
        downButton = Button(parentSurface, Positioning.rectToRight(upButton.rect, Padding.TOOLBAR),
                            skin.images["Down-Button-Up"],
                            skin.images["Down-Button-Down"],
                            borderColor,
                            delegate.onMoveDown)
        self.addWidget(downButton)

        cueButton = Button(parentSurface, Positioning.rectToRight(downButton.rect, Spacing.TOOLBAR_BUTTON_GAP),
                           skin.images["Cue-Button-Up"],
                           skin.images["Cue-Button-Down"],
                           borderColor,
                           delegate.onCue)
        self.addWidget(cueButton)
        undoButton = Button(parentSurface, Positioning.rectToRight(cueButton.rect, Padding.TOOLBAR),
                            skin.images["Undo-Button-Up"],
                            skin.images["Undo-Button-Down"],
                            borderColor,
                            delegate.onUndo)
        self.addWidget(undoButton)
        redoButton = Button(parentSurface, Positioning.rectToRight(undoButton.rect, Padding.TOOLBAR),
                            skin.images["Redo-Button-Up"],
                            skin.images["Redo-Button-Down"],
                            borderColor,
                            delegate.onRedo)
        self.addWidget(redoButton)

        selectButton = Button(parentSurface, Positioning.rectToRight(redoButton.rect, Spacing.TOOLBAR_BUTTON_GAP),
                              skin.images["Select-Button-Up"],
                              skin.images["Select-Button-Down"],
                              borderColor,
                              delegate.onSelect)
        self.addWidget(selectButton)
        cutButton = Button(parentSurface, Positioning.rectToRight(selectButton.rect, Padding.TOOLBAR),
                           skin.images["Cut-Button-Up"],
                           skin.images["Cut-Button-Down"],
                           borderColor,
                           delegate.onCut)
        self.addWidget(cutButton)
        cloneButton = Button(parentSurface, Positioning.rectToRight(cutButton.rect, Padding.TOOLBAR),
                             skin.images["Clone-Button-Up"],
                             skin.images["Clone-Button-Down"],
                             borderColor,
                             delegate.onClone)
        self.addWidget(cloneButton)
        bounceButton = Button(parentSurface, Positioning.rectToRight(cloneButton.rect, Padding.TOOLBAR),
                              skin.images["Bounce-Button-Up"],
                              skin.images["Bounce-Button-Down"],
                              borderColor,
                              delegate.onBounce)
        self.addWidget(bounceButton)

        lastButtonRect = pygame.Rect(rect.right - Padding.TOOLBAR - Sizing.TOOLBAR_BUTTON,
                                     rect.top + Padding.TOOLBAR, 0, 0)
        settingsButton = Button(parentSurface, lastButtonRect,
                                skin.images["Settings-Button-Up"],
                                skin.images["Settings-Button-Down"],
                                borderColor,
                                delegate.onSettings)
        self.addWidget(settingsButton)

        statusLabelLeft = bounceButton.rect.right + Spacing.TOOLBAR_BUTTON_GAP
        statusLabelRect = pygame.Rect(statusLabelLeft, rect.top + Padding.TOOLBAR,
                                      lastButtonRect.left - Spacing.TOOLBAR_BUTTON_GAP - statusLabelLeft,
                                      Sizing.TOOLBAR_BUTTON)
        self.statusLabel = Label(parentSurface, statusLabelRect,
                                 skin.font("Status"),
                                 skin.guiColor("Toolbar Text"), 1,
                                 borderColor,
                                 skin.guiColor("Toolbar Status Background"))
        self.addWidget(self.statusLabel)

    def onStatusUpdate(self, status:"str"):
        self.statusLabel.setText(status)

class BottomToolbar(Toolbar):
    def __init__(self, parentSurface:"Surface", rect:"pygame.Rect", skin:"Skin", backgroundColor, delegate):
        Toolbar.__init__(self, parentSurface, rect, skin, backgroundColor)

        borderColor = skin.guiColor("Toolbar Widget Border Color")

        lastButtonRect = pygame.Rect(rect.right - Sizing.TOOLBAR_BUTTON - Padding.TOOLBAR,
                                     rect.bottom - Sizing.TOOLBAR_BUTTON - Padding.TOOLBAR,
                                     Sizing.TOOLBAR_BUTTON, Sizing.TOOLBAR_BUTTON)
        self.cpuUsageButton = Filmstrip(parentSurface, lastButtonRect, skin.images["CPU-Usage"], borderColor)
        self.addWidget(self.cpuUsageButton)

    def processCpuUsage(self, percent):
        self.cpuUsageButton.setImage(percent)

    def processMemUsage(self, memUsage):
        pass
