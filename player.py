import pygame
from pygame.locals import *


vec = pygame.math.Vector2 
screen_height = 500
screen_width = int(16 / 9 * screen_height)

dash_cooldown_sprite = "images/ugandan-knuckles-orange-cartoon-character-illustration-png-clipart-thumbnail.png"
player_sprite = "images/450.png"

class Player(pygame.sprite.Sprite):

    def __init__(self, gravity, friction):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(player_sprite).convert_alpha(), (30,30))
        self.rect = self.surf.get_rect()
        self.gravity = gravity

        self.acceleration = 2
        self.acc = vec(0,0)

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.jumping = False
        self.dash_cooldown = 0
        self.dash_speed = 50
        self.grow = False
        self.friction = friction

    def move(self):
        self.acc = vec(0,self.gravity)
    
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LSHIFT] and self.dash_cooldown <= 0:
                self.vel = self.vel.normalize() * self.dash_speed
                self.dash_cooldown = 250
                self.surf = pygame.transform.scale(pygame.image.load(dash_cooldown_sprite).convert_alpha(), (30,30))

        if pressed_keys[K_t]:
            self.grow = not self.grow
                
        if pressed_keys[K_a]:
                self.acc.x = -self.acceleration
        if pressed_keys[K_d]:
                self.acc.x = self.acceleration 
        
        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > screen_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screen_width
        
        self.rect.midbottom = self.pos
    
    def update(self, platforms, enemy):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False


    def jump(self, platforms): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def get_player_sprite(event=None):
        return player_sprite