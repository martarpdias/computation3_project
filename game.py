from config import *
import math
import pygame
import random

from shed import shed
from enemy import *
from player import Player
from bullet import Bullet
from invicibility import Invincibility
from deSpawner import DeSpawner
from velocity import Velocity


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

    resolution=(1200,600)
    # Setting up the screen and background
    screen = pygame.display.set_mode((resolution))
    background = pygame.image.load("game_background.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Player setup
    player_group = pygame.sprite.Group()
    player_group.add(player)
    score = 0

    # Initialize bullets
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    # Initialize the enemy group
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0

    # Round management
    current_round = 1
    round_time = 90  # seconds per round
    start_time = pygame.time.get_ticks()  # Get initial time for the round
    enemy_spawn_rate = fps * 2  # Initial spawn rate (every 2 seconds)

    # Bullet type management
    selected_bullet_type = 1  # Default bullet type
    shooting_timer = 0

    running = True
    while running:
        # Control the frame rate
        clock.tick(fps)

        # Draw the background
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Detect key presses for bullet selection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_bullet_type = 1  # Normal bullet
                elif event.key == pygame.K_2:
                    selected_bullet_type = 2  # Fast bullet
                elif event.key == pygame.K_3:
                    selected_bullet_type = 3  # Large bullet

        # automatic shooting
        if shooting_timer <= 0:  # Shoot every few frames
            directions = [math.radians(0), math.radians(90), math.radians(180), math.radians(270)]

            for direction in directions:
                bullet = shoot_bullet(player.rect.centerx, player.rect.centery, direction, selected_bullet_type)
                bullets.add(bullet)

            shooting_timer = fps // 2  # Adjust shooting rate

        shooting_timer -= 0.5  # Decrement the shooting timer
        # Update and draw bullets
        bullets.update()
        for bullet in bullets:
            bullet.draw(screen)

        # Calculate remaining time
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
        time_left = max(0, round_time - elapsed_time)

        # Calculate the width of the time bar
        bar_width = int((time_left / round_time) * width - 40)  # Proportional to remaining time

        # Set the color of the time bar (optional: green -> yellow -> red transition)
        if time_left > round_time * 0.5:
            bar_color = (0, 255, 0)  # Green
        elif time_left > round_time * 0.2:
            bar_color = (255, 165, 0)  # Orange
        else:
            bar_color = (255, 0, 0)  # Red

        # Add rounded corners to the time bar
        pygame.draw.rect(screen, (255, 255, 255), (20, height - 40, width - 40, 25),
                         border_radius=10)  # Draw a background bar
        pygame.draw.rect(screen, bar_color, (30, height - 35, bar_width, 15),
                         border_radius=10)  # Time bar with rounded corners

        # Display the numerical time remaining
        font = pygame.font.SysFont("segoeuiblack", 20)
        time_text = font.render(f"Time: {int(time_left)}s", True, (255, 255, 255))
        screen.blit(time_text, (25, height - 70))

        if elapsed_time >= round_time:
            # Show transition screen
            show_transition_screen(screen)

            # Reset the timer and increase difficulty
            start_time = pygame.time.get_ticks()
            current_round += 1

        # Display round number
        round_text = font.render(f"Round: {current_round}", True, (255, 255, 255))
        screen.blit(round_text, (160, 45))

        # Draw player health bar
        player_health_bar_width = int(
            (player.health / 100) * (width / 3))  # Scale health to a thrid of the screen width
        pygame.draw.rect(screen, (255, 0, 0), (15, 20, (width / 3), 20),
                         border_radius=10)  # Background for the health bar
        pygame.draw.rect(screen, (0, 255, 0), (15, 20, player_health_bar_width, 20),
                         border_radius=10)  # Player health bar
        if player.health <= 0:
            show_game_over_screen(screen)

        # Display the numerical life remaining
        font = pygame.font.SysFont("segoeuiblack", 20)
        life_text = font.render(f"Life: {int(player.health)}%", True, (255, 255, 255))
        screen.blit(life_text, (25, 45))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for enemy in enemies:
            if isinstance(enemy, shooter_rastreio):
                enemy.shoot(enemy_bullets, player)
                pass

        # shooting
        # player.shoot(bullets)

        # spawning the enemies
        if enemy_spawn_timer <= 0:
            enemy_type = random.choice([Enemy, fast_enemy, shooter_rastreio])
            new_enemy = enemy_type()
            enemies.add(new_enemy)
            enemy_spawn_timer = enemy_spawn_rate

        # Checking for collisions between bullets and enemies
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5  # Decrease health by 5 for each hit
                bullet.kill()  # Destroy the bullet
                if enemy.health <= 0:
                    enemy.kill()  # Destroy the enemy
                    score += 100

        # Checking for collisions between bullets and players
        for bullet in enemy_bullets:
            collided_player = pygame.sprite.spritecollideany(bullet, player_group)
            if collided_player:
                player.health -= 5  # Decrease health by 5 for each hit
                bullet.kill()  # Destroy the bullet
                if player.health <= 0:
                    player.kill()  # Destroy the player
                    score += 100

        # Update the enemy spawn timer
        enemy_spawn_timer -= 1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)
        enemy_bullets.update()

        # check for colission btween player and enemies
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
        damage = 5
        for enemy in collided_enemies:
            player.take_damage(enemy.damage)

        # Check if the player is dead
        if player.health <= 0:
            print("game_over")

        # Checking if the user goes into the shed area
        if player.rect.right >= width:
            # Change the game state to shed
            return "shed"

        # Draw game objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for bullet in enemy_bullets:
            bullet.draw(screen)

        # Draw health bars for enemies
        enemy_health_bar_max_width = 50  # Maximum width of the health bar
        for enemy in enemies:
            enemy_health_bar_width = int(
                (enemy.health / enemy.max_health) * enemy_health_bar_max_width)  # Scale enemy health to the max width
            pygame.draw.rect(screen, (255, 0, 0), (enemy.rect.x, enemy.rect.y - 10, 50, 5))  # Background bar
            pygame.draw.rect(screen, (0, 255, 0),
                             (enemy.rect.x, enemy.rect.y - 10, enemy_health_bar_width, 5))  # Enemy health bar

        # Display the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
        screen.blit(score_text, (295, 45))  # Display the score at the top-left corner

        # Update the display
        pygame.display.flip()


