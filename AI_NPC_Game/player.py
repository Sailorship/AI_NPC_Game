import pygame
import math

class Player:
    def __init__(self, x, y):
        # Player Properties
        self.width = 50
        self.height = 50
        self.color = (123, 171, 128)
        self.speed = 3     # Horizontal speed
        self.TBspeed = 2   # Vertical speed

        # Rectangle used for position and collision
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Attack range
        self.attack_range = 80

        # Check if space was pressed last frame (prevents spam)
        self.space_was_pressed = False

    # Handle keyboard-based movement
    def move(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.TBspeed
        if keys[pygame.K_s] and self.rect.bottom < 600:
            self.rect.y += self.TBspeed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < 800:
            self.rect.x += self.speed


    def attack(self, keys, npc):
        # Calculate distance to NPC
        distance = math.dist(self.rect.center, npc.rect.center)

        if keys[pygame.K_SPACE] and not self.space_was_pressed:
            if distance <= self.attack_range:
                print("Attack!")
                # Add attack logic here (damage, animation)

        # Update space key state for next frame
        self.space_was_pressed = keys[pygame.K_SPACE]

    # Draw player on screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
