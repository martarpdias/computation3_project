import pygame
import random
from abc import ABC, abstractmethod

class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, duration):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Default size
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = duration  # Duration in seconds
        self.start_time = None  # When the power-up is activated

    @abstractmethod
    def affect_player(self, player):
        """Apply the power-up effect to the player."""
        pass

    @abstractmethod
    def affect_game(self, game):
        """Apply the power-up effect to the game (e.g., enemy behavior)."""
        pass

    def update(self):
        """Update the power-up (optional animations)."""
        pass

    def is_expired(self):
        """Check if the power-up duration has expired."""
        return pygame.time.get_ticks() - self.start_time > self.duration * 1000
