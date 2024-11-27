from utils import *
from config import *
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x:int ,y:int , direction:float):
        """
        Initialize the bullet instance:
        Args
        ----
        x:int
            Positions of the bullet in the x-axis.

        y:int
            Positions of the bullet in the y-axis.

        direction:float
            Direction in which it is fired, in radians.

        """

        super().__init__()
        self.radius = bullet_size
        self.color = yellow
        self.rect = pygame.Rect(x - self.radius,
                                y - self.radius,
                                self.radius*2,
                                self.radius*2)

        self.speed = 7
        self.direction = direction

    def update(self):
        """
        Update the bullet's position and check if it ages offscreen.
        """
        #Coordinate update
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        #Check if out of bounds
        if self.rect.x<0 or self.rect.x>width or self.rect.y<0 or self.rect.y>height:
            self.kill()

    def draw(self, screen:pygame.Surface):
        """
        Draw the bullet on the screen.

        Args
        ---
        screen(pygame.Surface)
            The screen to draw the bullet
        ---
        """
        #Draw the bullet as a circle
        pygame.draw.circle(screen, self.color,self.rect.center, self.radius)