import pygame
from powerUps import PowerUp
from config import *

class Velocity(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 191, 255))  # Light blue


    def affect_player(self, player):
        player.speed = 10
        player.image.fill((173, 216, 230))  # Change player color to light blue


    def affect_game(self, game_context):
        """Velocity does not directly affect the game."""
        pass

    def remove_effects(self, player, game_context):
        """Reset the player's speed."""
        player.speed = 5
        player.image.fill(blue)