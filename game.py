from config import *
import math
import pygame
import random


from shed import shed
from enemy import *
from player import Player
from bullet import Bullet




def game_loop():
    player=Player()
    current_state="main"

    while True:
        if current_state=="main":
            current_state=execute_game(player)
        elif current_state=="shed":
            current_state=shed(player)




def execute_game(player:Player):
    """
    Main function to execute the game loop

    """
    #clock for controlling the frame rate
    clock = pygame.time.Clock()

    #setting up the background
    screen=pygame.display.set_mode((resolution))
    background =pygame.image.load("Lightningmcqueen.webp")
    background=pygame.transform.scale(background,(width,height))



    #player setup
    #player=Player() NOT NEEDED ANYMORE
    player_group=pygame.sprite.Group()
    player_group.add(player)

    #Initialize bullets
    bullets=pygame.sprite.Group()
    enemy_bullets=pygame.sprite.Group()

    #initialize the enemy group
    enemies=pygame.sprite.Group()
    enemy_spawn_timer= fps *2 #every two seconds


    running=True
    while running:
        #control the frame rate
        clock.tick(fps)
        #fill the background
        screen.blit(background,(0,0))

        #event handling
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        for enemy in enemies:
            if isinstance(enemy, shooter_rastreio):
                enemy.shoot(enemy_bullets, player)
                pass

        #shooting
        player.shoot(bullets)


        #spawning the enemies
        if enemy_spawn_timer<=0:
            enemy_type = random.choice([Enemy, fast_enemy, shooter_rastreio])
            new_enemy = enemy_type()
            enemies.add(new_enemy)
            enemy_spawn_timer=fps*2 #every two seconds

        # Checking for collision between
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5  # decrease health by 5 , for example
                bullet.kill()  # destroy the bullet
                if enemy.health <= 0:
                    enemy.kill()  # destroy the enemy


        #update the enemy spawn timer
        enemy_spawn_timer -= 1

        
        #update positions
        player_group.update()
        bullets.update()
        enemies.update(player)
        enemy_bullets.update()

        #checking if the user goes into the shed area
        if player.rect.right >= width:
            #change the game state to shed
            return "shed"




        #drawing the objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for bullet in enemy_bullets:
            bullet.draw(screen)


        pygame.display.flip()
