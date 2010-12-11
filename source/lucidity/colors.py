import random

AllColors = [
    ('Mahogany', (205,74,74), None),
    ('Fuzzy Wuzzy Brown', (204,102,102), None),
    ('Chestnut', (188,93,88), None),
    ('Red Orange', (255,83,73), None),
    ('Sunset Orange', (253,94,83), None),
    ('Bittersweet', (253,124,110), None),
    ('Melon', (253,188,180), None),
    ('Outrageous Orange', (255,110,74), None),
    ('Vivid Tangerine', (255,160,137), None),
    ('Burnt Sienna', (234,126,93), None),
    ('Brown', (180,103,77), None),
    ('Sepia', (165,105,79), None),
    ('Orange', (255,117,56), None),
    ('Burnt Orange', (255,127,73), None),
    ('Copper', (221,148,117), None),
    ('Mango Tango', (255,130,67), None),
    ('Atomic Tangerine', (255,164,116), None),
    ('Beaver', (159,129,112), None),
    ('Antique Brass', (205,149,117), None),
    ('Desert Sand', (239,205,184), None),
    ('Raw Sienna', (214,138,89), None),
    ('Tumbleweed', (222,170,136), None),
    ('Tan', (250,167,108), None),
    ('Peach', (255,207,171), None),
    ('Macaroni and Cheese', (255,189,136), None),
    ('Apricot', (253,217,181), None),
    ('Neon Carrot', (255,163,67), None),
    ('Almond', (239,219,197), None),
    ('Yellow Orange', (255,182,83), None),
    ('Gold', (231,198,151), None),
    ('Shadow', (138,121,93), None),
    ('Banana Mania', (250,231,181), None),
    ('Sunglow', (255,207,72), None),
    ('Goldenrod', (252,217,117), None),
    ('Dandelion', (253,219,109), None),
    ('Yellow', (252,232,131), None),
    ('Green Yellow', (240,232,145), None),
    ('Spring Green', (236,234,190), None),
    ('Olive Green', (186,184,108), None),
    ('Laser Lemon', (253,252,116), None),
    ('Unmellow Yellow', (253,252,116), None),
    ('Canary', (255,255,153), None),
    ('Yellow Green', (197,227,132), None),
    ('Inch Worm', (178,236,93), None),
    ('Asparagus', (135,169,107), None),
    ('Granny Smith Apple', (168,228,160), None),
    ('Electric Lime', (29,249,20), None),
    ('Screamin Green', (118,255,122), None),
    ('Fern', (113,188,120), None),
    ('Forest Green', (109,174,129), None),
    ('Sea Green', (159,226,191), None),
    ('Green', (28,172,120), None),
    ('Mountain Meadow', (48,186,143), None),
    ('Shamrock', (69,206,162), None),
    ('Jungle Green', (59,176,143), None),
    ('Caribbean Green', (28,211,162), None),
    ('Tropical Rain Forest', (23,128,109), None),
    ('Pine Green', (21,128,120), None),
    ('Robin Egg Blue', (31,206,203), None),
    ('Aquamarine', (120,219,226), None),
    ('Turquoise Blue', (119,221,231), None),
    ('Sky Blue', (128,218,235), None),
    ('Outer Space', (65,74,76), None),
    ('Blue Green', (25,158,189), None),
    ('Pacific Blue', (28,169,201), None),
    ('Cerulean', (29,172,214), None),
    ('Cornflower', (154,206,235), None),
    ('Midnight Blue', (26,72,118), None),
    ('Navy Blue', (25,116,210), None),
    ('Denim', (43,108,196), None),
    ('Blue', (31,117,254), None),
    ('Periwinkle', (197,208,230), None),
    ('Cadet Blue', (176,183,198), None),
    ('Indigo', (93,118,203), None),
    ('Wild Blue Yonder', (162,173,208), None),
    ('Manatee', (151,154,170), None),
    ('Blue Bell', (173,173,214), None),
    ('Blue Violet', (115,102,189), None),
    ('Purple Heart', (116,66,200), None),
    ('Royal Purple', (120,81,169), None),
    ('Purple Mountains Majesty', (157,129,186), None),
    ('Violet', (146,110,174), None),
    ('Wisteria', (205,164,222), None),
    ('Vivid Violet', (143,80,157), None),
    ('Fuchsia', (195,100,197), None),
    ('Shocking Pink', (251,126,253), None),
    ('Pink Flamingo', (252,116,253), None),
    ('Plum', (142,69,133), None),
    ('Hot Magenta', (255,29,206), None),
    ('Purple Pizzazz', (255,29,206), None),
    ('Razzle Dazzle Rose', (255,72,208), None),
    ('Orchid', (230,168,215), None),
    ('Red Violet', (192,68,143), None),
    ('Eggplant', (110,81,96), None),
    ('Cerise', (221,68,146), None),
    ('Wild Strawberry', (255,67,164), None),
    ('Magenta', (246,100,175), None),
    ('Lavender', (252,180,213), None),
    ('Cotton Candy', (255,188,217), None),
    ('Violet Red', (247,83,148), None),
    ('Carnation Pink', (255,170,204), None),
    ('Razzmatazz', (227,37,107), None),
    ('Piggy Pink', (253,215,228), None),
    ('Jazzberry Jam', (202,55,103), None),
    ('Blush', (222,93,131), None),
    ('Tickle Me Pink', (252,137,172), None),
    ('Pink Sherbet', (247,128,161), None),
    ('Maroon', (200,56,90), None),
    ('Red', (238,32,77), None),
    ('Radical Red', (255,73,108), None),
    ('Mauvelous', (239,152,170), None),
    ('Wild Watermelon', (252,108,133), None),
    ('Scarlet', (252,40,71), None),
    ('Salmon', (255,155,170), None),
    ('Brick Red', (203,65,84), None),
    ('White', (237,237,237), None),
    ('Timberwolf', (219,215,210), None),
    ('Silver', (205,197,194), None),
    ('Gray', (149,145,140), None),
    ('Black', (35,35,35), None),
]

class ColorChooser:
    def __init__(self):
        self._currentIndex = 0

    def currentColor(self):
        return AllColors[self._currentIndex][1]

    def _findColor(self, colorName):
        # TODO: Yeah, yeah, this could easily be made more efficient.  Whatever.
        for i in range(0, len(AllColors)):
            color = AllColors[i]
            if color[0] == colorName:
                return color
        raise Exception("Color '" + colorName + "' not found")

    def findColor(self, colorName):
        color = self._findColor(colorName)
        return color[1]

    def nextColor(self, interval = 1):
        nextIndex = self._currentIndex + interval
        if nextIndex >= len(AllColors):
            nextIndex = 0
        self._currentIndex = nextIndex
        return self.currentColor()

    def randomColor(self):
        self._currentIndex = random.randint(0, len(AllColors))
        return self.currentColor()

    def removeColor(self, colorName):
        color = self._findColor(colorName)
        AllColors.remove(color)