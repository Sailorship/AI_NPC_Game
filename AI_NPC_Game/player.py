import pygame

class Player:
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
        self.color = (123, 171, 128)
        self.speed = 3

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < 600:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < 800:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
