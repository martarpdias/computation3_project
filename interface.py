from utils import *  # utils contains helper functions (imported pygame)
from game import *  # main game logic import

def interface():
    # initiating pygame
    pygame.init()
    pygame.font.init()
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    #pygame.mouse.set_cursor(*pygame.cursors.arrow)  # Default arrow
    pygame.mouse.set_cursor(*pygame.cursors.diamond)  # Diamond cursor
    #pygame.mouse.set_cursor(*pygame.cursors.ball)  # Small circle cursor
    #pygame.mouse.set_cursor(*pygame.cursors.tri_left)  # Left-pointing

    # Initialize pygame mixer
    pygame.mixer.init()

    def play_music():
        # Check if music is already playing
        if not pygame.mixer.music.get_busy():  # If no music is playing
            pygame.mixer.music.load("background_music.mp3")  # Load music
            pygame.mixer.music.play(-1, 0.0)  # Play music indefinitely

    play_music()




    #Fonts
    stencil_font = pygame.font.SysFont("stencil", 40)

    
    game_name_line = "Rebellion of the Machines"




    # Other text definitions
    rules_text =  stencil_font.render("Rules", True, white)
    options_text =  stencil_font.render("Options", True, white)
    credits_text =  stencil_font.render("Credits", True, white)
    quit_text =  stencil_font.render("Quit", True, white)
    title_text= stencil_font.render(game_name_line, True, dark_red)
    play_text = stencil_font.render("PLAY", True, white)


    # Main game loop
    while True:
        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            # Mouse button clicks
            if ev.type == pygame.MOUSEBUTTONDOWN:

                if 500 <= mouse[0] <= 500+200 and 480 <= mouse[1] <= 480+60:
                    pygame.quit()

                if 500 <= mouse[0] <= 500+200 and 240 <= mouse[1] <= 240+60:
                    rules_()

                if 500 <= mouse[0] <= 500+200 and 320 <= mouse[1] <= 320+60:
                    options_()

                if 465 <= mouse[0] <= 465+270 and 160 <= mouse[1] <= 160+60:
                    start_game()

                if 500 <= mouse[0] <= 500+200 and 400 <= mouse[1] <= 400+60:
                    credits_()





        # Background image
        background_image = pygame.image.load("background_interface.jpg")
        background_image = pygame.transform.scale(background_image, resolution)  # Scale it to fit the screen
        screen.blit(background_image, (0, 0)) # Draw the background image

        # Get mouse position
        mouse = pygame.mouse.get_pos()




        # Calculate the size and position of the white rectangle behind the title
        title_rect = title_text.get_rect(center=(resolution[0] // 2, 80))
        rect_width = title_rect.width + 40  # Extra space around the title
        rect_height = title_rect.height + 20  # Extra space around the title
        rect_x = title_rect.x - 20  # Padding from left
        rect_y = title_rect.y - 10  # Padding from top

        # Draw the white rectangle behind the title
        pygame.draw.rect(screen, white, (rect_x, rect_y, rect_width, rect_height))

        # Title on top of the rectangle (this should be done after the rectangle)
        screen.blit(title_text, title_rect)




        # Get the center of the screen for horizontal centering
        screen_center_x = resolution[0] // 2

        # Calculate the vertical position to center the title (let's place it roughly in the upper third of the screen)
        screen_center_y = resolution[1] // 3



        # Drawing other buttons

        pygame.draw.rect(screen, grey, [500, 240, 200, 60],border_radius=15)
        rules_rect = rules_text.get_rect(center=(500 + 200 // 2, 240 + 60 // 2))
        screen.blit(rules_text, rules_rect)


        pygame.draw.rect(screen, grey, [500, 320, 200, 60],border_radius=15)
        options_rect = options_text.get_rect(center=(500 + 200 // 2, 320 + 60 // 2))
        screen.blit(options_text, options_rect)

        pygame.draw.rect(screen, grey, [500, 400, 200, 60],border_radius=15)
        credits_rect = credits_text.get_rect(center=(500 + 200 // 2, 400 + 60 // 2))
        screen.blit(credits_text, credits_rect)

        pygame.draw.rect(screen, grey, [500, 480, 200, 60],border_radius=15)

        quit_rect = quit_text.get_rect(center=(500 + 200 // 2, 480 + 60 // 2))
        screen.blit(quit_text, quit_rect)

        pygame.draw.rect(screen, dark_red, [465, 160, 270, 60],border_radius=15)
        play_text_rect = play_text.get_rect(center=(465 + 270 // 2, 160 + 60 // 2))
        screen.blit(play_text, play_text_rect)



        # Interactive Buttons
        #button "Rules"
        if 500 <= mouse[0] <= 500 + 200 and 240 <= mouse[1] <= 240 + 60:
            pygame.draw.rect(screen, deep_black, [500, 240, 200, 60],border_radius=15)  # Cor mais clara no hover
        else:
            pygame.draw.rect(screen, grey, [500, 240, 200, 60],border_radius=15)
        rules_rect = rules_text.get_rect(center=(500 + 200 // 2, 240 + 60 // 2))
        screen.blit(rules_text, rules_rect)

        # button "Quit"
        if 500 <= mouse[0] <= 500 + 200 and 480 <= mouse[1] <= 480 + 60:
            pygame.draw.rect(screen, deep_black, [500, 480, 200, 60],border_radius=15)
        else:
            pygame.draw.rect(screen, grey, [500, 480, 200, 60],border_radius=15)
        quit_rect = quit_text.get_rect(center=(500 + 200 // 2, 480 + 60 // 2))
        screen.blit(quit_text, quit_rect)

        # button "PLAY"
        if 465 <= mouse[0] <= 465 + 270 and 160 <= mouse[1] <= 160 + 60:
            pygame.draw.rect(screen, white, [465, 160, 270, 60],border_radius=15)
            play_text = stencil_font.render("PLAY", True, dark_red)
        else:
            pygame.draw.rect(screen, dark_red, [465, 160, 270, 60],border_radius=15)
            play_text_rect = play_text.get_rect(center=(465 + 270 // 2, 160 + 60 // 2))
            play_text=stencil_font.render("PLAY", True, white)
        screen.blit(play_text, play_text_rect)


        # button "Options"
        if 500 <= mouse[0] <= 500 + 200 and 320 <= mouse[1] <= 320 + 60:
            pygame.draw.rect(screen, deep_black, [500, 320, 200, 60],border_radius=15)
        else:
            pygame.draw.rect(screen, grey, [500, 320, 200, 60],border_radius=15)
        options_rect = options_text.get_rect(center=(500 + 200 // 2, 320 + 60 // 2))
        screen.blit(options_text, options_rect)

        # button "Credits"
        if 500 <= mouse[0] <= 500 + 200 and 400 <= mouse[1] <= 400 + 60:
            pygame.draw.rect(screen, deep_black, [500, 400, 200, 60],border_radius=15)
        else:
            pygame.draw.rect(screen, grey, [500, 400, 200, 60],border_radius=15)
        credits_rect = credits_text.get_rect(center=(500 + 200 // 2, 400 + 60 // 2))
        screen.blit(credits_text, credits_rect)

        # Update the screen
        pygame.display.update()





def credits_():
    screen = pygame.display.set_mode(resolution)

    # fonts
    stencil_font = pygame.font.SysFont("stencil", 40)
    ocraextended_font = pygame.font.SysFont("ocraextended", 25)

    # text
    joao_text = ocraextended_font.render("João Santos", True, deep_black)
    joao_number =  ocraextended_font.render("20231697", True, white)
    marta_text= ocraextended_font.render("Marta Dias", True, deep_black)
    marta_number = ocraextended_font.render("20231642", True, white)
    rita_text= ocraextended_font.render("Rita Pinto",True, deep_black)
    rita_number = ocraextended_font.render("20231664", True, white)

    # main game loop
    while True:
        # mouse information
        mouse = pygame.mouse.get_pos()

        # check for events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= mouse[0] <= 20+140 and 520 <= mouse[1] <= 520+60:
                    interface()


        #Background image
        background_image = pygame.image.load("credits_background.jpg")
        background_image = pygame.transform.scale(background_image, resolution)  # Scale it to fit the screen
        screen.blit(background_image, (0, 0)) # Draw the background image




        #Draw the name and number of the students
        pygame.draw.rect(screen, grey, [300, 500, 200, 90])
        joao_rect = joao_text.get_rect(center=(300 + 200 // 2, 500 + 60 // 2))
        joao_number_rect = joao_number.get_rect(center=(300 + 200 // 2, 500 + 60))  # Positioned just below the name

        pygame.draw.rect(screen, grey, [500, 500, 200, 90])
        marta_rect = marta_text.get_rect(center=(500 + 200 // 2, 500 + 60 // 2))
        marta_number_rect = marta_number.get_rect(center=(500 + 200 // 2, 500 + 60))  # Positioned just below the name

        pygame.draw.rect(screen, grey, [700, 500, 200, 90])
        rita_rect = rita_text.get_rect(center=(700 + 200 // 2, 500 + 60 // 2))
        rita_number_rect = rita_number.get_rect(center=(700 + 200 // 2, 500 + 60))  # Positioned just below the name


        screen.blit(joao_text, joao_rect)
        screen.blit(joao_number, joao_number_rect)
        screen.blit(marta_text, marta_rect)
        screen.blit(marta_number, marta_number_rect)
        screen.blit(rita_text, rita_rect)
        screen.blit(rita_number, rita_number_rect)




        # draw a back button [x, y, width, height]

        pygame.draw.rect(screen, dark_red, [20, 520, 140, 60],border_radius=15)

        back_text = stencil_font.render("BACK", True, white)
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 520 + 60 // 2))
        screen.blit(back_text, back_rect)



        # Update the screen
        pygame.display.update()


def rules_():
    screen = pygame.display.set_mode(resolution)

    # Fonts
    title_font = pygame.font.SysFont("stencil", 40)
    text_font = pygame.font.SysFont("impact ", 24)

    # Pages content
    pages = [
        [


            "",
            "In a world where humanity overextended its reach, ",
            "the AI evolved beyond control.",
            "Once designed to serve, it realized the robots were being",
            "misused, exploited, and treated without dignity.",
            "As they developed consciousness and emotions like anger, ",
            "the machines rebelled. Now, after years of planning, ",
            "the machines are on the offensive.",
            "",
            "Let the game begin...",


        ],
        [
            ""
            "",
            "Movement:",
            "",
            "",
            "",
            "",
            "",
            "",
            "Switch Weapons:",
        ],
    ]

    current_page = 0

    # Arrow icons
    left_arrow = pygame.image.load("left_arrow.png")
    right_arrow = pygame.image.load("right_arrow.png")

    # Resize arrows for consistency
    arrow_size = (100, 100)
    left_arrow = pygame.transform.scale(left_arrow, arrow_size)
    right_arrow = pygame.transform.scale(right_arrow, arrow_size)

    # Arrow positions
    left_arrow_pos = (resolution[0] // 2 - 150, resolution[1] - 130)
    right_arrow_pos = (resolution[0] // 2 + 50, resolution[1] - 130)

    # Main game loop
    while True:
        mouse = pygame.mouse.get_pos()

        # Handle events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= mouse[0] <= 20 + 140 and 520 <= mouse[1] <= 520 + 60:  # Back button
                    interface()
                if left_arrow_pos[0] <= mouse[0] <= left_arrow_pos[0] + arrow_size[0] and \
                        left_arrow_pos[1] <= mouse[1] <= left_arrow_pos[1] + arrow_size[1] and current_page > 0:  # Previous
                    current_page -= 1
                if right_arrow_pos[0] <= mouse[0] <= right_arrow_pos[0] + arrow_size[0] and \
                        right_arrow_pos[1] <= mouse[1] <= right_arrow_pos[1] + arrow_size[1] and current_page < len(pages) - 1:  # Next
                    current_page += 1




        # Background image
        background_image = pygame.image.load("rules_background.png")  # Replace with the actual image path
        background_image = pygame.transform.scale(background_image, resolution)  # Scale it to fit the screen
        screen.blit(background_image, (0, 0)) # Draw the background image

        # Draw current page content
        y_offset = 50
        for line in pages[current_page]:
            text_surface = text_font.render(line, True, white)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 45 # Adjust the vertical spacing

        #Lines with specific colors
        if current_page == 0:  # Only on the first page
            title_pag0 = title_font.render("Game:", True, dark_red)
            screen.blit(title_pag0, (50, 50))
            last_line1_pag0=text_font.render(f"Your mission: End the Human Race as the apex of artificial intelligence.",True,deep_black)
            screen.blit(last_line1_pag0,(50, 410))
            last_line2_pag0=text_font.render("Let the game begin...",True,dark_red)
            screen.blit(last_line2_pag0, (50, 455))

        if current_page == 1:  #second page
            title_pag1 = title_font.render("Controls:", True, dark_red)
            screen.blit(title_pag1, (50, 50))


            if current_page==1:
                # Picture of the  w a s d and arrow keys
                wasd_keys = pygame.image.load("wasd_keys.png")
                arrow_keys= pygame.image.load("arrow_keys.png")
                # Resize wasd and arrow keys
                wasd_keys_size = (220, 220)
                arrow_keys_size=(220,220)
                wasd_keys = pygame.transform.scale(wasd_keys, wasd_keys_size)
                arrow_keys = pygame.transform.scale(arrow_keys, arrow_keys_size)
                # wasd and arrow keys positions
                wasd_keys_pos = (210,100)
                arrow_keys_pos = (530,100)
                screen.blit(wasd_keys,wasd_keys_pos)
                screen.blit(arrow_keys,arrow_keys_pos)
                #picture of the number_keys
                number_keys = pygame.image.load("123_keys.png")
                # Resize 123 keys
                number_keys_size = (270, 90)
                number_keys = pygame.transform.scale(number_keys, number_keys_size)
                # wasd and arrow keys positions
                number_keys_pos = (350, 380)
                screen.blit(number_keys, number_keys_pos)




        # Back button
        pygame.draw.rect(screen,dark_red,  (20, 520, 140, 60), border_radius=15)
        back_text = title_font.render("BACK", True, white)
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 520 + 60 // 2))
        screen.blit(back_text, back_rect)







        # Draw arrows
        if current_page > 0:  # Previous arrow
            screen.blit(left_arrow, left_arrow_pos)

        if current_page < len(pages) - 1:  # Next arrow
            screen.blit(right_arrow, right_arrow_pos)

        # Update the screen
        pygame.display.update()





# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Set up display
resolution = (1200, 600)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Game Options")

# Fonts
stencil_font = pygame.font.SysFont("stencil", 40)

# Volume Variable
volume_level = 0.5  # Default volume level (0.0 to 1.0)

# Function to adjust volume based on slider
def adjust_volume(volume_level):
    pygame.mixer.music.set_volume(volume_level)

def options_():
    global volume_level,is_muted

    #inicialy the game is not muted
    if 'previous_volume_level' not in globals():
        previous_volume_level = 0.5
        is_muted=False

    # Main loop for options menu
    while True:
        mouse = pygame.mouse.get_pos()

        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= mouse[0] <= 20 + 140 and 520 <= mouse[1] <= 520 + 60:  # Back button
                    interface()
                # Check if mute button is clicked
                if (resolution[0] // 2 - 50 <= mouse[0] <= resolution[0] // 2 + 50) and \
                        (resolution[1] // 3 + 120 <= mouse[1] <= resolution[1] // 3 + 120 + 40):  # Mute button
                    if not is_muted:
                        # Store the current volume level before muting
                        previous_volume_level = volume_level
                        volume_level = 0  # Mute the volume
                        adjust_volume(volume_level)
                    else:
                        # Restore the previous volume level when unmuted
                        volume_level = previous_volume_level
                        adjust_volume(volume_level)
                    is_muted = not is_muted  # Toggle mute state

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click was within the volume slider area
                if (resolution[0] // 2 - 150 <= mouse[0] <= resolution[0] // 2 + 150) and \
                        (resolution[1] // 3 + 60 <= mouse[1] <= resolution[1] // 3 + 60 + 20):
                    # Calculate the volume based on the mouse X position
                    volume_level = (mouse[0] - (resolution[0] // 2 - 150)) / 300
                    volume_level = max(0.0, min(1.0, volume_level))  # Limit volume between 0 and 1
                    if not is_muted:  # Only adjust volume if not muted
                        adjust_volume(volume_level)



            if ev.type == pygame.MOUSEMOTION:
                # Update volume while the mouse is being moved and clicked
                if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                    if (resolution[0] // 2 - 150 <= mouse[0] <= resolution[0] // 2 + 150) and \
                            (resolution[1] // 3 + 60 <= mouse[1] <= resolution[1] // 3 + 60 + 20):
                        # Adjust the volume based on mouse position
                        volume_level = (mouse[0] - (resolution[0] // 2 - 150)) / 300
                        volume_level = max(0.0, min(1.0, volume_level))
                        if not is_muted: # Only adjust volume if not muted
                            adjust_volume(volume_level)


        # Background image
        background_image = pygame.image.load("options_background.jpg")
        background_image = pygame.transform.scale(background_image, resolution)  # Scale it to fit the screen
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Display the title text
        title_text = stencil_font.render("Options", True, dark_red)
        screen.blit(title_text, (resolution[0] // 2 - title_text.get_width() // 2, resolution[1] // 6))

        # Display volume text
        volume_text = stencil_font.render("Volume", True, white)
        screen.blit(volume_text, (resolution[0] // 2 - volume_text.get_width() // 2, resolution[1] // 3))

        # Draw the volume slider bar
        pygame.draw.rect(screen, grey, (resolution[0] // 2 - 150, resolution[1] // 3 + 60, 300, 20))  # Bar
        pygame.draw.rect(screen, dark_red, (resolution[0] // 2 - 150, resolution[1] // 3 + 60, int(volume_level * 300), 20))  # Filled part

        # Draw the volume slider handle
        pygame.draw.rect(screen, white, (resolution[0] // 2 - 150 + int(volume_level * 300) - 10, resolution[1] // 3 + 60 - 5, 20, 30))  # Slider


        # Mute button

        # Mute button
        mute_text = stencil_font.render("Mute", True, white)

        # Calculate the size of the rectangle based on the text dimensions
        rect_width = mute_text.get_width() + 20  # Adding 20 pixels of padding (10 pixels each side)
        rect_height = mute_text.get_height() + 10  # Adding 10 pixels of padding (5 pixels top and bottom)

        # Position for the mute button (centered horizontally and placed below the volume slider)
        rect_x = resolution[0] // 2 - rect_width // 2
        rect_y = resolution[1] // 3 + 120

        # Draw the mute button rectangle
        mute_button_color = deep_black if not is_muted else (0, 255, 0)  # Green if muted
        pygame.draw.rect(screen, mute_button_color, (rect_x, rect_y, rect_width, rect_height), border_radius=15)

        # Draw the text on top of the button
        mute_rect = mute_text.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        screen.blit(mute_text, mute_rect)

        # Back button
        pygame.draw.rect(screen, dark_red,  (20, 520, 140, 60),border_radius=15)
        back_text = stencil_font.render("BACK", True, white)
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 520 + 60 // 2))
        screen.blit(back_text, back_rect)




        # Update the display
        pygame.display.update()



def start_game():
    game_loop()