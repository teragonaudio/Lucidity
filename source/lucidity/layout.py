import pygame

class PanelSizer:
    gridPadding = 24
    toolbarPadding = 6
    toolbarButtonSize = 32

    def _topToolbarHeight(self):
        return self.toolbarButtonSize + (self.toolbarPadding * 2)

    def getTopToolbarRect(self, screenWidth):
        toolbarHeight = self._topToolbarHeight()
        return pygame.Rect(0, 0, screenWidth, toolbarHeight)

    def _bottomToolbarHeight(self):
        toolbarHeight = (self.toolbarButtonSize * 2) + (self.toolbarPadding * 2)
        return toolbarHeight

    def getBottomToolbarRect(self, screenWidth, screenHeight):
        toolbarHeight = self._bottomToolbarHeight()
        return pygame.Rect(0, screenHeight - toolbarHeight, screenWidth, toolbarHeight)

    def getMainGridRect(self, screenWidth, screenHeight):
        return pygame.Rect(0, self._topToolbarHeight(), screenWidth,
                           screenHeight - self._topToolbarHeight() - self._bottomToolbarHeight())