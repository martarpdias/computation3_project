import pygame

from class1_ui.config import resolution, white, deep_black, dark_red



# Function to draw a stick figure with a construction hat
def draw_stick_figure_with_hat(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg

    # hat
    hat_color = (255, 215, 0)

    # drawing the construction hat
    pygame.draw.rect(screen, hat_color, [x - 25, y - 30, 50, 10])  # Hat's brim
    pygame.draw.rect(screen, hat_color, [x - 20, y - 40, 40, 20])  # Hat's dome


# Function to draw a normal stick figure (without a hat)
def draw_normal_stick_figure(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg


def under_construction():
    # creating the screen at 720x720 pixels - placeholder
    screen = pygame.display.set_mode(resolution)

    # fonts
    corbel_font = pygame.font.SysFont("Corbel", 50)
    conversation_font = pygame.font.SysFont("Arial", 30)

    # text
    back_text = corbel_font.render("    back", True, white)
    construction_text = corbel_font.render("Under Construction", True, white)

    # positions for the stick figures
    bob_x_position = 460
    bob_y_position = 450

    normal_x_position = 260
    normal_y_position = 450

    # main game loop
    while True:
        # mouse information
        mouse = pygame.mouse.get_pos()

        # check for events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    return

        # background
        screen.fill(deep_black)

        # display 'UNDER CONSTRUCTION' text
        construction_rect = construction_text.get_rect(center=(360, 300))
        screen.blit(construction_text, construction_rect)

        # draw a back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # stick figures
        draw_normal_stick_figure(screen, normal_x_position, normal_y_position)
        draw_stick_figure_with_hat(screen, bob_x_position, bob_y_position)

        # conversation
        normal_speech = conversation_font.render("Can we fix it?", True, white)
        bob_response = conversation_font.render("Probably not.", True, white)

        screen.blit(normal_speech, (normal_x_position - 60, normal_y_position - 80))
        screen.blit(bob_response, (bob_x_position - 60, bob_y_position - 80))

        # Update the screen
        pygame.display.update()
