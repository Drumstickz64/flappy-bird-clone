import pygame as pg
import os, platform


SOUND_FILE_EXT = ".wav" if platform.system() == "Windows" else ".ogg"


def load_sprite(sprite):
    return pg.image.load(os.path.join("assets", "sprites", sprite)).convert_alpha()
    

def load_sound(sound_name):
    return pg.mixer.Sound(os.path.join("assets", "audio", sound_name + SOUND_FILE_EXT))
    
    
def load_font(font, size):
    return pg.font.Font(os.path.join("assets", "fonts", font), size)