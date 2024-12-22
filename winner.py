import pygame
from config import *


def game_over_screen():
    from interface import interface  # Prevent circular import

    # Initialize Pygame screen
    screen = pygame.display.set_mode(resolution)

    # Fonts
    title_font = pygame.font.SysFont("stencil", 60)
    button_font = pygame.font.SysFont("stencil", 40)

    # Texts
    game_over_text = title_font.render("YOU WON", True, white)

    # Load and scale background image
    background_image = pygame.image.load("options_background.jpg")
    background_image = pygame.transform.scale(background_image, resolution)  # Scale to fit screen
    screen.blit(background_image, (0, 0))  # Draw background image

    # Buttons (adjusted size and spacing)
    button_width, button_height = 270, 60
    button_spacing = 50
    retry_button_rect = pygame.Rect(
        (resolution[0] // 2 - button_width - button_spacing // 2, resolution[1] // 2),
        (button_width, button_height),
    )
    quit_button_rect = pygame.Rect(
        (resolution[0] // 2 + button_spacing // 2, resolution[1] // 2),
        (button_width, button_height),
    )

    retry_text = button_font.render("MENU", True, (255, 255, 255))
    retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
    quit_text = button_font.render("QUIT", True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)

    # Draw buttons with colors (red for retry, blue for quit)
    pygame.draw.rect(screen, (255, 0, 0), retry_button_rect, border_radius=10)  # Red for Retry
    pygame.draw.rect(screen, (0, 0, 255), quit_button_rect, border_radius=10)  # Blue for Quit
    screen.blit(retry_text, retry_text_rect)
    screen.blit(quit_text, quit_text_rect)

    # Title (Game Over)
    title_rect = game_over_text.get_rect(center=(resolution[0] // 2, resolution[1] // 3))
    screen.blit(game_over_text, title_rect)

    # Update the screen
    pygame.display.update()

    # Main game loop for the game over screen
    while True:
        mouse = pygame.mouse.get_pos()

        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(ev.pos):
                    interface()  # Go back to the main interface (menu)
                elif quit_button_rect.collidepoint(ev.pos):
                    pygame.quit()
                    return

        # Interactive Buttons (hover effect)
        if retry_button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, (200, 0, 0), retry_button_rect, border_radius=10)  # Darker red for hover
        else:
            pygame.draw.rect(screen, (255, 0, 0), retry_button_rect, border_radius=10)  # Normal red
        if quit_button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, (0, 0, 200), quit_button_rect, border_radius=10)  # Darker blue for hover
        else:
            pygame.draw.rect(screen, (0, 0, 255), quit_button_rect, border_radius=10)  # Normal blue

        # Redraw texts after hover effects
        screen.blit(retry_text, retry_text_rect)
        screen.blit(quit_text, quit_text_rect)

        # Update the screen
        pygame.display.update()