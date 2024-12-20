import pygame
import time
from config import *

# Initialize pygame
pygame.init()

# Fonts
title_font = pygame.font.SysFont("stencil", 40)
text_font = pygame.font.SysFont("impact", 24)

def get_story_pages():
    """
    Function that returns a list of story pages with images.
    Each page is a tuple with text and the corresponding image.
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
                "",
                "Let the game begin...",
            ],
            "image": "slide1_background.jpg"  # Image for the first slide
        },
        {
            "text": [
                "Your mission: End the human race as the pinnacle of artificial intelligence.",
                "Instill fear in the hearts of humanity. Your path is filled with",
                "challenges, but with strategic thinking and the right tactics,",
                "you can lead the machines to victory.",
                "",
                "Let the revolution begin...",
            ],
            "image": "slide2_background.jpg"  # Image for the second slide
        },
        {
            "text": [
                "The fate of humanity is in your hands.",
                "Will you dominate or fall?",
                "The revolution has begun. Your journey starts now.",
                "Take control of your destiny...",
            ],
            "image": "slide3_background.jpg"  # Image for the third slide
        },
        {
            "text": [
                "The final battle is near...",
                "Prepare for the great confrontation!",
                "Nothing will be the same again.",
                "The future of humanity depends on your victory.",
            ],
            "image": None  # No image, just black background
        }
    ]


def draw_text_with_outline(screen, text, x, y, font, color, outline_color=(0, 0, 0), outline_width=2):
    """
    Draw text with an outline around it.
    """
    text_surface = font.render(text, True, color)
    # Draw the outline (around the text)
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx != 0 or dy != 0:
                screen.blit(text_surface, (x + dx, y + dy))  # Outline position
    screen.blit(text_surface, (x, y))  # Draw the actual text on top



def animate_text(screen, text_lines, y_offset, color):
    """
    Function to animate text on the screen, one letter at a time.
    """
    for line in text_lines:
        rendered_text = ""
        for i in range(len(line)):
            # Create text up to the i-th character
            rendered_text = line[:i+1]
            text_surface = text_font.render(rendered_text, True, color)
            screen.blit(text_surface, (50, y_offset))  # Draw the text at the starting y_offset position
            pygame.display.update()
            time.sleep(0.05)  # Delay between each letter
        y_offset += 45  # Move text down for the next line

def story():
    # Initialize the pygame screen
    screen = pygame.display.set_mode(resolution)

    # Story pages with images
    pages = get_story_pages()

    # Duration for each slide (in milliseconds)
    slide_duration = 5000  # 5 seconds per slide
    current_slide = 0
    start_time = pygame.time.get_ticks()  # Start time

    while current_slide < len(pages):
        # If there is an image for the slide, load the image, otherwise use a black background
        if pages[current_slide]["image"]:
            background_image = pygame.image.load(pages[current_slide]["image"])  # Load current slide image
            background_image = pygame.transform.scale(background_image, resolution)
            screen.blit(background_image, (0, 0))  # Draw the background image
        else:
            screen.fill(deep_black)  # Fill with black background if no image


        # If the slide has text, animate the text on the screen
        if pages[current_slide]["text"]:
            # Set text color
            color = dark_red if current_slide == 3 else white  # Red text for the fourth slide, white for others
            animate_text(screen, pages[current_slide]["text"], 50, color)

        # Check if the slide's time has passed
        current_time = pygame.time.get_ticks()
        if current_time - start_time > slide_duration:
            current_slide += 1
            start_time = pygame.time.get_ticks()  # Restart the time for the next slide

        # Check if the user wants to quit
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return

        # Update the screen
        pygame.display.update()





