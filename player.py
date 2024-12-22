from config import *
import pygame
import math
import time
from bullet import *
import time
from enemy import Enemy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the player instance
        """
        #super().__init__()
        #self.image = pygame.Surface(player_size)
        #self.image.fill(blue)
        #self.rect=self.image.get_rect()
        #self.rect.center=(width//2,height//2)

        super().__init__()
        # Upload the image of the player
        self.image = pygame.image.load("player_picture.png").convert_alpha()

        # Resize the image
        player_width, player_height = 75, 75  # new size
        self.image = pygame.transform.scale(self.image, (player_width, player_height))

        # Define the rectangle of the image
        self.rect = self.image.get_rect()

        # Puts the player in the center of the screen
        self.rect.center = (width // 2, height // 2)



        #Gameplay variables
        self.normal_speed = 5
        self.speed = self.normal_speed
        self.max_health = 100
        self.health = self.max_health
        self.bullet_cooldown = 0
        self.invincible = False  # To handle invincibility
        self.active_power_up = None  # Currently active power-up
        self.invincibility_cooldown = 1 #invincibility of 1 second
        self.invincibility_time = None
        self.last_hit_time = time.time() # Time of the last hit
        self.boost_start_time = None  # Time when the boost started to track the duration
        self.boost_duration = 15000  # Duration of the boost in milliseconds
        self.rifle_fire_rate = 15
        self.pistol_fire_rate = 30
        self.shotgun_fire_rate = 60
        self.RPG_fire_rate = 90
        self.fire_rate_timer = None
        self.coins = 0


        #guns avaliable to the player
        self.guns = {
            "pistol": {"unlocked": True, "bullet_type" : 1},
            "rifle" : {"unlocked": False, "bullet_type" : 2},
            "shotgun" : {"unlocked": False, "bullet_type" : 3},
            "RPG" : {"unlocked": False, "bullet_type" : 4}
        }
        self.current_gun = "pistol" #starting weapon

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
        if self.current_gun == "shotgun":
            fire_rate = self.shotgun_fire_rate
        elif self.current_gun == "pistol":
            fire_rate = self.pistol_fire_rate
        elif self.current_gun == "rifle":
            fire_rate = self.rifle_fire_rate
        elif self.current_gun == "RPG":
            fire_rate = self.RPG_fire_rate
        if self.bullet_cooldown<=0:
            bullet_type = self.guns[self.current_gun]["bullet_type"]
            for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
                if bullet_type == 1:
                    bullet = Bullet(self.rect.center[0], self.rect.center[1], angle)
                elif bullet_type == 2:
                    bullet = FastBullet(self.rect.center[0], self.rect.center[1], angle)
                elif bullet_type == 3:
                    bullet = LargeBullet(self.rect.center[0], self.rect.center[1], angle)
                elif bullet_type == 4:
                    bullet = RPG_rocket(self.rect.center[0], self.rect.center[1], angle)
                bullets.add(bullet)
            self.bullet_cooldown = fire_rate
        self.bullet_cooldown -=1

    def take_damage(self, damage):
        if not self.invincible:
            self.health -= damage
            self.health = max(0, self.health)  # Prevent health from going below zero

        #making sure the player doesn't take damage if it's invincible
        elif self.invincible:
            return # Do nothing if the player is invincible

    def apply_health_potion(self, amount):
        '''
        used to apply health potions to the player and garntee it doesn't go over the max health
        '''
        self.health = min(self.health + amount, self.max_health)
        

    def health_increase(self):
        '''
        inrcease the players max helth and refill the current health
        '''
        self.max_health += 20
        self.health = self.max_health

    def fire_rate_increase(self):
        '''
        increase the player's fire rate temporarly
        '''
        self.rifle_fire_rate /= 2
        self.shotgun_fire_rate /= 2
        self.pistol_fire_rate /= 2
        self.RPG_fire_rate /= 2
        self.fire_rate_timer = pygame.time.get_ticks() + self.boost_duration

    def check_fire_rate_increase(self):
        '''
        check if the fire rate increase hasn't expired yet
        '''
        if self.fire_rate_timer is not None:
            current_time = pygame.time.get_ticks()
            if current_time >= self.fire_rate_timer:
                self.pistol_fire_rate = 30
                self.rifle_fire_rate = 15
                self.shotgun_fire_rate = 60
                self.RPG_fire_rate = 90
                self.fire_rate_timer = None
    
    def doomsday_device(self, enemies):
        '''
        device that instantly kills all the enmies active in the game field
        '''
        #kill all the enemies in the sprite group
        for enemy in enemies:
            enemy.kill()
        
    def switch_guns(self, gun):
        '''
        allowing to switch the guns if they are unlocked

        Arg
        ------
        gun is string
            it's the name of the gun the player is switching into
        '''
        if gun in self.guns:
            if self.guns[gun]["unlocked"]:
                self.current_gun = gun
                print(f"Switched to: {gun}")
            else:
                print(f"Gun '{gun}' is locked or does not exist.")

    def unlock_guns(self, gun):
        '''
        allowing the player to unlock the guns
        '''
        if gun in self.guns:
            self.guns[gun]["unlocked"] = True
    

    
        

        

            



        





