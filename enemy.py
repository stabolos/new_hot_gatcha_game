import pygame
from pygame.locals import *
import random
import pygame.mixer
pygame.mixer.init()

vec = pygame.math.Vector2 


displaysurface = pygame.display.set_mode((100, 100))

sound_on_kill = pygame.mixer.Sound('sounds/Greater_Bash.mp3')
sound_on_charge = pygame.mixer.Sound("sounds/Charge_of_Darkness_cast.mp3")


class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image):
        super().__init__()

        self.image = enemy_image
        self.rect = pygame.image.load((self.image)).get_rect()
        self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), (50,50))
        self.pos = vec(10, 335)
        self.vel = vec(0, 0)
        self.charging = 0
        self.growth_rate = vec(1,1)
        self.dash_speed = 10
        self.rect = self.surf.get_rect(center=self.pos)

    def move(self, player):
        direction = player.pos - self.pos

        if random.randint(1, 100) == 101:
            self.growth_rate *= 1.1
            self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), self.growth_rate)
        
        if direction.length() > 5:  
            if random.randint(1, 250) == 250:
                #sound_on_charge.play()
                self.charging = 13

            if  self.charging > 0:
                self.dash_speed += 1.2
                self.vel = direction.normalize() * self.dash_speed
                
                self.charging -= 1
            else:
                self.vel = direction.normalize() * random.randint(1,5)

        else:
            self.vel = vec(0, 0)  
        
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def kill_player(event = None):
        #sound_on_kill.play()
        pass

    def collide(self, walls):
        hits = pygame.sprite.spritecollide(self, walls, False)
        if hits:
            if self.pos.y - self.rect.height / 2 < hits[0].rect.top and self.vel.y > 0:
                collider_center = hits[0].rect.center
                y_vorzeichen = self.vel.y / (abs(self.vel.y) if self.vel.y != 0 else 1) * -1
                self.pos.y = collider_center[1] + ((hits[0].rect.height / 2) * y_vorzeichen)
                self.jumping = False
                self.counter_jump = 0
                self.vel.y = min(self.vel.y, 0)

            elif self.pos.y > hits[0].rect.bottom and self.vel.y < 0:
                collider_center = hits[0].rect.center
                self.pos.y = collider_center[1] + ((hits[0].rect.height / 2) + self.rect.height)
                self.vel.y = 0

            else:
                collider_center = hits[0].rect.center
                x_vorzeichen = self.vel.x / (abs(self.vel.x) if self.vel.x != 0 else 1) * -1
                self.pos.x = collider_center[0] + ((self.rect.width / 2 + hits[0].rect.width / 2) * x_vorzeichen)
                self.vel.x = 0
            self.rect.midbottom = self.pos


class GravityAffectedEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image):
        super().__init__()
        self.image = enemy_image
        self.rect = pygame.image.load((self.image)).get_rect()
        self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), (50, 50))
        self.pos = vec(10, 335)
        self.vel = vec(0, 0)
        self.charging = 0
        self.growth_rate = vec(1, 1)
        self.dash_speed = 10
        self.rect = self.surf.get_rect(center=self.pos)
        self.gravity = 1.0

    def move(self, player):
        self.acc = vec(0, self.gravity)
        direction = player.pos - self.pos

        if random.randint(1, 100) == 101:
            self.growth_rate *= 1.1
            self.surf = pygame.transform.scale(pygame.image.load(self.image).convert_alpha(), self.growth_rate)

        if direction.length() > 5:
            if random.randint(1, 250) == 250:
                # sound_on_charge.play()
                self.charging = 13

            if self.charging > 0:
                self.dash_speed += 1.2
                self.vel = [direction.normalize().x * self.dash_speed, 0]

                self.charging -= 1
            else:
                self.vel = ((direction.normalize() * random.randint(1, 5)).x , 0 )

        else:
            self.vel = vec(0, 0)
        self.vel += self.acc
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def kill_player(event=None):
        # sound_on_kill.play()
        pass

    def collide(self, walls):
        hits = pygame.sprite.spritecollide(self, walls, False)
        if hits:
            for hit in hits:
                if self.pos.y - self.rect.height / 2 < hit.rect.top and self.vel.y > 0:
                    collider_center = hit.rect.center
                    y_vorzeichen = self.vel.y / (abs(self.vel.y) if self.vel.y != 0 else 1) * -1
                    self.pos.y = collider_center[1] + ((hit.rect.height / 2) * y_vorzeichen)
                    self.jumping = False
                    self.counter_jump = 0
                    self.vel.y = min(self.vel.y, 0)

                elif self.pos.y > hit.rect.bottom and self.vel.y < 0:
                    collider_center = hit.rect.center
                    self.pos.y = collider_center[1] + ((hit.rect.height / 2) + self.rect.height)
                    self.vel.y = 0

                else:
                    collider_center = hit.rect.center
                    x_vorzeichen = self.vel.x / (abs(self.vel.x) if self.vel.x != 0 else 1) * -1
                    self.pos.x = collider_center[0] + ((self.rect.width / 2 + hit.rect.width / 2) * x_vorzeichen)
                    self.vel.x = 0
            self.rect.midbottom = self.pos


    

        