import pygame
from config import *
from utils import *
from shop import *


def map(player):
    from interface import interface  # Prevent circular import
    #Setup of the background and screen
    background = pygame.image.load("map.jpg")
    background = pygame.transform.scale(background, resolution)
    screen = pygame.display.set_mode(resolution)
    clock=pygame.time.Clock()

    #Set the players position to thr left of the screen
    #player.rect.left=0
    player_group=pygame.sprite.Group()
    player_group.add(player)

    shop_area = pygame.Rect(400, 250, 200, 100)

    running=True
    in_shop = False

    while running:
        clock.tick(fps)
        screen.blit(background,(0,0))
        
        mouse = pygame.mouse.get_pos()
        #event handling
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        interface()  # Go back to the main interface (menu)

        #update their position
        player.update()

        #Detect the collision with the shop
        if shop_area.colliderect(player.rect):
            in_shop = True
            shop(player)

        #draw the player
        player_group.draw(screen)

        font = pygame.font.SysFont("segoeuiblack", 30)

        # Back button
        back_button = pygame.Rect(resolution[0] - 200, resolution[1] - 100, 150, 50)
        pygame.draw.rect(screen, deep_black, back_button, border_radius=10)
        back_text = font.render("MENU", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        #draw the player
        player_group.draw(screen)

        pygame.display.flip()

        if not in_shop:
            pass



