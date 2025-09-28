import pygame
import time
from network import Network
from player import Player
from coin import Coin
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 700, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game")


def draw_text_input(win, text):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 40)
    prompt = font.render("Enter your name:", True, (0, 0, 0))
    input_text = font.render(text, True, (0, 0, 255))
    win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 150))
    win.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, 220))
    pygame.display.update()


def get_player_name():
    run = True
    name = ""
    while run:
        draw_text_input(win, name)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    run = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode
    return name


def redraw_window(win, players, score, timer, coin):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 24)

    coin.draw(win)

    for pid, player in players.items():
        player.draw(win)
        label = font.render(f"{player.name}: {player.score}", True, (0, 0, 0))
        win.blit(label, (player.x, player.y - 30))

    score_text = font.render(f"Your Score: {score}", True, (0, 0, 0))
    timer_text = font.render(f"Time Left: {max(0, int(timer))}s", True, (255, 0, 0))
    win.blit(score_text, (10, 10))
    win.blit(timer_text, (WIDTH - 180, 10))
    pygame.display.update()


def show_result(win, players):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsans", 32)
    title = font.render("🏁 Final Scores", True, (255, 255, 255))
    win.blit(title, (win.get_width() // 2 - title.get_width() // 2, 40))

    sorted_scores = sorted(players.items(), key=lambda p: p[1].score, reverse=True)
    y_offset = 100
    for pid, player in sorted_scores:
        score_text = font.render(f"{player.name}: {player.score}", True, player.color)
        win.blit(
            score_text, (win.get_width() // 2 - score_text.get_width() // 2, y_offset)
        )
        y_offset += 40

    restart_text = font.render(
        "Press 'R' to Play Again or 'ESC' to Quit", True, (255, 255, 255)
    )
    win.blit(
        restart_text,
        (win.get_width() // 2 - restart_text.get_width() // 2, y_offset + 20),
    )
    pygame.display.update()


def main():
    player_name = get_player_name()
    clock = pygame.time.Clock()
    net = Network(player_name)

    if net.data is None:
        print("❌ Could not connect to server.")
        return

    players = {}
    my_id = net.id

    for pid, pdata in net.data.items():
        players[pid] = Player(
            pdata["x"], pdata["y"], 50, 50, pdata["color"], pdata["name"]
        )

    def reset_game():
        for pid, pdata in net.data.items():
            players[pid].reset(pdata["x"], pdata["y"])
        return Coin(), time.time()

    coin, start_time = reset_game()
    total_time = 60
    run = True
    game_over = False

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        remaining_time = total_time - elapsed_time

        if remaining_time <= 0:
            show_result(win, players)
            game_over = True

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        coin, start_time = reset_game()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        run = False
            continue

        players[my_id].move()

        if coin.check_collision(players[my_id]):
            players[my_id].increase_score()
            coin.relocate()

        send_data = {
            "x": players[my_id].x,
            "y": players[my_id].y,
            "name": players[my_id].name,
            "score": players[my_id].score,
        }

        received_data = net.send(send_data)

        for pid, pdata in received_data.items():
            if pid not in players:
                players[pid] = Player(
                    pdata["x"], pdata["y"], 50, 50, pdata["color"], pdata["name"]
                )
            else:
                players[pid].x = pdata["x"]
                players[pid].y = pdata["y"]
                players[pid].name = pdata["name"]
                players[pid].score = pdata.get("score", 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window(win, players, players[my_id].score, remaining_time, coin)

    pygame.quit()


if __name__ == "__main__":
    main()
