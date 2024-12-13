from utils import *  # utils contains helper functions (imported pygame)
from game import *  # main game logic import

def interface():
    # initiating pygame
    pygame.init()
    pygame.font.init()
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    # fonts
    stencil_font = pygame.font.SysFont("stencil", 50)
    segoeuiblack_font = pygame.font.SysFont("segoeuiblack", 50)

    # Define the two lines for the title text
    line1 = "Rebellion of the"
    line2 = "Machines"

    # Function to calculate the size of multi-line text
    def get_multiline_size(font, lines):
        # Get the height and width for the text based on the lines
        total_height = len(lines) * font.get_linesize()  # Total height of all lines
        max_width = max(font.size(line)[0] for line in lines)  # Width of the longest line
        return total_height, max_width

    # Function to render the multi-line text, centered horizontally
    def render_multiline_text(screen, font, lines, color, center):
        # Calculate the total height and width
        total_height, max_width = get_multiline_size(font, lines)
        x, y = center

        # Render the first line (center horizontally)
        text_surface1 = font.render(lines[0], True, color)
        screen.blit(text_surface1, (x - text_surface1.get_width() // 2, y - total_height // 2))

        # Render the second line (center horizontally)
        text_surface2 = font.render(lines[1], True, color)
        screen.blit(text_surface2, (x - text_surface2.get_width() // 2, y - total_height // 2 + font.get_linesize()))

    # Other text definitions
    rules_text =  stencil_font.render("Rules", True, white)
    options_text =  stencil_font.render("Options", True, white)
    credits_text =  stencil_font.render("Credits", True, white)
    quit_text =  stencil_font.render("Quit", True, white)
    title_text =  stencil_font.render("Computation III - Project", True, glowing_light_red)

    # Main game loop
    while True:
        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            # Mouse button clicks
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    pygame.quit()

                if 90 <= mouse[0] <= 230 and 480 <= mouse[1] <= 540:
                    under_construction()

                if 90 <= mouse[0] <= 230 and 600 <= mouse[1] <= 660:
                    under_construction()

                if 90 <= mouse[0] <= 630 and 240 <= mouse[1] <= 300:
                    wilderness_explorer()

                if 450 <= mouse[0] <= 590 and 480 <= mouse[1] <= 540:
                    credits_()

        # Background fill
        screen.fill(deep_black)

        # Get mouse position
        mouse = pygame.mouse.get_pos()

        # Drawing buttons and other elements
        pygame.draw.rect(screen, dark_red, [90, 240, 540, 100])

        # Get the center of the screen for horizontal centering
        screen_center_x = resolution[0] // 2

        # Calculate the vertical position to center the title (let's place it roughly in the upper third of the screen)
        screen_center_y = resolution[1] // 3

        # Render the title with two lines
        render_multiline_text(screen, stencil_font, [line1, line2], white, (screen_center_x, screen_center_y))

        # Drawing other buttons
        pygame.draw.rect(screen, grey, [90, 480, 140, 60])
        rules_rect = rules_text.get_rect(center=(90 + 140 // 2, 480 + 60 // 2))
        screen.blit(rules_text, rules_rect)

        pygame.draw.rect(screen, grey, [90, 600, 140, 60])
        options_rect = options_text.get_rect(center=(90 + 140 // 2, 600 + 60 // 2))
        screen.blit(options_text, options_rect)

        pygame.draw.rect(screen, grey, [450, 480, 140, 60])
        credits_rect = credits_text.get_rect(center=(450 + 140 // 2, 480 + 60 // 2))
        screen.blit(credits_text, credits_rect)

        pygame.draw.rect(screen, grey, [450, 600, 140, 60])
        quit_rect = quit_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(quit_text, quit_rect)

        # Update the screen
        pygame.display.update()


# Under construction screen


def credits_():
    screen = pygame.display.set_mode(resolution)

    # fonts
    stencil_font = pygame.font.SysFont("stencil", 40)
    ocraextended_font = pygame.font.SysFont("ocraextended", 40)

    # text
    joao =  ocraextended_font.render("João Santos", True, white)
    joao_mail =  ocraextended_font.render("20231697@novaims.unl.pt", True, white)
    marta = ocraextended_font.render("Marta Dias", True, white)
    marta_mail = ocraextended_font.render("20231642@novaims.unl.pt", True, white)
    rita = ocraextended_font.render("Rita Pinto",True, white)
    rita_mail = ocraextended_font.render("20231664@novaims.unl.pt", True, white)

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
                    interface()

        # background
        screen.fill(deep_black)

        # display text
        screen.blit(joao, (0, 0))
        screen.blit(joao_mail, (0, 50))
        screen.blit(marta, (0, 130))
        screen.blit(marta_mail, (0, 180))
        screen.blit(rita, (0, 260))
        screen.blit(rita_mail, (0, 310))

        # draw a back button [x, y, width, height]
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_text = stencil_font.render("    back", True, white)
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Update the screen
        pygame.display.update()


def rules_():
    print("Displaying rules...")


def wilderness_explorer():
    game_loop()