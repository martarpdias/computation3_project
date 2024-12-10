import pygame
from powerUps import PowerUp
from config import *

class Invincibility(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 105, 180))  # Pink
 

    def affect_player(self, player):
        """Make the player invincible."""
        player.invincible = True
        player.image.fill((255, 105, 180))  # Change player color to pink

    def affect_game(self, game_context):
        """Invincibility does not directly affect the game."""
        pass

    def remove_effects(self, player, game_context):
        """Remove the invincibility effect."""
        player.invincible = False
        player.image.fill(blue)


