import pygame
from powerUps import PowerUp

class Invincibility(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.image.fill((255, 105, 180))  # Pink star
        pygame.draw.polygon(self.image, (255, 20, 147), [(15, 0), (20, 30), (0, 10), (30, 10), (10, 30)])  # Star shape

    def affect_player(self, player):
        player.invincible = True
        player.image.fill((255, 255, 0))  # Change player color to yellow

    def affect_game(self, game):
        pass  # No effect on the game itself
