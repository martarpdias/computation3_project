from utils import *
from config import *
from bullet import *
import pygame
import math
import random

# Define enemy_bullet as a sprite group
enemy_bullet = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the enemy instance
        """
        super().__init__()
        #setting up the surface and rectangle of the enemy
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()

        #Positioning
        self.rect.x = random.randint(0, width - enemy_size)
        self.rect.y = random.randint(0, height - enemy_size)
        #Random speed
        self.speed = random.randint(1, 2)
        #Health
        self.health=5
        self.max_health = self.health
        #damage it deals
        self.damage = 5

    def update(self,player):
        """
        Update the enemy´s position according to the player´s.

        Args
        ---
        player (Player)
            The player to move towards
        """

        #Calculation the direction in which the player is (angle)
        direction=math.atan2(
            player.rect.y - self.rect.y, player.rect.x - self.rect.x)

        #coordinate update
        self.rect.x += int(self.speed * math.cos(direction))
        self.rect.y += int(self.speed * math.sin(direction))

        self.rect.x =int(self.rect.x)
        self.rect.y =int(self.rect.y)

'''class fast_enemy(Enemy):
    def __init__(self):
        """
        Initialize the enemy instance
        """
        super().__init__()
        #change the appearence
        self.image.fill(blue)

        #Random speed
        self.speed = random.randint(4, 5)
        #Health
        self.health = 10
        #damage it deals
        self.damage = 5

class shooter_rastreio(Enemy):
    def __init__(self):
        super().__init__()
        self.image.fill(pink)
        self.health = 50
        self.max_health = self.health
        self.shoot_cooldown = 0
        
    
    def shoot(self,enemy_bullet, player):
        direction = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
        # Check if cooldown is ready
        if self.shoot_cooldown <= 0:
            # Create and shoot a bullet
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
            enemy_bullet.add(bullet)
            
            # Reset cooldown to fps (1 second)
            self.shoot_cooldown = fps
        else:
            # Decrease cooldown
            self.shoot_cooldown -= 1
            
    
    def update(self, player):
       pass'''
    
        




