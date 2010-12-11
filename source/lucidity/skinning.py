import pygame
import os

class Skin:
    def __init__(self, name:"str"):
        self.name = name
        self.images = self._loadImages()

    def _loadImages(self):
        images = {}

        skinsPath = os.path.abspath("resources/graphics/skins")
        imagePath = os.path.join(skinsPath, self.name)
        if not os.path.exists(imagePath):
            raise Exception("Skins path '" + skinsPath + "' does not exist")
        for image in os.listdir(imagePath):
            imageTypeName = os.path.splitext(os.path.basename(image))[0]
            images[imageTypeName] = pygame.image.load(os.path.join(imagePath, image))

        return images