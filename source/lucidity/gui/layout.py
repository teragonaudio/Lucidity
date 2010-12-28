import pygame

class Sizing:
    gridPadding = 24
    toolbarPadding = 6
    toolbarEmptySpace = 24
    toolbarButtonSize = 32
    fontPadding = 4

class PanelSizer:
    def _topToolbarHeight(self):
        return Sizing.toolbarButtonSize + (Sizing.toolbarPadding * 2)

    def getTopToolbarRect(self, screenWidth):
        toolbarHeight = self._topToolbarHeight()
        return pygame.Rect(0, 0, screenWidth, toolbarHeight)

    def _bottomToolbarHeight(self):
        toolbarHeight = (Sizing.toolbarButtonSize * 2) + (Sizing.toolbarPadding * 2)
        return toolbarHeight

    def getBottomToolbarRect(self, screenWidth, screenHeight):
        toolbarHeight = self._bottomToolbarHeight()
        return pygame.Rect(0, screenHeight - toolbarHeight, screenWidth, toolbarHeight)

    def getMainGridRect(self, screenWidth, screenHeight):
        return pygame.Rect(0, self._topToolbarHeight(), screenWidth,
                           screenHeight - self._topToolbarHeight() - self._bottomToolbarHeight())

class Positioning:
    @staticmethod
    def rectToRight(sourceRect:"Rect", padding:"int" = 0):
        return pygame.Rect(sourceRect.left + sourceRect.width + padding, sourceRect.top,
                           sourceRect.width, sourceRect.height)