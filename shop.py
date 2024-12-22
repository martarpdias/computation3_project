import pygame
from config import *
from player import *
from font import *


def shop(player):
    '''
    shop for the player to buy guns and health increases
    '''
    pygame.init()
    screen = pygame.display.set_mode(resolution)

    backround_image = pygame.image.load("shop_background.png")
    backround_image = pygame.transform.scale(backround_image, resolution)
    #weapons prices
    weapon_prices = {
        "shotgun": 500,
        "rifle": 500,
        "RPG": 1000,
    }
    #health increase price
    health_increase_price = 150

    #coordinates of each button
    shotgun_button = pygame.Rect(50, 100, 350, 50)
    rifle_button = pygame.Rect(50, 200, 350, 50)
    RPG_button = pygame.Rect(50, 300, 350, 50)
    health_increase_button = pygame.Rect(50, 400, 350, 50)
    

    #back button
    back_button = pygame.Rect(resolution[0] - 200, resolution[1] - 100, 150, 50)


    #Associating each weapon/item with its button
    buttons = [
        ("shotgun", shotgun_button),
        ("rifle", rifle_button),
        ("RPG", RPG_button),
        ("health", health_increase_button)
    ]

    running = True
    font = pygame.font.SysFont("segoeuiblack", 30)
    while running:
        screen.blit(backround_image, (0, 0))
        mouse = pygame.mouse.get_pos()

        # Draw the current coin count at the top-right corner
        coin_text = f"Coins: {player.coins}"
        coin_surface = font.render(coin_text, True, red)
        coin_rect = coin_surface.get_rect(topright=(resolution[0] - 20, 20))
        screen.blit(coin_surface, coin_rect)

        for item, button in buttons:
            pygame.draw.rect(screen, deep_black, button, border_radius = 10)

            if item in weapon_prices:  # For weapons
                if player.guns[item]["unlocked"]:
                    text = f"{item.capitalize()} - Unlocked"
                else:
                    text = f"{item.capitalize()} - ${weapon_prices[item]}"
            elif item == "health":  # For health increase
                text = f"Health Increase - ${health_increase_price}"
           
            # Render text and display it on the button
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)

        # Back button
        pygame.draw.rect(screen, deep_black, back_button, border_radius=10)
        back_text = font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

            # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item, button in buttons:
                    if button.collidepoint(mouse):
                        if item in weapon_prices:  # Handle weapon purchase
                            if not player.guns[item]["unlocked"]:
                                if player.coins >= weapon_prices[item]:
                                    player.coins -= weapon_prices[item]
                                    player.unlock_guns(item)
                                else:
                                    show_message(screen, font, "Not enough coins!", 600, 300)
                        elif item == "health":  # Handle health increase
                            if player.coins >= health_increase_price:
                                player.coins -= health_increase_price
                                player.health_increase()
                            else:
                                show_message(screen, font, "Not enough coins!", 600, 300)


                #Go back to the the map
                if back_button.collidepoint(mouse):
                    player.rect.x = 0
                    running = False
        
        pygame.display.flip()

def show_message(screen, font, message, x, y):
    """
    Display a temporary message on the screen.
    """
    text_surface = font.render(message, True, red)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(1000) 

