# Config file used to set global variables and other settings
import pygame
import os
# COLORS
dark_red = (138, 0, 0)  # Dark red for buttons
deep_black = (19, 20, 20)  # Almost black for background
grey = (59, 60, 60)  # Dark grey for alternate buttons
white = (254, 255, 255)  # White for readable text
glowing_light_red = (239, 128, 128)  # Light red for brighter text
red = (255, 0, 0)  # Red for errors
green = (0, 255, 0)  # Green for success
blue = (0, 0, 255)  # Blue for information
yellow = (255, 255, 0)  # Yellow for warnings
pink = (255, 192, 203)  # Pinkdi pink pink
glowing_yellow = (255, 255, 102)  # Glowing yellow 
purple = (128, 0, 128)  # Purple
orange = (255, 165, 0)  # Orange



# SCREEN RESOLUTION
resolution = (1200, 600) # Screen resolution
width, height = resolution[0], resolution[1] #for calculation
fps=60 

#resolve the issue of the window not appearing in the center of the screen
pygame.init()

# Get screen width and height
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Calculate the position to center the window
x_pos = (screen_width - resolution[0]) // 2
y_pos = (screen_height - resolution[1]) // 2

# Set the window position
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_pos},{y_pos}"

# Set up the screen with resolution from config
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("My Game")

#SIZES
player_size=(50,100)
enemy_size=40
bullet_size=10
