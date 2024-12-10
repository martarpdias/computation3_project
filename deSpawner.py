import random
import pygame
from powerUps import PowerUp

class DeSpawner(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.image.fill((255, 165, 0))  # Orange star
        pygame.draw.polygon(self.image, (255, 20, 147), [(15, 0), (20, 30), (0, 10), (30, 10), (10, 30)]) #star shape
    
    def affect_player(self, player):
        pass  # No effect on the player directly

    def affect_game(self, game):
        # Remove a portion of enemies
        for _ in range(random.randint(2, 5)):
            if game.enemies:
                enemy = random.choice(game.enemies.sprites())
                enemy.kill()
        # Reduce enemy spawn rate temporarily
        game.enemy_spawn_rate = int(game.enemy_spawn_rate * 1.5)  # Spawn enemies slower
