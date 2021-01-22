import pygame as pg
import pymunk
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LAYERS


class Base(pg.sprite.Sprite):
    TOPLEFT = (-96, 800)
    
    def __init__(self, image, *groups):
        super().__init__(groups)
        
        self.image = image
        self.rect = self.image.get_rect(topleft = Base.TOPLEFT)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bird(pg.sprite.Sprite):
    CENTER = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
    FLAP_FORCE = (0, -10000)
    CYCLE_WINGS_TIME = 50
    DYING_IMPULSE = (-1500, -8000)
    
    def __init__(self, game, images, *groups):
        super().__init__(groups)
        
        # logic
        self.game = game
        self.images = images
        self.image = images[1]
        self.rect = self.image.get_rect(center = Bird.CENTER)
        self._layer = LAYERS["foreground"]
        
        
        # physics
        moment = pymunk.moment_for_box(15, self.image.get_size())
        self.body = pymunk.Body(15, moment, body_type = pymunk.Body.DYNAMIC)
        self.body.position = self.rect.x, self.rect.y
        
        self.game.space.add(self.body)
        
    
    def update(self):
        self.rect.x, self.rect.y = self.body.position
        
        if not self.game.gameover:
            self.check_collition()
        
        
    def cycle_wings(self):
        self.images.insert(0, self.images.pop())
        self.image = pg.transform.rotate(self.images[0], -self.body.velocity.y // 30)
        
    
    def flap(self):
        self.body.velocity = (0, 0)
        self.body.apply_impulse_at_local_point(Bird.FLAP_FORCE)
        self.game.wing_sound.play()
        
    
    def check_collition(self):
        is_collided_with_bounds = self.rect.y < 0
        is_collided_with_base = self.rect.colliderect(self.game.base.rect)
        is_collided_with_pipe = self.rect.collidelist(self.game.pipes) != -1
        
        if is_collided_with_base or is_collided_with_bounds or is_collided_with_pipe :
            self.game.end_game()
            
    
    def die(self):
        self.velocity = (0, 0)
        self.body.apply_impulse_at_local_point(Bird.DYING_IMPULSE)
        


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
    

class ScoreMessage(pg.sprite.Sprite):
    CENTER = (SCREEN_WIDTH // 2, 100)
    
    def __init__(self, font, *groups):
        super().__init__(groups)
        
        self.font = font
        self.update_score(0)
        self.rect = self.image.get_rect(center = ScoreMessage.CENTER)
        self._layer = LAYERS["ui"]
    
    
    def update_score(self, score):
        self.image = self.font.render(str(score), True, pg.Color("white"))
        

class StartMessage(pg.sprite.Sprite):
    CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def __init__(self, image, *groups):
        super().__init__(groups)
        
        self.image = image
        self.rect = image.get_rect(center = StartMessage.CENTER)
        self._layer = LAYERS["ui"]


class GameoverMessage(pg.sprite.Sprite):
    CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def __init__(self, image, *groups):
        super().__init__(groups)
        
        self.image = image
        self.rect = image.get_rect(center = GameoverMessage.CENTER)
        self._layer = LAYERS["ui"]

