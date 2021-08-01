import pygame as pg
import pymunk
import settings
from layer import Layer

class Bird(pg.sprite.Sprite):
    CENTER = (settings.SCREEN_WIDTH // 4, settings.SCREEN_HEIGHT // 3)
    FLAP_FORCE = (0, -10000)
    DYING_IMPULSE = (-1500, -8000)
    CYCLE_WINGS_TIME = 50
    CYCLE_WINGS_EVENT = pg.USEREVENT + 1

    
    def __init__(self, game, images, *groups):
        
        # logic
        self.game = game
        self.images = images
        self.image = images[1]
        self.rect = self.image.get_rect(center = Bird.CENTER)
        self._layer = Layer.CREATURE
        pg.time.set_timer(self.CYCLE_WINGS_EVENT, Bird.CYCLE_WINGS_TIME)
        
        super().__init__(groups)
        
        # physics
        moment = pymunk.moment_for_box(15, self.image.get_size())
        self.body = pymunk.Body(15, moment, body_type = pymunk.Body.DYNAMIC)
        self.body.position = self.rect.x, self.rect.y
        
        self.game.space.add(self.body)
        
    def update(self):
        self.rect.x, self.rect.y = self.body.position
        
        if not self.game.gameover:
            self.check_collition()
    
    def handle_event(self, event):
        if event.type == self.CYCLE_WINGS_EVENT:
            self.cycle_wings()
        
        elif event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            self.flap()
        
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
        
        if is_collided_with_base or is_collided_with_bounds or is_collided_with_pipe:
            self.fall()
            self.game.end_game()
            
    
    def fall(self):
        self.velocity = (0, 0)
        self.body.apply_impulse_at_local_point(Bird.DYING_IMPULSE)
