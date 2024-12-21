from config import *
import math
import pygame
import random

from shed import shed
from enemy import *
from player import Player
from bullet import Bullet
from invicibility import Invincibility
from deSpawner import DeSpawner
from velocity import Velocity
from chests import Chest


def game_loop():
    player = Player()
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)

def execute_game(player: Player):
    """
    Main function to execute the game loop, with round transitions.
    """
    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Setting up the screen and background
    screen = pygame.display.set_mode((resolution))

    background = pygame.image.load("game_background.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Player setup
    player_group = pygame.sprite.Group()
    player_group.add(player)
    score = 0

    #Initialize bullets
    bullets=pygame.sprite.Group()
    enemy_bullets=pygame.sprite.Group()

    # Initialize the enemy group
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = fps * 2

    # Initialize power-ups
    power_ups = pygame.sprite.Group()
    power_up_spawn_timer = 0

    #Initialize chests and set a delay of 10 seconds for the spawn
    chests = pygame.sprite.Group()
    chest_spwan_delay = 10000
    last_chest_spwan_time = pygame.time.get_ticks()

    # Round management
    current_round = 1
    final_round = 10
    round_time = 20  # seconds per round
    start_time = pygame.time.get_ticks()  # Get initial time for the round    

    # Initialize lists for active power-ups
    active_power_ups = []

    running = True
    while running:
        # Control the frame rate
        clock.tick(fps)

        # Draw the background
        screen.blit(background, (0, 0))

        # Calculate remaining time
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
        time_left = max(0, round_time - elapsed_time)

        # Update player
        player_group.update()

        
        # Handle power-ups
        # Spawn power-ups
        if not active_power_ups:  # Check if there are no active power
            if power_up_spawn_timer <= 0:
                if random.random() < 0.2:  # 20% chance to spawn a power-up
                    x, y = random.randint(50, width - 50), random.randint(50, height - 50)
                    new_power_up = random.choice([Invincibility(x, y), Velocity(x, y), DeSpawner(x, y)])
                    power_ups.add(new_power_up)
                power_up_spawn_timer = fps * 5  # Reset the power-up timer
            power_up_spawn_timer -= 1

        # Check for collisions between the player and power-ups
        collided_power_ups = pygame.sprite.spritecollide(player, power_ups, True)  # `True` removes collided power-ups
        for power_up in collided_power_ups:
            power_up.affect_player(player)  # Apply power-up effect to the player
            power_up.affect_game(locals())  # Apply power-up effect to the game
            power_up.start_time_use = pygame.time.get_ticks()  # Start usage timer after collision
            active_power_ups.append(power_up)  # Add the power-up to active list

        # Check for expired power-ups (before collision)
        for power_up in list(power_ups):  # Iterate over all visible power-ups
            if power_up.is_expired():
                power_up.kill()  # Remove the power-up sprite from the screen

        # Check for expired power-ups (after collision)
        for power_up in active_power_ups[:]:  # Iterate over a copy to allow removal
            if power_up.use_expired():
                power_up.remove_effects(player, locals())  # Remove power-up effects
                active_power_ups.remove(power_up)  # Remove from active list

    

        
        
        # Update power-ups
        power_ups.update()

        # Draw power-ups
        power_ups.draw(screen)



        # Calculate the width of the time bar
        bar_width = int((time_left / round_time) * (width - 40))  # Proportional to remaining time

        # Set the color of the time bar (optional: green -> yellow -> red transition)
        if time_left > round_time * 0.5:
            bar_color = (0, 255, 0)  # Green
        elif time_left > round_time * 0.2:
            bar_color = (255, 165, 0)  # Orange
        else:
            bar_color = (255, 0, 0)  # Red


        # Add rounded corners to the time bar
        pygame.draw.rect(screen, (255, 255, 255), (20, height - 40, width - 40, 25), border_radius=10)  # Background bar
        pygame.draw.rect(screen, bar_color, (30, height - 35, bar_width, 15), border_radius=10)  # Time bar with rounded corners

        # Display the numerical time remaining
        font = pygame.font.SysFont("segoeuiblack", 20)
        time_text = font.render(f"Time: {int(time_left)}s", True, (255, 255, 255))
        screen.blit(time_text, (25, height - 70))

        if elapsed_time >= round_time:
            # Show transition screen
            show_transition_screen(screen)

            # Reset the timer and increase difficulty
            start_time = pygame.time.get_ticks()
            current_round += 1
            player.health = min(100, int(player.health + player.health/3))  # Reset player health
            for enemy in enemies:
                enemy.kill()
            for bullet in bullets:
                bullet.kill()
            for power_up in power_ups:
                power_up.kill()
        
        # Enemy spawning according to the round
        if enemy_spawn_timer<=0:
            if current_round == 1:
                enemy_spawn_rate = fps * 2
                enemies.add(Enemy())
                enemy_spawn_timer = enemy_spawn_rate
            elif current_round == 2:
                enemy_spawn_rate = fps * 1.5
                enemies.add(Enemy())
                enemy_spawn_timer = enemy_spawn_rate
            elif current_round == 3:
                enemy_spawn_rate = fps * 2
                enemy_type = random.choice([Enemy, fast_enemy])
                new_enemy = enemy_type()
                enemies.add(new_enemy)
                enemy_spawn_timer = enemy_spawn_rate
            elif current_round == 4:
                enemy_spawn_rate = fps * 1.5
                enemy_type = random.choice([Enemy, fast_enemy])
                new_enemy = enemy_type()
                enemies.add(new_enemy)
                enemy_spawn_timer = enemy_spawn_rate
            elif current_round == 5:
                enemy_spawn_rate = fps * 2
                enemy_type = random.choice([Enemy, fast_enemy, shooter_rastreio])
                new_enemy = enemy_type()
                enemies.add(new_enemy)
                enemy_spawn_timer = enemy_spawn_rate
        enemy_spawn_timer -= 1


        # Display round number
        round_text = font.render(f"Round: {current_round}", True, (255, 255, 255))
        screen.blit(round_text, (160, 45))

        # Draw player health bar
        player_health_bar_width = int((player.health / 100) * (width / 3))  # Scale health to a third of the screen width
        pygame.draw.rect(screen, (255, 0, 0), (15, 20, (width / 3), 20), border_radius=10)  # Background for the health bar
        pygame.draw.rect(screen, (0, 255, 0), (15, 20, player_health_bar_width, 20), border_radius=10)  # Player health bar

        # Display the numerical life remaining
        life_text = font.render(f"Life: {int(player.health)}%", True, (255, 255, 255))
        screen.blit(life_text, (25, 45))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Switch guns
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.switch_guns("pistol")
                elif event.key == pygame.K_2:
                    player.switch_guns("rifle")
                elif event.key == pygame.K_3:
                    player.switch_guns("shotgun")
                elif event.key == pygame.K_4:
                    player.switch_guns("RPG")

        for enemy in enemies:
            if isinstance(enemy, shooter_rastreio):
                enemy.shoot(enemy_bullets, player)
                pass
        
        #shooting
        player.shoot(bullets)

        

        #Spawning the chests
        current_time = pygame.time.get_ticks()
        if current_time - last_chest_spwan_time > chest_spwan_delay:
            if random.random() < 0.05:
                new_chest = Chest()
                new_chest.spawner()
                chests.add(new_chest)
                last_chest_spwan_time = current_time


        #spawning the enemies
        if enemy_spawn_timer<=0:
            enemy_type = random.choice([Enemy, fast_enemy, shooter_rastreio])
            new_enemy = enemy_type()
            enemies.add(new_enemy)
            enemy_spawn_timer = enemy_spawn_rate

        # Checking for collisions between bullets and enemies
        for bullet in bullets:
            if isinstance(bullet, RPG_rocket):
                collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
                if collided_enemies:
                    bullet.explosion(enemies)
                    bullet.kill()
                    
            else:
                collided_enemies = pygame.sprite.spritecollide(bullet, enemies, True)            
                for enemy in collided_enemies:
                    enemy.health -= bullet.damage  # Decrease health by bullet damage
                    bullet.kill()  # Destroy the bullet
                    if enemy.health <= 0:
                        enemy.kill()  # Destroy the enemy
                        score += 100

        # Checking for collisions between bullets and players
        for bullet in enemy_bullets:
            collided_player = pygame.sprite.spritecollideany(bullet, player_group)
            if player.invincible == False and collided_player:
                player.health -= 5  # Decrease health by 1 for each hit
                bullet.kill()  # Destroy the bullet
            elif player.invincible == True and collided_player:
                bullet.kill()

        #check for collision between chest and player
        collided_chest = pygame.sprite.spritecollide(player, chests, False)
        for chest in collided_chest:
                rewards = chest.open()
                if rewards:
                    selected_reward = chest.display_rewards_options(screen, rewards, player, enemies)
                   
        chests.draw(screen)

        # Update the enemy spawn timer
        enemy_spawn_timer -= 1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)
        enemy_bullets.update()

        # Check collisions between player and enemies
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in collided_enemies:
            player.take_damage(enemy.damage)

        # Check if the player's speed boost has expired
        player.check_speed_boost()

        #check if the player's fire rate inrease has expired
        player.check_fire_rate_increase()

        player_group.update()


        # Check if the player is dead
        if player.health <= 0:
            show_game_over_screen(screen)
    
        # Checking if the user goes into the shed area
        if player.rect.right >= width:
            # Change the game state to shed
            return "shed"

        # Draw game objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for bullet in enemy_bullets:
            bullet.draw(screen)

        # Draw health bars for enemies
        enemy_health_bar_max_width = 50  # Maximum width of the health bar
        for enemy in enemies:
            enemy_health_bar_width = int((enemy.health / enemy.max_health) * enemy_health_bar_max_width)  # Scale enemy health to the max width
            pygame.draw.rect(screen, (255, 0, 0), (enemy.rect.x, enemy.rect.y - 10, 50, 5))  # Background bar
            pygame.draw.rect(screen, (0, 255, 0), (enemy.rect.x, enemy.rect.y - 10, enemy_health_bar_width, 5))  # Enemy health bar

        # Display the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
        screen.blit(score_text, (295, 45))  # Display the score at the top-left corner

        # Update groups
        player_group.update()
        bullets.update()
        enemies.update(player)
        power_ups.update()

        # Draw objects
        player_group.draw(screen)
        enemies.draw(screen)
        power_ups.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Display the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (295, 45))

        # Update the display
        pygame.display.flip()

#pause game function
def pause(screen, width, height):
    screen = pygame.display.set_mode((resolution))
    font = pygame.font.SysFont("segoeuiblack", 100)
    text = font.render("Paused", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    # Display the text at the center
    screen.blit(text, text_rect)
    pygame.display.flip()

    #loop to keep the game paused until the player unpauses
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False        
        



def show_transition_screen(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("segoeuiblack", 50)
    text = font.render("Round completed!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def show_game_over_screen(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("segoeuiblack", 50)
    text = font.render("Game Over!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(resolution[0] // 2, resolution[1] // 2))
    screen.blit(text, text_rect)

    # Restart button
    restart_button = pygame.Rect(resolution[0] // 2 - 100, resolution[1] // 2 + 100, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), restart_button)
    font = pygame.font.SysFont("segoeuiblack", 30)
    restart_text = font.render("Restart", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

    pygame.display.update()

    # Wait for interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return "restart" #is not working yet

