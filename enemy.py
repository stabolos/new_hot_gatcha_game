import pygame
from pygame.locals import *
import random


import pygame.mixer
pygame.mixer.init()

vec = pygame.math.Vector2 


displaysurface = pygame.display.set_mode((100, 100))

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
        self.charging = 0
        self.growth_rate = 1.1
        self.dash_speed = 5
        self.size = vec(50,50)

        self.rect = self.surf.get_rect(center=(50, 50))

    def move(self, player):
        direction = player.pos - self.pos

        if random.randint(1, 100) == 100:
            self.size *= self.growth_rate
            self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), self.size )
            print(self.size )
            self.rect.inflate(self.size[0] , self.size[1])
            
            
        if direction.length() > 5:  
            if random.randint(1, 250) == 250:
                sound_on_charge.play()
                sound_on_charge.set_volume(0.1)
                self.charging = 13

            if  self.charging > 0:
                self.dash_speed += 1.2
                self.vel = direction.normalize() * self.dash_speed 
                
                self.charging -= 1
            else:
                self.vel = direction.normalize() * random.randint(1,1)

        else:
            self.vel = vec(0, 0)  
        
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def kill_player(event = None):
        sound_on_kill.play()
        sound_on_kill.set_volume(0.1)
        


    

        