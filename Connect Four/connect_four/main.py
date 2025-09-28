import numpy as np
import pygame
import sys
import math
import random

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Init
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four vs AI")
font = pygame.font.SysFont("monospace", 75)

# State
board = np.zeros((ROW_COUNT, COLUMN_COUNT))
turn = 0
game_over = False
player1_score = 0
ai_score = 0


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )

    # Scores
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
    score_text = f"You: {player1_score}   AI: {ai_score}"
    score_surface = font.render(score_text, True, WHITE)
    screen.blit(score_surface, (40, 10))
    pygame.display.update()


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all([board[r][c + i] == piece for i in range(4)]):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all([board[r + i][c] == piece for i in range(4)]):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all([board[r + i][c + i] == piece for i in range(4)]):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all([board[r - i][c + i] == piece for i in range(4)]):
                return True
    return False


def reset_game():
    global board, game_over, turn
    board = create_board()
    game_over = False
    turn = 0
    draw_board(board)


def get_valid_columns(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]


def ai_move():
    valid_cols = get_valid_columns(board)
    return random.choice(valid_cols) if valid_cols else None


# Start game
draw_board(board)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

        if event.type == pygame.MOUSEMOTION and not game_over and turn == 0:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == 0:
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = font.render("You win!", True, RED)
                    screen.blit(label, (40, 10))
                    player1_score += 1
                    game_over = True

                draw_board(board)
                turn = 1  # Switch to AI

    # --- AI TURN ---
    if not game_over and turn == 1:
        pygame.time.wait(1000)  # delay to simulate thinking
        col = ai_move()

        if col is not None and is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                label = font.render("AI wins!", True, YELLOW)
                screen.blit(label, (40, 10))
                ai_score += 1
                game_over = True

            draw_board(board)
            turn = 0  # back to player
