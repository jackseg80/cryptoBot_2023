import pygame
import time
import random
from pygame.locals import *
pygame.init()

# Initialize pygame
pygame.init()

# Create a window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Brick Breaker")

# Set the parameters of the ball
ball_radius = 30
ball_size = [ball_radius*2, ball_radius*2]
ball_color = (255, 255, 255)
ball_pos = [350, 250]
ball_vel = [3, 3]

ball_image = pygame.image.load("test/img/ball.png")
ball_image = pygame.transform.scale(ball_image, ball_size)

# Load the animation image
background_image = pygame.image.load("test/img/fond.png")
background_image = pygame.transform.scale(background_image, size)

# Load the sound effects
bounce_sound = pygame.mixer.Sound("test/sound/bounce.mp3")
break_sound = pygame.mixer.Sound("test/sound/break.wav")
fall_sound = pygame.mixer.Sound("test/sound/fall.wav")
music = pygame.mixer.Sound("test/sound/music.mp3")

# Set the parameters of the paddle
paddle_width = 100
paddle_height = 20
paddle_color = (255, 255, 255)
paddle_pos = [size[0]//2 - paddle_width//2, size[1] - paddle_height - 10]
paddle_speed = 10

# Set the parameters of the bricks
brick_width = 67
brick_height = 20
brick_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255,255,255)]
bricks = []
brick_spacing = 5
for i in range(15):
    for j in range(8):
        bricks.append([i*brick_width + (i+1)*brick_spacing, j*brick_height + (j+1)*brick_spacing, brick_width, brick_height, random.choice(brick_colors)])

# Initialize the score
score = 0
font = pygame.font.Font(None, 30)
score_text = font.render("Score : {}".format(score), True, (255, 255, 255))
score_bg = pygame.Surface((score_text.get_width(), score_text.get_height()))
score_bg = score_bg.convert_alpha()
score_bg.fill((0, 0, 0, 128))
        
# Initialize the game status
game_over = False

# Set the parameters of the game loop
clock = pygame.time.Clock()
done = False
time_since_last_bounce = 0
time_since_last_speedup = 0
time_since_speedup_message = 0
music.play()

while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_pos[0] -= paddle_speed
            if event.key == pygame.K_RIGHT:
                paddle_pos[0] += paddle_speed
    paddle_pos[0] = max(paddle_pos[0], 0)
    paddle_pos[0] = min(paddle_pos[0], size[0]-paddle_width)
    # Handle mouse movement
    if pygame.mouse.get_focused():
        paddle_pos[0] = max(min(pygame.mouse.get_pos()[0] - paddle_width / 2, size[0] - paddle_width), 0)
    
    # Update the position of the ball
    if not game_over:
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        if ball_pos[1] > size[1]:
            fall_sound.play()
            music.stop()
            game_over = True
    else:
        font = pygame.font.Font(None, 70)
        game_over_text = font.render("Game Over !", True, (255, 255, 255))
        screen.blit(game_over_text, (size[0]//2-150, size[1]//2))
        pygame.display.flip()

    # Handle the collision with the walls
    if ball_pos[0] <= ball_radius or ball_pos[0] >= size[0] - ball_radius:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] <= ball_radius:
        ball_vel[1] = -ball_vel[1]
    if (ball_pos[1] >= paddle_pos[1] and ball_pos[0]>=paddle_pos[0] and ball_pos[0]<=paddle_pos[0]+paddle_width):
        ball_vel[1] = -ball_vel[1]
        bounce_sound.play()
        ball_size = [60, 30]  # make the ball bigger
        time_since_last_bounce = 0  # reset the time since last bounce
        
    # Score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_bg, (10, 10))
    screen.blit(score_text, (10, 10))

    # Handle the collision with the bricks
    for brick in bricks:
        if (ball_pos[0] >= brick[0] and ball_pos[0] <= brick[0] + brick[2]) and (ball_pos[1] >= brick[1] and ball_pos[1] <= brick[1] + brick[3]):
            ball_vel[1] = -ball_vel[1]
            break_sound.play()
            bricks.remove(brick)
            score += 1

    # Clear the screen
    screen.fill((0, 0, 0))
    screen.blit(background_image,(0,0))
    
    # Update the time since last speedup
    time_since_last_speedup += clock.get_time()  # add the time passed since last frame
    if time_since_last_speedup >= 10000:  # if it's been more than 10 seconds since last speedup
        ball_vel = [ball_vel[0]*1.2, ball_vel[1]*1.2]  # increase the speed of the ball
        time_since_last_speedup = 0  # reset the time since last speedup
        time_since_speedup_message = pygame.time.get_ticks()  # record the time of the speedup message
    
    # Draw the speedup message
    if time_since_speedup_message > 0:
        font = pygame.font.Font(None, 50)
        text_image = font.render("Speed up!", True, (255, 0, 0))
        screen.blit(text_image, (size[0]/2 - text_image.get_width()/2, size[1]/2 - text_image.get_height()/2))
        if pygame.time.get_ticks() - time_since_speedup_message > 2000:  # if 2 seconds have passed since the speedup message
            time_since_speedup_message = 0  # reset the time since the speedup message
    
    # Draw the paddle
    pygame.draw.rect(screen, paddle_color, pygame.Rect(paddle_pos[0], paddle_pos[1], paddle_width, paddle_height))

    # Draw the bricks
    for brick in bricks:
        shadow_image = pygame.Surface((brick[2], brick[3]))
        shadow_image.set_alpha(128)
        shadow_image.fill((0, 0, 0))
        screen.blit(shadow_image, (brick[0]+5, brick[1]+5))      
        pygame.draw.rect(screen, brick[4], (brick[0], brick[1], brick[2], brick[3]))
        #pygame.draw.rect(screen, (0, 0, 0), (brick[0]+3, brick[1]+3, brick[2], brick[3]), 3)

    # Update the size of the ball
    time_since_last_bounce += clock.get_time()  # add the time passed since last frame
    if time_since_last_bounce >= 150:  # if it's been more than 500ms since last bounce
        ball_size = [60, 60]  # make the ball smaller again
    ball_image = pygame.transform.scale(ball_image, ball_size)
    
    # Draw the ball
    #pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    screen.blit(ball_image, (ball_pos[0] - ball_radius, ball_pos[1] - ball_radius))
    
    screen.blit(score_bg, (10, 10))
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(90)

# Quit pygame
pygame.quit()
