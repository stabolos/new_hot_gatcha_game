import pygame
from pygame.locals import *
import sys
from player import Player
from walls import Walls
from platform_1 import Platform
from gameoptions import screendimensions
import pygame.mixer
from jsonLoader import jsonL
from enemy import *
pygame.mixer.init()
 
pygame.init()
vec = pygame.math.Vector2 
screen = screendimensions()
screen_height = screen[1]
screen_width = screen[0]
fps = 60
font_typ = pygame.font.SysFont("Comic Sans", 60)
game_time = 0
FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

death_sound = pygame.mixer.Sound('sounds/dark-souls-you-died-sound-effect_hm5sYFG.wav')

jL = jsonL()
platforms_from_json = jL.getPlatforms()

P1 = Player()


all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
npcs = pygame.sprite.Group()
enemy = GravityAffectedEnemy("images/download_2.png")
npcs.add(enemy)
all_sprites.add(enemy)
all_sprites.add(P1)

for wall in platforms_from_json:
    wall = Walls(wall["dimension"], wall["position"], wall["color"])
    walls.add(wall)
    all_sprites.add(wall)


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

    P1.dash_cooldown_tick()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump(walls)
            if event.key == pygame.K_q:
                P1.gravity = 0.5 if P1.gravity == 0.0 else 0.0
            if event.key == pygame.K_r:
                P1.gravity = -P1.gravity
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump() 

    P1.move()
    enemy.move(P1)

    P1.update(walls)
    for npc in npcs:
        npc.collide(walls)

    displaysurface.fill((0,0,0))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect.move(-P1.rect.x + screen_width / 2, -P1.rect.y + screen_height / 2))
 
    pygame.display.update()

    FramePerSec.tick(fps)
    game_time += 1
