import pygame

class Sizing:
    gridPadding = 24
    toolbarPadding = 6
    toolbarEmptySpace = 24
    toolbarButtonSize = 32
    fontPadding = 4
    blockPadding = 6

class FontSizer:
    MIN_FONT_SIZE_IN_POINTS = 8
    MAX_FONT_SIZE_IN_POINTS = 32

    @staticmethod
    def bestFitSizeInPoints(fontName:str, height:int):
        lastSize = FontSizer.MIN_FONT_SIZE_IN_POINTS

        # TODO: Yes, this is a bit lame.  Probably there is a better way to calculate this
        for pointSize in range(FontSizer.MIN_FONT_SIZE_IN_POINTS, FontSizer.MAX_FONT_SIZE_IN_POINTS):
            font = pygame.font.Font(fontName, pointSize)
            linesizeInPixels = font.get_linesize()
            if linesizeInPixels > height:
                break
            lastSize = pointSize

        return lastSize

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

    @staticmethod
    def innerRect(sourceRect:pygame.Rect, padding:int):
        return pygame.Rect(sourceRect.left + padding, sourceRect.top + padding,
                           sourceRect.width - (padding * 2), sourceRect.height - (padding * 2))