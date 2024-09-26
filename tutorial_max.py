import pygame
from pygame.locals import *
from pygame.sprite import _Group
import sys

pygame.init()
vec = pygame.math.Vector2 

screen_height = 450
screen_width = 400
acceleration = 0.5
friction = -0.12
fps = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 420))

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((screen_width, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (screen_width/2, screen_height - 10))

PT1 = Platform()
P1 = Player()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()