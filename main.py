import pygame as pygame
import sys
import random

# my modules
from classes import Player, Brick, Ball

# constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# init
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("break out")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# sounds
hit = pygame.mixer.Sound("./assets/sounds/hit.wav")
brick_hit = pygame.mixer.Sound("./assets/sounds/brick.wav")
boing = pygame.mixer.Sound("./assets/sounds/boing.wav")
boing.set_volume(.3)
death = pygame.mixer.Sound("./assets/sounds/death.wav")
death.set_volume(.1)
win = pygame.mixer.Sound("./assets/sounds/win.wav")

# fonts
p_font = pygame.font.Font(None, 100)
over_font = pygame.font.Font(None, 150)
ll_font = pygame.font.Font(None, 50)


# texts
p_text = p_font.render("Pause", False, "black")
over_text = over_font.render("Game Over", False, "black")

# rects
p_rect = p_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
over_rect = over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100))


# spawn bricks
def layout_bricks():
    bricks = []
    y = 12
    for i in range(15):
        brick_pos = [25, y]
        for j in range(24):
            brick = Brick((brick_pos[0], brick_pos[1]))
            bricks.append(brick)
            brick_pos[0] += 50
        y += 25
    return bricks

# groups and surfaces

bricks = layout_bricks()
player = Player()
ball = Ball(10)
bg = pygame.Surface((1200, 800))
bg.fill("#F7EEDD")

# setup

speed = 10
exploding_brick = {}
RUNNING, PAUSE, OVER = 0, 1, 2
game_state = RUNNING


def restart():
    player.lives = 3
    player.level = 1
    global speed
    speed = 10


while True:
    if clock.get_fps() < 50:
        print(clock.get_fps())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == OVER:
                game_state = RUNNING
                del bricks
                bricks = layout_bricks()
                restart()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == PAUSE:
                    game_state = RUNNING
                else:
                    game_state = PAUSE
    if game_state == RUNNING:
        if len(bricks) < 1:
            if player.lives > 0:
                player.lives = 3
                player.level += 1
                win.play()
                speed += 2
            del exploding_brick["x"]
            del exploding_brick["y"]
            ball.respawn(speed)
            bricks = layout_bricks()
        if pygame.Rect.colliderect(ball.rect, player.rect):
            ball.calc_velocity(player)
            hit.play()

        for i, brick in enumerate(bricks):
            if "x" in exploding_brick:
                y_d = abs(brick.rect.x - exploding_brick["x"])
                x_d = abs(brick.rect.y - exploding_brick["y"])
                if y_d <= 200 and x_d < 200:
                    if random.choice([True, False, False]):
                        brick_hit.play()
                        bricks.remove(brick)
            if pygame.Rect.colliderect(ball.rect, brick.rect):
                brick_hit.play()
                ball.calc_velocity(brick)
                bricks[i] = bricks.pop()
                if brick.explosive:
                    exploding_brick["x"] = brick.rect.x
                    exploding_brick["y"] = brick.rect.y
                else:
                    exploding_brick = {}

        if ball.rect.x < 0 or ball.rect.x > 1190:
            boing.play()
            ball.velocity_x *= -1
        if ball.rect.y < 0:
            boing.play()
            ball.velocity_y *= -1
        elif ball.rect.y > 1200:
            player.lives -= 1
            death.play()
            ball.respawn(speed)
        player.update()
        ball.update()
        if player.lives < 1:
            game_state = OVER
            exploding_brick = {}
        screen.blit(bg, (0, 0))
        for brick in bricks:
            screen.blit(brick.image, brick.rect)
        screen.blit(ball.image, ball.rect)
        screen.blit(player.image, player.rect)
        level_text = ll_font.render(f"Level {player.level}", True, 'black')
        lives_text = ll_font.render(f"Lives {player.lives}", True, 'red')
        level_rect = level_text.get_rect(bottomleft=(10, 800))
        lives_rect = lives_text.get_rect(bottomright=(1190, 800))
        screen.blit(level_text, level_rect)
        screen.blit(lives_text, lives_rect)
    elif game_state == PAUSE:
        screen.blit(bg, (0, 0))
        screen.blit(p_text, p_rect)
    else:
        screen.blit(over_text, over_rect)
        continue_text = ll_font.render("Click the mouse to continue..", False, 'black')
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))
        screen.blit(continue_text, continue_rect)
    pygame.display.update()
    clock.tick(60)
