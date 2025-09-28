# Importing the library
import pygame
import sys
import random
import time

# Initialising pygame
pygame.init()

# Frames per second controller
c = pygame.time.Clock()

# Game window dimensions
width = 900
height = 600

# Creating game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong Game")

# Game objects
ball = pygame.Rect(width / 2 - 15, height / 2 - 15, 30, 30)
player1 = pygame.Rect(width - 20, height / 2 - 70, 10, 140)
player2 = pygame.Rect(10, height / 2 - 70, 10, 140)

# Game variables
ball_speedx = 6 * random.choice((1, -1))
ball_speedy = 6 * random.choice((1, -1))
player1_speed = 0
player2_speed = 6
player1_score = 0
player2_score = 0

# Timer variables
start_time = time.time()
game_duration = 60  # seconds

# Font
font = pygame.font.SysFont("calibri", 25)


def ball_movement():
    global ball_speedx, ball_speedy, player1_score, player2_score
    ball.x += ball_speedx
    ball.y += ball_speedy

    if ball.top <= 0 or ball.bottom >= height:
        ball_speedy *= -1
    if ball.left <= 0:
        player1_score += 1
        ball_restart()
    if ball.right >= width:
        player2_score += 1
        ball_restart()

    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speedx *= -1


def player1_movement():
    global player1_speed
    player1.y += player1_speed
    if player1.top <= 0:
        player1.top = 0
    if player1.bottom >= height:
        player1.bottom = height


def player2_movement():
    global player2_speed
    if player2.top < ball.y:
        player2.top += player2_speed
    if player2.bottom > ball.y:
        player2.bottom -= player2_speed
    if player2.top <= 0:
        player2.top = 0
    if player2.bottom >= height:
        player2.bottom = height


def ball_restart():
    global ball_speedx, ball_speedy
    ball.center = (width / 2, height / 2)
    ball_speedx *= random.choice((1, -1))
    ball_speedy *= random.choice((1, -1))


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player1_speed += 8
            if event.key == pygame.K_UP:
                player1_speed -= 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player1_speed -= 8
            if event.key == pygame.K_UP:
                player1_speed += 8

    # Game mechanics
    ball_movement()
    player1_movement()
    player2_movement()

    # Timer logic
    elapsed_time = time.time() - start_time
    time_left = max(0, int(game_duration - elapsed_time))

    # Visuals
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (220, 220, 220), player1)
    pygame.draw.rect(screen, (220, 220, 220), player2)
    pygame.draw.ellipse(screen, (220, 220, 220), ball)
    pygame.draw.aaline(screen, (220, 220, 220), (width / 2, 0), (width / 2, height))

    # Scores
    player1_text = font.render("Score: " + str(player1_score), False, (255, 255, 255))
    screen.blit(player1_text, [600, 50])
    player2_text = font.render("Score: " + str(player2_score), False, (255, 255, 255))
    screen.blit(player2_text, [300, 50])

    # Timer display
    timer_text = font.render("Time Left: " + str(time_left), True, (255, 255, 0))
    screen.blit(timer_text, [width // 2 - 70, 10])

    # End game if time is up
    if time_left <= 0:
        winner = (
            "Player 1"
            if player1_score > player2_score
            else "Player 2" if player2_score > player1_score else "No one"
        )
        game_over_text = font.render(f"Time's up! Winner: {winner}", True, (255, 0, 0))
        screen.blit(game_over_text, [width // 2 - 150, height // 2])
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit()

    # Update screen
    pygame.display.update()
    c.tick(60)
