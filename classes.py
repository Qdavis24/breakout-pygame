import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # attr
        self.level = 1
        self.lives = 3
        self.velocity = 0
        self.image = pygame.Surface((90, 10))
        self.image.fill("#008DDA")
        self.rect = self.image.get_rect(midbottom=(600, 780))

    def player_input(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.velocity = (mousex - self.rect.x) * .3

    def update(self):
        self.player_input()
        self.rect.x += self.velocity
        self.velocity = 0


class Brick(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.explosive = random.randint(0, 10) == 1
        self.image = pygame.Surface((50, 25))
        self.image.fill("black")
        self.rect = self.image.get_rect(center=position)
        if self.explosive:
            self.color = "#ACE2E1"
        else:
            self.color = "#41C9E2"
        inner_rect = pygame.Rect((2, 2), (48, 23))
        pygame.draw.rect(self.image, self.color, inner_rect)


class Power(pygame.sprite.Sprite):
    def __init__(self, brick_position):
        flame_colors = [
            "#FF4500",  # OrangeRed
            "#FF7F50",  # Coral
            "#FFA500",  # Orange
            "#FFD700",  # Gold
            "#FF8C00",  # DarkOrange
            "#FFA07A",  # LightSalmon
            "#CD5C5C",  # IndianRed
            "#DC143C",  # Crimson
            "#B22222",  # FireBrick
            "#8B0000",  # DarkRed
            "#FF6347",  # Tomato
            "#FF0000",  # Red
            "#FF4500",  # OrangeRed (Repeated for more frequency)
            "#FF7F50",  # Coral (Repeated for more frequency)
            "#FFA500"  # Orange (Repeated for more frequency)
        ]
        self.velocity_y = -10
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, random.choice(flame_colors), (20, 20), 19)
        self.rect = self.image.get_rect(midtop=(brick_position))

    def update(self):
        self.velocity_y += .3
        self.rect.y += self.velocity_y


class Particle(pygame.sprite.Sprite):
    def __init__(self, brick_position, ball_veloc):
        flame_colors = [
            "#41C9E2",  # Original color
            "#48C9E2",
            "#4FC9E2",
            "#56C9E2",
            "#5DC9E2",
            "#64C9E2",
            "#6BC9E2",
            "#72C9E2",
            "#79C9E2",
            "#80C9E2"
        ]
        self.velocity_y = -5
        self.velocity_x = ball_veloc * random.uniform(.5, 1.5)
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, random.choice(flame_colors), (3, 3), 3)
        self.rect = self.image.get_rect(midtop=(brick_position[0]+ random.randint(-40, 40), brick_position[1]+ random.randint(-40, 40)))

    def update(self):
        self.velocity_y += .5
        self.velocity_x *= .9999
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x


class ExplosiveBall(pygame.sprite.Sprite):
    def __init__(self, player_position):
        super().__init__()
        self.velocity_x = random.randint(-10, 10)
        self.velocity_y = -20

        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, "#007F73", (5, 5), 5)
        self.rect = self.image.get_rect(midbottom=(player_position))

    def update(self, *args, **kwargs):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y


class Ball(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # attr
        self.velocity_x = 0
        self.velocity_y = speed

        # drawing
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.rect = self.image.get_rect(midbottom=(600, 400))
        pygame.draw.circle(self.image, "black", (12, 12), 12)
        pygame.draw.circle(self.image, "yellow", (12, 12), 10)

    def respawn(self, speed):
        self.velocity_y = speed
        self.velocity_x = 0
        self.rect.midbottom = (600, 400)

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def calc_velocity(self, collision):
        offset = self.rect.centerx - collision.rect.centerx
        self.velocity_x += (offset * .1)
        self.velocity_y *= -1
