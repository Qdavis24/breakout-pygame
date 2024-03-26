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


class Ball(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # attr
        self.velocity_x = 0
        self.velocity_y = speed

        # drawing
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(midbottom=(600, 400))
        pygame.draw.circle(self.image, "#007F73", (10, 10), 10)

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
