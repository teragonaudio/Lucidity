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
        self._fonts = self._loadFonts(skinPath, "Fonts.txt")

    def font(self, itemName:"str"):
        return self._fonts[itemName]

    def guiColor(self, itemName:"str"):
        return self._guiColors.findColor(itemName)

    def nextPaletteColor(self, interval:"int"=1):
        return self._palette.nextColor(interval)

    def _loadColors(self, skinPath:"str", colorFileName:"str"):
        return ColorChooser.createFromDefinition(os.path.join(skinPath, colorFileName))

    def _loadFonts(self, skinPath:"str", fontFileName:"str"):
        result = {}
        fontFile = open(os.path.join(skinPath, fontFileName))
        import re
        regex = re.compile("([\w\s]+):\s*([\w\.]+)")
        for line in fontFile:
            matches = regex.match(line)
            result[matches.group(1)] = os.path.join(skinPath, matches.group(2))

        return result

    def _loadImages(self, skinPath:"str"):
        images = {}

        for image in os.listdir(skinPath):
            imageTypeName = os.path.splitext(os.path.basename(image))[0]
            try:
                images[imageTypeName] = pygame.image.load(os.path.join(skinPath, image))
            except pygame.error:
                logger.debug("Could not load image '" + imageTypeName + "'")

        return images
