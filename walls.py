import pygame
from pygame.locals import *
from gameoptions import screendimensions

class Walls(pygame.sprite.Sprite):
    def __init__(self, dimensions, position, color):
        super().__init__()
        screen = screendimensions()
        self.surf = pygame.Surface(dimensions)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = position)
