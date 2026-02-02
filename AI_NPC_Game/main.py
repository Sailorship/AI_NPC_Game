import pygame
import sys
from player import Player
from npc import NPC


# Initialize all pygame modules
pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A_ Game")

# Clock to control FPS
clock = pygame.time.Clock()

# Create player and NPC objects
player = Player(WIDTH // 2, HEIGHT // 2)      # Player starts at center
npc = NPC(650,100)    # NPC starts at fixed position


running = True
while running:
    clock.tick(60)    # Run game at 60 frames per second

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keyboard input
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.attack(keys, npc)    # Player attack with distance check

    screen.fill((30, 30, 30))

    # Draw game objects
    player.draw(screen)

    # Update NPC logic (FSM + movement)
    npc.update(player)

    npc.draw(screen)

    # Update display
    pygame.display.update()

pygame.quit()
sys.exit()
