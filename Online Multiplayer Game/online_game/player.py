import pygame
import os


class Player:
    def __init__(self, x, y, width, height, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.name = name
        self.vel = 5
        self.score = 0
        self.collect_sound = pygame.mixer.Sound(os.path.join("assets", "collect.wav"))

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x - self.vel > 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.width < 700:
            self.x += self.vel
        if keys[pygame.K_UP] and self.y - self.vel > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y + self.vel + self.height < 500:
            self.y += self.vel

    def increase_score(self):
        self.score += 1
        self.collect_sound.play()

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
