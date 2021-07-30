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
        self.fps = settings.FPS
        
        self._started = False
        self.running = False
        self.gameover = False
        
        self.score = 0
        self._dt = 1 / settings.FPS
        self.SPAWNPIPE = pg.USEREVENT
        self.CYCLE_WINGS = pg.USEREVENT + 1
        
        self.rendering_group = pg.sprite.LayeredUpdates()
        self.pipes = []
        
    
    def init(self):
        self.running = True
        
        self._clock = pg.time.Clock()
        
        self.base = objects.Base(self.base_image)
        
        self.start_message = objects.StartMessage(self.start_message_image)
        self.rendering_group.add(self.start_message)
        
        self.score_message = objects.ScoreMessage(self.font)
        self.rendering_group.add(self.score_message)
        
        self.bird = objects.Bird(self, self.bird_images)
        self.rendering_group.add(self.bird)
        
        pg.time.set_timer(self.CYCLE_WINGS, objects.Bird.CYCLE_WINGS_TIME)
        
    
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
        
    
    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.running == False
        
        elif event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            self.handle_action_event()
        
        elif event.type == self.SPAWNPIPE and not self.gameover:
            self.spawn_pipe_pair()
        
        elif event.type == self.CYCLE_WINGS:
            self.bird.cycle_wings()
    
    def handle_action_event(self):
        '''Handles the "action event" which is when the user clicks or presses spacebar'''
        if self.gameover:
            self.running = False
            return
        
        if not self._started:
            self.start()
        
        self.bird.flap()
    
    def update(self):
        self.space.step(self._dt)
        self.rendering_group.update()
        
    
    def draw(self):
        self.rendering_group.clear(self.screen, self.background_image)
        
        dirty_rects = self.rendering_group.draw(self.screen)
        self.base.draw(self.screen)
        
        pg.display.update(dirty_rects)
        
    
    def quit(self):
        pg.quit()
        sys.exit()
        
        
    def draw_static_scenery(self):
        self.screen.blit(self.background_image, (0, 0))
        self.base.draw(self.screen)
        pg.display.flip()
        
        
    def spawn_pipe_pair(self):
        first_pipe_y = random.randint(objects.Pipe.GAP, settings.SCREEN_HEIGHT - objects.Pipe.GAP)
        second_pipe_y = first_pipe_y - objects.Pipe.GAP
        
        first_pipe = objects.Pipe(self, self.pipe_image, primary = True, topleft = (settings.SCREEN_WIDTH, first_pipe_y))
        self.pipes.append(first_pipe)
        self.rendering_group.add(first_pipe)
        
        second_pipe = objects.Pipe(self, self.pipe_image_flipped, primary = False, bottomleft = (settings.SCREEN_WIDTH, second_pipe_y))
        self.pipes.append(second_pipe)
        self.rendering_group.add(second_pipe)
        
        
    
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
        
        self.bird.die()
        self.hit_sound.play()
        
        gameover_message = objects.GameoverMessage(self.gameover_message_image)
        self.rendering_group.add(gameover_message)
        
        


if __name__ == "__main__":
    FlappyBird(SCREEN, SPACE, settings.FPS).run()
