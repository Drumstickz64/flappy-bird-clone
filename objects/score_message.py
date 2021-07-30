import pygame as pg
import settings

class ScoreMessage(pg.sprite.Sprite):
    '''Class that represents the floating score display at the top of the screen'''
    CENTER = (settings.SCREEN_WIDTH // 2, 100)
    
    def __init__(self, font, *groups):
        super().__init__(groups)
        
        self.font = font
        self.update_score(0)
        self.rect = self.image.get_rect(center = ScoreMessage.CENTER)
        self._layer = settings.LAYERS["ui"]
    
    
    def update_score(self, score):
        self.image = self.font.render(str(score), True, pg.Color("white"))
