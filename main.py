import pygame
from pygame.locals import *
import sys
import random
from player import Player
# from enemy import Enemy
from walls import Walls

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

# enemy = Enemy("images/download_2.png")

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

W1 = Walls(10, 20)
W1.surf = pygame.Surface((20, screen_height))
W1.surf.fill((255,0,0))
W1.rect = W1.surf.get_rect(center = (screen_width /2, screen_height / 2))

W2 = Walls(10, 20)
W2.surf = pygame.Surface((100, 50))
W2.surf.fill((255,0,0))
W2.rect = W2.surf.get_rect(center = (100, screen_height - 80))

platforms = pygame.sprite.Group()
walls = pygame.sprite.Group()
walls.add(W1)
walls.add(W2)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
all_sprites.add(W1)
all_sprites.add(W2)

# all_sprites.add(enemy)


# for x in range(random.randint(35, 45)):
#     pl = Platform()
#     platforms.add(pl)
#     all_sprites.add(pl)

platforms.add(PT1)

def game_over():
        game_over_text = font_typ.render("GAME OVER", True, (255, 255, 255)) 
        game_over_asset = pygame.image.load('images/gameover_sanic.png')
        pygame.mixer.music.stop()
        death_sound.play()
        displaysurface.fill((0, 0, 0))
        displaysurface.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2, screen_height/3))
        displaysurface.blit(game_over_asset, (screen_width/2 - game_over_asset.get_width()/2, screen_height/1.8))
        pygame.display.update()
        pygame.time.delay(1200)  
        pygame.quit()
        sys.exit()

# pygame.mixer.music.load('sounds/Ambient_Music.mp3')
# pygame.mixer.music.play(True,)
# pygame.mixer.music.set_volume(1)

while True:

    
    # if len(pygame.sprite.spritecollide(P1, [enemy], False)) == 1 and game_time >= 1:
    #     enemy.kill_player()

    # print(pygame.sprite.spritecollide(P1, [enemy], False))
    # enemy.move(P1)

    P1.dash_cooldown -= 1
    if P1.dash_cooldown == 0:
        P1.surf = pygame.transform.scale(pygame.image.load(P1.get_player_sprite() ).convert_alpha(), (30,30))

    if P1.grow:
        P1.surf = pygame.transform.scale(pygame.image.load(P1.get_player_sprite()).convert_alpha(), (P1.surf.get_width()+1,P1.surf.get_height()+1))
    else:
        #P1.surf = pygame.transform.scale(P1.surf, (P1.surf.get_width()- 1,P1.surf.get_height()-1))
        pass

    if P1.pos.y >= screen_height +10:
        # game_over()
        pass

    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump(platforms, walls)
            if event.key == pygame.K_q:
                P1.gravity = 0.5 if P1.gravity == 0.0 else 0.0
            if event.key == pygame.K_r:
                P1.gravity = -P1.gravity
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump() 

    P1.move()
    P1.update(platforms, walls)
   

    if random.randint(0, 100) > 95 and len(platforms) > 1:
        index = random.randint(1, len(platforms)-1)
        # platforms.sprites()[index].rect.midbottom = (0, 1000)
        # platforms.remove(platforms.sprites()[index])

    displaysurface.fill((0,0,0))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect.move(-P1.rect.x + screen_width / 2, -P1.rect.y + screen_height / 2))
        
 
    pygame.display.update()

    FramePerSec.tick(fps)
    game_time += 1
