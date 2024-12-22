import random
import pygame
from config import *
from game import *
from font import *
from player import *


class Chest(pygame.sprite.Sprite):
    '''
    Initialize the chest 
    '''
    def __init__(self, image_path="chest.jpeg"):
        super().__init__()
        # Load the image for the chest
        self.image = pygame.image.load(image_path).convert_alpha()

        # Scale the image to an appropriate size
        chest_size = (50, 50)  # Adjust size as needed
        self.image = pygame.transform.scale(self.image, chest_size)

        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            random.randint(0, width - chest_size[0]),
            random.randint(0, height - chest_size[1])
        )

        self.open_chest = False
        self.spawn_time = pygame.time.get_ticks()

    def spawner(self):
        '''
        swpan the chests randomly in the map
        '''
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.rect.topleft = (self.x, self.y)
        
    
    #Pergunatr se mantenho aqui ou coloco no game?
    def draw(self, screen):
        '''
        draw the chest on the screen
        '''
        screen.blit(self.image, self.rect.topleft)

    def chest_rewards(self):
        '''
        selects 3 random rewards for the player to choose from
        '''
        all_rewards = [
            {"name": "health potion","type": "instant", "value": 20, "probability": 0.5},
            {"name": "health increase","type": "permanent", "value": 20, "probability": 0.25},
            {"name": "fire rate increase","type": "instant", "value": 2, "probability": 0.5},
            {"name": "shotgun","type": "permanent", "value": 1, "probability": 0.1},
            {"name": "rifle","type": "permanent", "value": 1, "probability": 0.1},
            {"name": "RPG", "type": "permanent", "value": 1, "probability": 0.1},
            {"name": "doomsday device", "type": "instant", "value": 1, "probability": 0.05}
        ]

        #selecting 3 random, weighted and different rewards for the chests
        selected_rewards = []
        remaining_rewards = all_rewards.copy()
        for i in range(3):
            weight = [reward["probability"] for reward in remaining_rewards]
            # Select a random reward from the remaining rewards
            reward = random.choices(remaining_rewards, weights=weight, k=1)[0]
            selected_rewards.append(reward)
            remaining_rewards.remove(reward)

        return selected_rewards
    

    def open(self):
        '''
        open the chest if the player collided with it and dispawn once its oppened
        '''
        if not self.open_chest:
            self.open_chest = True
            self.kill() 
            return self.chest_rewards()
        else:
            return None
        
    
    def display_rewards_options(self, screen, selected_rewards, player, enemies):
        '''
        display the rewards randomly choosen in the chest for the player to choose one of them
        '''
        selected_reward = None
        # Create rectangles for the rewards to be displayed
        reward_rects = [
        pygame.Rect(150, 250, 300, 100), 
        pygame.Rect(500, 250, 300, 100), 
        pygame.Rect(850, 250, 300, 100)   
    ]
        # darken the backround like a shadow
        overlay = pygame.Surface((1200, 600))  # Match screen size
        overlay.set_alpha(150)  # Set transparency (0 is fully transparent, 255 is fully opaque)
        overlay.fill((0, 0, 0))  # Black color for the overlay

        # select the reward using the mouse
        while selected_reward == None:
            screen.blit(overlay, (0, 0)) # Draw the overlay

            for i, rect in enumerate(reward_rects):
                pygame.draw.rect(screen, (255, 223, 0), rect)
                reward_text = pygame.font.SysFont("segoeuiblack", 30).render(selected_rewards[i]["name"], True, (0, 0, 0))
                text_rect = reward_text.get_rect(center=rect.center)
                screen.blit(reward_text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(reward_rects):
                        if rect.collidepoint(mouse_pos):
                            selected_reward = selected_rewards[i]

                            if selected_reward["name"] == "health potion":
                                player.apply_health_potion(selected_reward["value"])
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
                            elif selected_reward["name"] == "RPG":
                                player.unlock_guns("RPG")
                            
            

        return selected_reward




    




