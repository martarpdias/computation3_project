from utils import *
from config import *
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, direction:float):
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
        super().__init__()  # Corrected to __init__ to call the Sprite constructor
        self.radius = bullet_size
        self.color = dark_red
        self.rect = pygame.Rect(x - self.radius,
                                y - self.radius,
                                self.radius * 2,
                                self.radius * 2)

        self.speed = 7
        self.direction = direction

    def update(self):
        """
        Update the bullet's position and check if it ages offscreen.
        """
        # Coordinate update
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # Check if out of bounds
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

    def draw(self, screen: pygame.Surface):
        """
        Draw the bullet on the screen.

        Args
        ---
        screen(pygame.Surface)
            The screen to draw the bullet
        """
        # Draw the bullet as a circle
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


class FastBullet(Bullet):
    # FASTER BUT SMALLER BULLET
    def __init__(self, x: int, y: int, direction: float):
        """
        Initialize the fast bullet instance:
        Args
        ----
        x:int
            Positions of the bullet in the x-axis.

        y:int
            Positions of the bullet in the y-axis.

        direction:float
            Direction in which it is fired, in radians.
        """
        super().__init__(x, y, direction)  # Corrected to __init__ to call the parent class constructor
        self.speed = 10
        self.color = green
        self.radius = bullet_size / 2  # Half the size of the normal bullet


class LargeBullet(Bullet):
    # LARGER BUT SLOWER BULLET
    def __init__(self, x: int, y: int, direction: float):
        """
        Initialize the large bullet instance:
        Args
        ----
        x:int
            Positions of the bullet in the x-axis.

        y:int
            Positions of the bullet in the y-axis.

        direction:float
            Direction in which it is fired, in radians.
        """
        super().__init__(x, y, direction)  # Corrected to __init__ to call the parent class constructor
        self.radius = bullet_size * 1.5  # Bigger than the normal bullet size
        self.color = blue
        self.speed = 5


def shoot_bullet(x, y, direction, bullet_type=1):
    """
    Shoots the bullet you decided to shoot.
    Args
    ---
    x:int
        Positions of the bullet in the x-axis.
    y:int
        Positions of the bullet in the y-axis.
    direction:float
        Direction in which it is fired, in radians.
    bullet_type:int
        The type of bullet to shoot. (1:normal,2:fast and smaller,3:larger and slower)
    """
    if bullet_type == 1:
        return Bullet(x, y, direction)
    elif bullet_type == 2:
        return FastBullet(x, y, direction)
    elif bullet_type == 3:
        return LargeBullet(x, y, direction)
    else:
        raise ValueError("Invalid bullet type")
