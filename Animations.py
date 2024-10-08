import pygame
from pygame.locals import *
import sys



class Animator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        vec = pygame.math.Vector2
        screen_height = 500
        screen_width = int(16 / 9 * screen_height)
        self.animationFrameCount = 60
        self.animationPath = "images/Player/Idle/"
        self.image = self.animationPath + "0000.png"
        self.surf = pygame.Surface((64, 64))
        self.rect = pygame.image.load((self.image)).get_rect()
        self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), (50, 50))
        self.pos = vec(50, 50)
        self.rect = self.surf.get_rect(center=(screen_width * 0.5, screen_height * 0.5))
    def tickAnim(self, animationFrame):
        self.zeros = (4 - len(str(abs(animationFrame)))) * "0"
        self.image = self.animationPath + self.zeros + str(animationFrame) + ".png"
        self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), (50, 50))
        pass


class AnimationStateMachine:
    class AnimationState:
        def __init__(self, animation, uptime, name):
            self.uptime = uptime
            self.automaticEdge = None
            self.triggerEdges = []
            self.conditionEdges = []
            self.animation = animation
            self.name = name

    class AnimationEdge:
        def __init__(self, stateStart, stateEnd, trigger, conditions = [], partialConditionMatchesAllowed = False):
            self.stateStart = stateStart
            self.stateEnd = stateEnd
            self.trigger = trigger
            self.conditions = conditions
            self.partialConditionMatchesAllowed = partialConditionMatchesAllowed


    def __init__(self, startState, animator, conditionDict = {}):
        self.animator = animator
        self.tickCounter = 0
        self.state = startState
        self.states = []
        self.edges = []
        self.conditionDict = conditionDict

    def setup(self):
        self.animator.animationPath = self.states[self.state].animation

    def addState(self, animationState):
        self.states.append(animationState)

    def addEdge(self, animationEdge):
        self.edges.append(animationEdge)
        self.edgeIndex = len(self.edges) - 1
        self.edgeStartState = self.states[animationEdge.stateStart]
        hasTrigger = (animationEdge.trigger != None)
        hasConditions = (animationEdge.conditions != [])
        if(hasTrigger):
            self.edgeStartState.triggerEdges.append([animationEdge.trigger, self.edgeIndex])
        if (hasConditions):
            for condition in animationEdge.conditions:
                self.edgeStartState.conditionEdges.append(animationEdge)
        if(hasTrigger == False and hasConditions == False):
            self.edgeStartState.automaticEdge = self.edgeIndex

    def tick(self):
        self.tickCounter += 1
        currentAnimationState = self.states[self.state]
        if(self.tickCounter >= currentAnimationState.uptime):
            if(False == self.passAnimationCondition(currentAnimationState)):
                self.passAnimationAuto(currentAnimationState)
            self.tickCounter = 0
        self.animator.animationPath = currentAnimationState.animation
        self.animator.tickAnim(self.tickCounter)

    def passAnimationCondition(self, currentAnimationState):
        if (currentAnimationState.conditionEdges != []):
            for conditionEdge in currentAnimationState.conditionEdges:
                if (conditionEdge.partialConditionMatchesAllowed):
                    for condition in conditionEdge.conditions:
                        if (condition[1] == self.conditionDict[condition[0]]):
                            self.state = conditionEdge.stateEnd
                            return True
                            break
                else:
                    for condition in conditionEdge.conditions:
                        print(condition[1])
                        print("#####")
                        print(self.conditionDict[condition[0]])
                        if (condition[1] != self.conditionDict[condition[0]]):
                            return False
                    self.state = conditionEdge.stateEnd
                    return True
        return False

    def passAnimationAuto(self, currentAnimationState):
        if (currentAnimationState.automaticEdge != None):
            self.state = self.edges[currentAnimationState.automaticEdge].stateEnd

    def fireTrigger(self, trigger):
        for stateTrig in self.states[self.state].triggerEdges:
            if(stateTrig[0]) == trigger:
                self.state = self.edges[stateTrig[1]].stateEnd
                self.tickCounter = 0

