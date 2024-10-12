import pygame 
from pygame.locals import *
import random
from gameoptions import screendimensions

screen = screendimensions()

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        self.rect = self.surf.get_rect(center = (random.randint(0,screen[0]-10),random.randint(0, screen[1]-30)))