import pygame as pg
from layer import Layer

class Base(pg.sprite.Sprite):
    '''The ground of the game'''
    TOPLEFT = (-96, 800)
    
    def __init__(self, image, *groups):
        self.image = image
        self.rect = self.image.get_rect(topleft = Base.TOPLEFT)
        self._layer = Layer.BASE

        super().__init__(groups)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)