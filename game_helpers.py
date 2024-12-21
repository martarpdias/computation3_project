import pygame
import random
from config import *
from enemy import Enemy, fast_enemy, shooter_rastreio
from invicibility import Invincibility
from velocity import Velocity 
from deSpawner import DeSpawner

def spawn_enemies(enemies, enemy_types, spawn_rate, max_enemies, last_spawn_time):
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= spawn_rate and len(enemies) < max_enemies:
        enemy_type = random.choice(enemy_types)
        new_enemy = enemy_type(random.randint(0, 800), 0)  # Adjust screen width/height as needed
        enemies.add(new_enemy)
        return current_time  # Update the last spawn time
    return last_spawn_time

def manage_power_ups(player, power_ups, active_power_ups, screen, power_up_spawn_timer, fps):
    if power_up_spawn_timer <= 0 and random.random() < 0.2:
        x, y = random.randint(50, 800), random.randint(50, 600)  # Adjust for your screen size
        new_power_up = random.choice([Invincibility(x, y), Velocity(x, y), DeSpawner(x, y)])
        power_ups.add(new_power_up)
        power_up_spawn_timer = fps * 5

    collided = pygame.sprite.spritecollide(player, power_ups, True)
    for power_up in collided:
        power_up.affect_player(player)
        power_up.start_time_use = pygame.time.get_ticks()
        active_power_ups.append(power_up)

    for power_up in active_power_ups[:]:
        if power_up.use_expired():
            power_up.remove_effects(player, locals())
            active_power_ups.remove(power_up)

    power_ups.update()
    power_ups.draw(screen)
    return power_up_spawn_timer

def handle_collisions(player, bullets, enemies, enemy_bullets, chests, score, power_ups):
    # Checking for collisions between bullets and enemies
    for bullet in bullets:
        if isinstance(bullet, RPG_rocket):  # If the bullet is a rocket
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            if collided_enemies:
                bullet.explosion(enemies)  # Cause explosion and damage nearby enemies
                bullet.kill()  # Destroy the rocket after explosion
        else:  # Regular bullet
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= bullet.damage  # Decrease enemy health
                bullet.kill()  # Destroy the bullet
                if enemy.health <= 0:
                    enemy.kill()  # Destroy the enemy
                    score += 100  # Add points for killing an enemy

    # Checking for collisions between enemy bullets and the player
    for bullet in enemy_bullets:
        if player.invincible:
            collided_player = pygame.sprite.spritecollideany(bullet, pygame.sprite.Group(player))
            if collided_player:
                bullet.kill()  # Destroy the bullet but no damage to the player
        else:
            collided_player = pygame.sprite.spritecollideany(bullet, pygame.sprite.Group(player))
            if collided_player:
                player.health -= 5  # Decrease player health
                bullet.kill()  # Destroy the bullet

    # Checking for collisions between the player and enemies
    collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in collided_enemies:
        enemy.deal_damage(player)  # Enemy deals damage to the player on collision

    # Checking for collisions between the player and chests
    collided_chests = pygame.sprite.spritecollide(player, chests, False)
    for chest in collided_chests:
        rewards = chest.open()  # Open the chest and get rewards
        if rewards:
            # Allow the player to choose a reward
            selected_reward = chest.display_rewards_options(screen=None, rewards=rewards, player=player, enemies=enemies)
            # Applying the selected reward to the player
            if selected_reward:
                if selected_reward["name"] == "health potion":
                    player.apply_health_potion(selected_reward["value"])
                elif selected_reward["name"] == "speed potion":
                    player.apply_speed_potion()
                elif selected_reward["name"] == "shield potion":
                    player.apply_shield_potion()
                elif selected_reward["name"] == "health increase":
                    player.health_increase()
                elif selected_reward["name"] == "fire rate increase":
                    player.fire_rate_increase()
                elif selected_reward["name"] == "doomsday device":
                    player.doomsday_device(enemies)
                elif selected_reward["name"] == "shotgun":
                    player.unlock_guns("shotgun")
                elif selected_reward["name"] == "rifle":
                    player.unlock_guns("rifle")

    # Checking for collisions between the player and power-ups
    collided_power_ups = pygame.sprite.spritecollide(player, power_ups, False)
    for power_up in collided_power_ups:
        # Apply the power-up's effect to the player
        power_up.affect_player(player)
        # Remove the power-up after it has been collected
        power_up.kill()

    return score


