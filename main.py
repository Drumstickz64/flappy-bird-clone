import pygame as pg
import pymunk
import sys
import random
from settings import SCREEN_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from utils import load_sprite, load_sound, load_font
from objects import Base, Bird, Pipe, ScoreMessage, StartMessage, GameoverMessage


pg.init()


SCREEN = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
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
        self._dt = 1 / fps
        self.SPAWNPIPE = pg.USEREVENT
        self.CYCLE_WINGS = pg.USEREVENT + 1
        
        self.objects = pg.sprite.LayeredUpdates()
        self.pipes = []
        
    
    def init(self):
        self.running = True
        
        self._clock = pg.time.Clock()
        
        self.base = Base(self.base_image)
        
        self.start_message = StartMessage(self.start_message_image)
        self.objects.add(self.start_message)
        
        self.score_message = ScoreMessage(self.font)
        self.objects.add(self.score_message)
        
        self.bird = Bird(self, self.bird_images)
        self.objects.add(self.bird)
        
        pg.time.set_timer(self.CYCLE_WINGS, Bird.CYCLE_WINGS_TIME)
        
    
    def load_assets(self):
        self.bird_images = [
            load_sprite("yellowbird-downflap.png"),
            load_sprite("yellowbird-midflap.png"),
            load_sprite("yellowbird-upflap.png"),
        ]
        
        self.background_image = load_sprite("background-day.png")
        
        self.base_image = load_sprite("base.png")
        
        self.pipe_image = load_sprite("pipe-green.png")
        self.pipe_image_flipped = pg.transform.flip(self.pipe_image, False, True)
        
        self.start_message_image = load_sprite("message.png")
        self.gameover_message_image = load_sprite("gameover.png")
        
        self.font = load_font("pixelmania.ttf", size = 84)
        
        self.wing_sound = load_sound("wing")
        self.point_sound = load_sound("point")
        self.hit_sound = load_sound("hit")
        
    
    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.running == False
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.gameover:
                self.running = False
                return
            
            if not self._started:
                self.start()
            
            self.bird.flap()
        
        elif event.type == self.SPAWNPIPE and not self.gameover:
            self.spawn_pipe_pair()
        
        elif event.type == self.CYCLE_WINGS:
            self.bird.cycle_wings()
        
    
    def update(self):
        self.space.step(self._dt)
        self.objects.update()
        
    
    def draw(self):
        self.objects.clear(self.screen, self.background_image)
        
        dirty_rects = self.objects.draw(self.screen)
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
        first_pipe_y = random.randint(Pipe.GAP, SCREEN_HEIGHT - Pipe.GAP)
        second_pipe_y = first_pipe_y - Pipe.GAP
        
        first_pipe = Pipe(self, self.pipe_image, primary = True, topleft = (SCREEN_WIDTH, first_pipe_y))
        self.pipes.append(first_pipe)
        self.objects.add(first_pipe)
        
        second_pipe = Pipe(self, self.pipe_image_flipped, primary = False, bottomleft = (SCREEN_WIDTH, second_pipe_y))
        self.pipes.append(second_pipe)
        self.objects.add(second_pipe)
        
        
    
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
            
            self._clock.tick(FPS)
        
        self.quit()
        
    def start(self):
        self.objects.remove(self.start_message)
        self.start_message.kill()
        
        pg.time.set_timer(self.SPAWNPIPE, Pipe.SPAWN_TIME)
        
        self._started = True
    
    
    def end_game(self):
        self.gameover = True
        
        self.bird.die()
        self.hit_sound.play()
        
        gameover_message = GameoverMessage(self.gameover_message_image)
        self.objects.add(gameover_message)
        
        


if __name__ == "__main__":
    FlappyBird(SCREEN, SPACE, FPS).run()