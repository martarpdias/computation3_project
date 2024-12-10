import pygame
from powerUps import PowerUp

class Velocity(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.image.fill(((173, 216, 230)))  # blue star
        pygame.draw.polygon(self.image, (255, 20, 147), [(15, 0), (20, 30), (0, 10), (30, 10), (10, 30)])  # Star shape

    def affect_player(self, player):
        player.speed = 10
        player.image.fill(((173, 216, 230)))  # Change player color to blue

    def affect_game(self, game):
        pass  # No effect on the game itself