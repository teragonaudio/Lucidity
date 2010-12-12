from pygame.sprite import Sprite
from lucidity.log import logger

class Block(Sprite):
    def __init__(self, image:"Surface", position):
        Sprite.__init__(self)
        self.rect = image.get_rect().move(position[0], position[1])
        self.image = image.convert_alpha()

    def moveLeft(self, numPixels:"int"):
        self.rect.move_ip(0 - numPixels, 0)

    def update(self, *args):
        self.moveLeft(1)

    def kill(self):
        logger.debug("Killing sprite")
        super().kill()
