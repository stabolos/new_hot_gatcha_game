import pygame
import copy

from pygame.locals import *


vec = pygame.math.Vector2 
screen_height = 500
screen_width = int(16 / 9 * screen_height)
dash_cooldown_sprite = "images/ugandan-knuckles-orange-cartoon-character-illustration-png-clipart-thumbnail.png"
player_sprite = "images/450.png"

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(player_sprite).convert_alpha(), (30,30))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect()
        self.gravity = 0.5
        self.counter_jump = 0
        self.counter_jump_max = 2
        self.counter_jump_max_static = 2
        self.acceleration = 2
        self.acc = vec(0,0)

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.jumping = False
        self.dash_cooldown = 0
        self.dash_speed = 25
        self.grow = False
        self.friction = -0.25
        self.rechts = False
        self.links = False
        self.speedlimit = vec(5,15)

    def move(self):
        self.acc = vec(0,self.gravity)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LSHIFT] and self.dash_cooldown <= 0:
                self.vel = self.vel.normalize() * self.dash_speed
                self.dash_cooldown = 250
                self.surf = pygame.transform.scale(pygame.image.load(dash_cooldown_sprite).convert_alpha(), (30,30))

        if pressed_keys[K_t]:
            self.grow = not self.grow
                
        if pressed_keys[K_a] and not self.links:
                self.acc.x = -self.acceleration
        if pressed_keys[K_d] and not self.rechts:
                self.acc.x = self.acceleration 
        
        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc

        if abs(self.vel[0]) > self.speedlimit[0]:
           self.vel[0] = self.vel[0]/abs(self.vel[0]) * self.speedlimit[0]

        if abs(self.vel[1]) > self.speedlimit[1]: 
           self.vel[1] = self.vel[1]/abs(self.vel[1]) * self.speedlimit[1]  

        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > screen_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screen_width
        

        self.rect.midbottom = self.pos
    
    def update(self, platforms, walls):
        sidewall = False
        pressed_keys = pygame.key.get_pressed()
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False  
                    self.counter_jump = 0   

        hits = pygame.sprite.spritecollide(self ,walls, False)        
        if hits:    
                if self.pos.y - self.rect.height / 2 < hits[0].rect.top and self.vel.y > 0:
                    collider_center = hits[0].rect.center
                    y_vorzeichen = self.vel.y / (abs(self.vel.y) if self.vel.y != 0 else 1) * -1 
                    self.pos.y = collider_center[1] + (( hits[0].rect.height / 2 ) * y_vorzeichen)  
                    self.jumping = False
                    self.counter_jump = 0
                    self.vel.y = min(self.vel.y, 0)

                elif self.pos.y > hits[0].rect.bottom and self.vel.y < 0:
                    collider_center = hits[0].rect.center
                    y_vorzeichen = self.vel.y / (abs(self.vel.y) if self.vel.y != 0 else 1) * -1 
                    self.pos.y = collider_center[1] + (( hits[0].rect.height / 2 ) + self.rect.height) 
                    self.vel.y = 0   

                else:
                    sidewall = True
                    collider_center = hits[0].rect.center
                    x_vorzeichen = self.vel.x / (abs(self.vel.x) if self.vel.x != 0 else 1) * -1 
                    self.pos.x = collider_center[0] + ((self.rect.width / 2 + hits[0].rect.width / 2 ) * x_vorzeichen)
                    self.vel.x = 0
                    self.counter_jump_max = self.counter_jump_max_static + 1

                    if pressed_keys[K_a] or pressed_keys[K_d]:
                        self.speedlimit[1] *= 0.925 
                        print(self.speedlimit)

                
                    if x_vorzeichen <= 0:
                         self.links = True
                    else:
                         self.rechts = True
        else:
             self.links = False
             self.rechts = False
        
        if sidewall == False or (not pressed_keys[K_a] and not pressed_keys[K_d]): 
            self.speedlimit[1] = 15

        if sidewall == False:
             self.counter_jump_max = self.counter_jump_max_static
        
        self.rect.midbottom = self.pos

    def jump(self, platforms, walls): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        player_copy = copy.copy(self)
        player_copy.rect.bottom += 10
        hits_w = pygame.sprite.spritecollide(player_copy, walls, False)
        del player_copy
        
        if hits or hits_w or self.counter_jump < self.counter_jump_max:
           self.jumping = True
           self.vel.y = -15
           self.counter_jump += 1
           self.speedlimit[1] = 15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def get_player_sprite(event=None):
        return player_sprite
    
    def dash_cooldown_tick(self):
        self.dash_cooldown -= 1
        if self.dash_cooldown == 0:
            self.surf = pygame.transform.scale(pygame.image.load(self.get_player_sprite() ).convert_alpha(), (30,30))

    