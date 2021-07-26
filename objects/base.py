import pygame as pg

class Base(pg.sprite.Sprite):
    '''The ground of the game'''
    TOPLEFT = (-96, 800)
    
    def __init__(self, image, *groups):
        super().__init__(groups)
        
        self.image = image
        self.rect = self.image.get_rect(topleft = Base.TOPLEFT)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)