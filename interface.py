from utils import *  # utils contains helper functions (imported pygame)
from game import *  # main game logic import

def interface():
    # initiating pygame
    pygame.init()
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    # fonts
    stencil_font = pygame.font.SysFont("stencil", 50)
    segoeuiblack_font = pygame.font.SysFont("segoeuiblack", 50)

    # Define the two lines for the title text
    line1 = "Rebellion of the"
    line2 = "Machines"

    # Function to get the height and width for multi-line text
    def get_multiline_rect(font, lines, center):
        total_height = len(lines) * font.get_linesize()  # Total height of all lines
        max_width = max(font.size(line)[0] for line in lines)  # Width of the longest line
        rect = pygame.Rect(0, 0, max_width, total_height)  # Create a rect with calculated size #
        rect.center = center  # Center the rect
        return rect

    # Function to render multi-line text with indentation for the second line
    def render_multiline_text(screen, font, lines, color, start_pos):
        x, y = start_pos
        # Render the first line centered
        text_surface1 = font.render(lines[0], True, color)
        screen.blit(text_surface1, (x - text_surface1.get_width() // 2, y))  # Centering the first line
        # Render the second line indented
        text_surface2 = font.render(lines[1], True, color)
        screen.blit(text_surface2, (x - text_surface2.get_width() // 2 + 20, y + font.get_linesize()))  # Indented second line

    # other text
    rules_text = segoeuiblack_font.render("Rules", True, white)
    options_text = segoeuiblack_font.render("Options", True, white)
    credits_text = segoeuiblack_font.render("Credits", True, white)
    quit_text = segoeuiblack_font.render("Quit", True, white)
    title_text = segoeuiblack_font.render("Computation III - Project", True, glowing_light_red)

    # main game loop
    while True:
        # event handling
        for ev in pygame.event.get():
            # quitting the game with the close button on the window (X)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # detecting if the user clicked on the quit button (450, 600 to 590, 660)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    pygame.quit()

            # detecting if the user clicked on options button (90, 630 to 230, 660):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 90 <= mouse[0] <= 230 and 600 <= mouse[1] <= 660:
                    under_construction()

            # detecting if the user clicked on the rules button (90, 480 to 230, 540):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 90 <= mouse[0] <= 230 and 480 <= mouse[1] <= 540:
                    under_construction()

            # detecting if the user clicked on the wilderness explorer button (90, 240 to 630, 300):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 90 <= mouse[0] <= 630 and 240 <= mouse[1] <= 300:
                    wilderness_explorer()

            # detecting if the user clicked on the credits button (450, 480 to 590, 540):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 480 <= mouse[1] <= 540:
                    credits_()

        # background
        screen.fill(deep_black)

        # get the mouse information
        mouse = pygame.mouse.get_pos()  # locates where the mouse is

        # drawing the buttons

        # wilderness explorer button - appearance
        pygame.draw.rect(screen, dark_red,
                         [90, 240, 540, 100])  # 90 pixels from the left, 240 from the top, 540 width, 60 height

        # Calculate the center of the screen horizontally (and leave the vertical position as is)
        screen_center_x = resolution[0] // 2

        # Calculate the bounding box for the multi-line text
        wilderness_rect = get_multiline_rect(stencil_font, [line1, line2], center=(screen_center_x, resolution[1] // 3))

        # Render the multi-line title text with indentation
        render_multiline_text(screen, stencil_font, [line1, line2], white, wilderness_rect.topleft)

        # rules button
        pygame.draw.rect(screen, grey, [90, 480, 140, 60])
        rules_rect = rules_text.get_rect(center=(90 + 140 // 2, 480 + 60 // 2))
        screen.blit(rules_text, rules_rect)

        # options button
        pygame.draw.rect(screen, grey, [90, 600, 140, 60])
        options_rect = options_text.get_rect(center=(90 + 140 // 2, 600 + 60 // 2))
        screen.blit(options_text, options_rect)

        # credits button
        pygame.draw.rect(screen, grey, [450, 480, 140, 60])
        credits_rect = credits_text.get_rect(center=(450 + 140 // 2, 480 + 60 // 2))
        screen.blit(credits_text, credits_rect)

        # quit button
        pygame.draw.rect(screen, grey, [450, 600, 140, 60])
        quit_rect = quit_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(quit_text, quit_rect)

        # title (already rendered using the multi-line method)
        # screen.blit(title_text, (55, 0))  # No longer needed as we use multi-line text rendering

        # at the end
        pygame.display.update()


