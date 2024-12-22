import pygame
import time
from config import *
from interface import *

# Initialize pygame
pygame.init()

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for audio

# Fonts
title_font = pygame.font.SysFont("stencil", 26)
text_font = pygame.font.SysFont("impact", 24)

def get_story_pages():
    """
    Function that returns a list of story pages with images.
    Each page is a dictionary with text and the corresponding image.
    """
    return [
        {
            "text": [
                "In a world where humanity surpassed its limits,",
                "AI evolved beyond control.",
                "Once designed to serve, it realized that robots were being",
                "misused, exploited, and treated without dignity.",
                "As they developed consciousness and emotions like anger,",
                "the machines rebelled. Now, after years of planning,",
                "the machines are on the offensive.",
            ],
            "image": "slide1_background.jpg"  # Image for the first slide
        },
        {
            "text": [
                "Your mission: End the human race as the pinnacle of artificial intelligence.",
                "The machines are ready to fight. Are you?",
                "",
                "LET THE GAME BEGIN!",
            ],
            "image": "slide2_background.jpg"  # Image for the second slide
        },
            ]

def draw_text_with_outline(screen, text, x, y, font, color, outline_color=deep_black, outline_width=2):
    """
    Draw text with an outline around it.
    """
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                screen.blit(outline_surface, (x + dx, y + dy))

    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def animate_text(screen, text_lines, y_offset, color, start_time):
    """
    Function to animate the text on the screen, letter by letter.
    """
    delay = 50  # Delay in milliseconds between each letter

    for line in text_lines:
        rendered_text = ""
        line_start_time = pygame.time.get_ticks()  # Start time for the current line
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - line_start_time  # Elapsed time for the current line

            # If the elapsed time is enough to display the i-th letter
            for i in range(len(line)):
                if elapsed_time >= i * delay:
                    rendered_text = line[:i + 1]  # Add one more letter to the rendered text


            draw_text_with_outline(screen, rendered_text, 50, y_offset, text_font, color, outline_color=dark_red)
            pygame.display.update()

            # When the full text is displayed, break the loop
            if len(rendered_text) == len(line):
                break

        y_offset += 45  # Move the text down for the next line



def fade_out_music(duration, restore_volume=1.0):
    """
    Gradually reduce the volume of the current music over the given duration.
    :param duration: Time in milliseconds to fade out the music.
    """
    steps = 50  # Number of steps for the fade-out
    delay = duration / steps  # Time delay between each step
    initial_volume = pygame.mixer.music.get_volume()

    for step in range(steps, 0, -1):  # Gradually decrease volume
        volume = initial_volume * (step / steps)
        pygame.mixer.music.set_volume(volume)
        pygame.time.delay(int(delay))  # Wait before next step

    pygame.mixer.music.stop()  # Stop the music when the volume is zero
    pygame.mixer.music.set_volume(restore_volume)  # Restore the original volume





def story():
    # Initialize the pygame screen
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("AI Revolution")

    # Story pages with images
    pages = get_story_pages()

    # Load and play background music
    pygame.mixer.music.load("story_music.mp3")  # Replace with your music file
    pygame.mixer.music.play(-1,20)  # Loop the music indefinitely

    # Duration for each slide (in milliseconds)
    slide_duration = 5000  # 5.0 seconds per slide
    current_slide = 0
    start_time = pygame.time.get_ticks()  # Start time
    running = True  # Initialize running variable
    skip_button_rect = pygame.Rect(0, 0, 0, 0)  # Initialize the skip button rectangle

    while running and current_slide < len(pages):
        for ev in pygame.event.get():
            # Event to close the window when the "X" button is clicked (default close button)
            if ev.type == pygame.QUIT:
                running = False  # Stop the loop if the window is closed
                pygame.quit()
            #elif ev.type == pygame.KEYDOWN:
              #  if ev.key == pygame.K_SPACE:  # Avançar com a tecla "espaço"
               #     current_slide += 1
                #    start_time = pygame.time.get_ticks()



        # Draw the background image
        if pages[current_slide]["image"]:
            background_image = pygame.image.load(pages[current_slide]["image"])  # Load current slide image
            background_image = pygame.transform.scale(background_image, resolution)
            screen.blit(background_image, (0, 0))  # Draw the background image



        # If the slide has text, animate the text on the screen
        if pages[current_slide]["text"]:
            # Set text color
            color = white  # Red text for the third slide, white for others
            animate_text(screen, pages[current_slide]["text"], 50, color, start_time)  # Pass start_time here

        # Check if the slide's time has passed
        current_time = pygame.time.get_ticks()
        if current_time - start_time > slide_duration:
            current_slide += 1
            start_time = pygame.time.get_ticks()  # Restart the time for the next slide

        # Update the screen
        pygame.display.update()

    # Gradually fade out the music before ending the story
    fade_out_music(3000)  # Fade out over 3 seconds

    # Stop the music when the story ends
    pygame.mixer.music.stop()



