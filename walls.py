import pygame
from pygame.locals import *
from gameoptions import screendimensions

class Walls(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        screen = screendimensions()
        self.surf = pygame.Surface((0, 0))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (screen[0] - 10, screen[1] / 2))
