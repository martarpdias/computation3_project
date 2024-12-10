import random
import pygame
from powerUps import PowerUp
from config import *

class DeSpawner(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 165, 0))  # Orange

    def affect_player(self, player):
        player.image.fill((255, 165, 0))  # Change player color to orange

    def affect_game(self, game):
        # Reduce enemy spawn rate temporarily
        game["enemy_spawn_rate"] = int(game["enemy_spawn_rate"])/2  # Spawn half as fast

    def remove_effects(self, player, game_context):
        """Reset the spawn rate to normal."""
        game_context["enemy_spawn_rate"] = fps * 2
        player.image.fill(blue)
