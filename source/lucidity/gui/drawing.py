import pygame

class Border:
    @staticmethod
    def draw(surface:pygame.Surface, color:tuple, width:int=1):
        rect = surface.get_rect()
        pointlist = [(rect.left, rect.top),
                     (rect.right - 1, rect.top),
                     (rect.right - 1, rect.bottom - 1),
                     (rect.left, rect.bottom - 1)]
        pygame.draw.lines(surface, color, True, pointlist, width)
