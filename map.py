import pygame
from config import *
from levels import LEVELS

def map(player):
    # Setup of the background and screen
    background = pygame.image.load("map.jpg")
    background = pygame.transform.scale(background, resolution)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Set the player's position
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Define level rectangles with scaled positions
    level_rects = {
        1: pygame.Rect(100, 560, 40, 40),
        2: pygame.Rect(267, 372, 20, 20),
        3: pygame.Rect(267, 266, 20, 20),
        4: pygame.Rect(401, 159, 20, 20),
        5: pygame.Rect(602, 159, 20, 20),
        6: pygame.Rect(803, 159, 20, 20),
        7: pygame.Rect(937, 266, 20, 20),
        8: pygame.Rect(937, 372, 20, 20),
        9: pygame.Rect(937, 479, 20, 20),
        10: pygame.Rect(803, 532, 20, 20),
    }


    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Update the player's position
        player.update()

        # Detect if the player walks into a level
        for level, rect in level_rects.items():
            if rect.colliderect(player.rect):
                if LEVELS[level]["unlock"]:  # Check if the level is unlocked
                    completed = start_level(level, player)
                    if completed and level + 1 in LEVELS:
                        LEVELS[level + 1]["unlock"] = True  # Unlock the next level
                    player.rect.top = 200  # Reset player position
                    player.rect.left = 560
                else:
                    display_locked_message(screen, player)  # Inform the player that the level is locked
                break  # Exit the loop once a level is detected

        # Draw the player
        player_group.draw(screen)

        pygame.display.flip()

def start_level(level_number, player):
    # Initialize the level
    print(f"Starting level {level_number}")  # Debugging
    enemies = pygame.sprite.Group()  # Reset enemies for the new level
    bullets = pygame.sprite.Group()  # Reset bullets for the new level
    enemy_bullets = pygame.sprite.Group()

    # Setup the environment based on level configuration
    current_level_data = LEVELS[level_number]
    enemy_spawn_rate = current_level_data["enemy_spawn_rate"]
    round_time = current_level_data["round_time"]

    # Main level loop
    start_time = pygame.time.get_ticks()
    completed = False

    while not completed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Gameplay logic
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Seconds
        if elapsed_time >= round_time:
            completed = True  # Level completed when the timer ends

        # Render and update game objects
        # [Add your level gameplay here, e.g., drawing enemies, handling player actions, etc.]

        pygame.display.flip()
        pygame.time.delay(50)  # Adjust frame delay

    return True  # Indicate the level was completed successfully



def display_locked_message(screen, player):
    font = pygame.font.Font(None, 36)
    text = font.render("Level is locked!", True, (255, 0, 0))
    screen.blit(text, (resolution[0] // 2 - text.get_width() // 2, resolution[1] // 2))
    player.rect.top = 200  # Reset player position
    player.rect.left = 560
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait 2 seconds before returning to the map



