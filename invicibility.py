import pygame
from powerUps import PowerUp

class Invincibility(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.image.fill((255, 105, 180))  # Pink star
        pygame.draw.polygon(self.image, (255, 20, 147), [(15, 0), (20, 30), (0, 10), (30, 10), (10, 30)])  # Star shape

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


