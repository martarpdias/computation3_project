from config import *
import math
import pygame


from shed import shed
from enemy import Enemy
from player import Player




def game_loop():
    player = Player()
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)


def execute_game(player: Player):
    """
    Main function to execute the game loop, with round transitions.
    """
    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Setting up the screen and background
    screen = pygame.display.set_mode((resolution))
    background = pygame.image.load("Lightningmcqueen.webp")
    background = pygame.transform.scale(background, (width, height))

    # Player setup
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize bullets
    bullets = pygame.sprite.Group()

    # Initialize the enemy group
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0

    # Round management
    round_time = 15  # seconds per round
    start_time = pygame.time.get_ticks()  # Get initial time for the round
    enemy_spawn_rate = fps * 2  # Initial spawn rate (every 2 seconds)

    running = True
    while running:
        # Control the frame rate
        clock.tick(fps)

        # Check if it's time for the transition
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
        if elapsed_time >= round_time:
            # Show transition screen
            show_transition_screen(screen)

            # Reset the timer and increase difficulty
            start_time = pygame.time.get_ticks()
            enemy_spawn_rate = max(10, enemy_spawn_rate - 5)  # Spawn faster enemies (min cap of 10 ticks)

        # Draw the background
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Shooting
        player.shoot(bullets)

        # Spawning the enemies
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer = enemy_spawn_rate  # Use the updated spawn rate

        # Checking for collisions between bullets and enemies
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5  # Decrease health by 5
                bullet.kill()  # Destroy the bullet
                if enemy.health <= 0:
                    enemy.kill()  # Destroy the enemy

        # Update the enemy spawn timer
        enemy_spawn_timer -= 1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Checking if the user goes into the shed area
        if player.rect.right >= width:
            # Change the game state to shed
            return "shed"

        # Draw game objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Update the display
        pygame.display.flip()


def show_transition_screen(screen):
    """
    Displays a black screen for 2 seconds as a transition between rounds.
    """
    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds
