import pygame
import sys
from player import Player
from npc import NPC



pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A_ Game")

clock = pygame.time.Clock()

# Creating player in the center
player = Player(WIDTH // 2, HEIGHT // 2)
npc = NPC(300, 200)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    screen.fill((30, 30, 30))
    player.draw(screen)
    #npcs = [
        #NPC(100, 150),
        #NPC(400, 300),
        #NPC(600, 100)
    #]

    #for npc in npcs:
        #npc.draw(screen)
    npc.update()
    npc.draw(screen)

    if player.rect.colliderect(npc.rect):
        print("Collision!")


    pygame.display.update()

pygame.quit()
sys.exit()
