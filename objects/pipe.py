import pygame as pg
from settings import SCREEN_WIDTH, LAYERS

class Pipe(pg.sprite.Sprite):
    VELOCITY_X = -5
    GAP = 250
    SPAWN_TIME = 1500
    
    def __init__(self, game, image, primary, *groups, **rect_kwargs):
        super().__init__(groups)
        
        # logic
        self.game = game
        self.image = image
        self.rect = self.image.get_rect(**rect_kwargs)
        self._layer = LAYERS["background"]
        # the primary pipe is the one that increments the score
        self.primary = primary
        # whether the pipe has passed the bird or not
        # keeps the same pipe from incrementing the score many times
        self.passed = False
        
    
    def update(self):
        if self.game.gameover:
            return
        
        self.rect.x += Pipe.VELOCITY_X
        
        # increment the score when a primary pipe passes the bird
        if self.rect.x < SCREEN_WIDTH // 6 and self.primary and not self.passed:
            self.passed = True
            self.game.increment_score()
            self.game.point_sound.play()
        
        # kill the sprite after it leaves the screen
        if self.rect.right < 0:
            self.game.objects.remove(self)
            self.kill()