'''
        #power ups
        power_ups = pygame.sprite.Group()
        power_up_spawn_timer = 0  # Timer for spawning power-ups

        # Spawning power-ups
        if power_up_spawn_timer <= 0:
            if random.random() < 0.2:  # 10% chance every cycle
                x, y = random.randint(50, width - 50), random.randint(50, height - 50)
                if random.random() < 0.33:  # 33% chance for Invincibility
                    new_power_up = Invincibility(x, y)
                elif random.random() < 0.66:  # 33% chance for Velocity
                    new_power_up = Velocity(x, y)
                else:  # 33% chance for DeSpawner
                    new_power_up = DeSpawner(x, y)
                power_ups.add(new_power_up)
            power_up_spawn_timer = fps * 5  # 5 seconds until next spawn
        power_up_spawn_timer -= 1

        # Checking for collisions with the player and power-ups
        collided_power_ups = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in collided_power_ups:
            power_up.start_time = pygame.time.get_ticks()
            power_up.affect_player(player)
            power_up.affect_game({
                "enemies": enemies,
                "enemy_spawn_rate": enemy_spawn_rate
            })
            player.active_power_up = power_up  # Track the active power-up

        # Handle active power-ups
        if player.active_power_up:
            if player.active_power_up.is_expired():
                # Remove effects
                if isinstance(player.active_power_up, Invincibility):
                    player.invincible = False
                    player.image.fill(blue)  # Revert player color
                elif isinstance(player.active_power_up, DeSpawner):
                    enemy_spawn_rate = fps * 2  # Reset spawn rate
                elif isinstance(player.active_power_up, Velocity):
                    player.speed = 5  # Reset player speed
                player.active_power_up = None
'''


def show_transition_screen(screen):
    """
    Displays a black screen for 2 seconds as a transition between rounds.
    """
    screen.fill((0, 0, 0))  # Fill the screen with black

    segoeuiblack_font = pygame.font.SysFont("segoeuiblack", 50)
    text = segoeuiblack_font.render("Round completed!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds


def show_game_over_screen(screen):
    """
    Displays a game over screen with a message and waits for the player to close the window.
    """
    screen = pygame.display.set_mode(resolution)
    screen.fill((0, 0, 0))  # Fill the screen with black

    segoeuiblack_font = pygame.font.SysFont("segoeuiblack", 50)
    text = segoeuiblack_font.render("Game Over!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
