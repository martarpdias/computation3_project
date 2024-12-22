from config import *
import pygame
import random

from map import map
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
        elif current_state == "map":
            current_state = map(player)

def spawn_enemies(enemies, enemy_types, spawn_rate, max_enemies, last_spawn_time):
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= spawn_rate and len(enemies) < max_enemies:
        enemy_type = random.choice(enemy_types)
        new_enemy = enemy_type(random.randint(0, resolution[0] - 50), 0)
        enemies.add(new_enemy)
        return current_time
    return last_spawn_time

def manage_power_ups(player, power_ups, active_power_ups, screen, power_up_spawn_timer):
    if power_up_spawn_timer <= 0 and random.random() < 0.2:
        x, y = random.randint(50, resolution[0] - 50), random.randint(50, resolution[1] - 50)
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
    for bullet in bullets:
        if isinstance(bullet, RPG_rocket):
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            if collided_enemies:
                bullet.explosion(enemies)
                bullet.kill()
        else:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= bullet.damage
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()
                    score += 100

    for bullet in enemy_bullets:
        if not player.invincible and pygame.sprite.spritecollideany(bullet, pygame.sprite.Group(player)):
            player.health -= 5
            bullet.kill()

    collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in collided_enemies:
        enemy.deal_damage(player)

    collided_chests = pygame.sprite.spritecollide(player, chests, False)
    for chest in collided_chests:
        rewards = chest.open()
        if rewards:
            selected_reward = chest.display_rewards_options(None, rewards, player, enemies)
            if selected_reward:
                handle_reward(selected_reward, player, enemies)

    return score

def handle_reward(reward, player, enemies):
    if reward["name"] == "health potion":
        player.apply_health_potion(reward["value"])
    elif reward["name"] == "speed potion":
        player.apply_speed_potion()
    elif reward["name"] == "shield potion":
        player.apply_shield_potion()
    elif reward["name"] == "health increase":
        player.health_increase()
    elif reward["name"] == "fire rate increase":
        player.fire_rate_increase()
    elif reward["name"] == "doomsday device":
        player.doomsday_device(enemies)
    elif reward["name"] == "shotgun":
        player.unlock_guns("shotgun")
    elif reward["name"] == "rifle":
        player.unlock_guns("rifle")

def pause(screen, width, height):
    font = pygame.font.SysFont("segoeuiblack", 100)
    text = font.render("Paused", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

def show_transition_screen(screen, current_level, width, height, map_callback=None):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont("segoeuiblack", 50)
    title_text = font.render(f"End of Level {current_level}", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(width // 2, height // 3))
    screen.blit(title_text, title_rect)

    button_width, button_height = 200, 60
    button_spacing = 50
    next_button_rect = pygame.Rect(
        (width // 2 - button_width - button_spacing // 2, height // 2),
        (button_width, button_height),
    )
    map_button_rect = pygame.Rect(
        (width // 2 + button_spacing // 2, height // 2),
        (button_width, button_height),
    )

    button_font = pygame.font.SysFont("segoeuiblack", 30)
    next_text = button_font.render("Next Round", True, (255, 255, 255))
    next_text_rect = next_text.get_rect(center=next_button_rect.center)
    map_text = button_font.render("Map", True, (255, 255, 255))
    map_text_rect = map_text.get_rect(center=map_button_rect.center)

    pygame.draw.rect(screen, (255, 0, 0), next_button_rect, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 255), map_button_rect, border_radius=10)
    screen.blit(next_text, next_text_rect)
    screen.blit(map_text, map_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    return "next_round"
                if map_button_rect.collidepoint(event.pos):
                    if map_callback:
                        map_callback()
                    return "map"

def show_game_over_screen(screen, width, height):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("segoeuiblack", 50)
    text = font.render("Game Over!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    restart_button = pygame.Rect(width // 2 - 100, height // 2 + 100, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), restart_button)
    font = pygame.font.SysFont("segoeuiblack", 30)
    restart_text = font.render("Restart", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                return "restart"

def draw_game_elements(screen, player, player_group, enemies, bullets, enemy_bullets, power_ups, chests, score, level, time_remaining, start_time, level_time, background):
    # Draw background every frame
    screen.blit(background, (0, 0))

    # Draw other game elements
    player_group.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)
    enemy_bullets.draw(screen)
    power_ups.draw(screen)
    chests.draw(screen)

    font = pygame.font.SysFont("segoeuiblack", 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    round_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(round_text, (160, 45))

    player_health_bar_width = int((player.health / 100) * (width / 3))
    pygame.draw.rect(screen, (255, 0, 0), (15, 20, (width / 3), 20), border_radius=10)
    pygame.draw.rect(screen, (0, 255, 0), (15, 20, player_health_bar_width, 20), border_radius=10)

    life_text = font.render(f"Life: {int(player.health)}%", True, (255, 255, 255))
    screen.blit(life_text, (25, 45))

    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, level_time - elapsed_time)
    bar_width = int((time_left / level_time) * (width - 40))

    if time_left > level_time * 0.5:
        bar_color = (0, 255, 0)
    elif time_left > level_time * 0.2:
        bar_color = (255, 165, 0)
    else:
        bar_color = (255, 0, 0)

    pygame.draw.rect(screen, (255, 255, 255), (20, height - 40, width - 40, 25), border_radius=10)
    pygame.draw.rect(screen, bar_color, (30, height - 35, bar_width, 15), border_radius=10)

    font = pygame.font.SysFont("segoeuiblack", 20)
    time_text = font.render(f"Time: {int(time_left)}s", True, (255, 255, 255))
    screen.blit(time_text, (25, height - 70))

    pygame.display.flip()


def play_level(level, spawn_rate, max_enemies, enemy_types, player):
    # In your initialization or main game loop:
    background = pygame.image.load("game_background.jpg")
    background = pygame.transform.scale(background, (width, height))

    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    chests = pygame.sprite.Group()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)
    # Round management
    current_level = 1
    level_time = 20  # seconds per round
    start_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()
    score = 0
    running = True

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause(screen, resolution[0], resolution[1])

        last_spawn_time = spawn_enemies(enemies, enemy_types, spawn_rate, max_enemies, last_spawn_time)
        power_up_spawn_timer = manage_power_ups(player, power_ups, [], screen, 0)
        score = handle_collisions(player, bullets, enemies, enemy_bullets, chests, score, power_ups)

        draw_game_elements(screen, player, pygame.sprite.Group(player), enemies, bullets, enemy_bullets, power_ups, chests, score, level, 300, start_time, level_time, background)

        if player.health <= 0:
            running = False
            return "game_over"
        if len(enemies) == 0 and len(bullets) == 0:
            return "level_complete"

def execute_game(player):
    #pygame.init()
    current_level = 1
    unlocked_levels = {1: True}

    while current_level <= len(LEVELS):
        if not unlocked_levels.get(current_level, False):
            print(f"Level {current_level} is locked.")
            break

        level_data = LEVELS[current_level]
        result = play_level(
            current_level,
            level_data["spawn_rate"],
            len(level_data.get("enemy_types", [])),
            level_data["enemy_types"],
            player
        )

        if result == "game_over":
            if show_game_over_screen(pygame.display.set_mode(resolution), resolution[0], resolution[1]) == "restart":
                current_level = 1
                player = Player()
                unlocked_levels = {1: True}
                continue
            break

        if result == "level_complete":
            unlocked_levels[current_level + 1] = True

