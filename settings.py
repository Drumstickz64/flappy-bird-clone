import pygame as pg
import pymunk


SCREEN_SIZE = (576, 1024)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
FPS = 60

LAYERS = {
    "background": 0,
    "foreground": 1,
    "ui": 2
}