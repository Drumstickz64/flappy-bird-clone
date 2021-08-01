import random
import sys

import pygame as pg
import pymunk

import objects
import settings
import resource

pg.init()


SCREEN = pg.display.set_mode(settings.SCREEN_SIZE, pg.SCALED)
SPACE = pymunk.Space()
SPACE.gravity = (0, 1600)


class FlappyBird:
    def __init__(self, screen, space, fps):
        self.screen = screen
        self.space = space
        self.fps = fps
        
        self._started = False
        self.running = False
        self.gameover = False
        
        self.score = 0
        self._dt = 1 / settings.FPS
        self.SPAWNPIPE = pg.USEREVENT
        
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.pipes = []
        
    def load_assets(self):
        self.bird_images = [
            resource.load_sprite("yellowbird-downflap.png"),
            resource.load_sprite("yellowbird-midflap.png"),
            resource.load_sprite("yellowbird-upflap.png"),
        ]
        
        self.background_image = resource.load_sprite("background-day.png")
        
        self.base_image = resource.load_sprite("base.png")
        
        self.pipe_image = resource.load_sprite("pipe-green.png")
        self.pipe_image_flipped = pg.transform.flip(self.pipe_image, False, True)
        
        self.start_message_image = resource.load_sprite("message.png")
        self.gameover_message_image = resource.load_sprite("gameover.png")
        
        self.font = resource.load_font("pixelmania.ttf", size = 84)
        
        self.wing_sound = resource.load_sound("wing")
        self.point_sound = resource.load_sound("point")
        self.hit_sound = resource.load_sound("hit")

    def init(self):
        self.running = True
        
        self._clock = pg.time.Clock()
        
        self.base = objects.Base(self.base_image, self.all_sprites)
        self.start_message = objects.StartMessage(self.start_message_image, self.all_sprites)
        self.score_message = objects.ScoreMessage(self.font, self.all_sprites)
        self.bird = objects.Bird(self, self.bird_images, self.all_sprites)
    
    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.running == False
        
        elif event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            self.handle_action_event()
        
        elif event.type == self.SPAWNPIPE and not self.gameover:
            self.spawn_pipe_pair()

        for sprite in self.all_sprites:
            try:
                sprite.handle_event(event)
            except AttributeError:
                pass
    
    def handle_action_event(self):
        '''Handles the "action event" which is when the user clicks or presses spacebar'''
        if self.gameover:
            self.running = False
            return
        
        if not self._started:
            self.start()
        
    def update(self):
        self.space.step(self._dt)
        self.all_sprites.update()
        
    
    def draw(self):
        self.all_sprites.clear(self.screen, self.background_image)
        dirty_rects = self.all_sprites.draw(self.screen)
        pg.display.update(dirty_rects)
        
    
    def quit(self):
        pg.quit()
        sys.exit()
        
        
    def draw_static_scenery(self):
        self.screen.blit(self.background_image, (0, 0))
        # self.base.draw(self.screen)
        pg.display.flip()
        
        
    def spawn_pipe_pair(self):
        pipe_x = settings.SCREEN_WIDTH

        first_pipe_y = random.randint(objects.Pipe.GAP, settings.SCREEN_HEIGHT - objects.Pipe.GAP)
        first_pipe = objects.Pipe(
            self,
            self.pipe_image,
            self.all_sprites,
            primary = True,
            topleft = (pipe_x, first_pipe_y)
        )
        self.pipes.append(first_pipe)
        
        second_pipe_y = first_pipe_y - objects.Pipe.GAP
        second_pipe = objects.Pipe(
            self,
            self.pipe_image_flipped,
            self.all_sprites,
            primary = False,
            bottomleft = (pipe_x, second_pipe_y)
        )
        self.pipes.append(second_pipe)
    
    def increment_score(self):
        self.score += 1
        self.score_message.update_score(self.score)
    
    
    def run(self):
        self.load_assets()
        self.init()
        self.draw_static_scenery()
        
        while self.running:
            for event in pg.event.get():
                self.handle_event(event)
                
            if self._started:
                self.update()
                
            self.draw()
            
            self._clock.tick(self.fps)
        
        self.quit()
        
    def start(self):
        self.start_message.kill()
        
        pg.time.set_timer(self.SPAWNPIPE, objects.Pipe.SPAWN_TIME)
        
        self._started = True
    
    
    def end_game(self):
        self.gameover = True
        
        self.hit_sound.play()
        
        gameover_message = objects.GameoverMessage(self.gameover_message_image)
        self.all_sprites.add(gameover_message)
        
        


if __name__ == "__main__":
    FlappyBird(SCREEN, SPACE, settings.FPS).run()
