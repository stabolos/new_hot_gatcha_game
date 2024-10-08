import pygame
from pygame.locals import *
import sys
import random
from player import Player


import pygame.mixer
pygame.mixer.init()

pygame.init()
vec = pygame.math.Vector2 

screen_height = 500
screen_width = int(16 / 9 * screen_height)
friction = -0.25
fps = 60
gravity = 0.5
font_typ = pygame.font.SysFont("Comic Sans", 60)
game_time = 0



FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

death_sound = pygame.mixer.Sound('sounds/dark-souls-you-died-sound-effect_hm5sYFG.wav')


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        self.rect = self.surf.get_rect(center = (random.randint(0,screen_width-10),random.randint(0, screen_height-30)))

PT1 = Platform()
P1 = Player(gravity, friction)
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
        game_over_asset = pygame.image.load('images/gameover_sanic.png')
    
        death_sound.play()
        displaysurface.fill((0, 0, 0))
        displaysurface.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2, screen_height/3))
        displaysurface.blit(game_over_asset, (screen_width/2 - game_over_asset.get_width()/2, screen_height/1.8))
        pygame.display.update()
        pygame.time.delay(1200)  
        pygame.quit()
        sys.exit()

while True:



    P1.dash_cooldown -= 1
    if P1.dash_cooldown == 0:
        P1.surf = pygame.transform.scale(pygame.image.load(P1.get_player_sprite() ).convert_alpha(), (30,30))

    if P1.grow:
        P1.surf = pygame.transform.scale(pygame.image.load(P1.get_player_sprite()).convert_alpha(), (P1.surf.get_width()+1,P1.surf.get_height()+1))
    else:
        #P1.surf = pygame.transform.scale(P1.surf, (P1.surf.get_width()- 1,P1.surf.get_height()-1))
        pass

    if P1.pos.y >= screen_height +10:
        game_over()

    
    plat_gen()
    


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump(platforms)
            if event.key == pygame.K_q:
                P1.gravity = 0.5 if P1.gravity == 0.0 else 0.0
            if event.key == pygame.K_r:
                P1.gravity = -P1.gravity
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump() 
         
    P1.move()
    P1.update(platforms)



    displaysurface.fill((0,0,0))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect.move(-P1.rect.x + screen_width / 2, -P1.rect.y + screen_height / 2))
        #displaysurface.blit(entity.surf,entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(fps)
    game_time += 1
