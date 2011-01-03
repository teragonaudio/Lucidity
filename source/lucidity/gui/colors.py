import random
import re

class ColorChooser:
    DEFAULT_COLOR = (0, 0, 0)
    REGEX_RGB_DECIMAL = re.compile('([\w\s]+):\s*(\d+)\s*,(\d+)\s*,(\d+)')
    REGEX_RGB_HEX = re.compile('([\w\s]+):\s*#(\w\w)(\w\w)(\w\w)')

    @staticmethod
    def createFromDefinition(definitionFilePath:"str"):
        colorChooser = ColorChooser()
        definitionFile = open(definitionFilePath, "r")
        for line in definitionFile:
            lineColor = ColorChooser.colorFromLine(line)
            if lineColor is not None:
                colorChooser.addColor(lineColor[0], lineColor[1])

        definitionFile.close()
        # Randomize first index
        colorChooser.randomColor()
        return colorChooser

    @staticmethod
    def colorFromLine(line:"str"):
        matches = ColorChooser.REGEX_RGB_DECIMAL.match(line)
        if matches is not None:
            colorName = matches.group(1)
            colorTuple = (int(matches.group(2)),
                          int(matches.group(3)),
                          int(matches.group(4)))
            return colorName, colorTuple

        matches = ColorChooser.REGEX_RGB_HEX.match(line)
        if matches is not None:
            colorName = matches.group(1)
            colorTuple = (int(matches.group(2), 16),
                          int(matches.group(3), 16),
                          int(matches.group(4), 16))
            return colorName, colorTuple

        return None

    @staticmethod
    def isDarkColor(color:"tuple"):
        # Convert RGB to luminosity
        # http://en.wikipedia.org/wiki/HSL_and_HSV#Lightness
        # Since RGB values go from 0- 255, I have divided each of those coefficients
        # by 255 rather than converting each value.
        luminosity = (float(color[0]) * 0.001176470588235 +
                      float(color[1]) * 0.002313725490196 +
                      float(color[2]) * 0.00043137254902)
        return luminosity < 0.5

    def __init__(self):
        self._currentIndex = 0
        self._colors = {}
        self._colorList = []

    def addColor(self, name:str, value:tuple):
        self._colors[name] = value
        self._colorList.append(value)

    def currentColor(self):
        try:
            return self._colorList[self._currentIndex]
        except IndexError:
            return self.DEFAULT_COLOR

    def findColor(self, colorName):
        try:
            return self._colors[colorName]
        except KeyError:
            return None

    def nextColor(self, interval=1):
        nextIndex = self._currentIndex + interval
        if nextIndex >= len(self._colorList):
            nextIndex %= len(self._colorList)
        self._currentIndex = nextIndex
        return self.currentColor()

    def randomColor(self):
        self._currentIndex = random.randint(0, len(self._colorList))
        return self.currentColor()
