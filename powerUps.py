import pygame
import random
from abc import ABC, abstractmethod

class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.radius = 15  # Radius of the glowing circle
        self.image = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)  # Semi-transparent surface
        self.rect = self.image.get_rect(center=(x, y))
        self.create_glow()

        self.duration = 5  # Duration in seconds
        self.start_time = pygame.time.get_ticks()  # Set start time when created

    def create_glow(self):
        """Create the glowing circle effect."""
        center = self.image.get_width() // 2
        for i in range(1, 4):  # Add multiple layers of glow
            pygame.draw.circle(
                self.image,
                (self.color[0], self.color[1], self.color[2], 255 // (i * 2)),  # Fading alpha for glow
                (center, center),
                self.radius + i * 5,  # Outer radius for the glow
            )
        pygame.draw.circle(
            self.image,
            self.color,
            (center, center),
            self.radius,  # Inner solid circle
        )

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
        """Add a pulsing glow animation."""
        pulse = (pygame.time.get_ticks() // 100) % 20  # Create a pulsing effect
        self.radius = 15 + pulse // 5  # Adjust the radius slightly
        self.image.fill((0, 0, 0, 0))  # Clear the previous surface
        self.create_glow()  # Redraw the glow with the new radius


    def is_expired(self):
        """Check if the power-up duration has expired."""
        return pygame.time.get_ticks() - self.start_time > self.duration * 1000



