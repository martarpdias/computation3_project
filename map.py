import pygame
from config import *
from utils import *
from utils import under_construction
from shop import *


def map(player):
    # Setup of the background and screen
    background = pygame.image.load("map.jpg")
    background = pygame.transform.scale(background, resolution)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Set the player's position
    player_group = pygame.sprite.Group()
    player_group.add(player)

    shop_area = pygame.Rect(400, 250, 200, 100)

    running=True
    in_shop = False

    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Update the player's position
        player.update()

        #Detect the collision with the shop
        if shop_area.colliderect(player.rect):
            in_shop = True
            shop(player)

        

        # Draw the player
        player_group.draw(screen)

        pygame.display.flip()

        if not in_shop:
            pass



