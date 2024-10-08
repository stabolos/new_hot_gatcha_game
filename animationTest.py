import pygame
from pygame.locals import *
import sys
import random
from player import Player
from enemy import Enemy
from Animations import Animator
from Animations import AnimationStateMachine

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





#
# playerrunning = 1
#
condtitionDict = {1: False}

machine = AnimationStateMachine(0, Animator(), condtitionDict)



idlestate = AnimationStateMachine.AnimationState("images/Player/Idle/", 60 , "Idle")
runningstate = AnimationStateMachine.AnimationState("images/Player/running/", 60 , "running")
jumpstate = AnimationStateMachine.AnimationState("images/Player/jump/", 40 , "jump")
landstate = AnimationStateMachine.AnimationState("images/Player/land/", 40 , "land")

idleToRunning = AnimationStateMachine.AnimationEdge(0, 1, "StartRunning")
idleToJumping = AnimationStateMachine.AnimationEdge(0, 2, "Jumping")
runningToJumping = AnimationStateMachine.AnimationEdge(1, 2, "Jumping")
runningToIdle = AnimationStateMachine.AnimationEdge(1, 0, "StopRunning", [[1, False]])
jumpingToLanding = AnimationStateMachine.AnimationEdge(2, 3, None)
landingToIdle = AnimationStateMachine.AnimationEdge(3, 0, None)
landingToRunning = AnimationStateMachine.AnimationEdge(3, 1, None, [[1, True]])


machine.addState(idlestate)
machine.addState(runningstate)
machine.addState(jumpstate)
machine.addState(landstate)

machine.addEdge(idleToRunning)
machine.addEdge(idleToJumping)
machine.addEdge(runningToJumping)
machine.addEdge(runningToIdle)
machine.addEdge(jumpingToLanding)
machine.addEdge(landingToIdle)
machine.addEdge(landingToRunning)

machine.setup()

all_sprites = pygame.sprite.Group()
all_sprites.add(machine.animator)


def game_over():
        displaysurface.fill((0, 0, 0))
        displaysurface.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2, screen_height/3))
        displaysurface.blit(game_over_asset, (screen_width/2 - game_over_asset.get_width()/2, screen_height/1.8))
        pygame.display.update()
        pygame.time.delay(1200)  
        pygame.quit()
        sys.exit()


#machine.tick()
#machine.fireTrigger("Trig1")

while True:

    #machine.fireTrigger("Trig1")

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_a:
                condtitionDict[1] = True
                machine.fireTrigger("StartRunning")
                pass
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                machine.fireTrigger("Jumping")
                pass
            if event.key == pygame.K_a:
                condtitionDict[1] = False
                machine.fireTrigger("StopRunning")
                print("StopRunningaaaa")
                pass

    machine.tick()

    displaysurface.fill((0,0,0))
    #animator.tickAnim()

    for entity in all_sprites:
        #displaysurface.blit(entity.surf, entity.rect.move(-P1.rect.x + screen_width / 2, -P1.rect.y + screen_height / 2))
        displaysurface.blit(entity.surf,entity.rect)
    pygame.display.update()
    FramePerSec.tick(fps)
    game_time += 1
