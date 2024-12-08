import random
import pygame
from powerUps import PowerUp

class DeSpawner(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.image.fill((255, 165, 0))  # Orange star
        pygame.draw.polygon(self.image, (255, 140, 0), [(15, 0), (20, 30), (0, 10), (30, 10), (10, 30)])  # Star shape

    def affect_player(self, player):
        player.image.fill((255, 165, 0))  # Change player color to orange

    def affect_game(self, game):
        # Reduce enemy spawn rate temporarily
        game["enemy_spawn_rate"] = int(game["enemy_spawn_rate"] * 2)  # Spawn half as fast

    def remove_effects(self, player, game_context):
        """Reset the spawn rate to normal."""
        game_context["enemy_spawn_rate"] = fps * 2
