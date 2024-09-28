import pygame
from pygame.locals import *
import random

import pygame.mixer
pygame.mixer.init()

vec = pygame.math.Vector2 


displaysurface = pygame.display.set_mode((100, 100))

chase_speed = 4
sound_on_kill = pygame.mixer.Sound('sounds/Greater_Bash.mp3')
sound_on_charge = pygame.mixer.Sound("sounds/Charge_of_Darkness_cast.mp3")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image):
        super().__init__()

        self.image = enemy_image
        self.rect = pygame.image.load((self.image)).get_rect()
        self.rect.center = vec(50,50)
        self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), (50,50))
        self.pos = vec(50, 50)  
        self.vel = vec(0, 0)

        self.rect = self.surf.get_rect(center=(50, 50))

    def move(self, player):
        direction = player.pos - self.pos
        
        if direction.length() > 5:  # Adjust the threshold as needed
            if random.randint(1, 100) != 100:
                self.vel = direction.normalize() * random.randint(1,5)
            else:
                self.vel = direction.normalize() * 35
                sound_on_charge.play()

        else:
            self.vel = vec(0, 0)  # Stop moving when close enough
        
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def kill_player(event = None):
        sound_on_kill.play()


    

        