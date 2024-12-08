import pygame
import random
from abc import ABC, abstractmethod

class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, duration):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Default size
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = duration  # Duration in seconds
        self.start_time = pygame.time.get_ticks()  # Set start time when created

    @abstractmethod
    def affect_player(self, player):
        """Apply the power-up's effect to the player."""
        pass

    @abstractmethod
    def affect_game(self, game):
        """Apply the power-up's effect to the game."""
        pass

    def remove_effects(self, player, game_context):
        """Remove the power-up's effects (default: do nothing)."""
        pass

    def update(self):
        """Update the power-up (for optional animations)."""
        pass

    def is_expired(self):
        """Check if the power-up duration has expired."""
        return pygame.time.get_ticks() - self.start_time > self.duration * 1000


