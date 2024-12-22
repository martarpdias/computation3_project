import random
import pygame
from powerUps import PowerUp
from config import *

class DeSpawner(PowerUp):


    def __init__(self, x, y, image_path="deSpawner.png"):
        super().__init__(x, y, image_path)

    def affect_player(self, player):
        player.image = pygame.image.load("player_deSpawner.png").convert_alpha()
        player_width, player_height = 110, 93
        player.image = pygame.transform.scale(player.image, (player_width, player_height))

    def affect_game(self, game):
        # Reduce enemy spawn rate temporarily
        game["enemy_spawn_rate"] = int(game["enemy_spawn_rate"]) * 3  # Spawn slower

        # Kill a random number of enemies on the screen
        enemies_to_kill = random.randint(1, max(1, len(game["enemies"])))
        # Choose random number
        enemies_killed = 0
        for enemy in list(game["enemies"]):  # Convert to list to avoid iteration issues
            if enemies_killed >= enemies_to_kill:
                break
            game["enemies"].remove(enemy)  # Remove the enemy from the group
            enemy.kill()


    def remove_effects(self, player, game_context):
        """Reset the spawn rate to normal."""
        game_context["enemy_spawn_rate"] = fps * 2
        player.image = pygame.image.load("player_picture.png").convert_alpha()
        player_width, player_height = 75, 75
        player.image = pygame.transform.scale(player.image, (player_width, player_height))
