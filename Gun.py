import math
import pygame
from pygame.locals import *
import random
import pygame.mixer
from main import Player
pygame.mixer.init()

vec = pygame.math.Vector2



class Gun(pygame.sprite.Sprite):
    def __init__(self,gun_image,gun_type):
        super().__init__()

        self.gun_sound = pygame.mixer.Sound('sounds/guns/..')
        self.original_image = gun_image

        self.rect = pygame.image.load(self.image).get_rect()
        self.rect.center = vec(10,10)
        
    def gun_position(self,player):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        rel_x,rel_y = mouse_x - self.x, mouse_y - self.y

        angle = (180 /math.pi) * -math.atan2(rel_y,rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.position)
