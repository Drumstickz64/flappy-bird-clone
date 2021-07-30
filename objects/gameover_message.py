import pygame as pg
import settings

class GameoverMessage(pg.sprite.Sprite):
    CENTER = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
    
    def __init__(self, image, *groups):
        super().__init__(groups)
        
        self.image = image
        self.rect = image.get_rect(center = GameoverMessage.CENTER)
        self._layer = settings.LAYERS["ui"]
