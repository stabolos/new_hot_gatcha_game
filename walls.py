import pygame
from pygame.locals import *

screen_height = 500
screen_width = int(16 / 9 * screen_height)

class Walls(pygame.sprite.Sprite):
    def __init__(self, height, width):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (screen_width - 10, screen_height / 2))

# W1 = Walls(10, 20)
# W1.surf = pygame.Surface((screen_width, 20))
# W1.surf.fill((255,0,0))
# W1.rect = W1.surf.get_rect(center = (screen_width - 10, screen_height / 2))

# platforms = pygame.sprite.Group()