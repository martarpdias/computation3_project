import pygame
from powerUps import PowerUp
from config import *

class Velocity(PowerUp):
    def __init__(self, x, y, image_path="velocity.png"):
        super().__init__(x,y,image_path)

    def affect_player(self, player):
        player.speed = 10
        player.image = pygame.image.load("player_velocity.png").convert_alpha()
        player_width, player_height = 85, 93  # new size
        player.image = pygame.transform.scale(player.image, (player_width, player_height))


    def affect_game(self, game_context):
        """Velocity does not directly affect the game."""
        pass

    def remove_effects(self, player, game_context):
        """Reset the player's speed."""
        player.speed = 5
        player.image = pygame.image.load("player_picture.png").convert_alpha()
        player_width, player_height = 75, 75  # new size
        player.image = pygame.transform.scale(player.image, (player_width, player_height))