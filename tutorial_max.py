import pygame
from pygame.locals import *
import sys
import random

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
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False

    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_a]:
            self.acc.x = -acceleration
        if pressed_keys[K_d]:
            self.acc.x = acceleration 
        
        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > screen_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screen_width
        
        self.rect.midbottom = self.pos
    
    def update(self):
        hits = pygame.sprite.spritecollide(P1 , platforms, False)
        if hits:
            if P1.vel.y > 0:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15 

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(5,100), 12))
        self.surf.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        self.rect = self.surf.get_rect(center = (random.randint(0,screen_width-10),random.randint(0, screen_height-30)))

PT1 = Platform()
P1 = Player()
PT1.surf = pygame.Surface((screen_width, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (screen_width/2, screen_height - 10))

platforms = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

for x in range(random.randint(5, 50)):
    pl = Platform()
    platforms.add(pl)
    all_sprites.add(pl)


platforms.add(PT1)

while True:
    
    if P1.pos.y >= 450:
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    P1.move()
    P1.update()
    print(len(platforms))
    print(P1.pos.y)

    if random.randint(0, 100) > 95 and len(platforms) > 1:
        index = random.randint(1, len(platforms)-1)
        platforms.sprites()[index].rect.midbottom = (0, 1000)
        platforms.remove(platforms.sprites()[index])


    displaysurface.fill((0,0,0))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(fps)

