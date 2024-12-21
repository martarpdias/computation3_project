from config import *
import math
import pygame
import random

from map import map
from enemy import *
from player import Player
from bullet import Bullet
from invicibility import Invincibility
from deSpawner import DeSpawner
from velocity import Velocity
from chests import Chest
from game_helpers import *


def execute_game(player: Player):
    """
    Main function to execute the game loop, with round transitions.
    """
    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Resolution and screen setup
    resolution = (1200, 600)
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("game_background.jpg")
    background = pygame.transform.scale(background, resolution)

    # Player setup
    player_group = pygame.sprite.Group(player)
    score = 0

    # Initialize bullets, enemies, power-ups, and chests
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    chests = pygame.sprite.Group()

    # Round management
    current_level = 1
    level_time = 20  # seconds per round
    start_time = pygame.time.get_ticks()  # Get initial time for the round

    # Initialize other gameplay variables
    power_up_spawn_timer = 0
    chest_spawn_delay = 10000
    last_chest_spawn_time = pygame.time.get_ticks()
    active_power_ups = []
    selected_bullet_type = 1  # Default bullet type
    shooting_timer = 0

    running = True
    while running:
        # Control the frame rate
        clock.tick(fps)

        # Draw the background
        screen.blit(background, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                # Switch guns
                if event.key == pygame.K_1:
                    player.switch_guns("pistol")
                elif event.key == pygame.K_2:
                    player.switch_guns("rifle")
                elif event.key == pygame.K_3:
                    player.switch_guns("shotgun")
                elif event.key == pygame.K_4:
                    player.switch_guns("RPG")
                # Change bullet type
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    selected_bullet_type = int(event.unicode)

        # Automatic shooting
        if shooting_timer <= 0:
            for direction in [math.radians(0), math.radians(90), math.radians(180), math.radians(270)]:
                bullet = shoot_bullet(player.rect.centerx, player.rect.centery, direction, selected_bullet_type)
                bullets.add(bullet)
            shooting_timer = fps // 2
        shooting_timer -= 0.5

        # Update bullets
        bullets.update()

        # Handle enemy spawning
        last_spawn_time = spawn_enemies(
            enemies=enemies,
            enemy_types=LEVELS[current_level]["enemy_types"],
            spawn_rate=LEVELS[current_level]["spawn_rate"],
            max_enemies=LEVELS[current_level]["max_enemies"],
            last_spawn_time=pygame.time.get_ticks()
        )

        # Manage power-ups
        power_up_spawn_timer = manage_power_ups(
            player=player,
            power_ups=power_ups,
            active_power_ups=active_power_ups,
            screen=screen,
            power_up_spawn_timer=power_up_spawn_timer,
            fps=fps
        )

        # Handle round transitions
        current_level, start_time = handle_round_transition(
            current_level=current_level,
            level_time=level_time,
            start_time=start_time,
            player=player,
            enemies=enemies,
            bullets=bullets,
            power_ups=power_ups,
            screen=screen
        )

        # Manage chests spawning
        current_time = pygame.time.get_ticks()
        if current_time - last_chest_spawn_time > chest_spawn_delay:
            new_chest = Chest()
            new_chest.spawner()
            chests.add(new_chest)
            last_chest_spawn_time = current_time

        # Check collisions
        handle_collisions(
            player=player,
            bullets=bullets,
            enemies=enemies,
            enemy_bullets=enemy_bullets,
            chests=chests,
            score=score
        )

        # Update all sprite groups
        player_group.update()
        enemies.update(player)
        bullets.update()
        enemy_bullets.update()
        power_ups.update()
        chests.update()

        # Draw all game elements
        draw_game_elements(
            screen=screen,
            player=player,
            player_group=player_group,
            enemies=enemies,
            bullets=bullets,
            enemy_bullets=enemy_bullets,
            power_ups=power_ups,
            chests=chests,
            score=score,
            current_level=current_level,
            level_time=level_time,
            start_time=start_time
        )

        # Check if the player is dead
        if player.health <= 0:
            show_game_over_screen(screen)

        # Update the display
        pygame.display.flip()
