from config import *
import pygame
import math
from bullet import Bullet
import time
from enemy import Enemy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the player instance
        """
        super().__init__()
        self.image = pygame.Surface(player_size)
        self.image.fill(blue)
        self.rect=self.image.get_rect()
        self.rect.center=(width//2,height//2)


        #Gameplay variables
        self.speed=5
        self.health=100
        self.bullet_cooldown=0
        self.invincible = False  # To handle invincibility
        self.active_power_up = None  # Currently active power-up
        self.invincibility_cooldown = 1 #invincibility of 1 second
        self.last_hit_time = time.time() # Time of the last hit

    def update(self):
        """
        Update the +position of the player based on keyboard input
        """
        keys=pygame.key.get_pressed()
        #Moving upwards
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top>0:
            self.rect.y-= self.speed
        #Moving downwards
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom<height:
            self.rect.y+= self.speed
        #Moving left
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left>0:
            self.rect.x-= self.speed
        #Moving right
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right<width:
            self.rect.x+= self.speed


    def shoot(self,bullets:pygame.sprite.Group):
        """
        Shoot bullets in 4 directions depending om«n cooldown.

        Args
        ---
        bullets (pygame.sprite.Group)
            The bullet group that we will add the news ones to
        ---
        """
        if self.bullet_cooldown<=0:
            for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
                bullet=Bullet(
                    self.rect.center[0],self.rect.center[1], angle
                )
                bullets.add(bullet)
            self.bullet_cooldown=fps #frames until the next shot
        self.bullet_cooldown -=1

    def take_damage(self, damage):
        '''
        give the player invincibility for a short period of time to avoid instantly diying
        '''
        current_time = time.time()
        if current_time - self.last_hit_time >= self.invincibility_cooldown:
            self.health -= damage
            self.last_hit_time = current_time