def draw_game_elements(screen, player, player_group, enemies, bullets, enemy_bullets, power_ups, chests, score, current_level, level_time, start_time):

    # Draw background (assuming it's loaded earlier in the main game loop)
    screen.fill((0, 0, 0))  # Fill the screen with black (or use an image as background)

    # Draw player and related elements
    player_group.draw(screen)

    # Draw enemies
    enemies.draw(screen)

    # Draw bullets (player's bullets and enemy's bullets)
    for bullet in bullets:
        bullet.draw(screen)
    
    for bullet in enemy_bullets:
        bullet.draw(screen)

    # Draw power-ups and display their timers if visible
    for power_up in power_ups:
        power_up.update()  # Update the pulsing effect
        screen.blit(power_up.image, power_up.rect)  # Draw power-up

        # If power-up is visible but hasn't been collected, show the remaining visibility time
        if not power_up.is_expired():
            remaining_time_before_use = (pygame.time.get_ticks() - power_up.start_time_before_use) // 1000
            font = pygame.font.SysFont("segoeuiblack", 20)
            time_text = font.render(f"{10 - remaining_time_before_use}s", True, (255, 255, 255))
            screen.blit(time_text, (power_up.rect.x, power_up.rect.y - 20))  # Timer above power-up

        # If power-up is collected and in use, display the remaining usage time
        elif power_up.start_time_use:
            remaining_time_use = (pygame.time.get_ticks() - power_up.start_time_use) // 1000
            font = pygame.font.SysFont("segoeuiblack", 20)
            time_text = font.render(f"{7 - remaining_time_use}s", True, (255, 255, 255))
            screen.blit(time_text, (power_up.rect.x, power_up.rect.y - 20))  # Timer above power-up

    # Draw chests
    chests.draw(screen)

    # Display the score at the top-left corner
    font = pygame.font.SysFont("segoeuiblack", 20)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (25, 45))

    # Display the current level
    level_text = font.render(f"Level: {current_level}", True, (255, 255, 255))
    screen.blit(level_text, (160, 45))

    # Calculate and display the remaining time for the level
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
    time_left = max(0, level_time - elapsed_time)
    time_text = font.render(f"Time: {int(time_left)}s", True, (255, 255, 255))
    screen.blit(time_text, (width - 150, 45))

    # Draw player health bar
    player_health_bar_width = int((player.health / 100) * (width / 3))  # Scale health bar width
    pygame.draw.rect(screen, (255, 0, 0), (15, 20, width / 3, 20), border_radius=10)  # Background for health bar
    pygame.draw.rect(screen, (0, 255, 0), (15, 20, player_health_bar_width, 20), border_radius=10)  # Player health bar

    # Display the player's health percentage
    life_text = font.render(f"Life: {int(player.health)}%", True, (255, 255, 255))
    screen.blit(life_text, (25, 70))

    # Draw health bars for each enemy
    enemy_health_bar_max_width = 50  # Maximum width for enemy health bars
    for enemy in enemies:
        enemy_health_bar_width = int((enemy.health / enemy.max_health) * enemy_health_bar_max_width)
        pygame.draw.rect(screen, (255, 0, 0), (enemy.rect.x, enemy.rect.y - 10, 50, 5))  # Background bar
        pygame.draw.rect(screen, (0, 255, 0), (enemy.rect.x, enemy.rect.y - 10, enemy_health_bar_width, 5))  # Enemy health bar

    # Calculate the width of the time bar
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
    time_left = max(0, level_time - elapsed_time)

    # Set the color of the time bar (optional: green -> yellow -> red transition)
    if time_left > level_time * 0.5:
        bar_color = (0, 255, 0)  # Green
    elif time_left > level_time * 0.2:
        bar_color = (255, 165, 0)  # Orange
    else:
        bar_color = (255, 0, 0)  # Red

    # Add rounded corners to the time bar
    pygame.draw.rect(screen, (255, 255, 255), (20, height - 40, width - 40, 25), border_radius=10)  # Background bar
    pygame.draw.rect(screen, bar_color, (30, height - 35, int((time_left / level_time) * (width - 40)), 15), border_radius=10)  # Time bar with rounded corners

    # Display the numerical time remaining
    font = pygame.font.SysFont("segoeuiblack", 20)
    time_text = font.render(f"Time: {int(time_left)}s", True, (255, 255, 255))
    screen.blit(time_text, (25, height - 70))

    # Update the display to show the drawn elements
    pygame.display.flip()


def handle_round_transition(current_level, level_time, start_time, player, enemies, bullets, power_ups, screen):
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if elapsed_time >= level_time:
        result = show_transition_screen(screen, current_level, lambda: map(player))
        if result == "next_round":
            current_level += 1
            start_time = pygame.time.get_ticks()
            player.health = min(100, player.health + player.health // 3)
            enemies.empty()
            bullets.empty()
            power_ups.empty()
        return current_level, start_time
    return current_level, start_time
