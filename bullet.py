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
        self.damage = 5

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
        ---
        """
        #Draw the bullet as a circle
        pygame.draw.circle(screen, self.color,self.rect.center, self.radius)

class FastBullet(Bullet):
    #Faster but smaller bullet used in the rifle
    def __init__(self, x:int, y:int, direction:float):
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
        super().__init__(x, y, direction)
        self.speed = 10
        self.color = green
        self.radius = bullet_size / 2  # Double the size of the normal

class LargeBullet(Bullet):
    #larger but slower buullet used in the shotgun
    def __init__(self, x:int, y:int, direction:float):
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
        super().__init__(x, y, direction)
        self.radius = bullet_size*1.25 #bigger than the size of the normal one
        self.color = blue
        self.speed = 5
        self.damage = 20

class RPG_rocket(Bullet):
    def __init__(self, x:int, y:int, direction:float):
        '''
        rocket that is going to be be used in the RPG, it will explode and cause damage 
        to enemies in a certain radius
        
        Args
            ----
            x:int
                Positions of the bullet in the x-axis.

            y:int
                Positions of the bullet in the y-axis.

            direction:float
                Direction in which it is fired, in radians.
        '''
        super().__init__(x, y, direction)
        self.speed = 4
        self.color = red
        self.radius = bullet_size * 2
        self.damage = 30
        self.explosion_radius = 100
        
    def explosion(self, enemies:pygame.sprite.Group):
        '''
        the explosion will cause damage to all the enemies in proximity

        Args
        ----
        enemies:pygame.sprite.Group
            The group of enemies to check for collision
        '''
        explosion_center = self.rect.center
        for enemy in enemies:
            #hypot computes the euclidian distance  in this case between the center of the explosion and the enemy
            distance = math.hypot(explosion_center[0] - enemy.rect.centerx,
                                  explosion_center[1] - enemy.rect.centery)
            if distance <= self.explosion_radius:
                enemy.health -= self.damage
                if enemy.health <= 0:
                    enemy.kill()
        self.kill()

def shoot_bullet(x,y,direction,bullet_type=1):
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
    if bullet_type==1:
        return Bullet(x,y,direction)
    elif bullet_type==2:
        return FastBullet(x,y,direction)
    elif bullet_type==3:
        return LargeBullet(x,y,direction)
    elif bullet_type == 4:
        return RPG_rocket(x, y, direction)