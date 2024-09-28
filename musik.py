import pygame
from pygame.locals import *
import sys
import random

import pygame.mixer
pygame.mixer.init()

pygame.init()
vec = pygame.math.Vector2 

screen_height = 500
screen_width = int(16 / 9 * screen_height)
acceleration = 2
friction = -0.25
fps = 60
gravity = 0.5
font_typ = pygame.font.SysFont("Comic Sans", 60)

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

death_sound = pygame.mixer.Sound('dark-souls-you-died-sound-effect_hm5sYFG.wav')

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((30, 30))
        self.surf = pygame.transform.scale(pygame.image.load('450.png').convert_alpha(), (30,30))
        #self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.dash_cooldown = 0
        self.dash_speed = 50
        self.grow = False

    def move(self):
        self.acc = vec(0,gravity)
    
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LSHIFT] and self.dash_cooldown <= 0:
                self.vel = self.vel.normalize() * self.dash_speed
                self.dash_cooldown = 250
                #P1.surf.fill((235, 12, 30))
                self.surf = pygame.transform.scale(pygame.image.load('ugandan-knuckles-orange-cartoon-character-illustration-png-clipart-thumbnail.png ').convert_alpha(), (30,30))

        if pressed_keys[K_t]:
            self.grow = not self.grow
                
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
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False

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
        self.surf = pygame.Surface((random.randint(50,100), 12))
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


for x in range(random.randint(35, 45)):
    pl = Platform()
    platforms.add(pl)
    all_sprites.add(pl)

platforms.add(PT1)

def plat_gen():
    while len(platforms) < 30:
        width = random.randrange(50,100)
        p  = Platform()             
        p.rect.center = (random.randrange(0, screen_width - width), random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)

def game_over():
        game_over_text = font_typ.render("GAME OVER", True, (255, 255, 255)) 
        game_over_asset = pygame.image.load('gameover_sanic.png')
        if P1.pos.y >= screen_height +10:
            death_sound.play()
            displaysurface.fill((0, 0, 0))
            displaysurface.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2, screen_height/3))
            displaysurface.blit(game_over_asset, (screen_width/2 - game_over_asset.get_width()/2, screen_height/1.8))
            pygame.display.update()
            pygame.time.delay(4800)  
            pygame.quit()
            sys.exit()

while True:
    P1.dash_cooldown -= 1
    if P1.dash_cooldown == 0:
        #P1.surf.fill((128,255,40))
        P1.surf = pygame.transform.scale(pygame.image.load('450.png').convert_alpha(), (30,30))

    if P1.grow:
        P1.surf = pygame.transform.scale(pygame.image.load('450.png').convert_alpha(), (P1.surf.get_width()+1,P1.surf.get_height()+1))
    else:
        #P1.surf = pygame.transform.scale(P1.surf, (P1.surf.get_width()- 1,P1.surf.get_height()-1))
        pass

    game_over()
    
    plat_gen()
    
    if P1.rect.top <= screen_height / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= screen_height:
                plat.kill()


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
            if event.key == pygame.K_q:
                gravity = 0.5 if gravity == 0.0 else 0.0
            if event.key == pygame.K_r:
                gravity = -gravity
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump() 
         
    P1.move()
    P1.update()

    if random.randint(0, 100) > 95 and len(platforms) > 1:
        index = random.randint(1, len(platforms)-1)
        platforms.sprites()[index].rect.midbottom = (0, 1000)
        platforms.remove(platforms.sprites()[index])

    displaysurface.fill((0,0,0))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(fps)
