import pygame as pg
import settings
from layer import Layer


class Pipe(pg.sprite.Sprite):
    VELOCITY_X = -5
    GAP = 250
    SPAWN_TIME = 1500
    
    def __init__(self, game, image, *groups, primary, **rect_kwargs):
        
        # logic
        self.game = game
        self.image = image
        self.rect = self.image.get_rect(**rect_kwargs)
        self._layer = Layer.OBSTACLE
        # the primary pipe is the one that increments the score
        self.primary = primary
        # whether the pipe has passed the bird or not
        # keeps the same pipe from incrementing the score many times
        self.passed = False
        
        super().__init__(groups)
    
    def update(self):
        if self.game.gameover:
            return
        
        self.rect.x += Pipe.VELOCITY_X
        
        # increment the score when a primary pipe passes the bird
        if self.rect.x < settings.SCREEN_WIDTH // 6 and self.primary and not self.passed:
            self.passed = True
            self.game.increment_score()
            self.game.point_sound.play()
        
        # kill the sprite after it leaves the screen
        if self.rect.right < 0:
            self.kill()
