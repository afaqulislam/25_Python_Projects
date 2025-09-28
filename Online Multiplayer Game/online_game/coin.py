import pygame
import random


class Coin:
    def __init__(self, radius=10):
        self.radius = radius
        self.x = random.randint(50, 650)
        self.y = random.randint(50, 450)
        self.color = (255, 165, 0)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def relocate(self):
        self.x = random.randint(50, 650)
        self.y = random.randint(50, 450)

    def check_collision(self, player):
        px = player.x + player.width // 2
        py = player.y + player.height // 2
        distance = ((self.x - px) ** 2 + (self.y - py) ** 2) ** 0.5
        return distance < self.radius + player.width // 2
