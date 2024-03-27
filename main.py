import pygame as pygame
import sys
import random

# my modules
from classes import Player, Brick, Ball, ExplosiveBall, Particle, Power

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
p_rect = p_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
over_rect = over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))


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


# func that loops through list of sprites and updates them
def update_sprite_list(sl):
    if len(sl) > 0:
        for i in sl:
            i.update()


# func for drawing sprites on screen and also garbage collects sprites offscreen
def draw_sprite_list(sl, surface):
    garbage = []
    if len(sl) > 0:
        for i in sl:
            if i.rect.y < 1200:
                surface.blit(i.image, i.rect)
            else:
                garbage.append(i)
    for j in garbage:
        sl.remove(j)


# groups and surfaces

bricks = layout_bricks()
player = Player()
ball = Ball(10)
bg = pygame.Surface((1200, 800))
bg.fill("#F7EEDD")
explosive_balls = []
particles = []
powers = []

# setup

speed = 10
exploding_brick = {}
dead_bricks = []
RUNNING, PAUSE, OVER = 0, 1, 2
game_state = RUNNING


# reset vars for restart
def restart():
    player.lives = 3
    player.level = 1
    global speed
    speed = 10


while True:
    # events
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

        # LOGIC -------------------------------------------------------------------------------------------------------

        # handle no more bricks aka next level
        if len(bricks) < 1:
            if player.lives > 0:
                player.lives = 3
                player.level += 1
                win.play()
                speed += 2
            exploding_brick = {}
            explosive_balls = []
            ball.respawn(speed)
            bricks = layout_bricks()

        # handle paddle hit
        if pygame.Rect.colliderect(ball.rect, player.rect):
            ball.calc_velocity(player)
            hit.play()
        # handle power up hit
        if len(powers) > 0:
            for power in powers:
                if pygame.Rect.colliderect(power.rect, player.rect):
                    for i in range(random.randint(5, 8)):
                        explosive_balls.append(ExplosiveBall(player.rect.midtop))

        # keep track of brick collisions with ball and exploding bricks
        # handle ball physics
        for brick in bricks:
            # check for explosive ball collisions w bricks only if explosive balls are present
            if len(explosive_balls) > 0:
                for eb in explosive_balls:
                    if pygame.Rect.colliderect(eb.rect, brick.rect):
                        brick_hit.play()
                        # classifying these as non exploded, might change later
                        dead_bricks.append([brick, 0])
            # if we have an explosion position stored in dict remove all bricks that are within 200 pixels
            if "x" in exploding_brick:
                y_d = abs(brick.rect.x - exploding_brick["x"])
                x_d = abs(brick.rect.y - exploding_brick["y"])
                if y_d <= 200 and x_d < 200:
                    if random.choice([True, False, False]):
                        brick_hit.play()
                        dead_bricks.append([brick, 1])
            # check normal ball w brick collision
            if pygame.Rect.colliderect(ball.rect, brick.rect):
                brick_hit.play()
                ball.calc_velocity(brick)
                dead_bricks.append([brick, 0])
                # if brick is light blue or explosive store explosion position in dict
                if brick.explosive:
                    exploding_brick["x"] = brick.rect.x
                    exploding_brick["y"] = brick.rect.y
                # if ball hits another non-explosive brick reset dict
                else:
                    exploding_brick = {}

        # remove hit bricks or exploded bricks
        if len(dead_bricks) > 0:
            for sublist in dead_bricks:
                # unpacks the sublists in dead_bricks into the brick object and exploded status
                db = sublist[0]
                exploded = sublist[1]
                # element not present in list occasionally not sure why
                # weird bug fix below
                if db in bricks:
                    bricks.remove(db)
                    if exploded:
                        # generate fewer particles for exploded bricks
                        if random.randint(0, 10) == 1:
                            particles.append(Particle(db.rect.midbottom, ball.velocity_x))
                    else:
                        # 2% chance of power spawn from non exploded brick
                        if random.randint(0, 50) == 1:
                            powers.append(Power(db.rect.midbottom))
                        # more particles for non exploded brick
                        for i in range(random.randint(3, 5)):
                            particles.append(Particle(db.rect.midbottom, ball.velocity_x))
            dead_bricks = []

        # handle ball wall collision or fall offscreen
        if ball.rect.x < 0 or ball.rect.x > SCREEN_WIDTH - 10:
            boing.play()
            ball.velocity_x *= -1
        if ball.rect.y < 0 and ball.velocity_y < 0:
            boing.play()
            ball.velocity_y *= -1
        elif ball.rect.y > SCREEN_HEIGHT:
            player.lives -= 1
            death.play()
            ball.respawn(speed)
        # update player, ball, power, and active powers positions
        update_sprite_list(particles)
        update_sprite_list(explosive_balls)
        update_sprite_list(powers)
        player.update()
        ball.update()

        # handle player death
        if player.lives < 1:
            game_state = OVER
            exploding_brick = {}

        # drawing on screen --------------------------------------------------------------------------------------------
        screen.blit(bg, (0, 0))
        draw_sprite_list(bricks, screen)
        draw_sprite_list(particles, screen)
        draw_sprite_list(powers, screen)
        draw_sprite_list(explosive_balls, screen)
        screen.blit(ball.image, ball.rect)
        screen.blit(player.image, player.rect)
        level_text = ll_font.render(f"Level {player.level}", True, 'black')
        lives_text = ll_font.render(f"Lives {player.lives}", True, 'red')
        level_rect = level_text.get_rect(bottomleft=(10, 800))
        lives_rect = lives_text.get_rect(bottomright=(1190, 800))
        screen.blit(level_text, level_rect)
        screen.blit(lives_text, lives_rect)
        # pause and game over menu
    elif game_state == PAUSE:

        screen.blit(p_text, p_rect)
    else:
        screen.blit(over_text, over_rect)
        continue_text = ll_font.render("Click the mouse to continue..", False, 'black')
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(continue_text, continue_rect)
    pygame.display.update()
    clock.tick(60)
