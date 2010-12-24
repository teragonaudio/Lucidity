import pygame
import os
from lucidity.colors import ColorChooser
from lucidity.paths import PathFinder
from lucidity.log import logger

class Skin:
    def __init__(self, name:"str"):
        self.name = name
        skinPath = PathFinder.findSkin(name)
        self.images = self._loadImages(skinPath)
        self._guiColors = self._loadColors(skinPath, "GuiColors.txt")
        self._palette = self._loadColors(skinPath, "Palette.txt")

    def guiColor(self, colorName:"str"):
        return self._guiColors.findColor(colorName)

    def nextPaletteColor(self, interval:"int"=1):
        return self._palette.nextColor(interval)

    def _loadColors(self, skinPath:"str", colorFileName:"str"):
        return ColorChooser.createFromDefinition(os.path.join(skinPath, colorFileName))

    def _loadImages(self, skinPath:"str"):
        images = {}

        for image in os.listdir(skinPath):
            imageTypeName = os.path.splitext(os.path.basename(image))[0]
            try:
                images[imageTypeName] = pygame.image.load(os.path.join(skinPath, image))
            except pygame.error:
                logger.debug("Could not load image '" + imageTypeName + "'")

        return images
