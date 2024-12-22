import pygame
from powerUps import PowerUp
from config import *

class Invincibility(PowerUp):
    def __init__(self, x, y, image_path="invincibility.png"):
        super().__init__(x,y,image_path)



    def affect_player(self, player):
        """Make the player invincible."""
        player.invincible = True
        player.image = pygame.image.load("player_invicibility.png").convert_alpha()
        player_width, player_height = 120, 80  # new size
        player.image = pygame.transform.scale(player.image, (player_width, player_height))

    def affect_game(self, game_context):
        """Invincibility does not directly affect the game."""
        pass

    def remove_effects(self, player, game_context):
        """Remove the invincibility effect."""
        player.invincible = False
        player.image = pygame.image.load("player_picture.png").convert_alpha()
        player_width, player_height = 75, 75  # new size
        player.image = pygame.transform.scale(player.image, (player_width, player_height))

