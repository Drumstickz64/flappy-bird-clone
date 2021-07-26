import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LAYERS

class StartMessage(pg.sprite.Sprite):
    CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def __init__(self, image, *groups):
        super().__init__(groups)
        
        self.image = image
        self.rect = image.get_rect(center = StartMessage.CENTER)
        self._layer = LAYERS["ui"]
