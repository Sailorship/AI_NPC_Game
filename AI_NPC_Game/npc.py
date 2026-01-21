import pygame

class NPC:
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
        self.color = (133, 29, 40)
        self.speed = 3
        self.direction = 1

        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.speed = 1
        self.direction = 1
        self.left_limit = x - 100
        self.right_limit = x + 100


    def update(self):
        # Move NPC
        self.rect.x += self.speed * self.direction

        # Change the direction at limits
        if self.rect.x >= self.right_limit:
            self.direction = -1
        elif self.rect.x <= self.left_limit:
            self.direction = 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
