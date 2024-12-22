from utils import *
from config import *
from bullet import *
import time
import pygame
import math
import random

# Define enemy_bullet as a sprite group
enemy_bullet = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self,image_path="enemy.png"):
        super().__init__()

        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (enemy_size, enemy_size))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, width - enemy_size)
        self.rect.y = random.randint(0, height - enemy_size)

        self.speed = random.randint(2, 3)
        self.health = 10
        self.max_health = self.health
        self.damage = 5
        self.damage_cooldown = 2  # Cooldown in seconds
        self.last_damage_time = 0  # Last time damage was dealt
        self.coin_value = 10

    def update(self, player):
        direction = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
        self.rect.x += int(self.speed * math.cos(direction))
        self.rect.y += int(self.speed * math.sin(direction))

    def can_deal_damage(self):
        """
        Check if enough time has passed since the last damage was dealt.
        """
        current_time = time.time()
        return current_time - self.last_damage_time >= self.damage_cooldown

    def deal_damage(self, player):
        """
        Deal damage to the player if cooldown has passed.
        """
        if self.can_deal_damage():
            player.take_damage(self.damage)
            self.last_damage_time = time.time()



class fast_enemy(Enemy):
    def __init__(self, image_path="fast_enemy.png"):
        super().__init__(image_path)
        self.image = pygame.image.load(image_path).convert_alpha()

        fast_enemy_size = 50
        self.image = pygame.transform.scale(self.image, (fast_enemy_size, fast_enemy_size))
        self.rect = self.image.get_rect()

        #Random speed
        self.speed = random.randint(4, 5)
        #Health
        self.health = 5
        self.max_health = self.health
        #damage it deals
        self.damage = 3
        self.coin_value = 10


class shooter_rastreio(Enemy):
    def __init__(self,image_path="shooter_rastreio.png"):
        super().__init__(image_path)
        self.image = pygame.image.load(image_path).convert_alpha()


        fast_enemy_size = 50
        self.image = pygame.transform.scale(self.image, (fast_enemy_size, fast_enemy_size))
        self.rect = self.image.get_rect()

        self.health = 50
        self.max_health = self.health
        self.shoot_cooldown = 0
        self.coin_value = 20
        
    
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
       pass



        

        
    
    
        




