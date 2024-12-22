# game.py
import pygame
from config import *
from player import Player
from map import map
from game import *

def game_loop():
    player = Player()
    screen = pygame.display.set_mode((width, height))
    current_state = "map"
    current_level = None

    while True:
        if current_state == "map":
            # Handle map state
            result = map(player)
            if isinstance(result, int):  # If a level number was returned
                current_level = result
                current_state = "level"
            
        elif current_state == "level":
            # Handle level state
            if current_level is not None:
                completed = execute_game(player, current_level)
                if completed and current_level + 1 in LEVELS:
                    LEVELS[current_level + 1]["unlock"] = True
                current_state = "map"
                current_level = None
        
        elif current_state == "game_over":
            result = show_game_over_screen(screen)
            if result == "restart":
                player = Player()
                current_state = "map"
                current_level = None