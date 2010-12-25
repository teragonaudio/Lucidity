import pygame
import os
from lucidity.colors import ColorChooser
from lucidity.paths import PathFinder

class Skin:
    def __init__(self, name:str, interval:int):
        self.name = name
        skinPath = PathFinder.findSkin(name)
        self.images = self._loadImages(skinPath)
        self._guiColors = self._loadColors(skinPath, "GuiColors.txt")
        self._palette = self._loadColors(skinPath, "Palette.txt")
        self._fonts = self._loadFonts(skinPath, "Fonts.txt")
        self.interval = interval

    def font(self, itemName:"str"):
        return self._fonts[itemName]

    def guiColor(self, itemName:"str"):
        return self._guiColors.findColor(itemName)

    def nextPaletteColor(self):
        return self._palette.nextColor(self.interval)

    def _loadColors(self, skinPath:"str", colorFileName:"str"):
        return ColorChooser.createFromDefinition(os.path.join(skinPath, colorFileName))

    def _loadFonts(self, skinPath:"str", fontFileName:"str"):
        result = {}

        pygame.font.init()
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
                # File could not be loaded, really not a big deal since there are also
                # other skinning resources in this directory and such.
                pass

        return images
