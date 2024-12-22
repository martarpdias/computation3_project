import pygame
from powerUps import PowerUp
from config import *
import random

class Freeze(PowerUp):
    def __init__(self, x, y, image_path="freeze.png"):
        super().__init__(x,y,image_path)

    def affect_player(self,player):
        enemies=pygame.sprite.Group()
        enemies.speed = fps*20
        player.image = pygame.image.load("player_freeze.png").convert_alpha()
        player_width, player_height = 100, 93  # new size
        player.image = pygame.transform.scale(player.image, (player_width, player_height))


    def affect_game(self, game_context):
        """Freeze does not directly affect the game."""
        pass

    def remove_effects(self, player, game_context):
        player.speed = 5
        enemies=pygame.sprite.Group()
        enemies.speed = random.randint(2, 3)
        player.image = pygame.image.load("player_picture.png").convert_alpha()
        player_width, player_height = 75, 75  # new size
        player.image = pygame.transform.scale(player.image, (player_width, player_height))