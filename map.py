import pygame
from config import *


def map(player):
    # Setup of the background and screen
    background = pygame.image.load("map.jpg")
    background = pygame.transform.scale(background, resolution)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Set the player's position
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Define level rectangles with corresponding level numbers
    level_rects = {
        1: pygame.Rect(400, 400, 20, 20),
        2: pygame.Rect(400, 300, 20, 20),
        3: pygame.Rect(400, 200, 20, 20),
        4: pygame.Rect(500, 100, 20, 20),
        5: pygame.Rect(600, 100, 20, 20),
        6: pygame.Rect(700, 100, 20, 20),
        7: pygame.Rect(800, 200, 20, 20),
        8: pygame.Rect(800, 300, 20, 20),
        9: pygame.Rect(800, 400, 20, 20),
        10: pygame.Rect(700, 500, 20, 20),
    }

    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Update the player's position
        player.update()

        # Detect if the player walks into a level
        for level, rect in level_rects.items():
            if rect.colliderect(player.rect):
                if LEVELS[level]["unlock"]:  # Check if the level is unlocked
                    start_level(level, player)  # Function to start the level
                    player.rect.top = 200  # Reset player position
                    player.rect.left = 560
                else:
                    display_locked_message(screen)  # Inform the player that the level is locked
                break  # Exit the loop once a level is detected

        # Draw the player
        player_group.draw(screen)

        pygame.display.flip()

def start_level(level, player):
    # Get level configuration
    level_data = LEVELS[level]
    spawn_rate = level_data["spawn_rate"]
    max_enemies = level_data["max_enemies"]
    enemy_types = level_data["enemy_types"]

    # Transition to the gameplay screen for this level
    result = play_level(level, spawn_rate, max_enemies, enemy_types, player)

    # Handle result (e.g., level completion or returning to map)
    if result == "map":
        return "map"

def display_locked_message(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Level is locked!", True, (255, 0, 0))
    screen.blit(text, (resolution[0] // 2 - text.get_width() // 2, resolution[1] // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait 2 seconds before returning to the map



