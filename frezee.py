import pygame
from powerUps import PowerUp
from config import *

class FreezeEnemiesPowerUp(PowerUp):
    def __init__(self, x, y, color=(0, 255, 255)):  # Default color: cyan
        super().__init__(x, y, color)
        self.frozen_enemies = []  # Track which enemies are frozen

    def affect_game(self, game):
        """Stop all enemies from moving and shooting."""
        for enemy in game.enemies:
            # Save enemy's current speed and shoot cooldown for restoration later
            self.frozen_enemies.append({
                "enemy": enemy,
                "original_speed": enemy.speed,
                "original_shoot_cooldown": getattr(enemy, "shoot_cooldown", None),
            })
            # Freeze the enemy
            enemy.speed = 0
            if hasattr(enemy, "shoot_cooldown"):
                enemy.shoot_cooldown = float("inf")  # Disable shooting by setting cooldown very high

    def remove_effects(self, player, game):
        """Restore all frozen enemies' original behaviors."""
        for frozen in self.frozen_enemies:
            enemy = frozen["enemy"]
            enemy.speed = frozen["original_speed"]
            if "original_shoot_cooldown" in frozen and frozen["original_shoot_cooldown"] is not None:
                enemy.shoot_cooldown = frozen["original_shoot_cooldown"]
        self.frozen_enemies.clear()

    def affect_player(self, player):
        """This power-up does not directly affect the player."""
        pass

