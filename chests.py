import random
import pygame
from config import *
from game import *
from font import *


class Chest(pygame.sprite.Sprite):
    '''
    Initialize the chest 
    '''
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, width - 50)
        self.y = random.randint(0, height - 50)
        self.open_chest = False
        self.image = pygame.Surface((50, 50))
        self.image.fill(glowing_yellow)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

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
            {"name": "damage potion","type": "instant", "value": 10, "probability": 0.5},
            {"name": "speed potion","type": "instant", "value": 5, "probability": 0.5},
            {"name": "shield potion","type": "instant", "value": 10, "probability": 0.5},
            {"name": "health increase","type": "permanent", "value": 20, "probability": 0.25},
            {"name": "damage increase","type": "permanent", "value": 10, "probability": 0.25},
            {"name": "speed increase","type": "permanent", "value": 5, "probability": 0.25},
            {"name": "fire rate increase","type": "instant", "value": 2, "probability": 0.5},
            {"name": "shotgun","type": "permanent", "value": 1, "probability": 0.15},
            {"name": "rifle","type": "permanent", "value": 1, "probability": 0.15},
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
        open the chest if the player collided with it
        '''
        if not self.open_chest:
            self.open_chest = True
            return self.chest_rewards()
        else:
            return None
        
    
    def display_rewards_options(self, screen, selected_rewards):
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
            

        return selected_reward




    




